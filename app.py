import io
import time
from PIL import Image

import streamlit as st
import pandas as pd
from streamlit.components.v1 import html as components_html

from core.models import SystemState
from simulation.scenarios import (
    safe_scenario,
    deadlock_scenario,
    partial_deadlock_scenario
)
from simulation.controller import SimulationController
from utils.graph_utils import (
    draw_rag,
    build_interactive_rag,
    generate_animation_steps
)
from utils.helpers import parse_vector, parse_matrix, validate_state_inputs

st.set_page_config(page_title="Deadlock Prevention Toolkit", layout="wide")


def render_matplotlib_figure(fig, target=None):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    image = Image.open(buf)
    if target is None:
        st.image(image, width="stretch")
    else:
        target.image(image, width="stretch")
    fig.clf()


if "controller" not in st.session_state:
    st.session_state.controller = SimulationController(safe_scenario())

if "anim_steps" not in st.session_state:
    st.session_state.anim_steps = []
    st.session_state.anim_index = 0
    st.session_state.anim_playing = False

controller = st.session_state.controller
state = controller.state

st.title("Deadlock Prevention and Recovery Toolkit")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Scenarios")

    if st.button("Load Safe Scenario"):
        st.session_state.controller = SimulationController(safe_scenario())
        st.session_state.anim_steps = []
        st.session_state.anim_index = 0
        st.session_state.anim_playing = False
        st.rerun()

    if st.button("Load Deadlock Scenario"):
        st.session_state.controller = SimulationController(deadlock_scenario())
        st.session_state.anim_steps = []
        st.session_state.anim_index = 0
        st.session_state.anim_playing = False
        st.rerun()

    if st.button("Load Partial Deadlock Scenario"):
        st.session_state.controller = SimulationController(partial_deadlock_scenario())
        st.session_state.anim_steps = []
        st.session_state.anim_index = 0
        st.session_state.anim_playing = False
        st.rerun()

    st.markdown("---")

    if st.button("Reset to Safe Scenario"):
        st.session_state.controller = SimulationController(safe_scenario())
        st.session_state.anim_steps = []
        st.session_state.anim_index = 0
        st.session_state.anim_playing = False
        st.rerun()

    st.subheader("Actions")

    if st.button("Check Safety"):
        safe, seq = controller.check_safety()
        if safe:
            st.success(f"SAFE state. Sequence: {seq}")
        else:
            st.warning("System is UNSAFE.")

    if st.button("Detect Deadlock"):
        deadlock, processes = controller.detect()
        if deadlock:
            st.error(f"Deadlock detected among processes: {processes}")
        else:
            st.success("No deadlock detected.")

    if st.button("Recover"):
        msg = controller.recover()
        st.info(msg)
        st.session_state.anim_steps = []
        st.session_state.anim_index = 0
        st.session_state.anim_playing = False
        st.rerun()

    st.markdown("---")
    st.subheader("Simulate Request")

    pid = st.number_input(
        "Process ID",
        min_value=0,
        max_value=max(0, state.num_processes - 1),
        step=1
    )

    default_request = ",".join(["0"] * state.num_resources)
    request_text = st.text_input("Request Vector", value=default_request)

    if st.button("Submit Request"):
        try:
            request = parse_vector(request_text)

            if len(request) != state.num_resources:
                st.error(f"Request must have exactly {state.num_resources} values.")
            else:
                success, msg = controller.make_request(pid, request)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
                st.session_state.anim_steps = []
                st.session_state.anim_index = 0
                st.session_state.anim_playing = False
                st.rerun()
        except Exception as e:
            st.error(f"Invalid request input: {e}")

with col2:
    st.subheader("System State")

    st.write("### Available")
    st.dataframe(
        pd.DataFrame(
            [state.available],
            columns=[f"R{i}" for i in range(state.num_resources)]
        ),
        width="stretch"
    )

    st.write("### Allocation")
    st.dataframe(
        pd.DataFrame(
            state.allocation,
            index=[f"P{i}" for i in range(state.num_processes)],
            columns=[f"R{i}" for i in range(state.num_resources)]
        ),
        width="stretch"
    )

    st.write("### Max")
    st.dataframe(
        pd.DataFrame(
            state.max_matrix,
            index=[f"P{i}" for i in range(state.num_processes)],
            columns=[f"R{i}" for i in range(state.num_resources)]
        ),
        width="stretch"
    )

    st.write("### Need")
    st.dataframe(
        pd.DataFrame(
            state.need,
            index=[f"P{i}" for i in range(state.num_processes)],
            columns=[f"R{i}" for i in range(state.num_resources)]
        ),
        width="stretch"
    )

    st.write("### Request Matrix")
    st.dataframe(
        pd.DataFrame(
            state.request_matrix,
            index=[f"P{i}" for i in range(state.num_processes)],
            columns=[f"R{i}" for i in range(state.num_resources)]
        ),
        width="stretch"
    )

st.markdown("---")
st.subheader("Custom System Input")

with st.expander("Create Custom Scenario"):
    available_text = st.text_input("Available Vector", value="3,3,2")
    max_text = st.text_area(
        "Max Matrix (one row per line)",
        value="7,5,3\n3,2,2\n9,0,2"
    )
    allocation_text = st.text_area(
        "Allocation Matrix (one row per line)",
        value="0,1,0\n2,0,0\n3,0,2"
    )
    request_matrix_text = st.text_area(
        "Request Matrix (one row per line)",
        value="0,0,0\n0,0,0\n0,0,0"
    )

    if st.button("Load Custom Scenario"):
        try:
            available = parse_vector(available_text)
            max_matrix = parse_matrix(max_text)
            allocation = parse_matrix(allocation_text)
            request_matrix = parse_matrix(request_matrix_text)

            validate_state_inputs(available, max_matrix, allocation, request_matrix)

            new_state = SystemState(
                available=available,
                max_matrix=max_matrix,
                allocation=allocation,
                request_matrix=request_matrix
            )

            st.session_state.controller = SimulationController(new_state)
            st.session_state.anim_steps = []
            st.session_state.anim_index = 0
            st.session_state.anim_playing = False
            st.success("Custom scenario loaded successfully.")
            st.rerun()

        except Exception as e:
            st.error(f"Invalid custom input: {e}")

st.subheader("Quick Status")

safe, seq, deadlock, processes = controller.get_status()

if deadlock:
    st.error(f"Current status: DEADLOCK among {processes}")
elif safe:
    st.success(f"Current status: SAFE | Sequence: {seq}")
else:
    st.warning("Current status: UNSAFE but not deadlocked")

st.markdown("""
**Legend**
- Blue circle = normal process
- Red circle = deadlocked process
- Green square = resource
- Green arrow = allocation edge
- Blue dashed arrow = request edge
- Red arrow = cycle/deadlock edge
- Gold highlight = current animation step
""")

st.subheader("Graph View")
graph_mode = st.radio(
    "Choose Graph Type",
    ["Static Graph", "Interactive Graph"],
    horizontal=True
)

if graph_mode == "Static Graph":
    fig = draw_rag(state, deadlocked_processes=processes if deadlock else [])
    render_matplotlib_figure(fig)
else:
    graph_html = build_interactive_rag(
        state,
        deadlocked_processes=processes if deadlock else []
    )
    components_html(graph_html, height=650, scrolling=True)

st.caption("Graph updates after every action in real time.")

st.subheader("Step-by-Step Animation Controller")
st.caption("Use controls to step through resource allocation and deadlock formation.")

if not st.session_state.anim_steps:
    st.session_state.anim_steps = generate_animation_steps(
        state,
        deadlocked_processes=processes if deadlock else []
    )
    st.session_state.anim_index = 0

steps = st.session_state.anim_steps

colA, colB, colC, colD, colE = st.columns(5)

with colA:
    if st.button("▶️ Play"):
        st.session_state.anim_playing = True

with colB:
    if st.button("⏸ Pause"):
        st.session_state.anim_playing = False

with colC:
    if st.button("⏮ Prev"):
        if st.session_state.anim_index > 0:
            st.session_state.anim_index -= 1

with colD:
    if st.button("⏭ Next"):
        if st.session_state.anim_index < len(steps) - 1:
            st.session_state.anim_index += 1

with colE:
    if st.button("🔄 Reset Animation"):
        st.session_state.anim_index = 0
        st.session_state.anim_playing = False

current_step = steps[st.session_state.anim_index]

st.info(
    f"Step {st.session_state.anim_index + 1} / {len(steps)}: "
    f"{current_step['title']}"
)

if graph_mode != "Static Graph":
    st.warning("Switch to Static Graph mode to view step-by-step animation.")
else:
    anim_placeholder = st.empty()
    fig = draw_rag(
        state,
        deadlocked_processes=processes if deadlock else [],
        highlighted_edges=current_step["highlighted_edges"],
        highlighted_nodes=current_step["highlighted_nodes"]
    )
    render_matplotlib_figure(fig, target=anim_placeholder)

if st.session_state.anim_playing and graph_mode == "Static Graph":
    time.sleep(3.0)   #1.0
    if st.session_state.anim_index < len(steps) - 1:
        st.session_state.anim_index += 1
        st.rerun()
    else:
        st.session_state.anim_playing = False

st.subheader("Logs")
if controller.logs:
    for log in reversed(controller.logs):
        st.write("-", log)
else:
    st.write("No logs yet.")
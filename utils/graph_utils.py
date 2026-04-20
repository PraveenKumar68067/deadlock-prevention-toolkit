#draw directed edges with clear arowheads for allocation,request, and cycle visualization
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import tempfile
import os


def build_rag(state):
    G = nx.DiGraph()

    # Process nodes
    for i in range(state.num_processes):
        G.add_node(f"P{i}", node_type="process")

    # Resource nodes
    for j in range(state.num_resources):
        G.add_node(f"R{j}", node_type="resource")

    # Allocation edges: Rj -> Pi
    for i in range(state.num_processes):
        for j in range(state.num_resources):
            if state.allocation[i][j] > 0:
                G.add_edge(
                    f"R{j}",
                    f"P{i}",
                    edge_type="allocation",
                    weight=int(state.allocation[i][j])
                )

    # Request edges: Pi -> Rj
    for i in range(state.num_processes):
        for j in range(state.num_resources):
            if state.request_matrix[i][j] > 0:
                G.add_edge(
                    f"P{i}",
                    f"R{j}",
                    edge_type="request",
                    weight=int(state.request_matrix[i][j])
                )

    return G


def get_cycle_edges(G):
    cycle_edges = set()
    try:
        cycles = list(nx.simple_cycles(G))
        for cycle in cycles:
            for i in range(len(cycle)):
                u = cycle[i]
                v = cycle[(i + 1) % len(cycle)]
                cycle_edges.add((u, v))
    except Exception:
        pass
    return cycle_edges


def draw_rag(
    state,
    deadlocked_processes=None,
    highlighted_edges=None,
    highlighted_nodes=None
):
    G = build_rag(state)
    fig, ax = plt.subplots(figsize=(11, 7))
    pos = nx.spring_layout(G, seed=42)

    deadlocked_processes = deadlocked_processes or []
    highlighted_edges = set(highlighted_edges or [])
    highlighted_nodes = set(highlighted_nodes or [])
    cycle_edges = get_cycle_edges(G)

    normal_process_nodes = []
    dead_process_nodes = []
    resource_nodes = []
    extra_highlight_nodes = []

    for node, data in G.nodes(data=True):
        if node in highlighted_nodes:
            extra_highlight_nodes.append(node)
        elif data["node_type"] == "process":
            pid = int(node[1:])
            if pid in deadlocked_processes:
                dead_process_nodes.append(node)
            else:
                normal_process_nodes.append(node)
        else:
            resource_nodes.append(node)

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=normal_process_nodes,
        node_shape="o",
        node_size=2200,
        node_color="lightblue",
        edgecolors="black",
        linewidths=1.5,
        ax=ax
    )

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=dead_process_nodes,
        node_shape="o",
        node_size=2400,
        node_color="tomato",
        edgecolors="black",
        linewidths=2,
        ax=ax
    )

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=resource_nodes,
        node_shape="s",
        node_size=2200,
        node_color="lightgreen",
        edgecolors="black",
        linewidths=1.5,
        ax=ax
    )

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=extra_highlight_nodes,
        node_size=2600,
        node_color="gold",
        edgecolors="black",
        linewidths=2.5,
        ax=ax
    )

    nx.draw_networkx_labels(
        G, pos,
        font_size=11,
        font_weight="bold",
        ax=ax
    )

    normal_allocation_edges = []
    normal_request_edges = []
    normal_cycle_edges = []
    animated_edges = []

    for u, v, data in G.edges(data=True):
        if (u, v) in highlighted_edges:
            animated_edges.append((u, v))
        elif (u, v) in cycle_edges:
            normal_cycle_edges.append((u, v))
        elif data["edge_type"] == "allocation":
            normal_allocation_edges.append((u, v))
        else:
            normal_request_edges.append((u, v))

    # Make arrowheads clearly visible
    plt.rcParams["patch.linewidth"] = 2

    # Allocation edges (green)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=normal_allocation_edges,
        edge_color="green",
        width=2.5,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=35,
        min_source_margin=15,
        min_target_margin=15,
        connectionstyle="arc3,rad=0.1",
        ax=ax
    )

    # Request edges (blue dashed)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=normal_request_edges,
        edge_color="blue",
        width=2.5,
        style="dashed",
        arrows=True,
        arrowstyle="-|>",
        arrowsize=35,
        min_source_margin=15,
        min_target_margin=15,
        connectionstyle="arc3,rad=0.1",
        ax=ax
    )

    # Cycle edges (red)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=normal_cycle_edges,
        edge_color="red",
        width=3.5,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=40,
        min_source_margin=20,
        min_target_margin=20,
        connectionstyle="arc3,rad=0.2",
        ax=ax
    )

    # Animated edges (gold)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=animated_edges,
        edge_color="gold",
        width=4,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=45,
        min_source_margin=20,
        min_target_margin=20,
        connectionstyle="arc3,rad=0.25",
        ax=ax
    )

    edge_labels = {
        (u, v): str(data["weight"])
        for u, v, data in G.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=10,
        ax=ax
    )

    ax.set_title("Resource Allocation Graph with deadlock visualization", fontsize=14, fontweight="bold")
    ax.axis("off")
    return fig


def generate_animation_steps(state, deadlocked_processes=None):
    G = build_rag(state)
    cycle_edges = list(get_cycle_edges(G))
    deadlocked_processes = deadlocked_processes or []

    steps = []

    steps.append({
        "title": "Initial graph",
        "highlighted_edges": [],
        "highlighted_nodes": []
    })

    for u, v, d in G.edges(data=True):
        if d["edge_type"] == "allocation":
            steps.append({
                "title": f"Allocation edge: {u} → {v}",
                "highlighted_edges": [(u, v)],
                "highlighted_nodes": [u, v]
            })

    for u, v, d in G.edges(data=True):
        if d["edge_type"] == "request":
            steps.append({
                "title": f"Request edge: {u} → {v}",
                "highlighted_edges": [(u, v)],
                "highlighted_nodes": [u, v]
            })

    if cycle_edges:
        steps.append({
            "title": "Deadlock cycle detected",
            "highlighted_edges": cycle_edges,
            "highlighted_nodes": []
        })

    if deadlocked_processes:
        steps.append({
            "title": f"Deadlocked processes highlighted: {deadlocked_processes}",
            "highlighted_edges": cycle_edges,
            "highlighted_nodes": [f"P{i}" for i in deadlocked_processes]
        })

    return steps


def build_interactive_rag(state, deadlocked_processes=None):
    G = build_rag(state)
    deadlocked_processes = deadlocked_processes or []
    cycle_edges = get_cycle_edges(G)

    net = Network(height="600px", width="100%", directed=True, notebook=False)

    for node, data in G.nodes(data=True):
        if data["node_type"] == "process":
            pid = int(node[1:])
            color = "tomato" if pid in deadlocked_processes else "lightblue"
            shape = "dot"
            title = f"Process {node}"
        else:
            color = "lightgreen"
            shape = "box"
            title = f"Resource {node}"

        net.add_node(
            node,
            label=node,
            color=color,
            shape=shape,
            title=title,
            size=25
        )

    for u, v, data in G.edges(data=True):
        if (u, v) in cycle_edges:
            color = "red"
            width = 4
        elif data["edge_type"] == "allocation":
            color = "green"
            width = 2
        else:
            color = "blue"
            width = 2

        net.add_edge(
            u,
            v,
            label=str(data["weight"]),
            color=color,
            width=width,
            arrows="to"
        )

    net.set_options("""
    var options = {
      "physics": {
        "enabled": true,
        "stabilization": {
          "enabled": true,
          "iterations": 100
        }
      },
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        },
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 1.2
          }
        },
        "font": {
          "size": 14
        }
      },
      "nodes": {
        "font": {
          "size": 18,
          "bold": true
        }
      }
    }
    """)

    temp_dir = tempfile.gettempdir()
    html_path = os.path.join(temp_dir, "rag_graph.html")
    net.save_graph(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    return html

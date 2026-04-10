from simulation.scenarios import deadlock_scenario
from utils.graph_utils import draw_rag

state = deadlock_scenario()
fig = draw_rag(state)
fig.savefig("deadlock_graph.png")
print("Graph saved as deadlock_graph.png")
import networkx as nx

def detect_deadlock(state):
    G = nx.DiGraph()

    # Process -> Resource (requests)
    for i in range(state.num_processes):
        for j in range(state.num_resources):
            if state.request_matrix[i][j] > 0:
                G.add_edge(f"P{i}", f"R{j}")

    # Resource -> Process (allocations)
    for i in range(state.num_processes):
        for j in range(state.num_resources):
            if state.allocation[i][j] > 0:
                G.add_edge(f"R{j}", f"P{i}")

    cycles = list(nx.simple_cycles(G))
    if cycles:
        deadlocked_processes = set()
        for cycle in cycles:
            for node in cycle:
                if node.startswith("P"):
                    deadlocked_processes.add(int(node[1:]))
        return True, sorted(deadlocked_processes)

    return False, []
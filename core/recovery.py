def recover_by_termination(state, deadlocked_processes):
    if not deadlocked_processes:
        return "No deadlock to recover from."

    # Choose victim: process holding maximum resources
    victim = max(
        deadlocked_processes,
        key=lambda pid: state.allocation[pid].sum()
    )

    released_resources = state.allocation[victim].copy()

    # Release resources
    state.available += released_resources
    state.allocation[victim] = 0
    state.request_matrix[victim] = 0

    return f"Terminated P{victim}, released resources {released_resources.tolist()}"


def recover_all(state, deadlocked_processes):
    if not deadlocked_processes:
        return "No deadlock to recover from."

    for pid in deadlocked_processes:
        state.available += state.allocation[pid]
        state.allocation[pid] = 0
        state.request_matrix[pid] = 0

    return f"Terminated all deadlocked processes: {deadlocked_processes}"
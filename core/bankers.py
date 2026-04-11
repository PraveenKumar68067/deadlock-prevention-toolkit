#Implementation of Banker's Algorithm
#Used to check safe state and avoid deadlock
import numpy as np

def is_safe_state(available, allocation, need):
    work = available.copy()
    finish = [False] * len(allocation)
    safe_sequence = []

    changed = True
    while changed:
        changed = False
        for i in range(len(allocation)):
            if not finish[i] and np.all(need[i] <= work):
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(i)
                changed = True

    return all(finish), safe_sequence


def request_resources(state, process_id, request):
    request = np.array(request, dtype=int)
    #check if request is within process need
    if np.any(request > state.need[process_id]):
        return False, "Error: request exceeds process maximum need."
    # check if resources are available
    if np.any(request > state.available):
        return False, "Resources not available right now."

    new_available = state.available - request
    new_allocation = state.allocation.copy()
    new_allocation[process_id] += request
    new_need = state.max_matrix - new_allocation

    safe, sequence = is_safe_state(new_available, new_allocation, new_need)

    if safe:
        state.available = new_available
        state.allocation = new_allocation
        state.request_matrix[process_id] = 0
        return True, f"Request granted. Safe sequence: {sequence}"
    else:
        return False, "Request denied: system would enter unsafe state."

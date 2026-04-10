import numpy as np
from core.models import SystemState
from core.bankers import is_safe_state, request_resources

state = SystemState(
    available=np.array([3, 3, 2]),
    max_matrix=np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]),
    allocation=np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
)

safe, seq = is_safe_state(state.available, state.allocation, state.need)
print("Is safe state?", safe)
print("Safe sequence:", seq)

print("\n--- Testing request ---")
success, msg = request_resources(state, 1, [1, 0, 2])
print(success, msg)

print("\nUpdated Available:", state.available)
print("Updated Allocation:\n", state.allocation)
print("Updated Need:\n", state.need)


print("\n--- Testing invalid request (exceeds need) ---")
success, msg = request_resources(state, 1, [10, 0, 0])
print(success, msg)


print("\n--- Testing invalid request (not available) ---")
success, msg = request_resources(state, 0, [10, 10, 10])
print(success, msg)
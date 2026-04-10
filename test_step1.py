import numpy as np
from core.models import SystemState

state = SystemState(
    available=np.array([3, 3, 2]),
    max_matrix=np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2]
    ]),
    allocation=np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2]
    ])
)

print("Available:", state.available)
print("\nAllocation:\n", state.allocation)
print("\nMax:\n", state.max_matrix)
print("\nNeed:\n", state.need)
print("\nProcesses:", state.num_processes)
print("Resources:", state.num_resources)
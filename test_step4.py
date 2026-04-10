import numpy as np
from core.models import SystemState
from core.detection import detect_deadlock
from core.recovery import recover_by_termination

state = SystemState(
    available=np.array([0, 0]),
    max_matrix=np.array([
        [1, 1],
        [1, 1]
    ]),
    allocation=np.array([
        [1, 0],
        [0, 1]
    ]),
    request_matrix=np.array([
        [0, 1],
        [1, 0]
    ])
)

print("Initial Available:", state.available)
print("Initial Allocation:\n", state.allocation)

deadlock, processes = detect_deadlock(
    state.available,
    state.allocation,
    state.request_matrix
)

print("\nDeadlock detected?", deadlock)
print("Deadlocked processes:", processes)

if deadlock:
    msg = recover_by_termination(state, processes)
    print("\nRecovery Action:", msg)

print("\nAfter Recovery Available:", state.available)
print("After Recovery Allocation:\n", state.allocation)

deadlock, processes = detect_deadlock(
    state.available,
    state.allocation,
    state.request_matrix
)

print("\nDeadlock after recovery?", deadlock)
print("Remaining deadlocked processes:", processes)
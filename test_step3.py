# Test case for verifying deadlock detection in no-deadlock, full-deadlock, and partial-deadlock scenarios
import numpy as np
from core.models import SystemState
from core.detection import detect_deadlock

print("=== Test 1: No deadlock ===")
state1 = SystemState(
    available=np.array([1, 1]),
    max_matrix=np.array([
        [1, 1],
        [1, 1]
    ]),
    allocation=np.array([
        [1, 0],
        [0, 0]
    ]),
    request_matrix=np.array([
        [0, 1],
        [0, 0]
    ])
)

deadlock, processes = detect_deadlock(
    state1.available,
    state1.allocation,
    state1.request_matrix
)

print("Deadlock?", deadlock)
print("Processes:", processes)


print("\n=== Test 2: Deadlock exists ===")
state2 = SystemState(
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

deadlock, processes = detect_deadlock(
    state2.available,
    state2.allocation,
    state2.request_matrix
)

print("Deadlock?", deadlock)
print("Processes:", processes)


print("\n=== Test 3: Partial deadlock ===")
state3 = SystemState(
    available=np.array([0, 0, 1]),
    max_matrix=np.array([
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1]
    ]),
    allocation=np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]),
    request_matrix=np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
)

deadlock, processes = detect_deadlock(
    state3.available,
    state3.allocation,
    state3.request_matrix
)

print("Deadlock?", deadlock)
print("Processes:", processes)

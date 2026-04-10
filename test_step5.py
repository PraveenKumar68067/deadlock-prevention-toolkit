import numpy as np
from core.models import SystemState
from simulation.controller import SimulationController

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

controller = SimulationController(state)

print("=== Checking safety ===")
safe, seq = controller.check_safety()
print("Safe?", safe)
print("Sequence:", seq)

print("\n=== Detecting deadlock ===")
deadlock, processes = controller.detect()
print("Deadlock?", deadlock)
print("Processes:", processes)

print("\n=== Recovering ===")
msg = controller.recover()
print(msg)

print("\n=== Final logs ===")
for log in controller.logs:
    print(log)
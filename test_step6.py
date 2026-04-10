from simulation.scenarios import (
    safe_scenario,
    deadlock_scenario,
    partial_deadlock_scenario
)
from simulation.controller import SimulationController

print("=== Safe Scenario ===")
controller1 = SimulationController(safe_scenario())
safe, seq = controller1.check_safety()
print("Safe?", safe)
print("Sequence:", seq)

print("\n=== Deadlock Scenario ===")
controller2 = SimulationController(deadlock_scenario())
deadlock, processes = controller2.detect()
print("Deadlock?", deadlock)
print("Processes:", processes)

print("\n=== Partial Deadlock Scenario ===")
controller3 = SimulationController(partial_deadlock_scenario())
deadlock, processes = controller3.detect()
print("Deadlock?", deadlock)
print("Processes:", processes)
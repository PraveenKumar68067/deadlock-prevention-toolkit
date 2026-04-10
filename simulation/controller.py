from core.bankers import request_resources, is_safe_state
from core.detection import detect_deadlock
from core.recovery import recover_by_termination

class SimulationController:
    def __init__(self, state):
        self.state = state
        self.logs = []

    def log(self, message):
        self.logs.append(message)

    def check_safety(self):
        safe, seq = is_safe_state(
            self.state.available,
            self.state.allocation,
            self.state.need
        )
        if safe:
            self.log(f"System is SAFE. Sequence: {seq}")
        else:
            self.log("System is UNSAFE.")
        return safe, seq

    def make_request(self, process_id, request):
        success, msg = request_resources(self.state, process_id, request)
        self.log(f"P{process_id} requested {request} -> {msg}")
        return success, msg

    def detect(self):
        deadlock, processes = detect_deadlock(self.state)
        if deadlock:
            self.log(f"Deadlock detected among: {processes}")
        else:
            self.log("No deadlock detected.")
        return deadlock, processes

    def recover(self):
        deadlock, processes = self.detect()
        if deadlock:
            msg = recover_by_termination(self.state, processes)
            self.log(msg)
            return msg
        return "No recovery needed."

    def get_state_snapshot(self):
        return {
            "available": self.state.available.copy(),
            "allocation": self.state.allocation.copy(),
            "max_matrix": self.state.max_matrix.copy(),
            "need": self.state.need.copy(),
            "request_matrix": self.state.request_matrix.copy()
        }

    def get_status(self):
        safe, seq = is_safe_state(
            self.state.available,
            self.state.allocation,
            self.state.need
        )

        deadlock, processes = detect_deadlock(self.state)

        return safe, seq, deadlock, processes
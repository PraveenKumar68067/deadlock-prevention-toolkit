import numpy as np
from core.models import SystemState

def safe_scenario():
    return SystemState(
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

def deadlock_scenario():
    state = SystemState(
        available=np.array([0, 0]),
        max_matrix=np.array([
            [1, 1],
            [1, 1]
        ]),
        allocation=np.array([
            [1, 0],
            [0, 1]
        ])
    )
    state.request_matrix = np.array([
        [0, 1],
        [1, 0]
    ])
    return state

def partial_deadlock_scenario():
    state = SystemState(
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
        ])
    )
    state.request_matrix = np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    return state

def complex_deadlock_scenario():
    state = SystemState(
        available=np.array([0, 1]),
        max_matrix=np.array([
            [2, 1],
            [1, 2]
        ]),
        allocation=np.array([
            [1, 0],
            [0, 1]
        ])
    )
    state.request_matrix = np.array([
        [0, 1],
        [1, 0]
    ])
    return state


def get_all_scenarios():
    return {
        "Safe Scenario": safe_scenario,
        "Deadlock Scenario": deadlock_scenario,
        "Partial Deadlock Scenario": partial_deadlock_scenario
        "Complex Deadlock Scenario": complex_deadlock_scenario
    }


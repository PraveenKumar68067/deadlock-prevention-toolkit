from dataclasses import dataclass, field
import numpy as np

@dataclass
class SystemState:
    available: np.ndarray
    max_matrix: np.ndarray
    allocation: np.ndarray
    request_matrix: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        # If request matrix not given, initialize it with zeros
        if self.request_matrix.size == 0:
            self.request_matrix = np.zeros_like(self.allocation)

    @property
    def need(self):
        return self.max_matrix - self.allocation

    @property
    def num_processes(self):
        return self.allocation.shape[0]

    @property
    def num_resources(self):
        return self.allocation.shape[1]
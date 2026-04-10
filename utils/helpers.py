import numpy as np

def parse_vector(text):
    text = text.strip()
    if not text:
        raise ValueError("Vector input is empty.")
    return np.array([int(x.strip()) for x in text.split(",")], dtype=int)

def parse_matrix(text):
    text = text.strip()
    if not text:
        raise ValueError("Matrix input is empty.")

    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            rows.append([int(x.strip()) for x in line.split(",")])

    matrix = np.array(rows, dtype=int)

    if len(matrix.shape) != 2:
        raise ValueError("Invalid matrix format.")

    return matrix

def validate_state_inputs(available, max_matrix, allocation, request_matrix):
    if max_matrix.shape != allocation.shape:
        raise ValueError("Max matrix and Allocation matrix must have the same shape.")

    if request_matrix.shape != allocation.shape:
        raise ValueError("Request matrix and Allocation matrix must have the same shape.")

    if available.shape[0] != allocation.shape[1]:
        raise ValueError("Available vector length must match number of resource types.")

    if np.any(allocation > max_matrix):
        raise ValueError("Allocation cannot exceed Max matrix.")

    if np.any(available < 0) or np.any(max_matrix < 0) or np.any(allocation < 0) or np.any(request_matrix < 0):
        raise ValueError("Negative values are not allowed.")
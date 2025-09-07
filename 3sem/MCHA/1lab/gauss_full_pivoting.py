import numpy as np
from gauss_method import check_zeros_diag


def gauss_full_method(a: np.array, b: np.array) -> np.array:
    if not check_zeros_diag(a, b):
        return None

    n = len(a)
    p = np.arange(1, n + 1)  # Initialize p vector with elements from 1 to n
    augmented_matrix = np.column_stack((a, b))

    for i in range(n):
        # Find the row and column with the maximum absolute value in the remaining submatrix
        max_value = 0
        max_row = i
        max_col = i

        for row in range(i, n):
            for col in range(i, n):
                abs_value = np.abs(augmented_matrix[row, col])
                if abs_value > max_value:
                    max_value = abs_value
                    max_row = row
                    max_col = col

        # Swap the current row and column with the row and column containing the maximum absolute value
        augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
        augmented_matrix[:, [i, max_col]] = augmented_matrix[:, [max_col, i]]
        p[[i, max_col]] = p[[max_col, i]]  # Update p vector for column swaps

        # Perform Gaussian elimination
        pivot = augmented_matrix[i, i]
        if abs(pivot) < 1e-14:
            print(f"Система несовместна.")
            return None
        augmented_matrix[i] /= pivot

        for j in range(i + 1, n):
            factor = augmented_matrix[j, i]
            augmented_matrix[j] -= factor * augmented_matrix[i]

    # Back substitution with respect to the modified order in p vector
    x = np.zeros(n)
    x[n - 1] = augmented_matrix[n - 1, n]
    for i in range(n - 2, -1, -1):
        x[i] = augmented_matrix[i, n] - np.dot(augmented_matrix[i, i + 1:n], x[i + 1:n])

    # Rearrange x vector based on p vector
    x_reordered = np.zeros(n)
    for i in range(n):
        x_reordered[p[i] - 1] = x[i]

    print("")
    return x_reordered

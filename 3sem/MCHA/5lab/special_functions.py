def is_matrix_symmetric(matrix, eps) -> bool:
    if not check_equal_dim(matrix):
        raise ValueError("Matrix isn't n, n dimension")
    for i in range(1, len(matrix)):
        for j in range(i):
            if matrix[i][j] - matrix[j][i] >= eps:
                return False
    return True


def check_equal_dim(matrix):
    if matrix.shape[0] != matrix.shape[1]:
        return False
    return True

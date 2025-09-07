import numpy as np


def check_zeros(matrix, b):
    nstr = len(matrix)
    for i in range(0, nstr):
        if matrix[i][i] == 0:
            return False
    return True


def gauss_partial_method(a: np.array, b: np.array) -> np.array:
    if not check_zeros(a, b):
        print("Система не имеет решений")
        return None
    n = a.shape[0]

    ma = np.column_stack((a, b))

    for k in range(n - 1):
        # Выбор главного элемента по столбцу
        pivot_row = np.argmax(np.abs(ma[k:, k])) + k

        # Перестановка строк
        ma[[k, pivot_row]] = ma[[pivot_row, k]]

        for j in range(k + 1, n):
            if abs(ma[k, k]) < 1e-14:
                print(f"Система несовместна.")
                return None
            m = ma[j, k] / ma[k, k]
            for i in range(k, n + 1):
                ma[j, i] = ma[j, i] - m * ma[k, i]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = ma[i, n]
        for j in range(i + 1, n):
            x[i] -= ma[i, j] * x[j]
        if abs(ma[i, i]) < 1e-14:
            print(f"Система несовместна.")
            return None
        x[i] /= ma[i, i]

    return x

import numpy as np


def swap_columns(a, i, j):
    for k in range(len(a)):
        a[k][i], a[k][j] = a[k][j], a[k][i]


def check_zeros_diag(matrix, b):
    nstr = len(matrix)
    for i in range(0, nstr):
        if matrix[i][i] == 0:
            check = True
            for j in range(0, nstr):
                if matrix[i][j] != 0 and matrix[j][i] != 0:
                    swap_columns(matrix, i, j)
                    check = False
                    break
            if check:
                if b[i] == 0:
                    print('Система имеет бесконечное количество решений')
                else:
                    print('Система не имеет решений')
                return False
    return True


def check_zeros(matrix, b):
    nstr = len(matrix)
    for i in range(0, nstr):
        if matrix[i][i] == 0:
            print("Не решаемо этим способом")
            return False
    return True


def gauss_method(a: np.array, b: np.array) -> np.array:
    if not check_zeros(a, b):
        return None

    n = a.shape[0]

    ma = np.column_stack((a, b))

    for k in range(n - 1):
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

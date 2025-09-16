import numpy as np

def inverse(matrix, x, i):
    matrix_copy = np.copy(matrix)
    matrix_copy[:, i] = x

    matrix_inverse = np.linalg.inv(matrix)
    l = matrix_inverse @ x

    if l[i] == 0:
        raise ValueError("Матрица необратима")

    l_copy = np.copy(l)
    l_copy[i] = -1
    l_vector = (-1 / l[i]) * l_copy

    Q = np.eye(2)
    Q[:, i] = l_vector

    return Q @ matrix_inverse

def main_phase(A, B, c, x):
    A_B = None
    index = min_index = 0

    while True:
        if index == 0:
            A_B = A[:, B]
            A_B_inv = np.linalg.inv(A_B)
            index += 1
        else:
            column = A[:, B[min_index]]
            A_B[:, min_index] = column
            A_B_inv = inverse(A_B, column, min_index)

        c_B = np.transpose(np.array([c[i] for i in B]))
        potentials = c_B @ A_B_inv
        grades = potentials @ A - c

        if np.all(grades >= 0):
            return x
        else:
            negatives = [(number, i) for i, number in enumerate(grades) if number < 0]
            first_negative_value, first_negative_index = negatives[0][0], negatives[0][1]

            z = A_B_inv @ A[:, first_negative_index]

            theta = np.array([x[B[i]] / z[i] if z[i] > 0 else float("inf") for i in range(len(B))])

            values = min(enumerate(theta), key=lambda i: i[1])

            min_index, min_value = values[0], values[1]

            if min_value == float("inf"):
                print("Целевой функционал задачи не ограничен сверху на множестве допустимых планов")
                break

            del_index = B[min_index]
            B[min_index] = first_negative_index

            x[first_negative_index] = min_value
            for i in range(len(z)):
                if i != min_index:
                    x[B[i]] -= min_value * z[i]
            x[del_index] = 0

def simplex_method(A, b, m, n):
    for i in range(len(b)):
        if b[i] < 0:
            b[i] *= -1
            A[i, :] *= -1

    c = np.hstack([np.zeros(n), -np.ones(m)])

    A_inv = np.hstack((A, np.eye(m)))

    x = np.hstack([np.zeros(n), b])
    B = np.array([n + i for i in range(m)])

    main_phase(A_inv, B, c, x)

    if np.any(x[n + 1:n + m + 1] != 0):
        print("Задача не совместна")
        return

    x = x[:n]

    while True:
        if np.all(B < n):
            #print(f"Базисный допустимый план: {x}, базисные индексы: {B}, вектор правых частей: {b}")
            #print(f"Матрица коэффициентов при переменных в основных ограничениях: {A.flatten()}")
            return (x, B)

        max_value = max(B)
        index = max_value - n

        j = set(range(n)) - set(B)

        replace = True

        for i in j:
            l_j = np.linalg.inv(A_inv[:, B]) @ np.array(A[:, i])

            if l_j[index] != 0:
                B[index] = j
                replace = False
                break

        if replace:
            A, A_inv = np.delete(A, index, axis=0), np.delete(A_inv, index, axis=0)
            B, b = np.delete(B, index), np.delete(b, index)
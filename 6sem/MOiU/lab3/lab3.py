import numpy as np


def solve(A, B, c, x):
    m, n = A.shape
    while True:
        # step 1
        Ab = A[:, B - 1]
        Ab_inv = np.linalg.inv(Ab)
        # step 2
        cb = c[B - 1]
        # step 3
        u = cb.dot(Ab_inv)
        # step 4
        delta = u.dot(A) - c
        # step 5
        negative_indices = np.where(delta < 0)[0]

        if negative_indices.size == 0:
            return x, B
        else:
            # step 6
            j0 = negative_indices[0]
            # step 7
            z = Ab_inv.dot(A[:, j0])
            # step 8
            theta = np.empty_like(z, dtype=float)
            for i in range(m):
                if z[i] > 0:
                    theta[i] = x[B[i] - 1] / z[i]
                else:
                    theta[i] = np.inf
            # step 9
            theta0 = np.min(theta)
            # step 10
            if theta0 == np.inf:
                print("Целевой функционал задачи не ограничен сверху на множестве допустимых планов")
                return

            # step 11
            k = np.argmin(theta)
            jstar = B[k]
            # step 12
            B[k] = j0 + 1
            # step 13
            x[j0] = theta0
            for i in range(m):
                if i == k:
                    x[jstar - 1] = 0
                else:
                    x[B[i] - 1] = x[B[i] - 1] - theta0 * z[i]


def check_B(B, n):
    for i in range(len(B)):
        if B[i] >= n:
            return False
    return True


def main():
    # A = np.array([
    #     [1, 10, 1],
    #     [2,2,2],
    # ], dtype=float)
    A = np.array([
        [1, 1, 1],
        [2, 2, 2],
    ], dtype=float)
    b = np.array(
        [0, 0]
        , dtype=float)

    m, n = A.shape
    # step 1 Корректировка правых частей
    for i in range(m):
        if b[i] < 0:
            A[i] *= -1
            b[i] *= -1

    # step 2 Формирование вспомогательной задачи
    zeros = np.zeros(n, dtype=int)
    minus_ones = np.full(m, -1, dtype=int)
    c_temp = np.concatenate((zeros, minus_ones))
    identity_matrix = np.eye(m)
    A_temp = np.hstack((A, identity_matrix))

    # step 3 Начальный базисный план для вспомогательной задачи
    x_temp = np.concatenate((zeros, b))
    B_temp = np.arange(n + 1, n + m + 1)

    # step 4
    solved_x, solved_B = solve(A_temp, B_temp, c_temp, x_temp)

    # step 5
    if not np.all(solved_x[n + 1:n + m + 1] == 0):
        print("Задача не совместна")
        return

    # step 6 Формирование начального плана для исходной задачи
    result_x = x_temp[0:n]
    B_temp -= 1

    # step 7-9 Удаление искусственных переменных из базиса
    while not check_B(B_temp, n):

        jk = np.max(B_temp)
        k = np.argmax(B_temp)
        i = jk - n

        all_numbers = np.arange(0, n)
        all_j = all_numbers[~np.isin(all_numbers, b)]

        for index in range(len(all_j)):
            Ab_temp = A_temp[:, B_temp]
            Ab_temp_inv = np.linalg.inv(Ab_temp)
            l = Ab_temp_inv.dot(A_temp[:, all_j[index]])
            if l[k] != 0:
                B_temp[k] = all_j[index]
                break
        else:
            b = np.delete(b, i)
            A = np.delete(A, i, axis=0)
            A_temp = np.delete(A_temp, i, axis=0)
            B_temp = np.delete(B_temp, k)

    print("x_t: ", result_x)
    print("B:   ", B_temp + 1)
    print("A:   ", A)
    print("b:   ", b)


main()

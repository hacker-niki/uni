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


def main():
    A = np.array([
        [-1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1]
    ], dtype=float)

    x = np.array([0, 0, 1, 3, 2], dtype=float)
    c = np.array([1, 1, 0, 0, 0], float)
    B = np.array([3, 4, 5], int)
    x, B = solve(A, B, c, x)
    print(f"Answer: {x}")
    print(f"B: {B}")


main()

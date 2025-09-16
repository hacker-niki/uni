import numpy as np

def dual_simplex_method(c, A, B, b):
    while True:
        A_B = A[:, B]
        A_inv = np.linalg.inv(A_B)

        c_B = c[B]

        y = c_B @ A_inv

        k_B = A_inv @ b
        k = np.zeros(len(c))
        for i, index in enumerate(B):
            k[index] = k_B[i]

        if np.all(k >= 0):
            #print("Оптимальный план:", *k)
            return k

        j_k = np.argmin(k_B)

        delta_y = A_inv[j_k, :]

        non_basis = [j for j in range(len(c)) if j not in B]
        u = np.array([delta_y @ A[:, j] for j in non_basis])

        if np.all(u >= 0):
            #print("Задача несовместна")
            return None

        sigma, sigma_indexes = list(), list()
        for idx, j in enumerate(non_basis):
            if u[idx] < 0:
                sigma_j = (c[j] - A[:, j] @ y) / u[idx]
                sigma.append(sigma_j)
                sigma_indexes.append(j)

        min_sigma = min(sigma)
        j0 = sigma_indexes[sigma.index(min_sigma)]

        B[j_k] = j0
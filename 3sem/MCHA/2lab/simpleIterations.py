import numpy as np

import addons
from tmp import eps


def simple_iterations(A, b, epsilon=eps, x0=None):
    addons.check_zeros_diag(A, b)
    if not addons.check_convergence(A) and not addons.check(A):
        print("Система не сходится при использовании метода простых итераций")
        return

    """
    Выполняет метод простых итераций для системы уравнений Ax = b.

    Параметры
    ----------
    A : np.ndarray
        Матрица коэффициентов A.
    b : np.ndarray
        Вектор правой части b.
    epsilon : float, optional
        Точность сходимости. По умолчанию 1e-10.
    x0 : np.ndarray, optional
        Начальное приближение решения. По умолчанию None.

    Возвращает
    -------
    x : np.ndarray
        Приближенное решение.
    """
    if A.shape[0] != A.shape[1] or A.shape[0] != b.shape[0]:
        raise ValueError("Размерности A и b не совпадают.")

    a = np.array(A, dtype=np.float64)
    b = np.array(b, dtype=np.float64)

    if x0 is None:
        x0 = np.zeros_like(b, dtype=np.float64)

    x = x0.copy()
    cnt = 0
    while True:
        x_new = np.zeros_like(b, dtype=np.float64)
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if j != i:
                    x_new[i] += a[i, j] * x[j]
            x_new[i] = (b[i] - x_new[i]) / a[i, i]
        cnt += 1

        if np.linalg.norm(x_new - x) < epsilon:
            break

        x = x_new
    return x, cnt

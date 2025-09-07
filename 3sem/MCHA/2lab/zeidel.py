import numpy as np

import addons
from tmp import eps


def zeidel_method(A, b, epsilon=eps, x0=None):
    addons.check_zeros_diag(A, b)
    """
    Perform simple iterations on the matrix equation Ax = b.

    Parameters
    ----------
    A : np.ndarray
        The coefficient matrix A.
    b : np.ndarray
        The right-hand side vector b.
    epsilon : float, optional
        The convergence tolerance. Default is 1e-10.
    x0 : np.ndarray, optional
        The initial guess for the solution. Default is None.

    Returns
    -------
    x : np.ndarray
        The approximate solution.
    """
    if A.shape[0] != A.shape[1] or A.shape[0] != b.shape[0]:
        raise ValueError("The dimensions of A and b do not match.")

    if not addons.check_convergence(A) and not addons.check(A):
        print("Система не сходится если использовать метод Зейделя")
        return

    a = np.array(A, dtype=np.float64)
    b = np.array(b, dtype=np.float64)

    if x0 is None:
        x0 = np.zeros_like(b, dtype=np.float64)

    x = x0.copy()
    cnt = 0
    while True:
        x_prev = x.copy()

        for i in range(a.shape[0]):
            sum1 = np.dot(a[i, :i], x[:i])
            sum2 = np.dot(a[i, i + 1:], x_prev[i + 1:])
            x[i] = (b[i] - sum1 - sum2) / a[i, i]

        cnt += 1
        if np.abs(x - x_prev).max() < epsilon:
            break

    return x, cnt

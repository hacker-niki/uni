import numpy as np
from sympy import *

def lagrange_interpolation(x: np.array, y: np.array):
    n = x.shape[0]
    xsym = symbols('x')
    L = 0
    for j in range(n):
        lj = 1
        for i in range(n):
            if x[j] == x[i]:
                continue
            lj *= (xsym - x[i])/(x[j] - x[i])
        L += y[j] * lj
    return simplify(L)
            
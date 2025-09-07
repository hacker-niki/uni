from sympy import *
import numpy as np

def newton_interpolation(x: np.array, y: np.array):
    xsym = symbols('x')
    n = x.shape[0]
    table = np.zeros(shape=(n-1, n-1))
    n-=1
    for i in range(n):
        table[0, i] = (y[i + 1] - y[i]) / (x[i+1] - x[i])
    for i in range(1, n):
        for j in range(n - i):
            table[i, j] = (table[i - 1, j + 1] - table[i - 1, j]) / (x[i+1+j] - x[j])
    N = 0
    N += y[0]
    for i in range(1, n+1):
        x_poly = 1
        for j in range(i):
            x_poly *= (xsym-x[j])
        N += table[i-1, 0] * x_poly
    N = simplify(N) 
    return N
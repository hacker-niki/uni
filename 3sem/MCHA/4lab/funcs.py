import random

import sympy as sp
import numpy as np


def count_j_matrix(system_expr: np.array, x, n: int):
    J_matrix = np.zeros((n, n), dtype=sp.core.add.Add)
    for i in range(n):
        for j in range(n):
            J_matrix[i, j] = system_expr[i].diff(x[j])
    return J_matrix


def count_j_matrix_values(J_matrix: np.array, x, x0: list, n: int):
    roots = dict()
    for i in range(n):
        roots[x[i]] = x0[i]
    J_matrix_values = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            J_matrix_values[i, j] = J_matrix[i, j].subs(roots)
    return J_matrix_values


def check_j_det(J_matrix: np.array):
    det = np.linalg.det(J_matrix)
    if det == 0:
        raise Exception("det(J(x)) = 0")
    print(f"{det:.3f}", end='  ')


def check_q(system_expr_fi: np.array, roots, x, n, eps=0.0001):
    x1 = random.uniform(roots[0] - eps, roots[0] + eps)
    x2 = random.uniform(roots[0] - eps, roots[0] + eps)
    q = [0 for _ in range(n)]
    for i in range(n):
        q[i] = (abs(system_expr_fi[i].subs({x[0]: x1, x[1]: roots[1]})
                    - system_expr_fi[i].subs({x[0]: x2, x[1]: roots[1]}))
                / abs(x1 - x2))
        if q[i] >= 1:
            print(f"q = {q[i]}")
            print("Условие сжатия не выполнено (q >= 1)")
            exit()
    print("Условие сжатия выполнено (q < 1):")
    for i in range(n):
        print(f"q{i+1} = {q[i]:.5f}")


def simple_iteration_method(system_expr: np.array, system_expr_fi: np.array, x0: list, eps=1e-7):
    roots_list = x0.copy()
    number_exprs = system_expr.shape[0]
    x = sp.symbols(f"x:{number_exprs}")
    check_q(system_expr_fi, roots_list, x, number_exprs)
    errs = [0 for _ in range(number_exprs)]
    err = 1
    iteration = 0
    while eps < err:
        prev_roots_list = roots_list.copy()
        roots_dict = dict()
        for i in range(number_exprs):
            roots_dict[x[i]] = roots_list[i]
        for i in range(number_exprs):
            roots_list[i] = system_expr_fi[i].subs(roots_dict)
            errs[i] = abs(prev_roots_list[i] - roots_list[i])
        err = np.amax(errs)
        iteration += 1
    return roots_list, iteration


def newton_method(system_expr: np.array, x0: list, eps=1e-7):
    roots_list = x0.copy()
    number_exprs = system_expr.shape[0]
    x = sp.symbols(f"x:{number_exprs}")
    J_matrix = count_j_matrix(system_expr, x, number_exprs)
    err = 1
    iteration = 0
    print("Значения det(J) в окрестности точки x0 (требуется det(J) != 0):")
    while eps < err:
        roots_dict = dict()
        for i in range(number_exprs):
            roots_dict[x[i]] = roots_list[i]
        f_x = np.zeros(shape=(number_exprs, ))
        for i in range(number_exprs):
            f_x[i] = system_expr[i].subs(roots_dict)
        J_matrix_values = count_j_matrix_values(J_matrix, x, roots_list, number_exprs)
        check_j_det(J_matrix_values)
        d_x = np.linalg.solve(J_matrix_values, -1 * f_x)
        roots_list += d_x
        err = np.amax(abs(d_x))
        iteration += 1
    print()
    return roots_list, iteration


def print_roots(roots: np.array, n):
    print("Решение системы:")
    for i in range(n):
        print(f"x{i+1} = {roots[i]:.15f}")


def accuracy(q, w):
    is_right_accuracy = True
    for i in range(len(w)):
        if abs(q[i] - w[i]) >= 0.0001:
            is_right_accuracy = False
        else:
            print(f"|{q[i]} - {w[i]}| < 0.0001")
            print(f"{abs(q[i] - w[i]):.17f} < 0.0001")
    return is_right_accuracy

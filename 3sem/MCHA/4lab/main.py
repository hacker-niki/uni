import sympy as sp
import numpy as np
import funcs as f
import time
import tests as t


m = 0.0
a = 0.5
x = sp.symbols("x:2")
system_expr = np.array([             # == 0
    sp.tan(x[0]*x[1] + m) - x[0],
    a * x[0]**2 + 2 * x[1]**2 - 1
])

system_expr_fi = np.array([
    sp.tan(x[0]*x[1] + m),            # == x[0]
    sp.sqrt((1 - a * x[0]**2) / 2.0)  # == x[1]
])

x0 = [0.0, 0.6]
roots_maple = [0.0, 0.7071067812]

if __name__ == '__main__':
    # system_expr = t.system_expr_4
    # system_expr_fi = t.system_expr_fi_4
    # x0 = t.x0_4
    # roots_maple = t.roots_maple_4

    print("-" * 50)
    print(f"Начальное приближение:")
    for i in range(len(x0)):
        print(f"x{i+1} = {x0[i]}")
    print("-" * 50)
    print("Метод простых итераций:")
    start = time.time()
    roots, iteration = f.simple_iteration_method(system_expr, system_expr_fi, x0)
    print("Время работы метода:")
    print(f"{(time.time() - start):.7f} сек")
    f.print_roots(roots, len(x0))
    print("Количество итераций для получаения корней с заданной точностью:")
    print(iteration)
    print("-" * 50)
    print("Метод Ньютона:")
    start = time.time()
    roots, iteration = f.newton_method(system_expr, x0)
    print("Время работы метода:")
    print(f"{(time.time() - start):.7f} сек")
    f.print_roots(roots, len(x0))
    print("Количество итераций для получаения корней с заданной точностью:")
    print(iteration)
    print("-" * 50)
    print("Оценка точности вычислений:")
    f.accuracy(roots_maple, roots)
    print("-" * 50)

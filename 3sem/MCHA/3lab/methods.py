from sympy import lambdify

import function
import separation_of_roots


def bisection_method(interval, fun=function.function, tolerance=function.epsilon):
    a, b = interval
    f_a = fun.subs('x', a)
    f_b = fun.subs('x', b)

    if f_a * f_b >= 0:
        print("Error: The function values at the interval endpoints have the same sign.")
        return None

    iteration = 0
    while (b - a) > tolerance:
        c = (a + b) / 2
        f_c = fun.subs('x', c)

        if f_c == 0:
            return c

        if f_a * f_c < 0:
            b = c
            f_b = f_c
        else:
            a = c
            f_a = f_c

        iteration += 1

    return (a + b) / 2, iteration


def solve_bisection():
    intervals = separation_of_roots.split_interval()
    ans = []
    max_iterations = 0
    for inter in intervals:
        tmp = bisection_method(interval=inter)
        ans.append(tmp[0])
        max_iterations = max(max_iterations, tmp[1])

    return ans, max_iterations


def hord_method(interval, fun=function.function, tolerance=function.epsilon):
    a, b = interval[0], interval[1]
    if fun.subs('x', a) * fun.subs('x', b) > 0:
        raise Exception(f"Secant method couldn't solve f(x) = 0, "
                        f"because f(a) * f(b) = {fun.subs('x', a) * fun.subs('x', b)} >= 0\n"
                        f"--> more than 1 root on ({(a, b)}) or no roots)")

    x2 = a - (fun.subs('x', a) * (b - a)) / (fun.subs('x', b) - fun.subs('x', a))

    x = 0
    iteration = 1
    while abs(fun.subs('x', x2)) > tolerance or x > tolerance:
        if fun.subs('x', a) == 0:
            return a, iteration
        elif fun.subs('x', b) == 0:
            return b, iteration
        elif fun.subs('x', x2) == 0:
            return x2, iteration

        if fun.subs('x', x2) * fun.subs('x', a) < 0:
            b = x2
        elif fun.subs('x', x2) * fun.subs('x', b) < 0:
            a = x2

        x = x2
        x2 = a - (fun.subs('x', a) * (b - a)) / (fun.subs('x', b) - fun.subs('x', a))

        x = abs(x - x2)
        iteration += 1

    return x2, iteration


def solve_hord():
    intervals = separation_of_roots.split_interval()
    ans = []
    max_iterations = 0
    for inter in intervals:
        tmp = hord_method(interval=inter)
        ans.append(tmp[0])
        max_iterations = max(max_iterations, tmp[1])

    return ans, max_iterations


def newton_method(interval, fun=function.function, tolerance=function.epsilon):
    a, b = interval[0], interval[1]

    if fun.subs('x', a) * fun.subs('x', b) > 0:
        raise Exception(f"Newton method couldn't solve f(x) = 0, "
                        f"because f(a) * f(b) = {fun.subs('x', a) * fun.subs('x', b)} >= 0\n"
                        f"--> more than 1 root on ({(a, b)}) or no roots)")

    x_start = (a + b) / 2
    y_diff = fun.diff()
    f_diff = lambdify('x', y_diff, 'numpy')

    x_newton = x_start - fun.subs('x', x_start) / f_diff(x_start)

    x_delta = tolerance * 2
    iteration = 1
    while abs(fun.subs('x', x_newton)) > tolerance or x_delta > tolerance:
        if fun.subs('x', x_newton) == 0:
            return x_newton, iteration

        x_delta = x_newton
        x_newton = x_newton - fun.subs('x', x_newton) / f_diff(x_newton)
        x_delta = abs(x_delta - x_newton)
        iteration += 1

    return x_newton, iteration


def solve_newton():
    intervals = separation_of_roots.split_interval()
    ans = []
    max_iterations = 0
    for inter in intervals:
        tmp = newton_method(interval=inter)
        ans.append(tmp[0])
        max_iterations = max(max_iterations, tmp[1])

    return ans, max_iterations

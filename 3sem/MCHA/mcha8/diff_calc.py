import sympy as sp

z = sp.symbols('z')
epsilon = 0.000001


def deriviative_first(f, x, f2, f3):
    M2 = abs(f2.subs(z, x))
    if M2 == 0:
        M3 = abs(f3.subs(z, x))
        h = (6 * epsilon / M3) ** (1 / 2)
    else:
        h2 = 2 * epsilon / M2
        M3 = abs(f3.subs(z, x))
        h3 = (6 * epsilon / M3) ** (1 / 2)
        h = min(h2, h3)
    return (f.subs(z, x + h) - f.subs(z, x - h)) / (2 * h)


def deriviative_second(f, x, f4):
    M4 = abs(f4.subs(z, x))
    h2 = abs((12 * epsilon / M4))
    h = abs(h2 ** (1 / 2))
    return (f.subs(z, x + h) - 2 * f.subs(z, x) + f.subs(z, x - h)) / h2


def deriviative_second2(f, x, f2, f4):
    M4 = abs(f4.subs(z, x))
    h2 = abs((12 * epsilon / M4))
    h = abs(h2 ** (1 / 2))
    a = (f.subs(z, x + h) - 2 * f.subs(z, x) + f.subs(z, x - h)) / h2
    while a - f2.subs(z, x) > epsilon:
        h -= epsilon ** 3
        a = (f.subs(z, x + h) - 2 * f.subs(z, x) + f.subs(z, x - h)) / h2
    return a

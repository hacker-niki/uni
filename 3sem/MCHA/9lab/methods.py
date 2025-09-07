import time


def euler(xdot, N, y0, y_diff):
    ydots = [y0]
    h = xdot / N
    for i in range(N):
        x = i * h
        y = ydots[-1]
        ydots += [y + h * y_diff(x, y)]
    return ydots


def modified_euler(xdot, N, y0, y_diff):
    ydots = [y0]
    h = xdot / N
    for i in range(N):
        x = i * h
        y = ydots[-1]
        ydots += [y + h * y_diff(x + h / 2, y + h / 2 * y_diff(x, y))]
    return ydots


def runge_kutta(xdot, N, y0, y_diff):
    ydots = [y0]
    h = xdot / N
    for i in range(N):
        x = i * h
        y = ydots[-1]
        K1 = h * y_diff(x, y)
        K2 = h * y_diff(x + h / 2, y + K1 / 2)
        K3 = h * y_diff(x + h / 2, y + K2 / 2)
        K4 = h * y_diff(x + h, y + K3)
        ydots += [y + 1 / 6 * (K1 + 2 * K2 + 2 * K3 + K4)]
    end_time = time.time()
    return ydots


def get_value_at_point(method, x, y0, y_diff, eps):
    n = 1
    old_dots, new_dots = method(x, n, y0, y_diff), method(x, 2 * n, y0, y_diff)
    while max(abs(new_dots[2 * i] - old_dots[i]) for i in range(n + 1)) > eps:
        n *= 2
        old_dots, new_dots = method(x, n, y0, y_diff), method(x, 2 * n, y0, y_diff)
    return new_dots[-1], 2 * n


def create_y_dots(method, xdots, y0, y_diff, eps):
    start_time = time.time()
    ydots = []
    maxn = 0
    midn = []
    for x in xdots:
        y, n = get_value_at_point(method, x, y0, y_diff, eps)
        ydots.append(y)
        maxn = max(maxn, n)
        midn += [n]
    midn = sum(midn) / len(xdots)
    end_time = time.time()
    print("Время: ", end_time - start_time)
    return ydots, midn, maxn

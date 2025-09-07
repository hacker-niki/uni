import matplotlib.pyplot as plt

from methods import euler, modified_euler, runge_kutta, create_y_dots

plotdots = 10 ** 3
eps = 10 ** -4
m, a = 1.0, 1.3
y0 = 0
left_border, right_border = -3, 3


def y_diff(x, y): return (a * (1 - y ** 2)) / ((1 + m) * x ** 2 + y ** 2 + 1)



print("Количество точек: ", plotdots)
print("Эпсилон:  ", eps)
x_dots = [left_border + (right_border - left_border) / plotdots * i for i in range(plotdots + 1)]

ydots, midn, maxn = create_y_dots(euler, x_dots, y0, y_diff, eps)
print("Метод Эйлера:")
for i in range(1, 10, 3):
    print(f"x[{i}]: {x_dots[i * 100]}\n"
          f"y[{i}]: {ydots[i * 100]}\n")
print(f"Максимальное количество частей (n): {maxn}")
print(f"Среднее количество частей (n): {midn}\n")
plt.plot(x_dots, ydots, 'y')

ydots, midn, maxn = create_y_dots(modified_euler, x_dots, y0, y_diff, eps)
print("Модифицированный метод Эйлера:")
for i in range(1, 10, 3):
    print(f"x[{i}] = {x_dots[i * 100]}\n"
          f"y[{i}] = {ydots[i * 100]}\n")
print(f"Максимальное количество частей (n): {maxn}")
print(f"Среднее количество частей (n): {midn}\n")
plt.plot(x_dots, ydots, 'b--')

ydots, midn, maxn = create_y_dots(runge_kutta, x_dots, y0, y_diff, eps)
print("Метод Кнута: ")
for i in range(1, 10, 3):
    print(f"x[{i}] = {x_dots[i * 100]}\n"
          f"y[{i}] = {ydots[i * 100]}\n")
print(f"max amount of parts (n): {maxn}")
print(f"average amount of parts (n): {midn}\n")
plt.plot(x_dots, ydots, 'r:')

plt.show()

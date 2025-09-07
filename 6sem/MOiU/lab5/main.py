import numpy as np
from collections import defaultdict

# Входные данные
c = np.array([[8, 4, 1], [8, 4, 3], [9, 7, 5]])  # Матрица стоимостей
a = np.array([100, 300, 300])  # Массив поставок
b = np.array([300, 200, 200])  # Массив спроса


# Функция для поиска цикла в базисе B с использованием DFS на матрице смежности
def find_cyclic(B, n, m):
    adj_matrix = [[0] * (n + m) for _ in range(n + m)]
    size = n + m
    edges = [[i[0], i[1] + n] for i in B]

    for i in edges:
        adj_matrix[i[0]][i[1]] = 1
        adj_matrix[i[1]][i[0]] = 1

    def dfs_util(v, visited, parent, path):
        visited[v] = True
        path.append(v)
        for i in range(size):
            if adj_matrix[v][i] == 1:
                if not visited[i]:
                    if dfs_util(i, visited, v, path):
                        return True
                elif parent != i:
                    path.append(i)
                    return True
        path.pop()
        return False

    def is_cyclic():
        visited = [False] * size
        path = []
        for i in range(size):
            if not visited[i]:
                if dfs_util(i, visited, -1, path):
                    return path
        return []

    k = is_cyclic()
    k = k[k.index(k[-1]):]
    ans = []
    for i in range(len(k)):
        if i + 1 < len(k):
            if k[i] < k[i + 1]:
                ans.append([k[i], k[i + 1] - n])
            else:
                ans.append([k[i + 1], k[i] - n])
    return ans


# Функция для проверки, образует ли точка b прямой угол с точками a и c
def is_right_angle(a, b, c):
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    return ab[0] * cb[0] + ab[1] * cb[1] == 0


# Функция для определения угловых точек в замкнутом контуре
def find_corner_points(points):
    n = len(points)
    corner_points = []
    for i in range(n):
        a = points[i - 1]
        b = points[i]
        c = points[(i + 1) % n]
        if is_right_angle(a, b, c):
            corner_points.append(b)
    return corner_points


# Основная функция для решения транспортной задачи методом потенциалов
def transport_task(c, a_orig, b_orig):
    # Создание копий входных массивов, чтобы не изменять оригиналы
    a = a_orig.copy()
    b = b_orig.copy()

    # Инициализация матрицы плана перевозок и базиса
    x = np.zeros((len(a), len(b)))  # План перевозок
    B = []  # Базис (список позиций базисных переменных)

    # Шаг 1: Нахождение начального опорного плана
    #  Метод северо-западного угла
    for i in range(len(a)):
        if a[i] == 0:
            continue
        for j in range(len(b)):
            if a[i] > 0 and b[j] > 0:
                # Выделяем минимальное из остатка поставки или спроса
                allocation = min(a[i], b[j])
                x[i][j] = allocation
                a[i] -= allocation
                b[j] -= allocation
                B.append([i, j])  # Добавляем в базис

    # Шаг 2: Итерации до нахождения оптимального решения
    while True:
        # Шаг 2.1: Настройка системы для двойственных переменных (u для поставщиков, v для потребителей)
        m, n = len(a), len(b)
        A = np.zeros((m + n, m + n))  # Матрица коэффициентов для u и v
        y = []  # Вектор правой части
        for k, (i, j) in enumerate(B):
            A[k][i] = 1  # Коэффициент для u_i
            A[k][j + m] = 1  # Коэффициент для v_j
            y.append(c[i][j])  # Стоимость в базисной позиции
        A[m + n - 1][0] = 1  # Фиксируем u_0 = 0 для разрешимости
        y.append(0)

        # Шаг 2.2: Решение системы для двойственных переменных
        s = np.linalg.solve(A, y)
        u = s[:m]  # Потенциалы поставщиков
        v = s[m:]  # Потенциалы потребителей

        # Шаг 2.3: Проверка условия оптимальности (u_i + v_j <= c[i][j] для всех i, j)
        optimal = True
        i0, j0 = -1, -1
        for i in range(m):
            for j in range(n):
                if u[i] + v[j] > c[i][j]:
                    optimal = False
                    i0, j0 = i, j
                    break
            if not optimal:
                break

        # Шаг 2.4: Если план оптимален, вычисляем и выводим результат
        if optimal:
            cost = sum(c[i][j] * x[i][j] for i in range(m) for j in range(n) if x[i][j] > 0)
            # Вывод человекочитаемого результата
            print("Оптимальный план транспортировки:")
            print("Поставщик | Потребитель | Количество | Стоимость")
            print("-" * 50)
            for i in range(m):
                for j in range(n):
                    if x[i][j] > 0:
                        print(
                            f"     {i + 1}    |      {j + 1}      |    {int(x[i][j])}    |    {c[i][j] * x[i][j]}")
            print("-" * 50)
            print(f"Общая стоимость: {int(cost)}")
            return x, cost

        # Шаг 2.5: Если план не оптимален, добавляем нарушающую ячейку в базис
        B.append([i0, j0])

        # Шаг 2.6: Находим цикл в базисе
        cycle_dots = find_cyclic(B, m, n)

        # Шаг 2.7: Определяем угловые точки в цикле
        corner_values = find_corner_points(cycle_dots)
        start_index = corner_values.index([i0, j0])
        sorted_dots = corner_values[start_index:] + corner_values[:start_index]

        # Шаг 2.8: Присваиваем знаки + и - поочерёдно
        for idx, dot in enumerate(sorted_dots):
            dot.append('+' if idx % 2 == 0 else '-')

        # Шаг 2.9: Находим тета (минимальное значение среди ячеек со знаком '-')
        theta = min(x[dot[0]][dot[1]] for dot in sorted_dots if dot[2] == '-')

        # Шаг 2.10: Корректируем значения вдоль цикла
        for dot in sorted_dots:
            if dot[2] == '-':
                x[dot[0]][dot[1]] -= theta
            else:
                x[dot[0]][dot[1]] += theta

        # Шаг 2.11: Удаляем из базиса ячейку, которая стала нулевой
        for dot in sorted_dots:
            if dot[2] == '-' and x[dot[0]][dot[1]] == 0:
                B.remove([dot[0], dot[1]])
                break


if __name__ == '__main__':
    x, cost = transport_task(c, a, b)
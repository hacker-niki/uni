import numpy as np
from itertools import zip_longest
from simplex_method import simplex_method

def Gomori(A, x, B):
    # Шаг 5. Находим дробную компоненту
    k = np.where(x % 1 != 0)

    m, n = np.shape(A)

    non_basiс = list(set(range(n)) - set(B))

    # Шаг 6. Строим базисную и небазисную матрицы
    A_B, A_N = A[:, B], A[:, non_basiс]

    # Шаг 7-9. Находим происзведение матриц Q
    Q = np.linalg.inv(A_B) @ A_N

    # Шаг 10. k-я строка из Q
    l = np.concatenate((np.zeros(len(non_basiс)), Q[k, :].flatten()), dtype='float64')

    fractional = np.array([i % 1 for i in l]).flatten()

    all_variables = [1 if i not in B else 0 for i in range(n)]
    s = np.array([i * j for i, j in zip_longest(fractional, all_variables, fillvalue=0)])
    s = np.append(s, -1)

    x2 = x[k] - np.trunc(x[k])

    return s, x2

if __name__ == '__main__':
    A = np.array([[3, 2, 1, 0],
                 [-3, 2, 0, 1]])

    c = np.array([0, 1, 0, 0])

    b = np.array([6, 0])

    m, n = len(b), np.shape(A)[1]

    # Шаг 1. Решаем задачу симплекс-методом
    x, B = simplex_method(A, b, m, n)

    if isinstance(x, np.ndarray):
        # Шаг 3. Если после решения получен целочисленный оптимальный план
        if np.all(x % 1 == 0):
            print(f'Оптимальный план: {x}')
        # Шаг 4. Если после решения получен дробный план
        else:
            s, x2 = Gomori(A, x, B)
            print(f'Вектор коэффициентов при переменных: {s}')
            print(f'Свободный член: {x2}')
    # Шаг 2. Еси после решения задача несовместна
    else:
        print('Задача несовместна или её целевая функция неограничена сверху на множестве допустимых планов')
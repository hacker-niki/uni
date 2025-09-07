import numpy as np

from special_functions import check_equal_dim


def meth_danil(matrix, tol=0.0001, verbose=0):
    # Проверяем размеры матрицы matrix с помощью функции check_equal_dim
    if not check_equal_dim(matrix):
        raise ValueError("Matrix isn't n, n dimension")

    # Если verbose установлен в 1, выводим сообщение о вычислении собственных значений
    if verbose == 1:
        print("Computing eigenvalues...")

    # Копируем матрицу matrix в a и f
    a = matrix.copy()
    f = matrix.copy()

    # Определяем размерность матрицы
    n = a.shape[0]

    # Инициализируем единичную матрицу s
    s = np.eye(n)

    # Счетчик итераций
    iteration = 0

    # Итерационный цикл
    for i in range(n - 1):
        # Создаем матрицу m, которая будет использоваться для преобразования f и s
        m = np.eye(n)
        m[n - 2 - i][:] = f[n - 1 - i][:]

        # Применяем преобразования к матрицам f и s
        f = np.dot(m, f)
        f = np.dot(f, np.linalg.inv(m))
        s = np.dot(s, np.linalg.inv(m))

        # Увеличиваем счетчик итераций
        iteration += 1

    # Создаем полином p на основе первой строки матрицы f
    p = f[0]
    p = p * (-1)
    p = np.insert(p, 0, 1)

    # Вычисляем корни полинома p, которые являются собственными значениями
    eig_val = np.roots(p)

    # Инициализируем матрицу eig_vec для хранения собственных векторов
    eig_vec = np.zeros(shape=(eig_val.shape[0], n))

    # Вычисление собственных векторов
    for j in range(0, eig_val.shape[0]):
        # Инициализируем вектор y
        y = np.zeros(shape=(n, 1))

        # Вычисляем значения y на основе собственного значения
        for i in range(0, n):
            y[n - 1 - i] = eig_val[j] ** i

        # Вычисляем собственный вектор x
        x = np.dot(s, y)

        # Нормируем собственный вектор x
        norm = np.linalg.norm(x)
        for i in range(0, n):
            eig_vec[i][j] = x[i] / norm

    # Возвращаем собственные значения, собственные векторы и количество итераций
    return eig_val, eig_vec, iteration + 1

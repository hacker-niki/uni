import numpy as np

from special_functions import check_equal_dim


def jacobi_eigenvalue_algorithm(A, tolerance):
    # Проверяем размеры матрицы A с помощью функции check_equal_dim
    if not check_equal_dim(A):
        raise ValueError("Matrix isn't n, n dimension")

    # Определяем размерность матрицы A
    n = A.shape[0]

    # Инициализируем массив для хранения собственных значений
    eigenvalues = np.diag(A)

    # Инициализируем единичную матрицу для хранения собственных векторов
    eigenvectors = np.eye(n)

    # Максимальное количество итераций и счетчик итераций
    max_iterations = 1000
    iteration = 0

    # Вычисляем максимальное значение элемента вне главной диагонали матрицы A
    off_diag = np.abs(A - np.diag(eigenvalues)).max()

    # Цикл выполняется, пока максимальное значение элемента вне главной диагонали больше заданной точности
    # и количество итераций не превышает максимальное значение
    while off_diag > tolerance and iteration < max_iterations:
        # Находим индексы максимального элемента вне главной диагонали
        indices = np.argmax(np.abs(A - np.diag(eigenvalues)))
        i = indices // n
        j = indices % n

        # Вычисляем угол поворота theta
        if A[i, i] == A[j, j]:
            theta = np.pi / 4
        else:
            theta = 0.5 * np.arctan(2 * A[i, j] / (A[i, i] - A[j, j]))

        # Создаем матрицу поворота
        rotation_matrix = np.eye(n)
        rotation_matrix[i, i] = rotation_matrix[j, j] = np.cos(theta)
        rotation_matrix[i, j] = -np.sin(theta)
        rotation_matrix[j, i] = np.sin(theta)

        # Применяем поворот к матрице A и собственным векторам
        A = rotation_matrix.T @ A @ rotation_matrix
        eigenvectors = eigenvectors @ rotation_matrix

        # Обновляем собственные значения и проверяем условие остановки
        eigenvalues = np.diag(A)
        off_diag = np.abs(A - np.diag(eigenvalues)).max()

        # Увеличиваем счетчик итераций
        iteration += 1

    # Возвращаем собственные значения, собственные векторы и количество итераций
    return eigenvalues, eigenvectors, iteration + 1

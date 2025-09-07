import time

import numpy as np

from simpleIterations import simple_iterations
from zeidel import zeidel_method


def check_convergence(M: np.array) -> bool:
    norms = [np.linalg.norm(M.astype(np.float64)),
             np.linalg.norm(M.astype(np.float64), ord=1),
             np.linalg.norm(M.astype(np.float64), ord=2),
             np.linalg.norm(M.astype(np.float64), ord=np.inf)]
    # print(norms)
    return any(norm < 1 for norm in norms)


def check_zeros_diag(matrix_a: np.ndarray, matrix_b: np.ndarray):
    l = len(matrix_a)
    for i in range(0, l):
        if matrix_a[i][i] == 0:
            check = True
            for j in range(0, l):
                if matrix_a[i][j] != 0 and matrix_a[j][i] != 0:
                    matrix_a[[i, j]] = matrix_a[[j, i]]
                    matrix_b[[i, j]] = matrix_b[[j, i]]
                    t = matrix_b[i]
                    matrix_b[i] = matrix_b[j]
                    matrix_b[j] = t
                    check = False
                    break
            if check:
                print("Невозможно избавиться от 0 на диагонали!")
                raise Exception('Невозможно избравиться от 0 на диагонали!')


def check(matrix_a: np.ndarray) -> bool:
    for i in range(matrix_a.shape[0]):
        sumar = 0
        for k in range(matrix_a.shape[1]):
            if k != i:
                sumar += abs(matrix_a[i, k])
        if sumar >= abs(matrix_a[i, i]):
            return False
    return True


def read_matrix_from_file(filename='a.mcha'):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            row = list(map(float, line.split()))  # Преобразуем строку в список целых чисел
            matrix.append(row)  # Добавляем строку в матрицу
    return np.array(matrix)


def test_methods(num_tests: int = 10, check=True):
    np.random.seed(42)

    tolerance = 0.0001

    for i in range(num_tests):
        n = np.random.randint(3, 101)  # Случайное число для размерности матрицы

        if check:
            a = np.random.rand(n, n)
            b = np.random.rand(n)

            # Добавляем число, равное размерности матрицы, к диагональным элементам матрицы a
            np.fill_diagonal(a, np.diagonal(a) + n)
        else:
            n = np.random.randint(3, 4)  # Случайное число для размерности матрицы
            a = np.random.rand(n, n)
            b = np.random.rand(n)

            # print(a)

        print(f"Тест #{i + 1}")
        # print("Матрица:")
        # print(a)
        # print("Вектор b:")
        # print(b)

        # Вычисляем решение с помощью np.linalg.solve
        start3 = time.time()
        expected_solution = np.linalg.solve(a, b)
        end3 = time.time() - start3

        # Вычисляем решение с помощью метода простых итераций

        start1 = time.time()
        val = simple_iterations(a, b)
        end1 = time.time() - start1

        if val:
            ans_simple, ans_simple_cnt = val

        # Вычисляем решение с помощью метода Зейделя
        start2 = time.time()
        val = zeidel_method(a, b)
        end2 = time.time() - start2

        if val:
            ans_zeidel, ans_zeidel_cnt = zeidel_method(a, b)
        else:
            continue
        # Проверяем точность результатов
        simple_correct = True
        zeidel_correct = True

        if ans_simple is None or ans_zeidel is None:
            continue

        for j in range(len(expected_solution)):
            if abs(abs(ans_simple[j]) - abs(expected_solution[j])) > tolerance:
                simple_correct = False
            if abs(abs(ans_zeidel[j]) - abs(expected_solution[j])) > tolerance:
                zeidel_correct = False

        print(
            f"Размерность заданной матрицы - {n}\n"
            f"Методом Зейделя количество итераций {ans_zeidel_cnt}, временные затраты {round(end2, 5)}с, "
            f"методом простых итераций количество итераций {ans_simple_cnt}, временные затраты {round(end1, 5)}с")
        if simple_correct and zeidel_correct:
            print(f"Все методы дали результаты с точностью 0.0001. Встроенная реализация затратила {round(end3, 5)}с")
        else:
            print("Один или несколько методов дали результаты с недопустимой точностью.")

        print("=============================")

import time

import numpy as np

from danilevski_method import meth_danil
from jacoby_method import jacobi_eigenvalue_algorithm


def test_methods(num_tests: int = 10, issym=True):
    np.random.seed(42)
    tolerance = 0.0001

    for i in range(num_tests):
        n = np.random.randint(3, 9)
        if issym:
            a = np.random.rand(n, n)
            a = 0.5 * (a + a.T)  # Создание симметричной матрицы
        else:
            a = np.random.rand(n, n)

        np.fill_diagonal(a, np.diagonal(a) + n)

        print(f"Тест #{i + 1}")

        expected_solution = np.linalg.eig(a).eigenvalues

        start1 = time.time()
        val = jacobi_eigenvalue_algorithm(a, tolerance)
        end1 = time.time() - start1

        start2 = time.time()
        val1 = meth_danil(a, tolerance)
        end2 = time.time() - start2

        if val and val1:
            eig_val, eig_vec, it1 = val
            eig_val1, eig_vec1, it2 = val1
        else:
            continue

        eigen_correct = True

        if eig_val1 is None or eig_val is None:
            continue

        # Сортировка собственных значений и векторов по возрастанию собственных значений
        sorted_indices = np.argsort(eig_val)
        eig_val = eig_val[sorted_indices]

        sorted_indices1 = np.argsort(eig_val1)
        eig_val1 = eig_val1[sorted_indices1]

        sorted_indices2 = np.argsort(expected_solution)
        expected_solution = expected_solution[sorted_indices2]

        # print(eig_val)
        # print(eig_val1)
        # print(expected_solution)

        for j in range(len(expected_solution)):
            if abs(abs(eig_val[j]) - abs(expected_solution[j])) > tolerance:
                eigen_correct = False

        for j in range(len(expected_solution)):
            if abs(abs(eig_val1[j]) - abs(expected_solution[j])) > tolerance:
                eigen_correct = False

        print(f"Размерность заданной матрицы - {n}")
        if eigen_correct:
            print("Метод вычисления собственных значений дал результаты с точностью 0.0001.")
            print(f"Количество итераций методом Якоби {it1}, время - {round(end1, 6)}c, "
                  f"Количество итераций методом Данилевского {it2}, время - {round(end2, 6)}c")
        else:
            print("Метод вычисления собственных значений дал результаты с недопустимой точностью.")

        print("=============================")


def test_method(num_tests: int = 10, issym=True):
    np.random.seed(42)
    tolerance = 0.0001

    for i in range(num_tests):
        n = np.random.randint(3, 9)
        if issym:
            a = np.random.rand(n, n)
            a = 0.5 * (a + a.T)  # Создание симметричной матрицы
        else:
            a = np.random.rand(n, n)

        np.fill_diagonal(a, np.diagonal(a) + n)

        print(f"Тест #{i + 1}")

        expected_solution = np.linalg.eig(a).eigenvalues

        start1 = time.time()
        val = jacobi_eigenvalue_algorithm(a, tolerance)
        end1 = time.time() - start1

        start2 = time.time()
        val1 = meth_danil(a, tolerance)
        end2 = time.time() - start2

        if val and val1:
            eig_val, eig_vec, it1 = val
            eig_val1, eig_vec1, it2 = val1
        else:
            continue

        eigen_correct = True

        if eig_val1 is None or eig_val is None:
            continue

        # Сортировка собственных значений и векторов по возрастанию собственных значений
        sorted_indices = np.argsort(eig_val)
        eig_val = eig_val[sorted_indices]

        sorted_indices1 = np.argsort(eig_val1)
        eig_val1 = eig_val1[sorted_indices1]

        sorted_indices2 = np.argsort(expected_solution)
        expected_solution = expected_solution[sorted_indices2]

        # print(eig_val)
        # print(eig_val1)
        # print(expected_solution)

        for j in range(len(expected_solution)):
            if abs(abs(eig_val1[j]) - abs(expected_solution[j])) > tolerance:
                eigen_correct = False

        print(f"Размерность заданной матрицы - {n}")
        if eigen_correct:
            print("Метод вычисления собственных значений дал результаты с точностью 0.0001."
                  f"Количество итераций методом Данилевского {it2}, время - {round(end2, 6)}c")
        else:
            print("Метод вычисления собственных значений дал результаты с недопустимой точностью.")

            print("=============================")

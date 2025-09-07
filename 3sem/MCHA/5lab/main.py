import numpy as np

import addons
from danilevski_method import meth_danil
from jacoby_method import jacobi_eigenvalue_algorithm
from special_functions import is_matrix_symmetric
from task import A, E

if not is_matrix_symmetric(A, 0.0001):
    print("Matrix not symmetric")
    exit(0)

# Решение первым способом
eig_val, eig_vec, iterations = jacobi_eigenvalue_algorithm(A, E)

print("Метод Якоби:")
print('Исходная матрица:', A)
print('\nМатрица собственных значений:', eig_val, )
print('Собственные вектора:', eig_vec)
print("Количество итераций:", iterations)

# Решение методом Данилевского
eig_val, eig_vec, iterations = meth_danil(A, E)
print("Метод Данилевского:")
print('Исходная матрица:', A)
print('\nМатрица собственных значений:', eig_val, )
print('Собственные вектора:', eig_vec)
print("Количество итераций:", iterations)

print(np.linalg.eig(A))

print("\nПроверка на симметричных матрицах:")

addons.test_methods(num_tests=15)

print("\nПроверка на несимметричных матрицах:")

addons.test_method(num_tests=15, issym=False)

import numpy as np


def input_matrix_and_vector():
    # Вводим размерность матрицы
    n = int(input("Введите размерность матрицы n: "))

    # Вводим индекс i
    i = int(input(f"Введите индекс i (0 до {n - 1}): "))

    # Вводим матрицу A
    print("Введите элементы матрицы A построчно (через пробел):")
    A = np.array([list(map(float, input().split())) for _ in range(n)])

    # Вводим вектор x
    print("Введите элементы вектора x (через пробел):")
    x = np.array(list(map(float, input().split()))).reshape(n, 1)

    # Проверка на корректность введенных данных
    if A.shape != (n, n):
        raise ValueError("Матрица A должна быть квадратной размерности n x n.")
    if x.shape != (n, 1):
        raise ValueError("Вектор x должен быть размерности n x 1.")
    if i < 0 or i >= n:
        raise ValueError(f"Индекс i должен быть в пределах от 0 до {n - 1}.")

    return i, n, A, x


def get_test_values():
    # Задаем тестовые значения
    n = 3  # Порядок матрицы
    i = 2 # Индекс i (например, 1)

    # Пример обратимой матрицы A
    A = np.array([[1, -1, 0],
                  [0, 1, 0],
                  [0, 0, 1]])

    # Пример вектора x
    x = np.array([[1],
                  [0],
                  [1]])

    return i, n, A, x

def multiply_matrices(Q, A_inv):
    n = Q.shape[0]
    result = np.zeros((n, n))

    for j in range(n):
        for k in range(n):
            sum = Q[j][i]*A_inv[i][k] + Q[j][j]*A_inv[j][k]
            if i == j:
                sum /= 2
            result[j, k] = sum

    return result

i, n, A, x = get_test_values()

A_inv = np.linalg.inv(A)

l = np.dot(A_inv, x)

if l[i] == 0:
    print("        _                                         \n"
          "матрица A необратима и метод завершает свою работу")
    exit(0)

l_tilda = l.copy()
l_tilda[i] = -1

l_house = (-1 / l[i]* l_tilda).flatten()

Q = np.eye(n)

Q[:, i] = l_house

A_ans = multiply_matrices(Q, A_inv)


print("\nМатрица A:")
print(A)
print("\nОбратная матрица A^{-1}:")
print(A_inv)
print("\nВектор x:")
print(x)
print("\nОтвет:")
print(A_ans)
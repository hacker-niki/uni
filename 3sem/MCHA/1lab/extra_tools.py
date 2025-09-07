import numpy as np


def print_equation(matrix_a, answers_b):
    A = np.array(matrix_a)
    b = np.array(answers_b)

    n = A.shape[0]
    m = A.shape[1]

    for i in range(n):
        for j in range(m):
            print(f'{A[i, j]:>6.2f}', end='')
        print(f' --> {b[i]:>6.2f}')
    print('\n')


def swap_columns(a, i, j):
    for k in range(len(a)):
        a[k][i], a[k][j] = a[k][j], a[k][i]


def check_zeros_on_diag(matrix, b):
    n = len(matrix)
    for i in range(0, n):
        if matrix[i][i] == 0:
            flag = True
            for j in range(0, n):
                if matrix[i][j] != 0 and matrix[j][i] != 0:
                    swap_columns(matrix, i, j)
                    flag = False
                    break
            if flag:
                if b[i] == 0:
                    print("Система уравнений имеет бесконечно много решений.")
                else:
                    print('Система не имеет решений')
                exit()

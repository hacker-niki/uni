import fractions

import numpy as np

import test_matrix
from gauss_full_pivoting import gauss_full_method
from gauss_method import gauss_method
from gauss_partial_pivoting import gauss_partial_method

Cf = np.array([[fractions.Fraction(0.2), fractions.Fraction(0), fractions.Fraction(0.2), fractions.Fraction(0),
                fractions.Fraction(0)],
               [fractions.Fraction(0), fractions.Fraction(0.2), fractions.Fraction(0), fractions.Fraction(0.2),
                fractions.Fraction(0)],
               [fractions.Fraction(0.2), fractions.Fraction(0), fractions.Fraction(0.2), fractions.Fraction(0),
                fractions.Fraction(0.2)],
               [fractions.Fraction(0), fractions.Fraction(0.2), fractions.Fraction(0), fractions.Fraction(0.2),
                fractions.Fraction(0)],
               [fractions.Fraction(0), fractions.Fraction(0), fractions.Fraction(0.2), fractions.Fraction(0),
                fractions.Fraction(0.2)]], dtype=fractions.Fraction)

Df = np.array([[fractions.Fraction(2.33), fractions.Fraction(0.81), fractions.Fraction(0.67), fractions.Fraction(0.92),
                fractions.Fraction(-0.53)],
               [fractions.Fraction(-0.53), fractions.Fraction(2.33), fractions.Fraction(0.81), fractions.Fraction(0.67),
                fractions.Fraction(0.92)],
               [fractions.Fraction(0.92), fractions.Fraction(-0.53), fractions.Fraction(2.33), fractions.Fraction(0.81),
                fractions.Fraction(0.67)],
               [fractions.Fraction(0.67), fractions.Fraction(0.92), fractions.Fraction(-0.53), fractions.Fraction(2.33),
                fractions.Fraction(0.81)],
               [fractions.Fraction(0.81), fractions.Fraction(0.67), fractions.Fraction(0.92), fractions.Fraction(-0.53),
                fractions.Fraction(2.33)]], dtype=fractions.Fraction)

bf = np.array([fractions.Fraction(4.2), fractions.Fraction(4.2), fractions.Fraction(4.2), fractions.Fraction(4.2),
               fractions.Fraction(4.2)], dtype=fractions.Fraction)
Af = Cf * 10 + Df

C = np.array([[0.2, 0, 0.2, 0, 0],
              [0, 0.2, 0, 0.2, 0],
              [0.2, 0, 0.2, 0, 0.2],
              [0, 0.2, 0, 0.2, 0],
              [0, 0, 0.2, 0, 0.2]], dtype=np.float64)
D = np.array([[2.33, 0.81, 0.67, 0.92, -0.53],
              [-0.53, 2.33, 0.81, 0.67, 0.92],
              [0.92, -0.53, 2.33, 0.81, 0.67],
              [0.67, 0.92, -0.53, 2.33, 0.81],
              [0.81, 0.67, 0.92, -0.53, 2.33]], dtype=np.float64)
b = np.array([4.2, 4.2, 4.2, 4.2, 4.2], dtype=np.float64)
A = C * 10 + D


def fun(x, y):
    print('----------------------------')
    print(x)
    print()
    print(y)
    print("Метод Гаусса:")
    a = gauss_method(x, y)
    if a is not None:
        for i in a:
            print(i, end=' ')
        print()
        print("Метод Гаусса с выбором главного элемента по столбцам:")

    a = gauss_partial_method(x, y)
    if a is not None:
        for i in a:
            print(i, end=' ')
        print()

    a = gauss_full_method(x, y)
    if a is not None:
        print("Метод Гаусса с выбором главного элемента по всей матрице:")
        for i in a:
            print(i, end=' ')
        print()
    print('----------------------------\n')


print("Число обусловленности заданной матрицы:")
print(np.linalg.cond(A))
print(np.linalg.cond(test_matrix.A_2))

print("Погрешность вычислений:")
print(0.05 / (1 + np.linalg.cond(A)))
formatted = "{:.6f}".format(np.linalg.cond(A))
print(formatted)
fun(test_matrix.A_2, test_matrix.b_2)
fun(test_matrix.A_3, test_matrix.b_3)
fun(test_matrix.A_4, test_matrix.b_4)
fun(test_matrix.A_5, test_matrix.b_5)
fun(test_matrix.A_6, test_matrix.b_6)
fun(test_matrix.A_8, test_matrix.b_8)

diff = gauss_full_method(Af, bf) - gauss_full_method(A, b)
print(diff)

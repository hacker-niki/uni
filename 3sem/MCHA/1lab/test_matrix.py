from fractions import Fraction as frac

import numpy as np

A_2 = np.array([[0, 2, -5],
                [2, 0, 3],
                [1, 2, 0]], dtype=np.float64)

b_2 = np.array([-1, 13, 9], dtype=np.float64)

A_3 = np.array([[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]], dtype=np.float64)

b_3 = np.array([0, 0, 0], dtype=np.float64)

A_4 = np.array([[8, 7, 3],
                [-7, -4, -4],
                [-6, 5, -4]], dtype=np.float64)

b_4 = np.array([18, -11, -15], dtype=np.float64)

A_5 = np.array([[0, 0, 0, 0],
                [1, 3, 2, 1],
                [2, 10, 9, 7],
                [3, 8, 9, 2]], dtype=np.float64)

b_5 = np.array([0, 11, 40, 37], dtype=np.float64)

A_6 = np.array([[1, 2, 3, 4, 5, 6, 7, 8],
                [11, 23, 30, 48, 65, 6, 72, 81],
                [12, 25, 39, 94, 55, 64, 73, 81],
                [1, 2, 3, 4, 5, 6, 7, 8],
                [11, 23, 30, 48, 65, 6, 72, 81],
                [12, 25, 39, 94, 55, 64, 73, 81],
                [12, 25, 39, 94, 55, 64, 73, 81],
                [1, 2, 3, 4, 5, 6, 7, 8]], dtype=np.float64)

b_6 = np.array([51, 25, 53, 45, 55, 56, 75, 85], dtype=np.float64)

A_7 = np.array([[1, 2, 3, 4, 5, 6, 7, 8],
                [2, 23, 30, 48, 65, 6, 9, 81],
                [3, 25, 39, 94, 55, 64, 73, 1],
                [4, 2, 2, 3, 44, 6, 7, 8],
                [5, 23, 30, 48, 65, 6, 72, 1],
                [6, 25, 39, 94, 55, 64, 73, 8],
                [7, 25, 1, 4, 12, 64, 12, 81],
                [8, 22, 33, 44, 55, 6, 7, 9]], dtype=np.float64)

b_7 = np.array([51, 13, 12, 45, 55, 56, 75, 85], dtype=np.float64)

A_8 = np.array([[1, 2], [1, 2]], dtype=np.float64)
b_8 = np.array([1, 1], dtype=np.float64)

matrix = np.array(
    [
        [frac('5'), frac('0'), frac('0'), frac('8'), frac('8'), frac('2'), frac('0'), frac('6'), frac('8'), frac('1'),
         frac('5'), frac('2'), frac('5'), frac('7'), frac('6'), frac('7'), frac('2'), frac('1'), frac('6'), frac('0')],
        [frac('1'), frac('6'), frac('7'), frac('0'), frac('4'), frac('2'), frac('3'), frac('1'), frac('6'), frac('3'),
         frac('5'), frac('9'), frac('9'), frac('3'), frac('4'), frac('8'), frac('1'), frac('2'), frac('9'), frac('4')],
        [frac('7'), frac('8'), frac('6'), frac('1'), frac('9'), frac('8'), frac('4'), frac('7'), frac('7'), frac('2'),
         frac('1'), frac('3'), frac('4'), frac('9'), frac('0'), frac('6'), frac('4'), frac('3'), frac('2'), frac('5')],
        [frac('1'), frac('3'), frac('7'), frac('4'), frac('5'), frac('8'), frac('8'), frac('9'), frac('0'), frac('6'),
         frac('6'), frac('2'), frac('3'), frac('6'), frac('6'), frac('9'), frac('3'), frac('5'), frac('8'), frac('2')],
        [frac('0'), frac('1'), frac('0'), frac('9'), frac('1'), frac('7'), frac('5'), frac('8'), frac('3'), frac('9'),
         frac('3'), frac('2'), frac('5'), frac('3'), frac('4'), frac('3'), frac('5'), frac('8'), frac('1'), frac('8')],
        [frac('5'), frac('0'), frac('7'), frac('8'), frac('2'), frac('7'), frac('5'), frac('0'), frac('0'), frac('4'),
         frac('9'), frac('6'), frac('7'), frac('1'), frac('3'), frac('5'), frac('5'), frac('9'), frac('9'), frac('6')],
        [frac('0'), frac('2'), frac('5'), frac('6'), frac('5'), frac('7'), frac('3'), frac('7'), frac('6'), frac('4'),
         frac('1'), frac('5'), frac('3'), frac('8'), frac('3'), frac('2'), frac('4'), frac('6'), frac('2'), frac('0')],
        [frac('6'), frac('8'), frac('9'), frac('9'), frac('7'), frac('6'), frac('4'), frac('8'), frac('7'), frac('8'),
         frac('0'), frac('6'), frac('2'), frac('6'), frac('6'), frac('4'), frac('0'), frac('1'), frac('8'), frac('5')],
        [frac('4'), frac('5'), frac('0'), frac('5'), frac('5'), frac('9'), frac('5'), frac('7'), frac('1'), frac('3'),
         frac('0'), frac('4'), frac('6'), frac('2'), frac('2'), frac('1'), frac('0'), frac('0'), frac('4'), frac('5')],
        [frac('3'), frac('2'), frac('3'), frac('0'), frac('6'), frac('4'), frac('7'), frac('3'), frac('1'), frac('3'),
         frac('9'), frac('2'), frac('7'), frac('1'), frac('9'), frac('5'), frac('0'), frac('1'), frac('9'), frac('1')],
        [frac('1'), frac('3'), frac('5'), frac('8'), frac('1'), frac('6'), frac('9'), frac('6'), frac('3'), frac('8'),
         frac('3'), frac('5'), frac('5'), frac('7'), frac('9'), frac('9'), frac('9'), frac('6'), frac('7'), frac('8')],
        [frac('8'), frac('0'), frac('2'), frac('7'), frac('7'), frac('1'), frac('5'), frac('7'), frac('3'), frac('3'),
         frac('0'), frac('2'), frac('0'), frac('6'), frac('9'), frac('9'), frac('1'), frac('0'), frac('3'), frac('9')],
        [frac('5'), frac('3'), frac('9'), frac('7'), frac('5'), frac('0'), frac('2'), frac('4'), frac('8'), frac('4'),
         frac('3'), frac('5'), frac('9'), frac('7'), frac('4'), frac('8'), frac('3'), frac('2'), frac('6'), frac('0')],
        [frac('2'), frac('5'), frac('9'), frac('6'), frac('3'), frac('9'), frac('6'), frac('4'), frac('8'), frac('6'),
         frac('8'), frac('0'), frac('2'), frac('9'), frac('3'), frac('0'), frac('7'), frac('5'), frac('0'), frac('4')],
        [frac('4'), frac('4'), frac('6'), frac('2'), frac('9'), frac('5'), frac('1'), frac('1'), frac('8'), frac('6'),
         frac('2'), frac('2'), frac('2'), frac('1'), frac('2'), frac('7'), frac('6'), frac('0'), frac('9'), frac('3')],
        [frac('7'), frac('1'), frac('2'), frac('1'), frac('7'), frac('5'), frac('8'), frac('2'), frac('1'), frac('9'),
         frac('5'), frac('5'), frac('1'), frac('0'), frac('6'), frac('4'), frac('2'), frac('0'), frac('1'), frac('5')],
        [frac('2'), frac('2'), frac('1'), frac('1'), frac('2'), frac('3'), frac('8'), frac('3'), frac('7'), frac('7'),
         frac('8'), frac('6'), frac('0'), frac('6'), frac('2'), frac('0'), frac('6'), frac('9'), frac('5'), frac('2')],
        [frac('3'), frac('5'), frac('6'), frac('4'), frac('6'), frac('8'), frac('7'), frac('9'), frac('4'), frac('9'),
         frac('1'), frac('4'), frac('0'), frac('4'), frac('5'), frac('3'), frac('8'), frac('2'), frac('0'), frac('4')],
        [frac('2'), frac('5'), frac('6'), frac('8'), frac('7'), frac('2'), frac('4'), frac('3'), frac('4'), frac('2'),
         frac('1'), frac('9'), frac('4'), frac('4'), frac('5'), frac('5'), frac('5'), frac('3'), frac('6'), frac('9')],
        [frac('9'), frac('4'), frac('5'), frac('1'), frac('9'), frac('0'), frac('6'), frac('5'), frac('2'), frac('6'),
         frac('0'), frac('1'), frac('0'), frac('2'), frac('4'), frac('1'), frac('8'), frac('8'), frac('2'), frac('4')]
    ]
)
matrix_b = np.array(
    [[frac('7')], [frac('2')], [frac('9')], [frac('6')], [frac('5')], [frac('6')], [frac('3')], [frac('3')],
     [frac('2')], [frac('2')], [frac('1')], [frac('7')], [frac('9')], [frac('5')], [frac('6')], [frac('6')],
     [frac('5')], [frac('6')], [frac('2')], [frac('4')]]
)

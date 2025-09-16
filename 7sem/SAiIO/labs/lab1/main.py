import numpy as np
from dual_simplex import dual_simplex_method


def lab1(c, A, b, d_minus, d_plus):
    n, m = d_minus.size, b.size

    # Шаг 1. Для ci > 0:
    c_minus_indexes = np.where(c > 0)[0]

    # 1.1. ci * -1
    c[c_minus_indexes] *= (-1)

    # 1.2. Ai * -1
    A[c_minus_indexes] *= (-1)

    # 1.3. d_minusi * -1 и d_plusi * -1
    d_minus[c_minus_indexes] *= (-1)
    d_plus[c_minus_indexes] *= (-1)

    # 1.4. d_minusi и d_plusi меняем местами
    d_minus[c_minus_indexes], d_plus[c_minus_indexes] = d_plus[c_minus_indexes], d_minus[c_minus_indexes]
    
    # Шаг 2. Перевод задачи в каноническую форму без учета ограничений неотрицательности
    alpha = 0

    c = np.concatenate((c, np.zeros(2 * n)), axis=0)

    A = np.concatenate((A, np.eye(n)), axis=0)
    A = np.concatenate((A, np.eye(m + n)), axis=1)

    b = np.concatenate((b, d_plus), axis=0)

    d_minus = np.concatenate((d_minus, np.zeros(2 * n)), axis=0)
    
    # Шаг 3. Создание стека и других переменных
    S = list()
    x_asterix = 0
    r = 0
    S.append([d_minus, b, alpha])

    B = np.array([n + i for i in range(n + m)])
    flag = False

    # Шаг 4. Берем задачи из стека
    while True:
        # 4.1. Стек не пуст
        if S:
            delta, b, alpha = S.pop()
            if np.any(b <= 0):
                if not flag:
                    b_shtrih = b - A @ d_minus
                    alpha_shtrih = alpha + c @ np.transpose(d_minus)
                    x = np.round(dual_simplex_method(c, A, B, b_shtrih), 2)
                else:
                    x = np.round(dual_simplex_method(c, A, B, b), 2)

            # 4.1.1. План целочисленный
            if np.all(x % 1 == 0):
                if isinstance(x_asterix, int) or c @ x + alpha_shtrih > r:
                    x_asterix = x + delta
                    r = c @ x + alpha_shtrih
                    S[-1] = [S[-1][0], b_two_shtrih, alpha_shtrih]
                    flag = True
            # 4.1.2. План дробный
            else:
                if isinstance(x_asterix, int) or np.ceil(c @ x + alpha_shtrih) > r:
                    x1, x2 = np.trunc(x[0]), np.ceil(x[0])

                    index = np.where(x == x[0])[-1][-1]

                    b_two_shtrih = b_shtrih.copy()
                    b_two_shtrih[index + m] = x1

                    d_minus = np.zeros(2 * n + m)
                    d_minus[index] = x2

                    S.append([delta + np.zeros(2 * n + m), b_two_shtrih, alpha_shtrih])
                    S.append([delta + d_minus, b_shtrih, alpha_shtrih])
        # 4.2. Стек пуст
        else:
            # Если нет плана, то задача несовместна
            if isinstance(x_asterix, int):
                print("Задача несовместна")
            # Если есть, то это оптимальный план с положительными элементами
            else:
                for i in range(n):
                    if x_asterix[i] < 0:
                        x_asterix[i] *= -1
                return x_asterix[:n] 

if __name__ == '__main__':
    c_ = np.array([1, 1])

    A_ = np.array([[5, 9],
                   [9, 5]])

    b_ = np.array([63, 63])

    d_minus = np.array([1, 1])

    d_plus = np.array([6, 6])

    ans = lab1(c_, A_, b_, d_minus, d_plus)

    print(f'Оптимальный план: {ans}')
import numpy as np
import math


n = 5
m = 2
c = np.array([-4, -3, -7, 0, 0])
A = np.array([[-2, -1, -4, 1, 0],
              [-2, -2, -2, 0, 1]])
b = np.array([-1, -1.5])
B = np.array([4, 5])

def dual_simplex_method(c, A, b, B, iteration=1):
    print(f"\n=== Итерация {iteration} ===")
    print(f"Текущие базисные индексы: {B}")

    #Составляем базисную матрицу AB и находим обратную A_B^{-1}
    Bc = B - 1  # Корректируем индексы для работы с массивами (0-based)
    AB = A[:, Bc]  # Извлекаем столбцы матрицы A с базисными индексами
    print("Базисная матрица AB:\n", AB)
    rAB = np.linalg.inv(AB)  # Обратная матрица
    print("Обратная матрица A_B^{-1}:\n", rAB)

    #Формируем вектор c_B из базисных компонент c
    cB = c[Bc]
    print("Вектор c_B:", cB)

    #Находим базисный допустимый план двойственной задачи y^T = c_B^T * A_B^{-1}
    yT = np.dot(cB, rAB)
    print("Двойственный план y^T:", yT)

    #Вычисляем псевдоплан κ: κ_B = A_B^{-1} * b, κ_N = 0
    kB = np.dot(rAB, b)  # Базисные компоненты псевдоплана
    kT = np.zeros(n)  # Полный псевдоплан
    kT[Bc] = kB  # Заполняем базисные компоненты
    print("Псевдоплан κ:", kT)

    #Проверяем, является ли псевдоплан неотрицательным
    if np.all(kT >= 0):
        print("Найден оптимальный план:", kT)
        return kT  # Завершаем работу, возвращаем решение

    #Находим отрицательную компоненту псевдоплана и её индекс в B
    negative_idx = np.where(kT < 0)[0][0]  # Первый отрицательный элемент
    k = np.where(B == negative_idx + 1)[0][0]  # Индекс в множестве B
    print(f"Отрицательная компонента κ[{negative_idx + 1}] = {kT[negative_idx]}, k = {k}")

    #Извлекаем строку Δy из A_B^{-1} для выбранного k
    deltaY = rAB[k, :]
    print("Вектор Δy:", deltaY)

    #Вычисляем μ_j для всех небазисных индексов
    mu = np.zeros(n)
    for i in range(n):
        if (i + 1) not in B:
            mu[i] = np.dot(deltaY, A[:, i])
    print("Вектор μ:", mu)

    #Проверяем условие несовместности задачи
    if np.all(mu >= 0):
        print("Прямая задача несовместна")
        return None

    #Вычисляем σ_j для всех j, где μ_j < 0
    sigma = np.array([math.inf] * n)
    for i in range(n):
        if mu[i] < 0:
            sigma[i] = (c[i] - np.dot(A[:, i], yT)) / mu[i]
    print("Вектор σ:", sigma)

    #Находим минимальное σ_0 и соответствующий индекс j_0
    sigma0 = np.min(sigma)
    j0 = np.where(sigma == sigma0)[0][0] + 1  # Корректируем индекс (1-based)
    print(f"Минимальное σ_0 = {sigma0}, новый базисный индекс j_0 = {j0}")

    #Обновляем множество базисных индексов
    B[k] = j0
    print(f"Обновлённые базисные индексы: {B}")

    # Рекурсивно продолжаем с новым базисом
    return dual_simplex_method(c, A, b, B, iteration + 1)

if __name__ == '__main__':
    # Запускаем алгоритм и выводим результат
    result = dual_simplex_method(c, A, b, B)
    if result is not None:
        print("\nФинальный оптимальный план:", result)
    else:
        print("\nРешение не найдено")
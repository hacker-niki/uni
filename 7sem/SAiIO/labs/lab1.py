import numpy as np
from scipy.optimize import linprog
from typing import List, Dict, Tuple, Optional

# Устанавливаем небольшую погрешность для операций с плавающей запятой
TOLERANCE = 1e-9

def get_fractional_part(value: float) -> float:
    """
    Вычисляет дробную часть числа {alpha} = alpha - floor(alpha).
    Справляется с небольшими погрешностями вычислений.
    """
    # Если число очень близко к целому, считаем его дробную часть нулем
    if abs(value - np.round(value)) < TOLERANCE:
        return 0.0
    
    return value - np.floor(value)

def generate_gomory_cut(c: np.ndarray, A: np.ndarray, b: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[Dict]]:
    """
    Реализует один шаг метода Гомори для генерации отсекающего ограничения.

    Args:
        c (np.ndarray): Вектор стоимостей целевой функции (n,).
        A (np.ndarray): Матрица ограничений (m, n).
        b (np.ndarray): Вектор свободных членов (m,).

    Returns:
        Tuple[Optional[np.ndarray], Optional[Dict]]:
        - Если найден оптимальный целочисленный план, возвращает (план, None).
        - Если сгенерировано отсечение, возвращает (None, словарь с данными отсечения).
        - Если задача несовместна/неограничена, возвращает (None, None).
    """
    print("--- Шаг 1: Решение задачи ЛП симплекс-методом ---")
    
    # linprog ищет минимум, поэтому для задачи максимизации инвертируем вектор c
    # ИСПОЛЬЗУЕМ СОВРЕМЕННЫЙ РЕШАТЕЛЬ 'highs'
    res = linprog(-c, A_eq=A, b_eq=b, method='highs')

    # --- Шаг 2: Проверка результата симплекс-метода ---
    if not res.success:
        print(f"\nРезультат: Задача несовместна или её целевая функция неограничена. ({res.message})")
        return None, None

    x_optimal = res.x
    print(f"Найден оптимальный план ЛП релаксации: x = {np.round(x_optimal, 4)}")
    
    # --- Шаг 3: Проверка на целочисленность ---
    is_integer = np.all(np.abs(x_optimal - np.round(x_optimal)) < TOLERANCE)
    
    if is_integer:
        print("\nРезультат: Найден оптимальный целочисленный план.")
        return np.round(x_optimal).astype(int), None

    print("\nПлан не является целочисленным. Приступаем к построению отсечения.")

    # --- Шаг 4, 5: Находим первую дробную компоненту среди базисных переменных ---
    # Базисные переменные - те, что > 0 в оптимальном плане
    basic_indices_mask = x_optimal > TOLERANCE
    
    # Ищем индекс переменной xi с максимальной дробной частью для генерации отсечения
    fractional_parts = np.array([get_fractional_part(v) for v in x_optimal])
    
    # Выбираем строку для отсечения (среди базисных переменных)
    source_row_var_index = -1
    max_frac = -1.0
    
    for i, is_basic in enumerate(basic_indices_mask):
        # Ищем базисную переменную с наибольшей дробной частью
        if is_basic and fractional_parts[i] > max_frac:
            max_frac = fractional_parts[i]
            source_row_var_index = i
            
    if source_row_var_index == -1:
        print("Ошибка: не найдена дробная базисная компонента для построения отсечения.")
        return None, None
        
    xi_val = x_optimal[source_row_var_index]
    print(f"--- Шаг 5: Выбрана переменная x{source_row_var_index + 1} = {xi_val:.4f} для генерации отсечения.")

    # --- Шаги 6, 7: Формируем базисные и небазисные матрицы и переменные ---
    basic_indices = np.where(basic_indices_mask)[0]
    non_basic_indices = np.where(~basic_indices_mask)[0]

    # Индекс k в наборе B
    k = np.where(basic_indices == source_row_var_index)[0][0]

    print(f"Базисные индексы B: {[i + 1 for i in basic_indices]}")
    print(f"Небазисные индексы N: {[i + 1 for i in non_basic_indices]}")
    
    A_B = A[:, basic_indices]
    A_N = A[:, non_basic_indices]

    # --- Шаг 8, 9: Находим A_B^-1 и Q = A_B^-1 * A_N ---
    try:
        A_B_inv = np.linalg.inv(A_B)
    except np.linalg.LinAlgError:
        print("Ошибка: Базисная матрица A_B вырождена и не может быть обращена.")
        return None, None
        
    Q = A_B_inv @ A_N
    
    # --- Шаг 10: Выделяем k-ую строку из Q ---
    l_row = Q[k, :]

    # --- Шаг 11: Формируем отсекающее ограничение ---
    f_i = get_fractional_part(xi_val)
    f_l = np.array([get_fractional_part(val) for val in l_row])

    # Собираем отсечение в виде строки для вывода
    cut_parts = []
    for i, coeff in enumerate(f_l):
        if coeff > TOLERANCE:
            cut_parts.append(f"{coeff:.4f} * x{non_basic_indices[i] + 1}")
    
    cut_expression = " + ".join(cut_parts) + f" >= {f_i:.4f}"
    
    print("\n--- Шаг 11: Сгенерировано отсекающее ограничение Гомори ---")
    print(cut_expression)

    # Возвращаем коэффициенты для нового ограничения и правую часть
    new_constraint_coeffs = np.zeros_like(c, dtype=float)
    new_constraint_coeffs[non_basic_indices] = f_l
    
    cut_info = {
        "expression": cut_expression,
        "coeffs": new_constraint_coeffs,
        "rhs": f_i
    }
    
    return None, cut_info

if __name__ == '__main__':
    # Пример задачи:
    # Максимизировать z = x2
    # При ограничениях:
    # 3*x1 + 2*x2 <= 6
    # -3*x1 + 2*x2 <= 0
    #
    # Канонический вид с добавлением слабых переменных s1 (x3) и s2 (x4):
    # 3*x1 + 2*x2 + 1*s1 + 0*s2 = 6
    # -3*x1 + 2*x2 + 0*s1 + 1*s2 = 0
    # Целевая функция: z = 0*x1 + 1*x2 + 0*s1 + 0*s2 -> max
    
    # Вектор стоимостей c для переменных [x1, x2, s1, s2]
    c_example = np.array([0, 1, 0, 0])
    
    # Матрица ограничений A
    A_example = np.array([
        [3,  2, 1, 0],
        [-3, 2, 0, 1]
    ])
    
    # Вектор свободных членов b
    b_example = np.array([6, 0])

    print("--- Запуск метода Гомори для примера ---")
    print(f"max z = {c_example[0]}*x1 + {c_example[1]}*x2") # Отображаем исходную целевую функцию
    print("Ограничения:")
    print("3*x1 + 2*x2 <= 6")
    print("-3*x1 + 2*x2 <= 0\n")

    optimal_plan, cut = generate_gomory_cut(c_example, A_example, b_example)

    if optimal_plan is not None:
        print("\nИтоговый оптимальный целочисленный план:")
        # Выводим только оригинальные переменные
        for i, val in enumerate(optimal_plan[:2]):
            print(f"x{i+1} = {val}")
            
    elif cut is not None:
        print("\nНеобходимо добавить сгенерированное ограничение к задаче и решить ее заново.")
        print(f"Выражение отсечения: {cut['expression']}")
        print(f"Коэффициенты нового ограничения для переменных [x1, x2, s1, s2]: {np.round(cut['coeffs'], 4)}")
        print(f"Правая часть нового ограничения: {cut['rhs']:.4f}")
    else:
        # Случай, когда задача несовместна/неограничена
        pass


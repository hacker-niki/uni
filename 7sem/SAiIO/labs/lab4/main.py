import numpy as np
import pandas as pd

def solve_knapsack(volumes, values, capacity):
    n = len(volumes)
    OPT = np.zeros((n + 1, capacity + 1), dtype=int)
    X = np.zeros((n + 1, capacity + 1), dtype=int)

    # прямой ход дп
    for k in range(1, n + 1):
        vk = volumes[k - 1]  # Объем k
        ck = values[k - 1]   # Ценность k
        
        for b in range(capacity + 1):
            
            # k-й предмет не выбран
            profit_not_taking = OPT[k - 1][b]
            
            # можем взять k-й предмет
            if vk <= b:
                # случай, когда k выбран
                profit_taking = ck + OPT[k - 1][b - vk]
                
                if profit_taking > profit_not_taking:
                    OPT[k][b] = profit_taking
                    X[k][b] = 1 
                else:
                    OPT[k][b] = profit_not_taking
                    X[k][b] = 0
            
            else:
                OPT[k][b] = profit_not_taking
                X[k][b] = 0

    # обратный ход дп
    selected_items = []
    current_capacity = capacity
    
    for k in range(n, 0, -1):
        
        # k-й предмет выбран
        if X[k][current_capacity] == 1:
            selected_items.append(k)
            current_capacity -= volumes[k - 1]
    
    max_total_value = OPT[n][capacity]
    selected_items.sort()
    
    return max_total_value, selected_items, OPT, X

volumes_example = [4, 3, 2, 5]  # Объемы v_i
values_example = [10, 5, 4, 11] # Ценности c_i
capacity_example = 8            # Вместимость B=8

# Шаг 5: Запускаю решение для примера
max_value, items_taken, OPT_matrix, X_matrix = solve_knapsack(volumes_example, values_example, capacity_example)

print(f"Количество предметов (n): {len(volumes_example)}")
print(f"Вместимость рюкзака (B): {capacity_example}")
print(f"Объемы: {volumes_example}")
print(f"Ценности: {values_example}")
print("-" * 50)

print("Матрица максимальной ценности OPT[k][b]:")

k_labels = [f"k={i}" for i in range(len(volumes_example) + 1)]
b_labels = [f"b={j}" for j in range(capacity_example + 1)]

df_opt = pd.DataFrame(OPT_matrix, index=k_labels, columns=b_labels)
print(df_opt)
print("-" * 50)

print(f"Максимальная суммарная ценность OPT(n, B): {max_value}")
print(f"Выбранные предметы (номера): {items_taken}")

print(f"Общая ценность выбранных предметов: {sum(values_example[i-1] for i in items_taken)}")
print(f"Общий объем выбранных предметов: {sum(volumes_example[i-1] for i in items_taken)}")

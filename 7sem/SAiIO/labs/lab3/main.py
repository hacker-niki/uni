import numpy as np

def solve_resource_allocation(P, Q, A):
    B = np.zeros((P, Q + 1), dtype=int)
    C = np.zeros((P, Q + 1), dtype=int)

    # прямой ход дп
    for p_idx in range(P):
        for q in range(Q + 1):
            
            # p = 1 (p_idx = 0)
            if p_idx == 0:
                # B(1, q) = A(1, q) и C(1, q) = q
                B[p_idx][q] = A[p_idx][q]
                C[p_idx][q] = q
            
            # p >= 2 (p_idx > 0)
            else:
                # B(p, q) = max_{i} {A(p, i) + B(p-1, q-i)}
                max_profit = -1
                optimal_i = -1
                
                # все возможные объемы ресурса 'i' для текущего агента p_idx
                for i in range(q + 1):
                    current_profit = A[p_idx][i] + B[p_idx - 1][q - i]
                    
                    if current_profit > max_profit:
                        max_profit = current_profit
                        optimal_i = i
                
                B[p_idx][q] = max_profit
                C[p_idx][q] = optimal_i

    # обратный ход дп
    optimal_allocation = {}
    q_current = Q
    p_idx = P - 1

    while p_idx >= 0:
        agent_number = p_idx + 1
        
        allocation_for_agent = C[p_idx][q_current]
        
        optimal_allocation[agent_number] = allocation_for_agent
        
        q_current -= allocation_for_agent
        
        p_idx -= 1

    max_total_profit = B[P - 1][Q]
    
    sorted_allocation = {k: optimal_allocation[k] for k in sorted(optimal_allocation)}
    
    return max_total_profit, B, C, sorted_allocation


P_example = 3
Q_example = 3

A_example = [
    [0, 1, 2, 3],
    [0, 0, 1, 2],
    [0, 2, 2, 3]
]


max_profit, B_matrix, C_matrix, allocation = solve_resource_allocation(P_example, Q_example, A_example)


print(f"P (количество агентов): {P_example}")
print(f"Q (общий ресурс): {Q_example}")
print("-" * 30)
print("Матрица прибыли A:")
print(np.array(A_example))
print("-" * 30)

print("Матрица максимальной прибыли B (Функция Беллмана):")
print(B_matrix)
print("-" * 30)

print("Матрица оптимального распределения C (Ресурс для p-го агента):")
print(C_matrix)
print("-" * 30)

print(f"Максимальная суммарная прибыль B(P, Q) = B({P_example}, {Q_example}): {max_profit}")
print("-" * 30)

print("Оптимальное распределение ресурсов (Агент: Ресурс):")
for agent, resource in allocation.items():
    print(f"Агент {agent}: {resource} ед. ресурса")

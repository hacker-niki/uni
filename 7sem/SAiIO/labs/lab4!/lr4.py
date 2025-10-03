def direct_run(vs, cs, b):
    n = len(vs)  # Количество предметов
    B = b  # Сохраняем исходную вместимость
    
    # Инициализируем таблицы:
    # OPT[k][b] - максимальная ценность для первых k предметов и вместимости b
    # x[k][b] - решение: брать (1) или не брать (0) k-й предмет
    OPT = [[0] * (B + 1) for _ in range(n + 1)]
    x = [[0] * (B + 1) for _ in range(n + 1)]
    
    for k in range(1, n + 1):
        for b in range(B + 1):
            if k == 1:
                if vs[0] <= b:
                    OPT[k][b] = cs[0]
                    x[k][b] = 1
            else:
                #предмет не помещается в рюкзак
                if vs[k-1] > b:
                    OPT[k][b] = OPT[k-1][b]
                    x[k][b] = 0
                #предмет помещается
                else:
                    not_take = OPT[k-1][b]
                    take = OPT[k-1][b - vs[k-1]] + cs[k-1]
                    
                    if take > not_take:
                        OPT[k][b] = take
                        x[k][b] = 1
                    else:
                        OPT[k][b] = not_take
                        x[k][b] = 0
    return OPT, B, n, x

def reverse_run(OPT, B, n, x):
    sel = []  # Список для хранения выбранных предметов
    cur_b = B  # Текущая оставшаяся вместимость

    for k in range(n, 0, -1):
        if x[k][cur_b] == 1:
            sel.append(k - 1)
            cur_b -= vs[k-1]
        
    sel.reverse()

    return OPT[n][B], sel

if __name__ == "__main__":

    vs = [2, 5, 7, 3, 4, 6, 1, 8]    # Объемы предметов
    cs = [5, 8, 12, 4, 6, 9, 4, 15]    # Ценности предметов
    b = 15                                # Вместимость рюкзака

    OPT, B, n, x = direct_run(vs, cs, b)
    max_value, selected = reverse_run(OPT, B, n, x)
        

    # Вывод результатов
    total_volume = 0
    print("Выбранные предметы:")
    for i in selected:
        total_volume += vs[i]
        print(f"Предмет {i+1}: объем={vs[i]}, ценность={cs[i]}")    
    
    print(f"\nОбъём: {total_volume} из {b}")
    print(f"Ценность: {max_value}")
    
    # Дополнительная информация для отладки
    print(f"\nТаблица OPT (максимальные ценности):")
    for i, row in enumerate(OPT):
        print(f"k={i}: {row}")
    
    print(f"\nТаблица x (решения):")
    for i, row in enumerate(x):
        print(f"k={i}: {row}")
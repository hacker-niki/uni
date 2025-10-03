import numpy as np

def direct_run(A, P, Q):
    #С - матрица кол единиц ресурса,
    # кот нужно дать p-му для max прибыли, при распределении q ресурсов между p агентами
    C = np.copy(np.zeros(np.shape(A)))
    
    #B - функция(матрица Беллмана) максимальная прибыль при распр q между p первыми агентами
    B = np.copy(np.zeros(np.shape(A))) 

    for p in range(1, P + 1):
        for q in range(0, Q + 1):
            max = 0
            #случай 1 агента
            if p == 1:
                B[p, q] = A[p, q]
                C[p, q] = q
            else:
                #поиск максимальной прибыли
                for i in range(0, q + 1):
                    # прибыль = прибыль p-го + прибыль всех p-1 агентов
                    temp = A[p, i] + B[p - 1, q - i]
                    if temp > max:
                        max = temp
                        B[p, q] = max
                        # запоминаем опт значение
                        C[p, q] = i 
    return B, C

def reverse_run(C, P, Q):
    #распределение ресурсов по агентам
    dist = np.zeros(P + 1)
    #оставшиемя ресурчы
    left_q = Q
    #текущий агент
    cur_p = P
    
    while cur_p > 0:
        #опт кол ресурсов для cur_p 
        res = C[cur_p, int(left_q)]
        dist[cur_p] = res
        left_q = left_q - res
        cur_p = cur_p - 1
    return dist 

if __name__ == "__main__":
    P, Q = 3, 3

    A = np.array([[0, 0, 0, 0], #пустая строка агентов(для упрощения кода)
                [0, 1, 2, 3],
                [0, 0, 1, 2],
                [0, 2, 2, 3]])

    B, C = direct_run(A, P, Q)
    print('Matrix B: ',B)
    print('Matrix C: ',C)

    res = reverse_run(C, P, Q)

    for i in range(1, len(res)):
        print('Agent: ', i, ' res: ', int(res[i]), " cost: ", A[i][int(res[i])])

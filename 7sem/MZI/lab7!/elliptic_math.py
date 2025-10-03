

# Формулы получаются из подстановки уравнения касательной/секущей и далее по Виета находится новая точка
def point_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    
    x1, y1 = P
    x2, y2 = Q
    
    if x1 == x2 and y1 != y2:
        return None
    
    if x1 == x2:
        m = (3 * x1 * x1 + a) * pow(2 * y1, p-2, p) % p
    else:
        m = (y2 - y1) * pow(x2 - x1, p-2, p) % p
    
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    
    return (x3, y3)

# В to_add всегда кратно 2 Point. Далее в соответствии с битами добавляем в результат и получаем kPoint
def point_mult(k, point, a, p):
    result = None
    to_add = point
    
    while k:
        if k & 1:
            result = point_add(result, to_add, a, p)
        to_add = point_add(to_add, to_add, a, p)
        k >>= 1
    
    return result
def point_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    
    x1, y1 = P
    x2, y2 = Q
    
    if x1 == x2 and y1 != y2:
        # P + (-P) = 0
        return None
    
    if x1 == x2:
        # Удвоение точки P + P
        # Наклон касательной
        m = (3 * x1 * x1 + a) * pow(2 * y1, -1, p)
    else:
        # Сложение разных точек
        # Наклон секущей
        m = (y2 - y1) * pow(x2 - x1, -1, p)
    
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    
    return (x3, y3)

def point_mult(k, point, a, p):
    result = None
    to_add = point
    
    while k:
        if k & 1: # Если текущий бит k равен 1
            result = point_add(result, to_add, a, p)
        # Удваиваем точку для следующего бита
        to_add = point_add(to_add, to_add, a, p)
        # Переходим к следующему биту
        k >>= 1
    
    return result

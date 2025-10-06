import random
def is_prime(n, k=5):
    # Четные числа, кроме 2, не являются простыми
    if n % 2 == 0:
        return False
    
    # Представляем n-1 в виде d * 2^r
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Проводим k раундов теста Миллера-Рабина
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def generate_q():
    while True:
        # Генерируем случайное 256-битное число
        q = random.getrandbits(256)
        # Обеспечиваем, чтобы число было в нужном диапазоне (254 - 256 бит)
        q = q % (2 ** 256) + 2 ** 254
        if is_prime(q):
            return q

def generate_p(q):
    return 2 * q + 1

def generate_g(p, q):
    for g in range(1, p):
        if pow(g, q, p) == 1:
            return g
    return -1


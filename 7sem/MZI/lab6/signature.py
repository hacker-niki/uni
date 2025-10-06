import random
from gost import GOST3411
import hashlib

HASH_ALGO = hashlib.sha256

def generate_signature(message, p, q, g, d):
    # Шаг 1 - Вычисление хэш-кода (используем SHA-256)
    h = HASH_ALGO(message.encode('utf-8')).digest()
    
    # Шаг 2 - Преобразование хэша в число e
    a = int.from_bytes(h, byteorder='big')
    e = a % q
    if e == 0:
        e = 1
    
    while True:
        # Шаг 3 - Генерация случайного числа k
        k = random.randint(1, q - 1)
        
        # Шаг 4 - Вычисление r = (g^k mod p) mod q
        r = pow(g, k, p) % q
        if r == 0:
            continue
        
        # Шаг 5 - Вычисление s = (r*d + k*e) mod q
        s = (r * d + k * e) % q
        if s == 0:
            continue
        
        return r, s, h

def verify_signature(message, p, q, g, Q, r, s):
    # Шаг 1 - Проверка границ r и s
    if not (0 < r < q and 0 < s < q):
        return False
    
    # Шаг 2 - Вычисление хэш-кода (используем SHA-256)
    h = HASH_ALGO(message.encode('utf-8')).digest()
    
    # Шаг 3 - Преобразование хэша в число e
    a = int.from_bytes(h, byteorder='big')
    e = a % q
    if e == 0:
        e = 1
    
    # Шаг 4 - Вычисление обратного элемента v = e^{-1} mod q
    v = pow(e, -1, q)
    
    # Шаг 5 - Вычисление z1 = s*v mod q, z2 = -r*v mod q
    z1 = (s * v) % q
    z2 = (-r * v) % q
    
    # Шаг 6 - Вычисление R = (g^z1 * Q^z2 mod p) mod q
    C = (pow(g, z1, p) * pow(Q, z2, p)) % p
    R = C % q
    
    # Шаг 7 - Проверка R == r
    return R == r

import random
from gost import GOST3411

def generate_signature(message, p, q, g, d):
    """
    Генерирует цифровую подпись для сообщения.
    
    Args:
        message (str): Сообщение для подписания
        p, q (int): Простые числа, параметры криптосистемы
        g (int): Генератор группы
        d (int): Закрытый ключ (случайное число от 1 до q-1)
    
    Returns:
        tuple: (r, s, h) - компоненты подписи и хеш сообщения
    
    Процесс подписания:
    1. Вычисляем хеш сообщения
    2. Преобразуем хеш в число e
    3. Генерируем случайное k
    4. Вычисляем r = (g^k mod p) mod q
    5. Вычисляем s = (r*d + k*e) mod q
    """
    # Шаг 1 - Вычисление хэш-кода
    h = bytes(GOST3411.hash(message.encode('utf-8')))
    
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
    """
    Проверяет цифровую подпись сообщения.
    
    Args:
        message (str): Подписанное сообщение
        p, q (int): Простые числа, параметры криптосистемы
        g (int): Генератор группы
        Q (int): Открытый ключ (g^d mod p)
        r, s (int): Компоненты подписи
    
    Returns:
        bool: True если подпись верна, False в противном случае
    
    Процесс проверки:
    1. Проверяем границы r и s
    2. Вычисляем хеш сообщения и преобразуем в число e
    3. Вычисляем v = e^{-1} mod q
    4. Вычисляем z1 = s*v mod q, z2 = -r*v mod q
    5. Вычисляем R = (g^z1 * Q^z2 mod p) mod q
    6. Проверяем R == r
    """
    # Шаг 1 - Проверка границ r и s
    if not (0 < r < q and 0 < s < q):
        return False
    
    # Шаг 2 - Вычисление хэш-кода
    h = bytes(GOST3411.hash(message.encode('utf-8')))
    
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
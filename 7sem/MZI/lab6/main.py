import random
import hashlib 

# Используем SHA-256
HASH_ALGO = hashlib.sha256 

# --- Начало модуля primes.py (исправлена generate_g) ---
def is_prime(n, k=5):
    # ... (стандартная реализация)
    if n % 2 == 0: return False
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def generate_q():
    while True:
        q = random.getrandbits(256)
        q = q % (2 ** 256) + 2 ** 254
        if is_prime(q): return q

def generate_p(q):
    return 2 * q + 1

def generate_g(p, q):
    """Генерирует генератор g подгруппы порядка q для p=2q+1."""
    while True:
        # 1. Выбрать случайное h
        h = random.randint(2, p - 2)
        
        # 2. Вычислить g = h^2 mod p
        g = pow(h, 2, p)
        
        # 3. Проверить g != 1. Если g=1, выбрать другой h.
        if g != 1:
            return g
# --- Конец модуля primes.py ---


# --- Начало модуля signature.py (без изменений, кроме удаления GOST3411) ---
def generate_signature(message, p, q, g, d):
    h = HASH_ALGO(message.encode('utf-8')).digest()
    a = int.from_bytes(h, byteorder='big')
    e = a % q
    if e == 0: e = 1
    
    while True:
        k = random.randint(1, q - 1)
        r = pow(g, k, p) % q
        if r == 0: continue
        s = (r * d + k * e) % q
        if s == 0: continue
        return r, s, h

def verify_signature(message, p, q, g, Q, r, s):
    # Шаг 1: Проверка границ r и s
    if not (0 < r < q and 0 < s < q): return False
    
    # Шаги 2-3: Хэш и e
    h = HASH_ALGO(message.encode('utf-8')).digest()
    a = int.from_bytes(h, byteorder='big')
    e = a % q
    if e == 0: e = 1
    
    # Шаги 4-5: v, z1, z2
    v = pow(e, -1, q)
    z1 = (s * v) % q
    z2 = (-r * v) % q # Python корректно обрабатывает отрицательные числа по модулю
    
    # Шаг 6: Вычисление R = (g^z1 * Q^z2 mod p) mod q
    C = (pow(g, z1, p) * pow(Q, z2, p)) % p
    R = C % q
    
    # Шаг 7: Проверка R == r
    return R == r

# --- Конец модуля signature.py ---


# --- Начало модуля main.py (для тестирования) ---
def main():
    message_original = "Это тестовое сообщение для цифровой подписи."
    message_wrong = "non" # Неправильное сообщение для проверки

    print(f"Исходное сообщение: {message_original}")
    print("Генерация параметров криптосистемы...")
    q = generate_q()
    p = generate_p(q)
    g = generate_g(p, q)
    
    # Генерация ключевой пары
    d = random.randint(1, q - 1)  # Закрытый ключ
    Q = pow(g, d, p)  # Открытый ключ
    
    print(f"Параметры: p: {p.bit_length()} бит, q: {q.bit_length()} бит")
    print(f"Публичный ключ Q: {Q}")
    
    print("\nГенерация подписи...")
    # Подписываем ОРИГИНАЛЬНОЕ сообщение
    r, s, text_hash = generate_signature(message_original, p, q, g, d) 
    
    # Вывод данных
    print(f"Подпись (r, s): r={r}, s={s}")
    print(f"Подпись (hex): {r:X}{s:X}")
    
    # ПРОВЕРКА 1: Проверка подписи с ПРАВИЛЬНЫМ сообщением (должна пройти)
    print("\nПроверка подписи (корректное сообщение)...")
    is_valid_correct = verify_signature(message_original, p, q, g, Q, r, s)
    print(f"Signature valid (correct message): {is_valid_correct}")

    # ПРОВЕРКА 2: Проверка подписи с НЕПРАВИЛЬНЫМ сообщением (должна НЕ пройти)
    print(f"\nПроверка подписи (некорректное сообщение: '{message_wrong}')...")
    is_valid_wrong = verify_signature(message_wrong, p, q, g, Q, r, s)
    print(f"Signature valid (wrong message): {is_valid_wrong}")

if __name__ == "__main__":
    main()

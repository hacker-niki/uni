import random
from primes import generate_q, generate_p, generate_g
from signature import generate_signature, verify_signature

def main():
    """
    Основная функция, демонстрирующая процесс:
    1. Генерации параметров криптосистемы
    2. Создания цифровой подписи
    3. Проверки цифровой подписи
    """
    # Исходное сообщение для подписания
    message = "Calm. Kindness. Kinship. Love."
    
    # Генерация параметров криптосистемы
    print("Генерация параметров криптосистемы...")
    q = generate_q()  # Генерируем простое число q
    p = generate_p(q)  # Вычисляем p = 2q + 1
    g = generate_g(p, q)  # Находим генератор группы
    
    # Генерация ключевой пары
    d = random.randint(1, q - 1)  # Закрытый ключ
    Q = pow(g, d, p)  # Открытый ключ
    
    # Генерация подписи
    print("Генерация подписи...")
    r, s, text_hash = generate_signature(message, p, q, g, d)
    
    # Форматирование подписи и хеша для вывода
    signature = f"{r:X}{s:X}"
    print(f"Hash: {''.join(f'{x:02x}' for x in text_hash)}")
    print(f"Signature: {signature}")
    
    # Проверка подписи
    print("Проверка подписи...")
    is_valid = verify_signature(message, p, q, g, Q, r, s)
    print(f"Signature valid: {is_valid}")

if __name__ == "__main__":
    main()
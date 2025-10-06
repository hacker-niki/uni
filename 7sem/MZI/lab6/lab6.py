import random
from primes import generate_q, generate_p, generate_g
from signature import generate_signature, verify_signature

def main():
    message_original = "Раскуривание гостов..."
    message_wrong = "Раскуривание гостов"

    print(f"Исходное сообщение: {message_original}")
    print("Генерация параметров криптосистемы...")
    q = generate_q()
    p = generate_p(q)
    g = generate_g(p, q)
    
    d = random.randint(1, q - 1)  # Закрытый ключ
    Q = pow(g, d, p)  # Открытый ключ
    
    print("Генерация подписи...")
    r, s, text_hash = generate_signature(message_original, p, q, g, d) 
    
    signature = f"{r:X}{s:X}"
    print(f"Hash (оригинального сообщения): {''.join(f'{x:02x}' for x in text_hash)}")
    print(f"Signature: {signature}")
    
    print("\nПравильное")
    is_valid_correct = verify_signature(message_original, p, q, g, Q, r, s)
    print(f"Signature valid (correct message): {is_valid_correct}")

    print(f"\nНеправильное: {message_wrong}")
    is_valid_wrong = verify_signature(message_wrong, p, q, g, Q, r+1, s)
    print(f"Signature valid (wrong message): {is_valid_wrong}")

if __name__ == "__main__":
    main()

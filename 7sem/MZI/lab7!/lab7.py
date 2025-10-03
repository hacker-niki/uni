import random
from elliptic_math import point_add, point_mult

# y^2 = (x^3 + ax + b) mod p
#https://habr.com/ru/articles/335906/

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
G = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
      0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


# S = d_A×H_B
# C = M + d_A×H_B
def encrypt_message(message, d_A,H_B):
    message_num = int.from_bytes(message.encode(), 'big')
    S = point_mult(d_A, H_B, a, p)
    C_x = (message_num + S[0]) % p
    C_y = S[1] % p
    return (C_x, C_y)

# S = d_B × H_A = d_B × (d_A×G) = d_A × (d_B×G) = d_A×Q
# M = C_x - S_x = (M + d_A×Q_x) - (d_A×Q_x)
def decrypt_message(C, d_B, H_A):
    S = point_mult(d_B, H_A, a, p)
    message_num = (C[0] - S[0]) % p
    try:
        byte_length = (message_num.bit_length() + 7) // 8
        if byte_length == 0:
            return ""
        message = message_num.to_bytes(byte_length, 'big').decode()
        return message
    except:
        return "Ошибка дешифрования"

if __name__ == "__main__":
    d_A = random.randint(1, n-1) # приватный ключ Алисы
    d_B = random.randint(1, n-1) #приватный ключ Боба
    H_A = point_mult(d_A, G, a, p) #публичный ключ Алисы
    H_B = point_mult(d_B, G, a, p) #публичный ключ Боба

    message = "Calm Kindness Kinship Love"
    
    print(f"Исходное сообщение: {message}")

    ciphertext = encrypt_message(message, d_A, H_B)
    print(f"\nЗашифрованное сообщение:")
    print(f"Шифртекст: {ciphertext}")
    
    decrypted_message = decrypt_message(ciphertext, d_B, H_A)
    print(f"\nДешифрованное сообщение: {decrypted_message}")
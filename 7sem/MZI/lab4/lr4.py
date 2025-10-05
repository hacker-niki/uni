import random
import numpy as np

# --- Определение и генерация ключевых матриц ---

# Проверочная матрица H для кода Хэмминга (7,4)
H = np.array([[1, 0, 1, 0, 1, 0, 1],
              [0, 1, 1, 0, 0, 1, 1],
              [0, 0, 0, 1, 1, 1, 1]])

# Порождающая матрица G для кода Хэмминга (7,4)
G = np.array([[1, 1, 0, 1],
              [1, 0, 1, 1],
              [1, 0, 0, 0],
              [0, 1, 1, 1],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

# Матрица R для извлечения информационных битов из кодового слова
R = np.array([[0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 1]])

def generate_keys():
    """
    Генерирует все необходимые матрицы (ключи) для шифрования и дешифрования.
    Возвращает словарь с открытым и закрытым ключами.
    """
    # S - случайная невырожденная матрица (4x4)
    s_matrix = random_binary_non_singular_matrix(4)
    s_inv_matrix = np.linalg.inv(s_matrix).astype(int)

    # P - случайная матрица перестановок (7x7)
    p_matrix = generate_permutation_matrix(7)
    p_inv_matrix = np.linalg.inv(p_matrix).astype(int)

    # G_hat - открытый ключ
    g_hat_matrix = np.mod(s_matrix.dot(G).dot(p_matrix), 2)
    
    public_key = g_hat_matrix
    # Закрытый ключ состоит из трех частей, необходимых для дешифрования
    private_key = {'S_inv': s_inv_matrix, 'P_inv': p_inv_matrix}

    return public_key, private_key

# --- Вспомогательные функции ---

def random_binary_non_singular_matrix(n):
    """Генерирует случайную бинарную невырожденную матрицу размера n x n."""
    a = np.random.randint(0, 2, size=(n, n))
    while np.linalg.det(a) % 2 == 0:
        a = np.random.randint(0, 2, size=(n, n))
    return a

def generate_permutation_matrix(n):
    """Генерирует случайную матрицу перестановок размера n x n."""
    i = np.eye(n, dtype=int)
    p = np.random.permutation(i)
    return p

def text_to_binary(text):
    """Преобразует строку в бинарное представление (строку из '0' и '1')."""
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def binary_to_text(binary_str):
    """Преобразует бинарную строку в обычный текст."""
    byte_chunks = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    bytes_list = [int(chunk, 2) for chunk in byte_chunks]
    return bytearray(bytes_list).decode('utf-8', errors='ignore')

# --- Основная логика шифрования и дешифрования ---

def encrypt_file(input_filename, output_filename, public_key):
    """
    Шифрует содержимое входного файла и сохраняет результат в выходной файл.
    """
    print(f"Начинается шифрование файла '{input_filename}'...")

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_filename}' не найден.")
        return

    binary_str = text_to_binary(text)
    
    # Дополняем строку нулями, чтобы ее длина была кратна 4
    if len(binary_str) % 4 != 0:
        padding = '0' * (4 - len(binary_str) % 4)
        binary_str += padding

    # Разбиваем бинарную строку на блоки по 4 бита
    blocks = [binary_str[i:i+4] for i in range(0, len(binary_str), 4)]
    
    encrypted_message = []
    for block in blocks:
        # 1. Преобразуем блок в вектор numpy
        p = np.array([int(x) for x in block])
        # 2. Кодируем вектор с помощью G_hat (открытого ключа)
        encoded_bits = np.mod(p.dot(public_key), 2)
        # 3. Вносим одну случайную ошибку
        error_vector = np.zeros(7, dtype=int)
        error_position = random.randint(0, 6)
        error_vector[error_position] = 1
        bits_with_error = np.mod(encoded_bits + error_vector, 2)
        
        encrypted_message.append(''.join(map(str, bits_with_error)))

    # Записываем зашифрованные данные в файл
    with open(output_filename, 'w') as f:
        f.write(''.join(encrypted_message))
        
    print(f"Шифрование завершено. Шифртекст сохранен в '{output_filename}'.")

def decrypt_file(input_filename, output_filename, private_key):
    """
    Дешифрует содержимое входного файла и сохраняет результат в выходной файл.
    """
    print(f"Начинается дешифрование файла '{input_filename}'...")

    try:
        with open(input_filename, 'r') as f:
            encrypted_str = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_filename}' не найден.")
        return

    # Извлекаем ключи
    S_inv = private_key['S_inv']
    P_inv = private_key['P_inv']

    # Разбиваем шифротекст на блоки по 7 бит
    blocks = [encrypted_str[i:i+7] for i in range(0, len(encrypted_str), 7)]
    
    decrypted_message = []
    for block in blocks:
        c = np.array([int(x) for x in block])
        
        # 1. Вычисляем c_hat = c * P_inv
        c_hat = np.mod(c.dot(P_inv), 2)
        
        # 2. Вычисляем синдром для поиска ошибки: s = H * c_hat^T
        syndrome = np.mod(H.dot(c_hat), 2)
        
        # 3. Находим позицию ошибки по синдрому
        # (столбцы H соответствуют синдромам для ошибок в позициях 1-7)
        error_pos = -1
        for i in range(H.shape[1]):
            if np.array_equal(syndrome, H[:, i]):
                error_pos = i
                break
        
        # 4. Исправляем ошибку, если она найдена
        if error_pos != -1:
            c_hat[error_pos] = (c_hat[error_pos] + 1) % 2

        # 5. Декодируем исправленное кодовое слово матрицей R
        m_hat = np.mod(c_hat.dot(R.T), 2)
        
        # 6. Восстанавливаем исходное сообщение: m = m_hat * S_inv
        m_out = np.mod(m_hat.dot(S_inv), 2)
        
        decrypted_message.append(''.join(map(str, m_out)))
        
    decrypted_binary_str = ''.join(decrypted_message)
    decrypted_text = binary_to_text(decrypted_binary_str)
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
        
    print(f"Дешифрование завершено. Результат сохранен в '{output_filename}'.")


def main():
    """
    Основная функция для демонстрации работы шифрования и дешифрования.
    """
    # Имена файлов
    source_file = "plaintext.txt"
    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"
    
    # 1. Генерируем открытый и закрытый ключи
    public_key, private_key = generate_keys()
    
    # 2. Создаем исходный текстовый файл
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write("Это тестовое сообщение для демонстрации работы криптосистемы Мак-Элиса.\n")
        f.write("Проверка работы с несколькими строками и знаками препинания!")
    
    print(f"Создан исходный файл '{source_file}'.")
    
    # 3. Шифруем файл
    encrypt_file(source_file, encrypted_file, public_key)
    
    # 4. Дешифруем файл
    decrypt_file(encrypted_file, decrypted_file, private_key)
    
    # 5. Сравниваем исходный и дешифрованный файлы
    with open(source_file, 'r', encoding='utf-8') as f1, open(decrypted_file, 'r', encoding='utf-8') as f2:
        original = f1.read()
        decrypted = f2.read()
        
        print("\n--- Проверка ---")
        if original == decrypted:
            print("Успех! Исходный и дешифрованный тексты полностью совпадают.")
        else:
            print("Ошибка! Тексты не совпадают.")

if __name__ == '__main__':
    main()

import struct


class SHA1:
    @staticmethod
    def hash(message_bytes):
        # Константы, инициализация
        A = 0x67452301
        B = 0xEFCDAB89
        C = 0x98BADCFE
        D = 0x10325476
        E = 0xC3D2E1F0

        # Дополнение сообщения 
        bytes_ = bytearray(message_bytes)
        bytes_.append(0x80)  # Добавление 1 в начале

        # Дополнение нулями до длины, кратной 512 битам (делается всегда)
        while len(bytes_) % 64 != 56:
            bytes_.append(0x00)

        # Добавление длины иcходного сообщения (в битах) в конец сообщения
        message_length_bits = len(message_bytes) * 8 #размер в байтах * 8
        bytes_.extend(struct.pack('>Q', message_length_bits))  # Преобразуем к big-endian(старший байт впереди), если система little-endian

        # Разделение сообщения на блоки по 512 бит (64 байта)
        for i in range(0, len(bytes_), 64):
            # Создание массива из 80 слов по 32 бита
            w = [0] * 80

            # Перенос блока в первые 16 слов
            for j in range(16):
                w[j] = struct.unpack('>I', bytes_[i + j * 4:i + j * 4 + 4])[0]

            # Дополнение массива до 80 слов
            for j in range(16, 80):
                w[j] = SHA1.rotate_left( w[j - 16] ^ w[j - 14] ^ w[j - 8] ^ w[j - 3], 1)

            # Инициализация переменных для текущего блока
            a, b, c, d, e = A, B, C, D, E

            # Основной цикл обработки
            for j in range(80):
                if j < 20:
                    f = (b & c) | (~b & d)
                    k = 0x5A827999
                elif j < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif j < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                else:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                temp = (SHA1.rotate_left(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
                a, b, c, d, e = temp, a, SHA1.rotate_left(b, 30), c, d 

            # Добавление результатов к текущим переменным и модуль 2^32 для каждого отдельно
            A = (A + a) & 0xFFFFFFFF
            B = (B + b) & 0xFFFFFFFF
            C = (C + c) & 0xFFFFFFFF
            D = (D + d) & 0xFFFFFFFF
            E = (E + e) & 0xFFFFFFFF

        # Склейка h0, h1, h2, h3, h4 в итоговый хэш
        hash_bytes = struct.pack('>5I', A, B, C, D, E)
        return hash_bytes

    #Метод для циулического сдвига влево
    @staticmethod
    def rotate_left(value, bits):
        return ((value << bits) | (value >> (32 - bits))) & 0xFFFFFFFF
<?php
// Устанавливаем заголовок, чтобы клиент точно знал, что это JSON
header('Content-Type: application/json');

// Проверяем, установлено ли расширение GMP, без него ничего не будет работать
if (!extension_loaded('gmp')) {
    echo json_encode(['success' => false, 'error' => 'Расширение PHP GMP не установлено. Оно необходимо для работы с большими числами.']);
    exit;
}

/**
 * Отправляет успешный JSON-ответ
 * @param array $data
 */
function send_success($data) {
    echo json_encode(['success' => true, 'data' => $data]);
    exit;
}

/**
 * Отправляет JSON-ответ с ошибкой
 * @param string $message
 */
function send_error($message) {
    echo json_encode(['success' => false, 'error' => $message]);
    exit;
}

/**
 * Генерирует простое число p, такое что p ≡ 3 (mod 4)
 * @param int $bitLength
 * @return GMP
 */
function generate_prime($bitLength) {
    do {
        // Генерируем случайное число нужной битности
        $bits = gmp_init(str_repeat('1', $bitLength), 2);
        $num = gmp_random_range(gmp_init(0), $bits);
        // Устанавливаем старший и младший биты в 1, чтобы число было нечетным и нужной длины
        gmp_setbit($num, $bitLength - 1);
        gmp_setbit($num, 0);

        // Ищем следующее простое число, которое удовлетворяет условию p % 4 == 3
        while (gmp_cmp(gmp_mod($num, 4), 3) != 0) {
            $num = gmp_add($num, 2); // Проверяем только нечетные
        }

        // Проверяем на простоту с помощью теста Миллера-Рабина (50 итераций - очень надежно)
        while (gmp_prob_prime($num, 50) == 0) {
            $num = gmp_add($num, 4); // Следующий кандидат, который будет p % 4 == 3
        }

    } while (gmp_prob_prime($num, 50) == 0);
    return $num;
}

/**
 * Расширенный алгоритм Евклида для нахождения модулярного обратного.
 * Находит y и z такие, что p*y + q*z = 1
 * @param GMP $p
 * @param GMP $q
 * @return array [g, y, z]
 */
function extended_gcd(GMP $p, GMP $q) {
    if (gmp_cmp($p, 0) == 0) {
        return [$q, gmp_init(0), gmp_init(1)];
    }
    list($g, $y, $x) = extended_gcd(gmp_mod($q, $p), $p);
    return [$g, gmp_sub($x, gmp_mul(gmp_div($q, $p), $y)), $y];
}

// ===================================================================
// ГЛАВНЫЙ МАРШРУТИЗАТОР ЗАПРОСОВ
// ===================================================================

if (isset($_POST['generate'])) {
    $bitLength = isset($_POST['bitLength']) ? (int)$_POST['bitLength'] : 512;
    if ($bitLength <= 0) {
        send_error("Некорректная длина ключа.");
    }

    $p = generate_prime($bitLength);
    $q = generate_prime($bitLength);

    // Убедимся, что p и q не равны
    while (gmp_cmp($p, $q) == 0) {
        $q = generate_prime($bitLength);
    }

    $n = gmp_mul($p, $q); // Публичный ключ N

    send_success([
        'keys' => [
            'public' => gmp_strval($n, 16),
            'private' => [
                'p' => gmp_strval($p, 16),
                'q' => gmp_strval($q, 16)
            ]
        ]
    ]);
}

if (isset($_POST['encrypt'])) {
    // 1. Проверяем, что все данные пришли и не пустые
    if (empty($_POST['message']) || empty($_POST['public_key_n'])) {
        send_error("Сообщение и публичный ключ (N) не могут быть пустыми.");
    }

    $m_hex = $_POST['message'];
    $n_hex = $_POST['public_key_n'];

    // 2. Конвертируем HEX в GMP объекты
    $m = gmp_init($m_hex, 16);
    $n = gmp_init($n_hex, 16);

    // 3. Проверяем условие M < N
    if (gmp_cmp($m, $n) >= 0) {
        send_error("Ошибка: Сообщение (M) должно быть меньше публичного ключа (N).");
    }

    // 4. Шифруем: C = M^2 mod N
    $c = gmp_powm($m, 2, $n);

    send_success(['ciphertext' => gmp_strval($c, 16)]);
}

if (isset($_POST['decrypt'])) {
    // 1. ГЛАВНАЯ ПРОВЕРКА: Убедимся, что шифротекст НЕ ПУСТОЙ
    if (empty($_POST['ciphertext']) || empty($_POST['private_key_p']) || empty($_POST['private_key_q'])) {
        send_error("Шифротекст и приватные ключи (p, q) не могут быть пустыми.");
    }

    $c_hex = $_POST['ciphertext'];
    $p_hex = $_POST['private_key_p'];
    $q_hex = $_POST['private_key_q'];

    // 2. Конвертируем HEX в GMP объекты
    $c = gmp_init($c_hex, 16);
    $p = gmp_init($p_hex, 16);
    $q = gmp_init($q_hex, 16);
    $n = gmp_mul($p, $q);

    // 3. Вычисляем квадратные корни по модулю p и q
    // m_p^2 ≡ c (mod p) -> m_p = c^((p+1)/4) mod p
    $m_p = gmp_powm($c, gmp_div_q(gmp_add($p, 1), 4), $p);
    // m_q^2 ≡ c (mod q) -> m_q = c^((q+1)/4) mod q
    $m_q = gmp_powm($c, gmp_div_q(gmp_add($q, 1), 4), $q);

    // 4. Используем расширенный алгоритм Евклида для нахождения y_p и y_q
    // y_p*p + y_q*q = 1
    list($gcd, $y_p, $y_q) = extended_gcd($p, $q);

    // 5. Находим 4 возможных корня с помощью Китайской теоремы об остатках
    // r1 = (y_p*p*m_q + y_q*q*m_p) mod n
    $r1 = gmp_mod(gmp_add(gmp_mul(gmp_mul($y_p, $p), $m_q), gmp_mul(gmp_mul($y_q, $q), $m_p)), $n);
    // r2 = n - r1
    $r2 = gmp_sub($n, $r1);
    // r3 = (y_p*p*m_q - y_q*q*m_p) mod n
    $r3 = gmp_mod(gmp_sub(gmp_mul(gmp_mul($y_p, $p), $m_q), gmp_mul(gmp_mul($y_q, $q), $m_p)), $n);
    // r4 = n - r3
    $r4 = gmp_sub($n, $r3);

    send_success([
        'decrypted_roots' => [
            gmp_strval($r1, 16),
            gmp_strval($r2, 16),
            gmp_strval($r3, 16),
            gmp_strval($r4, 16)
        ]
    ]);
}

// Если ни один из флагов не был установлен
send_error('Неизвестное действие.');
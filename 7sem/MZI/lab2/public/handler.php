<?php

use App\STB34101312011;

session_start();

// Подключаем класс. Убедитесь, что путь правильный.
// Если вы используете Composer, он должен найти его автоматически.

// Если используете Composer с неймспейсами, то:
// require_once __DIR__ . '/../vendor/autoload.php';
// use App\STB34101312011;

// Для примера без Composer, предполагаем, что класс в том же файле.
// Для работы с Request/Response от Symfony, Composer необходим.
// Упростим для примера без него, используя стандартные функции PHP.

// --- Получение данных из запроса ---
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit;
}

$key_input = $_POST['key'] ?? '';
$uploadedFile = $_FILES['inputFile'] ?? null;
$_SESSION['key_input'] = $key_input;

try {
    if (strlen($key_input) !== 32) {
        throw new Exception("Ключ должен содержать ровно 32 символа.");
    }

    if (!$uploadedFile || $uploadedFile['error'] !== UPLOAD_ERR_OK) {
        throw new Exception("Ошибка загрузки файла. Код ошибки: " . ($uploadedFile['error'] ?? 'неизвестно'));
    }

    $file_content = file_get_contents($uploadedFile['tmp_name']);
    $original_filename = $uploadedFile['name'];

    // Преобразуем строковый ключ в формат, необходимый для алгоритма
    $numeric_key = STB34101312011::keyFromString($key_input);

    if (isset($_POST['encrypt'])) {
        // Дополняем данные до размера, кратного 16 байтам (длина блока)
        $padded_length = ceil(strlen($file_content) / 16) * 16;
        $padded_content = str_pad($file_content, $padded_length, ' ', STR_PAD_RIGHT);

        $encrypted_data = STB34101312011::encrypt($padded_content, $numeric_key);

        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . $original_filename . '.enc"');
        header('Content-Length: ' . strlen($encrypted_data));
        echo $encrypted_data;
        exit;
    }

    if (isset($_POST['decrypt'])) {
        if (strlen($file_content) % 16 !== 0) {
            throw new Exception("Размер зашифрованного файла должен быть кратен 16 байтам.");
        }

        $decrypted_data = STB34101312011::decrypt($file_content, $numeric_key);

        // Убираем дополнение (пробелы в конце)
        $unpadded_data = rtrim($decrypted_data);

        // Формируем имя расшифрованного файла
        $decrypted_filename = preg_replace('/\.enc$/i', '', $original_filename);
        if ($decrypted_filename === $original_filename) {
            $decrypted_filename = 'decr_' . $original_filename;
        }

        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . $decrypted_filename . '"');
        header('Content-Length: ' . strlen($unpadded_data));
        echo $unpadded_data;
        exit;
    }

} catch (Exception $e) {
    $_SESSION['error'] = $e->getMessage();
}

header('Location: index.php');
exit;
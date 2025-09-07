<?php
session_start();

require_once __DIR__ . '/../vendor/autoload.php';

use App\GostEncrypt;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$request = Request::createFromGlobals();
if (!$request->isMethod('POST')) {
    // Если кто-то зашел на этот файл напрямую, перенаправляем на главную
    header('Location: index.php');
    exit;
}

$key_input = $request->request->get('key');
/** @var \Symfony\Component\HttpFoundation\File\UploadedFile|null $uploadedFile */
$uploadedFile = $request->files->get('inputFile');

$_SESSION['key_input'] = $key_input;

try {
    if (strlen($key_input) !== 32) {
        throw new Exception("Ключ должен содержать ровно 32 символа.");
    }

    if (!$uploadedFile || !$uploadedFile->isValid()) {
        throw new Exception("Ошибка загрузки файла. Пожалуйста, выберите корректный файл.");
    }

    $file_content = $uploadedFile->getContent();
    $original_filename = $uploadedFile->getClientOriginalName();

    $gost = new GostEncrypt();

    if ($request->request->has('encrypt')) {
        $encrypted_data = $gost->encrypt($file_content, $key_input);
        $response = new Response($encrypted_data);
        $response->headers->set('Content-Type', 'application/octet-stream');
        $response->headers->set('Content-Disposition', 'attachment; filename="' . $original_filename . '.enc"');

        $response->send();
        exit; // Важно завершить выполнение скрипта после отправки файла
    }

    if ($request->request->has('decrypt')) {
        if (strlen($file_content) < 8) {
            throw new Exception("Файл слишком короткий для расшифрования с MAC.");
        }

        $mac_from_file = substr($file_content, -8);
        $encrypted_data = substr($file_content, 0, -8);
        $decrypted_data = $gost->decrypt($encrypted_data, $key_input);

        $decrypted_filename = preg_replace('/\.txt$/i', '', $original_filename);
        $response = new Response($decrypted_data);
        $response->headers->set('Content-Type', 'application/octet-stream');
        $response->headers->set('Content-Disposition', 'attachment; filename="decr_' . $decrypted_filename . '.txt"');

        $response->send();
        exit;
    }

} catch (Exception $e) {
    $_SESSION['error'] = $e->getMessage();
}

header('Location: index.php');
exit;

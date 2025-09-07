<?php
session_start();

$error = $_SESSION['error'] ?? '';
$result = $_SESSION['result'] ?? '';
$key_input = $_SESSION['key_input'] ?? 'This is a 32-byte key for GOST!';

unset($_SESSION['error'], $_SESSION['result'], $_SESSION['key_input']);
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>СТБ 34.101.31-2011 | Шифрование</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5 mb-5" style="max-width: 800px;">
    <div class="card shadow-sm">
        <h1 class="card-header bg-primary text-white p-3 text-center">СТБ 34.101.31-2011</h1>
        <div class="card-body p-4">
            <form action="handler.php" method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label for="inputFile" class="form-label fw-bold">1. Выберите файл</label>
                    <input class="form-control" type="file" name="inputFile" id="inputFile" required>
                </div>

                <div class="mb-4">
                    <label for="key" class="form-label fw-bold">2. Введите ключ (ровно 32 символа)</label>
                    <div class="input-group">
                        <input type="text" name="key" id="key" value="<?= htmlspecialchars($key_input) ?>" maxlength="32" class="form-control" required>
                        <button class="btn btn-outline-secondary" type="button" id="generateKeyBtn">Сгенерировать</button>
                    </div>
                </div>

                <div class="d-grid gap-3">
                    <div class="btn-group">
                        <button type="submit" name="encrypt" class="btn btn-primary btn-lg">Зашифровать файл</button>
                        <button type="submit" name="decrypt" class="btn btn-success btn-lg">Расшифровать файл</button>
                    </div>
                </div>
            </form>

            <?php if ($error): ?>
                <div class="alert alert-danger mt-4" role="alert">
                    <strong>Ошибка:</strong> <?= htmlspecialchars($error) ?>
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<script>
    document.getElementById('generateKeyBtn').addEventListener('click', function() {
        const charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=_+[]{}|;:,.<>?';
        let newKey = '';
        const randomValues = new Uint32Array(32);
        window.crypto.getRandomValues(randomValues);
        for (let i = 0; i < 32; i++) {
            newKey += charset[randomValues[i] % charset.length];
        }
        document.getElementById('key').value = newKey;
    });
</script>
</body>
</html>
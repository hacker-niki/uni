<?php session_start(); ?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Криптосистема Рабина</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .monospace { font-family: monospace; word-break: break-all; }
        .form-section { border: 1px solid #ddd; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 2rem; }
        .spinner-border { display: none; }
        .btn.loading .spinner-border { display: inline-block; }
    </style>
</head>
<body class="bg-light">
<div class="container mt-5 mb-5" style="max-width: 900px;">
    <div class="card shadow-sm">
        <h1 class="card-header bg-primary text-white p-3 text-center">Криптосистема Рабина</h1>
        <div class="card-body p-4">

            <div id="error-container" class="alert alert-danger" style="display: none;" role="alert"></div>

            <!-- Секция 1: Генерация ключей -->
            <div class="form-section">
                <h3 class="mb-3">1. Генерация ключей</h3>
                <form id="generate-form" action="handler.php" method="post">
                    <div class="mb-3">
                        <label for="bitLength" class="form-label">Длина ключа (для p и q, в битах)</label>
                        <select name="bitLength" id="bitLength" class="form-select">
                            <option value="256">256 бит</option>
                            <option value="512" selected>512 бит</option>
                            <option value="1024">1024 бит</option>
                        </select>
                    </div>
                    <button type="submit" name="generate" class="btn btn-primary w-100">
                        <span class="spinner-border spinner-border-sm"></span> Сгенерировать ключи
                    </button>
                </form>
                <div id="generate-result" class="mt-4"></div>
            </div>

            <!-- Секция 2: Шифрование -->
            <div class="form-section">
                <h3 class="mb-3">2. Шифрование</h3>
                <form id="encrypt-form" action="handler.php" method="post">
                    <div class="mb-3">
                        <label for="message" class="form-label">Сообщение (в виде числа, HEX)</label>
                        <textarea name="message" id="message" class="form-control monospace" rows="3" required>123456789abcdef</textarea>
                    </div>
                    <div class="mb-3">
                        <label for="public_key_n" class="form-label">Публичный ключ (N, HEX)</label>
                        <textarea name="public_key_n" id="public_key_n" class="form-control monospace" rows="4" required></textarea>
                    </div>
                    <button type="submit" name="encrypt" class="btn btn-success w-100">
                        <span class="spinner-border spinner-border-sm"></span> Зашифровать
                    </button>
                </form>
                <div id="encrypt-result" class="mt-4"></div>
            </div>

            <!-- Секция 3: Дешифрование -->
            <div class="form-section">
                <h3 class="mb-3">3. Дешифрование</h3>
                <form id="decrypt-form" action="handler.php" method="post">
                    <div class="mb-3">
                        <label for="ciphertext" class="form-label">Шифротекст (HEX)</label>
                        <textarea name="ciphertext" id="ciphertext" class="form-control monospace" rows="4" required>123</textarea>
                    </div>
                    <div class="mb-3">
                        <label for="private_key_p" class="form-label">Приватный ключ (p, HEX)</label>
                        <textarea name="private_key_p" id="private_key_p" class="form-control monospace" rows="4" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="private_key_q" class="form-label">Приватный ключ (q, HEX)</label>
                        <textarea name="private_key_q" id="private_key_q" class="form-control monospace" rows="4" required></textarea>
                    </div>
                    <button type="submit" name="decrypt" class="btn btn-warning w-100">
                        <span class="spinner-border spinner-border-sm"></span> Расшифровать
                    </button>
                </form>
                <div id="decrypt-result" class="mt-4"></div>
            </div>
        </div>
    </div>
</div>

<script>
    async function handleFormSubmit(event) {
        event.preventDefault();

        const form = event.target;
        const button = form.querySelector('button[type="submit"]');
        const errorContainer = document.getElementById('error-container');
        errorContainer.style.display = 'none';

        // Проверка обязательных полей
        const requiredFields = form.querySelectorAll('[required]');
        for (const field of requiredFields) {
            if (!field.value.trim()) {
                errorContainer.textContent = `Ошибка: Поле "${field.previousElementSibling.textContent}" должно быть заполнено.`;
                errorContainer.style.display = 'block';
                return; // Прерываем отправку
            }
        }

        // Дополнительная проверка для формы дешифрования
        if (form.id === 'decrypt-form') {
            const ciphertext = form.querySelector('#ciphertext').value.trim();
            if (!ciphertext) {
                errorContainer.textContent = 'Ошибка: Шифротекст не может быть пустым.';
                errorContainer.style.display = 'block';
                return;
            }
            // Проверка формата HEX
            if (!/^[0-9A-Fa-f]+$/.test(ciphertext)) {
                errorContainer.textContent = 'Ошибка: Шифротекст должен быть в формате HEX (0-9, A-F).';
                errorContainer.style.display = 'block';
                return;
            }
        }

        const formData = new FormData(form);
        formData.append(button.name, '1');

        button.disabled = true;
        button.classList.add('loading');

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });
            const result = await response.json();

            if (result.success) {
                displayResult(form.id, result.data);
            } else {
                errorContainer.textContent = 'Ошибка: ' + result.error;
                errorContainer.style.display = 'block';
            }
        } catch (error) {
            errorContainer.textContent = 'Сетевая ошибка: ' + error.message;
            errorContainer.style.display = 'block';
        } finally {
            button.disabled = false;
            button.classList.remove('loading');
        }
    }

    function displayResult(formId, data) {
        if (formId === 'generate-form' && data.keys) {
            const resultDiv = document.getElementById('generate-result');
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    <h5 class="alert-heading">Ключи успешно сгенерированы!</h5>
                    <p><strong>Публичный ключ (N):</strong><br><small class="monospace">${data.keys.public}</small></p>
                    <hr>
                    <p><strong>Приватный ключ (p):</strong><br><small class="monospace">${data.keys.private.p}</small></p>
                    <p><strong>Приватный ключ (q):</strong><br><small class="monospace">${data.keys.private.q}</small></p>
                </div>`;
            document.getElementById('public_key_n').value = data.keys.public;
            document.getElementById('private_key_p').value = data.keys.private.p;
            document.getElementById('private_key_q').value = data.keys.private.q;
        } else if (formId === 'encrypt-form' && data.ciphertext) {
            const resultDiv = document.getElementById('encrypt-result');
            resultDiv.innerHTML = `
                <div class="alert alert-info">
                     <h5 class="alert-heading">Результат шифрования:</h5>
                     <p class="monospace">${data.ciphertext}</p>
                </div>`;
            // Убедимся, что шифротекст записывается в поле
            const ciphertextField = document.getElementById('ciphertext');
            ciphertextField.value = data.ciphertext.trim();
            if (!ciphertextField.value) {
                document.getElementById('error-container').textContent = 'Ошибка: Получен пустой шифротекст от сервера.';
                document.getElementById('error-container').style.display = 'block';
            }
        } else if (formId === 'decrypt-form' && data.decrypted_roots) {
            const resultDiv = document.getElementById('decrypt-result');
            let rootsHtml = data.decrypted_roots.map((root, index) =>
                `<p><strong>Вариант ${index + 1}:</strong><br><small class="monospace">${root}</small></p>`
            ).join('');
            resultDiv.innerHTML = `
                <div class="alert alert-dark">
                     <h5 class="alert-heading">Результаты дешифрования (4 возможных варианта):</h5>
                     ${rootsHtml}
                </div>`;
        }
    }

    document.getElementById('generate-form').addEventListener('submit', handleFormSubmit);
    document.getElementById('encrypt-form').addEventListener('submit', handleFormSubmit);
    document.getElementById('decrypt-form').addEventListener('submit', handleFormSubmit);
</script>

</body>
</html>

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

pages = {}

# Страницы администратора
pages["admin-users.html"] = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Управление пользователями</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Manrope,sans-serif;background:#f8fafc}.sidebar{width:250px;background:#0f172a;height:100vh;position:fixed;padding:20px;color:#fff}.logo{font-size:1.5rem;font-weight:700;margin-bottom:40px;color:#667eea}.nav-item{padding:12px 16px;border-radius:8px;margin-bottom:5px;cursor:pointer;transition:all .3s;display:flex;align-items:center;gap:10px}.nav-item:hover,.nav-item.active{background:rgba(102,126,234,.2)}.main{margin-left:250px;padding:30px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:30px}h1{font-size:2rem;font-weight:700;color:#0f172a}.btn{padding:12px 24px;border:none;border-radius:10px;font-weight:600;cursor:pointer;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff}.table-container{background:#fff;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,.05);overflow:hidden}table{width:100%;border-collapse:collapse}th{background:#f8fafc;padding:15px;text-align:left;font-weight:600;color:#334155;border-bottom:2px solid #e2e8f0}td{padding:15px;border-bottom:1px solid #e2e8f0}.avatar{width:35px;height:35px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:600;margin-right:10px}.role-badge{padding:4px 12px;border-radius:6px;font-size:.85rem;font-weight:600}.role-admin{background:#fce7f3;color:#be123c}.role-user{background:#dbeafe;color:#1e40af}.actions button{padding:8px 12px;border:none;border-radius:6px;cursor:pointer;margin:0 3px;font-size:.9rem}.btn-edit{background:#e0e7ff;color:#4338ca}.btn-delete{background:#fee2e2;color:#dc2626}</style>
</head>
<body>
<div class="sidebar"><div class="logo">📝 TestGen</div><div class="nav-item active">👥 Пользователи</div><div class="nav-item">📄 Документы</div><div class="nav-item">📝 Тесты</div><div class="nav-item">📊 Результаты</div><div class="nav-item">⚙️ Настройки</div></div>
<div class="main"><div class="header"><h1>Управление пользователями</h1><button class="btn">+ Добавить пользователя</button></div>
<div class="table-container"><table>
<thead><tr><th>Пользователь</th><th>Email</th><th>Роль</th><th>Группа</th><th>Дата создания</th><th>Действия</th></tr></thead>
<tbody>
<tr><td><span class="avatar">АП</span>Петров Алексей</td><td>petrov@company.com</td><td><span class="role-badge role-admin">Администратор</span></td><td>IT-отдел</td><td>15.01.2025</td><td class="actions"><button class="btn-edit">✏️ Изменить</button><button class="btn-delete">🗑️ Удалить</button></td></tr>
<tr><td><span class="avatar">ИИ</span>Иванов Иван</td><td>ivanov@company.com</td><td><span class="role-badge role-user">Пользователь</span></td><td>Разработка</td><td>20.01.2025</td><td class="actions"><button class="btn-edit">✏️ Изменить</button><button class="btn-delete">🗑️ Удалить</button></td></tr>
<tr><td><span class="avatar">СМ</span>Сидорова Мария</td><td>sidorova@company.com</td><td><span class="role-badge role-user">Пользователь</span></td><td>Аналитика</td><td>22.01.2025</td><td class="actions"><button class="btn-edit">✏️ Изменить</button><button class="btn-delete">🗑️ Удалить</button></td></tr>
<tr><td><span class="avatar">КД</span>Козлов Дмитрий</td><td>kozlov@company.com</td><td><span class="role-badge role-user">Пользователь</span></td><td>Разработка</td><td>25.01.2025</td><td class="actions"><button class="btn-edit">✏️ Изменить</button><button class="btn-delete">🗑️ Удалить</button></td></tr>
<tr><td><span class="avatar">НА</span>Новикова Анна</td><td>novikova@company.com</td><td><span class="role-badge role-user">Пользователь</span></td><td>QA</td><td>27.01.2025</td><td class="actions"><button class="btn-edit">✏️ Изменить</button><button class="btn-delete">🗑️ Удалить</button></td></tr>
</tbody>
</table></div></div>
</body></html>"""

pages["admin-create-test.html"] = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Создание теста</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Manrope,sans-serif;background:#f8fafc}.sidebar{width:250px;background:#0f172a;height:100vh;position:fixed;padding:20px;color:#fff}.logo{font-size:1.5rem;font-weight:700;margin-bottom:40px;color:#667eea}.nav-item{padding:12px 16px;border-radius:8px;margin-bottom:5px;cursor:pointer;display:flex;align-items:center;gap:10px}.nav-item.active{background:rgba(102,126,234,.2)}.main{margin-left:250px;padding:30px}.card{background:#fff;border-radius:16px;padding:30px;box-shadow:0 2px 10px rgba(0,0,0,.05);margin-bottom:20px}h1{font-size:2rem;font-weight:700;color:#0f172a;margin-bottom:30px}.form-group{margin-bottom:25px}label{display:block;font-weight:600;color:#334155;margin-bottom:8px}input,textarea,select{width:100%;padding:12px;border:2px solid #e2e8f0;border-radius:10px;font-family:Manrope,sans-serif;font-size:1rem}input:focus,textarea:focus,select:focus{outline:none;border-color:#667eea}textarea{min-height:100px;resize:vertical}.form-row{display:grid;grid-template-columns:1fr 1fr;gap:20px}.btn{padding:14px 28px;border:none;border-radius:10px;font-weight:600;cursor:pointer;font-size:1rem}.btn-primary{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff}.btn-secondary{background:#f1f5f9;color:#334155;margin-right:10px}.actions{display:flex;gap:10px;margin-top:30px}</style>
</head>
<body>
<div class="sidebar"><div class="logo">📝 TestGen</div><div class="nav-item">👥 Пользователи</div><div class="nav-item">📄 Документы</div><div class="nav-item active">📝 Тесты</div><div class="nav-item">📊 Результаты</div><div class="nav-item">⚙️ Настройки</div></div>
<div class="main">
<h1>Создание нового теста</h1>
<div class="card">
<form>
<div class="form-group"><label>Название теста *</label><input type="text" placeholder="Например: Основы Python" value="Основы Python"></div>
<div class="form-group"><label>Описание</label><textarea placeholder="Краткое описание содержания теста">Тест охватывает базовые конструкции языка Python: переменные, условия, циклы, функции и работу с коллекциями</textarea></div>
<div class="form-row">
<div class="form-group"><label>Ограничение по времени (минуты)</label><input type="number" value="45"></div>
<div class="form-group"><label>Количество попыток</label><select><option>Не ограничено</option><option selected>1 попытка</option><option>2 попытки</option><option>3 попытки</option></select></div>
</div>
<div class="form-row">
<div class="form-group"><label>Проходной балл (%)</label><input type="number" value="70"></div>
<div class="form-group"><label>Категория</label><select><option>Программирование</option><option selected>Базы данных</option><option>Аналитика</option></select></div>
</div>
<div class="actions"><button type="submit" class="btn btn-primary">Далее: Выбор вопросов →</button><button type="button" class="btn btn-secondary">Отмена</button></div>
</form>
</div>
</div>
</body></html>"""

pages["admin-results.html"] = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Результаты тестирования</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Manrope,sans-serif;background:#f8fafc}.sidebar{width:250px;background:#0f172a;height:100vh;position:fixed;padding:20px;color:#fff}.logo{font-size:1.5rem;font-weight:700;margin-bottom:40px;color:#667eea}.nav-item{padding:12px 16px;border-radius:8px;margin-bottom:5px;cursor:pointer;display:flex;align-items:center;gap:10px}.nav-item.active{background:rgba(102,126,234,.2)}.main{margin-left:250px;padding:30px}.test-info{background:#fff;border-radius:16px;padding:25px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center}.test-title{font-size:1.5rem;font-weight:700;color:#0f172a}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:20px}.stat-card{background:#fff;padding:20px;border-radius:12px;text-align:center}.stat-value{font-size:2rem;font-weight:700;color:#667eea}.stat-label{color:#64748b;font-size:.9rem;margin-top:5px}.table-container{background:#fff;border-radius:16px;overflow:hidden}table{width:100%;border-collapse:collapse}th{background:#f8fafc;padding:15px;text-align:left;font-weight:600;color:#334155;border-bottom:2px solid #e2e8f0}td{padding:15px;border-bottom:1px solid #e2e8f0}.avatar{width:35px;height:35px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:600;margin-right:10px}.score{font-weight:700;font-size:1.1rem}.score.high{color:#10b981}.score.medium{color:#f59e0b}.score.low{color:#ef4444}.status-badge{padding:4px 12px;border-radius:6px;font-size:.85rem;font-weight:600}.status-completed{background:#dcfce7;color:#166534}.status-progress{background:#fef3c7;color:#92400e}</style>
</head>
<body>
<div class="sidebar"><div class="logo">📝 TestGen</div><div class="nav-item">👥 Пользователи</div><div class="nav-item">📄 Документы</div><div class="nav-item">📝 Тесты</div><div class="nav-item active">📊 Результаты</div><div class="nav-item">⚙️ Настройки</div></div>
<div class="main">
<div class="test-info"><div><h2 class="test-title">Основы SQL</h2><p style="color:#64748b">Результаты прохождения теста</p></div><button style="padding:12px 24px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;border-radius:10px;font-weight:600;cursor:pointer">📥 Экспорт в Excel</button></div>
<div class="stats">
<div class="stat-card"><div class="stat-value">24</div><div class="stat-label">Всего попыток</div></div>
<div class="stat-card"><div class="stat-value">20</div><div class="stat-label">Завершено</div></div>
<div class="stat-card"><div class="stat-value">82%</div><div class="stat-label">Средний балл</div></div>
<div class="stat-card"><div class="stat-value">85%</div><div class="stat-label">Успешных</div></div>
</div>
<div class="table-container"><table>
<thead><tr><th>Пользователь</th><th>Группа</th><th>Статус</th><th>Балл</th><th>Время</th><th>Дата</th></tr></thead>
<tbody>
<tr><td><span class="avatar">ИИ</span>Иванов Иван</td><td>Разработка</td><td><span class="status-badge status-completed">Завершен</span></td><td><span class="score high">92%</span></td><td>28:45</td><td>27.01.2025 14:30</td></tr>
<tr><td><span class="avatar">СМ</span>Сидорова Мария</td><td>Аналитика</td><td><span class="status-badge status-completed">Завершен</span></td><td><span class="score high">88%</span></td><td>25:12</td><td>27.01.2025 15:15</td></tr>
<tr><td><span class="avatar">КД</span>Козлов Дмитрий</td><td>Разработка</td><td><span class="status-badge status-completed">Завершен</span></td><td><span class="score medium">75%</span></td><td>29:50</td><td>27.01.2025 16:00</td></tr>
<tr><td><span class="avatar">НА</span>Новикова Анна</td><td>QA</td><td><span class="status-badge status-progress">В процессе</span></td><td><span style="color:#94a3b8">—</span></td><td>12:20</td><td>28.01.2025 10:05</td></tr>
<tr><td><span class="avatar">ВС</span>Волков Сергей</td><td>Разработка</td><td><span class="status-badge status-completed">Завершен</span></td><td><span class="score low">62%</span></td><td>30:00</td><td>28.01.2025 11:45</td></tr>
</tbody>
</table></div>
</div>
</body></html>"""

# Пишем все файлы
for filename, content in pages.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {filename}")

print(f"\nСоздано {len(pages)} страниц")

#!/bin/bash

# Testing assigned tests
cat > testing-assigned-tests.html << 'EOF'
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Назначенные тесты - SQL</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'JetBrains Mono', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; font-size: 13px; line-height: 1.5; }
        .terminal { background: #1e1e1e; border: 1px solid #3e3e3e; border-radius: 8px; padding: 20px; max-width: 1100px; margin: 0 auto; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .prompt { color: #4ec9b0; }
        .keyword { color: #569cd6; font-weight: 600; }
        .string { color: #ce9178; }
        .number { color: #b5cea8; }
        .comment { color: #6a9955; }
        .line { margin: 3px 0; }
        table { border-collapse: collapse; margin: 10px 0; }
        td { padding: 8px 15px; border: 1px solid #3e3e3e; }
        .header-cell { background: #2d2d2d; font-weight: 600; color: #4ec9b0; }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="line"><span class="comment">-- Получение всех тестов, назначенных пользователю (лично или через группы)</span></div>
        <div class="line"><span class="prompt">mysql></span> <span class="keyword">SELECT DISTINCT</span> t.id, t.title, t.description</div>
        <div class="line">    -> <span class="keyword">FROM</span> tests t</div>
        <div class="line">    -> <span class="keyword">JOIN</span> test_assignments ta <span class="keyword">ON</span> t.id = ta.test_id</div>
        <div class="line">    -> <span class="keyword">LEFT JOIN</span> user_groups ug <span class="keyword">ON</span> ta.group_id = ug.group_id</div>
        <div class="line">    -> <span class="keyword">WHERE</span> ta.user_id = <span class="number">1</span> <span class="keyword">OR</span> ug.user_id = <span class="number">1</span>;</div>
        <div class="line">&nbsp;</div>
        <table>
            <tr>
                <td class="header-cell">id</td>
                <td class="header-cell">title</td>
                <td class="header-cell">description</td>
            </tr>
            <tr>
                <td><span class="number">3</span></td>
                <td>Основы SQL</td>
                <td>Тест по базовым операциям SQL</td>
            </tr>
            <tr>
                <td><span class="number">7</span></td>
                <td>Проектирование БД</td>
                <td>Нормализация и ER-диаграммы</td>
            </tr>
            <tr>
                <td><span class="number">12</span></td>
                <td>Транзакции и блокировки</td>
                <td>ACID-свойства и уровни изоляции</td>
            </tr>
            <tr>
                <td><span class="number">15</span></td>
                <td>Оптимизация запросов</td>
                <td>Индексы и план выполнения</td>
            </tr>
        </table>
        <div class="line"><span class="number">4</span> rows in set (0.02 sec)</div>
    </div>
</body>
</html>
EOF

# Testing score calculation  
cat > testing-score-calc.html << 'EOF'
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Подсчет балла</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'JetBrains Mono', monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; font-size: 13px; line-height: 1.5; }
        .terminal { background: #1e1e1e; border: 1px solid #3e3e3e; border-radius: 8px; padding: 20px; max-width: 1100px; margin: 0 auto; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .prompt { color: #4ec9b0; }
        .keyword { color: #569cd6; font-weight: 600; }
        .number { color: #b5cea8; }
        .comment { color: #6a9955; }
        .line { margin: 3px 0; }
        .success { color: #4ec9b0; font-weight: 600; }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="line"><span class="comment">-- Подсчет итогового балла для сессии тестирования</span></div>
        <div class="line"><span class="prompt">mysql></span> <span class="keyword">SELECT</span></div>
        <div class="line">    ->   (<span class="keyword">SUM</span>(<span class="keyword">CASE WHEN</span> ao.is_correct = <span class="number">1</span> <span class="keyword">THEN</span> <span class="number">1</span> <span class="keyword">ELSE</span> <span class="number">0</span> <span class="keyword">END</span>) / <span class="keyword">COUNT</span>(ua.id)) * <span class="number">100</span> <span class="keyword">AS</span> final_score</div>
        <div class="line">    -> <span class="keyword">FROM</span> user_answers ua</div>
        <div class="line">    -> <span class="keyword">JOIN</span> answer_options ao <span class="keyword">ON</span> ua.selected_option_id = ao.id</div>
        <div class="line">    -> <span class="keyword">WHERE</span> ua.test_session_id = <span class="number">10</span>;</div>
        <div class="line">&nbsp;</div>
        <div class="line">+-------------+</div>
        <div class="line">| final_score |</div>
        <div class="line">+-------------+</div>
        <div class="line">|   <span class="success">85.0000</span>   |</div>
        <div class="line">+-------------+</div>
        <div class="line"><span class="number">1</span> row in set (0.01 sec)</div>
        <div class="line">&nbsp;</div>
        <div class="line"><span class="comment">-- Детальная статистика</span></div>
        <div class="line"><span class="prompt">mysql></span> <span class="keyword">SELECT</span></div>
        <div class="line">    ->   <span class="keyword">COUNT</span>(*) <span class="keyword">as</span> total_questions,</div>
        <div class="line">    ->   <span class="keyword">SUM</span>(<span class="keyword">CASE WHEN</span> ao.is_correct = <span class="number">1</span> <span class="keyword">THEN</span> <span class="number">1</span> <span class="keyword">ELSE</span> <span class="number">0</span> <span class="keyword">END</span>) <span class="keyword">as</span> correct_answers,</div>
        <div class="line">    ->   <span class="keyword">SUM</span>(<span class="keyword">CASE WHEN</span> ao.is_correct = <span class="number">0</span> <span class="keyword">THEN</span> <span class="number">1</span> <span class="keyword">ELSE</span> <span class="number">0</span> <span class="keyword">END</span>) <span class="keyword">as</span> wrong_answers</div>
        <div class="line">    -> <span class="keyword">FROM</span> user_answers ua</div>
        <div class="line">    -> <span class="keyword">JOIN</span> answer_options ao <span class="keyword">ON</span> ua.selected_option_id = ao.id</div>
        <div class="line">    -> <span class="keyword">WHERE</span> ua.test_session_id = <span class="number">10</span>;</div>
        <div class="line">&nbsp;</div>
        <div class="line">+-----------------+-----------------+---------------+</div>
        <div class="line">| total_questions | correct_answers | wrong_answers |</div>
        <div class="line">+-----------------+-----------------+---------------+</div>
        <div class="line">|              <span class="number">20</span> |              <span class="success">17</span> |             <span class="number">3</span> |</div>
        <div class="line">+-----------------+-----------------+---------------+</div>
        <div class="line"><span class="number">1</span> row in set (0.00 sec)</div>
    </div>
</body>
</html>
EOF

echo "Создано страниц тестирования: 2"

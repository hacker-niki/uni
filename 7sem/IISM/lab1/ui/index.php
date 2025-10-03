<?php
// --- ОБЛАСТЬ ОБЪЯВЛЕНИЙ ---
const N = 1000000;

// Функция для Задания 1
function simulateSimpleEvent(float $probability): bool
{
    return (mt_rand() / mt_getrandmax()) < $probability;
}

// Функция для Задания 2
function simulateComplexIndependentEvents(array $probabilities): array
{
    $results = [];
    foreach ($probabilities as $p) {
        $results[] = simulateSimpleEvent($p);
    }
    return $results;
}

// Функция для Задания 3
function simulateDependentEvents(float $pA, float $pB_given_A): int
{
    $pB_given_notA = 1 - $pB_given_A;
    if (simulateSimpleEvent($pA)) {
        return simulateSimpleEvent($pB_given_A) ? 0 : 1;
    } else {
        return simulateSimpleEvent($pB_given_notA) ? 2 : 3;
    }
}

// Функция для Задания 4
function simulateCompleteGroup(array $probabilities): int
{
    $rand = mt_rand() / mt_getrandmax();
    $cumulativeProbability = 0;
    foreach ($probabilities as $index => $p) {
        $cumulativeProbability += $p;
        if ($rand < $cumulativeProbability) {
            return $index;
        }
    }
    return count($probabilities) - 1;
}

?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Симулятор вероятностных событий</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="container">
        <h1>Симулятор вероятностных событий</h1>

        <!-- Задание 1: Простое событие -->
        <div class="task">
            <h2>Задание 1: Симуляция простого события</h2>
            <form method="post">
                <input type="hidden" name="task" value="1">
                <label for="p_simple">Вероятность (0.0 до 1.0):</label>
                <input type="number" step="0.01" min="0" max="1" name="p_simple" id="p_simple" value="<?= htmlspecialchars($_POST['p_simple'] ?? 0.3) ?>" required>
                <button type="submit">Запустить симуляцию</button>
            </form>
            <?php
            if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['task'] == 1) {
                echo "<div class='results'>";
                $p_simple = (float)($_POST['p_simple'] ?? 0.3);
                $simple_event_count = 0;
                for ($i = 0; $i < N; $i++) {
                    if (simulateSimpleEvent($p_simple)) {
                        $simple_event_count++;
                    }
                }
                echo "<h3>Результаты Задания 1:</h3>";
                echo "<p>Теория = " . $p_simple . ", Практика = " . ($simple_event_count / N) . "</p>";
                echo "</div>";
            }
            ?>
        </div>

        <!-- Задание 2: Комплекс независимых событий -->
        <div class="task">
            <h2>Задание 2: Симуляция комплекса независимых событий</h2>
            <form method="post">
                <input type="hidden" name="task" value="2">
                <label for="p_complex">Вероятности (через запятую, например, 0.2, 0.8, 0.5):</label>
                <input type="text" name="p_complex" id="p_complex" value="<?= htmlspecialchars($_POST['p_complex'] ?? '0.2, 0.8, 0.5') ?>" required>
                <button type="submit">Запустить симуляцию</button>
            </form>
            <?php
            if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['task'] == 2) {
                echo "<div class='results'>";
                $p_complex_independent_str = $_POST['p_complex'] ?? '0.2, 0.8, 0.5';
                $p_complex_independent = array_map('floatval', explode(',', $p_complex_independent_str));
                $event_count = count($p_complex_independent);

                // Инициализация счетчиков
                $simple_counts = array_fill(0, $event_count, 0);
                $pairwise_counts = []; // Для парных событий

                // Основной цикл симуляции
                for ($i = 0; $i < N; $i++) {
                    $results = simulateComplexIndependentEvents($p_complex_independent);
                    
                    // Считаем простые события
                    foreach ($results as $index => $result) {
                        if ($result) {
                            $simple_counts[$index]++;
                        }
                    }

                    for ($j = 0; $j < $event_count; $j++) {
                        for ($k = $j + 1; $k < $event_count; $k++) {
                            $pair_key = "{$j}-{$k}";
                            if (!isset($pairwise_counts[$pair_key])) {
                                $pairwise_counts[$pair_key] = 0;
                            }
                            // Если оба события в паре произошли в этой итерации
                            if ($results[$j] && $results[$k]) {
                                $pairwise_counts[$pair_key]++;
                            }
                        }
                    }
                }

                // Вывод результатов для простых событий
                echo "<h3>Результаты для простых событий:</h3>";
                for ($i = 0; $i < $event_count; $i++) {
                    $frequency = $simple_counts[$i] / N;
                    echo "<p>Событие " . $i . ": Теория = " . $p_complex_independent[$i] . ", Практика = " . $frequency . "</p>";
                }

                // *** НОВЫЙ БЛОК: Вывод результатов для парных событий ***
                if ($event_count > 1) {
                    echo "<h3>Результаты для попарных сложных событий (пересечение):</h3>";
                    for ($j = 0; $j < $event_count; $j++) {
                        for ($k = $j + 1; $k < $event_count; $k++) {
                            $pair_key = "{$j}-{$k}";
                            $theoretical_p = $p_complex_independent[$j] * $p_complex_independent[$k];
                            $empirical_p = ($pairwise_counts[$pair_key] ?? 0) / N;
                            echo "<p>Событие (" . $j . " и " . $k . "): Теория = " . round($theoretical_p, 4) . ", Практика = " . $empirical_p . "</p>";
                        }
                    }
                }

                echo "</div>";
            }
            ?>
        </div>

        <!-- Задание 3: Зависимые события -->
        <div class="task">
            <h2>Задание 3: Симуляция зависимых событий</h2>
            <form method="post">
                <input type="hidden" name="task" value="3">
                <label for="pA">Вероятность P(A):</label>
                <input type="number" step="0.01" min="0" max="1" name="pA" id="pA" value="<?= htmlspecialchars($_POST['pA'] ?? 0.4) ?>" required>
                <label for="pB_given_A">Вероятность P(B|A):</label>
                <input type="number" step="0.01" min="0" max="1" name="pB_given_A" id="pB_given_A" value="<?= htmlspecialchars($_POST['pB_given_A'] ?? 0.8) ?>" required>
                <button type="submit">Запустить симуляцию</button>
            </form>
            <?php
            if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['task'] == 3) {
                echo "<div class='results'>";
                $pA = (float)($_POST['pA'] ?? 0.4);
                $pB_given_A = (float)($_POST['pB_given_A'] ?? 0.8);

                $theoretical_probabilities = [
                    'AB' => $pA * $pB_given_A,
                    'A(не B)' => $pA * (1 - $pB_given_A),
                    '(не A)B' => (1 - $pA) * (1 - $pB_given_A),
                    '(не A)(не B)' => (1 - $pA) * (1 - (1 - $pB_given_A)),
                ];

                $dependent_event_counts = [0, 0, 0, 0];
                for ($i = 0; $i < N; $i++) {
                    $dependent_event_counts[simulateDependentEvents($pA, $pB_given_A)]++;
                }

                echo "<h3>Результаты Задания 3:</h3>";
                $event_names = array_keys($theoretical_probabilities);
                foreach ($event_names as $index => $name) {
                    $frequency = $dependent_event_counts[$index] / N;
                    echo "<p>Событие " . $name . ": Теория = " . round($theoretical_probabilities[$name], 4) . ", Практика = " . $frequency . "</p>";
                }
                echo "</div>";
            }
            ?>
        </div>

        <!-- Задание 4: Полная группа событий -->
        <div class="task">
            <h2>Задание 4: Симуляция полной группы событий</h2>
            <form method="post">
                <input type="hidden" name="task" value="4">
                <label for="p_complete_group">Вероятности (сумма должна быть 1, через запятую):</label>
                <input type="text" name="p_complete_group" id="p_complete_group" value="<?= htmlspecialchars($_POST['p_complete_group'] ?? '0.1, 0.25, 0.4, 0.15, 0.1') ?>" required>
                <button type="submit">Запустить симуляцию</button>
            </form>
            <?php
            if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['task'] == 4) {
                echo "<div class='results'>";
                $p_complete_group_str = $_POST['p_complete_group'] ?? '0.1, 0.25, 0.4, 0.15, 0.1';
                $p_complete_group = array_map('floatval', explode(',', $p_complete_group_str));
                
                if (abs(array_sum($p_complete_group) - 1.0) > 0.0001) {
                    echo "<p class='error'>Ошибка: Сумма вероятностей должна быть равна 1.</p>";
                } else {
                    $complete_group_counts = array_fill(0, count($p_complete_group), 0);
                    for ($i = 0; $i < N; $i++) {
                        $complete_group_counts[simulateCompleteGroup($p_complete_group)]++;
                    }

                    echo "<h3>Результаты Задания 4:</h3>";
                    for ($i = 0; $i < count($p_complete_group); $i++) {
                        $frequency = $complete_group_counts[$i] / N;
                        echo "<p>Событие " . $i . ": Теория = " . $p_complete_group[$i] . ", Практика = " . $frequency . "</p>";
                    }
                }
                echo "</div>";
            }
            ?>
        </div>
    </div>

</body>
</html>

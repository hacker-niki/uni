<?php

const N = 1000000;

// Задание 1
function simulateSimpleEvent(float $probability): bool
{
    return (mt_rand() / mt_getrandmax()) < $probability;
}

$p_simple = 0.3;
$simple_event_count = 0;
for ($i = 0; $i < N; $i++) {
    if (simulateSimpleEvent($p_simple)) {
        $simple_event_count++;
    }
}
echo "Задание 1: Теория = " . $p_simple . ", Практика = " . ($simple_event_count / N) . "\n";

// Задание 2
function simulateComplexIndependentEvents(array $probabilities): array
{
    $results = [];
    foreach ($probabilities as $p) {
        $results[] = simulateSimpleEvent($p);
    }
    return $results;
}

$p_complex_independent = [0.2, 0.5, 0.75];
$complex_independent_counts = array_fill(0, count($p_complex_independent), 0);
for ($i = 0; $i < N; $i++) {
    $results = simulateComplexIndependentEvents($p_complex_independent);
    foreach ($results as $index => $result) {
        if ($result) {
            $complex_independent_counts[$index]++;
        }
    }
}
echo "Задание 2:\n";
for ($i = 0; $i < count($p_complex_independent); $i++) {
    $frequency = $complex_independent_counts[$i] / N;
    echo "  Событие " . ($i) . ": Теория = " . $p_complex_independent[$i] . ", Практика = " . $frequency . "\n";
}


// Задание 3
function simulateDependentEvents(float $pA, float $pB_given_A): int
{
    $pB_given_notA = 1 - $pB_given_A;

    if (simulateSimpleEvent($pA)) {
        return simulateSimpleEvent($pB_given_A) ? 0 : 1; // AB : A(не B)
    } else {
        return simulateSimpleEvent($pB_given_notA) ? 2 : 3; // (не A)B : (не A)(не B)
    }
}

$pA = 0.4;
$pB_given_A = 0.8;

$theoretical_probabilities = [
    'AB'          => $pA * $pB_given_A,
    'A(не B)'     => $pA * (1 - $pB_given_A),
    '(не A)B'     => (1 - $pA) * (1 - $pB_given_A),
    '(не A)(не B)'=> (1 - $pA) * (1 - (1 - $pB_given_A)),
];

$dependent_event_counts = [0, 0, 0, 0];
for ($i = 0; $i < N; $i++) {
    $dependent_event_counts[simulateDependentEvents($pA, $pB_given_A)]++;
}

echo "Задание 3:\n";
$event_names = array_keys($theoretical_probabilities);
foreach ($event_names as $index => $name) {
    $frequency = $dependent_event_counts[$index] / N;
    echo "  Событие " . $name . ": Теория = " . $theoretical_probabilities[$name] . ", Практика = " . $frequency . "\n";
}

// Задание 4
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

$p_complete_group = [0.1, 0.25, 0.4, 0.15, 0.1];
$complete_group_counts = array_fill(0, count($p_complete_group), 0);
for ($i = 0; $i < N; $i++) {
    $complete_group_counts[simulateCompleteGroup($p_complete_group)]++;
}

echo "Задание 4:\n";
for ($i = 0; $i < count($p_complete_group); $i++) {
    $frequency = $complete_group_counts[$i] / N;
    echo "  Событие " . $i . ": Теория = " . $p_complete_group[$i] . ", Практика = " . $frequency . "\n";
}
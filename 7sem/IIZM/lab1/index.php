<?php

class ItemSetGenerator
{
    function simulateSimpleEvent(float $probability): bool
    {
        return (mt_rand() / mt_getrandmax()) < $probability;
    }

    private const SET_SIZE = 10;

    public array $commonItems;
    public array $rareItems;
    public array $ultraRareItems;

    private float $probabilityRare;
    private float $probabilityUltraRare;

    public function __construct()
    {
        $this->probabilityRare = 0.15;
        $this->probabilityUltraRare = 0.02;

        $this->commonItems = [
                'Зелье здоровья', 'Слабый эликсир маны', 'Ржавый кинжал',
                'Потертый кожаный шлем', 'Кусок хлеба', 'Факел', 'Простая стрела',
        ];

        $this->rareItems = [
                'Меч рыцаря', 'Лук эльфийского дозорного', 'Кольцо защиты от огня',
                'Сильное зелье лечения', 'Амулет силы',
        ];

        $this->ultraRareItems = [
                'Драконий щит Вечности', 'Легендарный клинок "Душегуб"', 'Посох Архимага',
        ];
    }

    /**
     * @return array
     */
    public function generateSet(): array
    {
        $resultSet = [];
        $specialItem = null;

        if ($this->simulateSimpleEvent($this->probabilityUltraRare)) {
            $specialItem = $this->getRandomUltraRareItem();
        } elseif ($this->simulateSimpleEvent((1 - $this->probabilityUltraRare) / $this->probabilityRare)) {
            $specialItem = $this->getRandomRareItem();
        }

        if ($specialItem !== null) {
            $resultSet[] = $specialItem;
            for ($i = 0; $i < self::SET_SIZE - 1; $i++) {
                $resultSet[] = $this->getRandomCommonItem();
            }
        } else {
            for ($i = 0; $i < self::SET_SIZE; $i++) {
                $resultSet[] = $this->getRandomCommonItem();
            }
        }

        shuffle($resultSet);
        return $resultSet;
    }

    private function getRandomCommonItem(): string
    {
        return $this->commonItems[array_rand($this->commonItems)];
    }

    private function getRandomRareItem(): string
    {
        return $this->rareItems[array_rand($this->rareItems)];
    }

    private function getRandomUltraRareItem(): string
    {
        return $this->ultraRareItems[array_rand($this->ultraRareItems)];
    }
}


$generatedSet = null;
$generator = new ItemSetGenerator();


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $generatedSet = $generator->generateSet();
}

/**
 * @param string $item
 * @param ItemSetGenerator $generator
 * @return string
 */
function getItemRarityClass(string $item, ItemSetGenerator $generator): string
{
    if (in_array($item, $generator->ultraRareItems)) {
        return 'item-ultra-rare';
    }
    if (in_array($item, $generator->rareItems)) {
        return 'item-rare';
    }
    return 'item-common';
}

?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Генератор игровых наборов</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #2c3e50;
            color: #ecf0f1;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }

        .container {
            background-color: #34495e;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            text-align: center;
            width: 100%;
            max-width: 500px;
        }

        h1 {
            margin-top: 0;
            color: #ffffff;
            border-bottom: 2px solid #7f8c8d;
            padding-bottom: 15px;
        }

        .generate-button {
            background-color: #e67e22;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-bottom: 20px;
        }

        .generate-button:hover {
            background-color: #d35400;
        }

        .item-list {
            list-style: none;
            padding: 0;
            margin-top: 20px;
            text-align: left;
        }

        .item-list li {
            background-color: #2c3e50;
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 8px;
            font-size: 16px;
            border-left: 5px solid;
        }

        /* Цвета для разной редкости */
        .item-common {
            color: #95a5a6;
        }

        /* Серый */
        .item-rare {
            color: #88ff00;
            font-weight: bold;
        }

        /* Синий */
        .item-ultra-rare {
            color: #ff0000;
            font-weight: bold;
        }

        /* Фиолетовый */
    </style>
</head>
<body>

<div class="container">
    <h1>Генератор игровых наборов</h1>

    <!-- Форма с одной кнопкой для отправки POST-запроса на эту же страницу -->
    <form method="POST" action="">
        <button type="submit" class="generate-button">Открыть новый набор</button>
    </form>

    <?php if (!empty($generatedSet)): ?>
        <div class="result">
            <h2>Ваш набор:</h2>
            <ul class="item-list">
                <?php foreach ($generatedSet as $item): ?>
                    <?php $rarityClass = getItemRarityClass($item, $generator); ?>
                    <li class="<?= $rarityClass ?>"><?= htmlspecialchars($item) ?></li>
                <?php endforeach; ?>
            </ul>
        </div>
    <?php endif; ?>

</div>

</body>
</html>

def generate_html_table(rows=10, columns=5):
    if (rows < 0 or columns < 0):
        raise ValueError("rows and columns must be positive integers")
    # Создаем HTML-код для таблицы
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Градиентная Таблица</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 0px solid #000;
            padding: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <table>
"""
    # Вычисляем шаг изменения цвета
    step = 255 // (rows - 1)

    for i in range(rows):
        # Вычисляем цвет фона для текущей строки
        grey_value = 255 - i * step
        background_color = f"rgb({grey_value}, {grey_value}, {grey_value})"
        html += f'        <tr style="background-color: {background_color};">\n'
        for j in range(columns):
            html += f'<td></td>'
        html += '        </tr>\n'

    html += """    </table>
</body>
</html>"""

    # Записываем HTML-код в файл
    with open("gradient_table.html", "w", encoding="utf-8") as file:
        file.write(html)


if __name__ == "__main__":
    try:
        generate_html_table(255, 255)
    except ValueError as e:
        print(e)
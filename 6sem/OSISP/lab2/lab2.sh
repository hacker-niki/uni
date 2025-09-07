#!/bin/bash

# Функция для очистки CSV-файла
clean_csv() {
    local input_file="$1"
    
    awk '
    BEGIN {
        max_fields = 0
    }
    
    # Игнорируем строки с метаданными (начинающиеся с #)
    /^#/ {
        next
    }
    
    {
        # Обработка полей строки
        row_fields = split($0, fields, /,/)
        
        # Обновляем максимальное количество полей
        if (row_fields > max_fields) {
            max_fields = row_fields
        }
        
        # Очистка и сохранение полей
        cleaned_row = ""
        for (i = 1; i <= row_fields; i++) {
            # Проверка на числовое значение (целое или с плавающей точкой)
            if (fields[i] ~ /^[+-]?[0-9]*\.?[0-9]+$/) {
                cleaned_row = cleaned_row fields[i]
            } else {
                cleaned_row = cleaned_row "0"
            }
            if (i < row_fields) {
                cleaned_row = cleaned_row ","
            }
        }
        # Сохраняем очищенную строку
        cleaned_data[NR] = cleaned_row
    }
    
    END {
        # Дополнение строк до максимального количества полей
        for (i = 1; i <= NR; i++) {
            split(cleaned_data[i], fields, /,/)
            row_length = length(fields)
            for (j = row_length + 1; j <= max_fields; j++) {
                cleaned_data[i] = cleaned_data[i] ",0"
            }
            print cleaned_data[i]
        }
    }
    ' "$input_file"
}

# Проверка аргументов
if [ "$#" -lt 2 ]; then
    echo "Использование: $0 <операция> <файл1.csv> <файл2.csv> ..."
    exit 1
fi

# Обработка каждого файла, начиная с третьего аргумента
for file in "${@:2}"; do
    echo "Обработка файла: $file"
    clean_csv "$file"
done

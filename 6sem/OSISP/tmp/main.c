#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Использование: %s <директория> <имя_файла>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Формируем команду find: например, find /path -name "filename"
    char command[256];
    snprintf(command, sizeof(command), "find %s -name '%s'", argv[1], argv[2]);

    // Выполняем команду и читаем вывод
    FILE *pipe = popen(command, "r");
    if (!pipe) {
        perror("Ошибка выполнения команды find");
        exit(EXIT_FAILURE);
    }

    // Выводим результаты
    // char buffer[1024];
    // while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
    //     printf("%s", buffer);
    // }

    // Закрываем pipe
    pclose(pipe);
    return 0;
}

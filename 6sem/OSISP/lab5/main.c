#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>


// Глобальные переменные
int shared_data = 0;  // Общий ресурс
int reader_count = 0; // Количество активных читателей

// Мьютексы и условия
pthread_mutex_t resource_mutex = PTHREAD_MUTEX_INITIALIZER; // Для защиты ресурса
pthread_mutex_t reader_count_mutex = PTHREAD_MUTEX_INITIALIZER; // Для защиты счетчика читателей

// Функция для читателей
void *reader(void *arg) {
    int id = *(int *)arg;
    free(arg);

    while (1) {
        // Вход в критическую секцию для обновления счетчика читателей
        pthread_mutex_lock(&reader_count_mutex);
        reader_count++;
        if (reader_count == 1) {
            // Первый читатель блокирует ресурс
            pthread_mutex_lock(&resource_mutex);
        }
        pthread_mutex_unlock(&reader_count_mutex);

        // Чтение ресурса
        printf("Читатель %d читает данные: %d\n", id, shared_data);
        usleep(rand() % 1000000); // Задержка для симуляции чтения

        // Выход из критической секции
        pthread_mutex_lock(&reader_count_mutex);
        reader_count--;
        if (reader_count == 0) {
            // Последний читатель разблокирует ресурс
            pthread_mutex_unlock(&resource_mutex);
        }
        pthread_mutex_unlock(&reader_count_mutex);

        usleep(rand() % 1000000); // Задержка перед следующим чтением
    }

    return NULL;
}

// Функция для писателей
void *writer(void *arg) {
    int id = *(int *)arg;
    free(arg);

    while (1) {
        // Блокировка ресурса
        pthread_mutex_lock(&resource_mutex);

        // Запись в ресурс
        shared_data++;
        printf("Писатель %d записал данные: %d\n", id, shared_data);
        usleep(rand() % 1000000); // Задержка для симуляции записи

        // Разблокировка ресурса
        pthread_mutex_unlock(&resource_mutex);

        usleep(rand() % 1000000); // Задержка перед следующей записью
    }

    return NULL;
}

int main(int argc, const char** argv) {
    int NUM_READERS = 5;
    int NUM_WRITERS = 2;

    if (argc == 3) {
        NUM_READERS = atoi(argv[1]);
        NUM_WRITERS = atoi(argv[2]);
    }

    printf("%d читателя и %d писателя\n", NUM_READERS, NUM_WRITERS);

    sleep(3);

    pthread_t readers[NUM_READERS], writers[NUM_WRITERS];

    // Создание потоков читателей
    for (int i = 0; i < NUM_READERS; i++) {
        int *id = malloc(sizeof(int));
        *id = i + 1;
        if (pthread_create(&readers[i], NULL, reader, id) != 0) {
            perror("Ошибка создания потока читателя");
            exit(EXIT_FAILURE);
        }
    }

    // Создание потоков писателей
    for (int i = 0; i < NUM_WRITERS; i++) {
        int *id = malloc(sizeof(int));
        *id = i + 1;
        if (pthread_create(&writers[i], NULL, writer, id) != 0) {
            perror("Ошибка создания потока писателя");
            exit(EXIT_FAILURE);
        }
    }

    // Ожидание завершения потоков (в данном случае бесконечный цикл, поэтому join не используется)
    for (int i = 0; i < NUM_READERS; i++) {
        pthread_join(readers[i], NULL);
    }
    for (int i = 0; i < NUM_WRITERS; i++) {
        pthread_join(writers[i], NULL);
    }

    return 0;
}
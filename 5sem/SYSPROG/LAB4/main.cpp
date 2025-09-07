#include <windows.h>
#include <iostream>
#include <vector>

// Параметры
const int num_readers = 5;
const int num_writers = 2;
const int read_duration = 100;  // мс
const int write_duration = 150; // мс
const int simulation_time = 10; // секунды

// Глобальные переменные для управления доступом к ресурсу
SRWLOCK rw_lock = SRWLOCK_INIT;
int shared_data = 0;

// Метрики для анализа
LONG read_attempts = 0;
LONG successful_reads = 0;
LONG write_attempts = 0;
LONG successful_writes = 0;

// События для остановки потоков
HANDLE stop_event;

// Объект для синхронизации вывода в консоль
HANDLE io_mutex;

// Функция для потока-читателя
DWORD WINAPI reader(LPVOID lpParam) {
    int id = (int)(intptr_t)lpParam;
    while (WaitForSingleObject(stop_event, 0) != WAIT_OBJECT_0) {
        InterlockedIncrement(&read_attempts);

        AcquireSRWLockShared(&rw_lock);
        InterlockedIncrement(&successful_reads);

        WaitForSingleObject(io_mutex, INFINITE);
        std::cout << "Reader " << id << " reads data: " << shared_data << std::endl;
        ReleaseMutex(io_mutex);

        ReleaseSRWLockShared(&rw_lock);

        Sleep(read_duration);
    }
    return 0;
}

// Функция для потока-писателя
DWORD WINAPI writer(LPVOID lpParam) {
    int id = (int)(intptr_t)lpParam;
    while (WaitForSingleObject(stop_event, 0) != WAIT_OBJECT_0) {
        InterlockedIncrement(&write_attempts);

        AcquireSRWLockExclusive(&rw_lock);
        InterlockedIncrement(&successful_writes);

        ++shared_data;

        WaitForSingleObject(io_mutex, INFINITE);
        std::cout << "Writer " << id << " writes data: " << shared_data << std::endl;
        ReleaseMutex(io_mutex);

        ReleaseSRWLockExclusive(&rw_lock);

        Sleep(write_duration);
    }
    return 0;
}

int main() {
    // Инициализация мьютекса и события
    io_mutex = CreateMutex(NULL, FALSE, NULL);
    stop_event = CreateEvent(NULL, TRUE, FALSE, NULL);

    // Создаем потоки-читатели
    std::vector<HANDLE> reader_threads(num_readers);
    for (int i = 0; i < num_readers; ++i) {
        reader_threads[i] = CreateThread(NULL, 0, reader, (LPVOID)(intptr_t)i, 0, NULL);
    }

    // Создаем потоки-писатели
    std::vector<HANDLE> writer_threads(num_writers);
    for (int i = 0; i < num_writers; ++i) {
        writer_threads[i] = CreateThread(NULL, 0, writer, (LPVOID)(intptr_t)i, 0, NULL);
    }

    // Запускаем симуляцию
    Sleep(simulation_time * 1000); // Симуляция на 10 секунд

    // Сигнализируем о завершении
    SetEvent(stop_event);

    // Дожидаемся завершения всех потоков
    WaitForMultipleObjects(num_readers, reader_threads.data(), TRUE, INFINITE);
    WaitForMultipleObjects(num_writers, writer_threads.data(), TRUE, INFINITE);

    // Закрываем дескрипторы
    for (HANDLE thread : reader_threads) {
        CloseHandle(thread);
    }
    for (HANDLE thread : writer_threads) {
        CloseHandle(thread);
    }
    CloseHandle(io_mutex);
    CloseHandle(stop_event);

    // Вывод результатов моделирования
    std::cout << "Simulation Results:\n";
    std::cout << "Total Read Attempts: " << read_attempts << "\n";
    std::cout << "Total Successful Reads: " << successful_reads << "\n";
    std::cout << "Total Write Attempts: " << write_attempts << "\n";
    std::cout << "Total Successful Writes: " << successful_writes << "\n";
    std::cout << "Read Efficiency (%): " << (successful_reads * 100.0 / read_attempts) << "\n";
    std::cout << "Write Efficiency (%): " << (successful_writes * 100.0 / write_attempts) << "\n";

    return 0;
}

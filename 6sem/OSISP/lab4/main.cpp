#include <iostream>
#include <csignal>
#include <unistd.h>
#include <cstdlib>
#include <fstream>
#include <sys/wait.h>
#include <ctime>

struct ApplicationContext {
    int count;
};

ApplicationContext appContext;

void SaveContext() {
    std::ofstream file("context.dat", std::ios::binary);
    if (file) {
        file.write(reinterpret_cast<char*>(&appContext), sizeof(appContext));
    }
}

void LoadContext() {
    std::ifstream file("context.dat", std::ios::binary);
    if (file) {
        file.read(reinterpret_cast<char*>(&appContext), sizeof(appContext));
    } else {
        appContext.count = 0; // Инициализация, если файл не найден
    }
}

void SignalHandler(int signum) {
    std::cout << "Signal received: " << signum << ". Creating a child process." << std::endl;

    // Сохраняем текущее состояние
    SaveContext();

    pid_t pid = fork();
    if (pid < 0) {
        std::cerr << "Fork failed!" << std::endl;
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        // Дочерний процесс
        std::cout << "Child process created. Continuing execution..." << std::endl;
        while (true) {
            // Дочерний процесс продолжает выполнение
            appContext.count++;
            SaveContext();
            std::cout << "Child count: " << appContext.count << std::endl;
            sleep(1); // Задержка в 1 секунду
        }
    } else {
        // Родительский процесс
        std::cout << "Parent process exiting." << std::endl;
        exit(0); // Завершение родительского процесса
    }
}

int main() {
    signal(SIGINT, SignalHandler); // Перехват Ctrl+C

    LoadContext();
    std::cout << "Starting count from: " << appContext.count << std::endl;

    while (true) {
        // Основной цикл родительского процесса
        appContext.count++;
        SaveContext();
        std::cout << "Parent count: " << appContext.count << std::endl;
        sleep(1); // Задержка в 1 секунду
    }

    return 0;
}

#include <string>
#include <windows.h>

// Функция обработки сообщений для окна
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            FillRect(hdc, &ps.rcPaint, (HBRUSH) (COLOR_WINDOW + 1));
            EndPaint(hwnd, &ps);
        }
            return 0;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

// Главная функция программы
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nShowCmd) {
    const char CLASS_NAME[] = "Sample Window Class";

    // Регистрация класса окна
    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc; // Функция обработки сообщений
    wc.hInstance = hInstance; // Дескриптор экземпляра
    wc.lpszClassName = CLASS_NAME; // Имя класса окна

    RegisterClass(&wc); // Регистрация класса окна
    for (int i = 0; i < 100000000; i++) {
        // Создание основного окна
        HWND hwnd = CreateWindowEx(
            0, // Расширенные стили
            CLASS_NAME, // Имя класса
            ("Hello, Win32!" + std::to_string(i)).c_str(), // Заголовок окна
            WS_OVERLAPPEDWINDOW, // Стиль окна
            CW_USEDEFAULT, CW_USEDEFAULT, // Позиция окна
            CW_USEDEFAULT, CW_USEDEFAULT, // Размер окна
            NULL, // Родительское окно
            NULL, // Меню
            hInstance, // Дескриптор экземпляра
            NULL // Дополнительные параметры
        );

        if (hwnd == NULL) {
            return 0; // Обработка ошибки
        }

        ShowWindow(GetConsoleWindow(), SW_HIDE);

        ShowWindow(hwnd, nShowCmd); // Показать окно
    }

    // Главный цикл сообщений
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg); // Перевод сообщений
        DispatchMessage(&msg); // Обработка сообщений
    }

    return 0; // Завершение программы
}

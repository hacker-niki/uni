#include <iostream>
#include <ostream>
#include <string>
#include <windows.h>

struct ApplicationContext {
    int someData; // Example field for application state
};

LPSTR _lpstr;
ApplicationContext appContext;

// Function prototypes
void SaveContext();

void LoadContext();

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR lpstr, int nShowCmd) {
    LoadContext();

    // Initialize application context (example data)
    _lpstr = lpstr;
    const char CLASS_NAME[] = "SampleWindowClass";

    // Register the window class
    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    // Create the window
    HWND hwnd = CreateWindowA(
        // 0, // Optional window styles
        CLASS_NAME, // Window class
        "HAHA", // Window text
        WS_OVERLAPPEDWINDOW, // Window style
        CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
        NULL, // Parent window
        NULL, // Menu
        hInstance, // Instance handle
        NULL // Additional application data
    );
    //   HWND fuck = CreateWindowA(
    //     // 0, // Optional window styles
    //     CLASS_NAME, // Window class
    //     "FUCK", // Window text
    //     WS_OVERLAPPEDWINDOW, // Window style
    //     CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
    //     NULL, // Parent window
    //     NULL, // Menu
    //     hInstance, // Instance handle
    //     NULL // Additional application data
    // );

    if (hwnd == NULL) {
        return 0;
    }


    ShowWindow(GetConsoleWindow(), SW_HIDE);

    ShowWindow(hwnd, nShowCmd);
    // ShowWindow(fuck, nShowCmd);
    UpdateWindow(hwnd);
    // UpdateWindow(fuck);

    // Load previous context if needed

    // Run the message loop
    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

void SaveContext() {
    DeleteFile("context.dat");
    HANDLE hFile = CreateFile("context.dat", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        DWORD bytesWritten;
        WriteFile(hFile, &appContext, sizeof(appContext), &bytesWritten, NULL);
        CloseHandle(hFile);
    }
}

void LoadContext() {
    HANDLE hFile = CreateFile("context.dat", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        DWORD bytesRead;
        ReadFile(hFile, &appContext, sizeof(appContext), &bytesRead, NULL);
        appContext.someData += 1;
        CloseHandle(hFile);
    }
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_CLOSE: {
            SaveContext(); // Save the application state
            // Create a new process
            STARTUPINFO si;
            PROCESS_INFORMATION pi;

            ZeroMemory(&si, sizeof(si));
            si.cb = sizeof(si);
            ZeroMemory(&pi, sizeof(pi));

            if (CreateProcess(NULL, GetCommandLineA(), NULL, NULL, FALSE, 0, NULL,
                              NULL, &si, &pi)) {
                CloseHandle(pi.hProcess);
                CloseHandle(pi.hThread);
            }
            DestroyWindow(hwnd); // Destroy the window
            return 0;
        }
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            TextOut(hdc, 10, 10, TEXT(std::to_string(appContext.someData).c_str()), strlen(std::to_string(appContext.someData).c_str()));
            EndPaint(hwnd, &ps);
            ReleaseDC(hwnd, hdc);
            break;
        }

        case WM_DESTROY: {
            PostQuitMessage(0);
            TerminateProcess(GetCurrentProcess(), 0);
            return 0;
        }
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

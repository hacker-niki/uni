#include <windows.h>
#include <stdio.h>

#define PIPE_NAME L"\\\\.\\pipe\\SimpleChatPipe"
#define BUFFER_SIZE sizeof(Message)

typedef struct {
    char address[256];
    char body[1024];
} Message;

DWORD WINAPI ClientHandler(LPVOID lpParam) {
    HANDLE hPipe = (HANDLE)lpParam;
    Message message;
    DWORD bytesRead, bytesWritten;

    while (1) {
        BOOL success = ReadFile(
            hPipe,
            &message,
            sizeof(Message),
            &bytesRead,
            NULL
        );

        if (!success || bytesRead == 0) {
            printf("Client disconnected or ReadFile failed, GLE=%d.\n", GetLastError());
            break;
        }

        printf("Received message from %s: %s\n", message.address, message.body);

        success = WriteFile(
            hPipe,
            &message,
            sizeof(Message),
            &bytesWritten,
            NULL
        );

        if (!success || bytesWritten == 0) {
            printf("WriteFile failed, GLE=%d.\n", GetLastError());
            break;
        }
    }

    FlushFileBuffers(hPipe);
    DisconnectNamedPipe(hPipe);
    CloseHandle(hPipe);
    return 0;
}

int main() {
    HANDLE hPipe;
    HANDLE hThread;
    DWORD threadId;

    while (1) {
        hPipe = CreateNamedPipe(
            PIPE_NAME,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            PIPE_UNLIMITED_INSTANCES,
            BUFFER_SIZE,
            BUFFER_SIZE,
            0,
            NULL
        );

        if (hPipe == INVALID_HANDLE_VALUE) {
            printf("CreateNamedPipe failed, GLE=%d.\n", GetLastError());
            return 1;
        }

        printf("Waiting for client connection...\n");

        BOOL connected = ConnectNamedPipe(hPipe, NULL) ? TRUE : (GetLastError() == ERROR_PIPE_CONNECTED);

        if (connected) {
            printf("Client connected.\n");

            hThread = CreateThread(
                NULL,
                0,
                ClientHandler,
                (LPVOID)hPipe,
                0,
                &threadId
            );

            if (hThread == NULL) {
                printf("CreateThread failed, GLE=%d.\n", GetLastError());
                CloseHandle(hPipe);
            }
            else {
                CloseHandle(hThread);
            }
        }
        else {
            CloseHandle(hPipe);
        }
    }

    return 0;
}
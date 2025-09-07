#include <windows.h>
#include <stdio.h>

#define PIPE_NAME L"\\\\.\\pipe\\SimpleChatPipe"
#define BUFFER_SIZE sizeof(Message)

typedef struct {
    char address[256];
    char body[1024];
} Message;

int main() {
    HANDLE hPipe;
    Message message;
    DWORD bytesRead, bytesWritten;

    while (1) {
        hPipe = CreateFile(
            PIPE_NAME,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            0,
            NULL
        );

        if (hPipe != INVALID_HANDLE_VALUE)
            break;

        if (GetLastError() != ERROR_PIPE_BUSY) {
            printf("Could not open pipe. GLE=%d\n", GetLastError());
            return 1;
        }

        if (!WaitNamedPipe(PIPE_NAME, 20000)) {
            printf("Could not open pipe: 20 second wait timed out.");
            return 1;
        }
    }

    printf("Connected to server.\n");
    printf("Enter address: ");
    fgets(message.address, sizeof(message.address), stdin);
    message.address[strcspn(message.address, "\n")] = 0;

    while (1) {

        printf("Enter message: ");
        fgets(message.body, sizeof(message.body), stdin);
        message.body[strcspn(message.body, "\n")] = 0;

        BOOL success = WriteFile(
            hPipe,
            &message,
            sizeof(Message),
            &bytesWritten,
            NULL
        );

        if (!success) {
            printf("WriteFile failed, GLE=%d.\n", GetLastError());
            break;
        }

        success = ReadFile(
            hPipe,
            &message,
            sizeof(Message),
            &bytesRead,
            NULL
        );

        if (!success || bytesRead == 0) {
            printf("ReadFile failed, GLE=%d.\n", GetLastError());
            break;
        }

    }

    CloseHandle(hPipe);
    return 0;
}
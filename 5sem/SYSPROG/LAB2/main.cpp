#include <windows.h>
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>

int oddcnt = 0;

void processData(std::vector<char> &buffer, DWORD bytesRead) {
    for (DWORD i = 0; i < bytesRead; ++i) {
        buffer[i] = toupper(buffer[i]);
        oddcnt += (buffer[i] % 2);
    }
}

void displayProgressBar(double progress) {
    int barWidth = 50;
    std::cout << "[";
    int pos = static_cast<int>(barWidth * progress);
    for (int i = 0; i < barWidth; ++i) {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] " << int(progress * 100.0) << " %\r";
    std::cout.flush();
}

HANDLE openFile(const std::string &filename, DWORD desiredAccess, DWORD creationDisposition, DWORD flags) {
    HANDLE fileHandle = CreateFile(filename.c_str(), desiredAccess, 0, nullptr, creationDisposition, flags, nullptr);
    if (fileHandle == INVALID_HANDLE_VALUE) {
        std::cerr << "Error opening file: " << GetLastError() << std::endl;
    }
    return fileHandle;
}

bool getFileSize(HANDLE fileHandle, LARGE_INTEGER &fileSize) {
    if (!GetFileSizeEx(fileHandle, &fileSize)) {
        std::cerr << "Error getting file size: " << GetLastError() << std::endl;
        return false;
    }
    return true;
}

void closeFile(HANDLE fileHandle) {
    CloseHandle(fileHandle);
}

void readAndProcessFile(const std::string &inputFilename, const std::string &outputFilename) {
    HANDLE hInput = openFile(inputFilename, GENERIC_READ, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL);
    if (hInput == INVALID_HANDLE_VALUE) return;

    HANDLE hOutput = openFile(outputFilename, GENERIC_WRITE, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL);
    if (hOutput == INVALID_HANDLE_VALUE) {
        closeFile(hInput);
        return;
    }

    LARGE_INTEGER fileSize;
    if (!getFileSize(hInput, fileSize)) {
        closeFile(hInput);
        closeFile(hOutput);
        return;
    }

    std::vector<char> buffer(fileSize.QuadPart);
    DWORD bytesRead = 0;
    DWORD bytesWritten = 0;
    LONGLONG totalBytesRead = 0;

    auto startTime = std::chrono::high_resolution_clock::now();

    while (ReadFile(hInput, buffer.data(), fileSize.QuadPart, &bytesRead, nullptr) && bytesRead > 0) {
        totalBytesRead += bytesRead;
        displayProgressBar(static_cast<double>(totalBytesRead) / fileSize.QuadPart);

        processData(buffer, bytesRead);

        if (!WriteFile(hOutput, buffer.data(), bytesRead, &bytesWritten, nullptr)) {
            std::cerr << "Error writing file: " << GetLastError() << std::endl;
            break;
        }
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsedTime = endTime - startTime;
    std::cout << "\nElapsed time: " << elapsedTime.count() << " seconds\n";

    closeFile(hInput);
    closeFile(hOutput);
}

void readAndProcessFileAsync(const std::string &inputFilename, const std::string &outputFilename, int numStreams) {
    HANDLE hInput = openFile(inputFilename, GENERIC_READ, OPEN_EXISTING, FILE_FLAG_OVERLAPPED);
    if (hInput == INVALID_HANDLE_VALUE) return;

    HANDLE hOutput = openFile(outputFilename, GENERIC_WRITE, CREATE_ALWAYS, FILE_FLAG_OVERLAPPED);
    if (hOutput == INVALID_HANDLE_VALUE) {
        closeFile(hInput);
        return;
    }

    LARGE_INTEGER fileSize;
    if (!getFileSize(hInput, fileSize)) {
        closeFile(hInput);
        closeFile(hOutput);
        return;
    }

    int chunkSize = fileSize.QuadPart / numStreams;
    std::vector<OVERLAPPED> olRead(numStreams);
    std::vector<OVERLAPPED> olWrite(numStreams);
    std::vector<HANDLE> events(numStreams);
    std::vector<HANDLE> wevents(numStreams);
    std::vector<std::vector<char> > buffers(numStreams, std::vector<char>(chunkSize));
    std::vector<DWORD> bytesRead(numStreams, 0);
    std::vector<DWORD> bytesWritten(numStreams, 0);

    for (int i = 0; i < numStreams; ++i) {
        events[i] = CreateEvent(nullptr, TRUE, FALSE, nullptr);
        olRead[i].hEvent = events[i];
        olRead[i].Offset = i * chunkSize;
    }

    for (int i = 0; i < numStreams; ++i) {
        wevents[i] = CreateEvent(nullptr, TRUE, FALSE, nullptr);
        olWrite[i].hEvent = events[i];
        olWrite[i].Offset = i * chunkSize;
    }

    auto startTime = std::chrono::high_resolution_clock::now();

    LONGLONG totalBytesRead = 0;
    bool moreData = true;

    while (moreData) {
        for (int i = 0; i < numStreams; ++i) {
            ResetEvent(events[i]);
            if (!ReadFile(hInput, buffers[i].data(), chunkSize, nullptr, &olRead[i]) && GetLastError() !=
                ERROR_IO_PENDING) {
                std::cerr << "Error reading file: " << GetLastError() << std::endl;
                moreData = false;
                break;
            }
        }
        
        WaitForMultipleObjects(numStreams, events.data(), TRUE, INFINITE);

        for (int i = 0; i < numStreams; ++i) {
            if (!GetOverlappedResult(hInput, &olRead[i], &bytesRead[i], FALSE) || bytesRead[i] == 0) {
                moreData = false;
                break;
            }

            totalBytesRead += bytesRead[i];
            displayProgressBar(static_cast<double>(totalBytesRead) / fileSize.QuadPart);

            processData(buffers[i], bytesRead[i]);

            ResetEvent(events[i]);
            if (!WriteFile(hOutput, buffers[i].data(), bytesRead[i], nullptr, &olWrite[i]) && GetLastError() !=
                ERROR_IO_PENDING) {
                std::cerr << "Error writing file: " << GetLastError() << std::endl;
                moreData = false;
                break;
            }

            // WaitForSingleObject(olWrite[i].hEvent, INFINITE);
            // GetOverlappedResult(hOutput, &olWrite[i], &bytesWritten[i], TRUE);

            olRead[i].Offset += numStreams * chunkSize;
        }
        WaitForMultipleObjects(numStreams, wevents.data(), TRUE, INFINITE);
        for (int i = 0; i < numStreams; ++i) {
            GetOverlappedResult(hInput, &olWrite[i], &bytesWritten[i], FALSE);
        }
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsedTime = endTime - startTime;
    std::cout << "\nElapsed time: " << elapsedTime.count() << " seconds\n";

    for (HANDLE event: events) {
        CloseHandle(event);
    }
    closeFile(hInput);
    closeFile(hOutput);
}

int main() {
    std::string inputFilename = "input.txt";
    std::string outputFilename = "output.txt";
    int numThreads = 1024;

    std::cout << "ASYNC" << std::endl;
    readAndProcessFileAsync(inputFilename, outputFilename, numThreads);
    std::cout << "ODDS: " << oddcnt << std::endl << std::endl;

    oddcnt = 0;

    std::cout << "NO ASYNC" << std::endl;
    readAndProcessFile(inputFilename, outputFilename);
    std::cout << "ODDS: " << oddcnt << std::endl;

    getchar();
    return 0;
}

#include <fstream>
#include <iostream>
#include <random>
#include <string>

int main() {
    const std::string filename = "input.txt";
    const size_t fileSize = 1ULL * 1024 * 1024 * 1024; // 1GB
    const size_t bufferSize = 1024 * 1024; // 1MB buffer size

    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Error creating file!" << std::endl;
        return 1;
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(32, 126); // Printable ASCII range

    std::vector<char> buffer(bufferSize);

    size_t bytesWritten = 0;
    while (bytesWritten < fileSize) {
        for (auto &c: buffer) {
            c = static_cast<char>(dis(gen));
        }
        file.write(buffer.data(), buffer.size());
        bytesWritten += buffer.size();
        std::cout << "Progress: " << (bytesWritten * 100 / fileSize) << "%\r";
        std::cout.flush();
    }

    file.close();
    std::cout << "\n1GB file created successfully." << std::endl;

    return 0;
}

#include <iostream>
#include <fstream>
#include <string>
#include <locale>
#include <codecvt>

const std::wstring russian_lower = L"абвгдеёжзийклмнопрстувхцчшщьыъэюя";
const std::wstring russian_upper = L"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ";
const std::wstring english_lower = L"abcdefghijklmnopqrstuvwxyz";
const std::wstring english_upper = L"ABCDEFGHIJKLMNOPQRSTUVWXYZ";

bool is_rus(wchar_t c) {
    return (c >= L'а' && c <= L'я') || (c >= L'А' && c <= L'Я');
}

bool is_en(wchar_t c) {
    return (c >= L'a' && c <= L'z') || (c >= L'A' && c <= L'Z');
}

bool is_lower_rus(wchar_t c) {
    return (c >= L'а' && c <= L'я');
}

bool is_lower_en(wchar_t c) {
    return (c >= L'a' && c <= L'z');
}

wchar_t caesar_shift(wchar_t c, int shift, const std::wstring& alphabet) {
    size_t pos = alphabet.find(c);
    if (pos == std::wstring::npos) {
        return c; // Return character unchanged if not found in alphabet
    }
    size_t new_pos = (pos + shift + alphabet.size()) % alphabet.size();
    return alphabet[new_pos];
}

int main(int argc, char* argv[]) {
    setlocale(LC_CTYPE, "en_US.utf8");

    if (argc < 5) {
        std::cerr << "Usage: " << argv[0] << " <encode/decode> <filename> <shift> <alphabet_size>\n";
        return 1;
    }

    std::string mode = argv[1];
    std::string filename = argv[2];
    int shift = std::stoi(argv[3]);
    int alphabet_size = std::stoi(argv[4]);

    // Open file with wide character support
    std::wifstream file(filename);
    file.imbue(std::locale(file.getloc(), new std::codecvt_utf8<wchar_t>()));
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << "\n";
        return 1;
    }

    std::wstring line;

    while (std::getline(file, line)) {
        for (wchar_t& c : line) {
            if (alphabet_size == 33) {
                if (is_rus(c)) {
                    if (is_lower_rus(c)) {
                        c = caesar_shift(c, (mode == "encode" ? shift : -shift), russian_lower);
                    } else {
                        c = caesar_shift(c, (mode == "encode" ? shift : -shift), russian_upper);
                    }
                }
            } else if (alphabet_size == 26) {
                if (is_en(c)) {
                    if (is_lower_en(c)) {
                        c = caesar_shift(c, (mode == "encode" ? shift : -shift), english_lower);
                    } else {
                        c = caesar_shift(c, (mode == "encode" ? shift : -shift), english_upper);
                    }
                }
            } else {
                std::cerr << "Unsupported alphabet size: " << alphabet_size << "\n";
                return 1;
            }
        }
        std::wcout << line << L"\n"; // Output the processed line
    }

    file.close();
    return 0;
}
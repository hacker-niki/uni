#include <iostream>
#include <fstream>
#include <string>
#include <locale>
#include <codecvt>

const std::wstring russian_lower = L"абвгдеёжзийклмнопрстувхцчшщъыьэюя";
const std::wstring russian_upper = L"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ";
const std::wstring english_lower = L"abcdefghijklmnopqrstuvwxyz";
const std::wstring english_upper = L"ABCDEFGHIJKLMNOPQRSTUVWXYZ";

std::string mode;

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

std::wstring get_alphabet(wchar_t c) {
    if (is_rus(c)) {
        return is_lower_rus(c) ? russian_lower : russian_upper;
    }
    if (is_en(c)) {
        return is_lower_en(c) ? english_lower : english_upper;
    }
    return L"";
}

wchar_t vigenere_shift(wchar_t c, wchar_t key_char) {
    std::wstring alphabet_c = get_alphabet(c);
    std::wstring alphabet_key = get_alphabet(key_char);

    size_t pos = alphabet_c.find(c);
    size_t key_pos = alphabet_key.find(key_char);
    if (pos == std::wstring::npos || key_pos == std::wstring::npos) {
        return c;
    }
    size_t new_pos;
    if (mode == "encode") {
        new_pos = (pos + key_pos) % alphabet_c.size();
    } else {
        new_pos = (pos + alphabet_c.size() - key_pos) % alphabet_c.size();
    }
    return alphabet_c[new_pos];
}

std::wstring get_vigenere_key(const std::wstring& text, const std::wstring& key) {
    std::wstring extended_key;
    size_t key_length = key.length();
    for (size_t i = 0, j = 0; i < text.length(); ++i) {
        if (is_rus(text[i]) || is_en(text[i])) {
            extended_key += key[j % key_length];
            j++;
        } else {
            extended_key += text[i]; // Non-alphabetic characters are not encoded
        }
    }
    return extended_key;
}

int main(int argc, char* argv[]) {
    setlocale(LC_CTYPE, "en_US.utf8");

    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <encode/decode> <filename> <key_filename>\n";
        return 1;
    }

    mode = argv[1];
    std::string filename = argv[2];
    std::string key_filename = argv[3];

    // Open file with wide character support
    std::wifstream file(filename);
    file.imbue(std::locale(file.getloc(), new std::codecvt_utf8<wchar_t>()));
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << "\n";
        return 1;
    }

    std::wifstream key_file(key_filename);
    key_file.imbue(std::locale(key_file.getloc(), new std::codecvt_utf8<wchar_t>()));
    if (!key_file.is_open()) {
        std::cerr << "Error opening key file: " << key_filename << "\n";
        return 1;
    }

    std::wstring key;
    std::getline(key_file, key); // Read the key from the file
    key_file.close();

    std::wstring line;

    while (std::getline(file, line)) {
        std::wstring extended_key = get_vigenere_key(line, key);
        std::wstring output;

        for (size_t i = 0; i < line.length(); ++i) {
            wchar_t c = line[i];
            wchar_t key_char = extended_key[i];
            if (is_rus(c) || is_en(c)) {
                c = vigenere_shift(c, key_char);
            }
            output += c; // Append the processed character
        }
        std::wcout << output << L"\n"; // Output the processed line
    }

    file.close();
    return 0;
}
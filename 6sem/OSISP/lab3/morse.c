#include <stdio.h>
#include <string.h>
#include "morse.h"

typedef struct {
    char letter;
    const char* morse;
} MorseCode;

static MorseCode morse_table[] = {
    {'A', ".-"}, {'B', "-..."}, {'C', "-.-."}, {'D', "-.."},
    {'E', "."}, {'F', "..-."}, {'G', "--."}, {'H', "...."},
    {'I', ".."}, {'J', ".---"}, {'K', "-.-"}, {'L', ".-.."},
    {'M', "--"}, {'N', "-."}, {'O', "---"}, {'P', ".--."},
    {'Q', "--.-"}, {'R', ".-."}, {'S', "..."}, {'T', "-"},
    {'U', "..-"}, {'V', "...-"}, {'W', ".--"}, {'X', "-..-"},
    {'Y', "-.--"}, {'Z', "--.."},
    {'1', ".----"}, {'2', "..---"}, {'3', "...--"}, {'4', "....-"},
    {'5', "....."}, {'6', "-...."}, {'7', "--..."}, {'8', "---.."},
    {'9', "----."}, {'0', "-----"},
    {' ', "/"}
};

char* char_to_morse(char c) {
    for (long unsigned int i = 0; i < sizeof(morse_table) / sizeof(morse_table[0]); i++) {
        if (morse_table[i].letter == c) {
            return (char*)morse_table[i].morse;
        }
    }
    return NULL;
}

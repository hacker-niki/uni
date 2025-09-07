#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "morse.h"

void process_input() {
    char c;
    while ((c = fgetc(stdin)) != EOF) {
        char* morse_code = char_to_morse(toupper(c));
        if (morse_code) {
            printf("%s ", morse_code);
        }
    }
    printf("\n"); 
}

int main() {
    process_input();
    return EXIT_SUCCESS;
}

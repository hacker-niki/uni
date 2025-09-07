#include <iostream>


extern "C" int16_t *asm_foo(int8_t *a, int8_t *b, int8_t *c, int16_t *d);

int main() {
    int8_t a[] = {-1, 1, 127, -5, 1, -1, 1, 1},
            b[] = {-2, -17, 2, 2, 9, 2, 2, 2},
            c[] = {-1, 127, 2, 2, 2, 2, 2, 3};
    int16_t d[] = {3, 21, 3, 3, 3, -4, 3, 3};

    int16_t *tmp = asm_foo(a, b, c, d);

    for (int i = 0; i < 8; i++) {
        std::cout << static_cast<int>(tmp[i]) << ' ';
    }

    std::cout << std::endl;

    return 0;
}

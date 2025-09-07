#pragma once

#ifdef __cplusplus
#include <cstdint>

extern "C" {
#else //is pure C
#include <stdint.h>
#endif //__cplusplus

long long asm_foo(void);

void endMMX(void);

int16_t *eval(int8_t *a, int8_t *b, int8_t *c, int16_t *d);

#ifdef __cplusplus
} //End of extern "C" bloc
#endif //__cplusplus

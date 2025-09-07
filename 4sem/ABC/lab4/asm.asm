DEFAULT REL
section .text

global asm_foo
BITS 64

; void EndMMX();
global endMMX
endMMX:
    emms     ; Allow CPU to use floating point
    ret

section .text
global asm_foo

asm_foo:

    xorps xmm0, xmm0
    xorps xmm1, xmm1
    movlpd xmm1, [rsi]
    pcmpgtb xmm0, xmm1
    punpcklbw xmm1, xmm0

    xorps xmm0, xmm0
    xorps xmm2, xmm2
    movlpd xmm2, [rdx]
    pcmpgtb xmm0, xmm2
    punpcklbw xmm2, xmm0

    pmullw xmm1, xmm2

    xorps xmm0, xmm0
    xorps xmm2, xmm2
    movlpd xmm2, [rdi]
    pcmpgtb xmm0, xmm2
    punpcklbw xmm2, xmm0

    paddw xmm1, xmm2

    movupd xmm3, [rcx]

    paddw xmm1, xmm3

    movupd [F], xmm1
    mov rax, F
    ret
section .data
    F dw 0, 0, 0, 0, 0, 0, 0, 0
    one dq -1
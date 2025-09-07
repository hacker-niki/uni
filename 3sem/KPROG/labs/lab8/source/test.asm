public multiply
public LoudnessControl
public BalanceControl
public EchoControl
public EchoHandle


.data


first REAL4 ?
second REAL4 ?
third REAL4 ?
fourth REAL4 ?

                     ; Define variable first as 32-bit (4-byte float)
answer REAL4 0.0                                       ; REAL4 and DWORD are both same size.
                                   ; REAL4 makes for more readable code when using floats
.code
multiply PROC
    push rbp
    mov rbp, rsp                   ; Setup stack frame
                                   ; RSP aligned to 16 bytes at this point
    push rbx

    movd first, xmm0
    movd second, xmm1

    finit
    fld first                               ; at RBP+16 (this address is 16 byte aligned). Rather
    fld second                               ; than use a temporary variable in the data section to
    fmul st(0), st(1)                              ; store the value of RCX, we just store it to the
                                              ; shadow space on the stack.
    fstp [answer]

    movss xmm0, [answer]                              ; XMM0 = return value for 32(and 64-bit) floats
    pop rbx
    mov rsp, rbp                   ; Remove stack frame
    pop rbp
    ret
multiply ENDP

LoudnessControl PROC
    push rbp
    mov rbp, rsp                   ; Setup stack frame
                                   ; RSP aligned to 16 bytes at this point
    push rbx

    movd first, xmm0
    movd second, xmm1

    finit
    fld first                               ; at RBP+16 (this address is 16 byte aligned). Rather
    fld second                               ; than use a temporary variable in the data section to
    fmul st(0), st(1)                              ; store the value of RCX, we just store it to the
                                   ; shadow space on the stack.
    fstp [answer]

    movss xmm0, [answer]                              ; XMM0 = return value for 32(and 64-bit) floats
    pop rbx
    mov rsp, rbp                   ; Remove stack frame
    pop rbp
    ret
LoudnessControl ENDP

BalanceControl PROC
    push rbp
    mov rbp, rsp                   ; Setup stack frame
                                   ; RSP aligned to 16 bytes at this point
    push rbx

    movd first, xmm0
    movd second, xmm1

    finit
    fld first                               ; at RBP+16 (this address is 16 byte aligned). Rather
    fld second                               ; than use a temporary variable in the data section to
    fmul st(0), st(1)                              ; store the value of RCX, we just store it to the
                                   ; shadow space on the stack.
    fstp [answer]

    movss xmm0, [answer]                              ; XMM0 = return value for 32(and 64-bit) floats
    pop rbx
    mov rsp, rbp                   ; Remove stack frame
    pop rbp
    ret
BalanceControl ENDP

EchoControl PROC
    push rbp
    mov rbp, rsp                   ; Setup stack frame
                                   ; RSP aligned to 16 bytes at this point
    push rbx

    movd first, xmm0
    movd second, xmm1

    finit
    fld first                               ; at RBP+16 (this address is 16 byte aligned). Rather
    fld second                               ; than use a temporary variable in the data section to
    fadd st(0), st(1)                              ; store the value of RCX, we just store it to the
                                   ; shadow space on the stack.
    fstp [answer]

    movss xmm0, [answer]                              ; XMM0 = return value for 32(and 64-bit) floats
    pop rbx
    mov rsp, rbp                   ; Remove stack frame
    pop rbp
    ret
EchoControl ENDP

EchoHandle PROC
    push rbp
    mov rbp, rsp                   ; Setup stack frame
                                   ; RSP aligned to 16 bytes at this point
    push rbx

    movd first, xmm0
    movd second, xmm1

    finit
    fld second                               ; at RBP+16 (this address is 16 byte aligned). Rather
    fld first                               ; than use a temporary variable in the data section to
    fdiv st(0), st(1)                              ; store the value of RCX, we just store it to the
                                   ; shadow space on the stack.
    fstp [answer]

    movss xmm0, [answer]                              ; XMM0 = return value for 32(and 64-bit) floats
    pop rbx
    mov rsp, rbp                   ; Remove stack frame
    pop rbp
    ret
EchoHandle ENDP
END
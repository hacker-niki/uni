DEFAULT REL
global calcSum
; BITS 64
section .data
two: dq 2.0
one: dq 1.0
none: dq -1.0
tmp: dq 0.0
tmp2: dq 0.0
section .text

calcSum: 
    ; rdi - S
    ; rsi - k
    ; rcx - x
    finit   

    ; cos (2k-1)*x
    fld qword [rsi]
    fld qword [two]
    fmul
    
    fld qword [one]
    fsub
    
    fld qword [rdx]
    fmul
    
    fcos
    
    fst qword[tmp]
    
    ;2k-1
    fld qword [rsi]
    fld qword [two]
    fmul
    
    fld qword [one]
    fsub
    
    fst qword [tmp2]
    
    fld qword [tmp2]
    fld qword [tmp2]
    fmul
    
    fst qword [tmp2]
    
    fld qword [tmp]
    fld qword [tmp2]
    
    fdiv
    
    ;s+=s[k]
    fld qword [rdi]
    fadd
    
    fst qword [rdi]
    
    ret

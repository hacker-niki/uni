DEFAULT REL
global calcY

section .data
eight: dq 8.0
four: dq 4.0
tmp: dq 0.0
tmp2: dq 0.0
section .text

calcY:
    finit
    
    ;pi^2/8
    fldpi
    fldpi
    fmul
    fld qword [eight]
    fdiv 
    fstp qword [tmp]

    ;pi/4*x    
    fldpi
    fld qword [four]
    fdiv
    fld qword [rdi]
    fmul
    
    fstp qword [tmp2]
    fld qword [tmp]
    fld qword [tmp2]
    
    fsub
    
    fst qword [rax]

    ret

section .data
    val: dq 1
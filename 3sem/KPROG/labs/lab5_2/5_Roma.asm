; multi-segment executable file template.

data segment
    tmp_str db 5, 0, 5 dup ('$')
    num_str db 5, 0, 5 dup ('$')
    numstr db 10 dup ('$')
    num dw 0
    numa dw 0
    numb dw 0
    zero_c db '0'
    nine_c db '9'
    inpf_str db "input first number$"  
    inps_str db "input second number$"
    inp_str db "Input what to do:", 0Dh, 0Ah, " 1 - a and b", 0Dh, 0Ah, " 2 - a or b", 0Dh, 0Ah, " 3 - a xor b", 0Dh, 0Ah, " 4 - not a", 0Dh, 0Ah, " 5 - exit$"
    out_str db "ans: $"                              
    i db 0
    pkey db "press any key...$"
    incn db "incorrect number, try one more time$"
    ok_str db "OK$" 
    clrf db 0Dh, 0Ah, '$'
ends        

stack segment
    dw   128  dup(0)
ends

code segment
     
; prtint new line
print_nl macro
    PUSHA
    lea dx, clrf  
    mov ah, 9h
    int 21h
    POPA
endm
                 
; prtint a string
print_str macro str
    PUSHA
    lea dx, str
    mov ah, 9
    int 21h  
    lea dx, clrf
    int 21h
    POPA
endm

reverse_str macro sii
    LOCAL find_end, rev, done
    PUSHA
    mov si, sii
    mov di, si

find_end:
    lodsb
    cmp al, '$'
    jne find_end
    sub si, 2

rev:
    cmp di, si
    jge done

    mov cl, [di]
    mov al, [si]

    mov [si], cl
    mov [di], al

    dec si
    inc di
    jmp rev

done:
     POPA
endm

; num to string
num_to_str macro num, str
    LOCAL loopa, p4, ne 
    PUSHA
    mov ax, num
    lea si, str
    loopa:
    cmp ax, 0
    jge p4
    mov [si], '-'
    inc si
    neg ax
    p4:
    mov cx, 10
    div cl
    mov bh, ah
    add bh, 30h
    mov [si], bh
    inc si
    xor ah, ah
    cmp al, 0
    jne loopa
    mov [si], '$'
    
    lea si, str
    cmp [si], '-'
    jne ne
    inc si
    ne:
    reverse_str si
    POPA     
endm      

;string to num
str_to_num MACRO str, result
    LOCAL pl, ng, done, enda, pq
    PUSHA
    mov ax, 0
    mov bx, 0    ; Clear the result register
    mov cx, 10           ; Set the base to 10
    lea si, str       ; Point SI to the string buffer

    mov bl, [si]
    cmp bl, '-'          ; Check if the number is negative
    je ng

pl:
    cmp bl, '$'            ; Check for the null terminator
    je done

    sub bl, '0'          ; Convert character to digit
    
    mul cx               ; Multiply result by 10
    add ax, bx       ; Add the digit to the result

    inc si               ; Move to the next character
    mov bl, [si]         ; Load the next character
    jmp pl

ng:
    inc si
    mov bl, [si]               ; Skip the negative sign
    jmp pl

pq:
   neg ax
   jmp enda   
   
done:
    lea si, str
    mov bl, [si]
    cmp bl, '-'
    je pq
enda:
    mov result, ax     
    POPA
ENDM



; input a string:
input_str macro str
    PUSHA
    lea dx, str
    mov ah, 0Ah
    int 21h
    POPA
endm
            
            
;check if char is a number
check_num macro c_num
    LOCAL nn, an, exit
    PUSHA
    mov cx, 1
    cmp zero_c, c_num
    jg nn
    cmp nine_c, c_num 
    jb nn
    jmp an
    nn:
    cmp cx, 0    
    jmp exit
    an:
    cmp cx, 1
    exit:
    POPA
endm

;input a number
input_num macro tmpstr, numstr 
    LOCAL tryAgain, start, lup, lupa, ne, endStr, exit
    PUSHA
    
    jmp start
    tryAgain:
    print_nl
    print_str incn
    start:
    lea ax, num
    input_str tmpstr
    
    ;check that contains only numbers
    lea si, tmpstr
    cld
    mov cx, si[1]
    cmp si[2], '-'
    jne ne
    inc si
    ne:
    add si, 2
    lup:
    
    cmp [si], 0Dh
    je endStr
    
    mov al, [si]
    check_num al
    jne tryAgain
    inc si
    loop lup
    
    endStr:
    
    mov [si], '$'
    lea si, tmpstr
    lea di, numstr
    lupa:
    mov al, si[2]
    mov [di], al
    
    cmp si[2], '$'
    je exit
    
    inc si
    inc di
    
    jmp lupa
    exit:
    POPA
endm    
         
         
; program end, any key                 
program_end macro
    lea dx, pkey
    mov ah, 9
    int 21h        ; output string at ds:dx
    
    ; wait for any key....    
    mov ah, 1
    int 21h
    
    mov ax, 4c00h ; exit to operating system.
    int 21h    
endm    
    
start:
    ; set segment registers:
    mov ax, data
    mov ds, ax
    mov es, ax
    
    print_str inpf_str
    input_num tmp_str numstr
    str_to_num numstr num
    mov ax, num
    mov numa, ax
            
    print_nl        
    
    print_str inps_str
    input_num tmp_str numstr
    str_to_num numstr num
    mov bx, num
    mov numb, bx
    
    p1:
    
    print_nl
    
    print_str inp_str
    print_nl         
    
    input_num tmp_str numstr
    print_nl
    str_to_num numstr num
    mov cx, num
    
    cmp cx, 0
    jl p1
    cmp cx, 5
    jg p1
    
    cmp cx, 1
    je j1
    cmp cx, 2
    je j2
    cmp cx, 3
    je j3
    cmp cx, 4
    je j4
    jmp exit
    
    j1:
    mov ax, numa
    and ax, bx
    num_to_str ax numstr
    print_str out_str
    print_str numstr
    print_nl
    jmp p1
    
    j2:
    mov ax, numa     
    or ax, bx
    num_to_str ax numstr
    print_str out_str
    print_str numstr
    print_nl
    jmp p1
    
    j3:
    mov ax, numa
    xor ax, bx
    num_to_str ax numstr
    print_str out_str
    print_str numstr
    print_nl
    jmp p1
    
    j4:
    mov ax, numa
    not ax
    num_to_str ax numstr
    print_str out_str
    print_str numstr
    print_nl
    jmp p1
    
    ;num_to_str ax numstr
    ;print_str numstr
    
    ;num_to_str bx numstr
    ;print_str numstr
    
    exit:
    program_end        

ends

end start ; set entry point and stop the assembler.

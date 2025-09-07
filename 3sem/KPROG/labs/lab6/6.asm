
; You may customize this and other start-up templates; 
; The location of this template is c:\emu8086\inc\0_com_template.txt

org 100h
jmp start
   
    type db 100h dup(?)
    
    ; add your data here!
    
    word db 10, 0, 10 dup (0)
    iter dw 0
    tmp_str db 10 dup(0), '$'
    path_input db 100 dup(0)
    path_output db "output.txt", 0
 
    sz1 dw 0
    sz2 dw 0
    ptr dw 0
    
    ;system vars, don't touch this!!!
    ;files
    handle_input dw 0
    handle_output dw 0
    input_char db 0, '$'
    input_string db 100 dup(0), '$'
    
    
    len1 db 0
    len2 db 0
    string_sz dw 0
    
    error_str db "ahtung!!!$"
    
    ;sort
    num dw 0
    arr_size dw 0
    arr dw 30 dup (0)
    i dw 0
    piv dw 0
    begi dw 0
    endi dw 0
    l dw 0
    r dw 0
    ;input-output
    zero_c db '0'
    nine_c db '9'
    pkey db "press any key...$"
    clrf db 0dh, 0ah, '$'

.code
           
; prtint a string
print_str macro str
    pusha
    lea dx, str
    mov ah, 9
    int 21h  
    lea dx, clrf
    int 21h
    popa
endm

; prtint a string, no new line
print_str_nnl macro str
    pusha
    lea dx, str
    mov ah, 9
    int 21h
    popa
endm

reverse_str macro sii
    local find_end, rev, done
    pusha
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
     popa
endm

; num to string
num_to_str macro num, stri
    local loopa, p4, ne 
    pusha
    mov ax, num
    lea si, stri
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
    
    lea si, stri
    cmp [si], '-'
    jne ne
    inc si
    ne:
    reverse_str si
    popa     
endm      

;string to num
str_to_num macro str, result
    local pl, ng, done, enda, pq, overflow, st
    pusha
    jmp st
    overflow:
    print_nl
    print_str incn
    jmp start
    st:
    mov ax, 0
    mov bx, 0    ; clear the result register
    mov cx, 10           ; set the base to 10
    lea si, str       ; point si to the string buffer

    mov bl, [si]
    cmp bl, '-'          ; check if the number is negative
    je ng

pl:
    cmp bl, '$'            ; check for the null terminator
    je done

    sub bl, '0'          ; convert character to digit
    
    mul cx
    jo overflow               ; multiply result by 10
    add ax, bx       ; add the digit to the result

    inc si               ; move to the next character
    mov bl, [si]         ; load the next character
    jmp pl

ng:
    inc si
    mov bl, [si]               ; skip the negative sign
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
    popa
endm



; input a string:
input_str macro str
    pusha
    lea dx, str
    mov ah, 0ah
    int 21h
    popa
endm
            
            
;check if char is a number
check_num macro c_num
    local nn, an, exit
    pusha
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
    popa
endm

;input a number
input_num macro tmpstr, numstr 
    local tryagain, start, lup, lupa, ne, endstr, exit
    pusha
    
    jmp start
    tryagain:
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
    
    cmp [si], 0dh
    je endstr
    
    mov al, [si]
    check_num al
    jne tryagain
    inc si
    loop lup
    
    endstr:
    
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
    popa
endm   
    
;open a file    
open_file macro path, hand, mode
    local error, endmacro
    mov ah, 3dh              ;dos 3dh
    mov al, mode              
    lea dx, path      
    ;file name
    xor cx, cx               ;no attributes
    int 21h   
    jc error                 ;if error
    mov hand, ax
    jmp endmacro
    error:
    print_str error_str
    jmp exit
    endmacro:
endm

close_file macro hand
    mov ah, 3eh
    mov bx, hand
    int 21h
endm

read_symbol proc ;input_char - char
    mov ah, 3fh
    mov cx, 1
    mov bx, handle_input
    lea dx, input_char
    int 21h
    cmp ax, 1
    jne pq
    ret
pq:
    stc
    ret
read_symbol endp

read_string proc
    mov ax, 0
    mov string_sz, ax
    lea si, input_string
lup:
    call read_symbol
    jc error
    lea di, input_char
    mov al, [di]
    mov [si], al
    inc string_sz
    inc si
    cmp al, 10
    jne lup
    mov al, 0
    mov [si], al
    ret
    
error:
    inc si
    mov al, 0
    mov [si], al
    ret
read_string endp 
    
;write a string to the file
write_str macro size, stri
    pusha
    mov ah, 40h
    mov bx, handle_output
    mov cx, size
    lea dx, stri
    int 21h
    popa
endm
    
; program end, any key                 
program_end macro      
    mov ax, 4c00h ; exit to operating system.
    int 21h   
endm

find proc
    lea si, input_string
    lea di, word
    
    mov ax, si
    mov ptr, ax          
              
    mov sz1, 0
    mov sz2, 0
    
    lup4:
    inc sz1
    inc si
    cmp [si], 0
    jne lup4
    
    lup2:
    inc sz2
    inc di
    cmp [di], 0
    jne lup2
    
    lea si, input_string
    lea di, word
    
    lup3:
    mov cx, sz2
    repe cmpsb
    jz found
    lea di, word
    inc ptr
    mov ax, sz1
    lea bx, input_string
    add ax, bx
    cmp ax, ptr
    je notfound
    mov si, ptr
    jmp lup3
    
found:
    mov bx, si
    cmp si[1], ' '
    cmp si[1], 0
    
    
found2:    
    sub bx, sz2
    
    
    mov ax, 1
    jmp ex
    notfound:
    mov ax, 0
ex:
    ret
endp

    
start:
    mov si, 80h
    xor cx, cx
    mov cl, [si]
    add si, 2
    sub cx, 2
    lea di, path_input
    
lupp:
    mov ax, [si]
    mov [di], ax
    inc si
    inc di
    loop lupp
    
    open_file path_input, handle_input, 0
    open_file path_output, handle_output, 1
    
    input_str word
    
    lea si, word
    xor cx, cx 
    mov cl, si[1]
    lll:
    mov al, si[2]
    mov [si], al
    inc si
    loop lll
    mov ax, 0
    mov [si], al
    
lup1:
    call read_string
    jc lupend
    call find
    cmp ax, 0
    je write
    jmp lup1
    
write:
    write_str string_sz, input_string
    jmp lup1

lupend:
    call find
    cmp ax, 1
    je exit
    
    
    write_str string_sz, input_string
    
    exit:
    close_file handle_input
    close_file handle_output   
    
    
    program_end 


ret





; multi-segment executable file template.

data segment
    tmp_str db 6, 0, 6 dup ('$')
    num_str db 6, 0, 6 dup ('$')
    numstr db 10 dup ('$')
    num dw 0
    
    arr_size dw 0
    arr dw 30 dup (0)
    i dw 0
    piv dw 0
    begi dw 0
    endi dw 0
    l dw 0
    r dw 0
    
    zero_c db '0'
    nine_c db '9'
    inpn_str db "input number of elements$"  
 
    inp_str1 db "a[$"
    inp_str2 db "] = $"
    out_str db "ans: $"                              
    pkey db "press any key...$"
    incn db "incorrect number, try one more time$"
    ok_str db "ok$" 
    clrf db 0dh, 0ah, '$'
ends        

stack segment
    dw   128  dup(0)
ends

code segment
    
swap proc
    xor ax, bx
    xor bx, ax
    xor ax, bx
    
    ret
swap endp    

;void sort(int arr[], int beg, int end)
;{
;  if (end > beg + 1)
;  {
;    int piv = arr[beg], l = beg + 1, r = end;
;    while (l < r)
;    {
;      if (arr[l] <= piv)
;        l++;
;      else
;        swap(&arr[l], &arr[--r]);
;    }
;    swap(&arr[--l], &arr[beg]);
;    sort(arr, beg, l);
;    sort(arr, r, end);
;  }
;}
;

sort proc
    ;beg - cx
    ;end - dx
    ;arr - arr variable
    ;arr size - arr_size
    ;piv
    
    mov begi, cx
    mov endi, dx
    
;  if (end > beg + 1)    
    add begi, 2
    cmp dx, begi
    jle exit
    sub begi, 2
    
;   int piv = arr[beg], l = beg + 1, r = end;    
    mov si, begi
    mov ax, [si]
    mov piv, ax
    
    add begi, 2
    mov ax, begi
    mov l, ax
    sub begi, 2
    
    mov ax, endi
    mov r, ax
    
;   while (l < r)
    lup:
    mov ax, l
    cmp ax, r
    jge endlup
    
;   if (arr[l] <= piv)    
    mov ax, piv
    mov si, l
    cmp [si], ax
    jg else
    
;   l++;
    add l, 2

;   else    
    else:

;   swap(&arr[l], &arr[--r]);
    mov si, l
    mov ax, [si]
    sub r, 2
    mov si, r
    mov bx, [si]
    mov [si], ax
    mov si, l
    mov [si], bx     
    jmp lup
    endlup:

;   swap(&arr[--l], &arr[beg]);
    sub l, 2
    mov si, l
    mov ax, [si]
    mov si, begi
    mov bx, [si]
    mov si, l
    mov [si], bx
    mov si, r
    mov [si], ax         
    
;   sort(arr, beg, l);
    ;beg - cx
    ;end - dx
    ;arr - arr variable
    ;arr size - arr_size
    ;piv
    
    mov cx, begi
    mov dx, l
    call sort
;   sort(arr, r, end);    
    mov cx, r
    mov dx, endi
    call sort
    
    exit:
    sub cx, 2
    ret
sort endp
     
; prtint new line
print_nl macro
    pusha
    lea dx, clrf  
    mov ah, 9h
    int 21h
    popa
endm
                 
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
num_to_str macro num, str
    local loopa, p4, ne 
    pusha
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
           
    p1:           
    print_str inpn_str
    input_num tmp_str numstr
    str_to_num numstr num
    mov ax, num
    mov arr_size, ax
            
    print_nl        
    
    cmp arr_size, 1
    jl p1
    cmp arr_size, 30
    jg p1
    
    mov cx, arr_size
    lea si, arr
    
    lupa:
    print_str_nnl inp_str1
    num_to_str i, tmp_str
    print_str_nnl tmp_str
    print_str_nnl inp_str2
    input_num tmp_str numstr
    str_to_num numstr num
    mov ax, num
    mov [si], ax
    add si, 2
    inc i
    print_nl
    loop lupa
    
    lea si, arr
    mov cx, si
    mov ax, arr_size
    mov bl, 2
    mul bl
    mov dx, cx
    add dx, ax
    
    call sort
    
    mov cx, arr_size
    lea si, arr
    mov i, 0
    
    print_nl
    print_nl
    
    lupa1:
    print_str_nnl inp_str1
    num_to_str i, tmp_str
    print_str_nnl tmp_str
    print_str_nnl inp_str2
    num_to_str [si], tmp_str
    print_str tmp_str
    add si, 2
    inc i
    loop lupa1
    
    ex:
    program_end        

ends

end start ; set entry point and stop the assembler.

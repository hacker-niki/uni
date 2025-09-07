.model small

.data
print_message_begin db "Enter the string (max - 200 symbols)",0Dh, 0Ah, '$'
print_message_end db 0Dh, 0Ah, "Your modified string: ", 0Dh, 0Ah, '$'
buffer db 200, 0, 200 dup('$')
buffer_for_dollar db , "$"
enter db 0Dh, 0Ah, "$"
.stack 100h

.code
org 100h
main:
mov ax, @data
mov ds, ax
mov dx, offset print_message_begin
mov ah, 9
int 21h

; Enter string
lea dx, buffer
mov ah, 0Ah
int 21h

mov dx, offset enter
mov ah, 9
int 21h

mov si, 2
mov di, 0
mov cl, buffer[1]
jmp proccess_scanning

preendr:
    jmp endr

proccess_scanning:
    cmp cl, 0
    je preendr

    mov ah, buffer[si]
    cmp ah, 32    ; Check if it is a space
    je skip_space

    mov dl, buffer[si]
    mov buffer[di], dl
    inc di

skip_space:
    inc si
    dec cl
    jmp proccess_scanning

endr:
    mov buffer[di], '$'

    mov dx, offset print_message_end
    mov ah, 9
    int 21h

    lea dx, buffer
    mov ah, 9
    int 21h

    jmp exit_program

exit_program:
    mov ah, 4Ch
    int 21h

end main
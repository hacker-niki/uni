.model small
.data
message db "You opened the third file", 0Ah, 0Dh, "$"
.code
main:
mov ax, @data
mov ds, ax
mov dx, offset message
mov ah, 09h
int 21h
mov ah, 4ch
int 21h
end main
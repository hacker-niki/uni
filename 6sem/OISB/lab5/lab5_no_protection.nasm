section .data
    buffer1 db 10 dup(0)
    buffer2 db 'unprotected', 0xA

section .text
    global _start

_start:

	mov eax, 3
    mov ebx, 0
    mov ecx, buffer1
    mov edx, 20
    int 0x80
    
    mov eax, 4            
    mov ebx, 1            
    mov ecx, buffer1      
    mov edx, 10           
    int 0x80
 
    mov eax, 4           
    mov ebx, 1           
    mov ecx, buffer2      
    mov edx, 12           
    int 0x80

    mov eax, 1            
    xor ebx, ebx          
    int 0x80

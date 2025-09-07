[bits 16]
switch_to_pm:
    cli ; 1. disable interrupts
    lgdt [gdt_descriptor] ; 2. load the GDT descriptor
    mov eax, cr0
    or eax, 0x1 ; 3. set 32-bit mode bit in cr0
    mov cr0, eax
    jmp CODE_SEG:init_pm ; 4. far jump by using a different segment

[bits 32]
init_pm: ; we are now using 32-bit instructions
    mov ax, DATA_SEG ; 5. update the segment registers
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    mov ebp, 0x90000 ; 6. update the stack right at the top of the free space
    mov esp, ebp
    call BEGIN_PM ; 7. Call a well-known label with useful code

[bits 16]
switch_to_rm:
    ; Load real mode segment selectors into data segment registers
    mov ax, DATA_SEG_16 
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    cli                     ; 1. Disable interrupts

    ; Clear the protected mode enable (PE) bit in CR0
    mov eax, cr0
    and al, 0xFE     ; 3. Clear the PE bit to switch back to real mode
    mov cr0, eax



    ; Perform a far jump to flush the instruction pipeline and enter real mode
    jmp CODE_SEG:real_mode_entry
    jmp $


[bits 16]
real_mode_entry:
    ; Reset the stack segment register
    mov ebp, 0x90000        ; 2. Set stack pointer for real mode
    mov sp, bp
    sti                     ; 5. Enable interrupts

    ; Continue with real mode code
    call print
    jmp CODE_SEG:CONTINUE_RM
    jmp $

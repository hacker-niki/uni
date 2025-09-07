; Function to sort an array using Quick Sort algorithm
; Inputs:
;   - arr: pointer to the array to be sorted
;   - low: the starting index of the array
;   - high: the ending index of the array
; Outputs:
;   - The array is sorted in place
QUICK_SORT PROC
    ; Check if the array has more than one element
    mov ax, high
    sub ax, low
    cmp ax, 1
    jle QS_EXIT
    
    ; Partition the array and get the pivot index
    push high
    push low
    call PARTITION
    add sp, 4
    mov bx, ax
    
    ; Recursively sort the left and right sub-arrays
    mov ax, low
    sub ax, 1
    push bx
    push ax
    call QUICK_SORT
    add sp, 4
    
    mov ax, bx
    add ax, 1
    push high
    push ax
    call QUICK_SORT
    add sp, 8
    
QS_EXIT:
    ret
QUICK_SORT ENDP

; Function to partition an array for Quick Sort
; Inputs:
;   - arr: pointer to the array to be partitioned
;   - low: the starting index of the array
;   - high: the ending index of the array
; Outputs:
;   - The array is partitioned in place and the pivot index is returned in EAX
PARTITION PROC
    ; Set the pivot to the last element of the array
    mov ax, high
    mov cx, [arr + ax * 2]
    
    ; Initialize the partition index
    mov bx, low
    
    ; Loop through the array and partition it
    mov dx, low
    cmp dx, high
    jge PART_EXIT
PART_LOOP:
    mov si, [arr + dx * 2]
    cmp si, cx
    jg PART_NEXT
    mov si, [arr + bx * 2]
    mov [arr + dx * 2], si
    mov [arr + bx * 2], cx
    inc bx
PART_NEXT:
    inc dx
    jmp PART_LOOP
PART_EXIT:
    mov ax, bx
    dec ax
    ret
PARTITION ENDP
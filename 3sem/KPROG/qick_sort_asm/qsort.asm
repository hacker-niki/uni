; MULTI-SEGMENT EXECUTABLE FILE TEMPLATE.

DATA SEGMENT
    TMP_STR DB 6, 0, 6 DUP ('$')
    NUM_STR DB 6, 0, 6 DUP ('$')
    NUMSTR DB 10 DUP ('$')
    NUM DW 0
    
    ARR_SIZE DW 0
    ARR DW 30 DUP (0)
    I DW 0
    PIV DW 0
    BEGI DW 0
    ENDI DW 0
    L DW 0
    R DW 0
    
    ZERO_C DB '0'
    NINE_C DB '9'
    INPN_STR DB "INPUT NUMBER OF ELEMENTS$"  
 
    INP_STR1 DB "A[$"
    INP_STR2 DB "] = $"
    OUT_STR DB "ANS: $"                              
    PKEY DB "PRESS ANY KEY...$"
    INCN DB "INCORRECT NUMBER, TRY ONE MORE TIME$"
    OK_STR DB "OK$" 
    CLRF DB 0DH, 0AH, '$'
ENDS        

STACK SEGMENT
    DW   128  DUP(0)
ENDS

CODE SEGMENT
    
SWAP PROC
    XOR AX, BX
    XOR BX, AX
    XOR AX, BX
    
    RET
SWAP ENDP    

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

SORT PROC
    ;beg - cx
    ;end - dx
    ;arr - arr variable
    ;arr size - arr_size
    ;piv
    
    MOV BEGI, CX
    MOV ENDI, DX
    
;   if (end > beg + 1){    
    ADD BEGI, 2
    CMP DX, BEGI
    JLE EXIT
    SUB BEGI, 2
    
;   int piv = arr[beg], l = beg + 1, r = end;    
    MOV SI, BEGI
    MOV AX, [SI]
    MOV PIV, AX
    
    MOV AX, BEGI
    ADD AX, 2
    MOV L, AX
    
    
    MOV AX, ENDI
    MOV R, AX
    
;   while (l < r){
    LUP:
    MOV AX, L
    CMP AX, R
    JGE ENDLUP
    
;   if (arr[l] <= piv){    
    MOV AX, PIV
    MOV SI, L
    CMP [SI], AX
    JG ELSE
    
;   l++;
    ADD L, 2
    JMP LUP
;   }   
    
;   else{    
    ELSE:

;   swap(&arr[l], &arr[--r]);
    MOV SI, L
    MOV AX, [SI]
    SUB R, 2
    MOV SI, R
    MOV BX, [SI]
    MOV [SI], AX
    MOV SI, L
    MOV [SI], BX     
;   }

    JMP LUP
;   }    
    ENDLUP:

;   swap(&arr[--l], &arr[beg]);
    SUB L, 2
    MOV SI, L
    MOV AX, [SI]
    MOV SI, BEGI
    MOV BX, [SI]
    MOV SI, L
    MOV [SI], BX
    MOV SI, BEGI
    MOV [SI], AX         
    
;   sort(arr, beg, l);
    ;beg - cx
    ;end - dx
    ;arr - arr variable
    ;arr size - arr_size
    ;piv    
    MOV AX, R
    MOV BX, ENDI
    MOV CX, BEGI
    MOV DX, L
    PUSHA
    CALL SORT
    POPA
    MOV R, AX
    MOV ENDI, BX
    MOV BEGI, CX
    MOV L, DX      
    
;   sort(arr, r, end);    
    MOV AX, L
    MOV BX, BEGI
    MOV CX, R
    MOV DX, ENDI
    PUSHA
    CALL SORT
    POPA
    MOV L, AX
    MOV BEGI, BX
    MOV R, CX
    MOV ENDI, DX

;   }    
    EXIT:
    SUB CX, 2
    RET
SORT ENDP
     
; PRTINT NEW LINE
PRINT_NL MACRO
    PUSHA
    LEA DX, CLRF  
    MOV AH, 9H
    INT 21H
    POPA
ENDM
                 
; PRTINT A STRING
PRINT_STR MACRO STR
    PUSHA
    LEA DX, STR
    MOV AH, 9
    INT 21H  
    LEA DX, CLRF
    INT 21H
    POPA
ENDM

; PRTINT A STRING, NO NEW LINE
PRINT_STR_NNL MACRO STR
    PUSHA
    LEA DX, STR
    MOV AH, 9
    INT 21H
    POPA
ENDM

REVERSE_STR MACRO SII
    LOCAL FIND_END, REV, DONE
    PUSHA
    MOV SI, SII
    MOV DI, SI

FIND_END:
    LODSB
    CMP AL, '$'
    JNE FIND_END
    SUB SI, 2

REV:
    CMP DI, SI
    JGE DONE

    MOV CL, [DI]
    MOV AL, [SI]

    MOV [SI], CL
    MOV [DI], AL

    DEC SI
    INC DI
    JMP REV

DONE:
     POPA
ENDM

; NUM TO STRING
NUM_TO_STR MACRO NUM, STR
    LOCAL LOOPA, P4, NE 
    PUSHA
    MOV AX, NUM
    LEA SI, STR
    LOOPA:
    CMP AX, 0
    JGE P4
    MOV [SI], '-'
    INC SI
    NEG AX
    P4:
    MOV CX, 10
    DIV CL
    MOV BH, AH
    ADD BH, 30H
    MOV [SI], BH
    INC SI
    XOR AH, AH
    CMP AL, 0
    JNE LOOPA
    MOV [SI], '$'
    
    LEA SI, STR
    CMP [SI], '-'
    JNE NE
    INC SI
    NE:
    REVERSE_STR SI
    POPA     
ENDM      

;STRING TO NUM
STR_TO_NUM MACRO STR, RESULT
    LOCAL PL, NG, DONE, ENDA, PQ, OVERFLOW, ST
    PUSHA
    JMP ST
    OVERFLOW:
    PRINT_NL
    PRINT_STR INCN
    JMP START
    ST:
    MOV AX, 0
    MOV BX, 0    ; CLEAR THE RESULT REGISTER
    MOV CX, 10           ; SET THE BASE TO 10
    LEA SI, STR       ; POINT SI TO THE STRING BUFFER

    MOV BL, [SI]
    CMP BL, '-'          ; CHECK IF THE NUMBER IS NEGATIVE
    JE NG

PL:
    CMP BL, '$'            ; CHECK FOR THE NULL TERMINATOR
    JE DONE

    SUB BL, '0'          ; CONVERT CHARACTER TO DIGIT
    
    MUL CX
    JO OVERFLOW               ; MULTIPLY RESULT BY 10
    ADD AX, BX       ; ADD THE DIGIT TO THE RESULT

    INC SI               ; MOVE TO THE NEXT CHARACTER
    MOV BL, [SI]         ; LOAD THE NEXT CHARACTER
    JMP PL

NG:
    INC SI
    MOV BL, [SI]               ; SKIP THE NEGATIVE SIGN
    JMP PL

PQ:
   NEG AX
   JMP ENDA   
   
DONE:
    LEA SI, STR
    MOV BL, [SI]
    CMP BL, '-'
    JE PQ
ENDA:
    MOV RESULT, AX     
    POPA
ENDM



; INPUT A STRING:
INPUT_STR MACRO STR
    PUSHA
    LEA DX, STR
    MOV AH, 0AH
    INT 21H
    POPA
ENDM
            
            
;CHECK IF CHAR IS A NUMBER
CHECK_NUM MACRO C_NUM
    LOCAL NN, AN, EXIT
    PUSHA
    MOV CX, 1
    CMP ZERO_C, C_NUM
    JG NN
    CMP NINE_C, C_NUM 
    JB NN
    JMP AN
    NN:
    CMP CX, 0    
    JMP EXIT
    AN:
    CMP CX, 1
    EXIT:
    POPA
ENDM

;INPUT A NUMBER
INPUT_NUM MACRO TMPSTR, NUMSTR 
    LOCAL TRYAGAIN, START, LUP, LUPA, NE, ENDSTR, EXIT
    PUSHA
    
    JMP START
    TRYAGAIN:
    PRINT_NL
    PRINT_STR INCN
    START:
    LEA AX, NUM
    INPUT_STR TMPSTR
    
    ;CHECK THAT CONTAINS ONLY NUMBERS
    LEA SI, TMPSTR
    CLD
    MOV CX, SI[1]
    CMP SI[2], '-'
    JNE NE
    INC SI
    NE:
    ADD SI, 2
    LUP:
    
    CMP [SI], 0DH
    JE ENDSTR
    
    MOV AL, [SI]
    CHECK_NUM AL
    JNE TRYAGAIN
    INC SI
    LOOP LUP
    
    ENDSTR:
    
    MOV [SI], '$'
    LEA SI, TMPSTR
    LEA DI, NUMSTR
    LUPA:
    MOV AL, SI[2]
    MOV [DI], AL
    
    CMP SI[2], '$'
    JE EXIT
    
    INC SI
    INC DI
    
    JMP LUPA
    EXIT:
    POPA
ENDM    
         
         
; PROGRAM END, ANY KEY                 
PROGRAM_END MACRO
    LEA DX, PKEY
    MOV AH, 9
    INT 21H        ; OUTPUT STRING AT DS:DX
    
    ; WAIT FOR ANY KEY....    
    MOV AH, 1
    INT 21H
    
    MOV AX, 4C00H ; EXIT TO OPERATING SYSTEM.
    INT 21H    
ENDM    
    
START:
    ; SET SEGMENT REGISTERS: 
    MOV AX, DATA
    MOV DS, AX
    MOV ES, AX
           
    P1:           
    PRINT_STR INPN_STR
    INPUT_NUM TMP_STR NUMSTR
    STR_TO_NUM NUMSTR NUM
    MOV AX, NUM
    MOV ARR_SIZE, AX
            
    PRINT_NL        
    
    CMP ARR_SIZE, 1
    JL P1
    CMP ARR_SIZE, 30
    JG P1
    
    MOV CX, ARR_SIZE
    LEA SI, ARR
    
    LUPA:
    PRINT_STR_NNL INP_STR1
    NUM_TO_STR I, TMP_STR
    PRINT_STR_NNL TMP_STR
    PRINT_STR_NNL INP_STR2
    INPUT_NUM TMP_STR NUMSTR
    STR_TO_NUM NUMSTR NUM
    MOV AX, NUM
    MOV [SI], AX
    ADD SI, 2
    INC I
    PRINT_NL
    LOOP LUPA
    
    LEA SI, ARR
    MOV CX, SI
    MOV AX, ARR_SIZE
    MOV BL, 2
    MUL BL
    MOV DX, CX
    ADD DX, AX
    
    
    CALL SORT
    
    MOV CX, ARR_SIZE
    LEA SI, ARR
    MOV I, 0
    
    PRINT_NL
    PRINT_NL
    
    LUPA1:
    PRINT_STR_NNL INP_STR1
    NUM_TO_STR I, TMP_STR
    PRINT_STR_NNL TMP_STR
    PRINT_STR_NNL INP_STR2
    NUM_TO_STR [SI], TMP_STR
    PRINT_STR TMP_STR
    ADD SI, 2
    INC I
    LOOP LUPA1
    
    PRINT_NL
    PRINT_NL
                
                
    LEA SI, ARR
    
    MOV AX, ARR_SIZE
    MOV BX, 2
    DIV BL
    
    CMP AH, 0
    JNE P3
    XOR AH, AH
    MOV BL, 2
    MUL BL
    ADD SI, AX
    MOV AX, [SI]
    SUB SI, 2
    ADD AX, [SI]
    DIV BL
    xor cx, cx
    mov cl, ah
    XOR AH, AH
    JMP P4
    
    P3:
    XOR AH, AH
    MOV BL, 2
    MUL BL
    ADD SI, AX
    MOV AX, [SI]
    
    P4:
    PRINT_STR_NNL OUT_STR
    NUM_TO_STR AX, TMP_STR
    PRINT_STR TMP_STR
    NUM_TO_STR CX, TMP_STR
    PRINT_STR TMP_STR
    
    
    
    PRINT_NL
    
    EX:
    PROGRAM_END        

ENDS

END START ; SET ENTRY POINT AND STOP THE ASSEMBLER.

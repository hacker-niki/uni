 org $8000
 ldaa #$ff
 ldy #$8200
 clra
 ldx #0
p 
 ldab 0,y
 iny
 abx
 ldab #0
 deca
 bne p
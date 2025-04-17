

void __fastcall __macro getFarPointer( char far *obj<__fbank:__fptr>, unsigned int bank_p<__ax>, unsigned int addr_p<__bx> );

char __fastcall __macro getBank( char far *obj<__fbank:__fptr> );
char __fastcall __macro getAddress( char far *obj<__fbank:__fptr> );

#asm

_getBank.1 .macro


    .ifdef HUCC
            lda __fbank
            cly
    .else
            ldx __fbank
            cla
    .endif

 .endm

_getAddress.1 .macro


    .ifdef HUCC
            lda __fptr
            ldy __fptr + 1
    .else
            ldx __fptr
            lda __fptr + 1
    .endif

 .endm

_getFarPointer.3 macro

            lda __fbank
            sta [__ax]
            cly
            lda __fptr
            sta [__bx],y
            iny
            lda __fptr+1
            sta [__bx],y
 .endm

#endasm
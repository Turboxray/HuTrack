// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;
// ; HuTrack music engine for PC-Engine
// ;
// ; Ver: 0.8.6
// ;
// ; History:
// ; -------
// ;
// ;
// ;

char HuTrack_Arg_Pass_EAX0_l;
char HuTrack_Arg_Pass_EAX0_m;
char HuTrack_Arg_Pass_EAX0_h;
char HuTrack_Arg_Pass_EAX0_u;



// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;// Interface                                                                                               /
// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;interface

#pragma fastcall HuTrackEngine_QueueSong(farptr __fbank:__fptr);
#pragma fastcall HuTrackEngine_PlaySong(byte __al);
#pragma fastcall HuTrackEngine_PlayOnce(byte __al);
#pragma fastcall HuTrackEngine_Pause();
#pragma fastcall HuTrackEngine_Stop();
#pragma fastcall HuTrackEngine_ManualCall() macro;
#pragma fastcall HuTrackEngine_Vsync();
#pragma fastcall HuTrackEngine_Vsync(byte acc);
#pragma fastcall HuTrackEngine_SetGlobal(byte acc);
#pragma fastcall HuTrackEngine_SetGlobal(byte __al, byte __ah);

// #pragma fastcall HuTrackEngine_getSongTitle(byte __al, farptr __fbank:__fptr);
// #pragma fastcall HuTrackEngine_getSongAuthor(byte __al, farptr __fbank:__fptr);
#pragma fastcall HuTrackEngine_getCurrSongTitle(farptr __fbank:__fptr);
#pragma fastcall HuTrackEngine_getCurrSongAuthor(farptr __fbank:__fptr);

#pragma fastcall HuTrackEngine_chanSetSFX(byte __al);
#pragma fastcall HuTrackEngine_chanReleaseSFX(byte __al);

int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, unsigned char bank<__fbank>,   unsigned int addr<__fptr>, char mask1<__cl>, char mask2<__ch>);
int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, char far *pcm<__fbank:__fptr>, char mask1<__cl>,          char mask2<__ch> );
int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, unsigned char bank<__fbank>,   unsigned int addr<__fptr>);
int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, char far *pcm<__fbank:__fptr>);
int __fastcall HuTrackEngine_stopPcm   (unsigned char channel<__al>);
int __fastcall myTestFuncNotASM   (unsigned char channel<__al>);


int prevSubState1[20];
int subState1[20];
int subState2[20];
unsigned char vramSlot;
unsigned char temp;
extern unsigned int _ax, _bx, _cx;


void __fastcall __nop getAX (unsigned int tmp1<__ax>);
void __fastcall __nop getAX_BX (unsigned int tmp1<__ax>, unsigned int tmp2<__bx>);
void __fastcall __nop getAX_CX_BX (unsigned int tmp1<__ax>, unsigned int tmp2<__bx>, unsigned int tmp3<__cx>);

void __fastcall __nop getchangeSubState1Vars (unsigned int tmp1<_changeSubState1Var0>, unsigned int tmp2<_changeSubState1Var1>, unsigned int tmp3<_changeSubState1Var2>);

unsigned int changeSubState1Var0;
unsigned int changeSubState1Var1;
unsigned int changeSubState1Var2;

void changeSubState1 ( void )
{
    prevSubState1[vramSlot] = changeSubState1Var0;
    subState1[vramSlot]     = changeSubState1Var1;
    subState2[vramSlot]     = changeSubState1Var2;
}

void changeSubState0 ( unsigned int temp )
{
     prevSubState1[vramSlot] = temp;
    //  subState1[vramSlot]     = _bx;
    //  subState2[vramSlot]     = _cx;
}

void changeSubState3 ( unsigned int temp )
{
    // static unsigned int t;
    // t = temp;
    prevSubState1[vramSlot] = 1;
    //  subState1[vramSlot]     = _bx;
    //  subState2[vramSlot]     = _cx;
}


void changeSubState1_alt ( unsigned char SUB_STATE1, int* prevSubState1_p, int* subState1_p)
{
    static char idx;
    idx = SUB_STATE1;

    *((unsigned int*) (prevSubState1_p + vramSlot)) = *((unsigned int*) (subState1_p + vramSlot)) ;
    *((unsigned int*) (subState1_p + vramSlot)) = idx;

    //  prevSubState1[vramSlot]=subState1[vramSlot];
    //  subState1[vramSlot]=idx;
}


void changeSubState1_alt2 ( unsigned char SUB_STATE1, int* p_prevSubState1_p, int* p_subState1_p)
{
    static char idx;
    static unsigned int* prevSubState1_p, subState1_p;

    idx = SUB_STATE1;
    prevSubState1_p = p_prevSubState1_p;
    subState1_p     = p_subState1_p;

    *((unsigned int*) (prevSubState1_p + vramSlot)) = *((unsigned int*) (subState1_p + vramSlot)) ;
    *((unsigned int*) (subState1_p + vramSlot)) = idx;

}



int __fastcall __macro test222(unsigned char channel<__al>);
#asm
myFunc.1 .macro
    ; code
    lda __ax
.endm
#endasm


#pragma fastcall HuTrack_Init();


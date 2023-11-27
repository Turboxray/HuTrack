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
int __fastcall HuTrackEngine_SFXmode(unsigned char channel<__al>);
int __fastcall HuTrackEngine_SFXmode();
int __fastcall HuTrackEnginePauseDDA();
int __fastcall HuTrackEngineResumeDDA();
int __fastcall HuTrackEngineSFXrest(unsigned char channel<__al>);
int __fastcall HuTrackEngineSFXprocess();
int __fastcall HuTrackEngineSFXplay( char channel<__al>, unsigned char bank1<__fbank>, unsigned int addr1<__fptr>, unsigned char bank2<__cl>, unsigned int addr2<__bx>);

void __fastcall __nop getDataPtr(unsigned char far *my_data_label<__bl:__ax>);

#pragma fastcall HuTrack_Init();


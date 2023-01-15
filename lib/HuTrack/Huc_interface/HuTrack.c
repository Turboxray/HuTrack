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


#pragma fastcall HuTrack_Init();


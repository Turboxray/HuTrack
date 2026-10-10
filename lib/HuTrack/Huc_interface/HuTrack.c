#ifndef HUTRACK_C_INTERFACE
#define HUTRACK_C_INTERFACE

// Make the optional HuSFX group-volume hook visible before HuCC's final BSS.
#asm
HUTRACK_SFX_VOLUME = 1
#endasm

#define HUTRACK_STOPPED 0
#define HUTRACK_PLAYING 1
#define HUTRACK_PAUSED  2
#define HUTRACK_ENDED   3

// HuTrack music/PCM interface for HuC and HuCC 4.x.
// Call Init once before registering songs or acquiring SFX channels.

// Returns the queued song ID (0..63), or -1 if the 64-song catalog is full.
int __fastcall HuTrackEngine_QueueSong(char far *song<__fbank:__fptr>);
#pragma fastcall HuTrackEngine_PlaySong(byte __al);
#pragma fastcall HuTrackEngine_PlayOnce(byte __al);
#pragma fastcall HuTrackEngine_Pause();
#pragma fastcall HuTrackEngine_Stop();
#pragma fastcall HuTrackEngine_ManualCall() macro;
#pragma fastcall HuTrackEngine_SetGlobal(byte acc);
#pragma fastcall HuTrackEngine_SetGlobal(byte __al, byte __ah);

// Each metadata destination must provide at least 48 writable RAM bytes.
// Copy at most 47 text bytes plus NUL; these calls have no buffer-size argument.
#pragma fastcall HuTrackEngine_getCurrSongTitle(farptr __fbank:__fptr);
#pragma fastcall HuTrackEngine_getCurrSongAuthor(farptr __fbank:__fptr);

#pragma fastcall HuTrackEngine_chanReserve(byte __al);
#pragma fastcall HuTrackEngine_chanRelease(byte __al);


// Returns 0 for invalid/unreserved channels, header bank overflow, or empty
// loops; rejected requests preserve existing playback. Otherwise returns 1.
int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, unsigned char bank<__fbank>,   unsigned int addr<__fptr>, char mask1<__cl>, char mask2<__ch>);
int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, char far *pcm<__fbank:__fptr>, char mask1<__cl>,          char mask2<__ch> );
int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, unsigned char bank<__fbank>,   unsigned int addr<__fptr>);
int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, char far *pcm<__fbank:__fptr>);
int __fastcall HuTrackEngine_stopPcm   (unsigned char channel<__al>);
int __fastcall HuTrackEngine_PCMStatus(unsigned char channel<__al>); 	//Returns status of the PCM streaming
int __fastcall HuTrackEngine_SFXmode(unsigned char channel<__al>);
int __fastcall HuTrackEngine_SFXmode();
int __fastcall HuTrackEngineSFXrest(unsigned char channel<__al>);
// Suspend all PCM (music and SFX); 1 = changed, 0 = already in that state.
int __fastcall HuTrackEnginePauseDDA();
int __fastcall HuTrackEngineResumeDDA();

void __fastcall __nop getDataPtr(unsigned char far *my_data_label<__bl:__ax>);

#pragma fastcall HuTrack_Init();


// Music transport. Pause preserves note/PCM position; Stop cannot be resumed.
#pragma fastcall HuTrackEngine_Resume();
int __fastcall HuTrackEngine_Status();
int __fastcall HuTrackEngine_MusicVolume();
int __fastcall HuTrackEngine_SFXVolume();
// Reserved HuTrack PCM and HuSFX streams; same 0..31 levels as music below.
// SFX level persists across songs. Custom PSG writers manage their own volume.
#pragma fastcall HuTrackEngine_SetSFXVolume(byte __al);
// Level 31 = unchanged; level 0 = silent. Subtract (31-level) from each
// final 5-bit music volume, clamping at zero. PSG master/SFX unaffected.
// Applied at the next music update; a new song starts at level 31.
#pragma fastcall HuTrackEngine_SetMusicVolume(byte __al);
#pragma fastcall HuTrackEngine_FadeTo(byte __al, byte __ah);
#pragma fastcall HuTrackEngine_FadeOut(byte __al);
#pragma fastcall HuTrackEngine_FadeToPause(byte __al);
#pragma fastcall HuTrackEngine_FadeIn(byte __al);
// One-unit steps every N music updates (N=0 means immediate).
// FadeOut stops at zero; FadeToPause pauses; FadeIn resumes at zero toward 31.
int __fastcall HuTrackEngine_PollEvent(); // -1 empty, otherwise latest EE00..EEFF
int __fastcall HuTrackEngine_TryReserve(unsigned char channel<__al>); // 1 acquired

#endif

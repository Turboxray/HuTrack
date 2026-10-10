#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"
#include "HuSFX/HuC_interface/HucSFX.c"
#include "HuSFX/HuC_interface/HuVGM_defs.h"
#include "HuCsupport/HuCsupport.h"
#asm
.bank HUC_USER_RESERVED
#endasm
#incasmlabel(song, "constant/constant.song.inc", 2);
#incasmlabel(music_pcm, "pcm/pcm.song.inc", 2);
#incasmlabel(cut_pcm, "cut_pcm/cut_pcm.song.inc", 2);
#incasmlabel(cut_wave, "cut_wave/cut_wave.song.inc", 2);
#incasmlabel(wave_changes, "wave_changes/wave_changes.song.inc", 2);
#incasmlabel(delayed_retrigger, "delayed_retrigger/delayed_retrigger.song.inc", 2);
#incasmlabel(sfx_waves, "sfx_waves.inc", 2);
#incasmlabel(sfx, "sfx_a.inc", 2);
#incasmlabel(pcm, "pcm_cross.inc", 2);
#incasmlabel(short_pcm, "pcm_short.inc", 2);
#incasmlabel(empty_pcm, "pcm_empty.inc", 2);
#incasmlabel(empty_repeat_pcm, "pcm_empty_repeat.inc", 2);
extern char edge_pcm[];
const char edge_sfx[] = {HuPlayPCM(2), HuWait_frames(2), HuEndOfStream};
const char empty_loop[] = {HuLoopPCM(3), HuWait1frame, HuEndOfStream};
const char combined[] = {HuPlayPCM(0), HuWait_frames(2), HuStopPCM,
    HuChanWFupdate(0), HuPeriod(1,64), HuWFvol(31), HuWait_frames(2), HuEndOfStream};
const char looped[] = {HuLoopPCM(1), HuWait_frames(255), HuEndOfStream};
const char single[] = {HuPlayPCM(1), HuWait_frames(2), HuEndOfStream};
const char implicit_stop[] = {HuPlayPCM(0), HuWait1frame, HuChanWFupdate(0),
    HuWFvol(31), HuWait_frames(2), HuEndOfStream};
const char mode_stop[] = {HuPlayPCM(0), HuWait1frame, HuWFvol(31), HuWait1frame, HuEndOfStream};
const char eof_stop[] = {HuPlayPCM(0), HuWait1frame, HuEndOfStream};
const char invalid_pcm[] = {HuPlayPCM(64), HuWait1frame, HuEndOfStream};
const char invalid_flags[] = {0xfc, 0, 2, HuWait1frame, HuEndOfStream};
const char pcm_volume[] = {HuLoopPCM(1), HuDDAvol(19), HuWait_frames(255), HuEndOfStream};
const char pan_tone[] = {HuChanWFupdate(0), HuPeriod(1,64), HuWFvol(31),
    HuWait_frames(255), HuEndOfStream};
const char lfo_sfx[] = {0xa9,1, HuWait_frames(255), HuEndOfStream};
const char pan_levels[] = {0,0xf0,0x0f,0xff};
int error, done, stage, checks, count, frame, savedTick, savedRow, savedPcm, savedBank;
int snapTick, snapRow, snapPcm, snapBank, snapActive, snapProcess;
int oldVolume, asmCarry;
int decoder;
#pragma fastcall snapshot();
#pragma fastcall checkpoint();
#pragma fastcall assemblyPcm();
#pragma fastcall assemblySfx();

void check(int actual, int expected)
{
    checks++;
    if (actual != expected && error == 0) error=checks;
}
void ticks(int n) { while(n>0) { vsync(); n--; } }
void sfxTick(void) { if(decoder) assemblySfx(); else HuSFXprocess(); }
void sfxTicks(int n) { while(n>0) { vsync(); sfxTick(); n--; } }
void mark(int value) { stage=value; checkpoint(); }
void freeze(void)
{
    snapshot(); savedTick=snapTick; savedRow=snapRow;
    savedPcm=snapPcm; savedBank=snapBank;
}
void unchanged(void)
{
    snapshot(); check(snapTick,savedTick); check(snapRow,savedRow);
    check(snapPcm,savedPcm); check(snapBank,savedBank);
}
void checkNoteCuts(void)
{
    // EC01 cuts on the second row: stop PCM rather than activating bank 80.
    // Keep an unrelated SFX sample running so the timer continues scanning.
    check(HuTrackEngine_TryReserve(4),1);
    check(HuTrackEngine_PcmRequest(4,pcm,1,0x81),1);
    HuTrackEngine_PlaySong(2);vsync(6);
    snapshot();check(snapActive,0);
    vsync(4);snapshot();check(snapActive,128);mark(37);
    vsync(2);snapshot();check(snapActive,128);mark(38);
    HuTrackEngine_PlaySong(3);vsync(6);
    snapshot();check(snapActive,128);
    vsync(4);snapshot();check(snapActive,128);mark(37);
    vsync(2);snapshot();check(snapActive,128);mark(38);
    HuTrackEngine_chanRelease(4);HuTrackEngine_Stop();
}
void checkSfxRestart(void)
{
    for(decoder=0;decoder<2;decoder++) {
        for(count=0;count<4;count++) {
            HuSFXpanVol(5,pan_levels[count]);
            check(HuTrackEngine_TryReserve(5),1);
            check(HuSFXplay(5,getBank(pan_tone),getAddress(pan_tone)),1);
            sfxTick();mark(39);
            HuTrackEngine_chanRelease(5);
            check(HuTrackEngine_TryReserve(5),1);
            check(HuSFXplay(5,getBank(pan_tone),getAddress(pan_tone)),1);
            sfxTick();mark(39);
            HuTrackEngine_chanRelease(5);
        }
        for(count=0;count<2;count++) {
            check(HuTrackEngine_TryReserve(count),1);
            HuSFXplay(count,getBank(lfo_sfx),getAddress(lfo_sfx));
            sfxTick();mark(40);
            HuSFXstop(5);mark(40); // unrelated channel must preserve LFO
            HuSFXstop(count);mark(41);
            HuTrackEngine_chanRelease(count);
        }
    }
}
void checkCombinedPCM(void)
{
    for(decoder=0;decoder<2;decoder++) {
        HuSFX_ClearPCM();
        check(HuSFX_QueuePCM(pcm),0);
        check(HuSFX_QueuePCM(short_pcm),1);
        check(HuSFX_QueuePCM(edge_pcm),2);
        check(HuSFX_QueuePCM(empty_pcm),3);
        for(count=4;count<64;count++) check(HuSFX_QueuePCM(pcm),count);
        check(HuSFX_QueuePCM(pcm),-1);
        check(HuTrackEngine_TryReserve(5),1);
        HuSFXplay(5,getBank(empty_loop),getAddress(empty_loop)); sfxTick();
        check(HuSFXstate(5),HU_SFX_STOPPED); mark(32);
        HuTrackEnginePauseDDA();
        HuSFXplay(5,getBank(edge_sfx),getAddress(edge_sfx)); sfxTick();
        snapshot(); check(snapBank,63); check(snapPcm,0x4001); mark(36);
        HuTrackEngineResumeDDA(); sfxTicks(1);
        check(HuTrackEngine_PCMStatus(5),0); mark(32);
        HuSFXplay(5,getBank(combined),getAddress(combined)); sfxTick();
        check(HuTrackEngine_PCMStatus(5),1); mark(30);
        sfxTicks(2); check(HuTrackEngine_PCMStatus(5),0); mark(31);
        sfxTicks(2); check(HuSFXstate(5),HU_SFX_STOPPED);
        check(HuTrackEngine_SFXmode(5),1); mark(32);

        HuSFXplay(5,getBank(single),getAddress(single)); sfxTick();
        sfxTicks(1); check(HuTrackEngine_PCMStatus(5),0);
        check(HuSFXstate(5),HU_SFX_PLAYING); mark(32);
        HuSFXplay(5,getBank(looped),getAddress(looped)); sfxTick();
        sfxTicks(3); check(HuTrackEngine_PCMStatus(5),1); mark(30);
        HuSFX_ClearPCM(); sfxTicks(2); check(HuTrackEngine_PCMStatus(5),1);
        HuSFXstop(5); check(HuTrackEngine_PCMStatus(5),0); mark(32);
        check(HuSFX_QueuePCM(pcm),0); check(HuSFX_QueuePCM(short_pcm),1);

        HuSFXplay(5,getBank(implicit_stop),getAddress(implicit_stop)); sfxTick();
        sfxTicks(1); check(HuTrackEngine_PCMStatus(5),0); mark(31);
        sfxTicks(1); mark(31);
        HuSFXplay(5,getBank(mode_stop),getAddress(mode_stop)); sfxTick();
        sfxTicks(1); check(HuTrackEngine_PCMStatus(5),0); mark(31);
        HuSFXplay(5,getBank(eof_stop),getAddress(eof_stop)); sfxTick();
        sfxTicks(1); check(HuTrackEngine_PCMStatus(5),0);
        check(HuSFXstate(5),HU_SFX_STOPPED); mark(32);

        HuSFXplay(5,getBank(invalid_pcm),getAddress(invalid_pcm)); sfxTick();
        check(HuSFXstate(5),HU_SFX_STOPPED); mark(32);
        HuSFXplay(5,getBank(invalid_flags),getAddress(invalid_flags)); sfxTick();
        check(HuSFXstate(5),HU_SFX_STOPPED); mark(32);
        HuTrackEngine_chanRelease(5);
        HuSFXplay(5,getBank(combined),getAddress(combined)); sfxTick();
        check(HuSFXstate(5),HU_SFX_STOPPED);
        check(HuTrackEngine_SFXmode(5),0); mark(32);
        check(HuTrackEngine_TryReserve(5),1);

        HuTrackEnginePauseDDA();
        HuSFXplay(5,getBank(looped),getAddress(looped)); sfxTick();
        snapshot(); savedPcm=snapPcm;
        sfxTicks(2); snapshot(); check(snapPcm,savedPcm);
        HuTrackEngineResumeDDA(); sfxTicks(2); check(HuTrackEngine_PCMStatus(5),1);
        HuSFXplay(5,getBank(pcm_volume),getAddress(pcm_volume)); sfxTick(); mark(33);
        HuTrackEngine_SetSFXVolume(15); mark(34);
        HuSFXchanVol(5,15); sfxTick(); mark(35);
        HuSFXchanVol(5,31); HuTrackEngine_SetSFXVolume(31); sfxTick(); mark(33);
        HuTrackEngine_chanRelease(5); check(HuSFXstate(5),HU_SFX_STOPPED);
        mark(32);
    }
}
void checkWaveGain(void)
{
    HuTrackEngine_PlaySong(4);
    HuTrackEngine_SetMusicVolume(0);mark(42);vsync(16);mark(43);
    HuTrackEngine_SetMusicVolume(15);mark(44);vsync(16);mark(43);
    HuTrackEngine_Stop();
}
void checkDelayedRetrigger(void)
{
    HuTrackEngine_PlaySong(5);mark(45);vsync(30);mark(46);
    HuTrackEngine_Stop();
    HuTrackEngine_SetGlobal(0x35);vsync();mark(47);
    HuTrackEngine_SetGlobal(0xa0,0x60);vsync();mark(48);
    HuTrackEngine_SetGlobal(0xff);vsync();mark(49);
}
int main()
{
    error=0;done=0;checks=0;stage=0;
    HuTrack_Init();
    HuSFX_Init(getBank(sfx_waves),getAddress(sfx_waves));
    check(HuTrackEngine_Status(),HUTRACK_STOPPED);
    HuTrackEngine_Resume(); check(HuTrackEngine_Status(),HUTRACK_STOPPED);
    check(HuTrackEngineResumeDDA(),0);
    check(HuTrackEnginePauseDDA(),1); check(HuTrackEnginePauseDDA(),0);
    check(HuTrackEngineResumeDDA(),1); check(HuTrackEngineResumeDDA(),0);
    snapshot();check((snapProcess & 128)!=0,1);
    check(HuTrackEngine_PollEvent(),-1);
    check(HuTrackEngine_QueueSong(song),0);
    check(HuTrackEngine_QueueSong(music_pcm),1);
    check(HuTrackEngine_QueueSong(cut_pcm),2);
    check(HuTrackEngine_QueueSong(cut_wave),3);
    check(HuTrackEngine_QueueSong(wave_changes),4);
    check(HuTrackEngine_QueueSong(delayed_retrigger),5);
    for(count=6;count<64;count++) check(HuTrackEngine_QueueSong(song),count);
    check(HuTrackEngine_QueueSong(song),-1);
    HuTrackEngine_PlaySong(255); check(HuTrackEngine_Status(),HUTRACK_STOPPED);
    HuTrackEngine_PlaySong(0); check(HuTrackEngine_Status(),HUTRACK_PLAYING);
    vsync(6); check(HuTrackEngine_PollEvent(),0); check(HuTrackEngine_PollEvent(),-1);
    vsync(4); check(HuTrackEngine_PollEvent(),255); check(HuTrackEngine_PollEvent(),-1);
    mark(1);
    HuTrackEngine_Pause(); HuTrackEngine_Pause();
    check(HuTrackEngine_Status(),HUTRACK_PAUSED);
    freeze(); vsync(10); unchanged(); mark(2);
    HuTrackEngine_Resume(); HuTrackEngine_Resume();
    check(HuTrackEngine_Status(),HUTRACK_PLAYING); mark(3);
    HuTrackEngine_Stop(); HuTrackEngine_Resume();
    check(HuTrackEngine_Status(),HUTRACK_STOPPED); mark(4);

    HuTrackEngine_PlaySong(0); vsync(6);
    check(HuTrackEngine_TryReserve(5),1); check(HuTrackEngine_TryReserve(5),0);
    check(HuTrackEngine_TryReserve(6),0);check(HuTrackEngine_TryReserve(255),0);
    check(HuSFXplay(5,getBank(sfx),getAddress(sfx)),1); HuSFXprocess(); mark(5);
    HuTrackEngine_Pause(); HuTrackEngine_chanRelease(5); HuTrackEngine_Resume(); mark(6);
    // No new note occurs until the next loop: resume must not restart channel 5.
    vsync(5); mark(6);
    check(HuTrackEngine_TryReserve(5),1);
    check(HuSFXplay(5,getBank(sfx),getAddress(sfx)),1); HuSFXprocess();
    HuTrackEngine_PlaySong(0); mark(7);
    check(HuTrackEngine_SFXmode(5),1);check(HuSFXstate(5),HU_SFX_PLAYING);
    vsync(6);
    HuTrackEngine_SetGlobal(0x97);vsync();
    HuTrackEngine_SetMusicVolume(15);vsync();mark(8);
    check(HuTrackEngine_MusicVolume(),15);
    HuTrackEngine_FadeTo(0,1);
    for(count=14;count>=0;count--) { vsync();check(HuTrackEngine_MusicVolume(),count); }
    mark(9);check(HuTrackEngine_Status(),HUTRACK_PLAYING);
    HuTrackEngine_FadeIn(1); vsync(31);
    check(HuTrackEngine_MusicVolume(),31);mark(10);
    HuTrackEngine_FadeToPause(1);vsync(31);
    check(HuTrackEngine_Status(),HUTRACK_PAUSED);mark(11);
    HuTrackEngine_FadeIn(2);vsync(62);
    check(HuTrackEngine_Status(),HUTRACK_PLAYING);
    check(HuTrackEngine_MusicVolume(),31);mark(12);
    HuTrackEngine_FadeOut(0);check(HuTrackEngine_Status(),HUTRACK_STOPPED);mark(13);
    // SFX group mixing covers waiting control streams and already-running PCM.
    HuTrackEngine_SetSFXVolume(19);check(HuTrackEngine_SFXVolume(),19);mark(18);
    HuSFXchanVol(5,15);HuSFXprocess();mark(19);
    HuTrackEngine_SetSFXVolume(31);mark(20);
    HuSFXchanVol(5,31);HuSFXprocess();
    check(HuTrackEngine_TryReserve(4),1);check(HuTrackEngine_PcmRequest(4,pcm),1);
    HuTrackEngine_SetSFXVolume(9);mark(21);
    HuTrackEngine_PlaySong(0);ticks(6);mark(22);
    check(HuTrackEngine_SFXVolume(),9);
    HuTrackEngine_FadeTo(15,0);vsync();mark(23);
    HuTrackEngine_SetSFXVolume(0);mark(24);
    HuTrackEngine_SetSFXVolume(255);check(HuTrackEngine_SFXVolume(),31);mark(25);
    HuTrackEngine_chanRelease(4);
    HuTrackEngine_chanRelease(5);
    HuTrackEngine_PlaySong(0);vsync(6);
    HuTrackEngine_SetMusicVolume(255);check(HuTrackEngine_MusicVolume(),31);
    HuTrackEngine_FadeTo(5,2);vsync(7);oldVolume=HuTrackEngine_MusicVolume();
    HuTrackEngine_Pause();vsync(10);check(HuTrackEngine_MusicVolume(),oldVolume);
    HuTrackEngine_Resume();HuTrackEngine_SetMusicVolume(23);vsync(8);
    check(HuTrackEngine_MusicVolume(),23); // cancels the prior fade
    HuTrackEngine_FadeTo(23,255);check(HuTrackEngine_MusicVolume(),23);

    // Paused music PCM retains the exact stream position and bank.
    HuTrackEngine_PlaySong(1);vsync(6);snapshot();check(snapActive,0);
    HuTrackEngine_Pause();freeze();vsync(10);unchanged();mark(14);
    check(HuTrackEnginePauseDDA(),1);check(HuTrackEngineResumeDDA(),1);
    snapshot();check((snapProcess & 128)!=0,1);
    HuTrackEngine_Pause();HuTrackEngine_Resume();snapshot();check(snapActive,0);
    vsync(2);snapshot();check(snapPcm==savedPcm,0);mark(15);

    // Global DDA pause survives another request and a music change.
    check(HuTrackEnginePauseDDA(),1);check(HuTrackEnginePauseDDA(),0);
    check(HuTrackEngine_TryReserve(5),1);check(HuTrackEngine_PcmRequest(5,pcm),1);
    HuTrackEngine_PlaySong(0);freeze();vsync(8);snapshot();check(snapPcm,savedPcm);
    check(HuTrackEngine_SFXmode(5),1);mark(16);
    check(HuTrackEngineResumeDDA(),1);vsync(2);snapshot();check(snapPcm==savedPcm,0);
    check(HuTrackEngineResumeDDA(),0);HuTrackEngine_chanRelease(5);

    HuTrackEngine_PlayOnce(0);frame=0;
    while(HuTrackEngine_Status()==HUTRACK_PLAYING && frame<300) { vsync();frame++; }
    check(HuTrackEngine_Status(),HUTRACK_ENDED);check(frame>=260 && frame<=261,1);mark(17);
    HuTrackEngine_Resume();check(HuTrackEngine_Status(),HUTRACK_ENDED);
    HuTrackEngine_Stop();check(HuTrackEngine_Status(),HUTRACK_STOPPED);
    // The assembly PCM entry must clear noise left by a previous effect.
    check(HuTrackEngine_TryReserve(5),1);
    assemblyPcm(); check(asmCarry,0); mark(26);
    HuTrackEngine_chanRelease(5);
    checkCombinedPCM();
    // The direct API also skips a header split across physical ROM banks.
    check(HuTrackEngine_TryReserve(5),1);
    check(HuTrackEnginePauseDDA(),1);
    check(HuTrackEngine_PcmRequest(5,edge_pcm),1);
    snapshot();check(snapBank,63);check(snapPcm,0x4001);mark(36);
    check(HuTrackEngineResumeDDA(),1);vsync();
    check(HuTrackEngine_PCMStatus(5),0);
    HuTrackEngine_chanRelease(5);mark(32);

    // Reject bad direct requests before replacing an existing paused stream.
    check(HuTrackEngine_TryReserve(5),1);
    check(HuTrackEnginePauseDDA(),1);
    check(HuTrackEngine_PcmRequest(5,pcm),1);
    freeze();
    for(count=0x5ffd;count<=0x5fff;count++) {
        check(HuTrackEngine_PcmRequest(5,255,count),0);
        snapshot();check(snapPcm,savedPcm);check(snapBank,savedBank);
        check(HuTrackEngine_PCMStatus(5),1);
    }
    check(HuTrackEngine_PcmRequest(5,empty_pcm,1,0x81),0);
    snapshot();check(snapPcm,savedPcm);check(snapBank,savedBank);
    check(HuTrackEngine_PcmRequest(5,empty_repeat_pcm),0);
    snapshot();check(snapPcm,savedPcm);check(snapBank,savedBank);
    // Empty one-shots are safe; a forced stop must override a repeat marker.
    check(HuTrackEngine_PcmRequest(5,empty_repeat_pcm,0,0x80),1);
    check(HuTrackEngineResumeDDA(),1);vsync();
    check(HuTrackEngine_PCMStatus(5),0);
    check(HuTrackEngine_PcmRequest(5,empty_pcm),1);vsync();
    check(HuTrackEngine_PCMStatus(5),0);
    HuTrackEngine_chanRelease(5);mark(32);
    checkNoteCuts();
    checkSfxRestart();
    checkWaveGain();
    checkDelayedRetrigger();
    done=1;
    for(;;) vsync();
}
#asm
.proc _checkpoint
 .ifdef HUCC
    jmp leave_proc
 .else
    rts
 .endif
.endp
.proc _snapshot
    php
    sei
    lda HuTrack.tick
    sta _snapTick
    stz _snapTick+1
    lda HuTrack.channel.rowPos
    sta _snapRow
    stz _snapRow+1
    lda HuTrack.dda.addr.lo+5
    sta _snapPcm
    lda HuTrack.dda.addr.hi+5
    sta _snapPcm+1
    lda HuTrack.dda.bank+5
    sta _snapBank
    stz _snapBank+1
    lda HuTrack.dda.inactive+5
    sta _snapActive
    stz _snapActive+1
    lda HuTrack.DDAprocess
    sta _snapProcess
    stz _snapProcess+1
    plp
 .ifdef HUCC
    jmp leave_proc
 .else
    rts
 .endif
.endp

#endasm

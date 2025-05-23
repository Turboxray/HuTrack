#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"
#include "HuSFX/Huc_interface/HucSFX.h"
#include "HuSFX/Huc_interface/HucSFX.c"
#include "HuCsupport/HuCsupport.h"

#asm
.bank HUC_USER_RESERVED
#endasm

#incasmlabel(SMB3Overworld, "../assets/song/smb3_overworld/smb3_overworld.song.inc", 2);
#incasmlabel(FF3_smeared_graffiti, "../assets/song/FF3_smeared_graffiti/FF3_smeared_graffiti.song.inc", 2);
#incasmlabel(Initial_Velocity, "../assets/song/Night_Slave_-_Initial_Velocity/Night_Slave_-_Initial_Velocity.song.inc", 2);
#incasmlabel(Bottom_Sweep, "../assets/song/Night_Slave_-_Bottom_Sweep_V2/Night_Slave_-_Bottom_Sweep_V2.song.inc", 2);
#incasmlabel(Stormy_Edge_Stage, "../assets/song/Night_Slave_-_Stormy_Edge_Stage_3A/Night_Slave_-_Stormy_Edge_Stage_3A.song.inc", 2);

#incasmlabel(pcm1, "../assets/sfx/sample2/hypercocoon.inc", 2);
#incasmlabel(pcm2, "../assets/sfx/sample3/stageclear.inc", 2);
#incasmlabel(pcm3, "../assets/sfx/sample4/ShubibinmanIII.inc", 2);
#incasmlabel(pcm4, "../assets/sfx/sample5/loop7.inc", 2);
#incasmlabel(pcm5, "../assets/sfx/sample13/MissionFailed_b.inc", 2);

// HuSFX
#incasmlabel(SFX_1, "../assets/sfx/smb3/smb3_sfx.chan5.inc", 2);
#incasmlabel(SFX_2, "../assets/sfx/swiss/swiss.chan0.inc", 2);
#incasmlabel(SFX_3, "../assets/sfx/test1/test1.chan2.inc", 2);
#incasmlabel(SFX_4, "../assets/sfx/l1/light_1.chan0.inc", 2);

// HuSFX waveforms
#incasmlabel(sfx_waveforms, "../assets/sfx/main.wf.inc", 2);

char title[48];
char author[48];
char chanMask[7];

typedef struct {
    char idx;
    char bank[20];
    int  addr[20];
    char mask0[20];
    char mask1[20];
    enum PCMForceOn {
        PCM_NO_FORCE       = 0x00,
        PCM_FORCE_REPEAT   = 0x01,
        PCM_ALLOW_REPEAT   = 0x81,
        PCM_DISABLE_REPEAT = 0x80,
    };
} PcmPointers;
PcmPointers pcmPointers;

typedef struct {
    char len;
    char sfxBank[20];
    int  sfxBase[20];
} SFXcollection;
SFXcollection sFXcollection;

typedef struct {
    int  ptr;
    char status;
    enum SFXstream {
        SFX_OFF       = 0x00,
        SFX_ON        = 0x01,
        SFX_REPEAT    = 0x03,
        SFX_STOP_RQST = 0x08,
        SFX_RQST      = 0x10
    };
} SFXassign;
SFXassign sFXassign[6];


//###############################################################################
//###############################################################################
// Main                                                                         #
//###############################################################################

int main()
{

    // var setup and init start 
    int song_number, j1, j2, last_song, cur_channel, song_playing, sfxSelect, sfxMode;
    int i,j,k;
    HU_SFX_STREAMNIG_t sfx_streaming;

    last_song    = 4;    // variable to control number of songs available. base 0, should align with number of songs queued in song queue section
    song_number  = 0;    // currently selected song
    cur_channel  = 0;    // toggle variable for which channel of sfx is being used
    song_playing = 1;
    sfxSelect    = 0;
    sfxMode      = 0;

    getDataPtr(SMB3Overworld);

    for(i=0;i<6;i++) { chanMask[i] = '-'; }
    chanMask[6] = 0;    // Set the string null terminator
    
    set_xres(344);
    cls();
    load_default_font();
    disp_on();

    HuSFX_Init( getBank(sfx_waveforms), getAddress(sfx_waveforms) );

    HuTrack_Init();
    HuTrackEngine_QueueSong(SMB3Overworld);
    HuTrackEngine_QueueSong(FF3_smeared_graffiti);
    HuTrackEngine_QueueSong(Initial_Velocity);
    HuTrackEngine_QueueSong(Bottom_Sweep);
    HuTrackEngine_QueueSong(Stormy_Edge_Stage);

    loadPcmPointers();

    initSFXcollections();



    vsync(1);
    vsync(1);

    HuTrackEngine_getCurrSongTitle(title);
    HuTrackEngine_getCurrSongAuthor(author);
    put_string(title,  1,  5);
    put_string(author,  1,  3);

    put_string("Audio Test Suite", 8, 12);

    put_string("Song:",4,15);
    put_string("Song",11,15);
    put_number(song_number,2,16,15);

    put_string("SFX: ------",4,17);
    put_string("^",9,18);


    put_string("(Toggle) SELECT:  SFX / Song mode.", 0, 21);
    put_string("(Song)   UP/DOWN: Choose song.", 0, 22);
    put_string("(Song)   I/II:    Start / Stop song.", 0, 23);
    put_string("(SFX)    START:   En/Dis chan for SFX.", 0, 24);
    put_string("(SFX)    UP/DOWN: Choose SFX.", 0, 25);
    put_string("(SFX)    I/II:    Play/Stop SFX.", 0, 26);

    put_string("    Set SFX ", 0, 19);
    put_number(sfxSelect,2,12,19);
    put_string("                   ", 14, 19); 
    
    for(;;)
    {
        vsync();
        updateChipSFX();
        j1 = joy(0);
        j2 = joytrg(0);

        put_string("      ",9,18);
        cur_channel += (cur_channel < 5 && (j2 & JOY_RIGHT)) ? 1: 0;
        cur_channel -= (cur_channel > 0 && (j2 & JOY_LEFT)) ? 1: 0;
        put_string("^",9+cur_channel,18);

        if (j2 & JOY_SLCT) {
            sfxMode ^= 0x01;
        }

        // Song interface mode
        if ( !sfxMode ) {
            if (j2 & JOY_I) {
                HuTrackEngine_Stop();
                vsync(10);
                HuTrackEngine_PlaySong(song_number);
                HuTrackEngine_getCurrSongTitle(title);
                HuTrackEngine_getCurrSongAuthor(author);
                put_string("                                                     \0",  1,  5);
                put_string("                                                     \0",  1,  3);
                put_string(title,  1,  5);
                put_string(author,  1,  3);
                chanMask[0] = '-';
                chanMask[1] = '-';
                chanMask[2] = '-';
                chanMask[3] = '-';
                chanMask[4] = '-';
                chanMask[5] = '-';
            }
            else if (j2 & JOY_II)   { HuTrackEngine_Stop(); }
            else if (j2 & JOY_UP)   { song_number += (song_number < last_song) ? 1: 0; }
            else if (j2 & JOY_DOWN) { song_number -= (song_number > 0) ? 1: 0; }
        }
        // SFX interface mode
        else {
            if (j2 & JOY_STRT) {
                chanMask[cur_channel] = (chanMask[cur_channel] == '-') ? 'X':'-';

                if (chanMask[cur_channel]=='X') { HuTrackEngine_chanReserve(cur_channel); }
                else { HuTrackEngine_chanRelease(cur_channel); }
            }

            if ((j2 & JOY_DOWN) || (j2 & JOY_UP)) {
                sfxSelect += ((sfxSelect < (sFXcollection.len-1)) && (j2 & JOY_UP)) ? 1: 0;
                sfxSelect -= ((sfxSelect > 0) && (j2 & JOY_DOWN)) ? 1: 0;
                put_string("    Set SFX ", 0, 19);
                put_number(sfxSelect,2,12,19);
                put_string("                   ", 14, 19); 
            }

            if (j2 & JOY_I) { playSFX(cur_channel, sfxSelect); }
            else if (j2 & JOY_II) { stopSFX(cur_channel); }        
        }

        put_string(chanMask, 9,17);
        put_number(song_number,2,16,15);
        put_string("Mode: ", 0, 20);
        put_string(((!sfxMode) ? "Song" : "SFX " ), 7, 20);
    }

  return 0;
}

//###############################################################################
//###############################################################################
// Subs                                                                         #
//###############################################################################



//...............................................................................
//...............................................................................
//

void loadPcmPointers() {

    pcmPointers.idx = 0;
    getFarPointer(pcm1, &(pcmPointers.bank[pcmPointers.idx]), &(pcmPointers.addr[pcmPointers.idx]) );

    getFarPointer(pcm1, &(pcmPointers.bank[pcmPointers.idx]), &(pcmPointers.addr[pcmPointers.idx]) );

    pcmPointers.mask0[pcmPointers.idx  ] = PCM_NO_FORCE;
    pcmPointers.mask1[pcmPointers.idx++] = PCM_DISABLE_REPEAT;
    
    getFarPointer(pcm2, &(pcmPointers.bank[pcmPointers.idx]), &(pcmPointers.addr[pcmPointers.idx]) );
    pcmPointers.mask0[pcmPointers.idx  ] = PCM_FORCE_REPEAT;
    pcmPointers.mask1[pcmPointers.idx++] = PCM_DISABLE_REPEAT;

    getFarPointer(pcm3, &(pcmPointers.bank[pcmPointers.idx]), &(pcmPointers.addr[pcmPointers.idx]) );
    pcmPointers.mask0[pcmPointers.idx  ] = PCM_NO_FORCE;
    pcmPointers.mask1[pcmPointers.idx++] = PCM_DISABLE_REPEAT;

    getFarPointer(pcm4, &(pcmPointers.bank[pcmPointers.idx]), &(pcmPointers.addr[pcmPointers.idx]) );
    pcmPointers.mask0[pcmPointers.idx  ] = PCM_NO_FORCE;
    pcmPointers.mask1[pcmPointers.idx++] = PCM_ALLOW_REPEAT;

    getFarPointer(pcm5, &(pcmPointers.bank[pcmPointers.idx]), &(pcmPointers.addr[pcmPointers.idx]) );
    pcmPointers.mask0[pcmPointers.idx  ] = PCM_NO_FORCE;
    pcmPointers.mask1[pcmPointers.idx++] = PCM_ALLOW_REPEAT;

}

//...............................................................................
//...............................................................................
//

void initSFXcollections()
{
    char sfx_num;
    char x;

    sFXcollection.sfxBank[sfx_num] = getBank(SFX_1);
    sFXcollection.sfxBase[sfx_num] = getAddress(SFX_1);
    sfx_num++;

    sFXcollection.sfxBank[sfx_num] = getBank(SFX_2);
    sFXcollection.sfxBase[sfx_num] = getAddress(SFX_2);
    sfx_num++;

    sFXcollection.sfxBank[sfx_num] = getBank(SFX_3);
    sFXcollection.sfxBase[sfx_num] = getAddress(SFX_3);
    sfx_num++;

    sFXcollection.sfxBank[sfx_num] = getBank(SFX_4);
    sFXcollection.sfxBase[sfx_num] = getAddress(SFX_4);
    sfx_num++;

    sFXcollection.len = sfx_num;

    for (x=0; x<6; x++) {
        sFXassign[x].status = SFX_OFF;
        sFXassign[x].ptr = 0;
    }

}

//...............................................................................
//...............................................................................
//

int playSFX(int selectedChan, int sfxSelect)
{

    if ( HuTrackEngine_SFXmode(selectedChan) )
    {
        sFXassign[selectedChan].status = SFX_ON;
        sFXassign[selectedChan].ptr = sfxSelect;
        HuSFXplay(  selectedChan,
                    sFXcollection.sfxBank[sfxSelect],
                    sFXcollection.sfxBase[sfxSelect]
                    );
        put_string("    Set SFX ", 0, 19);
        put_number(sfxSelect,2,12,19);
        put_string("                   ", 14, 19); 
    } else {
        put_string("chan ", 0, 19);
        put_number(selectedChan,2,5,19);
        put_string(" is not in SFX mode.", 8, 19);
    }

}

//...............................................................................
//...............................................................................
//

int stopSFX(int selectedChan )
{
    if ( HuTrackEngine_SFXmode(selectedChan) ) {
        sFXassign[selectedChan].status = SFX_STOP_RQST;
        put_string("        SFX  Stopped           ", 0, 19);
    } else {
        put_string("chan ", 0, 19);
        put_number(selectedChan,2,5,19);
        put_string(" is not in SFX mode.", 8, 19);
    }
}



//...............................................................................
//...............................................................................
//
int updateChipSFX()
{
    char chan;

    for (chan=0; chan<6; chan++) {
        if ( sFXassign[chan].status == SFX_STOP_RQST && HuTrackEngine_SFXmode(chan)) { 
            HuSFXstop(chan);
            HuTrackEngineSFXrest(chan);
            continue;
        }
    }

    HuSFXprocess();

    return 1;
}

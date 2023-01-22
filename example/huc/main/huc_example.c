
#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"

#asm
  .bank HUC_USER_RESERVED
#endasm


#incasmlabel(SMB3Overworld, "../assets/song/smb3_overworld/smb3_overworld.song.inc", 2);
#incasmlabel(FF3_smeared_graffiti, "../assets/song/FF3_smeared_graffiti/FF3_smeared_graffiti.song.inc", 2);
#incasmlabel(Initial_Velocity, "../assets/song/Night_Slave_-_Initial_Velocity/Night_Slave_-_Initial_Velocity.song.inc", 2);
#incasmlabel(Bottom_Sweep, "../assets/song/Night_Slave_-_Bottom_Sweep_V2/Night_Slave_-_Bottom_Sweep_V2.song.inc", 2);
#incasmlabel(Stormy_Edge_Stage, "../assets/song/Night_Slave_-_Stormy_Edge_Stage_3A/Night_Slave_-_Stormy_Edge_Stage_3A.song.inc", 2);

char title[48];
char author[48];
char chanMask[7];

int main()
{

    // var setup and init start 
    int song_number, j1, j2, last_song, cur_channel;
    int i,j,k;
    last_song   = 4;    // variable to control number of songs available. base 0, should align with number of songs queued in song queue section
    song_number = 0;    // currently selected song
    cur_channel = 0;    // toggle variable for which channel of sfx is being used

    for(i=0;i<6;i++) { chanMask[i] = '-'; }
    chanMask[6] = 0;    // Set the string null terminator
    

    set_xres(344);
    cls();
    load_default_font();
    disp_on();

    HuTrack_Init();
    HuTrackEngine_QueueSong(SMB3Overworld);
    HuTrackEngine_QueueSong(FF3_smeared_graffiti);
    HuTrackEngine_QueueSong(Initial_Velocity);
    HuTrackEngine_QueueSong(Bottom_Sweep);
    HuTrackEngine_QueueSong(Stormy_Edge_Stage);

    vsync(1);
    HuTrackEngine_PlaySong(0);
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


    put_string("Up/Down : Choose songs.", 0, 23);
    put_string("Start: Enable/Disable channel for SFX.", 0, 24);
    put_string("Btn I: Start song.", 0, 25);
    put_string("Btn II: Stop song.", 0, 26);

    for(;;)
    {
        vsync();
        j1 = joy(0);
        j2 = joytrg(0);

        put_string("      ",9,18);
        cur_channel += (cur_channel < 5 && (j2 & JOY_RIGHT)) ? 1: 0;
        cur_channel -= (cur_channel > 0 && (j2 & JOY_LEFT)) ? 1: 0;
        put_string("^",9+cur_channel,18);

        song_number += (song_number < last_song && (j2 & JOY_UP)) ? 1: 0;
        song_number -= (song_number > 0 && (j2 & JOY_DOWN)) ? 1: 0;
        put_number(song_number,2,16,15);

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
        if (j2 & JOY_II) {
                HuTrackEngine_Stop();
        }

        if (j2 & JOY_STRT) {
            chanMask[cur_channel] = (chanMask[cur_channel] == '-') ? 'X':'-';
            if (chanMask[cur_channel]=='X') {
                HuTrackEngine_chanSetSFX(cur_channel);
            } else {
                HuTrackEngine_chanReleaseSFX(cur_channel);
            }
        }

        put_string(chanMask, 9,17);

    }

  return 0;
}


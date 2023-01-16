
#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"


// audio asm init start
enum Songs {
    SMB3_OVERWORLD,
    SMEARED_GRAFFITI,
    INITIAL_VECOCITY,
    BOTTOM_SWEEP,
    STORMY_EDGE_STAGE,
};

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
// char blankString[] = "                                           \0";

int main()
{

	// var setup and init start 
	int song_number, sfx1_number, sfx2_number, j1, j2, btn_release, button_down, max_songs, max_sfxs, mode, cursorx, cursory, cur_channel;
	max_songs=4; 		// variable to control number of songs available. base 0, should align with number of songs queued in song queue section
	max_sfxs=2;			// variable to control number of sfx available. base 0, should align with number of sfx queued in sfx queue section
	song_number=0;		// currently selected song
	sfx1_number=0;		// currently selected sfx for channel 1
	sfx2_number=0;		// currentlu selected sfx for channel 2
	btn_release=1;		// variable for tracking if button is pressed or not
	mode=0;				// toggle variable for if in sfx or song playtest mode. 0 = song. 1 = sfx
	cursorx = 70;		// x position of cursor
	cursory = 116;		// y position of cursor
	cur_channel=0;		// toggle variable for which channel of sfx is being used


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

	put_string("Up/Down : Choose songs.", 0, 23);
	put_string("Btn I: Start song.", 0, 25);
	put_string("Btn II: Stop song.", 0, 26);
	// text display stop

	for(;;)
	{
		vsync();
		j1 = joy(0);
		j2 = joytrg(0);

        song_number += (song_number < max_songs && (j2 & JOY_UP)) ? 1: 0;
        song_number -= (song_number > 0 && (j2 & JOY_DOWN)) ? 1: 0;
	    put_number(song_number,2,16,15);

    	if (j2 & JOY_I)
		{
            HuTrackEngine_Stop();
            vsync(10);
            HuTrackEngine_PlaySong(song_number);
            HuTrackEngine_getCurrSongTitle(title);
            HuTrackEngine_getCurrSongAuthor(author);
            put_string("                                                     \0",  1,  5);
            put_string("                                                     \0",  1,  3);
            put_string(title,  1,  5);
            put_string(author,  1,  3);
		}
		if (j2 & JOY_II)
		{
				HuTrackEngine_Stop();
		}

	}

  return 0;
}


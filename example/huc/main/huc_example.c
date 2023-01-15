
#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"



#asm
  .bank HUC_USER_RESERVED
#endasm


#incasmlabel(SMB3Overworld, "../assets/song/smb3_overworld/smb3_overworld.song.inc", 2);

char title[48];
char author[48];

int main()
{
    set_xres(344);
    cls();
    load_default_font();
    disp_on();

    HuTrack_Init();
    HuTrackEngine_QueueSong(SMB3Overworld);

    vsync(1);
    HuTrackEngine_PlaySong(0);
    vsync(1);

    HuTrackEngine_getCurrSongTitle(title);
    HuTrackEngine_getCurrSongAuthor(author);

    put_string(title,  2,  5);
    put_string(author,  2,  3);

    for(;;)

  return 0;
}


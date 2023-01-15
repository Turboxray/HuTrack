
#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"



#asm
  .bank HUC_USER_RESERVED
#endasm


#incasmlabel(SMB3Overworld, "../assets/song/smb3_overworld/smb3_overworld.song.inc", 2);



int main()
{

    HuTrack_Init();
    HuTrackEngine_QueueSong(SMB3Overworld);

    vsync(1);
    HuTrackEngine_PlaySong(0);

    for(;;)

  return 0;
}


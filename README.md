# HuTrack

HuTrack is a library and convertor for playing Deflemask files in HuC and PCEAS projects. The engine is lightweight and compact, and is intended to be inserted into game projects. The use of HuTrack requires legacy deflemask (https://www.deflemask.com/get_legacy/). HuTrack also requires that you install python and additional packages. 

# Usage 
To create a song, you need to first convert the deflemask file into files that can be included in your project. First, extract the HuTrack Project to your project directory. 
Run the convertor like this: 
python HuTrack/utils/HuTrackConverter.py

Open the song you wish to convert: 
![image](https://github.com/Turboxray/HuTrack/assets/14317892/6c1f9876-543e-40a1-ad8d-03366d3e752a)

Export the song to HuTrack files: 
Save.Image. 

For HuC- Include the library like this: 
#include "/HuTrack/lib/HuTrack/Huc_interface/HuTrack.c"
You can include songs as shown below: 
#incasmlabel(singcatsing, "SingCatSingDMF/SingCatSingDMF.song.inc", 2);

In your main function, you'll need to intialize HuTrack, and then also queue any song you intend to play: 
  HuTrack_Init();      
	HuTrackEngine_QueueSong(singcatsing);

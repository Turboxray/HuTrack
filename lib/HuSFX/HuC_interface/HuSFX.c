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


// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;// Interface                                                                                               /
// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;interface

// int __fastcall HuTrackEngine_SFXmode(unsigned char channel<__al>);
// int __fastcall HuTrackEngine_SFXmode();
// int __fastcall HuTrackEngineSFXrest(unsigned char channel<__al>);
int __fastcall HuSFXprocess();
int __fastcall HuSFXplay( char channel<__al>, unsigned char bank1<__fbank>, unsigned int addr1<__fptr>, unsigned char bank2<__cl>, unsigned int addr2<__bx>);

#ifdef __HUCC__
#asm
		.data
		include "HuSFX/HuSFX_vars.inc"
		.code
		include "HuSFX/HuSFX_lib.asm"
#endasm
#endif

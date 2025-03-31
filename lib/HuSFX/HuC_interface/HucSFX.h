// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;
// ; HucSFX header for PC-Engine
// ;
// ;
// ; file: HucSFX.h
// ;
// ; Ver: 1.0.0
// ;
// ; History:
// ; -------
// ;
// ;
// ;


int HuSFX_Init( void );
int HuSFXplay( char channel, unsigned char bank1, unsigned int addr1, unsigned char bank2, unsigned int addr2 );
int HuSFXstop( char channel );
int HuSFXprocess();
int HuSFXstatus( char channel );

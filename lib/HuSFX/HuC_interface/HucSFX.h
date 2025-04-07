#ifndef _HU_SFX_
#define _HU_SFX_
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

typedef enum
{
    HU_SFX_ERROR   = 0,
    HU_SFX_PLAYING = 1,
    HU_SFX_STOPPED = 2,
} HU_SFX_STREAMNIG_t;

typedef enum
{
    HU_SFX_ERROR   = 0,
    HU_SFX_OK      = 1,
} HU_SFX_STATUS_t;


void HuSFX_Init( char bank, unsigned int address );
void HuSFXprocess( void );
HU_SFX_STATUS_t HuSFXplay( char channel, unsigned char bank1, unsigned int addr1 );
HU_SFX_STATUS_t HuSFXstop( char channel );
HU_SFX_STATUS_t HuSFXchanVol( char channel, unsigned char vol );
HU_SFX_STATUS_t HuSFXpanVol( char channel, unsigned char pan );
HU_SFX_STREAMNIG_t HuSFXstate( char channel );

#endif // _HU_SFX_

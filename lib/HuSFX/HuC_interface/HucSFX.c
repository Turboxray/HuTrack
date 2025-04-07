// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;
// ; HuSFX for PC-Engine
// ;
// ; Ver: 1.0.0
// ;
// ; History:
// ; -------
// ;
// ;
// ;

#include "HuSFX/HuC_interface/HucSFX.h"
#include "HuSFX/HuC_interface/HucSFX.inc"

//......................................................
void HuSFX_Init( char bank, unsigned int address )
{
    HuSFX_Init_intf( bank, address );
}

//......................................................
void HuSFXprocess( void )
{
    HuSFXprocess_intf();
}

//......................................................
HU_SFX_STATUS_t HuSFXplay( char channel, unsigned char bank1, unsigned int addr1 )
{
    return HuSFXplay_intf( channel, bank1, addr1 );
}

//......................................................
HU_SFX_STATUS_t HuSFXchanVol( char channel, unsigned char vol )
{
    return HuSFXchanVol_intf( channel, vol );
}

//......................................................
HU_SFX_STATUS_t HuSFXpanVol( char channel, unsigned char pan )
{
    return HuSFXchanPan_intf( channel, pan );
}

//......................................................
HU_SFX_STATUS_t HuSFXstop( char channel )
{
    return HuSFXstop_intf( channel );
}

//......................................................
HU_SFX_STREAMNIG_t HuSFXstate( char channel )
{
    return HuSFXstate_intf( channel );
}

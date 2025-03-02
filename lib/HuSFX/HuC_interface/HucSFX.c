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

#include "HuSFX/HuC_interface/HucSFX.inc"

//......................................................
int HuSFX_Init(void)
{ 
   return HuSFX_Init_intf();
}

//......................................................
int HuSFXplay( char channel, unsigned char bank1, unsigned int addr1, unsigned char bank2, unsigned int addr2 )
{
    return HuSFXplay_intf( channel, bank1, addr1, bank2, addr2);
}

//......................................................
int HuSFXstop( char channel )
{
    return HuSFXstop_intf( channel );
}


//......................................................
int HuSFXprocess()
{
    return HuSFXprocess_intf();
}

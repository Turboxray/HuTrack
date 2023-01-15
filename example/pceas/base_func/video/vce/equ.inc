
; VCE resolution
LO_RES   			= %00000000		;5.369mhz
LOW_RES  			= %00000000		;5.369mhz
MID_RES  			= %00000001		;7.159mhz
HI_RES   			= %00000010		;10.739mhz
H_FILTER_ON 	= %00000100		;263 scanline
H_FILTER_OFF	= %00000000		;262 scanline
BW_MODE				= %10000000		;no color burst signal
COLOR_MODE		= %00000000		;color burst signal


;VCE ports
vce_cntrl  = $400
vce_clr	   = $402
vce_clr.l  = $402
vce_clr.h  = $403
vce_data   = $404
vce_data.l = $404
vce_data.h = $405
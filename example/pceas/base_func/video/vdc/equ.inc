; VDC REG equates

MAWR   .equ    $00        ;Memory Access Write Reg
MARR   .equ    $01        ;Memory Access Read Reg
VRWR   .equ    $02        ;Vram Read/Write reg
VWR    .equ    $02        ;Vram Read/Write reg
VRR    .equ    $02        ;Vram Read/Write reg
CR     .equ    $05        ;Control Reg
RCR    .equ    $06        ;Raster Control Reg
BXR    .equ    $07        ;Background X(scroll) Reg
BYR    .equ    $08        ;Background Y(scroll) Reg
MWR    .equ    $09        ;Memory Access Width Reg
HSR    .equ    $0a        ;Horizontal Synchro Reg
HDR    .equ    $0b        ;Horizontal Display Reg
VSR    .equ    $0c        ;Vertical Synchro Reg
VDR    .equ    $0d        ;Vertical Display Reg
VDE    .equ    $0e        ;Vertical Display End Reg
DCR    .equ    $0f        ;DMA Control Reg
DSR    .equ    $10        ;DMA Source Address Reg
DDR    .equ    $11        ;DMA Destination Address Reg
DBR    .equ    $12        ;DMA Block Length Reg
SATB   .equ    $13        ;VRAM-SATB Source Address Reg


;VDC ports
vreg_port    = $0000
vdata_port   = $0002
vdata_port.l = $0002
vdata_port.h = $0003

;VDC CR reg arguments
BG_ON    = $0080
BG_OFF   = $0000
SPR_ON   = $0040
SPR_OFF  = $0000
VINT_ON  = $0008
VINT_OFF = $0000
HINT_ON  = $0004
HINT_OFF = $0000
ALL_OFF  = $0000

;VDC vram increment
INC_1   = %00000000
INC_32  = %00001000
INC_64  = %00010000
INC_128 = %00011000

;VDC map sizes
SCR32_32  = %00000000
SCR32_64  = %01000000
SCR64_32  = %00010000
SCR64_64  = %01010000
SCR128_32 = %00100000
SCR128_64 = %01100000

;VDC DMA control
AUTO_SATB_ON  = $0010
AUTO_SATB_OFF = $0000

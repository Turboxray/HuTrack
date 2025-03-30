; ***************************************************************************
; ***************************************************************************
;
; hucc-sound.inc
;
; Included by hucc.asm to customize the sound driver.
;
; Copyright John Brandwood 2025.
;
; Distributed under the Boost Software License, Version 1.0.
; (See accompanying file LICENSE_1_0.txt or copy at
;  http://www.boost.org/LICENSE_1_0.txt)
;
; ***************************************************************************
; ***************************************************************************
;
; A customized sound driver for HuCard or CDROM usage can create a
; version of this file, and then have startup.asm use the new
; definitions just by including the new sound driver's path
; in the PCE_INCLUDE environment variable BEFORE the standard
; "include/hucc" path.
;
; ***************************************************************************
; ***************************************************************************



; ***************************************************************************
; ***************************************************************************
;
; Tell hucc.asm to reserve a bank for the sound driver.

NEED_SOUND_BANK	= 1



; ***************************************************************************
; ***************************************************************************
;
; Choose how much zero-page memory to allocate for the HuCC stack.
;
; This should normally be 128 bytes, but if compiling with "-fno-recursive"
; you can usually get it down to 16 or 32 bytes.
;
; Some sound drivers, such as HuTrack, use a lot of ZP memory, and so you
; will need to set a stack size of 96 or less bytes if using one of those.
;

	.ifndef HUCC_STACK_SZ
HUCC_STACK_SZ	=	96	; (16 .. 85)
	.endif



; ***************************************************************************
; ***************************************************************************
;
; This macro is invoked in hucc.asm just after the RAM is cleared, and before
; interrupts are enabled.

HUTRACK_BENCHMARK = 1

__sound_init	.macro
;		stz	<HuTrack.Status
;		; Stop parsing songs
;		smb6	<HuTrack.Status
;		; Stop parsing sfx
;		smb5	<HuTrack.Status
		.endm

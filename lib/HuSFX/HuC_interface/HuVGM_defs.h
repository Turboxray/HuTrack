#ifndef _HU_VGM_DEFS_
#define _HU_VGM_DEFS_

/* HuSFX byte-stream commands; see utils/PSG_SFX/decode.txt.
 * Arguments must fit their fields: volume 0..31, pan/period high 0..15,
 * other operands 0..255. HuC does not support '&' in ROM initializers.
 */
#define HuChanOff 0x00

/* Preserve the old $D0 PSG control value (DDA, level 16), encoded compactly. */
#define HuChanDDA 0x30

#define HuWFvol(x) (0x80 | (x))

#define HuDDAvol(x) (0x20 | (x))

#define HuPan(x,y) 0xA5, (((x) << 4) | (y))

#define HuChanWFupdate(x) 0xB0, (x)

#define HuWait1frame 0xff

#define HuWait_frames(x) 0xfe, (x)

#define HuEndOfStream 0xfb

#define HuPeriod(x,y) (0xC0 | (x)), (y)

#endif

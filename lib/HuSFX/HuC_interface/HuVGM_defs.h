
#define HuChanOff 0x00

#define HuChanDDA 0xD0

#define HuWFvol(x) x | 0x80

#define HuDDAvol(x) x | 0x80

#define HuPan(x,y) 0xA5, (x<<4) | y

#define HuChanWFupdate(x) 0xB0,x

#define HuWait1frame 0xff

#define HuWait_frames(x) 0xfe, x

#define HuEndOfStream 0xfb

#define HuPeriod(x,y) x | 0xC0, y

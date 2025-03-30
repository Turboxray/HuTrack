
#define huChanOff 0x00

#define huChanDDA 0xD0

#define huWFvol(x) x | 0x80

#define huDDAvol(x) x | 0x80

#define huPan(x,y) 0xA5, (x<<4) | y

#define huChanWFupdate(x) 0xB0,x

#define HuWait1frame 0xff

#define HuWait_frames(x) 0xfe, x

#define huEndOfStream 0xfb

#define huPeriod(x,y) x | 0xC0, y

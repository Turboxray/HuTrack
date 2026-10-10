


  .page 2
.song
  .dw 0 ; banked-format marker
  .db 1 ; format revision
  .dw .song.tables
  .db bank(.song.tables)
.songname
  .db 65,105,114,32,90,111,110,107,32,45,32,65,113,117,97,32,66,97,115,101,0
.author
  .db 65,105,114,32,90,111,110,107,32,47,32,111,114,105,103,105,110,97,108,32,103,97,109,101,32,115,111,117,110,100,116,114
  .db 97,99,107,0


  .page 2
.song.tables
  .dw .attributes
  .db bank(.attributes)
  .dw .patternList.table
  .db bank(.patternList.table)
  .dw .instrument.table
  .db bank(.instrument.table)
  .dw .waveform.table
  .db bank(.waveform.table)
  .dw .pattern.table
  .db bank(.pattern.table)
  .dw .samples.table
  .db bank(.samples.table)



  .page 2
.attributes
  ; Extended attributes: marker, initial arp ticks, legacy volume slides
  .db 0,1,1
 ;NOTE: time base =  1
 ;NOTE: frame mode =  1
 ;NOTE: custom mode =  0

.attributes.tick1
  .db 1
.attributes.tick2
  .db 1
.attributes.rowLength
  .db 0
.attributes.patternListLen
  .db 22
.attributes.instrumentLen
  .db 37
.attributes.waveformsLen
  .db 37
.attributes.samplesLen
  .db 13



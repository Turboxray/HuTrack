


  .page 2
.song
  .dw 0 ; banked-format marker
  .db 1 ; format revision
  .dw .song.tables
  .db bank(.song.tables)
.songname
  .db 65,101,114,111,32,66,108,97,115,116,101,114,115,32,45,32,83,101,97,115,105,100,101,32,70,114,111,110,116,0
.author
  .db 79,114,105,103,105,110,97,108,32,103,97,109,101,32,115,111,117,110,100,116,114,97,99,107,0


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
  .db 18
.attributes.instrumentLen
  .db 67
.attributes.waveformsLen
  .db 5
.attributes.samplesLen
  .db 0



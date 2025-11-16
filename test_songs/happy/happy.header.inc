


.song
  .dw .song.tables
  .dw .song.tables.bank
.songname
  .db "",0
.author
  .db "",0


.song.tables
  .dw .attributes
  .dw .patternList.table
  .dw .instrument.table
  .dw .waveform.table
  .dw .pattern.table
  .dw .samples.table

.song.tables.bank
  .db bank(.attributes)
  .db bank(.patternList.table)
  .db bank(.instrument.table)
  .db bank(.waveform.table)
  .db bank(.pattern.table)
  .db bank(.samples.table)


.attributes

 ;NOTE: time base =  4
 ;NOTE: frame mode =  1
 ;NOTE: custom mode =  0

.attributes.tick1
  .db 16
.attributes.tick2
  .db 12
.attributes.rowLength
  .db 64
.attributes.patternListLen
  .db 1
.attributes.instrumentLen
  .db 9
.attributes.waveformsLen
  .db 9
.attributes.samplesLen
  .db 4



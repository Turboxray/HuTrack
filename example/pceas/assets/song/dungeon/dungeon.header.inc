


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

 ;NOTE: time base =  1
 ;NOTE: frame mode =  1
 ;NOTE: custom mode =  0

.attributes.tick1
  .db 1
.attributes.tick2
  .db 3
.attributes.rowLength
  .db 64
.attributes.patternListLen
  .db 13
.attributes.instrumentLen
  .db 12
.attributes.waveformsLen
  .db 10
.attributes.samplesLen
  .db 0



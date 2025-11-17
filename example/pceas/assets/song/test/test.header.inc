


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
 ;NOTE: custom mode =  1

.attributes.tick1
  .db 6
.attributes.tick2
  .db 6
.attributes.rowLength
  .db 48
.attributes.patternListLen
  .db 1
.attributes.instrumentLen
  .db 5
.attributes.waveformsLen
  .db 4
.attributes.samplesLen
  .db 0



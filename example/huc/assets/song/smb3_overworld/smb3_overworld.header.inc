


.song
  .dw .song.tables
  .dw .song.tables.bank
.songname
  .db "Overworld - Super Mario Bros 3",0
.author
  .db "Koji Kondo - Arr. Michirin9801",0


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

 ;NOTE: time base =  0
 ;NOTE: frame mode =  1
 ;NOTE: custom mode =  0

.attributes.tick1
  .db 1
.attributes.tick2
  .db 3
.attributes.rowLength
  .db 96
.attributes.patternListLen
  .db 10
.attributes.instrumentLen
  .db 14
.attributes.waveformsLen
  .db 9
.attributes.samplesLen
  .db 0



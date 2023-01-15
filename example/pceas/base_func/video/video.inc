loadCellToVram  .macro

      .if (\# = 2)
            MAP_BANK.2 #(\1.cell) , MPR2
            VDC.reg MAWR, #\2
            VDC.reg VRWR
            DMA.word.port \1.cell, Page.2, vdata_port, \1.cell.size
      .endif

      .if (\# = 1)
            MAP_BANK.2 #(\1.cell) , MPR2
            DMA.word.port \1.cell, Page.2, vdata_port, \1.cell.size
      .endif
  .endm

loadCellToCram.BG  .macro

        MAP_BANK.2 #(\1.pal) , MPR2
        VCE.BGblock \2
        DMA.word.port \1.pal, Page.2, vce_data, \1.pal.size
  .endm

loadCellToCram.SPR  .macro

        MAP_BANK.2 #(\1.pal) , MPR2
        VCE.SPRblock \2
        DMA.word.port \1.pal, Page.2, vce_data, \1.pal.size
  .endm

debugBENCH  .macro
.ifdef DEBUG_BENCHMARK
      MAP_BANK.2 #(\1.pal) , MPR2
      VCE.SPRblock \2
      DMA.word.port \1.pal, Page.2, vce_data, \1.pal.size
.endif
  .endm

loadDataToVram.4banks  .macro

        VDC.reg MAWR, #\2
        VDC.reg VRWR
        MAP_BANK.4 #(\1) , MPR2
        DMA.word.port \1, Page.2, vdata_port, (\1.size)

  .endm

loadDataToVram.3banks  .macro

        VDC.reg MAWR, #\2
        VDC.reg VRWR
        MAP_BANK.3 #(\1) , MPR2
        DMA.word.port \1, Page.2, vdata_port, (\1.size)

  .endm

loadDataToVram.2banks  .macro

        VDC.reg MAWR, #\2
        VDC.reg VRWR
        MAP_BANK.2 #(\1) , MPR2
        DMA.word.port \1, Page.2, vdata_port, (\1.size)

  .endm

loadDataToVram.1bank  .macro

        VDC.reg MAWR, #\2
        VDC.reg VRWR
        MAP_BANK #(\1) , MPR2
        DMA.word.port \1, Page.2, vdata_port, (\1.size)

  .endm

loadDataToVram  .macro

        VDC.reg MAWR, #\2
        VDC.reg VRWR
        MAP_BANK.2 #(\1) , MPR2
        DMA.word.port \1, Page.2, vdata_port, (\1.size)

  .endm


loadDataToCram.BG  .macro

        MAP_BANK.4 #(\1) , MPR2
        VCE.BGblock \2
        DMA.word.port \1, Page.2, vce_data, \1.size
  .endm


;...................................
init_audio
				ldx #$05
.loop
				stx $800
				stz $801
				stz $802
				stz $803
				stz $804
				stz $805
				stz $806
				stz $807
				stz $808
				stz $809
				dex
			bpl .loop
	rts
	
;...................................
init_video
				
				clx
				ldy #$80
				st0 #$00
				st1 #$00
				st2 #$00
				st0 #$02
				
.loop
				st1 #$00
				st2 #$00
				dex
			bne .loop
				dey
			bne .loop
		
				clx
				stz $402
				stz $403
.loop1
				stz $404
				stz $405
				inx
			bne .loop1
		
	rts



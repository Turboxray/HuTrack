



;//enables soft reset
enable_pad_reset:
			lda #$AA
			sta soft_reset+0
			lda	#$55
			sta soft_reset+1
			lda #$3c
			sta soft_reset+2
		rts
;#end



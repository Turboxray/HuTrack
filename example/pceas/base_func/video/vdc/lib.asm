__wait_vblank:
.reload.loop
            lda #$01
            sta __vblank
.loop
            lda __vblank
            bne .loop
            dex
            bne .reload.loop
    rts

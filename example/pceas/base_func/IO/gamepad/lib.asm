;###############################################
;
; GAMEPAD support
;
; required variables:
;
;    b1_status
;    b2_status
;    sl_status
;    st_status
;    up_status
;    dn_status
;    lf_status
;    rh_status
;
; value returned is : TRUE/FALSE
;
;

Gamepad.Init:

        stz b1_status
        stz b2_status
        stz sl_status
        stz st_status
        stz up_status
        stz dn_status
        stz lf_status
        stz rh_status

    rts


Gamepad.READ_IO.single_controller:
;
; new and improved
;
            pha
            phx
        lda #$01
        sta $1000
        lda #$03
        sta $1000
        lda #$01
        sta $1000
        pha
        pla
        nop
        nop
        lda $1000
        eor #$0f
        tax
        and #$01
        sta up_status
        txa
        and #$04
        sta dn_status
        txa
        and #$08
        sta lf_status
        txa
        and #$02
        sta rh_status


        stz $1000
        pha
        pla
        nop
        nop
        lda $1000
        eor #$0f
        tax
        and #$01
        sta b1_status
        txa
        and #$02
        sta b2_status
        txa
        and #$04
        sta sl_status
        txa
        and #$08
        sta st_status


.exit
            plx
            pla
    rts
;#end
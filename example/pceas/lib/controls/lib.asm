
;....................................................
;//initialize gamepad status variables
Controls.Init:

        MOVE.b #3, b1_delay
        MOVE.b #3, b2_delay
        MOVE.b #3, sl_delay
        MOVE.b #3, st_delay
        MOVE.b #3, up_delay
        MOVE.b #3, dn_delay
        MOVE.b #3, lf_delay
        MOVE.b #3, rh_delay
        stz b1_counter
        stz b2_counter
        stz sl_counter
        stz st_counter
        stz up_counter
        stz dn_counter
        stz lf_counter
        stz rh_counter

  rts
;#end



;....................................................
; Convert incoming raw button status into button states
Controls.ProcessInput:


;................
.dpad_check

        lda up_status
        ora dn_status
        cmp #$1+$4
      bcs .invalid
        lda lf_status
        ora rh_status
        cmp #$8+$2
      bcs .invalid
        jmp .dpad_process

.invalid
      stz input_state.directions
      jmp .button_process




;....................................................
.dpad_process

;.....................
.up
        lda up_status
      beq .up.up

.up.down
        lda input_state.directions
        and #control.up.mask
        cmp #control.up.held
      beq .up.skip
        cmp #control.up.pressed
      bne .up.count
.up.held
        lda input_state.directions
        and #(control.up.mask ^ $ff)
        ora #control.up.held
        sta input_state.directions
        bra .up.skip

.up.count
        inc up_counter
        lda up_counter
        cmp up_delay
      bcc .up.skip
.up.pressed
        stz up_counter
        lda input_state.directions
        and #(control.up.mask ^ $ff)
        ora #control.up.pressed
        sta input_state.directions
        bra .up.skip

.up.up
        lda input_state.directions
        and #control.up.mask
        cmp #control.up.inactive
      beq .up.skip
        cmp #control.up.released
      bne .up.released
.up.clear
        lda input_state.directions
        and #(control.up.mask ^ $ff)
        sta input_state.directions
        bra .up.skip
.up.released
        lda input_state.directions
        and #(control.up.mask ^ $ff)
        ora #control.up.released
        sta input_state.directions


.up.skip


;.....................
.dn
        lda dn_status
      beq .dn.up

.dn.down
        lda input_state.directions
        and #control.dn.mask
        cmp #control.dn.held
      beq .dn.skip
        cmp #control.dn.pressed
      bne .dn.count
.dn.held
        lda input_state.directions
        and #(control.dn.mask ^ $ff)
        ora #control.dn.held
        sta input_state.directions
        bra .dn.skip

.dn.count
        inc dn_counter
        lda dn_counter
        cmp dn_delay
      bcc .dn.skip
.dn.pressed
        stz dn_counter
        lda input_state.directions
        and #(control.dn.mask ^ $ff)
        ora #control.dn.pressed
        sta input_state.directions
        bra .dn.skip

.dn.up
        lda input_state.directions
        and #control.dn.mask
        cmp #control.dn.inactive
      beq .dn.skip
        cmp #control.dn.released
      bne .dn.released
.dn.clear
        lda input_state.directions
        and #(control.dn.mask ^ $ff)
        sta input_state.directions
        bra .dn.skip
.dn.released
        lda input_state.directions
        and #(control.dn.mask ^ $ff)
        ora #control.dn.released
        sta input_state.directions


.dn.skip


;.....................
.lf
        lda lf_status
      beq .lf.up

.lf.down
        lda input_state.directions
        and #control.lf.mask
        cmp #control.lf.held
      beq .lf.skip
        cmp #control.lf.pressed
      bne .lf.count
.lf.held
        lda input_state.directions
        and #(control.lf.mask ^ $ff)
        ora #control.lf.held
        sta input_state.directions
        bra .lf.skip

.lf.count
        inc lf_counter
        lda lf_counter
        cmp lf_delay
      bcc .lf.skip
.lf.pressed
        stz lf_counter
        lda input_state.directions
        and #(control.lf.mask ^ $ff)
        ora #control.lf.pressed
        sta input_state.directions
        bra .lf.skip

.lf.up
        lda input_state.directions
        and #control.lf.mask
        cmp #control.lf.inactive
      beq .lf.skip
        cmp #control.lf.released
      bne .lf.released
.lf.clear
        lda input_state.directions
        and #(control.lf.mask ^ $ff)
        sta input_state.directions
        bra .lf.skip
.lf.released
        lda input_state.directions
        and #(control.lf.mask ^ $ff)
        ora #control.lf.released
        sta input_state.directions

.lf.skip


;.....................
.rh
        lda rh_status
      beq .rh.up

.rh.down
        lda input_state.directions
        and #control.rh.mask
        cmp #control.rh.held
      beq .rh.skip
        cmp #control.rh.pressed
      bne .rh.count
.rh.held
        lda input_state.directions
        and #(control.rh.mask ^ $ff)
        ora #control.rh.held
        sta input_state.directions
        bra .rh.skip
.rh.count
        inc rh_counter
        lda rh_counter
        cmp rh_delay
      bcc .rh.skip
.rh.pressed
        stz rh_counter
        lda input_state.directions
        and #(control.rh.mask ^ $ff)
        ora #control.rh.pressed
        sta input_state.directions
        bra .rh.skip

.rh.up
        lda input_state.directions
        and #control.rh.mask
        cmp #control.rh.inactive
      beq .rh.skip
        cmp #control.rh.released
      bne .rh.released
.rh.clear
        lda input_state.directions
        and #(control.rh.mask ^ $ff)
        sta input_state.directions
        bra .rh.skip
.rh.released
        lda input_state.directions
        and #(control.rh.mask ^ $ff)
        ora #control.rh.released
        sta input_state.directions

.rh.skip


;....................................................
.button_process


;.....................
.b1
        lda b1_status
      beq .b1.up

.b1.down
        lda input_state.buttons
        and #control.b1.mask
        cmp #control.b1.held
      beq .b1.skip
        cmp #control.b1.pressed
      bne .b1.count
.b1.held
        lda input_state.buttons
        and #(control.b1.mask ^ $ff)
        ora #control.b1.held
        sta input_state.buttons
        bra .b1.skip

.b1.count
        inc b1_counter
        lda b1_counter
        cmp b1_delay
      bcc .b1.skip
.b1.pressed
        stz b1_counter
        lda input_state.buttons
        and #(control.b1.mask ^ $ff)
        ora #control.b1.pressed
        sta input_state.buttons
        bra .b1.skip

.b1.up
        lda input_state.buttons
        and #control.b1.mask
        cmp #control.b1.inactive
      beq .b1.skip
        cmp #control.b1.released
      bne .b1.released
.b1.clear
        lda input_state.buttons
        and #(control.b1.mask ^ $ff)
        sta input_state.buttons
        bra .b1.skip
.b1.released
        lda input_state.buttons
        and #(control.b1.mask ^ $ff)
        ora #control.b1.released
        sta input_state.buttons

.b1.skip


;.....................
.b2
        lda b2_status
      beq .b2.up

.b2.down
        lda input_state.buttons
        and #control.b2.mask
        cmp #control.b2.held
      beq .b2.skip
        cmp #control.b2.pressed
      bne .b2.count
.b2.held
        lda input_state.buttons
        and #(control.b2.mask ^ $ff)
        ora #control.b2.held
        sta input_state.buttons
        bra .b2.skip

.b2.count
        inc b2_counter
        lda b2_counter
        cmp b2_delay
      bcc .b2.skip
.b2.pressed
        stz b2_counter
        lda input_state.buttons
        and #(control.b2.mask ^ $ff)
        ora #control.b2.pressed
        sta input_state.buttons
        bra .b2.skip

.b2.up
        lda input_state.buttons
        and #control.b2.mask
        cmp #control.b2.inactive
      beq .b2.skip
        cmp #control.b2.released
      bne .b2.released
.b2.clear
        lda input_state.buttons
        and #(control.b2.mask ^ $ff)
        sta input_state.buttons
        bra .b2.skip
.b2.released
        lda input_state.buttons
        and #(control.b2.mask ^ $ff)
        ora #control.b2.released
        sta input_state.buttons

.b2.skip


;.....................
.st
        lda st_status
      beq .st.up

.st.down
        lda input_state.buttons
        and #control.st.mask
        cmp #control.st.held
      beq .st.skip
        cmp #control.st.pressed
      bne .st.count
.st.held
        lda input_state.buttons
        and #(control.st.mask ^ $ff)
        ora #control.st.held
        sta input_state.buttons
        bra .st.skip

.st.count
        inc st_counter
        lda st_counter
        cmp st_delay
      bcc .st.skip
.st.pressed
        stz st_counter
        lda input_state.buttons
        and #(control.st.mask ^ $ff)
        ora #control.st.pressed
        sta input_state.buttons
        bra .st.skip

.st.up
        lda input_state.buttons
        and #control.st.mask
        cmp #control.st.inactive
      beq .st.skip
        cmp #control.st.released
      bne .st.released
.st.clear
        lda input_state.buttons
        and #(control.st.mask ^ $ff)
        sta input_state.buttons
        bra .st.skip
.st.released
        lda input_state.buttons
        and #(control.st.mask ^ $ff)
        ora #control.st.released
        sta input_state.buttons

.st.skip


;.....................
.sl
        lda sl_status
      beq .sl.up

.sl.down
        lda input_state.buttons
        and #control.sl.mask
        cmp #control.sl.held
      beq .sl.skip
        cmp #control.sl.pressed
      bne .sl.count
.sl.held
        lda input_state.buttons
        and #(control.sl.mask ^ $ff)
        ora #control.sl.held
        sta input_state.buttons
        bra .sl.skip

.sl.count
        inc sl_counter
        lda sl_counter
        cmp sl_delay
      bcc .sl.skip
.sl.pressed
        stz sl_counter
        lda input_state.buttons
        and #(control.sl.mask ^ $ff)
        ora #control.sl.pressed
        sta input_state.buttons
        bra .sl.skip

.sl.up
        lda input_state.buttons
        and #control.sl.mask
        cmp #control.sl.inactive
      beq .sl.skip
        cmp #control.sl.released
      bne .sl.released
.sl.clear
        lda input_state.buttons
        and #(control.sl.mask ^ $ff)
        sta input_state.buttons
        bra .sl.skip
.sl.released
        lda input_state.buttons
        and #(control.sl.mask ^ $ff)
        ora #control.sl.released
        sta input_state.buttons

.sl.skip

    rts

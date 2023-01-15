

  .bss

                                ; The amount of time between the button physically pressed and registered as pressed.
        b1_delay:      .ds 1
        b2_delay:      .ds 1
        sl_delay:      .ds 1
        st_delay:      .ds 1
        up_delay:      .ds 1
        dn_delay:      .ds 1
        lf_delay:      .ds 1
        rh_delay:      .ds 1

        b1_counter:    .ds 1
        b2_counter:    .ds 1
        sl_counter:    .ds 1
        st_counter:    .ds 1
        up_counter:    .ds 1
        dn_counter:    .ds 1
        lf_counter:    .ds 1
        rh_counter:    .ds 1

                                ; The transition state of each button; [null, just pressed, held, just released]
        input_state:   .ds 2

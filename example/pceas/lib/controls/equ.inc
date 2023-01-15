

input_state.buttons    = input_state
input_state.directions = input_state+1

control.b1.mask     = %00000011
control.b1.held     = %00000010
control.b1.pressed  = %00000011
control.b1.released = %00000001
control.b1.inactive = %00000000

control.b2.mask     = %00001100
control.b2.held     = %00001000
control.b2.pressed  = %00001100
control.b2.released = %00000100
control.b2.inactive = %00000000

control.st.mask     = %00110000
control.st.held     = %00100000
control.st.pressed  = %00110000
control.st.released = %00010000
control.st.inactive = %00000000

control.sl.mask     = %11000000
control.sl.held     = %10000000
control.sl.pressed  = %11000000
control.sl.released = %01000000
control.sl.inactive = %00000000

control.up.mask     = %00000011
control.up.held     = %00000010
control.up.pressed  = %00000011
control.up.released = %00000001
control.up.inactive = %00000000

control.dn.mask     = %00001100
control.dn.held     = %00001000
control.dn.pressed  = %00001100
control.dn.released = %00000100
control.dn.inactive = %00000000

control.lf.mask     = %00110000
control.lf.held     = %00100000
control.lf.pressed  = %00110000
control.lf.released = %00010000
control.lf.inactive = %00000000

control.rh.mask     = %11000000
control.rh.held     = %10000000
control.rh.pressed  = %11000000
control.rh.released = %01000000
control.rh.inactive = %00000000


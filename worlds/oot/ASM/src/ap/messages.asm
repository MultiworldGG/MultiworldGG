; Expand AP names and wrap the actual text after Message_OpenText loads it.
; Hook its shared return so both starting and continuing a textbox are covered.
ap_message_after_load:
    jal     ap_format_item_message
    lw      a0, 0x40(sp)          ; original Message_OpenText play argument
    lw      ra, 0x14(sp)
    jr      ra
    addiu   sp, sp, 0x40          ; original Message_OpenText stack frame

ap_message_payload_end:
.headersize (0x800110A0 - 0xA87000)
.org 0x800DCE08
    j       ap_message_after_load
    nop
.headersize (0x80400000 - 0x03480000)
.org ap_message_payload_end

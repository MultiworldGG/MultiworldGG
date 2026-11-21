HandleOwlStatue:
    call GetRoomStatusAddressInHL
    ld   a, [hl]
    and  $20
    ret  nz
    ld   a, [hl]
    or   $20
    ld   [hl], a

    ; use OffsetPointerByRoomNumber to get current map
    ; we're going to set our fake room differently depending on it
    ; see locations.owlStatue for transformation
    ld   hl, $0000
    call OffsetPointerByRoomNumber
    push hl ; store it to fix at end
    ld   a, h
    and  a
    jr   z, .mapZero
    dec  a
    jr   z, .mapOne
    dec  a
    jr   z, .mapTwo
.mapThree:
.mapZero:
    inc  hl
    ld   a, l
    jr   .finish
.mapTwo:
    inc  hl
    inc  hl
    jr   .mapZero
.mapOne:
    ld   a, l
    sub  $31
    xor  $75
.finish:
    ldh  [$FFF6], a
    call GiveItemAndMessageForRoomMultiworld
    pop  hl
    ld   a, l
    ldh  [$FFF6], a
    ret


GetRoomStatusAddressInHL:
    ld   a, [$DBA5] ; isIndoor
    ld   d, a
    ld   hl, $D800
    ldh  a, [$FFF6]   ; room nr
    ld   e, a
    ldh  a, [$FFF7]   ; map nr
    cp   $FF
    jr   nz, .notColorDungeon

    ld   d, $00
    ld   hl, $DDE0
    jr   .notIndoorB

.notColorDungeon:
    cp   $1A
    jr   nc, .notIndoorB

    cp   $06
    jr   c, .notIndoorB

    inc  d

.notIndoorB:
    add  hl, de
    ret


RenderOwlStatueItem:
    ldh  a, [$FFF6] ; map room
    cp $B2
    jr nz, .NotYipYip
    ; Add 2 to room to set room pointer to an empty room for trade items
    add a, 2
    ldh [$FFF6], a
    call RenderItemForRoom
    ldh  a, [$FFF6] ; map room
    ; ...and undo it
    sub a, 2
    ldh [$FFF6], a
    ret
.NotYipYip:
    call RenderItemForRoom
    ret

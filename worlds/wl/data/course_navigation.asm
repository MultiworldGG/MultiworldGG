; Optional course navigation. Rebuild with data/build_course_navigation.py and RGBDS.
DEF CourseHandlePathCommand EQU $5E53
DEF CourseNextAddress EQU $5E45
DEF CourseNativeNextSegment EQU $5E48

SECTION "Course getdir and segments", ROMX[$6E31], BANK[8]
CourseGetDir:
    ld a, [$A79E]
    cp $2F
    jr z, .native
    ld l, a
    ld h, $A5
    ld l, [hl]
    ret
.native:
    ld hl, $5629
    ld a, $2F
    jp $5F99
CourseGetSegment:
    ld a, [$A79E]
    cp $2F
    jr z, .native
    ld a, [hl]
    ld e, a
    ld d, $A5
    ld a, [$A7E3]
    ld b, a
.nextPath:
    ld a, [de]
    cp $FF
    jr z, .end
    inc de
    push de
    ld hl, $5760
    call $5F99
    pop de
.nextSegment:
    ld a, [hl]
    cp $FF
    jr z, .nextPath
    ld a, b
    and a
    ret z
    sub 3
    ld b, a
    inc hl
    inc hl
    inc hl
    jr .nextSegment
.end:
    ld h, d
    ld l, e
    ret
.native:
    ld a, [hl]
    ld hl, $5760
    jp $5F99
CourseDraw:
    ld a, [$A79C]
    cp 3
    jp nc, CourseHideDots
    ld a, $83
    ldh [$FF40], a
    ret
ASSERT @ <= $6E8C

SECTION "Course validation", ROMX[$7EB6], BANK[8]
CourseEnter:
    ld a, [$A79E]
    add $B0
    ld l, a
    ld h, $A4
    ld a, [hl]
    and a
    ret z
    ld a, $2B
    ld [$A61C], a
    jp $5D79
CourseValidateDirection:
    push af
    ld a, [$A79C]
    cp 2
    jr z, .native
    pop af
    ret
.native:
    pop af
    and b
    ret z
    ld a, b
    jp $6225
ASSERT @ <= $7EE1

SECTION "Course markers", ROMX[$7081], BANK[8]
CourseHideDots:
    push bc
    push de
    push hl
    ld a, $FF
    ld [$A4E1], a
    ld a, [$A79F]
    cp 7
    jr nz, .world
    ld a, 1
.world:
    ld hl, CourseMarkerPointers
    call $5F99
    ld a, [hl+]
    ld b, a
.loop:
    ld a, [hl+]
    cp $FF
    jr z, .end
    ld c, a
    and $7F
    add $B0
    ld e, a
    ld d, $A4
    ld a, [de]
    and a
    jr nz, .skip
    call CourseDotTile
    ld [$A4E0], a
    ld a, [hl+]
    ld [$A4E2], a
    ld a, [hl+]
    ld [$A4E3], a
    push bc
    push hl
    ld bc, $A4E0
    ld hl, $A4E2
    call $68A6
    pop hl
    pop bc
    jr .loop
.skip:
    inc hl
    inc hl
    jr .loop
.end:
    pop hl
    pop de
    pop bc
    ld a, $83
    ldh [$FF40], a
    ret
ASSERT @ <= $70D6

SECTION "Course next segment", ROMX[$6C33], BANK[8]
CourseNextSegment:
    ld a, [$A79E]
    cp $2F
    jr z, .native
    jp CourseHandlePathCommand
.native:
    ld a, [$A7E3]
    jp CourseNativeNextSegment
ASSERT @ <= $6C4D

SECTION "Course dotted castle tile", ROMX[$6C43], BANK[8]
CourseDotTile:
    ld a, b
    bit 7, c
    ret z
    ld a, $75
    ret
ASSERT @ <= $6C4D

SECTION "Course getdir hook", ROMX[$5F93], BANK[8]
    jp CourseGetDir
SECTION "Course segment hook", ROMX[$5F80], BANK[8]
    jp CourseGetSegment
SECTION "Course validation hook", ROMX[$6222], BANK[8]
    jp CourseValidateDirection
SECTION "Course entry hook", ROMX[$5D74], BANK[8]
    jp CourseEnter
SECTION "Course dots hook", ROMX[$533F], BANK[8]
    call CourseDraw
    nop
SECTION "Course next hook", ROMX[CourseNextAddress], BANK[8]
    jp CourseNextSegment
SECTION "Keep course 10 after lid", ROMX[$7901], BANK[8]
    ret

; Universal Tracker entrance discovery. All AP hooks live here; grotto.asm stays upstream.
; ut/rom.py replaces shuffled source indices with 0x2000 + source_id * 4 + variant.
; The four variants preserve blue-warp age/cutscene aliases. Resolve tags BEFORE any
; vanilla entrance-table lookup, then record discovery when Play_Init loads that destination.
; The RAM bitset lasts until reset. The client merges it into server datastorage.

AP_UT_ENTRANCE_DESTINATIONS:
.fill 512 * 4 * 2, 0
AP_UT_FOUND_ENTRANCES:
.fill 512 / 8, 0
AP_UT_PENDING_ENTRANCE:
.halfword 0                       ; source_id + 1; zero means no pending discovery
AP_UT_PENDING_DESTINATION:
.halfword 0
.align 4

; a0 = tagged or ordinary entrance; v0/a0 = real entrance.
; Match handle_grotto_load's register contract: only a0, v0, t0-t3 may change.
; In particular, scene_exit_hook needs at and t6 preserved.
ap_resolve_entrance:
    addiu   sp, sp, -0x20
    sw      ra, 0x1C(sp)
    sw      zero, 0x18(sp)
    addiu   t0, a0, -0x2000
    sltiu   t1, t0, 512 * 4
    beqz    t1, @@translate_grotto
    nop
    srl     t1, t0, 2
    addiu   t1, t1, 1
    sw      t1, 0x18(sp)
    sll     t0, t0, 1
    la      t1, AP_UT_ENTRANCE_DESTINATIONS
    addu    t1, t1, t0
    lhu     a0, 0(t1)

@@translate_grotto:
    jal     ap_original_grotto_load
    nop
    lw      t0, 0x18(sp)
    beqz    t0, @@return
    nop
    la      t1, AP_UT_PENDING_ENTRANCE
    sh      t0, 0(t1)
    move    t2, v0
    li      t3, 0x7FFF
    bne     t2, t3, @@store_destination
    nop
    ; A grotto return is resolved by Player after scene_exit_hook returns.
    ; Keep 0x7FFF in v0, but expect the actual return entrance on arrival.
    la      t3, SAVE_CONTEXT
    lhu     t2, 0x1394(t3)
@@store_destination:
    sh      t2, 2(t1)
@@return:
    lw      ra, 0x1C(sp)
    jr      ra
    addiu   sp, sp, 0x20

ap_original_grotto_load:
    ; Displaced first two instructions of upstream handle_grotto_load.
    li      t0, 0x7FF9
    j       handle_grotto_load + 8
    sub     t0, a0, t0

; a0 = PlayState*. Used both before Play_Update (songs, owls, blue warps)
; and before Scene_SetTransitionForNextEntrance (which reads the entrance table).
ap_resolve_next_entrance:
    addiu   sp, sp, -0x20
    sw      ra, 0x1C(sp)
    sw      a0, 0x18(sp)
    lui     t0, 1
    addu    t0, t0, a0
    jal     ap_resolve_entrance
    lhu     a0, 0x1E1A(t0)
    lw      a0, 0x18(sp)
    lui     t0, 1
    addu    t0, t0, a0
    sh      v0, 0x1E1A(t0)
    lw      ra, 0x1C(sp)
    jr      ra
    addiu   sp, sp, 0x20

ap_entrance_before_update:
    addiu   sp, sp, -0x20
    sw      ra, 0x1C(sp)
    sw      a0, 0x18(sp)
    lui     t0, 1
    addu    t0, t0, a0
    lbu     t1, 0x1E15(t0)
    li      t2, 0x14
    beq     t1, t2, @@resolve
    nop
    ; A cancelled departure must not become a discovery on a later respawn.
    la      t0, AP_UT_PENDING_ENTRANCE
    b       @@return
    sh      zero, 0(t0)
@@resolve:
    jal     ap_resolve_next_entrance
    nop
@@return:
    lw      a0, 0x18(sp)
    lw      ra, 0x1C(sp)
    addiu   sp, sp, 0x20
    ; Displaced Play_Update prologue.
    addiu   sp, sp, -0x78
    j       0x8009AF24
    sw      s0, 0x24(sp)

ap_entrance_transition:
    addiu   sp, sp, -0x18
    sw      ra, 0x14(sp)
    jal     ap_resolve_next_entrance
    nop
    lw      ra, 0x14(sp)
    addiu   sp, sp, 0x18
    ; Displaced Scene_SetTransitionForNextEntrance prologue.
    lui     v0, 0x8012
    j       0x800826E4
    addiu   v0, v0, 0xA5D0

ap_entrance_on_load:
    addiu   sp, sp, -0x20
    sw      ra, 0x1C(sp)
    sw      a0, 0x18(sp)
    ; File-select spawns enter Play_Init without a Play_Update transition.
    la      t0, SAVE_CONTEXT
    jal     ap_resolve_entrance
    lw      a0, 0(t0)
    la      t0, SAVE_CONTEXT
    sw      v0, 0(t0)
    lw      t0, 0x135C(t0)         ; game mode: don't discover title-screen demos
    la      t1, AP_UT_PENDING_ENTRANCE
    lhu     t2, 0(t1)
    sh      zero, 0(t1)
    bnez    t0, @@return
    nop
    beqz    t2, @@return
    nop
    lhu     t0, 2(t1)
    bne     t0, v0, @@return      ; transition was redirected or cancelled
    nop
    addiu   t2, t2, -1
    srl     t0, t2, 3
    andi    t2, t2, 7
    li      t3, 1
    sllv    t3, t3, t2
    la      t1, AP_UT_FOUND_ENTRANCES
    addu    t1, t1, t0
    lbu     t0, 0(t1)
    or      t0, t0, t3
    sb      t0, 0(t1)
@@return:
    lw      a0, 0x18(sp)
    lw      ra, 0x1C(sp)
    addiu   sp, sp, 0x20
    ; Displaced Play_Init prologue.
    addiu   sp, sp, -0x90
    j       0x8009A758
    sw      s2, 0x28(sp)

ap_entrance_payload_end:

; Replace the entry of the existing grotto translator instead of modifying it.
.org handle_grotto_load
    j       ap_resolve_entrance
    nop

.headersize (0x800110A0 - 0xA87000)
.org 0x8009AF1C                  ; Play_Update
    j       ap_entrance_before_update
    nop
.org 0x800826DC                  ; Scene_SetTransitionForNextEntrance
    j       ap_entrance_transition
    nop
.org 0x8009A750                  ; Play_Init
    j       ap_entrance_on_load
    nop

.headersize (0x80400000 - 0x03480000)
.org ap_entrance_payload_end

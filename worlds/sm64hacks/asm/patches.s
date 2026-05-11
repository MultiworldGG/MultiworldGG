.n64
.create "trap_patch", 0x8029D4B8
_start_trap:
.area 0x1C4
    SW S0, 0x001C(SP)
    LA T1, _flag
    LW S0, 0(T1)
    ADDIU T3, R0, 0x006B
    BEQ S0, T3, _1up
    NOP
    ADDIU T3, R0, 0x0069
    BNE S0, T3, _heaveho
    NOP
_1up:
    SW R0, 0(T1)
    LI A0, 0x80361158;mario
    LW A0, 0(A0)
    ADDIU A1, R0, 0x00D4 ;1-up model
    LI A2, 0x13004148 ;1-up bhv
    JAL 0x8029EDCC;spawn_object
    NOP
    ADDIU T3, R0, 0x006B;dont actually set flag if just 1-up :)
    BEQ S0, T3, _end;should make 1-ups more fun now
    NOP
    LA T1, _greendemon
    SW V0, 0(T1);put pos of object in the greendemon memory address
    B _end
    NOP
_heaveho:;jump table would probably be better but i cba to do that
    ADDIU T3, R0, 0x006A
    BNE S0, T3, _spin
    NOP
    SW R0, 0(T1)
    LI A0, 0x80361158;mario
    LW A0, 0(A0)
    ADDIU A1, R0, 0x007A ;star model. heaveho model doesnt always exist so this is a good patchwork solution to that problem
    LI A2, 0x13001548 ;1-up bhv
    JAL 0x8029EDCC;spawn_object
    NOP
    LA T1, _heavehoaddr
    SW V0, 0(T1)
    B _end
    NOP
_spin:
    LA T1, _spinaddr
    LW T2, 0(T1)
    BNE T2, T3, _steve
    NOP
    LUI T4, 0x8034
    LHU T5, 0xC74C(T4)
    ADDIU T5, 0x50
    SH T5, 0xC74C(T4)
    B _end
    NOP
_steve:
    ADDIU T3, T3, 0x0001
    BNE T2, T3, _end
    NOP
    LA A2, 0x801F1000
    ADDIU A0, R0, 0x50
    JAL 0x802D6554 ;print_text
    ADDIU A1, R0, 0x50
    

;_choir:
 ;   LA T1, _choirflag
 ;   LW T2, 0(T1)
 ;   BEQ T2, R0, _undo
  ;  LUI T0, 0x2412 ;ADDU S2, R0, X
  ;  ADDU T0, T0, T2
  ;  LUI T3, 0x8032
 ;   B _end
 ;   SW T0, 0x91E0(T3) ;self-modifying code won't ever bite me in the ass...


    ;this is a janky solution as im changing the bank in a completely unrelated section of code but its the best i can do right now
    ;reloading song
    ;LUI T3, 0x8033
    ;LW T3, 0xDDCC(T3)
    ;OR A2, R0, R0
    ;LHU A0, 0x0036(T3)
    ;JAL 0x80249178;set_background_music
    ;LHU A1, 0x0038(T3)
;_undo:
 ;   LI T0, 0x8FD20048 ;LW S2, 0x0048
 ;   LUI T3, 0x8032
 ;   SW T0, 0x91E0(T3) ;self-modifying code won't ever bite me in the ass...
_end:
    B _return_traps
    NOP
_return_traps:
    LW S0, 0x001C(SP)
    LW RA, 0x0014(SP)
    ADDIU SP, SP, 0x28
    JR RA
    NOP
_spinaddr:
    NOP
_staraddr:
    NOP
_flag:
    NOP
_greendemon:
    NOP
_heavehoaddr:
    NOP
.endarea
.close


.create "choir_patch", 0x8027FF00; this is to get "extra space" in load_banks_immediate to set s2 to the specific value we want
_start_choir:                    ; plenty of conventions are broken here in this "function" to save on space because of that
.area 0xF4
    LA T2, _choiraddr
    LW T2, 0(T2)
    BEQZ T2, _normal
    NOP
    B _end_choir
    ADDU S2, R0, T2
_normal:
    LW S2, 0x0048(FP)
_end_choir:
    JR RA
    NOP
_choiraddr:
    NOP
.endarea
.close

.create "star_patch", 0x80279C88
_star:
.area 0xC
   LA T3, _staraddr
   SW A1, 0(T3)
.endarea
.close

.create "move_patch_hook", 0x80252CFC ; hook in set_mario_action to extend function to the below code 
.area 0x8
    J _start_move_checks
    NOP
.endarea
.close

.create "move_patch", 0x801F1100 ;hooks into set_mario_action
.area 0x500
_start_move_checks:
    SW A0, 0x0028(SP)
    SW A1, 0x002C(SP) ;code replaced in the hook

    XORI T8, 0x4069
    BEQZ T8, _go_back ;special cases
    NOP

    LUI T7, 0x0000
    ORI T7, R0, 0x0001
    LI T9, 0x03000880
    BEQ T9, A1, _check_if_allowed ;single jump
    LI T9, 0x030008A0
    BEQ T9, A1, _check_if_allowed ;hold jump
    LI T9, 0x03000885
    BEQ T9, A1, _check_if_allowed ;steep jump
    LI T9, 0x010208B4
    BEQ T9, A1, _check_if_allowed ;burning jump


    LI T9, 0x03000881
    BEQ T9, A1, _check_if_allowed ;double jump
    ORI T7, R0, 0x0002

    LI T9, 0x01000882
    ORI T7, R0, 0x0004
    BEQ T9, A1, _check_if_allowed ;triple jump
    LI T9, 0x03000894
    BEQ T9, A1, _check_if_allowed ;flying triple jump
    LI T9, 0x030008AF
    BEQ T9, A1, _check_if_allowed ;special triple jump (never going to matter but im doing it)

    LI T9, 0x03000888
    BEQ T9, A1, _check_if_allowed ;long jump
    ORI T7, R0, 0x0008
    
    LI T9, 0x01000883
    BEQ T9, A1, _check_if_allowed ;backflip
    ORI T7, R0, 0x0010
    
    LI T9, 0x01000887
    BEQ T9, A1, _check_if_allowed ;sideflip
    ORI T7, R0, 0x0020

    LI T9, 0x03000886
    BEQ T9, A1, _check_if_allowed ;wallkick
    ORI T7, R0, 0x0040

    LI T9, 0x018008AA
    BEQ T9, A1, _check_if_allowed ;slidekick
    ORI T7, R0, 0x0080

    LI T9, 0x0188088A
    BEQ T9, A1, _check_if_allowed ;dive
    ORI T7, R0, 0x0100

    LI T9, 0x00800380
    ORI T7, R0, 0x0A00 ; allow punch if punch or kick
    BEQ T9, A1, _check_if_allowed ;punch
    LI T9, 0x00800457
    BEQ T9, A1, _check_if_allowed ;moving punch

    LI T9, 0x008008A9
    BEQ T9, A1, _check_if_allowed ;ground pound
    ORI T7, R0, 0x0400

    LI T9, 0x018008AC
    BEQ T9, A1, _check_if_allowed ;kick
    ORI T7, R0, 0x0800


    B _go_back ;if not in this list always allowed allowed
_check_if_allowed:
    LA T9, _jumps_allowed
    LW T9, 0(T9)
    AND T7, T7, T9
    BEQZ T7, _return_moves
    NOP 
_go_back:
    J 0x80252D04
    NOP
_return_moves: ;return since you arent in the function anymore
    OR V0, R0, R0
    ADDIU SP, SP, 0x28
    JR RA
    NOP
_burn_extension:
    LW A0, 0x0020(SP)
    LW A1, 0x001C(SP)
    ORI T8, R0, 0x4069
    JR RA
    NOP
_tree_extension:
    LUI A1, 0x0300
    ORI A1, A1, 0x0886
    ORI T8, R0, 0x4069
    JR RA
    NOP
_punch_extension:
    LHU T4, 0x0002(T2)
    ANDI T5, T4, 0x0080
    LA T7, _jumps_allowed
    LW T7, 0(T7)
    ORI T6, T7, 0x0A00 ;check if both punch and kick, go back to function if so
    BEQ T6, T7, _punch_end
    NOP
    ANDI T6, T7, 0x0200
    BNEZ T6, _punch_end
    ORI T5, R0, 0x0000
    ORI T5, R0, 0x0001
_punch_end:
    JR RA
    NOP
_move_punch_extension:
    LHU T8, 0x0002(T6)
    ANDI T9, T8, 0x0080
    LA T0, _jumps_allowed
    LW T0, 0(T0)
    ORI T1, T0, 0x0A00 ;check if both punch and kick, go back to function if so
    BEQ T1, T0, _move_punch_end
    NOP
    ANDI T1, T0, 0x0200
    BNEZ T1, _move_punch_end
    ORI T9, R0, 0x0000
    ORI T9, R0, 0x0001
_move_punch_end:
    JR RA
    NOP
    
_shell_extension:
    LW T9, 0x001C(SP)
    ADDIU AT, R0, 0x0040
    LA T0, _jumps_allowed
    LW T0, 0(T0)
    ANDI T0, T0, 0x1000
    BNEZ T0, _shell_allowed
    NOP
    J 0x8024F778
    NOP
_shell_allowed:
    JR RA
    NOP
_slope_fix_extension:
    LW A1, 0x0020(SP)
    JAL 0x802530A0
    ORI A2, R0, 0x0000
    BEQZ V0, _slope_fix_failed
    NOP
    J 0x80268058 ;jump successfully
    NOP
_check_wallkick_extension:
    LHU T7, 0x0002(T6)
    ANDI T8, T7, 0x0002
    LA T9, _jumps_allowed
    LW T9, 0(T9)
    ANDI T9, T9, 0x0040
    SRL T9, T9, 5
    AND T8, T8, T9
    JR RA
    NOP
_air_hit_wall_extension:
    LHU T4, 0x0002(T3)
    ANDI T5, T4, 0x0002
    LA T6, _jumps_allowed
    LW T6, 0(T6)
    ANDI T6, T6, 0x0040
    SRL T6, T6, 5
    AND T5, T5, T6
    JR RA
    NOP
_slope_fix_failed:
    J 0x80268028
    NOP
_drop_and_set_mario_action_if_gp:
    ADDIU SP, SP, -0x18
    SW RA, 0x0014(SP)
    ORI T0, R0, 0x0400
    LA T1, _jumps_allowed
    LW T1, 0(T1)
    AND T0, T0, T1
    BEQZ T0, _gpend
    NOP
    JAL 0x80253178
    NOP
_gpend:
    LW RA, 0x0014(SP)
    ADDIU SP, SP, 0x18
    JR RA
    NOP
_jumps_allowed: 
    NOP

.endarea
.close

.create "burning_patch", 0x8024EC1C
.area 0x8
    JAL _burn_extension
    NOP
.endarea
.close

.create "tree_patch_1", 0x8025E64C
.area 0x8
    JAL _tree_extension
    NOP
.endarea
.close

.create "tree_patch_2", 0x8025E2BC
.area 0x8
    JAL _tree_extension
    NOP
.endarea
.close

.create "punch_patch", 0x80275398
.area 0x8
    JAL _punch_extension
    NOP
.endarea
.close

.create "move_punch_patch", 0x802665FC
.area 0x8
    JAL _move_punch_extension
    NOP
.endarea
.close

.create "shell_patch", 0x8024F6E0
.area 0x8
    JAL _shell_extension
    NOP
.endarea
.close

.create "slope_fix_patch", 0x80268010
.area 0x8
    J _slope_fix_extension
    NOP
.endarea
.close

.create "wallkick_patch_1", 0x8026D34C
.area 0x8
    JAL _check_wallkick_extension
    NOP
.endarea
.close

.create "wallkick_patch_2", 0x8026D9D4
.area 0x8
    JAL _air_hit_wall_extension
    NOP
.endarea
.close

.create "hold_jump_gp_patch", 0x8026BB5C
.area 0x8
    JAL _drop_and_set_mario_action_if_gp
    OR A2, R0, R0
.endarea
.close

.create "hold_jump_freefall_patch", 0x8026BC7C
.area 0x8
    JAL _drop_and_set_mario_action_if_gp
    OR A2, R0, R0
.endarea
.close

;single jump = 0x0001, 
;double jump = 0x0002, 
;triple jump = 0x0004, 
;long_jump = 0x0008, 
;backflip = 0x0010, 
;sideflip = 0x0020, 
;wallkick = 0x0040, 
;slidekick = 0x0080, 
;dive = 0x0100, 
;punch = 0x0200,
;ground pound = 0x0400,
;kick = 0x0800
;shell = 0x1000

.create "decades_later_patch", 0x801E1000
.area 0x100
    ADDIU T9, RA, 0x0000 ;BAD but i dont want to mess with SP in this "not a function"
    LW A0, 0x8032DDF4 ;gCurrSaveFileNum
    SRL A0, A0, 16
    JAL 0x8027A1C8 ;save_file_get_star_flags
    ADDIU A0, A0, -0x1
    ANDI V0, V0, 0x001F ;dont want to somehow accidentally end up on "act 7/8"
    ADDIU T7, V0, 0x0000
    LUI V0, 0x0000
_most_significant_bit:
    ADDIU V0, V0, 0x1
    ANDI T8, T7, 0x1
    SRL T7, T7, 0x1
    BNEZ T8, _most_significant_bit
    NOP
    LUI AT, 0x8034
    J 0x801D0A68
    ADDIU RA, T9, 0x0000
    NOP
.endarea
.close



; set_mario_action deets:
; A0: mariostate
; A1: action id 

;i tried okay this just doesnt work for god knows what reason. it should work it just doesnt and fuck this

;.create "punch_or_kick_function", 0x8029AD80
;_punch_or_kick:
;    ADDIU SP, SP, -0x20
;    SW RA, 0x0014(SP)
;    SW A0, 0x0020(SP)
;    LW T6, 0x0020(SP)
;    LHU T7, 0x0002(T6)
;    ANDI T5, T7, 0x0080
;    BNEZ T5, _kick
;    NOP
;    LI A1, 0x00800380
;    JAL 0x80252CF4
;    OR A2, R0, R0
;    B _end
;    NOP
;_kick:
;    LI A1, 0x018008AC
;    JAL 0x80252CF4
;    OR A2, R0, R0
;_end:
;    LW RA, 0x0014(SP)
;    ADDIU SP, SP, 0x20
;    JR RA
;    NOP
;.close

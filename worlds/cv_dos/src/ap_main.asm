.nds
.relativeinclude on
.erroronwarning on
;.loadtable "dos_text.tbl"

@Overlay41Start equ 0x02308920
@FreeSpace equ @Overlay41Start + 0x50

@SoulFlagTable equ 0x02308930
@ServerItemType equ 0x02308940 ; 2 bytes
@SkipNameShowFlag equ 0x02308942 ; 1 byte
@TotalItemsReceived equ 0x0230894E ; 2 bytes
@GateKeys equ 0x02308943 ; 1 byte
@DoorKeys equ 0x02308944 ; 2 bytes ; Also includes the Chapel Gate


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/arm9.bin", 02000000h
;;Fixes ability souls setting other bits unintentionally
.org 0x0202E258
  b 0202E300h

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

.org 0x0203008C
    bl @GetItemFromServer

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x02010BCC
    bl @LoadAPData

.org 0x020111B8
    bl @SaveAPData

.org 0x020103A4
    bl @CopyAPData

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x02024D78
    b @PreventPlayerFromCorruptingData

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x02030010
    bl @OneScreenLowerMapOnBottom

.org 0x02030138
    bl @MapInit_CloseMapAndReset

.org 0x02021A40
    bl @MapInit_SkipWarpRoomCheck

.org 0x02039910
    bl @OneScreen_DisableScreenSwap

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x02020CE8
    bl @SetCanColor_Page

.org 0x02020D38
    bl @SetCanColor_Item

;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x0202DFB8
    b @LoadAPNameColor

;;;;;;;;;;;;;;;;;;;;;;;
.org 0x02034244
    nop ;Disable Soul Release

;;;;;;;;;;;;;;;;;;;;;;
.org 0x0203000C
    bl @CheckIfDeathReceived

.org 0x0202C63C
    b @SkipSoulPopupIfDead

;;;;;;;;;;;;;;;;;;;;;;
.org 0x0203AC60
    ; Enemies on topscreen
    b @EnemySouls_TopScreen

;;;;;;;;;;;;;;;;;;;;;;
.org 0x02042834
    ; Extended text pointers
    b @RepointExtendedTexIDs

.org 0x0202DF6C
    b @ShowItem_ExpandPointers

.org 0x0202DF68
    b @DisplayExpandedItemNames

.org 0x0204263C
    b @ExpandTextPointers_Menus

.org 0x0202E978
    b @ExpandTextPointers_PopupLength

.org 0x0202E9E8
    bl @ExpandTextPointers_Popups

;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;
.org 0x020B1BD4
    .dh 0x8000 ; tower

.org 0x020B1A60
    .dh 0x8001 ; twwarp

.org 0x020AC5C0
    .dh 0x8002 ; garden

.org 0x020BE41C
    .dh 0x8003 ; menace

;;;;;;;;;;;;;;;;;;;;
.org 0x0202682C
    bl @ThroneBoss_MirrorEntities


.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_0", 0219E3E0h

.org 0x021E9674
    bl @ToggleSoulFlag

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021D7B1C
    bl @FilterItemFlagHigh

.org 0x021E8A48
    bl @FilterWriteFlagHigh

.org 0x021E897C
    b @SpecialItemHandler ;This is normally the GetItem call in the get consumable func

.org 0x021E8AA8
    bl @SkipShowName

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021EEED4
    b @WarpToStart

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021E9640
    b @GetItemFromSoul
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021F60B4
    b @GiveStartingInventory

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021AF560
;Special/trigger items need to be handled differently, since they don't run the touch pickup code
bl @FilterSpecialItemFlagHigh

.org 0x021AFA28 ;Stop these items from being given by the original code
nop

.org 0x021AFA30
bl @GetItemFromSpecial

;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;
    ;Skip Ability souls activating normally
.org 0x021E96EC
    nop

;;;;;;;;;;;;;;;;;
.org 0x021BD16C
    b @MapInit_SkipActingLikeWarpRoom

.org 0x021BD074
    bl @MapInit_SkipGroundCheck

.org 0x021BD138
    bl @MapInit_LoadPlayerCoordinates

.org 0x021BD080
    bl @MapInit_ContinueCurAnim

.org 0x021BC93C
    bl @MapInit_AllocateWarpSpaceSelect

.org 0x021BCB70
    bl @MapInit_DisableTouchControls

.org 0x021BC8E4
    bl @MapInit_CloseWithBorSel

.org 0x021C852C
    bl @OneScreen_SetFirstScreenEnemy

;;;;;;;;;;;;;;;;;;;;;
.org 0x021E860C
    bl @SetSoulPerPickup

;;;;;;;;;;;;;;;;;;;;;
.org 0x021F6054
    bl @InitStartingWarpRoom

;;;;;;;;;;;;;;;;
.org 0x021AF5CC
    .dw 0x022C4684 ; Set the easter egg items to always use the full item palette

;;;;;;;;;;;;;;;;;;
.org 0x0220ED90
    ; Soul percent display
    bl @Soulsanity_SoulCheck

.org 0x021ED0B4
    ;Bestiary count
    bl @Soulsanity_SoulCheck

;;;;;;;;;;;;;;;;;
.org 0x021E8984  ; Don't stop from getting 9 items
    nop

;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021A748C
    b @GateSanity_CheckGateButtons ; Get items from the regular Gates

.org 0x021A737C
    ;Makes the Button go down based on the flag
    bl @GateSanity_CheckIfPressed

.org 0x021A7354
    ;Button collision- makes it not pressable
    bl @GateSanity_CheckIfPressed

.org 0x021EE7C0
    cmp r6, 0x47 ; Add 5 new items CHANGE WHEN ADDING DOOR LOCKS

.org 0x021EE784
    bl @ExtendedInv_SkipCountingItems

.org 0x021EE7AC
    bl @LoadExtendedItemNames

.org 0x021EE574
    bl @DrawExtendedNames_MenuHover

.org 0x021EE794
    bl @ExtendedInv_ShiftIDs

.org 0x021E7A88
    b @ExtendedInv_PointToData

.org 0x021E787C
    b @GiveExpandedItems

.org 0x021EE5D8
    bl @LoadExpandedDescriptions

.org 0x021E7B40
    b @FixExpandedItemTypes

.org 0x021A73FC
    b @OpenGatesWithKeys
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; Passive Soul eater
.org 0x021C3AA0
    bl @CheckPassiveSoulEaterRing
;;;;;;;;;;;;;;;;;;;;

.org 0x02215800 ; Remove the failsafe for Magic Seals not loading
    nop ; Death doesn't have room, and failing this
    nop ; causes a softlock when randomized.

.org 0x022153E0
    cmp r0, 0 ; This is a failsafe for the seal not loading
    beq @ReloadSealSlot ; We need to reload the entity without the GFX if this happens

 .org 0x0222CA80
    .dw @DarioEvent_Update

.org 0x0222C8A4
    .dw @DarioEvent_Create

.org 0x0222C8A0
    .dw @DimitriiEventCreate

.org 0x0222CA7C
    .dw @DimitriiEvent_Update

.org 0x021A9C78
    nop

.org 0x021A9C70
    nop ; Door collision delete

;;;;;;;;;;;;;;;;;;;;;
.org 0x021D7A64
    b @DespawnTowerBosses
;;;;;;;;;;

.org 0x0220F29C
    bl @ThroneBoss_ReloadRoom

.org 0x0220F378
    bl @ThroneBoss_LeaveMirror


.org 0x02227158 ; Replacement throne room entity list
@EntList_MirrorThrone:
    ; Boss door
    .dh 0x0000
    .dh 0x0080
    .db 0x00
    .db 0x02
    .db 0x25
    .db 0x00
    .dh 0x0001 
    .dh 0x000B
    ;;;;;;;;
    .dh 0x01F0
    .dh 0x00B0
    .db 0x00
    .db 0x02
    .db 0x25
    .db 0x00
    .dh 0x0001 
    .dh 0x0000
    ;;;;;;;;
    ; Mirror world
    .dh 0x0000
    .dh 0x0000
    .db 0x00
    .db 0x02
    .db 0x0B
    .db 0x00
    .dh 0x0000
    .dh 0x0000
    ;;;;;;;;;;
    ;Mirror
    .dh 0x0100
    .dh 0x0070
    .db 0x00
    .db 0x02
    .db 0x0A
    .db 0x00
    .dh 0x0001
    .dh 0x0000
    ;;;;;;;;;;;;
    ;Aguni
    .dh 0x0100
    .dh 0x0060
    .db 0x00
    .db 0x01
    .db 0x70
    .db 0x00
    .dh 0x0000
    .dh 0x0000
    .dw 0x7FFF7FFF
;;;;;;;;;;;;;;;;;
; Expand entities
.org 0x021D748C
    b @ExtendEntityInfo

.org 0x021D7604
    b @ExtendEntityInfo2

.org 0x021D747C ; Don't get rid of the high stuff
    .db 0xBC, 0x30, 0xF2 ;ldrh r3, [r2, #0x0C]!

.org 0x021D7770 ; Don't get rid of the high stuff
    .db 0xBC, 0x30, 0xF2, 0xE1;ldrh r3, [r2, #0x0C]!

.org 0x021D784C ; Don't get rid of the high stuff
    .db 0xBC, 0x00, 0xF7, 0xE1;ldrh r3, [r2, #0x0C]!

.org 0x021D7668 ; Don't get rid of the high stuff
    .db 0xBC, 0x00, 0xF5, 0xE1;ldrh r3, [r2, #0x0C]!

.org 0x021D75F8
    ldrh r1, [r9, r0]

.org 0x021BAA5C
    b @ChapelButton_IgnoreStateA

.org 0x021BAB80
    bl @ChapelButton_SwapFlag

.org 0x0219EF3C
    b @TowerFloorLoadNewFlag

.org 0x021A9B2C
    bl @SealDoor_SaveSeal

.org 0x021AA244
    bl @DisplayTextPerSeal
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021BA1DC
    bl @HammerShop_SkipMusic

.org 0x021BA1B8
    bl @HammerShop_Spawn

.org 0x021B9F20
    bl @HammerShop_SceneSkip

.org 0x021BA3C0
    bl @HammerShop_Dialogue

.org 0x021BA450 ; Watched dialogue
    bl @HammerShop_SkipShopMenu

.org 0x021BA99C ; Skip scene
    bl @HammerShop_SkipShopMenu

.org 0x021B9EFC
    b @HammerShop_CheckConditions

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

.org 0x021AF1B4
    b @CheckGoalCon_Menace

.org 0x0219E6FC
    b @CheckGoalCon_Mine

.org 0x021CEBEC
    b @CheckGoalCon_Garden

.org 0x021CEBE0
    mov r1, 0x14 ; Change the garden flag to menace's event flag so it always goes off

.org 0x021D43BC ; Set the flag back to off during the bad ending
    bic r2, r2, 0x100000

.org 0x021CEB54
    bl @ResetGardenFlags

.org 0x021CBEB8
    bl @ResetMineFlags ; Watched scene ver

.org 0x021CBF38
    bl @ResetMineFlags ;Skipped ver

.org 0x02230310  ; Goal text ptrs
    .dw 0x02223B4F
    .dw 0x02223D4F
    .dw 0x02223F4F
;;;;;;;;;;;;;;;;;;;;;;;
; Goal Conditionals
.org 0x02227127
    .db 0x01, 0xFF, 0x0FF ;FOR TESTING ONLY

.org 0x02227137
    .db 0x01, 0xFF, 0x0FF

.org 0x02227147
    .db 0x01, 0xFF, 0x0FF

    


;overlay 9 0
.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;BOSS FLAGS GO HERE
.open "ftc/overlay9_23", 0x022FF9C0
    .org 0x02300834
        bl @SetFlag_Balore

    .org 0x022FFBA8
        bl @CheckFlag_Balore

    .org 0x022FFD44
        b @BaloreFacePlayer

    .org 0x02300808 ; Prevent Balore from spawning ice blocks
        nop

.close

.open "ftc/overlay9_1", 0x02230A00
    .org 0x0225B5B8
        bl @SetFlag_Dario

    .org 0x0225A69C
        bl @CheckFlag_Dario

    .org 0x0225B318
        bl @FixDario_MirrorFlag

    .org 0x02243FC8
        bl @SetFlag_Aguni

    .org 0x02243C24
        bl @CheckFlag_Aguni

    .org 0x02244680
        nop ; Sets the flag twice?

    .org 0x0225A714
        bl @FixDarioMusic

    .org 0x02243C98
        bl @InitializeEnemyAndOverridePlayBossMusicForAguni

    .org 0x0225A9E0
        b @ThroneBoss_HideAguniSpawn
.close

.open "ftc/overlay9_25", 0x022FF9C0
    .org 0x022FFDC4
        bl @SetFlag_PuppetMaster

    .org 0x022FFA10
        bl @CheckFlag_PuppetMaster

    .org 0x022FFF48
        nop ; Sets the flag twice?
.close

.open "ftc/overlay9_26", 0x022FF9C0
    .org 0x022FFD0C
        bl @SetFlag_Rahab

    .org 0x022FF9F4
        bl @CheckFlag_Rahab

    .org 0x022FFE74
        nop; Sets the flag twice
.close

.open "ftc/overlay9_29", 0x022FF9C0
    .org 0x02300CE0
        bl @SetFlag_Malphas

    .org 0x022FF9DC
        bl @CheckFlag_Malphas
.close

.open "ftc/overlay9_30", 0x022FF9C0
    .org 0x02300BB8
        b @SetFlag_FlyingArmor

    .org 0x022FF9DC
        bl @CheckFlag_FlyingArmor

    .org 0x02300B28
        mov r1, 1 ; Make this not copied from r0

    .org 0x02300CE0
        mov r4, 0x180 ; Flying Armor's cutscene radius- same thing as Death

    ;.org 0x022FFA50
        ;bl @InitializeEnemyAndOverridePlayBossMusicForFlyingArmor
.close

.open "ftc/overlay9_33", 0x022FF9C0
    .org 0x02301558
        bl @SetFlag_Zephyr

    .org 0x022FF9DC
        bl @CheckFlag_Zephyr

    .org 0x022FFA80
    bl @InitializeEnemyAndOverridePlayBossMusicForZephyr
.close

.open "ftc/overlay9_34", 0x022FF9C0
    .org 0x02302388
        bl @SetFlag_Death

    .org 0x022FF9DC
        bl @CheckFlag_Death

    .org 0x0230282C
        mov r6, 0x180 ; Update Death's area detection

    .org 0x02302838
        mvn r2, 0x180
.close

.open "ftc/overlay9_35", 0x022FF9C0
    .org 0x02305728
        bl @SetFlag_Paranoia

    .org 0x02305B1C
        bl @CheckFlag_Paranoia
.close

.open "ftc/overlay9_36", 0x022FF9C0
    .org 0x022FFFE0
        bl @SetFlag_Gergoth

    .org 0x022FF9DC
        bl @CheckFlag_Gergoth

    .org 0x022FFF1C
        nop ; Gergoth sets the flag again here

    .org 0x02300E74
        bl @GergothBreakTowerFlag

    .org 0x022FFAF0 ; Code in Gergoth's initialization that normally floors him in different ways depending on his var A.
    ; First we simplify the flooring code (to make room for new code) by always doing the same thing instead of having 4 different possibilities for 4 different var As.
    mov r0, 0B0000h
    str r0, [r5, 30h] ; Set Gergoth's Y pos to 0xB0.
    
    ldr r0, =020CA95Ch
    ldr r0, [r0] ; Load player's X pos.
    cmp r0, 80000h ; Check if player came in on the left half of the room.
    movlt r0, 0C0000h
    strlt r0, [r5, 2Ch] ; Move Gergoth's X pos to 0xC0, close to the right wall.
    b 022FFB48h
    .pool
.close

.open "ftc/overlay9_37", 0x022FF9C0
    .org 0x022FFF38
        bl @SetFlag_BatCompany

    .org 0x022FF9E0
        bl @CheckFlag_BatCompany
.close

.open "ftc/overlay9_39", 0x022FF9C0
    .org 0x02300364
        bl @SetFlag_Abaddon

    .org 0x022FF9DC
        bl @CheckFlag_Abaddon
.close

.open "ftc/overlay9_40", 0x022FF9C0
    .org 0x02300D0C
        bl @SetFlag_Dimitrii

    .org 0x022FF9E0
        bl @CheckFlag_Dimitrii

    .org 0x022FFA54
        bl @FixDimitriiMusic
.close
    

.open "ftc/overlay9_41", @Overlay41Start

.org @FreeSpace
.area 0xC000 ; Maximum overlay space, failsafe if too big
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    @SoulTypeTable:
 ; Table used to override soul gets. This is used to define ANY item a Soul could give you.
    .dh 0x500
    .dh 0x501
    .dh 0x502
    .dh 0x503
    .dh 0x504
    .dh 0x505
    .dh 0x506
    .dh 0x507
    .dh 0x508
    .dh 0x509
    .dh 0x50a
    .dh 0x50b
    .dh 0x50c
    .dh 0x50d
    .dh 0x50e
    .dh 0x50f
    .dh 0x510
    .dh 0x511
    .dh 0x512
    .dh 0x513
    .dh 0x514
    .dh 0x515
    .dh 0x516
    .dh 0x517
    .dh 0x518
    .dh 0x519
    .dh 0x51a
    .dh 0x51b
    .dh 0x51c
    .dh 0x51d
    .dh 0x51e
    .dh 0x51f
    .dh 0x520
    .dh 0x521
    .dh 0x522
    .dh 0x523
    .dh 0x524
    .dh 0x525
    .dh 0x526
    .dh 0x527
    .dh 0x528
    .dh 0x529
    .dh 0x52a
    .dh 0x52b
    .dh 0x52c
    .dh 0x52d
    .dh 0x52e
    .dh 0x52f
    .dh 0x530
    .dh 0x531
    .dh 0x532
    .dh 0x533
    .dh 0x534
    .dh 0x535
    .dh 0x536
    .dh 0x537
    .dh 0x538
    .dh 0x539
    .dh 0x53a
    .dh 0x53b
    .dh 0x53c
    .dh 0x53d
    .dh 0x53e
    .dh 0x53f
    .dh 0x540
    .dh 0x541
    .dh 0x542
    .dh 0x543
    .dh 0x544
    .dh 0x545
    .dh 0x546
    .dh 0x547
    .dh 0x548
    .dh 0x549
    .dh 0x54a
    .dh 0x54b
    .dh 0x54c
    .dh 0x54d
    .dh 0x54e
    .dh 0x54f
    .dh 0x550
    .dh 0x551
    .dh 0x552
    .dh 0x553
    .dh 0x554
    .dh 0x555
    .dh 0x556
    .dh 0x557
    .dh 0x558
    .dh 0x559
    .dh 0x55a
    .dh 0x55b
    .dh 0x55c
    .dh 0x55d
    .dh 0x55e
    .dh 0x55f
    .dh 0x560
    .dh 0x561
    .dh 0x562
    .dh 0x563
    .dh 0x564
    .dh 0x565
    .dh 0x566
    .dh 0x567
    .dh 0x568
    .dh 0x569
    .dh 0x56a
    .dh 0x56b
    .dh 0x56c
    .dh 0x56d
    .dh 0x56e
    .dh 0x56f
    .dh 0x570
    .dh 0x571
    .dh 0x572
    .dh 0x573
    .dh 0x574
    .dh 0x575
    .dh 0x576
    .dh 0x577
    .dh 0x578
    .dh 0x579
    .dh 0x57a
.align 4
;;;;;;;;;;;;;;;;
@OptionFlag_FightMenace:
    .db 0x00

@OptionFlag_Soulsanity:
    .db 0x00 ; TESTING, REMOVE THIS!!!!
.align 4

@OptionFlag_OneScreenMode:
    .db 0x00
@RAMFlag_IsPausedOpenMap:
    .db 0x00

@Option_StartingWarpRoom:
    .dh 0x0001
    
.align 4
;;;;;;;;;;;;;;
@Romname_AP:
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
.align 4

@Fillerspace_fakewarp:
    .fill 0x10

@RAMFlag_CurrentSpawnedSoulColor:
    .db 0xFF
@RAMFlag_APItemColor:
    .db 0x00
.align 4

@AP_VersionChecker:
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
    .db 0x69
;;;;;;;;;;;;;;;
@AP_DiedFromDeathLink:
    .db 0x00
@OptionFlag_DeathLinkEnabled: ; used exclusively by the AP client
    .db 0x00
@OptionFlag_EXPMult:
    .dh 0x0000
@OptionFlag_SoulMult:
    .dh 0x0000
.align 4

@IncludedSouls:
.fill 0x66, 0xFF
;Boss Souls
.db 0x00, 0x01, 0x02, 0x2B, 0x2C, 0x35, 0x36, 0x57, 0x58, 0x74, 0x75, 0x77
.align 4

@OptionFlag_RandomizeSoulWalls:
.db 0x00

@OptionFlag_GateRando:
.db 0x00

@OptionFlag_HardMode:
.db 0x00

@OptionFlag_PassiveSoulEater:
.db 0x00

@ButtonItemTable:
;ID, Type, Color
.db 0x00, 0x00, 0x00, 0x00 ;
.db 0x00, 0x00, 0x00, 0x00 ;
.db 0x00, 0x00, 0x00, 0x00 ;
.db 0x00, 0x00, 0x00, 0x00 ; WizLab West

;;;;;;;;;;;;;;;;;
@BossFlag_FlyingArmor:
.dh 0x0002 ; Flying Armor
@BossFlag_Balore:
.dh 0x0004 ; Balore
@BossFlag_Dimitrii:
.dh 0x0008 ; Dimitrii
@BossFlag_Malphas:
.dh 0x0010 ; Malphas
@BossFlag_Dario:
.dh 0x0020 ; Dario 1
@BossFlag_PuppetMaster:
.dh 0x0040 ; Puppet Master
@BossFlag_Gergoth:
.dh 0x0080 ; Gergoth
@BossFlag_Rahab:
.dh 0x0100 ; Rahab
@BossFlag_Zephyr:
.dh 0x0200 ; Zephyr
@BossFlag_BatCompany:
.dh 0x0400 ; Bat Company
@BossFlag_Aguni:
.dh 0x0800
@BossFlag_Paranoia:
.dh 0x1000
@BossFlag_Death:
.dh 0x2000
@BossFlag_Abaddon:
.dh 0x8000

@GameFlag_ThroneIsShuffled: ; RESET
.db 0x00

.align 4


;EXPANDED TEXT STUFF
@ExpandedTexPointers:
@ItemNames:
.dh @ItemName_LabKeyWest
.dh @ItemName_LabKeyEast
.dh @ItemName_GardenKey
.dh @ItemName_CaveKey

;Descriptions start here
@ItemDescriptions:
.dh @ItemDescription_LabKeyWest
.dh @ItemDescription_LabKeyEast
.dh @ItemDescription_GardenKey
.dh @ItemDescription_CaveKey
@SealDoors:
.dh @SealDoor1
.dh @SealDoor2
.dh @SealDoor3
.dh @SealDoor4
.dh @SealDoor5

@ItemName_LabKeyWest:
.db 0x01, 0x00, 0x37, 0x45, 0x53, 0x54, 0x00, 0x2C, 0x41, 0x42, 0x00, 0x27, 0x41, 0x54, 0x45, 0x00, 0x2B, 0x45, 0x59, 0xEA

@ItemName_LabKeyEast:
.db 0x01, 0x00, 0x25, 0x41, 0x53, 0x54, 0x00, 0x2C, 0x41, 0x42, 0x00, 0x27, 0x41, 0x54, 0x45, 0x00, 0x2B, 0x45, 0x59, 0xEA

@ItemName_GardenKey:
.db 0x01, 0x00, 0x27, 0x41, 0x52, 0x44, 0x45, 0x4E, 0x00, 0x27, 0x41, 0x54, 0x45, 0x00, 0x2B, 0x45, 0x59, 0xEA

@ItemName_CaveKey:
.db 0x01, 0x00, 0x23, 0x41, 0x56, 0x45, 0x52, 0x4E, 0x00, 0x27, 0x41, 0x54, 0x45, 0x00, 0x2B, 0x45, 0x59, 0xEA

;Opens a metal gate in the Wizardry Lab.
@ItemDescription_LabKeyWest:
.db 0x01, 0x00, 0x2F, 0x50, 0x45, 0x4E, 0x53, 0x00, 0x41, 0x00, 0x4D, 0x45, 0x54, 0x41, 0x4C, 0x00, 0x47
.db 0x41, 0x54, 0x45, 0x00, 0x49, 0x4E, 0x00, 0x54, 0x48, 0x45, 0xE6, 0x37, 0x49, 0x5A, 0x41, 0x52, 0x44
.db 0x52, 0x59, 0x00, 0x2C, 0x41, 0x42, 0x0E, 0xEA

;Opens a metal gate in the Wizardry Lab.
@ItemDescription_LabKeyEast:
.db 0x01, 0x00, 0x2F, 0x50, 0x45, 0x4E, 0x53, 0x00, 0x41, 0x00, 0x4D, 0x45, 0x54, 0x41, 0x4C, 0x00, 0x47
.db 0x41, 0x54, 0x45, 0x00, 0x49, 0x4E, 0x00, 0x54, 0x48, 0x45, 0xE6, 0x37, 0x49, 0x5A, 0x41, 0x52, 0x44
.db 0x52, 0x59, 0x00, 0x2C, 0x41, 0x42, 0x0E, 0xEA

;Opens a metal gate in the Garden of Madness.
@ItemDescription_GardenKey:
.db 0x01, 0x00, 0x2F, 0x50, 0x45, 0x4E, 0x53, 0x00, 0x41, 0x00, 0x4D, 0x45, 0x54, 0x41, 0x4C, 0x00, 0x47
.db 0x41, 0x54, 0x45, 0x00, 0x49, 0x4E, 0x00, 0x54, 0x48, 0x45, 0xE6, 0x27, 0x41, 0x52, 0x44, 0x45, 0x4E
.db 0x00, 0x4F, 0x46, 0x00, 0x2D, 0x41, 0x44, 0x4E, 0x45, 0x53, 0x53, 0x0E, 0xEA

;Opens a metal gate in the Subterranean Hell.
@ItemDescription_CaveKey:
.db 0x01, 0x00, 0x2F, 0x50, 0x45, 0x4E, 0x53, 0x00, 0x41, 0x00, 0x4D, 0x45, 0x54, 0x41, 0x4C, 0x00, 0x47
.db 0x41, 0x54, 0x45, 0x00, 0x49, 0x4E, 0x00, 0x54, 0x48, 0x45, 0xE6, 0x33, 0x55, 0x42, 0x54, 0x45, 0x52
.db 0x52, 0x41, 0x4E, 0x45, 0x41, 0x4E, 0x00, 0x28, 0x45, 0x4C, 0x4C, 0x0E, 0xEA

; It is sealed. \n Magic Seal 1 is needed.
@SealDoor1:
.db 0x01, 0x00, 0x29, 0x54, 0x00, 0x49, 0x53, 0x00, 0x53, 0x45, 0x41, 0x4C, 0x45, 0x44, 0x0E, 0xE6,0x2D
.db 0x41, 0x47, 0x49, 0x43, 0x00, 0x33, 0x45, 0x41, 0x4C, 0x00, 0x11, 0x00, 0x49, 0x53, 0x00, 0x4E, 0x45
.db 0x45, 0x44, 0x45, 0x44, 0x0E, 0xEA

@SealDoor2:
.db 0x01, 0x00, 0x29, 0x54, 0x00, 0x49, 0x53, 0x00, 0x53, 0x45, 0x41, 0x4C, 0x45, 0x44, 0x0E, 0xE6,0x2D
.db 0x41, 0x47, 0x49, 0x43, 0x00, 0x33, 0x45, 0x41, 0x4C, 0x00, 0x12, 0x00, 0x49, 0x53, 0x00, 0x4E, 0x45
.db 0x45, 0x44, 0x45, 0x44, 0x0E, 0xEA

@SealDoor3:
.db 0x01, 0x00, 0x29, 0x54, 0x00, 0x49, 0x53, 0x00, 0x53, 0x45, 0x41, 0x4C, 0x45, 0x44, 0x0E, 0xE6,0x2D
.db 0x41, 0x47, 0x49, 0x43, 0x00, 0x33, 0x45, 0x41, 0x4C, 0x00, 0x13, 0x00, 0x49, 0x53, 0x00, 0x4E, 0x45
.db 0x45, 0x44, 0x45, 0x44, 0x0E, 0xEA

@SealDoor4:
.db 0x01, 0x00, 0x29, 0x54, 0x00, 0x49, 0x53, 0x00, 0x53, 0x45, 0x41, 0x4C, 0x45, 0x44, 0x0E, 0xE6,0x2D
.db 0x41, 0x47, 0x49, 0x43, 0x00, 0x33, 0x45, 0x41, 0x4C, 0x00, 0x14, 0x00, 0x49, 0x53, 0x00, 0x4E, 0x45
.db 0x45, 0x44, 0x45, 0x44, 0x0E, 0xEA

@SealDoor5:
.db 0x01, 0x00, 0x29, 0x54, 0x00, 0x49, 0x53, 0x00, 0x53, 0x45, 0x41, 0x4C, 0x45, 0x44, 0x0E, 0xE6,0x2D
.db 0x41, 0x47, 0x49, 0x43, 0x00, 0x33, 0x45, 0x41, 0x4C, 0x00, 0x15, 0x00, 0x49, 0x53, 0x00, 0x4E, 0x45
.db 0x45, 0x44, 0x45, 0x44, 0x0E, 0xEA



@ExtendedItemData:
@ItemData_LabKeyWest:
.dh 0x00CE ; ID
.dh 0x007E ; Icon/Palette
.dw 0 ; Price
.dh 0x0004 ; Item type
.dh 0x0000 ; Var a
.dw 0

@ItemData_LabKeyEast:
.dh 0x00CF ; ID
.dh 0x007E ; Icon/Palette
.dw 0 ; Price
.dh 0x0004 ; Item type
.dh 0x0000
.dw 0

@ItemData_GardenKey:
.dh 0x00D0 ; ID
.dh 0x007E ; Icon/Palette
.dw 0 ; Price
.dh 0x0004 ; Item type
.dh 0x0000
.dw 0

@ItemData_CaveKey:
.dh 0x00D1 ; ID
.dh 0x007E ; Icon/Palette
.dw 0 ; Price
.dh 0x0004 ; Item type
.dh 0x0000
.dw 0

.align 4

;   Convert souls to a Bitfield table to indicate that that soul has been obtained once
@ToggleSoulFlag:
    push r0 ;Backup the ID number
    push r1
    push lr
    push r11-r12
    bl @GetSoulFlagFromID
    ldr r11, =@SoulFlagTable
    mov r12, r0
    ldrb r0, [r11, r0]; The divided soul id is the index
    orr r0, r0, r1
    strb r0, [r11, r12]
    pop r11-r12
    pop lr
    pop r1
    pop r0
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Returns the index and bit to check from the soul table
@GetSoulFlagFromID:
    push lr
    ldr r1, =0x08
    bl 0x02075B28 ; Divide soul id by 8
    ldr r11, = 0x01
    lsl r1, r11, r1
    pop lr
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Get an item from the Server. What this does is take Item Type 0, Item ID 1,
    ;and gives it to the player. Type 5 is souls. AP server items fill these values
@MoneyValues:
.dh 0x0001, 0x000A, 0x0032, 0x0064, 0x01F4, 0x03E8, 0x07D0
.align 4


@GetItemFromServer:
    push lr
    ldr r0, =0x020CAA24
    ldrb r0, [r0, 0]
    cmp r0, #1 ;This usually means we're in text or something
    beq @GetItemFinished
    ldr r0, =0x020C07F0
    ldrb r0, [r0]
    cmp r0, 0
    bne @GetItemFinished ; Don't get items if we're currently in a mini text prompt

    ldr r0, =0x020F6DFC
    ldr r0, [r0, 0]
    and r0, r0, 0xFFFFFFF6 ;Dont check items in events or getting a Seal

    ldr r0, =@ServerItemType ;Get the current item type
    mov r2, r0
    ldrb r0, [r0]
    cmp r0, #0
    beq @GetItemFinished
    add r2, r2, #1
    ldrb r1, [r2] ;R0 = item type, R1 = item ID
    cmp r0, #5
    beq @GetSoul
@GetItem:
    bl @GetItemArbitrary
@CleanupItems:
    ldr r1, =@ServerItemType
    ldr r2, =0x00
    strb r2, [r1]
    b @GetItemFinished
    .pool
@GetSoul:
    bl @GetSoulArbitrary
    b @CleanupItems

@GetItemFinished:
    pop lr
    b 0x020213EC

@GetItemArbitrary:
    push lr
    cmp r0, #1 ;Is this money?
    beq @GetMoneyArbitrary
    cmp r0, #2
    bne @CheckForSeal
    cmp r1, #0x3C
    bgt @GetMagicSeal
    push r0-r1
    cmp r1, #0x39 ;Is a special item
    bgt @SkipGivingSpecialItem
    pop r0-r1
@CheckForSeal:
    push r0-r1
    bl 0x021E7870 ;GiveItem
@SkipGivingSpecialItem:
    pop r0-r1
    bl 0x021E7AB4 ;GetGlobalItemID+1
    ldr r1, =0xF0
    bl 0x0202DE80 ;ShowItemName

    ldr r0, =0x149
@PlaySoundFromItem:
    bl 0x02029BF0 ;PlaySound
    
    pop lr
    bx lr
    .pool
@GetMoneyArbitrary:
    ldr r0, =@MoneyValues
    mov r1, r1, lsl #1 ;Load the amount of money
    ldrh r0, [r0, r1]
    push r0
    bl 0x021E76D4 ;Function to give money
    pop r0
    ldr r1, =0xF0
    bl 0x0202DDC4 ;DisplayMoneyCount
    ldr r0, =0x01B1
    b @PlaySoundFromItem
    .pool
@GetMagicSeal:
    cmp r1, 0x41
    bgt @CheckForSeal
    push r0-r1
    sub r1, r1, 0x3D
    ldr r0, =0x01 
    lsl r0, r0, r1 ;Get the proper bit for the Seal
    ldr r1, =0x020F7254
    ldrb r2, [r1, 0]
    orr r0, r2
    strb r0, [r1, 0]
    pop r0-r1
    b @CheckForSeal
    .pool

@GetSoulArbitrary:
    mov r0, r1
    push lr
    push r0
    cmp r0, #0x74
    blt @GiveNormalSoul
    bl @ActivateAbilitySoul
@GiveNormalSoul:
    ldr r1, =0xF0
    bl 0x0202E184 ;ShowSoulName
    pop r0
    push r0
    bl 0x0221029C ;GetNumSoul
    mov r1, r0
    cmp r0, #9 ;Do we have 9 of this soul?
    beq @SkipSoulInc
    add r1, r0, #1
    @SkipSoulInc:
    pop r0
    bl 0x02210208 ;Get Soul
    ldr r0, =0x30
    bl 0x02029BF0 ;PlaySound
    pop lr
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Filters the high byte out of an item's flag when trying to spawn it.
@FilterItemFlagHigh:
    and r3, r3, 0xFF
    mov r1, 0x01
    cmp r3, 0x01 ; The Mina's talisman check
    beq @SetHammerFlag2
    bx lr
@SetHammerFlag2:
    ;If we're spawning the Mina's Talisman spot, set the flag for shop 2
    ;this is basically the same trigger as vanilla without the cutscene
    push r1-r2
    ldr r1, =0x020F7189
    ldrb r2, [r1]
    orr r2, r2, 0x02
    strb r2, [r1]
    pop r1-r2
    .pool
    bx lr

;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Prevents items from writing the high byte of their flag
@FilterWriteFlagHigh:
    ldr r12,[r0,0x6E]
    and r12, r12, 0xFF
    bx lr

;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Handles things like picking up AP items, and the Soul Can item.
@SpecialItemHandler:
    cmp r0, 0x02 ;We should only check this for consumables
    beq @GiveSpecial
@GiveNormal:
    bl 0x021E7870
    b 0x021E8980
@GiveSpecial:
    cmp r1, 0x3A
    blt @GiveNormal ;Only 3A-3C are Special items.
    cmp r1, 0x3C ; AP items have Color data defined
    beq @GiveSoulCan
    cmp r1, 0xCD
    bgt @GiveNormal
    b @SetAPNameColor ;AP items dont go into the inventory, so we skip adding them
@GiveSoulCan:
    ldrb r1, [r9, 0x026F] ; The high byte of the item's flag is used as the soul ID
    bl @GetSoulArbitrary
    ldr r1, =@SkipNameShowFlag
    ldr r0, =0x1
    ldr r4, =0x00
    strb r0, [r1, 0]

    b 0x021E89EC ;End the item handler
;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Causes the Castle Map 0 item to warp the player to the starting room
@WarpToStart:
    ldrb r2, [r8, 0]
    cmp r2, #0x2B ;Is this Castle Map 0?
    beq @UseWarp
@NormalUse:
    ldrb r2, [r8, 0x08]
    b 0x021EEED8
@UseWarp:
    ldr r1, =0x020F6DFC
    ldr r1, [r1, 0]
    and r1, r1, 0xB7FFFFFF ;Filter out all game state bits except for Paused and No Save
    and r1, r1, 0xCF
    cmp r1, 0x0
    bne @NormalUse
    ldr r1, =0x020F6DF9
    ldrb r1, [r1, 0]
    cmp r1, 0x0
    bne @NormalUse ;Don't use warp while in the mirror world
    push lr
    ldr r0, =0x00
    ldr r1, =0x01
    ldr r3, =0xA0
    ldr r2, =0x0100 ;This is the area/room/position. if i want to change starting room later ill have to edit these
    bl 0x02026AD0 ;Set Warp Dest
    ldr r1, =0x020F6DF4
    ldr r0, =0x6
    strb r0, [r1] 
    ldr r0, =0x0
    strb r0, [r1,1]
    bl 021F64BCh ;Enable controls
    ldr r0, =0x30
    bl 0x02029BF0 ;PlaySound
    pop lr
    b 0x021EF28C
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Overrides the function that gives the player a Soul normally. We interject here so I can call my arbitrary item giving funcs
@GetItemFromSoul:
    push lr
    push r0-r2
    bl @ToggleSoulFlag
    pop r0-r2

    ldr r2, =@SoulTypeTable
    mov r0, r0, lsl # 1
    ldrh r1, [r2, r0] ;Look up the item
    and r0, r1, 0xFF00
    and r1, r1, 0x00FF
    lsr r0, r0, 8
    cmp r0, #0x05
    beq @GetSoulSoul
    bgt @SetSoulColor
@APColorSoulDone:
    bl @GetItemArbitrary
    b @SoulGetFinish
@GetSoulSoul:
    bl @GetSoulArbitrary
@SoulGetFinish:
    pop lr
    b 0x021E96B0

@SetSoulColor:
    ldr r1, =@RAMFlag_APItemColor
    strb r0, [r1]
    ldr r1, =0x3A ; this only runs for AP items
    mov r0, 0x02
    b @APColorSoulDone
    .pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Give the starting weapon + Return Gem
@GiveStartingInventory:
    bl 0x021E78F0 ;Set Item Count
    ldr r0, =@OptionFlag_HardMode
    ldrb r0, [r0]
    ldr r1, =0x020F7259 ; Hard mode address
    strb r0, [r1]

    ldr r0, =0x02
    ldr r1, =0x2B
    bl 0x021E78F0
@ClearAPMemory:
    push r2
    ldr r0, =0x00
    ldr r1, =@SoulFlagTable
@ClearAPLoop:
    str r0, [r1, 0]
    add r1, 4
    add r2, 1
    cmp r2, 9
    bne @ClearAPLoop
    pop r2
    ldr r0, =0x020F7420 ;Starting weapon
    ldrb r1, [r0, 0]
    ldr r0, =0x03
    bl 0x021E78F0
    b 0x021F60B8
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Transfers AP data in and out of saved memory
    ;0x0A001F00 for testing
@LoadAPData:
    push r0-r3
    push lr
    ldr r1, =0x1F00
    mov r0, r0, lsl #5
    add r0, r0, r1
    ldr r1, =@SoulFlagTable
    ldr r2, =0x20
    ldr r3, =0x00
    bl 0x020684E0 ;WriteToSaveData
    pop lr
    pop r0-r3
    b 0x02010C7C
    .pool

@SaveAPData:
    push r0-r3
    push lr
    mov r2, r9, lsl #5
    ldr r0, =0x1F00
    add r0, r0, r2
    ldr r1, =@SoulFlagTable
    ldr r2, = 0x20
    ldr r3, =0x00
    bl 0x02068410
    pop lr
    pop r0-r3
    b 0x2011F3C
    .pool
    

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Activates Ability Souls when getting them
@ActivateAbilitySoul:
    push r0-r2
    sub r0, r0, 0x74 ;if getting an Ability soul, activate it
    ldr r1, = 0x01
    lsl r0, r1, r0 ;Translate the id to a bit
    ldr r1, =0x20F741E
    ldrb r2, [r1, 0]
    orr r0, r0, r2
    strb r0, [r1, 0]
    pop r0-r2
    bx lr
    .pool

    ;Saving data is 0x02068410. r0 = offset, r1 = source, r2 = count. r9 = file number
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@FilterSpecialItemFlagHigh:
    ldr r12,[r1,0x70]
    and r12, r12, 0xFF
    bx lr

@GetItemFromSpecial:
    ldr r12, [r0, 0x70]
    push r0-r1
    push lr
    push r12
    ldrb r1, [r4, 0x0F]
    mov r3, r12
    and r3, r3, 0xFF00
    lsr r3, r3, 0x08
    cmp r3, #5
    beq @GetSpecialSoul
    bgt @GetSpecialAPColor
@SpecialAPColorDone:
    mov r0, r3
    bl @GetItemArbitrary
    b @SpecialCleanup
@GetSpecialSoul:
    bl @GetSoulArbitrary
@SpecialCleanup:
    pop r12
    and r12, r12, 0xFF
    pop lr
    pop r0-r1
    bx lr

    ;For the specials, i dont think i can change the sprite (for now)
    ;Change the item ID in the global Special Item table. This var also acts as the Soul ID.
    ;spawner is at 0x021AF558
    ;It's definitely at 0x021F5A8. this calls LoadSpriteSingleGFX. But how does it work...?
    ;r3 is the Palette Index

;;;;;;;;;;;;;;;;;;;;;;;
@SkipShowName:
    push r0-r1
    ldr r1, =@SkipNameShowFlag
    ldrb r0, [r1, 0]
    cmp r0, #0
    bne @SkipName
    pop r0-r1
    b 0x0202DE80
@SkipName:
    ldr r0, =0x0
    strb r0, [r1, 0]
    pop r0-r1
    b 0x021E8AAC
    .pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Loads AP data from the current file so it can be cleanly copied
@CopyAPData:
    push r0-r4
    push lr
    bl @LoadAPData ;WriteToSaveData
    pop lr
    pop r0-r4
    b 0x020110FC
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Prevents the game from writing map exploration data while out of bounds, which corrupts memory
@PreventPlayerFromCorruptingData:
    tst r7, 0x80000000
    bne @PlayerOutofBounds
    sub r13, r13, 0x04
    b 0x02024D7C
    @PlayerOutofBounds:
    pop r14
    b 0x02022764
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;One-screen mode. Pulls up the Map on bottom screen when Select is pressed.
@OneScreenLowerMapOnBottom:
    push r0
    ands r0, r0, 0x08
    bne @OpenMenu
    b @CheckMap
@OpenMenu:
    pop r0
    b 0x02030018
@CheckMap:
    pop r0
    ands r0, r0, 0x04
    bne @ExitMapSkip
@ExitMap:
    b 0x0203008C
@ExitMapSkip:
    ldr r0, =0x020F6DFC
    ldrb r0, [r0]
    ands r0, r0, 0x01
    bne @ExitMap
    ldr r0, =@OptionFlag_OneScreenMode
    ldrb r0, [r0]
    cmp r0, 0
    beq @ExitMap
@LoadMap:
    ldr r1, =0x1
    ldr r0, =@RAMFlag_IsPausedOpenMap
    strb r1, [r0]
    ldr r0, =0x020D21F0
    ldr r1, =0x0223085C
    str r0, [r1]
    push r4-r8, r14
    sub r13,r13,0x20
    bl 0x021BD074
    b 0x0203008C
    .pool

;0x021BD074
;Skip a state check for opening the map
@MapInit_SkipGroundCheck:
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    beq @_SkipGround
    b 0x021F6588
@_SkipGround:
    bx lr
    .pool

;0x021BD16C
;Skip MOST of the code related to handling warp rooms
@MapInit_SkipActingLikeWarpRoom:
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    beq @_SkipJump
    b 0x021BD608
@_SkipJump:
    b 0x021BD7D4
    .pool

;0x021BD138
;Make the drawn map load the current Map Block position
@MapInit_LoadPlayerCoordinates:
    push r0
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    beq @_LoadPlayer
    pop r0
    b 0x02021714
@_LoadPlayer:
    pop r0
    ldr r0, =0x0210F018
    ldrb r0, [r0]
    ldr r1, =0x0210f014
    ldrb r1, [r1]
    push r2
    ldr r2, =0x0211504C
    ldrb r2, [r2]
    cmp r2, 0x0A
    blt @NotInAbyss
    cmp r2, 0x0B
    bgt @NotInAbyss ;Julius throne room, other maps
    add r0, r0, 0x14 ; Abyss maps use offset positions
    add r1, r1, 0x0A

@NotInAbyss:
    pop r2
    b 0x02021714
    .pool

;Close the map and reset the map opened flag
@MapInit_CloseMapAndReset:
    push r0-r5, r14
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    bne @_SkipMapClose
    mov r0, 0
    mov r1, 0
    bl 0x020073F0
    ldr r1, =0x020F6DFC
    ldrb r0, [r1]
    and r0, r0, 0xFE
    strb r0, [r1]
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldr r1, =0
    strb r1, [r0]
@_SkipMapClose:
    pop r0-r5, r14
    strb r0, [r5, 0x04]
    bx lr
    .pool

;0x021BD080
;Don't zero out the player's animation
@MapInit_ContinueCurAnim:
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    beq @_SkipMapAnim
    b 0x021F68F8
@_SkipMapAnim:
    bx lr
    .pool

;Set R5 to be dummy data, so the "warp room" used by the map doesn't intersect anything
;I found that warp room data intersects boss doors by default. there may be more.
@MapInit_AllocateWarpSpaceSelect:
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    bne @_WarpRoomSel
    ldr r5, =@Fillerspace_fakewarp
    mov r0, 0
@_WarpRoomSel:
    ldrb r0, [r5, 0x04]
    bx lr
    .pool

;Prevent the player from closing the map by touching something
@MapInit_DisableTouchControls:
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    bne @_WarpRoomTouch
    mov r0, 0
    bx lr
@_WarpRoomTouch:
    ldrb r0, [r11, 0x01]
    cmp r0, 0
    bx lr
    .pool

;0x021BC8E4
;Close the map when B or Select is pressed
@MapInit_CloseWithBorSel:
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    beq @_WarpRoomClose
    ands r0, r1, 0x02
    bx lr
@_WarpRoomClose:
    ldr r0, =0x020CA38C
    ldr r5, =@Fillerspace_fakewarp
    ldrb r0, [r0]
    and r0, 0x06
    cmp r0, 0
    bx lr
    .pool

;Don't show warp rooms as unlocked when opening the map
@MapInit_SkipWarpRoomCheck:
    push r0
    ldr r0, =@RAMFlag_IsPausedOpenMap
    ldrb r0, [r0]
    cmp r0, 1
    beq @_SkipWarpRooms
    pop r0
    ldr r0, [r0, 0x09C8]
    bx lr
@_SkipWarpRooms:
    pop r0
    mov r0, 0
    bx lr
    .pool

;If using one-screen mode, we don't want Map on the top
@OneScreen_DisableScreenSwap:
    ldr r0, =@OptionFlag_OneScreenMode
    ldrb r0, [r0]
    cmp r0, 0
    beq 0x0203BE9C
    bx lr
    .pool

;If one-screen mode, set the initial screen to Enemy Data
@OneScreen_SetFirstScreenEnemy:
    ldr r0, =@OptionFlag_OneScreenMode
    ldrb r0, [r0]
    ldr r1, =0x020F7251
    strb r0, [r1]
    b 0x0203B998
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@SetSoulPerPickup:
    cmp r7, 0x3C
    beq @Setpickup_SoulID
@SetNormalPickup:
    mov r5, 0xFF
@ExitSoulPickup:
    push r0
    ldr r0, =@RAMFlag_CurrentSpawnedSoulColor
    strb r5, [r0]
    pop r0
    cmp r8, 0xFF
    mov r5, 0
    bx lr
@Setpickup_SoulID:
    cmp r8, 0x02
    bne @SetNormalPickup
    ldrb r5, [r0, 0x6F]
    b @ExitSoulPickup
    .pool

@SetCanColor_Page:
    push r1
    ldr r1, =@RAMFlag_CurrentSpawnedSoulColor
    ldrb r1, [r1]
    cmp r1, 0xFF
    beq @SkipCanColor_Page
    cmp r1, 0x34
    bgt @SkipCanColor_Page
    mov r0, 0x7F
@SkipCanColor_Page:
    pop r1
    mov r0, r0, asr 0x06
    bx lr
    .pool

@SetCanColor_Item:
    ldr r0, [r0]
    push r0
    push r1
    ldr r1, =@RAMFlag_CurrentSpawnedSoulColor
    ldrb r0, [r1]
    cmp r0, 0xFF
    beq @SkipCanColorItem
    mov r2, 0x7F ;Bullet Soul
    cmp r0, 0x35
    blt @SkipCanColorItem
    mov r2, 0x82 ;Guardian Soul
    cmp r0, 0x59
    blt @SkipCanColorItem
    mov r2, 0x80 ;Enchant Soul
    cmp r0, 0x74
    blt @SkipCanColorItem
    mov r2, 0x81 ;Ability Soul
@SkipCanColorItem:
    mov r0, 0xFF
    strb r0, [r1]
    pop r1
    pop r0
    bx lr
    .pool

;;;;;;;;;;;;;;;;
;Initialize the AP color variable
@SetAPNameColor:
    ldrb r1, [r9, 0x026F]
    ldr r0, =@RAMFlag_APItemColor
    strb r1, [r0]
    b 0x021E8988
    .pool

@LoadAPNameColor:
    push r1
    ldr r1, =@RAMFlag_APItemColor
    ldrb r0, [r1]
    cmp r0, 0
    beq @EndAPName
    mov r6, r0
    mov r0, 0
    strb r0, [r1] ;Get rid of the color flag afterwards
@EndAPName:
    pop r1
    b 0x0202DFF4
    .pool

@GetSpecialAPColor:
    ldr r1, =@RAMFlag_APItemColor
    strb r3, [r1]
    mov r1, 0x3A
    mov r3, 0x02
    b @SpecialAPColorDone
    .pool

;;;;;;;;;;;;;;;;;
;Change the starting unlocked warp room
@InitStartingWarpRoom:
    push r2
    ldr r2, =@Option_StartingWarpRoom
    ldrh r2, [r2]
    orr r3, r3, r2
    pop r2
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Deathlink
@CheckIfDeathReceived:
    push r0
    ldr r0, =@AP_DiedFromDeathLink
    ldrb r0, [r0]
    cmp r0, 0
    bne @RemoteKillPlayer
@CantKillPlayer:
    pop r0
    ldr r0,[r0, 0x0BAC]
    bx lr
@RemoteKillPlayer:
    ldr r0, =0x020F6DFC
    ldr r0, [r0]
    ands r0, r0, 0x000000C1 ; Control + Dead
    bne @CantKillPlayer
    ldr r0, =0x020C07F0 ; Don't kill the player during a text prompt
    ldrb r0, [r0]

    ldr r0, =@AP_DiedFromDeathLink
    mov r1, 0
    strb r1, [r0] ; Reset the value
    ldr r0, =0x020C07F1 ; CanPauseGame
    strb r1, [r0]
    pop r0
    ldr r1, =0x020F738E
    mov r0, 6
    strb r0, [r1] ;Register that we took a hit
    ldr r1, =0x20F7410
    mov r0, 0
    strh r0, [r1] ;Zero out the player's health
    mov r0, 0
    bx lr
    .pool

@SkipSoulPopupIfDead:
    ; Prevent the game from playing a soul popup and interrupting the death sequence
    ldr r0, =0x020F6DFC
    ldrb r0, [r0]
    ands r0, r0, 0x40 ;Is the player dead
    mov r0, r1, lsl 0x1C
    bne @SkipPopup
    b 0x0202C640
@SkipPopup:
    b 0x0202C724
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; Replace the check for soul count in the Bestiary with the soul flag table, if soulsanity
    ; 0x0220ED90
@Soulsanity_SoulCheck:
    push r0, r1
    ldr r0, =@OptionFlag_Soulsanity
    ldrb r0, [r0]
    cmp r0, 0
    beq @GetSoulCount
    pop r0, r1
    push r1, r2, r3
    ldr r1, =@IncludedSouls
    mov r2, 0
@SoulSanity_CheckIfIncluded:
    ldrb r3, [r1, r2] ; Check the included table
    cmp r0, r3
    beq @Soulsanity_IncludeSoul
    cmp r2, 0x72 ; We've exhausted the entire table
    beq @Soulsanity_SoulDisabled
    add r2, r2, 1
    b @SoulSanity_CheckIfIncluded
@Soulsanity_IncludeSoul:
    push r11, lr
    bl @CheckIfSoulChecked
    pop r11, lr
    pop r1, r2, r3
    beq @Bestiary_NoSoul
    mov r0, 1
    bx lr
@Bestiary_NoSoul:
    mov r0, 0
    bx lr
@GetSoulCount:
    pop r0, r1
    b 0x0221029C
@Soulsanity_SoulDisabled:
    pop r1, r2, r3
    mov r0, 0x0F
    bx lr
.pool

@CheckIfSoulChecked:
    push lr
    bl @GetSoulFlagFromID
    pop lr
    ldr r2, =@SoulFlagTable
    ldrb r0, [r2, r0]
    ands r0, r0, r1
    bx lr
    .pool

@EnemySouls_TopScreen:
    push r0, r1
    ldr r1, =@OptionFlag_Soulsanity
    ldrb r0, [r1]
    cmp r0, 0
    beq @EnemySouls_Normal
    pop r0, r1
    bl @Soulsanity_SoulCheck
    cmp r0, 0x0F
    beq 0x203ACA4
    b 0x0203AC6C


@EnemySouls_Normal:
    pop r0,r1
    cmp r0, 0
    b 0x0203AC64
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Grant items based on pressing the button
    ;0x021A748C
@GateSanity_CheckGateButtons:
    ldr r0, =@OptionFlag_GateRando
    ldrb r0,[r0] ; Check the flag for gates being checks
    cmp r0, 0
    add r0, r4, 0x200
    beq 0x021A7490 ; If it's off, go back to the Gate Open code
    ldrb r1, [r0, 0x6E] ; We use the Gate Type as the item
;Set the Obtained flag here
    push r1
    ldr r0, =@GateKeys
    ldr r2, = 0x01
    lsl r2, r2, r1
    ldrb r1, [r0] ; The chapel key is different and manually checks the next byte
    orr r2, r2, r1
    strb r2, [r0]
    pop r1
;Give the item here
    lsl r1, r1, 2
    ldr r0, =@ButtonItemTable
    add r0, r0, r1
    ldrb r2, [r0, 2] ; Load the item color
    ldrb r1, [r0, 1] ;Load the ID
    ldrb r0, [r0] ; Load the item Type
    push lr
    bl @GiveItem_Any
    pop lr
    b 0x021A7584
    .pool


@GateSanity_CheckIfPressed:
    ;0x021A737C
    ldr r0, = @OptionFlag_GateRando
    ldrb r0, [r0]
    cmp r0, 0
    beq @Button_CheckNormal
    add r0, r5, 0x200
    ldrb r1, [r0, 0x6E] ; make sure we get the type of gate
    ldr r0, =@GateKeys
    ldr r2, = 0x01
    lsl r2, r2, r1 ; Convert the gate type into a Bit
    ldrb r1, [r0]
    ands r0, r1, r2
    bx lr
@Button_CheckNormal:
    ldrb r0, [r5, 0x0E]
    bx lr
    .pool

;@GateSanity_FlagChecker:
    ;Can i do the 0x6E thing on the Chapel. check that.

;Make a subroutine for Gate stuff?


;;;;;;;;;;;;;;;;;
;Grants an item
@GiveItem_Any:
    push lr
    cmp r0, 5 ; Soul
    beq @GiveAny_soul
    push r1
    ldr r1, =@RAMFlag_APItemColor
    strb r2, [r1]
    pop r1
    bl @GetItemArbitrary
    pop lr
    bx lr

@GiveAny_Soul:
    mov r0, r1
    bl @GetSoulArbitrary
    pop lr
    bx lr
    .pool
;;;;;;;;;;;;;;;;;;
; Checks items above 42 differently
;0x021EE784
@ExtendedInv_SkipCountingItems:
    cmp r6, 0x42
    blt @CountItem_Normal
    sub r3, r6, 0x42 ; Bring down to their new IDs
    mov r0, 0x10
    lsl r3, r0, r3

    ldr r0, =@GateKeys ; TODO. Increase for Door Keys
    ldrb r0, [r0] ; Load the high byte too probably
    ands r0, r0, r3
    beq @ExpandedInv_End
    mov r0, 1
@ExpandedInv_End:
    bx lr
@CountItem_Normal:
    push lr
    bl 0x021E79CC
    pop lr
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;
    ;Shifts item IDs if over 0x42
    ;021EE7AC
@LoadExtendedItemNames:
    cmp r6, 0x42
    blt @ExtendedName_End
    sub r2, r6, 0x42 ; Convert, etc
    add r2, r2, 0x0500 ;Extended Text IDs
    add r2, r2, 0x0B
    ;mov r6, r2
@ExtendedName_End:
    push lr
    bl 0x021EE620
    pop lr
    bx lr
    .pool
;;;;;;;;;;;;;;;;;;;;;
    ;0x02042834
    ; Loads text IDs above 0x050A by repointing them
@RepointExtendedTexIDs:
    push r3
    sub r3, r3, 0x500
    cmp r3, 0x0B
    blt @GetNormalText
    sub r3, r3, 0x0B
    ldr r0, =@ExpandedTexPointers
    lsl r3, r3, 1
    ldrh r3, [r0, r3]
    ldr r0, =0x02300000
    add r0, r0, r3
    pop r3
    b 0x02042838
@GetNormalText:
    pop r3
    ldr r0, [r0, r3, lsl 0x02]
    b 0x02042838
    .pool
;;;;;;;;;;;;;;;;;;
;0x021EE574, draws names when hovering over them
@DrawExtendedNames_MenuHover:
    cmp r2, 0xCE
    blt @MenuHover_NormalName
    sub r2, r2, 0xCE
    add r2, r2, 0x0500
    add r2, r2, 0x0B
    bx lr
@MenuHover_NormalName:
    add r2, r2, 0x0C
    bx lr
.pool

;;;;;;;;;;;;;;;;
    ; 0x021EE794 Set extended item ids to 0xCE and above when handling menus
@ExtendedInv_ShiftIDs:
    push r6
    cmp r6, 0x42
    blt @InvShiftNormal
    sub r6, r6, 0x42
    add r6, r6, 0xCE
@InvShiftNormal:
    strb r6, [r7]
    pop r6
    bx lr
.pool
;;;;;;;;;;;;;;;;
    ;0x021E7A88
    ; Loads extended pointer for extended IDs
@ExtendedInv_PointToData:
    push lr
    bl @GetExtendedItemPointer
    pop lr
    b 0x021E7A8C

@GetExtendedItemPointer:
    cmp r1, 0xCE
    blt @InvPoint_Normal
    ldr r0, =@ExtendedItemData
    sub r1, r1, 0xCE
    bx lr
@InvPoint_Normal:
    ldr r0, =0x0209BA68
    bx lr
.pool
;;;;;;;;;;;;;;;;;;;;;;;;
    ; 0x021E787C Set the Expanded Item bits if necessary
@GiveExpandedItems:
    mov r4, r1
    cmp r1, 0xCE
    blt @GiveNormalItem
    sub r1, r1, 0xCE
    cmp r1, 3
    bgt @GiveDoorKeys
    mov r0, 0x10
    lsl r1, r0, r1 ; Shift to get the bit
    ldr r0, =@GateKeys
    push r2
    ldrb r2, [r0]
    orr r1, r2, r1
    pop r2
    strb r1, [r0]
    b 0x021E78B0
@GiveDoorKeys:
    mov r0, 1
    lsl r1, r0, r1
    ldr r0, =@DoorKeys
    str r1, [r0]
    b 0x021E78B0
@GiveNormalItem:
    b 0x021E7880
.pool

;;;;;;;;;;;;;;;;;;;;
    ;Displays expanded item names
    ;0x0202DF6C
@ShowItem_ExpandPointers:
    push r2
    sub r2, r2, 0x500
    cmp r2, 0x0B
    blt @GetNormalTextDisplay
    sub r2, r2, 0x0B
    ldr r0, =@ExpandedTexPointers
    lsl r2, r2, 1
    ldrh r2, [r0, r2]
    ldr r0, =0x02300000
    add r0, r0, r2
    pop r2
    b 0x0202DF70
@GetNormalTextDisplay:
    pop r2
    ldr r0, [r0, r2, lsl 0x02]
    b 0x0202DF70
.pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@DisplayExpandedItemNames:
    cmp r8, 0xCE
    blt @DisplayExpanded_Normal
    sub r2, r8, 0xCE
    add r2, r2, 0x0500 ;Extended Text IDs
    add r2, r2, 0x0B
    mov r8, 0
@DisplayExpanded_Normal:
    add r2, r8, r2
    b 0x0202DF6C
.pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;0x0204263C
    ; Expands pointers for menu text
@ExpandTextPointers_Menus:
    push r1
    sub r1, r1, 0x500
    cmp r1, 0x0B
    blt @NormalDescription
    pop r8 ; get rid of the stored r1
    sub r1, r1, 0x0B
    ldr r0, =@ExpandedTexPointers
    lsl r1, r1, 1
    ldrh r1, [r0, r1]
    ldr r0, =0x02300000
    add r0, r0, r1
    b 0x02042640
@NormalDescription:
    pop r1
    ldr r0, [r0, r1, lsl 2]
    b 0x02042640
.pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;0x021EE5D8
    ; Loads description numbers for expanded items
@LoadExpandedDescriptions:
    @@DescriptionsStart equ ((@ItemDescriptions - @ExpandedTexPointers) / 2)
    cmp r3, 0xCE ; is this an expanded item
    blt @@NormalDesc
    ldr r4, =0x050B
    sub r3, r3, 0xCE
    add r4, r4, @@DescriptionsStart
    add r4, r4, r3
    bx lr
@@NormalDesc:
    add r4, r3, 0xDA
    bx lr 
.pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;0x021E7B40
    ; Changes expanded items to type 2 so they don't cause invalid writes
@FixExpandedItemTypes:
    cmp r0, 0xCE ; Expanded item ids
    blt @@NormalItem
    mov r1, 2
    b 0x021E7B60
@@NormalItem:
    cmp r0, 0x42
    b 0x021E7B44
.pool
;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;0x021A73FC
@OpenGatesWithKeys:
    push r0-r3
    push r1
    add r0, r4, 0x0200 ; Gate data pointer
    add r0, r0, 0x6E ; Gate type
    ldrb r2, [r0, 2] ; Grab the flag of the gate
    ldrb r0, [r0] ; Grab the Type of the gate.
    sub r2, r2, 0x28

    mov r3, 1
    lsl r1, r3, r2 ; Get the bit of the gate
    ldr r3, =0x020F7185
    ldrb r3, [r3] ; Event flags for the gates being opened
    ands r3, r3, r1
    bne @@Gate_Nocollision ; If this gate is already open, skip the rest entirely


    ldr r2, [r5, 0x2C] ; Load the Button's position
    ldr r3, = 0x40000 ; Distance from the button to the gate
    cmp r0, 2
    bne @@NormalGate
    lsr r3, r3, 1 ; Gate 2 specifically has a halved position
@@NormalGate:
    cmp r0, 1
    bgt @@LeftButton
@@RightButton:
    rsb r3, r3, 0 ; If the button is on the right, invert the distance
@@LeftButton:
    add r2, r2, r3 ; Add button position + distance to get the gate's position

    sub r1, r2, 0x15000
    cmp r0, 0
    bne @@SkipLeftButtonExtraGate
    sub r1, r1, 0x10000
@@SkipLeftButtonExtraGate:
    cmp r12, r1
    blt @@Gate_NoCollision
    add r1, r2, 0x17000
    cmp r0, 3
    bne @@SkipRightButtonExtraGate
    add r1, r1, 0x17000
@@SkipRightButtonExtraGate:
    cmp r12, r1
    bgt @@Gate_Nocollision
    ; We have collided with the gate's X-position
    pop r1
    ldr r3, [r1, 0x30] ; Soma Y-pos
    ldr r1, [r5, 0x30] ; Button Y-pos
    sub r1, r1, 0x20000
    cmp r3, r1
    blt @@Gate_NoVertColl
    ; This should run when we are NOT above the gate
    add r0, r4, 0x0200
    add r0, r0, 0x70
    ldrb r0, [r0] ; Gate type
    sub r0, r0, 0x28
    mov r1, 0x10
    lsl r0, r1, r0 ; Get the bit for the key
    ldr r1, =@GateKeys
    ldrb r1, [r1]
    ands r1, r1, r0
    beq @@Gate_NoVertColl 
    ;If we have the key, unlock the gate!
    pop r0-r3
    add r0, r4, 0x0200
    b 0x021A7490
@@Gate_Nocollision:
    pop r1
@@Gate_NoVertColl:
    pop r0-r3
    ldr r3, [r1, 0x30]
    cmp r2, 0
    b 0x021A7400
    .pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;0x021C3AA0
@CheckPassiveSoulEaterRing:
    push r2,r3
    ldr r2, =@OptionFlag_PassiveSoulEater
    ldrb r3, [r2]
    cmp r3, 0
    beq @NormalSoulRing
    ldr r2, =0x020F7224
    ldrb r2, [r2]
    ands r2, r2, 0x0F
    beq @NoulEaterRing
    mov r2, 0
    cmp r2, 0
    pop r2,r3
    bx lr
@NoulEaterRing:
    cmp r2, 0xFF
    pop r2,r3
    bx lr

@NormalSoulRing:
    pop r2,r3
    cmp r2, 0x38
    bx lr
.pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@SetFlag_FlyingArmor:
    push r1
    ldr r1, = @BossFlag_FlyingArmor
    ldrh r1, [r1]
    orr r14, r14, r1
    pop r1
    b 0x02300BBC
@SetFlag_Balore:
    push r1
    ldr r1, = @BossFlag_Balore
    ldrh r1, [r1]
    orr r8, r8, r1
    pop r1
    bx lr

@SetFlag_Dimitrii:
    push r1
    push r0-r3,lr
    ldr r0, =@GameFlag_ThroneIsShuffled
    ldrb r0, [r0] ; is boss shuffle on
    cmp r0, 0
    beq @@End
    bl 0x020298A0 ; Mute the music when dimitrii dies
@@End:
    pop r0-r3,lr
    ldr r1, = @BossFlag_Dimitrii
    ldrh r1, [r1]
    orr r2, r2, r1
    pop r1
    bx lr

@SetFlag_Malphas:
    push r1
    ldr r1, = @BossFlag_Malphas
    ldrh r1, [r1]
    orr r4, r4, r1
    pop r1
    bx lr

@SetFlag_Dario:
    push r0-r3, lr
    ldr r0, =@GameFlag_ThroneIsShuffled
    ldrb r0, [r0] ; is boss shuffle on
    cmp r0, 0
    beq @@End
    bl 0x020298A0 ; Mute the music when dimitrii dies
@@End:
    pop r0-r3, lr
    ldr r2, = @BossFlag_Dario
    ldrh r2, [r2]
    orr r1, r1, r2
    bx lr

@SetFlag_PuppetMaster:
    push r2
    ldr r2, = @BossFlag_PuppetMaster
    ldrh r2, [r2]
    orr r1, r1, r2
    pop r2
    bx lr

@SetFlag_Gergoth:
    push r2
    ldr r2, = @BossFlag_Gergoth
    ldrh r2, [r2]
    orr r6, r6, r2
    pop r2
    bx lr

@SetFlag_Rahab:
    push r2
    ldr r2, = @BossFlag_Rahab
    ldrh r2, [r2]
    orr r1, r1, r2
    pop r2
    bx lr

@SetFlag_Zephyr:
    push r1
    ldr r1, = @BossFlag_Zephyr
    ldrh r1, [r1]
    orr r2, r2, r1
    pop r1
    bx lr

@SetFlag_BatCompany:
    push r1
    ldr r1, = @BossFlag_BatCompany
    ldrh r1, [r1]
    orr r12, r12, r1
    pop r1
    bx lr

@SetFlag_Paranoia:
    push r1
    ldr r1, = @BossFlag_Paranoia
    ldrh r1, [r1]
    orr r5, r5, r1
    pop r1
    bx lr

@SetFlag_Aguni:
    push r0-r3,lr
    ldr r0, =@GameFlag_ThroneIsShuffled
    ldrb r0, [r0] ; is boss shuffle on
    cmp r0, 0
    beq @@End
    bl 0x020298A0 ; Mute the music when aguni dies
@@End:
    pop r0-r3,lr
    push r2
    ldr r2, = @BossFlag_Aguni
    ldrh r2, [r2]
    orr r1, r1, r2
    pop r2
    bx lr

@SetFlag_Death:
    push r2
    ldr r2, = @BossFlag_Death
    ldrh r2, [r2]
    orr r7, r7, r2
    pop r2
    bx lr

@SetFlag_Abaddon:
    push r2
    ldr r2, = @BossFlag_Abaddon
    ldrh r2, [r2]
    orr r3, r3, r2
    pop r2
    bx lr
;;;;;;;;;;;;;;;;;;;
@CheckFlag_FlyingArmor:
    push r2
    ldr r2, = @BossFlag_FlyingArmor
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Balore:
    push r2
    ldr r2, = @BossFlag_Balore
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Dimitrii:
    push r2
    ldr r2, = @BossFlag_Dimitrii
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Dario:
    push r2
    add r2, r5, 0x270
    ldrb r2, [r2] ;varB
    cmp r2, 1
    beq @@FlagNormal
    ldr r2, = @BossFlag_Dario
    ldrh r2, [r2]
    ands r0, r0, r2
    pop r2
    bx lr
@@FlagNormal:
    pop r2
    ands r0,r0,r2
    bx lr ; Check Dario's normal flag if fighting Dario2

@CheckFlag_Malphas:
    push r2
    ldr r2, = @BossFlag_Malphas
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_PuppetMaster:
    push r2
    ldr r2, = @BossFlag_PuppetMaster
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Gergoth:
    push r2
    ldr r2, = @BossFlag_Gergoth
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Zephyr:
    push r2
    ldr r2, = @BossFlag_Zephyr
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Rahab:
    push r2
    ldr r2, = @BossFlag_Rahab
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_BatCompany:
    push r2
    ldr r2, = @BossFlag_BatCompany
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Aguni:
    push r2
    ldr r2, = @BossFlag_Aguni
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Paranoia:
    push r2
    ldrb r2, [r2, 0x6E]
    cmp r2, 2
    pop r2
    bne @@ParanoiaManual ; We want to check the normal flag if it's mini-paranoia
    ldr r2, = @BossFlag_Paranoia
    ldrh r2, [r2]
@@End:
    ands r0, r0, r2
    bx lr
@@ParanoiaManual:
    ands r0, r0, 0x1000
    bx lr

@CheckFlag_Death:
    push r2
    ldr r2, = @BossFlag_Death
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr

@CheckFlag_Abaddon:
    push r2
    ldr r2, = @BossFlag_Abaddon
    ldrh r2, [r2]
    ands r1, r1, r2
    pop r2
    bx lr
.pool

;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;
    ; Sets Balore to always face the player depending on entrance direction
@BaloreFacePlayer:
  mov r0, r5
  bl 021C3278h ; GetPlayerXPos
  cmp r0, 80000h ; X pos 0x80, halfway through the leftmost screen
  bge @BaloreFaceRight
@BaloreFaceLeft:
  mov r0, 0h ; Var A
  mov r1, 0F0000h ; X pos
  str r1, [r5, 2Ch]
  b @BaloreFacePlayerEnd
@BaloreFaceRight:
  mov r0, 1h ; Var A
  ; We don't set X pos here because we assume Balore's X pos was already properly set for facing right.
@BaloreFacePlayerEnd:
  ; Go back to Balore's normal code to set the direction he faces
  ; We make sure r0 has Var A in it - but not Balore's real Var A, just the one to check for the purposes of deciding the direction he faces.
  b 0x022FFD48
.pool
;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;
; Open Dario's boss doors if the flag is set
@DarioEvent_Update:
    push r0,r1
    ldr r0, = @GameFlag_ThroneIsShuffled
    ldrb r0, [r0]
    cmp r0, 0
    beq @@End
    ldr r0, =0x020F7038 ; Boss flags
    ldrb r0, [r0]
    ands r0, r0, 0x20
    beq @@SkipEvent
    ldr r0, =0x020F6DFC
    ldrb r1, [r0]
    and r1, r1, 0xFD ; Get rid of the InBoss flag
    strb r1, [r0]
@@SkipEvent:
    pop r0,r1
    bx lr
@@End:
    pop r0,r1
    b 0x021CA7CC
.pool

@DarioEvent_Create:
    push r0
    ldr r0, = @GameFlag_ThroneIsShuffled
    ldrb r0, [r0]
    cmp r0, 0
    beq @@End
    pop r0
    bx lr
@@End:
    pop r0
    b 0x021CB584
.pool

@DimitriiEventCreate:
    push r0
    ldr r0, = @GameFlag_ThroneIsShuffled
    ldrb r0, [r0]
    cmp r0, 0
    beq @@End
    pop r0
    bx lr
@@End:
    pop r0
    b 0x021CA748
.pool

@DimitriiEvent_Update:
    push r0,r1
    ldr r0, = @GameFlag_ThroneIsShuffled
    ldrb r0, [r0]
    cmp r0, 0
    beq @@End
    ldr r0, =0x020F7038 ; Boss flags
    ldrb r0, [r0]
    ands r0, r0, 0x08
    beq @@SkipEvent
    ldr r0, =0x020F6DFC
    ldrb r1, [r0]
    and r1, r1, 0xFD ; Get rid of the InBoss flag
    strb r1, [r0]
@@SkipEvent:
    pop r0,r1
    bx lr
@@End:
    pop r0,r1
    b 0x021CA074
.pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;
; Delete all Boss entities if the player's Y-value is ABOVE a certain height
; used to control spawning in Condemned Tower
@DespawnTowerBosses:
    cmp r3, 0x65
    blt @@End ; We only want to check this for boss entities
    cmp r3, 0x72
    bgt @@End ; Don't trigger for the final bosses tho
    ldr r3, = 0x020CA960 ; Y pos
    ldr r3, [r3]
    cmp r3, 0x0C0000 ; If the player is higher than this position, despawn the boss
    blt @@End
    mov r1, 0
    b 0x021D7A54 ; Set the type to None and check again
@@End:
    b 0x021D7A7C
.pool
;;;;;;;;;;;;;;;;;;;
@ThroneBoss_ReloadRoom:
    strb r0, [r5, 0x09] ; Store the mirror flag here
    ldr r0, = 0x020F7039
    ldrb r0, [r0] ; Get the boss event flags
    ands r0, r0, 0x08
    bne @@End ; If we've already defeated the throne boss, just don't do this part

    ldr r0, =0x0211504C ; Check the current area
    ldrb r0, [r0]
    cmp r0, 9
    bne @@End  ; We only do this in the Pinnacle

    ldr r0, = @GameFlag_ThroneIsShuffled
    ldrb r0, [r0]
    cmp r0, 0
    beq @@End ; Don't re-wardp if boss shuffle is off
    push r0-r4, lr
    ldr r0, =0x020CA95E
    ldrh r2, [r0]
    lsl r2, r2, 4
    ldrh r3, [r0, 0x04]
    lsl r3, r3, 4
    mov r0, 0x09
    ldr r1, =0x01
    bl 0x02026AD0 ;Set Warp Dest
    pop r0-r4, lr
  ldr r1, =020F6DF4h
  mov r0, 0x0006
  strh r0, [r1] ; We set the current type of transition mode (020F6DF4) to 6, meaning a warp of some kind.
@@End:
    bx lr
.pool

@ThroneBoss_LeaveMirror:
    strb r3, [r5, 0x09]
    ldr r1, =@GameFlag_ThroneIsShuffled
    ldrb r1, [r1]
    cmp r1, 0
    beq @@End
    ldr r1, =0x0211504C
    ldrb r1, [r1]
    cmp r1, 9 ; Don't reload unless we're in the Pinnacle's mirror...
    bne @@End
    ldr r1, =0x020F7189
    ldrb r4, [r1] ; Get the game flags
    ands r2, r4, 0xA0 ; Have we done this yet?
    bne @@End

    ldr r2, = 0xA0
    orr r2, r2, r4 ; Set the flags
    strb r2, [r1]
    push r0-r3,lr
    bl 0x020298A0
    pop r0-r3,lr
@@End:    
    bx lr
.pool

;Get rid of the sound/init code for spawning Aguni. This is done to hide the room transition
@ThroneBoss_HideAguniSpawn:
push r0
    ldr r0, =@GameFlag_ThroneIsShuffled
    ldrb r0, [r0]
    cmp r0, 0
    beq @@End
    pop r0
    b 0x0225AA10

@@End:
    pop r0
    bl 0x02243C04
    b 0x0225A9E4
.pool

;;;;;;;;;;;;;;;;;;;;;;;;;;
@InitializeEnemyAndOverridePlayBossMusic:
  push r14
  push r1 ; Preserve the music ID
  
  bl 021C34A8h ; InitializeEnemy (replaces the line we overwrote to call this custom function)
  
  pop r0 ; Get the music ID out of the stack
  cmp r0, 0xFF
  beq @@SkipSong ; For dario throne room
  bl 0202991Ch ; PlaySong
  @@SkipSong:
  ; Set bit to make the song that was set override the BGM.
  ldr r0, =020F6DFCh
  ldr r1, [r0]
  orr r1, r1, 00040000h
  str r1, [r0]
  
  pop r15

@InitializeEnemyAndOverridePlayBossMusic2ForDmitriiAndDario:
  push r14
  ldr r1, =1005h ; Music ID for Scarlet Battle Soul
  bl @InitializeEnemyAndOverridePlayBossMusic
  pop r15

@InitializeEnemyAndOverridePlayBossMusicForZephyr:
  push r14
  
  add r1, r10, 200h
  ldr r1, [r1, 6Eh] ; Read Zephyr's Var A
  cmp r1, 1h ; Normal Zephyr
  beq @ZephyrOnlyInitializeEnemy
  
  ; For boss rush Zephyr, we want to play the music immediately.
  ldr r1, = 0x023029B4
  ldrh r1, [r1]
  bl @InitializeEnemyAndOverridePlayBossMusic
  b @ZephyrInitializeEnemyEnd
  
  @ZephyrOnlyInitializeEnemy:
  ; For normal Zephyr, we don't want to play music on initialization, or it will bug out because of how he starts the music later.
  bl 021C34A8h ; InitializeEnemy
  
  @ZephyrInitializeEnemyEnd:
  pop r15

@InitializeEnemyAndOverridePlayBossMusicForAguni:
  push r14
  ldr r1, =0x0211504C
  ldrb r1, [r1]
  cmp r1, 9
  bne @@PlayMusic
  ldr r1, = 0x020F6DF9
  ldrb r1, [r1]
  cmp r1, 3 ; If we're in the throne room, don't play Aguni's music unless we're in the Mirror World
  bne @@End
@@PlayMusic:
  ldr r1, =0x0225B208
  ldrh r1, [r1]
  bl @InitializeEnemyAndOverridePlayBossMusic
@@End:
  pop r15

@FixDarioMusic:
  push r14
  add r1, r0, 0x200
  ldrh r1, [r1, 0x70]  ; Get Dario's VarB
  cmp r1, 1 ; Throne room dario
  bne @@LoadSong
  mov r1, 0xFF
  b @@PlayMusic  ; We load 0xFF as the song so it knows not to play it
@@LoadSong:
  ldr r1, = 0x021CB574
  ldrh r1, [r1]
@@PlayMusic:
  bl @InitializeEnemyAndOverridePlayBossMusic
  pop r15

@FixDimitriiMusic:
  push r14
  ldr r1, =@GameFlag_ThroneIsShuffled
  ldrb r1, [r1]
  cmp r1, 0
  beq @@skipsong
  ldr r1, =0x021CA738
  ldrh r1, [r1]
@@SkipProperly:
  bl @InitializeEnemyAndOverridePlayBossMusic
  pop r15
@@skipsong:
    mov r1, 0xFF
    b @@SkipProperly
.pool
;;;;;;;;;;;;;;
; Repoints entity lists to NEW lists if the end flag is X greater than 0x7FFF
@ExtendedEntityList:
.dw @ExtEnt_TowerButton
.dw @ExtEnt_TowerBackBossDoor
.dw @ExtEnt_GardenConDisplay
.dw @ExtEnt_MenaceConDisplay

@ExtendEntityInfo:
    push r3
    sub r3, r3, 0x8000
    cmp r3, 0 ; Only check this for entries above 0x7FFF
    blt @@End
    ldr r2, =@ExtendedEntityList
    ldr r2, [r2, r3, lsl 2]
    pop r3
    b 0x021D7404
@@End:
    pop r3
    ldrsh r1,[r9]
    b 0x021D7490

@ExtendEntityInfo2:
    blt 0x021D74C0 ; back to normal code if not 7ffff
    push r1
    sub r1, r1, 0x8000
    cmp r1, 0 ; Only check this for entries above 0x7FFF
    blt @@End
    ldr r9, =@ExtendedEntityList
    ldr r9, [r9, r1, lsl 2]
    mov r7, 0
    pop r1
    b 0x021D74C0
@@End:
    pop r1
    b 0x021D7608

;;;;;;;;;;;;;;;;;;;;;;;;
; 0x021BAA5C
; Ignore the pressed state when loading the room if Var a is nonzero
@ChapelButton_IgnoreStateA:
    cmp r12, 0x44
    beq 0x021BAA64
@@NormalButton:
    ldr r0,[r0, 0x9A0]
    b 0x021BAA60

@ChapelButton_SwapFlag:
; 0x021BAB80
    cmp r12, 0x44
    beq @@InvertFlag
    orr r0, r2, r1, lsl r0
    bx lr
@@InvertFlag:
    eor r0, r2, 0x10
    bx lr
.pool

@ExtEnt_TowerButton:
;;;;;;;;;;;;;;;;;;;;;;
; Entity hider, hides the button until Gergoth's flag is set.
.dh 0x0000
.dh 0x0000
.db 0x00
.db 0x06 ; Hider
.db 0x07 ; Gergoth flag
.db 0x00
.dh 0x0000 ; Boss flag
.dh 0x0000 ; Despawn if not set


;Button. Triggers the tower floors on/off.
.dh 0x0080
.dh 0x0160
.db 0x00
.db 0x02
.db 0x28 ; Chapel button
.db 0x00
.dh 0x0000 
.dh 0x0044 ; Flag for the tower, (020F7188, 0x10)
.dw 0x7FFF7FFF
;;;;;;;;;;;;;;;;;;;;;;;;;;;
@ExtEnt_TowerBackBossDoor:
; Boss door for Gergoth, left side
.dh 0x00F0
.dh 0x0080
.db 0x00
.db 0x02
.db 0x25 ; Boss Door
.db 0x00
.dh 0x0000
.dh 0x0007 ; Gergoth door
.dw 0x7FFF7FFF
;;;;;;;;;;;;;;;;;;;;;;;
@ExtEnt_GardenConDisplay:
; Hammer Goal NPC for garden of madness event
.dh 0x0160
.dh 0x00B0
.db 0x00
.db 0x02
.db 0x47 ; NPC Hammer
.db 0x00
.dh 0x0001 ; Garden Goal condition
.dh 0x0000 ; Gergoth door
.dw 0x7FFF7FFF
;;;;;;;;;;;;;;;;;;;;;;;;;
@ExtEnt_MenaceConDisplay:
; Font loader entity
.dh 0x0000
.dh 0x0000
.db 0x00
.db 0x07
.db 0x00
.db 0x00
.dh 0x0000
.dh 0x0000
; Menace warp - Put this here because we need Hammer to load FIRST
.dh 0x0080
.dh 0x0060
.db 0x00
.db 0x02
.db 0x32 ; Abyss teleporter
.db 0x00
.dh 0x0002 ; Menace
.dh 0x0000
.dw 0x7FFF7FFF
.align 4
;;;;;;;;;;;;;;;;;;;;;;;;;
; Set the tower to use a main flag instead of Gergoth's flag
@TowerFloorLoadNewFlag:
    push r0
    ldr r0, =0x020F7188
    ldrb r0,[r0]
    ands r0,r0,0x10
    pop r0
    b 0x0219EF48
.pool
;;;;;;;;;;;;;;;;;;;;;
@GergothBreakTowerFlag:
    push r1
    ldr r0, =0x020F7188
    ldrb r1,[r0]
    orr r1,r1,0x10
    strb r1,[r0]
    pop r1
    add r0,r12,0x1B000
    bx lr
.pool

;;;;;;;;;;;;;;;;;;;;;
; Save the seal at the door for later use
@RamFlag_SealDoor:
    .db 0x00
    .align 4

@SealDoor_SaveSeal:
    ldr r4, = @RamFlag_SealDoor
    strb r2,[r4]
    ldr r4, [r1]
    bx lr
.pool
;;;;;;;;;;;;;;;;;
@DisplayTextPerSeal:
    @@SealTexts equ ((@SealDoors - @ExpandedTexPointers) / 2)
    ldr r0, =@RamFlag_SealDoor
    ldrb r0, [r0] ; Get the seal value back
    add r0, r0, @@SealTexts
    add r0, r0, 0x0500
    add r0, r0, 0x0B

    b 0x0202E520
;;;;;;;;;
;0x0202E978
@ExpandTextPointers_PopupLength:
    push r0
    sub r0, r0, 0x500
    cmp r0, 0x0B
    pop r0
    blt @@NormalDesc
    push r1,r2
    sub r0, r0, 0x500
    sub r0, r0, 0x0B
    ldr r1, =@ExpandedTexPointers
    lsl r0, r0, 1
    ldrh r0, [r1, r0]
    ldr r1, =0x02300000
    add r2, r0, r1
    add r0, r3, 0x36000
    mov r3, r2
    pop r1,r2
    b 0x0202E980
@@NormalDesc:
    add r0, r3, 0x36000
    b 0x0202E97C

@ExpandTextPointers_Popups:
    push r10
    sub r10, r10, 0x500
    cmp r10, 0x0B
    blt @@Normal
    sub r10, r10, 0x0B
    ldr r3, =@ExpandedTexPointers
    lsl r10, r10, 1
    ldrh r3, [r3, r10]
    ldr r10, =0x02300000
    add r10, r10, r3
    mov r0, r10
    pop r10
    bx lr
@@Normal:
    pop r10
    ldr r0, [r0, r10, lsl 2]
    bx lr
.pool
;;;;;;;;;;;;;;;;;;;;;
;Pretend to get the entity slot
;This loads some data required for the Orb drop. If it fails, it gets deleted, so we need to put it back for the game to function
@ReloadSealSlot:
    mov r0, 0xF5
    mov r1, r0
    ldr r2, =0x022154C4
    bl 0x02012B10
    b 0x02215404

;;;;;;;;;;;;
; Skip playing the Shop music if varA is set.
@HammerShop_SkipMusic: ; TODO. if r5 is consistent, make a subroutine out of the varA check
    push r5
    add r5, r5, 0x0200
    add r5, r5, 0x06E
    ldrb r5, [r5]
    cmp r5, 0 ; Normal shop
    bne @@End
    push lr
    bl 0x02029A1C
    pop lr
@@End:
    pop r5
    bx lr

; Changes hammer so that if varA is set, we load his actual position
; instead of hardcoding it
@HammerShop_Spawn:
    ldrb r3, [r6, 8] ; Get the varA
    cmp r3, 0
    beq @@End
    ldrh r3, [r6] ; Get the actual coordinates he's set to
    ldrh r4, [r6, 2]
    bx lr
@@End:
    mov r3, 0xB8
    bx lr

; Don't play the opening cutscene for the shop if varA is set
@HammerShop_SceneSkip:
    push r5
    add r5, r5, 0x200
    add r5, r5, 0x6E
    ldrb r12, [r5] ; Get the vara
    cmp r12, 0
    beq @@End
    mov r2, 1 ; Make this check always succeed
@@End:
    ands r12, r2, 1
    pop r5
    bx lr

;Play specific dialogue for the Shop depending on vara
@HammerShop_Dialogue:
    pop r0, r1 ; Get the r5 thing back in here
    push r0, r1
    add r1, r1, 0x200
    ldrb r1, [r1, 0x6E] ; Read the varA
    cmp r1, 0
    beq @@End
    ; Update the cutscene camera coordinates to the player's pos
    push lr
    push r0-r2
    bl 0x021C3250 ; Get y position
    str r0, [r4, 4]
    bl 0x021C3278 ; Get X position
    str r0, [r4]
    pop r0-r2
    pop lr
    ldr r0, = 0x0403 ; Base pointers/IDs for the GoalCon text
    add r1, r0, r1 ; Add varA to it
    bx lr
@@End:
    ldrh r1, [r4, 0x46]
    bx lr

;Prevent the game from opening the shop menu
@HammerShop_SkipShopMenu:
    push r5
    add r5, r5, 0x0200
    ldrb r5, [r5, 0x6E] ; Check var A
    cmp r5, 0
    bne @@EndFixVol ; Skip this entirely if varA is set
    pop r5
    push lr
    bl 0x02014510
    pop lr
    bx lr
@@EndFixVol:
    ldr r0, =0x2115670
    ldr r0, [r0]
    add r0, r0, 0x1C
    mov r5, 0x7F00
    strh r5, [r0, 0x04] ; Fix the volume post-scene
    pop r5
    bx lr

;Despawn the condition hammer if varA goal condition has been met
@HammerShop_CheckConditions:
    add r1, r5, 0x0200
    push r0
    ldrb r0, [r1, 0x6E]
    cmp r0, 0 ; Skip goal checks if hammer is a shop
    beq @@End
    sub r0, r0, 1
    bl @CheckGoal_Sub
    cmp r0, 0 ; Goal is NOT met
@@End:
    pop r0
    bne 0x021B9EEC
    mov r1, 0
    b 0x021B9F00
.pool


;;;;;;;;;;;;;;;;;;;;;;
;R0 = goal ID
;0 - garden
; 1 - mine
; 2 - menace
@CheckGoal_Sub:
    ldr r1, =0x02227127
@@CountPointer:
    cmp r0, 0
    beq @@EndMathLoop
    sub r0, r0, 1
    add r1, r1, 0x10 ; Add 10 to the pointer
    b @@CountPointer
@@EndMathLoop:
    ldrb r0, [r1] ; Check the goal number
    cmp r0, 0
    beq @@Goal_None
    cmp r0, 1
    beq @@Goal_Aguni
    cmp r0, 2
    beq @@Goal_Garden
    cmp r0, 3
    beq @@Goal_Bosses
    bx lr
@@Goal_None:
; No condition; always true
    mov r0, 1
    bx lr
@@Goal_Aguni:
; Checks the Flag for the event at the throne room ; set after defeating the Mirror boss there
    ldr r1, =0x20F7039 ; Check event flags
    ldrb r0, [r1, 0]
    ands r0, r0, 0x08 ;Event flag for the top floor boss fight
    bx lr 
@@Goal_Garden:
; Checks the Flag for the garden of madness/bad ending event
    ldr r1, =0x20F7039 ; Check event flags
    ldrb r0, [r1, 0]
    ands r0, r0, 0x40 ;Event flag for the garden of madness event
    bx lr
@@Goal_Bosses:
; Compare the player's Boss Defeat flags with pointer + 1 boss defeat flags
    ldrh r1, [r1, 1] ; 1 byte after the goal is the Boss Bitfield
    ldr r0, = 0x020F7038
    ldrh r0, [r0] ; Get the boss flags
    ands r0, r0, r1 ; AND the required flags and the boss flags
    cmp r0, r1 ; If equal, all of the corresponding bits are set
    beq @@BossGoalSet
    mov r0, 0
    bx lr
    @@BossGoalSet:
    mov r0, 1
    bx lr
;;;;;;;;;;;;;;;;;;
@CheckGoalCon_Menace:
    add r0, r5, 0x0200
    ldrb r0, [r0, 0x6E] ; Get varA
    cmp r0, 2 ; Is this the Menace warp?
    bne @@End
    mov r0, 2
    bl @CheckGoal_Sub
    cmp r0, 0 ; Is the goal complete?
    beq 0x021AF1F0
@@End:
    mov r0, 1
    b 0x021AF1B8

@CheckGoalCon_Mine:
    ands r0, r0, 0x800000 ; Check the dark gate's original flag. we don't want to do any of this again if the gate is already open
    bne 0x0219E780
    mov r0, 1
    bl @CheckGoal_Sub
    cmp r0, 0 ; Goal is NOT met
    beq @@Exit
    mov r0, 1
    ldr r1, = 0x020F718A
    strb r0, [r1] ; Set the flag to prime the mine cutscene
@@Exit:
    b 0x0219E704 ; Go back to normal but create the gate for the scene


;;;;;;;;;;;;;;;;;;;;;;;;
@CheckGoalCon_Garden:
    cmp r0, 0x0
    beq 0x021CEBF4 ; Vanilla condition. checks the flag
    ldr r0, =0x020F7039
    ldrb r0, [r0]
    ands r0, r0, 0x40
    bne @@End ; Boss flag that we've done the garden scene already
    mov r0, 0
    bl @CheckGoal_Sub
    cmp r0, 0
    bne 0x021CEC08 ; Resume the event as normal
@@End:
    ldr r0, =0x020F6DFC
    ldrb r1, [r0]
    and r1, 0x7E ; Remove the bits for HUD display and inScene
    strb r1, [r0]
    b 0x021CEBF4

@ResetGardenFlags:
    ldr r0, =0x020F6DFC
    ldrb r1, [r0]
    and r1, 0x7E ; Remove the bits for HUD display and inScene
    strb r1, [r0]
    bx lr
.pool
;;;;;;;;;;;;;;;;;;;;;;;;;
; Prevent the game from unloading stuff and crashing after the first Julius cutscene at the mine
@ResetMineFlags:
    ldr r0, =0x020F6DFC
    ldrb r1, [r0]
    and r1, 0x7E ; Remove the bits for HUD display and inScene
    strb r1, [r0]

    ldr r0, =0x020F7189
    ldrb r1, [r0]
    orr r1, r1, 0x04 ; set the flag for having viewed this scene
    strb r1, [r0]

    ldr r0, =0x2115670
    ldr r0, [r0]
    add r0, r0, 0x1C
    mov r1, 0x7F00
    strh r1, [r0, 0x04] ; Fix the volume post-scene
    bx lr
.pool

;Load a different, static entity list if we're in the Mirror World
@ThroneBoss_MirrorEntities:
    ldr r0, =0x020F6DF9
    ldrb r0, [r0]
    cmp r0, 3 ; Are we in the mirror world fully?
    bne @@End
    ldr r0, = @EntList_MirrorThrone
    bx lr
@@End:
    ldr r0,[r5, 0x14]
    bx lr

@FixDario_MirrorFlag:
    ldr r0, =0x020F6DF9
    ldrb r0, [r0]
    cmp r0, 0 ; We're not in the mirror world
    beq @@Normal
    mov r0, 0 ; Force this to fail so dario doesnt get fucked up
    bx lr
@@Normal:
    push lr
    bl 0x02018B24
    pop lr
    bx lr

.pool
.endarea
.close
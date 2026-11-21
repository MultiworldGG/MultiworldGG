; Handle the multiworld link

MainLoop:
    ; Check if the gameplay is world
    ld   a, [$DB95]
    cp   $0B
    jr   nz, .clearSafeAndRet
    ; Check if the world subtype is the normal one
    ld   a, [$DB96]
    cp   $07
    jr   nz, .clearSafeAndRet
    ; Check if we are moving between rooms
    ld   a, [$C124]
    and  a
    jr   nz, .clearSafeAndRet
    ; Check if link is in a normal walking/swimming state
    ld   a, [$C11C]
    cp   $02
    jr   nc, .clearSafeAndRet
    ; Check if a dialog is open
    ld   a, [$C19F]
    and  a
    jr   nz, .clearSafeAndRet
    ; Check if interaction is blocked
    ldh  a, [$FFA1]
    and  a
    jr   z, .gameplayIsSafe
.clearSafeAndRet:
    xor  a
    ld   [wConsecutiveSafe], a
    ret

.gameplayIsSafe:
    ; Store consecutive safe frames, up to overflow
    ld   a, [wConsecutiveSafe]
    inc  a
    jr   z, .checkSpawnDelay
    ld   [wConsecutiveSafe], a

.checkSpawnDelay:
    ld   a, [wLinkSpawnDelay]
    and  a
    jr   z, .spawnThings
    dec  a
    ld   [wLinkSpawnDelay], a
    jr   .readCommand ; no spawn

.spawnThings:
    ld   a, [wZolSpawnCount]
    and  a
    call nz, LinkSpawnSlime
    ld   a, [wCuccoSpawnCount]
    and  a
    call nz, LinkSpawnCucco
    ld   a, [wDropBombSpawnCount]
    and  a
    call nz, LinkSpawnBomb

.readCommand:
    ; require an arbitrary number of consecutive safe frames to do anything
    ; mostly for safety in sending death
    ld   a, [wConsecutiveSafe]
    cp   $10
    ret  c
    ; do nothing unless bit 7 is set
    ld   hl, wMWCommand
    bit  7, [hl]
    ret  z
    

    ; for the precollected cycle, bits 0 and 1 are expected to be set.
    ; mp_a should start at 0x00.
    ; runs through the block of precollected item ids stored on the rom,
    ; broken into two sections, each terminated by 0xFF.
    ; first section will display item message from server (mp_a=0x00)
    ; second section displays no item messages (mp_a=0xFF).
    ; this bit is also checked at .finish to maintain loop until done
    bit  5, [hl]
    jr   z, .collect

    ; get our next precollected item lined up
    ld   a, [wMWRecvIndexHi]
    ld   [wMWMultipurposeC], a
    ld   b, a
    ld   a, [wMWRecvIndexLo]
    ld   [wMWMultipurposeD], a
    ld   c, a
    ld   hl, PrecollectedItemIds
    add  hl, bc
    ; shift forward one more if we're in second section
    ld   a, [wMWMultipurposeA]
    and  a
    jr   z, .readPrecollectedItemCode
    inc  hl
.readPrecollectedItemCode:
    ld   a, [hl]
    ld   [wMWItemCode], a

    ; check for end of section
    cp   $FF
    jr   nz, .giveItem
    ; check if end of second section
    ld   a, [wMWMultipurposeA]
    and  a
    jp   nz, .clearCmdAndRet
    ; otherwise move to second section where we skip text
    ld   a, $FF
    ld   [wMWMultipurposeA], a
    ret


    ; mp_cd = location address
    ; mp_e = location mask
    ; tries to set mask at address, may give item if so
.collect:
    ld   hl, wMWCommand
    bit  2, [hl]
    jr   z, .giveItem
    ; get current location value onto b
    ld   a, [wMWMultipurposeC] ; collect location hi
    ld   h, a
    ld   a, [wMWMultipurposeD] ; collect location lo
    ld   l, a
    ldh  a, [$FFF6] ; current room
    cp   l
    jr   z, .checkTrade ; might be in current room
    ld   a, [hl]
    ld   b, a
    ld   a, [wMWMultipurposeE] ; location mask
    or   b ; apply mask
    cp   b ; was location already set?
    jr   z, .finish ; if so, do nothing else
    ld   [hl], a


    ; mp_a = sender slot, or 0xFF for no message
    ; if bit 1 set, check recvindex against mp_cd and increment on success
.giveItem:
    ld   hl, wMWCommand
    bit  0, [hl]
    jr   z, .checkTrade
    ld   hl, wMWCommand
    bit  1, [hl] ; do recvindex check only if bit set
    jr   z, .skipRecvIndexCheck
    ; check mp_cd against recvindex
    ld   a, [wMWRecvIndexHi]
    ld   b, a
    ld   a, [wMWMultipurposeC]
    cp   b
    jr   nz, .finish ; failed check on hi
    ld   a, [wMWRecvIndexLo]
    ld   b, a
    ld   a, [wMWMultipurposeD]
    cp   b
    jr   nz, .finish ; failed check on lo
    ; increment recvindex
    ld   a, [wMWRecvIndexLo]
    inc  a
    ld   [wMWRecvIndexLo], a
    jr   nz, .skipRecvIndexCheck ; no overflow, done
    ld   a, [wMWRecvIndexHi]
    inc  a
    ld   [wMWRecvIndexHi], a

.skipRecvIndexCheck:
    ; Give an item to the player
    ld   a, [wMWItemCode]
    ; if zol:
    cp   $22 ; zol item
    jr   z, StartZolDrop
    ; tmpChestItem = a
    ldh  [$FFF1], a
    ; Give the item
    call GiveItemFromChest
    ; Paste the item text
    call BuildItemMessage
    ; Paste " from "
    ld   hl, SpaceFrom
    call MessageCopyString
    ; Paste the player name
    ld   a, [wMWMultipurposeA]
    cp   $FF ; skip message on 0xFF
    jr   z, .checkTrade
    call MessageAddPlayerName
    ld   a, $C9
    ; OpenDialog()
    jp   $2385 ; Opendialog in $000-$0FF range

.checkTrade:
    ; check if trade item should be cleared
    ; get mask loaded
    ld   a, [wMWMultipurposeF]
    ld   b, a

    ; check trade 1
    ld   hl, wMWCommand
    bit  3, [hl]
    jr   z, .checkTrade2
    ld   a, [wTradeSequenceItem]
    and  b
    ld   [wTradeSequenceItem], a

.checkTrade2:
    ld   hl, wMWCommand
    bit  4, [hl]
    jr   z, .finish
    ld   a, [wTradeSequenceItem2]
    and  b
    ld   [wTradeSequenceItem2], a

.finish:
    ld   hl, wMWCommand
    bit  5, [hl]
    jr   nz, .ret
.clearCmdAndRet:
    ld   hl, wMWCommand
    res  7, [hl]
.ret:
    ret

GiveDeath:
    ld   a, [wHasMedicine]
    ; set health and health loss to a
    ; instant kill if no medicine
    ; kill with damage if medicine (to trigger medicine)
    ld   [$DB5A], a ; wHealth
    ld   [$DB94], a ; wSubtractHealthBuffer
    ; set health gain to zero
    xor  a
    ld   [$DB93], a ; wAddHealthBuffer
    ret
StartZolDrop:
    ld   a, $05
    ld   [wZolSpawnCount], a
    ;ld   a, $1D ; JINGLE_WRONG_ANSWER
    ;ldh  [$FFF2], a ; hJingle
    ret
SpecialSlimeStorm:
    ld   a, $20
    ld   [wZolSpawnCount], a
    ret
SpecialBombDrop:
    ld   a, $10
    ld   [wDropBombSpawnCount], a
    ret
SpecialCuccoParty:
    ld   a, $20
    ld   [wCuccoSpawnCount], a
    ret
SpecialPieceOfPower:
    ; Give the piece of power and the music
    ld   a, $01
    ld   [$D47C], a
    ld   a, $27
    ld   [$D368], a
    ld   a, $49
    ldh  [$FFBD], a
    ldh  [$FFBF], a
    ret
SpecialHealth:
    ; Regen all health
    ld   hl, $DB93
    ld   [hl], $FF
    ret
SpecialHealOne:
    ld   hl, $DB93
    ld   [hl], $04
    ret
LinkSpawnSlime:
    ld   a, $1B
    ld   e, $08
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place somewhere random
    call placeRandom

    ld   hl, $C310
    add  hl, de
    ld   [hl], $7F

    ld   hl, wZolSpawnCount
    dec  [hl]

    call $280D
    and  $03
    ld   [wLinkSpawnDelay], a
    ret

LinkSpawnCucco:
    ld   a, $6C
    ld   e, $04
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place where link is at.
    ld   hl, $C200
    add  hl, de
    ldh  a, [$FF98]
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    ldh  a, [$FF99]
    ld   [hl], a

    ; Set the "hits till cucco killer attack" much lower
    ld   hl, $C2B0
    add  hl, de
    ld   a, $21
    ld   [hl], a

    ld   hl, wCuccoSpawnCount
    dec  [hl]

    call $280D
    and  $07
    ld   [wLinkSpawnDelay], a
    ret

LinkSpawnBomb:
    ld   a, $02
    ld   e, $08
    call $3B98 ; SpawnNewEntity in range
    ret  c

    call placeRandom

    ld   hl, $C310 ; z pos
    add  hl, de
    ld   [hl], $4F

    ld   hl, $C430 ; wEntitiesOptions1Table
    add  hl, de
    res  0, [hl]
    ld   hl, $C2E0 ; wEntitiesTransitionCountdownTable
    add  hl, de
    ld   [hl], $80
    ld   hl, $C440 ; wEntitiesPrivateState4Table
    add  hl, de
    ld   [hl], $01

    ld   hl, wDropBombSpawnCount
    dec  [hl]

    call $280D
    and  $1F
    ld   [wLinkSpawnDelay], a
    ret

placeRandom:
    ; Place somewhere random
    ld   hl, $C200
    add  hl, de
    call $280D ; random number
    and  $7F
    add  a, $08
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    call $280D ; random number
    and  $3F
    add  a, $20
    ld   [hl], a
    ret


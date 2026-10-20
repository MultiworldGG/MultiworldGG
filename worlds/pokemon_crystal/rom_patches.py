from dataclasses import dataclass


@dataclass
class RomPatchEntry:
    bank: int
    address: int
    data: list[int]
    # patch is skipped unless every entry's ROM bytes match (overrides apply after token writes)
    expected: list[int] | None = None

    @property
    def rom_offset(self) -> int:
        if self.bank == 0:
            return self.address
        return (self.bank * 0x4000) + (self.address - 0x4000)


@dataclass
class RomPatch:
    name: str
    entries: list[RomPatchEntry]


ROM_PATCHES: list[RomPatch] = [
    # Qwilfish swarm applied to every fishing spot instead of only Route 32, and outlived ENGINE_QWILFISH_SWARM
    RomPatch("Qwilfish swarm fishgroup and engine flag check", [
        # bank $24 free space: z if fishgroup is QWILFISH, ENGINE_QWILFISH_SWARM set and swarm flag QWILFISH
        RomPatchEntry(0x24, 0x7fcb, [
            0x7a,              # ld a, d
            0xfe, 0x0a,        # cp FISHGROUP_QWILFISH
            0xc0,              # ret nz
            0xfa, 0x5b, 0xdc,  # ld a, [wDailyFlags1]
            0x2f,              # cpl
            0xcb, 0x57,        # bit DAILYFLAGS1_FISH_SWARM_F, a
            0xc0,              # ret nz
            0xfa, 0xd4, 0xdf,  # ld a, [wFishingSwarmFlag]
            0xfe, 0x01,        # cp FISHSWARM_QWILFISH
            0xc9,              # ret
        ], expected=[0x00] * 17),
        # Fish: ld a, [wFishingSwarmFlag] / cp FISHSWARM_QWILFISH -> call $7fcb / nop / nop
        RomPatchEntry(0x24, 0x682f, [0xcd, 0xcb, 0x7f, 0x00, 0x00],
                      expected=[0xfa, 0xd4, 0xdf, 0xfe, 0x01]),
    ]),
    # swarms persist until the triggering trainer is called again
    RomPatch("Keep swarm flags across daily reset", [
        # ROM0 free space: clear daily flags except the swarm bits, return a = 0
        RomPatchEntry(0x00, 0x0082, [
            0x21, 0x5b, 0xdc,  # ld hl, wDailyFlags1
            0x7e,              # ld a, [hl]
            0xe6, 0x04,        # and 1 << DAILYFLAGS1_FISH_SWARM_F
            0x22,              # ld [hli], a
            0xaf,              # xor a
            0x22,              # ld [hli], a ; wDailyFlags2
            0x7e,              # ld a, [hl]
            0xe6, 0x0c,        # and (1 << SWARMFLAGS_DUNSPARCE_SWARM_F) | (1 << SWARMFLAGS_YANMA_SWARM_F)
            0x22,              # ld [hli], a ; wSwarmFlags
            0xaf,              # xor a
            0x77,              # ld [hl], a ; wSwarmFlags + 1
            0xc9,              # ret
        ], expected=[0x00] * 16),
        # CheckDailyResetTimer: xor a / ld hl, wDailyFlags1 / ld [hli], a x3 / ld [hl], a -> call $0082 / nop x5
        RomPatchEntry(0x04, 0x53db, [0xcd, 0x82, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      expected=[0xaf, 0x21, 0x5b, 0xdc, 0x22, 0x22, 0x22, 0x77]),
    ]),
    # simple mode incoming calls only start swarms; ending one requires calling the trainer
    RomPatch("Incoming calls don't end swarms", [
        # <Trainer>PhoneCallerScript.Simple: iffalse/sjump <Trainer>_ToggleSwarm -> .TryActivate
        RomPatchEntry(0x2f, 0x59f8, [0xe1, 0x59], expected=[0x0e, 0x5a]),  # Ralph
        RomPatchEntry(0x2f, 0x5a02, [0xe1, 0x59], expected=[0x0e, 0x5a]),
        RomPatchEntry(0x2f, 0x5bb6, [0x9f, 0x5b], expected=[0xcc, 0x5b]),  # Anthony
        RomPatchEntry(0x2f, 0x5bc0, [0x9f, 0x5b], expected=[0xcc, 0x5b]),
        RomPatchEntry(0x2f, 0x5e1d, [0x06, 0x5e], expected=[0x33, 0x5e]),  # Arnie
        RomPatchEntry(0x2f, 0x5e27, [0x06, 0x5e], expected=[0x33, 0x5e]),
    ]),
    # Elm only checked the trainer ID of the first party mon of the species
    RomPatch("Search whole party for species with player's trainer ID", [
        # bank $13 free space: nz if any party mon is species b with the player's trainer ID
        RomPatchEntry(0x13, 0x72d7, [
            0x11, 0xde, 0xdc,  # ld de, wPartySpecies
            0x21, 0xeb, 0xdc,  # ld hl, wPartyMon1ID
            0x1a,              # .loop: ld a, [de]
            0x13,              # inc de
            0xfe, 0xff,        # cp -1
            0xc8,              # ret z
            0xb8,              # cp b
            0x20, 0x0e,        # jr nz, .next
            0xfa, 0x81, 0xd4,  # ld a, [wPlayerID]
            0xbe,              # cp [hl]
            0x20, 0x08,        # jr nz, .next
            0x23,              # inc hl
            0xfa, 0x82, 0xd4,  # ld a, [wPlayerID + 1]
            0xbe,              # cp [hl]
            0x2b,              # dec hl
            0x28, 0x08,        # jr z, .found
            0xc5,              # .next: push bc
            0x01, 0x30, 0x00,  # ld bc, PARTYMON_STRUCT_LENGTH
            0x09,              # add hl, bc
            0xc1,              # pop bc
            0x18, 0xe2,        # jr .loop
            0x3e, 0x01,        # .found: ld a, 1
            0xa7,              # and a
            0xc9,              # ret
        ], expected=[0x00] * 40),
        # _FindPartyMonThatSpeciesYourTrainerID: ld hl, wPartyMon1Species -> jp $72d7
        RomPatchEntry(0x13, 0x5a7e, [0xc3, 0xd7, 0x72], expected=[0x21, 0xe5, 0xdc]),
    ]),
    # resetting statics cleared the got-egg flag but not EVENT_TOGEPI_HATCHED, so Elm refused the hatchling
    RomPatch("Static reset keeps got-egg flag", [
        # LinkReceptionistScript_TimeCapsule: clearevent EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE -> checkevent
        RomPatchEntry(0x64, 0x6094, [0x31], expected=[0x32, 0x2d, 0x00]),
    ]),
    # any hatch of the egg species set EVENT_TOGEPI_HATCHED; stamp the aide's egg instead (eggs have zero caught data)
    RomPatch("Only the aide's egg sets EVENT_TOGEPI_HATCHED", [
        # bank $1a free space: script called from the aide after giveegg
        RomPatchEntry(0x1a, 0x7c18, [
            0x0e, 0x1a, 0x1d, 0x7c,  # callasm MarkAideEgg
            0x91,                    # end
        ], expected=[0x00] * 5),
        # MarkAideEgg: stamp the last party mon's caught level byte
        RomPatchEntry(0x1a, 0x7c1d, [
            0xfa, 0xdd, 0xdc,  # ld a, [wPartyCount]
            0x3d,              # dec a
            0x21, 0x02, 0xdd,  # ld hl, wPartyMon1CaughtLevel
            0x01, 0x30, 0x00,  # ld bc, PARTYMON_STRUCT_LENGTH
            0xcd, 0x07, 0x31,  # call AddNTimes
            0x36, 0xff,        # ld [hl], $ff
            0xc9,              # ret
        ], expected=[0x00] * 16),
        # CheckAideEgg: set EVENT_TOGEPI_HATCHED if the hatching egg is stamped, then SetEggMonCaughtData
        RomPatchEntry(0x1a, 0x7c2d, [
            0xfa, 0x10, 0xd1,  # ld a, [wCurPartyMon]
            0x21, 0x02, 0xdd,  # ld hl, wPartyMon1CaughtLevel
            0x01, 0x30, 0x00,  # ld bc, PARTYMON_STRUCT_LENGTH
            0xcd, 0x07, 0x31,  # call AddNTimes
            0x7e,              # ld a, [hl]
            0xfe, 0xff,        # cp $ff
            0x20, 0x08,        # jr nz, .done
            0x11, 0x54, 0x00,  # ld de, EVENT_TOGEPI_HATCHED
            0x06, 0x01,        # ld b, SET_FLAG
            0xcd, 0x80, 0x2e,  # call EventFlagAction
            0x3e, 0x13,        # .done: ld a, BANK(SetEggMonCaughtData)
            0x21, 0x50, 0x5a,  # ld hl, SetEggMonCaughtData
            0xcf,              # rst FarCall
            0xc9,              # ret
        ], expected=[0x00] * 32),
        # VioletPokecenter1F_ElmsAideScript: clearevent EVENT_ELMS_AIDE_IN_LAB / clearevent EVENT_TOGEPI_HATCHED
        # -> scall $7c18 / clearevent EVENT_ELMS_AIDE_IN_LAB
        RomPatchEntry(0x1a, 0x5525, [0x00, 0x18, 0x7c, 0x32, 0xb5, 0x06],
                      expected=[0x32, 0xb5, 0x06, 0x32, 0x54, 0x00]),
        # HatchEggs: farcall SetEggMonCaughtData -> farcall CheckAideEgg
        RomPatchEntry(0x05, 0x7a94, [0x3e, 0x1a, 0x21, 0x2d, 0x7c, 0xcf],
                      expected=[0x3e, 0x13, 0x21, 0x50, 0x5a, 0xcf]),
        # HatchEggs species check: jr nz, .nottogepi -> jr .nottogepi
        RomPatchEntry(0x05, 0x7ab5, [0x18], expected=[0x20, 0x08]),
    ]),
    # Elm asked to see the hatchling without the got-egg flag that his check requires
    RomPatch("Elm's egg hint checks got-egg before hatched", [
        # ElmScript_EverstoneHint, falls through to .ThoughtEggHatched
        RomPatchEntry(0x1e, 0x4e9d, [
            0x31, 0x56, 0x00,  # checkevent EVENT_GOT_EVERSTONE_FROM_ELM
            0x09, 0xfb, 0x50,  # iftrue ElmScript_CallYou
            0x31, 0x2d, 0x00,  # checkevent EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE
            0x09, 0xb2, 0x4e,  # iftrue .has_egg
            0x31, 0x00, 0x03,  # checkevent EVENT_BEAT_FALKNER
            0x09, 0xc6, 0x50,  # iftrue ElmAideHasEggScript
            0x03, 0xfb, 0x50,  # sjump ElmScript_CallYou
            0x31, 0x54, 0x00,  # .has_egg: checkevent EVENT_TOGEPI_HATCHED
            0x08, 0xcc, 0x50,  # iffalse ElmWaitingEggHatchScript
        ], expected=[
            0x31, 0x56, 0x00, 0x09, 0xfb, 0x50, 0x31, 0x54, 0x00, 0x09, 0xb8, 0x4e, 0x31, 0x2d,
            0x00, 0x09, 0xcc, 0x50, 0x31, 0x00, 0x03, 0x09, 0xc6, 0x50, 0x03, 0xfb, 0x50,
        ]),
    ]),
    # Psywave's damage roll loops forever at level 1 (range is 1 to 1), hanging trainer AI scoring
    RomPatch("Psywave level 1 hang", [
        # bank $0d free space: b = max(level * 1.5, 2)
        RomPatchEntry(0x0d, 0x7ff3, [
            0x78,              # ld a, b
            0xcb, 0x3f,        # srl a
            0x80,              # add b
            0xfe, 0x02,        # cp 2
            0x30, 0x02,        # jr nc, .ok
            0x3e, 0x02,        # ld a, 2
            0x47,              # .ok: ld b, a
            0xc9,              # ret
        ], expected=[0x00] * 12),
        # BattleCommand_ConstantDamage.psywave: ld a, b / srl a / add b / ld b, a -> call $7ff3 / nop x2
        RomPatchEntry(0x0d, 0x5606, [0xcd, 0xf3, 0x7f, 0x00, 0x00],
                      expected=[0x78, 0xcb, 0x3f, 0x80, 0x47]),
    ]),
]

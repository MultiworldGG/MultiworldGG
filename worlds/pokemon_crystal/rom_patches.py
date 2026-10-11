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
]

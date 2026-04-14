from dataclasses import dataclass

from .utils import convert_to_ingame_text


@dataclass
class RomPatchEntry:
    bank: int
    address: int
    data: list[int]

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
    # QwilfishText in fish.asm is missing its "@" terminator. The byte after the string is the
    # FishGroups chance byte which gets randomized per-seed, so the string reads into garbage.
    # Fix: write a terminated copy to free space at end of bank 0x24, update all 3 pointers.
    RomPatch("Fix QwilfishText missing terminator", [
        RomPatchEntry(bank=0x24, address=0x7E8E,
                      data=convert_to_ingame_text("ROUTES 12, 13, 32", string_terminator=True)),
        RomPatchEntry(bank=0x24, address=0x67CF, data=[0x8E, 0x7E]),
        RomPatchEntry(bank=0x24, address=0x681C, data=[0x8E, 0x7E]),
        RomPatchEntry(bank=0x24, address=0x686A, data=[0x8E, 0x7E]),
    ]),
    # The Pokecenter 2F battle sets wCatchDisabled and checks it at .can_escape to guarantee
    # fleeing. But three checks happen before .can_escape: Mean Look (SUBSTATUS_CANT_RUN),
    # trapping moves (wPlayerWrapCount), and the speed-based flee RNG (.cant_escape_2).
    # Fix: insert wCatchDisabled check inline at 0f:585E (right after the trainer battle check),
    # before all escape-prevention logic. Relocate original checks to trampoline in free space.
    RomPatch("Fix Pokecenter 2F battle flee with trapping moves", [
        # Inline wCatchDisabled check at 0f:585E, replacing the original 15 bytes of
        # SUBSTATUS_CANT_RUN + wPlayerWrapCount checks (relocated to trampoline)
        RomPatchEntry(bank=0x0F, address=0x585E, data=[
            0xFA, 0x5F, 0xD2,  # ld a, [wCatchDisabled]
            0xA7,               # and a
            0xC2, 0x47, 0x59,   # jp nz, .got_away_safely
            0xC3, 0xD9, 0x7F,   # jp trampoline
            0x00, 0x00, 0x00, 0x00, 0x00,  # nop padding (unreachable)
        ]),
        # Trampoline in free space at end of bank 0x0F: original checks then continue
        RomPatchEntry(bank=0x0F, address=0x7FD9, data=[
            0xFA, 0x71, 0xC6,  # ld a, [wEnemySubStatus5]
            0xCB, 0x7F,        # bit 7, a  (SUBSTATUS_CANT_RUN)
            0xC2, 0x09, 0x59,  # jp nz, .cant_escape
            0xFA, 0x30, 0xC7,  # ld a, [wPlayerWrapCount]
            0xA7,              # and a
            0xC2, 0x09, 0x59,  # jp nz, .cant_escape
            0xC3, 0x6D, 0x58,  # jp 586D (continue to flee item check)
        ]),
    ]),
    # Script_ExplosionTrap.asm_FaintFirstAliveMon zeros HP but doesn't clear MON_STATUS,
    # so a poisoned/burned/sleeping mon fainted by an explosion trap keeps its status.
    # Fix: replace "ld [hl], a; ld a, PARTY_LENGTH" with a call to a trampoline that
    # also clears status by decrementing hl past Unused to the Status byte.
    RomPatch("Fix explosion trap not clearing fainted mon status", [
        # Replace "ld [hl], a; ld a, PARTY_LENGTH" (77 3E 06) with call to trampoline
        RomPatchEntry(bank=0x7D, address=0x725E, data=[
            0xCD, 0x80, 0x72,        # call $7280
        ]),
        # Trampoline in free space after .ExplosionTrapText
        RomPatchEntry(bank=0x7D, address=0x7280, data=[
            0x77,                    # ld [hl], a         ; HP high = 0
            0x2B,                    # dec hl             ; -> Unused
            0x2B,                    # dec hl             ; -> Status
            0x77,                    # ld [hl], a         ; Status = 0
            0x3E, 0x06,              # ld a, PARTY_LENGTH
            0xC9,                    # ret                ; -> 7261 (sub b)
        ]),
    ]),
    # ChooseWildEncounter_BugContest doesn't check MORE_UNCAUGHT_ENCOUNTERS, so bug catching
    # contest Pokemon ignore the "more uncaught encounters" option. Fix: redirect the function
    # entry and return through a trampoline in free space that initializes wEncounterTryCount,
    # checks the option, and retries up to MAX_ENCOUNTER_RETRIES times if the species is caught.
    RomPatch("Fix bug catching contest ignoring more uncaught encounters", [
        # Redirect entry: replace "call Random" with "jp trampoline_init"
        RomPatchEntry(bank=0x25, address=0x7E64, data=[
            0xC3, 0x9C, 0x7F,  # jp trampoline_init
        ]),
        # Redirect return: replace "ld [wCurPartyLevel], a" with "jp trampoline_check"
        RomPatchEntry(bank=0x25, address=0x7E92, data=[
            0xC3, 0xA6, 0x7F,  # jp trampoline_check
        ]),
        # Trampoline in free space at 25:7F9C
        RomPatchEntry(bank=0x25, address=0x7F9C, data=[
            # trampoline_init: initialize retry counter then do original call Random
            0xAF,  # xor a
            0xEA, 0xD1, 0xC2,  # ld [wEncounterTryCount], a
            # contest_retry: (retry target at 25:7FA0)
            0xCD, 0x58, 0x2F,  # call Random
            0xC3, 0x67, 0x7E,  # jp 7E67  (continue after original call Random)
            # trampoline_check: store level then check uncaught option (at 25:7FA6)
            0xEA, 0x4A, 0xD1,  # ld [wCurPartyLevel], a
            0xFA, 0xCD, 0xCF,  # ld a, [MORE_UNCAUGHT_ENCOUNTERS address]
            0xCB, 0x77,  # bit 6, a  (MORE_UNCAUGHT_ENCOUNTERS bit)
            0x28, 0x14,  # jr z, .done  (option off -> return normally)
            0xFA, 0xD1, 0xC2,  # ld a, [wEncounterTryCount]
            0xFE, 0x04,  # cp MAX_ENCOUNTER_RETRIES
            0x28, 0x0D,  # jr z, .done  (max retries -> return normally)
            0x3C,  # inc a
            0xEA, 0xD1, 0xC2,  # ld [wEncounterTryCount], a
            0xFA, 0x35, 0xD2,  # ld a, [wTempWildMonSpecies]
            0x3D,  # dec a  (CheckCaughtMon expects 0-indexed)
            0xCD, 0xD2, 0x32,  # call CheckCaughtMon
            0x20, 0xDC,  # jr nz, contest_retry  (caught -> retry)
            # .done:
            0xAF,  # xor a
            0xC9,  # ret
        ]),
    ]),
    # CheckRockets.load_gym_count reads wGymCount, which is incremented by gym scripts AND
    # written by the client's compute_gym_count from synced EVENT_BEAT_* flags. With remote
    # items on, a remotely-synced gym beat event inflates wGymCount via the client, then the
    # gym script increments it again, double-counting and triggering rockets early.
    # Fix: replace .load_gym_count with a trampoline that recalculates wGymCount by counting
    # EVENT_BEAT_* flag bits (IDs 768-783 = wEventFlags bytes 96-97) using CountSetBits,
    # matching the client's compute_gym_count logic. Works for both remote-on and remote-off.
    RomPatch("Fix wGymCount double-counting with remote items", [
        # Replace .load_gym_count (03:586F) with jp to trampoline in bank 3 free space
        RomPatchEntry(bank=0x03, address=0x586F, data=[
            0xC3, 0x6A, 0x7E,  # jp $7E6A (trampoline)
            0x00, 0x00,         # nop nop (was jr .compare, now unreachable)
        ]),
        # Trampoline at 03:7E6A: count gym beat flags, update wGymCount, jump to .compare
        RomPatchEntry(bank=0x03, address=0x7E6A, data=[
            0x21, 0xE8, 0xDA,  # ld hl, wEventFlags + 96  ($DAE8)
            0xC5,              # push bc                   (save threshold in b)
            0x06, 0x02,        # ld b, 2                   (2 bytes = 16 flags)
            0xCD, 0x8C, 0x32,  # call CountSetBits         ($328C, home bank)
            0xFA, 0x6C, 0xD2,  # ld a, [wNumSetBits]       ($D26C)
            0xC1,              # pop bc                     (restore threshold)
            0xEA, 0xB1, 0xDC,  # ld [wGymCount], a         ($DCB1)
            0xC3, 0x47, 0x58,  # jp .compare               ($5847)
        ]),
    ]),
]

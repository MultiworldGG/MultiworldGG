from worlds.tloz_oos.common.patching.z80asm.Assembler import Z80Assembler


def define_unlocks(assembler: Z80Assembler):
    unlock_flag_data: list[int] = []
    # Format: Group / Room 1 / Flag 1 / Room 2 / Flag 2
    # (Room 0 changes do not matter in gp 4/5 since they are unused rooms)

    # Flag $01 is up, $02 is right, $04 is down, $08 is left, $80 is keyblock
    unlock_flag_data.extend([0x04, 0x07, 0x02, 0x00, 0x00])  # Hero's Cave: Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x1A, 0x08, 0x00, 0x00])  # Gnarled Root Dungeon: Keydoor Left of Entrance Unlock
    unlock_flag_data.extend([0x04, 0x0C, 0x01, 0x00, 0x00])  # Gnarled Root Dungeon: Miniboss Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x2F, 0x01, 0x2B, 0x04])  # Snake's Remains: Keydoor to Hardhats Unlock
    unlock_flag_data.extend([0x04, 0x20, 0x04, 0x00, 0x00])  # Snake's Remains: Miniboss Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x23, 0x80, 0x00, 0x00])  # Snake's Remains: Spinner Keyblock Unlock
    unlock_flag_data.extend([0x04, 0x52, 0x01, 0x00, 0x00])  # Poison Moth Lair: Keydoor to Mimics Unlock
    unlock_flag_data.extend([0x04, 0x49, 0x08, 0x00, 0x00])  # Poison Moth Lair: Miniboss Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x81, 0x02, 0x82, 0x08])  # Dancing Dragon Dungeon: Entrance Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x77, 0x80, 0x00, 0x00])  # Dancing Dragon Dungeon: Minecart Keyblock Unlock
    unlock_flag_data.extend([0x04, 0x74, 0x08, 0x73, 0x02])  # Dancing Dragon Dungeon: Crumbling Floor Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x71, 0x80, 0x00, 0x00])  # Dancing Dragon Dungeon: Pool Keyblock Unlock
    unlock_flag_data.extend([0x04, 0x69, 0x80, 0x00, 0x00])  # Dancing Dragon Dungeon: Boss Keyblock Unlock
    unlock_flag_data.extend([0x04, 0x8A, 0x08, 0x00, 0x00])  # Unicorn's Cave: Magnet Gloves Keydoor Unlock
    unlock_flag_data.extend([0x04, 0xA1, 0x02, 0x00, 0x00])  # Unicorn's Cave: Miniboss Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x9B, 0x08, 0x9A, 0x02])  # Unicorn's Cave: Wall of Flames Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x94, 0x01, 0x90, 0x04])  # Unicorn's Cave: Basement Keydoor Unlock
    unlock_flag_data.extend([0x04, 0x9B, 0x80, 0x00, 0x00])  # Unicorn's Cave: Boss Keyblock Unlock
    unlock_flag_data.extend([0x04, 0xB6, 0x80, 0x00, 0x00])  # Ancient Ruins: Entrance Keyblock Unlock
    unlock_flag_data.extend([0x04, 0xB2, 0x01, 0xAD, 0x04])  # Ancient Ruins: Right Path Keydoor Unlock
    unlock_flag_data.extend([0x04, 0xCB, 0x01, 0x00, 0x00])  # Ancient Ruins: Miniboss Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x59, 0x02, 0x5A, 0x08])  # Explorer's Crypt: Entrance Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x4A, 0x04, 0x4D, 0x01])  # Explorer's Crypt: Keydoor to Enclosed Trampoline Unlock
    unlock_flag_data.extend([0x05, 0x4D, 0x02, 0x4E, 0x08])  # Explorer's Crypt: Margret's Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x3C, 0x80, 0x00, 0x00])  # Explorer's Crypt: Flying Tile Keyblock Unlock
    unlock_flag_data.extend([0x05, 0x3D, 0x02, 0x3E, 0x08])  # Explorer's Crypt: Shining Blue Puzzle Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x77, 0x80, 0x00, 0x00])  # Sword & Shield Dungeon: Entrance Keyblock Unlock
    unlock_flag_data.extend([0x05, 0x6E, 0x02, 0x6F, 0x08])  # Sword & Shield Dungeon: Spinner Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x71, 0x02, 0x00, 0x00])  # Sword & Shield Dungeon: Miniboss Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x86, 0x08, 0x85, 0x02])  # Sword & Shield Dungeon: Ice Crystals Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x7E, 0x80, 0x00, 0x00])  # Sword & Shield Dungeon: Lava Hole Keyblock Unlock
    unlock_flag_data.extend([0x05, 0x7E, 0x04, 0x83, 0x01])  # Sword & Shield Dungeon: Beamos Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x65, 0x80, 0x00, 0x00])  # Sword & Shield Dungeon: Boss Keyblock Unlock
    unlock_flag_data.extend([0x05, 0x32, 0x01, 0x00, 0x00])  # Linked Hero's Cave: Floor 2 Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x2B, 0x80, 0x00, 0x00])  # Linked Hero's Cave: Floor 3 Keyblock Unlock
    unlock_flag_data.extend([0x05, 0x2A, 0x01, 0x00, 0x00])  # Linked Hero's Cave: Floor 3 Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x22, 0x02, 0x00, 0x00])  # Linked Hero's Cave: Boomerang Maze Keydoor Unlock
    unlock_flag_data.extend([0x05, 0x23, 0x04, 0x00, 0x00])  # Linked Hero's Cave: Final Challenge Keydoor Unlock

    assembler.add_floating_chunk("unlockFlagsData", unlock_flag_data)

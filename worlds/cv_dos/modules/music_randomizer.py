valid_area_music = [
    0x00,
    0x01,
    0x0B,
    0x0D,
    0x0E,
    0x0F,
    0x10,
    0x11,
    0x12,
    0x13,
    0x14,
    0x15,
    0x16,
    0x17,
    0x18
]

valid_boss_music = [
    0x02,
    0x03,
    0x05,
    0x06,
    0x1A,
    0x1B
]

boss_song_addresses = {
    0x2300d38: "overlay_30",  # F. Armor
    0x2300940: "overlay_23",  # Balore
    0x21ca738: "overlay_0",  # Dimitrii
    0x2300ae8: "overlay_29",  # Malphas
    0x21cb574: "overlay_0",  # Dario
    0x2300f64: "overlay_25",  # P. Master
    0x22ffd8c: "overlay_36",  # Gergoth
    0x22ffbcc: "overlay_26",  # Rahab
    0x23029b4: "overlay_33",  # Zephyr
    0x22ffb88: "overlay_37",  # Bat Company
    0x2305660: "overlay_35",  # Paranoia
    0x230565c: "overlay_35",  # Paranoia 2
    0x21cd6ac: "overlay_0",  # Dario 2
    0x225b208: "overlay_1",  # Aguni
    0x2302bb8: "overlay_34",  # Death
    0x22ffb74: "overlay_39",  # Abaddon
    0x021D2B9C: "overlay_0",  # Menace
    0x02238944: "overlay_1"  # Soma

}


def area_music_randomizer(world, rom):
    music_pool = valid_area_music.copy()
    for i in range(0x11):
        if i in {0x0C, 0x0D, 0x0E, 0x0F}:
            continue  # Areas where music isn't used
        song = world.random.choice(music_pool)
        music_pool.remove(song)
        rom.write_to_file(0x209A634 + (i * 4), "arm9", bytearray([song]))


def boss_music_randomizer(world, rom):
    for address in boss_song_addresses:
        song = world.random.choice(valid_boss_music)
        rom.write_to_file(address, boss_song_addresses[address], bytearray([song]))

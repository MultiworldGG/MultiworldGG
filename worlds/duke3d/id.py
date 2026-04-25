GAME_ID = 1


def local_id(ap_id: int) -> int:
    return ap_id & 0x7FF


def net_id(short_id: int) -> int:
    return local_id(short_id) | 0xB17D0000 | GAME_ID << 11

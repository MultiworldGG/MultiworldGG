"""Wonder trade JSON serialization for Crystal party mons."""

import json
import random
from typing import Any, Dict, List

PARTY_MON_LENGTH = 48
NICK_LENGTH = 11
OT_LENGTH = 11

MON_SPECIES = 0
MON_ITEM = 1
MON_MOVES = 2
MON_ID = 6
MON_EXP = 8
MON_STAT_EXP = 11
MON_DVS = 21
MON_PP = 23
MON_HAPPINESS = 27
MON_POKERUS = 28
MON_CAUGHTDATA = 29
MON_LEVEL = 31
MON_STATUS = 32
MON_HP = 34
MON_MAXHP = 36
MON_STATS = 38

CRYSTAL_MAX_SPECIES = 251
CRYSTAL_MAX_MOVE = 251
RAZOR_WIND_ID = 13
UNOWN_ID = 201

POOL_METLOC_IN_GAME_TRADE = 0xFE
CRYSTAL_LANDMARK_GIFT = 0x7E

# Held-item id mappings between Crystal and the shared pool. Items absent
# from the map are stripped on transfer (Apricorns, Gen2 berries, quest items).
CRYSTAL_TO_POOL_ITEM = {
    1: 1, 2: 2, 3: 179, 4: 3, 5: 4, 7: 360, 8: 94, 9: 14, 10: 15, 11: 16,
    12: 17, 13: 18, 14: 19, 15: 20, 16: 21, 17: 22, 18: 13, 19: 85, 20: 86,
    21: 37, 22: 95, 23: 96, 24: 97, 25: 63, 26: 64, 27: 65, 28: 66, 29: 222,
    30: 67, 31: 68, 32: 78, 33: 98, 34: 223, 35: 110, 36: 80, 37: 23, 38: 24,
    39: 25, 40: 73, 41: 83, 42: 84, 43: 74, 44: 26, 45: 27, 46: 28, 47: 75,
    48: 76, 49: 77, 50: 79, 51: 260, 52: 261, 55: 262, 56: 263, 58: 264,
    59: 69, 60: 34, 61: 35, 62: 36, 65: 265, 69: 29, 70: 183, 73: 203,
    74: 210, 78: 211, 79: 187, 83: 103, 84: 104, 85: 188, 87: 189, 90: 190,
    91: 209, 92: 214, 94: 207, 97: 206, 100: 225, 101: 194, 102: 212, 103: 208,
    105: 106, 106: 107, 107: 195, 108: 213, 112: 205, 113: 224, 114: 196,
    115: 30, 116: 31, 117: 32, 118: 33, 119: 204, 120: 197, 121: 355,
    125: 108, 126: 109, 127: 271, 129: 215, 130: 44, 131: 198, 132: 199,
    133: 216, 134: 200, 136: 201, 138: 45, 144: 202, 150: 93, 152: 218,
    168: 369, 169: 349, 170: 182,
}
# TMs map by slot, not by move. Crystal TM_1..50 = 198..247; pool = 289..338.
for _tm in range(1, 51):
    CRYSTAL_TO_POOL_ITEM[197 + _tm] = 288 + _tm
del _tm
POOL_TO_CRYSTAL_ITEM = {v: k for k, v in CRYSTAL_TO_POOL_ITEM.items()}


def _build_decode_map() -> Dict[int, str]:
    pairs = [
        (0x75, "…"), (0x7f, " "),
        *[(0x80 + i, chr(ord("A") + i)) for i in range(26)],
        (0x9a, "("), (0x9b, ")"), (0x9c, ":"), (0x9d, ";"), (0x9e, "["), (0x9f, "]"),
        *[(0xa0 + i, chr(ord("a") + i)) for i in range(26)],
        (0xc0, "Ä"), (0xc1, "Ö"), (0xc2, "Ü"), (0xc3, "ä"), (0xc4, "ö"), (0xc5, "ü"),
        (0xd0, "'d"), (0xd1, "'l"), (0xd2, "'m"), (0xd3, "'r"), (0xd4, "'s"), (0xd5, "'t"), (0xd6, "'v"),
        (0xe0, "'"), (0xe3, "-"), (0xe4, "+"), (0xe6, "?"), (0xe7, "!"),
        (0xe8, "."), (0xe9, "&"), (0xea, "é"),
        (0xef, "♂"), (0xf0, "$"), (0xf3, "/"), (0xf4, ","), (0xf5, "♀"),
        *[(0xf6 + i, str(i)) for i in range(10)],
    ]
    return dict(pairs)


_DECODE_MAP = _build_decode_map()
_STRING_TERMINATOR = 0x50


def _decode_charmap(data: bytes) -> str:
    out: List[str] = []
    for b in data:
        if b == _STRING_TERMINATOR:
            break
        out.append(_DECODE_MAP.get(b, "?"))
    return "".join(out)


def _encode_charmap(text: str, max_chars: int) -> bytes:
    charmap = {
        "…": 0x75, " ": 0x7f, "(": 0x9a, ")": 0x9b, ":": 0x9c, ";": 0x9d, "[": 0x9e, "]": 0x9f,
        "Ä": 0xc0, "Ö": 0xc1, "Ü": 0xc2, "ä": 0xc3, "ö": 0xc4, "ü": 0xc5,
        "'": 0xe0, "-": 0xe3, "+": 0xe4, "?": 0xe6, "!": 0xe7, ".": 0xe8, "&": 0xe9, "é": 0xea,
        "♂": 0xef, "$": 0xf0, "/": 0xf3, ",": 0xf4, "♀": 0xf5,
    }
    for i in range(26):
        charmap[chr(ord("A") + i)] = 0x80 + i
        charmap[chr(ord("a") + i)] = 0xa0 + i
    for i in range(10):
        charmap[str(i)] = 0xf6 + i
    out = bytearray()
    text = text[:max_chars]
    for ch in text:
        out.append(charmap.get(ch, 0xe6))
    if len(out) < max_chars + 1:
        out.append(_STRING_TERMINATOR)
    while len(out) < max_chars + 1:
        out.append(0x50)
    return bytes(out[: max_chars + 1])


def _dv_word_to_nibbles(dvs: int) -> Dict[str, int]:
    atk = (dvs >> 12) & 0xF
    df = (dvs >> 8) & 0xF
    spd = (dvs >> 4) & 0xF
    spc = dvs & 0xF
    hp = ((atk & 1) << 3) | ((df & 1) << 2) | ((spd & 1) << 1) | (spc & 1)
    return {"hp": hp, "atk": atk, "def": df, "spd": spd, "spc": spc}


def _nibbles_to_dv_word(atk: int, df: int, spd: int, spc: int) -> int:
    return ((atk & 0xF) << 12) | ((df & 0xF) << 8) | ((spd & 0xF) << 4) | (spc & 0xF)


def _stat_exp_to_ev(stat_exp: int) -> int:
    return min(0xFF, stat_exp >> 8)


def _ev_to_stat_exp(ev: int) -> int:
    return (ev & 0xFF) * 257


def pokemon_data_to_json(party_mon: bytes, nickname: bytes, ot: bytes,
                          trainer_id: int, player_female: bool) -> str:
    species = party_mon[MON_SPECIES]
    held_item = party_mon[MON_ITEM]
    moves = list(party_mon[MON_MOVES:MON_MOVES + 4])
    pps = list(party_mon[MON_PP:MON_PP + 4])
    exp = int.from_bytes(party_mon[MON_EXP:MON_EXP + 3], "big")
    stat_exp = [
        int.from_bytes(party_mon[MON_STAT_EXP + i * 2:MON_STAT_EXP + i * 2 + 2], "big")
        for i in range(5)
    ]
    dvs = int.from_bytes(party_mon[MON_DVS:MON_DVS + 2], "big")
    pokerus = party_mon[MON_POKERUS]
    caught_data = int.from_bytes(party_mon[MON_CAUGHTDATA:MON_CAUGHTDATA + 2], "big")
    caught_level = caught_data >> 8

    nibbles = _dv_word_to_nibbles(dvs)

    json_object: Dict[str, Any] = {
        "version": "1",
        "personality": (trainer_id << 16) | (dvs << 8) | species,
        "nickname": _decode_charmap(nickname),
        "language": "English",
        "species": species,
        "experience": exp,
        # Crystal has no ability concept; randomize the slot so species with
        # two distinct abilities don't always resolve to slot 0 on receive.
        "ability": random.randint(0, 1),
        "ivs": [
            nibbles["hp"] * 2 + 1,
            nibbles["atk"] * 2 + 1,
            nibbles["def"] * 2 + 1,
            nibbles["spd"] * 2 + 1,
            nibbles["spc"] * 2 + 1,
            nibbles["spc"] * 2 + 1,
        ],
        "evs": [
            _stat_exp_to_ev(stat_exp[0]),
            _stat_exp_to_ev(stat_exp[1]),
            _stat_exp_to_ev(stat_exp[2]),
            _stat_exp_to_ev(stat_exp[3]),
            _stat_exp_to_ev(stat_exp[4]),
            _stat_exp_to_ev(stat_exp[4]),
        ],
        "conditions": [0, 0, 0, 0, 0, 0],
        "pokerus": pokerus,
        # Crystal landmark ids collide with the receiver's location ids;
        # sub the "in-game trade" sentinel.
        "location_met": POOL_METLOC_IN_GAME_TRADE,
        "level_met": caught_level & 0x7F,
        "game": 0,
        "ball": 4,
        "moves": [
            [moves[i], pps[i] & 0x3F, (pps[i] >> 6) & 0x3]
            for i in range(4)
        ],
        "trainer": {
            "name": _decode_charmap(ot),
            "id": trainer_id,
            "female": player_female,
        },
    }
    pool_item = CRYSTAL_TO_POOL_ITEM.get(held_item)
    if pool_item:
        json_object["item"] = pool_item

    return json.dumps(json_object, separators=(",", ":"))


def json_to_pokemon_data(json_str: str) -> Dict[str, bytes]:
    payload: Dict[str, Any] = json.loads(json_str)
    payload.setdefault("trainer", {})

    species = int(payload.get("species", 1))
    if species < 1 or species > CRYSTAL_MAX_SPECIES:
        species = UNOWN_ID

    raw_moves = payload.get("moves") or []
    moves: List[int] = []
    pps: List[int] = []
    for entry in raw_moves:
        if not isinstance(entry, (list, tuple)) or len(entry) < 1:
            continue
        move_id = int(entry[0])
        if move_id < 1 or move_id > CRYSTAL_MAX_MOVE:
            continue
        pp = int(entry[1]) if len(entry) > 1 else 0
        pp_ups = int(entry[2]) if len(entry) > 2 else 0
        moves.append(move_id & 0xFF)
        pps.append(((pp_ups & 0x3) << 6) | (pp & 0x3F))
        if len(moves) == 4:
            break
    if not moves:
        # Razor Wind has 10 base PP, no PP-ups.
        moves.append(RAZOR_WIND_ID)
        pps.append(10)
    while len(moves) < 4:
        moves.append(0)
        pps.append(0)

    ivs = list(payload.get("ivs") or [0] * 6)
    while len(ivs) < 6:
        ivs.append(0)
    atk_dv = (ivs[1] >> 1) & 0xF
    def_dv = (ivs[2] >> 1) & 0xF
    spd_dv = (ivs[3] >> 1) & 0xF
    spc_dv = (((ivs[4] + ivs[5]) // 2) >> 1) & 0xF
    dvs = _nibbles_to_dv_word(atk_dv, def_dv, spd_dv, spc_dv)

    evs = list(payload.get("evs") or [0] * 6)
    while len(evs) < 6:
        evs.append(0)
    stat_exps = [
        _ev_to_stat_exp(evs[0]),
        _ev_to_stat_exp(evs[1]),
        _ev_to_stat_exp(evs[2]),
        _ev_to_stat_exp(evs[3]),
        _ev_to_stat_exp((evs[4] + evs[5]) // 2),
    ]

    exp = max(0, int(payload.get("experience", 0))) & 0xFFFFFF
    level = max(1, min(100, int(payload.get("level_met", 1)) or 1))

    held_item = POOL_TO_CRYSTAL_ITEM.get(int(payload.get("item", 0) or 0), 0)

    trainer = payload.get("trainer") or {}
    trainer_id = int(trainer.get("id", 0)) & 0xFFFF
    nickname_str = str(payload.get("nickname") or "WONDER")
    ot_str = str(trainer.get("name") or "AP")

    party_mon = bytearray(PARTY_MON_LENGTH)
    party_mon[MON_SPECIES] = species
    party_mon[MON_ITEM] = held_item
    for i in range(4):
        party_mon[MON_MOVES + i] = moves[i]
    party_mon[MON_ID:MON_ID + 2] = trainer_id.to_bytes(2, "big")
    party_mon[MON_EXP:MON_EXP + 3] = exp.to_bytes(3, "big")
    for i, se in enumerate(stat_exps):
        party_mon[MON_STAT_EXP + i * 2:MON_STAT_EXP + i * 2 + 2] = se.to_bytes(2, "big")
    party_mon[MON_DVS:MON_DVS + 2] = dvs.to_bytes(2, "big")
    for i in range(4):
        party_mon[MON_PP + i] = pps[i]
    party_mon[MON_HAPPINESS] = 70
    party_mon[MON_POKERUS] = int(payload.get("pokerus", 0)) & 0xFF
    party_mon[MON_CAUGHTDATA] = level & 0x3F
    gender_bit = 0x80 if bool(trainer.get("female")) else 0
    party_mon[MON_CAUGHTDATA + 1] = gender_bit | CRYSTAL_LANDMARK_GIFT
    party_mon[MON_LEVEL] = level

    nickname = _encode_charmap(nickname_str, max_chars=NICK_LENGTH - 1)
    ot = _encode_charmap(ot_str, max_chars=OT_LENGTH - 1)

    return {
        "party_mon": bytes(party_mon),
        "nickname": nickname,
        "ot": ot,
    }


def trade_is_eligible(item: List[Any], own_id: int) -> bool:
    """Pool entries are `[trainer_id, json_blob]`. own_id is this player's
    Crystal trainer id (or the slot for foreign games that use slot-based
    identity — the comparison only needs to reject self-trades)."""
    if not isinstance(item, (list, tuple)) or len(item) < 2:
        return False
    other_id, blob = item[0], item[1]
    if other_id == own_id:
        return False
    try:
        payload = json.loads(blob)
    except (ValueError, TypeError):
        return False
    species = payload.get("species")
    if not isinstance(species, int) or species < 1 or species > CRYSTAL_MAX_SPECIES:
        return False
    moves = payload.get("moves") or []
    has_compatible_move = any(
        isinstance(m, (list, tuple)) and len(m) >= 1 and 1 <= int(m[0]) <= CRYSTAL_MAX_MOVE
        for m in moves
    )
    return has_compatible_move

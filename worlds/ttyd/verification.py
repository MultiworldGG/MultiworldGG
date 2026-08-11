"""Validator for the credits-screen verification code.

The mod displays three lines over the credits:

    Time: 1:23:45.67 [*<reasons>]
    Seed: 1234567890123456
    Code: A1B2-C3D4-E5F6-0718

The code is self-contained: the first 8 hex digits are the payload (24-bit RTA
frame count + 8-bit dirty-reason mask) and the last 8 are a keyed MAC over
"payload|seed". Verifying a run therefore only needs the code and the seed:

    python verification.py A1B2-C3D4-E5F6-0718 1234567890123456

Deliberately dependency-free so race organizers can run it standalone. The key
and MAC must stay in sync with creditsResultsDisp in the mod's rel/source/OWR.cpp
(the key also lives in Data.py as SEED_OBFUSCATION_KEY).
"""

import sys

SEED_OBFUSCATION_KEY = bytes([0xA5, 0x1C, 0x7E, 0x33, 0xC9, 0x58, 0xE2, 0x0F,
                              0x96, 0x41, 0xDB, 0x6A, 0x24, 0xB7, 0x5D, 0xF0])

# Dirty-reason bitmask carried in the payload (and shown after the time as *<hex>).
# Bits 0x01-0x04 are set by the mod, 0x08-0x10 by the client; keep in sync with both.
DIRTY_REASONS = {
    0x01: "This save file was started on a different seed.",
    0x02: "A savestate was loaded or the emulator was paused during the run.",
    0x04: "The system clock was set to a time before this seed existed.",
    0x08: "Game flags were changed from outside the game (client sync or debug commands).",
    0x10: "Items were sent to this save from outside the game.",
}


def _fnv1a32(data: bytes, hash_value: int) -> int:
    for b in data:
        hash_value = ((hash_value ^ b) * 0x01000193) & 0xFFFFFFFF
    return hash_value


def _mac(payload: int, seed: str) -> int:
    message = f"{payload:08X}|{seed}".encode("utf-8")
    return _fnv1a32(message, _fnv1a32(SEED_OBFUSCATION_KEY, 0x811C9DC5))


def _mask(mac: int, seed: str) -> int:
    """Keystream the payload is XOR-whitened with; derived from the MAC so any
    payload change avalanches across the whole code (no visible structure)."""
    message = f"{mac:08X}|{seed}".encode("utf-8")
    return _fnv1a32(message, _fnv1a32(SEED_OBFUSCATION_KEY, 0xCBF29CE4))


def compute_code(frames: int, dirty_mask: int, seed: str) -> str:
    """Render the code exactly as the mod displays it."""
    payload = (min(frames, 0xFFFFFF) << 8) | (dirty_mask & 0xFF)
    mac = _mac(payload, seed)
    whitened = payload ^ _mask(mac, seed)
    return f"{whitened >> 16:04X}-{whitened & 0xFFFF:04X}-{mac >> 16:04X}-{mac & 0xFFFF:04X}"


def parse_code(code: str, seed: str):
    """Validate a code against a seed. Returns (frames, dirty_mask) or None."""
    digits = code.replace("-", "").replace(" ", "").strip().upper()
    if len(digits) != 16 or any(c not in "0123456789ABCDEF" for c in digits):
        return None
    whitened = int(digits[:8], 16)
    mac = int(digits[8:], 16)
    payload = whitened ^ _mask(mac, seed)
    if mac != _mac(payload, seed):
        return None
    return payload >> 8, payload & 0xFF


def format_time(frames: int) -> str:
    seconds = frames // 60
    centis = (frames % 60) * 100 // 60
    return f"{seconds // 3600}:{(seconds // 60) % 60:02d}:{seconds % 60:02d}.{centis:02d}"


def dirty_reasons(mask: int) -> list:
    reasons = [text for bit, text in DIRTY_REASONS.items() if mask & bit]
    unknown = mask & ~sum(DIRTY_REASONS)
    if unknown:
        reasons.append(f"unknown reason bits {unknown:#x}")
    return reasons


def main(argv) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2

    code, seed = argv[1].strip(), argv[2].strip()[:16]
    parsed = parse_code(code, seed)
    if parsed is None:
        print("INVALID")
        return 1

    frames, mask = parsed
    print(f"Time: {format_time(frames)}")
    reasons = dirty_reasons(mask)
    if reasons:
        print("VALID, but the run is marked dirty:")
        for r in reasons:
            print(f"  - {r}")
    else:
        print("VALID (clean run)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

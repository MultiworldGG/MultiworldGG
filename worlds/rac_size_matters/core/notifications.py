"""SAC-style receipt colours for the non-blocking item HUD."""


def _clean(value, limit):
    value = "".join(c if 32 <= ord(c) < 127 else "?" for c in str(value))
    return value if len(value) <= limit else value[:limit - 3] + "..."


def receipt_text(item, sender, trap=False):
    colour = 3 if trap else 13
    return (b"Received " + bytes((0x90, colour)) + _clean(item, 32).encode("ascii")
            + b"\x90\x01\nfrom \x90\x0b" + _clean(sender, 30).encode("ascii")
            + b"\x90\x01\0")


def sent_text(item, receiver):
    return (b"Sent " + bytes((0x90, 13)) + _clean(item, 32).encode("ascii")
            + b"\x90\x01\nto \x90\x0b" + _clean(receiver, 30).encode("ascii")
            + b"\x90\x01\0")

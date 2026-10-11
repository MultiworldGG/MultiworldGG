import sys
from pathlib import Path

from PIL import Image

SIZE = 32
MAX_COLORS = 256


def _csm1_swizzle(logical_index: int) -> int:
    """PS2 GS stores a 256-color CLUT in VRAM with each 32-entry block's middle two
    8-entry groups swapped. This patch writes straight into VRAM, so the bytes on disk
    must already sit at their physical (swizzled) slot, not their logical index."""
    block, pos = divmod(logical_index, 32)
    if 8 <= pos < 16:
        pos += 8
    elif 16 <= pos < 24:
        pos -= 8
    return block * 32 + pos


def convert(src: Path, dest_dir: Path) -> None:
    im = Image.open(src).convert("RGBA")
    if im.size != (SIZE, SIZE):
        im = im.resize((SIZE, SIZE), Image.LANCZOS)

    palette: dict[tuple[int, int, int, int], int] = {}
    indices = bytearray(SIZE * SIZE)
    for i, rgba in enumerate(im.getdata()):
        idx = palette.get(rgba)
        if idx is None:
            if len(palette) >= MAX_COLORS:
                raise ValueError(f"{src} has more than {MAX_COLORS} unique colors; flatten/quantize it first")
            idx = len(palette)
            palette[rgba] = idx
        indices[i] = idx

    clut = bytearray(MAX_COLORS * 4)
    for (r, g, b, a), idx in palette.items():
        # PS2 GS alpha is 7-bit (0-128); halve the PNG's 0-255 alpha to match.
        phys = _csm1_swizzle(idx)
        clut[phys * 4:phys * 4 + 4] = bytes((r, g, b, a >> 1))

    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / "archipelago-icon.indices").write_bytes(indices)
    (dest_dir / "archipelago-icon.clut").write_bytes(clut)
    print(f"{len(palette)} unique colors -> {dest_dir}")


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else src.parent
    convert(src, dest)

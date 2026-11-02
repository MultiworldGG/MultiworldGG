"""rebuild course_navigation.ips: python build_course_navigation.py /path/to/rgbds"""

from pathlib import Path
import subprocess, re, runpy
import sys, tempfile

project = Path(__file__).resolve().parents[3]
source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
work = tempfile.TemporaryDirectory()
root = Path(work.name)
markers = runpy.run_path(str(project / "worlds/wl/MapData.py"))["MARKERS"]
rows = [(project / "worlds/wl/data/course_navigation.asm").read_text()]
for address, worlds, limit in (
    (0x6BFD, (0, 1, 2), 0x6C33),
    (0x6D2C, (4, 3, 5, 6), 0x6D75),
):
    rows.append(f'SECTION "Course marker data {address:x}", ROMX[${address:04X}], BANK[8]')
    if address == 0x6D2C:
        rows.extend([
            "CourseMarkerPointers:",
            "dw " + ",".join(f"CourseMarkers{world}" for world in range(7)),
        ])
    for world in worlds:
        records = [record for record in markers if record[0] == world]
        rows.extend([f"CourseMarkers{world}:", f"db ${records[0][3]:02X}"])
        for _, course, position, tile in records:
            if tile != records[0][3]:
                assert tile == 0x75
                course |= 0x80
            rows.append(f"db ${course:02X},${position >> 8:02X},${position & 255:02X}")
        rows.append("db $FF")
    rows.append(f"ASSERT @ <= ${limit:04X}")
assembly = root / "navigation.asm"
assembly.write_text("\n".join(rows), encoding="utf-8")
subprocess.run(
    [
        str(source / "rgbasm.exe"),
        "-o",
        str(root / "navigation.o"),
        str(assembly),
    ],
    check=True,
)
subprocess.run(
    [
        str(source / "rgblink.exe"),
        "-o",
        str(root / "navigation.gb"),
        "-m",
        str(root / "navigation.map"),
        str(root / "navigation.o"),
    ],
    check=True,
)
data = (root / "navigation.gb").read_bytes()
ips = bytearray(b"PATCH")
for line in (root / "navigation.map").read_text().splitlines():
    match = re.search(
        r"SECTION: \$([0-9a-fA-F]+)(?:-\$[0-9a-fA-F]+)? \(\$([0-9a-fA-F]+) bytes?\)",
        line,
    )
    if match:
        start, size = (int(v, 16) for v in match.groups())
        start += 0x1C000
        ips += (
            start.to_bytes(3, "big")
            + size.to_bytes(2, "big")
            + data[start : start + size]
        )
ips += b"EOF"
assert len(ips) > 100
out = project / "worlds/wl/data/course_navigation.ips"
out.write_bytes(ips)
print("Built", out, len(ips), "bytes")

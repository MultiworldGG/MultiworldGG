#!/usr/bin/env python3
"""Bundle the TTYD Dolphin Memory Engine native package for frozen builds.

The MWGG freezer compiles Python modules before creating each .apworld, so the
raw DME directory in a frozen ttyd.apworld does not reliably contain the
package's __init__.py and version.py. This tool writes a nested archive that
keeps the complete, cross-platform DME package together for runtime extraction.

To update native binaries from wheel artifacts, run:

    python tools/bundle_dme.py <dir-of-wheels | wheel.whl> [more.whl ...]

To rebuild the archive from the files already in the package, run:

    python tools/bundle_dme.py --archive-only
"""
import shutil
import sys
import zipfile
from pathlib import Path


LIB = Path(__file__).resolve().parent.parent / "lib" / "dolphin_memory_engine_ttyd"
ARCHIVE = LIB.parent / "dolphin_memory_engine_ttyd.zip"


def classify(name: str):
    normalized = name.lower()
    if not normalized.endswith(".whl"):
        return []
    if "win_amd64" in normalized:
        return [("_dolphin_memory_engine.pyd", "_dolphin_memory_engine.pyd")]
    if "macosx" in normalized and "universal2" in normalized:
        return [
            ("_dolphin_memory_engine.abi3.so", "_abi3_macos_arm64.so"),
            ("_dolphin_memory_engine.abi3.so", "_abi3_macos_x86_64.so"),
        ]
    if "macosx" in normalized and "arm64" in normalized:
        return [("_dolphin_memory_engine.abi3.so", "_abi3_macos_arm64.so")]
    if "macosx" in normalized and "x86_64" in normalized:
        return [("_dolphin_memory_engine.abi3.so", "_abi3_macos_x86_64.so")]
    if "x86_64" in normalized and ("manylinux" in normalized or "linux_x86_64" in normalized):
        return [("_dolphin_memory_engine.abi3.so", "_abi3_linux_x86_64.so")]
    return []


def collect(args):
    wheels = []
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            wheels += sorted(path.rglob("*.whl"))
        elif path.suffix == ".whl":
            wheels.append(path)
    return wheels


def extract(wheel: Path, member: str, destination: Path) -> bool:
    with zipfile.ZipFile(wheel) as wheel_zip:
        for candidate in wheel_zip.namelist():
            if candidate.rsplit("/", 1)[-1] == member:
                with wheel_zip.open(candidate) as source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output)
                return True
    return False


def write_archive() -> None:
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(LIB.rglob("*")):
            if "__pycache__" in path.parts:
                continue
            if path.is_file():
                archive.write(path, path.relative_to(LIB.parent))
    print("wrote", ARCHIVE)


def main(argv) -> int:
    archive_only = "--archive-only" in argv
    argv = [arg for arg in argv if arg != "--archive-only"]
    wheels = collect(argv)
    if not wheels and not archive_only:
        print("usage: bundle_dme.py [--archive-only] <dir-of-wheels | wheel.whl> [more.whl ...]")
        return 1

    LIB.mkdir(parents=True, exist_ok=True)
    extracted = 0
    for wheel in wheels:
        targets = classify(wheel.name)
        if not targets:
            print("skip (unrecognized tag):", wheel.name)
            continue
        for member, output_name in targets:
            if extract(wheel, member, LIB / output_name):
                print("bundled", output_name, "<-", wheel.name)
                extracted += 1
            else:
                print("MISSING", member, "in", wheel.name)

    if extracted or archive_only:
        write_archive()
    return 0 if extracted or archive_only else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

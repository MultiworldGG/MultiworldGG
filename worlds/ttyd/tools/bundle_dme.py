#!/usr/bin/env python3
"""Bundle the cibuildwheel abi3 wheels into the apworld's DME lib dir.

The fork (github.com/jamesbrq/py-dolphin-memory-engine) builds one abi3
wheel per platform via .github/workflows/python.yml. Download those
python-package-* artifacts (or build wheels locally) and run:

    python tools/bundle_dme.py <dir-of-wheels | wheel.whl> [more.whl ...]

Each wheel's compiled extension is copied into
lib/dolphin_memory_engine_ttyd/ under the platform-tagged name that
TTYDPatcher._select_native_binary expects. The abi3 binaries work on any
CPython >= 3.9, so one file per platform is all that's needed.
"""
import shutil
import sys
import zipfile
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "lib" / "dolphin_memory_engine_ttyd"


def classify(name: str):
    n = name.lower()
    if not n.endswith(".whl"):
        return []
    if "win_amd64" in n:
        return [("_dolphin_memory_engine.pyd", "_dolphin_memory_engine.pyd")]
    if "macosx" in n and "universal2" in n:
        return [("_dolphin_memory_engine.abi3.so", "_abi3_macos_arm64.so"),
                ("_dolphin_memory_engine.abi3.so", "_abi3_macos_x86_64.so")]
    if "macosx" in n and "arm64" in n:
        return [("_dolphin_memory_engine.abi3.so", "_abi3_macos_arm64.so")]
    if "macosx" in n and "x86_64" in n:
        return [("_dolphin_memory_engine.abi3.so", "_abi3_macos_x86_64.so")]
    if "x86_64" in n and ("manylinux" in n or "linux_x86_64" in n):
        return [("_dolphin_memory_engine.abi3.so", "_abi3_linux_x86_64.so")]
    return []


def collect(args):
    out = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out += sorted(p.rglob("*.whl"))
        elif p.suffix == ".whl":
            out.append(p)
    return out


def extract(whl: Path, member: str, dest: Path) -> bool:
    with zipfile.ZipFile(whl) as z:
        for m in z.namelist():
            if m.rsplit("/", 1)[-1] == member:
                with z.open(m) as s, open(dest, "wb") as o:
                    shutil.copyfileobj(s, o)
                return True
    return False


def main(argv) -> int:
    wheels = collect(argv)
    if not wheels:
        print("usage: bundle_dme.py <dir-of-wheels | wheel.whl> [more.whl ...]")
        return 1
    LIB.mkdir(parents=True, exist_ok=True)
    done = 0
    for whl in wheels:
        targets = classify(whl.name)
        if not targets:
            print("skip (unrecognized tag):", whl.name)
            continue
        for member, out_name in targets:
            if extract(whl, member, LIB / out_name):
                print("bundled", out_name, "<-", whl.name)
                done += 1
            else:
                print("MISSING", member, "in", whl.name)
    return 0 if done else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Reproduce RestrictedCave-Assert failures with --code + seed."""
from __future__ import annotations

import logging
import sys
import traceback

# Cases from automate DB (suite=mystery, error_type=RestrictedCave-Assert)
CASES = {
    "open_lite": {
        "seed": 643606960,
        "code": "SAWQg4A5ILAAIAGIMgmR0Q==",
        "notes": "lite open ow_mixed=0 door_shuffle=crossed",
    },
    "inverted_lite": {
        "seed": 913874356,
        "code": "CBBIgyA5OTMBIAGRIgIRkA==",
        "notes": "lite inverted ow_mixed=0 door_shuffle=vanilla (worst slice ~53%)",
    },
    "district_mixed": {
        "seed": 42440780,
        "code": "SwIgAwA8OewAoAFA0gEJgQ==",
        "notes": "district open ow_mixed=1 door_shuffle=crossed",
    },
}


def main(case_name: str = "open_lite") -> int:
    case = CASES[case_name]
    seed = case["seed"]
    code = case["code"]
    print(f"CASE={case_name} seed={seed} code={code}")
    print(f"notes: {case['notes']}")

    logging.basicConfig(format="%(levelname)s %(message)s", level=logging.INFO)
    for name in ("", "Main", "DoorShuffle", "Fill", "EntranceShuffle", "OverworldShuffle"):
        logging.getLogger(name).setLevel(logging.INFO)

    from CLI import parse_cli
    from Main import main as generate
    from source.classes.BabelFish import BabelFish

    args = parse_cli(
        [
            f"--seed={seed}",
            f"--code={code}",
            "--suppress_rom",
            "--spoiler",
            "none",
            "--skip_playthrough",
            "--loglevel",
            "error",
        ]
    )
    try:
        generate(args=args, seed=seed, fish=BabelFish())
        print("UNEXPECTED SUCCESS")
        return 0
    except Exception as e:
        print("FAILED AS EXPECTED:" if "restricted cave" in str(e).lower() else "FAILED:")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "open_lite"
    if name not in CASES:
        print("available:", ", ".join(CASES))
        raise SystemExit(2)
    raise SystemExit(main(name))

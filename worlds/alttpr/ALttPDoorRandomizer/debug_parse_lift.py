#!/usr/bin/env python3
import json
from pathlib import Path

lift = json.loads(Path("debug_lift_restricted.json").read_text(encoding="utf-8-sig"))
print(
    "error_type:",
    lift.get("error_type"),
    "n=",
    lift.get("n"),
    "errors=",
    lift.get("errors"),
    "baseline=",
    round(lift.get("baseline", 0), 4),
)
rows = lift.get("rows", [])
print("\nTOP LIFTS:")
for r in rows[:30]:
    print(
        f"  {r['setting']}={r['value']}: n={r['n']} err={r['errors']} "
        f"rate={r['rate']:.3%} lift={r['lift']:.2f} p={r['p_value']:.2g}"
    )

print("\nBOTTOM LIFTS:")
for r in rows[-15:]:
    print(
        f"  {r['setting']}={r['value']}: n={r['n']} err={r['errors']} "
        f"rate={r['rate']:.3%} lift={r['lift']:.2f} p={r['p_value']:.2g}"
    )

# shuffle-focused
print("\nSHUFFLE ROWS:")
for r in rows:
    if r["setting"] == "shuffle":
        print(
            f"  {r['value']}: n={r['n']} err={r['errors']} "
            f"rate={r['rate']:.3%} lift={r['lift']:.2f} p={r['p_value']:.2g}"
        )

xt = json.loads(Path("debug_xtab_restricted.json").read_text(encoding="utf-8-sig"))
print("\nCROSSTAB keys:", list(xt.keys()))
for k in ("row_values", "col_values", "rows", "cols", "cells", "matrix", "data"):
    if k in xt:
        v = xt[k]
        if isinstance(v, list) and len(v) > 20:
            print(k, "len", len(v), "sample", v[:3])
        else:
            print(k, ":", v)

runs = json.loads(Path("debug_runs_restricted.json").read_text(encoding="utf-8-sig"))
print("\nRUNS total", runs.get("total"))
for r in runs.get("runs", [])[:5]:
    print(r)

#!/usr/bin/env python3
"""One-off triage for RestrictedCave-Assert failures."""
import sqlite3
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(r"L:\_Work\Zelda\ROMs\Bug\Automate\log.db")

print("DB:", DB_PATH)
print("exists:", DB_PATH.exists())
conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("\n=== RestrictedCave-Assert counts ===")
row = cur.execute(
    """
    SELECT COUNT(*) AS n,
      MIN(datetime(timestamp,'unixepoch','localtime')) AS first,
      MAX(datetime(timestamp,'unixepoch','localtime')) AS last,
      ROUND(AVG(duration_ms)/1000.0,1) AS avg_sec
    FROM suite_runs WHERE error_type=?
    """,
    ("RestrictedCave-Assert",),
).fetchone()
print(dict(row))

print("\n=== by suite ===")
for row in cur.execute(
    """
    SELECT COALESCE(suite,'(null)') AS suite, COUNT(*) AS n
    FROM suite_runs WHERE error_type=?
    GROUP BY 1 ORDER BY n DESC
    """,
    ("RestrictedCave-Assert",),
):
    print(dict(row))

print("\n=== which assert site (main vs dungeonsfull) ===")
for label, needle in (
    ("main", "(main)"),
    ("dungeonsfull", "(dungeonsfull)"),
    ("other", None),
):
    if needle:
        n = cur.execute(
            """
            SELECT COUNT(*) FROM suite_runs
            WHERE error_type=? AND log LIKE ?
            """,
            ("RestrictedCave-Assert", f"%{needle}%"),
        ).fetchone()[0]
    else:
        n = cur.execute(
            """
            SELECT COUNT(*) FROM suite_runs
            WHERE error_type=?
              AND (log IS NULL OR (log NOT LIKE '%(main)%' AND log NOT LIKE '%(dungeonsfull)%'))
            """,
            ("RestrictedCave-Assert",),
        ).fetchone()[0]
    print(f"  {label}: {n}")

print("\n=== settings correlation ===")
for row in cur.execute(
    """
    SELECT s.shuffle AS er, s.door_shuffle, s.intensity, s.mode, s.logic,
      s.ow_layout, s.ow_crossed, s.ow_mixed, s.ow_parallel,
      s.shufflelinks, s.shuffletavern,
      COUNT(*) AS n
    FROM suite_runs r
    JOIN suite_settings s
      ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
    WHERE r.error_type=?
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11
    ORDER BY n DESC
    LIMIT 40
    """,
    ("RestrictedCave-Assert",),
):
    print(dict(row))

print("\n=== lift vs baseline: shuffle ===")
for row in cur.execute(
    """
    WITH base AS (
      SELECT s.shuffle AS v, COUNT(*) AS attempts, SUM(CASE WHEN r.success=0 THEN 1 ELSE 0 END) AS fails
      FROM suite_runs r
      JOIN suite_settings s ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
      GROUP BY 1
    ),
    err AS (
      SELECT s.shuffle AS v, COUNT(*) AS n
      FROM suite_runs r
      JOIN suite_settings s ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
      WHERE r.error_type=?
      GROUP BY 1
    )
    SELECT e.v, e.n AS err_n, b.attempts, b.fails,
      ROUND(100.0*e.n/b.attempts, 3) AS err_pct,
      ROUND(100.0*b.fails/b.attempts, 2) AS fail_pct
    FROM err e JOIN base b ON b.v=e.v
    ORDER BY err_pct DESC
    """,
    ("RestrictedCave-Assert",),
):
    print(dict(row))

# Dimension lifts for a few key columns
dims = [
    "shuffle", "door_shuffle", "mode", "logic", "ow_layout", "ow_crossed",
    "ow_mixed", "ow_parallel", "intensity", "shufflelinks", "shuffletavern",
]
print("\n=== per-dimension err rate (min 5 errs or top) ===")
for dim in dims:
    print(f"\n-- {dim} --")
    rows = cur.execute(
        f"""
        WITH base AS (
          SELECT s.{dim} AS v, COUNT(*) AS attempts
          FROM suite_runs r
          JOIN suite_settings s ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
          GROUP BY 1
        ),
        err AS (
          SELECT s.{dim} AS v, COUNT(*) AS n
          FROM suite_runs r
          JOIN suite_settings s ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
          WHERE r.error_type=?
          GROUP BY 1
        )
        SELECT e.v, e.n AS err_n, b.attempts,
          ROUND(100.0*e.n/NULLIF(b.attempts,0), 3) AS err_pct
        FROM err e JOIN base b ON b.v IS e.v OR (b.v IS NULL AND e.v IS NULL)
        ORDER BY err_pct DESC, err_n DESC
        """,
        ("RestrictedCave-Assert",),
    ).fetchall()
    for row in rows[:12]:
        print(dict(row))

print("\n=== recent samples ===")
for row in cur.execute(
    """
    SELECT id, seed, suite, settings_code, settings_ver,
      datetime(timestamp,'unixepoch','localtime') AS when_local,
      duration_ms, log
    FROM suite_runs
    WHERE error_type=?
    ORDER BY id DESC
    LIMIT 5
    """,
    ("RestrictedCave-Assert",),
):
    print("---")
    d = dict(row)
    log = d.pop("log") or ""
    print(d)
    # keep traceback-ish tail
    lines = log.strip().splitlines()
    print("LOG TAIL:")
    print("\n".join(lines[-25:]))

print("\n=== overall failure mix (top) ===")
for row in cur.execute(
    """
    SELECT COALESCE(stage,'(null)') AS stage,
           COALESCE(error_type,'(null)') AS error_type,
           COUNT(*) AS n
    FROM suite_runs
    WHERE success=0
    GROUP BY 1,2
    ORDER BY n DESC
    LIMIT 20
    """
):
    print(dict(row))

print("\n=== shuffle x ow_mixed rates ===")
for row in cur.execute(
    """
    SELECT s.shuffle, s.ow_mixed, COUNT(*) AS attempts,
      SUM(CASE WHEN r.error_type='RestrictedCave-Assert' THEN 1 ELSE 0 END) AS err_n,
      ROUND(100.0*SUM(CASE WHEN r.error_type='RestrictedCave-Assert' THEN 1 ELSE 0 END)/COUNT(*),2) AS err_pct
    FROM suite_runs r
    JOIN suite_settings s
      ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
    WHERE s.shuffle IN ('lite','district','simple','dungeonssimple','lean','full','crossed','restricted','swapped')
    GROUP BY 1,2
    ORDER BY err_pct DESC, attempts DESC
    """
):
    print(dict(row))

print("\n=== lite-only mode x ow_mixed ===")
for row in cur.execute(
    """
    SELECT s.mode, s.ow_mixed, COUNT(*) AS attempts,
      SUM(CASE WHEN r.error_type='RestrictedCave-Assert' THEN 1 ELSE 0 END) AS err_n,
      ROUND(100.0*SUM(CASE WHEN r.error_type='RestrictedCave-Assert' THEN 1 ELSE 0 END)/COUNT(*),2) AS err_pct
    FROM suite_runs r
    JOIN suite_settings s
      ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
    WHERE s.shuffle='lite'
    GROUP BY 1,2
    ORDER BY err_pct DESC
    """
):
    print(dict(row))

print("\n=== one lite repro row with settings ===")
row = cur.execute(
    """
    SELECT r.id, r.seed, r.settings_code, r.settings_ver,
           s.shuffle, s.mode, s.ow_mixed, s.ow_layout, s.ow_crossed, s.ow_parallel,
           s.door_shuffle, s.intensity, s.logic, s.shufflelinks, s.shuffletavern
    FROM suite_runs r
    JOIN suite_settings s
      ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
    WHERE r.error_type='RestrictedCave-Assert' AND s.shuffle='lite'
    ORDER BY r.id DESC
    LIMIT 1
    """
).fetchone()
print(dict(row) if row else None)

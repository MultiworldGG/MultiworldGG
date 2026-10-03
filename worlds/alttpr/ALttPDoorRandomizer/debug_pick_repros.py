#!/usr/bin/env python3
import sqlite3

c = sqlite3.connect(r"L:\_Work\Zelda\ROMs\Bug\Automate\log.db")
c.row_factory = sqlite3.Row

queries = {
    "inverted lite ow_mixed=0": """
        SELECT r.id, r.seed, r.settings_code, s.mode, s.ow_mixed, s.ow_layout,
               s.ow_crossed, s.door_shuffle, s.intensity, s.logic, s.shufflelinks, s.shuffletavern
        FROM suite_runs r
        JOIN suite_settings s ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
        WHERE r.error_type='RestrictedCave-Assert'
          AND s.shuffle='lite' AND s.mode='inverted' AND s.ow_mixed=0
        ORDER BY r.id DESC LIMIT 3
    """,
    "district ow_mixed=1": """
        SELECT r.id, r.seed, r.settings_code, s.mode, s.ow_mixed, s.ow_layout,
               s.ow_crossed, s.door_shuffle, s.intensity, s.logic, s.shufflelinks, s.shuffletavern
        FROM suite_runs r
        JOIN suite_settings s ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
        WHERE r.error_type='RestrictedCave-Assert'
          AND s.shuffle='district' AND s.ow_mixed=1
        ORDER BY r.id DESC LIMIT 3
    """,
    "open lite ow_mixed=0 (recent)": """
        SELECT r.id, r.seed, r.settings_code, s.mode, s.ow_mixed, s.ow_layout,
               s.ow_crossed, s.door_shuffle, s.intensity, s.logic, s.shufflelinks, s.shuffletavern
        FROM suite_runs r
        JOIN suite_settings s ON s.settings_code=r.settings_code AND s.settings_ver=r.settings_ver
        WHERE r.error_type='RestrictedCave-Assert'
          AND s.shuffle='lite' AND s.mode='open' AND s.ow_mixed=0
        ORDER BY r.id DESC LIMIT 3
    """,
}

for title, q in queries.items():
    print("===", title, "===")
    for row in c.execute(q):
        print(dict(row))
    print()

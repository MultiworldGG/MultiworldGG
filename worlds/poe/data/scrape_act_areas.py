#!/usr/bin/env python3
"""Scrape act area progression data from poewiki.net and output JSON."""

import json
import re
import urllib.request
from html import unescape


def fetch_act(act: int) -> list[dict]:
    url = f"https://www.poewiki.net/wiki/Act_{act}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode("utf-8")

    prog_start = content.find('id="Progression"')
    if prog_start == -1:
        return []
    # Grab everything up to the next section heading to catch multiple tables
    next_section = content.find("<h2", prog_start + 1)
    section = content[prog_start:next_section] if next_section != -1 else content[prog_start:]

    seen = set()
    areas = []
    for td_match in re.finditer(r"<td[^>]*border[^>]*>(.*?)</td>", section, re.DOTALL):
        td_content = td_match.group(1)

        link = re.search(r'<a[^>]*title="([^"]+)"', td_content)
        if not link:
            continue

        area_name = unescape(link.group(1))
        area_name = re.sub(r"\s*\(Act \d+\)", "", area_name).strip()

        if area_name in seen:
            continue
        seen.add(area_name)

        level_match = re.search(r"<br\s*/?>\s*(\d+)", td_content)
        area_level = int(level_match.group(1)) if level_match else 0

        areas.append({"areaLevel": area_level, "act": act, "areaName": area_name})

    return areas


def main():
    all_areas = []
    for act in range(1, 11):
        #print(f"Fetching Act {act}...", flush=True)
        all_areas.extend(fetch_act(act))

    print(json.dumps(all_areas, indent=4))


if __name__ == "__main__":
    main()

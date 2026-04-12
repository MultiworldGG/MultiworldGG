import csv

with open("locations.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

rows.sort(
    key=lambda r: (r["logical region"], int(r["id"]))
)

param_table = {
    "drop": "CHR",
    "reward/pickup": "OTHER",
    "shop": "SHOP"
}

current_region = None
print("locations_by_region: Dict[str, List[LocationData]] = {")
for row in rows:
    region = row["logical region"]
    if current_region != region:
        if current_region != None:
            print("    ],")
        current_region = region
        print(f"    \"{current_region}\": [")

    ingame_id = row["ingame id"]
    name = row["final name"]
    table = param_table[row["type"]]

    line = ""

    if row["done"] == "TRUE": line += "        "
    else: line += "        # "

    table_str = f"{table},"
    id_str = f"{ingame_id},"
    name_str = f"\"{name}\""
    line += f"LocationData({table_str.ljust(6)} {id_str} {name_str}"

    if row["version"] == "sotfs": line += ", sotfs=True"
    elif row["version"] == "vanilla": line += ", vanilla=True"
    if row["missable"] == "TRUE" and row["done"] == "TRUE": line += ", missable=True"
    if row["keep original item"] == "TRUE": line += ", keep_original_item=True"

    print(line+"),")

print("    ],")
print("}")

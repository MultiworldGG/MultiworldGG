import csv

with open("items.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

rows.sort(
    key=lambda r: (int(r["ID"]))
)

current_region = None
print("item_list: list[ItemData] = [")
for row in rows:
    ingame_id = row["ID"]
    name = row["Name"]
    classification = row["ItemClassification"]
    category = row["Category Name"].upper().replace(" ", "_")

    line = ""

    if row["dont add"] == "TRUE": line += "    # "
    else: line += "    "

    name_str = f"\"{name}\","
    id_str = ingame_id + ","
    line += f"ItemData({id_str.ljust(9)} {name_str.ljust(54)} ItemCategory.{category}"

    max_reinforcemnet = row["Max Reinforcement"]
    if max_reinforcemnet != "-1":
        line += f", max_reinforcement={max_reinforcemnet}"

    if classification != "filler":
        line += f", classification=ItemClassification.{classification}"
        
    if row["version"] == "sotfs": line += ", sotfs=True"
    elif row["version"] == "vanilla": line += ", vanilla=True"

    if row["Skip"] == "TRUE": line += ", skip=True"

    print(line+"),")

print("]")

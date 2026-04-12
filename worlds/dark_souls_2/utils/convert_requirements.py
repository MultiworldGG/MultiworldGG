import csv

with open("locations.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

rows.sort(
    key=lambda r: (r["logical region"], int(r["id"]))
)

current_region = None
for row in rows:
    region = row["logical region"]
    if current_region != region:
        current_region = region
        print(f"    # {current_region}")

    if not row["requirements"]: continue
    if row["done"] == "FALSE": continue
    line = f"    RuleData(\"{row["final name"]}\", \"{row["requirements"]}\""
    if row["version"] == "sotfs": line += ", version=DS2Version.SOTFS"
    elif row["version"] == "vanilla": line += ", version=DS2Version.VANILLA"
    line += "),"
    print(line)

with open("../locations.py") as file, open("result.txt", "w") as output:
    inside = False
    region = None

    for line in file:
        if "locations_by_region:" in line:
            inside = True

        if line == "}\n" and inside:
            inside = False

        if not inside:
            continue

        if "LocationData(" in line and not line.strip().startswith("#"):
            location = line.split("\"")[1]
            formatted = f"{{\"@{region}/{location}/\"}},\n"
            print(formatted, end="")
            output.write(formatted)

        elif ": [" in line:
            region = line.split("\"")[1]
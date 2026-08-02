import yaml

with open("entrances.yaml", "r") as file:
    ent = yaml.safe_load(file)
with open("rooms.yaml", "r") as file:
    rooms = yaml.safe_load(file)
with open("entrancespairs.yaml", "r") as file:
    ep = yaml.safe_load(file)
with open("shufflingdata.yaml", "r") as file:
    sd = yaml.safe_load(file)

with open("rooms.py", "w") as file:
    file.write("rooms = " + str(rooms) + "\n" + "entrances = " + str(ent) + "\n" + "entrances_pairs = " + str(ep) + "\nshuffling_data = " + str(sd))
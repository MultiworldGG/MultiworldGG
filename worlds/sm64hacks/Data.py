from typing import List, Tuple, Set
from pathlib import Path
from importlib import resources
from importlib.resources.abc import Traversable
from .Updater import update_jsons
import pkgutil
import Utils
import json
import re
import os
import shutil

sm64hack_items: Tuple[str, ...] = (
    "Key 1", 
    "Key 2", 
    "Wing Cap", 
    "Vanish Cap", 
    "Metal Cap", 
    "Castle Moat",
    "Power Star",
    "Progressive Key", 
    "Course 1 Cannon",
    "Course 2 Cannon",
    "Course 3 Cannon",
    "Course 4 Cannon",
    "Course 5 Cannon",
    "Course 6 Cannon",
    "Course 7 Cannon",
    "Course 8 Cannon",
    "Course 9 Cannon",
    "Course 10 Cannon",
    "Course 11 Cannon",
    "Course 12 Cannon",
    "Course 13 Cannon",
    "Course 14 Cannon",
    "Course 15 Cannon",
    "Bowser 1 Cannon",
    "Bowser 2 Cannon",
    "Bowser 3 Cannon",
    "Slide Cannon",
    "Secret 1 Cannon",
    "Secret 2 Cannon",
    "Secret 3 Cannon",
    "Metal Cap Cannon",
    "Wing Cap Cannon",
    "Vanish Cap Cannon",
    "Overworld Cannon",
    "Progressive Stomp Badge",
    "Wall Badge",
    "Triple Jump Badge",
    "Lava Badge",
    "Overworld Cannon Star",
    "Bowser 2 Cannon Star",
    "Yellow Switch",
    "Black Switch",
    "Coin",
    "Green Demon Trap",
    "Mario Choir",
    "Heave-Ho Trap",
    "Squish Trap",
    "Spin Trap",
    "Tempo Trap",
    "Course 1 Ticket",
    "Course 2 Ticket",
    "Course 3 Ticket",
    "Course 4 Ticket",
    "Course 5 Ticket",
    "Course 6 Ticket",
    "Course 7 Ticket",
    "Course 8 Ticket",
    "Course 9 Ticket",
    "Course 10 Ticket",
    "Course 11 Ticket",
    "Course 12 Ticket",
    "Course 13 Ticket",
    "Course 14 Ticket",
    "Course 15 Ticket",
    "Bowser 1 Ticket",
    "Bowser 2 Ticket",
    "Bowser 3 Ticket",
    "Slide Ticket",
    "Secret 1 Ticket",
    "Secret 2 Ticket",
    "Secret 3 Ticket",
    "Metal Cap Ticket",
    "Wing Cap Ticket",
    "Vanish Cap Ticket",
    "Overworld Ticket",
    "Progressive Jump",
    "Backflip",
    "Sideflip",
    "Wallkick",
    "Long Jump",
    "Dive",
    "Ground Pound",
    "Kick",
    "Punch",
    "Slidekick",
    "Shell",
    "Star Bundle",
    "Blue Star",
    "Blue Star Bundle",
    "Gray Switch",
    "1-Up Mushroom",
    "5% 100-coin star discount",
    "Cap Timer Extension",
    "Temporary Metal Cap",
    "Temporary Vanish Cap",
    "Cap Timer Extension",
    "+1 Wallkick Frame",
    "Steve"
)
tickets: Set[str] = {
    "Course 1 Cannon",
    "Course 2 Cannon",
    "Course 3 Cannon",
    "Course 4 Cannon",
    "Course 5 Cannon",
    "Course 6 Cannon",
    "Course 7 Cannon",
    "Course 8 Cannon",
    "Course 9 Cannon",
    "Course 10 Cannon",
    "Course 11 Cannon",
    "Course 12 Cannon",
    "Course 13 Cannon",
    "Course 14 Cannon",
    "Course 15 Cannon",
    "Bowser 1 Cannon",
    "Bowser 2 Cannon",
    "Bowser 3 Cannon",
    "Slide Cannon",
    "Secret 1 Cannon",
    "Secret 2 Cannon",
    "Secret 3 Cannon",
    "Metal Cap Cannon",
    "Wing Cap Cannon",
    "Vanish Cap Cannon",
    "Overworld Cannon"
}
fullmoves: Set[str] = {
    "Progressive Jump",
    "Backflip",
    "Sideflip",
    "Wallkick",
    "Long Jump",
    "Dive",
    "Ground Pound",
    "Kick",
    "Punch",
    "Slidekick",
    "Shell"
}
cannons: Set[str] = {
    "Course 1 Cannon",
    "Course 2 Cannon",
    "Course 3 Cannon",
    "Course 4 Cannon",
    "Course 5 Cannon",
    "Course 6 Cannon",
    "Course 7 Cannon",
    "Course 8 Cannon",
    "Course 9 Cannon",
    "Course 10 Cannon",
    "Course 11 Cannon",
    "Course 12 Cannon",
    "Course 13 Cannon",
    "Course 14 Cannon",
    "Course 15 Cannon",
    "Bowser 1 Cannon",
    "Bowser 2 Cannon",
    "Bowser 3 Cannon",
    "Slide Cannon",
    "Secret 1 Cannon",
    "Secret 2 Cannon",
    "Secret 3 Cannon",
    "Metal Cap Cannon",
    "Wing Cap Cannon",
    "Vanish Cap Cannon",
    "Overworld Cannon",
}
badge_items: Set[str] = {
    "Progressive Stomp Badge",
    "Wall Badge",
    "Triple Jump Badge",
    "Lava Badge"
}


moves: Tuple[str, ...] = (
    "Backflip",
    "Sideflip",
    "Long Jump",
    "Dive",
    "Ground Pound",
    "Kick",
    "Punch",
    "Slidekick",
    "Shell"
)

traps: Tuple[str, ...] = (
    "Green Demon Trap",
    "Mario Choir",
    "Heave-Ho Trap",
    "Squish Trap",
    "Spin Trap",
    "Tempo Trap"
)

junk: Tuple[str, ...] = (
    "Coin",
    "1-Up Mushroom"
)

useful: Tuple[str, ...] = (
    "5% 100-coin star discount",
    "Cap Timer Extension",
    "+1 Wallkick Frame"
)

badges: Tuple[str, ...] = (
    "Super Badge",
    "Ultra Badge",
    "Wall Badge",
    "Triple Jump Badge",
    "Lava Badge"
)

star_like: Tuple[str, ...] = (
    "Power Star",
    "Overworld Cannon Star",
    "Bowser 2 Cannon Star"
)

c1 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c2 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c3 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c4 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c5 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c6 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c7 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c8 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c9 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c10 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c11 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c12 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c13 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c14 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c15 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]

b1 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
b2 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
b3 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]

slide = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
s1 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
s2 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
s3 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]

mc = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
wc = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
vc = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]

ow = [{"exists": True}, {"exists": True}, {"exists": True, "StarRequirement":15}, {"exists": True, "StarRequirement":50}, {"exists": True, "StarRequirement":25}, {"exists": True, "StarRequirement":35}, {"exists": True, "StarRequirement":10}]

other = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "StarRequirement":50}]


sr6_25_locations = ( #special = hack-specific
    "Yellow Switch",
    "Bowser Fight Reds",
    "Star 210",
    "Toursome Trouble RT Star 1",
    "Toursome Trouble RT Star 2",
    "Toursome Trouble RT Star 3",
    "Toursome Trouble RT Star 4",
    "Toursome Trouble RT Star 5",
    "Toursome Trouble RT Star 6",
)

def find_json_files(directory: Traversable):
    if directory.is_file() and directory.endswith("json"):
        return directory
    if directory.is_dir():
        ret = []

def create_json_folders(auto_update):
    json_dir = os.path.join(Utils.user_path(), "sm64hack_jsons")
    custom_json_dir = os.path.join(json_dir, "custom_jsons")
    downloaded_json_dir = os.path.join(json_dir, "downloaded_jsons")
    os.makedirs(json_dir, exist_ok=True)
    if not os.path.exists(custom_json_dir): #new install and/or update from before 0.4.4
        files = os.listdir(json_dir)
        os.makedirs(custom_json_dir, exist_ok=True)
        for file in files:
            shutil.move(os.path.join(json_dir, file), os.path.join(json_dir, "custom_jsons", file))

    
    os.makedirs(downloaded_json_dir, exist_ok=True)
    if(auto_update):
        update_jsons()

class Data:
    #default locations for location_name_to_id, will be overritten by import_json
    locations = {
        "Course 1": {"Stars": c1, "StarRequirement": 0,},
        "Course 2": {"Stars": c2, "StarRequirement": 0,},
        "Course 3": {"Stars": c3, "StarRequirement": 0,},
        "Course 4": {"Stars": c4, "StarRequirement": 10,},
        "Course 5": {"Stars": c5, "StarRequirement": 10,},
        "Course 6": {"Stars": c6, "StarRequirement": 0,},
        "Course 7": {"Stars": c7, "StarRequirement": 20,},
        "Course 8": {"Stars": c8, "StarRequirement": 20,},
        "Course 9": {"Stars": c9, "StarRequirement": 20,},
        "Course 10": {"Stars": c10, "StarRequirement": 0,},
        "Course 11": {"Stars": c11, "StarRequirement": 40,},
        "Course 12": {"Stars": c12, "StarRequirement": 40,},
        "Course 13": {"Stars": c13, "StarRequirement": 40,},
        "Course 14": {"Stars": c14, "StarRequirement": 75, "Requirements": ["Metal Cap"]},
        "Course 15": {"Stars": c15, "StarRequirement": 100,},
        "Bowser 1": {"Stars": b1, "StarRequirement": 20,},
        "Bowser 2": {"Stars": b2, "StarRequirement": 33,},
        "Bowser 3": {"Stars": b3, "StarRequirement": 80, "Requirements": ["Metal Cap"]},
        "Slide": {"Stars": slide, "StarRequirement": 20,},
        "Secret 1": {"Stars": s1, "StarRequirement": 80, "Requirements": ["Metal Cap"]},
        "Secret 2": {"Stars": s2, "StarRequirement": 80, "Requirements": ["Metal Cap"]},
        "Secret 3": {"Stars": s3, "StarRequirement": 0,},
        "Metal Cap": {"Stars": mc, "StarRequirement": 33,},
        "Wing Cap": {"Stars": wc, "StarRequirement": 100,},
        "Vanish Cap": {"Stars": vc, "StarRequirement": 50},
        "Overworld": {"Stars": ow, "StarRequirement": 0},
        "Other": {"Stars": other, "StarRequirement": 0} 
        #Other represents the keys + caps; the "star" ids 1 and 2 are keys 1 and 2, and 3-5 are wing, vanish, and metal cap
        #respectively
    }


    def import_json(self, file_name):
        json_dir = os.path.join(Utils.user_path(), "sm64hack_jsons")
        custom_json_dir = os.path.join(json_dir, "custom_jsons")
        downloaded_json_dir = os.path.join(json_dir, "downloaded_jsons")

        json_file = list(Path(custom_json_dir).rglob(file_name)) #custom takes priority over downloaded
        if json_file == []:
            json_file = list(Path(downloaded_json_dir).rglob(file_name))
        if len(json_file) > 1:
            raise ValueError("Multiple JSON files with the same name detected")
        if len(json_file) == 0:
            raise FileNotFoundError(f"JSON file {file_name} does not exist")
        json_file = json_file[0]
        #print(json_file)
        with open(json_file, 'r') as infile:
            filetext = infile.read()
            self.maxstarcount = max(int(i) for i in re.findall(r"\|Stars:(\d+)\|", filetext))
            self.locations = json.loads(filetext)
            if self.locations["Other"]["Settings"].get("Entrances"):
                self.progression_courses = set() 
                for entrance in self.locations["Other"]["Entrances"]:
                    self.progression_courses |= set((entrance[0], entrance[2]))
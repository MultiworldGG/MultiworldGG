from typing import List
import json


sm64hack_items: List[str] = [
    "Key 1", 
    "Key 2", 
    "Wing Cap", 
    "Vanish Cap", 
    "Metal Cap", 
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
    "Lava Badge"
] 

badges: List[str] = [
    "Super Badge",
    "Ultra Badge",
    "Wall Badge",
    "Triple Jump Badge",
    "Lava Badge"
]

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

    def import_json(self, file):
        with open("data/sm64hacks/" + file) as infile:
            self.locations = json.load(infile)






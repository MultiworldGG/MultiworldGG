from functools import lru_cache
from BaseClasses import Location
from typing import List
from .Options import SM64HackOptions
from .Data import sm64hack_items, Data, badges, sr6_25_locations
from .Requirements import check_if_location_exists

class SM64HackLocation(Location):
    game = "SM64 Romhack"

    # override constructor to automatically mark event locations as such
    def __init__(self, player: int, name = "", code = None, parent = None):
        super(SM64HackLocation, self).__init__(player, name, code, parent)
        self.event = code is None

@lru_cache(maxsize=None)
def location_names(data = Data()) -> List[str]:
    output: List[str] = []
    for course, info in data.locations.items():
        
        if(course == "Other"):
            for itemId in range(5):
                output.append(sm64hack_items[itemId])
                output.append(badges[itemId])
            continue
        for star in range(8): #generates locations for each possible star in each level
            output.append(f"{course} Star {star + 1}")
            if star != 7:
                output.append(f"{course} Blue Star {star + 1}")
        output.append(f"{course} Cannon")
        output.append(f"{course} Troll Star")
        output.append(f"{course} Sign")
    
    output.append("Black Switch") #star revenge 3.5
    output.extend(sr6_25_locations)
    output.append("Castle Moat")
    output.append(f"Gray Switch")

    return output

def location_names_that_exist(data: Data, options:SM64HackOptions) -> List[str]:
    output: List[str] = []
    macros = data.locations["Other"]["Macros"]
    for course, info in data.locations.items():
        if(course == "Other"):
            for itemId in range(5):
                if info["Stars"][itemId].get("exists") and check_if_location_exists(info["Stars"][itemId].get("Requirements"), options, macros, data):
                    output.append(sm64hack_items[itemId])
            if "sr7" in data.locations["Other"]["Settings"]:
                for itemId in range(5):
                    if(info["Stars"][itemId + 7].get("exists") and check_if_location_exists(info["Stars"][itemId + 7].get("Requirements"), options, macros, data)):
                        output.append(badges[itemId])
            continue
        for star in range(8): #generates locations for each possible star in each level
            try:
                if "decadeslater" in data.locations["Other"]["Settings"]:
                    if star == 7:
                        continue
                    if info["Stars"][star].get("exists") and check_if_location_exists(info["Stars"][star].get("Requirements"), options, macros, data):
                        output.append(f"{course} Star {star + 1}")
                    if info["Stars"][star+7].get("exists") and check_if_location_exists(info["Stars"][star+7].get("Requirements"), options, macros, data):
                        output.append(f"{course} Blue Star {star + 1}")
                else:
                    if info["Stars"][star].get("exists") and check_if_location_exists(info["Stars"][star].get("Requirements"), options, macros, data):
                        output.append(f"{course} Star {star + 1}")
            except IndexError:
                data.locations[course]["Stars"].append({"exists": False}) #so i dont need to do this try except block later
        if(info["Cannon"].get("exists") and check_if_location_exists(info["Cannon"].get("Requirements"), options, macros, data)):
            output.append(f"{course} Cannon")
        if info.get("Troll Star") is None:
            info["Troll Star"] = {"exists": False}
        if(info["Troll Star"].get("exists") and options.troll_stars > 0 and check_if_location_exists(info["Troll Star"].get("Requirements"), options, macros, data)):
            output.append(f"{course} Troll Star")
        if(info["Sign"].get("exists") and options.sign_randomization and check_if_location_exists(info["Sign"].get("Requirements"), options, macros, data)):
            output.append(f"{course} Sign")
        
    moatexists = check_if_location_exists(data.locations["Other"]["Stars"][5].get("Requirements"), options, macros, data)
    if "sr3.5" in data.locations["Other"]["Settings"] and moatexists:
        output.append("Black Switch")
    elif "sr6.25" in data.locations["Other"]["Settings"] and moatexists:
        output.extend(sr6_25_locations)
    elif "decadeslater" in data.locations["Other"]["Settings"] and moatexists:
        output.append("Gray Switch")
    elif data.locations["Other"]["Stars"][5].get("exists") and moatexists:
        output.append("Castle Moat") #at the end for now to avoid client troubles
    

    return output
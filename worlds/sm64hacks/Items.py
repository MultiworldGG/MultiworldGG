from BaseClasses import Item
from .Locations import location_names
from .Data import Data


class SM64HackItem(Item):
    game = "SM64 Romhack" 

def star_count(data):
    return len(["Star" for location in location_names(data) if "Star" in location])

def item_is_important(item_name, data = Data()):
    datastring = str(data.locations)
    if item_name == "Progressive Key":
        return item_is_important("Key 1", data) or item_is_important("Key 2", data)
    if item_name == "Progressive Stomp Badge":
        return item_is_important("Super Badge", data) or item_is_important("Ultra Badge", data) #i very much doubt this will EVER be false because in sr7/sr7.5 its importand but just in case to be 100% sure someone isnt making an edit of sr7 or something
    if item_name == "Progressive Jump": #if being able to jump somehow is not progression in a hack i will be surprised and i cba to do this properly because of that
        return True
    
    return f"|{item_name}|" in datastring
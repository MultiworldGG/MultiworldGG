from typing import TYPE_CHECKING

from BaseClasses import Region, Entrance, ItemClassification, CollectionState
from .Locations import location_table, ApeEscapeLocation
from .Strings import AEDoor, AELocation, AEItem
from .Items import ApeEscapeItem
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from . import ApeEscapeWorld


class ApeEscapeLevel:
    # Example call: level = ApeEscapeLevel("Fossil Field", 0x01, 0)
    def __init__(self, name, entrance, vanillapos):
        self.name = name # Level Name (plaintext)
        self.bytes = [] # Level name converted to List of bytes
        # order 3 + entrance 0x01 = the third level is Fossil Field
        self.entrance = entrance # The ID of the level being entered
        self.keys = -1 # The number of required keys to enter this level
        self.vanillapos = vanillapos # The order the levels normally appear
        self.newpos = -1 # The order the levels will appear after shuffling

    def __lt__(self, comp):
        return self.vanillapos < comp.vanillapos

    # Creates an event item in a specified region. Thanks Aquaria for having a good template!
    # Example call: __add_event_location(self, self.get_region(AEDoor.DR_OUTSIDE_OBELISK_TOP.value), "Dark Ruins - Floor Broken", "DR-Block")
def __add_event_location(self, region: Region, name: str, event_name: str) -> None:
    location: ApeEscapeLocation = ApeEscapeLocation(self.player, name, None, region)
    region.locations.append(location)
    location.place_locked_item(ApeEscapeItem(event_name, ItemClassification.progression, None, self.player))

    # Create all needed event items for checking access.


def create_event_items(self):
    # Buttons and state changes.
    __add_event_location(self, self.get_region(AEDoor.DR_OUTSIDE_OBELISK_TOP.value),
                         "Dark Ruins - Floor Broken", "DR-Block")
    __add_event_location(self, self.get_region(AEDoor.DI_SLIDE_ROOM_GALLERY.value),
                         "Dexter's Island - Button Reached", "DI-Button")
    __add_event_location(self, self.get_region(AEDoor.CC_BASEMENT_BUTTON_DOWN.value),
                         "Crumbling Castle - Button Reached", "CC-Button")
    __add_event_location(self, self.get_region(AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value),
                         "Monkey Madness - Spawn UFOs", "MM-UFOs")
    __add_event_location(self, self.get_region(AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value),
                         "Monkey Madness - Monkey Head Room", "MM-Button")
    __add_event_location(self, self.get_region(AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value),
                         "Monkey Madness - Specter 1 Open", "MM-Painting")
    # Monkey Madness UFO monkeys - specifically for the door.
    __add_event_location(self, self.get_region(AELocation.W9L1Donovan.value),
                         "Monkey Madness UFO Monkey 1", "MM UFO Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Laura.value),
                         "Monkey Madness UFO Monkey 2", "MM UFO Monkey")

    # ''' Event items for monkeys - mostly useful for debugging. NOTE: Add "# " to the beginning to uncomment.
    # Monkeys by level, for lamps and Specter 2 vanilla condition.
    # Fossil Field
    __add_event_location(self, self.get_region(AELocation.W1L1Noonan.value), "Fossil Field Monkey 1", "FF Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L1Jorjy.value), "Fossil Field Monkey 2", "FF Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L1Nati.value), "Fossil Field Monkey 3", "FF Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L1TrayC.value), "Fossil Field Monkey 4", "FF Monkey")
    # Primordial Ooze
    __add_event_location(self, self.get_region(AELocation.W1L2Shay.value), "Primordial Ooze Monkey 1", "PO Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L2DrMonk.value), "Primordial Ooze Monkey 2", "PO Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L2Grunt.value), "Primordial Ooze Monkey 3", "PO Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L2Ahchoo.value), "Primordial Ooze Monkey 4", "PO Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L2Gornif.value), "Primordial Ooze Monkey 5", "PO Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L2Tyrone.value), "Primordial Ooze Monkey 6", "PO Monkey")
    # Molten Lava
    __add_event_location(self, self.get_region(AELocation.W1L3Scotty.value), "Molten Lava Monkey 1", "ML Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L3Coco.value), "Molten Lava Monkey 2", "ML Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L3JThomas.value), "Molten Lava Monkey 3", "ML Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L3Mattie.value), "Molten Lava Monkey 4", "ML Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L3Barney.value), "Molten Lava Monkey 5", "ML Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L3Rocky.value), "Molten Lava Monkey 6", "ML Monkey")
    __add_event_location(self, self.get_region(AELocation.W1L3Moggan.value), "Molten Lava Monkey 7", "ML Monkey")
    # Thick Jungle
    __add_event_location(self, self.get_region(AELocation.W2L1Marquez.value), "Thick Jungle Monkey 1", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Livinston.value), "Thick Jungle Monkey 2", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1George.value), "Thick Jungle Monkey 3", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Maki.value), "Thick Jungle Monkey 4", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Herb.value), "Thick Jungle Monkey 5", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Dilweed.value), "Thick Jungle Monkey 6", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Mitong.value), "Thick Jungle Monkey 7", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Stoddy.value), "Thick Jungle Monkey 8", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Nasus.value), "Thick Jungle Monkey 9", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Selur.value), "Thick Jungle Monkey 10", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Elehcim.value), "Thick Jungle Monkey 11", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Gonzo.value), "Thick Jungle Monkey 12", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Alphonse.value), "Thick Jungle Monkey 13", "TJ Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L1Zanzibar.value), "Thick Jungle Monkey 14", "TJ Monkey")
    # Dark Ruins
    __add_event_location(self, self.get_region(AELocation.W2L2Mooshy.value), "Dark Ruins Monkey 1", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Kyle.value), "Dark Ruins Monkey 2", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Cratman.value), "Dark Ruins Monkey 3", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Nuzzy.value), "Dark Ruins Monkey 4", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Mav.value), "Dark Ruins Monkey 5", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Stan.value), "Dark Ruins Monkey 6", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Bernt.value), "Dark Ruins Monkey 7", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Runt.value), "Dark Ruins Monkey 8", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Hoolah.value), "Dark Ruins Monkey 9", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Papou.value), "Dark Ruins Monkey 10", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Kenny.value), "Dark Ruins Monkey 11", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Trance.value), "Dark Ruins Monkey 12", "DR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L2Chino.value), "Dark Ruins Monkey 13", "DR Monkey")
    # Cryptic Relics
    __add_event_location(self, self.get_region(AELocation.W2L3Troopa.value), "Cryptic Relics Monkey 1", "CR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L3Spanky.value), "Cryptic Relics Monkey 2", "CR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L3Stymie.value), "Cryptic Relics Monkey 3", "CR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L3Pally.value), "Cryptic Relics Monkey 4", "CR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L3Freeto.value), "Cryptic Relics Monkey 5", "CR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L3Jesta.value), "Cryptic Relics Monkey 6", "CR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L3Bazzle.value), "Cryptic Relics Monkey 7", "CR Monkey")
    __add_event_location(self, self.get_region(AELocation.W2L3Crash.value), "Cryptic Relics Monkey 8", "CR Monkey")
    # Crabby Beach
    __add_event_location(self, self.get_region(AELocation.W4L1CoolBlue.value), "Crabby Beach Monkey 1", "CB Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L1Sandy.value), "Crabby Beach Monkey 2", "CB Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L1ShellE.value), "Crabby Beach Monkey 3", "CB Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L1Gidget.value), "Crabby Beach Monkey 4", "CB Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L1Shaka.value), "Crabby Beach Monkey 5", "CB Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L1MaxMahalo.value), "Crabby Beach Monkey 6", "CB Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L1Moko.value), "Crabby Beach Monkey 7", "CB Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L1Puka.value), "Crabby Beach Monkey 8", "CB Monkey")
    # Coral Cave
    __add_event_location(self, self.get_region(AELocation.W4L2Chip.value), "Coral Cave Monkey 1", "CoC Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L2Oreo.value), "Coral Cave Monkey 2", "CoC Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L2Puddles.value), "Coral Cave Monkey 3", "CoC Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L2Kalama.value), "Coral Cave Monkey 4", "CoC Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L2Iz.value), "Coral Cave Monkey 5", "CoC Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L2Jux.value), "Coral Cave Monkey 6", "CoC Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L2BongBong.value), "Coral Cave Monkey 7", "CoC Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L2Pickles.value), "Coral Cave Monkey 8", "CoC Monkey")
    # Dexter's Island
    __add_event_location(self, self.get_region(AELocation.W4L3Stuw.value), "Dexter's Island Monkey 1", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3TonTon.value), "Dexter's Island Monkey 2", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Murky.value), "Dexter's Island Monkey 3", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Howeerd.value), "Dexter's Island Monkey 4", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Robbin.value), "Dexter's Island Monkey 5", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Jakkee.value), "Dexter's Island Monkey 6", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Frederic.value), "Dexter's Island Monkey 7", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Baba.value), "Dexter's Island Monkey 8", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Mars.value), "Dexter's Island Monkey 9", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Horke.value), "Dexter's Island Monkey 10", "DI Monkey")
    __add_event_location(self, self.get_region(AELocation.W4L3Quirck.value), "Dexter's Island Monkey 11", "DI Monkey")
    # Snowy Mammoth
    __add_event_location(self, self.get_region(AELocation.W5L1Popcicle.value), "Snowy Mammoth Monkey 1", "SM Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L1Iced.value), "Snowy Mammoth Monkey 2", "SM Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L1Denggoy.value), "Snowy Mammoth Monkey 3", "SM Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L1Skeens.value), "Snowy Mammoth Monkey 4", "SM Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L1Rickets.value), "Snowy Mammoth Monkey 5", "SM Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L1Chilly.value), "Snowy Mammoth Monkey 6", "SM Monkey")
    # Frosty Retreat
    __add_event_location(self, self.get_region(AELocation.W5L2Storm.value), "Frosty Retreat Monkey 1", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Qube.value), "Frosty Retreat Monkey 2", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Gash.value), "Frosty Retreat Monkey 3", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Kundra.value), "Frosty Retreat Monkey 4", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Shadow.value), "Frosty Retreat Monkey 5", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Ranix.value), "Frosty Retreat Monkey 6", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Sticky.value), "Frosty Retreat Monkey 7", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Sharpe.value), "Frosty Retreat Monkey 8", "FR Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L2Droog.value), "Frosty Retreat Monkey 9", "FR Monkey")
    # Hot Springs
    __add_event_location(self, self.get_region(AELocation.W5L3Punky.value), "Hot Springs Monkey 1", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Ameego.value), "Hot Springs Monkey 2", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Roti.value), "Hot Springs Monkey 3", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Dissa.value), "Hot Springs Monkey 4", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Yoky.value), "Hot Springs Monkey 5", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Jory.value), "Hot Springs Monkey 6", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Crank.value), "Hot Springs Monkey 7", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Claxter.value), "Hot Springs Monkey 8", "HS Monkey")
    __add_event_location(self, self.get_region(AELocation.W5L3Looza.value), "Hot Springs Monkey 9", "HS Monkey")
    # Sushi Temple
    __add_event_location(self, self.get_region(AELocation.W7L1Taku.value), "Sushi Temple Monkey 1", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Rocka.value), "Sushi Temple Monkey 2", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Maralea.value), "Sushi Temple Monkey 3", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Wog.value), "Sushi Temple Monkey 4", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Long.value), "Sushi Temple Monkey 5", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Mayi.value), "Sushi Temple Monkey 6", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Owyang.value), "Sushi Temple Monkey 7", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1QuelTin.value), "Sushi Temple Monkey 8", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Phaldo.value), "Sushi Temple Monkey 9", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Voti.value), "Sushi Temple Monkey 10", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Elly.value), "Sushi Temple Monkey 11", "ST Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L1Chunky.value), "Sushi Temple Monkey 12", "ST Monkey")
    # Wabi Sabi Wall
    __add_event_location(self, self.get_region(AELocation.W7L2Minky.value), "Wabi Sabi Wall Monkey 1", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Zobbro.value), "Wabi Sabi Wall Monkey 2", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Xeeto.value), "Wabi Sabi Wall Monkey 3", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Moops.value), "Wabi Sabi Wall Monkey 4", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Zanabi.value), "Wabi Sabi Wall Monkey 5", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Buddha.value), "Wabi Sabi Wall Monkey 6", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Fooey.value), "Wabi Sabi Wall Monkey 7", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Doxs.value), "Wabi Sabi Wall Monkey 8", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Kong.value), "Wabi Sabi Wall Monkey 9", "WSW Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L2Phool.value), "Wabi Sabi Wall Monkey 10", "WSW Monkey")
    # Crumbling Castle
    __add_event_location(self, self.get_region(AELocation.W7L3Naners.value), "Crumbling Castle Monkey 1", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Robart.value), "Crumbling Castle Monkey 2", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Neeners.value), "Crumbling Castle Monkey 3", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Gustav.value), "Crumbling Castle Monkey 4", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Wilhelm.value), "Crumbling Castle Monkey 5", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Emmanuel.value), "Crumbling Castle Monkey 6",
                         "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3SirCutty.value), "Crumbling Castle Monkey 7",
                         "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Calligan.value), "Crumbling Castle Monkey 8",
                         "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Castalist.value), "Crumbling Castle Monkey 9",
                         "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Deveneom.value), "Crumbling Castle Monkey 10",
                         "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Igor.value), "Crumbling Castle Monkey 11", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Charles.value), "Crumbling Castle Monkey 12",
                         "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Astur.value), "Crumbling Castle Monkey 13", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Kilserack.value), "Crumbling Castle Monkey 14",
                         "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Ringo.value), "Crumbling Castle Monkey 15", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Densil.value), "Crumbling Castle Monkey 16", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Figero.value), "Crumbling Castle Monkey 17", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Fej.value), "Crumbling Castle Monkey 18", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Joey.value), "Crumbling Castle Monkey 19", "CrC Monkey")
    __add_event_location(self, self.get_region(AELocation.W7L3Donqui.value), "Crumbling Castle Monkey 20", "CrC Monkey")
    # City Park
    __add_event_location(self, self.get_region(AELocation.W8L1Kaine.value), "City Park Monkey 1", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Jaxx.value), "City Park Monkey 2", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Gehry.value), "City Park Monkey 3", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Alcatraz.value), "City Park Monkey 4", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Tino.value), "City Park Monkey 5", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1QBee.value), "City Park Monkey 6", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1McManic.value), "City Park Monkey 7", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Dywan.value), "City Park Monkey 8", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1CKHutch.value), "City Park Monkey 9", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Winky.value), "City Park Monkey 10", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1BLuv.value), "City Park Monkey 11", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Camper.value), "City Park Monkey 12", "CP Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L1Huener.value), "City Park Monkey 13", "CP Monkey")
    # Specter's Factory
    __add_event_location(self, self.get_region(AELocation.W8L2BigShow.value), "Specter's Factory Monkey 1", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2Dreos.value), "Specter's Factory Monkey 2", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2Reznor.value), "Specter's Factory Monkey 3", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2Urkel.value), "Specter's Factory Monkey 4", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2VanillaS.value), "Specter's Factory Monkey 5",
                         "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2Radd.value), "Specter's Factory Monkey 6", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2Shimbo.value), "Specter's Factory Monkey 7", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2Hurt.value), "Specter's Factory Monkey 8", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2String.value), "Specter's Factory Monkey 9", "SF Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L2Khamo.value), "Specter's Factory Monkey 10", "SF Monkey")
    # TV Tower
    __add_event_location(self, self.get_region(AELocation.W8L3Fredo.value), "TV Tower Monkey 1", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Charlee.value), "TV Tower Monkey 2", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Mach3.value), "TV Tower Monkey 3", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Tortuss.value), "TV Tower Monkey 4", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Manic.value), "TV Tower Monkey 5", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Ruptdis.value), "TV Tower Monkey 6", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Eighty7.value), "TV Tower Monkey 7", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Danio.value), "TV Tower Monkey 8", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Roosta.value), "TV Tower Monkey 9", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Tellis.value), "TV Tower Monkey 10", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Whack.value), "TV Tower Monkey 11", "TVT Monkey")
    __add_event_location(self, self.get_region(AELocation.W8L3Frostee.value), "TV Tower Monkey 12", "TVT Monkey")
    # Monkey Madness
    __add_event_location(self, self.get_region(AELocation.W9L1Goopo.value), "Monkey Madness Monkey 1", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Porto.value), "Monkey Madness Monkey 2", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Slam.value), "Monkey Madness Monkey 3", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Junk.value), "Monkey Madness Monkey 4", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Crib.value), "Monkey Madness Monkey 5", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Nak.value), "Monkey Madness Monkey 6", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Cloy.value), "Monkey Madness Monkey 7", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Shaw.value), "Monkey Madness Monkey 8", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Flea.value), "Monkey Madness Monkey 9", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Schafette.value), "Monkey Madness Monkey 10", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Donovan.value), "Monkey Madness Monkey 11", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Laura.value), "Monkey Madness Monkey 12", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Uribe.value), "Monkey Madness Monkey 13", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Gordo.value), "Monkey Madness Monkey 14", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Raeski.value), "Monkey Madness Monkey 15", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Poopie.value), "Monkey Madness Monkey 16", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Teacup.value), "Monkey Madness Monkey 17", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Shine.value), "Monkey Madness Monkey 18", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Wrench.value), "Monkey Madness Monkey 19", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Bronson.value), "Monkey Madness Monkey 20", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Bungee.value), "Monkey Madness Monkey 21", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Carro.value), "Monkey Madness Monkey 22", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1Carlito.value), "Monkey Madness Monkey 23", "MM Monkey")
    __add_event_location(self, self.get_region(AELocation.W9L1BG.value), "Monkey Madness Monkey 24", "MM Monkey")


'''
# I love this trick :) '''


def create_regions(world: "ApeEscapeWorld"):
    options = world.options
    player = world.player
    multiworld = world.multiworld
    # menu
    menu = Region("Menu", player, multiworld)

    # Format for region names is LevelRoomTransition, so L73R3T2 is Level 7-3 (Crumbling Castle) Room 3 (Bell Tower) Transition to room 2 (Castle Main). A lack of a Room or Transition is the default spawn location for that level.
    # Time Station
    TS = Region(AEDoor.TIME_ENTRY.value, player, multiworld)
    TSR1T2 = Region(AEDoor.TIME_MAIN_TRAINING.value, player, multiworld)
    TSR1T3 = Region(AEDoor.TIME_MAIN_MINIGAME.value, player, multiworld)
    TSR2T1 = Region(AEDoor.TIME_TRAINING_MAIN.value, player, multiworld)
    TSR2T2 = Region(AEDoor.TIME_TRAINING_WATERNET.value, player, multiworld)
    TSR3T1 = Region(AEDoor.TIME_MINIGAME_MAIN.value, player, multiworld)
    
    # 1-1
    L11 = Region(AEDoor.FF_ENTRY.value, player, multiworld)
    
    noonan = Region(AELocation.W1L1Noonan.value, player, multiworld)
    noonan.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], noonan) for loc_name in get_array([1])]
    jorjy = Region(AELocation.W1L1Jorjy.value, player, multiworld)
    jorjy.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], jorjy) for loc_name in get_array([2])]
    nati = Region(AELocation.W1L1Nati.value, player, multiworld)
    nati.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], nati) for loc_name in get_array([3])]
    trayc = Region(AELocation.W1L1TrayC.value, player, multiworld)
    trayc.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], trayc) for loc_name in get_array([4])]
    
    # 1-2
    L12 = Region(AEDoor.PO_ENTRY.value, player, multiworld)
    
    shay = Region(AELocation.W1L2Shay.value, player, multiworld)
    shay.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], shay) for loc_name in get_array([5])]
    drmonk = Region(AELocation.W1L2DrMonk.value, player, multiworld)
    drmonk.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], drmonk) for loc_name in get_array([6])]
    grunt = Region(AELocation.W1L2Grunt.value, player, multiworld)
    grunt.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], grunt) for loc_name in get_array([7])]
    ahchoo = Region(AELocation.W1L2Ahchoo.value, player, multiworld)
    ahchoo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], ahchoo) for loc_name in get_array([8])]
    gornif = Region(AELocation.W1L2Gornif.value, player, multiworld)
    gornif.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], gornif) for loc_name in get_array([9])]
    tyrone = Region(AELocation.W1L2Tyrone.value, player, multiworld)
    tyrone.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], tyrone) for loc_name in get_array([10])]
    
    # 1-3
    L13 = Region(AEDoor.ML_ENTRY.value, player, multiworld)
    L13R1T2 = Region(AEDoor.ML_ENTRY_VOLCANO.value, player, multiworld)
    L13R1T3 = Region(AEDoor.ML_ENTRY_TRICERATOPS.value, player, multiworld)
    L13R2T1 = Region(AEDoor.ML_VOLCANO_ENTRY.value, player, multiworld)
    L13R3T1 = Region(AEDoor.ML_TRICERATOPS_ENTRY.value, player, multiworld)
    
    scotty = Region(AELocation.W1L3Scotty.value, player, multiworld)
    scotty.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], scotty) for loc_name in get_array([11])]
    coco = Region(AELocation.W1L3Coco.value, player, multiworld)
    coco.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coco) for loc_name in get_array([12])]
    jthomas = Region(AELocation.W1L3JThomas.value, player, multiworld)
    jthomas.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], jthomas) for loc_name in get_array([13])]
    mattie = Region(AELocation.W1L3Mattie.value, player, multiworld)
    mattie.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mattie) for loc_name in get_array([14])]
    barney = Region(AELocation.W1L3Barney.value, player, multiworld)
    barney.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], barney) for loc_name in get_array([15])]
    rocky = Region(AELocation.W1L3Rocky.value, player, multiworld)
    rocky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], rocky) for loc_name in get_array([16])]
    moggan = Region(AELocation.W1L3Moggan.value, player, multiworld)
    moggan.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], moggan) for loc_name in get_array([17])]
    
    # 2-1
    L21 = Region(AEDoor.TJ_ENTRY.value, player, multiworld)
    L21R1T2 = Region(AEDoor.TJ_ENTRY_MUSHROOM.value, player, multiworld)
    L21R1T3 = Region(AEDoor.TJ_ENTRY_FISH.value, player, multiworld)
    L21R1T5 = Region(AEDoor.TJ_ENTRY_BOULDER.value, player, multiworld)
    L21R2T1 = Region(AEDoor.TJ_MUSHROOM_ENTRY.value, player, multiworld)
    L21R2HELP = Region(AEDoor.TJ_MUSHROOMMAIN.value, player, multiworld)
    L21R3T1 = Region(AEDoor.TJ_FISH_ENTRY.value, player, multiworld)
    L21R3T4 = Region(AEDoor.TJ_FISH_TENT.value, player, multiworld)
    L21R3HELP = Region(AEDoor.TJ_FISHBOAT.value, player, multiworld)
    L21R4T3 = Region(AEDoor.TJ_TENT_FISH.value, player, multiworld)
    L21R4T5 = Region(AEDoor.TJ_TENT_BOULDER.value, player, multiworld)
    L21R5T1 = Region(AEDoor.TJ_BOULDER_ENTRY.value, player, multiworld)
    L21R5T4 = Region(AEDoor.TJ_BOULDER_TENT.value, player, multiworld)
    
    marquez = Region(AELocation.W2L1Marquez.value, player, multiworld)
    marquez.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], marquez) for loc_name in get_array([18])]
    livinston = Region(AELocation.W2L1Livinston.value, player, multiworld)
    livinston.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], livinston) for loc_name in get_array([19])]
    george = Region(AELocation.W2L1George.value, player, multiworld)
    george.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], george) for loc_name in get_array([20])]
    gonzo = Region(AELocation.W2L1Gonzo.value, player, multiworld)
    gonzo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], gonzo) for loc_name in get_array([29])]
    zanzibar = Region(AELocation.W2L1Zanzibar.value, player, multiworld)
    zanzibar.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], zanzibar) for loc_name in get_array([31])]
    alphonse = Region(AELocation.W2L1Alphonse.value, player, multiworld)
    alphonse.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], alphonse) for loc_name in get_array([30])]
    maki = Region(AELocation.W2L1Maki.value, player, multiworld)
    maki.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], maki) for loc_name in get_array([21])]
    herb = Region(AELocation.W2L1Herb.value, player, multiworld)
    herb.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], herb) for loc_name in get_array([22])]
    dilweed = Region(AELocation.W2L1Dilweed.value, player, multiworld)
    dilweed.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], dilweed) for loc_name in get_array([23])]
    stoddy = Region(AELocation.W2L1Stoddy.value, player, multiworld)
    stoddy.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], stoddy) for loc_name in get_array([25])]
    mitong = Region(AELocation.W2L1Mitong.value, player, multiworld)
    mitong.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mitong) for loc_name in get_array([24])]
    nasus = Region(AELocation.W2L1Nasus.value, player, multiworld)
    nasus.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], nasus) for loc_name in get_array([26])]
    elehcim = Region(AELocation.W2L1Elehcim.value, player, multiworld)
    elehcim.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], elehcim) for loc_name in get_array([28])]
    selur = Region(AELocation.W2L1Selur.value, player, multiworld)
    selur.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], selur) for loc_name in get_array([27])]
    
    # 2-2
    L22 = Region(AEDoor.DR_ENTRY.value, player, multiworld)
    L22R1T21 = Region(AEDoor.DR_OUTSIDE_FENCE.value, player, multiworld)
    L22R1T22 = Region(AEDoor.DR_OUTSIDE_HOLE.value, player, multiworld)
    L22R1T31 = Region(AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value, player, multiworld)
    L22R1T32 = Region(AEDoor.DR_OUTSIDE_OBELISK_TOP.value, player, multiworld)
    L22R1T41 = Region(AEDoor.DR_OUTSIDE_WATER_BUTTON.value, player, multiworld)
    L22R1T42 = Region(AEDoor.DR_OUTSIDE_WATER_LEDGE.value, player, multiworld)
    L22R2T11 = Region(AEDoor.DR_FAN_OUTSIDE_FENCE.value, player, multiworld)
    L22R2T12 = Region(AEDoor.DR_FAN_OUTSIDE_HOLE.value, player, multiworld)
    L22R3T11 = Region(AEDoor.DR_OBELISK_BOTTOM.value, player, multiworld)
    L22R3T12 = Region(AEDoor.DR_OBELISK_TOP.value, player, multiworld)
    L22R4T11 = Region(AEDoor.DR_WATER_SIDE.value, player, multiworld)
    L22R4T12 = Region(AEDoor.DR_WATER_LEDGE.value, player, multiworld)

    mooshy = Region(AELocation.W2L2Mooshy.value, player, multiworld)
    mooshy.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mooshy) for loc_name in get_array([32])]
    kyle = Region(AELocation.W2L2Kyle.value, player, multiworld)
    kyle.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], kyle) for loc_name in get_array([33])]
    cratman = Region(AELocation.W2L2Cratman.value, player, multiworld)
    cratman.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], cratman) for loc_name in get_array([34])]
    nuzzy = Region(AELocation.W2L2Nuzzy.value, player, multiworld)
    nuzzy.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], nuzzy) for loc_name in get_array([35])]
    mav = Region(AELocation.W2L2Mav.value, player, multiworld)
    mav.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mav) for loc_name in get_array([36])]
    stan = Region(AELocation.W2L2Stan.value, player, multiworld)
    stan.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], stan) for loc_name in get_array([37])]
    bernt = Region(AELocation.W2L2Bernt.value, player, multiworld)
    bernt.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bernt) for loc_name in get_array([38])]
    runt = Region(AELocation.W2L2Runt.value, player, multiworld)
    runt.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], runt) for loc_name in get_array([39])]
    hoolah = Region(AELocation.W2L2Hoolah.value, player, multiworld)
    hoolah.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], hoolah) for loc_name in get_array([40])]
    papou = Region(AELocation.W2L2Papou.value, player, multiworld)
    papou.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], papou) for loc_name in get_array([41])]
    kenny = Region(AELocation.W2L2Kenny.value, player, multiworld)
    kenny.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], kenny) for loc_name in get_array([42])]
    trance = Region(AELocation.W2L2Trance.value, player, multiworld)
    trance.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], trance) for loc_name in get_array([43])]
    chino = Region(AELocation.W2L2Chino.value, player, multiworld)
    chino.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], chino) for loc_name in get_array([44])]
    
    # 2-3
    L23 = Region(AEDoor.CR_ENTRY.value, player, multiworld)
    L23R1T2 = Region(AEDoor.CR_ENTRY_SIDE_ROOM.value, player, multiworld)
    L23R1T3 = Region(AEDoor.CR_ENTRY_MAIN_RUINS.value, player, multiworld)
    L23R1HELP = Region(AEDoor.CR_ENTRYOBA.value, player, multiworld)
    L23R2T1 = Region(AEDoor.CR_SIDE_ROOM_ENTRY.value, player, multiworld)
    L23R3T1 = Region(AEDoor.CR_MAIN_RUINS_ENTRY.value, player, multiworld)
    L23R3T4 = Region(AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, player, multiworld)
    L23R4T3 = Region(AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, player, multiworld)

    troopa = Region(AELocation.W2L3Troopa.value, player, multiworld)
    troopa.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], troopa) for loc_name in get_array([45])]
    spanky = Region(AELocation.W2L3Spanky.value, player, multiworld)
    spanky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], spanky) for loc_name in get_array([46])]
    stymie = Region(AELocation.W2L3Stymie.value, player, multiworld)
    stymie.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], stymie) for loc_name in get_array([47])]
    pally = Region(AELocation.W2L3Pally.value, player, multiworld)
    pally.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], pally) for loc_name in get_array([48])]
    freeto = Region(AELocation.W2L3Freeto.value, player, multiworld)
    freeto.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], freeto) for loc_name in get_array([49])]
    jesta = Region(AELocation.W2L3Jesta.value, player, multiworld)
    jesta.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], jesta) for loc_name in get_array([50])]
    bazzle = Region(AELocation.W2L3Bazzle.value, player, multiworld)
    bazzle.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bazzle) for loc_name in get_array([51])]
    crash = Region(AELocation.W2L3Crash.value, player, multiworld)
    crash.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], crash) for loc_name in get_array([52])]

    # 3-1
    L31 = Region(AEDoor.SA_ENTRY.value, player, multiworld)
    
    # 4-1
    L41 = Region(AEDoor.CB_ENTRY.value, player, multiworld)
    L41R1T2 = Region(AEDoor.CB_ENTRY_SECOND_ROOM.value, player, multiworld)
    L41R2T1 = Region(AEDoor.CB_SECOND_ROOM_ENTRY.value, player, multiworld)
    
    coolblue = Region(AELocation.W4L1CoolBlue.value, player, multiworld)
    coolblue.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coolblue) for loc_name in get_array([53])]
    sandy = Region(AELocation.W4L1Sandy.value, player, multiworld)
    sandy.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], sandy) for loc_name in get_array([54])]
    shelle = Region(AELocation.W4L1ShellE.value, player, multiworld)
    shelle.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], shelle) for loc_name in get_array([55])]
    gidget = Region(AELocation.W4L1Gidget.value, player, multiworld)
    gidget.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], gidget) for loc_name in get_array([56])]
    shaka = Region(AELocation.W4L1Shaka.value, player, multiworld)
    shaka.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], shaka) for loc_name in get_array([57])]
    maxmahalo = Region(AELocation.W4L1MaxMahalo.value, player, multiworld)
    maxmahalo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], maxmahalo) for loc_name in get_array([58])]
    moko = Region(AELocation.W4L1Moko.value, player, multiworld)
    moko.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], moko) for loc_name in get_array([59])]
    puka = Region(AELocation.W4L1Puka.value, player, multiworld)
    puka.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], puka) for loc_name in get_array([60])]
    
    # 4-2
    L42 = Region(AEDoor.CCAVE_ENTRY.value, player, multiworld)
    L42R1T2 = Region(AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, player, multiworld)
    L42R2T1 = Region(AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, player, multiworld)
    
    chip = Region(AELocation.W4L2Chip.value, player, multiworld)
    chip.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], chip) for loc_name in get_array([61])]
    oreo = Region(AELocation.W4L2Oreo.value, player, multiworld)
    oreo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], oreo) for loc_name in get_array([62])]
    puddles = Region(AELocation.W4L2Puddles.value, player, multiworld)
    puddles.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], puddles) for loc_name in get_array([63])]
    kalama = Region(AELocation.W4L2Kalama.value, player, multiworld)
    kalama.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], kalama) for loc_name in get_array([64])]
    iz = Region(AELocation.W4L2Iz.value, player, multiworld)
    iz.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], iz) for loc_name in get_array([65])]
    jux = Region(AELocation.W4L2Jux.value, player, multiworld)
    jux.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], jux) for loc_name in get_array([66])]
    bongbong = Region(AELocation.W4L2BongBong.value, player, multiworld)
    bongbong.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bongbong) for loc_name in get_array([67])]
    pickles = Region(AELocation.W4L2Pickles.value, player, multiworld)
    pickles.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], pickles) for loc_name in get_array([68])]
    
    # 4-3
    L43 = Region(AEDoor.DI_ENTRY.value, player, multiworld)
    L43R1T2 = Region(AEDoor.DI_ENTRY_STOMACH.value, player, multiworld)
    L43R2T1 = Region(AEDoor.DI_STOMACH_ENTRY.value, player, multiworld)
    L43R2T3 = Region(AEDoor.DI_STOMACH_SLIDE_ROOM.value, player, multiworld)
    L43R3T1 = Region(AEDoor.DI_SLIDE_ROOM_STOMACH.value, player, multiworld)
    L43R3T41 = Region(AEDoor.DI_SLIDE_ROOM_GALLERY.value, player, multiworld)
    L43R3T42 = Region(AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, player, multiworld)
    L43R4T31 = Region(AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, player, multiworld)
    L43R4T32 = Region(AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, player, multiworld)
    L43R4T5 = Region(AEDoor.DI_GALLERY_TENTACLE.value, player, multiworld)
    L43R4HELP = Region(AEDoor.DI_GALLERYBOULDER.value, player, multiworld)
    L43R5T4 = Region(AEDoor.DI_TENTACLE.value, player, multiworld)
    
    stuw = Region(AELocation.W4L3Stuw.value, player, multiworld)
    stuw.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], stuw) for loc_name in get_array([69])]
    tonton = Region(AELocation.W4L3TonTon.value, player, multiworld)
    tonton.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], tonton) for loc_name in get_array([70])]
    murky = Region(AELocation.W4L3Murky.value, player, multiworld)
    murky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], murky) for loc_name in get_array([71])]
    howeerd = Region(AELocation.W4L3Howeerd.value, player, multiworld)
    howeerd.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], howeerd) for loc_name in get_array([72])]
    robbin = Region(AELocation.W4L3Robbin.value, player, multiworld)
    robbin.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], robbin) for loc_name in get_array([73])]
    jakkee = Region(AELocation.W4L3Jakkee.value, player, multiworld)
    jakkee.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], jakkee) for loc_name in get_array([74])]
    frederic = Region(AELocation.W4L3Frederic.value, player, multiworld)
    frederic.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], frederic) for loc_name in get_array([75])]
    baba = Region(AELocation.W4L3Baba.value, player, multiworld)
    baba.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], baba) for loc_name in get_array([76])]
    mars = Region(AELocation.W4L3Mars.value, player, multiworld)
    mars.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mars) for loc_name in get_array([77])]
    horke = Region(AELocation.W4L3Horke.value, player, multiworld)
    horke.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], horke) for loc_name in get_array([78])]
    quirck = Region(AELocation.W4L3Quirck.value, player, multiworld)
    quirck.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], quirck) for loc_name in get_array([79])]
    
    # 5-1
    L51 = Region(AEDoor.SM_ENTRY.value, player, multiworld)
    
    popcicle = Region(AELocation.W5L1Popcicle.value, player, multiworld)
    popcicle.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], popcicle) for loc_name in get_array([80])]
    iced = Region(AELocation.W5L1Iced.value, player, multiworld)
    iced.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], iced) for loc_name in get_array([81])]
    denggoy = Region(AELocation.W5L1Denggoy.value, player, multiworld)
    denggoy.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], denggoy) for loc_name in get_array([82])]
    skeens = Region(AELocation.W5L1Skeens.value, player, multiworld)
    skeens.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], skeens) for loc_name in get_array([83])]
    rickets = Region(AELocation.W5L1Rickets.value, player, multiworld)
    rickets.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], rickets) for loc_name in get_array([84])]
    chilly = Region(AELocation.W5L1Chilly.value, player, multiworld)
    chilly.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], chilly) for loc_name in get_array([85])]
    
    # 5-2
    L52 = Region(AEDoor.FR_ENTRY.value, player, multiworld)
    L52R1T2 = Region(AEDoor.FR_ENTRY_CAVERNS.value, player, multiworld)
    L52R2T1 = Region(AEDoor.FR_CAVERNS_ENTRY.value, player, multiworld)
    L52R2T3 = Region(AEDoor.FR_CAVERNS_WATER.value, player, multiworld)
    L52R3T2 = Region(AEDoor.FR_WATER_CAVERNS.value, player, multiworld)
    
    storm = Region(AELocation.W5L2Storm.value, player, multiworld)
    storm.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], storm) for loc_name in get_array([86])]
    qube = Region(AELocation.W5L2Qube.value, player, multiworld)
    qube.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], qube) for loc_name in get_array([87])]
    gash = Region(AELocation.W5L2Gash.value, player, multiworld)
    gash.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], gash) for loc_name in get_array([88])]
    kundra = Region(AELocation.W5L2Kundra.value, player, multiworld)
    kundra.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], kundra) for loc_name in get_array([89])]
    shadow = Region(AELocation.W5L2Shadow.value, player, multiworld)
    shadow.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], shadow) for loc_name in get_array([90])]
    ranix = Region(AELocation.W5L2Ranix.value, player, multiworld)
    ranix.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], ranix) for loc_name in get_array([91])]
    sticky = Region(AELocation.W5L2Sticky.value, player, multiworld)
    sticky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], sticky) for loc_name in get_array([92])]
    sharpe = Region(AELocation.W5L2Sharpe.value, player, multiworld)
    sharpe.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], sharpe) for loc_name in get_array([93])]
    droog = Region(AELocation.W5L2Droog.value, player, multiworld)
    droog.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], droog) for loc_name in get_array([94])]
    
    # 5-3
    L53 = Region(AEDoor.HS_ENTRY.value, player, multiworld)
    L53R1T2 = Region(AEDoor.HS_ENTRY_HOT_SPRING.value, player, multiworld)
    L53R1T3 = Region(AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value, player, multiworld)
    L53R2T1 = Region(AEDoor.HS_HOT_SPRING.value, player, multiworld)
    L53R3T1 = Region(AEDoor.HS_POLAR_BEAR_CAVE.value, player, multiworld)
    
    punky = Region(AELocation.W5L3Punky.value, player, multiworld)
    punky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], punky) for loc_name in get_array([95])]
    ameego = Region(AELocation.W5L3Ameego.value, player, multiworld)
    ameego.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], ameego) for loc_name in get_array([96])]
    roti = Region(AELocation.W5L3Roti.value, player, multiworld)
    roti.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], roti) for loc_name in get_array([97])]
    dissa = Region(AELocation.W5L3Dissa.value, player, multiworld)
    dissa.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], dissa) for loc_name in get_array([98])]
    yoky = Region(AELocation.W5L3Yoky.value, player, multiworld)
    yoky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], yoky) for loc_name in get_array([99])]
    jory = Region(AELocation.W5L3Jory.value, player, multiworld)
    jory.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], jory) for loc_name in get_array([100])]
    crank = Region(AELocation.W5L3Crank.value, player, multiworld)
    crank.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], crank) for loc_name in get_array([101])]
    claxter = Region(AELocation.W5L3Claxter.value, player, multiworld)
    claxter.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], claxter) for loc_name in get_array([102])]
    looza = Region(AELocation.W5L3Looza.value, player, multiworld)
    looza.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], looza) for loc_name in get_array([103])]

    # 6-1
    L61 = Region(AEDoor.GA_ENTRY.value, player, multiworld)
    
    # 7-1
    L71 = Region(AEDoor.ST_ENTRY.value, player, multiworld)
    L71R1T2 = Region(AEDoor.ST_ENTRY_TEMPLE.value, player, multiworld)
    L71R1T3 = Region(AEDoor.ST_ENTRY_WELL.value, player, multiworld)
    L71R2T1 = Region(AEDoor.ST_TEMPLE.value, player, multiworld)
    L71R3T1 = Region(AEDoor.ST_WELL.value, player, multiworld)
    
    taku = Region(AELocation.W7L1Taku.value, player, multiworld)
    taku.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], taku) for loc_name in get_array([104])]
    rocka = Region(AELocation.W7L1Rocka.value, player, multiworld)
    rocka.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], rocka) for loc_name in get_array([105])]
    maralea = Region(AELocation.W7L1Maralea.value, player, multiworld)
    maralea.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], maralea) for loc_name in get_array([106])]
    wog = Region(AELocation.W7L1Wog.value, player, multiworld)
    wog.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], wog) for loc_name in get_array([107])]
    long = Region(AELocation.W7L1Long.value, player, multiworld)
    long.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], long) for loc_name in get_array([108])]
    mayi = Region(AELocation.W7L1Mayi.value, player, multiworld)
    mayi.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mayi) for loc_name in get_array([109])]
    owyang = Region(AELocation.W7L1Owyang.value, player, multiworld)
    owyang.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], owyang) for loc_name in get_array([110])]
    queltin = Region(AELocation.W7L1QuelTin.value, player, multiworld)
    queltin.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], queltin) for loc_name in get_array([111])]
    phaldo = Region(AELocation.W7L1Phaldo.value, player, multiworld)
    phaldo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], phaldo) for loc_name in get_array([112])]
    voti = Region(AELocation.W7L1Voti.value, player, multiworld)
    voti.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], voti) for loc_name in get_array([113])]
    elly = Region(AELocation.W7L1Elly.value, player, multiworld)
    elly.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], elly) for loc_name in get_array([114])]
    chunky = Region(AELocation.W7L1Chunky.value, player, multiworld)
    chunky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], chunky) for loc_name in get_array([115])]
    
    # 7-2
    L72 = Region(AEDoor.WSW_ENTRY.value, player, multiworld)
    L72R1T2 = Region(AEDoor.WSW_ENTRY_GONG.value, player, multiworld)
    L72R2T1 = Region(AEDoor.WSW_GONG_ENTRY.value, player, multiworld)
    L72R2T3 = Region(AEDoor.WSW_GONG_MIDDLE.value, player, multiworld)
    L72R3T2 = Region(AEDoor.WSW_MIDDLE_GONG.value, player, multiworld)
    L72R3T4 = Region(AEDoor.WSW_MIDDLE_OBSTACLE.value, player, multiworld)
    L72R4T3 = Region(AEDoor.WSW_OBSTACLE_MIDDLE.value, player, multiworld)
    L72R4T5 = Region(AEDoor.WSW_OBSTACLE_BARREL.value, player, multiworld)
    L72R5T4 = Region(AEDoor.WSW_BARREL_OBSTACLE.value, player, multiworld)
    
    minky = Region(AELocation.W7L2Minky.value, player, multiworld)
    minky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], minky) for loc_name in get_array([116])]
    zobbro = Region(AELocation.W7L2Zobbro.value, player, multiworld)
    zobbro.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], zobbro) for loc_name in get_array([117])]
    xeeto = Region(AELocation.W7L2Xeeto.value, player, multiworld)
    xeeto.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], xeeto) for loc_name in get_array([118])]
    moops = Region(AELocation.W7L2Moops.value, player, multiworld)
    moops.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], moops) for loc_name in get_array([119])]
    zanabi = Region(AELocation.W7L2Zanabi.value, player, multiworld)
    zanabi.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], zanabi) for loc_name in get_array([120])]
    buddah = Region(AELocation.W7L2Buddha.value, player, multiworld)
    buddah.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], buddah) for loc_name in get_array([121])]
    fooey = Region(AELocation.W7L2Fooey.value, player, multiworld)
    fooey.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], fooey) for loc_name in get_array([122])]
    doxs = Region(AELocation.W7L2Doxs.value, player, multiworld)
    doxs.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], doxs) for loc_name in get_array([123])]
    kong = Region(AELocation.W7L2Kong.value, player, multiworld)
    kong.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], kong) for loc_name in get_array([124])]
    phool = Region(AELocation.W7L2Phool.value, player, multiworld)
    phool.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], phool) for loc_name in get_array([125])]

    # 7-3
    L73 = Region(AEDoor.CC_ENTRY.value, player, multiworld)
    L73R1T2 = Region(AEDoor.CC_ENTRY_CASTLE.value, player, multiworld)
    L73R1T3 = Region(AEDoor.CC_ENTRY_BELL.value, player, multiworld)
    L73R1T5 = Region(AEDoor.CC_ENTRY_BASEMENT.value, player, multiworld)
    L73R1T7 = Region(AEDoor.CC_ENTRY_BOSS.value, player, multiworld)
    L73R2T1 = Region(AEDoor.CC_CASTLEMAIN_ENTRY.value, player, multiworld)
    L73R2T3 = Region(AEDoor.CC_CASTLEMAIN_BELL.value, player, multiworld)
    L73R2T4 = Region(AEDoor.CC_CASTLEMAIN_ELEVATOR.value, player, multiworld)
    L73R2HELP = Region(AEDoor.CC_CASTLEMAINTHRONEROOM.value, player, multiworld)
    L73R3T1 = Region(AEDoor.CC_BELL_ENTRY.value, player, multiworld)
    L73R3T2 = Region(AEDoor.CC_BELL_CASTLE.value, player, multiworld)
    L73R4T2 = Region(AEDoor.CC_ELEVATOR_CASTLEMAIN.value, player, multiworld)
    L73R4T5 = Region(AEDoor.CC_ELEVATOR_BASEMENT.value, player, multiworld)
    L73R5T1 = Region(AEDoor.CC_BASEMENT_ENTRY.value, player, multiworld)
    L73R5T4 = Region(AEDoor.CC_BASEMENT_ELEVATOR.value, player, multiworld)
    L73R5T61 = Region(AEDoor.CC_BASEMENT_BUTTON_DOWN.value, player, multiworld)
    L73R5T62 = Region(AEDoor.CC_BASEMENT_BUTTON_UP.value, player, multiworld)
    L73R6T51 = Region(AEDoor.CC_BUTTON_BASEMENT_WATER.value, player, multiworld)
    L73R6T52 = Region(AEDoor.CC_BUTTON_BASEMENT_LEDGE.value, player, multiworld)
    L73R7T1 = Region(AEDoor.CC_BOSS_ROOM.value, player, multiworld)
    
    L73BOSS = Region(AELocation.Boss73.value, player, multiworld)
    L73BOSS.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], L73BOSS) for loc_name in get_array([500])]
    naners = Region(AELocation.W7L3Naners.value, player, multiworld)
    naners.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], naners) for loc_name in get_array([126])]
    robart = Region(AELocation.W7L3Robart.value, player, multiworld)
    robart.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], robart) for loc_name in get_array([127])]
    neeners = Region(AELocation.W7L3Neeners.value, player, multiworld)
    neeners.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], neeners) for loc_name in get_array([128])]
    gustav = Region(AELocation.W7L3Gustav.value, player, multiworld)
    gustav.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], gustav) for loc_name in get_array([129])]
    wilhelm = Region(AELocation.W7L3Wilhelm.value, player, multiworld)
    wilhelm.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], wilhelm) for loc_name in get_array([130])]
    emmanuel = Region(AELocation.W7L3Emmanuel.value, player, multiworld)
    emmanuel.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], emmanuel) for loc_name in get_array([131])]
    sircutty = Region(AELocation.W7L3SirCutty.value, player, multiworld)
    sircutty.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], sircutty) for loc_name in get_array([132])]
    calligan = Region(AELocation.W7L3Calligan.value, player, multiworld)
    calligan.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], calligan) for loc_name in get_array([133])]
    castalist = Region(AELocation.W7L3Castalist.value, player, multiworld)
    castalist.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], castalist) for loc_name in get_array([134])]
    deveneom = Region(AELocation.W7L3Deveneom.value, player, multiworld)
    deveneom.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], deveneom) for loc_name in get_array([135])]
    igor = Region(AELocation.W7L3Igor.value, player, multiworld)
    igor.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], igor) for loc_name in get_array([136])]
    charles = Region(AELocation.W7L3Charles.value, player, multiworld)
    charles.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], charles) for loc_name in get_array([137])]
    astur = Region(AELocation.W7L3Astur.value, player, multiworld)
    astur.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], astur) for loc_name in get_array([138])]
    kilserack = Region(AELocation.W7L3Kilserack.value, player, multiworld)
    kilserack.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], kilserack) for loc_name in get_array([139])]
    ringo = Region(AELocation.W7L3Ringo.value, player, multiworld)
    ringo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], ringo) for loc_name in get_array([140])]
    densil = Region(AELocation.W7L3Densil.value, player, multiworld)
    densil.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], densil) for loc_name in get_array([141])]
    figero = Region(AELocation.W7L3Figero.value, player, multiworld)
    figero.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], figero) for loc_name in get_array([142])]
    fej = Region(AELocation.W7L3Fej.value, player, multiworld)
    fej.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], fej) for loc_name in get_array([143])]
    joey = Region(AELocation.W7L3Joey.value, player, multiworld)
    joey.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], joey) for loc_name in get_array([144])]
    donqui = Region(AELocation.W7L3Donqui.value, player, multiworld)
    donqui.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], donqui) for loc_name in get_array([145])]
    
    # 8-1
    L81 = Region(AEDoor.CP_ENTRY.value, player, multiworld)
    L81R1T2 = Region(AEDoor.CP_OUTSIDE_SEWERS_FRONT.value, player, multiworld)
    L81R1T3 = Region(AEDoor.CP_OUTSIDE_BARREL.value, player, multiworld)
    L81R2T1 = Region(AEDoor.CP_SEWERSFRONT_OUTSIDE.value, player, multiworld)
    L81R2T3 = Region(AEDoor.CP_SEWERSFRONT_BARREL.value, player, multiworld)
    L81R3T1 = Region(AEDoor.CP_BARREL_OUTSIDE.value, player, multiworld)
    L81R3T2 = Region(AEDoor.CP_BARREL_SEWERS_FRONT.value, player, multiworld)
    L81R3HELP = Region(AEDoor.CP_BARRELSEWERMIDDLE.value, player, multiworld)

    kaine = Region(AELocation.W8L1Kaine.value, player, multiworld)
    kaine.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], kaine) for loc_name in get_array([146])]
    jaxx = Region(AELocation.W8L1Jaxx.value, player, multiworld)
    jaxx.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], jaxx) for loc_name in get_array([147])]
    gehry = Region(AELocation.W8L1Gehry.value, player, multiworld)
    gehry.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], gehry) for loc_name in get_array([148])]
    alcatraz = Region(AELocation.W8L1Alcatraz.value, player, multiworld)
    alcatraz.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], alcatraz) for loc_name in get_array([149])]
    tino = Region(AELocation.W8L1Tino.value, player, multiworld)
    tino.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], tino) for loc_name in get_array([150])]
    qbee = Region(AELocation.W8L1QBee.value, player, multiworld)
    qbee.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], qbee) for loc_name in get_array([151])]
    mcmanic = Region(AELocation.W8L1McManic.value, player, multiworld)
    mcmanic.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mcmanic) for loc_name in get_array([152])]
    dywan = Region(AELocation.W8L1Dywan.value, player, multiworld)
    dywan.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], dywan) for loc_name in get_array([153])]
    ckhutch = Region(AELocation.W8L1CKHutch.value, player, multiworld)
    ckhutch.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], ckhutch) for loc_name in get_array([154])]
    winky = Region(AELocation.W8L1Winky.value, player, multiworld)
    winky.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], winky) for loc_name in get_array([155])]
    bluv = Region(AELocation.W8L1BLuv.value, player, multiworld)
    bluv.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bluv) for loc_name in get_array([156])]
    camper = Region(AELocation.W8L1Camper.value, player, multiworld)
    camper.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], camper) for loc_name in get_array([157])]
    huener = Region(AELocation.W8L1Huener.value, player, multiworld)
    huener.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], huener) for loc_name in get_array([158])]

    # 8-2
    L82 = Region(AEDoor.SF_ENTRY.value, player, multiworld)
    L82R1T2 = Region(AEDoor.SF_OUTSIDE_FACTORY.value, player, multiworld)
    L82R2T1 = Region(AEDoor.SF_FACTORY_OUTSIDE.value, player, multiworld)
    L82R2T3 = Region(AEDoor.SF_FACTORY_RC_CAR.value, player, multiworld)
    L82R2T41 = Region(AEDoor.SF_FACTORY_WHEEL_BOTTOM.value, player, multiworld)
    L82R2T42 = Region(AEDoor.SF_FACTORY_WHEEL_TOP.value, player, multiworld)
    L82R2T5 = Region(AEDoor.SF_FACTORY_MECH.value, player, multiworld)
    L82R3T2 = Region(AEDoor.SF_RC_CAR_FACTORY.value, player, multiworld)
    L82R4T21 = Region(AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, player, multiworld)
    L82R4T22 = Region(AEDoor.SF_WHEEL_FACTORY_TOP.value, player, multiworld)
    L82R5T2 = Region(AEDoor.SF_MECH_FACTORY.value, player, multiworld)
    L82R5T6 = Region(AEDoor.SF_MECH_LAVA.value, player, multiworld)
    L82R6T5 = Region(AEDoor.SF_LAVA_MECH.value, player, multiworld)
    L82R6T7 = Region(AEDoor.SF_LAVA_CONVEYOR.value, player, multiworld)
    L82R7T6 = Region(AEDoor.SF_CONVEYOR_LAVA.value, player, multiworld)
    L82R7T71E = Region(AEDoor.SF_CONVEYOR1_ENTRY.value, player, multiworld)
    L82R7T71X = Region(AEDoor.SF_CONVEYOR1_EXIT.value, player, multiworld)
    L82R7T72E = Region(AEDoor.SF_CONVEYOR2_ENTRY.value, player, multiworld)
    L82R7T72X = Region(AEDoor.SF_CONVEYOR2_EXIT.value, player, multiworld)
    L82R7T73E = Region(AEDoor.SF_CONVEYOR3_ENTRY.value, player, multiworld)
    L82R7T73X = Region(AEDoor.SF_CONVEYOR3_EXIT.value, player, multiworld)
    L82R7T74E = Region(AEDoor.SF_CONVEYOR4_ENTRY.value, player, multiworld)
    L82R7T74X = Region(AEDoor.SF_CONVEYOR4_EXIT.value, player, multiworld)
    L82R7T75E = Region(AEDoor.SF_CONVEYOR5_ENTRY.value, player, multiworld)
    L82R7T75X = Region(AEDoor.SF_CONVEYOR5_EXIT.value, player, multiworld)
    L82R7T76E = Region(AEDoor.SF_CONVEYOR6_ENTRY.value, player, multiworld)
    L82R7T76X = Region(AEDoor.SF_CONVEYOR6_EXIT.value, player, multiworld)
    L82R7T77E = Region(AEDoor.SF_CONVEYOR7_ENTRY.value, player, multiworld)

    bigshow = Region(AELocation.W8L2BigShow.value, player, multiworld)
    bigshow.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bigshow) for loc_name in get_array([159])]
    dreos = Region(AELocation.W8L2Dreos.value, player, multiworld)
    dreos.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], dreos) for loc_name in get_array([160])]
    reznor = Region(AELocation.W8L2Reznor.value, player, multiworld)
    reznor.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], reznor) for loc_name in get_array([161])]
    urkel = Region(AELocation.W8L2Urkel.value, player, multiworld)
    urkel.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], urkel) for loc_name in get_array([162])]
    vanillas = Region(AELocation.W8L2VanillaS.value, player, multiworld)
    vanillas.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], vanillas) for loc_name in get_array([163])]
    radd = Region(AELocation.W8L2Radd.value, player, multiworld)
    radd.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], radd) for loc_name in get_array([164])]
    shimbo = Region(AELocation.W8L2Shimbo.value, player, multiworld)
    shimbo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], shimbo) for loc_name in get_array([165])]
    hurt = Region(AELocation.W8L2Hurt.value, player, multiworld)
    hurt.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], hurt) for loc_name in get_array([166])]
    strung = Region(AELocation.W8L2String.value, player, multiworld)
    strung.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], strung) for loc_name in get_array([167])]
    khamo = Region(AELocation.W8L2Khamo.value, player, multiworld)
    khamo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], khamo) for loc_name in get_array([168])]
    
    # 8-3
    L83 = Region(AEDoor.TVT_ENTRY.value, player, multiworld)
    L83R1T2 = Region(AEDoor.TVT_OUTSIDE_LOBBY.value, player, multiworld)
    L83R2T1 = Region(AEDoor.TVT_LOBBY_OUTSIDE.value, player, multiworld)
    L83R2T3 = Region(AEDoor.TVT_LOBBY_WATER.value, player, multiworld)
    L83R2T4 = Region(AEDoor.TVT_LOBBY_TANK.value, player, multiworld)
    L83R3T2 = Region(AEDoor.TVT_WATER_LOBBY.value, player, multiworld)
    L83R4T2 = Region(AEDoor.TVT_TANK_LOBBY.value, player, multiworld)
    L83R4T5 = Region(AEDoor.TVT_TANK_FAN.value, player, multiworld)
    L83R4T6 = Region(AEDoor.TVT_TANK_BOSS.value, player, multiworld)
    L83R5T4 = Region(AEDoor.TVT_FAN_TANK.value, player, multiworld)
    L83R6T4 = Region(AEDoor.TVT_BOSS_TANK.value, player, multiworld)
    
    L83BOSS = Region(AELocation.Boss83.value, player, multiworld)
    L83BOSS.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], L83BOSS) for loc_name in get_array([501])]
    fredo = Region(AELocation.W8L3Fredo.value, player, multiworld)
    fredo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], fredo) for loc_name in get_array([169])]
    charlee = Region(AELocation.W8L3Charlee.value, player, multiworld)
    charlee.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], charlee) for loc_name in get_array([170])]
    mach3 = Region(AELocation.W8L3Mach3.value, player, multiworld)
    mach3.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mach3) for loc_name in get_array([171])]
    tortuss = Region(AELocation.W8L3Tortuss.value, player, multiworld)
    tortuss.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], tortuss) for loc_name in get_array([172])]
    manic = Region(AELocation.W8L3Manic.value, player, multiworld)
    manic.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], manic) for loc_name in get_array([173])]
    ruptdis = Region(AELocation.W8L3Ruptdis.value, player, multiworld)
    ruptdis.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], ruptdis) for loc_name in get_array([174])]
    eighty7 = Region(AELocation.W8L3Eighty7.value, player, multiworld)
    eighty7.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], eighty7) for loc_name in get_array([175])]
    danio = Region(AELocation.W8L3Danio.value, player, multiworld)
    danio.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], danio) for loc_name in get_array([176])]
    roosta = Region(AELocation.W8L3Roosta.value, player, multiworld)
    roosta.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], roosta) for loc_name in get_array([177])]
    tellis = Region(AELocation.W8L3Tellis.value, player, multiworld)
    tellis.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], tellis) for loc_name in get_array([178])]
    whack = Region(AELocation.W8L3Whack.value, player, multiworld)
    whack.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], whack) for loc_name in get_array([179])]
    frostee = Region(AELocation.W8L3Frostee.value, player, multiworld)
    frostee.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], frostee) for loc_name in get_array([180])]

    # 9-1
    L91 = Region(AEDoor.MM_SL_HUB.value, player, multiworld)
    L91R1T2 = Region(AEDoor.MM_SL_HUB_WESTERN.value, player, multiworld)
    L91R1T3 = Region(AEDoor.MM_SL_HUB_COASTER.value, player, multiworld)
    L91R1T4 = Region(AEDoor.MM_SL_HUB_CIRCUS.value, player, multiworld)
    L91R1T5 = Region(AEDoor.MM_SL_HUB_GO_KARZ.value, player, multiworld)
    L91R1T10 = Region(AEDoor.MM_SL_HUB_CRATER.value, player, multiworld)
    L91R2T1 = Region(AEDoor.MM_WESTERN_SL_HUB.value, player, multiworld)
    L91R3T1 = Region(AEDoor.MM_COASTER_ENTRY_SL_HUB.value, player, multiworld)
    L91R3T6E = Region(AEDoor.MM_COASTER_ENTRY_COASTER1.value, player, multiworld)
    L91R3T9X = Region(AEDoor.MM_COASTER_ENTRY_DISEMBARK.value, player, multiworld)
    L91R4T1 = Region(AEDoor.MM_CIRCUS_SL_HUB.value, player, multiworld)
    L91R5T1 = Region(AEDoor.MM_GO_KARZ_SL_HUB.value, player, multiworld)
    L91R6T3X = Region(AEDoor.MM_COASTER1_ENTRY.value, player, multiworld)
    L91R6T7E = Region(AEDoor.MM_COASTER1_COASTER2.value, player, multiworld)
    L91R7T6X = Region(AEDoor.MM_COASTER2_ENTRY.value, player, multiworld)
    L91R7T8E = Region(AEDoor.MM_COASTER2_HAUNTED_HOUSE.value, player, multiworld)
    L91R8T7X = Region(AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, player, multiworld)
    L91R8T9 = Region(AEDoor.MM_HAUNTED_HOUSE_COFFIN.value, player, multiworld)
    L91R9T3E = Region(AEDoor.MM_COFFIN_COASTER_ENTRY.value, player, multiworld)
    L91R9T8 = Region(AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, player, multiworld)
    L91R10T1 = Region(AEDoor.MM_CRATER_SL_HUB.value, player, multiworld)
    L91R10T11 = Region(AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, player, multiworld)
    L91R11T10 = Region(AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, player, multiworld)
    L91R11T12 = Region(AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value, player, multiworld)
    L91R11T13 = Region(AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value, player, multiworld)
    L91R12T11 = Region(AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, player, multiworld)
    L91R13T11 = Region(AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, player, multiworld)
    L91R13T14 = Region(AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, player, multiworld)
    L91R13T15 = Region(AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value, player, multiworld)
    L91R13T16X = Region(AEDoor.MM_CASTLE_MAIN_FROM_OUTSIDE.value, player, multiworld)
    L91R13T17E = Region(AEDoor.MM_CASTLE_MAIN_SPECTER1.value, player, multiworld)
    L91R14T13 = Region(AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, player, multiworld)
    L91R15T13 = Region(AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value, player, multiworld)
    L91R15T16 = Region(AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value, player, multiworld)
    L91R16T15 = Region(AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, player, multiworld)
    L91R16T13E = Region(AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value, player, multiworld)
    L91R17T13X = Region(AEDoor.MM_SPECTER1_ROOM.value, player, multiworld)

    L91BOSS = Region(AELocation.Specter.value, player, multiworld)

    if options.goal not in ("mm","mmtoken"):
        # Normal location if the goal is not MM related
        L91BOSS.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], L91BOSS) for loc_name in get_array([205])]
    else:
        # Create event location to prevent players to send_location or send the Victory item
        L91BOSS.locations += [ApeEscapeLocation(player, loc_name, None, L91BOSS) for loc_name in get_array([205])]
    L91PROF = Region(AELocation.W9L1Professor.value, player, multiworld)
    L91PROF.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], L91PROF) for loc_name in get_array([502])]
    L91JAKE = Region(AELocation.W9L1Jake.value, player, multiworld)
    L91JAKE.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], L91JAKE) for loc_name in get_array([503])]
    goopo = Region(AELocation.W9L1Goopo.value, player, multiworld)
    goopo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], goopo) for loc_name in get_array([181])]
    porto = Region(AELocation.W9L1Porto.value, player, multiworld)
    porto.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], porto) for loc_name in get_array([182])]
    slam = Region(AELocation.W9L1Slam.value, player, multiworld)
    slam.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], slam) for loc_name in get_array([183])]
    junk = Region(AELocation.W9L1Junk.value, player, multiworld)
    junk.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], junk) for loc_name in get_array([184])]
    crib = Region(AELocation.W9L1Crib.value, player, multiworld)
    crib.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], crib) for loc_name in get_array([185])]
    nak = Region(AELocation.W9L1Nak.value, player, multiworld)
    nak.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], nak) for loc_name in get_array([186])]
    cloy = Region(AELocation.W9L1Cloy.value, player, multiworld)
    cloy.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], cloy) for loc_name in get_array([187])]
    shaw = Region(AELocation.W9L1Shaw.value, player, multiworld)
    shaw.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], shaw) for loc_name in get_array([188])]
    flea = Region(AELocation.W9L1Flea.value, player, multiworld)
    flea.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], flea) for loc_name in get_array([189])]
    schafette = Region(AELocation.W9L1Schafette.value, player, multiworld)
    schafette.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], schafette) for loc_name in get_array([190])]
    donovan = Region(AELocation.W9L1Donovan.value, player, multiworld)
    donovan.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], donovan) for loc_name in get_array([191])]
    laura = Region(AELocation.W9L1Laura.value, player, multiworld)
    laura.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], laura) for loc_name in get_array([192])]
    uribe = Region(AELocation.W9L1Uribe.value, player, multiworld)
    uribe.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], uribe) for loc_name in get_array([193])]
    gordo = Region(AELocation.W9L1Gordo.value, player, multiworld)
    gordo.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], gordo) for loc_name in get_array([194])]
    raeski = Region(AELocation.W9L1Raeski.value, player, multiworld)
    raeski.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], raeski) for loc_name in get_array([195])]
    poopie = Region(AELocation.W9L1Poopie.value, player, multiworld)
    poopie.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], poopie) for loc_name in get_array([196])]
    teacup = Region(AELocation.W9L1Teacup.value, player, multiworld)
    teacup.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], teacup) for loc_name in get_array([197])]
    shine = Region(AELocation.W9L1Shine.value, player, multiworld)
    shine.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], shine) for loc_name in get_array([198])]
    wrench = Region(AELocation.W9L1Wrench.value, player, multiworld)
    wrench.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], wrench) for loc_name in get_array([199])]
    bronson = Region(AELocation.W9L1Bronson.value, player, multiworld)
    bronson.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bronson) for loc_name in get_array([200])]
    bungee = Region(AELocation.W9L1Bungee.value, player, multiworld)
    bungee.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bungee) for loc_name in get_array([201])]
    carro = Region(AELocation.W9L1Carro.value, player, multiworld)
    carro.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], carro) for loc_name in get_array([202])]
    carlito = Region(AELocation.W9L1Carlito.value, player, multiworld)
    carlito.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], carlito) for loc_name in get_array([203])]
    bg = Region(AELocation.W9L1BG.value, player, multiworld)
    bg.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], bg) for loc_name in get_array([204])]
    
    regions = [menu,
               TS, TSR1T2, TSR1T3, TSR2T1, TSR2T2, TSR3T1,
               L11, noonan, jorjy, nati, trayc,
               L12, shay, drmonk, grunt, ahchoo, gornif, tyrone,
               L13, L13R1T2, L13R1T3, L13R2T1, L13R3T1, scotty, coco, jthomas, mattie, barney, rocky, moggan,
               L21, L21R1T2, L21R1T3, L21R1T5, L21R2T1, L21R3T1, L21R3T4, L21R4T3, L21R4T5, L21R5T1, L21R5T4, L21R2HELP, L21R3HELP, marquez, livinston, george, maki, herb, dilweed, mitong, stoddy, nasus, selur, elehcim, gonzo, alphonse, zanzibar,
               L22, L22R1T21, L22R1T22, L22R1T31, L22R1T32, L22R1T41, L22R1T42, L22R2T11, L22R2T12, L22R3T11, L22R3T12, L22R4T11, L22R4T12, kyle, stan, kenny, cratman, mooshy, nuzzy, mav, papou, trance, bernt, runt, hoolah, chino,
               L23, L23R1T2, L23R1T3, L23R2T1, L23R3T1, L23R3T4, L23R4T3, L23R1HELP, bazzle, freeto, troopa, stymie, spanky, jesta, pally, crash,
               L31,
               L41, L41R1T2, L41R2T1, coolblue, sandy, shelle, gidget, shaka, maxmahalo, moko, puka,
               L42, L42R1T2, L42R2T1, chip, oreo, puddles, kalama, iz, bongbong, jux, pickles,
               L43, L43R1T2, L43R2T1, L43R2T3, L43R3T1, L43R3T41, L43R3T42, L43R4T31, L43R4T32, L43R4T5, L43R5T4, L43R4HELP, tonton, stuw, mars, murky, horke, howeerd, robbin, jakkee, frederic, baba, quirck,
               L51, popcicle, iced, rickets, skeens, denggoy, chilly,
               L52, L52R1T2, L52R2T1, L52R2T3, L52R3T2, storm, qube, ranix, sharpe, sticky, droog, gash, kundra, shadow,
               L53, L53R1T2, L53R1T3, L53R2T1, L53R3T1, punky, ameego, yoky, jory, crank, claxter, looza, roti, dissa,
               L61,
               L71, L71R1T2, L71R1T3, L71R2T1, L71R3T1, taku, rocka, maralea, wog, mayi, owyang, long, elly, chunky, voti, queltin, phaldo,
               L72, L72R1T2, L72R2T1, L72R2T3, L72R3T2, L72R3T4, L72R4T3, L72R4T5, L72R5T4, minky, zobbro, xeeto, moops, zanabi, doxs, buddah, fooey, kong, phool,
               L73, L73R1T2, L73R1T3, L73R1T5, L73R1T7, L73R2T1, L73R2T3, L73R2T4, L73R3T1, L73R3T2, L73R4T2, L73R4T5, L73R5T1, L73R5T4, L73R5T61, L73R5T62, L73R6T51, L73R6T52, L73R7T1, L73R2HELP, L73BOSS, 
               robart, igor, naners, neeners, charles, gustav, wilhelm, emmanuel, sircutty, calligan, castalist, deveneom, astur, kilserack, ringo, densil, figero, fej, joey, donqui,
               L81, L81R1T2, L81R1T3, L81R2T1, L81R2T3, L81R3T1, L81R3T2, L81R3HELP, kaine, jaxx, gehry, alcatraz, tino, qbee, mcmanic, dywan, ckhutch, winky, bluv, camper, huener,
               L82, L82R1T2, L82R2T1, L82R2T3, L82R2T41, L82R2T42, L82R2T5, L82R3T2, L82R4T21, L82R4T22, L82R5T2, L82R5T6, L82R6T5, L82R6T7, L82R7T6,
               L82R7T71E, L82R7T71X, L82R7T72E, L82R7T72X, L82R7T73E, L82R7T73X, L82R7T74E, L82R7T74X,L82R7T75E, L82R7T75X, L82R7T76E, L82R7T76X, L82R7T77E,
               bigshow, dreos, reznor, urkel, vanillas, radd, shimbo, hurt, strung, khamo,
               L83, L83R1T2, L83R2T1, L83R2T3, L83R2T4, L83R3T2, L83R4T2, L83R4T5, L83R4T6, L83R5T4, L83R6T4, L83BOSS, fredo, charlee, mach3, tortuss, manic, ruptdis, eighty7, danio, roosta, tellis, whack, frostee,
               L91, L91R1T2, L91R1T3, L91R1T4, L91R1T5, L91R1T10, L91R2T1, L91R3T1, L91R3T6E, L91R3T9X, L91R4T1, L91R5T1, L91R6T3X, L91R6T7E, L91R7T6X, L91R7T8E, L91R8T7X, L91R8T9, L91R9T3E, L91R9T8, L91R10T1, L91R10T11, L91R11T10, L91R11T12, L91R11T13, L91R12T11, L91R13T11, L91R13T14, L91R13T15, L91R13T16X, L91R13T17E, L91R14T13, L91R15T13, L91R15T16, L91R16T15, L91R16T13E, L91R17T13X, L91BOSS, L91PROF, L91JAKE,
               goopo, porto, slam, junk, crib, nak, cloy, shaw, flea, schafette, donovan, laura, uribe, gordo, raeski, poopie, teacup, shine, wrench, bronson, bungee, carro, carlito, bg]
    

    # Don't create Specter 2 location if it would be guaranteed to be post-goal.

    if options.goal != "mm":
        # 9-2
        L92 = Region(AEDoor.PPM_ENTRY.value, player, multiworld)

        L92BOSS = Region(AELocation.Specter2.value, player, multiworld)
        # Normal location
        if options.goal not in ("ppm","ppmtoken"):
            L92BOSS.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], L92BOSS) for loc_name in get_array([206])]
        else:
            # Create event location to prevent players to send_location or send the Victory item
            L92BOSS.locations += [ApeEscapeLocation(player, loc_name, None, L92BOSS) for loc_name in get_array([206])]
        regions += [L92, L92BOSS]

    if options.coin == "true":
        coin1 = Region(AELocation.Coin1.value, player, multiworld)
        coin1.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin1) for loc_name in get_array([301])]
        coin2 = Region(AELocation.Coin2.value, player, multiworld)
        coin2.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin2) for loc_name in get_array([302])]
        coin3 = Region(AELocation.Coin3.value, player, multiworld)
        coin3.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin3) for loc_name in get_array([303])]
        coin6 = Region(AELocation.Coin6.value, player, multiworld)
        coin6.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin6) for loc_name in get_array([306])]
        coin7 = Region(AELocation.Coin7.value, player, multiworld)
        coin7.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin7) for loc_name in get_array([307])]
        coin8 = Region(AELocation.Coin8.value, player, multiworld)
        coin8.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin8) for loc_name in get_array([308])]
        coin9 = Region(AELocation.Coin9.value, player, multiworld)
        coin9.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin9) for loc_name in get_array([309])]
        coin11 = Region(AELocation.Coin11.value, player, multiworld)
        coin11.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin11) for loc_name in get_array([311])]
        coin12 = Region(AELocation.Coin12.value, player, multiworld)
        coin12.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin12) for loc_name in get_array([312])]
        coin13 = Region(AELocation.Coin13.value, player, multiworld)
        coin13.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin13) for loc_name in get_array([313])]
        coin14 = Region(AELocation.Coin14.value, player, multiworld)
        coin14.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin14) for loc_name in get_array([314])]
        coin17 = Region(AELocation.Coin17.value, player, multiworld)
        coin17.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin17) for loc_name in get_array([317])]
        coin19 = Region(AEDoor.SA_COMPLETE.value, player, multiworld)
        coin19.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin19) for loc_name in get_array([295, 296, 297, 298, 299])]
        coin21 = Region(AELocation.Coin21.value, player, multiworld)
        coin21.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin21) for loc_name in get_array([321])]
        coin23 = Region(AELocation.Coin23.value, player, multiworld)
        coin23.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin23) for loc_name in get_array([323])]
        coin24 = Region(AELocation.Coin24.value, player, multiworld)
        coin24.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin24) for loc_name in get_array([324])]
        coin25 = Region(AELocation.Coin25.value, player, multiworld)
        coin25.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin25) for loc_name in get_array([325])]
        coin28 = Region(AELocation.Coin28.value, player, multiworld)
        coin28.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin28) for loc_name in get_array([328])]
        coin29 = Region(AELocation.Coin29.value, player, multiworld)
        coin29.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin29) for loc_name in get_array([329])]
        coin30 = Region(AELocation.Coin30.value, player, multiworld)
        coin30.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin30) for loc_name in get_array([330])]
        coin31 = Region(AELocation.Coin31.value, player, multiworld)
        coin31.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin31) for loc_name in get_array([331])]
        coin32 = Region(AELocation.Coin32.value, player, multiworld)
        coin32.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin32) for loc_name in get_array([332])]
        coin34 = Region(AELocation.Coin34.value, player, multiworld)
        coin34.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin34) for loc_name in get_array([334])]
        coin35 = Region(AELocation.Coin35.value, player, multiworld)
        coin35.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin35) for loc_name in get_array([335])]
        coin36 = Region(AEDoor.GA_COMPLETE.value, player, multiworld)
        coin36.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin36) for loc_name in get_array([290, 291, 292, 293, 294])]
        coin37 = Region(AELocation.Coin37.value, player, multiworld)
        coin37.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin37) for loc_name in get_array([337])]
        coin38 = Region(AELocation.Coin38.value, player, multiworld)
        coin38.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin38) for loc_name in get_array([338])]
        coin39 = Region(AELocation.Coin39.value, player, multiworld)
        coin39.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin39) for loc_name in get_array([339])]
        coin40 = Region(AELocation.Coin40.value, player, multiworld)
        coin40.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin40) for loc_name in get_array([340])]
        coin41 = Region(AELocation.Coin41.value, player, multiworld)
        coin41.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin41) for loc_name in get_array([341])]
        coin44 = Region(AELocation.Coin44.value, player, multiworld)
        coin44.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin44) for loc_name in get_array([344])]
        coin45 = Region(AELocation.Coin45.value, player, multiworld)
        coin45.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin45) for loc_name in get_array([345])]
        coin46 = Region(AELocation.Coin46.value, player, multiworld)
        coin46.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin46) for loc_name in get_array([346])]
        coin49 = Region(AELocation.Coin49.value, player, multiworld)
        coin49.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin49) for loc_name in get_array([349])]
        coin50 = Region(AELocation.Coin50.value, player, multiworld)
        coin50.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin50) for loc_name in get_array([350])]
        coin53 = Region(AELocation.Coin53.value, player, multiworld)
        coin53.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin53) for loc_name in get_array([353])]
        coin54 = Region(AELocation.Coin54.value, player, multiworld)
        coin54.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin54) for loc_name in get_array([354])]
        coin55 = Region(AELocation.Coin55.value, player, multiworld)
        coin55.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin55) for loc_name in get_array([355])]
        coin58 = Region(AELocation.Coin58.value, player, multiworld)
        coin58.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin58) for loc_name in get_array([358])]
        coin59 = Region(AELocation.Coin59.value, player, multiworld)
        coin59.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin59) for loc_name in get_array([359])]
        coin64 = Region(AELocation.Coin64.value, player, multiworld)
        coin64.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin64) for loc_name in get_array([364])]
        coin66 = Region(AELocation.Coin66.value, player, multiworld)
        coin66.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin66) for loc_name in get_array([366])]
        coin73 = Region(AELocation.Coin73.value, player, multiworld)
        coin73.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin73) for loc_name in get_array([373])]
        coin74 = Region(AELocation.Coin74.value, player, multiworld)
        coin74.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin74) for loc_name in get_array([374])]
        coin75 = Region(AELocation.Coin75.value, player, multiworld)
        coin75.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin75) for loc_name in get_array([375])]
        coin77 = Region(AELocation.Coin77.value, player, multiworld)
        coin77.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin77) for loc_name in get_array([377])]
        coin78 = Region(AELocation.Coin78.value, player, multiworld)
        coin78.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin78) for loc_name in get_array([378])]
        coin79 = Region(AELocation.Coin79.value, player, multiworld)
        coin79.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin79) for loc_name in get_array([379])]
        coin80 = Region(AELocation.Coin80.value, player, multiworld)
        coin80.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin80) for loc_name in get_array([380])]
        coin82 = Region(AELocation.Coin82.value, player, multiworld)
        coin82.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin82) for loc_name in get_array([382])]
        coin84 = Region(AELocation.Coin84.value, player, multiworld)
        coin84.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin84) for loc_name in get_array([384])]
        coin85 = Region(AELocation.Coin85.value, player, multiworld)
        coin85.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], coin85) for loc_name in get_array([385])]
        regions += [coin1, coin2, coin3, coin6, coin7, coin8, coin9, coin11, coin12, coin13, coin14, coin17, coin19,
                    coin21, coin23, coin24, coin25, coin28, coin29, coin30, coin31, coin32, coin34, coin35, coin36,
                    coin37, coin38, coin39, coin40, coin41, coin44, coin45, coin46, coin49, coin50, coin53, coin54,
                    coin55, coin58, coin59, coin64, coin66, coin73, coin74, coin75, coin77, coin78, coin79, coin80,
                    coin82, coin84, coin85]

    # Mailboxes
    # These locations need to be created both for mailbox shuffle and for net shuffle. In the case of net shuffle, since net shuffle requires non-monkey locations, we also check for coins being shuffled here.
    if options.mailbox == "true" or (options.shufflenet == "true" and options.coin == "true"):
        # Time Station
        mailbox60 = Region(AELocation.Mailbox60.value, player, multiworld)
        mailbox60.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox60) for loc_name in get_array([460])]
        mailbox61 = Region(AELocation.Mailbox61.value, player, multiworld)
        mailbox61.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox61) for loc_name in get_array([461])]
        mailbox62 = Region(AELocation.Mailbox62.value, player, multiworld)
        mailbox62.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox62) for loc_name in get_array([462])]
        mailbox63 = Region(AELocation.Mailbox63.value, player, multiworld)
        mailbox63.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox63) for loc_name in get_array([463])]
        regions += [mailbox60, mailbox61, mailbox62, mailbox63]
    # The rest are only needed for mailbox shuffle
    if options.mailbox == "true":
        # 1-1
        mailbox1 = Region(AELocation.Mailbox1.value, player, multiworld)
        mailbox1.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox1) for loc_name in get_array([401])]
        mailbox2 = Region(AELocation.Mailbox2.value, player, multiworld)
        mailbox2.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox2) for loc_name in get_array([402])]
        mailbox3 = Region(AELocation.Mailbox3.value, player, multiworld)
        mailbox3.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox3) for loc_name in get_array([403])]
        # 1-2
        mailbox4 = Region(AELocation.Mailbox4.value, player, multiworld)
        mailbox4.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox4) for loc_name in get_array([404])]
        mailbox5 = Region(AELocation.Mailbox5.value, player, multiworld)
        mailbox5.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox5) for loc_name in get_array([405])]
        mailbox6 = Region(AELocation.Mailbox6.value, player, multiworld)
        mailbox6.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox6) for loc_name in get_array([406])]
        mailbox7 = Region(AELocation.Mailbox7.value, player, multiworld)
        mailbox7.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox7) for loc_name in get_array([407])]
        # 1-3
        mailbox8 = Region(AELocation.Mailbox8.value, player, multiworld)
        mailbox8.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox8) for loc_name in get_array([408])]
        mailbox9 = Region(AELocation.Mailbox9.value, player, multiworld)
        mailbox9.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox9) for loc_name in get_array([409])]
        mailbox10 = Region(AELocation.Mailbox10.value, player, multiworld)
        mailbox10.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox10) for loc_name in get_array([410])]
        mailbox11 = Region(AELocation.Mailbox11.value, player, multiworld)
        mailbox11.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox11) for loc_name in get_array([411])]
        mailbox12 = Region(AELocation.Mailbox12.value, player, multiworld)
        mailbox12.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox12) for loc_name in get_array([412])]
        # 2-1
        mailbox13 = Region(AELocation.Mailbox13.value, player, multiworld)
        mailbox13.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox13) for loc_name in get_array([413])]
        mailbox14 = Region(AELocation.Mailbox14.value, player, multiworld)
        mailbox14.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox14) for loc_name in get_array([414])]
        mailbox15 = Region(AELocation.Mailbox15.value, player, multiworld)
        mailbox15.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox15) for loc_name in get_array([415])]
        mailbox16 = Region(AELocation.Mailbox16.value, player, multiworld)
        mailbox16.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox16) for loc_name in get_array([416])]
        mailbox17 = Region(AELocation.Mailbox17.value, player, multiworld)
        mailbox17.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox17) for loc_name in get_array([417])]
        mailbox18 = Region(AELocation.Mailbox18.value, player, multiworld)
        mailbox18.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox18) for loc_name in get_array([418])]
        mailbox19 = Region(AELocation.Mailbox19.value, player, multiworld)
        mailbox19.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox19) for loc_name in get_array([419])]
        mailbox20 = Region(AELocation.Mailbox20.value, player, multiworld)
        mailbox20.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox20) for loc_name in get_array([420])]
        mailbox21 = Region(AELocation.Mailbox21.value, player, multiworld)
        mailbox21.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox21) for loc_name in get_array([421])]
        # 2-2
        mailbox22 = Region(AELocation.Mailbox22.value, player, multiworld)
        mailbox22.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox22) for loc_name in get_array([422])]
        mailbox23 = Region(AELocation.Mailbox23.value, player, multiworld)
        mailbox23.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox23) for loc_name in get_array([423])]
        mailbox24 = Region(AELocation.Mailbox24.value, player, multiworld)
        mailbox24.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox24) for loc_name in get_array([424])]
        mailbox25 = Region(AELocation.Mailbox25.value, player, multiworld)
        mailbox25.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox25) for loc_name in get_array([425])]
        mailbox26 = Region(AELocation.Mailbox26.value, player, multiworld)
        mailbox26.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox26) for loc_name in get_array([426])]
        mailbox27 = Region(AELocation.Mailbox27.value, player, multiworld)
        mailbox27.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox27) for loc_name in get_array([427])]
        mailbox28 = Region(AELocation.Mailbox28.value, player, multiworld)
        mailbox28.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox28) for loc_name in get_array([428])]
        # 2-3
        mailbox29 = Region(AELocation.Mailbox29.value, player, multiworld)
        mailbox29.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox29) for loc_name in get_array([429])]
        mailbox30 = Region(AELocation.Mailbox30.value, player, multiworld)
        mailbox30.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox30) for loc_name in get_array([430])]
        mailbox31 = Region(AELocation.Mailbox31.value, player, multiworld)
        mailbox31.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox31) for loc_name in get_array([431])]
        mailbox32 = Region(AELocation.Mailbox32.value, player, multiworld)
        mailbox32.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox32) for loc_name in get_array([432])]
        mailbox33 = Region(AELocation.Mailbox33.value, player, multiworld)
        mailbox33.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox33) for loc_name in get_array([433])]
        # 4-1
        mailbox34 = Region(AELocation.Mailbox34.value, player, multiworld)
        mailbox34.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox34) for loc_name in get_array([434])]
        mailbox35 = Region(AELocation.Mailbox35.value, player, multiworld)
        mailbox35.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox35) for loc_name in get_array([435])]
        mailbox36 = Region(AELocation.Mailbox36.value, player, multiworld)
        mailbox36.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox36) for loc_name in get_array([436])]
        # 4-2
        mailbox37 = Region(AELocation.Mailbox37.value, player, multiworld)
        mailbox37.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox37) for loc_name in get_array([437])]
        mailbox38 = Region(AELocation.Mailbox38.value, player, multiworld)
        mailbox38.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox38) for loc_name in get_array([438])]
        # 4-3
        mailbox39 = Region(AELocation.Mailbox39.value, player, multiworld)
        mailbox39.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox39) for loc_name in get_array([439])]
        mailbox40 = Region(AELocation.Mailbox40.value, player, multiworld)
        mailbox40.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox40) for loc_name in get_array([440])]
        mailbox41 = Region(AELocation.Mailbox41.value, player, multiworld)
        mailbox41.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox41) for loc_name in get_array([441])]
        mailbox42 = Region(AELocation.Mailbox42.value, player, multiworld)
        mailbox42.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox42) for loc_name in get_array([442])]
        # 5-1
        mailbox43 = Region(AELocation.Mailbox43.value, player, multiworld)
        mailbox43.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox43) for loc_name in get_array([443])]
        mailbox44 = Region(AELocation.Mailbox44.value, player, multiworld)
        mailbox44.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox44) for loc_name in get_array([444])]
        mailbox45 = Region(AELocation.Mailbox45.value, player, multiworld)
        mailbox45.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox45) for loc_name in get_array([445])]
        # 5-2
        mailbox46 = Region(AELocation.Mailbox46.value, player, multiworld)
        mailbox46.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox46) for loc_name in get_array([446])]
        # 5-3
        mailbox47 = Region(AELocation.Mailbox47.value, player, multiworld)
        mailbox47.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox47) for loc_name in get_array([447])]
        mailbox48 = Region(AELocation.Mailbox48.value, player, multiworld)
        mailbox48.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox48) for loc_name in get_array([448])]
        mailbox49 = Region(AELocation.Mailbox49.value, player, multiworld)
        mailbox49.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox49) for loc_name in get_array([449])]
        # 7-1
        mailbox50 = Region(AELocation.Mailbox50.value, player, multiworld)
        mailbox50.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox50) for loc_name in get_array([450])]
        mailbox51 = Region(AELocation.Mailbox51.value, player, multiworld)
        mailbox51.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox51) for loc_name in get_array([451])]
        mailbox52 = Region(AELocation.Mailbox52.value, player, multiworld)
        mailbox52.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox52) for loc_name in get_array([452])]
        # 7-2
        mailbox53 = Region(AELocation.Mailbox53.value, player, multiworld)
        mailbox53.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox53) for loc_name in get_array([453])]
        mailbox54 = Region(AELocation.Mailbox54.value, player, multiworld)
        mailbox54.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox54) for loc_name in get_array([454])]
        mailbox55 = Region(AELocation.Mailbox55.value, player, multiworld)
        mailbox55.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox55) for loc_name in get_array([455])]
        mailbox56 = Region(AELocation.Mailbox56.value, player, multiworld)
        mailbox56.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox56) for loc_name in get_array([456])]
        # 7-3
        mailbox57 = Region(AELocation.Mailbox57.value, player, multiworld)
        mailbox57.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox57) for loc_name in get_array([457])]
        # 8-1
        # 8-2
        mailbox58 = Region(AELocation.Mailbox58.value, player, multiworld)
        mailbox58.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox58) for loc_name in get_array([458])]
        # 8-3
        # 9-1
        mailbox59 = Region(AELocation.Mailbox59.value, player, multiworld)
        mailbox59.locations += [ApeEscapeLocation(player, loc_name, location_table[loc_name], mailbox59) for loc_name in get_array([459])]
        regions += [mailbox1, mailbox2, mailbox3, mailbox4, mailbox5, mailbox6, mailbox7, mailbox8, mailbox9, mailbox10,
                    mailbox11, mailbox12, mailbox13, mailbox14, mailbox15, mailbox16, mailbox17, mailbox18, mailbox19, mailbox20,
                    mailbox21, mailbox22, mailbox23, mailbox24, mailbox25, mailbox26, mailbox27, mailbox28, mailbox29, mailbox30,
                    mailbox31, mailbox32, mailbox33, mailbox34, mailbox35, mailbox36, mailbox37, mailbox38, mailbox39, mailbox40,
                    mailbox41, mailbox42, mailbox43, mailbox44, mailbox45, mailbox46, mailbox47, mailbox48, mailbox49, mailbox50,
                    mailbox51, mailbox52, mailbox53, mailbox54, mailbox55, mailbox56, mailbox57, mailbox58, mailbox59]

    multiworld.regions.extend(regions)
    create_event_items(world)


def connect_regions(world: "ApeEscapeWorld", source: str, target: str, rule=None):
    source_region = world.get_region(source)
    target_region = world.get_region(target)

    connection = Entrance(world.player, source + "_to_" + target, source_region)
    try:
        varEntrance = world.get_entrance(connection.name)
        connectionExist = True
    except:
        varEntrance = ""
        connectionExist = False

    # Connection exists only when this is an UT re-gen.
    if rule and connectionExist:
        glitched_rule = lambda state: state.has(AEItem.FAKE_OOL_ITEM.value, world.player) and rule(state)
        add_rule(varEntrance, glitched_rule, "or")
    elif rule:
        connection.access_rule = rule
    if not connectionExist:
        source_region.exits.append(connection)
        connection.connect(target_region)


def get_range(i, j):
    i += 128000000
    j += 128000000
    res = dict()
    for key, val in location_table.items():
        if i <= int(val) <= j:
            res[key] = val
    return res


def get_array(array):
    res = dict()
    for i in array:
        for key, val in location_table.items():
            if int(val) == i + 128000000:
                res[key] = val
    return res

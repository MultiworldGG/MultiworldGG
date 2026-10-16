import typing
import threading


from BaseClasses import MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table, soul_filler_table
from .Options import DoSOptions, dos_option_groups
from .Client import DoSClient
from .static_location_data import location_ids, get_location_groups
from .generator_main import (generate_early, create_regions, set_rules, create_items, fill_slot_data, create_item,
                             get_filler_item_name, modify_multidata, generate_output, write_spoiler_header,
                             connect_entrances)


class DoSWeb(WebWorld):
    display_name: str = "Castlevania - Dawn of Sorrow"
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Dawn of Sorrow randomizer"
        "and connecting to a MultiworldGG server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    option_groups = dos_option_groups
    tutorials = [setup_en]


class DoSSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania: Dawn of Sorrow ROM file."""
        description = "Dawn of Sorrow ROM File"
        copy_to = "CASTLEVANIA1_ACVEA4_00.nds"
        md5 = "cc0f25b8783fb83cb4588d1c111bdc18"

    rom_file: RomFile = RomFile(RomFile.copy_to)


class DoSWorld(World):
    """One year after the events of Aria, Soma is targetted by a recently emerged cult.
       Having rejected his fate, the cult seeks to create a new Dark Lord in his stead.
       Explore a new castle and defeat the Dark Lord Candidates!"""
    
    game = "Castlevania: Dawn of Sorrow"
    option_definitions = DoSOptions
    data_version = 1
    origin_region_name = "Lost Village Upper"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()
    web = DoSWeb()
    settings: typing.ClassVar[DoSSettings]
    # topology_present = True
    ut_can_gen_without_yaml = True

    location_name_groups = get_location_groups()
    options_dataclass = DoSOptions
    options: DoSOptions
    generate_early = generate_early
    create_items = create_items
    create_item = create_item
    create_regions = create_regions
    fill_slot_data = fill_slot_data
    modify_multidata = modify_multidata
    generate_output = generate_output
    get_filler_item_name = get_filler_item_name
    write_spoiler_header = write_spoiler_header
    set_rules = set_rules
    connect_entrances = connect_entrances

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.location_cache = []
        self.has_tried_chaos_ring = False
        self.starting_warp_room = None
        self.connected_doors = {}

        self.armor_table = [
            "Casual Clothes",
            "Cloth Tunic",
            "Gym Clothes",
            "Kung Fu Suit",
            "Biker Jacket",
            "War Fatigues",
            "Ninja Suit",
            "Three 7s",
            "Justaucorps",
            "Army Jacket",
            "Leather Armor",
            "Breastplate",
            "Ring Mail",
            "Scale Mail",
            "Chain Mail",
            "Hauberk",
            "Cuirass",
            "Silk Robe",
            "Mage Robe",
            "Elfin Robe",
            "Serenity Robe",
            "Cape",
            "Traveler Cape",
            "Crimson Cloak",
            "Black Cloak",
            "Pendant",
            "Heart Pendant",
            "Skull Necklace",
            "Flame Necklace",
            "Rosary",
            "Scarf",
            "Red Scarf",
            "Neck Warmer",
            "Power Belt",
            "Black Belt",
            "Megingiord",
            "Hoop Earring",
            "Turquoise Stud",
            "Silver Stud",
            "Gold Stud",
            "Bloody Stud",
            "Platinum Stud",
            "Lucky Charm",
            "Satan's Ring",
            "Rare Ring",
            "Rune Ring",
            "Shaman Ring",
            "Gold Ring"
        ]

        self.good_armor_table = [
            "Pitch Black Suit",
            "Olrox's Suit",
            "Dracula's Tunic",
            "Soul Eater Ring",
            "Tear Of Blood",
            "Wyrm Robe",
            "Aquarius",
            "Death's Robe",
            "Blocking Mail",
            "Eversing",
            "Demon's Mail"
        ]

        self.weapon_table = [
            "Knife",
            "Combat Knife",
            "Baselard",
            "Cutall",
            "Cinquedia",
            "Rapier",
            "Fleuret",
            "Main Gauche",
            "Small Sword",
            "Estoc",
            "Whip Sword",
            "Garian Sword",
            "Kris Naga",
            "Nebula",
            "Short Sword",
            "Cutlass",
            "Long Sword",
            "Fragarach",
            "Hrunting",
            "Mystletain",
            "Joyeuse",
            "Milican's Sword",
            "Ice Brand",
            "Laevatain",
            "Burtgang",
            "Claymore",
            "Falchion",
            "Great Sword",
            "Durandal",
            "Dainslef",
            "Ascalon",
            "Balmung",
            "Spear",
            "Partizan",
            "Halberd",
            "Lance",
            "Trident",
            "Brionac",
            "Mace",
            "Morgenstern",
            "Axe",
            "Battle Axe",
            "Bhuj",
            "Great Axe",
            "Blunt Sword",
            "Katana",
            "Kotetsu",
            "Masamune",
            "Osafune",
            "Brass Knuckles",
            "Cestus",
            "Whip Knuckle",
            "Mach Punch",
            "Handgun",
            "Silver Gun",
            "Boomerang",
            "Chakram",
            "Tomahawk",
            "Throwing Sickle",
            "Terror Bear",
            "Nunchakus"
        ]

        self.good_weapon_table = [
            "RPG",
            "Kaladbolg",
            "Valmanway",
            "Golden Axe",
            "Death Scythe",
            "Kunitsuna",
            "Yasutsuna",
            "Muramasa",
            "Kaiser Knuckle",
            "Mjollnjr",
            "Geiborg",
            "Longinus",
            "Gungner",
            "Final Sword",
            "Claimh Solais"

        ]

        self.common_souls = {
            "Axe Armor Soul",
            "Warg Soul",
            "Spin Devil Soul",
            "Slime Soul",
            "Corpseweed Soul",
            "Yeti Soul",
            "Flying Humanoid Soul",
            "Buer Soul",
            "Guillotiner Soul",
            "Cave Troll Soul",
            "Merman Soul",
            "Homunculus Soul",
            "Decarabia Soul",
            "Dead Mate Soul",
            "Mothman Soul"

        }

        self.uncommon_souls = {
            "Zombie Soul",
            "Bat Soul",
            "Skeleton Soul",
            "Skull Archer Soul",
            "Armor Knight Soul",
            "Student Witch Soul",
            "Slaughterer Soul",
            "Bomber Armor Soul",
            "Golem Soul",
            "Une Soul",
            "Manticore Soul",
            "Mollusca Soul",
            "Rycuda Soul",
            "Mandragora Soul",
            "Yorick Soul",
            "Catoblepas Soul",
            "Ghost Dancer Soul",
            "Mini Devil Soul",
            "Quetzalcoatl Soul",
            "Amalaric Sniper Soul",
            "Great Armor Soul",
            "Waiter Skeleton Soul",
            "Persephone Soul",
            "Witch Soul",
            "Lilith Soul",
            "Killer Clown Soul",
            "Skelerang Soul",
            "Fleaman Soul",
            "Devil Soul",
            "Needles Soul",
            "Hell Boar Soul",
            "White Dragon Soul",
            "Wakwak Tree Soul",
            "Imp Soul",
            "Harpy Soul",
            "Malachi Soul",
            "Larva Soul",
            "Fish Head Soul",
            "Ukoback Soul",
            "Killer Fish Soul",
            "Dead Pirate Soul",
            "Frozen Shade Soul",
            "Disc Armor Soul",
            "Alura Une Soul",
            "Mushussu Soul",
            "Succubus Soul",
            "Werewolf Soul",
            "Flame Demon Soul",
            "Alastor Soul"

        }

        self.rare_souls = {
            "Ghost Soul",
            "Ouija Table Soul",
            "Peeping Eye Soul",
            "Skeleton Ape Soul",
            "Skeleton Farmer Soul",
            "The Creature Soul",
            "Ghoul Soul",
            "Tombstone Soul",
            "Treant Soul",
            "Valkyrie Soul",
            "Killer Doll Soul",
            "Draghignazzo Soul",
            "Bone Pillar Soul",
            "Barbariccia Soul",
            "Heart Eater Soul",
            "Medusa Head Soul",
            "Mimic Soul",
            "Bugbear Soul",
            "Procel Soul",
            "Bone Ark Soul",
            "Gorgon Soul",
            "Great Axe Armor Soul",
            "Dead Crusader Soul",
            "Dead Warrior Soul",
            "Erinys Soul",
            "Tanjelly Soul",
            "Final Guard Soul",
            "Iron Golem Soul"
        }

        self.red_soul_walls = []
        self.magic_seal_table = []

        self.important_souls = {
            "Bone Ark Soul",
            "Skeleton Ape Soul"
        }
        # These souls are always required for movment logic

        self.excluded_static_souls = {
            "Aguni Soul",
            "Abaddon Soul"
        }

        self.filler_souls = soul_filler_table.copy()

        self.iron_mode = bool(False)

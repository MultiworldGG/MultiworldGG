import os
import typing
import threading
import pkgutil


from typing import List, Set, Dict, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, soul_filler_table, item_table, consumable_table, money_table
from .Locations import get_locations
from .Regions import init_areas
from .Options import DoSOptions, dos_option_groups, SoulsanityLevel, SoulRandomizer
from .Rules import set_location_rules
from .Client import DoSClient
from .Rom import DoSProcPatch, patch_rom
from .static_location_data import location_ids
from .setup_game import place_static_items, setup_game, place_static_souls


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


class CVDoSItem(Item):
    game: str = "Castlevania: Dawn of Sorrow"


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
    required_client_version = (0, 6, 0)
    origin_region_name = "Lost Village Upper"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()

    web = DoSWeb()
    settings: typing.ClassVar[DoSSettings]
    # topology_present = True
    ut_can_gen_without_yaml = True

    options_dataclass = DoSOptions
    options: DoSOptions

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.extra_item_count = 0
        self.has_tried_chaos_ring = False
        self.starting_warp_room = None

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
            "Pitch Black Suit",
            "Olrox's Suit",
            "Dracula's Tunic",
            "Leather Armor",
            "Breastplate",
            "Ring Mail",
            "Scale Mail",
            "Chain Mail",
            "Hauberk",
            "Cuirass",
            "Blocking Mail",
            "Eversing",
            "Demon's Mail",
            "Silk Robe",
            "Mage Robe",
            "Elfin Robe",
            "Wyrm Robe",
            "Aquarius",
            "Serenity Robe",
            "Death's Robe",
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
            "Tear Of Blood",
            "Lucky Charm",
            "Satan's Ring",
            "Rare Ring",
            "Soul Eater Ring",
            "Rune Ring",
            "Shaman Ring",
            "Gold Ring"
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
            "Kaladbolg",
            "Valmanway",
            "Claymore",
            "Falchion",
            "Great Sword",
            "Durandal",
            "Dainslef",
            "Ascalon",
            "Balmung",
            "Final Sword",
            "Claimh Solais",
            "Spear",
            "Partizan",
            "Halberd",
            "Lance",
            "Trident",
            "Brionac",
            "Geiborg",
            "Longinus",
            "Gungner",
            "Mace",
            "Morgenstern",
            "Mjollnjr",
            "Axe",
            "Battle Axe",
            "Bhuj",
            "Great Axe",
            "Golden Axe",
            "Death Scythe",
            "Blunt Sword",
            "Katana",
            "Kotetsu",
            "Masamune",
            "Osafune",
            "Kunitsuna",
            "Yasutsuna",
            "Muramasa",
            "Brass Knuckles",
            "Cestus",
            "Whip Knuckle",
            "Mach Punch",
            "Kaiser Knuckle",
            "Handgun",
            "Silver Gun",
            "Boomerang",
            "Chakram",
            "Tomahawk",
            "Throwing Sickle",
            "RPG",
            "Terror Bear",
            "Nunchakus"
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
            "Skeleton Ape Soul",
            "Mandragora Soul",
            "Rycuda Soul",
            "Waiter Skeleton Soul"
        }
        # These souls are always required for movment logic

        self.excluded_static_souls = {
            "Aguni Soul",
            "Abaddon Soul"
        }

    def generate_early(self) -> None:
        if hasattr(self.multiworld, "re_gen_passthrough"):  # If UT
           if "Castlevania: Dawn of Sorrow" not in self.multiworld.re_gen_passthrough: return
           passthrough = self.multiworld.re_gen_passthrough["Castlevania: Dawn of Sorrow"]
           self.options.goal = passthrough["goal"]
           self.options.soul_randomizer = passthrough["soul_randomizer"]
           self.options.soulsanity_level = passthrough["soulsanity_level"]
           self.starting_warp_room = passthrough["starting_warp"]
           self.options.open_drawbridge = passthrough["open_drawbridge"]
           self.options.boost_speed = passthrough["speed_boost"]
           self.red_soul_walls = passthrough["soul_walls"]
           self.options.gate_items = passthrough["buttonsanity"]
           self.magic_seal_table = passthrough["seals"]
           self.options.menace_condition.value = passthrough["menace_condition"]
           self.options.mine_condition.value = passthrough["mine_condition"]
           self.options.garden_condition.value = passthrough["garden_condition"]
        setup_game(self)

        self.auth_id = self.random.getrandbits(32)

    def create_regions(self) -> None:
        init_areas(self, get_locations(self))
        place_static_items(self)
        if self.options.soul_randomizer != SoulRandomizer.option_soulsanity:
            place_static_souls(self)
        if self.options.soul_randomizer != SoulRandomizer.option_soulsanity or self.options.soulsanity_level < SoulsanityLevel.option_medium:
            self.get_location("Imp Soul").place_locked_item(self.create_static_soul("Imp Soul"))

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())
        self.fill_pool(pool)

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Menace Defeated", self.player)

    def generate_output(self, output_directory: str) -> None:
        self.has_generated_output = True  # Make sure data defined in generate output doesn't get added to spoiler only mode
        try:
            code_patch = pkgutil.get_data(__name__, "src/overlay_41.bin")
            patch = DoSProcPatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("dos_base.bsdiff4", pkgutil.get_data(__name__, "src/dos_base.bsdiff4"))
            patch_rom(self, patch, self.player, code_patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def fill_slot_data(self) -> Dict[str, typing.Any]:
        return {
            "goal": self.options.goal.value,
            "starting_warp": self.starting_warp_room,
            "soul_randomizer": self.options.soul_randomizer.value,
            "soulsanity_level": self.options.soulsanity_level.value,
            "open_drawbridge": self.options.open_drawbridge.value,
            "speed_boost": self.options.boost_speed.value,
            "soul_walls": self.red_soul_walls,
            "buttonsanity": self.options.gate_items.value,
            "seals": self.magic_seal_table,
            "menace_condition": self.options.menace_condition.value,
            "garden_condition": self.options.garden_condition.value,
            "mine_condition": self.options.mine_condition.value
        }

    def modify_multidata(self, multidata: dict) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            multidata["connect_names"][self.rom_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.shuffle_starting_warp_room:
            spoiler_handle.write(f"Default Warp Room:    {self.starting_warp_room}\n")

        if self.options.randomize_red_soul_walls:
            spoiler_handle.write(f"\nSoul Barriers:\n")
            spoiler_handle.write(f" Paranoia 1:  {self.red_soul_walls[1]}\n")
            spoiler_handle.write(f" Paranoia 2:  {self.red_soul_walls[0]}\n")
            spoiler_handle.write(f" Paranoia 3:  {self.red_soul_walls[3]}\n")
            spoiler_handle.write(f" Dark Chapel Catacombs:  {self.red_soul_walls[2]}\n")

        if self.options.boss_shuffle:
            spoiler_handle.write(f"\nBosses:\n")
            for boss in self.boss_slots:
                spoiler_handle.write(f" {boss}:  {self.boss_slots[boss].new_boss}\n")

        if self.options.seal_shuffle:
            spoiler_handle.write(f"\nMagic Seals:\n")
            for seal in self.magic_seal_table:
                if seal in ["Mine of Judgment", "The Abyss"] and self.mine_status == "Disabled":  # Ignore Magic Seals that are past the endgame trigger
                    continue
                else:
                    spoiler_handle.write(f" {seal}:  {self.magic_seal_table[seal]}\n")

    def create_item(self, name: str) -> CVDoSItem:
        data = self.set_classifications(name)

        return CVDoSItem(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        weights = {"soul": 10, "money": 20, "weapon": 30, "armor": 40, "consumable": 60}

        # If these pools have been exhausted, set their weights to 0
        if not self.weapon_table:
            weights["weapon"] = 0

        if not self.armor_table:
            weights["armor"] = 0
        
        filler_type = self.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
        weight_table = {
            "soul": soul_filler_table,
            "weapon": self.weapon_table,
            "armor": self.armor_table,
            "money": money_table,
            "consumable": consumable_table,
        }

        filler_item = self.random.choice(weight_table[filler_type])

        if filler_item in self.weapon_table:
            self.weapon_table.remove(filler_item)
        elif filler_item in self.armor_table:
            self.armor_table.remove(filler_item)
        
        if not self.has_tried_chaos_ring:
            self.has_tried_chaos_ring = True
            if self.random.randint(0, 101) <= 10:  # Chaos ring should have a single 10/100 chance to be placed
                filler_item = "Chaos Ring"

        return filler_item

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        return excluded_items

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = CVDoSItem(name, data.classification, data.code, self.player)
        if name in self.important_souls:
            item.classification = ItemClassification.progression

        if self.options.soul_randomizer == SoulRandomizer.option_soulsanity:
            if name == "Soul Eater Ring" and self.options.soulsanity_level == SoulsanityLevel.option_rare:
                item.classification = ItemClassification.progression

        return item

    def fill_pool(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - self.extra_item_count):  # Change to fix event count
            item = self.set_classifications(self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        return pool

    def create_static_soul(self, soul):
        data = item_table[soul]
        item = Item(soul, ItemClassification.progression, None, self.player)  # Create an event item of the soul
        return item
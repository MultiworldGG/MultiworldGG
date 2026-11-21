from dataclasses import dataclass, asdict
import logging
from typing import Any, Tuple
from enum import IntEnum
from Options import (Choice, Toggle, DefaultOnToggle, Range, PerGameCommonOptions, OptionGroup, Removed,
                     DeathLink, StartInventoryPool, ItemSet, ItemDict, OptionSet, OptionDict, NamedRange,
                     FreeText, Option)
from schema import Schema, Optional
from .Items import possible_filler, hint_groups
from .Locations import dungeon_info
from .LADXR.worldSetup import WorldSetup

DefaultOffToggle = Toggle

base_world_setup = WorldSetup()


def convert_ap_options_to_ladxr(options):
    options_dict = options if isinstance(options, dict) else asdict(options)
    ladxr_settings_dict = {}
    for option in options_dict.values():
        if not hasattr(option, 'to_ladxr_option'):
            continue
        name, value = option.to_ladxr_option(options_dict)
        if name:
            ladxr_settings_dict[name] = value
    return ladxr_settings_dict


class Override(IntEnum):
    NEVER = 0
    NOT_RACE = 1
    ALWAYS = 2


class Rich(Option):
    rich_text_doc = True
    default = True

class LADXROption(Rich):
    may_override: Override = Override.NEVER
    ladxr_name: str | None

    def to_ladxr_option(self, all_options) -> Tuple[Any, Any]:
        if not self.ladxr_name:
            return None, None
        return (self.ladxr_name, self.name_lookup[self.value].replace("_", ""))

    def set_to(self, option: str) -> None:
        option_value = getattr(self, f'option_{option}')
        self.value = option_value


class Logic(Choice, LADXROption):
    """
    **Casual:** Prevents players from needing to use bombs or magic powder
    for bush breaking and general combat.

    **Normal:** Playable without using any tricks or glitches. Can require
    knowledge from a vanilla playthrough, such as how to open Color Dungeon.

    **Hard:** More advanced techniques may be required, but glitches are not.
    Examples include tricky jumps, killing enemies with only pots.

    **Glitched:** Advanced glitches and techniques may be required, but
    extremely difficult or tedious tricks are not required. Examples include
    Bomb Triggers, Super Jumps and Jesus Jumps.

    **Hell:** Obscure knowledge and hard techniques may be required. Examples
    include featherless jumping with boots and/or hookshot, sequential pit
    buffers and unclipped superjumps. Things in here can be extremely hard to do
    or very time consuming.
    """
    display_name = "Logic"
    ladxr_name = "logic"
    option_casual = 0
    option_normal = 1
    option_hard = 2
    option_glitched = 3
    option_hell = 4

    default = option_normal


class TradeQuest(DefaultOnToggle, LADXROption):
    """
    Trade quest items are randomized. Each NPC takes its normal trade quest
    item and gives a randomized item in return.
    """
    display_name = "Trade Quest"
    ladxr_name = "tradequest"


class Owlsanity(Choice, LADXROption):
    """
    Replaces the hints from owl statues with additional randomized items.
    These owl statues will no longer give hints.
    """
    display_name = "Owlsanity"
    ladxr_name = "owlstatues"
    option_none = 0
    option_dungeon = 1
    option_overworld = 2
    option_both = 3
    default = option_none
    alias_true = option_both
    alias_false = option_none


class TextShuffle(DefaultOffToggle, LADXROption):
    """
    Shuffles all text in the game.
    """
    display_name = "Text Shuffle"
    ladxr_name = "textshuffle"
    may_override = Override.ALWAYS


class Rooster(DefaultOnToggle, LADXROption):
    """
    Adds the rooster to the item pool. If disabled, the overworld will be
    modified so that any location requiring the rooster is accessible by other
    means.
    """
    display_name = "Rooster"
    ladxr_name = "rooster"


class EntranceRules(Choice, LADXROption):
    """
    **Normal:** Inside always leads to outside, outside always leads to inside.

    **Wild:** Inside can lead to outside, outside can lead to inside.

    **Chaos:** Entrances and exits are decoupled.

    **Insane:** Combines chaos and wild.

    **Madness:** Insane, but multiple entrances can lead to the same location.

    This does nothing unless other settings are enabled to select entrances to shuffle.
    """
    option_normal = 0
    option_wild = 1
    option_chaos = 2
    option_insane = 3
    option_madness = 4
    default = option_normal
    display_name = "Entrance Rules"
    ladxr_name = "entrancerules"
             

class EntranceShuffle(Choice, LADXROption):
    option_disabled = 0
    option_limited = 1
    option_global = 2
    default = option_disabled


class ShuffleStart(EntranceShuffle):
    """
    Randomizes where your starting house is located.

    **Limited:** Your start location will be selected from a curated list of overworld locations.

    **Global:** Your start location is shuffled into the global entrance pool.
    """
    display_name = "Random Start Location"
    ladxr_name = "randomstartlocation"


class ShuffleDungeons(EntranceShuffle):
    """
    Randomizes where dungeon entrances lead to.

    **Limited:** They are shuffled with each other.

    **Global:** They are shuffled into the global entrance pool.
    """
    display_name = "Shuffle Dungeons"
    ladxr_name = "dungeonshuffle"


class ShuffleBasic(EntranceShuffle):
    """
    Randomizes where caves/houses with one entrance and an item lead to.

    **Limited:** They are shuffled with each other.

    **Global:** They are shuffled into the global entrance pool.
    """
    display_name = "Shuffle Basic"
    ladxr_name = "shufflebasic"


class ShuffleJunk(EntranceShuffle):
    """
    Randomizes where caves/houses with one entrance and no items lead to.

    **Limited:** They are shuffled with each other.

    **Global:** They are shuffled into the global entrance pool.
    """
    display_name = "Shuffle Junk"
    ladxr_name = "shufflejunk"


class ShuffleConnectors(EntranceShuffle):
    """
    Randomizes where caves/houses with two entrances lead to.

    **Limited:** They are shuffled with each other.

    **Global:** They are shuffled into the global entrance pool.
    """
    display_name = "Shuffle Connectors"
    ladxr_name = "shuffleconnectors"


class ShuffleWater(EntranceShuffle):
    """
    Randomizes water entrances lead to (Manbo and Damp Cave).

    **Limited:** They are shuffled with each other.

    **Global:** They are shuffled into the global entrance pool.

    Use the warp-to-home from the Save & Quit menu if you get stuck (hold A+B+Start+Select until it works).
    """
    display_name = "Shuffle Water"
    ladxr_name = "shufflewater"


class ShuffleAnnoying(EntranceShuffle):
    """
    Randomizes where a few very annoying entrances lead to (Mamu and the Raft House). 

    **Limited:** They are shuffled with each other.

    **Global:** They are shuffled into the global entrance pool.
    """
    display_name = "Shuffle Annoying"
    ladxr_name = "shuffleannoying"


class WorldSetupSeed(FreeText, Rich):
    """
    Specify seed for entrance shuffle, boss shuffle, miniboss shuffle, and enemizer.
    Does not have to be numeric. Everybody with the same seed will get the same result
    if their relevant settings are the same. At zero, no seed is used.
    """
    display_name = "World Setup Seed"


class LADXPlando(OptionDict, Rich):
    def verify(self, world, player_name, plando_options):
        super().verify(world, player_name, plando_options)
        # verify values
        data = set(self.value.values())
        dataset = set(word.casefold() for word in data) if self.valid_keys_casefold else set(data)
        extra = dataset - self._valid_keys
        if extra:
            raise OptionError(
                f"Found unexpected value {', '.join(extra)} in {getattr(self, 'display_name', self)}. "
                f"Allowed values: {self._valid_keys}."
            )
        schema = Schema({
            Optional(str): str
        })

class EntrancePlando(LADXPlando):
    """
    Define some or all entrance connections. If your entrance rules keep entrances
    coupled, the inverse of your plando connections will be automatically applied for
    you. So if you set up `"mabe_phone": "d1:inside"`, you will also automatically get
    `"d1:inside": "mabe_phone"`. However depending on your shuffle groups, this can
    still leave the groups imbalanced, causing a mapping failure. This can be avoided
    by also mapping the complement, so in this case: `"d1": "mabe_phone:inside"`.
    """
    display_name = "Entrance Plando"
    valid_keys = set(base_world_setup.entrance_mapping)
    valid_values = valid_keys


class BossPlando(LADXPlando):
    """
    Define some or all boss placements. Color dungeon and its boss are not mappable,
    and there can only be one `ANGLER_FISH` and `EVIL_EAGLE`.
    """
    display_name = "Boss Plando"
    valid_keys = set(d.entrance for d in dungeon_info if d.index != 9)
    valid_values = set(d.boss for d in dungeon_info if d.index != 9)

    def verify(self, world, player_name, plando_options):
        super().verify(world, player_name, plando_options)
        fish_count = sum(1 for boss in self.value.values() if boss == "ANGLER_FISH")
        eagle_count = sum(1 for boss in self.value.values() if boss == "EVIL_EAGLE")
        if fish_count > 1 or eagle_count > 1:
            raise OptionError("There can only be one each of ANGLER_FISH and EVIL_EAGLE in boss mapping.")


class MinibossPlando(LADXPlando):
    """
    Define some or all miniboss placements.
    """
    display_name = "Miniboss Plando"
    valid_keys = set(base_world_setup.miniboss_mapping)
    valid_values = set(base_world_setup.miniboss_mapping.values())


class APTitleScreen(DefaultOnToggle, LADXROption):
    """
    Enables AP specific title screen and disables the intro cutscene.
    """
    display_name = "AP Title Screen"
    ladxr_name = "aptitlescreen"
    may_override = Override.ALWAYS


class BossShuffle(Choice, LADXROption):
    """
    Changes the bosses at the end of dungeons.

    **Shuffle:** All the same bosses, just moved around.

    **Randomize:** Completely random boss at each spot.
    Some bosses may be duplicated, others may be missing.
    """
    display_name = "Boss Shuffle"
    option_disabled = 0
    option_shuffle = 1
    option_randomize = 2
    default = option_disabled
    ladxr_name = "boss"
    alias_true = option_shuffle
    alias_false = option_disabled


class MinibossShuffle(Choice, LADXROption):
    """
    Changes the minibosses in dungeons and on the overworld.

    **Shuffle:** All the same minibosses, just moved around.

    **Randomize:** Completely random miniboss at each spot.
    Some minibosses may be duplicated, others may be missing.
    """
    display_name = "Miniboss Shuffle"
    option_disabled = 0
    option_shuffle = 1
    option_randomize = 2
    default = option_disabled
    ladxr_name = "miniboss"
    alias_true = option_shuffle
    alias_false = option_disabled


class Enemizer(Choice, LADXROption):
    """
    Randomizes which enemies are placed. Does not affect logic.
    """
    display_name = "Enemizer"
    option_disabled = 0
    option_overworld = 1
    default = option_disabled
    ladxr_name = "enemies"
    alias_true = option_overworld
    alias_false = option_disabled


class DungeonItemShuffle(Choice, Rich):
    display_name = "Dungeon Item Shuffle"
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    # option_delete = 5
    # option_start_inventory = 6
    alias_true = 3
    alias_false = 0
    ladxr_item: str


class ShuffleNightmareKeys(DungeonItemShuffle, LADXROption):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.

    **Start Inventory:** The item will be in your starting inventory.
    """
    display_name = "Shuffle Nightmare Keys"
    ladxr_item = "NIGHTMARE_KEY"
    ladxr_name = "shufflenightmarekeys"
    option_start_inventory = 6


class ShuffleSmallKeys(DungeonItemShuffle, LADXROption):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.

    **Start Inventory:** The item will be in your starting inventory.
    """
    display_name = "Shuffle Small Keys"
    ladxr_item = "KEY"
    ladxr_name = "shufflesmallkeys"
    option_start_inventory = 6


class ShuffleMaps(DungeonItemShuffle, LADXROption):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.

    **Start Inventory:** The item will be in your starting inventory.
    """
    display_name = "Shuffle Maps"
    ladxr_item = "MAP"
    ladxr_name = "shufflemaps"
    option_start_inventory = 6


class ShuffleCompasses(DungeonItemShuffle, LADXROption):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.

    **Start Inventory:** The item will be in your starting inventory.
    """
    display_name = "Shuffle Compasses"
    ladxr_item = "COMPASS"
    ladxr_name = "shufflecompasses"
    option_start_inventory = 6


class ShuffleStoneBeaks(DungeonItemShuffle, LADXROption):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.

    **Start Inventory:** The item will be in your starting inventory.
    """
    display_name = "Shuffle Stone Beaks"
    ladxr_item = "STONE_BEAK"
    ladxr_name = "shufflestonebeaks"
    option_start_inventory = 6


class ShuffleInstruments(DungeonItemShuffle, LADXROption):
    """
    **Original Dungeon:** The item will be within its original dungeon.

    **Own Dungeons:** The item will be within a dungeon in your world.

    **Own World:** The item will be somewhere in your world.

    **Any World:** The item could be anywhere.

    **Different World:** The item will be somewhere in another world.

    **Vanilla:** The item will be in its vanilla location in your world.
    """
    display_name = "Shuffle Instruments"
    ladxr_item = "INSTRUMENT"
    option_vanilla = -1
    default = option_vanilla
    alias_false = option_vanilla
    ladxr_name = "shuffleinstruments"

    def is_in_original_dungeon(self):
        return self.value <= self.option_original_dungeon


class Goal(Choice, LADXROption):
    """
    **Instruments:** The Wind Fish's Egg will only open if you have the required
    number of Instruments of the Sirens, and play the Ballad of the Wind Fish.

    **Specific:** The Wind Fish's Egg will open with specific instruments,
    check the sign at the egg to see which.

    **Seashells:** The Egg will open when you bring 20 seashells.
    The Ballad and Ocarina are not needed.

    **Open:** The Egg will start pre-opened.
    """
    display_name = "Goal"
    ladxr_name = "goal"
    option_instruments = 1
    option_specific = 2
    option_seashells = 10
    option_open = 100

    default = option_instruments

    def to_ladxr_option(self, all_options):
        if self.value == self.option_instruments:
            return ("goal", int(all_options["instrument_count"]))
        else:
            return LADXROption.to_ladxr_option(self, all_options)


class InstrumentCount(Range, LADXROption):
    """
    Sets the number of instruments required to open the Egg.
    """
    display_name = "Required Instrument Count"
    ladxr_name = "goalcount"
    range_start = 0
    range_end = 8
    default = 8

    def to_ladxr_option(self, all_options):
        return (self.ladxr_name, int(all_options["instrument_count"]))

    def set_min(self, n: int):
        self.value = min(self.value, n)


class SpecificOptionalDungeons(Choice, LADXROption):
    """
    Choose what happens to dungeons without instruments in the specific
    instruments goal. Color Dungeon will not be affected. Does nothing if
    instruments are shuffled outside of their dungeons.

    Condensing a dungeon strips it down to three rooms, mostly just a
    boss fight.
    """
    display_name = "Specific Optional Dungeons"
    ladxr_name = "specificoptionaldungeons"
    option_normal = 0
    option_condense = 1
    alias_condensed = 1
    option_condense_and_exclude = 2
    alias_condensed_and_excluded = 2
    default = option_normal


class NagMessages(DefaultOffToggle, LADXROption):
    """
    Controls if nag messages are shown when rocks and crystals are touched.
    Useful for glitches, annoying for everything else.
    """
    display_name = "Nag Messages"
    ladxr_name = "nagmessages"
    may_override = Override.ALWAYS


class MusicChangeCondition(Choice, LADXROption):
    """
    Controls how the music changes.

    **Sword:** When you pick up a sword, the music changes.

    **Always:** You always have the post-sword music.
    """
    display_name = "Music Change Condition"
    option_sword = 0
    option_always = 1
    default = option_always
    ladxr_name = "musicchange"
    may_override = Override.ALWAYS


class HardMode(Choice, LADXROption):
    """
    **Oracle:** Less iframes and health from drops. Bombs damage yourself. Water
    damages you without flippers. No pieces of power or acorns.

    **Hero:** Switch version hero mode, double damage, no heart/fairy drops.

    **OHKO:** You die on a single hit, always.
    """
    display_name = "Hard Mode"
    ladxr_name = "hardmode"
    option_none = 0
    option_oracle = 1
    option_hero = 2
    option_ohko = 3
    default = option_none


class Stealing(Choice, LADXROption):
    """
    Puts stealing from the shop in logic if the player has a sword.
    """
    display_name = "Stealing"
    ladxr_name = "steal"
    option_in_logic = 1
    option_out_of_logic = 2
    option_disabled = 3
    default = option_out_of_logic


class Overworld(Choice, LADXROption):
    """
    **Open Mabe:** Replaces rocks on the east side of Mabe Village with bushes,
    allowing access to Ukuku Prairie without Power Bracelet.

    **Open Beach:** Replaces rocks on the east side of the beach with bushes,
    allowing access to Martha's Bay without Power Bracelet.

    **Dungeon Dive:** Creates a different overworld where all the dungeons are
    directly accessible and very few are located in the overworld.
    """
    display_name = "Overworld"
    ladxr_name = "overworld"
    option_normal = 0
    option_open_mabe = 1
    option_open_beach = 2
    option_dungeon_dive = 3
    default = option_normal


class Quickswap(Choice, LADXROption):
    """
    Instead of opening the map, the *SELECT* button swaps the top item of your inventory on to your *A* or *B* button.
    """
    display_name = "Quickswap"
    ladxr_name = "quickswap"
    may_override = Override.ALWAYS
    option_none = 0
    option_a = 1
    option_b = 2
    default = option_none


class TextMode(Choice, LADXROption):
    """
    **Fast:** Makes text appear twice as fast.

    **None:** Fast, but all dialogs are emptied. Empty text boxes will still come up.
    """
    display_name = "Text Mode"
    ladxr_name = "textmode"
    may_override = Override.ALWAYS
    option_normal = 0
    option_fast = 1
    option_none = 2
    default = option_fast


class LowHpBeep(Choice, LADXROption):
    """
    Slows or disables the low health beeping sound.
    """
    display_name = "Low HP Beep"
    ladxr_name = "lowhpbeep"
    may_override = Override.ALWAYS
    option_default = 0
    option_slow = 1
    option_none = 2
    default = option_default


class NoFlash(DefaultOnToggle, LADXROption):
    """
    Remove the flashing light effects from Mamu, shopkeeper and MadBatter.
    Useful for capture cards and people that are sensitive to these things.
    """
    display_name = "No Flash"
    ladxr_name = "noflash"
    may_override = Override.ALWAYS


class BootsControls(Choice, LADXROption):
    """
    Adds an additional button to activate Pegasus Boots (does nothing if you
    haven't picked up your boots!)

    **Vanilla:** Nothing changes, you have to equip the boots to use them.

    **Bracelet:** Holding down the button for the bracelet also activates boots
    (somewhat like Link to the Past).

    **Press A:** Holding down A activates boots.

    **Press B:** Holding down B activates boots.
    """
    display_name = "Boots Controls"
    option_vanilla = 0
    option_bracelet = 1
    option_press_a = 2
    alias_a = 2
    option_press_b = 3
    alias_b = 3
    ladxr_name = "bootscontrols"
    may_override = Override.ALWAYS


class LinkPalette(Choice, LADXROption):
    """
    Sets Link's palette.

    A-D are color palettes usually used during the damage animation and can
    change based on where you are.
    """
    display_name = "Link's Palette"
    ladxr_name = "linkspalette"
    may_override = Override.ALWAYS
    option_normal = -1
    option_green = 0
    option_yellow = 1
    option_red = 2
    option_blue = 3
    option_invert_a = 4
    option_invert_b = 5
    option_invert_c = 6
    option_invert_d = 7
    default = option_normal

    def to_ladxr_option(self, all_options):
        return self.ladxr_name, str(self.value)


class TrendyGame(Choice, LADXROption):
    """
    **Easy:** All of the items hold still for you.

    **Normal:** The vanilla behavior.

    **Hard:** The trade item also moves.

    **Harder:** The items move faster.

    **Hardest:** The items move diagonally.

    **Impossible:** The items move impossibly fast, may scroll on and off the
    screen.
    """
    display_name = "Trendy Game"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_harder = 3
    option_hardest = 4
    option_impossible = 5
    default = option_normal
    ladxr_name = "trendygame"
    may_override = Override.NOT_RACE


class BlockFreePowder(DefaultOffToggle, LADXROption):
    """
    Trendy game, floating, and freestanding magic powder won't do anything
    unless you have received/found the magic powder item.

    This has no logic implications, because these powder pickups are never
    considered in logic.
    """
    display_name = "Block Free Powder"
    ladxr_name = 'blockfreepowder'
    may_override = Override.NOT_RACE


class GfxMod(DefaultOffToggle, LADXROption):
    """
    If enabled, the patcher will prompt the user for a modification file to change sprites in the game and optionally some text.
    """
    display_name = "GFX Modification"
    ladxr_name = "gfxmod"
    may_override = Override.ALWAYS


class Palette(Choice, LADXROption):
    """
    Sets the palette for the game.

    Note: A few places aren't patched, such as the menu and a few color dungeon
    tiles.

    **Normal:** The vanilla palette.

    **1-Bit:** One bit of color per channel.

    **2-Bit:** Two bits of color per channel.

    **Greyscale:** Shades of grey.

    **Pink:** Aesthetic.

    **Inverted:** Inverted.
    """
    display_name = "Palette"
    option_normal = 0
    option_1bit = 1
    option_2bit = 2
    option_greyscale = 3
    option_pink = 4
    option_inverted = 5
    ladxr_name = "palette"
    may_override = Override.ALWAYS


class Music(Choice, LADXROption):
    """
    **Vanilla:** Regular Music

    **Shuffled:** Shuffled Music

    **Off:** No music
    """
    display_name = "Music"
    ladxr_name = "music"
    may_override = Override.ALWAYS
    option_vanilla = 0
    option_shuffled = 1
    option_off = 2

    def to_ladxr_option(self, all_options):
        s = ""
        if self.value == self.option_shuffled:
            s = "random"
        elif self.value == self.option_off:
            s = "off"
        return self.ladxr_name, s


class Warps(Choice, LADXROption):
    """
    **Improved:** Adds remake style warp screen to the game. Choose your warp
    destination on the map after jumping in a portal and press *B* to select.

    **Improved Additional:** Additionally, adds a warp point at Crazy
    Tracy's house (the Mambo teleport spot) and Eagle's Tower.
    """
    display_name = "Warps"
    option_vanilla = 0
    option_improved = 1
    option_improved_additional = 2
    default = option_vanilla
    ladxr_name = 'warps'
    may_override = Override.NOT_RACE


class InGameHintItemGroups(OptionSet, Rich):
    """
    Choose which item groups to generate in-game hints for. Disabling everything
    effectively disables hints.

    Available groups: Entrance Keys, Equipment, Instruments, Nightmare Keys,
    Seashells, Small Keys, Songs, Stone Beaks, Trading Items
    """
    display_name = "In-Game Hint Items"
    default = {
        "Equipment",
        "Entrance Keys"
    }
    valid_keys = hint_groups


class ExpandStart(NamedRange, Rich):
    """
    Starting from Tarin's Gift, locally place progression items until the target
    number of locations or more can be reached. Does nothing if set to 1.
    When set to 2 it will only ever place an item on Tarin's Gift.
    Interferes with item plando at higher settings.
    """
    display_name = "Expand Start"
    range_start = 1
    range_end = 10
    default = 5
    special_range_names = {
        "disabled": 1,
        "only_tarins_gift": 2,
        "recommended": 5,
        "high": 10,
    }


class ReserveFiller(NamedRange, Rich):
    """
    Removes non-essential items to make more room for filler.
    The actual amount of filler removed will depend on other settings,
    but this option will usually define the minimum number of filler
    items in the world. At extremely high reserve filler amounts or
    extremely low location counts, you may end up with less filler
    than specified, after it has run out of items to remove.
    """
    display_name = "Reserve Filler"
    range_start = 0
    range_end = 175
    default = 6
    special_range_names = {
        "none": 0,
        "default": 6,
        "reasonable": 20,
        "extreme": 50,
    }


class FillerPool(ItemDict, Rich):
    """
    Weighted options to randomly select from when creating filler items.

    Available items: 10 Arrows, 20 Rupees, Anti-Heart Container, Bomb Drop,
    Bombs, Cucco Party, Death, Fairy, Guardian Acorn, Magic Powder,
    Medicine, Nothing, Piece of Power, Recovery Heart, Seashell,
    Single Arrow, Slime Storm, Zol Attack
    """
    display_name = "Filler Pool"
    default = {
        "Bombs": 10,
        "Single Arrow": 5,
        "10 Arrows": 10,
        "Magic Powder": 10,
        "Medicine": 1,
    }
    valid_keys = possible_filler


class ForeignItemIcons(Choice, LADXROption):
    """
    Choose how to display foreign items.

    **Guess By Name:** Foreign items can look like any Link's Awakening item.

    **Indicate Progression:** Foreign items are displayed with an archipelago icon.
    Color cycling indicates high value progression, two-tone indicates deprioritized
    progression, flat indicates non-progression.
    """
    display_name = "Foreign Item Icons"
    option_guess_by_name = 0
    option_indicate_progression = 1
    default = option_guess_by_name
    ladxr_name = 'foreignitemicons'


class Follower(Choice, LADXROption):
    """
    Gives you a pet follower in the game.
    """
    display_name = "Follower"
    option_none = 0
    option_fox = 1
    option_navi = 2
    option_ghost = 3
    option_yip_yip = 4
    ladxr_name = 'follower'


class CondenseDungeons(OptionSet, Rich):
    """
    Transforms a dungeon into a tiny version, with mostly just a boss fight.

    Condensing all dungeons is equivalent to the upstream *no dungeons* overworld.

    Excluding a full dungeon by entering its location group into
    `exclude_locations` will automatically condense it.

    Dungeon names: Color Dungeon, Tail Cave, Bottle Grotto, Key Cavern,
    Angler's Tunnel, Catfish's Maw, Face Shrine, Eagle's Tower, Turtle Rock
    """
    display_name = "Condense Dungeons"
    valid_keys = [d.name for d in dungeon_info]


ladx_option_groups = [
    OptionGroup("World", [
        Overworld,
        CondenseDungeons,
        Warps,
    ]),
    OptionGroup("Items", [
        ShuffleInstruments,
        ShuffleNightmareKeys,
        ShuffleSmallKeys,
        ShuffleMaps,
        ShuffleCompasses,
        ShuffleStoneBeaks,
        TradeQuest,
        Rooster,
        Owlsanity,
        InGameHintItemGroups,
        ReserveFiller,
        FillerPool,
    ]),
    OptionGroup("Entrances", [
        EntranceRules,
        ShuffleStart,
        ShuffleDungeons,
        ShuffleBasic,
        ShuffleJunk,
        ShuffleConnectors,
        ShuffleWater,
        ShuffleAnnoying,
    ]),
    OptionGroup("Enemies", [
        BossShuffle,
        MinibossShuffle,
        Enemizer,
    ]),
    OptionGroup("Seeding & Plando", [
        WorldSetupSeed,
        EntrancePlando,
        BossPlando,
        MinibossPlando,
    ]),
    OptionGroup("Quality of Life & Aesthetic", [
        NagMessages,
        Quickswap,
        BootsControls,
        ForeignItemIcons,
        GfxMod,
        LinkPalette,
        Palette,
        APTitleScreen,
        TextShuffle,
        TextMode,
        Music,
        MusicChangeCondition,
        LowHpBeep,
        NoFlash,
        Follower,
        TrendyGame,
    ]),
    OptionGroup("Miscellaneous", [
        HardMode,
        Stealing,
        BlockFreePowder,
        DeathLink,
    ]),
]

@dataclass
class LinksAwakeningOptions(PerGameCommonOptions):
    expand_start: ExpandStart
    logic: Logic
    goal: Goal
    instrument_count: InstrumentCount
    specific_optional_dungeons: SpecificOptionalDungeons
    stealing: Stealing
    tradequest: TradeQuest
    rooster: Rooster
    entrance_rules: EntranceRules
    shuffle_start: ShuffleStart
    shuffle_dungeons: ShuffleDungeons
    shuffle_basic: ShuffleBasic
    shuffle_junk: ShuffleJunk
    shuffle_connectors: ShuffleConnectors
    shuffle_water: ShuffleWater
    shuffle_annoying: ShuffleAnnoying
    condense_dungeons: CondenseDungeons
    link_palette: LinkPalette
    warps: Warps
    trendy_game: TrendyGame
    gfxmod: GfxMod
    palette: Palette
    text_shuffle: TextShuffle
    foreign_item_icons: ForeignItemIcons
    shuffle_nightmare_keys: ShuffleNightmareKeys
    shuffle_small_keys: ShuffleSmallKeys
    shuffle_maps: ShuffleMaps
    shuffle_compasses: ShuffleCompasses
    shuffle_stone_beaks: ShuffleStoneBeaks
    music: Music
    shuffle_instruments: ShuffleInstruments
    music_change_condition: MusicChangeCondition
    nag_messages: NagMessages
    ap_title_screen: APTitleScreen
    boots_controls: BootsControls
    quickswap: Quickswap
    hard_mode: HardMode
    low_hp_beep: LowHpBeep
    text_mode: TextMode
    no_flash: NoFlash
    in_game_hint_item_groups: InGameHintItemGroups
    overworld: Overworld
    death_link: DeathLink
    reserve_filler: ReserveFiller
    filler_pool: FillerPool
    start_inventory_from_pool: StartInventoryPool
    follower: Follower
    block_free_powder: BlockFreePowder
    owlsanity: Owlsanity
    boss_shuffle: BossShuffle
    miniboss_shuffle: MinibossShuffle
    enemizer: Enemizer
    world_setup_seed: WorldSetupSeed
    entrance_plando: EntrancePlando
    boss_plando: BossPlando
    miniboss_plando: MinibossPlando

    warp_improvements: Removed
    additional_warp_points: Removed
    stabilize_item_pool: Removed
    tarins_gift: Removed
    experimental_dungeon_shuffle: Removed
    experimental_entrance_shuffle: Removed
    in_game_hints: Removed
    more_filler: Removed
    entrance_shuffle: Removed
    in_game_hint_count: Removed
    in_game_hint_excluded_items: Removed
    in_game_hint_priority_items: Removed

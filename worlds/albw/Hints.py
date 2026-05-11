from random import Random
from typing import List, Tuple
from BaseClasses import Item, LocationProgressType, MultiWorld
from .Items import Items, ItemData, ItemType, item_table
from .Locations import Dungeon, LocationType, dungeon_table
from .Options import ALBWOptions, NiceItems

charset = \
    " !\"#$%&'()*+,-./" \
    "0123456789:;<=>?" \
    "ABCDEFGHIJKLMNOP" \
    "QRSTUVWXYZ[]^_`a" \
    "bcdefghijklmnopq" \
    "rstuvwxyz{|}~¡¢£" \
    "¤¥¦§¨©ª«¬®¯°±²³´" \
    "µ¶·¸¹º»¼½¾¿ÀÁÂÃÄ" \
    "ÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔ" \
    "ÕÖ×ØÙÚÛÜÝÞßàáâãä" \
    "åæçèéêëìíîïðñòóô" \
    "õö÷øùúûüýþÿĀāĂăĄ" \
    "ąĆćĊċČčĎďĒēĖėĘęĚ" \
    "ěĞğĠġĢģĦħĪīĮįİıĲ" \
    "ĳĶķĹĺĻļĽľŁłŃńŅņŇ" \
    "ňŐőŒœŔŕŘřŚśŞşŠšŤ" \
    "ťŪūŮůŰűŲųŸŹźŻżŽž" \
    "ƒǅǆǲǳȚțˇ˘˙˛˜;΄΅Ά" \
    "·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘ" \
    "ΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ" \
    "ΪΫάέήίΰαβγδεζηθι" \
    "κλμνξοπρςστυφχψω" \
    "ϊϋόύώЁАБВГДЕЖЗИЙ" \
    "КЛМНОПРСТУФХЦЧШЩ" \
    "ЪЫЬЭЮЯабвгдежзий" \
    "клмнопрстуфхцчшщ" \
    "ъыьэюяё–—‘’‚‛“”„" \
    "†‡•…‰′″‹›※€№™←↑→" \
    "↓⇒⇔∀∂√∞∴∵⊂⊃⌒■□▲△" \
    "▼▽◆◇○◎●★☆♀♂♥♪♭　、" \
    "。〃々〆「」『』【】〒ぁあぃいぅ" \
    "うぇえぉおかがきぎくぐけげこごさ" \
    "ざしじすずせぜそぞただちぢっつづ" \
    "てでとどなにぬねのはばぱひびぴふ" \
    "ぶぷへべぺほぼぽまみむめもゃやゅ" \
    "ゆょよらりるれろゎわをんゝゞァア" \
    "ィイゥウェエォオカガキギクグケゲ" \
    "コゴサザシジスズセゼソゾタダチヂ" \
    "ッツヅテデトドナニヌネノハバパヒ" \
    "ビピフブプヘベペホボポマミムメモ" \
    "ャヤュユョヨラリルレロヮワヲンヴ" \
    "ヵヶ・ー仝" \
    "！？～"

def sanitize(string: str) -> str:
    return "".join([char if char in charset else "?" for char in string])

def color_item(name: str) -> str:
    return f"@9:{sanitize(name)}@"

def color_location(name: str) -> str:
    return f"@10:{sanitize(name)}@"

def color_region(name: str) -> str:
    return f"@10:{sanitize(name)}@"

def color_player(name: str) -> str:
    return f"@8:{sanitize(name)}@"

def color_dungeon(dungeon: Dungeon) -> str:
    return f"@{dungeon.textcolor}:{dungeon.name}@"

junk_hints: List[str] = [
    "Dodongo dislikes smoke.",
    "I am Error.",
    "The Wind Fish in name only, for it is neither.",
    "Rupees can be found in your wallet.",
    "Items can be found in chests.",
    "The Whopper can be found at Burger King.",
    "The Triforce can be found in the Sacred Realm.",
    "Bunnies are cute.",
    "Trans rights are human rights.",
    "An archipelago is a group of islands.",
    "There is a secret passage under one of the graves.",
    "You need gloves to lift rocks.",
    "Try bombing suspicious walls.",
    "Boots make you go fast.",
    "A fairy can help you out in a pinch.",
    "You need the Bow of Light to defeat Ganon.",
    "Spoiler: Ganon is Link's father.",
    "The word \"gullible\" is written in the sky.",
    "Ghosts... don't... DIE!",
    "Somebody once told me the world was gonna roll me.",
    "Help! I'm trapped in a hint writing factory.",
    "Boo!",
    "Remember to stay hydrated.",
    "Tell someone you love them.",
]

long_locations: List[Tuple[str, str]] = [
    ("Irene", "The gift from Irene is {}."),
    ("Haunted Grove Stump", "A stump in the haunted grove has {}."),
    ("Hyrule Hotfoot 65s", "The prize for the second Hyrule Hotfoot challenge is {}."),
    ("Queen Oren", "Queen Oren rewards you with {}."),
    ("Rosso (1)", "The gift from Rosso is {}."),
    ("Rosso (2)", "Rosso's reward for clearing rocks is {}."),
    ("Blacksmith", "The blacksmith in Hyrule crafts {}."),
    ("[HC] Throne", "In the throne room of Hyrule Castle, you can find {}."),
    ("Master Sword Pedestal", "The prize on the Master Sword Pedestal is {}."),
    ("Bee Guy (2)", "The reward for turning in a gold bee is {}."),
    ("Bouldering Guy", "In exchange for a bottle of milk, a man on Death Mountain gives you {}."),
    ("Octoball Derby", "The prize for winning Octoball Derby is {}."),
    ("Great Rupee Fairy", "A fairy charges you 3000 rupees for {}."),
    ("Blacksmith (Lorule)", "The blacksmith in Lorule crafts {}."),
    ("Thief Girl", "The gift from the thief girl is {}."),
    ("Treacherous Tower", "The reward at the end of the Treacherous Tower is {}."),
]

major_items: List[ItemData] = [
    Items.Bow,
    Items.Boomerang,
    Items.Hookshot,
    Items.Bombs,
    Items.FireRod,
    Items.IceRod,
    Items.Hammer,
    Items.SandRod,
    Items.TornadoRod,
    Items.Boots,
    Items.Flippers,
    Items.Bracelet,
    Items.Quake,
    Items.Lamp,
    Items.Sword,
    Items.Glove,
    Items.Merge,
]

NUM_GHOSTS = 58

def generate_hints(multiworld: MultiWorld, player: int, options: ALBWOptions, random: Random) -> List[str]:
    dungeon_hints = []
    dungeon_count_hints = []
    for dungeon in dungeon_table:
        if "Sanctuary" in dungeon.name:
            continue
        dungeon_item_names = [item.name for item in dungeon.items]
        count = 0
        for loc in dungeon.locations:
            if loc.loctype != LocationType.Normal:
                continue
            item = multiworld.get_location(loc.name, player).item
            if item and not (item.player == player and item.name in dungeon_item_names):
                if item.advancement:
                    count += 1
                if item.advancement and not item.deprioritized and not item.skip_in_prog_balancing:
                    player_possessive = "Your" if item.player == player else color_player(f"{multiworld.get_player_name(item.player)}'s")
                    hint = f"{player_possessive} {color_item(item.name)} can be found in {color_dungeon(dungeon)}."
                    dungeon_hints.append(hint)
        suffix = "" if count == 1 else "s"
        hint = f"{color_dungeon(dungeon)} contains {count} progression item{suffix}."
        dungeon_count_hints.append(hint)

    long_location_hints = []
    for loc_name, hint_format in long_locations:
        try:
            location = multiworld.get_location(loc_name, player)
            if not location or not location.item or location.progress_type == LocationProgressType.EXCLUDED:
                continue
            item = location.item
            player_possessive = "your" if item.player == player else color_player(f"{multiworld.get_player_name(item.player)}'s")
            hint = hint_format.format(f"{player_possessive} {color_item(item.name)}")
            long_location_hints.append(hint)
        except KeyError:
            continue

    major_item_hints = []
    major_names = set([item.name for item in major_items])
    for location in multiworld.find_items_in_locations(major_names, player):
        item = location.item
        item_name = item.name
        item_determiner = "The"
        if item_name.startswith("Progressive "):
            item_name = item_name.partition(" ")[2]
            item_determiner = "A"
        if options.nice_items == NiceItems.option_shuffled and item_table[item.name].itemtype == ItemType.Ravio:
            item_determiner = "A"
        if options.super_items and item.name == Items.Lamp.name:
            item_determiner = "A"
        if item_determiner == "A" and item_name[0] in "AEIOU":
            item_determiner = "An"
        player_possessive = "your" if location.player == player else color_player(f"{multiworld.get_player_name(location.player)}'s")
        region_modifier = ""
        region_chance = 20
        if location.parent_region and location.parent_region.name != "Menu":
            region_modifier = f"the {color_region(location.parent_region.hint_text)} region of "
            region_chance = 60
        if random.randrange(100) < region_chance:
            hint = f"{item_determiner} {color_item(item_name)} can be found in {region_modifier}{player_possessive} world."
        else:
            hint = f"An important item can be found at {color_location(location.name)} in {player_possessive} world."
        major_item_hints.append(hint)
    
    hints = [*dungeon_hints, *dungeon_count_hints, *long_location_hints, *major_item_hints]
    random.shuffle(hints)
    hints = hints[:NUM_GHOSTS]
    while len(hints) < NUM_GHOSTS:
        num_junk_hints = NUM_GHOSTS - len(hints)
        junk_hints_copy = junk_hints[:]
        random.shuffle(junk_hints_copy)
        hints += junk_hints_copy[:num_junk_hints]

    return hints

def generate_bow_of_light_hint(multiworld: MultiWorld, player: int) -> str:
    bow_name = set([Items.BowOfLight.name])
    locations = multiworld.find_items_in_locations(bow_name, player)
    if locations:
        location = locations[0]
        player_possessive = "your" if location.player == player else color_player(f"{multiworld.get_player_name(location.player)}'s")
        hint = f"Did you find the @7:Bow of Light@ at {color_location(location.name)} in {player_possessive} world?"
    else:
        hint = f"Did you find the @7:Bow of Light@?"
    return hint
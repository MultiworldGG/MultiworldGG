# Archipelago MultiWorld integration for Tyrian
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details.

import itertools
import logging
from typing import NamedTuple

from .. import TyrianWorld

# =================================================================================================


class TyrianALTTPText(NamedTuple):
    pedestal: str
    sick_kid: str
    potion_shop: str
    zora: str
    flute_spot: str


# Items associated with text strings -> list of strings to give to ALTTP world
alttp_item_texts: list[tuple[list[str], TyrianALTTPText]] = [
    # Items currently missing:
    # - "Mega Cannon"
    # - "Widget Beam"
    # - "Starburst"
    # - "Fireball"
    # - "Scatter Wave"
    # - "Soul of Zinglon"
    # - "Flare"
    # - "SandStorm"
    # - "Astral Zone"
    # - "Charge Cannon"
    # - "Phoenix Device"
    # - "Plasma Storm"
    # - "Zica Flamethrower"
    # - "Side Ship"
    # - "MicroSol FrontBlaster"
    # - "BattleShip-Class Firebomb"
    # - "Protron Cannon Indigo"
    # - "Protron Cannon Tangerine"
    # - "MicroSol FrontBlaster II"
    # - "Beno Wallop Beam"
    # - "Beno Protron System -B-"

    (  # Levels
        ["TYRIAN (Episode 1)", "BUBBLES (Episode 1)", "HOLES (Episode 1)", "SOH JIN (Episode 1)",
              "ASTEROID1 (Episode 1)", "ASTEROID2 (Episode 1)", "ASTEROID? (Episode 1)", "MINEMAZE (Episode 1)",
              "WINDY (Episode 1)", "SAVARA (Episode 1)", "SAVARA II (Episode 1)", "BONUS (Episode 1)",
              "MINES (Episode 1)", "DELIANI (Episode 1)", "SAVARA V (Episode 1)", "ASSASSIN (Episode 1)",
              "TORM (Episode 2)", "GYGES (Episode 2)", "BONUS 1 (Episode 2)", "ASTCITY (Episode 2)",
              "BONUS 2 (Episode 2)", "GEM WAR (Episode 2)", "MARKERS (Episode 2)", "MISTAKES (Episode 2)",
              "SOH JIN (Episode 2)", "BOTANY A (Episode 2)", "BOTANY B (Episode 2)", "GRYPHON (Episode 2)",
              "GAUNTLET (Episode 3)", "IXMUCANE (Episode 3)", "BONUS (Episode 3)", "STARGATE (Episode 3)",
              "AST. CITY (Episode 3)", "SAWBLADES (Episode 3)", "CAMANIS (Episode 3)", "MACES (Episode 3)",
              "TYRIAN X (Episode 3)", "SAVARA Y (Episode 3)", "NEW DELI (Episode 3)", "FLEET (Episode 3)",
              "SURFACE (Episode 4)", "WINDY (Episode 4)", "LAVA RUN (Episode 4)", "CORE (Episode 4)",
              "LAVA EXIT (Episode 4)", "DESERTRUN (Episode 4)", "SIDE EXIT (Episode 4)", "?TUNNEL? (Episode 4)",
              "ICE EXIT (Episode 4)", "ICESECRET (Episode 4)", "HARVEST (Episode 4)", "UNDERDELI (Episode 4)",
              "APPROACH (Episode 4)", "SAVARA IV (Episode 4)", "DREAD-NOT (Episode 4)", "EYESPY (Episode 4)",
              "BRAINIAC (Episode 4)", "NOSE DRIP (Episode 4)", "ASTEROIDS (Episode 5)", "AST ROCK (Episode 5)",
              "MINERS (Episode 5)", "SAVARA (Episode 5)", "CORAL (Episode 5)", "STATION (Episode 5)",
              # "CANYONRUN (Episode 5)",
              "FRUIT (Episode 5)"],
        TyrianALTTPText(
              pedestal="and the ship coordinates",
              sick_kid="the planet-watching kid",
              potion_shop="shrooms to guide you",
              zora="ship coordinates for sale",
              flute_spot="star boy finds planet again")
    ),
    (  # Pulse Weapons
        ["Pulse-Cannon", "Multi-Cannon (Front)", "Mega Pulse (Front)", "Hyper Pulse", "NortShip Super Pulse",
              "Multi-Cannon (Rear)", "Mega Pulse (Rear)", "NortShip Spreader", "NortShip Spreader B", "Pulse Blast",
              "Single Shot Option", "Dual Shot Option"],
        TyrianALTTPText(
              pedestal="and the pulse shooter",
              sick_kid="the pulse-beam kid",
              potion_shop="shrooms to go pew pew",
              zora="pulse gun for sale",
              flute_spot="pulse boy goes pew pew again")
    ),
    (  # Protron Weapons
        ["Protron Z", "Protron (Front)", "Protron Wave", "Protron (Rear)", "Pearl Wind", "Protron Dispersal"],
        TyrianALTTPText(
              pedestal="and the orb shooter",
              sick_kid="the orb-making kid",
              potion_shop="press shrooms into spheres",
              zora="orb maker for sale",
              flute_spot="orb boy throws sphere again")
    ),
    (  # Vulcan Weapons
        ["Vulcan Cannon (Front)", "Vulcan Cannon (Rear)", "Dual Vulcan", "Vulcan Shot Option"],
        TyrianALTTPText(
              pedestal="and the quick shooter",
              sick_kid="the quick-draw kid",
              potion_shop="shrooms with bullet holes",
              zora="rapid shooter for sale",
              flute_spot="vulcan boy shoots fast again")
    ),
    (  # Laser Weapons
        ["Laser", "Zica Laser", "Needle Laser", "MegaLaser Dual", "MegaLaser", "SDF Main Gun", "Zica SuperCharger"],
        TyrianALTTPText(
              pedestal="and the space laser",
              sick_kid="the laser-beam kid",
              potion_shop="dealing for illegal lasers",
              zora="laser beams for sale",
              flute_spot="laser boy shines beam again")
    ),
    (  # Missile Weapons
        ["Missile Launcher", "Heavy Missile Launcher (Front)", "Heavy Missile Launcher (Rear)", "Missile Pod",
              "MegaMissile", "Atom Bombs", "Mini-Missile", "Buster Rocket"],
        TyrianALTTPText(
              pedestal="and the space missile",
              sick_kid="the missile-making kid",
              potion_shop="rocket shrooms",
              zora="rocket launcher for sale",
              flute_spot="rocket boy fires missile again")
    ),
    (  # Guided Bomb Weapons
        ["Guided Bombs", "Guided Micro Bombs", "Heavy Guided Bombs"],
        TyrianALTTPText(
              pedestal="and the guided booms",
              sick_kid="the homing-boom kid",
              potion_shop="homing in on shrooms",
              zora="guided bombs for sale",
              flute_spot="homing boy finds target again")
    ),
    (  # Lightning Weapons
        ["Lightning Cannon", "Lightning Zone"],
        TyrianALTTPText(
              pedestal="and the zap cannon",
              sick_kid="the zap-touch kid",
              potion_shop="shrooms will zap you",
              zora="very very frightening",
              flute_spot="wizard boy zaps things again")
    ),
    (  # Audio Weapons
        ["Sonic Impulse", "Sonic Wave"],
        TyrianALTTPText(
              pedestal="and the audio device",
              sick_kid="the boom-box kid",
              potion_shop="the loudest shrooms",
              zora="noise complaints for sale",
              flute_spot="loud boy makes noise again")
    ),
    (  # Fruit Weapons
        ["Banana Blast (Front)", "The Orange Juicer", "Banana Blast (Rear)", "Banana Bomb", "Orange Shield",
              "Tropical Cherry Companion"],
        TyrianALTTPText(
              pedestal="and the fruit shooter",
              sick_kid="the fruit-throwing kid",
              potion_shop="throwing food away",
              zora="space fruit for sale",
              flute_spot="fruit boy wastes food again")
    ),
    (  # Snack-food Weapons
        ["HotDog (Front)", "Pretzel Missile", "HotDog (Rear)", "People Pretzels", "Super Pretzel", "Bubble Gum-Gun"],
        TyrianALTTPText(
              pedestal="and the snack shooter",
              sick_kid="the snack-tossing kid",
              potion_shop="throwing food away",
              zora="space snack for sale",
              flute_spot="snack boy wastes food again")
    ),
    (  # Ninja Weapons
        ["Shuriken Field", "Poison Bomb", "Blade Field"],
        TyrianALTTPText(
              pedestal="and the ninja tools",
              sick_kid="the ninja kid",
              potion_shop="shrooms for ninja stuff",
              zora="ninja gear for sale",
              flute_spot="ninja boy hides again")
    ),
    (  # Ball Weapons
        ["RetroBall", "Wild Ball", "Xega Ball"],
        TyrianALTTPText(
              pedestal="and the funky ball",
              sick_kid="the pitcher kid",
              potion_shop="shrooms for weird ball",
              zora="strange ball for sale",
              flute_spot="funky boy tosses ball again")
    ),
    (  # Dragon Weapons
        ["Dragon Frost", "Dragon Flame", "Dragon Lightning"],
        TyrianALTTPText(
              pedestal="and the dragon breath",
              sick_kid="the dragon kid",
              potion_shop="shrooms only for dragons",
              zora="dragon breath for sale",
              flute_spot="dragon boy breathes again")
    ),
    (  # MicroBombs
        ["MicroBomb", "8-Way MicroBomb"],
        TyrianALTTPText(
              pedestal="and the tiny bomb",
              sick_kid="the mini-boom kid",
              potion_shop="shrooms for little boom",
              zora="mini boom for sale",
              flute_spot="mini boy goes boom again")
    ),
    (  # Companion Ships
        ["Companion Ship Warfly", "Companion Ship Gerund", "Companion Ship Quicksilver"],
        TyrianALTTPText(
              pedestal="and the companion",
              sick_kid="kid flies along with you",
              potion_shop="shrooms for a friend",
              zora="companionship for sale",
              flute_spot="lonely boy has friend again")
    ),
    (  # Generators
        ["Advanced MR-12", "Gencore Custom MR-12", "Standard MicroFusion", "Advanced MicroFusion",
              "Gravitron Pulse-Wave", "Progressive Generator"],
        TyrianALTTPText(
              pedestal="and the energy device",
              sick_kid="the power-plant kid",
              potion_shop="shrooms to make power",
              zora="power plant for sale",
              flute_spot="energy boy makes power again")
    ),
    (  # Money
        ["50 Credits", "75 Credits", "100 Credits", "150 Credits", "200 Credits", "300 Credits", "375 Credits",
              "500 Credits", "750 Credits", "800 Credits", "1000 Credits", "2000 Credits", "5000 Credits",
              "7500 Credits", "10000 Credits", "20000 Credits", "40000 Credits"],
        TyrianALTTPText(
              pedestal="and the space money",
              sick_kid="the currency conversion kid",
              potion_shop="shrooms for other currency",
              zora="bad exchange rate for sale",
              flute_spot="space boy sends money again")
    ),
    (  # Large Money
        ["75000 Credits", "100000 Credits", "1000000 Credits"],
        TyrianALTTPText(
              pedestal="and the space jackpot",
              sick_kid="the very rich kid",
              potion_shop="one very expensive shroom",
              zora="good exchange rate for sale",
              flute_spot="lucky boy wins lottery again")
    ),

    # Singletons
    (
        ["Atomic RailGun"],
        TyrianALTTPText(
              pedestal="and the overpowered gun",
              sick_kid="the quad-damage kid",
              potion_shop="shrooms for quad damage",
              zora="quad damage for sale",
              flute_spot="quake boy is overpowered again")
    ),
    (
        ["Repulsor"],
        TyrianALTTPText(
              pedestal="and social distancing",
              sick_kid="kid didn't want company",
              potion_shop="stay away from shrooms",
              zora="zora says go away",
              flute_spot="distant boy stays home again")
    ),
    (
        ["Ice Beam"],
        TyrianALTTPText(
              pedestal="and the freeze beam",
              sick_kid="the frozen-solid kid",
              potion_shop="ice cold frozen shrooms",
              zora="chill beam for sale",
              flute_spot="icy boy freezes things again")
    ),
    (
        ["Attractor"],
        TyrianALTTPText(
              pedestal="and the super magnet",
              sick_kid="the magnetic kid",
              potion_shop="the shrooms are attractive",
              zora="strong magnets for sale",
              flute_spot="magnet boy attracts again"),
    ),
    (
        ["MineField"],
        TyrianALTTPText(
              pedestal="and the tiny bomb",
              sick_kid="the many-boom kid",
              potion_shop="shrooms for lots of boom",
              zora="many booms for sale",
              flute_spot="mini boy scatters mines again")
    ),
    (
        ["Invulnerability"],
        TyrianALTTPText(
              pedestal="and your i-frames",
              sick_kid="the invulnerable kid",
              potion_shop="indestructible shrooms",
              zora="i-frames for sale",
              flute_spot="super boy has i-frames again"),
    ),
    (
        ["Wobbley"],
        TyrianALTTPText(
              pedestal="and the wobble beam",
              sick_kid="the wobbling kid",
              potion_shop="drunk on shrooms",
              zora="wobble beam for sale",
              flute_spot="strange boy wobbles again")
    ),
    (
        ["Post-It Mine"],
        TyrianALTTPText(
              pedestal="and the sticky note",
              sick_kid="the sticky note kid",
              potion_shop="shrooms for sticky notes",
              zora="sticky notes for sale",
              flute_spot="post-it boy takes note again")
    ),
    (
        ["Mint-O-Ship"],
        TyrianALTTPText(
              pedestal="and the mint shooter",
              sick_kid="the mint-fresh kid",
              potion_shop="refreshing shrooms",
              zora="minty freshness for sale",
              flute_spot="mint boy is fresh again")
    ),
    (
        ["Satellite Marlo"],
        TyrianALTTPText(
              pedestal="and the satellite gun",
              sick_kid="the orbiting kid",
              potion_shop="shrooms in orbit",
              zora="satellites for sale",
              flute_spot="satellite boy orbits again")
    ),
    (
        ["Flying Punch"],
        TyrianALTTPText(
              pedestal="and the sky punch",
              sick_kid="the martial arts kid",
              potion_shop="throwing fists for shrooms",
              zora="i don't like your attitude",
              flute_spot="fist boy throws punch again")
    ),
    (
        ["Maximum Power Up"],
        TyrianALTTPText(
              pedestal="and the power boost",
              sick_kid="the power-boost kid",
              potion_shop="shrooms make you powerful",
              zora="power-up for sale",
              flute_spot="strong boy powers up again")
    ),
    (
        ["Armor Up"],
        TyrianALTTPText(
              pedestal="and the space hull",
              sick_kid="the well-armored kid",
              potion_shop="shrooms with a shell",
              zora="stronger hull for sale",
              flute_spot="space boy has armor again")
    ),
    (
        ["Shield Up"],
        TyrianALTTPText(
              pedestal="and the space shield",
              sick_kid="the well-shielded kid",
              potion_shop="shielded shrooms",
              zora="space shield for sale",
              flute_spot="space boy has shield again")
    ),
    (
        ["Solar Shields"],
        TyrianALTTPText(
              pedestal="and solar power",
              sick_kid="the solar-powered kid",
              potion_shop="solar-powered shrooms",
              zora="solar energy for sale",
              flute_spot="solar boy makes energy again")
    ),
    (
        ["Data Cube"],
        TyrianALTTPText(
              pedestal="and the infodump",
              sick_kid="the secret-holding kid",
              potion_shop="give shrooms and i'll talk",
              zora="knowledge for sale",
              flute_spot="secret boy tells all again")
    ),
    (
        ["SuperBomb"],
        TyrianALTTPText(
              pedestal="and the super explosive",
              sick_kid="the large-boom kid",
              potion_shop="super explosive shrooms",
              zora="large ordinance for sale",
              flute_spot="boom boy makes big boom again")
    ),
]

# =================================================================================================

try:
    from worlds.alttp import ALTTPWorld

    # -------------------------------------------------------------------------

    pedestal_credit_texts: dict[int, str] = {}
    sickkid_credit_texts: dict[int, str] = {}
    zora_credit_texts: dict[int, str] = {}
    magicshop_credit_texts: dict[int, str] = {}
    fluteboy_credit_texts: dict[int, str] = {}

    # Convert from our format that makes combining them easier, into item_id->string dicts
    for (items, text_strings) in alttp_item_texts:
        item_ids = [TyrianWorld.item_name_to_id[item_name] for item_name in items]
        pedestal_credit_texts.update(zip(item_ids, itertools.repeat(text_strings.pedestal)))
        sickkid_credit_texts.update(zip(item_ids, itertools.repeat(text_strings.sick_kid)))
        magicshop_credit_texts.update(zip(item_ids, itertools.repeat(text_strings.potion_shop)))
        zora_credit_texts.update(zip(item_ids, itertools.repeat(text_strings.zora)))
        fluteboy_credit_texts.update(zip(item_ids, itertools.repeat(text_strings.flute_spot)))

    # -------------------------------------------------------------------------

    def try_update_alttp_texts(attr_name: str, our_texts: dict[int, str]) -> None:
        lttp_attr = getattr(ALTTPWorld, attr_name, None)
        if lttp_attr is None or not isinstance(lttp_attr, dict):
            logging.debug(f"Tyrian crossgame.alttp: 'ALTTPWorld.{attr_name}' not found. "
                          f"Please update the code in the crossgame subpackage accordingly.")
            return

        # Don't trample over others' code; if types aren't what we expect, bail
        test_key, test_value = next(iter(lttp_attr.items()))
        if not isinstance(test_key, int) or not isinstance(test_value, str):
            logging.debug(f"Tyrian crossgame.alttp: 'ALTTPWorld.{attr_name}' has unexpected types. "
                          f"Please update the code in the crossgame subpackage accordingly.")
            return

        lttp_attr.update(our_texts)
        logging.debug(f"Tyrian crossgame.alttp: Updated 'ALTTPWorld.{attr_name}' successfully.")

    try_update_alttp_texts("pedestal_credit_texts", pedestal_credit_texts)
    try_update_alttp_texts("sickkid_credit_texts", sickkid_credit_texts)
    try_update_alttp_texts("zora_credit_texts", zora_credit_texts)
    try_update_alttp_texts("magicshop_credit_texts", magicshop_credit_texts)
    try_update_alttp_texts("fluteboy_credit_texts", fluteboy_credit_texts)

    # -------------------------------------------------------------------------

    # Clean up temp dicts that we made.
    del pedestal_credit_texts
    del sickkid_credit_texts
    del zora_credit_texts
    del magicshop_credit_texts
    del fluteboy_credit_texts

except ImportError:
    logging.debug("Tyrian crossgame.alttp: 'ALTTPWorld' not found (likely not loaded).")

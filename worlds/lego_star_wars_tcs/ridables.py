from .constants import CharacterAbility
from .levels import SHORT_NAME_TO_CHAPTER_AREA, BONUS_NAME_TO_BONUS_AREA


class Ridable:
    user_facing_name: str
    character_id: int
    chapter_shortnames: tuple[str, ...]
    bonus_area_names: tuple[str, ...]
    is_in_cantina: bool

    def __init__(self,
                 _internal_name: str,  # Currently unused, but useful for reference.
                 user_facing_name: str,
                 character_id: int,
                 *area_names: str
                 ):
        self.user_facing_name = user_facing_name
        self.character_id = character_id
        chapter_names = []
        bonus_names = []
        unknown_names = []
        for name in area_names:
            if name in SHORT_NAME_TO_CHAPTER_AREA:
                chapter_names.append(name)
            elif name in BONUS_NAME_TO_BONUS_AREA:
                bonus_names.append(name)
            elif name == "cantina":
                self.is_in_cantina = True
            else:
                unknown_names.append(name)
        if unknown_names:
            raise ValueError(f"Unknown area names for ridable {user_facing_name}: {unknown_names}")
        self.chapter_shortnames = tuple(chapter_names)
        self.bonus_area_names = tuple(bonus_names)

    @property
    def location_name(self):
        return f"Ride {self.user_facing_name}"


# There is apparently a resident ATAT in HOTHESCAPE/5-2?
_RIDABLES: tuple[Ridable, ...] = (
    Ridable("STAP2", "STAP", 302, "1-1"),
    Ridable("speeder_land", "Landspeeder", 15, "4-2", "4-3", "New Town", "LEGO City"),
    # This is in the files for New Town, but does not appear to be present.
    Ridable("WookieFlyer", "Wookie Flyer", 222, "LEGO City"),
    # There is also a Dewback out-of-bounds/unloaded in 4-3 MOSEISLEY_B.
    Ridable("Dewback", "Dewback", 137, "4-2", "4-3", "New Town", "LEGO City"),
    # Orange Car.
    # In 4-1, requires destroying Silver Bricks + (Imperial Panel or Bounty Hunter Panel)
    Ridable("MoonCar", "Moon Car", 187, "4-1", "New Town", "LEGO City"),
    Ridable("lifeBoat", "Lifeboat", 310, "New Town"),
    Ridable("fireTruck", "Firetruck", 309, "New Town"),
    Ridable("BasketCannon", "Basketball Cannon", 245, "New Town"),
    Ridable("CloneWalker", "Clone Walker", 18, "3-4", "New Town"),
    # Red Car from Cloud City.
    Ridable("CloudCar", "Cloud Car", 191, "5-6", "New Town", "LEGO City"),
    Ridable("TaunTaun", "Tauntaun", 108, "5-2", "New Town", "LEGO City"),
    # 'Milk Van'.
    # In New Town, requires destroying a house (melee OK)
    # In 4-1, requires protocol droid + jedi + (Bounty Hunter panel or Imperial Panel) (basically the same as the Power
    #   Brick)
    Ridable("TownCar", "Town Car", 189, "4-1", "New Town", "LEGO City"),
    # In 5-4 there is one Tractor used to get the Power Brick, requiring SITH, but there is a later Tractor that only
    # requires JEDI
    Ridable("Tractor", "Tractor", 188, "5-4", "6-4", "New Town", "LEGO City"),
    Ridable("bantha", "Bantha", 106, "4-2", "New Town", "LEGO City"),
    Ridable("ATST", "AT-ST", 164, "4-3", "6-3", "6-4", "LEGO City"),
    Ridable("service_car", "Service Car", 160, "1-5", "1-6", "4-5"),
    Ridable("FlashSpeeder", "Flash Speeder", 271, "1-5"),
    Ridable("GrabberControl", "Crane Control", 135, "4-1", "4-4", "4-5", "5-5", "5-6"),
    Ridable("MosCannon", "Mos Eisley Cannon", 180, "4-3"),
    # Note: Also in the HOTH NEWBONUS, which is not part of the randomizer currently.
    # This is in the files for 6-3, but if it exists, I don't know where it is.
    Ridable("TrooperCannon", "Stormtrooper Cannon", 200, "5-2", "5-5"),
    # This is in the files, but I'm not sure this exists?
    # _Ridable("HeavyRepeatingCannon", "Hoth Heavy Repeating Cannon", 0, "5-2"),
    # The one that is used to launch C-3PO.
    Ridable("SnowMob", "Snowmobile", 203, "5-2"),
    Ridable("Catapult", "Ewok Catapult", 159, "6-4"),
    Ridable("Cannon", "Skiff Cannon", 134, "6-2"),
    Ridable("BigGun", "Big Skiff Cannon", 210, "6-2"),
    # Requires pulling a lever OR destroying barrels and building bricks.
    Ridable("mapcar", "Cantina Car", 303, "cantina"),
    Ridable("speederbike", "Speeder Bike", 30, "6-3"),
    # Apparently there is also one in HOTHESCAPE/5-2?
    Ridable("ATAT", "AT-AT", 47, "6-3"),
    Ridable("bomarmonk", "B'omarr Monk", 184, "6-1"),
)

RIDABLES_BY_NAME = {ridable.user_facing_name: ridable for ridable in _RIDABLES}
del _RIDABLES

# Most ridables can be reached with only the characters that are needed to complete the chapter in Story.
RIDABLES_REQUIREMENTS: dict[str, dict[str, tuple[CharacterAbility, ...]]] = {
    "4-1": {
        # The car is hidden within Silver Bricks.
        "Moon Car": (CharacterAbility.BOUNTY_HUNTER,),
        # The car is at the end of a hallway that needs a Bounty Hunter or Imperial to access.
        # A Protocol Droid Panel must be used to remove a force field, and a Jedi must be used to spawn the plants that
        # spawn the Town Car bricks when destroyed.
        "Town Car": (
            CharacterAbility.JEDI | CharacterAbility.BOUNTY_HUNTER,
            CharacterAbility.JEDI | CharacterAbility.IMPERIAL,
        ),
    },
    "LEGO City": {
        # The car is hidden within Silver Bricks, and then needs to be built.
        "Moon Car": (CharacterAbility.BOUNTY_HUNTER | CharacterAbility.CAN_BUILD_BRICKS,),
        # To access the first part, levers need to be pulled, then force is needed to move a part into place, and build
        # bricks is needed to build the final part.
        "Wookie Flyer": (CharacterAbility.JEDI | CharacterAbility.CAN_BUILD_BRICKS | CharacterAbility.CAN_PULL_LEVERS,),
        # A house needs to be destroyed to reveal the parts and then a Jedi is needed to assemble the AT-ST.
        "AT-ST": (CharacterAbility.JEDI | CharacterAbility.CAN_ATTACK_UP_CLOSE,),
        # A house needs to be destroyed to reveal the parts and then the Tractor needs to be built.
        "Tractor": (CharacterAbility.CAN_ATTACK_UP_CLOSE, CharacterAbility.CAN_BUILD_BRICKS,),
        # Either The AT-ST or a Bounty Hunter can destroy the obstacles in the way of getting to the Landspeeder.
        "Landspeeder": (
            CharacterAbility.JEDI | CharacterAbility.CAN_ATTACK_UP_CLOSE,
            CharacterAbility.BOUNTY_HUNTER,
        ),
        # There are Dewbacks and Banthas close enough to the fences that there is no requirement to destroy or jump over
        # the fences. The CharacterAbility.CAN_RIDE_VEHICLES that is added to every Ridable location is enough to
        # guarantee that the player has at least one character that can enter LEGO City.
    },
    "New Town": {
        # The car is hidden within Silver Bricks and then must be built.
        "Moon Car": (CharacterAbility.BOUNTY_HUNTER | CharacterAbility.CAN_BUILD_BRICKS,),
        # The boat needs fixing.
        "Lifeboat": (CharacterAbility.CAN_BUILD_BRICKS,),
        # The house and bins need destroying, and then the car needs to be built.
        "Town Car": (CharacterAbility.CAN_ATTACK_UP_CLOSE | CharacterAbility.CAN_BUILD_BRICKS,),
        # A small building needs to be destroyed, and then the tractor needs to be built.
        "Tractor": (CharacterAbility.CAN_ATTACK_UP_CLOSE | CharacterAbility.CAN_BUILD_BRICKS,),
        # There is a Tauntaun just barely close enough to the fence that there is no need for a character that can jump
        # or destroy the fences, though all characters that can ride vehicles can also jump.
    },
    "cantina": {
        # There are two cars, one is accessed by destroying garbage cans and then building it, and the other is accessed
        # by pulling a lever.
        "Cantina Car": (
            CharacterAbility.CAN_ATTACK_UP_CLOSE | CharacterAbility.CAN_BUILD_BRICKS,
            CharacterAbility.CAN_PULL_LEVERS,
        )
    }
}
assert all(ridable in RIDABLES_BY_NAME
           for chapter_ridables in RIDABLES_REQUIREMENTS.values()
           for ridable in chapter_ridables)


def get_ridable_requirements(chapter_short_name_or_bonus: str, ridable_name: str) -> tuple[CharacterAbility, ...]:
    # todo: Requiring CAN_RIDE_VEHICLES is not strictly necessary currently because the player is always forced to start
    #  with a Jedi.
    requirements = RIDABLES_REQUIREMENTS.get(chapter_short_name_or_bonus, {}).get(ridable_name, ())
    if not requirements:
        return (CharacterAbility.CAN_RIDE_VEHICLES,)
    else:
        return tuple(CharacterAbility.CAN_RIDE_VEHICLES | ability for ability in requirements)


def _make_lookups() -> tuple[dict[str, list[Ridable]], dict[str, list[Ridable]]]:
    from collections import defaultdict
    chapter_to_ridable = defaultdict(list)
    bonus_to_ridable = defaultdict(list)
    for ridable in RIDABLES_BY_NAME.values():
        for chapter in ridable.chapter_shortnames:
            chapter_to_ridable[chapter].append(ridable)
        for bonus in ridable.bonus_area_names:
            bonus_to_ridable[bonus].append(ridable)
    return dict(chapter_to_ridable), dict(bonus_to_ridable)


CHAPTER_TO_RIDABLES: dict[str, list[Ridable]]
BONUS_TO_RIDABLES: dict[str, list[Ridable]]
CHAPTER_TO_RIDABLES, BONUS_TO_RIDABLES = _make_lookups()
del _make_lookups

from collections import defaultdict

from .areas import PURCHASABLE_NON_POWER_BRICK_EXTRAS, BONUS_ROOM_BONUSES
from .characters import UnlockMethod, Character, AREA_TO_PURCHASE_CHARACTERS, AREA_TO_STORY_CHARACTERS
from .logic import EPISODES
from .logic.gold_brick_bonuses import AREA_TO_GOLD_BRICK_BONUS
from .shop import CHARACTER_SHOP_SLOTS

AREA_ID_OFFSET_MULTIPLIER: int = 10_000_000
# ID 0 is skipped because all IDs must be greater than zero, and this just keeps things simpler.
MINIKITS_OFFSET = 1
COMPLETION_OFFSET = 11
TRUE_JEDI_OFFSET = 12
# CHALLENGE_KITS_OFFSET = 20
# TRUE_JEDI_PERCENT_OFFSET = 100

CHARACTERS_OFFSET = 0
"""Character unlock (story/purchase) and ridesanity use this offset, additionally offset by the Character's ID."""

EXTRAS_OFFSET = 400
"""Extra purchases use this offset, additionally offset by the Extra's ID."""
# BLUE_AND_PURPLE_STUDS_OFFSET = 20_000
# GOLD_STUDS_OFFSET = 30_000
# SILVER_STUDS_OFFSET = 40_000
# BLOWUPS_OFFSET = 50_000
# PANELS_OFFSET = 60_000
# ZIP_UPS_OFFSET = 70_000
# GIZ_FORCE_OFFSET = 80_000
# STATIC_POWER_UPS_OFFSET = 90_000
# MAP_SANITY = 100_000

# ENEMY_SANITY_PSUDO_AREA_ID = 100  # BOSS_SANITY would be a subset of these locations


LOCATION_GROUPS = defaultdict(set)


def _make_location_name_to_id() -> dict[str, int]:
    location_name_to_id: dict[str, int] = {}

    def register(name: str, location_id: int, *location_groups: str):
        if name in location_name_to_id:
            raise Exception(f"{name} is already registered")
        location_name_to_id[name] = location_id
        for location_group in location_groups:
            LOCATION_GROUPS[location_group].add(name)

    all_ridables: set[Character] = set()
    all_level_completion_character_unlocks: set[Character] = set()

    for episode in EPISODES:
        for chapter in episode:
            area = chapter.area
            area_id_offset = (area + 1) * AREA_ID_OFFSET_MULTIPLIER

            # Minikits.
            area_minikits_location_group = f"{area.readable_name} Minikits"
            for i, minikit_name in enumerate(chapter.minikits.keys()):
                location_name = area.prefix_name(minikit_name)
                register(location_name, area_id_offset + MINIKITS_OFFSET + i,
                         area.readable_name, "Minikits", area_minikits_location_group)

            # Purchase Characters.
            area_purchases_location_group = f"{area.readable_name} Character Purchases"
            for character in area.get_purchase_characters():
                location_name = character.get_purchase_location_name()
                register(location_name, CHARACTERS_OFFSET + character,
                         area.readable_name, "Character Purchases", area_purchases_location_group)

            # Power Brick.
            extra = area.extra
            assert extra is not None
            extra_purchase_location_name = extra.get_purchase_location_name()
            register(extra_purchase_location_name, EXTRAS_OFFSET + extra,
                     area.readable_name, "Power Brick Extra Purchases")

            # True Jedi.
            true_jedi_name = area.get_true_jedi_name()
            register(true_jedi_name, area_id_offset + TRUE_JEDI_OFFSET,
                     area.readable_name, "True Jedi")

            # Completion.
            completion_name = area.get_completion_name()
            register(completion_name, area_id_offset + COMPLETION_OFFSET,
                     area.readable_name, "Chapter Completions")

            # Update ridables.
            all_ridables.update(chapter.ridables.keys())

            # Update story characters.
            story_characters = area.get_story_characters()
            all_level_completion_character_unlocks.update(story_characters)
            area_level_completion_character_unlock_group = f"Level Completion Character Unlocks - {area.readable_name}"
            for character in story_characters:
                location_name = character.get_level_completion_unlock_location_name()
                LOCATION_GROUPS[area_level_completion_character_unlock_group].add(location_name)

    for bonus_area in BONUS_ROOM_BONUSES:
        area_id_offset = (bonus_area + 1) * AREA_ID_OFFSET_MULTIPLIER

        # Completion
        completion_name = bonus_area.get_completion_name()
        register(completion_name, area_id_offset + COMPLETION_OFFSET,
                 bonus_area.readable_name, "Bonus Completions")

        # Update ridables.
        all_ridables.update(AREA_TO_GOLD_BRICK_BONUS[bonus_area].ridables.keys())

        # Update story characters.
        all_level_completion_character_unlocks.update(AREA_TO_STORY_CHARACTERS.get(bonus_area, ()))
        
        # Purchase characters.
        for character in AREA_TO_PURCHASE_CHARACTERS.get(bonus_area, ()):
            location_name = character.get_purchase_location_name()
            register(location_name, CHARACTERS_OFFSET + character, "Character Purchases")

    # Cantina

    # Cantina purchase characters.
    cantina_purchase_characters = []
    for character in CHARACTER_SHOP_SLOTS:
        unlock_method = character.unlock_method
        if unlock_method is UnlockMethod.START or unlock_method is UnlockMethod.ALL_EPISODES_COMPLETE:
            cantina_purchase_characters.append(character)
    for character in cantina_purchase_characters:
        location_name = character.get_purchase_location_name()
        register(location_name, CHARACTERS_OFFSET + character, "Character Purchases")

    # Cantina ridesanity.
    all_ridables.add(Character.MAPCAR)

    # Cantina Extras.
    for extra in PURCHASABLE_NON_POWER_BRICK_EXTRAS:
        location_name = extra.get_purchase_location_name()
        register(location_name, EXTRAS_OFFSET + extra)

    # Ridesanity locations.
    for ridesanity_character in all_ridables:
        location_name = ridesanity_character.get_ridesanity_location_name()
        register(location_name, CHARACTERS_OFFSET + ridesanity_character, "Ridesanity")

    # Level completion unlock locations.
    for character in all_level_completion_character_unlocks:
        location_name = character.get_level_completion_unlock_location_name()
        register(location_name, CHARACTERS_OFFSET + character, "Level Completion Character Unlocks")

    return location_name_to_id


LOCATION_NAME_TO_ID = _make_location_name_to_id()
del _make_location_name_to_id

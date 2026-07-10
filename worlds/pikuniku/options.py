import re
from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionError,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    TextChoice,
    Toggle,
    Visibility,
    ExcludeLocations,
)


class Coinsanity(Toggle):
    """
    Adds every freestanding coin in the world as a location check.
    When enabled, Coins are added to the item pool as progression items,
    and shop purchases logically require receiving Coins.
    """

    display_name = "Coinsanity"


class EarlyPencilHat(Choice):
    """
    Determines how the Pencil Hat is placed.

    - Early Local: Placed in an early sphere in your own world.
    - Early Global: Placed in an early sphere any world in the multiworld. (Default)
    - Shuffled: Placed anywhere in the multiworld. This will make you get stuck quickly.
    """

    display_name = "Early Pencil Hat"

    option_early_local = 0
    option_early_global = 1
    option_shuffled = 2

    default = option_early_global


class PikuColor(TextChoice):
    """
    Randomizes Piku's color scheme.

    Accepts one of the named modes below, or a 6-digit hex color code
    (e.g. "#FF0000" or "FF0000") to force Piku to always use that exact color.

    - Off: Piku keeps its normal color. (Default)
    - Random Per Screen: Piku is given a new random color every time you enter a screen.
    - Random Per Seed: Piku is given a single random color for the entire seed.
    """

    display_name = "Piku Color"

    option_off = 0
    option_random_per_screen = 1
    option_random_per_seed = 2

    default = option_off

    def verify(self, world, player_name, plando_options) -> None:
        super().verify(world, player_name, plando_options)
        # Named modes resolve to int; any free-text value must be a valid hex color code.
        if isinstance(self.value, str):
            match = re.fullmatch(r"#?([0-9A-Fa-f]{6})", self.value.strip())
            if not match:
                raise OptionError(
                    f"'{self.value}' is not a valid Piku Color for player {player_name}. "
                    f"Use one of {', '.join(self.options)} or a 6-digit hex color code like '#FF0000'."
                )
            # Normalize to a canonical "#RRGGBB" so the client receives a consistent value.
            self.value = f"#{match.group(1).upper()}"


class CoopLevels(Toggle):
    """
    Adds the Piku & Niku co-op levels to the randomizer.
    A "Co-op Level Access" item is added to the item pool, which is required
    to access the co-op level completion checks and the Piku & Niku trophies.
    
    CURRENTLY UNIMPLEMENTED, DO NOT SELECT
    """

    display_name = "Co-op Levels"

    # Currently unimplemented, so hide it from option templates, the player/weighted UIs, and spoilers.
    visibility = Visibility.none


class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink. DeathLinks only apply during the
    platforming challenges or bossfights.
    """

    display_name = "Death Link Amnesty"

    range_start = 1
    range_end = 30

    default = 10

class PikuExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({"Sunshine Inc. Robot Trophy", "Mr. Sunshine Trophy", "Sunshine HQ Dancing Bug"})

@dataclass
class PikunikuOptions(PerGameCommonOptions):
    coinsanity: Coinsanity
    coop_levels: CoopLevels
    early_pencil_hat: EarlyPencilHat
    piku_color: PikuColor
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    exclude_locations: PikuExcludeLocations


option_groups = [
    OptionGroup(
        "Sanity Options",
        [Coinsanity, CoopLevels],
    ),
    OptionGroup(
        "Item Options",
        [EarlyPencilHat],
    ),
    OptionGroup(
        "Cosmetic Options",
        [PikuColor],
    ),
    OptionGroup(
        "Death Link Options",
        [DeathLink, DeathLinkAmnesty],
    ),
    OptionGroup(
        "Excluded Locations",
        [PikuExcludeLocations],
    )
]

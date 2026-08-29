import settings
from typing import Union

class YellowTaxiSettings(settings.Group):
    class MultiworldCoinsanityPercentageCap(int):
        """
        Caps the percentage of Coinsanity coins that can be checks.

        Any players that set a Coinsanity percentage above this will have it lowered to this value.
        """

    multiworld_coinsanity_percentage_cap: Union[MultiworldCoinsanityPercentageCap, int] = 100

    class MultiworldCoinsanityPercentageNonFillerCap(int):
        """
        Caps the percentage of individual coins that can be anything other than filler in Multiworld games.

        100% is thousands of coins even in the smallest game, so it's recommended to keep this low for most cases.
        """

    multiworld_coinsanity_percentage_non_filler_cap: Union[MultiworldCoinsanityPercentageNonFillerCap, int] = 5
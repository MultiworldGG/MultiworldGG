from rule_builder.options import OptionFilter
from rule_builder.rules import Has, Rule

from ..constants import Rac5CutsceneLocations, Rac5EventInfobots, Rac5Infobots, Rac5Planets
from ..locations import ALL_LOCATIONS, MENU_REGION
from ..options import EnableHIGTreehouse

# (region, rule) of the event location granting each event-only infobot. Each region must only be
# entered from Menu, so vendor_rules.py can inline the region's entrance rule plus this rule wherever
# the event item is required.
EVENT_INFOBOT_RULES: dict[str, tuple[str, Rule]] = {
    Rac5EventInfobots.DREAMTIME: (MENU_REGION, Has(Rac5Infobots.OUTPOST_OMEGA)),
    Rac5EventInfobots.OUTPOST_OMEGA_1: (MENU_REGION, Has(Rac5Infobots.OUTPOST_OMEGA)),
    # Beating Luna on Dayni Moon is what opens Inside Clank.
    Rac5EventInfobots.INSIDE_CLANK: (Rac5Planets.DAYNI_MOON, ALL_LOCATIONS[Rac5CutsceneLocations.DAYNI_MOON_LUNA].rule),
}

# Access rule for each Menu -> planet entrance, keyed by planet region name.
ENTRANCE_RULES: dict[str, Rule] = {
    Rac5Planets.POKITARU: Has(Rac5Infobots.POKITARU),
    Rac5Planets.RYLLUS: Has(Rac5Infobots.RYLLUS),
    Rac5Planets.KALIDON: Has(Rac5Infobots.KALIDON),
    Rac5Planets.METALIS: Has(Rac5Infobots.METALIS),
    Rac5Planets.DREAMTIME: Has(Rac5EventInfobots.DREAMTIME),
    Rac5Planets.OUTPOST_OMEGA: Has(Rac5EventInfobots.OUTPOST_OMEGA_1),
    Rac5Planets.CHALLAX: Has(Rac5Infobots.CHALLAX),
    Rac5Planets.DAYNI_MOON: Has(Rac5Infobots.DAYNI_MOON),
    Rac5Planets.INSIDE_CLANK: Has(Rac5EventInfobots.INSIDE_CLANK),
    Rac5Planets.QUODRONA: Has(Rac5Infobots.QUODRONA),
    # Without its checks the Treehouse stays open, as the ship menu shows it unconditionally then.
    Rac5Planets.HIG_TREEHOUSE: Has(
        Rac5Infobots.HIG_TREEHOUSE, options=[OptionFilter(EnableHIGTreehouse, 1)], filtered_resolution=True
    ),
}

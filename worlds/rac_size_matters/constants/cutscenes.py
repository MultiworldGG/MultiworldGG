"""String constants for every in-game cutscene and mission event, grouped by planet."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5CutsceneLocations:
    """String constants for cutscene and mission location names.

    Each planet section begins with an Enter Planet entry (mask 0x01 on the
    mission address for that planet) followed by flag-based cutscenes and
    mission completions in narrative order.
    """

    POKITARU_ENTER = "Pokitaru: Enter Planet"
    POKITARU_RESCUE = "Pokitaru: Rescue the girl"
    POKITARU_FIGHT = "Pokitaru: Fight some robots (Complete Luna's photoshoot)"

    RYLLUS_ENTER = "Ryllus: Enter Planet"
    RYLLUS_BUZZING = "Ryllus: Buzzing Cameras"
    RYLLUS_ARTIFACT = "Ryllus: Investigate the artifact (Reach the temple)"
    RYLLUS_TEMPLE = "Ryllus: Unlock the temple"

    KALIDON_ENTER = "Kalidon: Enter Planet"
    KALIDON_SEARCH = "Kalidon: Search the factory"
    KALIDON_EXPLORE = "Kalidon: Explore the planet"
    KALIDON_WIN = "Kalidon: Win the skyboard race (Complete Learner's Permit)"

    METALIS_ENTER = "Metalis: Enter Planet"
    METALIS_WAR = "Metalis: Survive Robot War III (Complete Buzzsaw Blitz)"
    METALIS_ESCAPE = "Metalis: Escape the planet (Giant Clank)"

    # TODO: add in missing cutscenes
    DREAMTIME_ENTER = "Dreamtime: Enter Planet"
    DREAMTIME_SLEEPING_RATCHET = "Dreamtime: Clank finds sleeping Ratchet"
    DREAMTIME_COMPLETE = "Dreamtime: Complete Dreamtime"

    # TODO: One Cutscene is missing from this list
    OUTPOST_OMEGA_ENTER = "Outpost Omega: Enter Planet"
    OUTPOST_OMEGA = "Outpost Omega: Escape from facility pt 1"
    OUTPOST_OMEGA_ESCAPE = "Outpost Omega: Escape the medical facility"
    OUTPOST_OMEGA_REMATCH = "Outpost Omega: Rematch - Skyboard racers (Complete Interior Decorating)"

    CHALLAX_ENTER = "Challax: Enter Planet"
    CHALLAX_EXPLORE = "Challax: Explore the miniature city"
    METALIS_CLANK = "Metalis: Start Giant Clank"
    CHALLAX_CLANK = "Challax: Destroy the space fortress (Giant Clank)"

    DAYNI_MOON_FIGHT1 = "Dayni Moon: Luna fight pt 1"
    DAYNI_MOON_FIGHT2 = "Dayni Moon: Luna fight pt 2"
    DAYNI_MOON = "Dayni Moon: Catch Luna"
    DAYNI_MOON_LUNA = "Dayni Moon: Defeat Luna"

    # TODO: One Cutscene is missing from this list
    INSIDE_CLANK_ENTER = "Inside Clank: Enter Planet"
    INSIDE_CLANK_ESCAPE = "Inside Clank: Escape from Clank"
    INSIDE_CLANK_TECHNOMITES = "Inside Clank: Defeat all Technomites"

    QUODRONA_ENTER = "Quodrona: Enter Planet"
    QUODRONA_CLONE = "Quodrona: Clone Wars (Fight the Ratchet Clones)"
    QUODRONA_CHASE = "Quodrona: Runnnn from Otto"
    QUODRONA_MECHA = "Quodrona: Defeat Mecha Otto"
    QUODRONA_FIND = "Quodrona: Find Otto Destruct"
    QUODRONA_GOAL = "Quodrona: Defeat Otto Destruct"

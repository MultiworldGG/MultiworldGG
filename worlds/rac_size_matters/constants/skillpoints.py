"""This module contains string constants for skillpoint locations"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5SkillPoints:
    """String constants for skillpoint locations"""

    POKITARU_TRAIN = "Pokitaru: Skill Point: Train Faster"
    POKITARU_BOAT = "Pokitaru: Skill Point: Don't Rock the Boat"
    POKITARU_COWS = "Pokitaru: Skill Point: Do Cows Get Crabby?"

    RYLLUS_BURY = "Ryllus: Skill Point: Bury the Pygmies"
    RYLLUS_CAMERA = "Ryllus: Skill Point: Lights, Camera, Action!"
    RYLLUS_SHIP_IT = "Ryllus: Skill Point: Ship It"

    KALIDON_EXPLOSIVE = "Kalidon: Skill Point: Explosive Ordnance Disposal"
    KALIDON_SUPER_LOMBAX = "Kalidon: Skill Point: Super Lombax"
    KALIDON_SKYBOARDER = "Kalidon: Skill Point: Be A Cool Skyboarder"

    METALIS_SHUTOUT = "Metalis: Skill Point: Shutout"
    METALIS_TERROR = "Metalis: Skill Point: Terror of the Skies"
    METALIS_GLADIATOR = "Metalis: Skill Point: Ultimate Gladiator"

    DREAMTIME_FRIENDS = "Dreamtime: Skill Point: Friends Don't Hurt Friends"
    DREAMTIME_NIGHT_TERRORS = "Dreamtime: Skill Point: Night Terrors"

    OUTPOST_OMEGA_AWESOME = "Outpost Omega: Skill Point: Be An Awesome Skyboarder"

    CHALLAX_SHOCK = "Challax: Skill Point: Take Them Down A Shock"
    CHALLAX_MASTER = "Challax: Skill Point: High Tech Weapons Master"
    CHALLAX_VARMINTS = "Challax: Skill Point: No More Varmints!"

    DAYNI_MOON_GLADIATOR = "Dayni Moon: Skill Point: Ultimate Gladiator"
    DAYNI_MOON_WOOL_PROTEST = "Dayni Moon: Skill Point: Wool Protest"
    DAYNI_MOON_BOUNCY = "Dayni Moon: Skill Point: Bouncy, Bouncy, Bouncy"

    INSIDE_CLANK_SHOCK = "Inside Clank: Skill Point: Not the Shock of Me Now"
    INSIDE_CLANK_RATCHET = "Inside Clank: Skill Point: Ratchet... Just Ratchet"

    QUODRONA_ELITE = "Quodrona: Skill Point: Elite Annihilation"
    QUODRONA_STORM = "Quodrona: Skill Point: Storm the Front"

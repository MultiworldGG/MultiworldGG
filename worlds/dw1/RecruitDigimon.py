from typing import NamedTuple, List

class RecruitDigimon(NamedTuple):
    name: str
    prosperity_value: int
    digimon_requirements: List[str]
    prosperity_requirement: int
    requires_recruit: bool
    min_statcap: int = 0
    or_digimon_requirements: tuple = ()

recruit_digimon_list = [
    RecruitDigimon("Betamon",       1, [],                                      1,  True),
    RecruitDigimon("Kunemon",       1, [],                                      1,  True),
    RecruitDigimon("Palmon",        1, [],                                      1,  True),
    RecruitDigimon("Bakemon",       2, [],                                      1,  True),
    RecruitDigimon("Centarumon",    2, [],                                      1,  True),
    RecruitDigimon("Coelamon",      2, [],                                      1,  True),
    RecruitDigimon("Gabumon",       1, [],                                      1,  True),
    RecruitDigimon("Greymon",       2, [],                                     15,  False),
    RecruitDigimon("Monochromon",   2, [],                                      6,  True),
    RecruitDigimon("Meramon",       2, [],                                      1,  True, min_statcap=1, or_digimon_requirements=("Coelamon", "Betamon")),
    RecruitDigimon("Elecmon",       1, [],                                      1,  True),
    RecruitDigimon("Patamon",       1, [],                                      1,  True),
    RecruitDigimon("Biyomon",       1, [],                                      1,  True),
    RecruitDigimon("Sukamon",       1, [],                                      1,  True),
    RecruitDigimon("Tyrannomon",    2, [],                         1,  True),
    RecruitDigimon("Birdramon",     2, [],                                      6,  True),
    RecruitDigimon("Unimon",        2, ["Centarumon"],              1,  True),
    RecruitDigimon("Penguinmon",    1, [],                                      6,  True),
    RecruitDigimon("Mojyamon",      2, [],                                      6,  True),
    RecruitDigimon("Angemon",       2, [],                                      6,  True),
    RecruitDigimon("Vegiemon",      2, ["Palmon"],                           10,  True),
    RecruitDigimon("Shellmon",      2, [],                                      6,  True),
    RecruitDigimon("Piximon",       3, [],                                      1,  True, min_statcap=3),
    RecruitDigimon("Whamon",        2, [],                                      6,  True),
    RecruitDigimon("Numemon",       1, [],                            6,  True),
    RecruitDigimon("Giromon",       3, [],                 6,  True),
    RecruitDigimon("Andromon",      3, [],                 6,  True),
    RecruitDigimon("Frigimon",      2, [],                                      6,  True),
    RecruitDigimon("Seadramon",     2, [],                                      1,  True),
    RecruitDigimon("Garurumon",     2, [],                                      6,  True),
    RecruitDigimon("Monzaemon",     3, [],                                      6,  True),
    RecruitDigimon("Kokatorimon",   2, [],                                      6,  True),
    RecruitDigimon("Ogremon",       2, [],                                      6,  True),
    RecruitDigimon("Kuwagamon",     2, [],                         1,  True),
    RecruitDigimon("Kabuterimon",   2, [],                         1,  True),
    RecruitDigimon("Drimogemon",    2, ["Meramon", "Leomon"],                           50,  True),
    RecruitDigimon("Vademon",       3, ["Shellmon"],               45,  True),
    RecruitDigimon("MetalMamemon",  3, ["Whamon"],                            1,  True),
    RecruitDigimon("SkullGreymon",  3, ["Greymon", "Shellmon"],               50,  True),
    RecruitDigimon("Mamemon",       3, [],                           1,  True),
    RecruitDigimon("Ninjamon",      2, [],                                     50,  True),
    RecruitDigimon("Devimon",       2, [],                                     50,  True),
    RecruitDigimon("Leomon",        2, ["Meramon"],                          50,  True),
    RecruitDigimon("Nanimon",       1, ["Leomon", "Tyrannomon", "Numemon"],   1,  True),
    RecruitDigimon("MetalGreymon",  3, [],                          50,  False),
    RecruitDigimon("Etemon",        3, [],                                     50,  True),
    RecruitDigimon("Megadramon",    3, [],                                     50,  True),
    RecruitDigimon("Airdramon",     2, [],                                     50,  True),
    RecruitDigimon("Digitamamon",   3, [],                                     50,  True),
]

from typing import NamedTuple, List

class RecruitDigimon(NamedTuple):
    name: str
    prosperity_value: int
    digimon_requirements: List[str]
    prosperity_requirement: int
    requires_soul: bool
    meramon_gate: bool = False
    min_statcap: int = 0
    or_digimon_requirements: tuple = ()

recruit_digimon_list = [
    RecruitDigimon("Agumon",        1, [],                                              0,  True),
    RecruitDigimon("Betamon",       1, ["Agumon"],                                      1,  True),
    RecruitDigimon("Kunemon",       1, ["Agumon"],                                      1,  True),
    RecruitDigimon("Palmon",        1, ["Agumon"],                                      1,  True),
    RecruitDigimon("Bakemon",       2, ["Agumon"],                                      1,  True, meramon_gate=True),
    RecruitDigimon("Centarumon",    2, ["Agumon"],                                      1,  True),
    RecruitDigimon("Coelamon",      2, ["Agumon"],                                      1,  True),
    RecruitDigimon("Gabumon",       1, ["Agumon"],                                      1,  True, meramon_gate=True),
    RecruitDigimon("Greymon",       2, ["Agumon"],                                     15,  False),
    RecruitDigimon("Monochromon",   2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Meramon",       2, ["Agumon"],                                      1,  True, min_statcap=1, or_digimon_requirements=("Coelamon", "Betamon")),
    RecruitDigimon("Elecmon",       1, ["Agumon"],                                      1,  True, meramon_gate=True),
    RecruitDigimon("Patamon",       1, ["Agumon"],                                      1,  True, meramon_gate=True),
    RecruitDigimon("Biyomon",       1, ["Agumon"],                                      1,  True, meramon_gate=True),
    RecruitDigimon("Sukamon",       1, ["Agumon"],                                      1,  True, meramon_gate=True),
    RecruitDigimon("Tyrannomon",    2, ["Agumon", "Centarumon"],                         1,  True),
    RecruitDigimon("Birdramon",     2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Unimon",        2, ["Agumon", "Centarumon", "Meramon"],              1,  True),
    RecruitDigimon("Penguinmon",    1, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Mojyamon",      2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Angemon",       2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Vegiemon",      2, ["Agumon", "Palmon"],                            1,  True),
    RecruitDigimon("Shellmon",      2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Piximon",       3, ["Agumon"],                                      1,  True, min_statcap=3),
    RecruitDigimon("Whamon",        2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Numemon",       1, ["Agumon", "Whamon"],                            6,  True),
    RecruitDigimon("Giromon",       3, ["Agumon", "Whamon", "Numemon"],                 6,  True),
    RecruitDigimon("Andromon",      3, ["Agumon", "Whamon", "Numemon"],                 6,  True),
    RecruitDigimon("Frigimon",      2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Seadramon",     2, ["Agumon"],                                      1,  True),
    RecruitDigimon("Garurumon",     2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Monzaemon",     3, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Kokatorimon",   2, ["Agumon"],                                      6,  True, meramon_gate=True),
    RecruitDigimon("Ogremon",       2, ["Agumon", "Whamon"],                            6,  True, meramon_gate=True),
    RecruitDigimon("Kuwagamon",     2, ["Agumon", "Seadramon"],                         1,  True),
    RecruitDigimon("Kabuterimon",   2, ["Agumon", "Seadramon"],                         1,  True),
    RecruitDigimon("Drimogemon",    2, ["Agumon", "Meramon"],                           1,  True),
    RecruitDigimon("Vademon",       3, ["Agumon", "Meramon", "Shellmon"],               45,  True),
    RecruitDigimon("MetalMamemon",  3, ["Agumon", "Whamon"],                            1,  True),
    RecruitDigimon("SkullGreymon",  3, ["Agumon", "Greymon", "Shellmon"],               50,  True),
    RecruitDigimon("Mamemon",       3, ["Agumon", "Meramon"],                           1,  True),
    RecruitDigimon("Ninjamon",      2, ["Agumon"],                                     50,  True),
    RecruitDigimon("Devimon",       2, ["Agumon"],                                     50,  True),
    RecruitDigimon("Leomon",        2, ["Agumon", "Meramon"],                          50,  True),
    RecruitDigimon("Nanimon",       1, ["Agumon", "Leomon", "Tyrannomon", "Numemon"],   1,  True),
    RecruitDigimon("MetalGreymon",  3, ["Agumon", "Greymon"],                          50,  False),
    RecruitDigimon("Etemon",        3, ["Agumon"],                                     50,  True),
    RecruitDigimon("Megadramon",    3, ["Agumon"],                                     50,  True),
    RecruitDigimon("Airdramon",     2, ["Agumon"],                                     50,  True),
    RecruitDigimon("Digitamamon",   3, ["Agumon"],                                     50,  True),
]

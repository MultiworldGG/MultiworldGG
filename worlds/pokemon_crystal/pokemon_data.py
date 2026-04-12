from .data import data

ALL_UNOWN = [
    f"UNOWN_{char}" for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
]

LEGENDARY_POKEMON = {"Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew", "Entei", "Raikou", "Suicune", "Celebi",
                     "Lugia", "Ho-Oh"}

NON_LEGENDARY_POKEMON = {pokemon.friendly_name for pokemon in data.pokemon.values() if
                         pokemon.friendly_name not in LEGENDARY_POKEMON}

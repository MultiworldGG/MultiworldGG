from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data
from .options import RandomizeMusic

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

# radio tracks are also compared against wMapMusic (Snorlax wake-up, encounter rate), so they can't play as map music
EXCLUDED_MUSIC = ["MUSIC_NONE", "MUSIC_LAKE_OF_RAGE_ROCKET_RADIO", "MUSIC_PRINTER", "MUSIC_RUINS_OF_ALPH_RADIO",
                  "MUSIC_POKE_FLUTE_CHANNEL", "MUSIC_POKEMON_MARCH", "MUSIC_POKEMON_LULLABY"]

# id $64 == MUSIC_MAHOGANY_MART, which GetMapMusic treats as a sentinel in map headers
MAP_UNSAFE_MUSIC = ["MUSIC_SUICUNE_BATTLE"]

# scripts that restart a track already chosen elsewhere: script -> script it mirrors
LINKED_SCRIPT_MUSIC = {
    "overworld__MUSIC_BICYCLE": "audio__MUSIC_BICYCLE",
    "magnet_train_midpoint__MUSIC_MAGNET_TRAIN": "magnet_train__MUSIC_MAGNET_TRAIN",
}

# scripts that fade back to the current map's music: script -> map
MAP_RETURN_SCRIPT_MUSIC = {
    "PlayersHouse2F__MUSIC_NEW_BARK_TOWN": "MAP_PlayersHouse2F",
    "PlayersNeighborsHouse__MUSIC_NEW_BARK_TOWN": "MAP_PlayersNeighborsHouse",
}


def randomize_music(world: "PokemonCrystalWorld"):
    if not world.options.randomize_music: return

    music_pool_loop = [music_name for music_name, music_data in data.music.consts.items() if
                       music_name not in EXCLUDED_MUSIC and music_data.loop]
    music_pool_no_loop = [music_name for music_name, music_data in data.music.consts.items() if
                          music_name not in EXCLUDED_MUSIC and not music_data.loop]
    music_pool_map = [music_name for music_name in music_pool_loop if music_name not in MAP_UNSAFE_MUSIC]

    if world.options.randomize_music == RandomizeMusic.option_completely_random:
        scripts = {script_name: world.random.choice(
            music_pool_loop if data.music.consts[script_music].loop else music_pool_no_loop) for
            script_name, script_music in world.generated_music.scripts.items()}
        maps = {map_name: world.random.choice(music_pool_map) for map_name in world.generated_music.maps.keys()}
        for script_name, source in LINKED_SCRIPT_MUSIC.items():
            if script_name in scripts and source in scripts:
                scripts[script_name] = scripts[source]
        for script_name, map_name in MAP_RETURN_SCRIPT_MUSIC.items():
            if script_name in scripts and map_name in maps:
                scripts[script_name] = maps[map_name]
        world.generated_music = replace(
            world.generated_music,
            maps=maps,
            encounters=[world.random.choice(music_pool_loop) for _ in world.generated_music.encounters],
            scripts=scripts,
        )
    else:

        all_loop_music = [music_name for music_name, music_data in data.music.consts.items() if music_data.loop] + [
            "MUSIC_NONE"]
        all_no_loop_music = [music_name for music_name, music_data in data.music.consts.items() if not music_data.loop]

        map_music = set(world.generated_music.maps.values())
        loop_mapping = {name: world.random.choice(music_pool_map if name in map_music else music_pool_loop)
                        for name in all_loop_music}
        no_loop_mapping = {name: world.random.choice(music_pool_no_loop) for name in all_no_loop_music}

        world.generated_music = replace(
            world.generated_music,
            maps={map_name: loop_mapping[music] for map_name, music in world.generated_music.maps.items()},
            encounters=[loop_mapping[music] for music in world.generated_music.encounters],
            scripts={script_name: loop_mapping[music] if data.music.consts[music].loop else no_loop_mapping[music] for
                     script_name, music in world.generated_music.scripts.items()}
        )

import json
from pathlib import Path

import Utils
from ..RomData import RomData
from ..text.decoding import parse_text_dict, parse_all_texts


def load_vanilla_dict_data(seasons: bool) -> None | dict[str, str]:
    """
    Gets the vanilla dict, this is always assumed to already exist
    """
    game_name = "seasons" if seasons else "ages"

    text_dir = Path(Utils.cache_path("oos_ooa/text"))
    vanilla_text_file = text_dir.joinpath(f"{game_name}_dict.json")
    return json.load(open(vanilla_text_file, encoding="utf-8"))


def load_vanilla_text_data(seasons: bool) -> None | dict[str, str]:
    game_name = "seasons" if seasons else "ages"

    text_dir = Path(Utils.cache_path("oos_ooa/text"))
    vanilla_text_file = text_dir.joinpath(f"{game_name}_texts_vanilla.json")
    if not vanilla_text_file.is_file():
        return None
    return json.load(open(vanilla_text_file, encoding="utf-8"))


def save_vanilla_text_data(dictionary: dict[str, str],
                           texts: dict[str, str],
                           seasons: bool) -> None:
    text_dir = Path(Utils.cache_path("oos_ooa/text"))
    text_dir.mkdir(parents=True, exist_ok=True)

    game_name = "seasons" if seasons else "ages"
    dict_file = text_dir.joinpath(f"{game_name}_dict.json")
    text_file = text_dir.joinpath(f"{game_name}_texts_vanilla.json")

    with dict_file.open("w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False)

    with text_file.open("w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False)


def get_text_data(rom_data: RomData, get_dictionary: bool, seasons: bool) -> tuple[None | dict[str, str], dict[str, str]]:
    result = load_vanilla_text_data(seasons)
    if result is not None:
        if get_dictionary:
            dictionary = load_vanilla_dict_data(seasons)
        else:
            dictionary = None
        return dictionary, result

    dictionary = parse_text_dict(rom_data, seasons)
    texts = parse_all_texts(rom_data, dictionary, seasons)
    save_vanilla_text_data(dictionary, texts, seasons)
    return dictionary, texts

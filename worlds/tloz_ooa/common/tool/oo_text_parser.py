import json
import os

from settings import get_settings
from ..patching.RomData import RomData
from ..patching.text.decoding import parse_all_texts, decode_text, parse_text_dict
from ..patching.text.encoding import encode_dict, write_text_data

if __name__ == "__main__":
    if not os.path.isdir("output"):
        os.mkdir("output")
    file_name = get_settings()["tloz_oos_options"]["rom_file"]
    rom = RomData(bytes(open(file_name, "rb").read()))
    dict_seasons = parse_text_dict(rom, True)
    text = parse_all_texts(rom, dict_seasons, True)

    with open("output/seasons_text_dict.json", "w+", encoding="utf-8") as f:
        json.dump(dict_seasons, f, ensure_ascii=False, indent=4)

    with open("output/seasons_text.json", "w+", encoding="utf-8") as f:
        json.dump(text, f, ensure_ascii=False, indent=4)

    encoded_dict1 = encode_dict(dict_seasons)
    for key in dict_seasons:
        fake_rom = RomData(encoded_dict1[key])
        assert decode_text(fake_rom, 0) == dict_seasons[key], (decode_text(fake_rom, 0), dict_seasons[0])

    encoded_dict2 = encode_dict(text, dict_seasons)
    for key in text:
        fake_rom = RomData(encoded_dict2[key])
        assert decode_text(fake_rom, 0, dict_seasons) == text[key], (decode_text(fake_rom, 0, dict_seasons), text[key])

    write_text_data(rom, dict_seasons, text, True)

    dict_seasons2 = parse_text_dict(rom, True)

    for key in dict_seasons:
        assert dict_seasons2[key] == dict_seasons[key], (dict_seasons2[key], dict_seasons[key])

    text2 = parse_all_texts(rom, dict_seasons2, True)

    for key in text2:
        assert text2[key] == text[key], (text2[key], text[key])
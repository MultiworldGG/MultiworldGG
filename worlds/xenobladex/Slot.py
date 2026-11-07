from .Options import XenobladeXOptions, generate_cemu_options


def generate_slot_data(options: XenobladeXOptions) -> dict[str, object]:
    slot_data: dict[str, object] = {}
    slot_data["cemu_options"] = generate_cemu_options(options)
    slot_data["options"] = options.as_dict("death_link", "logic_level_steps", "character_level",
                                           "loc", "clp", "ebk", "shpbp", "shpamr", "shpwpn", "shpaug",
                                           "shpskamr", "shpskwpn", "shpskaug", "shpskf", "impit")
    return slot_data

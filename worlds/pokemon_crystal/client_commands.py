"""Client-side /headbutt and /fishing commands listing each encounter group's in-game areas."""

from collections.abc import Callable
from typing import TYPE_CHECKING

from .options import JohtoOnly

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def gen_group_cmd(title: str, data: dict[str, tuple[list[str], list[int]]]) -> Callable[[], None]:
    from CommonClient import logger
    genned_str = f"{title.title()} Groups:\n\n"
    group_strs = []
    for group_name, group_data in data.items():
        locations = group_data[0]
        routes = sorted(group_data[1])
        if len(locations + routes) == 0: continue
        if len(routes) == 1:
            routes[0] = f"Route {routes[0]}"
        elif len(routes) > 1:
            routes[0] = f"Routes {routes[0]}"
        group_strs.append(f"{group_name}: " + ", ".join(locations + [str(r) for r in routes]))

    if len(group_strs) == 0:
        group_strs = ["None?"]
    genned_str += "\n".join(group_strs)

    func = lambda self: logger.info(genned_str)
    func.__doc__ = f"Show the in-game areas corresponding to each {title.title()} group."
    return func


def register_commands(ctx: "BizHawkClientContext") -> None:
    headbutt_data = {
        "Canyon": ([], [44]),
        "Town": (["Azalea Town"], [33, 42]),
        "Route": ([], [29, 30, 31, 34, 35, 36, 37, 38, 39]),
        "Border": ([], [26, 27, 32]),
        "Lake": (["Lake of Rage"], [43]),
        "Forest": (["Ilex Forest"], [])
    }
    fishing_data = {
        "Shore": (["Cherrygrove City", "Olivine City", "Cianwood City", "Union Cave B2F"],
                  [34, 40]),
        "Ocean": (["New Bark Town", "Olivine City Port"],
                  [26, 27, 41]),
        "Lake":  (["Dark Cave", "Union Cave", "Slowpoke Well", "Mount Mortar", "Tohjo Falls"],
                  [42]),
        "Pond":  (["Violet City", "Ruins of Alph", "Ilex Forest", "Ecruteak City", "Blackthorn City"],
                  [30, 31, 35, 43, 44]),
        "Gyarados/Lake of Rage": (["Lake of Rage"], []),
        "Dratini/Dragon's Den":  (["Dragon's Den"], []),
        "Dratini_2/Route 45": ([], [45]),
        "Qwilfish/Routes 12, 13, 32": ([], [32]),
        "Whirl Islands": (["Whirl Islands (inside)"], [])
    }

    if ctx.slot_data["johto_only"] == JohtoOnly.option_off:
        fishing_data["Shore"][1].append(19)
        fishing_data["Ocean"][0].extend(["Vermilion City", "Vermilion City Port", "Pallet Town", "Cinnabar Island"])
        fishing_data["Ocean"][1].extend([20, 21])
        fishing_data["Lake"][1].extend([9, 10, 24, 25])
        fishing_data["Pond"][0].append("Viridian City")
        fishing_data["Pond"][1].extend([6, 22])
        fishing_data["Gyarados/Lake of Rage"][0].append("Fuchsia City")
        fishing_data["Qwilfish/Routes 12, 13, 32"][1].extend([12, 13])
    if ctx.slot_data["johto_only"] != JohtoOnly.option_on:
        fishing_data["Lake"][0].append("Silver Cave")
        fishing_data["Pond"][0].append("Silver Cave Outside")
        fishing_data["Pond"][1].append(28)
    if ctx.slot_data["route_23_restored"]:
        fishing_data["Dratini_2/Route 45"][1].append(23)
    if ctx.slot_data.get("flooded_mine"):
        fishing_data["Ocean"][0].append("Flooded Mine")

    ctx.command_processor.commands["headbutt"] = gen_group_cmd("Headbutt", headbutt_data)
    ctx.command_processor.commands["fishing"] = gen_group_cmd("Fishing", fishing_data)

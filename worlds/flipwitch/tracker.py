from typing import Any, TYPE_CHECKING, List

if TYPE_CHECKING:
    from . import FlipwitchWorld


def setup_options_from_slot_data(world: "FlipwitchWorld"):
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "Flipwitch Forbidden Sex Hex" in world.multiworld.re_gen_passthrough:
            world.passthrough = world.multiworld.re_gen_passthrough["Flipwitch Forbidden Sex Hex"]
            world.options.starting_gender.value = world.passthrough["starting_gender"]
            world.options.starting_area.value = world.passthrough["starting_area"]
            world.options.shuffle_double_jump.value = world.passthrough["shuffle_double_jump"]
            world.options.shuffle_dodge.value = world.passthrough["shuffle_dodge"]
            world.options.shuffle_chaos_pieces.value = world.passthrough["shuffle_chaos_pieces"]
            world.options.pottery_lottery.value = world.passthrough["pottery_lottery"]
            world.options.shopsanity.value = world.passthrough["shopsanity"]
            world.options.stat_shuffle.value = world.passthrough["stat_shuffle"]
            world.options.gachapon_shuffle.value = world.passthrough["gachapon_shuffle"]
            world.options.quest_for_sex.value = world.passthrough["quest_for_sex"]
            world.options.crystal_teleports.value = world.passthrough["crystal_teleports"]
            world.animal_order = world.passthrough["animal_order"]
            world.bunny_order = world.passthrough["bunny_order"]
            world.monster_order = world.passthrough["monster_order"]
            world.angel_order = world.passthrough["angel_order"]
            world.seed = world.passthrough["ut_seed"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False


TRACKER_WORLD = {

}

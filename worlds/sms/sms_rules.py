from typing import TYPE_CHECKING, Callable

from BaseClasses import Entrance, CollectionState, Region
from .sms_regions.sms_region_helper import SmsLocation, Requirements
from ..generic.Rules import set_rule, add_item_rule, add_rule
from .items import TICKET_ITEMS, REGULAR_PROGRESSION_ITEMS

if TYPE_CHECKING:
    from . import SmsWorld


def interpret_requirements(
    spot: Entrance | SmsLocation,
    requirement_set: list[Requirements],
    world: "SmsWorld",
) -> None:
    """Correctly applies and interprets custom requirements namedtuple for a given entrance/location."""
    # If a region/location does not have any items required, make the section(s) return no logic.
    if requirement_set is None or len(requirement_set) < 1:
        return

    # If all shines are selectable, remove all the entrance requirements related to location access.
    # If a location has no reqs after that is removed, then it is considered empty and should be removed from the list.
    if isinstance(spot, Entrance) and world.options.all_shines_selectable.value:
        reqs_copy: list[Requirements] = []
        for copy_req in requirement_set:
            if not copy_req.location:
                reqs_copy.append(copy_req)
                continue

            temp_req = Requirements(copy_req.nozzles, copy_req.shines, copy_req.blue_coins, None,
                copy_req.corona, copy_req.skip_forward, copy_req.manual_none)
            if not temp_req.is_empty():
                reqs_copy.append(copy_req)
        requirement_set = reqs_copy

        # Secondary check after requirements were updated.
        if requirement_set is None or len(requirement_set) < 1:
            return

    # Otherwise, if a region/location DOES have items required, make the section(s) return list of logic.
    skip_forward_locs: bool = (
        world.options.starting_nozzle.value == 2
        or world.options.level_access.value == 1
    )
    any_skip_locs: bool = any([reqs for reqs in requirement_set if reqs.skip_forward])

    for single_req in requirement_set:
        # If entry is set to ticket mode or fluddless and this location is not set to skip forward
        if (skip_forward_locs and any_skip_locs) and not single_req.skip_forward:
            continue

        # Else if entry is NOT set to ticket mode or fluddless and this location is set to skip forward
        elif not (skip_forward_locs and any_skip_locs) and single_req.skip_forward:
            continue

        # Else if the requirement manually set to have none
        elif single_req.manual_none:
            continue

        req_rules: list[Callable[[CollectionState], bool]] = []

        if single_req.nozzles:
            # Requires one or more sets of at least 1 Nozzle to access.
            default_rule: Callable[[CollectionState], bool] = lambda state: True
            nozz_rule: Callable[[CollectionState], bool] = default_rule

            for nozzle_req in single_req.nozzles:
                if nozz_rule is default_rule:
                    nozz_rule = lambda state, item_set=tuple(nozzle_req): state.has_all(
                        item_set, world.player
                    )
                else:
                    nozz_rule = lambda state, item_set=tuple(
                        nozzle_req
                    ), current_rule=nozz_rule: current_rule(state) or state.has_all(
                        item_set, world.player
                    )
            req_rules.append(lambda state, captured_rule=nozz_rule: captured_rule(state))

        if single_req.shines and world.corona_mountain_shines > 0:
            # Requires X amount of shine sprites to access
            required_shines: int = single_req.shines

            # If the required shines is more than the amount required for corona mountain.
            if required_shines > world.corona_mountain_shines:
                required_shines = world.corona_mountain_shines

            # This is an entrance that has shines and level access is tickets, no shine requirements
            if isinstance(spot, Entrance) and world.options.level_access == 1:
                required_shines = 0

            if required_shines > 0:
                req_rules.append(
                    lambda state, shine_req_count=required_shines: state.has(
                        "Shine Sprite", world.player, shine_req_count))

        if single_req.blue_coins:
            # Requires X amount of blue coins (event item or actual)
            req_rules.append(
                lambda state, coin_count=single_req.blue_coins: (
                    state.has("Blue Coin", world.player, coin_count)
                )
            )

        if single_req.location:
            req_rules.append(lambda state, loc_name=single_req.location: state.can_reach_location(
                    loc_name, world.player))
            ref_region: Region = world.get_location(single_req.location).parent_region

            if isinstance(spot, Entrance):
                #  We use this to explicitly tell the generator that, when a given region becomes accessible,
                #   it is necessary to re-check a specific entrance, as we determine if a user has access to a
                #   region if they complete previous stars/regions.
                world.multiworld.register_indirect_condition(ref_region, spot)
            else:
                # For locations, register against every entrance into the location's own parent region so
                #   sweep knows to re-check when the referenced region becomes newly reachable.
                for entrance in spot.parent_region.entrances:
                    world.multiworld.register_indirect_condition(ref_region, entrance)

        if (
            world.corona_mountain_shines > 0 and (
                single_req.corona or
                (hasattr(spot, "corona") and spot.corona)
            )
        ):
            # Player requires all shine sprites that are required to reach corona mountain as well.
            req_rules.append(
                lambda state, shine_count=world.options.corona_mountain_shines.value: state.has(
                    "Shine Sprite", world.player, shine_count
                )
            )

        # If no requirement rules are found, don't set any rules and continue
        if not req_rules:
            continue

        if spot.access_rule is SmsLocation.access_rule or spot.access_rule is Entrance.access_rule:
            set_rule(spot, (lambda state, all_rules=tuple(req_rules): all(req_rule(state) for req_rule in all_rules)))
        else:
            if isinstance(spot, SmsLocation):
                add_rule(spot, (lambda state, all_rules=tuple(req_rules):
                    all(req_rule(state) for req_rule in all_rules)), combine="or")
            else:
                add_rule(spot,
                    (lambda state, all_rules=tuple(req_rules): all(req_rule(state) for req_rule in all_rules)))
    return

def create_sms_region_and_entrance_rules(world: "SmsWorld"):
    for sms_reg in world.get_regions():
        region_ticket: str = ""
        if sms_reg.entrances:
            # Add the entrance rule for all entrances in the region based on the Requirements NamedTuple defined.
            for sms_entrance in sms_reg.entrances:
                if hasattr(sms_entrance, "requirements"):
                    interpret_requirements(
                        sms_entrance, sms_entrance.requirements, world
                    )

                # If a parent region has any ticket str, get that ticket as well
                if (hasattr(sms_entrance.parent_region, "ticket_str")
                    and sms_entrance.parent_region.ticket_str
                    and sms_entrance.parent_region == world.get_region(
                        sms_entrance.parent_region.name
                    )
                ):
                    region_ticket = sms_entrance.parent_region.ticket_str
                    break

            # Add the location rules within this region.
            for sms_loc in sms_reg.locations:
                # Skip any event based locations that do not have this attribute
                if hasattr(sms_loc, "loc_reqs"):
                    interpret_requirements(sms_loc, sms_loc.loc_reqs, world)

                # A Region cannot have its own ticket item in ticket mode, so prevent that.
                if world.options.level_access.value == 1 and hasattr(sms_reg, "ticket_str") or region_ticket:
                    reg_ticket: str = (
                        sms_reg.ticket_str
                        if hasattr(sms_reg, "ticket_str")
                        else region_ticket
                    )
                    add_item_rule(
                        sms_loc,
                        (
                            lambda item, reg_tick=reg_ticket: item.game != world.game
                            or (item.game == world.game and item.name != reg_tick)
                        ),
                    )

                # Corona can never have any tickets at high shine counts, otherwise generation is guaranteed to fail.
                if hasattr(sms_loc, "corona") and sms_loc.corona:
                    # Since Corona requires Spray Nozzle and Hover Nozzle to complete, ensure those items can never
                    # be placed. Additionally, Yoshi is required for basically every late game stage.
                    blocked: set[str] = {"Spray Nozzle", "Hover Nozzle", *TICKET_ITEMS}

                    # If there is a high amount of progression items, the world is too restrictive for non-macguffin
                    # items to be placed in corona, especially with previous levels required to be beaten.
                    if world.large_shine_count:
                        blocked |= set(REGULAR_PROGRESSION_ITEMS.keys())

                    add_item_rule(
                        sms_loc,
                        lambda item, blocked_items=frozenset(sorted(blocked)): (
                                item.game != world.game or item.name not in blocked_items
                        )
                    )

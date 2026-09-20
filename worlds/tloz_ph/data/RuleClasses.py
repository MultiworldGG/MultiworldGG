from BaseClasses import LocationProgressType, Location
from rule_builder.rules import *
from .. import PhantomHourglassWorld, PhantomHourglassOptions
from .Items import ITEM_GROUPS
from math import ceil

cost_multiplier = 0.7

def beedle_discount(state: CollectionState, player) -> float:
    """
    Calculate current beedle discount from beedle points
    """
    thresholds = {100: 0.7, 50: 0.8, 20: 0.9}
    points = state.count("Beedle Points", player)
    for threshold, discount in thresholds.items():
        if points >= threshold:
            return discount
    return 1


def beedle_eval(state: CollectionState, player, options: PhantomHourglassOptions, price) -> bool:
    """
    Evaluate if you have enough rupees for beedle
    """
    if state.has("_UT_Glitched_Logic", player) or _can_farm_rupees(state, player):
        return True
    discount = beedle_discount(state, player)  # Discount from points
    return count_rupees(state, player) >= price - 1500*(1-discount)

def _can_farm_rupees(state, player):
    return any([
        all([
            state.has("_has_treasure_teller", player),  # Can Sell Treasure
            any([
                all([
                    state.has("_can_farm_totok", player),
                    state.has("Sword (Progressive)", player, 2),
                ]),
                all([  # Can Farm Minigames
                    state.multiworld.worlds[player].options.randomize_minigames,
                    any([
                        state.has("_can_play_archery", player),
                        state.has("_can_play_cannon_game", player),
                        state.has("_can_play_goron_race", player),
                    ])
                ])
            ]),
        ]),
        all([  # Can farm harrow (and chooses to play with harrow)
            state.has("_can_play_harrow", player),
            state.multiworld.worlds[player].options.randomize_harrow
        ]),
    ])

def count_rupees(state, player):
    rupees = state.count("Rupees", player)
    if state.has("_has_treasure_teller", player):
        rupees += state.count("Treasure", player)
    return rupees

def buy_beedle_points_eval(state, player, options: PhantomHourglassOptions, points) -> bool:
    """
    Evaluate if you have enough rupees to buy beedle points
    """
    points_res = points - state.count("Beedle Points", player)

    if points_res <= 0:
        return True
    cost = points_res * 100
    rupees = state.multiworld.worlds[player].required_rupees
    return beedle_eval(state, player, options, rupees)

tloz_ph = PhantomHourglassWorld.game

class PHShop(Rule[PhantomHourglassWorld], game=tloz_ph):
    """
    Base class for shared code in shops
    """
    price: int

    def __init__(self, price: int):
        self.price = price
        super().__init__()

    def _instantiate(self, world: PhantomHourglassWorld) -> Rule.Resolved:
        return self.Resolved(
            self.price,
            player=world.player,
            caching_enabled=False)

    class Resolved(Rule.Resolved):
        price: int


class IslandShop(PHShop, game=tloz_ph):
    class Resolved(Rule.Resolved):
        price: int

        def calculate_costs(self, state):
            other_costs = 0
            options: PhantomHourglassOptions = state.multiworld.worlds[self.player].options
            if state.has("SW Sea Chart", self.player):
                # Includes cannon island, but not salvage arm cause that also unlocks treasure shop
                other_costs += 1550
                if options.randomize_masked_beedle:
                    other_costs += 1500
                other_costs *= cost_multiplier
            return other_costs

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            if state.has("_UT_Glitched_Logic", self.player):
                return True
            if _can_farm_rupees(state, self.player):
                return True
            other_costs = self.calculate_costs(state)
            return count_rupees(state, self.player) >= self.price+other_costs

        def __str__(self):
            return f"Has a bunch of Rupees (Island Shop)"


class BeedleShop(PHShop, game=tloz_ph):
    class Resolved(Rule.Resolved):
        price: int

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {i: {id(self)} for i in ITEM_GROUPS["Point Logic"]}

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            options: PhantomHourglassOptions = state.multiworld.worlds[self.player].options
            return beedle_eval(state, self.player, options, self.price)

        def __str__(self):
            return f"Has a bunch of Rupees (Beedle)"


class HasBeedlePoints(PHShop, game=tloz_ph):
    class Resolved(Rule.Resolved):
        price: int

        @override
        def _evaluate(self, state: CollectionState):
            if state.has("_UT_Glitched_Logic", self.player):
                return True
            points = self.price  # lol don't care
            options: PhantomHourglassOptions = state.multiworld.worlds[self.player].options
            if options.randomize_beedle_membership == "randomize":
                if self.price <= 20:  # Buying 20 points is always in logic
                    return buy_beedle_points_eval(state, self.player, options, points)
                return state.count("Beedle Points", self.player) >= points
            elif options.randomize_beedle_membership == "randomize_with_grinding":
                return buy_beedle_points_eval(state, self.player, options, points)
            return False

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            can_buy_points = buy_beedle_points_eval(state, self.player, state.multiworld.worlds[self.player].options, self.price)
            point_count = state.count("Beedle Points", self.player)
            points_res = self.price - point_count
            if points_res <= 0:
                points_res = 0
            cost = points_res * 100 * beedle_discount(state, self.player)
            has_points = state.has("Beedle Points", self.player, self.price)
            rupee_count = count_rupees(state, self.player)
            has_rupees = rupee_count >= cost
            can_farm = _can_farm_rupees(state, self.player) and (state.multiworld.worlds[self.player].options.randomize_beedle_membership == "randomize_with_grinding" or self.price <= 20)
            needed_rupees = state.multiworld.worlds[self.player].required_rupees

            return [
                {"type": "text", "text": "Has "},
                {"type": "color", "color": "green" if has_points else "salmon", "text": f"{point_count}/{str(self.price)}"},
                {"type": "text", "text": " Beedle Points"},
                {"type": "color", "color": "blue", "text": " OR "},
                {"type": "text", "text": "Has "},
                {"type": "color", "color": "green" if has_rupees else "salmon", "text": f"{rupee_count}/{needed_rupees}"},
                {"type": "text", "text": " Rupees"},
                {"type": "color", "color": "blue", "text": " OR "},
                {"type": "color", "color": "green" if can_farm else "salmon", "text": "can_farm_rupees"},
                {"type": "color", "color": "blue", "text": " OR "},
                {"type": "color", "color": "salmon", "text": "out_of_logic"},
            ]

class HasTime(Rule[PhantomHourglassWorld], game=tloz_ph):
    """
    Determine if you have enough time
    """
    time: int
    floor_func: "Callable"
    room: int or str

    def __init__(self, time, floor_func, room=4):
        self.time = time
        self.room = room
        self.floor_func = floor_func
        super().__init__()

    def _instantiate(self, world: PhantomHourglassWorld) -> Rule.Resolved:
        return self.Resolved(
            self.time,
            self.room,
            self.floor_func,
            player=world.player,
            caching_enabled=True)

    class Resolved(Rule.Resolved):
        time: int
        room: int or str
        floor_func: "Callable"

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            # print(f"Time cache: {ITEM_GROUPS['Time Logic']}")
            return {i: {id(self)} for i in ITEM_GROUPS["Time Logic"]}

        @override
        def _evaluate(self, state: CollectionState):
            options: PhantomHourglassOptions = state.multiworld.worlds[self.player].options
            time_option = options.ph_time_logic.value
            if time_option == 5:
                return True
            if time_option > 2:
                room_lookup = {3: 0, 4: 3}
                # print(f"Room = {self.room}")
                if isinstance(self.room, str) or self.room > room_lookup[time_option]:
                    return state.has("Phantom Hourglass", self.player)
                return True
            if options.ph_required and not state.has("Phantom Hourglass", self.player):
                total_sand = (state.count("Heart Container", self.player) + 2) * options.ph_heart_time.value
            else:
                total_sand = state.count("Sand", self.player) + options.ph_heart_time.value * 2
            time_lookup = {0: 1, 1: 2, 2: 4, -1: 0.5}
            multiplier = time_lookup.get(time_option, 1)

            floor_time = self.floor_func(state, self.player) + self.time
            # print(f"Floor Time {floor_time} from {self.floor_func} + {self.time}")
            # if type(self.room) == int and self.room > 12:
            #     print(f"Time floor {self.room}: {total_sand} >= {ceil(floor_time / multiplier)}")
            return total_sand >= ceil(floor_time / multiplier)

        def __str__(self):
            return f"Has enough Sand to reach floor {self.room} + {self.time}/time_logic_difficulty"

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            options: PhantomHourglassOptions = state.multiworld.worlds[self.player].options
            time_option = options.ph_time_logic.value
            has_ph_message: list[JSONMessagePart] = [
                        {"type": "text", "text": "Has "},
                        {"type": "color", "color": "green" if state.has("Phantom Hourglass", self.player) else "salmon",
                         "text": "Phantom Hourglass"}
                    ]
            if time_option == 5:
                return []
            if time_option > 2:
                room_lookup = {3: 0, 4: 3}
                if isinstance(self.room, str) or self.room > room_lookup[time_option]:
                    return has_ph_message
                return []

            if options.ph_required and not state.has("Phantom Hourglass", self.player):
                total_sand = (state.count("Heart Container", self.player) + 2) * options.ph_heart_time.value
            else:
                total_sand = state.count("Sand", self.player) + options.ph_heart_time.value * 2

            time_lookup = {0: 1, 1: 2, 2: 4, -1: 0.5}
            multiplier = time_lookup.get(time_option, 1)

            floor_time = self.floor_func(state, self.player) + self.time
            if floor_time >= 6000:
                res: list[JSONMessagePart] = [
                    {"type": "color", "color": "salmon", "text": "TimeLogicMissingItems"},
                ]
            else:
                # print(f"Floor Time {floor_time} from {self.floor_func} + {self.time}")
                has_sand = total_sand >= ceil(floor_time / multiplier)
                res: list[JSONMessagePart] = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "green" if has_sand else "salmon", "text": f"{total_sand}/{ceil(floor_time / multiplier)}"},
                    {"type": "text", "text": " Sand of Hours"},
                ]
            return res

class TotOKSmallKeys(Rule[PhantomHourglassWorld], game=tloz_ph):
    """
    Determine if you have enough time
    """
    base_count: int

    def __init__(self, base_count):
        self.base_count = base_count
        super().__init__()

    def _instantiate(self, world: PhantomHourglassWorld) -> Rule.Resolved:
        return self.Resolved(
            self.base_count,
            player=world.player,
            caching_enabled=False)

    class Resolved(Rule.Resolved):
        base_count: int

        @override
        def _evaluate(self, state: CollectionState):
            if state.has("Keyring (Temple of the Ocean King)", self.player):
                return True
            sub = 0
            ut_glitched = state.has("_UT_Glitched_Logic", self.player)
            options: PhantomHourglassOptions = state.multiworld.worlds[self.player].options
            if self.base_count >= 2 and ut_glitched and not state.has("_UT_got_chart", self.player):
                sub += 1
            if all([
                self.base_count >= 5,
                any([
                    state.has("Grappling Hook", self.player),
                    all([
                        options.randomize_pedestal_items, # Not vanilla
                        any([
                            ut_glitched,
                            options.logic in ["hard", "glitched"],
                            options.randomize_pedestal_items.value > 1,
                        ])
                    ])
                ])
            ]):
                sub += 1
            return state.has("Small Key (Temple of the Ocean King)", self.player, self.base_count - sub)

    def __str__(self):
        return f"Has {self.base_count}-shortcuts TotOK Small Keys"

class LocationNotExcluded(Rule[PhantomHourglassWorld], game=tloz_ph):
    loc: str
    def __init__(self, loc):
        self.loc = loc
        super().__init__()

    def _instantiate(self, world: PhantomHourglassWorld) -> Rule.Resolved:
        return self.Resolved(
            self.loc,
            player=world.player,
            caching_enabled=False)

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.loc}{options})"

    class Resolved(Rule.Resolved):
        location: str

        @override
        def _evaluate(self, state: CollectionState):
            loc = state.multiworld.worlds[self.player].get_location(self.location)
            return loc.progress_type != LocationProgressType.EXCLUDED

        def __str__(self):
            return f"Location {self.location} is not Excluded"


class HasRequiredSpirits(Rule[PhantomHourglassWorld], game=tloz_ph):

    def _instantiate(self, world: PhantomHourglassWorld) -> Rule.Resolved:
        return self.Resolved(
            player=world.player,
            caching_enabled=True)

    class Resolved(Rule.Resolved):

        @override
        def _evaluate(self, state: CollectionState):
            world: "PhantomHourglassWorld" = state.multiworld.worlds[self.player]
            required_items = world.boss_reward_items_pool
            spirit_items = [i for i in required_items if i in ITEM_GROUPS["Spirits"]]
            # print(f"spirit pool: {spirit_items}")
            if "Spirit (Progressive)" in spirit_items:
                if len(spirit_items) == 3:
                    # print(f"spirits: {state.has('Spirit (Progressive)', self.player, 3)}")
                    return state.has("Spirit (Progressive)", self.player, 3)
                # print(f"{spirit_items} | {state.count('_required_dungeon', self.player)}")
                # print(f"spirits: {state.has('Spirit (Progressive)', self.player, len(spirit_items))} and {state.has('_required_dungeon', self.player, len(spirit_items))}")
                return state.has("Spirit (Progressive)", self.player, len(spirit_items)) and state.has("_required_dungeon", self.player, len(spirit_items))
            # print(f"spirits: {state.has_all(spirit_items, self.player)}")
            if spirit_items[0].endswith("(Progressive)"):
                return state.has_all(spirit_items, self.player) and state.has("_required_dungeon", self.player, world.options.dungeons_required.value)
            return state.has_all(spirit_items, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            # print(f"Time cache: {ITEM_GROUPS['Time Logic']}")
            return {i: {id(self)} for i in ITEM_GROUPS["Spirits"]}

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {r: {id(self)} for r in ["Post Blaaz", "Post Cyclok", "Post Crayk",
                                            "Ghost Ship Tetra", "Post Cubus Sisters",
                                            "Post Dongorongo", "Post Gleeok", "Post Eox",
                                            "TotOK B13 Chest"]}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            world: "PhantomHourglassWorld" = state.multiworld.worlds[self.player]
            required_items = world.boss_reward_items_pool
            spirit_items = [i for i in required_items if i in ITEM_GROUPS["Spirits"]]
            print(f"Spirit items: {spirit_items}")
            extra_bit: list[JSONMessagePart] = []
            if "Spirit (Progressive)" in spirit_items:

                if len(spirit_items) < 3:
                    extra_bit = [{"type": "text", "text": " & Has Cleared "},
                                 {"type": "color", "color": "green" if state.count('_required_dungeon', self.player)>=world.options.dungeons_required.value else "salmon",
                                  "text": f"{state.count('_required_dungeon', self.player)}/{world.options.dungeons_required.value} required dungeons"}
                                 ]
                return [
                        {"type": "text", "text": "Has "},
                        {"type": "color", "color": "green" if state.has("Spirit (Progressive)", self.player, len(spirit_items)) else "salmon",
                         "text": f"{state.count('Spirit (Progressive)', self.player)}/{len(spirit_items)} Spirit (Progressive)"}
                    ] + extra_bit

            if spirit_items[0].endswith("(Progressive)"):
                extra_bit = [{"type": "text", "text": " & Has Cleared "},
                             {"type": "color", "color": "green" if state.count('_required_dungeon', self.player)>=world.options.dungeons_required.value else "salmon",
                              "text": f"{state.count('_required_dungeon', self.player)}/{world.options.dungeons_required.value} required dungeons"}
                             ]
            return [
                        {"type": "text", "text": "Has All: [ "},
                        *[{"type": "color", "color": "green" if state.has(i, self.player) else "salmon",
                         "text": f"{i}{', ' if i != spirit_items[-1] else ''}"} for i in spirit_items],
                        {"type": "text", "text": "]"}
                    ] + extra_bit
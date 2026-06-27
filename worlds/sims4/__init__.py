# standard lib imports
from typing import Any, ClassVar
from collections.abc import Mapping

# ap imports
from BaseClasses import ItemClassification, Region, Entrance
from worlds.AutoWorld import World
from ..LauncherComponents import Component, components, Type, icon_paths, launch

# TS4 specific imports
from .Locations import location_table, Sims4Location, skill_locations_table
from .Items import item_table, Sims4Item, junk_table, filler_set
from .Names import EventNames
from .Options import AspirationGoal, Sims4Options
from .Regions import sims4_careers, sims4_aspiration_milestones
from .Rules import set_rules
from .Groups import location_name_groups, item_name_groups
from .UT import UTMixin
from .Settings import Sims4Settings
from .Web import Sims4Web
from .Version import VERSION, Sims4Version


def run_client(*args: str) -> None:
    from .Client import main
    launch(main, name="The Sims 4 Client", args=args)


components.append(Component("The Sims 4 Client", func=run_client, component_type=Type.CLIENT, icon="plumbob"))

icon_paths["plumbob"] = f"ap:{__name__}/icons/plumbob.png"


class Sims4World(World, UTMixin):
    """
    The Sims 4 is the fourth installment in The Sims franchise. Like the previous games in the series,
    The Sims 4 focuses on creating and controlling a neighborhood of virtual people, called "Sims".
    """

    game = "The Sims 4"
    topology_present = False
    web = Sims4Web()

    item_name_to_id = {data["name"]: item_id for item_id, data in item_table.items()}
    location_name_to_id = {data["name"]: loc_id for loc_id, data in location_table.items()}

    location_name_groups = location_name_groups
    item_name_groups = item_name_groups

    data_version = 0
    base_id = 0x73340001
    required_client_version = (0, 4, 0)

    area_connections: dict[int, int]

    options_dataclass = Sims4Options
    options: Sims4Options

    settings: ClassVar[Sims4Settings]

    GOAL_TO_EVENT_MAPPING: ClassVar[dict[int, tuple[str, str]]] = {
        AspirationGoal.option_bodybuilder: (EventNames.bodybuilder, EventNames.bodybuilder_item),
        AspirationGoal.option_painter_extraordinaire: (
            EventNames.painter_extraordinaire, EventNames.painter_extraordinaire_item
        ),
        AspirationGoal.option_bestselling_author: (EventNames.bestselling_author, EventNames.bestselling_author_item),
        AspirationGoal.option_musical_genius: (EventNames.musical_genius, EventNames.musical_genius_item),
        AspirationGoal.option_public_enemy: (EventNames.public_enemy, EventNames.public_enemy_item),
        AspirationGoal.option_chief_of_mischief: (EventNames.chief_of_mischief, EventNames.chief_of_mischief_item),
        AspirationGoal.option_master_chef: (EventNames.master_chef, EventNames.master_chef_item),
        AspirationGoal.option_master_mixologist: (EventNames.master_mixologist, EventNames.master_mixologist_item),
        AspirationGoal.option_renaissance_sim: (EventNames.renaissance_sim, EventNames.renaissance_sim_item),
        AspirationGoal.option_nerd_brain: (EventNames.nerd_brain, EventNames.nerd_brain_item),
        AspirationGoal.option_computer_whiz: (EventNames.computer_whiz, EventNames.computer_whiz_item),
        AspirationGoal.option_serial_romantic: (EventNames.serial_romantic, EventNames.serial_romantic_item),
        AspirationGoal.option_freelance_botanist: (EventNames.freelance_botanist, EventNames.freelance_botanist_item),
        AspirationGoal.option_the_curator: (EventNames.the_curator, EventNames.the_curator_item),
        AspirationGoal.option_angling_ace: (EventNames.angling_ace, EventNames.angling_ace_item),
        AspirationGoal.option_joke_star: (EventNames.joke_star, EventNames.joke_star_item),
        AspirationGoal.option_friend_of_the_world: (
            EventNames.friend_of_the_world, EventNames.friend_of_the_world_item
        ),
        AspirationGoal.option_neighborly_advisor: (
            EventNames.neighborly_advisor, EventNames.neighborly_advisor_item
        )
    }

    def generate_early(self) -> None:
        # this is specific to UT, it doesn't apply unless UT is being used
        self.get_options_from_slot_data(self)

    def create_item(self, name: str) -> Sims4Item:
        item_id: int = self.item_name_to_id[name]

        return Sims4Item(name,
                         item_table[item_id]["classification"],
                         item_id, self.player)

    def create_location(self, name: str, parent: Region) -> Sims4Location:
        location_id: int = self.location_name_to_id[name]

        return Sims4Location(self.player, name, location_id, parent)

    def create_event(self, event: str) -> Sims4Item:
        return Sims4Item(event, ItemClassification.progression, None, self.player)

    def create_event_location(self, event: str, region: Region) -> Sims4Location:
        return Sims4Location(self.player, event, None, region)

    def create_items(self) -> None:
        used_dlc = set(
            self.options.expansion_packs.value |
            self.options.game_packs.value |
            self.options.stuff_packs.value
        )
        pool = []

        unfilled_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for item_data in item_table.values():
            if item_data['expansion'] == 'base' or item_data['expansion'] in used_dlc:
                for i in range(item_data["count"]):
                    sims4_item = self.create_item(item_data["name"])
                    pool.append(sims4_item)

        filler_needed = unfilled_locations - len(pool)

        for item_name in self.random.choices(sorted(filler_set), k=filler_needed):
            item = self.create_item(item_name)
            pool.append(item)

        self.multiworld.itempool += pool

    def create_region(self, name: str, locations: list[str] | None = None, exits: list[str] | None = None) -> Region:
        ret = Region(name, self.player, self.multiworld)
        if locations:
            for location_name in locations:
                location = self.create_location(location_name, ret)
                ret.locations.append(location)
        if exits:
            for region_exit in exits:
                ret.exits.append(Entrance(self.player, region_exit, ret))
        return ret

    def create_regions(self) -> None:
        menu = self.create_region("Menu", locations=None, exits=None)
        chosen_careers = sorted(self.options.career.value)
        goal = self.options.goal
        goal_value = goal.value
        aspiration_key = goal.current_key
        for career_key in chosen_careers:
            for career in sims4_careers[career_key.lower().replace(" ", "_")]:
                menu.locations.append(self.create_location(career, menu))
        for aspiration in sims4_aspiration_milestones[aspiration_key]:
            menu.locations.append(self.create_location(aspiration, menu))
        used_dlc = set(
            self.options.expansion_packs.value |
            self.options.game_packs.value |
            self.options.stuff_packs.value
        )
        for skill in skill_locations_table.values():
            skill_name = skill["name"]
            if skill['expansion'] == 'base' or skill['expansion'] in used_dlc:
                menu.locations.append(self.create_location(skill_name, menu))
        mapping = self.GOAL_TO_EVENT_MAPPING.get(goal_value)
        if mapping:
            event_name, item_name = mapping
            event = self.create_event_location(event_name, menu)
            menu.locations.append(event)
            event.place_locked_item(self.create_event(item_name))

        self.multiworld.regions.append(menu)

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, self.options)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {
            "goal": self.options.goal.current_key,
            "career": self.options.career.value,
            "expansion_packs": self.options.expansion_packs.value,
            "game_packs": self.options.game_packs.value,
            "stuff_packs": self.options.stuff_packs.value,
            "cas_kits": self.options.cas_kits.value,
            "build_kits": self.options.build_kits.value,
            "version": Sims4Version.tuple_to_str(VERSION),
        }
        return slot_data

    def get_filler_item_name(self) -> str:
        return self.random.choice([entry['name'] for entry in junk_table.values()])

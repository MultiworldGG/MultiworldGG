from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC
from BaseClasses import CollectionState

from ..Hints import *
from ..Items import ITEM_TABLE
from ..Locations import SSLocType, SSLocHintType
from ..Constants import GONDO_UPGRADES, HINT_REGIONS, DUNGEON_FINAL_CHECKS, DUNGEON_INITIAL_REGIONS
from ..logic.Requirements import ALL_REQUIREMENTS

from .ItemPlacement import item_classification

if TYPE_CHECKING:
    from .. import SSWorld


class Hints:
    """
    Class handles in-game fi and gossip stone hints, as well as song and impa hints.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.hint_regions = HintRegions(self.world)
        self.hint_regions.get_sots_barren_regions()
        self.hint_regions.get_path_regions()
        self.hint_regions.get_er_regions()

        #self.advancement_hints = AdvancementHints(self.world, self.hint_regions)

        self.placed_hints: dict[str, list] = {}
        self.placed_hints_log: dict[str, list] = {}
        self.locations_for_hint: dict = {}
        self.hinted_locations: list[Location] = []
        self.distribution_option = [
            "Standard",
            "Weak",
            "Strong",
            "Funky",
            "Location and Item Hints Only",
            "Large Multiworld",
            "Standard with Dungeon ER",
            #"Full Entrance Rando",
            "Junk",
        ][self.world.options.hint_distribution.value]
        self.distribution: dict[str, any] = HINT_DISTRIBUTIONS[self.distribution_option]

        self.always_locations = [
            self.world.get_location(loc)
            for loc in self.world.progress_locations
            if self.world.get_location(loc).hint == SSLocHintType.ALWAYS
        ]
        self.sometimes_locations = [
            self.world.get_location(loc)
            for loc in self.world.progress_locations
            if self.world.get_location(loc).hint == SSLocHintType.SOMETIMES
        ]
        self.hintable_items = []
        for itm, data in ITEM_TABLE.items():
            classification = (
                data.classification
                if item_classification(self.world, itm) is None
                else item_classification(self.world, itm)
            )
            if classification == IC.progression or classification == IC.progression_skip_balancing:
                if data.code is None:
                    continue
                self.hintable_items.extend([itm] * data.quantity)

        # Remove starting items and gondo items (if shuffle off) from hintable pool
        for itm in self.world.starting_items:
            if itm in self.hintable_items:
                self.hintable_items.remove(itm)
        if not self.world.options.gondo_upgrades:
            for itm in GONDO_UPGRADES:
                if itm in self.hintable_items:
                    self.hintable_items.remove(itm)
        self.all_hints = []

    def handle_hints(self) -> tuple[dict[str, list], dict[str, list]]:
        """
        Handles hints for Skyward Sword during the APSSR file output.

        :param world: The SS game world.
        :return: A tuple of a dict containing in-game hints for Fi, each Gossip Stone, and songs; and a dict of log hints.
        """
        if self.world.options.song_hints == "direct":
            self.sometimes_locations = [
                loc
                for loc in self.sometimes_locations
                if loc.type != SSLocType.WPOBJ
            ]

        # Create and fill hint classes
        location_hints, item_hints, sots_hints, barren_hints, path_hints, entrance_hints, junk_hints = self._create_hints()

        self.all_hints.extend(location_hints)
        self.all_hints.extend(item_hints)
        self.all_hints.extend(sots_hints)
        self.all_hints.extend(barren_hints)
        self.all_hints.extend(path_hints)
        self.all_hints.extend(entrance_hints)
        self.all_hints.extend(junk_hints)
        self.world.random.shuffle(self.all_hints)

        for hint, data in HINT_TABLE.items():
            if data.type == SSHintType.FI:
                fi_hints = []
                for _ in range(self.distribution["fi"]):
                    fi_hints.append(self.all_hints.pop())
                if self.world.options.explicit_hints:
                    self.placed_hints["Fi"] = [fh.to_explicit_text() for fh in fi_hints]
                else:
                    self.placed_hints["Fi"] = [fh.to_fi_text() for fh in fi_hints]
                self.placed_hints_log["Fi"] = [fh.to_log_text() for fh in fi_hints]
                self.locations_for_hint["Fi"] = [(fh.location.address, fh.location.player, 0) for fh in fi_hints if isinstance(fh, SSLocationHint)]
                if self.world.options.precise_item_hints:
                    self.locations_for_hint["Fi"].extend([(fh.location.address, fh.location.player, 0) for fh in fi_hints if isinstance(fh, SSItemHint)])
                if self.world.options.precise_hints:
                    self.locations_for_hint["Fi"].extend([(fh.location.address, self.world.player, 30 if fh.location.item.player == self.world.player else 0) for fh in fi_hints if isinstance(fh, SSSotSHint) or isinstance(fh, SSPathHint)])
            elif data.type == SSHintType.STONE:
                stone_hints = []
                for _ in range(self.distribution["hints_per_stone"]):
                    stone_hints.append(self.all_hints.pop())
                if self.world.options.explicit_hints:
                    self.placed_hints[hint] = [sh.to_explicit_text() for sh in stone_hints]
                else:
                    self.placed_hints[hint] = [sh.to_stone_text() for sh in stone_hints]
                self.placed_hints_log[hint] = [sh.to_log_text() for sh in stone_hints]
                self.locations_for_hint[hint] = [(sh.location.address, sh.location.player, 0) for sh in stone_hints if isinstance(sh, SSLocationHint)]
                if self.world.options.precise_item_hints:
                    self.locations_for_hint[hint].extend([(sh.location.address, sh.location.player, 0) for sh in stone_hints if isinstance(sh, SSItemHint)])
                if self.world.options.precise_hints:
                    self.locations_for_hint[hint].extend([(sh.location.address, self.world.player, 30 if sh.location.item.player == self.world.player else 0) for sh in stone_hints if isinstance(sh, SSSotSHint) or isinstance(sh, SSPathHint)])
            elif data.type == SSHintType.SONG:
                song_hints = self._handle_song_hints(hint)
                self.placed_hints[hint] = song_hints
                self.placed_hints_log[hint] = song_hints

        return self.placed_hints, self.placed_hints_log

    def handle_impa_sot_hint(self) -> tuple[str, str] | None:
        """
        Handles Impa's Stone of Trials hint.
        """
        sot_locations = [
            loc
            for loc in self.multiworld.get_locations()
            if loc.item.player == self.world.player
            and loc.item.name == "Stone of Trials"
        ]
        if len(sot_locations) == 1:
            sot_location = sot_locations.pop()
            return (
                sot_location.parent_region.name,
                self.multiworld.get_player_name(sot_location.player),
            )
        else:
            return None

    def _create_hints(self) -> tuple[list, list, list, list, list, list, list]:
        fi_hints = self.distribution["fi"]
        hints_per_stone = self.distribution["hints_per_stone"]
        num_hints_to_place = fi_hints + (18 * hints_per_stone)
        location_hints: list[SSLocationHint] = []
        item_hints: list[SSItemHint] = []
        sots_hints: list[SSSotSHint] = []
        barren_hints: list[SSBarrenHint] = []
        path_hints: list[SSPathHint] = []
        entrance_hints: list[SSEntranceHint] = []
        #advancement_hints: list[] = []
        junk_hints: list[SSJunkHint] = []

        if num_hints_to_place == 0:
            return location_hints, item_hints, sots_hints, barren_hints, path_hints, entrance_hints, junk_hints

        # Place always hints first
        if "always" in self.distribution["distribution"]:
            for loc in self.always_locations:
                location_hints.append(SSLocationHint(loc, self.world))
                self.hinted_locations.append(loc)

        if len(location_hints) >= num_hints_to_place:
            return location_hints, item_hints, sots_hints, barren_hints, path_hints, entrance_hints, junk_hints

        # Place fixed hints next, in order
        current_order = 0
        max_order = self.distribution["max_order"]
        while (
            len(location_hints) + len(item_hints) + len(sots_hints) + len(barren_hints) + len(path_hints) + len(entrance_hints) + len(junk_hints)
        ) < num_hints_to_place:
            for h_type, h_data in self.distribution["distribution"].items():
                if h_type != "always":
                    if h_data["order"] == current_order:
                        fixed_hints_to_place = h_data["fixed"]
                        if h_type == "sometimes":
                            location_hints.extend(
                                self._create_sometimes_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
                        elif h_type == "item":
                            item_hints.extend(
                                self._create_item_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
                        elif h_type == "sots":
                            sots_hints.extend(
                                self._create_sots_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
                        elif h_type == "barren":
                            barren_hints.extend(
                                self._create_barren_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
                        elif h_type == "path":
                            path_hints.extend(
                                self._create_path_hints(fixed_hints_to_place, True)
                                * h_data["copies"]
                            )
                        elif h_type == "entrance":
                            entrance_hints.extend(
                                self._create_entrance_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
                        elif h_type == "junk":
                            junk_hints.extend(
                                self._create_junk_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
            if current_order >= max_order:
                break
            current_order += 1

        # Fill the remaining hints based on weights
        while (
            len(location_hints) + len(item_hints) + len(sots_hints) + len(barren_hints) + len(path_hints) + len(entrance_hints) + len(junk_hints)
        ) < num_hints_to_place:
            placeable_hint_types = ["junk"]
            if (
                len(self.sometimes_locations) > 0
                and "sometimes" in self.distribution["distribution"]
            ):
                placeable_hint_types.append("sometimes")
            if (
                len(self.hintable_items) > 0
                and "item" in self.distribution["distribution"]
            ):
                placeable_hint_types.append("item")
            if len(self.hint_regions.sots_locations) > 0 and "sots" in self.distribution["distribution"]:
                placeable_hint_types.append("sots")
            if len(self.hint_regions.barren_regions) > 0 and "barren" in self.distribution["distribution"]:
                placeable_hint_types.append("barren")
            if "path" in self.distribution["distribution"]:
                for dun, locs in self.hint_regions.path_locations.items():
                    if len(locs) > 0:
                        placeable_hint_types.append("path")
                        break
            if "entrance" in self.distribution["distribution"]:
                if (
                    len(self.hint_regions.er_priority_regions) > 0
                    or len(self.hint_regions.er_sots_regions) > 0
                    or len(self.hint_regions.er_nonpriority_regions) > 0
                ):
                    placeable_hint_types.append("entrance")

            hint_type_to_place = self.world.random.choices(
                placeable_hint_types,
                weights=[
                    self.distribution["distribution"][t]["weight"]
                    for t in placeable_hint_types
                ],
                k=1,
            ).pop()

            if hint_type_to_place == "sometimes":
                copies = self.distribution["distribution"]["sometimes"]["copies"]
                location_hints.extend(self._create_sometimes_hints(1) * copies)
            if hint_type_to_place == "item":
                copies = self.distribution["distribution"]["item"]["copies"]
                item_hints.extend(self._create_item_hints(1) * copies)
            if hint_type_to_place == "sots":
                copies = self.distribution["distribution"]["sots"]["copies"]
                sots_hints.extend(self._create_sots_hints(1) * copies)
            if hint_type_to_place == "barren":
                copies = self.distribution["distribution"]["barren"]["copies"]
                barren_hints.extend(self._create_barren_hints(1) * copies)
            if hint_type_to_place == "path":
                copies = self.distribution["distribution"]["path"]["copies"]
                path_hints.extend(self._create_path_hints(1, False) * copies)
            if hint_type_to_place == "entrance":
                copies = self.distribution["distribution"]["entrance"]["copies"]
                entrance_hints.extend(self._create_entrance_hints(1) * copies)
            if hint_type_to_place == "junk":
                copies = self.distribution["distribution"]["junk"]["copies"]
                junk_hints.extend(self._create_junk_hints(1) * copies)

        return location_hints, item_hints, sots_hints, barren_hints, path_hints, entrance_hints, junk_hints

    def _create_sometimes_hints(self, q) -> list[SSLocationHint]:
        hints = []

        for _ in range(q):
            self.world.random.shuffle(self.sometimes_locations)
            loc_to_hint = self.sometimes_locations.pop()
            if loc_to_hint in self.hinted_locations:
                raise Exception(
                    f"Tried to hint location {loc_to_hint.name} but location was already hinted!"
                )
            hints.append(loc_to_hint)
            self.hinted_locations.append(loc_to_hint)

        return [SSLocationHint(loc, self.world) for loc in hints]

    def _create_item_hints(self, q) -> list[SSItemHint]:
        hints = []

        for _ in range(q):
            while True:
                self.world.random.shuffle(self.hintable_items)
                itm_to_hint = self.hintable_items.pop()
                locs = [
                    loc
                    for loc in self.world.multiworld.get_locations()
                    if loc.item.name == itm_to_hint and loc.item.player == self.world.player
                ]
                for loc in self.hinted_locations:
                    if loc in locs:
                        locs.remove(loc)
                if len(locs) > 0:
                    break

            hints.append(itm_to_hint)

        return [SSItemHint(itm, self.world) for itm in hints]
    
    def _create_sots_hints(self, q) -> list[SSSotSHint]:
        hints = []

        if q > len(self.hint_regions.sots_locations):
            num_hints = len(self.hint_regions.sots_locations)
        else:
            num_hints = q

        for _ in range(num_hints):
            self.world.random.shuffle(self.hint_regions.sots_locations)
            loc_to_hint = self.hint_regions.sots_locations.pop()
            hints.append(loc_to_hint)

        return [SSSotSHint(loc, self.world) for loc in hints]
    
    def _create_barren_hints(self, q) -> list[SSBarrenHint]:
        hints = []

        if q > len(self.hint_regions.barren_regions):
            num_hints = len(self.hint_regions.barren_regions)
        else:
            num_hints = q

        for _ in range(num_hints):
            self.world.random.shuffle(self.hint_regions.barren_regions)
            reg_to_hint = self.hint_regions.barren_regions.pop()
            hints.append(reg_to_hint)

        return [SSBarrenHint(reg, self.world) for reg in hints]
    
    def _create_path_hints(self, q, per_dun) -> list[SSPathHint]:
        hints = []

        duns = [dun for dun in self.hint_regions.path_locations.keys()]
        self.world.random.shuffle(duns)

        if per_dun:
            q = q * len(duns)

        i = 0
        for _ in range(q):
            dun = duns[i]
            if len(self.hint_regions.path_locations[dun]) == 0:
                continue
            self.world.random.shuffle(self.hint_regions.path_locations[dun])
            loc_to_hint = self.hint_regions.path_locations[dun].pop()
            hints.append((loc_to_hint, dun))

            i =+ 1
            if i % len(duns) == 0:
                i = 0

        return [SSPathHint(loc, dun, self.world) for loc, dun in hints]
    
    def _create_entrance_hints(self, q) -> list[SSEntranceHint]:
        hints = []

        for _ in range(q):
            # Try to place priority -> sots -> nonpriority
            if len(self.hint_regions.er_priority_regions) > 0:
                self.world.random.shuffle(self.hint_regions.er_priority_regions)
                reg = self.hint_regions.er_priority_regions.pop()
            elif len(self.hint_regions.er_sots_regions) > 0:
                self.world.random.shuffle(self.hint_regions.er_sots_regions)
                reg = self.hint_regions.er_sots_regions.pop()
            elif len(self.hint_regions.er_nonpriority_regions) > 0:
                self.world.random.shuffle(self.hint_regions.er_nonpriority_regions)
                reg = self.hint_regions.er_nonpriority_regions.pop()
            else:
                continue
            region_ents = [(ex, ent) for ex, ent, x in self.world.entrances.entrance_mapping.mapping if ent.region == reg.name and x == False]
            if len(region_ents) == 0:
                continue
            ex, ent = self.world.random.choice(region_ents)
            
            hints.append((ex, ent))

        return [SSEntranceHint(ex, ent, self.world) for ex, ent in hints]

    def _create_junk_hints(self, q) -> list[SSJunkHint]:
        hints = self._get_junk_hint_texts(q)
        return [SSJunkHint(text) for text in hints]

    def _handle_song_hints(self, hint) -> list[str]:
        direct_text = "This trial holds {plr}'s {itm}"
        required_text = "Your spirit will grow by completing this trial"
        useful_text = "Someone might need its reward..."
        useless_text = "Its reward is probably not too important..."

        trial_gate = SONG_HINT_TO_TRIAL_GATE[hint]
        trial_connection = [
            trl
            for trl, gate in self.world.entrances.trial_connections.items()
            if gate == trial_gate
        ].pop()
        trial_item = self.world.get_location(f"{trial_connection} - Trial Reward").item
        if self.world.options.song_hints == "none":
            return [""]
        if self.world.options.song_hints == "basic":
            return (
                [useful_text]
                if trial_item.classification == IC.progression
                or trial_item.classification == IC.progression_skip_balancing
                or trial_item.classification == IC.useful
                else [useless_text]
            )
        if self.world.options.song_hints == "advanced":
            if trial_item.classification == IC.progression or trial_item.classification == IC.progression_skip_balancing:
                return [required_text]
            elif trial_item.classification == IC.useful:
                return [useful_text]
            else:
                return [useless_text]
        if self.world.options.song_hints == "direct":
            self.locations_for_hint[hint] = [(self.world.get_location((f"{trial_connection} - Trial Reward")).address, self.world.player, 0)]
            player_name = self.multiworld.get_player_name(trial_item.player)
            item_name = trial_item.name
            return [direct_text.format(plr=player_name, itm=item_name)]

    def _get_junk_hint_texts(self, q: int) -> list[str]:
        """
        Get q number of junk hint texts.

        :param q: Quantity of junk hints to return.
        :return: List of q junk hints.
        """
        return self.world.random.sample(JUNK_HINT_TEXT, k=q)

class HintRegions:
    """
    
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = self.world.multiworld

        # Spirit of the Sword (SotS), items are required to beat the game
        self.sots_locations = []
        self.sots_regions = []

        # Progress, items assist progression but are not required to beat the game
        self.progress_locations = []
        self.progress_regions = []
        
        # Barren, items are filler and not required to beat the game
        self.barren_locations = []
        self.barren_regions = []

        # Path, items are required to beat a dungeon
        self.path_locations = {}

        # ER Regions
        self.er_priority_regions = []
        self.er_sots_regions = []
        self.er_nonpriority_regions = []

    def get_sots_barren_regions(self):
        for reg in HINT_REGIONS:
            if (
                reg == "Hylia's Realm"
                or reg in self.world.dungeons.required_dungeons
                or (reg in self.world.dungeons.banned_dungeons and self.world.options.empty_unrequired_dungeons)
                or (reg == "Sky Keep" and self.world.dungeons.sky_keep_required)
                or (reg == "Sky Keep" and not self.world.dungeons.sky_keep_required and self.world.options.empty_unrequired_dungeons)
            ):
                continue
            for loc in self.world.get_locations():
                if loc.region != reg:
                    continue
                state = CollectionState(self.multiworld)
                state.locations_checked.add(loc)
                if not self.multiworld.can_beat_game(state):
                    self.sots_locations.append(loc)
                    if reg not in self.sots_regions:
                        self.sots_regions.append(reg)
                else:
                    if loc.item.classification & IC.progression:
                        self.progress_locations.append(loc)
                        if reg not in self.progress_regions:
                            self.progress_regions.append(reg)
                    else:
                        self.barren_locations.append(loc)
            if reg not in self.sots_regions and reg not in self.progress_regions:
                self.barren_regions.append(reg)

    def get_path_regions(self):
        for dun in self.world.dungeons.required_dungeons:
            self.path_locations[dun] = []
            for loc in self.world.get_locations():
                state = CollectionState(self.multiworld)
                state.sweep_for_advancements([swloc for swloc in self.world.get_locations() if swloc != loc])
                if not state.can_reach_location(DUNGEON_FINAL_CHECKS[dun], self.world.player):
                    if self.world.region_to_hint_region(loc.parent_region) != dun:
                        self.path_locations[dun].append(loc)

    def get_er_regions(self):
        if self.world.options.randomize_entrances == "none":
            return
        elif self.world.options.randomize_entrances == "required_dungeons_only":
            priority_regions = []
            priority_regions.extend([DUNGEON_INITIAL_REGIONS[dun] for dun in self.world.dungeons.required_dungeons])
            if self.world.dungeons.sky_keep_required:
                priority_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])
            nonpriority_regions = []
            sots_regions = []
        elif self.world.options.randomize_entrances == "dungeons_only":
            priority_regions = []
            priority_regions.extend([DUNGEON_INITIAL_REGIONS[dun] for dun in self.world.dungeons.required_dungeons])
            if self.world.dungeons.sky_keep_required:
                priority_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])
            nonpriority_regions = []
            nonpriority_regions.extend([DUNGEON_INITIAL_REGIONS[dun] for dun in self.world.dungeons.banned_dungeons])
            if not self.world.dungeons.sky_keep_required:
                nonpriority_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])
            sots_regions = []
        # elif self.world.options.randomize_entrances == "all_entrances":
        #     priority_regions = ["Sealed Grounds - Sealed Temple"]
        #     priority_regions.extend([DUNGEON_INITIAL_REGIONS[dun] for dun in self.world.dungeons.required_dungeons])
        #     if self.world.dungeons.sky_keep_required:
        #         priority_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])
        #     sots_regions = []
        #     nonpriority_regions = []
        #     for reg, data in ALL_REQUIREMENTS.items():
        #         if data["hint_region"] in self.sots_regions:
        #             sots_regions.append(reg)
        #         else:
        #             nonpriority_regions.append(reg)
        else:
            raise Exception("Unknown option for setting randomize_entrances")
        
        self.er_priority_regions.extend([self.world.get_region(reg) for reg in priority_regions])
        self.er_sots_regions.extend([self.world.get_region(reg) for reg in sots_regions])
        self.er_nonpriority_regions.extend([self.world.get_region(reg) for reg in nonpriority_regions])

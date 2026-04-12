# Credit to sg4e and the YuGiOh Forbidden Memories apworld for being the basis of this project

import typing
import warnings
import Utils
import json
import os
import settings

from worlds.AutoWorld import World, WebWorld
from BaseClasses import CollectionState, Region, Tutorial, LocationProgressType
from worlds.generic.Rules import set_rule

from .rom import YuGiOhDDMProcedurePatch
from .client import YGODDMClient
from .utils import Constants
from .items import YGODDMItem, item_name_to_item_id, create_item as fabricate_item, create_victory_event, create_victory_event_tournament
from .locations import YGODDMLocation, DuelistLocation, Duelist2ndLocation, location_name_to_id as location_map, TournamentLocation, Tournament2ndLocation, Tournament3rdLocation, DiceLocation
from .dice import Dice, all_dice, id_to_dice
from .options import YGODDMOptions, FreeDuelRewards, Progression, BonusItemMode, RandomizeStartingDice
from .duelists import Duelist, all_duelists, map_duelists_to_ids, all_duelists_test
from .tournament import Tournament, all_tournaments, name_to_tournament
from .version import __version__

class YGODDMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the YuGiOh Dungeon Dice Monsters rom"""
        description = "Yu-Gi-Oh! Dungeon Dice Monsters rom File"
        copy_to = "Yu-Gi-Oh! - Dungeon Dice Monsters.gba"
        md5s = ["1AC4901F9A831D6B86CA776BB61F8D8B"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = False

class YGODDMWeb(WebWorld):
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing {Constants.GAME_NAME} with MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jumza"]
    )

    tutorials = [setup_en]

class YGODDMWorld(World):
    """Yu-Gi-Oh! Dungeon Dice Monsters is a Game Boy Advance dice-based tactics game based on an original board game
    featured in the Yu-Gi-Oh! storyline."""
    game: str = Constants.GAME_NAME
    options_dataclass = YGODDMOptions
    options: YGODDMOptions
    required_client_version = (0, 5, 0)
    web = YGODDMWeb()
    settings: typing.ClassVar[YGODDMSettings]

    duelist_unlock_order: typing.List[Duelist]
    starting_unlocked_duelists: typing.List[Duelist]
    starting_randomized_dice: typing.List[Dice]

    location_name_to_id = location_map
    item_name_to_id = item_name_to_item_id

    def generate_output(self, output_directory: str) -> None:
        patch_dict: dict[str, typing.Any] = dict()
        patch_dict["DiceStats"] = self.options.dice_stats.value

        rom_name_text = f"YGODDM{Utils.__version__.replace(".","")[0:3]}_{self.player}_{self.multiworld.seed:9}"
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        patch_dict["RomName"] = f'YGODDM{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'

        patch_dict["OutputFile"] = f'{self.multiworld.get_out_file_name_base(self.player)}'

        patch = YuGiOhDDMProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("patch_file.json", json.dumps(patch_dict).encode("UTF-8"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)


    def get_available_duelists(self, state: CollectionState) -> typing.List[Duelist]:
        available_duelists: typing.List[Duelist] = [duelist for duelist in self.starting_unlocked_duelists]
        for d in self.duelist_unlock_order:
            if d not in self.starting_unlocked_duelists:
                if state.has(d.name, self.player):
                    available_duelists.append(d)
        return available_duelists
    
    def get_available_dice(self, state: CollectionState) -> typing.List[Dice]:
        available_dice: typing.List[Dice] = []
        for d in all_dice:
            if d.name != "D. Magician Girl": #Exclude Dark Magician Girl
                if state.count(Constants.SHOP_PROGRESSION_ITEM_NAME, self.player) >= (d.shop_level + 2) // 3 or state.has(d.name, self.player):
                    #Hardcoded to be 6 groups of 3 for shop progression
                    available_dice.append(d)
        return available_dice

    def generate_early(self) -> None:
        self.duelist_unlock_order = all_duelists
        self.tournament_locations = all_tournaments
        self.starting_unlocked_duelists = [Duelist.YUGI_MOTO]
        self.starting_randomized_dice = []
        # Figure out which other duelists will start unlocked
        start_duelists: typing.List[Duelist] = [duelist for duelist in all_duelists]
        start_duelists.remove(Duelist.YUGI_MOTO)
        start_duelists.remove(Duelist.YAMI_YUGI)
        self.random.shuffle(start_duelists)
        self.starting_unlocked_duelists += start_duelists[0:self.options.starting_duelists.value - 1]
        # Add all starting unlocked duelists to starting item pool, if you're on free duel progression
        if (self.options.progression.value == Progression.option_free_duel):
            for d in self.starting_unlocked_duelists:
                self.options.start_inventory.value[d.name] = 1
        # Given the option, get a random set of starting dice
        if (self.options.randomize_starting_dice.value):
            rando_dice_ids: typing.Set[int] = set()
            while (len(rando_dice_ids) < 15):
                new_dice_id = self.random.randint(0, 200)
                while ((new_dice_id in rando_dice_ids) or (new_dice_id not in id_to_dice)):
                    new_dice_id = (new_dice_id + 1) % 201
                rando_dice_ids.add(new_dice_id)
                self.starting_randomized_dice.append(id_to_dice[new_dice_id])
                # Put the Randomized dice into the start inventory
                self.options.start_inventory.value[id_to_dice[new_dice_id].name] = 1


    def create_item(self, name: str) -> YGODDMItem:
        return fabricate_item(name, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        itempool: typing.List[YGODDMItem] = []

        if (self.options.progression.value == Progression.option_free_duel):
            # All duelists are accessible from Free Duel, so it is the only region
            free_duel_region = Region("Free Duel", self.player, self.multiworld)

            # Add duelist locations
            # Hold a reference to these to set locked items and victory event

            for duelist in self.duelist_unlock_order:
                if duelist is not Duelist.YAMI_YUGI:
                    duelist_location: DuelistLocation = DuelistLocation(free_duel_region, self.player, duelist)
                    set_rule(duelist_location, (lambda state, d=duelist_location, duelist_name = duelist.name: state.has(duelist_name, self.player)))
                    free_duel_region.locations.append(duelist_location)

            # If enabled, add Duelist 2nd locations
            if (self.options.free_duel_rewards.value == FreeDuelRewards.option_two):
                for duelist in self.duelist_unlock_order:
                    if duelist is not Duelist.YAMI_YUGI:
                        duelist_2nd_location: Duelist2ndLocation = Duelist2ndLocation(free_duel_region, self.player, duelist)
                        set_rule(duelist_2nd_location, (lambda state, d=duelist_2nd_location, duelist_name = duelist.name: state.has(duelist_name, self.player)))
                        free_duel_region.locations.append(duelist_2nd_location)
                
            
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                Constants.VICTORY_ITEM_NAME, self.player
            )

            # Add Duelist unlock items
            for duelist in self.duelist_unlock_order:
                if duelist not in self.starting_unlocked_duelists and duelist is not Duelist.YAMI_YUGI:
                    itempool.append(self.create_item(duelist.name))

            # Set Yami Yugi's item to game victory
            # Set rule so it knows that Yami Yugi can't appear until you have the right number of duelist items
            yami_yugi_location: DuelistLocation = DuelistLocation(free_duel_region, self.player, Duelist.YAMI_YUGI)
            duelist_names: typing.List[str] = []
            for d in self.duelist_unlock_order:
                if d not in self.starting_unlocked_duelists and d is not Duelist.YAMI_YUGI:
                    duelist_names.append(d.name)

            set_rule(yami_yugi_location, lambda state: state.has_from_list(duelist_names, self.player, max(self.options.free_duel_goal.value - self.options.starting_duelists, 0)))
            yami_yugi_location.place_locked_item(create_victory_event(self.player))
            free_duel_region.locations.append(yami_yugi_location)

            menu_region.connect(free_duel_region)
            self.multiworld.regions.append(free_duel_region)
        else:
            # else Progression is Tournament mode
            division_1_region = Region("Division 1", self.player, self.multiworld)
            division_2_region = Region("Division 2", self.player, self.multiworld)
            division_3_region = Region("Division 3", self.player, self.multiworld)

            for tournament in all_tournaments:
                if tournament.name != Constants.VICTORY_ITEM_TOURNAMENT_NAME:
                    if tournament.offset == Constants.DIVISION_1_COMPLETION_OFFSET:
                        tournament_location: TournamentLocation = TournamentLocation(division_1_region, self.player, tournament)
                        division_1_region.locations.append(tournament_location)
                    elif tournament.offset == Constants.DIVISION_2_COMPLETION_OFFSET:
                        tournament_location: TournamentLocation = TournamentLocation(division_2_region, self.player, tournament)
                        set_rule(tournament_location, lambda state: state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                        division_2_region.locations.append(tournament_location)
                    else:
                        tournament_location: TournamentLocation = TournamentLocation(division_3_region, self.player, tournament)
                        set_rule(tournament_location, lambda state: state.has(Constants.DIVISION_3_ITEM_NAME, self.player) and state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                        division_3_region.locations.append(tournament_location)

            # If enabled, add Tournament 2nd locations
            if (self.options.tournament_rewards.value >= 1):
                for tournament in all_tournaments:
                    if tournament.name != Constants.VICTORY_ITEM_TOURNAMENT_NAME:
                        if tournament.offset == Constants.DIVISION_1_COMPLETION_OFFSET:
                            tournament_2nd_location: Tournament2ndLocation = Tournament2ndLocation(division_1_region, self.player, tournament)
                            division_1_region.locations.append(tournament_2nd_location)
                        elif tournament.offset == Constants.DIVISION_2_COMPLETION_OFFSET:
                            tournament_2nd_location: Tournament2ndLocation = Tournament2ndLocation(division_2_region, self.player, tournament)
                            set_rule(tournament_2nd_location, lambda state: state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                            division_2_region.locations.append(tournament_2nd_location)
                        else:
                            tournament_2nd_location: Tournament2ndLocation = Tournament2ndLocation(division_3_region, self.player, tournament)
                            set_rule(tournament_2nd_location, lambda state: state.has(Constants.DIVISION_3_ITEM_NAME, self.player) and state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                            division_3_region.locations.append(tournament_2nd_location)
            
            # If enabled, add Tournament 3rd locations
            if (self.options.tournament_rewards.value >= 2):
                for tournament in all_tournaments:
                    if tournament.name != Constants.VICTORY_ITEM_TOURNAMENT_NAME:
                        if tournament.offset == Constants.DIVISION_1_COMPLETION_OFFSET:
                            tournament_3rd_location: Tournament3rdLocation = Tournament3rdLocation(division_1_region, self.player, tournament)
                            division_1_region.locations.append(tournament_3rd_location)
                        elif tournament.offset == Constants.DIVISION_2_COMPLETION_OFFSET:
                            tournament_3rd_location: Tournament3rdLocation = Tournament3rdLocation(division_2_region, self.player, tournament)
                            set_rule(tournament_3rd_location, lambda state: state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                            division_2_region.locations.append(tournament_3rd_location)
                        else:
                            tournament_3rd_location: Tournament3rdLocation = Tournament3rdLocation(division_3_region, self.player, tournament)
                            set_rule(tournament_3rd_location, lambda state: state.has(Constants.DIVISION_3_ITEM_NAME, self.player) and state.has(Constants.DIVISION_2_ITEM_NAME, self.player))
                            division_3_region.locations.append(tournament_3rd_location)
            
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                Constants.VICTORY_ITEM_TOURNAMENT_NAME, self.player
            )

            # Add Division 2 and 3 unlock items to pool
            itempool.append(self.create_item(Constants.DIVISION_2_ITEM_NAME))
            itempool.append(self.create_item(Constants.DIVISION_3_ITEM_NAME))

            # Set The Last Judgment's item to game victory
            the_last_judgment_location: TournamentLocation = TournamentLocation(division_3_region, self.player, name_to_tournament["The Last Judgment"])
            the_last_judgment_location.place_locked_item(create_victory_event_tournament(self.player))
            division_3_region.locations.append(the_last_judgment_location)

            menu_region.connect(division_1_region)
            division_1_region.connect(
                division_2_region,
                None,
                lambda state: state.has(Constants.DIVISION_2_ITEM_NAME, self.player)
            )
            division_2_region.connect(
                division_3_region,
                None,
                lambda state: state.has(Constants.DIVISION_3_ITEM_NAME, self.player) and state.has(Constants.DIVISION_2_ITEM_NAME, self.player)
                )
            self.multiworld.regions.append(division_1_region)
            self.multiworld.regions.append(division_2_region)
            self.multiworld.regions.append(division_3_region)

        if (self.options.bonus_item_mode.value == BonusItemMode.option_shop_progress):
            # All dice locations are considered to be in the Grandpas Shop region
            grandpas_shop_region = Region("Grandpas Shop", self.player, self.multiworld)

            for dice in all_dice:
                if dice.name != "D. Magician Girl": #Exclude her from dice locations
                    dice_location: DiceLocation = DiceLocation(grandpas_shop_region, self.player, dice)
                    set_rule(dice_location, (lambda state, d=dice_location:
                                             d.dice in self.get_available_dice(state)))
                    grandpas_shop_region.locations.append(dice_location)

            self.multiworld.regions.append(grandpas_shop_region)
            menu_region.connect(grandpas_shop_region)
            
            # Create the 6 shop progression items
            for i in range(1,7):
                itempool.append(self.create_item(Constants.SHOP_PROGRESSION_ITEM_NAME))

            # Create filler gold checks
            filler_slots: int
            if (self.options.progression.value == Progression.option_free_duel):
                filler_slots = (len(free_duel_region.locations) + len(grandpas_shop_region.locations)) - len(itempool)
            else:
                filler_slots = (len(division_1_region.locations) + len(division_2_region.locations) + len(division_3_region.locations) + len(grandpas_shop_region.locations)) - len(itempool)
            itempool += [self.create_item(Constants.GOLD_FILLER_ITEM_NAME) for i in range(1, filler_slots)] # Less one (range start at 1) because of locked victory item
        else: #BonusItemMode Random Dice
            # Add random Dice items from the pool to fill in empty locations
            filler_slots: int
            if (self.options.progression.value == Progression.option_free_duel):
                filler_slots = len(free_duel_region.locations) - len(itempool)
            else:
                filler_slots = len(division_1_region.locations) + len(division_2_region.locations) + len(division_3_region.locations) - len(itempool)
            reward_dice: typing.List[Dice] = [dice for dice in all_dice]
            while len(reward_dice) < filler_slots:
                reward_dice += reward_dice
            self.random.shuffle(reward_dice)

            itempool += [self.create_item(dice.name) for dice in reward_dice][:filler_slots - 1] # Less one becuase of locked victory item
        
        self.multiworld.itempool.extend(itempool)

        self.multiworld.regions.append(menu_region)


    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            Constants.GENERATED_WITH_KEY: __version__,
            Constants.DUELIST_UNLOCK_ORDER_KEY: map_duelists_to_ids(self.duelist_unlock_order),
            Constants.GAME_OPTIONS_KEY: self.options.serialize()
        }

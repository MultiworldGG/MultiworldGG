import typing

from BaseClasses import Item, ItemClassification
from .utils import Constants
from .dice import all_dice, name_to_dice
from .duelists import all_duelists, name_to_duelist
from .tournament import name_to_tournament

item_id_to_item_name: typing.Dict[int, str] = {}
# Duelist unlock items as their Duelist ID's + Duelist unlock offset
for duelist in all_duelists:
    item_id_to_item_name[Constants.DUELIST_UNLOCK_OFFSET + duelist.id] = duelist.name
# Dice items as their Dice ID + Dice offset
for dice in all_dice:
    item_id_to_item_name[Constants.DICE_COLLECTION_OFFSET + dice.id] = dice.name

# Name the victory item
item_id_to_item_name[Constants.VICTORY_ITEM_ID] = Constants.VICTORY_ITEM_NAME

# Gold and Shop Progression
item_id_to_item_name[Constants.GOLD_FILLER_ITEM_ID] = Constants.GOLD_FILLER_ITEM_NAME
item_id_to_item_name[Constants.SHOP_PROGRESSION_ITEM_ID] = Constants.SHOP_PROGRESSION_ITEM_NAME

# Tournament Division 2 and 3 unlock items, as Division 1 and 2 offsets
item_id_to_item_name[Constants.DIVISION_1_COMPLETION_OFFSET_ID] = Constants.DIVISION_2_ITEM_NAME
item_id_to_item_name[Constants.DIVISION_2_COMPLETION_OFFSET_ID] = Constants.DIVISION_3_ITEM_NAME

# Tournament Victory item, as Division 3 offset
item_id_to_item_name[Constants.VICTORY_ITEM_TOURNAMENT_ID] = Constants.VICTORY_ITEM_TOURNAMENT_NAME

item_name_to_item_id: typing.Dict[str, int] = {value: key for key, value in item_id_to_item_name.items()}

class YGODDMItem(Item):
    game: str = Constants.GAME_NAME

def create_item(name: str, player_id: int) -> YGODDMItem:
    return YGODDMItem(name, ItemClassification.progression if (name in name_to_duelist) or (name in [Constants.DIVISION_2_ITEM_NAME, Constants.DIVISION_3_ITEM_NAME] or (name is Constants.SHOP_PROGRESSION_ITEM_NAME) or (name in name_to_dice))
                      else ItemClassification.filler, item_name_to_item_id[name], player_id)

def create_victory_event(player_id: int) -> YGODDMItem:
    return YGODDMItem(Constants.VICTORY_ITEM_NAME, ItemClassification.progression, Constants.VICTORY_ITEM_ID, player_id)

def create_victory_event_tournament(player_id: int) -> YGODDMItem:
    return YGODDMItem(Constants.VICTORY_ITEM_TOURNAMENT_NAME, ItemClassification.progression, Constants.VICTORY_ITEM_TOURNAMENT_ID, player_id)

def is_dice_item(item_id: int) -> bool:
    return item_id >= Constants.DICE_COLLECTION_OFFSET and item_id <= Constants.DICE_COLLECTION_OFFSET + 200

def convert_item_id_to_dice_id(item_id: int) -> int:
    return item_id - Constants.DICE_COLLECTION_OFFSET
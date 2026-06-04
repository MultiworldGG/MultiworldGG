from typing import Dict, NamedTuple, List, TYPE_CHECKING
from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import ChainedEchoesWorld


class ChainedEchoesItem(NamedTuple):
    id: int
    item_name: str  # Name of the item
    game_id: str  # Unique ID for the item (used internally in the game)
    count: int  # Total count of this item
    item_type: str  # Type of the item (e.g., KeyItem, CharacterSkill, etc.)
    classification: ItemClassification  # Progression, Useful, Filler, Trap


# Item data will be parsed from a text file
item_data_table: List[ChainedEchoesItem] = []

# Example text data for items
items_txt = '''
// Item User Friendly Name,ID,Count,Type,Classification
// KEY ITEMS
Key Card A,Key Card A,1,Item,Progression
Key Card B,Key Card B,1,Item,Progression
Key Card C,Key Card C,1,Item,Progression
Key Card D,Key Card D,1,Item,Progression
Miner's Key,Miner's Key,1,Item,Progression
Norgant's Key,Norgant's Key,1,KeyItemItem,Progression
Manor Key,Manor Key,1,Item,Progression
Charon's Coin Bag,Charon's Coin Bag,1,Item,Progression
Elevator Key,Elevator Key,1,Item,Progression
Church Key,Church Key,1,Item,Progression
Silver Key,Silver Key,1,Item,Progression
Gold Key,Gold Key,1,Item,Progression
Water Handle,Water Handle,1,Item,Progression
// END KEY ITEMS
// GLENN PROGRESSIVES
Glenn Skill #1,GlennSkill,1,CharacterSkill,Progression
Glenn Skill #2,GlennSkill,1,CharacterSkill,Progression
Glenn Skill #3,GlennSkill,1,CharacterSkill,Progression
Glenn Skill #4,GlennSkill,1,CharacterSkill,Progression
Glenn Skill #5,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #6,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #7,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #8,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #9,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #10,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #11,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #12,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #13,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #14,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #15,GlennSkill,1,CharacterSkill,Useful
Glenn Skill #16,GlennSkill,1,CharacterSkill,Useful
Glenn Passive #1,GlennPassive,1,CharacterPassive,Progression
Glenn Passive #2,GlennPassive,1,CharacterPassive,Progression
Glenn Passive #3,GlennPassive,1,CharacterPassive,Progression
Glenn Passive #4,GlennPassive,1,CharacterPassive,Progression
Glenn Passive #5,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #6,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #7,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #8,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #9,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #10,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #11,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #12,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #13,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #14,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #15,GlennPassive,1,CharacterPassive,Useful
Glenn Passive #16,GlennPassive,1,CharacterPassive,Useful
Glenn Boost #1,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #2,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #3,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #4,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #5,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #6,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #7,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #8,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #9,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #10,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #11,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #12,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #13,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #14,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #15,GlennStatBoost,1,CharacterStatBoost,Progression
Glenn Boost #16,GlennStatBoost,1,CharacterStatBoost,Progression
// SIENNA PROGRESSIVES
Sienna Skill #1,SiennaSkill,1,CharacterSkill,Progression
Sienna Skill #2,SiennaSkill,1,CharacterSkill,Progression
Sienna Skill #3,SiennaSkill,1,CharacterSkill,Progression
Sienna Skill #4,SiennaSkill,1,CharacterSkill,Progression
Sienna Skill #5,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #6,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #7,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #8,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #9,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #10,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #11,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #12,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #13,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #14,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #15,SiennaSkill,1,CharacterSkill,Useful
Sienna Skill #16,SiennaSkill,1,CharacterSkill,Useful
Sienna Passive #1,SiennaPassive,1,CharacterPassive,Progression
Sienna Passive #2,SiennaPassive,1,CharacterPassive,Progression
Sienna Passive #3,SiennaPassive,1,CharacterPassive,Progression
Sienna Passive #4,SiennaPassive,1,CharacterPassive,Progression
Sienna Passive #5,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #6,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #7,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #8,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #9,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #10,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #11,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #12,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #13,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #14,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #15,SiennaPassive,1,CharacterPassive,Useful
Sienna Passive #16,SiennaPassive,1,CharacterPassive,Useful
Sienna Boost #1,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #2,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #3,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #4,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #5,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #6,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #7,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #8,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #9,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #10,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #11,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #12,SiennaStatBoost,1,CharacterStatBoost,Progression
Sienna Boost #13,SiennaStatBoost,1,CharacterStatBoost,Useful
Sienna Boost #14,SiennaStatBoost,1,CharacterStatBoost,Useful
Sienna Boost #15,SiennaStatBoost,1,CharacterStatBoost,Useful
Sienna Boost #16,SiennaStatBoost,1,CharacterStatBoost,Useful
// AMALIA PROGRESSIVES
Amalia Skill #1,AmaliaSkill,1,CharacterSkill,Progression
Amalia Skill #2,AmaliaSkill,1,CharacterSkill,Progression
Amalia Skill #3,AmaliaSkill,1,CharacterSkill,Progression
Amalia Skill #4,AmaliaSkill,1,CharacterSkill,Progression
Amalia Skill #5,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #6,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #7,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #8,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #9,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #10,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #11,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #12,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #13,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #14,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #15,AmaliaSkill,1,CharacterSkill,Useful
Amalia Skill #16,AmaliaSkill,1,CharacterSkill,Useful
Amalia Passive #1,AmaliaPassive,1,CharacterPassive,Progression
Amalia Passive #2,AmaliaPassive,1,CharacterPassive,Progression
Amalia Passive #3,AmaliaPassive,1,CharacterPassive,Progression
Amalia Passive #4,AmaliaPassive,1,CharacterPassive,Progression
Amalia Passive #5,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #6,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #7,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #8,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #9,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #10,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #11,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #12,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #13,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #14,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #15,AmaliaPassive,1,CharacterPassive,Useful
Amalia Passive #16,AmaliaPassive,1,CharacterPassive,Useful
Amalia Boost #1,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #2,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #3,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #4,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #5,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #6,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #7,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #8,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #9,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #10,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #11,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #12,AmaliaStatBoost,1,CharacterStatBoost,Progression
Amalia Boost #13,AmaliaStatBoost,1,CharacterStatBoost,Useful
Amalia Boost #14,AmaliaStatBoost,1,CharacterStatBoost,Useful
Amalia Boost #15,AmaliaStatBoost,1,CharacterStatBoost,Useful
Amalia Boost #16,AmaliaStatBoost,1,CharacterStatBoost,Useful
// BA'THRAZ PROGRESSIVES
Ba'Thraz Skill #1,Ba'ThrazSkill,1,CharacterSkill,Progression
Ba'Thraz Skill #2,Ba'ThrazSkill,1,CharacterSkill,Progression
Ba'Thraz Skill #3,Ba'ThrazSkill,1,CharacterSkill,Progression
Ba'Thraz Skill #4,Ba'ThrazSkill,1,CharacterSkill,Progression
Ba'Thraz Skill #5,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #6,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #7,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #8,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #9,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #10,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #11,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #12,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #13,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #14,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #15,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Skill #16,Ba'ThrazSkill,1,CharacterSkill,Useful
Ba'Thraz Passive #1,Ba'ThrazPassive,1,CharacterPassive,Progression
Ba'Thraz Passive #2,Ba'ThrazPassive,1,CharacterPassive,Progression
Ba'Thraz Passive #3,Ba'ThrazPassive,1,CharacterPassive,Progression
Ba'Thraz Passive #4,Ba'ThrazPassive,1,CharacterPassive,Progression
Ba'Thraz Passive #5,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #6,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #7,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #8,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #9,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #10,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #11,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #12,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #13,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #14,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #15,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Passive #16,Ba'ThrazPassive,1,CharacterPassive,Useful
Ba'Thraz Boost #1,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #2,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #3,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #4,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #5,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #6,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #7,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #8,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #9,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #10,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #11,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #12,Ba'ThrazStatBoost,1,CharacterStatBoost,Progression
Ba'Thraz Boost #13,Ba'ThrazStatBoost,1,CharacterStatBoost,Useful
Ba'Thraz Boost #14,Ba'ThrazStatBoost,1,CharacterStatBoost,Useful
Ba'Thraz Boost #15,Ba'ThrazStatBoost,1,CharacterStatBoost,Useful
Ba'Thraz Boost #16,Ba'ThrazStatBoost,1,CharacterStatBoost,Useful
// LENNE PROGRESSIVES
Lenne Skill #1,LenneSkill,1,CharacterSkill,Progression
Lenne Skill #2,LenneSkill,1,CharacterSkill,Progression
Lenne Skill #3,LenneSkill,1,CharacterSkill,Progression
Lenne Skill #4,LenneSkill,1,CharacterSkill,Progression
Lenne Skill #5,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #6,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #7,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #8,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #9,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #10,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #11,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #12,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #13,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #14,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #15,LenneSkill,1,CharacterSkill,Useful
Lenne Skill #16,LenneSkill,1,CharacterSkill,Useful
Lenne Passive #1,LennePassive,1,CharacterPassive,Progression
Lenne Passive #2,LennePassive,1,CharacterPassive,Progression
Lenne Passive #3,LennePassive,1,CharacterPassive,Progression
Lenne Passive #4,LennePassive,1,CharacterPassive,Progression
Lenne Passive #5,LennePassive,1,CharacterPassive,Useful
Lenne Passive #6,LennePassive,1,CharacterPassive,Useful
Lenne Passive #7,LennePassive,1,CharacterPassive,Useful
Lenne Passive #8,LennePassive,1,CharacterPassive,Useful
Lenne Passive #9,LennePassive,1,CharacterPassive,Useful
Lenne Passive #10,LennePassive,1,CharacterPassive,Useful
Lenne Passive #11,LennePassive,1,CharacterPassive,Useful
Lenne Passive #12,LennePassive,1,CharacterPassive,Useful
Lenne Passive #13,LennePassive,1,CharacterPassive,Useful
Lenne Passive #14,LennePassive,1,CharacterPassive,Useful
Lenne Passive #15,LennePassive,1,CharacterPassive,Useful
Lenne Passive #16,LennePassive,1,CharacterPassive,Useful
Lenne Boost #1,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #2,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #3,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #4,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #5,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #6,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #7,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #8,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #9,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #10,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #11,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #12,LenneStatBoost,1,CharacterStatBoost,Progression
Lenne Boost #13,LenneStatBoost,1,CharacterStatBoost,Useful
Lenne Boost #14,LenneStatBoost,1,CharacterStatBoost,Useful
Lenne Boost #15,LenneStatBoost,1,CharacterStatBoost,Useful
Lenne Boost #16,LenneStatBoost,1,CharacterStatBoost,Useful
// ROBB PROGRESSIVES
Robb Skill #1,RobbSkill,1,CharacterSkill,Progression
Robb Skill #2,RobbSkill,1,CharacterSkill,Useful
Robb Skill #3,RobbSkill,1,CharacterSkill,Useful
Robb Skill #4,RobbSkill,1,CharacterSkill,Useful
Robb Skill #5,RobbSkill,1,CharacterSkill,Useful
Robb Skill #6,RobbSkill,1,CharacterSkill,Useful
Robb Skill #7,RobbSkill,1,CharacterSkill,Useful
Robb Skill #8,RobbSkill,1,CharacterSkill,Useful
Robb Skill #9,RobbSkill,1,CharacterSkill,Useful
Robb Skill #10,RobbSkill,1,CharacterSkill,Useful
Robb Skill #11,RobbSkill,1,CharacterSkill,Useful
Robb Skill #12,RobbSkill,1,CharacterSkill,Useful
Robb Skill #13,RobbSkill,1,CharacterSkill,Useful
Robb Skill #14,RobbSkill,1,CharacterSkill,Useful
Robb Skill #15,RobbSkill,1,CharacterSkill,Useful
Robb Skill #16,RobbSkill,1,CharacterSkill,Useful
Robb Passive #1,RobbPassive,1,CharacterPassive,Progression
Robb Passive #2,RobbPassive,1,CharacterPassive,Progression
Robb Passive #3,RobbPassive,1,CharacterPassive,Progression
Robb Passive #4,RobbPassive,1,CharacterPassive,Progression
Robb Passive #5,RobbPassive,1,CharacterPassive,Useful
Robb Passive #6,RobbPassive,1,CharacterPassive,Useful
Robb Passive #7,RobbPassive,1,CharacterPassive,Useful
Robb Passive #8,RobbPassive,1,CharacterPassive,Useful
Robb Passive #9,RobbPassive,1,CharacterPassive,Useful
Robb Passive #10,RobbPassive,1,CharacterPassive,Useful
Robb Passive #11,RobbPassive,1,CharacterPassive,Useful
Robb Passive #12,RobbPassive,1,CharacterPassive,Useful
Robb Passive #13,RobbPassive,1,CharacterPassive,Useful
Robb Passive #14,RobbPassive,1,CharacterPassive,Useful
Robb Passive #15,RobbPassive,1,CharacterPassive,Useful
Robb Passive #16,RobbPassive,1,CharacterPassive,Useful
Robb Boost #1,RobbStatBoost,1,CharacterStatBoost,Progression
Robb Boost #2,RobbStatBoost,1,CharacterStatBoost,Progression
Robb Boost #3,RobbStatBoost,1,CharacterStatBoost,Progression
Robb Boost #4,RobbStatBoost,1,CharacterStatBoost,Progression
Robb Boost #5,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #6,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #7,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #8,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #9,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #10,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #11,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #12,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #13,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #14,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #15,RobbStatBoost,1,CharacterStatBoost,Useful
Robb Boost #16,RobbStatBoost,1,CharacterStatBoost,Useful
// VICTOR PROGRESSIVES
Victor Skill #1,VictorSkill,1,CharacterSkill,Progression
Victor Skill #2,VictorSkill,1,CharacterSkill,Useful
Victor Skill #3,VictorSkill,1,CharacterSkill,Useful
Victor Skill #4,VictorSkill,1,CharacterSkill,Useful
Victor Skill #5,VictorSkill,1,CharacterSkill,Useful
Victor Skill #6,VictorSkill,1,CharacterSkill,Useful
Victor Skill #7,VictorSkill,1,CharacterSkill,Useful
Victor Skill #8,VictorSkill,1,CharacterSkill,Useful
Victor Skill #9,VictorSkill,1,CharacterSkill,Useful
Victor Skill #10,VictorSkill,1,CharacterSkill,Useful
Victor Skill #11,VictorSkill,1,CharacterSkill,Useful
Victor Skill #12,VictorSkill,1,CharacterSkill,Useful
Victor Skill #13,VictorSkill,1,CharacterSkill,Useful
Victor Skill #14,VictorSkill,1,CharacterSkill,Useful
Victor Skill #15,VictorSkill,1,CharacterSkill,Useful
Victor Skill #16,VictorSkill,1,CharacterSkill,Useful
Victor Passive #1,VictorPassive,1,CharacterPassive,Useful
Victor Passive #2,VictorPassive,1,CharacterPassive,Useful
Victor Passive #3,VictorPassive,1,CharacterPassive,Useful
Victor Passive #4,VictorPassive,1,CharacterPassive,Useful
Victor Passive #5,VictorPassive,1,CharacterPassive,Useful
Victor Passive #6,VictorPassive,1,CharacterPassive,Useful
Victor Passive #7,VictorPassive,1,CharacterPassive,Useful
Victor Passive #8,VictorPassive,1,CharacterPassive,Useful
Victor Passive #9,VictorPassive,1,CharacterPassive,Useful
Victor Passive #10,VictorPassive,1,CharacterPassive,Useful
Victor Passive #11,VictorPassive,1,CharacterPassive,Useful
Victor Passive #12,VictorPassive,1,CharacterPassive,Useful
Victor Passive #13,VictorPassive,1,CharacterPassive,Useful
Victor Passive #14,VictorPassive,1,CharacterPassive,Useful
Victor Passive #15,VictorPassive,1,CharacterPassive,Useful
Victor Passive #16,VictorPassive,1,CharacterPassive,Useful
Victor Boost #1,VictorStatBoost,1,CharacterStatBoost,Progression
Victor Boost #2,VictorStatBoost,1,CharacterStatBoost,Progression
Victor Boost #3,VictorStatBoost,1,CharacterStatBoost,Progression
Victor Boost #4,VictorStatBoost,1,CharacterStatBoost,Progression
Victor Boost #5,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #6,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #7,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #8,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #9,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #10,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #11,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #12,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #13,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #14,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #15,VictorStatBoost,1,CharacterStatBoost,Useful
Victor Boost #16,VictorStatBoost,1,CharacterStatBoost,Useful
// EGYL PROGRESSIVES
Egyl Skill #1,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #2,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #3,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #4,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #5,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #6,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #7,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #8,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #9,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #10,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #11,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #12,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #13,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #14,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #15,EgylSkill,1,CharacterSkill,Useful
Egyl Skill #16,EgylSkill,1,CharacterSkill,Useful
Egyl Passive #1,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #2,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #3,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #4,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #5,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #6,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #7,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #8,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #9,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #10,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #11,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #12,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #13,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #14,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #15,EgylPassive,1,CharacterPassive,Useful
Egyl Passive #16,EgylPassive,1,CharacterPassive,Useful
Egyl Boost #1,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #2,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #3,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #4,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #5,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #6,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #7,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #8,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #9,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #10,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #11,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #12,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #13,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #14,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #15,EgylStatBoost,1,CharacterStatBoost,Useful
Egyl Boost #16,EgylStatBoost,1,CharacterStatBoost,Useful
// TOMKE PROGRESSIVES
Tomke Skill #1,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #2,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #3,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #4,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #5,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #6,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #7,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #8,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #9,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #10,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #11,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #12,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #13,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #14,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #15,TomkeSkill,1,CharacterSkill,Filler
Tomke Skill #16,TomkeSkill,1,CharacterSkill,Filler
Tomke Passive #1,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #2,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #3,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #4,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #5,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #6,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #7,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #8,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #9,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #10,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #11,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #12,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #13,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #14,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #15,TomkePassive,1,CharacterPassive,Filler
Tomke Passive #16,TomkePassive,1,CharacterPassive,Filler
Tomke Boost #1,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #2,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #3,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #4,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #5,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #6,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #7,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #8,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #9,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #10,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #11,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #12,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #13,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #14,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #15,TomkeStatBoost,1,CharacterStatBoost,Filler
Tomke Boost #16,TomkeStatBoost,1,CharacterStatBoost,Filler
// MIKAH PROGRESSIVES
Mikah Skill #1,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #2,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #3,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #4,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #5,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #6,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #7,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #8,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #9,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #10,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #11,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #12,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #13,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #14,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #15,MikahSkill,1,CharacterSkill,Filler
Mikah Skill #16,MikahSkill,1,CharacterSkill,Filler
Mikah Passive #1,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #2,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #3,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #4,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #5,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #6,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #7,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #8,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #9,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #10,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #11,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #12,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #13,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #14,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #15,MikahPassive,1,CharacterPassive,Filler
Mikah Passive #16,MikahPassive,1,CharacterPassive,Filler
Mikah Boost #1,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #2,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #3,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #4,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #5,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #6,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #7,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #8,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #9,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #10,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #11,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #12,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #13,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #14,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #15,MikahStatBoost,1,CharacterStatBoost,Filler
Mikah Boost #16,MikahStatBoost,1,CharacterStatBoost,Filler
// RAPHAEL PROGRESSIVES
Raphael Skill #1,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #2,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #3,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #4,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #5,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #6,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #7,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #8,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #9,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #10,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #11,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #12,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #13,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #14,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #15,RaphaelSkill,1,CharacterSkill,Filler
Raphael Skill #16,RaphaelSkill,1,CharacterSkill,Filler
Raphael Passive #1,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #2,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #3,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #4,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #5,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #6,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #7,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #8,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #9,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #10,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #11,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #12,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #13,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #14,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #15,RaphaelPassive,1,CharacterPassive,Filler
Raphael Passive #16,RaphaelPassive,1,CharacterPassive,Filler
Raphael Boost #1,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #2,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #3,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #4,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #5,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #6,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #7,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #8,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #9,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #10,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #11,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #12,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #13,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #14,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #15,RaphaelStatBoost,1,CharacterStatBoost,Filler
Raphael Boost #16,RaphaelStatBoost,1,CharacterStatBoost,Filler
// Magnolia PROGRESSIVES
Magnolia Skill #1,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #2,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #3,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #4,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #5,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #6,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #7,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #8,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #9,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #10,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #11,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #12,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #13,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #14,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #15,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Skill #16,MagnoliaSkill,1,CharacterSkill,Filler
Magnolia Passive #1,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #2,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #3,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #4,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #5,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #6,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #7,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #8,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #9,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #10,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #11,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #12,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #13,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #14,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #15,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Passive #16,MagnoliaPassive,1,CharacterPassive,Filler
Magnolia Boost #1,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #2,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #3,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #4,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #5,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #6,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #7,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #8,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #9,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #10,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #11,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #12,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #13,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #14,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #15,MagnoliaStatBoost,1,CharacterStatBoost,Filler
Magnolia Boost #16,MagnoliaStatBoost,1,CharacterStatBoost,Filler
// KYLIAN PROGRESSIVES
Kylian Skill #1,KylianSkill,1,CharacterSkill,Progression
Kylian Skill #2,KylianSkill,1,CharacterSkill,Filler
Kylian Skill #3,KylianSkill,1,CharacterSkill,Filler
Kylian Skill #4,KylianSkill,1,CharacterSkill,Filler
Kylian Skill #5,KylianSkill,1,CharacterSkill,Filler
Kylian Skill #6,KylianSkill,1,CharacterSkill,Filler
Kylian Skill #7,KylianSkill,1,CharacterSkill,Filler
Kylian Skill #8,KylianSkill,1,CharacterSkill,Filler
Kylian Passive #1,KylianPassive,1,CharacterPassive,Filler
Kylian Passive #2,KylianPassive,1,CharacterPassive,Filler
Kylian Passive #3,KylianPassive,1,CharacterPassive,Filler
Kylian Passive #4,KylianPassive,1,CharacterPassive,Filler
Kylian Passive #5,KylianPassive,1,CharacterPassive,Filler
Kylian Passive #6,KylianPassive,1,CharacterPassive,Filler
Kylian Passive #7,KylianPassive,1,CharacterPassive,Filler
Kylian Passive #8,KylianPassive,1,CharacterPassive,Filler
Kylian Boost #1,KylianStatBoost,1,CharacterStatBoost,Filler
Kylian Boost #2,KylianStatBoost,1,CharacterStatBoost,Filler
Kylian Boost #3,KylianStatBoost,1,CharacterStatBoost,Filler
Kylian Boost #4,KylianStatBoost,1,CharacterStatBoost,Filler
Kylian Boost #5,KylianStatBoost,1,CharacterStatBoost,Filler
Kylian Boost #6,KylianStatBoost,1,CharacterStatBoost,Filler
Kylian Boost #7,KylianStatBoost,1,CharacterStatBoost,Filler
Kylian Boost #8,KylianStatBoost,1,CharacterStatBoost,Filler
// WEAPON PROGRESSIVES
Sword #1,Sword,1,Equipment,Useful
Sword #2,Sword,1,Equipment,Useful
Sword #3,Sword,1,Equipment,Useful
Sword #4,Sword,1,Equipment,Useful
Sword #5,Sword,1,Equipment,Useful
Sword #6,Sword,1,Equipment,Useful
Sword #7,Sword,1,Equipment,Useful
Sword #8,Sword,1,Equipment,Useful
Sword #9,Sword,1,Equipment,Useful
Spear #1,Spear,1,Equipment,Useful
Spear #2,Spear,1,Equipment,Useful
Spear #3,Spear,1,Equipment,Useful
Spear #4,Spear,1,Equipment,Useful
Spear #5,Spear,1,Equipment,Useful
Spear #6,Spear,1,Equipment,Useful
Spear #7,Spear,1,Equipment,Useful
Spear #8,Spear,1,Equipment,Useful
Spear #9,Spear,1,Equipment,Useful
Bow #1,Bow,1,Equipment,Useful
Bow #2,Bow,1,Equipment,Useful
Bow #3,Bow,1,Equipment,Useful
Bow #4,Bow,1,Equipment,Useful
Bow #5,Bow,1,Equipment,Useful
Bow #6,Bow,1,Equipment,Useful
Bow #7,Bow,1,Equipment,Useful
Bow #8,Bow,1,Equipment,Useful
Bow #9,Bow,1,Equipment,Useful
Rapier #1,Rapier,1,Equipment,Useful
Rapier #2,Rapier,1,Equipment,Useful
Rapier #3,Rapier,1,Equipment,Useful
Rapier #4,Rapier,1,Equipment,Useful
Rapier #5,Rapier,1,Equipment,Useful
Rapier #6,Rapier,1,Equipment,Useful
Rapier #7,Rapier,1,Equipment,Useful
Rapier #8,Rapier,1,Equipment,Useful
Rapier #9,Rapier,1,Equipment,Useful
Gun #1,Gun,1,Equipment,Useful
Gun #2,Gun,1,Equipment,Useful
Gun #3,Gun,1,Equipment,Useful
Gun #4,Gun,1,Equipment,Useful
Gun #5,Gun,1,Equipment,Useful
Gun #6,Gun,1,Equipment,Useful
Gun #7,Gun,1,Equipment,Useful
Amulet #1,Amulet,1,Equipment,Useful
Amulet #2,Amulet,1,Equipment,Useful
Amulet #3,Amulet,1,Equipment,Useful
Amulet #4,Amulet,1,Equipment,Useful
Amulet #5,Amulet,1,Equipment,Useful
Amulet #6,Amulet,1,Equipment,Useful
Amulet #7,Amulet,1,Equipment,Useful
Amulet #8,Amulet,1,Equipment,Useful
Gunspear #1,Gunspear,1,Equipment,Useful
Gunspear #2,Gunspear,1,Equipment,Useful
Gunspear #3,Gunspear,1,Equipment,Useful
Gunspear #4,Gunspear,1,Equipment,Useful
Katana #1,Katana,1,Equipment,Useful
Katana #2,Katana,1,Equipment,Useful
Katana #3,Katana,1,Equipment,Useful
Katana #4,Katana,1,Equipment,Useful
Katana #5,Katana,1,Equipment,Useful
Katana #6,Katana,1,Equipment,Useful
Katana #7,Katana,1,Equipment,Useful
Katana #8,Katana,1,Equipment,Useful
Katana #9,Katana,1,Equipment,Useful
Greatsword #1,Greatsword,1,Equipment,Useful
Greatsword #2,Greatsword,1,Equipment,Useful
Greatsword #3,Greatsword,1,Equipment,Useful
Greatsword #4,Greatsword,1,Equipment,Useful
Greatsword #5,Greatsword,1,Equipment,Useful
Greatsword #6,Greatsword,1,Equipment,Useful
Anchor #1,Anchor,1,Equipment,Useful
Anchor #2,Anchor,1,Equipment,Useful
Anchor #3,Anchor,1,Equipment,Useful
Anchor #4,Anchor,1,Equipment,Useful
Anchor #5,Anchor,1,Equipment,Useful
Anchor #6,Anchor,1,Equipment,Useful
Anchor #7,Anchor,1,Equipment,Useful
Claw #1,Claw,1,Equipment,Useful
Claw #2,Claw,1,Equipment,Useful
Claw #3,Claw,1,Equipment,Useful
Claw #4,Claw,1,Equipment,Useful
Claw #5,Claw,1,Equipment,Useful
Cards #1,Cards,1,Equipment,Useful
Cards #2,Cards,1,Equipment,Useful
Cards #3,Cards,1,Equipment,Useful
// ARMOR PROGRESSIVES
Light Armor Set 1 #1,Light Armor,1,Equipment,Useful
Light Armor Set 1 #2,Light Armor,1,Equipment,Useful
Light Armor Set 1 #3,Light Armor,1,Equipment,Useful
Light Armor Set 1 #4,Light Armor,1,Equipment,Useful
Light Armor Set 1 #5,Light Armor,1,Equipment,Useful
Light Armor Set 1 #6,Light Armor,1,Equipment,Useful
Light Armor Set 1 #7,Light Armor,1,Equipment,Useful
Light Armor Set 1 #8,Light Armor,1,Equipment,Useful
Heavy Armor Set 1 #1,Heavy Armor,1,Equipment,Useful
Heavy Armor Set 1 #2,Heavy Armor,1,Equipment,Useful
Heavy Armor Set 1 #3,Heavy Armor,1,Equipment,Useful
Heavy Armor Set 1 #4,Heavy Armor,1,Equipment,Useful
Heavy Armor Set 1 #5,Heavy Armor,1,Equipment,Useful
Heavy Armor Set 1 #6,Heavy Armor,1,Equipment,Useful
Heavy Armor Set 1 #7,Heavy Armor,1,Equipment,Useful
Heavy Armor Set 1 #8,Heavy Armor,1,Equipment,Useful
Clothes Set 1 #1,Clothes,1,Equipment,Useful
Clothes Set 1 #2,Clothes,1,Equipment,Useful
Clothes Set 1 #3,Clothes,1,Equipment,Useful
Clothes Set 1 #4,Clothes,1,Equipment,Useful
Clothes Set 1 #5,Clothes,1,Equipment,Useful
Clothes Set 1 #6,Clothes,1,Equipment,Useful
Clothes Set 1 #7,Clothes,1,Equipment,Useful
Clothes Set 1 #8,Clothes,1,Equipment,Useful
Robe Set 1 #1,Robe,1,Equipment,Useful
Robe Set 1 #2,Robe,1,Equipment,Useful
Robe Set 1 #3,Robe,1,Equipment,Useful
Robe Set 1 #4,Robe,1,Equipment,Useful
Robe Set 1 #5,Robe,1,Equipment,Useful
Robe Set 1 #6,Robe,1,Equipment,Useful
Robe Set 1 #7,Robe,1,Equipment,Useful
Robe Set 1 #8,Robe,1,Equipment,Useful
Light Armor Set 2 #1,Light Armor,1,Equipment,Filler
Light Armor Set 2 #2,Light Armor,1,Equipment,Filler
Light Armor Set 2 #3,Light Armor,1,Equipment,Filler
Light Armor Set 2 #4,Light Armor,1,Equipment,Filler
Light Armor Set 2 #5,Light Armor,1,Equipment,Filler
Light Armor Set 2 #6,Light Armor,1,Equipment,Filler
Light Armor Set 2 #7,Light Armor,1,Equipment,Filler
Light Armor Set 2 #8,Light Armor,1,Equipment,Filler
Heavy Armor Set 2 #1,Heavy Armor,1,Equipment,Filler
Heavy Armor Set 2 #2,Heavy Armor,1,Equipment,Filler
Heavy Armor Set 2 #3,Heavy Armor,1,Equipment,Filler
Heavy Armor Set 2 #4,Heavy Armor,1,Equipment,Filler
Heavy Armor Set 2 #5,Heavy Armor,1,Equipment,Filler
Heavy Armor Set 2 #6,Heavy Armor,1,Equipment,Filler
Heavy Armor Set 2 #7,Heavy Armor,1,Equipment,Filler
Heavy Armor Set 2 #8,Heavy Armor,1,Equipment,Filler
Clothes Set 2 #1,Clothes,1,Equipment,Filler
Clothes Set 2 #2,Clothes,1,Equipment,Filler
Clothes Set 2 #3,Clothes,1,Equipment,Filler
Clothes Set 2 #4,Clothes,1,Equipment,Filler
Clothes Set 2 #5,Clothes,1,Equipment,Filler
Clothes Set 2 #6,Clothes,1,Equipment,Filler
Clothes Set 2 #7,Clothes,1,Equipment,Filler
Clothes Set 2 #8,Clothes,1,Equipment,Filler
Robe Set 2 #1,Robe,1,Equipment,Filler
Robe Set 2 #2,Robe,1,Equipment,Filler
Robe Set 2 #3,Robe,1,Equipment,Filler
Robe Set 2 #4,Robe,1,Equipment,Filler
Robe Set 2 #5,Robe,1,Equipment,Filler
Robe Set 2 #6,Robe,1,Equipment,Filler
Robe Set 2 #7,Robe,1,Equipment,Filler
Robe Set 2 #8,Robe,1,Equipment,Filler
// MECH PROGRESSIVES
Merlin #1,Merlin,1,MechEquipment,Useful
Merlin #2,Merlin,1,MechEquipment,Useful
Merlin #3,Merlin,1,MechEquipment,Useful
Merlin #4,Merlin,1,MechEquipment,Useful
Merlin #5,Merlin,1,MechEquipment,Useful
Kerberos #1,Kerberos,1,MechEquipment,Useful
Kerberos #2,Kerberos,1,MechEquipment,Useful
Kerberos #3,Kerberos,1,MechEquipment,Useful
Kerberos #4,Kerberos,1,MechEquipment,Useful
Kerberos #5,Kerberos,1,MechEquipment,Useful
Agamemnon #1,Agamemnon,1,MechEquipment,Useful
Agamemnon #2,Agamemnon,1,MechEquipment,Useful
Agamemnon #3,Agamemnon,1,MechEquipment,Useful
Agamemnon #4,Agamemnon,1,MechEquipment,Useful
Agamemnon #5,Agamemnon,1,MechEquipment,Useful
Ovelia #1,Ovelia,1,MechEquipment,Useful
Ovelia #2,Ovelia,1,MechEquipment,Useful
Ovelia #3,Ovelia,1,MechEquipment,Useful
Ovelia #4,Ovelia,1,MechEquipment,Useful
Ovelia #5,Ovelia,1,MechEquipment,Useful
Paris #1,Paris,1,MechEquipment,Useful
Paris #2,Paris,1,MechEquipment,Useful
Paris #3,Paris,1,MechEquipment,Useful
Paris #4,Paris,1,MechEquipment,Useful
Paris #5,Paris,1,MechEquipment,Useful
Mech Sword & Shield #1,MechSword,1,MechEquipment,Useful
Mech Sword & Shield #2,MechSword,1,MechEquipment,Useful
Mech Sword & Shield #3,MechSword,1,MechEquipment,Useful
Mech Sword & Shield #4,MechSword,1,MechEquipment,Useful
Mech Sword & Shield #5,MechSword,1,MechEquipment,Useful
Mech Hammer & Shield #1,MechHammer,1,MechEquipment,Useful
Mech Hammer & Shield #2,MechHammer,1,MechEquipment,Useful
Mech Hammer & Shield #3,MechHammer,1,MechEquipment,Useful
Mech Hammer & Shield #4,MechHammer,1,MechEquipment,Useful
Mech Hammer & Shield #5,MechHammer,1,MechEquipment,Useful
Mech Greatsword #1,MechGreatsword,1,MechEquipment,Useful
Mech Greatsword #2,MechGreatsword,1,MechEquipment,Useful
Mech Greatsword #3,MechGreatsword,1,MechEquipment,Useful
Mech Greatsword #4,MechGreatsword,1,MechEquipment,Useful
Mech Greatsword #5,MechGreatsword,1,MechEquipment,Useful
Mech Glaive #1,MechGlaive,1,MechEquipment,Useful
Mech Glaive #2,MechGlaive,1,MechEquipment,Useful
Mech Glaive #3,MechGlaive,1,MechEquipment,Useful
Mech Glaive #4,MechGlaive,1,MechEquipment,Useful
Mech Glaive #5,MechGlaive,1,MechEquipment,Useful
Mech Bowgun #1,MechBowgun,1,MechEquipment,Useful
Mech Bowgun #2,MechBowgun,1,MechEquipment,Useful
Mech Bowgun #3,MechBowgun,1,MechEquipment,Useful
Mech Bowgun #4,MechBowgun,1,MechEquipment,Useful
Mech Bowgun #5,MechBowgun,1,MechEquipment,Useful
Mech Ether Cannon #1,MechEther,1,MechEquipment,Useful
Mech Ether Cannon #2,MechEther,1,MechEquipment,Useful
Mech Ether Cannon #3,MechEther,1,MechEquipment,Useful
Mech Ether Cannon #4,MechEther,1,MechEquipment,Useful
Mech Ether Cannon #5,MechEther,1,MechEquipment,Useful
Mech Support Drones #1,MechSupport,1,MechEquipment,Useful
Mech Support Drones #2,MechSupport,1,MechEquipment,Useful
Mech Support Drones #3,MechSupport,1,MechEquipment,Useful
Mech Support Drones #4,MechSupport,1,MechEquipment,Useful
Mech Support Drones #5,MechSupport,1,MechEquipment,Useful
Mech Elemental Cannon #1,MechElemental,1,MechEquipment,Useful
Mech Elemental Cannon #2,MechElemental,1,MechEquipment,Useful
Mech Elemental Cannon #3,MechElemental,1,MechEquipment,Useful
Mech Elemental Cannon #4,MechElemental,1,MechEquipment,Useful
Mech Elemental Cannon #5,MechElemental,1,MechEquipment,Useful
Mech Offensive Drones #1,MechOffensive,1,MechEquipment,Useful
Mech Offensive Drones #2,MechOffensive,1,MechEquipment,Useful
Mech Offensive Drones #3,MechOffensive,1,MechEquipment,Useful
Mech Offensive Drones #4,MechOffensive,1,MechEquipment,Useful
Mech Offensive Drones #5,MechOffensive,1,MechEquipment,Useful
// EMBLEMS
Emblem Gambler,EmblemGambler,1,ClassEmblem,Progression
Emblem Summoner,EmblemSummoner,1,ClassEmblem,Progression
Emblem Cleric,EmblemCleric,1,ClassEmblem,Progression
Emblem Monk,EmblemMonk,1,ClassEmblem,Progression
Emblem Bandit,EmblemBandit,1,ClassEmblem,Progression
Emblem Mage Warrior,EmblemMageWarrior,1,ClassEmblem,Progression
Emblem Vampire,EmblemVampire,1,ClassEmblem,Progression
Emblem Warrior,EmblemWarrior,1,ClassEmblem,Progression
Emblem Rune Knight,EmblemRuneKnight,1,ClassEmblem,Progression
Emblem Shaman,EmblemShaman,1,ClassEmblem,Progression
Emblem Pyromancer,EmblemPyromancer,1,ClassEmblem,Progression
Emblem Chemist,EmblemChemist,1,ClassEmblem,Progression
// ACCESSORIES
Medallion,Medallion,1,Equipment,Filler
Swift Sandals,Swift Sandals,1,Equipment,Filler
Life Thread,Life Thread,1,Equipment,Filler
Titan Helm,Titan Helm,1,Equipment,Filler
Herbal Collar,Herbal Collar,1,Equipment,Filler
Silph Armlet,Silph Armlet,1,Equipment,Filler
Black Tippet,Black Tippet,1,Equipment,Filler
Charm of the Learner,Charm of the Learner,1,Equipment,Filler
Comfy Scarf,Comfy Scarf,1,Equipment,Filler
Lava Gorget,Lava Gorget,1,Equipment,Filler
Raincoat,Raincoat,1,Equipment,Filler
Glasses,Glasses,1,Equipment,Filler
Gauntlets,Gauntlets,1,Equipment,Filler
Bangle,Bangle,1,Equipment,Filler
Mystic Ring,Mystic Ring,1,Equipment,Filler
Heavenly Ring,Heavenly Ring,1,Equipment,Filler
Winged Cape,Winged Cape,1,Equipment,Filler
Magician’s Belt,Magician’s Belt,1,Equipment,Filler
Iron Poleyns,Iron Poleyns,1,Equipment,Filler
Festival Ribbon,Festival Ribbon,1,Equipment,Filler
Sunglasses,Sunglasses,1,Equipment,Filler
Attack Gorget,Attack Gorget,1,Equipment,Filler
Defense Gorget,Defense Gorget,1,Equipment,Filler
Pacifist’s Charm,Pacifist’s Charm,1,Equipment,Filler
Can Machine,Can Machine,1,Equipment,Filler
Cool Scarf,Cool Scarf,1,Equipment,Filler
Stylish Accessory,Stylish Accessory,1,Equipment,Filler
Thunder Clap,Thunder Clap,1,Equipment,Filler
Rubber Duck,Rubber Duck,1,Equipment,Filler
Reaction Armlet,Reaction Armlet,1,Equipment,Filler
Blueprint,Blueprint,1,Equipment,Filler
Knight’s Honor,Knight’s Honor,1,Equipment,Filler
Herbalist’s Advise,Herbalist’s Advise,1,Equipment,Filler
Queen of Slots,Queen of Slots,1,Equipment,Filler
Berserker’s Will,Berserker’s Will,1,Equipment,Filler
Rare Grimoire,Rare Grimoire,1,Equipment,Filler
Ultima Shield,Ultima Shield,1,Equipment,Filler
Rabbit’s Charm,Rabbit’s Charm,1,Equipment,Filler
Pondering Orb,Pondering Orb,1,Equipment,Filler
Healing Belt,Healing Belt,1,Equipment,Filler
Thief’s Gloves,Thief’s Gloves,1,Equipment,Filler
Shadow Garb,Shadow Garb,1,Equipment,Filler
Opal Ring,Opal Ring,1,Equipment,Filler
Magic Poleyns,Magic Poleyns,1,Equipment,Filler
Leaf Hood,Leaf Hood,1,Equipment,Filler
Friendship Ring,Friendship Ring,1,Equipment,Filler
Holy Symbol,Holy Symbol,1,Equipment,Filler
Dancing Shoes,Dancing Shoes,1,Equipment,Filler
Adrenalin Stone,Adrenalin Stone,1,Equipment,Filler
Flask of Power,Flask of Power,1,Equipment,Filler
Fire Belt,Fire Belt,1,Equipment,Filler
Water Belt,Water Belt,1,Equipment,Filler
Earth Belt,Earth Belt,1,Equipment,Filler
Wind Belt,Wind Belt,1,Equipment,Filler
Dark Belt,Dark Belt,1,Equipment,Filler
Light Belt,Light Belt,1,Equipment,Filler
Bracelet of Power,Bracelet of Power,1,Equipment,Filler
Bracelet of Magic,Bracelet of Magic,1,Equipment,Filler
Bracelet of Defense,Bracelet of Defense,1,Equipment,Filler
Bracelet of Wisdom,Bracelet of Wisdom,1,Equipment,Filler
Chicken Feet,Chicken Feet,1,Equipment,Filler
// EXTRA FILLER ITEMS
Meal #1,Meal,1,Item,Filler
Meal #2,Meal,1,Item,Filler
Meal #3,Meal,1,Item,Filler
Meal #4,Meal,1,Item,Filler
Meal #5,Meal,1,Item,Filler
Meal #6,Meal,1,Item,Filler
Meal #7,Meal,1,Item,Filler
Meal #8,Meal,1,Item,Filler
Meal #9,Meal,1,Item,Filler
Meal #10,Meal,1,Item,Filler
Ambrosia #1,Ambrosia,1,Item,Filler
Ambrosia #2,Ambrosia,1,Item,Filler
Ambrosia #3,Ambrosia,1,Item,Filler
Ambrosia #4,Ambrosia,1,Item,Filler
Ambrosia #5,Ambrosia,1,Item,Filler
Ambrosia #6,Ambrosia,1,Item,Filler
Ambrosia #7,Ambrosia,1,Item,Filler
Ambrosia #8,Ambrosia,1,Item,Filler
Ambrosia #9,Ambrosia,1,Item,Filler
Ambrosia #10,Ambrosia,1,Item,Filler
Nectar #1,Nectar,1,Item,Filler
Nectar #2,Nectar,1,Item,Filler
Nectar #3,Nectar,1,Item,Filler
Nectar #4,Nectar,1,Item,Filler
Nectar #5,Nectar,1,Item,Filler
Nectar #6,Nectar,1,Item,Filler
Nectar #7,Nectar,1,Item,Filler
Nectar #8,Nectar,1,Item,Filler
Nectar #9,Nectar,1,Item,Filler
Nectar #10,Nectar,1,Item,Filler
Elixir #1,Elixir,1,Item,Filler
Elixir #2,Elixir,1,Item,Filler
Elixir #3,Elixir,1,Item,Filler
Elixir #4,Elixir,1,Item,Filler
Elixir #5,Elixir,1,Item,Filler
Elixir #6,Elixir,1,Item,Filler
Elixir #7,Elixir,1,Item,Filler
Elixir #8,Elixir,1,Item,Filler
Elixir #9,Elixir,1,Item,Filler
Elixir #10,Elixir,1,Item,Filler
Attack Overdrive #1,Attack Overdrive,1,Item,Filler
Attack Overdrive #2,Attack Overdrive,1,Item,Filler
Attack Overdrive #3,Attack Overdrive,1,Item,Filler
Buff Overdrive #1,Buff Overdrive,1,Item,Filler
Buff Overdrive #2,Buff Overdrive,1,Item,Filler
Buff Overdrive #3,Buff Overdrive,1,Item,Filler
Heal Overdrive #1,Heal Overdrive,1,Item,Filler
Heal Overdrive #2,Heal Overdrive,1,Item,Filler
Heal Overdrive #3,Heal Overdrive,1,Item,Filler
Debuff Overdrive #1,Debuff Overdrive,1,Item,Filler
Debuff Overdrive #2,Debuff Overdrive,1,Item,Filler
Debuff Overdrive #3,Debuff Overdrive,1,Item,Filler
Utility Overdrive #1,Utility Overdrive,1,Item,Filler
Utility Overdrive #2,Utility Overdrive,1,Item,Filler
Utility Overdrive #3,Utility Overdrive,1,Item,Filler
Magic Overdrive #1,Magic Overdrive,1,Item,Filler
Magic Overdrive #2,Magic Overdrive,1,Item,Filler
Magic Overdrive #3,Magic Overdrive,1,Item,Filler
Repair Kit DX #1,Repair Kit DX,1,Item,Filler
Repair Kit DX #2,Repair Kit DX,1,Item,Filler
Repair Kit DX #3,Repair Kit DX,1,Item,Filler
Repair Kit DX #4,Repair Kit DX,1,Item,Filler
Repair Kit DX #5,Repair Kit DX,1,Item,Filler
Exchange Parts #1,Exchange Parts,1,Item,Filler
Exchange Parts #2,Exchange Parts,1,Item,Filler
Exchange Parts #3,Exchange Parts,1,Item,Filler
Exchange Parts #4,Exchange Parts,1,Item,Filler
Exchange Parts #5,Exchange Parts,1,Item,Filler
Crap #1,Crap,1,Item,Trap
Crap #2,Crap,1,Item,Trap
Crap #3,Crap,1,Item,Trap
Crap #4,Crap,1,Item,Trap
Crap #5,Crap,1,Item,Trap
'''

# Map string classifications to `ItemClassification`
classification_map = {
    "Progression": ItemClassification.progression,
    "Useful": ItemClassification.useful,
    "Filler": ItemClassification.filler,
    "Trap": ItemClassification.trap,
}

# Parse the item data from the text
ITEM_ID_START = 8500000
current_id = ITEM_ID_START
for line in items_txt.strip().splitlines():
    if line.startswith("//"):  # Skip comments
        continue
    parts = line.split(",")
    if len(parts) < 5:
        print(f"Malformed line: {line}")  # Debugging output
        continue

    item_data_table.append(ChainedEchoesItem(
        id=current_id,
        item_name=parts[0].strip(),
        game_id=parts[1].strip(),
        count=int(parts[2].strip()),
        item_type=parts[3].strip(),
            classification=classification_map[parts[4].strip()],
    ))
    current_id += 1


item_data_by_name: Dict[str, ChainedEchoesItem] = {item.item_name: item for item in item_data_table}
item_table: Dict[str, int] = {item.item_name: item.id for item in item_data_table}


def create_items(world: "ChainedEchoesWorld"):
    """
    Create the full deterministic item pool during world setup.

    Universal Tracker and AP generation both rely on create_items() being the
    single place where the item pool is populated.  Use the world's create_item()
    factory so any future item metadata logic remains centralized.
    """
    for item in item_data_table:
        for _ in range(item.count):
            world.multiworld.itempool.append(world.create_item(item.item_name))

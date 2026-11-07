# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


import typing

from .types.regions import Goal, RegionConnection, RegionsData
from .types.condition import *

modes = [
    'open',
]

default_mode = "open"

region_packs: typing.Dict[str, RegionsData] = {
    "open": RegionsData(
        starting_region = "harbor",
        excluded_regions = [],
        region_connections = [
            RegionConnection(region_from='harbor', region_to='rise', cond=[ItemCondition(item_name='Green Leaf Shade', amount=1)]),
            RegionConnection(region_from='rise', region_to='trail', cond=None),
            RegionConnection(region_from='trail', region_to='bergen', cond=None),
            RegionConnection(region_from='harbor', region_to='bergen', cond=[ItemCondition(item_name='Green Leaf Shade', amount=1), VariableCondition(name='rhombusHubUnlock')]),
            RegionConnection(region_from='bergen', region_to='mine.1', cond=[ItemCondition(item_name='Mine Pass', amount=1)]),
            RegionConnection(region_from='mine.1', region_to='mine.2', cond=[ItemCondition(item_name='Mine Key', amount=1)]),
            RegionConnection(region_from='mine.2', region_to='mine.3', cond=[ItemCondition(item_name='Mine Key', amount=2)]),
            RegionConnection(region_from='mine.3', region_to='mine.4', cond=[ItemCondition(item_name='Mine Key', amount=3)]),
            RegionConnection(region_from='mine.4', region_to='mine.5', cond=[ItemCondition(item_name='Mine Key', amount=5)]),
            RegionConnection(region_from='mine.4', region_to='mine.6', cond=[ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='mine.6', region_to='mine.7', cond=[ItemCondition(item_name='Mine Key', amount=5)]),
            RegionConnection(region_from='mine.1', region_to='mine.8', cond=[ItemCondition(item_name='Mine Master Key', amount=1)]),
            RegionConnection(region_from='trail', region_to='valley', cond=[ItemCondition(item_name='Green Leaf Shade', amount=1), ItemCondition(item_name='Blue Ice Shade', amount=1)]),
            RegionConnection(region_from='valley', region_to='bakii', cond=None),
            RegionConnection(region_from='harbor', region_to='bakii', cond=[ItemCondition(item_name='Blue Ice Shade', amount=1), VariableCondition(name='rhombusHubUnlock')]),
            RegionConnection(region_from='valley', region_to='fajro.1', cond=[ItemCondition(item_name='Yellow Sand Shade', amount=1)]),
            RegionConnection(region_from='fajro.1', region_to='fajro.2', cond=[ItemCondition(item_name="Faj'ro Key", amount=1), ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='fajro.2', region_to='fajro.3', cond=[ItemCondition(item_name="Faj'ro Key", amount=3)]),
            RegionConnection(region_from='fajro.1', region_to='fajro.5', cond=[ItemCondition(item_name='Cold', amount=1)]),
            RegionConnection(region_from='fajro.5', region_to='fajro.6', cond=[ItemCondition(item_name='White Key', amount=1)]),
            RegionConnection(region_from='fajro.6', region_to='fajro.7', cond=[ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='fajro.6', region_to='fajro.8', cond=[ItemCondition(item_name="Faj'ro Master Key", amount=1)]),
            RegionConnection(region_from='harbor', region_to='harbor.north', cond=[ItemCondition(item_name='Red Flame Shade', amount=1)]),
            RegionConnection(region_from='harbor', region_to='fall', cond=[ItemCondition(item_name='Red Flame Shade', amount=1)]),
            RegionConnection(region_from='harbor', region_to='rhombus', cond=[ItemCondition(item_name='Meteor Shade', amount=1)]),
            RegionConnection(region_from='fall', region_to='garden', cond=[ItemCondition(item_name='Red Flame Shade', amount=1), ItemCondition(item_name='Green Seed Shade', amount=1)]),
            RegionConnection(region_from='harbor', region_to='basin', cond=[ItemCondition(item_name='Green Seed Shade', amount=1), VariableCondition(name='rhombusHubUnlock')]),
            RegionConnection(region_from='garden', region_to='basin', cond=None),
            RegionConnection(region_from='basin', region_to='basin.slums', cond=[ItemCondition(item_name='Pond Slums Pass', amount=1)]),
            RegionConnection(region_from='garden', region_to='garden.west', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='on', desired=False), AndCondition(subconditions=[ItemCondition(item_name='West Gaia Pass', amount=1), VariableEntryCondition(name='closedGaia', value='on', desired=True)])])]),
            RegionConnection(region_from='garden', region_to='garden.east', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='on', desired=False), AndCondition(subconditions=[ItemCondition(item_name='East Gaia Pass', amount=1), VariableEntryCondition(name='closedGaia', value='on', desired=True)])])]),
            RegionConnection(region_from='garden', region_to='garden.mid', cond=[OrCondition(subconditions=[AndCondition(subconditions=[OrCondition(subconditions=[ItemCondition(item_name='East Gaia Pass', amount=1), ItemCondition(item_name='West Gaia Pass', amount=1)]), VariableEntryCondition(name='closedGaia', value='on', desired=True)]), VariableEntryCondition(name='closedGaia', value='on', desired=False)])]),
            RegionConnection(region_from='garden.west', region_to='garden.grove', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='full', desired=False), AndCondition(subconditions=[ItemCondition(item_name='Azure Drop Shade', amount=1), VariableEntryCondition(name='closedGaia', value='full', desired=True)])])]),
            RegionConnection(region_from='garden.east', region_to='garden.infested', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='full', desired=False), AndCondition(subconditions=[ItemCondition(item_name='Purple Bolt Shade', amount=1), VariableEntryCondition(name='closedGaia', value='full', desired=True)])])]),
            RegionConnection(region_from='garden.east', region_to='zirvitar.1', cond=[ItemCondition(item_name="Zir'vitar Key", amount=2), AnyElementCondition()]),
            RegionConnection(region_from='zirvitar.1', region_to='zirvitar.2', cond=[ItemCondition(item_name='Wave', amount=1)]),
            RegionConnection(region_from='garden.west', region_to='sonajiz.1', cond=[ItemCondition(item_name="So'najiz Key", amount=1), AnyElementCondition()]),
            RegionConnection(region_from='sonajiz.1', region_to='sonajiz.2', cond=[ItemCondition(item_name="So'najiz Key", amount=3)]),
            RegionConnection(region_from='sonajiz.2', region_to='sonajiz.3', cond=[ItemCondition(item_name="So'najiz Key", amount=4), ItemCondition(item_name='Radiant Key', amount=1)]),
            RegionConnection(region_from='sonajiz.3', region_to='sonajiz.4', cond=[ItemCondition(item_name='Shock', amount=1)]),
            RegionConnection(region_from='garden.mid', region_to='kajo.1', cond=[ItemCondition(item_name='Azure Drop Shade', amount=1), ItemCondition(item_name='Purple Bolt Shade', amount=1), ItemCondition(item_name='Wave', amount=1), ItemCondition(item_name='Shock', amount=1)]),
            RegionConnection(region_from='kajo.1', region_to='kajo.2', cond=[ItemCondition(item_name="Krys'kajo Key", amount=2)]),
            RegionConnection(region_from='kajo.1', region_to='kajo.3', cond=[ItemCondition(item_name='Kajo Master Key', amount=1)]),
            RegionConnection(region_from='fall', region_to='ridge', cond=[ItemCondition(item_name='Red Flame Shade', amount=1), ItemCondition(item_name='Star Shade', amount=1)]),
            RegionConnection(region_from='harbor', region_to='ridge', cond=[ItemCondition(item_name='Star Shade', amount=1), VariableCondition(name='rhombusHubUnlock')]),
            RegionConnection(region_from='ridge', region_to='ridge.north', cond=[ItemCondition(item_name='Meteor Shade', amount=1)]),
            RegionConnection(region_from='ridge', region_to='wasteland', cond=[VariableCondition(name='vwPassage')]),
            RegionConnection(region_from='rise', region_to='dlc_homestedt', cond=[ItemCondition(item_name='Guild Pass', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='rhombus', region_to='dlc_archipelago', cond=[ItemCondition(item_name='Azure Archipelago Pass', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='ridge.north', region_to='dlc_kulero.entry', cond=[ItemCondition(item_name='Ancient Shade', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.entry', region_to='dlc_kulero.entry.1F', cond=[ItemCondition(item_name="Ku'lero Key", amount=3), ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.entry', region_to='dlc_kulero.entry.1L', cond=[ItemCondition(item_name="Ku'lero Key", amount=3)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.entry', region_to='dlc_kulero.entry.1R', cond=[OrCondition(subconditions=[AndCondition(subconditions=[ItemCondition(item_name="Ku'lero Key", amount=2), ItemCondition(item_name='Wave', amount=1)]), ItemCondition(item_name="Ku'lero Key", amount=3)])], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.entry', region_to='dlc_kulero.GF_R', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.entry', region_to='dlc_kulero.GF_L', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.GF_R', region_to='dlc_kulero.main', cond=[], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.GF_L', region_to='dlc_kulero.main', cond=[], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.main', region_to='dlc_kulero.B2_R', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Cold', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.B2_R', region_to='dlc_kulero.B2_R.1', cond=[ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.main', region_to='dlc_kulero.B2_L', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Wave', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.B2_L', region_to='dlc_kulero.B2_L.1', cond=[ItemCondition(item_name="Ku'lero Key", amount=3)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.main', region_to='dlc_kulero.B3_L', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.main', region_to='dlc_kulero.B3_R', cond=[ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='dlc_kulero.main', region_to='dlc_kulero.boss', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Wave', amount=1), ItemCondition(item_name="Ku'lero Master Key", amount=1)], metadata={'dlc': True}),
        ],
        goals = {
            'creator': Goal(region='wasteland', condition=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Wave', amount=1), VariableCondition(name='vtShadeLock')]),
            'monkey': Goal(region='kajo.3', condition=None),
            'observatory': Goal(region='rise', condition=[LocationCondition(location_name='The Observatory')]),
            'facility_x': Goal(region='ridge', condition=[ItemCondition(item_name='Encrypted Key', amount=4), RegionCondition(target_mode='open', region_name='trail'), RegionCondition(target_mode='open', region_name='valley'), RegionCondition(target_mode='open', region_name='fall'), RegionCondition(target_mode='open', region_name='garden.east')]),
            'diorbis': Goal(region='dlc_kulero.boss', condition=None),
        }
    ),
    
}

region_botanics_amounts: dict[str, dict[str, int]] = {
    "open": {
        'rise': 6,
        'trail': 13,
        'mine.4': 6,
        'valley': 17,
        'fall': 6,
        'garden': 4,
        'garden.mid': 4,
        'garden.west': 1,
        'garden.east': 3,
        'garden.infested': 3,
        'ridge': 9,
        'bergen': 1,
        'bakii': 1,
        'harbor.north': 1,
        'basin.slums': 1,
        'rhombus': 1,
        'dlc_kulero.entry': 5,
        'dlc_archipelago': 6,
    }
    
}
# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


import typing

from .types.regions import Goal, RegionConnection, RegionsData
from .types.condition import *

modes = [
    'linear',
    'open',
]

default_mode = "open"

region_packs: typing.Dict[str, RegionsData] = {
    "linear": RegionsData(
        starting_region = "2",
        excluded_regions = ['1'],
        region_connections = [
            RegionConnection(region_from='2', region_to='3', cond=[ItemCondition(item_name='Green Leaf Shade', amount=1)]),
            RegionConnection(region_from='3', region_to='4', cond=[ItemCondition(item_name='Mine Pass', amount=1), ItemCondition(item_name='Guild Pass', amount=1)]),
            RegionConnection(region_from='3', region_to='3.1', cond=[ItemCondition(item_name='Mine Pass', amount=1)]),
            RegionConnection(region_from='4', region_to='5', cond=[ItemCondition(item_name='Mine Key', amount=1)]),
            RegionConnection(region_from='5', region_to='6', cond=[ItemCondition(item_name='Mine Key', amount=2)]),
            RegionConnection(region_from='6', region_to='7', cond=[ItemCondition(item_name='Mine Key', amount=3)]),
            RegionConnection(region_from='7', region_to='8', cond=[ItemCondition(item_name='Mine Key', amount=4)]),
            RegionConnection(region_from='7', region_to='9', cond=[ItemCondition(item_name="Thief's Key", amount=1), ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='9', region_to='10', cond=[ItemCondition(item_name='Mine Key', amount=5)]),
            RegionConnection(region_from='10', region_to='11', cond=[ItemCondition(item_name='Mine Master Key', amount=1), ItemCondition(item_name='Blue Ice Shade', amount=1)]),
            RegionConnection(region_from='11', region_to='12', cond=[ItemCondition(item_name='Maroon Cave Pass', amount=1)]),
            RegionConnection(region_from='12', region_to='13', cond=[ItemCondition(item_name='Yellow Sand Shade', amount=1), ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='13', region_to='14', cond=[ItemCondition(item_name="Faj'ro Key", amount=1)]),
            RegionConnection(region_from='14', region_to='15', cond=[ItemCondition(item_name="Faj'ro Key", amount=3)]),
            RegionConnection(region_from='15', region_to='16', cond=[ItemCondition(item_name="Faj'ro Key", amount=4)]),
            RegionConnection(region_from='16', region_to='17', cond=[ItemCondition(item_name='Cold', amount=1)]),
            RegionConnection(region_from='17', region_to='17.5', cond=[ItemCondition(item_name='White Key', amount=1)]),
            RegionConnection(region_from='17.5', region_to='18', cond=[ItemCondition(item_name="Faj'ro Key", amount=9)]),
            RegionConnection(region_from='17.5', region_to='19', cond=[ItemCondition(item_name="Faj'ro Master Key", amount=1)]),
            RegionConnection(region_from='19', region_to='20', cond=[ItemCondition(item_name='Red Flame Shade', amount=1)]),
            RegionConnection(region_from='20', region_to='21', cond=[ItemCondition(item_name='Green Seed Shade', amount=1)]),
            RegionConnection(region_from='21', region_to='23', cond=[]),
            RegionConnection(region_from='21', region_to='24', cond=[ItemCondition(item_name='Pond Slums Pass', amount=1)]),
            RegionConnection(region_from='23', region_to='25', cond=[ItemCondition(item_name="Zir'vitar Key", amount=2)]),
            RegionConnection(region_from='23', region_to='26', cond=[ItemCondition(item_name="So'najiz Key", amount=1)]),
            RegionConnection(region_from='26', region_to='26.5', cond=[ItemCondition(item_name="So'najiz Key", amount=3)]),
            RegionConnection(region_from='26', region_to='27', cond=[ItemCondition(item_name='Radiant Key', amount=1), ItemCondition(item_name="So'najiz Key", amount=4), ItemCondition(item_name='Shock', amount=1)]),
            RegionConnection(region_from='23', region_to='28', cond=[ItemCondition(item_name='Azure Drop Shade', amount=1), ItemCondition(item_name='Purple Bolt Shade', amount=1), ItemCondition(item_name='Wave', amount=1), ItemCondition(item_name='Shock', amount=1)]),
            RegionConnection(region_from='28', region_to='29', cond=[ItemCondition(item_name="Krys'kajo Key", amount=2)]),
            RegionConnection(region_from='28', region_to='30', cond=[ItemCondition(item_name='Kajo Master Key', amount=1)]),
            RegionConnection(region_from='30', region_to='31', cond=[ItemCondition(item_name='Star Shade', amount=1)]),
            RegionConnection(region_from='31', region_to='32', cond=[ItemCondition(item_name='Old Dojo Key', amount=1)]),
            RegionConnection(region_from='32', region_to='33', cond=[ItemCondition(item_name='Meteor Shade', amount=1)]),
            RegionConnection(region_from='31', region_to='22', cond=None),
        ],
        goals = {
            'creator': Goal(region='32', condition=None),
        }
    ),
    "open": RegionsData(
        starting_region = "open2",
        excluded_regions = ['open1'],
        region_connections = [
            RegionConnection(region_from='open2', region_to='open3', cond=[ItemCondition(item_name='Green Leaf Shade', amount=1)]),
            RegionConnection(region_from='open3', region_to='open4.1', cond=[ItemCondition(item_name='Mine Pass', amount=1)]),
            RegionConnection(region_from='open3', region_to='open3.1', cond=[ItemCondition(item_name='Mine Pass', amount=1)]),
            RegionConnection(region_from='open4.1', region_to='open4.2', cond=[ItemCondition(item_name='Mine Key', amount=1)]),
            RegionConnection(region_from='open4.2', region_to='open4.3', cond=[ItemCondition(item_name='Mine Key', amount=2)]),
            RegionConnection(region_from='open4.3', region_to='open4.4', cond=[ItemCondition(item_name='Mine Key', amount=3)]),
            RegionConnection(region_from='open4.4', region_to='open4.5', cond=[ItemCondition(item_name='Mine Key', amount=5)]),
            RegionConnection(region_from='open4.4', region_to='open4.6', cond=[ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='open4.6', region_to='open4.7', cond=[ItemCondition(item_name='Mine Key', amount=5)]),
            RegionConnection(region_from='open4.1', region_to='open4.8', cond=[ItemCondition(item_name='Mine Master Key', amount=1)]),
            RegionConnection(region_from='open3', region_to='open5', cond=[ItemCondition(item_name='Blue Ice Shade', amount=1)]),
            RegionConnection(region_from='open2', region_to='open5', cond=[ItemCondition(item_name='Blue Ice Shade', amount=1), VariableCondition(name='rhombusHubUnlock')]),
            RegionConnection(region_from='open5', region_to='open6', cond=[ItemCondition(item_name='Maroon Cave Pass', amount=1)]),
            RegionConnection(region_from='open5', region_to='open7.1', cond=[ItemCondition(item_name='Yellow Sand Shade', amount=1)]),
            RegionConnection(region_from='open7.1', region_to='open7.2', cond=[ItemCondition(item_name="Faj'ro Key", amount=1), ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='open7.2', region_to='open7.3', cond=[ItemCondition(item_name="Faj'ro Key", amount=3)]),
            RegionConnection(region_from='open7.1', region_to='open7.5', cond=[ItemCondition(item_name='Cold', amount=1)]),
            RegionConnection(region_from='open7.5', region_to='open7.6', cond=[ItemCondition(item_name='White Key', amount=1)]),
            RegionConnection(region_from='open7.6', region_to='open7.7', cond=[ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='open7.6', region_to='open7.8', cond=[ItemCondition(item_name="Faj'ro Master Key", amount=1)]),
            RegionConnection(region_from='open2', region_to='open8', cond=[ItemCondition(item_name='Red Flame Shade', amount=1)]),
            RegionConnection(region_from='open2', region_to='open9', cond=[ItemCondition(item_name='Red Flame Shade', amount=1)]),
            RegionConnection(region_from='open2', region_to='open20', cond=[ItemCondition(item_name='Meteor Shade', amount=1)]),
            RegionConnection(region_from='open9', region_to='open10', cond=[ItemCondition(item_name='Green Seed Shade', amount=1)]),
            RegionConnection(region_from='open2', region_to='open10', cond=[ItemCondition(item_name='Green Seed Shade', amount=1), VariableCondition(name='rhombusHubUnlock')]),
            RegionConnection(region_from='open10', region_to='open11', cond=[ItemCondition(item_name='Pond Slums Pass', amount=1)]),
            RegionConnection(region_from='open10', region_to='open10.Left', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='on', desired=False), AndCondition(subconditions=[ItemCondition(item_name='West Gaia Pass', amount=1), VariableEntryCondition(name='closedGaia', value='on', desired=True)])])]),
            RegionConnection(region_from='open10', region_to='open10.Right', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='on', desired=False), AndCondition(subconditions=[ItemCondition(item_name='East Gaia Pass', amount=1), VariableEntryCondition(name='closedGaia', value='on', desired=True)])])]),
            RegionConnection(region_from='open10', region_to='open10.Mid', cond=[OrCondition(subconditions=[AndCondition(subconditions=[OrCondition(subconditions=[ItemCondition(item_name='East Gaia Pass', amount=1), ItemCondition(item_name='West Gaia Pass', amount=1)]), VariableEntryCondition(name='closedGaia', value='on', desired=True)]), VariableEntryCondition(name='closedGaia', value='on', desired=False)])]),
            RegionConnection(region_from='open10.Left', region_to='open10.Grove', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='full', desired=False), AndCondition(subconditions=[ItemCondition(item_name='Azure Drop Shade', amount=1), VariableEntryCondition(name='closedGaia', value='full', desired=True)])])]),
            RegionConnection(region_from='open10.Right', region_to='open10.Infested', cond=[OrCondition(subconditions=[VariableEntryCondition(name='closedGaia', value='full', desired=False), AndCondition(subconditions=[ItemCondition(item_name='Purple Bolt Shade', amount=1), VariableEntryCondition(name='closedGaia', value='full', desired=True)])])]),
            RegionConnection(region_from='open10.Right', region_to='open13.1', cond=[ItemCondition(item_name="Zir'vitar Key", amount=2), AnyElementCondition()]),
            RegionConnection(region_from='open13.1', region_to='open13.2', cond=[ItemCondition(item_name='Wave', amount=1)]),
            RegionConnection(region_from='open10.Left', region_to='open14.1', cond=[ItemCondition(item_name="So'najiz Key", amount=1), AnyElementCondition()]),
            RegionConnection(region_from='open10.Left', region_to='open14.2', cond=[ItemCondition(item_name="So'najiz Key", amount=3), ItemCondition(item_name='Heat', amount=1)]),
            RegionConnection(region_from='open14.2', region_to='open14.3', cond=[ItemCondition(item_name='Cold', amount=1)]),
            RegionConnection(region_from='open14.3', region_to='open14.4', cond=[ItemCondition(item_name="So'najiz Key", amount=4), ItemCondition(item_name='Radiant Key', amount=1)]),
            RegionConnection(region_from='open14.4', region_to='open14.5', cond=[ItemCondition(item_name='Shock', amount=1)]),
            RegionConnection(region_from='open10.Mid', region_to='open15.1', cond=[ItemCondition(item_name='Azure Drop Shade', amount=1), ItemCondition(item_name='Purple Bolt Shade', amount=1), ItemCondition(item_name='Wave', amount=1), ItemCondition(item_name='Shock', amount=1)]),
            RegionConnection(region_from='open15.1', region_to='open15.2', cond=[ItemCondition(item_name="Krys'kajo Key", amount=2)]),
            RegionConnection(region_from='open15.1', region_to='open15.3', cond=[ItemCondition(item_name='Kajo Master Key', amount=1)]),
            RegionConnection(region_from='open9', region_to='open16', cond=[ItemCondition(item_name='Star Shade', amount=1)]),
            RegionConnection(region_from='open2', region_to='open16', cond=[ItemCondition(item_name='Star Shade', amount=1), VariableCondition(name='rhombusHubUnlock')]),
            RegionConnection(region_from='open16', region_to='open17', cond=[ItemCondition(item_name='Old Dojo Key', amount=1)]),
            RegionConnection(region_from='open16', region_to='open16.1', cond=[ItemCondition(item_name='Meteor Shade', amount=1)]),
            RegionConnection(region_from='open16', region_to='open18', cond=[VariableCondition(name='vwPassage')]),
            RegionConnection(region_from='open3', region_to='openDLC1', cond=[ItemCondition(item_name='Guild Pass', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='open20', region_to='openDLC_Beach', cond=[ItemCondition(item_name='Azure Archipelago Pass', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='open16.1', region_to='openDLC_DungeonEntry', cond=[ItemCondition(item_name='Ancient Shade', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonEntry', region_to='openDLC_DungeonEntry.1F', cond=[ItemCondition(item_name="Ku'lero Key", amount=3), ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonEntry', region_to='openDLC_DungeonEntry.1L', cond=[ItemCondition(item_name="Ku'lero Key", amount=3)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonEntry', region_to='openDLC_DungeonEntry.1R', cond=[OrCondition(subconditions=[AndCondition(subconditions=[ItemCondition(item_name="Ku'lero Key", amount=2), ItemCondition(item_name='Wave', amount=1)]), ItemCondition(item_name="Ku'lero Key", amount=3)])], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonEntry', region_to='openDLC_DungeonGF_R', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonEntry', region_to='openDLC_DungeonGF_L', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonGF_R', region_to='openDLC_DungeonMain', cond=[], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonGF_L', region_to='openDLC_DungeonMain', cond=[], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonMain', region_to='openDLC_DungeonB2_R', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Cold', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonB2_R', region_to='openDLC_DungeonB2_R.1', cond=[ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonMain', region_to='openDLC_DungeonB2_L', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Wave', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonB2_L', region_to='openDLC_DungeonB2_L.1', cond=[ItemCondition(item_name="Ku'lero Key", amount=3)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonMain', region_to='openDLC_DungeonB3_L', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonMain', region_to='openDLC_DungeonB3_R', cond=[ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Wave', amount=1)], metadata={'dlc': True}),
            RegionConnection(region_from='openDLC_DungeonMain', region_to='openDLC_DungeonBoss', cond=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Wave', amount=1), ItemCondition(item_name="Ku'lero Master Key", amount=1)], metadata={'dlc': True}),
        ],
        goals = {
            'creator': Goal(region='open18', condition=[ItemCondition(item_name='Heat', amount=1), ItemCondition(item_name='Cold', amount=1), ItemCondition(item_name='Shock', amount=1), ItemCondition(item_name='Wave', amount=1), VariableCondition(name='vtShadeLock')]),
            'monkey': Goal(region='open15.3', condition=None),
            'observatory': Goal(region='open2', condition=[LocationCondition(location_name='The Observatory')]),
            'diorbis': Goal(region='openDLC_DungeonBoss', condition=None),
        }
    ),
    
}

region_botanics_amounts: dict[str, dict[str, int]] = {
    "open": {
        'open3': 20,
        'open4.4': 6,
        'open5': 18,
        'open8': 7,
        'open10': 4,
        'open10.Mid': 2,
        'open10.Left': 3,
        'open10.Right': 3,
        'open10.Infested': 3,
        'open16': 9,
        'open11': 1,
        'open20': 1,
        'openDLC_DungeonEntry': 5,
        'openDLC_Beach': 6,
    }
    
}
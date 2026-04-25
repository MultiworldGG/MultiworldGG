from test.general.test_client_server_interaction import TestClient
from test.general.test_entrance_rando import (TestEntranceLookup, TestRandomizeEntrances,
                                              TestDisconnectForRandomization, TestBakeTargetGroupLookup)
from test.general.test_entrances import TestBase as TestEntrance
from test.general.test_fill import TestFillRestrictive, TestDistributeItemsRestrictive, TestBalanceMultiworldProgression
from test.general.test_groups import TestNameGroups
from test.general.test_helpers import TestHelpers
from test.general.test_host_yaml import TestIDs, TestSettingsDumper
from test.general.test_ids import TestIDs as TestItemIDs
from test.general.test_implemented import TestImplemented
from test.general.test_items import TestBase as TestItems
from test.general.test_locations import TestBase as TestLocations
from test.general.test_memory import TestWorldMemory
from test.general.test_names import TestNames
from test.general.test_options import TestOptions
from test.general.test_player_options import TestPlayerOptions
from test.general.test_reachability import TestBase as TestReach


class WotWTestClient(TestClient):
    game = "Ori and the Will of the Wisps"


class WotWTestEntranceLookup(TestEntranceLookup):
    game = "Ori and the Will of the Wisps"


class WotWTestRandomizeEntrances(TestRandomizeEntrances):
    game = "Ori and the Will of the Wisps"


class WotWTestDisconnect(TestDisconnectForRandomization):
    game = "Ori and the Will of the Wisps"


class WotWTestGroupLookup(TestBakeTargetGroupLookup):
    game = "Ori and the Will of the Wisps"


class WotWTestEntrance(TestEntrance):
    game = "Ori and the Will of the Wisps"


class WotWTestFill(TestFillRestrictive):
    game = "Ori and the Will of the Wisps"


class WotWTestItems(TestDistributeItemsRestrictive):
    game = "Ori and the Will of the Wisps"


class WotWTestBalance(TestBalanceMultiworldProgression):
    game = "Ori and the Will of the Wisps"


class WotWTestGroup(TestNameGroups):
    game = "Ori and the Will of the Wisps"


class WotWTestHelpers(TestHelpers):
    game = "Ori and the Will of the Wisps"


class WotWTestHostID(TestIDs):
    game = "Ori and the Will of the Wisps"


# class WotWTestHostSave(TestSettingsSave):
#     game = "Ori and the Will of the Wisps"


class WotWTestHostDumper(TestSettingsDumper):
    game = "Ori and the Will of the Wisps"


class WotWTestID(TestItemIDs):
    game = "Ori and the Will of the Wisps"


class WotWTestImpl(TestImplemented):
    game = "Ori and the Will of the Wisps"


class WotWTestItem(TestItems):
    game = "Ori and the Will of the Wisps"


class WotWTestLoc(TestLocations):
    game = "Ori and the Will of the Wisps"


class WotWTestMemory(TestWorldMemory):
    game = "Ori and the Will of the Wisps"


class WotWTestName(TestNames):
    game = "Ori and the Will of the Wisps"


class WotWTestOptions(TestOptions):
    game = "Ori and the Will of the Wisps"


class WotWTestPlayerOptions(TestPlayerOptions):
    game = "Ori and the Will of the Wisps"


class WotWTestReach(TestReach):
    game = "Ori and the Will of the Wisps"

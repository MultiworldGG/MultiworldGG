import unittest

from unittest.mock import patch
from ..client.links.trap_link import TrapLink, TrapLinkType, TrapLinkConstants
from ..client.links.network_engine import ArchipelagoNetworkEngine

class MockNetworkEngine(ArchipelagoNetworkEngine):
    def __init__(self, tags = tuple(["TrapLink"]), player_name = "rando-player"):
        self.tags = list(tags)
        self.player_name = player_name

    def update_tags_async(self, enable_tag: bool, tag_name:str):
        pass

    def get_tags(self):
        return self.tags

    def get_player_name(self, slot: int) -> str:
        return self.player_name

    def get_slot(self) -> int:
        return 0

TRAP_TEST_CASES = {
    TrapLinkType.BANANA: "Banana Trap",
    TrapLinkType.ICE: "Ice Trap",
    TrapLinkType.BOMB: "Bomb",
    TrapLinkType.BONK: "Bonk Trap",
    TrapLinkType.FEAR: "Fear Trap",
    TrapLinkType.GHOST: "Ghost Trap",
    TrapLinkType.NOVAC: "No Vac Trap",
    TrapLinkType.POISON: "Poison Trap",
    TrapLinkType.POSSESSION: "Possession Trap",
    TrapLinkType.SPOOKY: "Spooky Trap"
}

class TestTrapLink(unittest.TestCase):

    @patch("Utils.async_start")
    def test_on_connect_trap_link_disabled_flags(self, mock_async_start):
        """ Verifies that on_connected is able to correctly cast 'disabled_traps' from an int to 'TrapLinkType'. """
        trap_link = TrapLink(MockNetworkEngine())

        args = {
            "slot_data":{
                "trap_link": "TrapLink",
                "disabled_traps": 3,
                "enable_trap_client_msg": True,
            }
        }

        trap_link.on_connected(args)
        self.assertEqual(trap_link.disabled_trap_flags, TrapLinkType(TrapLinkType.POISON.value + TrapLinkType.ICE.value))

    def test_on_bounced_flag_no_traps_triggered(self):
        """ Verifies that when a trap type is on the disabled list it doesn't trigger. """
        net_engine = MockNetworkEngine()
        trap_link = TrapLink(net_engine)

        for trap_type, trap_name in TRAP_TEST_CASES.items():
            with self.subTest(F"test_on_bounced_flag_no_traps_triggered_{trap_name}"):
                args = {
                    "tags": [ "TrapLink" ],
                    "data":{
                        "source": "player-too",
                        "trap_name": trap_name
                    }
                }

                trap_link.disabled_trap_flags |= trap_type
                trap_link.on_bounced(args, 0)
                self.assertFalse(trap_link.received_trap)

    def test_on_bounced_traps_triggered(self):
        """ Verifies that we are able to successfully send a trap via traplink. """
        net_engine = MockNetworkEngine()
        trap_link = TrapLink(net_engine)

        for trap_type, trap_name in TRAP_TEST_CASES.items():
            with self.subTest(F"test_on_bounced_traps_triggered_{trap_name}"):

                args = {
                    "tags": [ "TrapLink" ],
                    "data":{
                        "source": "player-too",
                        "trap_name": trap_name
                    }
                }

                trap_link.on_bounced(args, 0)
                self.assertTrue(trap_link.received_trap)

    def test_on_bounced_traps_all_flags_not_triggered(self):
        """ Verifies that any traplink request is ignored when all disabled flags are present. """
        net_engine = MockNetworkEngine()
        trap_link = TrapLink(net_engine)

        for trap_type, trap_name in TRAP_TEST_CASES.items():
            with self.subTest(F"test_on_bounced_traps_all_disabled_not_triggered_{trap_name}"):

                args = {
                    "tags": [ "TrapLink" ],
                    "data":{
                        "source": "rando-player",
                        "trap_name": trap_name
                    }
                }
                all_disabled_traps: TrapLinkType = TrapLinkType(TrapLinkType.BANANA.value + TrapLinkType.BOMB.value +
                    TrapLinkType.BONK.value + TrapLinkType.FEAR.value + TrapLinkType.GHOST.value +
                    TrapLinkType.ICE.value + TrapLinkType.NOVAC.value + TrapLinkType.POISON.value +
                    TrapLinkType.POSSESSION.value + TrapLinkType.SPOOKY.value + TrapLinkType.SQUASH.value)
                trap_link.disabled_trap_flags |= all_disabled_traps
                trap_link.on_bounced(args, 1)
                self.assertFalse(trap_link.received_trap)

    def test_on_bounced_trap_link_disabled(self):
        """ Verifies when client TrapLink tag is not present we don't send a trap. """
        net_engine = MockNetworkEngine(tags=tuple())
        trap_link = TrapLink(net_engine)

        args = {
            "tags": [ "TrapLink" ],
            "data":{
                "source": "rando-player",
                "trap_name": "Ice Trap"
            }
        }

        trap_link.on_bounced(args, 0)
        self.assertFalse(trap_link.received_trap)

    def test_on_bounced_no_tag_disabled(self):
        """ Verifies when the bounce args doesn't have the TrapLink tag we don't send a trap. """
        net_engine = MockNetworkEngine()
        trap_link = TrapLink(net_engine)

        args = {
            "tags": [ ],
            "data":{
                "source": "player-too",
                "trap_name": "Ice Trap"
            }
        }

        trap_link.on_bounced(args, 0)
        self.assertFalse(trap_link.received_trap)

    def test_on_bounced_same_player_disabled(self):
        """ Verifies when the source is the same as the player's name we don't send a trap. """
        expected_player = "player"
        net_engine = MockNetworkEngine(player_name=expected_player)
        trap_link = TrapLink(net_engine)

        args = {
            "tags": [ "TrapLink" ],
            "data":{
                "source": expected_player,
                "trap_name": "Ice Trap"
            }
        }

        trap_link.on_bounced(args, 0)
        self.assertFalse(trap_link.received_trap)

    def test_on_bounced_enabled_traps_receive_with_disabled_flag(self):
        """ Verifies when a flag is disabling a trap we still send enabled traps. """
        net_engine = MockNetworkEngine()
        trap_link = TrapLink(net_engine)

        for trap_type, trap_name in { k: v for k, v in TRAP_TEST_CASES.items() if k != TrapLinkType.ICE }.items():
            with self.subTest(F"test_on_bounced_traps_all_disabled_not_triggered_{trap_name}"):
                args = {
                    "tags": [ "TrapLink" ],
                    "data":{
                        "source": "player-too",
                        "trap_name": trap_name
                    }
                }

                trap_link.disabled_trap_flags |= TrapLinkType.ICE
                trap_link.on_bounced(args, 0)
                self.assertTrue(trap_link.received_trap)

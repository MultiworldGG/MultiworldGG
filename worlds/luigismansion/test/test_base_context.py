import unittest

from ..client.contexts.base_context import BaseContext, _check_tag
from ..client.links.link_base import LinkBase
from ..client.links.network_engine import ArchipelagoNetworkEngine

class _MockNetworkEngine(ArchipelagoNetworkEngine):
    def __init__(self, tags=tuple(), player_name = "rando-player"):
        self.tags = list(tags)
        self.player_name = player_name

    def update_tags_async(self, enable_tag: bool, tag_name:str):
        if enable_tag:
            self.tags += tag_name

    def get_tags(self):
        return self.tags

    def get_player_name(self, slot: int) -> str:
        return self.player_name

    def get_slot(self) -> int:
        return 0

class _MockLinkBase(LinkBase):
    def on_connected(self, args):
        pass

class MockBaseContext(BaseContext):
    def __init__(self, network_engine: ArchipelagoNetworkEngine):
        self.network_engine = network_engine
        self.trap_link = _MockLinkBase("TrapLink", "trap_link", self.network_engine)
        self.ring_link = _MockLinkBase("RingLink", "ring_link",  self.network_engine)

class TestBaseContext(unittest.TestCase):
    def test_link_enabled_check_tag(self):
        mock_network_engine = _MockNetworkEngine()
        link_base = _MockLinkBase("RingLink", "ring_link", mock_network_engine)
        args = {
            "slot_data": {
                "ring_link": 1
            }
        }

        result: bool = _check_tag(link_base, mock_network_engine, args)
        self.assertTrue(result)

    def test_link_disabled_check_tag(self):
        mock_network_engine = _MockNetworkEngine()
        link_base = _MockLinkBase("RingLink", "ring_link", mock_network_engine)
        args = {
            "slot_data": {
                "ring_link": 0
            }
        }

        result: bool = _check_tag(link_base, mock_network_engine, args)
        self.assertFalse(result)

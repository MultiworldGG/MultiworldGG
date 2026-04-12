import unittest

from ..client.links.ring_link import RingLink, _should_send_rings, _get_difference
from ..client.links.network_engine import ArchipelagoNetworkEngine
from ..client.wallet import Wallet
from ..game.Currency import CURRENCY_NAME

class _MockNetworkEngine(ArchipelagoNetworkEngine):
    def __init__(self, tags = tuple(["RingLink"]), player_name = "rando-player"):
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

class _MockWallet(Wallet):
    _currencies: dict[str, int]
    def __init__(self, currencies: dict[str, int] = { CURRENCY_NAME.COINS: 0 }):
        self._currencies = currencies
    def get_currency_amount(self, currency_name):
        return self._currencies[currency_name]

class TestRingLink(unittest.TestCase):
    def test_should_send_rings_true(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet()

        ring_link = RingLink(mock_network_engine, mock_wallet)

        result: bool = _should_send_rings(ring_link, 100)
        self.assertTrue(result)

    def test_should_send_rings_false_difference_too_high_positive_value(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet()

        ring_link = RingLink(mock_network_engine, mock_wallet)

        result: bool = _should_send_rings(ring_link, 1100)

        self.assertFalse(result)
        self.assertFalse(ring_link.remote_rings_received)
    
    def test_should_send_rings_false_difference_too_high_negatvie_value(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet()

        ring_link = RingLink(mock_network_engine, mock_wallet)

        result: bool = _should_send_rings(ring_link, -1100)

        self.assertFalse(result)
        self.assertFalse(ring_link.remote_rings_received)

    def test_should_send_rings_false_remote_rings_present(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet()

        ring_link = RingLink(mock_network_engine, mock_wallet)
        ring_link.remote_rings_received = True

        result: bool = _should_send_rings(ring_link, 100)

        self.assertFalse(result)
        self.assertFalse(ring_link.remote_rings_received)

    def test_get_difference_zero_on_initalize(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet({ CURRENCY_NAME.COINS: 0})

        ring_link = RingLink(mock_network_engine, mock_wallet)

        difference = _get_difference(ring_link)
        self.assertEqual(difference, 0)

    def test_get_difference_negative_base(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet({ CURRENCY_NAME.COINS: 1 })

        ring_link = RingLink(mock_network_engine, mock_wallet)
        ring_link.previous_coins = -2
        ring_link.initialized = True

        difference = _get_difference(ring_link)
        self.assertEqual(difference, 3)

    def test_get_difference_positive_base(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet({ CURRENCY_NAME.COINS: 98 })

        ring_link = RingLink(mock_network_engine, mock_wallet)
        ring_link.previous_coins = 98
        ring_link.initialized = True

        difference = _get_difference(ring_link)
        self.assertEqual(difference, 0)

    def test_get_difference_zero(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet({ CURRENCY_NAME.COINS: 0 })

        ring_link = RingLink(mock_network_engine, mock_wallet)
        ring_link.previous_coins = 1
        ring_link.initialized = True

        difference = _get_difference(ring_link)
        self.assertEqual(difference, -1)

    def test_get_large_difference(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet({ CURRENCY_NAME.COINS: -30 })

        ring_link = RingLink(mock_network_engine, mock_wallet)
        ring_link.previous_coins = 1
        ring_link.initialized = True

        difference = _get_difference(ring_link)
        self.assertEqual(difference, 0)

    def test_get_positive_difference(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet = _MockWallet({ CURRENCY_NAME.COINS: 100 })

        ring_link = RingLink(mock_network_engine, mock_wallet)
        ring_link.previous_coins = 98
        ring_link.initialized = True

        difference = _get_difference(ring_link)
        self.assertEqual(difference, 2)

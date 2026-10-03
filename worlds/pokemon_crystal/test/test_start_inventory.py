from Options import OptionError

from .bases import PokemonCrystalTestBase
from ..data import data
from ..item_data import START_INVENTORY_ENTRIES


def pocket_items(*pockets):
    return sorted(item.label for item in data.items.values()
                  if item.pocket in pockets and "INVALID" not in item.tags)


# TMs have their own slot each, so these only ever run the table out of room
UNCAPPED_ITEMS = pocket_items("ITEM", "TM_HM")
ITEMS = pocket_items("ITEM")
BALLS = pocket_items("BALL")
TMS = pocket_items("TM_HM")


class StartInventorySizeTest(PokemonCrystalTestBase):
    auto_construct = False

    def generate(self, start_inventory, **options):
        self.options = {"start_inventory": start_inventory, **options}
        self.world_setup(seed=1)

    def assert_rejected(self, start_inventory, *expected, **options) -> str:
        self.options = {"start_inventory": start_inventory, **options}
        with self.assertRaises(OptionError) as ctx:
            self.world_setup(seed=1)
        for text in expected:
            self.assertIn(text, str(ctx.exception))
        return str(ctx.exception)

    def test_full_table_generates(self):
        self.generate({name: 1 for name in UNCAPPED_ITEMS[:START_INVENTORY_ENTRIES]},
                      unlockable_time_of_day=False, randomize_pokedex="vanilla")
        self.assertTrue(self.multiworld.itempool)

    def test_too_many_items_rejected(self):
        self.assert_rejected({name: 1 for name in UNCAPPED_ITEMS[:START_INVENTORY_ENTRIES + 1]},
                             f"room for {START_INVENTORY_ENTRIES} starting stacks", f"needs {START_INVENTORY_ENTRIES + 1}")

    def test_from_pool_counts_towards_limit(self):
        split = START_INVENTORY_ENTRIES // 2
        self.assert_rejected(
            {name: 1 for name in UNCAPPED_ITEMS[:split]},
            f"room for {START_INVENTORY_ENTRIES} starting stacks",
            start_inventory_from_pool={name: 1 for name in UNCAPPED_ITEMS[split:START_INVENTORY_ENTRIES + 1]})

    def test_stacks_fill_the_item_pocket(self):
        # every 99 copies takes another pocket slot, without running the table out of room
        count = data.pocket_sizes["ITEM"] // 2 + 1
        message = self.assert_rejected({name: data.max_item_stack + 1 for name in ITEMS[:count]},
                                       f"Item pocket only holds {data.pocket_sizes['ITEM']} stacks",
                                       f"starts with {count * 2}")
        self.assertNotIn("starting stacks", message, "should not have run the table out of room")

    def test_stacks_fill_the_ball_pocket(self):
        # there are fewer ball items than pocket slots, so it takes more than one stack of each
        stacks = data.pocket_sizes["BALL"] // len(BALLS) + 1
        quantity = (stacks - 1) * data.max_item_stack + 1
        message = self.assert_rejected({name: quantity for name in BALLS},
                                       f"Ball pocket only holds {data.pocket_sizes['BALL']} stacks",
                                       f"starts with {stacks * len(BALLS)}")
        self.assertNotIn("starting stacks", message, "should not have run the table out of room")

    def test_oversized_tm_stack_rejected(self):
        self.assert_rejected({TMS[0]: data.max_item_stack + 1},
                             f"no more than {data.max_item_stack} of a TM or HM", TMS[0])

    def test_start_with_pokedex_counts_towards_limit(self):
        self.assert_rejected({name: 1 for name in UNCAPPED_ITEMS[:START_INVENTORY_ENTRIES]},
                             f"needs {START_INVENTORY_ENTRIES + 1}", randomize_pokedex="start_with")

    def test_precollected_time_of_day_item_counts_towards_limit(self):
        self.assert_rejected({name: 1 for name in UNCAPPED_ITEMS[:START_INVENTORY_ENTRIES]},
                             f"needs {START_INVENTORY_ENTRIES + 1}",
                             time_of_day_encounters=True, unlockable_time_of_day=True)

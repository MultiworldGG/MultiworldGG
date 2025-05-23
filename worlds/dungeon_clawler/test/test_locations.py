from BaseClasses import ItemClassification
from . import DungeonClawlerTestBase
from .. import options
from ..constants.fighters import Fighter, all_fighters
from ..constants.combat_items import CombatItem, all_combat_items
from ..constants.lucky_paws import all_lucky_paws
from ..constants.perks import Perk, all_perk_items
from ..locations import character_location_name


class TestAccessibilityRules(DungeonClawlerTestBase):
    options = {options.Goal.internal_name: options.Goal.option_beat_nightmare,
               options.ShuffleFighters.internal_name: options.ShuffleFighters.option_fighters_and_paws,
               options.ShuffleCombatItems.internal_name: options.ShuffleCombatItems.option_true,
               options.ShufflePerks.internal_name: options.ShufflePerks.option_true,}

    def test_win_with_specific_character(self):
        # Remove the start inventory
        self.multiworld.state.prog_items[self.player].clear()
        for character in all_fighters:
            with self.subTest(character.name):
                location_name = character_location_name(character.name)
                self.assertFalse(self.multiworld.state.can_reach_location(location_name, self.player))

                character_item = self.world.create_item(character.name, ItemClassification.progression)
                self.collect(character_item)

                self.assertFalse(self.multiworld.state.can_reach_location(location_name, self.player))

                paws = [self.world.create_item(paw, ItemClassification.progression) for paw in all_lucky_paws]
                synergy_items = [self.world.create_item(item.name, ItemClassification.progression) for item in all_combat_items if any([synergy_flag in item.flags for synergy_flag in character.good_item_flags])]
                other_items = [self.world.create_item(item.name, ItemClassification.progression) for item in all_combat_items if all([synergy_flag not in item.flags for synergy_flag in character.good_item_flags])]
                synergy_perks = [self.world.create_item(perk.name, ItemClassification.progression) for perk in all_perk_items if any([synergy_flag in perk.flags for synergy_flag in character.good_item_flags])]
                other_perks = [self.world.create_item(perk.name, ItemClassification.progression) for perk in all_perk_items if all([synergy_flag not in perk.flags for synergy_flag in character.good_item_flags])]

                self.collect(paws)
                self.collect(other_items)
                self.collect(other_perks)

                self.assertFalse(self.multiworld.state.can_reach_location(location_name, self.player))

                self.collect(synergy_items)
                self.collect(synergy_perks)

                self.assertTrue(self.multiworld.state.can_reach_location(location_name, self.player))
            self.remove(character_item)
            self.remove(synergy_items)
            self.remove(other_items)
            self.remove(synergy_perks)
            self.remove(other_perks)
            self.remove(paws)
            self.assertFalse(self.multiworld.state.can_reach_location(location_name, self.player))

from .bases import PokemonCrystalTestBase
from ..battle_tower_data import BATTLE_TOWER_TRAINERS, BATTLE_TOWER_TRAINER_OFFSET, BATTLE_TOWER_NUM_TRAINERS, \
    BATTLE_TOWER_TIER_OFFSET, BATTLE_TOWER_NUM_TIERS


class BattleTowerOffTest(PokemonCrystalTestBase):
    options = {
        "battle_tower_sanity": "off",
    }

    def test_no_trainer_locations(self):
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        assert not any(name.startswith("Battle Tower -") for name in names)


class BattleTowerTiersTest(PokemonCrystalTestBase):
    options = {
        "battle_tower_sanity": "tiers",
    }

    def test_tier_locations_only(self):
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        tier_names = {n for n in names if n.startswith("Battle Tower -") and "Tier" in n}
        trainer_names = {n for n in names if n.startswith("Battle Tower -") and "Tier" not in n}
        assert len(tier_names) == BATTLE_TOWER_NUM_TIERS
        assert len(trainer_names) == 0


class BattleTowerTiersAndTrainersTest(PokemonCrystalTestBase):
    options = {
        "battle_tower_sanity": "tiers_and_trainers",
    }

    def test_trainer_locations_present(self):
        locs = [loc for loc in self.multiworld.get_locations(self.player)
                if loc.name.startswith("Battle Tower -") and "Tier" not in loc.name]
        assert len(locs) == BATTLE_TOWER_NUM_TRAINERS
        ids = sorted(loc.address for loc in locs)
        assert ids[0] == BATTLE_TOWER_TRAINER_OFFSET
        assert ids[-1] == BATTLE_TOWER_TRAINER_OFFSET + BATTLE_TOWER_NUM_TRAINERS - 1
        assert len(set(ids)) == BATTLE_TOWER_NUM_TRAINERS

    def test_trainer_names_unique_and_match_curated_list(self):
        locs = {loc.name for loc in self.multiworld.get_locations(self.player)
                if loc.name.startswith("Battle Tower -") and "Tier" not in loc.name}
        expected = {f"Battle Tower - {cls} {name}" for cls, name in BATTLE_TOWER_TRAINERS}
        assert locs == expected

    def test_trainer_locations_distributed_across_tiers(self):
        regions_by_trainer = {}
        for loc in self.multiworld.get_locations(self.player):
            if loc.name.startswith("Battle Tower -") and "Tier" not in loc.name:
                regions_by_trainer[loc.name] = loc.parent_region.name
        assert len(regions_by_trainer) == BATTLE_TOWER_NUM_TRAINERS
        tiers_used = set(regions_by_trainer.values())
        assert tiers_used == {f"Battle Tower Tier {n}" for n in range(1, BATTLE_TOWER_NUM_TIERS + 1)}
        per_tier = {n: 0 for n in range(1, BATTLE_TOWER_NUM_TIERS + 1)}
        for region in regions_by_trainer.values():
            tier = int(region.rsplit(" ", 1)[1])
            per_tier[tier] += 1
        assert all(count == 7 for count in per_tier.values())

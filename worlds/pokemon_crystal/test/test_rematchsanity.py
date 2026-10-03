from .bases import PokemonCrystalTestBase
from ..rematch_trainer_data import (REMATCH_TRAINERS,
                                     all_rematch_locations, rematch_location_name)


class RematchsanityOffTest(PokemonCrystalTestBase):
    options = {"rematchsanity": "false"}

    def test_no_rematch_locations(self):
        labels = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for label, _id, _t, _i in all_rematch_locations():
            self.assertNotIn(label, labels)


class RematchsanityOnTest(PokemonCrystalTestBase):
    options = {
        "rematchsanity": "true",
        # Enable phone-call items so the gift-item chain rules are also exercised.
        "randomize_phone_call_items": "true",
        "randomize_pokegear": True,
        "randomize_pokemon_requests": "items_and_pokemon",
    }

    def test_all_rematch_locations_present(self):
        labels = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for label, _id, _t, _i in all_rematch_locations():
            self.assertIn(label, labels, f"missing rematch location: {label}")

    def test_each_gate_required(self):
        """For every rematch location, removing any gate it should depend on
        from an all-state must make the rule fail. All gates are now uniformly
        world events (VISITED_* events on city regions are events too)."""
        for trainer in REMATCH_TRAINERS.values():
            for i in range(trainer.num_rematches):
                label = rematch_location_name(trainer, i)
                loc = self.multiworld.get_location(label, self.player)
                self.assertTrue(
                    loc.access_rule(self.multiworld.get_all_state(False)),
                    f"{label}: rule should pass in all-state",
                )
                for j in range(i + 1):
                    g = trainer.tier_gates[j]
                    state = self.multiworld.get_all_state(False)
                    state.remove(self.world.create_event(g))
                    self.assertFalse(
                        loc.access_rule(state),
                        f"{label}: removing required gate {g!r} should fail the rule",
                    )

    def test_phone_gift_items_reachable_without_rematch_tiers(self):
        """The 7 non-Joey gift-item trainers announce their item via phone
        when no fresh rematch tier is available. At game start no tier is
        unlocked, so the phone helper returns 'no fresh tier' and the gift
        fires immediately — these locations must not gate on any tier event.
        Joey is excluded: his HP Up is handed over after the JOEY5 in-person
        battle, so his location does gate on the full tier chain."""
        gift_locations = {
            "WADE":    "Route 31 - Berry from Wade",
            "GINA":    "Route 34 - Leaf Stone from Gina",
            "ALAN":    "Route 36 - Fire Stone from Alan",
            "DANA":    "Route 38 - Thunderstone from Dana",
            "TULLY":   "Route 42 - Water Stone from Tully",
            "TIFFANY": "Route 43 - Pink Bow from Tiffany",
            "WILTON":  "Route 44 - Poke Ball from Wilton",
            "JOSE":    "Route 27 - Star Piece from Jose",
        }
        for trainer_key, loc_name in gift_locations.items():
            trainer = REMATCH_TRAINERS[trainer_key]
            try:
                loc = self.multiworld.get_location(loc_name, self.player)
            except KeyError:
                continue
            state = self.multiworld.get_all_state(False)
            for gate in trainer.tier_gates:
                state.remove(self.world.create_event(gate))
            self.assertTrue(
                loc.access_rule(state),
                f"{loc_name} should be reachable with all tier gates removed",
            )


class RematchsanityNoPokemonRequestsTest(PokemonCrystalTestBase):
    """Rematchsanity on but pokemon_requests off: trainers with a
    pokemon_request_slot must not have rematch locations in the pool."""
    options = {
        "rematchsanity": "true",
        "randomize_phone_call_items": "true",
        "randomize_pokegear": True,
    }

    def test_request_trainer_rematch_locations_excluded(self):
        labels = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for label, _id, trainer, _idx in all_rematch_locations():
            if trainer.pokemon_request_slot is not None:
                self.assertNotIn(label, labels,
                                 f"{label} should be excluded when pokemon_requests is off")
            else:
                self.assertIn(label, labels,
                              f"{label} should be present")


class RematchsanityJohtoOnlyTest(PokemonCrystalTestBase):
    """Rematchsanity + johto_only: KANTO-tier rematches (POWER tier) must not
    be in the AP location pool, since EVENT_RESTORED_POWER_TO_KANTO can never
    fire in a Johto-only seed. Otherwise fill would place items behind those
    locations and the seed becomes uncompletable."""
    options = {
        "rematchsanity": "true",
        "johto_only": "true",
    }

    def test_no_kanto_tier_rematch_locations(self):
        """All-state must be able to reach every rematch location that exists."""
        all_state = self.multiworld.get_all_state(False)
        for label, _id, trainer, idx in all_rematch_locations():
            gate = trainer.tier_gates[idx]
            try:
                loc = self.multiworld.get_location(label, self.player)
            except KeyError:
                if trainer.pokemon_request_slot is not None:
                    continue
                self.assertEqual(gate, "EVENT_RESTORED_POWER_TO_KANTO",
                                 f"{label} excluded but gate is {gate}, not POWER")
                continue
            # Location exists — must be reachable in all-state.
            self.assertTrue(
                loc.access_rule(all_state),
                f"{label}: present in pool but unreachable in johto_only all-state",
            )

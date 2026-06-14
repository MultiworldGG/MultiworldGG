from collections.abc import Iterable
from dataclasses import dataclass, field

from test.param import classvar_matrix

from .bases import NoStepHK, StateVarSetup


@dataclass
class Inputs:
    key: str | None = None
    resource: dict[str, int] = field(default_factory=dict)
    cs: dict[str, int] = field(default_factory=dict)
    prep_vars: Iterable[str] = ()
    assert_empty: bool = False
    notches: int | None = None
    masks: int | None = None
    damage_count: int = 0
    damage_value: int = 1


take_damage_matrix = [
    Inputs("$LIFEBLOOD", resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0},
           cs={"Lifeblood_Heart": 1}, assert_empty=True, damage_count=2, notches=4),
    *[Inputs("$LIFEBLOOD", resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}, cs={charm: 1}, damage_count=2, notches=4)
      for charm in ("Lifeblood_Core", "Joni's_Blessing")],

    Inputs("$TAKEDAMAGE", assert_empty=True,  masks=8, damage_count=1),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=8, damage_count=1, cs={"FOCUS": 1}),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=4, damage_count=1, notches=6,
           cs={"Lifeblood_Heart": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=True,  masks=4, damage_count=1, notches=1,
           cs={"Lifeblood_Heart": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=8, damage_count=1, damage_value=2, notches=6,
           cs={"Lifeblood_Heart": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE[2]", assert_empty=True, masks=8, damage_count=1, notches=6,
           cs={"Lifeblood_Heart": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=12, damage_count=1, notches=1,
           cs={"Lifeblood_Heart": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=4, damage_count=1, notches=6,
           cs={"Lifeblood_Core": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=False,  masks=4, damage_count=1, notches=1,
           cs={"Lifeblood_Core": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=8, damage_count=1, notches=6,
           cs={"Hiveblood": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=12, notches=6, damage_count=3, damage_value=2,
           cs={"Deep_Focus": 1, "FOCUS": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
    Inputs("$TAKEDAMAGE", assert_empty=True,  masks=12, notches=6, damage_count=4, damage_value=2,
           cs={"Deep_Focus": 1, "FOCUS": 1}, resource={"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}),
]


@classvar_matrix(matrix_vars=take_damage_matrix)
class TestDamagedVars(StateVarSetup, NoStepHK):
    matrix_vars: Inputs
    assert_empty: bool
    damage_count: int
    damage_value: int

    def setUp(self):
        super().setUp()
        self.key = self.matrix_vars.key
        self.resource = self.matrix_vars.resource
        self.cs = self.matrix_vars.cs
        self.prep_vars = self.matrix_vars.prep_vars
        self.notch_override = self.matrix_vars.notches
        self.mask_override = self.matrix_vars.masks

        self.assert_empty = self.matrix_vars.assert_empty
        self.damage_count = self.matrix_vars.damage_count
        self.damage_value = self.matrix_vars.damage_value

    def test_output(self):
        rs, cs = self.get_initialized_args()
        handler = self.get_handler()
        damage_key = "$TAKEDAMAGE" if self.damage_value == 1 else f"$TAKEDAMAGE[{self.damage_value}]"
        damage_handler = self.get_handler(damage_key)

        outputs = [rs]
        for _ in range(self.damage_count):
            outputs = [s for os in outputs for s in damage_handler.modify_state(os, cs)]

        outputs = [s for os in outputs for s in handler.modify_state(os, cs)]
        if self.assert_empty:
            self.assertFalse(outputs, "Expected to not be in logic but was")
        else:
            self.assertTrue(outputs, "Expected to be in logic but was not")

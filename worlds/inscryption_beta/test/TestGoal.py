from . import InscryptionTestBase


class GoalTestOneAct(InscryptionTestBase):
    options = {
        "goal": 0,
    }

    def test_beatable(self) -> None:
        self.assertBeatable(False)
        self.collect_act_1()
        self.assertBeatable(True)


class GoalTestTwoActs(InscryptionTestBase):
    options = {
        "goal": 1,
    }

    def test_beatable(self) -> None:
        self.collect_act_1()
        self.assertBeatable(False)
        self.collect_act_2()
        self.assertBeatable(True)


class GoalTestAllActs(InscryptionTestBase):
    options = {
        "goal": 2,
    }

    def test_beatable(self) -> None:
        self.collect_act_1()
        self.collect_act_2()
        self.assertBeatable(False)
        self.collect_act_3()
        self.assertBeatable(True)

    def test_every_act_is_required(self) -> None:
        self.collect_act_1()
        self.collect_act_2()
        self.collect_act_3()
        self.assertBeatable(True)
        for item_name in ("Film Roll", "Monocle", "Inspectometer Battery"):
            item = self.get_item_by_name(item_name)
            self.remove(item)
            self.assertBeatable(False)
            self.collect(item)


class GoalTestGroupedEpitaphs(InscryptionTestBase):
    options = {
        "epitaph_pieces_randomization": 1,
    }

    def test_beatable(self) -> None:
        self.collect_act_1()
        self.collect_act_2(epitaph_name="Epitaph Pieces", epitaph_count=3)
        self.collect_act_3()
        self.assertBeatable(True)
        item = self.get_item_by_name("Epitaph Pieces")
        self.remove(item)
        self.assertBeatable(False)
        self.collect(item)


class GoalTestEpitaphsAsOne(InscryptionTestBase):
    options = {
        "epitaph_pieces_randomization": 2,
    }

    def test_beatable(self) -> None:
        self.collect_act_1()
        self.collect_act_2(epitaph_name="Epitaph Pieces", epitaph_count=1)
        self.collect_act_3()
        self.assertBeatable(True)
        item = self.get_item_by_name("Epitaph Pieces")
        self.remove(item)
        self.assertBeatable(False)
        self.collect(item)

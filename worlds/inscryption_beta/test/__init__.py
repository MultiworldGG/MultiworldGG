from test.bases import WorldTestBase


class InscryptionTestBase(WorldTestBase):
    game = "Inscryption Beta"
    required_items_all_acts = ["Film Roll", "Camera Replica", "Pile Of Meat", "Monocle",
                               "Inspectometer Battery", "Gems Module", "Quill"]

    act_1_items = ["Film Roll"]
    act_2_items = ["Camera Replica", "Pile Of Meat", "Monocle"]
    act_3_items = ["Inspectometer Battery", "Gems Module", "Quill"]

    def collect_items(self, item_names) -> None:
        for item_name in item_names:
            self.collect(self.get_item_by_name(item_name))

    def collect_act_1(self) -> None:
        self.collect_items(self.act_1_items)

    def collect_act_2(self, epitaph_name: str = "Epitaph Piece", epitaph_count: int = 9) -> None:
        self.collect_items(self.act_2_items)
        for _ in range(epitaph_count):
            self.collect(self.get_item_by_name(epitaph_name))

    def collect_act_3(self) -> None:
        self.collect_items(self.act_3_items)

from ..items import PMItem


# A table that represents all areas of interactivity
class Node:

    # MapArea this node is found in
    map_id: int = -1
    area_id: int = -1

    # Entrance data of the Map if this note represents an entrance
    entrance_id: int = None
    entrance_type: str = None  # like walk, pipe, door etc.
    entrance_name: str = None  # verbose name of entrance

    # Human-readable name of item location (eg ItemA) or item price (eg ShopPriceA)
    key_name_item: str = None
    key_name_price: str = None
    item_source_type: int = None

    # reference to item placed here in the unmodified game
    vanilla_item: int = None

    # reference to item placed here during randomization
    current_item: PMItem = None

    # vanilla item price if shop
    vanilla_price: int = None

    # index bytes of the DBKey
    item_index: int = None
    price_index: int = None

    identifier: str = None

    # used for in game strings like shop descriptions
    shop_string_location: int = -1
    shop_string: list[int] = None

    def __str__(self):
        """Return string representation of current node"""
        entrance = ("[" + format(self.entrance_id) + "] ") if self.entrance_id else ''
        itemkey = ("[" + format(self.key_name_item) + "] ") if self.key_name_item else ''
        item = self.current_item.name if self.current_item else ''
        price = (
            " (" + format(self.current_item.base_price) + ")"
            if self.current_item and self.key_name_price
            else ''
        )

        return f"[{self.identifier}]{entrance}{itemkey}{item}{price}"

    def get_item_key(self):
        """Return convention key for item location"""
        if self.current_item is None:
            return None
        return (0xA1 << 24) | (self.area_id << 16) | (self.map_id << 8) | self.item_index

    def get_price_key(self):
        """Return convention key for item location"""
        if self.current_item is None:
            return None
        return (0xA1 << 24) | (self.area_id << 16) | (self.map_id << 8) | self.price_index

    def is_shop(self):
        """Return whether this location is a shop or not."""
        return self.key_name_price is not None

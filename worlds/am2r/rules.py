from typing import TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import AM2RWorld
else:
    AM2RWorld = object


class AM2RLogic:
    player: int

    def __init__(self, world: AM2RWorld, player: int):
        self.player = player

    def AM2R_can_bomb(self, state: CollectionState) -> bool:
        return state.has('Bombs', self.player) or state.has('Power Bomb', self.player, 2)

    def AM2R_can_jump(self, state: CollectionState) -> bool:
        return state.has_any({'Hi Jump', 'Space Jump', 'Bombs'}, self.player)

    def AM2R_can_fly(self, state: CollectionState) -> bool:
        return state.has_any({'Bombs', 'Space Jump'}, self.player)

    def AM2R_can_spider(self, state: CollectionState) -> bool:
        return state.has('Spider Ball', self.player) \
            or self.AM2R_can_fly(state)

    def AM2R_can_schmove(self, state: CollectionState) -> bool:
        return self.AM2R_can_spider(state) \
            or state.has('Hi Jump', self.player)

    def AM2R_has_ballspark(self, state: CollectionState) -> bool:
        return state.has_all({'Speed Booster', 'Spring Ball'}, self.player)

    def AM2R_can_down(self, state: CollectionState) -> bool:  # both of these fall to else and I really dont want to fix it until the full rewrite
        return state.has_all({"Speed Booster", "Ice Beam", "Super Missile"}, self.player) \
            and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state) and (state.has("Screw Attack", self.player) or state.has("Power Bomb", self.player))

    def AM2R_can_lab(self, state: CollectionState) -> bool:  # both of these fall to else and I really dont want to fix it until the full rewrite
        return state.has_all({"Speed Booster", "Ice Beam", "Super Missile"}, self.player) \
            and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state) and (state.has("Screw Attack", self.player) or state.has("Power Bomb", self.player))

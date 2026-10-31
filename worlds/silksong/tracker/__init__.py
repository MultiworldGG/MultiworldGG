from functools import wraps
import sys

from rule_builder.rules import And, Rule


class ActThreeActive(Rule, game='Hollow Knight: Silksong'):
    class Resolved(Rule.Resolved):
        force_recalculate = True

        def _evaluate(self, state):
            return getattr(state.multiworld.worlds[self.player], '_silksong_act_three_active', False)

        def explain_json(self, state=None):
            color = 'green' if state is not None and self(state) else 'salmon'
            return [{'type': 'color', 'color': color, 'text': 'Currently in Act 3'}]


def install_act_gate(world):
    if not getattr(world.multiworld, 'generation_is_fake', False):
        return
    region = world.multiworld.get_region('Event: Act 3 Started', world.player)
    for entrance in region.entrances:
        if getattr(entrance, '_silksong_act_gate', False):
            continue
        entrance.access_rule = And.Resolved(
            (entrance.access_rule, ActThreeActive().resolve(world)),
            player=world.player, caching_enabled=False,
        )
        entrance._silksong_act_gate = True


def act_state_key(context):
    return f'Silksong:Act3:{context.team}:{context.slot}'


def install_marker_status():
    client = sys.modules.get('worlds.tracker.TrackerClient')
    context = getattr(client, 'TrackerGameContext', None)
    if context is None or getattr(context.updateTracker, '_silksong_markers', False):
        return
    update = context.updateTracker
    on_package = context.on_package

    @wraps(on_package)
    def receive_package(self, cmd, args):
        if cmd == 'Connected':
            self.stored_data.pop(act_state_key(self), None)
        result = on_package(self, cmd, args)
        world = self.tracker_core.get_current_world()
        if world is not None and world.game == 'Hollow Knight: Silksong':
            key = act_state_key(self)
            if ((cmd == 'SetReply' and args.get('key') == key)
                    or (cmd == 'Retrieved' and key in args.get('keys', {}))):
                self.updateTracker()
        return result

    @wraps(update)
    def update_tracker(self):
        world = self.tracker_core.get_current_world()
        if world is not None and world.game == 'Hollow Knight: Silksong':
            install_act_gate(world)
            key = act_state_key(self)
            if getattr(self, '_silksong_act_subscription', None) != (world, key):
                self.set_notify(key)
                self._silksong_act_subscription = (world, key)
            world._silksong_act_three_active = self.stored_data.get(key) is True
        result = update(self)
        if result.state is None or self.ui is None:
            return result
        world = self.tracker_core.get_current_world()
        if world is None or world.game != 'Hollow Knight: Silksong':
            return result
        locations = world.multiworld.regions.location_cache[world.player]
        # UT treats reachable parents as passable even when the check is blocked.
        for name, coords in self.ldeferred_dict.items():
            location = locations.get(name)
            if location is None or location.address is not None:
                continue
            status = 'passed' if location.can_reach(result.state) else 'impassable'
            for coord in coords:
                coord.update_status(name, status)
        return result

    update_tracker._silksong_markers = True
    context.updateTracker = update_tracker
    context.on_package = receive_package

from functools import wraps
import sys


def install_marker_status():
    client = sys.modules.get('worlds.tracker.TrackerClient')
    context = getattr(client, 'TrackerGameContext', None)
    if context is None or getattr(context.updateTracker, '_silksong_markers', False):
        return
    update = context.updateTracker

    @wraps(update)
    def update_tracker(self):
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

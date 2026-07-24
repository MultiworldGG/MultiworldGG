""" Root Context for Luigi's Mansion. This Context attempts to load UT's TrackerGameContext, if not found CommonContext is used instead. """
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"


# Load Universal Tracker modules with aliases
_tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as CommonContext, TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION, logger
    _tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor, logger

class UniversalCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext, server_address: str = None):
        if server_address:
            ctx.server_address = server_address
        super().__init__(ctx)

class UniversalContext(CommonContext):
    tracker_enabled: bool = False

    def __init__(self, server_address, password):
        """
        Initialize the Luigi's Mansion Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)
        self.tracker_enabled = _tracker_loaded

    def _main(self):
        if self.tracker_enabled:
            self.run_generator()
            self.tags.remove("Tracker")
        else:
            logger.warning("Could not find Universal Tracker.")

    def make_gui(self):
        if _tracker_loaded:
            if not _check_universal_tracker_version():
                Utils.messagebox("Universal Tracker needs updated", f"The minimum version of Universal Tracker required for LM is v0.2.11. The version currently installed is {UT_VERSION}.", error=True)
                raise ImportError("Need to update universal tracker version to at least v0.2.11.")

        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from kvui import GameManager
        ui: GameManager = super().make_gui()
        class UniversalWrapper(ui):
            base_title: str = f" | {apname}"

            def build(self):
                container = super().build()
                if _tracker_loaded:
                    self.base_title += f" | Universal Tracker {UT_VERSION}"
                return container

        return UniversalWrapper


def _check_universal_tracker_version() -> bool:
    import re
    from Utils import tuplize_version
    if not _tracker_loaded:
        return False

    # We are checking for a string that starts with v contains any amount of digits followed by a period
    # repeating three times (e.x. v0.2.11)
    match = re.search(r"v\d+.(\d+).(\d+)", UT_VERSION)
    if len(match.groups()) < 2:
        return False
    if not tuplize_version(match.string.replace("v", "")) > tuplize_version("0.2.11"):
        return False

    return True

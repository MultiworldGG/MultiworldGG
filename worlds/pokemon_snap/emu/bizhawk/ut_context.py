from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor
from ..ut_helper import TrackerGameContext, universal_tracker_loaded
from .. import PokemonSnapGenericCommandProcessor

class BizHawkTrackerCommandProcessor(BizHawkClientCommandProcessor, PokemonSnapGenericCommandProcessor):
    pass

if universal_tracker_loaded:
    class BizHawkTrackerClientContext(TrackerGameContext, BizHawkClientContext):
        tags = {"AP"}
        command_processor = BizHawkTrackerCommandProcessor
        server_auth = BizHawkClientContext.server_auth

        def on_package(self, cmd, args):
            BizHawkClientContext.on_package(self, cmd, args)
            TrackerGameContext.on_package(self, cmd, args)

        def make_gui(self):
            ui = super().make_gui()
            ui.base_title = "Archipelago BizHawk Client"
            return ui

    ContextClass = BizHawkTrackerClientContext
else:
    class BizHawkNoTrackerClientContext(BizHawkClientContext):
        command_processor = BizHawkTrackerCommandProcessor

        def run_generator(self):
            pass

    ContextClass = BizHawkNoTrackerClientContext
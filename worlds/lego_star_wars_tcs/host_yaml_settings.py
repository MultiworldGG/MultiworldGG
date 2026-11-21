from settings import Group, Bool

class LegoStarWarsTCSSettings(Group):
    class RunInAWindow(Bool):
        """Whether the client should force the game to run in a window instead of fullscreen. The game won't update
        between windowed/fullscreen unless you alt+tab, or you go to the Video Settings menu and Accept at the bottom of
        the menu. When windowed, the window shows over the top of other windows unless you minimize it. This setting can
        be toggled in the client with /toggle_windowed."""
    class AutoResizeWindow(Bool):
        """Whether the client should automatically resize the window to your game resolutions when run_in_a_window is
        enabled. This uses Windows APIs and could be weird for Mac/Linux users running the Windows version of
        Archipelago."""
    run_in_a_window: RunInAWindow | bool = False
    auto_resize_window: AutoResizeWindow | bool = True

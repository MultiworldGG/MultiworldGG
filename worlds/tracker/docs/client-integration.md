# Client integration

This document describes how you can integrate Universal Tracker into your own game's client and take advantage of its features.

## Adding a tracker tab to your CommonClient client

With the addition of ctx.make_gui() in 0.5.1 adding a UT tracker tab is very simplified,
When you import CommonContext, try and import the UT context instead
```py

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext
```

You'll also need to remove the "Tracker" tag from your context by resetting it back to {"AP"}
```py
class YourGameContext(SuperContext):
    tags = {"AP"}
```

if your client has an `on_package` function, remember to call UT's `on_package` in order for it to respond to network events
```py
def on_package(self, cmd: str, args: dict):
    super().on_package(cmd, args)
```

if you edit your GameManager at all, just use super().make_gui() to inheret UT's ui if it got loaded
```py
def make_gui(self):
    ui = super().make_gui()
    ui.base_title = "Minit CLIENT"
    return ui
```

and when you start your client up add a call to ctx.run_generate() if the UT apworld was found
```py
if tracker_loaded:
    ctx.run_generator()
if gui_enabled:
    ctx.run_gui()
```

## Calling UT's tracker engine directly

Thanks to a recent refactor, calling UT as a library has become easier.

Be making a new instance of the TrackerCore, assuming you provide it with the expected information in the expected order, you can get access to UT's logic tracking methods without the need for a network connection

```py
from worlds.tracker.TrackerCore import TrackerCore
import logging

# Making some constants
slot_name = "qwintBug"
game = "Hollow Knight"
slot = 1
team = 1
print_list = False
print_count = False
logger = logging.getLogger("Client")

# logger is a logging.Logger used for messaging
# print_list and print_count are used for CLI implementations and should likely be set to False always
tracker_core = TrackerCore(logger,print_list, print_count)
# Initial UT gen
tracker_core.run_generator(None, None)
# get the class of the world, if you're tracking your own world you can probally just reference that
connected_cls = AutoWorld.AutoWorldRegister.world_types.get(game)
# Set the slot parameters to track
tracker_core.set_slot_params(game,slot,slot_name,team)
# Interpret slot data + regen if needed
tracker_core.initalize_tracker_core(connected_cls,slot_data)

# At this point the tracker core has been fully initalized 

# Set the list of locations to check for logic
tracker_core.set_missing_locations(set([16777360, 16777370, 16777410]))
# Set the list of items recieved
# This part is annoying still as Tracker Core still depends on the NetworkItem format
items = [16777224, 16777227, 16777289]
#                                     id  ,loc,player,flags
tracker_core.set_items_received(set([(item,-1 ,-1    ,0    ) for item in items]))
# you can set hints here but it's not imporant unless you like the color blue in the output format
# tracker_core.update_hints()

# Now you can actually ask tracker_core what the expected logic is
updateTracker_ret = tracker_core.updateTracker()

# Check UT's __init__.py for the class definition of the CurrentTrackerState type

print(updateTracker_ret.in_logic_locations)
# [16777370, 16777410]
```

## World flags

UT supports a number of world flags that determine how UT will handle the world, the following is the current list

 * `disable_ut` : This causes UT to ignore the world, to be used only if the world is known to have issues when loaded in UT and fixing it would be more trouble then it's worth (Merged game/existing compatent poptracker etc)
 * `ut_can_gen_without_yaml` : Tells UT that the game will do a full regen

## Command Line Interface

UT provides two args that allow it to run as a "single shot" command line utility

  * `--list` which simply lists all currently in logic locations (as they would appear on the tab in the UI)
  * `--count` which provides an easier to parse overview of the current in logic state

To  use these commands, do the following

  1) Invoke the Launcher (if not on source, use the debug launcher to get a command line)
  2) Tell the launcher to open Universal Tracker
  3) Pass in the `--nogui` and whichever (or both) CLI args you want
  4) Input the URL

For example
```sh
python .\Launcher.py "Universal Tracker" -- --nogui --list Player1:None@localhost
```

## Automating getting logic counts

Thanks to digiholic we have an example Powershell script that will use UT to connect to each specified slot and get the in logic counts

```powershell
Clear-Content count.txt
Get-Content -Path "slots.txt" | ForEach-Object {
    .\MultiworldGGLauncherDebug.exe "Universal Tracker" -- --nogui --name "$_" --connect localhost:38281 --count | Select-Object -Last 4 >> count.txt
    echo "-----------------------------------------" >> count.txt
}
PAUSE
```

This script requires a `slots.txt` that contains each slot name on it's own line, and correct the address in the script, it will then create a `counts.txt` file that can be parsed further.

## Adding In-Logic Callbacks

For clients that have a desire to "poll" the tracker stats, this causes problems as every time a client runs updateTracker a lot of rules get called and that can take some time (even if it's faster then most humans will notice)

The better solution for this problem is to use the callback registers that UT provides to get automatically notified when there is an update

UT provides the following registers

* set_callback : Called with the current in logic locations
* set_region_callback : Called with the current in logic regions
* set_events_callback : Called with the current in logic event location names
* set_glitches_callback : Called with the current in logic locations that are only in logic with the "Glitches" state

All of these functions must be provided with a function (that will be called with the appropriate parameter) that takes in a list of strings (currently expects to return a bool but that isn't used at the moment)

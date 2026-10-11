export const GAME_NAME = "Ratchet & Clank: The Odd Couple";
export const INTRO_LOCATION = "The Odd Couple Intro";

// The Archipelago client only ever installs one file, under this fixed name
// (see client/backend.py's PATCHED_SWF_NAME) - there is nothing else to pick
// from, so the movie dropdown that used to live here has been removed.
export const PATCHED_MOVIE = "ap_patched_odd_couple.swf";

// Reserved suppressed-event name that means "block all mouse clicks on the
// player itself". Needed because most SWFs handle button clicks (AVM1
// buttons etc.) entirely inside Flash/Ruffle's own runtime and never call
// out to ExternalInterface for permission, so the checkEvent() bridge can't
// intercept them. This overlay physically sits on top of the player and
// swallows the click before it ever reaches the canvas.
export const CLICK_BLOCK_EVENT = "Avm1Button";

// Maps backend scene/event names to the item name the player receives to
// unlock them. Kept in sync by hand with items.py/locations.py/swf_patch.py.
export const SCENE_TO_ITEM = {
  stereo: "Stereo",
  taxiDriver: "Taxi Driver",
  gimp: "Gimp",
  phonecall1: "Phonecall",
  scissors: "Scissors",
  tv: "TV",
};

// Which location(s) get checked off when a scene is reported. "gimp" can be
// replayed, and each playthrough fills the next not-yet-checked Gimp location.
export const SCENE_TO_LOCATIONS = {
  stereo: ["Stereo"],
  taxiDriver: ["Fruit Bowl: Taxi Driver!"],
  gimp: [
    "Is That Captan Qwark?: Scene 1",
    "Is That Captan Qwark?: Scene 2",
    "Is That Captan Qwark?: Scene 3",
  ],
  phonecall1: ["Join The Darkside: Phonecall"],
  scissors: ["Snip Snip: Scissors"],
  tv: ["A link to the past: TV"],
};

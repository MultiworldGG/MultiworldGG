import { state } from "./state.js";
import { PATCHED_MOVIE } from "./constants.js";

const playerWrapper = document.getElementById("player-wrapper");

let player = null;
let currentMovie = null;
let pollHandle = null;
let hasReportedPlayed = false;

// --- ExternalInterface bridge: available for a SWF to call by name via
// ExternalInterface.call("checkEvent", "someEventName") if it ever needs a
// synchronous in-page check instead of the relay server's HTTP endpoints.
window.checkEvent = function (eventName) {
  return !state.suppressedEvents.has(eventName);
};

window.reportMovieEnded = function () {
  reportPlayed();
};

function reportPlayed() {
  if (hasReportedPlayed || !currentMovie) return;
  hasReportedPlayed = true;
  console.log(`Movie played: ${currentMovie}`);
}

// --- Fallback "played" detection: poll Ruffle's Flash-compatible scripting
// properties. A movie is considered played once it has started (currentFrame
// advanced past 0) and then stops playing on its own (isPlaying becomes
// false), which is the standard pattern for a SWF that calls stop() on its
// last frame.
function startPlayedPolling() {
  let everPlayed = false;
  stopPlayedPolling();
  pollHandle = setInterval(() => {
    if (!player) return;
    try {
      const playing = player.isPlaying;
      const frame = player.currentFrame;
      if (playing && frame > 0) everPlayed = true;
      if (everPlayed && !playing) {
        reportPlayed();
        stopPlayedPolling();
      }
    } catch (e) {
      // player not ready yet
    }
  }, 250);
}

function stopPlayedPolling() {
  if (pollHandle) clearInterval(pollHandle);
  pollHandle = null;
}

// --- Movie loading: there is exactly one movie - the one the .apoddcouple
// patch file produced - so this loads unconditionally on startup,
// independent of the Archipelago connection.
export function loadMovie(filename = PATCHED_MOVIE) {
  currentMovie = filename;
  hasReportedPlayed = false;
  stopPlayedPolling();
  playerWrapper.innerHTML = "";

  const ruffle = window.RufflePlayer.newest();
  player = ruffle.createPlayer();
  playerWrapper.appendChild(player);
  player.load({ url: `/game/${filename}?v=${Date.now()}`, allowScriptAccess: "always" });
  player.traceObserver = (msg) => console.log("[SWF trace]", msg);

  startPlayedPolling();
}

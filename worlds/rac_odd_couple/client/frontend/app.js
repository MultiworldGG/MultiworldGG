import { state } from "./state.js";
import { checkSwfInstalled, startHeartbeat } from "./relay.js";
import { loadMovie } from "./swf.js";
import "./items.js";
import "./chat.js";
import "./connection.js";

const connectForm = document.getElementById("connect-form");
const noSwfMessage = document.getElementById("no-swf-message");

// Refuse to offer a login form at all if the relay server has no patched swf
// installed yet - there's nothing to play or check locations against without one.
async function init() {
  state.swfInstalled = await checkSwfInstalled();
  if (!state.swfInstalled) {
    connectForm.classList.add("hidden");
    noSwfMessage.classList.remove("hidden");
    return;
  }
  loadMovie();
}

init();
startHeartbeat();

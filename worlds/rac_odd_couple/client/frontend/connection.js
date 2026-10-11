import { Client } from "https://unpkg.com/archipelago.js@2.1.0/dist/archipelago.min.js";
import { state } from "./state.js";
import { GAME_NAME, INTRO_LOCATION, SCENE_TO_ITEM, SCENE_TO_LOCATIONS } from "./constants.js";
import { locationIdByName } from "./package.js";
import { renderItems, updateClickBlocker } from "./items.js";
import { appendChatLine } from "./chat.js";
import { syncSuppressedToRelay, startReceivedPolling, stopReceivedPolling } from "./relay.js";

const connStatus = document.getElementById("conn-status");
const connectOverlay = document.getElementById("connect-overlay");
const connectForm = document.getElementById("connect-form");
const connectError = document.getElementById("connect-error");

function recomputeSuppressed() {
  const receivedNames = new Set(state.client.items.received.map((item) => item.name));
  const newSuppressed = new Set();
  for (const [scene, itemName] of Object.entries(SCENE_TO_ITEM)) {
    if (!receivedNames.has(itemName)) newSuppressed.add(scene);
  }
  state.suppressedEvents = newSuppressed;
  renderItems();
  updateClickBlocker();
  syncSuppressedToRelay();
}

function checkIntroLocation() {
  const introId = locationIdByName(INTRO_LOCATION);
  const checked = new Set(state.client.room.checkedLocations);
  if (introId != null && !checked.has(introId)) {
    state.client.check(introId);
  }
}

// Mirrors the old Python client's on_scene_initiated: check the next
// not-yet-checked location for this scene (only "gimp" ever has more than
// one, each replay filling the next).
function onSceneInitiated(scene) {
  const locationNames = SCENE_TO_LOCATIONS[scene];
  if (!locationNames) return;
  const checked = new Set(state.client.room.checkedLocations);
  for (const name of locationNames) {
    const id = locationIdByName(name);
    if (id != null && !checked.has(id)) {
      state.client.check(id);
      break;
    }
  }
}

// The goal is 100% - every one of this slot's locations checked.
// missingLocations is server-confirmed (updated on connect/roomUpdate), so
// it's only accurate to check here rather than right after check(), which
// hasn't round-tripped yet.
function maybeSendGoal() {
  if (state.finishedGame || !state.client) return;
  if (state.client.room.missingLocations.length > 0) return;
  state.finishedGame = true;
  state.client.goal();
}

async function connect(server, slot, password) {
  state.client = new Client();

  state.client.items.on("itemsReceived", () => recomputeSuppressed());
  state.client.messages.on("message", (text, nodes) => appendChatLine(text, nodes));
  state.client.socket.on("roomUpdate", () => {
    renderItems();
    maybeSendGoal();
  });
  state.client.socket.on("disconnected", () => {
    connStatus.textContent = "disconnected";
    connStatus.className = "status bad";
    stopReceivedPolling();
  });

  await state.client.login(server, slot, GAME_NAME, { password });
  await state.client.package.fetchPackage([GAME_NAME]);

  connStatus.textContent = "connected";
  connStatus.className = "status ok";
  connectOverlay.classList.add("hidden");

  state.finishedGame = false;
  recomputeSuppressed();
  checkIntroLocation();
  maybeSendGoal();
  startReceivedPolling(onSceneInitiated);
}

connectForm.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  if (!state.swfInstalled) return;
  connectError.classList.add("hidden");
  const server = document.getElementById("connect-server").value.trim();
  const slot = document.getElementById("connect-slot").value.trim();
  const password = document.getElementById("connect-password").value;

  connStatus.textContent = "connecting...";
  connStatus.className = "status";
  try {
    await connect(server, slot, password);
  } catch (err) {
    console.error("Failed to connect", err);
    connStatus.textContent = "disconnected";
    connStatus.className = "status bad";
    connectError.textContent = err && err.message ? err.message : "Failed to connect.";
    connectError.classList.remove("hidden");
  }
});

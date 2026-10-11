import { state } from "./state.js";

// --- Local relay server (client/backend.py) sync ---
// The patched swf's own ActionScript calls this same-origin server directly
// over HTTP (LoadVars) to gate its scene buttons - Flash/Ruffle content has
// no way to call into this page's JS. This page keeps that server's
// suppressed-event state in sync, and polls it for scene-initiated reports
// the swf sent it, since there's no push channel between them anymore.
export function syncSuppressedToRelay() {
  fetch("/api/suppressed", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ events: Array.from(state.suppressedEvents) }),
  }).catch((err) => console.error("Failed to sync suppressed events to relay", err));
}

let receivedPollHandle = null;

async function pollReceivedEvents(onSceneInitiated) {
  let scenes;
  try {
    const res = await fetch("/api/poll-received");
    scenes = await res.json();
  } catch (err) {
    return;
  }
  for (const scene of scenes) {
    onSceneInitiated(scene);
  }
}

export function startReceivedPolling(onSceneInitiated) {
  stopReceivedPolling();
  receivedPollHandle = setInterval(() => pollReceivedEvents(onSceneInitiated), 400);
}

export function stopReceivedPolling() {
  if (receivedPollHandle) clearInterval(receivedPollHandle);
  receivedPollHandle = null;
}

// Refuse to offer a login form at all if the relay server has no patched swf
// installed yet - there's nothing to play or check locations against without one.
export async function checkSwfInstalled() {
  try {
    const res = await fetch("/api/status");
    const status = await res.json();
    return !!status.swf_installed;
  } catch (err) {
    console.error("Failed to check swf status", err);
    return true; // fail open - don't block login over a transient fetch error
  }
}

// --- Keep the relay server (client/__init__.py's launch()) alive only as
// long as this tab is: a periodic heartbeat while open, plus an immediate
// beacon on close/refresh so the Python process doesn't linger after you're
// done. sendBeacon (not fetch) is used on unload since it's designed to
// reliably deliver even as the page is being torn down.
const HEARTBEAT_INTERVAL_MS = 15000;

function sendHeartbeat() {
  fetch("/api/heartbeat").catch(() => {});
}

export function startHeartbeat() {
  sendHeartbeat();
  setInterval(sendHeartbeat, HEARTBEAT_INTERVAL_MS);
  window.addEventListener("pagehide", () => {
    navigator.sendBeacon("/api/closed");
  });
}

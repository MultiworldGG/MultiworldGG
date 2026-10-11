import { state } from "./state.js";

const chatToggle = document.getElementById("chat-toggle");
const chatPanel = document.getElementById("chat-panel");
const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const itemsPanel = document.getElementById("items-panel");

chatToggle.addEventListener("click", () => {
  chatPanel.classList.toggle("hidden");
  itemsPanel.classList.add("hidden");
});

// Reproduces the reference text client's message coloring (NetUtils.py's
// JSONtoTextParser) so chat/hint/item-received lines read the same here as
// they do in the normal client, instead of flattening everything to plain text.
function isSelf(player) {
  const self = state.client && state.client.players.self;
  return !!self && player.slot === self.slot && player.team === self.team;
}

function messageNodeClasses(node) {
  switch (node.type) {
    case "item": {
      const item = node.item;
      if (item.progression) return ["apc-plum"];
      if (item.useful) return ["apc-slateblue"];
      if (item.trap) return ["apc-salmon"];
      return ["apc-cyan"];
    }
    case "location":
      return ["apc-green"];
    case "entrance":
      return ["apc-blue"];
    case "player":
      return [isSelf(node.player) ? "apc-magenta" : "apc-yellow"];
    case "color":
      return String(node.color).split(";").filter(Boolean).map((c) => `apc-${c}`);
    default:
      return [];
  }
}

// #chat-log is already visually capped (see style.css) and scrolls once
// full, but that's only a display limit - without this, the underlying
// message elements would keep growing for as long as the tab stays open.
// Once it's past MAX_CHAT_LINES, drop the oldest to keep it bounded.
const MAX_CHAT_LINES = 500;

export function appendChatLine(text, nodes) {
  const line = document.createElement("div");
  line.className = "chat-line";
  if (nodes && nodes.length) {
    for (const node of nodes) {
      const span = document.createElement("span");
      span.className = messageNodeClasses(node).join(" ");
      span.textContent = node.text;
      line.appendChild(span);
    }
  } else {
    line.textContent = text;
  }
  chatLog.appendChild(line);
  while (chatLog.children.length > MAX_CHAT_LINES) {
    chatLog.removeChild(chatLog.firstChild);
  }
  chatLog.scrollTop = chatLog.scrollHeight;
}

chatForm.addEventListener("submit", (evt) => {
  evt.preventDefault();
  const text = chatInput.value.trim();
  if (!text || !state.client) return;
  state.client.messages.say(text).catch((err) => console.error("Failed to send chat message", err));
  chatInput.value = "";
});

import { state } from "./state.js";
import { SCENE_TO_ITEM, SCENE_TO_LOCATIONS, CLICK_BLOCK_EVENT } from "./constants.js";
import { locationIdByName } from "./package.js";

const clickBlocker = document.getElementById("click-blocker");
const itemsToggle = document.getElementById("items-toggle");
const itemsPanel = document.getElementById("items-panel");
const itemsList = document.getElementById("items-list");
const chatPanel = document.getElementById("chat-panel");

export function updateClickBlocker() {
  clickBlocker.classList.toggle("active", state.suppressedEvents.has(CLICK_BLOCK_EVENT));
}

// The items panel always lists every scene item: gray while still locked,
// then red once unlocked but its location(s) aren't all checked yet, green
// once they are.
export function renderItems() {
  itemsList.innerHTML = "";
  const checked = state.client ? new Set(state.client.room.checkedLocations) : new Set();
  for (const scene of Object.keys(SCENE_TO_ITEM)) {
    const li = document.createElement("li");
    li.textContent = SCENE_TO_ITEM[scene];
    if (state.suppressedEvents.has(scene)) {
      li.className = "locked";
    } else {
      const locationNames = SCENE_TO_LOCATIONS[scene] || [];
      const allChecked = locationNames.length > 0 && locationNames.every((name) => {
        const id = locationIdByName(name);
        return id != null && checked.has(id);
      });
      li.className = allChecked ? "checked" : "unchecked";
    }
    itemsList.appendChild(li);
  }
}

itemsToggle.addEventListener("click", () => {
  itemsPanel.classList.toggle("hidden");
  chatPanel.classList.add("hidden");
});

// Shared mutable state, held in one place so the other modules can read/write
// it without needing to import each other just to pass it around.
export const state = {
  client: null,
  swfInstalled: false,
  suppressedEvents: new Set(),
  finishedGame: false,
};

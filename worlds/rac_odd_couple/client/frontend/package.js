import { state } from "./state.js";
import { GAME_NAME } from "./constants.js";

// Looks up a location's numeric id from its name via the data package
// archipelago.js fetched on login. Kept in its own module (rather than on
// connection.js) so items.js can use it too without the two modules having
// to import each other.
export function locationIdByName(name) {
  const pkg = state.client.package.findPackage(GAME_NAME);
  return pkg ? pkg.locationTable[name] : undefined;
}

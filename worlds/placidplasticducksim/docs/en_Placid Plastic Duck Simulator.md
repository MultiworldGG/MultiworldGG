# Placid Plastic Duck Simulator for MultiworldGG

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## Randomizer Info

- new game only appears once you connect to MWGG
- removed the ability to save (not needed)
- removed the ability to resume a save (not needed because you can't save)
- the classic spawner was shut down and replaced with a custom one
  - it will only spawn ducks from columns you have available, if you have no more unique ducks, it will spawn a random one from the available pool
  - random ducks do not count for checks
- goal requires all the 46 (excluding the alien) from the first page of the collection to be found
- `Progressive Column Unlock`
  - will make the next column in the collection book available to spawn
  - the first column is a given
- `Progressive Spawn Speed Upgrade`
  - spawn speed is calculated as so: [120 - `Progressive Spawn Speed Upgrade` amount * 10]
  - there are 9 of these so 120s -> 30s
- `Random Duck`
  - spawns a duck from the random pool
## Funny quirks
- will goal before sending last check
- crashes when loosing connection
- as long as you don't bk the MAX time to goal is 1hr 30min

## Special Thanks

- Sterlia for buying me the game and 'forcing' me to make an ap for it
- Silent, Ethical Logic, and FyreDay for programming support
- BadMagic for telling me about IlRepack

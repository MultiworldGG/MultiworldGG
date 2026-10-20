# Ocarina of Time APWorld

This repository contains a modern Archipelago world implementation for **The Legend of Zelda: Ocarina of Time**.

It is based on and related to the upstream [Ocarina of Time Randomizer](https://github.com/OoTRandomizer/OoT-Randomizer) project, adapting OoT randomizer behavior and data for use with [Archipelago](https://archipelago.gg/).

## Current Version
Based on OoTR version 9.1.0, released May 21 2026

## Setup

See the [Setup guide](docs/setup_en.md) for installation and play instructions.

Important: OoT currently ships with Archipelago in a non-standard way, so the old bundled APWorld will collide with this one. Before installing this APWorld, delete the existing `oot` folder from `lib/worlds` in your Archipelago install directory. After installing this APWorld, restart the Archipelago Launcher.

The setup guide also covers the current client/adjuster requirement: use the new `Ocarina of Time Client` and `Ocarina of Time Adjuster` entries provided for this APWorld. The old OoT Client and OoT Adjuster shipping with AP will *not* work.

## Requirements

- Archipelago 0.6.4 or newer
- An Ocarina of Time v1.0 NTSC-U or NTSC-J ROM (only needed to patch and play)
- A supported N64 emulator

Generation produces a new `.apoot` procedural patch and requires no ROM. Each player
applies their patch with the Ocarina of Time Client or Adjuster and their own base ROM.

## Documentation

- [Setup guide](docs/setup_en.md)
- [Game page documentation](docs/en_Ocarina%20of%20Time.md)

## Credits

This project builds on work from the OoT Randomizer and Archipelago communities.

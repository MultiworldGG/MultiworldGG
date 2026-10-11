# Ratchet & Clank: The Odd Couple Setup Guide

## Required Software

- MultiworldGG, with the Ratchet & Clank: The Odd Couple Archipelago client included.
- Your own copy of the vanilla `odd_couple.swf` minigame file. Nothing else is needed - the client
  patches it, serves it, and runs the whole minigame itself, with no external project, web server,
  or virtualenv required.

## Installation

1. Open your `.apoddcouple` patch file (e.g. from the MultiworldGG Launcher, or by double-clicking it
   if file associations are set up). This launches the Ratchet & Clank: The Odd Couple Client.
2. The first time you patch a file, you'll be prompted to browse to your `odd_couple.swf` file. Your
   choice is remembered in `host.yaml` (under `rac_odd_couple_options > swf_file`) for next time.
3. The client patches the swf, installs it locally, starts its own embedded web server, and opens
   the minigame in your browser, then connects to the multiworld server you specify.

## Playing

Each of the six interactions in Ratchet's apartment (Stereo, Taxi Driver, Gimp, Phonecall, Scissors,
TV) is locked until you receive the matching item from the multiworld. The Gimp scene can be played
through three times, each one sending a separate check. Once you've found everything, the night is
yours.

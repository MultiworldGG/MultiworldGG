# Portal 2

***
\**Cough cough\**
Cave Johnson here.

We have a **BIG** problem on our hands.
I'm gonna bet most of you here already know about the whole multiverse thing. Remember - "infinite earths, with an infinite number of Apertures"?

Well, *some* of those outer-world Apertures had decided they've had enough of our borrowing, and began stealing testing elements right back from us! **AND** replacing them with all sorts of weird junk that not even my father would be able to decipher!

Anyway, we're bankrupt. Again. Even more so now than before.
But there's no reason to panic! The lab boys and I have been bashing our heads against the wall for a while, but we've found a way to bring it back under control.

That's where you come in. We're going to send a rescue squad through the multiverse to get our precious buttons and cubes back! ...Oh, and my coffee mug. If you see that, bring that back too.

Now, we do need at least a few thousand people back here to manage the place, and one lucky son of a gun to oversee the return of the testing apparatus, so we can't send out everyone.

But if **YOU** want to be part of the **Archipelago Exploration Unit**, sign the relevant papers at the reception, then jump into that gaping hole in reality by the water cooler.

Seriously, though, we'll need everyone we can get on this. And fast. Before we have a repeat of what happened wi...

**[ ▮▮▮▮ AUDIO LOST ▮▮▮▮ ]**
***

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.


## How does Portal 2 work in MultiworldGG

You play through a randomised chapters completing maps. Initially the puzzle elements (e.g. Upgraded Portal Gun, Weighted Storage Cube) will be unavailable and you will gain them as you play gaining the ability to complete more levels that require these puzzle elements.

## Locations

The base locations in the game are completing maps, some of these maps are test chambers and some are locations in aperture laboratories, basically each new loading zone in the game is a separate map.
Additional optional locations include:
- "Cutscene" maps, those that require no input from the player (removed by default)
- Breaking **Wheatley Monitors** in Chapter 8 (and one in Chapter 9)
- Custom buttons in **Ratman Dens**

## Items

Items are test chamber elements e.g. Floor Button, Gels, PotatOS.

The junk filler items include Moon Dust, Slice of Cake and Lemon.

Traps are also in the game and can be set and adjusted in the yaml options.


## The Goal

At the moment the only goal is to finish the final level in Chapter 9 (Chapter 9 is not randomised)

# FAQ

**Why do checks not send/ items are usable in game even if I don't have them unlocked?**

This could be due to a few different issues:

1. You are not using the Portal 2 Client from the Archipelago Launcher. The custom client must be open at all times while playing the game
2. Your Portal 2 Archipelago Mod has not got the -netconport launch option set. You can check using the `/check_connection` command in the client. See step 7 of [Installation](../setup_en) to set the launch option.

**Why does my map menu not show any of the maps and just says "Connect to game to load levels"?**

You most likely didn't select the correct extras.txt file when joining a game for the first time. 

- Open host.yaml using the "Open host.yaml" button in the Archipelago Client
- Go down to `portal2` and see if the `menu_file` points to the **mods** extras.txt file as seen in step 4 of [Running](#running)

If you selected another file in the mod e.g. `GameInfo.txt` the game will not run correctly as the file has probably already been overwritten by the client so you will have to replace that file with an original copy or [reinstall the mod from scratch](../setup_en).

There is a very small chance that for people running another server on their machine the 3000 port is already in use. In this case you can change the `default_port` setting in `host.yaml` to another unused port and the `-netconport 3000` to the same port as in `host.yaml`.

## Acknowledgements

### Mod Creators

- **GlassToadstool** - Lead Developer
- **Proplayen** - Initial Logic Design
- **JD** - Icon Graphics
- **Kaito Kid** - Answering lots of questions about APWorld development
- **studkid** - UT Support
- **Clone Fighter** - Loading Screens, Logo Graphics, and Cave Johnson Speech
- **Charged_Neon** - Documentation
- **LimeDreaming** - Custom Font and Models
- **James** - apworld additions

### Initial Testers

**22TwentyTwo, ahhh reptar, Bfbfan26, buzzman5001, ChaiMint, Default Miserable, Fewffwa, Fox, Grenhunterr, Kit Lemonfoot, Knux, MarioXTurn, miketizzle411, Pigmaster100, Rya, Scrungip**
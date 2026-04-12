# Toontown

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## Description

This version of toontown makes modifications to the base game to not only to provide support for MultiworldGG, but also introduce gameplay tweaks to make the experience quicker, more satisfying, and more solo friendly. This game also has support for hosting and joining mini-servers if you still wish to play with friends! This game is a fully remote MultiworldGG game, which means that however you want to set up your slots for gameplay, it should work as you would expect. This means the following ways to play are supported:

* Playing alone on a slot
* Playing with friends on the same server with unique slots
* Playing with friends on the same server sharing one slot
* Multi-tooning 2-4 toons that all share a slot (and share progression)
* Multi-tooning 2-4 toons that all have unique slots
* Playing with 2 other friends who are also multi-tooning 4 toons and all sharing the same slot
The possibilities really are endless, and you can play the game however you want. Just make sure you set up your MultiworldGG rooms to accommodate that!

## Common Issues/FAQ

### I set up the server and everything is running fine. I can connect to my own server but my friends can't. Why?

If you are hosting a Mini-Server, you **must** port forward to allow incoming connections on port `7198`.
There are two ways to accomplish this:

- Port forward the port `7198` in your router's settings.
- Use a third party program (such as Hamachi) to emulate a LAN connection over the internet.

As router settings are wildly different, I cannot provide a tutorial on how to do this on this README for your specific
router. However, the process is pretty straight forward assuming you have access to your router's settings. 
You should be able to figure it out with a bit of research on Google.


### I launched the game and I am getting the error: The system cannot find the path specified

You did not do the `PPYTHON_PATH` step correctly from before. Double check that Panda3D is installed at the directory
located in `PPYTHON_PATH` and try again.


### I logged in and I have no gags and can't access the Toon HQ.... why can't I play?

This game is specifically designed to only work properly when you are connected to a MultiworldGG game. If you want to
play the game as intended, please generate a MultiworldGG seed or join a MultiworldGG room with others.

If you are a developer or just want to play around with the source, you have access to use commands. Check your 
book and look at the spellbook page to see what you can do. `~maxtoon` will put your toon in a state where you can do 
anything in the game with no restrictions.


### I was playing and my game crashed :(

Toontown: Archipelago is currently in an early alpha build so many issues are expected to be present. If you found a
crash/bug, feel free to [create an Issue](https://github.com/DevvyDont/toontown-archipelago/issues/new) on the GitHub page for the repository. Developers/contributors
use this as a "todo list". If you choose to do this, try and be as descriptive as possible on what caused the crash, and 
any sort of possible steps that can be taken to reproduce it.


### I was playing and the district reset :(

Similarly to a game crash, sometimes the district can crash. Follow the same steps as the previous point.


### I was given an MultiworldGG room link and my game works fine, how do I connect to the multiworld and play?

When in game, you first need to type (in Toontown's chat) `!slot <SLOT NAME>` where you replace `<SLOT NAME>` with 
whatever your slot is in the Multiworld room. Once you have done this, you can then type `!connect <AP SERVER IP>`
to play! The AP Server IP is usually listed at the top where it says "You can type /connect (AP SERVER IP) in your client...".

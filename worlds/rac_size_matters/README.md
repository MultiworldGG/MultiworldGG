# Ratchet & Clank Size Matters Archipelago

This is an implementation for the PS2 version of the game. You can find the setup guide [here](docs/setup_en.md).

## Disclamer
This is **not** all **Human written code**, this was developed with the help of AI. This was mostly done to speed up development and to test new logical improvements from how the original version of the AP was written.

## Known Bugs and issues

The rest of these are open design questions we're deliberately not resolving right now — parked pending feedback or a plan that doesn't regress other logic, not active bugs blocking play.
- **Nanotech (health) level check rule scaling isn't tuned.** The difficulty curve for higher Nanotech Levels is a rough cut, not a carefully considered scale — we don't yet know the right way to space it out, so it's parked until we get more playtesting feedback.
- **Skyboard Challenges has no item-only tier.** Unlike Clank Challenges (off / item rewards only / all completions), Skyboard Challenges is only off/all — no middle option for just the reward-bearing checks, and no separate "all checks" toggle for Skyboard missions specifically.
- **Experimental Skins can cause a large texture or show missing textures.** The experimental skins are as they say experimental, there are patches located in the `standalone_skins` folder for all 3 versions of the game (EU, US and JP). If you are using Experiemental skins without the patch it will work but you must connected the client to the game before loading a planet. the patch is applied during load transitions so as long as you dont enter a level transition while disconnected to the client it should work as intended. this is a toggleable option and is optional you are not forced into this patch.

## Massive thank you's
The PCSX2 PINE interface (`pcsx2_interface/`) is adapted from [evilwb/pypine](https://github.com/evilwb/pypine), based on https://projects.govanify.com/govanify/pine. This couldn't have been done without his pcsx2 interface.

Massive inspiration from RAC2 and RAC3 AP's for how to handle Ratchet and Clank games.

Massive thanks to RAC3 dev Taoshi for letting me steal his logic and some functions to fit into size matters.

Amondo for tidying up my static strings and for testing this game ( honestly think hes played the game more than I have at this point )

Concrete for making the absolutly fantastic icon im no artist so having someone actually talanted make one is amazing!!!

I cant believe i didnt mention him before but SomeLazyGamer for his amazing poptracker (he fixes it and i break it thats entirly on me) he does fantastic work on it and deserves the credit. check out his poptracker [here](https://github.com/SomeLazyGamer/RaC-5-SM-AP-Poptracker)

ImJustATester for helping me find addresses (especially the traps) as well as load logic and other fixes theres honestly too many addresses and maps they helped find i couldnt list them all.

Juniper Bunbun for their amazing AP icons these are cosmetic icons and can be changed using the `/apicon [blue|purple|grey]` or set in the options menu.

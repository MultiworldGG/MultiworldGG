import settings

class OraclesSettings(settings.Group):
    """
    Settings for any Oracle Game
    """
    class OoCharacterSprite(str):
        """
        The name of the sprite file to use (from "data/sprites/oos_ooa/").
        Putting "link" as a value uses the default game sprite.
        Putting "random" as a value randomly picks a sprite from your sprites directory for each generated ROM.
        If you want some weighted result, you can arrange the options like in your option yaml.
        """

    class OoCharacterPalette(str):
        """
        The color palette used for character sprite throughout the game.
        Valid values are: "green", "red", "blue", "orange", and "random"
        If you want some weighted result, you can arrange the options like in your option yaml.
        If you want a color weight to only apply to a specific sprite, you can write color|sprite: weight.
        For example, red|link: 1 would add red in the possible palettes with a weight of 1 only if link is the selected sprite
        """

    class OoHeartBeepInterval(str):
        """
        A factor applied to the infamous heart beep sound interval.
        Valid values are: "vanilla", "half", "quarter", "disabled"
        """

    class OoRemoveMusic(str):
        """
        If true, no music will be played in the game while sound effects remain untouched
        """

    class OoMusicShuffle(str):
        """
        Defines if you want music tracks to be shuffled each time you patch a new game.
        """

    class OoSfxShuffle(str):
        """
        Defines if you want sound effects to be shuffled each time you patch a new game.
        """
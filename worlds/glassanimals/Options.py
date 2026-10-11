# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.


from dataclasses import dataclass

from Options import DefaultOnToggle, OptionGroup, PerGameCommonOptions, Toggle


class IncludeDreamland(DefaultOnToggle):
    """Include the album Dreamland in the shuffling."""
    display_name = "Include Dreamland"


class IncludeILYSFM(DefaultOnToggle):
    """Include the album I Love You So F***ing Much in the shuffling."""
    display_name = "Include I Love You So F***ing Much"


class IncludeHTBAHB(Toggle):
    """Include the album How to Be a Human Being in the shuffling."""
    display_name = "Include How to Be a Human Being"


class IncludeZaba(Toggle):
    """Include the album Zaba in the shuffling."""
    display_name = "Include Zaba"


class IncludeShortSongs(Toggle):
    """Include short songs in the shuffling. This includes the Home Movie tracks from Dreamland if Dreamland is enabled."""
    display_name = "Include Short Songs"


@dataclass
class GlassAnimalsOptions(PerGameCommonOptions):
    include_dreamland: IncludeDreamland
    include_ilysfm: IncludeILYSFM
    include_htbahb: IncludeHTBAHB
    include_zaba: IncludeZaba
    include_short_songs: IncludeShortSongs


option_groups = [
    OptionGroup("Album Options", [
        IncludeDreamland,
        IncludeILYSFM,
        IncludeHTBAHB,
        IncludeZaba,
    ]),
    OptionGroup("Song Options", [
        IncludeShortSongs,
    ]),
]
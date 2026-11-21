from ..areas import Area
from .episode1 import CHAPTERS as EP1_CHAPTERS
from .episode2 import CHAPTERS as EP2_CHAPTERS
from .episode3 import CHAPTERS as EP3_CHAPTERS
from .episode4 import CHAPTERS as EP4_CHAPTERS
from .episode5 import CHAPTERS as EP5_CHAPTERS
from .episode6 import CHAPTERS as EP6_CHAPTERS
from .extra_toggle import PRE_RULE_OPTIMIZER as EXTRA_TOGGLE_PRE_RULE_OPTIMIZER
from .types import Chapter, RULE_OPTIMIZER

__all__ = [
    "EPISODES",
    "CHAPTERS_BY_SHORT_NAME",
    "CHAPTERS_BY_NUMBERS",
    "CHAPTERS_BY_AREA",
    "ALL_CHAPTERS",
]

EPISODES = (
    EP1_CHAPTERS,
    EP2_CHAPTERS,
    EP3_CHAPTERS,
    EP4_CHAPTERS,
    EP5_CHAPTERS,
    EP6_CHAPTERS,
)
# todo:
#  - Add more moderate logic for deflecting bolts into silver brick objects with Exploding Blaster Bolts active.
#  - Add more hard logic for deflecting bolts into silver brick objects with Exploding Blaster Bolts active, where the
#  enemies have to be pushed towards the silver bricks because they won't follow.
#  - Add more moderate/hard logic for Flutter characters being able to fly over slippery surfaces (yellow in BrickBench).
#  - Add more hard logic for Grievous wall climbing (https://youtu.be/KkGG4zZmpKk?list=PLVZqKtWzb3Ze1OySnameWsMp29o5t1bx1&t=409)
#  - Yoda Grabs also have some weird interactions with Gonk Droid, where if you swap from Yoda to Gonk droid, move with
#  Gonk Droid, and then switch back to Yoda, the Yoda-Grab occurs at the last X/Z position Yoda was at, but at the
#  current Y height. Maybe there is a use for this somewhere. It seems that if you swap with another character, then
#  this effect is lost.
#  Watto is affected similarly, but Watto allows you to swap from a Jedi character, swap to Watto, and then swap to Yoda
#  to inherit some of the glitchiness.
#  - Add more 'oil glitch' use, getting an enemy Stormtrooper to activate an Imperial panel.


CHAPTERS_BY_SHORT_NAME: dict[str, Chapter] = {
    chapter.short_name: chapter for episode in EPISODES for chapter in episode
}
CHAPTERS_BY_NUMBERS: dict[int, dict[int, Chapter]] = {
    i: {j: chapter for j, chapter in enumerate(episode, start=1)}
    for i, episode in enumerate(EPISODES, start=1)
}
CHAPTERS_BY_AREA: dict[Area, Chapter] = {
    chapter.area: chapter for episode in EPISODES for chapter in episode
}
ALL_CHAPTERS: tuple[Chapter, ...] = (
    *EP1_CHAPTERS,
    *EP2_CHAPTERS,
    *EP3_CHAPTERS,
    *EP4_CHAPTERS,
    *EP5_CHAPTERS,
    *EP6_CHAPTERS,
)

# Free up memory used by the rule optimizers.
RULE_OPTIMIZER.purge_memodict()
EXTRA_TOGGLE_PRE_RULE_OPTIMIZER.purge_memodict()

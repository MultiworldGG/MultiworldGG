from ..base_classes import D3DEpisode
from .e1l1 import E1L1
from .e1l2 import E1L2
from .e1l3 import E1L3
from .e1l4 import E1L4
from .e1l5 import E1L5
from .e1l6 import E1L6
from .e1l7 import E1L7
from .e2l1 import E2L1
from .e2l2 import E2L2
from .e2l3 import E2L3
from .e2l4 import E2L4
from .e2l5 import E2L5
from .e2l6 import E2L6
from .e2l7 import E2L7
from .e2l8 import E2L8
from .e2l9 import E2L9
from .e2l10 import E2L10
from .e2l11 import E2L11
from .e3l1 import E3L1
from .e3l2 import E3L2
from .e3l3 import E3L3
from .e3l4 import E3L4
from .e3l5 import E3L5
from .e3l6 import E3L6
from .e3l7 import E3L7
from .e3l8 import E3L8
from .e3l9 import E3L9
from .e3l10 import E3L10
from .e3l11 import E3L11
from .e4l1 import E4L1
from .e4l2 import E4L2
from .e4l3 import E4L3
from .e4l4 import E4L4
from .e4l5 import E4L5
from .e4l6 import E4L6
from .e4l7 import E4L7
from .e4l8 import E4L8
from .e4l9 import E4L9
from .e4l10 import E4L10
from .e4l11 import E4L11


class E1(D3DEpisode):
    name = "L.A. Meltdown"
    volumenum = 0
    levels = [E1L1(), E1L2(), E1L3(), E1L4(), E1L5(), E1L6(), E1L7()]
    maxlevel = 6


class E2(D3DEpisode):
    name = "Lunar Apocalypse"
    volumenum = 1
    levels = [
        E2L1(),
        E2L2(),
        E2L3(),
        E2L4(),
        E2L5(),
        E2L6(),
        E2L7(),
        E2L8(),
        E2L9(),
        E2L10(),
        E2L11(),
    ]
    maxlevel = 11


class E3(D3DEpisode):
    name = "Shrapnel City"
    volumenum = 2
    levels = [
        E3L1(),
        E3L2(),
        E3L3(),
        E3L4(),
        E3L5(),
        E3L6(),
        E3L7(),
        E3L8(),
        E3L9(),
        E3L10(),
        E3L11(),
    ]
    maxlevel = 11


class E4(D3DEpisode):
    name = "The Birth"
    volumenum = 3
    levels = [
        E4L1(),
        E4L2(),
        E4L3(),
        E4L4(),
        E4L5(),
        E4L6(),
        E4L7(),
        E4L8(),
        E4L9(),
        E4L10(),
        E4L11(),
    ]
    maxlevel = 11


all_episodes = [E1(), E2(), E3(), E4()]
all_levels = [level for ep in all_episodes for level in ep.levels]

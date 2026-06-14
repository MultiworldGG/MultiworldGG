from __future__ import annotations

from .options import Difficulty, GoldenTreasureCount
from rule_builder.rules import Has, HasGroupUnique, OptionFilter, True_
from rule_builder.field_resolvers import FromOption


has_treasures = HasGroupUnique("Golden Treasure", count=FromOption(GoldenTreasureCount))

normal_mode = True_(options=[OptionFilter(Difficulty, Difficulty.option_normal)])
hard_mode = True_(options=[OptionFilter(Difficulty, Difficulty.option_hard)])
s_hard_mode = True_(options=[OptionFilter(Difficulty, Difficulty.option_s_hard)])

can_ground_pound = Has("Progressive Ground Pound")
can_super_ground_pound = Has("Progressive Ground Pound", count=2)
can_grab = Has("Progressive Grab")
can_heavy_grab = Has("Progressive Grab", count=2)
can_swim = Has("Swim")
can_dash_attack = Has("Dash Attack")
can_stomp_jump = Has("Stomp Jump")
can_head_smash = Has("Head Smash")

from rule_builder.rules import Or, And

from ..macros import (
    CAN_GRAPPLE,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_DAMAGE_SHIELDED_DROIDEKA,
    CAN_USE_SELF_DESTRUCT,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...extras import Extra

from ....character_ability import *

R_ARENA = "Arena"

_helper = ChapterHelper(
    area=Area.JEDI,
    start_region=R_ARENA,
)

JEDI_BATTLE = _helper.make_chapter(
    regions={
        R_ARENA: (
            ExitData(
                "Chapter Completion",
                logic_options(
                    # JEDI is strictly required to free Padme/Anakin/Obi-Wan
                    # Jango's first phase requires shooting him or reflecting his bolts back at him, so ghost jedi have
                    # difficulty proceeding.
                    base=HasAbility(JEDI) & HasAnyAbilities(BLASTER | IS_NON_GHOST_JEDI),
                    # If the player only has a ghost jedi, allow Self Destruct, Super Jedi Slam,
                    # Ewok+EBB/Super Ewok Catapult.
                    normal=And(
                        HasAbility(JEDI),
                        Or(
                            HasAnyAbilities(BLASTER | IS_NON_GHOST_JEDI),
                            CAN_USE_SELF_DESTRUCT,
                            Extra.SUPER_JEDI_SLAM.has(),
                            And(
                                HasAbility(WEAPON_EWOK),
                                Extra.has_any(Extra.EXPLODING_BLASTER_BOLTS, Extra.SUPER_EWOK_CATAPULT)
                            ),
                        ),
                    ),
                    # Slam attacks with ghost jedi do work, but can be a little awkward because you have to be close,
                    # and Jango is almost constantly moving away from you.
                    moderate=HasAbility(JEDI),
                )
            ),
        ),
    },
    minikits={
        "Padmé Pillar Lower Minikit": minikit_data(
            R_ARENA,
            logic_options(
                base=HasAbility(HIGH_JUMP) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                normal=HasAbility(HIGH_JUMP),
                moderate=HasAnyAbilities(HIGH_JUMP | JEDI),
            ),
            pickup_name="m_pup7",
        ),
        "Padmé Pillar Upper Minikit": minikit_data(
            R_ARENA,
            logic_options(
                base=HasAbility(HIGH_JUMP) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                normal=HasAbility(HIGH_JUMP),
                moderate=HasAnyAbilities(HIGH_JUMP | JEDI),
            ),
            pickup_name="m_pup8",
        ),
        "Two Player Force Gate Minikit": minikit_data(
            R_ARENA,
            HasAbility(JEDI),
            pickup_name="m_pup9",
        ),
        "Anakin Pillar Lower Minikit": minikit_data(
            R_ARENA,
            logic_options(
                base=HasAnyAbilities(GRAPPLE | HIGH_JUMP) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                normal=HasAbility(HIGH_JUMP) | CAN_GRAPPLE,
                moderate=HasAnyAbilities(GRAPPLE | HIGH_JUMP | JEDI),
            ),
            pickup_name="m_pup4",
        ),
        "Anakin Pillar Upper Minikit": minikit_data(
            R_ARENA,
            logic_options(
                base=HasAnyAbilities(GRAPPLE | HIGH_JUMP) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                normal=HasAbility(HIGH_JUMP) | CAN_GRAPPLE,
                moderate=HasAnyAbilities(GRAPPLE | HIGH_JUMP | JEDI),
            ),
            pickup_name="m_pup5",
        ),
        "Obi-Wan Pillar Lower Minikit": minikit_data(
            R_ARENA,
            logic_options(
                # High jump ignores the need to grapple/imperial.
                # Grapple up and activate the Imperial panel to make the platform move.
                base=Or(
                    HasAbility(HIGH_JUMP),
                    HasAllAbilities(GRAPPLE | IMPERIAL),
                ) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                normal=HasAbility(HIGH_JUMP) | HasAllAbilities(GRAPPLE | IMPERIAL),
                moderate=HasAnyAbilities(HIGH_JUMP | JEDI) | HasAllAbilities(GRAPPLE | IMPERIAL),
            ),
            pickup_name="m_pup2",
        ),
        "Obi-Wan Pillar Upper Minikit": minikit_data(
            R_ARENA,
            # Same as the lower minikit, but use force to rebuild the second platform to go from the lower minikit
            # platform to the upper minikit platform.
            logic_options(
                base=Or(
                    HasAbility(HIGH_JUMP) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                    HasAllAbilities(GRAPPLE | IMPERIAL | JEDI),
                ),
                normal=HasAbility(HIGH_JUMP) | HasAllAbilities(GRAPPLE | IMPERIAL | JEDI),
                moderate=HasAnyAbilities(HIGH_JUMP | JEDI),
            ),
            pickup_name="m_pup3",
        ),
        "Access Hatch Minikit": minikit_data(
            R_ARENA,
            HasAllAbilities(JEDI | SHORTIE),
            pickup_name="m_pup1",
        ),
        "Rebuild Destroyed Pillar Minikit": minikit_data(
            R_ARENA,
            logic_options(
                # Force to rebuild the pillar. Sith force to make platforms. High jump to get up to the first platform.
                base=HasAllAbilities(SITH | HIGH_JUMP),
                # Force to rebuild the pillar. Then force to un-build two pieces. Double jump to the top of the
                # partially built pillar and then double jump + slam to get the minikit.
                normal=HasAbility(JEDI),
            ),
            pickup_name="m_pup6",
        ),
        "Minikit Hiding Behind Pillar": minikit_data(
            R_ARENA,
            pickup_name="m_pup10",
        )
    },
    power_brick=LocationData(
        R_ARENA,
        logic_options(
            base=HasAllAbilities(BOUNTY_HUNTER | CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
            normal=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAllAbilities(CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
        ).ror_rule(
            # Use Jango's own rockets to destroy the silver bricks.
            # If you can complete the chapter then you must have a JEDI, meaning you can jump to get the power brick.
            apply_to="moderate+",
            rule=_helper.can_reach_region("Chapter Completion"),
        ),
        er_rule=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAllAbilities(CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
    ),
)

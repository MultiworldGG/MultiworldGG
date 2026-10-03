from typing import Dict, Tuple, Union

from ..enums import ZorkGrandInquisitorLocations


missable_location_grant_conditions_data: Dict[ZorkGrandInquisitorLocations, Tuple[Union[ZorkGrandInquisitorLocations, Tuple[int, int]], ...]] = {
    ZorkGrandInquisitorLocations.BOING_BOING_BOING: (ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON,),
    ZorkGrandInquisitorLocations.BONK: (ZorkGrandInquisitorLocations.PROZORKED,),
    ZorkGrandInquisitorLocations.DEATH_ARRESTED_WITH_JACK: (ZorkGrandInquisitorLocations.ARREST_THE_VANDAL,),
    ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES: (ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES,),
    ZorkGrandInquisitorLocations.DEATH_LOST_SOUL_TO_OLD_SCRATCH: (ZorkGrandInquisitorLocations.OLD_SCRATCH_WINNER,),
    ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES: (ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES,),
    ZorkGrandInquisitorLocations.DEATH_RILED_THE_FISHWIFE: (ZorkGrandInquisitorLocations.MEAD_LIGHT_AND_PLASTIC_SIX_PACK_HOLDER,),
    ZorkGrandInquisitorLocations.DEATH_SLICED_UP_BY_THE_INVISIBLE_GUARD: (ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS,),
    ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE: (ZorkGrandInquisitorLocations.A_SMALLWAY,),
    ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON: (ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL,),
    ZorkGrandInquisitorLocations.DEATH_ZORK_ROCKS_EXPLODED: (ZorkGrandInquisitorLocations.CRISIS_AVERTED,),
    ZorkGrandInquisitorLocations.DENIED_BY_THE_LAKE_MONSTER: ((4743, 1),),
    ZorkGrandInquisitorLocations.EMERGENCY_MAGICATRONIC_MESSAGE: (ZorkGrandInquisitorLocations.ARTIFACTS_EXPLAINED,),
    ZorkGrandInquisitorLocations.FAT_LOT_OF_GOOD_THATLL_DO_YA: (ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS,),
    ZorkGrandInquisitorLocations.ITS_ALMOST_AS_IF_IT_WERE_INFINITE: (ZorkGrandInquisitorLocations.A_SMALLWAY,),
    ZorkGrandInquisitorLocations.ITS_PLAYING_A_LITTLE_HARD_TO_GET: (ZorkGrandInquisitorLocations.PROZORKED,),
    ZorkGrandInquisitorLocations.IT_DOESNT_APPEAR_TO_BE_FOOLED: (ZorkGrandInquisitorLocations.PROZORKED,),
    ZorkGrandInquisitorLocations.I_DONT_THINK_YOU_WOULDVE_WANTED_THAT_TO_WORK_ANYWAY: (ZorkGrandInquisitorLocations.PROZORKED,),
    ZorkGrandInquisitorLocations.I_SPIT_ON_YOUR_FILTHY_COINAGE: (ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS,),
    ZorkGrandInquisitorLocations.MUSHROOM_HAMMERED: (ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED,),
    ZorkGrandInquisitorLocations.NO_AUTOGRAPHS: (ZorkGrandInquisitorLocations.FIRE_FIRE,),
    ZorkGrandInquisitorLocations.NO_BONDAGE: (ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE,),
    ZorkGrandInquisitorLocations.SPELL_CHECK_COMPLETE: (ZorkGrandInquisitorLocations.IMBUE_BEBURTT,),
    ZorkGrandInquisitorLocations.TALK_TO_ME_GRAND_INQUISITOR: (ZorkGrandInquisitorLocations.FIRE_FIRE,),
    ZorkGrandInquisitorLocations.THATS_A_ROPE: (ZorkGrandInquisitorLocations.FIRE_FIRE,),
    ZorkGrandInquisitorLocations.THATS_IT_JUST_KEEP_HITTING_THOSE_BUTTONS: (ZorkGrandInquisitorLocations.ENJOY_YOUR_TRIP,),
    ZorkGrandInquisitorLocations.THATS_STILL_A_ROPE: (ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS,),
    ZorkGrandInquisitorLocations.WHAT_ARE_YOU_STUPID: (ZorkGrandInquisitorLocations.FIRE_FIRE, ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE),
    ZorkGrandInquisitorLocations.YAD_GOHDNUORGREDNU_3_YRAUBORF: (ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG,),
    ZorkGrandInquisitorLocations.YOUR_PUNY_WEAPONS_DONT_PHASE_ME_BABY: (ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO,),
    ZorkGrandInquisitorLocations.YOU_DONT_GO_MESSING_WITH_A_MANS_ZIPPER: (ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS,),
    ZorkGrandInquisitorLocations.YOU_WANT_A_PIECE_OF_ME_DOCK_BOY: (ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE,),
}

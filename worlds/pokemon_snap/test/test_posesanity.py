from .bases import PokemonSnapTestBase
from ..options import PoseSanity

class TestPoseSanity(PokemonSnapTestBase):
    options = { 
        'posesanity': PoseSanity.range_end,
        "include_rng_poses":   True,
        "include_hard_poses":  True,
    }
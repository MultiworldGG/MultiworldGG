from dataclasses import dataclass, field

@dataclass(frozen=True)
class MoveChange:
    move_name: str
    is_buff: bool
    generation: int
    power : int | None = field(default=None)
    accuracy: int | None = field(default=None)
    pp: int | None = field(default=None)

    @property
    def is_nerf(self):
        return not self.is_buff


MODERN_MOVE_CHANGES = [
    MoveChange("ABSORB", True, 4, pp=25),
    MoveChange("ACID_ARMOR", False, 6, pp=20),
    MoveChange("BARRIER", False, 6, pp=20),
    MoveChange("BIND", True, 5, accuracy=85),
    MoveChange("BLIZZARD", False, 6, power=110),
    MoveChange("BONE_RUSH", True, 5, accuracy=90),
    MoveChange("BUBBLE", True, 6, power=40),
    MoveChange("CLAMP", True, 5, pp=15, accuracy=85),
    MoveChange("COTTON_SPORE", True, 5, accuracy=100),
    MoveChange("CRABHAMMER", True, 5, accuracy=90),
    MoveChange("CRABHAMMER", True, 6, power=100),
    MoveChange("DIG", True, 4, power=80),
    MoveChange("DISABLE", True, 4, accuracy=80),
    MoveChange("DISABLE", True, 5, accuracy=100),
    MoveChange("FIRE_BLAST", False, 6, power=110),
    MoveChange("FIRE_SPIN", True, 5, power=35, accuracy=85),
    MoveChange("FLAMETHROWER", False, 6, power=90),
    MoveChange("FLASH", True, 4, accuracy=100),
    MoveChange("FLY", True, 4, power=90),
    MoveChange("FURY_CUTTER", True, 5, power=20),
    MoveChange("FURY_CUTTER", True, 6, power=40),
    MoveChange("FUTURE_SIGHT", True, 5, power=100, accuracy=100),
    MoveChange("FUTURE_SIGHT", True, 5, power=120),
    MoveChange("GIGA_DRAIN", True, 4, pp=10),
    MoveChange("GIGA_DRAIN", True, 5, power=75),
    MoveChange("GLARE", True, 5, accuracy=90),
    MoveChange("GLARE", True, 6, accuracy=100),
    MoveChange("HI_JUMP_KICK",True, 4, power=100),
    MoveChange("HI_JUMP_KICK", True, 5, power=130),
    MoveChange("HYDRO_PUMP", False, 6, power=110),
    MoveChange("ICE_BEAM", False, 6, power=90),
    MoveChange("JUMP_KICK", True, 5, power=85),
    MoveChange("JUMP_KICK", True, 6, power=100),
    MoveChange("LEECH_LIFE", True, 7, power=80),
    MoveChange("LEECH_LIFE", False, 7, pp=10),
    MoveChange("LICK", True, 6, power=30),
    MoveChange("MEGA_DRAIN", True, 4, pp=15),
    MoveChange("MILK_DRINK", False, 9, pp=5),
    MoveChange("MINIMIZE", False, 6, pp=10),
    MoveChange("OUTRAGE", True, 4, power=120),
    MoveChange("PETAL_DANCE", True, 4, power=90),
    MoveChange("PETAL_DANCE", True, 5, power=120),
    MoveChange("PETAL_DANCE", False, 5, pp=10),
    MoveChange("PIN_MISSILE", True, 6, power=25, accuracy=95),
    MoveChange("POISON_GAS", True, 5, accuracy=80),
    MoveChange("POISON_GAS", True, 6, accuracy=90),
    MoveChange("PSYWAVE", True, 6, accuracy=100),
    MoveChange("RAPID_SPIN", True, 8, power=50),
    MoveChange("RAZOR_WIND", True, 3, accuracy=100),
    MoveChange("RECOVER", False, 4, pp=10),
    MoveChange("RECOVER", False, 9, pp=5),
    MoveChange("REST", False, 9, pp=5),
    MoveChange("ROCK_SMASH", True, 4, power=40),
    MoveChange("SCARY_FACE", True, 5, accuracy=100),
    MoveChange("SKULL_BASH", True, 6, power=130),
    MoveChange("SMOG", True, 6, power=30),
    MoveChange("SNORE", True, 6, power=50),
    MoveChange("SUBMISSION", False, 6, pp=20),
    MoveChange("SURF", False, 6, power=90),
    MoveChange("SWAGGER", False, 7, accuracy=85),
    MoveChange("SWORDS_DANCE", False, 6, pp=20),
    MoveChange("TACKLE", True, 5, power=50, accuracy=100),
    MoveChange("TACKLE", False, 7, power=40),
    MoveChange("THIEF", True, 6, power=60, pp=25),
    MoveChange("THRASH", True, 5, power=120),
    MoveChange("THRASH", False, 5, pp=10),
    MoveChange("THUNDER", False, 6, power=110),
    MoveChange("THUNDER_WAVE", False, 7, accuracy=90),
    MoveChange("THUNDERBOLT", False, 6, power=90),
    MoveChange("TOXIC", True, 5, accuracy=90),
    MoveChange("VINE_WHIP", True, 4, pp=15),
    MoveChange("VINE_WHIP", True, 6, power=45, pp=25),
    MoveChange("WHIRLPOOL", True, 5, power=35, accuracy=85),
    MoveChange("WRAP", True, 5, accuracy=90),
    MoveChange("ZAP_CANNON", True, 4, power=120)
]
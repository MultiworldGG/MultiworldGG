"""This module contains the data class for Memory Address data"""
from dataclasses import dataclass

from worlds.rac3.constants.check_type import CHECKTYPE
from worlds.rac3.constants.data.item import non_prog_weapon_data
from worlds.rac3.constants.status import RAC3STATUS


@dataclass
class RAC3ADDRESSDATA:
    """Memory Address data"""
    ADDRESS: int
    TYPE: CHECKTYPE
    VALUE: int

    def __init__(self, data: tuple[int, CHECKTYPE, int] = (0, CHECKTYPE.SKIP, 0)):
        """Memory Address data
        :param data:
        :rtype: RAC3ADDRESSDATA
        """
        self.ADDRESS, self.TYPE, self.VALUE = data

    def check_condition(self, value: int) -> bool:
        """Check if value meets the condition

        :param value:
        """
        match self.TYPE & CHECKTYPE.SIGN:
            case CHECKTYPE.EQ:
                return value == self.VALUE
            case CHECKTYPE.NEQ:
                return value != self.VALUE
            case CHECKTYPE.GT:
                return value > self.VALUE
            case CHECKTYPE.LT:
                return value < self.VALUE
            case CHECKTYPE.GE:
                return value >= self.VALUE
            case CHECKTYPE.LE:
                return value <= self.VALUE
        raise Exception(f'Incorrect CheckType for this operation, {self.TYPE} cannot be compared')


SAVE_DATA: list[RAC3ADDRESSDATA] = [
    # Player Stats
    RAC3ADDRESSDATA((RAC3STATUS.HEALTH, CHECKTYPE.BYTE, 10)),
    RAC3ADDRESSDATA((RAC3STATUS.MAX_HEALTH, CHECKTYPE.BYTE, 10)),
    RAC3ADDRESSDATA((RAC3STATUS.NANOTECH_EXP, CHECKTYPE.INT, 0)),
    RAC3ADDRESSDATA((RAC3STATUS.BOLTS, CHECKTYPE.INT, 0)),
    RAC3ADDRESSDATA((RAC3STATUS.CRYSTALS_TRADED, CHECKTYPE.BYTE, 0)),
    RAC3ADDRESSDATA((RAC3STATUS.CRYSTALS_CURRENT, CHECKTYPE.BYTE, 0)),
    *[RAC3ADDRESSDATA((weapon.AMMO_ADDRESS, CHECKTYPE.INT, weapon.AMMO)) for weapon in non_prog_weapon_data.values()],
    *[RAC3ADDRESSDATA((weapon.XP_ADDRESS, CHECKTYPE.INT, 0)) for weapon in non_prog_weapon_data.values()],
    *[RAC3ADDRESSDATA((weapon.LEVEL_ADDRESS, CHECKTYPE.BYTE, weapon.ID)) for weapon in non_prog_weapon_data.values()],
    # Stored Fillers
    RAC3ADDRESSDATA((RAC3STATUS.BOLT_PACKS, CHECKTYPE.INT, 0)),
    RAC3ADDRESSDATA((RAC3STATUS.NANOTECH_EXP_PACKS, CHECKTYPE.INT, 0)),
    RAC3ADDRESSDATA((RAC3STATUS.JACKPOT_PACKS, CHECKTYPE.INT, 0)),
    RAC3ADDRESSDATA((RAC3STATUS.WEAPON_LEVEL_PACKS, CHECKTYPE.INT, 0)),
    # Gameplay Progress
    RAC3ADDRESSDATA((RAC3STATUS.ROBONOIDS, CHECKTYPE.BYTE, 0)),
]

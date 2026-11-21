from dataclasses import dataclass

from ..extras import Extra

from . import EXTRA_ITEMS_BASE, GenericItemData


# Populated by the construction of EXTRA_DATA below, and then used to maintain singletons.
_ALL_EXTRA_DATA_SINGLETONS_CREATED = False
_EXTRA_TO_EXTRA_DATA: "dict[Extra, ExtraData]" = {}


@dataclass(frozen=True)
class ExtraData(GenericItemData):
    extra: Extra
    item_type = "Extra"
    
    def __post_init__(self):
        if _ALL_EXTRA_DATA_SINGLETONS_CREATED:
            # A new ExtraData is being created after the point at which all ExtraData should have been created. This is
            # an error.
            raise KeyError(f"No ExtraData exists for Extra {self.extra}")

    @classmethod
    def from_extra(
            cls,
            extra: Extra
    ):
        if extra in _EXTRA_TO_EXTRA_DATA:
            return _EXTRA_TO_EXTRA_DATA[extra]
        else:
            new = cls(
                code=extra + EXTRA_ITEMS_BASE,
                name=extra.readable_name,
                extra=extra,
            )
            _EXTRA_TO_EXTRA_DATA[extra] = new
            return new


EXTRA_DATA: list[ExtraData] = [
    ExtraData.from_extra(extra) for extra in Extra if extra.is_purchasable() and not extra.is_score_multiplier()
]
# All creation of ExtraData singletons is now complete, no more should be created.
_ALL_EXTRA_DATA_SINGLETONS_CREATED = True

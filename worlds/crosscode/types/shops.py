import typing
from dataclasses import dataclass

from .locations import AccessInfo
from .metadata import IncludeOptions


@dataclass
class ShopData:
    internal_name: str
    name: str
    access: AccessInfo
    metadata: typing.Optional[IncludeOptions] = None

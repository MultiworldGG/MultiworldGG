from dataclasses import dataclass
from typing import Optional
from BaseClasses import ItemClassification as ItCl


@dataclass(frozen=True)
class Itm:
    name: str
    valid: bool = True
    count: int = 1
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None
    progression: ItCl = ItCl.filler
    type_count: int = 1
    required: bool = False

    def get_item(self) -> str:
        if self.prefix is None:
            return self.name
        return f"{self.prefix}: {self.name}"

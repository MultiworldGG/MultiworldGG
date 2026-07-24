from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Loc:
    name: str
    valid: bool = True
    rules: list[str] = field(default_factory=lambda: [])
    depends: list[str] = field(default_factory=lambda: [])
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None
    required: bool = False
    pooled: bool = True

    def get_location(self) -> str:
        return f"{self.prefix}: {self.name}"

    def get_region(self) -> str:
        return "+".join(sorted(self.rules))

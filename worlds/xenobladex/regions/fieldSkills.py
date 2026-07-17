from typing import List
from ..Regions import Requirement as Req, Rule


def generate_field_skill_region(field_skill: str) -> List[Rule]:
    return [Rule("Menu"), *(Rule(f"{field_skill} {i}", {Req(f"FLDSK: {field_skill}", i - 1)}) for i in range(1, 6))]


field_skill_regions: List[Rule] = [
    *generate_field_skill_region("Mechanical"),
    *generate_field_skill_region("Biological"),
    *generate_field_skill_region("Archeological")
]

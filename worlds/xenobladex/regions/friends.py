from typing import List
from ..Regions import Requirement as Req, Rule


def generate_friend_region(friend: str) -> List[Rule]:
    return [Rule("Menu"), *(Rule(f"{friend} {i}", {Req(f"FRD: {friend}", i)}) for i in range(1, 6))]


friends_regions: List[Rule] = [
    *generate_friend_region("Nagi"),
    *generate_friend_region("L"),
    *generate_friend_region("Lao"),
    *generate_friend_region("HB"),
    *generate_friend_region("Gwin"),
    *generate_friend_region("Frye"),
    *generate_friend_region("Doug"),
    *generate_friend_region("Yelv"),
    *generate_friend_region("Boze"),
    *generate_friend_region("Phog"),
    *generate_friend_region("Elma"),
    *generate_friend_region("Lin"),
    *generate_friend_region("Celica"),
    *generate_friend_region("Irina"),
    *generate_friend_region("Murderess"),
    *generate_friend_region("Alexa"),
    *generate_friend_region("Hope"),
    *generate_friend_region("Mia")
]

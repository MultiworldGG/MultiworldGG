
from dataclasses import dataclass


@dataclass(frozen=True)
class Crd:
    r1: int = 0
    r2: int = 0
    r3: int = 0
    r4: int = 0
    r5: int = 0
    r6: int = 0
    dp: int = 0
    b1: int = 0
    b2: int = 0
    mech: int = 1


fnet_credits_data: dict[int, list[Crd]] = {
    15: [
        Crd(mech=3),
        Crd(r1=1, mech=2),
        Crd(r2=1, mech=2),
        Crd(r3=1, mech=2),
        Crd(r4=1, mech=2),
        Crd(r5=1, mech=2),
        Crd(r6=1, mech=2),
    ],
    # Need improvement but too difficult for too little gain right now
    70: [
        Crd(r1=3, r2=4, r3=2, r4=6, r5=7, r6=3, dp=4, b1=3, b2=3),
        Crd(r6=2, dp=1, b2=1, mech=3),
    ],
    130: [
        Crd(r6=2, dp=1, b2=2, mech=3),
    ]
}

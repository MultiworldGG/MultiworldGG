from dataclasses import dataclass

from ..constants.options import Rac5Options


@dataclass(slots=True)
class ClientOptions:
    clank_pack_enabled: bool = False
    clank_enabled: bool = True
    clank_all_challenges: bool = False
    skyboard_enabled: bool = False
    shrink_ray_skips_enabled: bool = False
    shrink_ray_locations_enabled: bool = False
    skill_points_enabled: bool = False
    weapon_level_checks_enabled: bool = False
    nanotech_level_checks_enabled: bool = False
    progressive_challenge_mode_enabled: bool = False
    all_missions_enabled: bool = True
    all_cutscenes_enabled: bool = False

    @classmethod
    def from_slot_data(cls, data):
        clank = int(data.get(Rac5Options.CLANK_CHALLENGES, 1))
        shrink = int(data.get(Rac5Options.SHRINK_RAY_OPTIONS, 1))
        return cls(
            clank_pack_enabled=bool(data.get(Rac5Options.CLANK_PACK, False)),
            clank_enabled=clank >= 1,
            clank_all_challenges=clank >= 2,
            skyboard_enabled=int(data.get(Rac5Options.SKYBOARD_CHALLENGES, 0)) >= 1,
            shrink_ray_skips_enabled=shrink == 2,
            shrink_ray_locations_enabled=shrink == 1,
            skill_points_enabled=(
                int(data.get(Rac5Options.SKILL_POINTS, 0)) >= 1
                or bool(data.get(Rac5Options.ENABLE_CLANK_CHALLENGE_SKILL_POINTS, False))
                or bool(data.get(Rac5Options.ENABLE_SKYBOARD_CHALLENGE_SKILL_POINTS, False))
            ),
            weapon_level_checks_enabled=int(data.get(Rac5Options.WEAPON_LEVEL_CHECKS, 0)) >= 1,
            nanotech_level_checks_enabled=int(data.get(Rac5Options.NANOTECH_LEVEL_INTERVAL, 0)) > 0,
            progressive_challenge_mode_enabled=bool(data.get(Rac5Options.PROGRESSIVE_CHALLENGE_MODE, False)),
            all_missions_enabled=bool(data.get(Rac5Options.ALL_MISSIONS, True)),
            all_cutscenes_enabled=bool(data.get(Rac5Options.ALL_CUTSCENES, False)),
        )


class ClientOption:
    """Keep existing client integrations backed by the single option snapshot."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance.options, self.name)

    def __set__(self, instance, value):
        setattr(instance.options, self.name, value)

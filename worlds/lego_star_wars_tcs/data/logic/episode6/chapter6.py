from rule_builder.rules import True_, Or

from ..option_filters import logic_options
from ..rules import HasAbility
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

from ....character_ability import IS_A_VEHICLE

R_STAR_DESTROYER_BATTLE = "Star Destroyer Battle"
R_STAR_DESTROYER_BATTLE_MINIKITS = "Star Destroyer Battle Minikits"
R_INTO_THE_DEATH_STAR_II = "Into The Death Star II"
R_AFTER_FORCE_FIELD = "After Force Field"
R_REACTOR_CORE = "Reactor Core"
R_ESCAPE_PART_1 = "Escape Part 1"
R_ESCAPE_PART_2 = "Escape Part 2"
R_ESCAPE_PART_3 = "Escape Part 3"


INTO_THE_DEATH_STAR = Chapter(
    area=Area.DEATHSTAR2BATTLE,
    start_region=R_STAR_DESTROYER_BATTLE,
    extra_entrance_rules=HasAbility(IS_A_VEHICLE),
    regions={
        R_STAR_DESTROYER_BATTLE: (
            ExitData(
                R_STAR_DESTROYER_BATTLE_MINIKITS,
                logic_options(
                    base=HasAbility(VEHICLE_BLASTER),
                    # These are quite easy to destroy by deflecting enemy bolts into them, or shooting torpedoes into
                    # them.
                    normal=HasAbility(VEHICLE_BLASTER) | Extra.has_any(Extra.DEFLECT_BOLTS, Extra.INFINITE_TORPEDOS),
                )
            ),
            ExitData(
                R_INTO_THE_DEATH_STAR_II,
                logic_options(
                    base=HasAbility(VEHICLE_BLASTER),
                    normal=HasAbility(VEHICLE_BLASTER) | Extra.INFINITE_TORPEDOS.has(),
                    # It is theoretically possible to kill TIE Bombers with Deflect Bolts and use the torpedoes they
                    # drop to progress, but good luck with that.
                ),
                new_level=Level.DEATHSTAR2BATTLE_B,
            ),
        ),
        R_STAR_DESTROYER_BATTLE_MINIKITS: (),
        R_INTO_THE_DEATH_STAR_II: (
            ExitData(
                R_AFTER_FORCE_FIELD,
                # Torpedoes from the dispenser are all that are needed.
                True_(),
                new_level=Level.DEATHSTAR2BATTLE_C,
            ),
        ),
        R_AFTER_FORCE_FIELD: (
            ExitData(
                R_REACTOR_CORE,
                # Torpedoes from the dispenser are all that are needed.
                True_(),
                new_level=Level.DEATHSTAR2BATTLE_D,
            ),
        ),
        R_REACTOR_CORE: (
            ExitData(
                R_ESCAPE_PART_1,
                # Shoot all the shield generators on the wall (possible with torpedoes, but the hitboxes are annoying).
                # Once all shield generators are destroyed, there is a housing around the reactor core that must be shot
                # (torpedoes do not appear to work). Deflect Bolts works okay for this.
                # Deflect-Bolts-only would be theoretically possible, but you cannot get close to the shield generators
                # because they push you away when you get close, so using Deflect Bolts to destroy them is heavily RNG
                # dependent.
                logic_options(
                    base=True_(),
                    normal=HasAbility(VEHICLE_BLASTER),
                    # Allow Infinite Torpedos [sic] and Deflect Bolts.
                    moderate=Or(
                        HasAbility(VEHICLE_BLASTER),
                        Extra.has_all(Extra.INFINITE_TORPEDOS, Extra.DEFLECT_BOLTS),
                    ),
                    # Technically, instead of Infinite Torpedos [sic], you could repeatedly go back and forth between
                    # the Reactor Core area and the previous area, going all the way back to the torpedo dispenser, but
                    # that sounds way too tedious, especially when there are 6 generators to destroy and hitting them
                    # with torpedoes is a pain enough even with Infinite Torpedos [sic], so I don't think even Super
                    # Expert logic should expect doing this. If this was to be expected in higher logic, then I think
                    # that the logic should at least require a vehicle that can carry 5 torpedoes, to reduce the number
                    # of trips.
                ).and_rule(
                    # Without being able to shoot, you will likely crash into many obstacles, slowing you down and
                    # causing you to die over and over, so moderate logic is expecting either a blaster vehicle to shoot
                    # the obstacles or invincibility to be immune to the explosion. This also helps make the escape
                    # sequence minikits a lot easier.
                    apply_to="moderate",
                    rule=HasAbility(VEHICLE_BLASTER) | Extra.INVINCIBILITY.has(),
                ),
                new_level=Level.DEATHSTAR2BATTLE_E
            ),
        ),
        R_ESCAPE_PART_1: (
            ExitData(R_ESCAPE_PART_2, new_level=Level.DEATHSTAR2BATTLE_F),
        ),
        R_ESCAPE_PART_2: (
            ExitData(R_ESCAPE_PART_3, new_level=Level.DEATHSTAR2BATTLE_G),
        ),
        R_ESCAPE_PART_3: (
            ExitData("Chapter Completion"),
        ),
    },
    minikits={
        "Front Start Destroyer Minikit": minikit_data(
            R_STAR_DESTROYER_BATTLE_MINIKITS,
            pickup_name="m_pup2",
        ),
        "Rear Start Destroyer Minikit": minikit_data(
            R_STAR_DESTROYER_BATTLE_MINIKITS,
            pickup_name="m_pup1",
        ),
        "Torpedo Pipes Minikit": minikit_data(
            R_INTO_THE_DEATH_STAR_II,
            # There is a torpedo dispenser, and Base logic, which would expect fighting the turrets, requires a Blaster
            # vehicle to reach here, so there are no extra requirements.
            # The minikit is granted by going near it, there is no requirement to shoot it to get it.
            pickup_name="m_pup3",
        ),
        "First TIE Gate Minikit": minikit_data(
            R_INTO_THE_DEATH_STAR_II,
            # There is a giant collision wall going up above the TIE gate, so skipping this one would need a clip.
            logic_options(
                base=HasAbility(VEHICLE_TIE),
                # You can shoot through the gate with torpedoes and hit the minikit.
                # Expect Infinite Torpedos [sic] for Moderate logic.
                # Vehicles with higher idle movement speed tend to be more difficult because you cannot spend as long
                # lining up your shot.
                # Vehicles with visually larger torpedoes tend to be more difficult because you fire torpedoes from the
                # back of the line of torpedoes, which are further away from the player the larger the torpedoes are.
                # When Infinite Torpedos [sic] is active, this can be mitigated by toggling the Extra on and off.
                moderate=HasAbility(VEHICLE_TIE) | Extra.INFINITE_TORPEDOS.has(),
                # Learn where to shoot the torpedoes, or go back for more torpedoes when running out.
                hard=True_(),
            ),
            pickup_name="m_pup4",
        ),
        "Hidden Corner Path Minikit": minikit_data(
            R_AFTER_FORCE_FIELD,
            # The minikit is granted by going near it.
            pickup_name="m_pup5",
        ),
        "Second TIE Gate Minikit": minikit_data(
            R_AFTER_FORCE_FIELD,
            logic_options(
                base=HasAbility(VEHICLE_TIE),
                # You can shoot the minikit through the TIE gate fairly easily with a torpedo.
                # Moderate is expecting Infinite Torpedos [sic], but this is easier than it may seem, so this logical
                # requirement could be removed.
                moderate=HasAbility(VEHICLE_TIE) | Extra.INFINITE_TORPEDOS.has(),
                # Go back and get more torpedoes if you miss.
                hard=True_(),
                # I have also managed to shoot this minikit from outside the gate with Slave 1 while doing 1P2C somehow.
            ),
            pickup_name="m_pup6",
        ),
        "Reactor Core Minikit": minikit_data(
            R_REACTOR_CORE,
            # Driving into the minikit collects it.
            True_(),
            pickup_name="m_pup7",
        ),
        "Escape Minikit 1": minikit_data(
            R_ESCAPE_PART_1,
            # Driving into the minikit collects it.
            True_(),
            pickup_name="m_pup8",
        ),
        "Escape Minikit 2": minikit_data(
            R_ESCAPE_PART_2,
            # Driving into the minikit collects it.
            True_(),
            pickup_name="m_pup9",
        ),
        "Escape Minikit 3": minikit_data(
            R_ESCAPE_PART_3,
            # Driving into the minikit collects it.
            True_(),
            pickup_name="m_pup10",
        )
    },
    power_brick=LocationData(
        R_REACTOR_CORE,
        # Torpedoes only spawn in this area once you've destroyed all the shield generators and the reactor core
        # housing, but you can go back to the previous area and pick up torpedoes from there.
        True_(),
    ),
)

import asyncio
import logging
import time
from enum import IntEnum
from random import Random

from Utils import async_start

from . import ClientComponent
from .studs import give_studs
from ..common import StaticUint, FloatField
from ..common_addresses import (
    CURRENT_AREA_ADDRESS,
    player_character_entity_iter,
    CHARACTER_CHARACTER_DATA_POINTER,
    CHARACTER_DATA_ID,
)
from ..custom_save_data import CustomSaveFlags1
from ..events import (
    subscribe_event,
    OnReceiveSlotDataEvent,
    OnGameWatcherTickEvent,
    OnAreaChangeEvent,
    OnPlayerCharacterIdChangeEvent,
)
from ..type_aliases import TCSContext

from ...data.areas import Area
from ...data.characters import Character, UnlockMethod
from ...data.items.all_character_items import CHARACTER_TO_ITEM_DATA
from ...slot_data import EnabledFeature

_DEBUG_LOGGER = logging.getLogger("TCS Debug")

# Currently, all characters are allowed to be killed because the client sets the respawn timer before killing the
# character.
_DISALLOWED_DEATH_CHARACTER_IDS = frozenset()


# Player death count in the current area. Resets to zero upon area change.
_PLAYER_DEATH_COUNT_IN_CURRENT_AREA = StaticUint(0x951244)
# Player death count in the current level. Resets to zero upon level change.
# _PLAYER_DEATH_COUNTER_IN_CURRENT_LEVEL = StaticUint(0x87b2f0)


# Flags for the currently active 'cheats' (Extras).
_CHEAT_FLAGS = StaticUint(0x950dac)
# For some reason, if the in-area death count is 0, but flag cheat 0x2000 is active, then the in-area death count is
# increased to 1.
_CHEAT_FLAGS_STARTING_DEATH_COUNT = 0x2000


# There are a maximum of 8 playable characters in a level, pointers to their 'character entity' objects are in an
# entity*[8] array at this address.
_PLAYER_CHARACTER_POINTERS_ARRAY_ADDRESS = 0x93d810


_VEHICLE_AMNESTY_AREAS = frozenset({
    Area.PURSUIT,
    Area.GUNSHIP,
    Area.DEATHSTARBATTLE,
    Area.HOTHBATTLE,
    Area.ASTEROIDCHASE,
    Area.DEATHSTAR2BATTLE,
    Area.PODRACE,
    Area.ANAKINSFLIGHT,
    Area.BONUS_GUNSHIP,
})


_DEATH_COOLDOWN = 2.25
"""
Respawn is typically 2.0s, so ignore any deaths to send or receive within just above this time.
If something goes horrendously wrong with this Death Link implementation, this has the added benefit of
limiting death spam.
"""


class _CharacterActionState(IntEnum):
    """The current action a character is undergoing. The real name of the type itself is unknown."""
    # # Original name "NoContext" is converted to NO_CONTEXT for enum names. Other names follow the same pattern.
    # JUMP = 0x0
    # LAND_JUMP = 0x1  # Landing from a normal jump
    # LAND_JUMP_2 = 0x2
    # LAND_FLIP = 0x3
    # LAND_COMBO_JUMP = 0x4
    # COMBO = 0x5  # Lightsaber basic (combo) attack
    # WEAPON_IN = 0x6  # Putting weapon away
    # WEAPON_OUT = 0x7  # Getting weapon out
    # FORCE = 0x8
    # COMBO_ROTATE = 0x9  # Unknown use
    # SHOOT = 0xa
    # INTERFACE = 0xb  # Interacting with a Bounty Hunter/Astromech/Protocol/Imperial panel
    # BLOCK = 0xc  # Unknown use
    # LAND_LUNGE = 0xd  # Landing from Jedi single-jump attack
    # LAND_SLAM = 0xe  # Jedi slam attack
    TELEPORT = 0xf  # Crawling through a vent
    # SWIPE = 0x10  # Lightsaber 'backwards attack' when an enemy is directly behind the character
    # TUBE = 0x11  # Floating in an updraft (internally, updrafts are called tubes)
    # FORCE_THROW = 0x12  # Unknown use, perhaps not implemented
    # HOVER_UP = 0x13  # Unknown use
    # ROCKET = 0x14  # Firing a Bounty Hunter Rocket from the Bounty Hunter Rockets Extra
    # TAKE_HIT = 0x15
    # ZAP = 0x16  # Astromech/jawa zap
    # DEACTIVATED = 0x17  # Zapped or force confused, also seen sometimes when exiting vehicles
    # HOLD = 0x18  # Blocking with a melee weapon
    # LAND_SPECIAL = 0x19
    # COMMUNICATE = 0x1a  # Using a Walkie Talkie (Battle Droid (Commander)/Imperial Spy)
    # FORCE_PUSH = 0x1b  # Using force lightning/choke/confusion
    # FORCE_PUSHED = 0x1c  # Held by force lightning/choke or pushed by force as a droid
    # FORCE_DEFLECT = 0x1d  # Unknown use
    # FORCE_FROZEN = 0x1e  # Unknown use
    # BIG_JUMP = 0x1f  # Force Grapple Leap jump
    # BACK_FLIP = 0x20  # General Grievous' backflip
    # RECOIL = 0x21  # Unknown use, looks like being pushed backwards by something, maybe an air vent
    # FORCED_BACK = 0x22  # Unknown use, looks the same as RECOIL
    # # Unknown use, perhaps for an older drop-in implementation. Jedi go into a blocking animation. Characters
    # # sometimes instantly shrink tiny and then scale up to normal over time.
    # DROP_IN = 0x23
    # DROP_OUT = 0x24  # Unknown use, teleports P1 to P2 or vice versa
    # DODGE = 0x25  # When a blaster character performs a sidestep dodge of incoming blaster fire
    # PUNCH = 0x26  # Non Jedi (non-combo?) melee attacking
    # PUSH = 0x27  # Pushing a block
    # PUSH_SPINNER = 0x28  # Pushing a rotatable object
    # LAND_COMBAT_ROLL = 0x29  # Landing from a blaster character's roll, also used by Stormtroopers when they flop
    # TURN = 0x2a  # Vehicle 180 degree turn around

    DOOMED = 0x2b  # Falling death, body parts fall through the floor, seems to work on vehicles too

    # LAUNCH = 0x2c  # Suspected to be grabbed by a crane's claw, makes the character appear to be falling
    # BUILD_IT = 0x2d  # Building bricks. Crashes if used incorrectly.
    # THROW_DETONATOR = 0x2c  # Throwing a thermal detonator
    # GRABBED = 0x2f  # Unknown use
    # SPECIAL_MOVE_VICTIM = 0x30  # Unknown use
    # ROLL = 0x31  # Droideka roll movement
    # UN_ROLL = 0x32  # Droideka unrolling into standing pose
    # SLIDE = 0x33  # Sliding down a slippery surface, e.g. ice in 5-2
    # BEEN_DRAGGED = 0x34  # Unknown use
    # ZIP_DOWN = 0x35  # Unknown use
    # LOOP = 0x36  # Vehicle loop in-place
    # POO = 0x37  # Make ridden animal poo when the Fertilizer Extra is enabled
    # GRAB = 0x38  # Unknown use
    # EATEN = 0x39  # Unknown use, maybe Rancor related, makes the character disappear
    # BARREL_ROLL = 0x3a  # Vehicle aileron roll that is commonly mistakenly called a barrel roll
    # BEEN_TAKEN_OVER = 0x3b  # Getting into a vehicle/turret (I'm guessing this is the state the vehicle enters?)
    # GET_IN = 0x3c  # Getting into a vehicle/turret (I'm guessing this is the state the non-vehicle enters?)
    # FLATTEN = 0x3d  # Flattened by a vehicle
    # # Used by the vehicle in 5-2 that C-3PO is supposed to stand on the back of and then get launched by the vehicle,
    # # like a bucking horse.
    # BUCK = 0x3e
    # EAT = 0x3f
    # DISORIENTATE = 0x40
    # ACTIVE = 0x41  # Seen very briefly sometimes when getting into vehicles
    # ZAPPED_BY_FLOOR = 0x42
    # CLIMB = 0x43  # Probably specific to the incomplete Lego Batman 1 demo
    # TIGHTROPE = 0x44  # Probably specific to the incomplete Lego Batman 1 demo
    # WALL_SHUFFLE = 0x45  # Probably specific to the incomplete Lego Batman 1 demo
    # GRAPPLE = 0x46  # Maybe specific to the incomplete Lego Batman 1 demo
    # ZIP_UP = 0x47  # Using a grapple point with a grapple character
    # PLACE_DETONATOR = 0x48  # Probably specific to the incomplete Lego Batman 1 demo
    # PICK_UP_DETONATOR = 0x49  # Probably specific to the incomplete Lego Batman 1 demo
    # PULL_LEVER = 0x4a  # Pulling a lever

    # These are probably all specific to the incomplete Lego Batman 1 demo:
    # FLOAT = 0x4b
    # SIGNAL = 0x4c  # Crashes if used incorrectly.
    # BATARANG = 0x4d
    # HANG = 0x4e
    # GLIDE = 0x4f
    # CATCH = 0x50
    # TECHNO = 0x51
    # ATTRACTO_TARGET = 0x52
    # ATTRACTO_DEPOSIT = 0x53
    # SONAR = 0x54
    # Moves the character very fast towards an unknown part of the current level, colliding and possibly getting stuck
    # on objects (maybe towards (0, 0, 0)?).
    # LEDGE_TERRAIN = 0x55
    # TRANSFORM = 0x56
    # WALL_JUMP_WAIT = 0x57
    # SUPER_CARRY = 0x58
    # PUSH_OBSTACLE = 0x59
    # STUNNED = 0x5a
    # LEDGE = 0x5b
    # SECURITY = 0x5c  # Crashes if used incorrectly.
    # BALLOONING = 0x5d
    # THROW_QUICK = 0x5e

    DIE_AIR = 0x5f  # Throw death from Force Lightning/Choke. Notably, the spawned body parts have physics.
    # DIE_GROUND = 0x60  # Unknown use
    # HAT_MACHINE = 0x61  # Using a Hat Machine. This is used by both characters that can and cannot wear hats.

    # These are probably specific to the incomplete Lego Indiana Jones 1 demo:
    # WHIP = 0x62
    # NET_WAIT = 0x63
    # NO_CONTEXT = 0xFF  # Idle

    @staticmethod
    def _get(ctx: TCSContext, character_address: int) -> int:
        return ctx.read_uchar(character_address + 0x7b5, raw=True)

    # @classmethod
    # def get(cls, ctx: TCSContext, character_address: int):
    #     return cls(ctx.read_uchar(character_address + 0x7b5, raw=True))

    def set(self, ctx: TCSContext, character_address: int):
        ctx.write_byte(character_address + 0x7b5, self.value, raw=True)

    def is_set(self, ctx: TCSContext, character_address: int) -> bool:
        return self._get(ctx, character_address) == self.value


class _CharacterDeathState(IntEnum):
    ALIVE = 0
    UNKNOWN_BUT_ALSO_DEAD = 1
    DEAD = 2

    @classmethod
    def get(cls, ctx: TCSContext, character_address: int):
        return cls(ctx.read_uchar(character_address + 0x28b, raw=True))

    def set(self, ctx: TCSContext, character_address: int):
        ctx.write_byte(character_address + 0x28b, self.value, raw=True)


_CHARACTER_RESPAWN_TIMER = FloatField(0x1010)
"""
Usually set by the game when a player dies, but can be set manually before killing a player, to make them wait a
different amount of time before they respawn, so long as it is set greater than 0.0
"""

_PLAYER_SPECIFIC_VEHICLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias}'s P{player} crashed their {character}",
    "{alias}'s P{player}'s {character} crashed",
    "{alias}'s P{player}'s {character} exploded",
)
_VEHICLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias} crashed their {character}",
    "{alias}'s {character} crashed",
    "{alias}'s {character} exploded",
)
_PLAYER_SPECIFIC_NON_VEHICLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias}'s P{player} broke their {character} minifigure",
    "{alias}'s P{player}'s {character} minifigure broke",
)
_NON_VEHICLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias} broke their {character} minifigure",
    "{alias}'s {character} minifigure broke",
)
_PLAYER_SPECIFIC_STATIONARY_RIDABLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias}'s P{players}'s {character} exploded",
)
_STATIONARY_RIDABLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias}'s {character} exploded",
)
_PLAYER_SPECIFIC_FALLBACK_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias}'s P{player} lost their studs",
)
_PLAYER_SPECIFIC_ANIMAL_RIDABLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias}'s P{player} broke their {character} minifigure",
    "{alias}'s P{player}'s {character} minifigure broke",
    "{alias}'s P{player}'s {character} died",
)
_ANIMAL_RIDABLE_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias} broke their {character} minifigure",
    "{alias}'s {character} minifigure broke",
    "{alias}'s {character} died",
)
_FALLBACK_DEATH_MESSAGES: tuple[str, ...] = (
    "{alias} lost their studs",
)
_ANIMAL_RIDABLES: frozenset[Character] = frozenset({
    Character.BANTHA,
    Character.BOMARRMONK,  # I guess a brain in a jar still counts as an animal.
    Character.DEWBACK,
    Character.TAUNTAUN,
    # Controllable as an Extra Toggle character in minikit bonuses rather than ridable.
    Character.WAMPA,
    Character.RANCOR,
})
# Many of these are probably impossible to kill, since damaging a vehicle usually just ejects the player.
_VEHICLE_RIDABLES: frozenset[Character] = frozenset({
    Character.ATAT,
    Character.ATST,
    Character.MAPCAR,
    Character.CLONEWALKER,
    Character.CLOUDCAR,
    Character.FIRETRUCK,
    Character.FLASHSPEEDER,
    Character.SPEEDER_LAND,
    Character.LIFEBOAT,
    Character.MOONCAR,
    Character.SERVICE_CAR,
    Character.SPEEDERBIKE,
    Character.SNOWMOB,
    Character.STAP,
    Character.TOWNCAR,
    Character.TRACTOR,
    Character.WOOKIEFLYER,
    # Controllable in minikit bonuses rather than ridable.
    *[c for c in Character if c.unlock_method is UnlockMethod.MINIKIT]
})
# I don't think any of these can be killed because they are stationary. The player is just ejected instead.
_STATIONARY_RIDABLES: frozenset[Character] = frozenset({
    Character.BASKETCANNON,
    Character.BIGGUN,
    Character.GRABBERCONTROL,
    Character.CATAPULT,
    Character.MOSCANNON,
    Character.CANNON,
    Character.TROOPERCANNON,
})

def _make_character_to_death_link_messages() -> dict[Character, tuple[tuple[str, ...], tuple[str, ...]]]:
    vehicle = (_PLAYER_SPECIFIC_VEHICLE_DEATH_MESSAGES, _VEHICLE_DEATH_MESSAGES)
    non_vehicle = (_PLAYER_SPECIFIC_NON_VEHICLE_DEATH_MESSAGES, _NON_VEHICLE_DEATH_MESSAGES)
    stationary_ridable = (_PLAYER_SPECIFIC_STATIONARY_RIDABLE_DEATH_MESSAGES, _STATIONARY_RIDABLE_DEATH_MESSAGES)
    animal_ridable = (_PLAYER_SPECIFIC_ANIMAL_RIDABLE_DEATH_MESSAGES, _ANIMAL_RIDABLE_DEATH_MESSAGES)
    fallback = (_FALLBACK_DEATH_MESSAGES, _FALLBACK_DEATH_MESSAGES)
    d: dict[Character, tuple[tuple[str, ...], tuple[str, ...]]] = {}
    for character in Character:
        if character in CHARACTER_TO_ITEM_DATA:
            item_data = CHARACTER_TO_ITEM_DATA[character]
            if item_data.item_type == "Vehicle":
                d[character] = vehicle
            else:
                d[character] = non_vehicle
        else:
            if character in _STATIONARY_RIDABLES:
                d[character] = stationary_ridable
            elif character in _ANIMAL_RIDABLES:
                d[character] = animal_ridable
            else:
                d[character] = fallback
    return d
_CHARACTER_TO_DEATH_LINK_MESSAGES: dict[Character, tuple[tuple[str, ...], tuple[str, ...]]]
_CHARACTER_TO_DEATH_LINK_MESSAGES = _make_character_to_death_link_messages()


_RANDOM: Random = Random()
def _get_death_message_for_character(ctx: TCSContext, character_id: int, player_number: int | None) -> str | None:
    # Get the current player's name.
    slot = ctx.slot
    if slot is None:
        return None
    player_name = ctx.player_names.get(slot)
    if player_name is None:
        return None

    if character_id not in Character:
        # This branch may be hit deliberately if it is not possible to determine which player has died.
        return _RANDOM.choice(_FALLBACK_DEATH_MESSAGES).format(alias=player_name, player=player_number)

    c = Character(character_id)
    character_name = c.readable_name
    if character_name == "?":
        # Probably shouldn't happen, but fall back to automatically getting a name from the enum constant name.
        character_name = c.name.replace("_", " ").title()
    if c in _CHARACTER_TO_DEATH_LINK_MESSAGES:
        messages_tuple = _CHARACTER_TO_DEATH_LINK_MESSAGES[c]
        if player_number is not None:
            # Player-specific.
            format_messages = messages_tuple[0]
        else:
            # Not player-specific.
            format_messages = messages_tuple[1]
    else:
        format_messages = _FALLBACK_DEATH_MESSAGES
    return _RANDOM.choice(format_messages).format(alias=player_name, player=player_number, character=character_name)


class DeathLinkManager(ClientComponent):
    pending_received_death = False
    last_received_death_message: str = ""

    death_link_enabled = False

    waiting_for_respawn = False
    normal_death_link_amnesty = 0
    vehicle_death_link_amnesty = 0

    normal_death_amnesty_remaining = 0
    vehicle_death_amnesty_remaining = 0

    last_death_amnesty = time.time()

    death_link_stud_loss: int = 0
    death_link_stud_loss_scaling: bool = False

    _last_area_death_count: int = 999_999_999
    _last_processed_received_death: float = float("-inf")

    p1_is_allowed_to_be_killed: bool = True
    p2_is_allowed_to_be_killed: bool = True

    current_area_uses_vehicle_amnesty: bool = False

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        ctx = event.context

        slot_data = event.slot_data

        self.death_link_enabled = EnabledFeature.DEATH_LINK.is_enabled(slot_data)
        self.normal_death_link_amnesty = slot_data.death_link_amnesty.value
        self.vehicle_death_link_amnesty = slot_data.vehicle_death_link_amnesty.value
        self.death_link_stud_loss = slot_data.death_link_studs_loss.value
        self.death_link_stud_loss_scaling = EnabledFeature.DEATH_LINK_STUD_LOSS_SCALING.is_enabled(slot_data)

        if event.first_time_setup:
            # Write whether Death Link is enabled into slot data.
            self._update_death_link(ctx, self.death_link_enabled)
        else:
            # Read whether Death Link is enabled from save data, in-case the user toggled it on/off in the client.
            self.death_link_enabled = CustomSaveFlags1.DEATH_LINK_ENABLED.is_set(ctx)
            # Update the client tags for whether Death Link is enabled/disabled.
            self._update_client_tags(ctx)

        # Initialise remaining amnesty.
        self.normal_death_amnesty_remaining = self.normal_death_link_amnesty
        self.vehicle_death_amnesty_remaining = self.vehicle_death_link_amnesty

        # Set the last known death count to its current value.
        self._last_area_death_count = _PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)

    def _update_client_tags(self, ctx: TCSContext):
        """Update the client's tags to add/remove the DeathLink tag."""
        async_start(ctx.update_death_link(self.death_link_enabled))

    def _update_death_link(self, ctx: TCSContext, enabled: bool):
        if enabled:
            # The game's death counter increments even with Death Link is disabled, so update the current expected death
            # count to whatever the game's death counter is set to, to prevent sending a death as soon as Death Link is
            # enabled.
            self._last_area_death_count = _PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)
            CustomSaveFlags1.DEATH_LINK_ENABLED.set(ctx)
        else:
            CustomSaveFlags1.DEATH_LINK_ENABLED.unset(ctx)
        self.death_link_enabled = enabled
        self._update_client_tags(ctx)

    def toggle_death_link(self, ctx: TCSContext):
        """Toggle Death Link on/off."""
        self._update_death_link(ctx, not self.death_link_enabled)

    @staticmethod
    def _get_kill_state_to_set(ctx: TCSContext) -> _CharacterActionState:
        area_id = CURRENT_AREA_ADDRESS.get(ctx)
        area = Area(area_id) if area_id in Area else None

        if area is None:
            # This should mean there is currently no Area. I am not sure if this can happen.
            if area_id != -1:
                # This should not happen unless the memory read is garbage for some reason.
                _DEBUG_LOGGER.warning("Got unknown Area ID %i when trying to determine kill state to set.", area_id)
            return _CharacterActionState.DOOMED

        if area.is_vehicle_area():
            # Many of the vehicle levels ignore DIE_AIR.
            return _CharacterActionState.DOOMED
        elif area is Area.MAP or area.is_chapter():
            # It is more pleasing for the character's parts to have physics instead of disappearing through the floor.
            return _CharacterActionState.DIE_AIR
        else:
            # If the current Area is anywhere else, just use DOOMED because most other areas have not been tested.
            return _CharacterActionState.DOOMED

    async def _kill_player_controlled_characters(self, ctx: TCSContext) -> bool:
        kill_state = DeathLinkManager._get_kill_state_to_set(ctx)
        expecting_death = []
        for player_number, character_address in player_character_entity_iter(ctx):
            if _CharacterDeathState.get(ctx, character_address) == _CharacterDeathState.ALIVE:
                if player_number == 1 and not self.p1_is_allowed_to_be_killed:
                    continue
                if player_number == 2 and not self.p2_is_allowed_to_be_killed:
                    continue
                # Do not kill players in the middle of crawling through a vent, they tend to get stuck and break the
                # vent's interaction.
                if _CharacterActionState.TELEPORT.is_set(ctx, character_address):
                    continue
                expecting_death.append((player_number, character_address))
                # WORKAROUND: Some characters, notably set-pieces such as Cranes, do not respawn when killed.
                # I am not currently sure what determines that they do not respawn. There is a flag that can be set that
                # will allow these non-respawning characters to respawn after 1.0s when killed, but normally respawning
                # characters do not use this flag. By setting the respawn time manually, this appears to allow for
                # non-respawning characters to respawn.
                # For turrets that break into bricks when destroyed, this does not cause issues. The 5-5 turret actually
                # respawns by default because it can be observed to be setting the respawn timer, which updates for a
                # frame before the turret breaks into bricks.
                _CHARACTER_RESPAWN_TIMER.set(ctx, character_address, 2.0)
                kill_state.set(ctx, character_address)

        killed_at_least_one = len(expecting_death) > 0

        if kill_state != _CharacterActionState.DOOMED:
            # The DIE_AIR state can take some time before it actually kills, especially for Player 2 who sometimes
            # ignores the state entirely for some reason. Some characters, notably turrets and other set-pieces, also
            # ignore DIE_AIR.
            await asyncio.sleep(0.05)
            for player_number, character_address in expecting_death:
                if _CharacterDeathState.get(ctx, character_address) == _CharacterDeathState.ALIVE:
                    # Set the respawn timer to ensure this character does actually respawn, even if it would not
                    # normally do so.
                    _CHARACTER_RESPAWN_TIMER.set(ctx, character_address, 2.0)
                    # Use the more forceful DOOMED death state because it is better at interrupting current actions,
                    # especially for Player 2.
                    _CharacterActionState.DOOMED.set(ctx, character_address)
                    _DEBUG_LOGGER.info("Retrying killing player %i with DOOMED", player_number)

            # Force kill implementation if needed.
            # if expecting_death:
            #     # Force kill characters that were still alive even after the check attempts.
            #     for player_number, character_address in expecting_death:
            #         _DEBUG_LOGGER.info("Force killing player %i", player_number)
            #         _CharacterDeathState.DEAD.set(ctx, character_address)

        return killed_at_least_one

    async def kill_player_characters(self, ctx: TCSContext) -> bool:
        self.waiting_for_respawn = True
        return await self._kill_player_controlled_characters(ctx)

    @staticmethod
    def _find_dead_player_controlled_character(ctx: TCSContext) -> tuple[bool, int]:
        for player_number, character_address in player_character_entity_iter(ctx):
            if _CharacterDeathState.get(ctx, character_address) != _CharacterDeathState.ALIVE:
                return True, player_number
        return False, -1

    async def attempt_to_send_death(self, ctx: TCSContext):
        """
        Attempt to send a death due to the last known in-area player death count being less than the current in-area
        player death count.

        The attempt to send a death may be blocked by amnesty.
        """
        # todo: Customise the death cause.
        #  Ideas:
        #  f"{alias name} crashed their {vehicle name}"
        #  f"{alias name} lost their studs"
        #  f"{alias name} broke their {character name} minifigure"
        #  f"Caused by {alias name}'s {character name}"
        #  Special messages for when both P1 and P2 are player controlled?
        #  f"{alias name}'s P{player number} crashed their {vehicle name}"
        #  f"{alias name}'s P{player number} lost their studs"
        #  Special messages only when both P1 and P2 are player controlled and are the same character?
        #  f"Caused by {alias name}'s {character name} (P{player number})"

        if time.time() < self.last_death_amnesty + _DEATH_COOLDOWN:
            # Do not send another death if sending a death through Death Link was recently prevented due to amnesty.
            return

        amnesty_remaining = 0
        if self.current_area_uses_vehicle_amnesty:
            if self.vehicle_death_amnesty_remaining <= 0:
                send_death = True
                # Reset amnesty.
                self.vehicle_death_amnesty_remaining = self.vehicle_death_link_amnesty
            else:
                send_death = False
                self.vehicle_death_amnesty_remaining -= 1
                amnesty_remaining = self.vehicle_death_amnesty_remaining
        else:
            if self.normal_death_amnesty_remaining <= 0:
                send_death = True
                # Reset amnesty.
                self.normal_death_amnesty_remaining = self.normal_death_link_amnesty
            else:
                send_death = False
                self.normal_death_amnesty_remaining -= 1
                amnesty_remaining = self.normal_death_amnesty_remaining

        if send_death:
            player_character_ids = {}
            dead_players: dict[int, float] = {}

            for player_number, character_address in player_character_entity_iter(ctx):
                c_data = CHARACTER_CHARACTER_DATA_POINTER.get(ctx, character_address)
                if not c_data:
                    # Somehow NULL.
                    continue
                player_character_ids[player_number] = CHARACTER_DATA_ID.get(ctx, c_data)
                if _CharacterDeathState.get(ctx, character_address) is not _CharacterDeathState.ALIVE:
                    respawn_timer = _CHARACTER_RESPAWN_TIMER.get(ctx, character_address)
                    dead_players[player_number] = respawn_timer

            custom_death_message = None
            if dead_players:
                # If both players happen to be dead, prefer the one with the most recent death (largest respawn timer).
                for dead_player, _ in sorted(dead_players.items(), key=lambda x: x[1], reverse=True):
                    specific_player_number = dead_player if len(player_character_ids) > 1 else None
                    death_message = _get_death_message_for_character(
                        ctx, player_character_ids.get(dead_player, -1), specific_player_number)
                    if death_message is not None:
                        custom_death_message = death_message
                        break
            elif len(player_character_ids) == 1:
                # If there is only one player character, assume it was them that died.
                character_id = next(iter(player_character_ids.values()))
                custom_death_message = _get_death_message_for_character(ctx, character_id, None)
            else:
                # No players are dead and both players are active, so there is no way to make a reasonable guess at who
                # died, e.g. both players are active and one of them died in 3-1 or 3-6, where dying instantly reloads a
                # checkpoint. By providing an invalid Character ID, the fallback messages will be used.
                custom_death_message = _get_death_message_for_character(ctx, -1, None)

            ctx.text_display.priority_message("DeathLink: Death Sent")
            # todo: This could probably be a fire-and-forget task.
            await ctx.send_death(custom_death_message if custom_death_message else "")
            # Ideally, we would kill any other player characters too, just like when receiving a death, but in levels
            # where death instantly respawns the player at an earlier checkpoint, this would result in the player, that
            # died, dying a second time after respawning at the checkpoint.
            # await self.kill_player_characters(ctx)
        else:
            if amnesty_remaining == 0:
                ctx.text_display.priority_message("DeathLink: No amnesty remaining")
            else:
                ctx.text_display.priority_message(f"DeathLink: {amnesty_remaining} amnesty remaining")
            self.last_death_amnesty = time.time()

    @subscribe_event
    async def update_game_state(self, event: OnGameWatcherTickEvent) -> None:
        ctx = event.context
        if not self.death_link_enabled or not ctx.is_in_game() or not event.is_actively_playing:
            return

        now = time.time()

        # Check if players have died by comparing the expected death count to the actual death count.
        player_death_count = _PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)
        expected_death_count = self._last_area_death_count
        if player_death_count == expected_death_count:
            # No death to send.
            pass
        elif player_death_count < expected_death_count:
            # The area has changed, resetting the game's death counter. Note that there is a delay between when the area
            # changes and when the game's death counter gets updated.
            self._last_area_death_count = player_death_count
            return
        elif player_death_count == 1 and (_CHEAT_FLAGS_STARTING_DEATH_COUNT & _CHEAT_FLAGS.get(ctx)):
            # The game's level update function sets the in-area death count to at least 1 when an Extra with this flag
            # is active. I have no idea why.
            # This means the player has not actually died.
            self._last_area_death_count = 1
            return

        # Update for new deaths.
        self._last_area_death_count = player_death_count

        # Wait for respawn from a received death.
        if self.waiting_for_respawn:
            # The player was killed by a received death link, and the client is still waiting for the player to respawn.

            # Ignore all received deaths until the player has respawned.
            self.pending_received_death = False
            dead_player_controlled_characters_found, _ = self._find_dead_player_controlled_character(ctx)
            if dead_player_controlled_characters_found:
                # Still dead, so don't send any more deaths or receive any more deaths.
                return
            else:
                _DEBUG_LOGGER.info("Players have respawned.")
                self.waiting_for_respawn = False
                # If it took a long time for the death to actually be processed, e.g. the game was paused, act as if the
                # death was actually recently processed.
                pretend_last_processed_death = now - _DEATH_COOLDOWN
                if pretend_last_processed_death > self._last_processed_received_death:
                    _DEBUG_LOGGER.info("Waiting for respawn took a while, so the last processed death time has been"
                                      " increased.")
                    self._last_processed_received_death = pretend_last_processed_death
                # Update the expected death count to match however many player controlled characters were killed by the
                # received death.
                self._last_area_death_count = _PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)
        # Receive death.
        elif self.pending_received_death:
            self.pending_received_death = False
            message = self.last_received_death_message
            self.last_received_death_message = ""
            # Kill player characters
            if await self.kill_player_characters(ctx):
                # The client could have paused the current coroutine for a while when hitting the await, so re-get the
                # current time instead of using `now`.
                self._last_processed_received_death = time.time()
                _DEBUG_LOGGER.info("Killing player characters from received death")
                # At least one character was alive and should now be dead or dying, so the death has been received.
                ctx.text_display.priority_message(message)
                # Remove studs from the player.
                studs_to_lose = self.death_link_stud_loss
                if studs_to_lose > 0:
                    if self.death_link_stud_loss_scaling:
                        studs_to_lose *= ctx.acquired_generic.current_score_multiplier
                    give_studs(ctx, -studs_to_lose, only_give_if_in_level=True, allow_power_up_multiplier=False)
            else:
                # There were no living players to kill, or the living players are not currently allowed to be killed, so
                # skip the received death.
                _DEBUG_LOGGER.info("There were no living players allowed to be killed.")
                pass
        # Send death.
        elif player_death_count > expected_death_count:
            # The player has died since the last time the in-area death count was checked.
            x = now - _DEATH_COOLDOWN
            if x < self._last_processed_received_death:
                # The player only recently received a death, don't send another death just yet.
                # This generally should not happen because the player has to wait to respawn to be able to die again.
                _DEBUG_LOGGER.info("Skipping sending a death because the player too recently received a death.")
                return
            if x < ctx.last_death_link:
                # The player only recently sent/received a death, don't send another death just yet.
                _DEBUG_LOGGER.info("Skipping sending a death because the player too recently sent/received a death.")
                return
            await self.attempt_to_send_death(ctx)

    def on_deathlink(self, previous_death: float, last_death: float, message: str):
        if (not self.last_received_death_message
                or ((previous_death < last_death) and (last_death - previous_death) < 0.5)):
            # If there is no stored message or the new death is only just after the previous death, store the new death
            # message instead.
            self.last_received_death_message = message
        self.pending_received_death = True

    @subscribe_event
    def on_area_change(self, event: OnAreaChangeEvent) -> None:
        # The area has changed, so the expected death count should reset. The area changes before the game resets the
        # death count, so the DeathLinkManager relies on the OnGameWatcherTickEvent to reduce _expected_area_death_count
        # from this very large dummy value to the proper value.
        self._last_area_death_count = 999_999_999
        self.waiting_for_respawn = False
        _DEBUG_LOGGER.info("Reset expected death count to 0 upon area change.")
        self.current_area_uses_vehicle_amnesty = event.new_area_data_id in _VEHICLE_AMNESTY_AREAS

    @subscribe_event
    def on_character_id_change(self, event: OnPlayerCharacterIdChangeEvent):
        self.p1_is_allowed_to_be_killed = event.new_p1_character_id not in _DISALLOWED_DEATH_CHARACTER_IDS
        self.p2_is_allowed_to_be_killed = event.new_p2_character_id not in _DISALLOWED_DEATH_CHARACTER_IDS

import asyncio
import logging
import time
from enum import IntEnum

from Utils import async_start

from . import ClientComponent
from .studs import give_studs
from ..common import StaticUint, FloatField
from ..common_addresses import CURRENT_AREA_ADDRESS, is_actively_playing, player_character_entity_iter, CustomSaveFlags1
from ..events import (
    subscribe_event,
    OnReceiveSlotDataEvent,
    OnGameWatcherTickEvent,
    OnAreaChangeEvent,
    OnPlayerCharacterIdChangeEvent,
)
from ..type_aliases import TCSContext
from ...levels import (
    AREA_ID_TO_CHAPTER_AREA,
    VEHICLE_CHAPTER_SHORTNAMES,
    AREA_ID_TO_BONUS_AREA,
    VEHICLE_BONUS_AREA_NAMES,
    SHORT_NAME_TO_CHAPTER_AREA,
    BONUS_NAME_TO_BONUS_AREA,
)

logger = logging.getLogger("Client")
debug_logger = logging.getLogger("TCS Debug")

# Currently, all characters are allowed to be killed because the client sets the respawn timer before killing the
# character.
DISALLOWED_DEATH_CHARACTER_IDS = frozenset()


# Player death count in the current area. Resets to zero upon area change.
PLAYER_DEATH_COUNT_IN_CURRENT_AREA = StaticUint(0x951224)
# Player death count in the current level. Resets to zero upon level change.
# PLAYER_DEATH_COUNTER_IN_CURRENT_LEVEL = StaticUint(0x87b2d0)


# Flags for the currently active 'cheats' (Extras).
CHEAT_FLAGS = StaticUint(0x950d8c)
# For some reason, if the in-area death count is 0, but flag cheat 0x2000 is active, then the in-area death count is
# increased to 1.
CHEAT_FLAGS_STARTING_DEATH_COUNT = 0x2000


# There are a maximum of 8 playable characters in a level, pointers to their 'character entity' objects are in an
# entity*[8] array at this address.
PLAYER_CHARACTER_POINTERS_ARRAY_ADDRESS = 0x93d7f0


VEHICLE_AMNESTY_AREA_IDS = frozenset({
    SHORT_NAME_TO_CHAPTER_AREA["2-1"].area_id,
    SHORT_NAME_TO_CHAPTER_AREA["2-5"].area_id,
    SHORT_NAME_TO_CHAPTER_AREA["4-6"].area_id,
    SHORT_NAME_TO_CHAPTER_AREA["5-1"].area_id,
    SHORT_NAME_TO_CHAPTER_AREA["5-3"].area_id,
    SHORT_NAME_TO_CHAPTER_AREA["6-6"].area_id,
    BONUS_NAME_TO_BONUS_AREA["Mos Espa Pod Race (Original)"].area_id,
    BONUS_NAME_TO_BONUS_AREA["Anakin's Flight"].area_id,
    BONUS_NAME_TO_BONUS_AREA["Gunship Cavalry (Original)"].area_id,
})


DEATH_COOLDOWN = 2.25
"""
Respawn is typically 2.0s, so ignore any deaths to send or receive within just above this time.
If something goes horrendously wrong with this Death Link implementation, this has the added benefit of
limiting death spam.
"""


class CharacterActionState(IntEnum):
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


class CharacterDeathState(IntEnum):
    ALIVE = 0
    UNKNOWN_BUT_ALSO_DEAD = 1
    DEAD = 2

    @classmethod
    def get(cls, ctx: TCSContext, character_address: int):
        return cls(ctx.read_uchar(character_address + 0x28b, raw=True))

    def set(self, ctx: TCSContext, character_address: int):
        ctx.write_byte(character_address + 0x28b, self.value, raw=True)


CHARACTER_RESPAWN_TIMER = FloatField(0x1010)
"""
Usually set by the game when a player dies, but can be set manually before killing a player, to make them wait a
different amount of time before they respawn, so long as it is set greater than 0.0
"""


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
        slot_data = event.slot_data
        ctx = event.context

        # Death Link did not exist as an option in older apworld versions.
        if event.generator_version < (1, 2, 0):
            self.death_link_enabled = False
            self.normal_death_link_amnesty = 0
            self.vehicle_death_link_amnesty = 0
            self.death_link_stud_loss = 0
            self.death_link_stud_loss_scaling = False
        else:
            self.death_link_enabled = bool(slot_data["death_link"])
            self.normal_death_link_amnesty = slot_data["death_link_amnesty"]
            self.vehicle_death_link_amnesty = slot_data["vehicle_death_link_amnesty"]
            self.death_link_stud_loss = slot_data["death_link_studs_loss"]
            self.death_link_stud_loss_scaling = bool(slot_data["death_link_studs_loss_scaling"])

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
        self._last_area_death_count = PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)

    def _update_client_tags(self, ctx: TCSContext):
        """Update the client's tags to add/remove the DeathLink tag."""
        async_start(ctx.update_death_link(self.death_link_enabled))

    def _update_death_link(self, ctx: TCSContext, enabled: bool):
        if enabled:
            # The game's death counter increments even with Death Link is disabled, so update the current expected death
            # count to whatever the game's death counter is set to, to prevent sending a death as soon as Death Link is
            # enabled.
            self._last_area_death_count = PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)
            CustomSaveFlags1.DEATH_LINK_ENABLED.set(ctx)
        else:
            CustomSaveFlags1.DEATH_LINK_ENABLED.unset(ctx)
        self.death_link_enabled = enabled
        self._update_client_tags(ctx)

    def toggle_death_link(self, ctx: TCSContext):
        """Toggle Death Link on/off."""
        self._update_death_link(ctx, not self.death_link_enabled)

    @staticmethod
    def _get_kill_state_to_set(ctx: TCSContext) -> CharacterActionState:
        area_id = CURRENT_AREA_ADDRESS.get(ctx)
        area = AREA_ID_TO_CHAPTER_AREA.get(area_id)
        is_vehicle_or_unknown: bool
        if area is None:
            bonus_area = AREA_ID_TO_BONUS_AREA.get(area_id)
            # if `bonus_area` is also None, then the player is somewhere that the apworld does not have information
            # about currently, e.g. an Episode's Minikit Bonus or 2-player Arcade.
            is_vehicle_or_unknown = bonus_area is None or bonus_area.name in VEHICLE_BONUS_AREA_NAMES
        else:
            is_vehicle_or_unknown = area.short_name in VEHICLE_CHAPTER_SHORTNAMES
        if is_vehicle_or_unknown:
            # Many of the vehicle levels ignore THROWN_BY_FORCE_LIGHTNING_OR_CHOKE_.
            return CharacterActionState.DOOMED
        else:
            # It is more pleasing for the character's parts to have physics instead of disappearing through the floor.
            return CharacterActionState.DIE_AIR

    async def _kill_player_controlled_characters(self, ctx: TCSContext) -> bool:
        kill_state = DeathLinkManager._get_kill_state_to_set(ctx)
        expecting_death = []
        for player_number, character_address in player_character_entity_iter(ctx):
            if CharacterDeathState.get(ctx, character_address) == CharacterDeathState.ALIVE:
                if player_number == 1 and not self.p1_is_allowed_to_be_killed:
                    continue
                if player_number == 2 and not self.p2_is_allowed_to_be_killed:
                    continue
                # Do not kill players in the middle of crawling through a vent, they tend to get stuck and break the
                # vent's interaction.
                if CharacterActionState.TELEPORT.is_set(ctx, character_address):
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
                CHARACTER_RESPAWN_TIMER.set(ctx, character_address, 2.0)
                kill_state.set(ctx, character_address)

        killed_at_least_one = len(expecting_death) > 0

        if kill_state != CharacterActionState.DOOMED:
            # The DIE_AIR state can take some time before it actually kills, especially for Player 2 who sometimes
            # ignores the state entirely for some reason. Some characters, notably turrets and other set-pieces, also
            # ignore DIE_AIR.
            await asyncio.sleep(0.05)
            for player_number, character_address in expecting_death:
                if CharacterDeathState.get(ctx, character_address) == CharacterDeathState.ALIVE:
                    # Set the respawn timer to ensure this character does actually respawn, even if it would not
                    # normally do so.
                    CHARACTER_RESPAWN_TIMER.set(ctx, character_address, 2.0)
                    # Use the more forceful DOOMED death state because it is better at interrupting current actions,
                    # especially for Player 2.
                    CharacterActionState.DOOMED.set(ctx, character_address)
                    debug_logger.info("Retrying killing player %i with DOOMED", player_number)

            # Force kill implementation if needed.
            # if expecting_death:
            #     # Force kill characters that were still alive even after the check attempts.
            #     for player_number, character_address in expecting_death:
            #         debug_logger.info("Force killing player %i", player_number)
            #         CharacterDeathState.DEAD.set(ctx, character_address)

        return killed_at_least_one

    async def kill_player_characters(self, ctx: TCSContext) -> bool:
        self.waiting_for_respawn = True
        return await self._kill_player_controlled_characters(ctx)

    @staticmethod
    def _find_dead_player_controlled_character(ctx: TCSContext) -> tuple[bool, int]:
        for player_number, character_address in player_character_entity_iter(ctx):
            if CharacterDeathState.get(ctx, character_address) != CharacterDeathState.ALIVE:
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
        #  f"Caused by {alias name}'s {character name}"
        #  Special messages for when both P1 and P2 are player controlled?
        #  f"{alias name}'s P{player number} crashed their {vehicle name}"
        #  f"{alias name}'s P{player number} lost their studs"
        #  Special messages only when both P1 and P2 are player controlled and are the same character?
        #  f"Caused by {alias name}'s {character name} (P{player number})"

        if time.time() < self.last_death_amnesty + DEATH_COOLDOWN:
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
            ctx.text_display.priority_message("DeathLink: Death Sent")
            # todo: This could probably be a fire-and-forget task.
            await ctx.send_death()
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
        if not self.death_link_enabled or not ctx.is_in_game() or not is_actively_playing(ctx):
            return

        now = time.time()

        # Check if players have died by comparing the expected death count to the actual death count.
        player_death_count = PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)
        expected_death_count = self._last_area_death_count
        if player_death_count == expected_death_count:
            # No death to send.
            pass
        elif player_death_count < expected_death_count:
            # The area has changed, resetting the game's death counter. Note that there is a delay between when the area
            # changes and when the game's death counter gets updated.
            self._last_area_death_count = player_death_count
            return
        elif player_death_count == 1 and (CHEAT_FLAGS_STARTING_DEATH_COUNT & CHEAT_FLAGS.get(ctx)):
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
                debug_logger.info("Players have respawned.")
                self.waiting_for_respawn = False
                # If it took a long time for the death to actually be processed, e.g. the game was paused, act as if the
                # death was actually recently processed.
                pretend_last_processed_death = now - DEATH_COOLDOWN
                if pretend_last_processed_death > self._last_processed_received_death:
                    debug_logger.info("Waiting for respawn took a while, so the last processed death time has been"
                                      " increased.")
                    self._last_processed_received_death = pretend_last_processed_death
                # Update the expected death count to match however many player controlled characters were killed by the
                # received death.
                self._last_area_death_count = PLAYER_DEATH_COUNT_IN_CURRENT_AREA.get(ctx)
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
                debug_logger.info("Killing player characters from received death")
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
                debug_logger.info("There were no living players allowed to be killed.")
                pass
        # Send death.
        elif player_death_count > expected_death_count:
            # The player has died since the last time the in-area death count was checked.
            x = now - DEATH_COOLDOWN
            if x < self._last_processed_received_death:
                # The player only recently received a death, don't send another death just yet.
                # This generally should not happen because the player has to wait to respawn to be able to die again.
                debug_logger.info("Skipping sending a death because the player too recently received a death.")
                return
            if x < ctx.last_death_link:
                # The player only recently sent/received a death, don't send another death just yet.
                debug_logger.info("Skipping sending a death because the player too recently sent/received a death.")
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
        debug_logger.info("Reset expected death count to 0 upon area change.")
        self.current_area_uses_vehicle_amnesty = event.new_area_data_id in VEHICLE_AMNESTY_AREA_IDS

    @subscribe_event
    def on_character_id_change(self, event: OnPlayerCharacterIdChangeEvent):
        self.p1_is_allowed_to_be_killed = event.new_p1_character_id not in DISALLOWED_DEATH_CHARACTER_IDS
        self.p2_is_allowed_to_be_killed = event.new_p2_character_id not in DISALLOWED_DEATH_CHARACTER_IDS

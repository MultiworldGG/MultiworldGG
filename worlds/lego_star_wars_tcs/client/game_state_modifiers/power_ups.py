import logging

from ..common import AREA_ID_CANTINA
from ..common_addresses import (
    player_character_entity_iter,
    CURRENT_AREA_ADDRESS,
    CHARACTER_POWER_UP_TIMER
)
from ..events import subscribe_event, OnGameWatcherTickEvent
from ..game_state_modifiers import ItemReceiver
from ...items import GENERIC_BY_NAME
from ...levels import BONUS_NAME_TO_BONUS_AREA, SHORT_NAME_TO_CHAPTER_AREA


debug_logger = logging.getLogger("TCS Debug")


# todo: Duplicated here for now, but common values like this should be moved to another module.
LEVEL_ID_CANTINA = 325

# LEGO City and New Town are special levels where the player has to get 1 million studs from the level. Most sources of
# studs in these levels ignore the 2x multiplier of having a Power Up, only loose studs on the ground get multiplied.
# 3-1 also ignores Power Ups for most sources of studs.
BANNED_AREA_IDS = frozenset({
    BONUS_NAME_TO_BONUS_AREA["LEGO City"].area_id,
    BONUS_NAME_TO_BONUS_AREA["New Town"].area_id,
    SHORT_NAME_TO_CHAPTER_AREA["3-1"].area_id,
    AREA_ID_CANTINA,
})


class PowerUpReceiver(ItemReceiver):
    receivable_ap_ids = frozenset({GENERIC_BY_NAME["Power Up"].code})

    power_ups_to_give = 0

    def clear_received_items(self) -> None:
        self.power_ups_to_give = 0

    approximate_remaining_time: float = 0.0
    last_time_remaining: float = 0.0

    def give_power_up(self):
        self.power_ups_to_give += 1

    @subscribe_event
    async def update_game_state(self, event: OnGameWatcherTickEvent) -> None:
        if self.power_ups_to_give <= 0:
            # Nothing to do if there are no power ups to give.
            return
        # Give all player controlled characters + 20s of Power Up while in a level that is not the Cantina, and the game
        # is not paused/alt tabbed etc.
        # Power Up time is not stacked up much higher than 20s so that the player won't lose stacked up Power Ups if
        # they return to the Cantina from a level.
        ctx = event.context
        if (
                ctx.is_in_game()
                and CURRENT_AREA_ADDRESS.get(ctx) not in BANNED_AREA_IDS
                and event.is_actively_playing
        ):
            gave_power_up = False

            player_numbers = []
            character_addresses = []
            power_up_timers = []
            for player_number, character_address in player_character_entity_iter(ctx):
                player_numbers.append(player_number)
                character_addresses.append(character_address)
                power_up_timers.append(CHARACTER_POWER_UP_TIMER.get(ctx, character_address))

            if len(player_numbers) == 1:
                power_up_timer = power_up_timers[0]

                # The Power Up in the UI starts flickering at 3s remaining, so add to the time when less than 3.5 to try
                # to avoid flickering happening at all.
                if power_up_timer < 3.5:
                    CHARACTER_POWER_UP_TIMER.set(ctx, character_addresses[0], power_up_timer + 20.0)
                    gave_power_up = True
                    debug_logger.info("Gave +20s of Power Up to P%i", player_numbers[0])
            elif len(player_numbers) == 2:
                max_power_up_timer = max(power_up_timers)
                if max_power_up_timer < 3.5:
                    # Both players are about to run out, or have run out of Power Up time.
                    zipped = zip(player_numbers, character_addresses, power_up_timers)
                    for player_number, character_address, power_up_timer in zipped:
                        CHARACTER_POWER_UP_TIMER.set(ctx, character_address, power_up_timer + 20.0)
                        gave_power_up = True
                        debug_logger.info("Gave +20s of Power Up to P%i", player_number)
                else:
                    min_power_up_timer = min(power_up_timers)
                    if min_power_up_timer < 3.5:
                        # One player is running out, but the other still has enough Power Up remaining.

                        if min_power_up_timer <= 0.0 < max_power_up_timer:
                            # One player has no time at all, e.g. they just dropped in, and the other player has some
                            # time, just give the player with no time the same time as the other player.
                            shared_time = max_power_up_timer
                            averaged = False
                        else:
                            # Average out the remaining time for the two players.
                            shared_time = sum(power_up_timers) / 2
                            averaged = True

                        # If the shared time is lower than 3.5, then add 20.0 and use a Power Up.
                        if shared_time < 3.5:
                            shared_time += 20.0
                            gave_power_up = True

                        zipped = zip(player_numbers, character_addresses, power_up_timers)
                        for player_number, character_address, original_power_up_timer in zipped:
                            CHARACTER_POWER_UP_TIMER.set(ctx, character_address, shared_time)
                            if gave_power_up:
                                if averaged:
                                    msg_format = "Averaged P%i Power Up time and gave +20s to %.3f from %.3f"
                                else:
                                    msg_format = "Synchronized P%i Power Up time and gave +20s to %.3f from %.3f"
                            else:
                                if averaged:
                                    msg_format = "Averaged P%i Power Up time to %.3f from %.3f"
                                else:
                                    msg_format = "Synchronized P%i Power Up time to %.3f from %.3f"
                            debug_logger.info(msg_format, player_number, shared_time, original_power_up_timer)
                    else:
                        # Neither player is running out of time, so there is nothing to do.
                        pass

            if gave_power_up:
                self.power_ups_to_give -= 1
                remaining = self.power_ups_to_give
                if remaining > 0:
                    message = f"> Power Up Activated ({remaining} remaining) <"
                else:
                    message = "> Power Up Activated <"
                ctx.text_display.priority_message(message)

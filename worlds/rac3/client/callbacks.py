"""This module contains functions related to the game client"""
from asyncio import sleep
from time import time
from traceback import format_exc
from typing import TYPE_CHECKING

from CommonClient import logger
from NetUtils import ClientStatus
from worlds.rac3.client.message import ClientMessage
from worlds.rac3.client.texthelper import colorize_item_name, get_sent_item_message
from worlds.rac3.constants.data.location import RAC3_LOCATION_DATA_TABLE
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.data.vendorslot import (ITEM_TO_ARMOR_VENDOR_LOCATION, ITEM_TO_WEAPON_VENDOR_LOCATION,
                                                   SHIP_VENDOR_INVENTORY)
from worlds.rac3.constants.input import RAC3INPUT
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING
from worlds.rac3.constants.moby_flag import HACKER_PUZZLE_TO_REGION
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.player_action import PERMITTED_DEATHLINK_SHIP_TELEPORT_ACTIONS
from worlds.rac3.constants.region import PLANET_VENDOR_OFFSET, PLANETS_WITH_HACKER_PUZZLES, RAC3REGION
from worlds.rac3.constants.shortcuts import RAC3SHORTCUTS
from worlds.rac3.constants.speedups import RAC3SPEEDUPS
from worlds.rac3.constants.vendors.vendor import RAC3VENDOR
from worlds.rac3.locations import get_challenge_locations

##################################################
# Only change point: Change filename/Class name  #
##################################################
if TYPE_CHECKING:
    from worlds.rac3.client.client import Rac3Context as Context


async def pcsx2_sync_task(ctx: "Context") -> None:
    """Connects to PCSX2 and loops through update functions until the connection is closed.
    :param ctx: RAC3 context class
    """
    logger.info(f"Starting {RAC3OPTION.GAME_TITLE_FULL} Connector")
    if "-dev" in RAC3OPTION.VERSION_NUMBER or RAC3OPTION.VERSION_NUMBER.count(".") >= 3:
        logger.warning("\nYou are using a development build of the RaC3 Archipelago Randomizer!\n"
                       "There may be bugs present and features that have not been tested fully.\n"
                       "These builds are meant for testing and bug reporting purposes "
                       "and should not be used for normal play!\n")
    connection_retry_attempts: int = 0
    game_initialized = False
    while not ctx.exit_event.is_set():
        try:
            connected_to_server = ctx.server is not None and ctx.slot is not None and ctx.slot_data is not None
            connected_to_game = ctx.game_interface.get_connection_state()
            if connected_to_game and not ctx.is_connected_to_game:
                logger.info(f"Connected to {RAC3OPTION.GAME_TITLE_FULL}")
                ctx.last_pine_message = None
                ctx.is_connected_to_game = connected_to_game
                if not connected_to_server:
                    logger.info("Waiting for server connection...")

            if not connected_to_game and not ctx.game_interface.is_connecting:
                if ctx.is_connected_to_game:
                    ctx.game_interface.disconnect_from_game()
                    logger.info("Connection to game lost")
                elif ctx.last_pine_message is None:
                    message = "Not connected to the PCSX2 instance"
                    ctx.game_interface.emulator_connected = False
                    logger.info(message)
                    ctx.last_pine_message = message
                ctx.game_interface.connect_to_game()
                if not ctx.game_interface.get_connection_state():
                    if connection_retry_attempts < 3:
                        connection_retry_attempts += 1

                    retry_wait = connection_retry_attempts * 10
                    if ctx.game_interface.emulator_connected:
                        connection_retry_attempts = 0
                        retry_wait = 10
                        logger.warning(
                            f"Could not connect to RaC3! Will retry connection in {retry_wait} seconds...\nEmulator "
                            f"already connected. Please launch RaC3.")
                    else:
                        logger.warning(
                            f"Could not connect to RaC3! Will retry connection in {retry_wait} seconds...\nPlease "
                            f"check your PINE settings both global and game specific, and restart PCSX2 if you "
                            f"changed them.")
                    await sleep(retry_wait)
                else:
                    connection_retry_attempts = 0

            if not connected_to_server:
                if ctx.server:
                    ctx.last_server_message = None
                elif ctx.last_server_message is None:
                    message = "Waiting for player to connect to server"
                    logger.info(message)
                    ctx.last_server_message = message

            if connected_to_game and connected_to_server:
                if not game_initialized:
                    ctx.game_interface.init()
                    game_initialized = True
                await _handle_game_ready(ctx)

        except ConnectionError:
            logger.info("ConnectionError")
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            logger.info("ExceptionError")
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(format_exc())
            # await sleep(3)

        await sleep(ctx.fps)
    logger.info(f"{RAC3OPTION.GAME_TITLE_FULL} Client Shutdown")


async def _handle_game_ready(ctx: "Context") -> None:
    """:param ctx: RAC3 context class"""
    # Quite a lot of stuff ended up in this function, even though it might
    # have fit better in init(). It just didn't work when I put it there,
    # probably because of when the game loads stuff.

    if ctx.slot_data is not None and ctx.slot is not None:
        # Check if exit to main menu
        menu = ctx.main_menu
        ctx.main_menu = ctx.game_interface.check_main_menu()

        if ctx.main_menu:
            ctx.save_file_identity = None
            if menu:
                ctx.game_interface.main_menu = True
            if ctx.last_game_message is None:
                message = "Currently on Main Menu, please load a file..."
                logger.info(message)
                ctx.last_game_message = message
            await sleep(5)

        if menu is True and ctx.main_menu is False:
            file_identity = ctx.connected_identity
            ctx.last_game_message = None
            await ctx.send_msgs([ClientMessage.status_update(ClientStatus.CLIENT_PLAYING)])
            if ctx.connected_identity != file_identity:
                return
            logger.info("Starting game...")
            ctx.game_interface.reset_file()
            logger.info("Old state removed!")
            logger.info("Checking for items...")
            logger.debug(f"Data Package: {ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, 'Empty')}")
            received_count = len(ctx.items_received)
            logger.info(f"Items Received: {received_count}")
            saved_count = ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, received_count)
            items_to_restore = max(0, min(saved_count, received_count))
            ctx.game_interface.initial_fillers.clear()
            for index, item in enumerate(ctx.items_received[:items_to_restore]):
                logger.debug(f"Restoring item {index}: {ctx.item_names.lookup_in_slot(item.item, item.player)}")
                ctx.game_interface.important_items(item.item, ctx.player_names[ctx.slot], item.location)
                ctx.game_interface.filler_items(item.item)
            ctx.processed_item_count = items_to_restore
            await ctx.send_msgs([ClientMessage.set_processed(ctx.processed_item_count)])
            if ctx.connected_identity != file_identity:
                return
            logger.info(f"Items Processed: {ctx.processed_item_count}")
            logger.info("Checking locations...")
            checks = set()
            for loc in ctx.checked_locations:
                logger.debug(f"Collecting location: {ctx.location_names.lookup_in_slot(loc, ctx.slot)}")
                checks.add(ctx.location_names.lookup_in_slot(loc, ctx.slot))
            counter = len(ctx.game_interface.collect_locations(checks))
            logger.info(f"Locations collected: {counter}")
            logger.info("Updating save data...")
            ctx.game_interface.load_save(ctx.save_data)
            ctx.game_interface.init_stored_fillers()
            ctx.game_interface.process_offline_fillers(ctx.data_received)
            ctx.save_file_identity = file_identity
            ctx.game_interface.reset_death_count()
            ctx.game_interface.setup_challenge_mode()
            ctx.game_interface.setup_settings()
            logger.info("Checking cosmetics...")
            ctx.game_interface.add_cosmetics()
            logger.info("Setting up codecave...")
            ctx.code_cave_setup = False
            await handle_codecave(ctx)
            logger.info("Adding Speedups...")
            ctx.game_interface.speedup_setup()
            logger.info("Game READY!")
            ctx.game_interface.batch_write()

        if not ctx.main_menu:
            ctx.game_interface.cycle_reads_count = 0
            ctx.game_interface.cycle_writes_count = 0
            ctx.game_interface.cycle_batch_reads_count = 0
            ctx.game_interface.cycle_batch_writes_count = 0
            current_time = time()
            await update(ctx)
            after_time = time()
            elapsed = after_time - current_time
            if "-dev" in RAC3OPTION.VERSION_NUMBER or RAC3OPTION.VERSION_NUMBER.count(".") >= 3:  # Is dev build
                logger.debug(f"Update cycle took {elapsed:.5f} seconds (Reads: {ctx.game_interface.cycle_reads_count} "
                             f"(Batch: {ctx.game_interface.cycle_batch_reads_count} operations), "
                             f"Writes: {ctx.game_interface.cycle_writes_count} "
                             f"(Batch: {ctx.game_interface.cycle_batch_writes_count} operations))")
            # logger.debug(f"Data Package: {ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, 'Empty')}")
            ctx.game_interface.cycle_times.append(elapsed)
            if len(ctx.game_interface.cycle_times) > 100:
                ctx.game_interface.cycle_times.pop(0)


##################################################
# Only change point: Change filename/Class name  #
##################################################


# common functions
async def update(ctx: "Context") -> None:
    """Called continuously
    :param ctx: RAC3 context class
    """
    ctx.game_interface.early_update()
    # Check codecave and set values if needed
    await handle_codecave(ctx)
    # Skip the intro and set the Veldin flags if the option is enabled
    await handle_intro_skip(ctx)
    # Check received items
    await handle_received_items(ctx)
    # Check collected locations
    await handle_checked_locations(ctx)
    # Check player dead or not
    await handle_deathlink(ctx)
    # Check goal is checked or not
    await handle_check_goal(ctx)
    # Check planet id
    await handle_planet_changed(ctx)
    # Check player respawn
    await handle_respawn(ctx)
    # Check the vendor
    await handle_vendors(ctx)
    if ctx.code_cave_setup:
        ctx.game_interface.overwrite_challenge_descriptions()
        ctx.game_interface.overwrite_pda_vendor_prompts()
    # Check sequence breaks
    await handle_sequence_break(ctx)
    ctx.game_interface.late_update()
    # Save to the server
    await handle_save(ctx)
    ctx.game_interface.overwrite_planet_location_counts(
        ctx.server_locations, ctx.checked_locations | ctx.locations_checked)
    # logger.info(f"Update is called")
    ctx.game_interface.batch_write()


async def handle_codecave(ctx: "Context") -> None:
    """Write item data to the code cave to be used later by vendors and challenges.
    :param ctx: RAC3 context class"""
    if ctx.slot_data is None or ctx.code_cave_setup:
        return
    # An open Galactic Map may still be reading the previous cave layout.
    if ctx.game_interface.galactic_map_uses_code_cave():
        return
    all_vendor_locations: list[str] = [RAC3LOCATION.HIDEOUT_PDA]
    if ctx.slot_data.get(RAC3OPTION.WEAPON_VENDORS, False):
        all_vendor_locations.extend(ITEM_TO_WEAPON_VENDOR_LOCATION.values())
    if ctx.slot_data.get(RAC3OPTION.ARMOR_VENDOR, False):
        all_vendor_locations.extend(ITEM_TO_ARMOR_VENDOR_LOCATION.values())
    if ctx.slot_data.get(RAC3OPTION.SHIP_VENDOR, False):
        all_vendor_locations.extend(SHIP_VENDOR_INVENTORY.keys())
    challenges = {location.NAME: location for location in get_challenge_locations()}
    vendor_strings: dict[str, str] = {}
    challenge_groups: dict[tuple[str, tuple[int, ...]], list[tuple[str, str]]] = {}
    for name in (*all_vendor_locations, *challenges):
        location = RAC3_LOCATION_DATA_TABLE[name]
        if location.AP_CODE not in ctx.server_locations:
            continue
        net_item = ctx.locations_info.get(location.AP_CODE)
        if net_item is None:
            return
        item_name = colorize_item_name(ctx.item_names.lookup_in_slot(net_item.item, net_item.player), net_item.flags)
        own_item = net_item.player == ctx.slot
        if not own_item:
            item_name = f"{RAC3TEXTFORMATSTRING.GREEN}{ctx.player_names.get(net_item.player, '???')}'s {item_name}"
        if name == RAC3LOCATION.HIDEOUT_PDA:
            purchase_item_name = f"a {item_name}" if own_item else item_name
            vendor_strings[name] = f"{RAC3TEXTFORMATSTRING.TRIANGLE} Buy {purchase_item_name} for 250,000 bolts"
            vendor_strings[RAC3VENDOR.PDA_INSUFFICIENT_BOLTS_KEY] = (
                f"You need 250,000 bolts to buy {purchase_item_name}"
            )
        elif name in challenges:
            group = (location.REGION, location.DESCRIPTION_TEXT_IDS)
            challenge_groups.setdefault(group, []).append((name, item_name))
        else:
            vendor_strings[name] = item_name

    challenge_strings = {
        name: "Obtain " + ", ".join(item_name for _, item_name in rewards) + " on challenge completion!"
        for rewards in challenge_groups.values()
        for name, _ in rewards
    }
    qwarktastic = RAC3LOCATION.NATION_QWARKTASTIC_BATTLE
    if RAC3_LOCATION_DATA_TABLE[qwarktastic].AP_CODE not in ctx.server_locations:
        challenge_strings[qwarktastic] = (
            f"To make this a location, enable {RAC3OPTION.GOAL_QWARK} "
            f"and set {RAC3OPTION.ARENA} to All in a new seed."
        )
    ctx.game_interface.setup_code_cave(vendor_strings, challenge_strings)
    ctx.code_cave_setup = True


async def handle_intro_skip(ctx: "Context") -> None:
    """Checks if the intro skip option is enabled, then skips veldin and sets required story/mission flags
    :param ctx: RAC3 context class"""
    if ctx.slot_data is None or ctx.slot is None:
        return
    if (ctx.slot_data[RAC3OPTION.SHORTCUTS].get(RAC3SHORTCUTS.VELDIN_SKIP, False)
        and ctx.current_planet == RAC3REGION.VELDIN and not ctx.game_interface.homewarping):
        ap_codes: set[int] = set()
        locations: set[str] = set()
        for ap_code in [ap_code for ap_code in ctx.missing_locations if
                        RAC3_LOCATION_DATA_TABLE[ctx.location_names.lookup_in_slot(ap_code, ctx.slot)].REGION
                        == RAC3REGION.VELDIN]:
            ctx.locations_checked.update([ap_code])
            ap_codes.add(ap_code)
            locations.add(ctx.location_names.lookup_in_slot(ap_code, ctx.slot))
        ctx.game_interface.collect_locations(locations)
        ctx.locations_checked.update(await ctx.check_locations(ap_codes))
        ctx.game_interface.homewarp()


async def handle_received_items(ctx: "Context") -> None:
    """Process items received from the AP server
    :param ctx: RAC3 context class"""
    if ctx.slot_data is None or ctx.slot is None:
        return

    # 初回だけ記録用に items_received の長さを記憶しておく
    for item in ctx.items_received[ctx.processed_item_count:]:
        ctx.game_interface.item_received(item.item, ctx.player_names[ctx.slot], ctx.player_names[item.player],
                                         item.location)
        # logger.info(f"Received item: ({item_id})")

    if ctx.processed_item_count != len(ctx.items_received):
        logger.debug(f"Update Data Package to {len(ctx.items_received)}")
        ctx.stored_data[RAC3OPTION.PROCESSED_LOCATIONS] = len(ctx.items_received)
        ctx.processed_item_count = len(ctx.items_received)
        await ctx.send_msgs([ClientMessage.set_processed(ctx.processed_item_count)])


async def handle_checked_locations(ctx: "Context") -> None:
    """Check for new locations collected, send these to the AP server
    :param ctx: RAC3 context class"""
    if ctx.slot_data is None or ctx.slot is None:
        return

    # logger.info(f"{ctx.server_locations}")
    new_checks = []
    for ap_code in ctx.server_locations:
        if ap_code in ctx.checked_locations | ctx.locations_checked:
            continue
        if ctx.game_interface.is_location_checked(ap_code):
            new_checks.append(ap_code)

    if new_checks:
        real_checks = list(await ctx.check_locations(new_checks))
        ctx.locations_checked.update(real_checks)
        ctx.skip_save_cooldown = True
        for location in real_checks:
            net_item = ctx.locations_info.get(location, None)
            if net_item is not None and net_item.player != ctx.slot:
                item_to_player_names = get_sent_item_message(ctx, net_item, True)
                ctx.game_interface.enqueue_notification(item_to_player_names)

    # else:
    #     logger.info("Not found new location")


async def handle_deathlink(ctx: "Context") -> None:
    """Receive and send deathlink
    :param ctx: RAC3 context class"""
    if not ctx.death_link and not ctx.game_interface.track_deaths:
        return
    ctx.game_interface.reload_check()
    if time() - ctx.last_death_link > 10 and ctx.death_link:
        alive, message = ctx.game_interface.alive()
        if alive:
            if ctx.queued_deaths > 0:
                logger.debug(f"Deaths requires processing: {ctx.queued_deaths}")
                if ctx.game_interface.kill_player():
                    ctx.game_interface.enqueue_notification(
                        f"{RAC3TEXTFORMATSTRING.WHITE}Deathlink Received from {RAC3TEXTFORMATSTRING.GREEN}"
                        f"{ctx.last_deathlink_sender}{RAC3TEXTFORMATSTRING.WHITE}:\n{ctx.last_deathlink_msg}",
                        RAC3BOXTHEME.DEATHLINK)
                    logger.debug("Deaths processed")
                    ctx.queued_deaths = 0
                    ctx.last_death_link = time()
        else:
            logger.debug(f"Sending Death, queue: {ctx.queued_deaths}")
            ctx.game_interface.enqueue_notification(f"{RAC3TEXTFORMATSTRING.WHITE}Sending Deathlink:\n{message}",
                                                    RAC3BOXTHEME.DEATHLINK)
            await ctx.send_death(message)
            logger.debug(f"Sent Death, queue: {ctx.queued_deaths}")


async def handle_check_goal(ctx: "Context") -> None:
    """Checks if the goal is completed
    :param ctx: RAC3 context class"""
    if ctx.slot_data is None or ctx.slot is None or ctx.finished_game:
        return
    if ctx.game_interface.check_victory(ctx.server_locations):
        ctx.finished_game = True
        await ctx.send_msgs([ClientMessage.status_update(ClientStatus.CLIENT_GOAL)])


async def handle_planet_changed(ctx: "Context") -> None:
    """Checks if the player is changing planet
    :param ctx: RAC3 context class"""
    if ctx.slot_data is None or ctx.slot is None:
        return
    # Player visits a new planet/region
    if ctx.game_interface.new_planet:
        ctx.game_interface.hacker_door_addresses = {}

        # Changing planet counts as a reload.
        ctx.game_interface.puzzle_cycler(RAC3ITEM.HACKER,
                                         ctx.slot_data[RAC3OPTION.SPEEDUPS].get(RAC3SPEEDUPS.HACKER, False),
                                         "opened_the_hacker_doors", PLANETS_WITH_HACKER_PUZZLES,
                                         HACKER_PUZZLE_TO_REGION, True)
        ctx.game_interface.softlock_warning()
        ctx.game_interface.region_disabled_warning()
        ctx.game_interface.speedup_unavailable_warning()
        ctx.game_interface.tyhrranosis_fix()

    # Handle UT map changes
    last_planet = ctx.current_planet
    ctx.current_planet, _map = ctx.game_interface.map_switch()
    if last_planet is not ctx.current_planet:
        ctx.current_map = _map
        await ctx.send_msgs([ClientMessage.set_map(ctx.slot, ctx.team, _map)])

    if ctx.current_map != _map:
        ctx.current_map = _map
        await ctx.send_msgs([ClientMessage.set_map(ctx.slot, ctx.team, _map)])


async def handle_respawn(ctx: "Context", force_respawn: bool = False, force_load: bool = False):
    """Check if the player should respawn
    :param ctx: RAC3 context class
    :param force_respawn: Ignore player inputs and force a respawn
    :param force_load: Ignore player inputs and force a reload
    """
    if ctx.game_interface.is_reloading:
        return
    if ctx.death_link and ctx.game_interface.action not in PERMITTED_DEATHLINK_SHIP_TELEPORT_ACTIONS:
        if force_load:
            logger.error("Player cannot homewarp right now")
        elif force_respawn:
            logger.error("Player cannot respawn right now")
        return
    planet_data = RAC3_REGION_DATA_TABLE[ctx.game_interface.planet]
    if planet_data.ID > 55:
        return
    if planet_data.PAUSE_ADDRESS is not None:  # Vid comics do not have a pause address
        if ctx.game_interface.check_inputs(RAC3INPUT.SQUARE, True) or force_respawn:
            ctx.game_interface.unpause_game()
            ctx.game_interface.teleport_to_ship()
            return
        if ctx.game_interface.check_intro():
            if force_load:
                logger.error("Player cannot homewarp right now")
            elif force_respawn:
                logger.error("Player cannot respawn right now")
            return
        if ctx.game_interface.check_inputs(RAC3INPUT.RELOAD, True) or force_load:
            ctx.game_interface.unpause_game()
            ctx.game_interface.homewarp()
            return
    if ctx.game_interface.check_inputs(RAC3INPUT.RELOAD) or force_load:
        ctx.game_interface.homewarp()
        return
    return


async def handle_vendors(ctx: "Context") -> None:
    """Read current vendor inventory and replace all items after the all ammo item with all items in the game
    :param ctx: RAC3 context class"""
    if ctx.slot_data is None or ctx.current_planet not in PLANET_VENDOR_OFFSET.keys():
        return

    ctx.game_interface.vendor_update()
    vendor_location_apcodes = ctx.game_interface.get_vendor_apcodes()
    if vendor_location_apcodes:
        current_hints = set(vendor_location_apcodes)
        if current_hints and not current_hints.issubset(ctx.already_hinted):
            await ctx.send_msgs([{"cmd": "CreateHints", "locations": vendor_location_apcodes, "player": ctx.slot}])
            ctx.already_hinted.update(current_hints)


async def handle_sequence_break(ctx: "Context") -> None:
    """
    Undoes the flags for infobot locations when sequence breaking if you haven't checked the corresponding location yet
    :param ctx: RAC3 context class
    """
    if ctx.slot_data is None or ctx.slot is None:
        return
    ctx.game_interface.sequence_break()


async def handle_save(ctx: "Context") -> None:
    """Checks if any memory values need to be saved to the server
    :param ctx: RAC3 context class"""
    save_key = ctx.save_key
    if ctx.slot_data is None or save_key is None or ctx.save_file_identity != ctx.connected_identity:
        return
    if ctx.data_received:
        local_save = ctx.game_interface.update_save()
        # logger.debug(f"local_save : {local_save}")
        # logger.debug(f"server_save: {ctx.save_data}")
        current_time = time()
        if not (local_save == ctx.save_data) and (current_time - ctx.last_saved > 20 or ctx.skip_save_cooldown):
            logger.debug("Sending new save data to server")
            ctx.last_saved = current_time
            ctx.data_received = False
            ctx.skip_save_cooldown = False
            ctx.save_data = local_save
            await ctx.send_msgs([ClientMessage.update_save(save_key, local_save)])
    else:
        logger.debug("Waiting for save data from server")

# Do the vendor imports
from . import fileHelper
fileHelper.load_vendor_modules()

import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.poe.Client import PathOfExileContext

from . import itemFilter
from . import inputHelper
from . import validationLogic
from . import gggAPI
from . import tts
import asyncio
import threading
import time
import logging
import pkgutil

from pynput import keyboard
from pathlib import Path


logger = logging.getLogger("poeClient.main")
_debug = True  # Set to True for debug output, False for production
validate_char_debounce_time = 2  # seconds
context = None  # This will be set in the client_start function
_run_update_item_filter = False
_last_pressed_key: keyboard.Key | None = None

possible_paths_to_client_txt = [
    Path("C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/client.txt"),
    Path("C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/client.txt"),
    Path("D:/games/poe/logs/Client.txt"),
    Path.home() / "Documents" / "My Games" / "Path of Exile" / "Client.txt",
]
path_to_client_txt = Path("D:/games/poe/logs/Client.txt")

key_functions = {
    #keyboard.KeyCode: lambda: validate_char(),
    # numpad 1
    keyboard.Key.f12: lambda: asyncio.create_task(validate_char(context)),
    keyboard.Key.f11: lambda: asyncio.create_task( lambda :(_ for _ in ()).throw(Exception("F11 pressed, raising exception for testing purposes"))),
}

def on_press(key):
    # key is a keycode, key or none.
    global _last_pressed_key
    _last_pressed_key = key

last_ran_validate_char = 0
async def validate_char(ctx: "PathOfExileContext" = context):

    # add a debounce timer to the validate_char function. I want this function to run at most every 5 seconds
    global last_ran_validate_char, _run_update_item_filter
    current_time = time.time()
    if current_time - last_ran_validate_char < validate_char_debounce_time:
        logger.debug(f"Debounced: validate_char called too soon. Last ran at {last_ran_validate_char}, current time is {current_time}.")
        return
    logger.debug(f"[DEBUG] Validating character: {ctx.character_name} at {current_time}")
    _run_update_item_filter = True
    last_ran_validate_char = time.time()

    return await validationLogic.when_enter_new_zone(context,
                                        "2025/08/01 19:40:29 39555609 cff945b9 [INFO Client 30324] : You have entered f12refresh.")  # hacky I know lol


async def async_load(ctx: "PathOfExileContext" = None):
    global context
    await gggAPI.async_get_access_token()
    ctx = ctx if ctx is not None else context

    # Extract jingle sound files from package data to the filter sounds directory
    jingle_dir = itemFilter.poe_doc_path / itemFilter.JINGLE_FILTER_SOUNDS_DIR_NAME
    jingle_dir.mkdir(parents=True, exist_ok=True)

    tts_dir = itemFilter.poe_doc_path / itemFilter.TTS_FILTER_SOUNDS_DIR_NAME
    tts_dir.mkdir(parents=True, exist_ok=True)

    if ctx.filter_options.tts_enabled:
        tts.generate_tts_tasks_from_missing_locations(ctx, ctx.filter_options.tts_speed)
        threading.Thread(target=tts.run_tts_tasks, daemon=True).start()  # Run TTS tasks in a separate thread

    try:
        # All files to extract from the jingles directory (including documentation)
        jingle_files = [
            "Filler.wav",
            "Useful.wav", 
            "Trap.wav",
            "ProgUseful.wav",
            "Progression.wav",
            "LICENSE.md",
            "README.md"
        ]
        
        for filename in jingle_files:
            if filename is None:
                continue
                
            try:
                src_data = pkgutil.get_data("worlds.poe.data", f"sounds/jingles/{filename}")
                if src_data is not None:
                    dest_path = jingle_dir / filename
                    dest_path.write_bytes(src_data)
                    logger.debug(f"Extracted jingle file: {filename}")
                else:
                    logger.warning(f"Could not find jingle file: {filename}")
            except Exception as file_error:
                logger.warning(f"Could not extract jingle file {filename}: {file_error}")
                continue
                
    except Exception as e:
        logger.error(f"Could not extract jingles: {e}")
        # Continue execution - jingles are optional

    itemFilter.update_item_filter_from_context(ctx)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    await inputHelper.important_send_poe_text(f"/itemfilter {itemFilter.AP_FILTER_NAME}")


async def text_queue_processor(ctx: "PathOfExileContext"):
    """Dedicated task for processing text message queue"""
    logger.info("Text queue processor started.")
    polling_rate = 0.05  # seconds
    try:
        while True:
            # Wait a bit before checking
            await asyncio.sleep(polling_rate)
            # Process messages one at a time
            if ctx.text_to_send: # [] is false
                try:
                    message, prepend_char_name = ctx.text_to_send.pop(0)
                    name = ctx.character_name if ctx.character_name else "_ap"
                    max_length = 500 - ((len(name) + 2) if prepend_char_name else 0)
                    if len(message) > max_length:
                        # Split the message into chunks of max_length, and put them back in the queue
                        chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
                        for chunk in chunks:
                            ctx.text_to_send.append((chunk, prepend_char_name))
                        continue #

                    # Prepend character name if requested
                    if prepend_char_name:
                        message = f"@{name} {message}"
                    await inputHelper.send_poe_text(message, retry_times=3, retry_delay=1)
                    await asyncio.sleep(inputHelper.DEBOUNCE_TIME + 0.001) 
                    
                except IndexError:
                    # Queue was empty (race condition)
                    pass
                except Exception as e:
                    logger.error(f"Error sending message: {e}")
                    await asyncio.sleep(1)  # Back off on error
                    
    except asyncio.CancelledError:
        logger.info("Text queue processor cancelled.")
        raise
    except Exception as e:
        logger.error(f"Error in text queue processor: {e}")
        raise
    finally:
        logger.info("Text queue processor stopped.")


async def timer_loop(ctx: "PathOfExileContext" = None):
    loop_timer = 0.1  # Time in seconds to wait before polling
    ticks = 0.1
    global _run_update_item_filter, _last_pressed_key
    try:
        while True:
            await asyncio.sleep(loop_timer)
            ticks += 0.1

            if _last_pressed_key is not None and _last_pressed_key in key_functions:
                try:
                    if _debug:
                        logger.info(f"[DEBUG] Key pressed: {_last_pressed_key}, executing function.")
                    await key_functions[_last_pressed_key]()
                except Exception as e:
                    logger.error(f"[ERROR] Error executing function for key {_last_pressed_key}: {e}")
                    raise e
                _last_pressed_key = None

    except asyncio.CancelledError:
        logger.info("Timer loop cancelled.")
        raise
    except Exception as e:
        logger.error(f"Error in timer loop: {e}")
        raise
    finally:
        logger.info("Timer loop stopped.")
        # Adjust the sleep time as needed
#        ticks += 0.1
#        if _run_update_item_filter: # every hour
#            await inputHelper.send_poe_text("/itemfilter __ap")
#            _run_update_item_filter = False
#
#
#        if ticks % 1 < 0.1:
#            pass
            
            



async def client_start(ctx: "PathOfExileContext") -> asyncio.Task:
    global context, path_to_client_txt
    context = ctx
    validationLogic.defaultContext = ctx
    path_to_client_txt = ctx.client_text_path if ctx.client_text_path else path_to_client_txt
    path_to_client_txt = Path(path_to_client_txt)

    return await main_async(ctx)
    
async def main_async(context: "PathOfExileContext"):
    import time
    tasks = []
    
    try:
        await async_load(context)
        
        async def enter_new_zone_callback(line: str):
            await asyncio.wait_for(validationLogic.when_enter_new_zone(context, line), timeout=7.0)

        async def chat_commands(line: str):
            from worlds.poe.poeClient.textUpdate import chat_commands_callback
            await asyncio.wait_for(chat_commands_callback(context, line), timeout=7.0)

            from worlds.poe.poeClient.textUpdate import deathlink_callback
            if context.get_is_death_linked():
                await asyncio.wait_for(deathlink_callback(context, line), timeout=7.0)

        logger.info("Starting Main Loop...")
        
        tasks = [
            asyncio.create_task(fileHelper.callback_on_file_change(path_to_client_txt, [enter_new_zone_callback, chat_commands]), name="file_watcher"),
            asyncio.create_task(timer_loop(context), name="timer_loop"),
            asyncio.create_task(text_queue_processor(context), name="text_queue")
        ]
        
        await asyncio.gather(*tasks)
        
    except (KeyboardInterrupt, asyncio.CancelledError) as e:
        logger.info(f"Main Loop interrupted: {type(e).__name__}")
        raise
    except Exception as e:
        logger.error(f"Main Loop error: {e}")
        raise
    finally:
        await cancel_tasks(tasks)

async def cancel_tasks(tasks: list[asyncio.Task]):
    """Cancel a list of tasks gracefully."""
    if not tasks:
        return
            
    logger.info(f"Cancelling {len(tasks)} tasks...")

    # Cancel all tasks
    for task in tasks:
        if not task.done():
            task.cancel()
    
    # Wait for cancellation to complete
    if tasks:
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Error during task cancellation: {e}")
            raise
    
    logger.info("All tasks cancelled.")

def run_async_or_not():
    try:
        if asyncio.get_event_loop().is_running():
            # If already in an event loop, schedule as a task
            asyncio.create_task(main_async())
        else:
            asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Main Loop stopped by user.")

if __name__ == '__main__':
    # Set the character name here or pass it as an argument
#    context.character_name = "merc_MY_FIREEE"  # Replace with your character name

    run_async_or_not()

































#
# polling_interval = 3  # seconds
# client_txt_last_modified_time = path_to_client_txt.stat().st_mtime
# last_entered = ""
# async def polling_loop():
#     global client_txt_last_modified_time
#     while True:
#         await asyncio.sleep(polling_interval)  # Polling interval
#         entered = fileHelper.get_last_zone_log(str(path_to_client_txt))
#         if entered == last_entered:
#             return #we are done here, no change detected
#
#             logger.info(f"Detected change in {path_to_client_txt}, reloading item filter...")
#             validate_char()
#             await inputHelper.send_poe_text("/itemfilter __ap")
#             client_txt_last_modified_time = current_mod_time
#         else:
#             logger.info(f"Path to client.txt does not exist: {path_to_client_txt}")



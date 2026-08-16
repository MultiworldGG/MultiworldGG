import asyncio
from Utils import logging
import websockets
from typing import TYPE_CHECKING, Iterable

from MultiServer import on_client_connected, Endpoint
from NetUtils import decode, encode

if TYPE_CHECKING:
    from worlds.deltarune.DeltaruneClient import DeltaruneContext

# Big thanks of Pizza Tower devs for that
# https://github.com/unsafetyskizzers/Archipelago/blob/pizza_ap/worlds/pizza_tower/Client.py
# because without their code and help i would be lost
# however you can see what part is mine because they are awful ~Tenebrosful


async def proxy_loop(ctx: "DeltaruneContext"):
    logging.info("Proxy Loop start")
    try:
        while not ctx.exit_event.is_set():
            if not ctx.is_connected():
                ctx.connected = False
            if len(ctx.proxy_server_msgs) > 0:
                for msg in ctx.proxy_server_msgs:
                    await send_msgs_proxy(ctx, msg)

                ctx.proxy_server_msgs.clear()
            await asyncio.sleep(0.1)
    except Exception as e:
        logging.info(f"Proxy loop error: {e}")


async def proxy(websocket, path: str = "/", ctx: "DeltaruneContext" = None):
    logging.info(f"Proxy connected: {websocket}")
    ctx.proxy_endpoint = Endpoint(websocket)
    try:
        await on_client_connected(ctx)
        if ctx.is_proxy_connected():
            async for data in websocket:
                if not ctx.is_connected() and ctx.authenticated:
                    await send_msgs_proxy(ctx, {"cmd": "ProxyDisconnect"})
                    ctx.authenticated = False
                await parse_game_packets(ctx, data)
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logging.info(f"Proxy error: {e}")
    finally:
        await ctx.disconnect_proxy()


async def on_client_connected(ctx: "DeltaruneContext"):
    logging.info(f"Proxy client connected")
    if ctx.room_info and ctx.connected:
        await send_msgs_proxy(ctx, ctx.room_info)
    else:
        await send_msgs_proxy(ctx, {"cmd": "ProxyDisconnect"})


async def parse_game_packets(ctx: "DeltaruneContext", data):
    for msg in decode(data):
        # connection with server is handled by proxy client already, just send back the important data
        if msg["cmd"] == "Connect":
            # Proxy is connecting, make sure it is valid
            if msg["game"] != "DELTARUNE":
                await ctx.disconnect_proxy()
                break
            logging.info(f"Game -> Proxy | {msg}")
            # send over connection data and receiveditems if valid
            if ctx.connected_msg and ctx.is_connected():
                await send_msgs_proxy(ctx, ctx.connected_msg)
                await send_msgs_proxy(ctx, {"cmd": "ReceivedItems", "index": 0, "items": ctx.items_received})
        elif not ctx.is_proxy_connected():
            break
        # send over any packets received from the game client to the server
        else:
            logging.info(f"Game -> Proxy -> Server | {msg}")

            if msg["cmd"] == "ConnectUpdate":
                if "NoText" in msg["tags"]:
                    msg["tags"].remove("NoText")
                    logging.info(f"Removing NoText Tag")
                    logging.info(f"NEW | {msg}")

            await ctx.send_msgs([msg])


async def send_msgs_proxy(ctx: "DeltaruneContext", msgs: Iterable[dict]) -> bool:
    """`msgs` JSON serializable"""
    if not ctx.proxy_endpoint or not ctx.proxy_endpoint.socket.open or ctx.proxy_endpoint.socket.closed:
        return False

    logging.info(f"Proxy -> Game | {msgs}")

    # queue so that packets sent in quick succession don't get lost
    # special thanks to profdecube for looking into this issue and writing a fix for it
    ctx.proxy_message_queue.append(msgs)
    if not ctx.is_processing_outgoing_messages:
        ctx.is_processing_outgoing_messages = True
        while len(ctx.proxy_message_queue) > 0:
            message_to_process = ctx.proxy_message_queue.pop(0)
            await ctx.proxy_endpoint.socket.send(
                encode(message_to_process if type(message_to_process) == list else [message_to_process])
            )
            await asyncio.sleep(0.1)
        ctx.is_processing_outgoing_messages = False
    return True

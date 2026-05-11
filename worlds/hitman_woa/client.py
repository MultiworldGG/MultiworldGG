import asyncio

import threading
import time
import typing
import requests
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"

from CommonClient import ClientCommandProcessor, get_base_parser, handle_url_arg, server_loop, gui_enabled, logger
from NetUtils import ClientStatus, NetworkItem
from settings import get_settings

from worlds import AutoWorldRegister
from .items import item_table, base_id
from .locations import goal_table, item_pickup_location_table, split_item_pickup_location_table, level_completion_location_table, target_kill_location_table, disguise_location_table

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext, load_json

    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

class HitmanCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: SuperContext):
        super().__init__(ctx)

class HitmanContext(SuperContext):
    command_processor = HitmanCommandProcessor
    game = "HITMAN World of Assassination"
    tags = {"AP"}
    items_handling = 0b111
    want_slot_data = True
    slot_data = {}
    collected_contract_pieces = 0
    sse_thread = None
    sse_running = False
    current_seed = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        import settings
        # Force a cache refresh so we can find our own settings
        settings._world_settings_name_cache_updated = False
        self.peacock_url = "http://"+get_settings().hitman_woa_options.peacock_url+ "/_wf/archipelago"

    async def connect(self, address: typing.Optional[str] = None) -> None:
        # check if Peacock is running
        logger.info("Testing connection to Peacock...")
        try:
            r = requests.get(self.peacock_url)
            r.raise_for_status()
        except Exception as e:
            self.print_error("No response from Peacock, please make sure the Peacock server is running before connecting.")
            return
        logger.info("Peacock connection established.")            

        await super().connect(address)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(HitmanContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game) 

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args) #keep Universal Tracker in the loop
        match cmd:
            case "Connected":
                self.collected_contract_pieces = 0
                self.slot_data = None

                self.game = self.slot_info[self.slot].game
                self.slot_data = args["slot_data"]

                if tracker_loaded:
                    #for map tab in UT, give Events insight into which location was already checked
                    self.tracker_core.multiworld.hitman_client_checked_locations = self.checked_locations

                    #add/remove UT map locations based on master difficulty in yaml
                    new_locations = self.tracker_world.map_page_locations.copy()
                    if "master" in self.slot_data["entitlements"]:
                        new_locations.remove("locations/itempickup_map_non_master_locations.json")

                    self.locs = []
                    for loc_page in new_locations:
                        self.locs += load_json(self.tracker_core.get_current_world().__class__.__module__, f"/{self.tracker_world.map_page_folder}/{loc_page}")

                    #force reload the map
                    self.load_map(1)
                    self.load_map(0)
                try:
                    self.set_slot_data()
                    self.set_goal()
                    self.process_checked_locations(args["checked_locations"])
                    self.sse_thread = threading.Thread(name="SSE-Thread",target=self.periodically_get_checks, daemon=True)
                    self.sse_thread.start()
                except RuntimeError as e:
                    asyncio.run_coroutine_threadsafe(self.disconnect(False), asyncio.get_running_loop())
            case "ReceivedItems":
                self.process_recieved_items(args["items"])
            case "RoomUpdate":
                self.process_checked_locations(args.get("checked_locations",[]))
            case "PrintJSON"| "Retrieved" |  "Bounced" | "SetReply" | "DataPackage":
                pass
            case "RoomInfo":
                self.current_seed = args["seed_name"].removeprefix("W")
            case _:
                print("Not implemented cmd: "+cmd+", with args: "+str(args))

    async def disconnect(self, allow_autoreconnect: bool = False):
        if self.sse_thread is not None:
            self.sse_running = False

        await super().disconnect(allow_autoreconnect)

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"{apname} HITMAN Client"
        return ui

    def set_slot_data(self):
        logger.info("Sending Slot Data to Peacock...")
        try:
            cares_about_goal_rating = self.slot_data["goal_mode"] == "level_completion" or\
                    self.slot_data["goal_mode"] == "contract_collection_level_completion"

            enabled_levels = self.slot_data["included_s1_locations"]+\
            self.slot_data["included_s2_locations"]+\
            self.slot_data["included_s2_dlc_locations"]+\
            self.slot_data["included_s3_locations"]+\
            [self.slot_data["starting_location_name"]]

            if(cares_about_goal_rating):
                enabled_levels.append(self.slot_data["goal_location_name"])

            level_data = {}
            targets = self.slot_data.get("targets","vanilla")
            if targets != "vanilla":
                targets = targets.split("-")

            complications = self.slot_data.get("complications","vanilla")
            if complications != "vanilla":
                complications = complications.split("-")

            i = 0
            for level in goal_table.keys():
                level_object = {}
                if level in enabled_levels:
                    level_object["enabled"] = True
                    if complications != "vanilla":
                        level_object["complications"] = list(x for x in complications[i].split("_") if x != "")
                    else:
                        level_object["complications"] = []

                    if targets != "vanilla" and targets[i] != "":
                        level_object["targets"] = list(x for x in targets[i].split("_") if x != "")

                else:
                    level_object["enabled"] = False
                
                level_data[goal_table[level]] = level_object 
                i = i+1

            all_checks = {
                "itemPickupChecks":[],
                "splitItemPickupChecks":[],
                "completionChecks":[],
                "eliminationChecks":[],
                "disguiseChecks":[]
            }
            for id in list(x-base_id for x in self.server_locations):
                location_name = self.location_names.lookup_in_game(id+base_id)
                if location_name in item_pickup_location_table:
                    all_checks["itemPickupChecks"].append(id)
                elif location_name in split_item_pickup_location_table:
                    all_checks["splitItemPickupChecks"].append(id)
                elif location_name in level_completion_location_table:
                    all_checks["completionChecks"].append(id)
                elif location_name in target_kill_location_table:
                    all_checks["eliminationChecks"].append(id)
                elif location_name in disguise_location_table:
                    all_checks["disguiseChecks"].append(id)
            
            all_checks["itemPickupChecks"].sort()
            all_checks["splitItemPickupChecks"].sort()
            all_checks["completionChecks"].sort()
            all_checks["eliminationChecks"].sort()
            all_checks["disguiseChecks"].sort()

            r = requests.post(
                self.peacock_url+"/setData",
                json={
                    "difficulty":self.slot_data.get("difficulty","normal"),
                    "seed":self.current_seed,
                    "everythingItemInInventory":self.slot_data.get("item_packages","")=="in_inventory",
                    "checks":all_checks,
                    "levels":level_data,
                    "genVersion":self.slot_data.get("gen_version","pre-0.8.0"),
                    "clientVersion":AutoWorldRegister.world_types[self.game].world_version.as_simple_string()
                    #TODO: consolidate goal into this
                })
            r.raise_for_status()
            logger.info("Slot Data sent.")
        except Exception as e:
            self.print_error("No response when sending slot data to Peacock, disconnecting")
            print("Error sending slot data:", e)
            raise RuntimeError()
        
    def set_goal(self):
        try:
            match self.slot_data["goal_mode"]:
                case "level_completion":
                    goal_data = self.slot_data["goal_location_name"]
                    more_goal_data = self.slot_data["goal_rating"]
                    even_more_goal_data = "none"
                case "contract_collection":
                    goal_data = self.slot_data["goal_amount"]
                    more_goal_data = "none"
                    even_more_goal_data = "none"
                case "contract_collection_level_completion":
                    goal_data = self.slot_data["goal_amount"]
                    more_goal_data = self.slot_data["goal_location_name"]
                    even_more_goal_data = self.slot_data["goal_rating"]
                case "number_of_completions":
                    goal_data = self.slot_data["goal_amount"]
                    more_goal_data = self.slot_data["goal_rating"]
                    even_more_goal_data = "none"

            logger.info("Sending Goal information...")
            r = requests.get(self.peacock_url+"/setGoal/"+self.slot_data["goal_mode"]+"/"+str(goal_data)+"/"+more_goal_data+"/"+even_more_goal_data)
            r.raise_for_status()
            logger.info("Goal information sent.")
        except Exception as e:
            self.print_error("No response when sending Goal Data to Peacock, disconnecting!")
            print("Error sending goal info:", e)
            raise RuntimeError()

    def process_recieved_items(self, items:list[NetworkItem]):
        itemIds = []
        for item in items:
            itemIds.append(item.item - base_id)
            if item.item == base_id + item_table["Contract Piece"][0]:
                self.collected_contract_pieces += 1

            if len(itemIds) > 500:
                self.send_items(itemIds)
                itemIds = []
        
        self.send_items(itemIds)
          
    def send_items(self, itemIds:list[int]):
        try:
            r = requests.post(self.peacock_url+"/sendItems?items="+str(itemIds)) 
            r.raise_for_status()
        except Exception as e:
            self.print_error("No response when sending Items to Peacock, disconnecting!")
            asyncio.run_coroutine_threadsafe(self.disconnect(False), asyncio.get_running_loop())
 
    def process_checked_locations(self, locations:list[int]):
        locationIds = []
        for locationId in locations:
            if locationId == self.slot_data["goal_location_id"]:
                continue #If goal was collected or cheated, don't let Peacock know
                        #so challange remains completeable and thus goalable (don't check for goal here, as a collect could goal you)

            locationIds.append(locationId-base_id)

            if len(locationIds) > 500:
                self.send_checked_locations(locationIds)
                locationIds = []
        
        self.send_checked_locations(locationIds)

    def send_checked_locations(self, locationIds:list[int]):
        try:
            r = requests.post(self.peacock_url+"/sendCheckedLocations?items="+str(locationIds)) 
            r.raise_for_status()
        except Exception as e:
            self.print_error("No response when sending checked Locations to Peacock, disconnecting")
            asyncio.run_coroutine_threadsafe(self.disconnect(False), asyncio.get_running_loop())

    def periodically_get_checks(self):
        self.sse_running = True
        while self.sse_running:
            try:
                response = requests.get(f"{self.peacock_url}/checks")

                response.raise_for_status()  # Raises on 4xx and 5xx codes
                checks = response.json()
                asyncio.run(self.check_locations(checks))

                if self.slot_data["goal_location_id"] in checks:
                    asyncio.run(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
            except requests.RequestException as e:
                print("Error fetching checks:", e)
                self.print_error("No response when trying to get Checks from Peacock, disconnecting")
                asyncio.run(self.disconnect(False))
                self.sse_running = False
            if self.sse_running:
                time.sleep(3)
    def print_error(self, text:str):
        self.ui.print_json([{"text":text,"type":"color","color":"red"}])

async def main(args):
    ctx = HitmanContext(args.connect, args.password)
    ctx.auth = args.name

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()

def launch(*args):
    import colorama

    parser = get_base_parser(description="HITMAN Archipelago Client, for interfacing with a Peacock server.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    args = handle_url_arg(args, parser=parser)

    # use colorama to display colored text highlighting on windows
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()

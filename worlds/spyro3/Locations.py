from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import Spyro3Item

class Spyro3LocationCategory(IntEnum):
    EGG = 0,
    SKIP = 1,
    EVENT = 2,
    GEM = 3,
    SKILLPOINT = 4,
    GEM_25 = 5,
    GEM_50 = 6,
    GEM_75 = 7,
    HINT = 8,
    SKILLPOINT_GOAL = 9,
    TOTAL_GEM = 10,
    LIFE_BOTTLE = 11,
    LIFE_BOTTLE_HARD = 12,
    GEMSANITY = 13,
    EGG_EOL = 14


class Spyro3LocationData(NamedTuple):
    name: str
    default_item: str
    category: Spyro3LocationCategory


class Spyro3Location(Location):
    game: str = "Spyro 3"
    category: Spyro3LocationCategory
    default_item_name: str

    def __init__(
        self,
        player: int,
        name: str,
        category: Spyro3LocationCategory,
        default_item_name: str,
        address: Optional[int] = None,
        parent: Optional[Region] = None
    ):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.name = name

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 1230000
        table_offset = 1000

        table_order = [
            "Sunrise Spring","Sunny Villa","Cloud Spires","Molten Crater","Seashell Shore","Mushroom Speedway","Sheila's Alp", "Buzz", "Crawdad Farm",
            "Midday Gardens","Icy Peak","Enchanted Towers","Spooky Swamp","Bamboo Terrace","Country Speedway","Sgt. Byrd's Base","Spike","Spider Town",
            "Evening Lake","Frozen Altars","Lost Fleet","Fireworks Factory","Charmed Ridge","Honey Speedway","Bentley's Outpost","Scorch","Starfish Reef",
            "Midnight Mountain","Crystal Islands","Desert Ruins","Haunted Tomb","Dino Mines","Harbor Speedway","Agent 9's Lab","Sorceress","Bugbot Factory","Super Bonus Round",
            "Inventory"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output

    def place_locked_item(self, item: Spyro3Item):
        self.item = item
        self.locked = True
        item.location = self


hint_locations = [
    "Sunrise Spring: First Zoe",
    "Sunrise Spring: Superfly Zoe",
    "Sunrise Spring: Camera Zoe",
    "Sunny Villa: Big Rhynoc Zoe",
    "Sunny Villa: Checkpoint Zoe",
    "Cloud Spires: Metal Armor Zoe",
    "Cloud Spires: Glide Zoe",
    "Molten Crater: Fodder Zoe",
    "Seashell Shore: Atlas Zoe",
    "Seashell Shore: Hover Zoe",
    "Sheila's Alp: Controls Zoe",
    "Midday Gardens: Fireball Zoe",
    "Evening Lake: Invincibility Zoe"
]

# To ensure backwards compatibility, do not reorder locations or insert new ones in the middle of a list.
location_tables = {
    #Homeworld 1
    "Sunrise Spring": [
        Spyro3LocationData("Sunrise Spring Home: Learn gliding. (Coltrane)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunrise Spring Home: Egg by the stream. (Isabelle)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunrise Spring Home: Fly through the cave. (Ami)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunrise Spring Home: Bottom of the lake. (Bruce)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunrise Spring Home: Head bash the rock. (Liam)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunrise Spring: First Zoe", "Hint 1", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Sunrise Spring: Superfly Zoe", "Hint 2", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Sunrise Spring: Camera Zoe", "Hint 3", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Sunrise Spring: Life Bottle By Starting Pond", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Sunrise Spring: Life Bottle By Sheila's Alp", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Sunny Villa": [
        Spyro3LocationData("Sunny Villa: Rescue the mayor. (Sanders)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Sunny Villa: Hop to Rapunzel. (Lucy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunny Villa: Lizard skating I. (Emily)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunny Villa: Lizard skating II. (Daisy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunny Villa: Egg by the building. (Vanessa)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunny Villa: Glide to the spring. (Miles)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sunny Villa Complete", "Sunny Villa Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Sunny Villa: Flame all trees (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Sunny Villa: Skateboard course record I (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Sunny Villa: Flame all trees (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Sunny Villa: Skateboard course record I (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Sunny Villa: Big Rhynoc Zoe", "Hint 4", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Sunny Villa: Checkpoint Zoe", "Hint 5", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Sunny Villa: Life Bottle Past Starting Area Pillars", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Sunny Villa: Life Bottle By Skateboarding Sub-Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Cloud Spires": [
        Spyro3LocationData("Cloud Spires: Turn on the cloud generator. (Henry)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Cloud Spires: Plant the sun seeds. (LuLu)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Cloud Spires: Bell tower spirits. (Jake)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Cloud Spires: Bell tower thief. (Bryan)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Cloud Spires: Run along the wall. (Stephanie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Cloud Spires: Glide to the island. (Clare)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Cloud Spires Complete", "Cloud Spires Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Cloud Spires: Metal Armor Zoe", "Hint 6", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Cloud Spires: Glide Zoe", "Hint 7", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Cloud Spires: Life Bottle Past Whirlwind", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Molten Crater": [
        Spyro3LocationData("Molten Crater: Get to the tiki lodge. (Curlie)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Molten Crater: Replace idol heads. (Ryan)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Molten Crater: Catch the thief. (Moira)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Molten Crater: Supercharge after the thief. (Kermitt)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Molten Crater: Sgt. Byrd blows up a wall. (Luna)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Molten Crater: Egg by lava river. (Rikki)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Molten Crater Complete", "Molten Crater Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Molten Crater: Assemble tiki heads (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Molten Crater: Supercharge the wall (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Molten Crater: Assemble tiki heads (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Molten Crater: Supercharge the wall (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Molten Crater: Fodder Zoe", "Hint 8", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Molten Crater: Life Bottle in Breakable Wall in Thief Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Seashell Shore": [
        Spyro3LocationData("Seashell Shore: Free the seals. (Dizzy)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Seashell Shore: Under the docks. (Jason)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Seashell Shore: Destroy the sand castle. (Mollie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Seashell Shore: Defeat the shark sub. (Jackie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Seashell Shore: Clear out the pipe. (Duke)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Seashell Shore: Hop to the secret cave. (Jared)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Seashell Shore Complete", "Seashell Shore Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Seashell Shore: Catch the funky chicken (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Seashell Shore: Catch the funky chicken (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Seashell Shore: Atlas Zoe", "Hint 9", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Seashell Shore: Hover Zoe", "Hint 10", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Seashell Shore: Life Bottle in Nook in Second Room", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Mushroom Speedway": [
        Spyro3LocationData("Mushroom Speedway: Time attack. (Sabina)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Mushroom Speedway: Race the butterflies. (John)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Mushroom Speedway: Hunter's dogfight. (Tater)", "Egg", Spyro3LocationCategory.EGG),
    ],
    "Sheila's Alp": [
        Spyro3LocationData("Sheila's Alp: Help Bobby get home. (Nan)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Sheila's Alp: Help Pete get home. (Jenny)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sheila's Alp: Help Billy get home. (Ruby)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sheila's Alp Complete", "Sheila's Alp Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Sheila's Alp: Controls Zoe", "Hint 11", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Sheila's Alp: Life Bottle by Headbash Crate in Huts Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Buzz": [
        Spyro3LocationData("Buzz's Dungeon: Defeat Buzz. (Grayson)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Buzz Defeated", "Buzz Defeated", Spyro3LocationCategory.EVENT)
    ],
    "Crawdad Farm": [
        Spyro3LocationData("Crawdad Farm: Take Sparx to the farm. (Nora)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Crawdad Farm Complete", "Crawdad Farm Complete", Spyro3LocationCategory.EVENT),
    ],
    #Homeworld 2
    "Midday Gardens": [
        Spyro3LocationData("Midday Gardens Home: Underwater egg. (Dave)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midday Gardens Home: Secret ice cave. (Mingus)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midday Gardens Home: Catch the thief. (Trixie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midday Gardens Home: Superflame the flowerpots. (Matt)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midday Gardens Home: Climb to the ledge. (Modesty)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midday Gardens: Fireball Zoe", "Hint 12", Spyro3LocationCategory.HINT),
    ],
    "Icy Peak": [
        Spyro3LocationData("Icy Peak: Find Doug the polar bear. (Chet)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Icy Peak: Protect Nancy the skater. (Cerny)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Icy Peak: Speedy thieves I. (Betty)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Icy Peak: Speedy thieves II. (Scout)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Icy Peak: On top of a ledge. (Maynard)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Icy Peak: Glide to the sky island. (Reez)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Icy Peak Complete", "Icy Peak Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Icy Peak: Glide to pedestal (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Icy Peak: Glide to pedestal (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Icy Peak: Life Bottle on hidden path to 'Glide to the sky island. (Reez)'", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Enchanted Towers": [
        Spyro3LocationData("Enchanted Towers: Destroy the sorceress statue. (Peanut)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Enchanted Towers: Rescue the lost wolf. (Lys)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Enchanted Towers: Collect the bones. (Ralph)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Enchanted Towers: Trick skater I. (Caroline)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Enchanted Towers: Trick skater II. (Alex)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Enchanted Towers: Glide to the small island. (Gladys)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Enchanted Towers Complete", "Enchanted Towers Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Enchanted Towers: Skateboard course record II (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Enchanted Towers: Skateboard course record II (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Enchanted Towers: Life Bottle on Tower Near Start", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Spooky Swamp": [
        Spyro3LocationData("Spooky Swamp: Find Shiny the firefly. (Thelonious)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Spooky Swamp: Jump to the island. (Michael)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Spooky Swamp: Across the treetops. (Frank)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Spooky Swamp: Escort the twins I. (Peggy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Spooky Swamp: Escort the twins II. (Michele)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Spooky Swamp: Defeat sleepy head. (Herbi)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Spooky Swamp Complete", "Spooky Swamp Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Spooky Swamp: Destroy all piranha signs (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Spooky Swamp: Destroy all piranha signs (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
    ],
    "Bamboo Terrace": [
        Spyro3LocationData("Bamboo Terrace: Clear the pandas' path. (Tom)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Bamboo Terrace: Shoot from the boat. (Rusty)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bamboo Terrace: Smash to the mountain top. (Brubeck)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bamboo Terrace: Glide to the hidden cave. (Madison)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bamboo Terrace: Glide to the small island. (Dwight)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bamboo Terrace: Catch the thief. (Pee-wee)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bamboo Terrace Complete", "Bamboo Terrace Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Bamboo Terrace: Life Bottle in Bentley Sub-Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Bamboo Terrace: Life Bottle in Underwater Breakable Wall 1", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Bamboo Terrace: Life Bottle in Underwater Breakable Wall 2", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Bamboo Terrace: Life Bottle in Underwater Breakable Wall 3", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Bamboo Terrace: Life Bottle in Underwater Breakable Wall 4", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Country Speedway": [
        Spyro3LocationData("Country Speedway: Time attack. (Gavin)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Country Speedway: Race the pigs. (Shemp)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Country Speedway: Hunter's rescue mission. (Roberto)", "Egg", Spyro3LocationCategory.EGG),
    ],
    "Sgt. Byrd's Base": [
        Spyro3LocationData("Sgt. Byrd's Base: Clear the building. (RyanLee)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Sgt. Byrd's Base: Clear the caves. (Sigfried)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sgt. Byrd's Base: Rescue 5 hummingbirds. (Roy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sgt. Byrd's Base Complete", "Sgt. Byrd's Base Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Sgt. Byrd's Base: Bomb the gophers (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Sgt. Byrd's Base: Bomb the gophers (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Sgt. Byrd's Base: Life Bottle above Exit Portal", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Spike": [
        Spyro3LocationData("Spike's Arena: Defeat Spike. (Monique)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Spike Defeated", "Spike Defeated", Spyro3LocationCategory.EVENT)
    ],
    "Spider Town": [
        Spyro3LocationData("Spider Town: Go to town. (Tootie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Spider Town Complete", "Spider Town Complete", Spyro3LocationCategory.EVENT),
    ],
    #Homeworld 3
    "Evening Lake": [
        Spyro3LocationData("Evening Lake Home: On the bridge (Ted)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Evening Lake Home: Glide to the tower. (Hannah)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Evening Lake Home: Break the tower wall. (Stooby)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Evening Lake Home: Belly of the whale. (Jonah)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Evening Lake Home: I'm invincible! (Stuart)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Evening Lake: Invincibility Zoe", "Hint 13", Spyro3LocationCategory.HINT),
        Spyro3LocationData("Evening Lake: Life Bottle on Upper Path", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Frozen Altars": [
        Spyro3LocationData("Frozen Altars: Melt the snowmen. (Jana)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Frozen Altars: Box the yeti. (Aly)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Frozen Altars: Box the yeti again! (Ricco)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Frozen Altars: Catch the ice cats. (Ba'ah)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Frozen Altars: Glide from the temple roof. (Cecil)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Frozen Altars: Across the rooftops. (Jasper)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Frozen Altars Complete", "Frozen Altars Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Frozen Altars: Beat yeti in two rounds (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Frozen Altars: Beat yeti in two rounds (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
    ],
    "Lost Fleet": [
        Spyro3LocationData("Lost Fleet: Find Crazy Ed's treasure. (Craig)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Lost Fleet: Sink the subs I. (Ethel)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Lost Fleet: Sink the subs II. (Dolores)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Lost Fleet: Swim through acid. (Chad)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Lost Fleet: Skate race the rhynocs. (Oliver)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Lost Fleet: Skate race Hunter. (Aiden)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Lost Fleet Complete", "Lost Fleet Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Lost Fleet: Skateboard record time (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Lost Fleet: Skateboard record time (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Lost Fleet: Life Bottle in Acid River", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Lost Fleet: Life Bottle in Skateboarding Sub-Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Fireworks Factory": [
        Spyro3LocationData("Fireworks Factory: Destwoy the wocket! (Grady)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Fireworks Factory: You're doomed! (Patty)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Fireworks Factory: You're still doomed! (Donovan)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Fireworks Factory: Ninja HQ (Sam)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Fireworks Factory: Bad dragon! (Evan)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Fireworks Factory: Hidden in an alcove. (Noodles)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Fireworks Factory Complete", "Fireworks Factory Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Fireworks Factory: Find Agent 9's powerup (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Fireworks Factory: Find Agent 9's powerup (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Fireworks Factory: Life Bottle in Agent 9 Sub-Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Fireworks Factory: Life Bottle Out of Bounds Near Start", "Filler", Spyro3LocationCategory.LIFE_BOTTLE_HARD),
    ],
    "Charmed Ridge": [
        Spyro3LocationData("Charmed Ridge: Rescue the Fairy Princess. (Sakura)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Charmed Ridge: Glide to the tower. (Moe)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Charmed Ridge: Egg in the cave. (Benjamin)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Charmed Ridge: Cat witch chaos. (Abby)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Charmed Ridge: Jack and the beanstalk I. (Shelley)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Charmed Ridge: Jack and the beanstalk II. (Chuck)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Charmed Ridge Complete", "Charmed Ridge Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Charmed Ridge: The Impossible Tower (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Charmed Ridge: Shoot the temple windows (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Charmed Ridge: The Impossible Tower (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Charmed Ridge: Shoot the temple windows (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Charmed Ridge: Life Bottle by End of Level 1", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Charmed Ridge: Life Bottle by End of Level 2", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Honey Speedway": [
        Spyro3LocationData("Honey Speedway: Time attack. (Chris)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Honey Speedway: Race the bees (Henri)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Honey Speedway: Hunter's narrow escape. (Nori)", "Egg", Spyro3LocationCategory.EGG),
    ],
    "Bentley's Outpost": [
        Spyro3LocationData("Bentley's Outpost: Help Bartholomew home. (Eric)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Bentley's Outpost: The Gong Show (Brian)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bentley's Outpost: Snowball's chance. (Charlie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bentley's Outpost Complete", "Bentley's Outpost Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Bentley's Outpost: Push box off the cliff (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Bentley's Outpost: Push box off the cliff (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
    ],
    "Scorch": [
        Spyro3LocationData("Scorch's Pit: Defeat Scorch. (James)", "Egg", Spyro3LocationCategory.EGG_EOL),
        Spyro3LocationData("Scorch Defeated", "Scorch Defeated", Spyro3LocationCategory.EVENT)
    ],
    "Starfish Reef": [
        Spyro3LocationData("Starfish Reef: Beach party! (Ahnashawn)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Starfish Reef Complete", "Starfish Reef Complete", Spyro3LocationCategory.EVENT),
    ],
    #Homeworld 4
    "Midnight Mountain": [
        Spyro3LocationData("Midnight Mountain Home: Shhh, it's a secret (Billy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midnight Mountain Home: At the top of the waterfall. (Evie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midnight Mountain Home: Catch the thief. (Maiken)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midnight Mountain Home: Glide to the island. (Saki)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midnight Mountain Home: Stomp the floor. (Buddy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midnight Mountain Home: Egg for sale. (Al)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Midnight Mountain Home: Moneybags Chase Complete", "Moneybags Chase Complete", Spyro3LocationCategory.EVENT),
    ],
    "Crystal Islands": [
        Spyro3LocationData("Crystal Islands: Reach the crystal tower. (Lloyd)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Crystal Islands: Ride the slide. (Elloise)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Crystal Islands: Whack a mole. (Hank)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Crystal Islands: Fly to the hidden egg. (Grace)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Crystal Islands: Glide to the island. (Manie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Crystal Islands: Catch the flying thief. (Max)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Crystal Islands Complete", "Crystal Islands Complete", Spyro3LocationCategory.EVENT),
    ],
    "Desert Ruins": [
        Spyro3LocationData("Desert Ruins: Raid the tomb. (Marty)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Desert Ruins: Shark shootin'. (Sadie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Desert Ruins: Krash Kangaroo I. (Lester)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Desert Ruins: Krash Kangaroo II. (Pete)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Desert Ruins: Sink or singe. (Nelly)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Desert Ruins: Give me a hand (Andy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Desert Ruins Complete", "Desert Ruins Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Desert Ruins: Destroy all seaweed (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Desert Ruins: Destroy all seaweed (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Desert Ruins: Life Bottle near Sharks Sub-Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
        Spyro3LocationData("Desert Ruins: Life Bottle before Moneybags", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Haunted Tomb": [
        Spyro3LocationData("Haunted Tomb: Release the temple dweller. (Will)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Haunted Tomb: Snake slide. (Malcom)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Haunted Tomb: Tank blast I. (MJ)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Haunted Tomb: Tank blast II. (TJ)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Haunted Tomb: Clear the caves. (Roxy)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Haunted Tomb: Climb the wall. (Christine)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Haunted Tomb Complete", "Haunted Tomb Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Haunted Tomb: Swim into the dark hole (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Haunted Tomb: Swim into the dark hole (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Haunted Tomb: Life Bottle by Upper Falling Rocks Area", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Dino Mines": [
        Spyro3LocationData("Dino Mines: Jail break! (Kiki)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Dino Mines: Shafted! (Elliot)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Dino Mines: Swim through the wall. (Romey)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Dino Mines: Gunfight at the Jurassic Corral. (Sharon)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Dino Mines: Leap of faith. (Dan)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Dino Mines: Take it to the bank. (Sergio)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Dino Mines Complete", "Dino Mines Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Dino Mines: Hit all the seahorses (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Dino Mines: Hit the secret dino (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Dino Mines: Hit all the seahorses (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Dino Mines: Hit the secret dino (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
        Spyro3LocationData("Dino Mines: Life Bottle in Fireplace", "Filler", Spyro3LocationCategory.LIFE_BOTTLE),
    ],
    "Harbor Speedway": [
        Spyro3LocationData("Harbor Speedway: Time attack. (Kobe)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Harbor Speedway: Race the blue footed boobies. (Jessie)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Harbor Speedway: Hunter's pursuit. (Sara)", "Egg", Spyro3LocationCategory.EGG),
    ],
    "Agent 9's Lab": [
        Spyro3LocationData("Agent 9's Lab: Blast and bomb the rhynocs. (Rowan)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Agent 9's Lab: Snipe the boats (Tony)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Agent 9's Lab: This place has gone to the birds. (Beulah)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Agent 9's Lab Complete", "Agent 9's Lab Complete", Spyro3LocationCategory.EVENT),
        Spyro3LocationData("Agent 9's Lab: Blow up all palm trees (Skill Point)", "Filler", Spyro3LocationCategory.SKILLPOINT),
        Spyro3LocationData("Agent 9's Lab: Blow up all palm trees (Goal)", "Skill Point", Spyro3LocationCategory.SKILLPOINT_GOAL),
    ],
    "Sorceress": [
        Spyro3LocationData("Sorceress's Lair: Defeat the Sorceress? (George)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Sorceress Defeated", "Sorceress Defeated", Spyro3LocationCategory.EVENT)
    ],
    "Bugbot Factory": [
        Spyro3LocationData("Bugbot Factory: Shut down the factory. (Anabelle)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Bugbot Factory Complete", "Bugbot Factory Complete", Spyro3LocationCategory.EVENT),
    ],
    "Super Bonus Round": [
        Spyro3LocationData("Super Bonus Round: Woo, a secret egg. (Yin Yang)", "Egg", Spyro3LocationCategory.EGG),
        Spyro3LocationData("Super Bonus Round Complete", "Super Bonus Round Complete", Spyro3LocationCategory.EVENT),
    ],
    # Total counts like eggs and gems
    "Inventory": [
        Spyro3LocationData("Total Gems: 500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 1000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 1500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 2000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 2500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 3000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 3500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 4000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 4500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 5000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 5500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 6000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 6500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 7000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 7500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 8000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 8500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 9000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 9500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 10000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 10500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 11000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 11500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 12000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 12500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 13000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 13500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 14000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 14500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 15000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 15500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 16000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 16500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 17000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 17500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 18000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 18500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 19000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 19500", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Total Gems: 20000", "Filler", Spyro3LocationCategory.TOTAL_GEM),
        Spyro3LocationData("Sunrise Spring: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Sunrise Spring: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Sunrise Spring: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Sunrise Spring: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Sunny Villa: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Sunny Villa: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Sunny Villa: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Sunny Villa: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Cloud Spires: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Cloud Spires: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Cloud Spires: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Cloud Spires: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Molten Crater: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Molten Crater: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Molten Crater: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Molten Crater: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Seashell Shore: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Seashell Shore: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Seashell Shore: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Seashell Shore: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Mushroom Speedway: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Mushroom Speedway: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Mushroom Speedway: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Mushroom Speedway: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Sheila's Alp: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Sheila's Alp: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Sheila's Alp: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Sheila's Alp: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Crawdad Farm: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Crawdad Farm: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Crawdad Farm: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Crawdad Farm: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Midday Gardens: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Midday Gardens: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Midday Gardens: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Midday Gardens: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Icy Peak: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Icy Peak: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Icy Peak: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Icy Peak: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Enchanted Towers: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Enchanted Towers: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Enchanted Towers: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Enchanted Towers: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Spooky Swamp: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Spooky Swamp: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Spooky Swamp: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Spooky Swamp: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Bamboo Terrace: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Bamboo Terrace: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Bamboo Terrace: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Bamboo Terrace: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Country Speedway: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Country Speedway: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Country Speedway: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Country Speedway: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Sgt. Byrd's Base: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Sgt. Byrd's Base: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Sgt. Byrd's Base: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Sgt. Byrd's Base: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Spider Town: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Spider Town: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Spider Town: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Spider Town: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Evening Lake: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Evening Lake: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Evening Lake: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Evening Lake: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Frozen Altars: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Frozen Altars: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Frozen Altars: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Frozen Altars: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Lost Fleet: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Lost Fleet: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Lost Fleet: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Lost Fleet: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Fireworks Factory: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Fireworks Factory: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Fireworks Factory: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Fireworks Factory: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Charmed Ridge: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Charmed Ridge: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Charmed Ridge: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Charmed Ridge: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Honey Speedway: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Honey Speedway: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Honey Speedway: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Honey Speedway: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Bentley's Outpost: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Bentley's Outpost: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Bentley's Outpost: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Bentley's Outpost: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Starfish Reef: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Starfish Reef: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Starfish Reef: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Starfish Reef: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Midnight Mountain: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Midnight Mountain: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Midnight Mountain: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Midnight Mountain: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Crystal Islands: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Crystal Islands: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Crystal Islands: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Crystal Islands: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Desert Ruins: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Desert Ruins: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Desert Ruins: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Desert Ruins: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Haunted Tomb: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Haunted Tomb: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Haunted Tomb: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Haunted Tomb: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Dino Mines: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Dino Mines: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Dino Mines: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Dino Mines: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Harbor Speedway: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Harbor Speedway: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Harbor Speedway: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Harbor Speedway: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Agent 9's Lab: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Agent 9's Lab: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Agent 9's Lab: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Agent 9's Lab: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Bugbot Factory: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Bugbot Factory: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Bugbot Factory: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Bugbot Factory: All Gems", "Filler", Spyro3LocationCategory.GEM),
        Spyro3LocationData("Super Bonus Round: 25% Gems", "Filler", Spyro3LocationCategory.GEM_25),
        Spyro3LocationData("Super Bonus Round: 50% Gems", "Filler", Spyro3LocationCategory.GEM_50),
        Spyro3LocationData("Super Bonus Round: 75% Gems", "Filler", Spyro3LocationCategory.GEM_75),
        Spyro3LocationData("Super Bonus Round: All Gems", "Filler", Spyro3LocationCategory.GEM),
    ]
}

sunrise_gems = []
for i in range(142):
    sunrise_gems += [Spyro3LocationData(f"Sunrise Spring: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Sunrise Spring"] = location_tables["Sunrise Spring"] + sunrise_gems
sunny_gems = []
for i in range(198):
    sunny_gems += [Spyro3LocationData(f"Sunny Villa: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Sunny Villa"] = location_tables["Sunny Villa"] + sunny_gems
cloud_gems = []
for i in range(148):
    cloud_gems += [Spyro3LocationData(f"Cloud Spires: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Cloud Spires"] = location_tables["Cloud Spires"] + cloud_gems
molten_gems = []
for i in range(147):
    molten_gems += [Spyro3LocationData(f"Molten Crater: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Molten Crater"] = location_tables["Molten Crater"] + molten_gems
seashell_gems = []
for i in range(169):
    seashell_gems += [Spyro3LocationData(f"Seashell Shore: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Seashell Shore"] = location_tables["Seashell Shore"] + seashell_gems
mushroom_gems = []
for i in range(32):
    mushroom_gems += [Spyro3LocationData(f"Mushroom Speedway: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Mushroom Speedway"] = location_tables["Mushroom Speedway"] + mushroom_gems
sheila_gems = []
for i in range(117):
    sheila_gems += [Spyro3LocationData(f"Sheila's Alp: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Sheila's Alp"] = location_tables["Sheila's Alp"] + sheila_gems
crawdad_gems = []
for i in range(47):
    crawdad_gems += [Spyro3LocationData(f"Crawdad Farm: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Crawdad Farm"] = location_tables["Crawdad Farm"] + crawdad_gems

midday_gems = []
for i in range(123):
    midday_gems += [Spyro3LocationData(f"Midday Gardens: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Midday Gardens"] = location_tables["Midday Gardens"] + midday_gems
icy_gems = []
for i in range(175):
    icy_gems += [Spyro3LocationData(f"Icy Peak: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Icy Peak"] = location_tables["Icy Peak"] + icy_gems
enchanted_gems = []
for i in range(174):
    enchanted_gems += [Spyro3LocationData(f"Enchanted Towers: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Enchanted Towers"] = location_tables["Enchanted Towers"] + enchanted_gems
spooky_gems = []
for i in range(151):
    spooky_gems += [Spyro3LocationData(f"Spooky Swamp: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Spooky Swamp"] = location_tables["Spooky Swamp"] + spooky_gems
bamboo_gems = []
for i in range(159):
    bamboo_gems += [Spyro3LocationData(f"Bamboo Terrace: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Bamboo Terrace"] = location_tables["Bamboo Terrace"] + bamboo_gems
country_gems = []
for i in range(32):
    country_gems += [Spyro3LocationData(f"Country Speedway: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Country Speedway"] = location_tables["Country Speedway"] + country_gems
byrd_gems = []
for i in range(117):
    byrd_gems += [Spyro3LocationData(f"Sgt. Byrd's Base: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Sgt. Byrd's Base"] = location_tables["Sgt. Byrd's Base"] + byrd_gems
spider_gems = []
for i in range(47):
    spider_gems += [Spyro3LocationData(f"Spider Town: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Spider Town"] = location_tables["Spider Town"] + spider_gems

evening_gems = []
for i in range(75):
    evening_gems += [Spyro3LocationData(f"Evening Lake: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Evening Lake"] = location_tables["Evening Lake"] + evening_gems
frozen_gems = []
for i in range(129):
    frozen_gems += [Spyro3LocationData(f"Frozen Altars: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Frozen Altars"] = location_tables["Frozen Altars"] + frozen_gems
fleet_gems = []
for i in range(223):
    fleet_gems += [Spyro3LocationData(f"Lost Fleet: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Lost Fleet"] = location_tables["Lost Fleet"] + fleet_gems
fireworks_gems = []
for i in range(233):
    fireworks_gems += [Spyro3LocationData(f"Fireworks Factory: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Fireworks Factory"] = location_tables["Fireworks Factory"] + fireworks_gems
charmed_gems = []
for i in range(175):
    charmed_gems += [Spyro3LocationData(f"Charmed Ridge: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Charmed Ridge"] = location_tables["Charmed Ridge"] + charmed_gems
honey_gems = []
for i in range(32):
    honey_gems += [Spyro3LocationData(f"Honey Speedway: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Honey Speedway"] = location_tables["Honey Speedway"] + honey_gems
bentley_gems = []
for i in range(109):
    bentley_gems += [Spyro3LocationData(f"Bentley's Outpost: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Bentley's Outpost"] = location_tables["Bentley's Outpost"] + bentley_gems
starfish_gems = []
for i in range(53):
    starfish_gems += [Spyro3LocationData(f"Starfish Reef: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Starfish Reef"] = location_tables["Starfish Reef"] + starfish_gems

midnight_gems = []
for i in range(105):
    midnight_gems += [Spyro3LocationData(f"Midnight Mountain: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Midnight Mountain"] = location_tables["Midnight Mountain"] + midnight_gems
crystal_gems = []
for i in range(205):
    crystal_gems += [Spyro3LocationData(f"Crystal Islands: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Crystal Islands"] = location_tables["Crystal Islands"] + crystal_gems
desert_gems = []
for i in range(144):
    desert_gems += [Spyro3LocationData(f"Desert Ruins: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Desert Ruins"] = location_tables["Desert Ruins"] + desert_gems
haunted_gems = []
for i in range(115):
    haunted_gems += [Spyro3LocationData(f"Haunted Tomb: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Haunted Tomb"] = location_tables["Haunted Tomb"] + haunted_gems
dino_gems = []
for i in range(143):
    dino_gems += [Spyro3LocationData(f"Dino Mines: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Dino Mines"] = location_tables["Dino Mines"] + dino_gems
harbor_gems = []
for i in range(32):
    harbor_gems += [Spyro3LocationData(f"Harbor Speedway: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Harbor Speedway"] = location_tables["Harbor Speedway"] + harbor_gems
agent_gems = []
for i in range(106):
    agent_gems += [Spyro3LocationData(f"Agent 9's Lab: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Agent 9's Lab"] = location_tables["Agent 9's Lab"] + agent_gems
bugbot_gems = []
for i in range(42):
    bugbot_gems += [Spyro3LocationData(f"Bugbot Factory: Gem {i + 1}", "Filler", Spyro3LocationCategory.GEMSANITY)]
location_tables["Bugbot Factory"] = location_tables["Bugbot Factory"] + bugbot_gems


location_dictionary: Dict[str, Spyro3LocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})

location_name_groups = {"Speedways": set(), "Sparx Levels": set(), "Speedway Races": set(), "Skateboarding": set()}
speedways = ["Mushroom Speedway", "Country Speedway", "Honey Speedway", "Harbor Speedway"]
for location in location_dictionary.keys():
    for speedway in speedways:
        if location.startswith(speedway):
            location_name_groups["Speedways"].add(location)
        if location.startswith(speedway) and "Race the" in location:
            location_name_groups["Speedway Races"].add(location)
sparx_levels = ["Crawdad Farm", "Spider Town", "Starfish Reef", "Bugbot Factory"]
for location in location_dictionary.keys():
    for sparx_level in sparx_levels:
        if location.startswith(sparx_level):
            location_name_groups["Sparx Levels"].add(location)
skateboarding_locations = [
    "Sunny Villa: Lizard skating I. (Emily)",
    "Sunny Villa: Lizard skating II. (Daisy)",
    "Sunny Villa: Skateboard course record I (Skill Point)",
    "Sunny Villa: Skateboard course record I (Goal)",
    "Enchanted Towers: Trick skater I. (Caroline)",
    "Enchanted Towers: Trick skater II. (Alex)",
    "Enchanted Towers: Skateboard course record II (Skill Point)",
    "Enchanted Towers: Skateboard course record II (Goal)",
    "Lost Fleet: Skate race the rhynocs. (Oliver)",
    "Lost Fleet: Skate race Hunter. (Aiden)",
    "Lost Fleet: Skateboard record time (Skill Point)",
    "Lost Fleet: Skateboard record time (Goal)"
]
for location in skateboarding_locations:
    location_name_groups["Skateboarding"].add(location)

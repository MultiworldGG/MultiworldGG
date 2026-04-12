from typing import NamedTuple
from BaseClasses import Location
from .Names import *

class LocData(NamedTuple):
    id: int
    region: str


class AUSLocation(Location):
    game: str = "An Untitled Story"

    # override constructor to automatically mark event locations as such
    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        super(AUSLocation, self).__init__(player, name, code, parent)
        self.event = code is None


# Sorting areas alphabetically since a vanilla order doesn't really exist in a comprehensive sense.
# Locations within an area are sorted top-to-bottom, left-to-right.

# Arcade locations are not added to the full location table below.
# This is so they can be added with an option at some point in time.
arcade_location_table = {
    L_SKY_TOWN_ASTROCRASH: LocData(72152, R_START_REGION),  # Exclude?
    L_SKY_TOWN_JUMPBOX: LocData(72162, R_START_REGION),  # Exclude?
    L_SKY_TOWN_KEEPGOING: LocData(72163, R_START_REGION),  # Exclude?
}

blackcastle_location_table = {
    L_BLACKCASTLE_BOSS: LocData(72417, A_BLACKCASTLE),
    L_BLACKCASTLE_FLOWER: LocData(72358, A_BLACKCASTLE),
    L_BLACKCASTLE_REDBLOCKS: LocData(72190, A_BLACKCASTLE),
}

blancland_location_table = {
    L_BLANCLAND_FREEZE: LocData(72187, A_BLANCLAND),
    L_BLANCLAND_KILL: LocData(72186, A_BLANCLAND),
    L_BLANCLAND_POSTBOSS: LocData(72210, A_BLANCLAND),
    L_BLANCLAND_BOSS: LocData(72416, A_BLANCLAND),
    L_BLANCLAND_FLOWER: LocData(72354, A_BLANCLAND),
}

bonus_location_table = {
    L_BONUS_1: LocData(72020, A_FIRECAGE),
    L_BONUS_2: LocData(72135, A_FIRECAGE),
}

bottom_location_table = {
    L_THE_BOTTOM_CLOUD: LocData(72131, A_THE_BOTTOM),
    L_THE_BOTTOM_FLOWER: LocData(72361, A_THE_BOTTOM),
}

cloudrun_location_table = {
    L_CLOUDRUN_FLOWER: LocData(72366, A_THE_BOTTOM),
    L_CLOUDRUN_UNDER: LocData(72141, A_THE_BOTTOM),
    L_CLOUDRUN_MIDDLE: LocData(72142, A_THE_BOTTOM),
    L_CLOUDRUN_BOSS: LocData(72411, A_THE_BOTTOM),
    L_CLOUDRUN_POSTBOSS: LocData(72205, A_THE_BOTTOM),
    L_CLOUDRUN_FARRIGHT: LocData(72143, A_THE_BOTTOM),
}

coldkeep_location_table = {
    L_COLDKEEP_CANNON: LocData(72132, R_START_REGION),
    L_COLDKEEP_BOSS: LocData(72403, R_START_REGION),
    L_COLDKEEP_POSTBOSS: LocData(72010, R_START_REGION),
    L_COLDKEEP_UPPER: LocData(72002, R_START_REGION),
    L_COLDKEEP_LOWER: LocData(72102, R_START_REGION),
}

the_curtain_location_table = {
    L_THE_CURTAIN_FLOWER: LocData(72351, A_MOUNTSIDE),
    L_THE_CURTAIN_KILL: LocData(72161, A_THE_CURTAIN),
    L_THE_CURTAIN_BREAKABLE: LocData(72159, A_THE_CURTAIN),
    L_THE_CURTAIN_BOSS: LocData(72414, A_THE_CURTAIN),
    L_THE_CURTAIN_POSTBOSS: LocData(72208, A_THE_CURTAIN),
}

dark_grotto_location_table = {
    L_DARK_GROTTO_UPPER: LocData(72154, A_DARK_GROTTO),
    L_DARK_GROTTO_CAMPSITE: LocData(72155, A_DARK_GROTTO),
    L_DARK_GROTTO_BOSS: LocData(72413, A_DARK_GROTTO),
    L_DARK_GROTTO_POSTBOSS: LocData(72207, A_DARK_GROTTO),
    L_DARK_GROTTO_TORCHES: LocData(72156, A_DARK_GROTTO),
    L_DARK_GROTTO_FLOWER: LocData(72364, A_DARK_GROTTO),
}

deepdive_location_table = {
    L_DEEPDIVE_LEFT: LocData(72144, A_DEEPDIVE),
    L_DEEPDIVE_CHEST: LocData(72149, A_DEEPDIVE),
    L_DEEPDIVE_LEFTCEILING: LocData(72019, A_DEEPDIVE),
    L_DEEPDIVE_TOP: LocData(72145, A_DEEPDIVE),
    L_DEEPDIVE_LEFTFISHNOOK: LocData(72018, A_DEEPDIVE),
    L_DEEPDIVE_1FISHROOM: LocData(72136, A_DEEPDIVE),
    L_DEEPDIVE_MIDDLEROOM: LocData(72021, A_DEEPDIVE),
    L_DEEPDIVE_BOTTOM: LocData(72185, A_DEEPDIVE),
    L_DEEPDIVE_CARGO: LocData(72151, A_DEEPDIVE),
    L_DEEPDIVE_BOSS: LocData(72412, R_DEEPDIVE_RIGHT),
    L_DEEPDIVE_INBLOCK: LocData(72165, R_DEEPDIVE_RIGHT),
    L_DEEPDIVE_RIGHTFISHNOOK: LocData(72164, R_DEEPDIVE_RIGHT),
    L_DEEPDIVE_FLOWER: LocData(72360, R_DEEPDIVE_RIGHT),
    L_DEEPDIVE_POSTBOSS: LocData(72206, R_DEEPDIVE_RIGHT),
    L_DEEPDIVE_SPIKEPATH: LocData(72184, R_DEEPDIVE_RIGHT),
}

deeptower_location_table = {
    L_DEEPTOWER_DOOR: LocData(72022, A_THE_CURTAIN),
    L_DEEPTOWER_BOSS: LocData(72402, R_START_REGION),
    L_DEEPTOWER_POSTBOSS: LocData(72014, R_START_REGION),
    L_DEEPTOWER_SPIKES: LocData(72101, R_START_REGION),
}

farfall_location_table = {
    L_FARFALL_KILL: LocData(72118, R_START_REGION),
    L_FARFALL_CHEST: LocData(72147, R_START_REGION),
    L_FARFALL_5BALLOONS: LocData(72134, A_FARFALL),
    L_FARFALL_SPECIALBALLOON: LocData(72130, A_THE_BOTTOM),
    L_FARFALL_PITDOOR: LocData(72005, A_FARFALL),
    L_FARFALL_FLOWER: LocData(72356, A_FARFALL),
    L_FARFALL_PITEND: LocData(72122, A_FARFALL),
    L_FARFALL_YELLOWDOOR: LocData(72121, A_FARFALL),
    L_FARFALL_BOSS: LocData(72408, A_STRANGECASTLE),
    L_FARFALL_POSTBOSS: LocData(72202, A_STRANGECASTLE),
}

final_climb_location_table = {
    VICTORY: LocData(None, A_BLACKCASTLE)
}

firecage_location_table = {
    L_FIRECAGE_TOLL: LocData(72008, A_FIRECAGE),
    L_FIRECAGE_LEFTSAVE: LocData(72125, A_FIRECAGE),
    L_FIRECAGE_CRUSHERS: LocData(72124, A_FIRECAGE),
    L_FIRECAGE_UPPERDOOR: LocData(72123, A_FIRECAGE),
    L_FIRECAGE_MIDDLE: LocData(72127, A_FIRECAGE),
    L_FIRECAGE_LOWERDOOR: LocData(72128, A_FIRECAGE),
    L_FIRECAGE_RIGHTSAVE: LocData(72129, A_FIRECAGE),
    L_FIRECAGE_POSTBOSS: LocData(72016, A_FIRECAGE),
    L_FIRECAGE_BOSS: LocData(72407, A_FIRECAGE),
}

grotto_location_table = {
    L_GROTTO_POSTBOSS: LocData(72006, R_START_REGION),
    L_GROTTO_BOSS: LocData(72401, R_START_REGION),
    L_GROTTO_FLOWER: LocData(72367, R_START_REGION),
    L_GROTTO_MURAL: LocData(72107, R_START_REGION),
    L_GROTTO_POSTBOSS2: LocData(72153, A_DEEPDIVE),
    L_GROTTO_BOSS2: LocData(72406, A_DEEPDIVE),
}

highlands_location_table = {
    L_HIGHLANDS_PLATFORM: LocData(72157, A_MOUNTSIDE),
}

icecastle_location_table = {
    L_ICECASTLE_LEFTOUTER: LocData(72167, A_THE_CURTAIN),
    L_ICECASTLE_ENTRYDOOR: LocData(72168, A_THE_CURTAIN),
    L_ICECASTLE_SPIKEFUNNEL: LocData(72166, A_THE_CURTAIN),
    L_ICECASTLE_FLOWER: LocData(72353, A_THE_CURTAIN),
    L_ICECASTLE_YELLOWDOOR: LocData(72171, A_THE_CURTAIN),
    L_ICECASTLE_UNDERSIDE: LocData(72177, A_THE_CURTAIN),
    L_ICECASTLE_TINYDOOR: LocData(72170, A_THE_CURTAIN),
    L_ICECASTLE_CANNONDOOR: LocData(72169, A_THE_CURTAIN),
    L_ICECASTLE_SPIKEFLOOR: LocData(72189, A_THE_CURTAIN),
    L_ICECASTLE_POSTBOSS: LocData(72209, A_THE_CURTAIN),
    L_ICECASTLE_BOSS: LocData(72415, A_THE_CURTAIN),
    L_ICECASTLE_TOPRIGHT: LocData(72172, A_THE_CURTAIN),
}

library_location_table = {
    L_LIBRARY_UPPER: LocData(72183, A_THE_CURTAIN),
    L_LIBRARY_FLOWER: LocData(72363, A_THE_CURTAIN),
}

longbeach_location_table = {
    L_LONGBEACH_FLOWER: LocData(72352, R_START_REGION),
}

mountside_location_table = {
    L_MOUNTSIDE_FLOWER: LocData(72362, A_MOUNTSIDE),
    L_MOUNTSIDE_DOOR: LocData(72023, A_MOUNTSIDE),
}

nightclimb_location_table = {
    L_NIGHTCLIMB_BOSS: LocData(72404, A_NIGHTCLIMB),
    L_NIGHTCLIMB_CANNONS: LocData(72106, A_NIGHTCLIMB),
    L_NIGHTCLIMB_TOP: LocData(72009, A_NIGHTCLIMB),
    L_NIGHTCLIMB_DUCK: LocData(72126, A_NIGHTCLIMB),
    L_NIGHTCLIMB_UPPERSAVE: LocData(72108, A_NIGHTCLIMB),
    L_NIGHTCLIMB_FLOWER: LocData(72359, A_NIGHTCLIMB),
    L_NIGHTCLIMB_RIGHT: LocData(72105, A_NIGHTCLIMB),
    L_NIGHTCLIMB_CHEST: LocData(72150, A_NIGHTCLIMB),
}

nightwalk_location_table = {
    L_NIGHTWALK_UPPEREND: LocData(72158, A_THE_CURTAIN),
    L_NIGHTWALK_NESTFLOWER: LocData(72370, A_THE_CURTAIN),
    L_NIGHTWALK_LOWERFLOWER: LocData(72357, R_START_REGION),
    L_NIGHTWALK_SKYRED: LocData(72117, R_START_REGION),
    L_NIGHTWALK_FIRST: LocData(72001, R_START_REGION),
    L_NIGHTWALK_BREAKABLE: LocData(72120, R_START_REGION),
    L_NIGHTWALK_CHEST: LocData(72160, A_THE_CURTAIN),
    L_NIGHTWALK_SKYTEMPLE: LocData(72017, R_START_REGION),
    L_NIGHTWALK_GROUNDTEMPLE: LocData(72146, R_START_REGION),
    L_NIGHTWALK_TORCHES: LocData(72103, R_START_REGION),
    L_NIGHTWALK_UPPERFLOWER: LocData(72365, A_THE_CURTAIN),
}

rainbowdive_location_table = {
    L_RAINBOWDIVE_4TH: LocData(72421, A_THE_CURTAIN),
    L_RAINBOWDIVE_3RD: LocData(72420, A_THE_CURTAIN),
    L_RAINBOWDIVE_2ND: LocData(72175, A_THE_CURTAIN),
    L_RAINBOWDIVE_1ST: LocData(72176, A_THE_CURTAIN),
}

skylands_location_table = {
    L_SKYLANDS_CHEST: LocData(72179, A_THE_CURTAIN),
    L_SKYLANDS_TOLL: LocData(72188, A_THE_CURTAIN),
    L_SKYLANDS_DUCK: LocData(72180, A_THE_CURTAIN),
    L_SKYLANDS_BALLOONS: LocData(72181, A_THE_CURTAIN),
    L_SKYLANDS_PORTAL: LocData(72182, A_MOUNTSIDE),
    L_SKYLANDS_DOOR: LocData(72192, A_THE_CURTAIN),
    L_SKYLANDS_TOPRIGHT: LocData(72178, A_THE_CURTAIN),
}

skysand_location_table = {
    L_SKYSAND_LEFTSTATUE: LocData(72138, A_SKYSAND),
    L_SKYSAND_FLOWER: LocData(72368, A_SKYSAND),
    L_SKYSAND_BOTTOMSAVE: LocData(72011, A_NIGHTCLIMB),
    L_SKYSAND_POSTBOSS: LocData(72204, A_SKYSAND),
    L_SKYSAND_BOSS: LocData(72410, A_SKYSAND),
    L_SKYSAND_UPPERDOOR: LocData(72140, A_SKYSAND),
    L_SKYSAND_YELLOW: LocData(72139, A_SKYSAND),
    L_SKYSAND_LOWERDOOR: LocData(72137, A_SKYSAND),
    L_SKYSAND_CHEST: LocData(72148, A_SKYSAND),
}

sky_town_location_table = {
    L_SKY_TOWN_YELLOW: LocData(72111, R_START_REGION),
    L_SKY_TOWN_RED: LocData(72110, R_START_REGION),
    L_SKY_TOWN_SHOP1: LocData(72112, R_START_REGION),
    L_SKY_TOWN_SHOP2: LocData(72113, R_START_REGION),
    L_SKY_TOWN_SHOP3: LocData(72114, R_START_REGION),
    L_SKY_TOWN_SHOP4: LocData(72115, R_START_REGION),
    L_SKY_TOWN_SHOP5: LocData(72116, R_START_REGION),
    L_SKY_TOWN_SHOP6: LocData(72004, R_START_REGION),
    L_SKY_TOWN_SHOP7: LocData(72015, R_START_REGION),
    L_SKY_TOWN_SHOP8: LocData(72201, R_START_REGION),
    L_SKY_TOWN_TOWER: LocData(72109, A_NIGHTCLIMB),
    L_SKY_TOWN_FLOWER: LocData(72369, R_START_REGION),
    L_SKY_TOWN_PITLEFT: LocData(72104, R_START_REGION),
    # ST_PIT: LocData(72012, START_REGION),
    L_SKY_TOWN_PITRIGHT: LocData(72007, R_START_REGION),
}

staircase_location_table = {
    L_STAIRCASE_5FLOWERS: LocData(72418, A_THE_CURTAIN),
    L_STAIRCASE_10FLOWERS: LocData(72173, A_THE_CURTAIN),
    L_STAIRCASE_15FLOWERS: LocData(72419, A_THE_CURTAIN),
    L_STAIRCASE_20FLOWERS: LocData(72174, A_THE_CURTAIN),
}

stonecastle_location_table = {
    L_STONECASTLE_FLOWER: LocData(72355, R_START_REGION),
    L_STONECASTLE_UPPER: LocData(72133, R_START_REGION),
    L_STONECASTLE_DOOR: LocData(72003, R_START_REGION),
    L_STONECASTLE_HIDDEN: LocData(72119, R_START_REGION),
    L_STONECASTLE_BOSS: LocData(72405, R_START_REGION),
    L_STONECASTLE_BOSS2: LocData(72409, R_START_REGION),
    L_STONECASTLE_POSTBOSS: LocData(72013, R_START_REGION),
    L_STONECASTLE_POSTBOSS2: LocData(72203, R_START_REGION),
}

strangecastle_location_table = {
    L_STRANGECASTLE_END: LocData(72024, A_STRANGECASTLE),
    L_STRANGECASTLE_DOOR: LocData(72191, A_STRANGECASTLE),
}

undertomb_location_table = {
    L_UNDERTOMB_LEFT: LocData(72194, A_LONGBEACH),
    L_UNDERTOMB_LEFTDOOR: LocData(72195, A_LONGBEACH),
    L_UNDERTOMB_RIGHTDOOR: LocData(72193, A_LONGBEACH),
}

base_location_table = {
    **blackcastle_location_table,
    **blancland_location_table,
    **bonus_location_table,
    **bottom_location_table,
    **cloudrun_location_table,
    **coldkeep_location_table,
    **the_curtain_location_table,
    **dark_grotto_location_table,
    **deepdive_location_table,
    **deeptower_location_table,
    **farfall_location_table,
    **firecage_location_table,
    **grotto_location_table,
    **highlands_location_table,
    **icecastle_location_table,
    **library_location_table,
    **longbeach_location_table,
    **mountside_location_table,
    **nightclimb_location_table,
    **nightwalk_location_table,
    **rainbowdive_location_table,
    **skylands_location_table,
    **skysand_location_table,
    **sky_town_location_table,
    **staircase_location_table,
    **stonecastle_location_table,
    **strangecastle_location_table,
    **undertomb_location_table,
    #arcade and final climb are now added in init
}
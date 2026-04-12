import typing
from BaseClasses import Region
from . import world_list
from .Options import SMOOptions
from .Locations import SMOLocation, loc_Cap, loc_Cascade, loc_Cascade_Revisit, \
    loc_Sand, loc_Lake, loc_Wooded, loc_Cloud, loc_Lost, loc_Lost_Revisit, loc_Metro, \
    loc_Snow, loc_Seaside, loc_Luncheon, loc_Ruined, loc_Bowser, loc_Moon, \
    locations_table, post_game_locations_table, loc_Dark, loc_Darker, special_locations_table, \
    loc_Cap_Shop, loc_Cascade_Shop, loc_Sand_Shop, loc_Lake_Shop, loc_Wooded_Shop, \
    loc_Lost_Shop, loc_Metro_Shop, loc_Snow_Shop, loc_Seaside_Shop, loc_Luncheon_Shop, \
    loc_Bowser_Shop, loc_Moon_Shop, loc_Mushroom_Shop, loc_Dark_Outfit, loc_Darker_Outfit, \
    loc_Sand_Revisit, loc_Lake_Post_Seaside, loc_Wooded_Post_Metro, loc_Metro_Post_Sand, \
    loc_Cascade_Post_Metro, loc_Cascade_Post_Snow, loc_Post_Cloud, loc_Moon_Post_Moon, \
    loc_Luncheon_Post_Wooded, loc_Mushroom_Post_Luncheon, loc_Sand_Peace, loc_Wooded_Post_Story1, \
    loc_Wooded_Peace, loc_Metro_Sewer_Access, loc_Metro_Peace, loc_Snow_Peace, loc_Seaside_Peace, \
    loc_Luncheon_Post_Spewart, loc_Luncheon_Post_Cheese_Rocks, loc_Luncheon_Peace, \
    loc_Bowser_Infiltrate, loc_Bowser_Post_Bombing, loc_Bowser_Peace, loc_Postgame_Shop, loc_Sand_Pyramid, \
    loc_Sand_Underground, loc_Bowser_Mecha_Broodal, loc_Cap_Captures, loc_Cap_Captures_Revisit, \
    loc_Cascade_Captures, loc_Sand_Captures, loc_Sand_Captures_Underground, loc_Sand_Captures_Peace, \
    loc_Wooded_Captures, loc_Wooded_Captures_Post_Story1, loc_Wooded_Captures_Postgame, \
    loc_Lake_Captures, loc_Cloud_Captures, loc_Lost_Captures, loc_Metro_Captures, \
    loc_Metro_Captures_Postgame, loc_Seaside_Captures, loc_Snow_Captures, \
    loc_Snow_Captures_Peace, loc_Luncheon_Captures, loc_Luncheon_Captures_Post_Cheese_Rocks, \
    loc_Bowser_Captures, loc_Bowser_Captures_Post_Bombing, loc_Moon_Captures, \
    loc_Moon_Cave_Captures, loc_Mushroom_Captures, loc_Cascade_Peace, loc_Moon_Outfit, loc_Night_Metro, \
    loc_Cascade_Full, loc_Sand_Full

from .Logic import count_moons, total_moons

class SMORegion(Region):
    subregions: typing.List[Region] = []

# world_regions = [
#     ("Cap", loc_Cap, SMOOptions.goal.option_sand),
#     ("Cascade", loc_Cascade, SMOOptions.goal.option_sand),
#     ("Cascade Peace", loc_Cascade_Peace, SMOOptions.goal.option_sand),
#     ("Cascade Revisit", loc_Cascade_Revisit, SMOOptions.goal.option_sand),
#     ("Sand", loc_Sand, SMOOptions.goal.option_sand),
#     ("Sand Pyramid", loc_Sand_Pyramid, SMOOptions.goal.option_sand),
#     ("Sand Peace", loc_Sand_Peace, SMOOptions.goal.option_sand),
#     ("Wooded", loc_Cap, SMOOptions.goal.option_sand),
#     ("Lake", loc_Cap, SMOOptions.goal.option_sand),
#     ("Cloud", loc_Cap, SMOOptions.goal.option_metro),
#     ("Lost", loc_Cap, SMOOptions.goal.option_metro),
#     ("Metro", loc_Cap, SMOOptions.goal.option_metro),
#     ("Seaside", loc_Cap, SMOOptions.goal.option_luncheon),
#     ("Snow", loc_Cap, SMOOptions.goal.option_luncheon),
#     ("Luncheon", loc_Cap, SMOOptions.goal.option_luncheon),
#     ("Ruined", loc_Cap, SMOOptions.goal.option_moon),
#     ("Bowser", loc_Cap, SMOOptions.goal.option_moon),
#     ("Moon", loc_Cap, SMOOptions.goal.option_moon),
#     ("Mushroom", loc_Cap, SMOOptions.goal.option_dark),
#     ("Dark Side", loc_Cap, SMOOptions.goal.option_dark),
#     ("Darker Side", loc_Cap, SMOOptions.goal.option_darker),
# ]

def create_region(self, world, player, region : tuple[str, dict, int]):
    """ Creates the regions for Super Mario Odyssey.
            Args:
                self: SMOWorld object for this player's world.
                world: The MultiWorld instance.
                player: The index of this player in the multiworld.
                region: Tuple containing region information.
    """
    pass
    # for world_id in range(len(world_list)):
    #     name, locations, goal = region
    #     reg = Region(name, player, world, name + " Region")
    #     if world_id <= self.options.goal:
    #         create_locs(reg, *locations.keys())


def create_regions(self, world, player):
    """ Creates the regions for Super Mario Odyssey.
            Args:
                self: SMOWorld object for this player's world.
                world: The MultiWorld instance.
                player: The index of this player in the multiworld.
    """

    # Cascade Regions
    regCascade = Region("Menu", player, world, "Cascade Kingdom")
    create_locs(regCascade, *loc_Cascade.keys())
    world.regions.append(regCascade)
    regCascadePeace = Region("Cascade Peace", player, world, "Cascade Kingdom")
    create_locs(regCascadePeace, *loc_Cascade_Peace.keys())
    world.regions.append(regCascadePeace)

    regCascadeRe = Region("Cascade Revisit", player, world, "Cascade Kingdom 2")
    create_locs(regCascadeRe, *loc_Cascade_Revisit.keys())
    world.regions.append(regCascadeRe)

    # Cap
    regCap = Region("Cap", player, world, "Cap Kingdom")
    create_locs(regCap, *loc_Cap.keys())
    world.regions.append(regCap)

    # Sand Regions
    regSand = Region("Sand", player, world, "Sand Kingdom")
    create_locs(regSand, *loc_Sand.keys())
    world.regions.append(regSand)
    regSandPyramid = Region("Sand Pyramid", player, world, "Sand Kingdom Pyramid")
    create_locs(regSandPyramid, *loc_Sand_Pyramid.keys())
    world.regions.append(regSandPyramid)
    regSandUnderground = Region("Sand Underground", player, world, "Sand Kingdom Underground")
    create_locs(regSandUnderground, *loc_Sand_Underground.keys())
    world.regions.append(regSandUnderground)
    regSandPeace = Region("Sand Peace", player, world, "Sand Kingdom Peace")
    if self.options.goal > self.options.goal.option_sand:
        create_locs(regSandPeace, *loc_Sand_Peace.keys())
    world.regions.append(regSandPeace)

    # Lake Regions
    regLake = Region("Lake", player, world, "Lake Kingdom")
    if self.options.goal > self.options.goal.option_sand:
        create_locs(regLake, *loc_Lake.keys())
    world.regions.append(regLake)

    # Wooded
    regWooded = Region("Wooded" , player, world, "Wooded Kingdom")

    if self.options.goal > self.options.goal.option_lake:
        create_locs(regWooded, *loc_Wooded.keys())
    world.regions.append(regWooded)
    regWoodedStory1 = Region("Wooded Post Road to Sky Garden", player, world, "Wooded Kingdom Story 1")
    if self.options.goal > self.options.goal.option_lake:
        create_locs(regWoodedStory1, * loc_Wooded_Post_Story1.keys())
    world.regions.append(regWoodedStory1)
    regWoodedPeace = Region("Wooded Peace", player, world, "Wooded Kingdom Peace")
    if self.options.goal > self.options.goal.option_lake:
        create_locs(regWoodedPeace, * loc_Wooded_Peace.keys())
    world.regions.append(regWoodedPeace)

    # Cloud
    regCloud = Region("Cloud", player, world, "Cloud Kingdom")
    if self.options.goal > self.options.goal.option_lake:
        create_locs(regCloud, *loc_Cloud.keys())
    world.regions.append(regCloud)

    # Lost
    regLost = Region("Lost", player, world, "Lost Kingdom")
    if self.options.goal > self.options.goal.option_lake:
        create_locs(regLost, *loc_Lost.keys())
    world.regions.append(regLost)

    # Metro
    regNightMetro = Region("Night Metro", player, world, "Metro Kingdom")
    regMetro = Region("Metro", player, world, "Metro Kingdom")
    if self.options.goal > self.options.goal.option_lake:
        create_locs(regNightMetro, *loc_Night_Metro.keys())
        create_locs(regMetro, *loc_Metro.keys())
    world.regions.append(regNightMetro)
    world.regions.append(regMetro)
    regMetroSewer = Region("Metro Sewer", player, world, "Metro Kingdom Story 1")
    if self.options.goal > self.options.goal.option_lake:
        create_locs(regMetroSewer, *loc_Metro_Sewer_Access.keys())
    world.regions.append(regMetroSewer)
    regMetroPeace = Region("Metro World Peace", player, world, "Metro Kingdom Peace")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regMetroPeace, *loc_Metro_Peace.keys())
    world.regions.append(regMetroPeace)


    # Snow
    regSnow = Region("Snow", player, world, "Snow Kingdom")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regSnow, *loc_Snow.keys())
    world.regions.append(regSnow)
    regSnowPeace = Region("Snow World Peace", player, world, "Snow Kingdom Peace")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regSnowPeace, *loc_Snow_Peace.keys())
    world.regions.append(regSnowPeace)

    # Seaside
    regSeaside = Region("Seaside", player, world, "Seaside Kingdom")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regSeaside, *loc_Seaside.keys())
    world.regions.append(regSeaside)
    regSeasidePeace = Region("Seaside World Peace", player, world, "Seaside Kingdom Peace")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regSeasidePeace, *loc_Seaside_Peace.keys())
    world.regions.append(regSeasidePeace)

    # Luncheon
    regLuncheon = Region("Luncheon", player, world, "Luncheon Kingdom")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regLuncheon, *loc_Luncheon.keys())
    world.regions.append(regLuncheon)
    regLuncheonSpewart = Region("Luncheon Post Spewart", player, world, "Luncheon Kingdom Story 1")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regLuncheonSpewart, *loc_Luncheon_Post_Spewart.keys())
    world.regions.append(regLuncheonSpewart)
    regLuncheonCheese = Region("Luncheon Post Cheese Rocks", player, world, "Luncheon Kingdom Story 2")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regLuncheonCheese, *loc_Luncheon_Post_Cheese_Rocks.keys())
    world.regions.append(regLuncheonCheese)
    regLuncheonPeace = Region("Luncheon World Peace", player, world, "Luncheon Kingdom Peace")
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regLuncheonPeace, *loc_Luncheon_Peace.keys())
    world.regions.append(regLuncheonPeace)

    # Ruined
    regRuined = Region("Ruined", player, world, "Ruined Kingdom")
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regRuined, *loc_Ruined.keys())
    world.regions.append(regRuined)

    # Bowser
    regBowser = Region("Bowser", player, world, "Bowser Kingdom")
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regBowser, *loc_Bowser.keys())
    world.regions.append(regBowser)
    regBowserInfiltrate = Region("Bowser Infiltrate", player, world, "Bowser Kingdom Story 1")
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regBowserInfiltrate, *loc_Bowser_Infiltrate.keys())
    world.regions.append(regBowserInfiltrate)
    regBowserBombing = Region("Bowser Post Bombing", player, world, "Bowser Kingdom Story 2")
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regBowserBombing, *loc_Bowser_Post_Bombing.keys())
    world.regions.append(regBowserBombing)
    regBowserMecha = Region("Bowser Mecha Broodal", player, world, "Bowser Kingdom Story 3")
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regBowserMecha, *loc_Bowser_Mecha_Broodal.keys())
    world.regions.append(regBowserMecha)
    regBowserPeace = Region("Bowser World Peace", player, world, "Bowser Kingdom Peace")
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regBowserPeace, *loc_Bowser_Peace.keys())
    world.regions.append(regBowserPeace)

    # Moon
    regMoon = Region("Moon", player, world, "Moon Kingdom")
    if self.options.goal > self.options.goal.option_moon or self.options.capture_sanity.value == self.options.capture_sanity.option_true:
        create_locs(regMoon, *loc_Moon.keys())
    world.regions.append(regMoon)
    regMoonOutfit = Region("Moon Gift Outfit", player, world, "Moon Gift Outfit")
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regMoonOutfit, *loc_Moon_Outfit.keys())
    world.regions.append(regMoonOutfit)

    # Post Game
    regPostGame = Region("Post Game", player, world, "Post Game Moons")
    if self.options.goal > self.options.goal.option_moon:
        create_locs(regPostGame, *post_game_locations_table.keys(), locs_table= post_game_locations_table)
    world.regions.append(regPostGame)

    # Dark Side
    regDark = Region("Dark", player, world, "Dark Side")
    if self.options.goal > self.options.goal.option_moon:
        create_locs(regDark, *loc_Dark.keys(),  locs_table=special_locations_table)
    world.regions.append(regDark)

    # Darker Side
    regDarker = Region("Darker", player, world, "Darker Side")
    if self.options.goal > self.options.goal.option_dark:
        create_locs(regDarker, *loc_Darker.keys(), locs_table=special_locations_table)
    world.regions.append(regDarker)

    # Revisits
    regCascadeMetro = Region("Cascade Post Metro", player, world, "Cascade Wanderer")
    regCascadeSnow = Region("Cascade Painting", player, world, "Cascade Painting")
    regSandRe = Region("Sand Revisit", player, world, "Sand Revisit")
    regLakeSeaside = Region("Lake Painting", player, world, "Lake Painting")
    regWoodedMetro = Region("Wooded Painting", player, world, "Wooded Painting")
    regLostRe = Region("Lost Revisit", player, world, "Lost Revisit")
    regPostCloud = Region("Post Cloud", player, world, "Post Cloud")
    regMetroSand = Region("Metro Painting", player, world, "Metro Painting")
    regLuncheonWooded = Region("Luncheon Painting", player, world, "Luncheon Painting")
    regPostMoon = Region("Post Moon", player, world, "Post Moon")
    regMushroomLuncheon = Region("Mushroom Painting", player, world, "Mushroom Painting")

    if self.options.goal > self.options.goal.option_metro:
        create_locs(regCascadeMetro, *loc_Cascade_Post_Metro.keys())
        create_locs(regCascadeSnow, *loc_Cascade_Post_Snow.keys())

    if self.options.goal > self.options.goal.option_lake:
        create_locs(regSandRe, *loc_Sand_Revisit.keys())
        create_locs(regMetroSand, *loc_Metro_Post_Sand.keys())


    if self.options.goal > self.options.goal.option_metro:
        create_locs(regLakeSeaside, *loc_Lake_Post_Seaside.keys())
        create_locs(regWoodedMetro, *loc_Wooded_Post_Metro.keys())
        create_locs(regLostRe, *loc_Lost_Revisit.keys())
        create_locs(regPostCloud, *loc_Post_Cloud.keys())
        create_locs(regLuncheonWooded, *loc_Luncheon_Post_Wooded.keys())

    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regPostMoon, *loc_Moon_Post_Moon.keys())
        create_locs(regMushroomLuncheon, *loc_Mushroom_Post_Luncheon.keys())

    world.regions.append(regCascadeMetro)
    world.regions.append(regCascadeSnow)
    world.regions.append(regSandRe)
    world.regions.append(regLakeSeaside)
    world.regions.append(regWoodedMetro)
    world.regions.append(regLostRe)
    world.regions.append(regPostCloud)
    world.regions.append(regMetroSand)
    world.regions.append(regLuncheonWooded)
    world.regions.append(regPostMoon)
    world.regions.append(regMushroomLuncheon)

    # Shops
    regCapShop = Region("Cap Shop", player, world, "Shop")
    regCascadeShop = Region("Cascade Shop", player, world, "Shop")
    regSandShop = Region("Sand Shop", player, world, "Shop")
    regLakeShop = Region("Lake Shop", player, world, "Shop")
    regWoodedShop = Region("Wooded Shop", player, world, "Shop")
    regLostShop = Region("Lost Shop", player, world, "Shop")
    regMetroShop = Region("Metro Shop", player, world, "Shop")
    regSnowShop = Region("Snow Shop", player, world, "Shop")
    regSeasideShop = Region("Seaside Shop", player, world, "Shop")
    regLuncheonShop = Region("Luncheon Shop", player, world, "Shop")
    regBowserShop = Region("Bowser Shop", player, world, "Shop")
    regMoonShop = Region("Moon Shop", player, world, "Shop")
    regMushroomShop = Region("Mushroom Shop", player, world, "Shop")
    regPostGameShop = Region("Postgame Shop", player, world, "Shop")
    regDarkOutfit = Region("Dark Outfit", player, world, "Shop")
    regDarkerOutfit = Region("Darker Outfit", player, world, "Shop")

    create_locs(regCapShop, *loc_Cap_Shop.keys())
    create_locs(regCascadeShop, *loc_Cascade_Shop.keys())
    create_locs(regSandShop, *loc_Sand_Shop.keys())

    if self.options.goal > self.options.goal.option_sand:
        create_locs(regLakeShop, *loc_Lake_Shop.keys())

    if self.options.goal > self.options.goal.option_lake:
        create_locs(regWoodedShop, *loc_Wooded_Shop.keys())
        create_locs(regLostShop, *loc_Lost_Shop.keys())
        create_locs(regMetroShop, *loc_Metro_Shop.keys())
    if self.options.goal > self.options.goal.option_metro:
        create_locs(regSnowShop, *loc_Snow_Shop.keys())
        create_locs(regSeasideShop, *loc_Seaside_Shop.keys())
        create_locs(regLuncheonShop, *loc_Luncheon_Shop.keys())
    if self.options.goal > self.options.goal.option_luncheon:
        create_locs(regBowserShop, *loc_Bowser_Shop.keys())

    if self.options.goal > self.options.goal.option_moon:
        create_locs(regMoonShop, *loc_Moon_Shop.keys())
        create_locs(regMushroomShop, *loc_Mushroom_Shop.keys())
        for outfit in self.outfit_moon_counts.keys():
            if self.options.goal == self.options.goal.option_dark:
                if self.outfit_moon_counts[outfit] < self.moon_counts["dark"]:
                    create_locs(regPostGameShop, outfit)
            elif self.options.goal == self.options.goal.option_darker:
                if self.outfit_moon_counts[outfit] < self.moon_counts["darker"]:
                    create_locs(regPostGameShop, outfit)


    if self.options.goal > self.options.goal.option_dark:
        create_locs(regDarkOutfit, *loc_Dark_Outfit.keys())
    if self.options.goal > self.options.goal.option_darker:
        create_locs(regDarkerOutfit, *loc_Darker_Outfit.keys())

    world.regions.append(regCapShop)
    world.regions.append(regCascadeShop)
    world.regions.append(regSandShop)
    world.regions.append(regLakeShop)
    world.regions.append(regWoodedShop)
    world.regions.append(regLostShop)
    world.regions.append(regMetroShop)
    world.regions.append(regSnowShop)
    world.regions.append(regSeasideShop)
    world.regions.append(regLuncheonShop)
    world.regions.append(regBowserShop)
    world.regions.append(regMoonShop)
    world.regions.append(regMushroomShop)
    world.regions.append(regPostGameShop)
    world.regions.append(regDarkOutfit)
    world.regions.append(regDarkerOutfit)

    # Captures
    regCapCaptures = Region("Cap Captures", player, world, "Captures")
    regCapRevisitCaptures = Region("Cap Revisit Captures", player, world, "Captures")
    regCascadeCaptures = Region("Cascade Captures", player, world, "Captures")
    regSandCaptures = Region("Sand Captures", player, world, "Captures")
    regSandUndergroundCaptures = Region("Sand Underground Captures", player, world, "Captures")
    regSandPeaceCaptures = Region("Sand Peace Captures", player, world, "Captures")
    regWoodedCaptures = Region("Wooded Captures", player, world, "Captures")
    regWoodedStory1Captures = Region("Wooded Story 1 Captures", player, world, "Captures")
    regWoodedPostGameCaptures = Region("Wooded Post Game Captures", player, world, "Captures")
    regLakeCaptures = Region("Lake Captures", player, world, "Captures")
    regCloudCaptures = Region("Cloud Captures", player, world, "Captures")
    regLostCaptures = Region("Lost Captures", player, world, "Captures")
    regMetroCaptures = Region("Metro Captures", player, world, "Captures")
    regMetroPostGameCaptures = Region("Metro Post Game Captures", player, world, "Captures")
    regSeasideCaptures = Region("Seaside Captures", player, world, "Captures")
    regSnowCaptures = Region("Snow Captures", player, world, "Captures")
    regSnowPeaceCaptures = Region("Snow Peace Captures", player, world, "Captures")
    regLuncheonCaptures = Region("Luncheon Captures", player, world, "Captures")
    regLuncheonPostCheeseRocksCaptures = Region("Luncheon Post Cheese Rocks Captures", player, world, "Captures")
    regBowserCaptures = Region("Bowser Captures", player, world, "Captures")
    regBowserPostBombingCaptures = Region("Bowser Post Bombing Captures", player, world, "Captures")
    regMoonCaptures = Region("Moon Captures", player, world, "Captures")
    regMoonCaveCaptures = Region("Moon Cave Captures", player, world, "Captures")
    regMushroomCaptures = Region("Mushroom Captures", player, world, "Captures")

    if self.options.capture_sanity.value == self.options.capture_sanity.option_true:
        create_locs(regCapCaptures, *loc_Cap_Captures)
        create_locs(regCapRevisitCaptures, *loc_Cap_Captures_Revisit)
        create_locs(regCascadeCaptures, *loc_Cascade_Captures)
        create_locs(regSandCaptures, *loc_Sand_Captures)
        create_locs(regSandUndergroundCaptures, *loc_Sand_Captures_Underground)

        if self.options.goal > self.options.goal.option_sand:
            create_locs(regSandPeaceCaptures, *loc_Sand_Captures_Peace)
            create_locs(regLakeCaptures, *loc_Lake_Captures)
            create_locs(regWoodedCaptures, *loc_Wooded_Captures)
            create_locs(regWoodedStory1Captures, *loc_Wooded_Captures_Post_Story1)
            create_locs(regCloudCaptures, *loc_Cloud_Captures)
            create_locs(regLostCaptures, *loc_Lost_Captures)
            create_locs(regMetroCaptures, *loc_Metro_Captures)

        if self.options.goal > self.options.goal.option_metro:
            create_locs(regSeasideCaptures, *loc_Seaside_Captures)
            create_locs(regSnowCaptures, *loc_Snow_Captures)
            create_locs(regSnowPeaceCaptures, *loc_Snow_Captures_Peace)
            create_locs(regLuncheonCaptures, *loc_Luncheon_Captures)
            create_locs(regLuncheonPostCheeseRocksCaptures, *loc_Luncheon_Captures_Post_Cheese_Rocks)

        if self.options.goal > self.options.goal.option_luncheon:
            create_locs(regBowserCaptures, *loc_Bowser_Captures)
            create_locs(regBowserPostBombingCaptures, *loc_Bowser_Captures_Post_Bombing)
            create_locs(regMoonCaptures, *loc_Moon_Captures)
            create_locs(regMoonCaveCaptures, *loc_Moon_Cave_Captures)

        if self.options.goal > self.options.goal.option_moon:
            create_locs(regMushroomCaptures, *loc_Mushroom_Captures)
            create_locs(regWoodedPostGameCaptures, *loc_Wooded_Captures_Postgame)
            create_locs(regMetroPostGameCaptures, *loc_Metro_Captures_Postgame)

        world.regions.append(regCapCaptures)
        world.regions.append(regCapRevisitCaptures)
        world.regions.append(regCascadeCaptures)
        world.regions.append(regSandCaptures)
        world.regions.append(regSandUndergroundCaptures)
        world.regions.append(regSandPeaceCaptures)
        world.regions.append(regWoodedCaptures)
        world.regions.append(regWoodedStory1Captures)
        world.regions.append(regLakeCaptures)
        world.regions.append(regCloudCaptures)
        world.regions.append(regLostCaptures)
        world.regions.append(regMetroCaptures)
        world.regions.append(regSeasideCaptures)
        world.regions.append(regSnowCaptures)
        world.regions.append(regSnowPeaceCaptures)
        world.regions.append(regLuncheonCaptures)
        world.regions.append(regLuncheonPostCheeseRocksCaptures)
        world.regions.append(regBowserCaptures)
        world.regions.append(regBowserPostBombingCaptures)
        world.regions.append(regMoonCaptures)
        world.regions.append(regMoonCaveCaptures)
        world.regions.append(regMushroomCaptures)
        world.regions.append(regWoodedPostGameCaptures)
        world.regions.append(regMetroPostGameCaptures)

    # Progression Connections
        regCascade.connect(regCascadePeace, "Menu", lambda state: state.has("Broode's Chain Chomp", player) and (state.has("Big Chain Chomp", self.player) or state.has("T-Rex", self.player)))
        regSandUnderground.connect(regSandPeace, "Sand World Peace",
            lambda state: state.has("Bullet Bill", self.player) and state.has("Knucklotec's Fist", self.player))
        regWoodedStory1.connect(regWoodedPeace, "Wooded World Peace",
                                lambda state: state.has("Uproot", self.player) and state.has("Sherm", self.player))
        regLost.connect(regNightMetro, "Night Metro Enter",
                         lambda state: count_moons(self, state, "Lost", player) >= self.moon_counts["lost"] and state.has("Spark Pylon", player))
        regNightMetro.connect(regMetro, "Metro Enter", lambda state: state.has("Sherm", player))

        regMetro.connect(regMetroSewer, "Metro Sewer", lambda state: state.has("Manhole", player))
        regSnow.connect(regSnowPeace, "Snow World Peace", lambda state: state.has("Shiverian Racer", player))
        regSeaside.connect(regSeasidePeace, "Seaside World Peace", lambda state: state.has("Gushen", player))
        regLuncheonCheese.connect(regMushroomLuncheon, "Luncheon Mushroom Painting", lambda state: state.has("Lava Bubble", player))
        regLuncheonSpewart.connect(regLuncheonCheese, "Luncheon Meat Plateau",
                                   lambda state: state.has("Hammer Bro", player))
        regLuncheonCheese.connect(regLuncheonPeace, "Luncheon World Peace",
                                  lambda state: state.has("Lava Bubble", player) and state.has("Meat", player))

        regBowser.connect(regBowserInfiltrate, "Bowser Infiltrate",lambda state: state.has("Spark Pylon", player)
                                        and state.has("Pokio", player))
        regBowserInfiltrate.connect(regBowserBombing, "Bowser Bombing")

        regBowserBombing.connect(regBowserMecha, "Bowser Mecha Fight")

        regMoon.connect(regPostMoon, "Post Moon", lambda state: state.has("Bowser", player))

    else:
        regCascade.connect(regCascadePeace)
        regSandUnderground.connect(regSandPeace, "Sand World Peace")
        regWoodedStory1.connect(regWoodedPeace, "Wooded World Peace")
        regLost.connect(regNightMetro, "Night Metro Enter",
                         lambda state: count_moons(self, state, "Lost", player) >= self.moon_counts["lost"])

        regNightMetro.connect(regMetro, "Metro Enter")
        regMetro.connect(regMetroSewer, "Metro Sewer")
        regSnow.connect(regSnowPeace, "Snow World Peace")
        regSeaside.connect(regSeasidePeace, "Seaside World Peace")
        regLuncheonCheese.connect(regMushroomLuncheon)
        regLuncheonSpewart.connect(regLuncheonCheese, "Luncheon Meat Plateau")
        regLuncheonCheese.connect(regLuncheonPeace, "Luncheon World Peace")
        regBowser.connect(regBowserInfiltrate, "Bowser Infiltrate")
        regBowserInfiltrate.connect(regBowserBombing, "Bowser Bombing")

        regBowserBombing.connect(regBowserMecha, "Bowser Mecha Fight")

        regMoon.connect(regPostMoon)


    regCascadePeace.connect(regSand, "Sand Enter", lambda state: count_moons(self, state, "Cascade", player) >= self.moon_counts["cascade"])
    regSand.connect(regSandPyramid, "Sand Pyramid Access")
    regSandPyramid.connect(regSandUnderground, "Sand Story Subarea")

    regSand.connect(regCap)
    regSand.connect(regCascadeRe)
    regSandPeace.connect(regMetroSand)
    regSand.connect(regLake, "Lake Enter", lambda state: count_moons(self, state, "Sand", player) >= self.moon_counts["sand"])

    regLake.connect(regWooded, "Wooded Enter")
    regLake.connect(regSandRe)

    regWooded.connect(regWoodedStory1, "Wooded Story 1")

    regWoodedPeace.connect(regLuncheonWooded)
    regWooded.connect(regPostCloud, "Cloud Bowser", lambda state: count_moons(self, state, "Lake", player) >= self.moon_counts["lake"] and count_moons(self, state, "Wooded", player) >= self.moon_counts["wooded"])
    regPostCloud.connect(regLost, "Enter Lost")
    regLost.connect(regCloud, "Cloud Available")

    regMetroSewer.connect(regMetroPeace, "Metro World Peace")
    regMetro.connect(regSnow, "Snow Enter", lambda state: count_moons(self, state, "Metro", player) >= self.moon_counts["metro"])
    regMetro.connect(regCascadeMetro)
    regMetro.connect(regWoodedMetro)
    regMetro.connect(regLostRe)


    regSnow.connect(regSeaside, "Seaside Enter")
    regSnow.connect(regCascadeSnow)


    regSeaside.connect(regLuncheon, "Enter Luncheon", lambda state: count_moons(self, state, "Snow", player) >= self.moon_counts["snow"] and count_moons(self, state, "Seaside", player) >= self.moon_counts["seaside"])
    regSeasidePeace.connect(regLakeSeaside)

    regLuncheon.connect(regRuined, "Enter Ruined", lambda state: count_moons(self, state, "Luncheon", player) >= self.moon_counts["luncheon"])
    regLuncheon.connect(regLuncheonSpewart, "Luncheon Town")
    regRuined.connect(regBowser,"Enter Bowser", lambda state: count_moons(self, state, "Ruined", player) >= self.moon_counts["ruined"])

    regBowserMecha.connect(regBowserPeace, "Bowser World Peace")
    regBowserPeace.connect(regMoon, "Enter Moon", lambda state: count_moons(self, state, "Bowser", player) >= self.moon_counts["bowser"])
    regBowserPeace.connect(regMoonOutfit, "Obtain Mario Tuxedo", lambda state: count_moons(self, state, "Bowser", player) >= self.moon_counts["bowser"])

    regPostMoon.connect(regPostGame)
    regPostGame.connect(regDark, "Dark Access", lambda state: total_moons(self, state, player) >= self.moon_counts["dark"])
    regPostGame.connect(regDarker, "Darker Access", lambda state: total_moons(self, state, player) >= self.moon_counts["darker"])

    if self.options.capture_sanity.value == self.options.capture_sanity.option_true:
        regMetro.connect(regMetroShop, "Metro Shop", lambda state: state.has("Spark Pylon", player)
                         and state.has("Sherm", player))

    else:
        regMetro.connect(regMetroShop)

    # Shop Connections
    regCap.connect(regCapShop)
    regCascadeRe.connect(regCascadeShop)
    regSand.connect(regSandShop)
    regLake.connect(regLakeShop)
    regWooded.connect(regWoodedShop)
    regLost.connect(regLostShop)
    regSnow.connect(regSnowShop)
    regSeaside.connect(regSeasideShop)
    regLuncheon.connect(regLuncheonShop)
    regBowserBombing.connect(regBowserShop)
    regPostGame.connect(regMoonShop)
    regPostGame.connect(regMushroomShop)
    regPostGame.connect(regPostGameShop)

    # if self.options.shops == "outfits" or self.options.shops == "all":
    #     regSand.connect(regPostGameShop)

    regDark.connect(regDarkOutfit)
    regDarker.connect(regDarkerOutfit)


    # Capture Connections
    #if self.options.capture_sanity.value == self.options.capture_sanity.option_true:
    regCascade.connect(regCapCaptures)
    regCascade.connect(regCascadeCaptures)
    regSand.connect(regCapRevisitCaptures)
    regSand.connect(regSandCaptures)
    regSandUnderground.connect(regSandUndergroundCaptures)
    regSandPeace.connect(regSandPeaceCaptures)
    regWooded.connect(regWoodedCaptures)
    regWoodedStory1.connect(regWoodedStory1Captures)
    regLake.connect(regLakeCaptures)
    regLost.connect(regCloudCaptures)
    regLost.connect(regLostCaptures)
    regMetro.connect(regMetroCaptures)
    regSeaside.connect(regSeasideCaptures)
    regSnow.connect(regSnowCaptures)
    regSnowPeace.connect(regSnowPeaceCaptures)
    regLuncheon.connect(regLuncheonCaptures)
    regLuncheonCheese.connect(regLuncheonPostCheeseRocksCaptures)
    regBowser.connect(regBowserCaptures)
    regBowserBombing.connect(regBowserPostBombingCaptures)
    regMoon.connect(regMoonCaptures)
    regMoon.connect(regMoonCaveCaptures)
    regPostGame.connect(regMushroomCaptures)
    regPostGame.connect(regWoodedPostGameCaptures)
    regPostGame.connect(regMetroPostGameCaptures)

def create_region (self, world, player):

    pass

def create_locs(reg: Region, *locs: str, locs_table = locations_table):
    reg.locations += ([SMOLocation(reg.player, loc_name, locs_table[loc_name], reg) for loc_name in locs])

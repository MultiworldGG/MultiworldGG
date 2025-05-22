from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, OptionSet, StartInventoryPool, Visibility

from .Names.DLC import ExpansionNames, GamePackNames, StuffNames, CASKitNames, BuildKitNames

class AspirationGoal(Choice):
    """The Aspiration Needed to win the game and the only one that will be included in the locations"""
    display_name = "goal"
    default = 1
    option_bodybuilder = 0
    option_painter_extraordinaire = 1
    option_bestselling_author = 2
    option_musical_genius = 3
    option_public_enemy = 4
    option_chief_of_mischief = 5
    option_master_chef = 6
    option_master_mixologist = 7
    option_renaissance_sim = 8
    option_nerd_brain = 9
    option_computer_whiz = 10
    option_serial_romantic = 11
    option_freelance_botanist = 12
    option_the_curator = 13
    option_angling_ace = 14
    option_joke_star = 15
    option_friend_of_the_world = 16
    option_neighborly_advisor = 17



class Career(Choice):
    """The career that will be the only one included in the locations"""
    display_name = "career"
    default = 1
    option_astronaut = 0
    option_athlete = 1
    option_business = 2
    option_criminal = 3
    option_culinary = 4
    option_entertainer = 5
    option_painter = 6
    option_secret_agent = 7
    option_style_influencer = 8
    option_tech_guru = 9
    option_writer = 10


class ExpansionPacks(OptionSet):
    """List of Expansion Packs that will be included in the shuffling. (Not Yet Implemented)"""
    display_name = "expansion_packs"
    visibility = Visibility.none
    valid_keys = {ExpansionNames.get_to_work, ExpansionNames.get_together, ExpansionNames.city_living,
                  ExpansionNames.cats_and_dogs, ExpansionNames.seasons, ExpansionNames.get_famous,
                  ExpansionNames.island_living, ExpansionNames.discover_university, ExpansionNames.eco_lifestyle,
                  ExpansionNames.snowy_escape, ExpansionNames.high_school_years, ExpansionNames.growing_together,
                  ExpansionNames.horse_ranch, ExpansionNames.for_rent, ExpansionNames.lovestruck,
                  ExpansionNames.life_and_death}

class GamePacks(OptionSet):
    """List of Game Packs that will be included in the shuffling. (Not Yet Implemented)"""
    display_name = "game_packs"
    visibility = Visibility.none
    valid_keys = {GamePackNames.outdoor_retreat, GamePackNames.spa_day, GamePackNames.dine_out,
                  GamePackNames.vampires, GamePackNames.parenthood, GamePackNames.jungle_adventure,
                  GamePackNames.stranger_ville, GamePackNames.realm_of_magic, GamePackNames.dream_home_decorator,
                  GamePackNames.my_wedding_stories, GamePackNames.werewolves}

class StuffPacks(OptionSet):
    """List of Stuff Packs that will be included in the shuffling. (Not Yet Implemented)"""
    display_name = "stuff_packs"
    visibility = Visibility.none
    valid_keys = {StuffNames.luxury_party, StuffNames.perfect_patio, StuffNames.cool_kitchen,
                  StuffNames.spooky, StuffNames.movie_hangout, StuffNames.romantic_garden,
                  StuffNames.kids_room, StuffNames.backyard, StuffNames.vintage_glamour,
                  StuffNames.bowling_night, StuffNames.fitness, StuffNames.toddler,
                  StuffNames.laundry_day, StuffNames.my_first_pet, StuffNames.moshino,
                  StuffNames.tiny_living, StuffNames.nifty_knitting, StuffNames.paranormal,
                  StuffNames.home_chef_hustle, StuffNames.crystal_creations}
class CASKits(OptionSet):
    """List of CAS (Create a Sim) Kits that will be included in the shuffling. (Not Yet Implemented)"""
    display_name = "cas_kits"
    visibility = Visibility.none
    valid_keys = {CASKitNames.throwback_fit, CASKitNames.fashion_street, CASKitNames.incheon_arrivals,
                  CASKitNames.modern_menswear, CASKitNames.carnaval_streetwear, CASKitNames.moonlight_chic,
                  CASKitNames.first_fits, CASKitNames.simtimates_collection, CASKitNames.grunge_revival,
                  CASKitNames.poolside_splash, CASKitNames.goth_galore, CASKitNames.urban_homage,
                  CASKitNames.sweet_slumber_party}

class BuildKits(OptionSet):
    """List of Build Kits that will be included in the shuffling. (Not Yet Implemented)"""
    display_name = "build_kits"
    visibility = Visibility.none
    valid_keys = {BuildKitNames.country_kitchen, BuildKitNames.courtyard_oasis, BuildKitNames.industrial_loft,
                  BuildKitNames.blooming_rooms, BuildKitNames.decor_to_the_max, BuildKitNames.little_campers,
                  BuildKitNames.desert_luxe, BuildKitNames.everyday_clutter, BuildKitNames.pastel_pop,
                  BuildKitNames.bathroom_clutter, BuildKitNames.basement_treasures, BuildKitNames.greenhouse_haven,
                  BuildKitNames.book_nook, BuildKitNames.modern_luxe, BuildKitNames.castle_estate,
                  BuildKitNames.party_essentials, BuildKitNames.cozy_bistro, BuildKitNames.riviera_retreat,
                  BuildKitNames.artist_studio, BuildKitNames.storybook_nursery, BuildKitNames.cozy_kitsch}

@dataclass
class Sims4Options(PerGameCommonOptions):
    goal: AspirationGoal
    career: Career
    expansion_packs: ExpansionPacks
    game_packs: GamePacks
    stuff_packs: StuffPacks
    cas_kits: CASKits
    build_kits: BuildKits
    start_inventory_from_pool: StartInventoryPool

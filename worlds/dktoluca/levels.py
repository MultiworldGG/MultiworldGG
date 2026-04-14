from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DKC3World

from .enums import Regions, Events, Locations
from .constants import *


level_region_data: dict[str, dict[str, list[str]]] = {
    Regions.lakeside_limbo_level:  {
        "Clear": [
            Locations.lakeside_limbo_clear,
        ],
        "Bonus": [
            Locations.lakeside_limbo_bonus_1, 
            Locations.lakeside_limbo_bonus_2,
        ],
        "DK Coin": [
            Locations.lakeside_limbo_dk_coin,
        ],
        "KONG": [
            Locations.lakeside_limbo_kong,
            ],
        "Balloons": [
            Locations.lakeside_limbo_balloon_1,
            Locations.lakeside_limbo_balloon_2,
            Locations.lakeside_limbo_balloon_3,
            Locations.lakeside_limbo_balloon_4,
            Locations.lakeside_limbo_balloon_5,
        ],
        "Bananas": [
            Locations.lakeside_limbo_bananas_1,
            Locations.lakeside_limbo_bananas_2,
            Locations.lakeside_limbo_bananas_3,
            Locations.lakeside_limbo_bananas_4,
        ],
        "Coins":  [
            Locations.lakeside_limbo_coin_1,
            Locations.lakeside_limbo_coin_2,
            Locations.lakeside_limbo_coin_3,
            Locations.lakeside_limbo_coin_4,
        ],
    },
    Regions.doorstop_dash_level:  {
        "Clear":  [
            Locations.doorstop_dash_clear,
        ],
        "Bonus":  [
            Locations.doorstop_dash_bonus_1,
            Locations.doorstop_dash_bonus_2,
        ],
        "DK Coin":  [
            Locations.doorstop_dash_dk_coin,
        ],
        "KONG":  [
            Locations.doorstop_dash_kong,
        ],
        "Balloons":  [
            Locations.doorstop_dash_balloon_1,
            Locations.doorstop_dash_balloon_2,
            Locations.doorstop_dash_balloon_3,
            Locations.doorstop_dash_balloon_4,
        ],
        "Bananas":  [
            Locations.doorstop_dash_bananas_1,
            Locations.doorstop_dash_bananas_2,
        ],
        "Coins":  [
            Locations.doorstop_dash_coin_1,
            Locations.doorstop_dash_coin_2,
        ],
    },
    Regions.tidal_trouble_level:  {
        "Clear":  [
            Locations.tidal_trouble_clear,
        ],
        "Bonus":  [
            Locations.tidal_trouble_bonus_1,
            Locations.tidal_trouble_bonus_2,
        ],
        "DK Coin":  [
            Locations.tidal_trouble_dk_coin,
        ],
        "KONG":  [
            Locations.tidal_trouble_kong,
        ],
        "Balloons":  [
            Locations.tidal_trouble_balloon_1,
        ],
        "Bananas":  [
            Locations.tidal_trouble_bananas_1,
            Locations.tidal_trouble_bananas_2,
        ],
        "Coins":  [
            Locations.tidal_trouble_coin_1,
            Locations.tidal_trouble_coin_2,
        ],
    },
    Regions.skiddas_row_level:  {
        "Clear":  [
            Locations.skiddas_row_clear,
        ],
        "Bonus":  [
            Locations.skiddas_row_bonus_1,
            Locations.skiddas_row_bonus_2,
        ],
        "DK Coin":  [
            Locations.skiddas_row_dk_coin,
        ],
        "KONG":  [
            Locations.skiddas_row_kong,
        ],
        "Balloons":  [
            Locations.skiddas_row_balloon_1,
        ],
        "Bananas":  [
            Locations.skiddas_row_bananas_1,
        ],
        "Coins":  [
            Locations.skiddas_row_coin_1,
            Locations.skiddas_row_coin_2,
            Locations.skiddas_row_coin_3,
        ],
    },
    Regions.murky_mill_level:  {
        "Clear":  [
            Locations.murky_mill_clear,
        ],
        "Bonus":  [
            Locations.murky_mill_bonus_1,
            Locations.murky_mill_bonus_2,
        ],
        "DK Coin":  [
            Locations.murky_mill_dk_coin,
        ],
        "KONG":  [
            Locations.murky_mill_kong,
        ],
        "Balloons":  [
            Locations.murky_mill_balloon_1,
        ],
        "Bananas":  [
            Locations.murky_mill_bananas_1,
            Locations.murky_mill_bananas_2,
        ],
        "Coins":  [
            Locations.murky_mill_coin_1,
            Locations.murky_mill_coin_2,
            Locations.murky_mill_coin_3,
        ],
    },
    Regions.barrel_shield_bust_up_level:  {
        "Clear":  [
            Locations.barrel_shield_bust_up_clear,
        ],
        "Bonus":  [
            Locations.barrel_shield_bust_up_bonus_1,
            Locations.barrel_shield_bust_up_bonus_2,
        ],
        "DK Coin":  [
            Locations.barrel_shield_bust_up_dk_coin,
        ],
        "KONG":  [
            Locations.barrel_shield_bust_up_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.barrel_shield_bust_up_bananas_1,
            Locations.barrel_shield_bust_up_bananas_2,
        ],
        "Coins":  [
            Locations.barrel_shield_bust_up_coin_1,
            Locations.barrel_shield_bust_up_coin_2,
        ],
    },
    Regions.riverside_race_level:  {
        "Clear":  [
            Locations.riverside_race_clear,
        ],
        "Bonus":  [
            Locations.riverside_race_bonus_1,
            Locations.riverside_race_bonus_2,
        ],
        "DK Coin":  [
            Locations.riverside_race_dk_coin,
        ],
        "KONG":  [
            Locations.riverside_race_kong,
        ],
        "Balloons":  [
            Locations.riverside_race_balloon_1,
        ],
        "Bananas":  [
            Locations.riverside_race_bananas_1,
            Locations.riverside_race_bananas_2,
            Locations.riverside_race_bananas_3,
            Locations.riverside_race_bananas_4,
            Locations.riverside_race_bananas_5,
            Locations.riverside_race_bananas_6,
        ],
        "Coins":  [
            Locations.riverside_race_coin_1,
            Locations.riverside_race_coin_2,
            Locations.riverside_race_coin_3,
            Locations.riverside_race_coin_4,
        ],
    },
    Regions.squeals_on_wheels_level:  {
        "Clear":  [
            Locations.squeals_on_wheels_clear,
        ],
        "Bonus":  [
            Locations.squeals_on_wheels_bonus_1,
            Locations.squeals_on_wheels_bonus_2,
        ],
        "DK Coin":  [
            Locations.squeals_on_wheels_dk_coin,
        ],
        "KONG":  [
            Locations.squeals_on_wheels_kong,
        ],
        "Balloons":  [
            Locations.squeals_on_wheels_balloon_1,
        ],
        "Bananas":  [
            Locations.squeals_on_wheels_bananas_1,
            Locations.squeals_on_wheels_bananas_2,
            Locations.squeals_on_wheels_bananas_3,
            Locations.squeals_on_wheels_bananas_4,
            Locations.squeals_on_wheels_bananas_5,
            Locations.squeals_on_wheels_bananas_6,
            Locations.squeals_on_wheels_bananas_7,
        ],
        "Coins":  [
            Locations.squeals_on_wheels_coin_1,
        ],
    },
    Regions.springing_spiders_level:  {
        "Clear":  [
            Locations.springing_spiders_clear,
        ],
        "Bonus":  [
            Locations.springing_spiders_bonus_1,
            Locations.springing_spiders_bonus_2,
        ],
        "DK Coin":  [
            Locations.springing_spiders_dk_coin,
        ],
        "KONG":  [
            Locations.springing_spiders_kong,
        ],
        "Balloons":  [
            Locations.springing_spiders_balloon_1,
            Locations.springing_spiders_balloon_2,
            Locations.springing_spiders_balloon_3,
        ],
        "Bananas":  [
            Locations.springing_spiders_bananas_1,
            Locations.springing_spiders_bananas_2,
            Locations.springing_spiders_bananas_3,
            Locations.springing_spiders_bananas_4,
            Locations.springing_spiders_bananas_5,
            Locations.springing_spiders_bananas_6,
        ],
        "Coins":  [
            Locations.springing_spiders_coin_1,
            Locations.springing_spiders_coin_2,
            Locations.springing_spiders_coin_3,
            Locations.springing_spiders_coin_4,
            Locations.springing_spiders_coin_5,
            Locations.springing_spiders_coin_6,
            Locations.springing_spiders_coin_7,
        ],
    },
    Regions.bobbing_barrel_brawl_level:  {
        "Clear":  [
            Locations.bobbing_barrel_brawl_clear,
        ],
        "Bonus":  [
            Locations.bobbing_barrel_brawl_bonus_1,
            Locations.bobbing_barrel_brawl_bonus_2,
        ],
        "DK Coin":  [
            Locations.bobbing_barrel_brawl_dk_coin,
        ],
        "KONG":  [
            Locations.bobbing_barrel_brawl_kong,
        ],
        "Balloons":  [
            Locations.bobbing_barrel_brawl_balloon_1,
        ],
        "Bananas":  [
            Locations.bobbing_barrel_brawl_bananas_1,
        ],
        "Coins":  [
            Locations.bobbing_barrel_brawl_coin_1,
            Locations.bobbing_barrel_brawl_coin_2,
            Locations.bobbing_barrel_brawl_coin_3,
        ],
    },
    Regions.bazzas_blockade_level:  {
        "Clear":  [
            Locations.bazzas_blockade_clear,
        ],
        "Bonus":  [
            Locations.bazzas_blockade_bonus_1,
            Locations.bazzas_blockade_bonus_2,
        ],
        "DK Coin":  [
            Locations.bazzas_blockade_dk_coin,
        ],
        "KONG":  [
            Locations.bazzas_blockade_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.bazzas_blockade_bananas_1,
            Locations.bazzas_blockade_bananas_2,
        ],
        "Coins":  [
            Locations.bazzas_blockade_coin_1,
            Locations.bazzas_blockade_coin_2,
            Locations.bazzas_blockade_coin_3,
            Locations.bazzas_blockade_coin_4,
        ],
    },
    Regions.rocket_barrel_ride_level:  {
        "Clear":  [
            Locations.rocket_barrel_ride_clear,
        ],
        "Bonus":  [
            Locations.rocket_barrel_ride_bonus_1,
            Locations.rocket_barrel_ride_bonus_2,
        ],
        "DK Coin":  [
            Locations.rocket_barrel_ride_dk_coin,
        ],
        "KONG":  [
            Locations.rocket_barrel_ride_kong,
        ],
        "Balloons":  [
            Locations.rocket_barrel_ride_balloon_1,
            Locations.rocket_barrel_ride_balloon_2,
        ],
        "Bananas":  [
            Locations.rocket_barrel_ride_bananas_1,
            Locations.rocket_barrel_ride_bananas_2,
            Locations.rocket_barrel_ride_bananas_3,
            Locations.rocket_barrel_ride_bananas_4,
            Locations.rocket_barrel_ride_bananas_5,
            Locations.rocket_barrel_ride_bananas_6,
            Locations.rocket_barrel_ride_bananas_7,
        ],
        "Coins":  [
            Locations.rocket_barrel_ride_coin_1,
            Locations.rocket_barrel_ride_coin_2,
            Locations.rocket_barrel_ride_coin_3,
            Locations.rocket_barrel_ride_coin_4,
            Locations.rocket_barrel_ride_coin_5,
            Locations.rocket_barrel_ride_coin_6,
        ],
    },
    Regions.kreeping_klasps_level:  {
        "Clear":  [
            Locations.kreeping_klasps_clear,
        ],
        "Bonus":  [
            Locations.kreeping_klasps_bonus_1,
            Locations.kreeping_klasps_bonus_2,
        ],
        "DK Coin":  [
            Locations.kreeping_klasps_dk_coin,
        ],
        "KONG":  [
            Locations.kreeping_klasps_kong,
        ],
        "Balloons":  [
            Locations.kreeping_klasps_balloon_1,
            Locations.kreeping_klasps_balloon_2,
        ],
        "Bananas":  [
            Locations.kreeping_klasps_bananas_1,
            Locations.kreeping_klasps_bananas_2,
        ],
        "Coins":  [
            Locations.kreeping_klasps_coin_1,
            Locations.kreeping_klasps_coin_2,
        ],
    },
    Regions.tracker_barrel_trek_level:  {
        "Clear":  [
            Locations.tracker_barrel_trek_clear,
        ],
        "Bonus":  [
            Locations.tracker_barrel_trek_bonus_1,
            Locations.tracker_barrel_trek_bonus_2,
        ],
        "DK Coin":  [
            Locations.tracker_barrel_trek_dk_coin,
        ],
        "KONG":  [
            Locations.tracker_barrel_trek_kong,
        ],
        "Balloons":  [
            Locations.tracker_barrel_trek_balloon_1,
        ],
        "Bananas":  [
            Locations.tracker_barrel_trek_bananas_1,
        ],
        "Coins":  [
            Locations.tracker_barrel_trek_coin_1,
            Locations.tracker_barrel_trek_coin_2,
            Locations.tracker_barrel_trek_coin_3,
            Locations.tracker_barrel_trek_coin_4,
        ],
    },
    Regions.fish_food_frenzy_level:  {
        "Clear":  [
            Locations.fish_food_frenzy_clear,
        ],
        "Bonus":  [
            Locations.fish_food_frenzy_bonus_1,
            Locations.fish_food_frenzy_bonus_2,
        ],
        "DK Coin":  [
            Locations.fish_food_frenzy_dk_coin,
        ],
        "KONG":  [
            Locations.fish_food_frenzy_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.fish_food_frenzy_bananas_1,
        ],
        "Coins":  [
            Locations.fish_food_frenzy_coin_1,
            Locations.fish_food_frenzy_coin_2,
        ],
    },
    Regions.fireball_frenzy_level:  {
        "Clear":  [
            Locations.fireball_frenzy_clear,
        ],
        "Bonus":  [
            Locations.fireball_frenzy_bonus_1,
            Locations.fireball_frenzy_bonus_2,
        ],
        "DK Coin":  [
            Locations.fireball_frenzy_dk_coin,
        ],
        "KONG":  [
            Locations.fireball_frenzy_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.fireball_frenzy_bananas_1,
            Locations.fireball_frenzy_bananas_2,
            Locations.fireball_frenzy_bananas_3,
        ],
        "Coins":  [
            Locations.fireball_frenzy_coin_1,
            Locations.fireball_frenzy_coin_2,
            Locations.fireball_frenzy_coin_3,
            Locations.fireball_frenzy_coin_4,
            Locations.fireball_frenzy_coin_5,
        ],
    },
    Regions.demolition_drain_pipe_level:  {
        "Clear":  [
            Locations.demolition_drain_pipe_clear,
        ],
        "Bonus":  [
            Locations.demolition_drain_pipe_bonus_1,
            Locations.demolition_drain_pipe_bonus_2,
        ],
        "DK Coin":  [
            Locations.demolition_drain_pipe_dk_coin,
        ],
        "KONG":  [
            Locations.demolition_drain_pipe_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.demolition_drain_pipe_bananas_1,
            Locations.demolition_drain_pipe_bananas_2,
            Locations.demolition_drain_pipe_bananas_3,
            Locations.demolition_drain_pipe_bananas_4,
            Locations.demolition_drain_pipe_bananas_5,
            Locations.demolition_drain_pipe_bananas_6,
            Locations.demolition_drain_pipe_bananas_7,
        ],
        "Coins":  [
            Locations.demolition_drain_pipe_coin_1,
            Locations.demolition_drain_pipe_coin_2,
            Locations.demolition_drain_pipe_coin_3,
            Locations.demolition_drain_pipe_coin_4,
            Locations.demolition_drain_pipe_coin_5,
            Locations.demolition_drain_pipe_coin_6,
            Locations.demolition_drain_pipe_coin_7,
        ],
    },
    Regions.ripsaw_rage_level:  {
        "Clear":  [
            Locations.ripsaw_rage_clear,
        ],
        "Bonus":  [
            Locations.ripsaw_rage_bonus_1,
            Locations.ripsaw_rage_bonus_2,
        ],
        "DK Coin":  [
            Locations.ripsaw_rage_dk_coin,
        ],
        "KONG":  [
            Locations.ripsaw_rage_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.ripsaw_rage_bananas_1,
            Locations.ripsaw_rage_bananas_2,
            Locations.ripsaw_rage_bananas_3,
            Locations.ripsaw_rage_bananas_4,
        ],
        "Coins":  [
            Locations.ripsaw_rage_coin_1,
            Locations.ripsaw_rage_coin_2,
            Locations.ripsaw_rage_coin_3,
        ],
    },
    Regions.blazing_bazukas_level:  {
        "Clear":  [
            Locations.blazing_bazukas_clear,
        ],
        "Bonus":  [
            Locations.blazing_bazukas_bonus_1,
            Locations.blazing_bazukas_bonus_2,
        ],
        "DK Coin":  [
            Locations.blazing_bazukas_dk_coin,
        ],
        "KONG":  [
            Locations.blazing_bazukas_kong,
        ],
        "Balloons":  [
            Locations.blazing_bazukas_balloon_1,
        ],
        "Bananas":  [
            Locations.blazing_bazukas_bananas_1,
            Locations.blazing_bazukas_bananas_2,
            Locations.blazing_bazukas_bananas_3,
        ],
        "Coins":  [
            Locations.blazing_bazukas_coin_1,
            Locations.blazing_bazukas_coin_2,
            Locations.blazing_bazukas_coin_3,
            Locations.blazing_bazukas_coin_4,
        ],
    },
    Regions.low_g_labyrinth_level:  {
        "Clear":  [
            Locations.low_g_labyrinth_clear,
        ],
        "Bonus":  [
            Locations.low_g_labyrinth_bonus_1,
            Locations.low_g_labyrinth_bonus_2,
        ],
        "DK Coin":  [
            Locations.low_g_labyrinth_dk_coin,
        ],
        "KONG":  [
            Locations.low_g_labyrinth_kong,
        ],
        "Balloons":  [
            Locations.low_g_labyrinth_balloon_1,
        ],
        "Bananas":  [
            Locations.low_g_labyrinth_bananas_1,
            Locations.low_g_labyrinth_bananas_2,
            Locations.low_g_labyrinth_bananas_3,
            Locations.low_g_labyrinth_bananas_4,
        ],
        "Coins":  [
            Locations.low_g_labyrinth_coin_1,
            Locations.low_g_labyrinth_coin_2,
            Locations.low_g_labyrinth_coin_3,
            Locations.low_g_labyrinth_coin_4,
            Locations.low_g_labyrinth_coin_5,
            Locations.low_g_labyrinth_coin_6,
            Locations.low_g_labyrinth_coin_7,
        ],
    },
    Regions.krevice_kreepers_level:  {
        "Clear":  [
            Locations.krevice_kreepers_clear,
        ],
        "Bonus":  [
            Locations.krevice_kreepers_bonus_1,
            Locations.krevice_kreepers_bonus_2,
        ],
        "DK Coin":  [
            Locations.krevice_kreepers_dk_coin,
        ],
        "KONG":  [
            Locations.krevice_kreepers_kong,
        ],
        "Balloons":  [
            Locations.krevice_kreepers_balloon_1,
        ],
        "Bananas":  [
            Locations.krevice_kreepers_bananas_1,
            Locations.krevice_kreepers_bananas_2,
            Locations.krevice_kreepers_bananas_3,
            Locations.krevice_kreepers_bananas_4,
        ],
        "Coins":  [
            Locations.krevice_kreepers_coin_1,
            Locations.krevice_kreepers_coin_2,
            Locations.krevice_kreepers_coin_3,
            Locations.krevice_kreepers_coin_4,
            Locations.krevice_kreepers_coin_5,
            Locations.krevice_kreepers_coin_6,
        ],
    },
    Regions.tearaway_toboggan_level:  {
        "Clear":  [
            Locations.tearaway_toboggan_clear,
        ],
        "Bonus":  [
            Locations.tearaway_toboggan_bonus_1,
            Locations.tearaway_toboggan_bonus_2,
        ],
        "DK Coin":  [
            Locations.tearaway_toboggan_dk_coin,
        ],
        "KONG":  [
            Locations.tearaway_toboggan_kong,
        ],
        "Balloons":  [
            Locations.tearaway_toboggan_balloon_1,
            Locations.tearaway_toboggan_balloon_2,
        ],
        "Bananas":  [
            Locations.tearaway_toboggan_bananas_1,
            Locations.tearaway_toboggan_bananas_2,
            Locations.tearaway_toboggan_bananas_3,
            Locations.tearaway_toboggan_bananas_4,
            Locations.tearaway_toboggan_bananas_5,
            Locations.tearaway_toboggan_bananas_6,
            Locations.tearaway_toboggan_bananas_7,
        ],
        "Coins":  [
            Locations.tearaway_toboggan_coin_1,
            Locations.tearaway_toboggan_coin_2,
            Locations.tearaway_toboggan_coin_3,
            Locations.tearaway_toboggan_coin_4,
            Locations.tearaway_toboggan_coin_5,
            Locations.tearaway_toboggan_coin_6,
        ],
    },
    Regions.barrel_drop_bounce_level:  {
        "Clear":  [
            Locations.barrel_drop_bounce_clear,
        ],
        "Bonus":  [
            Locations.barrel_drop_bounce_bonus_1,
            Locations.barrel_drop_bounce_bonus_2,
        ],
        "DK Coin":  [
            Locations.barrel_drop_bounce_dk_coin,
        ],
        "KONG":  [
            Locations.barrel_drop_bounce_kong,
        ],
        "Balloons":  [
            Locations.barrel_drop_bounce_balloon_1,
        ],
        "Bananas":  [
        ],
        "Coins":  [
            Locations.barrel_drop_bounce_coin_1,
            Locations.barrel_drop_bounce_coin_2,
        ],
    },
    Regions.krackshot_krock_level:  {
        "Clear":  [
            Locations.krackshot_krock_clear,
        ],
        "Bonus":  [
            Locations.krackshot_krock_bonus_1,
            Locations.krackshot_krock_bonus_2,
        ],
        "DK Coin":  [
            Locations.krackshot_krock_dk_coin,
        ],
        "KONG":  [
            Locations.krackshot_krock_kong,
        ],
        "Balloons":  [
            Locations.krackshot_krock_balloon_1,
        ],
        "Bananas":  [
            Locations.krackshot_krock_bananas_1,
            Locations.krackshot_krock_bananas_2,
            Locations.krackshot_krock_bananas_3,
            Locations.krackshot_krock_bananas_4,
            Locations.krackshot_krock_bananas_5,
        ],
        "Coins":  [
            Locations.krackshot_krock_coin_1,
            Locations.krackshot_krock_coin_2,
            Locations.krackshot_krock_coin_3,
            Locations.krackshot_krock_coin_4,
            Locations.krackshot_krock_coin_5,
        ],
    },
    Regions.lemguin_lunge_level:  {
        "Clear":  [
            Locations.lemguin_lunge_clear,
        ],
        "Bonus":  [
            Locations.lemguin_lunge_bonus_1,
            Locations.lemguin_lunge_bonus_2,
        ],
        "DK Coin":  [
            Locations.lemguin_lunge_dk_coin,
        ],
        "KONG":  [
            Locations.lemguin_lunge_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.lemguin_lunge_bananas_1,
        ],
        "Coins":  [
            Locations.lemguin_lunge_coin_1,
            Locations.lemguin_lunge_coin_2,
        ],
    },
    Regions.buzzer_barrage_level:  {
        "Clear":  [
            Locations.buzzer_barrage_clear,
        ],
        "Bonus":  [
            Locations.buzzer_barrage_bonus_1,
            Locations.buzzer_barrage_bonus_2,
        ],
        "DK Coin":  [
            Locations.buzzer_barrage_dk_coin,
        ],
        "KONG":  [
            Locations.buzzer_barrage_kong,
        ],
        "Balloons":  [
            Locations.buzzer_barrage_balloon_1,
            Locations.buzzer_barrage_balloon_2,
            Locations.buzzer_barrage_balloon_3,
        ],
        "Bananas":  [
            Locations.buzzer_barrage_bananas_1,
            Locations.buzzer_barrage_bananas_2,
            Locations.buzzer_barrage_bananas_3,
            Locations.buzzer_barrage_bananas_4,
            Locations.buzzer_barrage_bananas_5,
            Locations.buzzer_barrage_bananas_6,
            Locations.buzzer_barrage_bananas_7,
        ],
        "Coins":  [
            Locations.buzzer_barrage_coin_1,
            Locations.buzzer_barrage_coin_2,
            Locations.buzzer_barrage_coin_3,
            Locations.buzzer_barrage_coin_4,
            Locations.buzzer_barrage_coin_5,
            Locations.buzzer_barrage_coin_6,
            Locations.buzzer_barrage_coin_7,
        ],
    },
    Regions.kongfused_cliffs_level:  {
        "Clear":  [
            Locations.kongfused_cliffs_clear,
        ],
        "Bonus":  [
            Locations.kongfused_cliffs_bonus_1,
            Locations.kongfused_cliffs_bonus_2,
        ],
        "DK Coin":  [
            Locations.kongfused_cliffs_dk_coin,
        ],
        "KONG":  [
            Locations.kongfused_cliffs_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.kongfused_cliffs_bananas_1,
            Locations.kongfused_cliffs_bananas_2,
        ],
        "Coins":  [
            Locations.kongfused_cliffs_coin_1,
            Locations.kongfused_cliffs_coin_2,
            Locations.kongfused_cliffs_coin_3,
            Locations.kongfused_cliffs_coin_4,
            Locations.kongfused_cliffs_coin_5,
        ],
    },
    Regions.floodlit_fish_level:  {
        "Clear":  [
            Locations.floodlit_fish_clear,
        ],
        "Bonus":  [
            Locations.floodlit_fish_bonus_1,
            Locations.floodlit_fish_bonus_2,
        ],
        "DK Coin":  [
            Locations.floodlit_fish_dk_coin,
        ],
        "KONG":  [
            Locations.floodlit_fish_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.floodlit_fish_bananas_1,
            Locations.floodlit_fish_bananas_2,
            Locations.floodlit_fish_bananas_3,
            Locations.floodlit_fish_bananas_4,
            Locations.floodlit_fish_bananas_5,
            Locations.floodlit_fish_bananas_6,
            Locations.floodlit_fish_bananas_7,
            Locations.floodlit_fish_bananas_8,
        ],
        "Coins":  [
            Locations.floodlit_fish_coin_1,
            Locations.floodlit_fish_coin_2,
            Locations.floodlit_fish_coin_3,
        ],
    },
    Regions.pot_hole_panic_level:  {
        "Clear":  [
            Locations.pot_hole_panic_clear,
        ],
        "Bonus":  [
            Locations.pot_hole_panic_bonus_1,
            Locations.pot_hole_panic_bonus_2,
        ],
        "DK Coin":  [
            Locations.pot_hole_panic_dk_coin,
        ],
        "KONG":  [
            Locations.pot_hole_panic_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.pot_hole_panic_bananas_1,
            Locations.pot_hole_panic_bananas_2,
            Locations.pot_hole_panic_bananas_3,
            Locations.pot_hole_panic_bananas_4,
            Locations.pot_hole_panic_bananas_5,
            Locations.pot_hole_panic_bananas_6,
            Locations.pot_hole_panic_bananas_7,
            Locations.pot_hole_panic_bananas_8,
            Locations.pot_hole_panic_bananas_9,
            Locations.pot_hole_panic_bananas_10,
            Locations.pot_hole_panic_bananas_11,
        ],
        "Coins":  [
            Locations.pot_hole_panic_coin_1,
            Locations.pot_hole_panic_coin_2,
            Locations.pot_hole_panic_coin_3,
            Locations.pot_hole_panic_coin_4,
        ],
    },
    Regions.ropey_rumpus_level:  {
        "Clear":  [
            Locations.ropey_rumpus_clear,
        ],
        "Bonus":  [
            Locations.ropey_rumpus_bonus_1,
            Locations.ropey_rumpus_bonus_2,
        ],
        "DK Coin":  [
            Locations.ropey_rumpus_dk_coin,
        ],
        "KONG":  [
            Locations.ropey_rumpus_kong,
        ],
        "Balloons":  [
            Locations.ropey_rumpus_balloon_1,
            Locations.ropey_rumpus_balloon_2,
        ],
        "Bananas":  [
            Locations.ropey_rumpus_bananas_1,
            Locations.ropey_rumpus_bananas_2,
            Locations.ropey_rumpus_bananas_3,
            Locations.ropey_rumpus_bananas_4,
            Locations.ropey_rumpus_bananas_5,
            Locations.ropey_rumpus_bananas_6,
            Locations.ropey_rumpus_bananas_7,
            Locations.ropey_rumpus_bananas_8,
            Locations.ropey_rumpus_bananas_9,
            Locations.ropey_rumpus_bananas_10,
        ],
        "Coins":  [
            Locations.ropey_rumpus_coin_1,
            Locations.ropey_rumpus_coin_2,
            Locations.ropey_rumpus_coin_3,
            Locations.ropey_rumpus_coin_4,
            Locations.ropey_rumpus_coin_5,
            Locations.ropey_rumpus_coin_6,
            Locations.ropey_rumpus_coin_7,
            Locations.ropey_rumpus_coin_8,
        ],
    },
    Regions.konveyor_rope_klash_level:  {
        "Clear":  [
            Locations.konveyor_rope_klash_clear,
        ],
        "Bonus":  [
            Locations.konveyor_rope_klash_bonus_1,
            Locations.konveyor_rope_klash_bonus_2,
        ],
        "DK Coin":  [
            Locations.konveyor_rope_klash_dk_coin,
        ],
        "KONG":  [
            Locations.konveyor_rope_klash_kong,
        ],
        "Balloons":  [
            Locations.konveyor_rope_klash_balloon_1,
            Locations.konveyor_rope_klash_balloon_2,
        ],
        "Bananas":  [
        ],
        "Coins":  [
            Locations.konveyor_rope_klash_coin_1,
            Locations.konveyor_rope_klash_coin_2,
            Locations.konveyor_rope_klash_coin_3,
        ],
    },
    Regions.creepy_caverns_level:  {
        "Clear":  [
            Locations.creepy_caverns_clear,
        ],
        "Bonus":  [
            Locations.creepy_caverns_bonus_1,
            Locations.creepy_caverns_bonus_2,
        ],
        "DK Coin":  [
            Locations.creepy_caverns_dk_coin,
        ],
        "KONG":  [
            Locations.creepy_caverns_kong,
        ],
        "Balloons":  [
            Locations.creepy_caverns_balloon_1,
        ],
        "Bananas":  [
            Locations.creepy_caverns_bananas_1,
            Locations.creepy_caverns_bananas_2,
        ],
        "Coins":  [
            Locations.creepy_caverns_coin_1,
            Locations.creepy_caverns_coin_2,
            Locations.creepy_caverns_coin_3,
            Locations.creepy_caverns_coin_4,
            Locations.creepy_caverns_coin_5,
            Locations.creepy_caverns_coin_6,
        ],
    },
    Regions.lightning_look_out_level:  {
        "Clear":  [
            Locations.lightning_look_out_clear,
        ],
        "Bonus":  [
            Locations.lightning_look_out_bonus_1,
            Locations.lightning_look_out_bonus_2,
        ],
        "DK Coin":  [
            Locations.lightning_look_out_dk_coin,
        ],
        "KONG":  [
            Locations.lightning_look_out_kong,
        ],
        "Balloons":  [
            Locations.lightning_look_out_balloon_1,
            Locations.lightning_look_out_balloon_2,
        ],
        "Bananas":  [
            Locations.lightning_look_out_bananas_1,
        ],
        "Coins":  [
            Locations.lightning_look_out_coin_1,
            Locations.lightning_look_out_coin_2,
            Locations.lightning_look_out_coin_3,
        ],
    },
    Regions.koindozer_klamber_level:  {
        "Clear":  [
            Locations.koindozer_klamber_clear,
        ],
        "Bonus":  [
            Locations.koindozer_klamber_bonus_1,
            Locations.koindozer_klamber_bonus_2,
        ],
        "DK Coin":  [
            Locations.koindozer_klamber_dk_coin,
        ],
        "KONG":  [
            Locations.koindozer_klamber_kong,
        ],
        "Balloons":  [
            Locations.koindozer_klamber_balloon_1,
        ],
        "Bananas":  [
            Locations.koindozer_klamber_bananas_1,
        ],
        "Coins":  [
            Locations.koindozer_klamber_coin_1,
            Locations.koindozer_klamber_coin_2,
            Locations.koindozer_klamber_coin_3,
        ],
    },
    Regions.poisonous_pipeline_level:  {
        "Clear":  [
            Locations.poisonous_pipeline_clear,
        ],
        "Bonus":  [
            Locations.poisonous_pipeline_bonus_1,
            Locations.poisonous_pipeline_bonus_2,
        ],
        "DK Coin":  [
            Locations.poisonous_pipeline_dk_coin,
        ],
        "KONG":  [
            Locations.poisonous_pipeline_kong,
        ],
        "Balloons":  [
            Locations.poisonous_pipeline_balloon_1,
        ],
        "Bananas":  [
            Locations.poisonous_pipeline_bananas_1,
            Locations.poisonous_pipeline_bananas_2,
        ],
        "Coins":  [
            Locations.poisonous_pipeline_coin_1,
            Locations.poisonous_pipeline_coin_2,
        ],
    },
    Regions.stampede_sprint_level:  {
        "Clear":  [
            Locations.stampede_sprint_clear,
        ],
        "Bonus":  [
            Locations.stampede_sprint_bonus_1,
            Locations.stampede_sprint_bonus_2,
            Locations.stampede_sprint_bonus_3,
        ],
        "DK Coin":  [
            Locations.stampede_sprint_dk_coin,
        ],
        "KONG":  [
            Locations.stampede_sprint_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
        ],
        "Coins":  [
            Locations.stampede_sprint_coin_1,
            Locations.stampede_sprint_coin_2,
        ],
    },
    Regions.criss_kross_cliffs_level:  {
        "Clear":  [
            Locations.criss_kross_cliffs_clear,
        ],
        "Bonus":  [
            Locations.criss_kross_cliffs_bonus_1,
            Locations.criss_kross_cliffs_bonus_2,
        ],
        "DK Coin":  [
            Locations.criss_kross_cliffs_dk_coin,
        ],
        "KONG":  [
            Locations.criss_kross_cliffs_kong,
        ],
        "Balloons":  [
            Locations.criss_kross_cliffs_balloon_1,
            Locations.criss_kross_cliffs_balloon_2,
        ],
        "Bananas":  [
            Locations.criss_kross_cliffs_bananas_1,
            Locations.criss_kross_cliffs_bananas_2,
            Locations.criss_kross_cliffs_bananas_3,
        ],
        "Coins":  [
            Locations.criss_kross_cliffs_coin_1,
            Locations.criss_kross_cliffs_coin_2,
            Locations.criss_kross_cliffs_coin_3,
            Locations.criss_kross_cliffs_coin_4,
        ],
    },
    Regions.tyrant_twin_tussle_level:  {
        "Clear":  [
            Locations.tyrant_twin_tussle_clear,
        ],
        "Bonus":  [
            Locations.tyrant_twin_tussle_bonus_1,
            Locations.tyrant_twin_tussle_bonus_2,
            Locations.tyrant_twin_tussle_bonus_3,
        ],
        "DK Coin":  [
            Locations.tyrant_twin_tussle_dk_coin,
        ],
        "KONG":  [
            Locations.tyrant_twin_tussle_kong,
        ],
        "Balloons":  [
            Locations.tyrant_twin_tussle_balloon_1,
            Locations.tyrant_twin_tussle_balloon_2,
        ],
        "Bananas":  [
            Locations.tyrant_twin_tussle_bananas_1,
            Locations.tyrant_twin_tussle_bananas_2,
            Locations.tyrant_twin_tussle_bananas_3,
        ],
        "Coins":  [
            Locations.tyrant_twin_tussle_coin_1,
            Locations.tyrant_twin_tussle_coin_2,
            Locations.tyrant_twin_tussle_coin_3,
            Locations.tyrant_twin_tussle_coin_4,
            Locations.tyrant_twin_tussle_coin_5,
            Locations.tyrant_twin_tussle_coin_6,
        ],
    },
    Regions.swoopy_salvo_level:  {
        "Clear":  [
            Locations.swoopy_salvo_clear,
        ],
        "Bonus":  [
            Locations.swoopy_salvo_bonus_1,
            Locations.swoopy_salvo_bonus_2,
            Locations.swoopy_salvo_bonus_3,
        ],
        "DK Coin":  [
            Locations.swoopy_salvo_dk_coin,
        ],
        "KONG":  [
            Locations.swoopy_salvo_kong,
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.swoopy_salvo_bananas_1,
            Locations.swoopy_salvo_bananas_2,
        ],
        "Coins":  [
            Locations.swoopy_salvo_coin_1,
        ],
    },
    Regions.rocket_rush_level:  {
        "Clear":  [
            Locations.rocket_rush_clear,
        ],
        "Bonus":  [
        ],
        "DK Coin":  [
            Locations.rocket_rush_dk_coin,
        ],
        "KONG":  [
        ],
        "Balloons":  [
        ],
        "Bananas":  [
            Locations.rocket_rush_bananas_1,
            Locations.rocket_rush_bananas_2,
            Locations.rocket_rush_bananas_3,
        ],
        "Coins":  [
            Locations.rocket_rush_coin_1,
            Locations.rocket_rush_coin_2,
            Locations.rocket_rush_coin_3,
            Locations.rocket_rush_coin_4,
        ],
    },
    Regions.belchas_barn_level:  {
        "Clear":  [
            Locations.belchas_barn_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
    Regions.arichs_ambush_level:  {
        "Clear":  [
            Locations.arichs_ambush_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
    Regions.squirt_showdown_level:  {
        "Clear":  [
            Locations.squirt_showdown_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
    Regions.kaos_karnage_level:  {
        "Clear":  [
            Locations.kaos_karnage_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
    Regions.bleaks_house_level:  {
        "Clear":  [
            Locations.bleaks_house_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
    Regions.barbos_barrier_level:  {
        "Clear":  [
            Locations.barbos_barrier_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
    Regions.kastle_kaos_level:  {
        "Clear":  [
            Locations.kastle_kaos_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
    Regions.knautilus_level:  {
        "Clear":  [
            Locations.knautilus_clear,
        ],
        "Bonus":  [],
        "DK Coin":  [],
        "KONG":  [],
        "Balloons":  [],
        "Bananas":  [],
        "Coins":  [],
    },
}

level_rom_data = {
    Regions.lakeside_limbo_level: 0x34D19C,
    Regions.doorstop_dash_level: 0x34D1A7,
    Regions.tidal_trouble_level: 0x34D1BD,
    Regions.skiddas_row_level: 0x34D1C8,
    Regions.murky_mill_level: 0x34D1D3,
    Regions.barrel_shield_bust_up_level: 0x34D217,
    Regions.riverside_race_level: 0x34D22D,
    Regions.squeals_on_wheels_level: 0x34D238,
    Regions.springing_spiders_level: 0x34D24E,
    Regions.bobbing_barrel_brawl_level: 0x34D264,
    Regions.bazzas_blockade_level: 0x34D29D,
    Regions.rocket_barrel_ride_level: 0x34D2A8,
    Regions.kreeping_klasps_level: 0x34D2BE,
    Regions.tracker_barrel_trek_level: 0x34D2D4,
    Regions.fish_food_frenzy_level: 0x34D2DF,
    Regions.fireball_frenzy_level: 0x34D30D,
    Regions.demolition_drain_pipe_level: 0x34D323,
    Regions.ripsaw_rage_level: 0x34D339,
    Regions.blazing_bazukas_level: 0x34D34F,
    Regions.low_g_labyrinth_level: 0x34D35A,
    Regions.krevice_kreepers_level: 0x34D388,
    Regions.tearaway_toboggan_level: 0x34D393,
    Regions.barrel_drop_bounce_level: 0x34D39E,
    Regions.krackshot_krock_level: 0x34D3A9,
    Regions.lemguin_lunge_level: 0x34D3B4,
    Regions.buzzer_barrage_level: 0x34D40E,
    Regions.kongfused_cliffs_level: 0x34D424,
    Regions.floodlit_fish_level: 0x34D42F,
    Regions.pot_hole_panic_level: 0x34D43A,
    Regions.ropey_rumpus_level: 0x34D450,
    Regions.konveyor_rope_klash_level: 0x34D489,
    Regions.creepy_caverns_level: 0x34D49F,
    Regions.lightning_look_out_level: 0x34D4AA,
    Regions.koindozer_klamber_level: 0x34D4C0,
    Regions.poisonous_pipeline_level: 0x34D4D6,
    Regions.stampede_sprint_level: 0x34D51A,
    Regions.criss_kross_cliffs_level: 0x34D525,
    Regions.tyrant_twin_tussle_level: 0x34D530,
    Regions.swoopy_salvo_level: 0x34D53B,
    Regions.rocket_rush_level: 0x34D546,
}

level_list = [
    [Regions.lakeside_limbo_level, L11 >> 24],
    [Regions.doorstop_dash_level, L12 >> 24],
    [Regions.tidal_trouble_level, L13 >> 24],
    #[Regions.skiddas_row_level, L14 >> 24],
    [Regions.murky_mill_level, L15 >> 24],
    [Regions.barrel_shield_bust_up_level, L21 >> 24],
    [Regions.riverside_race_level, L22 >> 24],
    [Regions.squeals_on_wheels_level, L23 >> 24],
    [Regions.springing_spiders_level, L24 >> 24],
    [Regions.bobbing_barrel_brawl_level, L25 >> 24],
    [Regions.bazzas_blockade_level, L31 >> 24],
    [Regions.rocket_barrel_ride_level, L32 >> 24],
    [Regions.kreeping_klasps_level, L33 >> 24],
    [Regions.tracker_barrel_trek_level, L34 >> 24],
    [Regions.fish_food_frenzy_level, L35 >> 24],
    [Regions.fireball_frenzy_level, L41 >> 24],
    [Regions.demolition_drain_pipe_level, L42 >> 24],
    [Regions.ripsaw_rage_level, L43 >> 24],
    [Regions.blazing_bazukas_level, L44 >> 24],
    [Regions.low_g_labyrinth_level, L45 >> 24],
    [Regions.krevice_kreepers_level, L51 >> 24],
    [Regions.tearaway_toboggan_level, L52 >> 24],
    [Regions.barrel_drop_bounce_level, L53 >> 24],
    [Regions.krackshot_krock_level, L54 >> 24],
    [Regions.lemguin_lunge_level, L55 >> 24],
    [Regions.buzzer_barrage_level, L61 >> 24],
    [Regions.kongfused_cliffs_level, L62 >> 24],
    [Regions.floodlit_fish_level, L63 >> 24],
    [Regions.pot_hole_panic_level, L64 >> 24],
    [Regions.ropey_rumpus_level, L65 >> 24],
    [Regions.konveyor_rope_klash_level, L71 >> 24],
    [Regions.creepy_caverns_level, L72 >> 24],
    [Regions.lightning_look_out_level, L73 >> 24],
    [Regions.koindozer_klamber_level, L74 >> 24],
    [Regions.poisonous_pipeline_level, L75 >> 24],
    [Regions.stampede_sprint_level, L81 >> 24],
    [Regions.criss_kross_cliffs_level, L82 >> 24],
    [Regions.tyrant_twin_tussle_level, L83 >> 24],
    [Regions.swoopy_salvo_level, L84 >> 24],
    [Regions.rocket_rush_level, L85 >> 24],
]

boss_list = [
    [Regions.belchas_barn_level, L1B >> 24],
    [Regions.arichs_ambush_level, L2B >> 24],
    [Regions.squirt_showdown_level, L3B >> 24],
    [Regions.kaos_karnage_level, L4B >> 24],
    [Regions.bleaks_house_level, L5B >> 24],
    [Regions.barbos_barrier_level, L6B >> 24],
]

level_map = {
    Regions.lakeside_limbo_map: Regions.lake_orangatanga,
    Regions.doorstop_dash_map: Regions.lake_orangatanga,
    Regions.tidal_trouble_map: Regions.lake_orangatanga,
    Regions.skiddas_row_map: Regions.lake_orangatanga,
    Regions.murky_mill_map: Regions.lake_orangatanga,
    Regions.belchas_barn_map: Regions.lake_orangatanga,
    Regions.barrel_shield_bust_up_map: Regions.kremwood_forest,
    Regions.riverside_race_map: Regions.kremwood_forest,
    Regions.squeals_on_wheels_map: Regions.kremwood_forest,
    Regions.springing_spiders_map: Regions.kremwood_forest,
    Regions.bobbing_barrel_brawl_map: Regions.kremwood_forest,
    Regions.arichs_ambush_map: Regions.kremwood_forest,
    Regions.bazzas_blockade_map: Regions.cotton_top_cove,
    Regions.rocket_barrel_ride_map: Regions.cotton_top_cove,
    Regions.kreeping_klasps_map: Regions.cotton_top_cove,
    Regions.tracker_barrel_trek_map: Regions.cotton_top_cove,
    Regions.fish_food_frenzy_map: Regions.cotton_top_cove,
    Regions.squirt_showdown_map: Regions.cotton_top_cove,
    Regions.fireball_frenzy_map: Regions.mekanos,
    Regions.demolition_drain_pipe_map: Regions.mekanos,
    Regions.ripsaw_rage_map: Regions.mekanos,
    Regions.blazing_bazukas_map: Regions.mekanos,
    Regions.low_g_labyrinth_map: Regions.mekanos,
    Regions.kaos_karnage_map: Regions.mekanos,
    Regions.krevice_kreepers_map: Regions.k3,
    Regions.tearaway_toboggan_map: Regions.k3,
    Regions.barrel_drop_bounce_map: Regions.k3,
    Regions.krackshot_krock_map: Regions.k3,
    Regions.lemguin_lunge_map: Regions.k3,
    Regions.bleaks_house_map: Regions.k3,
    Regions.buzzer_barrage_map: Regions.razor_ridge,
    Regions.kongfused_cliffs_map: Regions.razor_ridge,
    Regions.floodlit_fish_map: Regions.razor_ridge,
    Regions.pot_hole_panic_map: Regions.razor_ridge,
    Regions.ropey_rumpus_map: Regions.razor_ridge,
    Regions.barbos_barrier_map: Regions.razor_ridge,
    Regions.konveyor_rope_klash_map: Regions.kaos_kore,
    Regions.creepy_caverns_map: Regions.kaos_kore,
    Regions.lightning_look_out_map: Regions.kaos_kore,
    Regions.koindozer_klamber_map: Regions.kaos_kore,
    Regions.poisonous_pipeline_map: Regions.kaos_kore,
    Regions.kastle_kaos_map: Regions.kaos_kore,
    Regions.stampede_sprint_map: Regions.krematoa,
    Regions.criss_kross_cliffs_map: Regions.krematoa,
    Regions.tyrant_twin_tussle_map: Regions.krematoa,
    Regions.swoopy_salvo_map: Regions.krematoa,
    Regions.rocket_rush_map: Regions.krematoa,
    Regions.knautilus_map: Regions.krematoa,
}

level_connections = {
    Regions.lakeside_limbo_map: Regions.lakeside_limbo_level,
    Regions.doorstop_dash_map: Regions.doorstop_dash_level,
    Regions.tidal_trouble_map: Regions.tidal_trouble_level,
    #Regions.skiddas_row_map: Regions.skiddas_row_level,
    Regions.murky_mill_map: Regions.murky_mill_level,
    Regions.barrel_shield_bust_up_map: Regions.barrel_shield_bust_up_level,
    Regions.riverside_race_map: Regions.riverside_race_level,
    Regions.squeals_on_wheels_map: Regions.squeals_on_wheels_level,
    Regions.springing_spiders_map: Regions.springing_spiders_level,
    Regions.bobbing_barrel_brawl_map: Regions.bobbing_barrel_brawl_level,
    Regions.bazzas_blockade_map: Regions.bazzas_blockade_level,
    Regions.rocket_barrel_ride_map: Regions.rocket_barrel_ride_level,
    Regions.kreeping_klasps_map: Regions.kreeping_klasps_level,
    Regions.tracker_barrel_trek_map: Regions.tracker_barrel_trek_level,
    Regions.fish_food_frenzy_map: Regions.fish_food_frenzy_level,
    Regions.fireball_frenzy_map: Regions.fireball_frenzy_level,
    Regions.demolition_drain_pipe_map: Regions.demolition_drain_pipe_level,
    Regions.ripsaw_rage_map: Regions.ripsaw_rage_level,
    Regions.blazing_bazukas_map: Regions.blazing_bazukas_level,
    Regions.low_g_labyrinth_map: Regions.low_g_labyrinth_level,
    Regions.krevice_kreepers_map: Regions.krevice_kreepers_level,
    Regions.tearaway_toboggan_map: Regions.tearaway_toboggan_level,
    Regions.barrel_drop_bounce_map: Regions.barrel_drop_bounce_level,
    Regions.krackshot_krock_map: Regions.krackshot_krock_level,
    Regions.lemguin_lunge_map: Regions.lemguin_lunge_level,
    Regions.buzzer_barrage_map: Regions.buzzer_barrage_level,
    Regions.kongfused_cliffs_map: Regions.kongfused_cliffs_level,
    Regions.floodlit_fish_map: Regions.floodlit_fish_level,
    Regions.pot_hole_panic_map: Regions.pot_hole_panic_level,
    Regions.ropey_rumpus_map: Regions.ropey_rumpus_level,
    Regions.konveyor_rope_klash_map: Regions.konveyor_rope_klash_level,
    Regions.creepy_caverns_map: Regions.creepy_caverns_level,
    Regions.lightning_look_out_map: Regions.lightning_look_out_level,
    Regions.koindozer_klamber_map: Regions.koindozer_klamber_level,
    Regions.poisonous_pipeline_map: Regions.poisonous_pipeline_level,
    Regions.stampede_sprint_map: Regions.stampede_sprint_level,
    Regions.criss_kross_cliffs_map: Regions.criss_kross_cliffs_level,
    Regions.tyrant_twin_tussle_map: Regions.tyrant_twin_tussle_level,
    Regions.swoopy_salvo_map: Regions.swoopy_salvo_level,
    Regions.rocket_rush_map: Regions.rocket_rush_level,
}

boss_connections = {
    Regions.belchas_barn_map: Regions.belchas_barn_level,
    Regions.arichs_ambush_map: Regions.arichs_ambush_level,
    Regions.squirt_showdown_map: Regions.squirt_showdown_level,
    Regions.kaos_karnage_map: Regions.kaos_karnage_level,
    Regions.bleaks_house_map: Regions.bleaks_house_level,
    Regions.barbos_barrier_map: Regions.barbos_barrier_level,
}

regional_events = {
    Regions.lake_orangatanga: Events.lake_level,
    Regions.kremwood_forest: Events.forest_level,
    Regions.cotton_top_cove: Events.cove_level,
    Regions.mekanos: Events.mekanos_level,
    Regions.k3: Events.k3_level,
    Regions.razor_ridge: Events.ridge_level,
    Regions.kaos_kore: Events.kore_level,
    Regions.krematoa: Events.krematoa_level,
}


def generate_level_list(world: "DKC3World"):
    shuffled_level_list = level_list.copy()
    shuffled_boss_list = boss_list.copy()
    if world.options.shuffle_levels:
        world.random.shuffle(shuffled_level_list)
        #world.random.shuffle(shuffled_boss_list)

    for map_level, level in level_connections.items():
        selected_level = shuffled_level_list.pop(0)
        world.level_connections[map_level] = selected_level[0]
        world.rom_connections[level] = selected_level

    for map_boss, boss in boss_connections.items():
        selected_boss = shuffled_boss_list.pop(0)
        world.level_connections[map_boss] = selected_boss[0]
        world.rom_connections[boss] = selected_boss

    # Place locked levels
    world.level_connections[Regions.skiddas_row_map] = Regions.skiddas_row_level

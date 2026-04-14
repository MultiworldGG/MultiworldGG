from enum import StrEnum

class Items(StrEnum):
    # Worlds
    lake_orangatanga = "Lake Orangatanga Access"
    kremwood_forest = "Kremwood Forest Access"
    cotton_top_cove = "Cotton-Top Cove Access"
    mekanos = "Mekanos Access"
    k3 = "K3 Access"
    razor_ridge = "Razor Ridge Access"
    kaos_kore = "Kaos Kore Access"
    krematoa = "Krematoa Access"
    # Currency
    bonus_coin = "Bonus Coin"       # Krematoa levels
    banana_bird = "Banana Bird"     # Boss Tokens?
    cog = "Cog"                     # Knautilus unlock
    # Unlockables
    dixie = "Dixie"
    kiddy = "Kiddy"
    vehicle = "Progressive Vehicle"
    carry = "Carry"
    spin = "Spin"
    climb = "Climb"
    team_attack = "Team Attack"
    helicopter_spin = "Helicopter Spin"
    water_bounce = "Water Bounce"
    swim = "Swim"
    ellie = "Ellie"
    enguarde = "Enguarde"
    squawks = "Squawks"
    squitter = "Squitter"
    parry = "Parry"
    barrel_cannon = "Barrel Cannon"
    barrel_rocket = "Rocket Barrel"
    barrel_tracker = "Tracker Barrel"
    barrel_ghost = "Ghost Barrel"
    barrel_warp = "Warp Barrel"
    barrel_invincible = "Invincibility Barrel"
    barrel_switch = "Barrel Switch"
    barrel_shield = "Barrel Shield"
    barrel_waterfall = "Waterfall Barrel"
    # Trade
    gift = "Present"
    wrench = "No.6 wrench"
    bowling_ball = "Bowling Ball"
    shell = "Shell"
    mirror = "Mirror"
    flower = "Flupperius Petallus Pongus"
    patch = "Patch"
    ski = "Ski"
    # Junk
    dk_barrel = "Backup DK Barrel"
    dk_coin = "DK Coin"             # Filler lol
    bear_coin = "Bear Coin"         # Hints?
    balloon = "Red Balloon"
    # Traps
    # Misc
    extractinator = "Banana Extractinator"
    radar = "Banana Radar"
    # Tracker
    glitched = "Skill"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)

class Locations(StrEnum):
    bird_bounty_beach = "Banana Bird - Bounty Beach"
    bird_kong_cave = "Banana Bird - Kong Cave"
    bird_undercover_cove = "Banana Bird - Undercover Cove"
    bird_belchas_burrow = "Banana Bird - Belcha's Burrow"
    bird_ks_kache = "Banana Bird - K's Kache"
    bird_hill_top_hoard = "Banana Bird - Hill-Top Hoard"
    bird_smugglers_cove = "Banana Bird - Smuggler's Cove"
    bird_arichs_hoard = "Banana Bird - Arich's Hoard"
    bird_bounty_bay = "Banana Bird - Bounty Bay"
    bird_sky_high_secret = "Banana Bird - Sky-High Secret"
    bird_glacial_grotto = "Banana Bird - Glacial Grotto"
    bird_clifftop_cache = "Banana Bird - Clifftop Cache"
    bird_sewer_stockpile = "Banana Bird - Sewer Stockpile"

    belchas_barn_clear = "Belcha's Barn - Clear"
    arichs_ambush_clear = "Arich's Ambush - Clear"
    squirt_showdown_clear = "Squirt's Showdown - Clear"
    kaos_karnage_clear = "KAOS Karnage - Clear"
    bleaks_house_clear = "Bleak's House - Clear"
    barbos_barrier_clear = "Barbos's Barrier - Clear"
    kastle_kaos_clear = "Kastle KAOS - Clear"
    knautilus_clear = "Knautilus - Clear"

    defeated_belcha = "Defeated Belcha"
    defeated_arich = "Defeated Arich"
    defeated_squirt = "Defeated Squirt"
    defeated_kaos = "Defeated KAOS"
    defeated_bleak = "Defeated Bleak"
    defeated_barbos = "Defeated Barbos"
    defeated_krool_castle = "Defeated K. Rool at Kastle"
    defeated_krool_knautilus = "Defeated K. Rool at Knautilus"

    lakeside_limbo_clear = "Lakeside Limbo - Clear"
    lakeside_limbo_bonus_1 = "Lakeside Limbo - Bonus #1"
    lakeside_limbo_bonus_2 = "Lakeside Limbo - Bonus #2"
    lakeside_limbo_dk_coin = "Lakeside Limbo - DK Coin"
    lakeside_limbo_kong = "Lakeside Limbo - KONG"
    lakeside_limbo_balloon_1 = "Lakeside Limbo - Balloon #1 (On roof at the start)" # 2
    lakeside_limbo_balloon_2 = "Lakeside Limbo - Balloon #2 (On roof at the start)" # 3
    lakeside_limbo_bananas_1 = "Lakeside Limbo - Banana Bunch #1 (At start)" # 4
    lakeside_limbo_coin_1 = "Lakeside Limbo - Bear Coin #1 (On roof near checkpoint)" # 20
    lakeside_limbo_balloon_3 = "Lakeside Limbo - Balloon #3 (On roof near checkpoint)" # 21
    lakeside_limbo_coin_2 = "Lakeside Limbo - Bear Coin #2 (On roof near checkpoint)" # 22
    lakeside_limbo_bananas_2 = "Lakeside Limbo - Banana Bunch #2 (Underwater after checkpoint)" # 27
    lakeside_limbo_balloon_4 = "Lakeside Limbo - Balloon #4 (Near bonus #2)" # 31
    lakeside_limbo_balloon_5 = "Lakeside Limbo - Balloon #5 (Near no animal sign)" # 38
    lakeside_limbo_coin_3 = "Lakeside Limbo - Bear Coin #3 (No animal sign reward)" # 41
    lakeside_limbo_coin_4 = "Lakeside Limbo - Bear Coin #4 (On roof at the end)" # 44
    lakeside_limbo_bananas_3 = "Lakeside Limbo - Banana Bunch #3 (On roof at the end)" # 45
    lakeside_limbo_bananas_4 = "Lakeside Limbo - Banana Bunch #4 (At the end)" # 46

    doorstop_dash_clear = "Doorstop Dash - Clear"
    doorstop_dash_bonus_1 = "Doorstop Dash - Bonus #1"
    doorstop_dash_bonus_2 = "Doorstop Dash - Bonus #2"
    doorstop_dash_dk_coin = "Doorstop Dash - DK Coin"
    doorstop_dash_kong = "Doorstop Dash - KONG"
    doorstop_dash_bananas_1 = "Doorstop Dash - Banana Bunch #1 (Near start)" # 3
    doorstop_dash_coin_1 = "Doorstop Dash - Bear Coin #1 (Above second door)" # 18
    doorstop_dash_balloon_1 = "Doorstop Dash - Balloon #1 (Near bonus #1)" # 35
    doorstop_dash_balloon_2 = "Doorstop Dash - Balloon #2 (Invisible near rope)" # 72
    doorstop_dash_bananas_2 = "Doorstop Dash - Banana Bunch #1 (Near open trap door)" # 77
    doorstop_dash_coin_2 = "Doorstop Dash - Bear Coin #2 (Above pile of bags)" # 78
    doorstop_dash_balloon_3 = "Doorstop Dash - Balloon #3 (At the top the big fall)" # 114
    doorstop_dash_balloon_4 = "Doorstop Dash - Balloon #4 (Near the end of big fall)" # 115

    tidal_trouble_clear = "Tidal Trouble - Clear"
    tidal_trouble_bonus_1 = "Tidal Trouble - Bonus #1"
    tidal_trouble_bonus_2 = "Tidal Trouble - Bonus #2"
    tidal_trouble_dk_coin = "Tidal Trouble - DK Coin"
    tidal_trouble_kong = "Tidal Trouble - KONG"
    tidal_trouble_bananas_1 = "Tidal Trouble - Banana Bunch #1 (Above green Koco)" # 14
    tidal_trouble_bananas_2 = "Tidal Trouble - Banana Bunch #2 (No animal sign reward)" # 22
    tidal_trouble_coin_1 = "Tidal Trouble - Bear Coin #1 (Above green Buzz)" # 29
    tidal_trouble_coin_2 = "Tidal Trouble - Bear Coin #2 (Above green Buzz between two wooden pillars)" # 32
    tidal_trouble_balloon_1 = "Tidal Trouble - Balloon #1 (Below cracked floor at the end)" # 58

    skiddas_row_clear = "Skidda's Row - Clear"
    skiddas_row_bonus_1 = "Skidda's Row - Bonus #1"
    skiddas_row_bonus_2 = "Skidda's Row - Bonus #2"
    skiddas_row_dk_coin = "Skidda's Row - DK Coin"
    skiddas_row_kong = "Skidda's Row - KONG"
    skiddas_row_coin_1 = "Skidda's Row - Bear Coin #1 (Inside second house)" # 6
    skiddas_row_coin_2 = "Skidda's Row - Bear Coin #2 (Invisible between two holes)" # 9
    skiddas_row_coin_3 = "Skidda's Row - Bear Coin #3 (Above O)" # 16
    skiddas_row_bananas_1 = "Skidda's Row - Banana Bunch #1 (After a background Snowman)" # 32
    skiddas_row_balloon_1 = "Skidda's Row - Balloon #1 (Above Knik-Knak)" # 33

    murky_mill_clear = "Murky Mill - Clear"
    murky_mill_bonus_1 = "Murky Mill - Bonus #1"
    murky_mill_bonus_2 = "Murky Mill - Bonus #2"
    murky_mill_dk_coin = "Murky Mill - DK Coin"
    murky_mill_kong = "Murky Mill - KONG"
    murky_mill_bananas_1 = "Murky Mill - Banana Bunch #1 (After getting Ellie)" # 10
    murky_mill_bananas_2 = "Murky Mill - Banana Bunch #2 (Above second lift)" # 13
    murky_mill_coin_1 = "Murky Mill - Bear Coin #1 (Above Re-Koil)" # 18
    murky_mill_coin_2 = "Murky Mill - Bear Coin #2 (In corner after falling section with red Buzzes)" # 52
    murky_mill_coin_3 = "Murky Mill - Bear Coin #3 (No animal sign)" # 77
    murky_mill_balloon_1 = "Murky Mill - Balloon #1 (Above Sneek)" # 24

    barrel_shield_bust_up_clear = "Barrel Shield Bust-Up - Clear"
    barrel_shield_bust_up_bonus_1 = "Barrel Shield Bust-Up - Bonus #1"
    barrel_shield_bust_up_bonus_2 = "Barrel Shield Bust-Up - Bonus #2"
    barrel_shield_bust_up_dk_coin = "Barrel Shield Bust-Up - DK Coin"
    barrel_shield_bust_up_kong = "Barrel Shield Bust-Up - KONG"
    barrel_shield_bust_up_bananas_1 = "Barrel Shield Bust-Up - Banana Bunch #1 (At start behind Buzz)" # 7
    barrel_shield_bust_up_bananas_2 = "Barrel Shield Bust-Up - Banana Bunch #2 (Between trees)" # 30
    barrel_shield_bust_up_coin_1 = "Barrel Shield Bust-Up - Bear Coin #1 (In hole above Barrel Kannon)" # 34
    barrel_shield_bust_up_coin_2 = "Barrel Shield Bust-Up - Bear Coin #2 (In ledge)" # 60

    riverside_race_clear = "Riverside Race - Clear"
    riverside_race_bonus_1 = "Riverside Race - Bonus #1"
    riverside_race_bonus_2 = "Riverside Race - Bonus #2"
    riverside_race_dk_coin = "Riverside Race - DK Coin"
    riverside_race_kong = "Riverside Race - KONG"
    riverside_race_bananas_1 = "Riverside Race - Banana Bunch #1 (At start)" # 2
    riverside_race_coin_1 = "Riverside Race - Bear Coin #1 (Before second pond)" # 8
    riverside_race_coin_2 = "Riverside Race - Bear Coin #2 (In second pond)" # 10
    riverside_race_bananas_2 = "Riverside Race - Banana Bunch #2 (In water below bonus #1)" # 15
    riverside_race_balloon_1 = "Riverside Race - Balloon #1 (On detour)" # 24
    riverside_race_bananas_3 = "Riverside Race - Banana Bunch #3 (In pond with single Red Koco)" # 32
    riverside_race_bananas_4 = "Riverside Race - Banana Bunch #4 (In pond with single Red Koco)" # 33
    riverside_race_bananas_5 = "Riverside Race - Banana Bunch #5 (In pond with single Red Koco)" # 35
    riverside_race_coin_3 = "Riverside Race - Bear Coin #3 (In pond after bonus #2)" # 49
    riverside_race_bananas_6 = "Riverside Race - Banana Bunch #6 (Between two Re-Koils)" # 52
    riverside_race_coin_4 = "Riverside Race - Bear Coin #4 (In last pond)" # 60

    squeals_on_wheels_clear = "Squeals on Wheels - Clear"
    squeals_on_wheels_bonus_1 = "Squeals on Wheels - Bonus #1"
    squeals_on_wheels_bonus_2 = "Squeals on Wheels - Bonus #2"
    squeals_on_wheels_dk_coin = "Squeals on Wheels - DK Coin"
    squeals_on_wheels_kong = "Squeals on Wheels - KONG"
    squeals_on_wheels_bananas_1 = "Squeals on Wheels - Banana Bunch #1 (At start)" # 45
    squeals_on_wheels_bananas_2 = "Squeals on Wheels - Banana Bunch #2 (At end of first rope)" # 51
    squeals_on_wheels_bananas_3 = "Squeals on Wheels - Banana Bunch #3 (At end of first rope)" # 53
    squeals_on_wheels_bananas_4 = "Squeals on Wheels - Banana Bunch #4 (Above steel keg after N)" # 104
    squeals_on_wheels_bananas_5 = "Squeals on Wheels - Banana Bunch #5 (Above steel keg after N)" # 105
    squeals_on_wheels_bananas_6 = "Squeals on Wheels - Banana Bunch #6 (In corner near Barrel Kannon)" # 114
    squeals_on_wheels_bananas_7 = "Squeals on Wheels - Banana Bunch #7 (Near top of the level)" # 121
    squeals_on_wheels_coin_1 = "Squeals on Wheels - Bear Coin #1 (Above Booty Bird)" # 135
    squeals_on_wheels_balloon_1 = "Squeals on Wheels - Balloon #1 (No animal sign)" # 139

    springing_spiders_clear = "Springin' Spiders - Clear"
    springing_spiders_bonus_1 = "Springin' Spiders - Bonus #1"
    springing_spiders_bonus_2 = "Springin' Spiders - Bonus #2"
    springing_spiders_dk_coin = "Springin' Spiders - DK Coin"
    springing_spiders_kong = "Springin' Spiders - KONG"
    springing_spiders_coin_1 = "Springin' Spiders - Bear Coin #1 (Above Warp Barrel)" # 63
    springing_spiders_balloon_1 = "Springin' Spiders - Balloon #1 (Above a red Buzz at the start)" # 78
    springing_spiders_bananas_1 = "Springin' Spiders - Banana Bunch #1 (Hidden in top corner)" # 36
    springing_spiders_coin_2 = "Springin' Spiders - Bear Coin #2 (Behind a green Buzz)" # 77
    springing_spiders_coin_3 = "Springin' Spiders - Bear Coin #3 (In a ledge below a Buzz)" # 76
    springing_spiders_coin_4 = "Springin' Spiders - Bear Coin #4 (In a ledge below a Buzz)" # 120
    springing_spiders_bananas_2 = "Springin' Spiders - Banana Bunch #1 (Behind Green Buzz before no animal sign)" # 68
    springing_spiders_coin_5 = "Springin' Spiders - Bear Coin #5 (No animal sign)" # 88
    springing_spiders_coin_6 = "Springin' Spiders - Bear Coin #6 (Above Red Buzz)" # 47
    springing_spiders_bananas_3 = "Springin' Spiders - Banana Bunch #4 (Above Red Buzz)" # 50
    springing_spiders_bananas_4 = "Springin' Spiders - Banana Bunch #5 (Below a wooden barrel)" # 101
    springing_spiders_balloon_2 = "Springin' Spiders - Balloon #2 (In hole between Buzzes)" # 62
    springing_spiders_balloon_3 = "Springin' Spiders - Balloon #3 (Below N)" # 37
    springing_spiders_bananas_5 = "Springin' Spiders - Banana Bunch #6 (Above a red Buzz)" # 100
    springing_spiders_bananas_6 = "Springin' Spiders - Banana Bunch #7 (Next to a hole with a single banana below)" # 109
    springing_spiders_coin_7 = "Springin' Spiders - Bear Coin #7 (Next to Bonus #2)" # 72

    bobbing_barrel_brawl_clear = "Bobbing Barrel Brawl - Clear"
    bobbing_barrel_brawl_bonus_1 = "Bobbing Barrel Brawl - Bonus #1"
    bobbing_barrel_brawl_bonus_2 = "Bobbing Barrel Brawl - Bonus #2"
    bobbing_barrel_brawl_dk_coin = "Bobbing Barrel Brawl - DK Coin"
    bobbing_barrel_brawl_kong = "Bobbing Barrel Brawl - KONG"
    bobbing_barrel_brawl_balloon_1 = "Bobbing Barrel Brawl - Balloon #1 (Cache below Koin)" # 0
    bobbing_barrel_brawl_coin_1 = "Bobbing Barrel Brawl - Bear Coin #1 (Above Knik-Knak)" # 40
    bobbing_barrel_brawl_coin_2 = "Bobbing Barrel Brawl - Bear Coin #2 (Before Green-Red Buzz combo)" # 90
    bobbing_barrel_brawl_bananas_1 = "Bobbing Barrel Brawl - Banana Bunch #1 (No animal sign)" # 100
    bobbing_barrel_brawl_coin_3 = "Bobbing Barrel Brawl - Bear Coin #3 (Cache below no animal sign)" # 1

    bazzas_blockade_clear = "Bazza's Blockade - Clear"
    bazzas_blockade_bonus_1 = "Bazza's Blockade - Bonus #1"
    bazzas_blockade_bonus_2 = "Bazza's Blockade - Bonus #2"
    bazzas_blockade_dk_coin = "Bazza's Blockade - DK Coin"
    bazzas_blockade_kong = "Bazza's Blockade - KONG"
    bazzas_blockade_bananas_1 = "Bazza's Blockade - Banana Bunch #1 (Near start)" # 14
    bazzas_blockade_bananas_2 = "Bazza's Blockade - Banana Bunch #2 (Near start)" # 13
    bazzas_blockade_coin_1 = "Bazza's Blockade - Bear Coin #1 (In small passage)" # 38
    bazzas_blockade_coin_2 = "Bazza's Blockade - Bear Coin #2 (In small passage)" # 37
    bazzas_blockade_coin_3 = "Bazza's Blockade - Bear Coin #3 (Below Bazza's exit)" # 62
    bazzas_blockade_coin_4 = "Bazza's Blockade - Bear Coin #4 (In Bounty Bass near end)" # 87

    rocket_barrel_ride_clear = "Rocket Barrel Ride - Clear"
    rocket_barrel_ride_bonus_1 = "Rocket Barrel Ride - Bonus #1"
    rocket_barrel_ride_bonus_2 = "Rocket Barrel Ride - Bonus #2"
    rocket_barrel_ride_dk_coin = "Rocket Barrel Ride - DK Coin"
    rocket_barrel_ride_kong = "Rocket Barrel Ride - KONG"
    rocket_barrel_ride_bananas_1 = "Rocket Barrel Ride - Banana Bunch #1 (After first rocket)" # 5
    rocket_barrel_ride_bananas_2 = "Rocket Barrel Ride - Banana Bunch #2 (Behind waterfall near start)" # 7
    rocket_barrel_ride_coin_1 = "Rocket Barrel Ride - Bear Coin #1 (Behind waterfall near start)" # 8
    rocket_barrel_ride_coin_2 = "Rocket Barrel Ride - Bear Coin #2 (Before third rocket)" # 11
    rocket_barrel_ride_bananas_3 = "Rocket Barrel Ride - Banana Bunch #3 (Near Barrel Kannons)" # 16
    rocket_barrel_ride_coin_3 = "Rocket Barrel Ride - Bear Coin #3 (Near Barrel Kannons)" # 17
    rocket_barrel_ride_bananas_4 = "Rocket Barrel Ride - Banana Bunch #4 (After Barrel Kannons)" # 19
    rocket_barrel_ride_coin_4 = "Rocket Barrel Ride - Bear Coin #4 (Behind waterfall above K)" # 25
    rocket_barrel_ride_coin_5 = "Rocket Barrel Ride - Bear Coin #5 (Next to a rotating barrel)" # 36
    rocket_barrel_ride_bananas_5 = "Rocket Barrel Ride - Banana Bunch #5 (Near checkpoint)" # 49
    rocket_barrel_ride_coin_6 = "Rocket Barrel Ride - Bear Coin #6 (Above Krimp behind waterfall)" # 58
    rocket_barrel_ride_bananas_6 = "Rocket Barrel Ride - Banana Bunch #6 (After Krumple pair)" # 83
    rocket_barrel_ride_bananas_7 = "Rocket Barrel Ride - Banana Bunch #7 (After Krumple pair)" # 84
    rocket_barrel_ride_balloon_1 = "Rocket Barrel Ride - Balloon #1 (After Krumple pair)" # 85
    rocket_barrel_ride_balloon_2 = "Rocket Barrel Ride - Balloon #1 (No animal sign)" # 89

    kreeping_klasps_clear = "Kreeping Klasps - Clear"
    kreeping_klasps_bonus_1 = "Kreeping Klasps - Bonus #1"
    kreeping_klasps_bonus_2 = "Kreeping Klasps - Bonus #2"
    kreeping_klasps_dk_coin = "Kreeping Klasps - DK Coin"
    kreeping_klasps_kong = "Kreeping Klasps - KONG"
    kreeping_klasps_balloon_1 = "Kreeping Klasps - Balloon #1 (Near start)" # 7
    kreeping_klasps_coin_1 = "Kreeping Klasps - Bear Coin #1 (Near start below cracked ground)" # 10
    kreeping_klasps_bananas_1 = "Kreeping Klasps - Banana Bunch #1 (After bonus #1)" # 21
    kreeping_klasps_balloon_2 = "Kreeping Klasps - Balloon #2 (After bonus #1)" # 23
    kreeping_klasps_bananas_2 = "Kreeping Klasps - Banana Bunch #2 (Before checkpoint)" # 29
    kreeping_klasps_coin_2 = "Kreeping Klasps - Bear Coin #2 (After checkpoint)" # 35

    tracker_barrel_trek_clear = "Tracker Barrel Trek - Clear"
    tracker_barrel_trek_bonus_1 = "Tracker Barrel Trek - Bonus #1"
    tracker_barrel_trek_bonus_2 = "Tracker Barrel Trek - Bonus #2"
    tracker_barrel_trek_dk_coin = "Tracker Barrel Trek - DK Coin"
    tracker_barrel_trek_kong = "Tracker Barrel Trek - KONG"
    tracker_barrel_trek_coin_1 = "Tracker Barrel Trek - Bear Coin #1 (Near start above DK Barrel)" # 4
    tracker_barrel_trek_coin_2 = "Tracker Barrel Trek - Bear Coin #2 (Between Krumples)" # 11
    tracker_barrel_trek_bananas_1 = "Tracker Barrel Trek - Banana Bunch #1 (Above Tracker Barrel)" # 15
    tracker_barrel_trek_balloon_1 = "Tracker Barrel Trek - Balloon #1 (Near checkpoint)" # 33
    tracker_barrel_trek_coin_3 = "Tracker Barrel Trek - Bear Coin #3 (Behind waterffal above two Re-Koils)" # 47
    tracker_barrel_trek_coin_4 = "Tracker Barrel Trek - Bear Coin #4 (Before Koin)" # 66

    fish_food_frenzy_clear = "Fish Food Frenzy - Clear"
    fish_food_frenzy_bonus_1 = "Fish Food Frenzy - Bonus #1"
    fish_food_frenzy_bonus_2 = "Fish Food Frenzy - Bonus #2"
    fish_food_frenzy_dk_coin = "Fish Food Frenzy - DK Coin"
    fish_food_frenzy_kong = "Fish Food Frenzy - KONG"
    fish_food_frenzy_coin_1 = "Fish Food Frenzy - Bear Coin #1 (Near start)" # 8
    fish_food_frenzy_bananas_1 = "Fish Food Frenzy - Banana Bunch #1 (Above Lurchin before O)" # 13
    fish_food_frenzy_coin_2 = "Fish Food Frenzy - Bear Coin #2 (Below Lurchin)" # 54

    fireball_frenzy_clear = "Fire-Ball Frenzy - Clear"
    fireball_frenzy_bonus_1 = "Fire-Ball Frenzy - Bonus #1"
    fireball_frenzy_bonus_2 = "Fire-Ball Frenzy - Bonus #2"
    fireball_frenzy_dk_coin = "Fire-Ball Frenzy - DK Coin"
    fireball_frenzy_kong = "Fire-Ball Frenzy - KONG"
    fireball_frenzy_coin_1 = "Fire-Ball Frenzy - Bear Coin #1 (Near start)" # 17
    fireball_frenzy_coin_2 = "Fire-Ball Frenzy - Bear Coin #2 (In a corner above rope)" # 29
    fireball_frenzy_bananas_1 = "Fire-Ball Frenzy - Banana Bunch #1 (Before checkpoint)" # 49
    fireball_frenzy_coin_3 = "Fire-Ball Frenzy - Bear Coin #3 (After checkpoint)" # 54
    fireball_frenzy_bananas_2 = "Fire-Ball Frenzy - Banana Bunch #2 (After checkpoint)" # 55
    fireball_frenzy_coin_4 = "Fire-Ball Frenzy - Bear Coin #4 (No animal sign)" # 62
    fireball_frenzy_coin_5 = "Fire-Ball Frenzy - Bear Coin #5 (After no animal sign)" # 61
    fireball_frenzy_bananas_3 = "Fire-Ball Frenzy - Banana Bunch #3 (In corner below wooden platform)" # 72

    demolition_drain_pipe_clear = "Demolition Drain-Pipe - Clear"
    demolition_drain_pipe_bonus_1 = "Demolition Drain-Pipe - Bonus #1"
    demolition_drain_pipe_bonus_2 = "Demolition Drain-Pipe - Bonus #2"
    demolition_drain_pipe_dk_coin = "Demolition Drain-Pipe - DK Coin"
    demolition_drain_pipe_kong = "Demolition Drain-Pipe - KONG"
    demolition_drain_pipe_coin_1 = "Demolition Drain-Pipe - Bear Coin #1" # 3
    demolition_drain_pipe_bananas_1 = "Demolition Drain-Pipe - Banana Bunch #1" # 4
    demolition_drain_pipe_coin_2 = "Demolition Drain-Pipe - Bear Coin #2" # 12
    demolition_drain_pipe_bananas_2 = "Demolition Drain-Pipe - Banana Bunch #2" # 15
    demolition_drain_pipe_coin_3 = "Demolition Drain-Pipe - Bear Coin #3" # 16
    demolition_drain_pipe_bananas_3 = "Demolition Drain-Pipe - Banana Bunch #3" # 18
    demolition_drain_pipe_coin_4 = "Demolition Drain-Pipe - Bear Coin #4" # 22
    demolition_drain_pipe_bananas_4 = "Demolition Drain-Pipe - Banana Bunch #4" # 36
    demolition_drain_pipe_bananas_5 = "Demolition Drain-Pipe - Banana Bunch #5" # 44
    demolition_drain_pipe_bananas_6 = "Demolition Drain-Pipe - Banana Bunch #6" # 63
    demolition_drain_pipe_coin_5 = "Demolition Drain-Pipe - Bear Coin #5" # 69
    demolition_drain_pipe_coin_6 = "Demolition Drain-Pipe - Bear Coin #6" # 78
    demolition_drain_pipe_coin_7 = "Demolition Drain-Pipe - Bear Coin #7" # 81
    demolition_drain_pipe_bananas_7 = "Demolition Drain-Pipe - Banana Bunch #7" # 84

    ripsaw_rage_clear = "Ripsaw Rage - Clear"
    ripsaw_rage_bonus_1 = "Ripsaw Rage - Bonus #1"
    ripsaw_rage_bonus_2 = "Ripsaw Rage - Bonus #2"
    ripsaw_rage_dk_coin = "Ripsaw Rage - DK Coin"
    ripsaw_rage_kong = "Ripsaw Rage - KONG"
    ripsaw_rage_coin_1 = "Ripsaw Rage - Bear Coin #1 (After exiting second tree at start)" # 4
    ripsaw_rage_bananas_1 = "Ripsaw Rage - Banana Bunch #1 (Below branch)" # 7
    ripsaw_rage_coin_2 = "Ripsaw Rage - Bear Coin #2 (Below wooden barrel for bonus 1)" # 10
    ripsaw_rage_bananas_2 = "Ripsaw Rage - Banana Bunch #2 (Below Sneek)" # 22
    ripsaw_rage_coin_3 = "Ripsaw Rage - Bear Coin #3 (Between branches)" # 25
    ripsaw_rage_bananas_3 = "Ripsaw Rage - Banana Bunch #3 (Between branches before steel keg)" # 31
    ripsaw_rage_bananas_4 = "Ripsaw Rage - Banana Bunch #4 (Below branch near Koin)" # 43

    blazing_bazukas_clear = "Blazing Bazukas - Clear"
    blazing_bazukas_bonus_1 = "Blazing Bazukas - Bonus #1"
    blazing_bazukas_bonus_2 = "Blazing Bazukas - Bonus #2"
    blazing_bazukas_dk_coin = "Blazing Bazukas - DK Coin"
    blazing_bazukas_kong = "Blazing Bazukas - KONG"
    blazing_bazukas_coin_1 = "Blazing Bazukas - Bear Coin #1 (In rope near start)" # 7
    blazing_bazukas_bananas_1 = "Blazing Bazukas - Banana Bunch #1 (No animal sign)" # 45
    blazing_bazukas_coin_2 = "Blazing Bazukas - Bear Coin #2 (Next to Barrel Cannon before No animal sign)" # 26
    blazing_bazukas_coin_3 = "Blazing Bazukas - Bear Coin #3 (No animal sign)" # 62
    blazing_bazukas_bananas_2 = "Blazing Bazukas - Banana Bunch #2 (Before pair of Krimps)" # 85
    blazing_bazukas_bananas_3 = "Blazing Bazukas - Banana Bunch #3 (Above Bazuka)" # 101
    blazing_bazukas_coin_4 = "Blazing Bazukas - Bear Coin #4 (Above Bazuka)" # 103
    blazing_bazukas_balloon_1 = "Blazing Bazukas - Balloon #1 (Near end)" # 111

    low_g_labyrinth_clear = "Low-G Labyrinth - Clear"
    low_g_labyrinth_bonus_1 = "Low-G Labyrinth - Bonus #1"
    low_g_labyrinth_bonus_2 = "Low-G Labyrinth - Bonus #2"
    low_g_labyrinth_dk_coin = "Low-G Labyrinth - DK Coin"
    low_g_labyrinth_kong = "Low-G Labyrinth - KONG"
    low_g_labyrinth_bananas_1 = "Low-G Labyrinth - Banana Bunch #1 (Near start)" # 8
    low_g_labyrinth_coin_1 = "Low-G Labyrinth - Bear Coin #1 (In a corner next to a banana arc)" # 20
    low_g_labyrinth_bananas_2 = "Low-G Labyrinth - Banana Bunch #2 (Below O)" # 31
    low_g_labyrinth_coin_2 = "Low-G Labyrinth - Bear Coin #2 (Above a Buzzes column)" # 49
    low_g_labyrinth_bananas_3 = "Low-G Labyrinth - Banana Bunch #3 (Between two circling Buzzes)" # 79
    low_g_labyrinth_balloon_1 = "Low-G Labyrinth - Balloon #1 (In a long fall)" # 91
    low_g_labyrinth_coin_3 = "Low-G Labyrinth - Bear Coin #3 (In a long fall)" # 92
    low_g_labyrinth_coin_4 = "Low-G Labyrinth - Bear Coin #4 (Near invincibility barrel)" # 101
    low_g_labyrinth_coin_5 = "Low-G Labyrinth - Bear Coin #5 (Near invincibility barrel)" # 100
    low_g_labyrinth_coin_6 = "Low-G Labyrinth - Bear Coin #6 (Near invincibility barrel)" # 99
    low_g_labyrinth_coin_7 = "Low-G Labyrinth - Bear Coin #7 (No animal sign)" # 113
    low_g_labyrinth_bananas_4 = "Low-G Labyrinth - Banana Bunch #4 (Behind green Buzz)" # 116

    krevice_kreepers_clear = "Krevice Kreepers - Clear"
    krevice_kreepers_bonus_1 = "Krevice Kreepers - Bonus #1"
    krevice_kreepers_bonus_2 = "Krevice Kreepers - Bonus #2"
    krevice_kreepers_dk_coin = "Krevice Kreepers - DK Coin"
    krevice_kreepers_kong = "Krevice Kreepers - KONG"
    krevice_kreepers_bananas_1 = "Krevice Kreepers - Banana Bunch #1 (Above start)" # 3
    krevice_kreepers_bananas_2 = "Krevice Kreepers - Banana Bunch #2 (Above start)" # 4
    krevice_kreepers_bananas_3 = "Krevice Kreepers - Banana Bunch #3 (Above start)" # 5
    krevice_kreepers_coin_1 = "Krevice Kreepers - Bear Coin #1 (Near start)" # 11
    krevice_kreepers_bananas_4 = "Krevice Kreepers - Banana Bunch #4 (Near start)" # 13
    krevice_kreepers_coin_2 = "Krevice Kreepers - Bear Coin #2 (Cache near start)" # 2
    krevice_kreepers_balloon_1 = "Krevice Kreepers - Balloon #1 (Floating between two rocks)" # 26
    krevice_kreepers_coin_3 = "Krevice Kreepers - Bear Coin #3 (Near Koin)" # 34
    krevice_kreepers_coin_4 = "Krevice Kreepers - Bear Coin #4 (Next to rope with 4 bananas)" # 65
    krevice_kreepers_coin_5 = "Krevice Kreepers - Bear Coin #5 (Cache below last wooden ledge)" # 1
    krevice_kreepers_coin_6 = "Krevice Kreepers - Bear Coin #6 (Cache below goal)" # 0

    tearaway_toboggan_clear = "Tearaway Toboggan - Clear"
    tearaway_toboggan_bonus_1 = "Tearaway Toboggan - Bonus #1"
    tearaway_toboggan_bonus_2 = "Tearaway Toboggan - Bonus #2"
    tearaway_toboggan_dk_coin = "Tearaway Toboggan - DK Coin"
    tearaway_toboggan_kong = "Tearaway Toboggan - KONG"
    tearaway_toboggan_coin_1 = "Tearaway Toboggan - Bear Coin #1 (Above green Buzz in house)" # 9
    tearaway_toboggan_bananas_1 = "Tearaway Toboggan - Banana Bunch #1 (After banana arc)" # 15
    tearaway_toboggan_coin_2 = "Tearaway Toboggan - Bear Coin #2 (After a Skidda)" # 21
    tearaway_toboggan_coin_3 = "Tearaway Toboggan - Bear Coin #3 (Inside house)" # 22
    tearaway_toboggan_bananas_2 = "Tearaway Toboggan - Banana Bunch #2 (In a hill)" # 27
    tearaway_toboggan_coin_4 = "Tearaway Toboggan - Bear Coin #4 (Above house)" # 30
    tearaway_toboggan_bananas_3 = "Tearaway Toboggan - Banana Bunch #3 (Above a Knik-Knak)" # 31
    tearaway_toboggan_balloon_1 = "Tearaway Toboggan - Balloon #1 (Below a Knik-Knak)" # 33
    tearaway_toboggan_coin_5 = "Tearaway Toboggan - Bear Coin #5 (Below a Knik-Knak)" # 41
    tearaway_toboggan_coin_6 = "Tearaway Toboggan - Bear Coin #6 (Above house)" # 45
    tearaway_toboggan_bananas_4 = "Tearaway Toboggan - Banana Bunch #4 (Next to a Knik-Knak)" # 46
    tearaway_toboggan_bananas_5 = "Tearaway Toboggan - Banana Bunch #5 (At the end of a big hill)" # 66
    tearaway_toboggan_bananas_6 = "Tearaway Toboggan - Banana Bunch #6 (After a big hill)" # 67
    tearaway_toboggan_bananas_7 = "Tearaway Toboggan - Banana Bunch #7 (Inside Booty Bird)" # 71
    tearaway_toboggan_balloon_2 = "Tearaway Toboggan - Balloon #2 (At the end)" # 74

    barrel_drop_bounce_clear = "Barrel Drop Bounce - Clear"
    barrel_drop_bounce_bonus_1 = "Barrel Drop Bounce - Bonus #1"
    barrel_drop_bounce_bonus_2 = "Barrel Drop Bounce - Bonus #2"
    barrel_drop_bounce_dk_coin = "Barrel Drop Bounce - DK Coin"
    barrel_drop_bounce_kong = "Barrel Drop Bounce - KONG"
    barrel_drop_bounce_coin_1 = "Barrel Drop Bounce - Bear Coin #1 (At start)" # 0
    barrel_drop_bounce_coin_2 = "Barrel Drop Bounce - Bear Coin #2 (In Hidden Booty Bird above 10 banana set)" # 24
    barrel_drop_bounce_balloon_1 = "Barrel Drop Bounce - Balloon #1 (No animal sign)" # 41

    krackshot_krock_clear = "Krackshot Krock - Clear"
    krackshot_krock_bonus_1 = "Krackshot Krock - Bonus #1"
    krackshot_krock_bonus_2 = "Krackshot Krock - Bonus #2"
    krackshot_krock_dk_coin = "Krackshot Krock - DK Coin"
    krackshot_krock_kong = "Krackshot Krock - KONG"
    krackshot_krock_coin_1 = "Krackshot Krock - Bear Coin #1 (At start)" # 80
    krackshot_krock_coin_2 = "Krackshot Krock - Bear Coin #2 (At start)" # 81
    krackshot_krock_balloon_1 = "Krackshot Krock - Balloon #1 (In corner)" # 79
    krackshot_krock_bananas_1 = "Krackshot Krock - Banana Bunch #1 (Near bonus #1)" # 72
    krackshot_krock_bananas_2 = "Krackshot Krock - Banana Bunch #2 (Above cauldron)" # 57
    krackshot_krock_coin_3 = "Krackshot Krock - Bear Coin #3 (Above O)" # 59
    krackshot_krock_coin_4 = "Krackshot Krock - Bear Coin #4 (Below red Buzz)" # 49
    krackshot_krock_coin_5 = "Krackshot Krock - Bear Coin #5 (Below red Buzz)" # 47
    krackshot_krock_bananas_3 = "Krackshot Krock - Banana Bunch #3 (Near bonus #2)" # 19
    krackshot_krock_bananas_4 = "Krackshot Krock - Banana Bunch #4 (Above triple cauldron)" # 35
    krackshot_krock_bananas_5 = "Krackshot Krock - Banana Bunch #5 (Near circling red Buzz)" # 38

    lemguin_lunge_clear = "Lemguin Lunge - Clear"
    lemguin_lunge_bonus_1 = "Lemguin Lunge - Bonus #1"
    lemguin_lunge_bonus_2 = "Lemguin Lunge - Bonus #2"
    lemguin_lunge_dk_coin = "Lemguin Lunge - DK Coin"
    lemguin_lunge_kong = "Lemguin Lunge - KONG"
    lemguin_lunge_coin_1 = "Lemguin Lunge - Bear Coin #1 (Below O)" # 12
    lemguin_lunge_bananas_1 = "Lemguin Lunge - Banana Bunch #1 (Near a Lemguin exit)" # 28
    lemguin_lunge_coin_2 = "Lemguin Lunge - Bear Coin #2 (Near N)" # 36

    buzzer_barrage_clear = "Buzzer Barrage - Clear"
    buzzer_barrage_bonus_1 = "Buzzer Barrage - Bonus #1"
    buzzer_barrage_bonus_2 = "Buzzer Barrage - Bonus #2"
    buzzer_barrage_dk_coin = "Buzzer Barrage - DK Coin"
    buzzer_barrage_kong = "Buzzer Barrage - KONG"
    buzzer_barrage_balloon_1 = "Buzzer Barrage - Balloon #1 (Cache at start)" # 0
    buzzer_barrage_coin_1 = "Buzzer Barrage - Bear Coin #1 (In a Booty Bird at the start)" # 5 
    buzzer_barrage_bananas_1 = "Buzzer Barrage - Banana Bunch #1 (Near bonus #1 exit)" # 21
    buzzer_barrage_bananas_2 = "Buzzer Barrage - Banana Bunch #2 (Below Kopter)" # 34
    buzzer_barrage_bananas_3 = "Buzzer Barrage - Banana Bunch #3 (In a dead end after triple Buzzes)" # 29
    buzzer_barrage_bananas_4 = "Buzzer Barrage - Banana Bunch #4 (In a dead end after triple Buzzes)" # 30
    buzzer_barrage_bananas_5 = "Buzzer Barrage - Banana Bunch #5 (In a dead end after circling Buzzes)" # 52
    buzzer_barrage_bananas_6 = "Buzzer Barrage - Banana Bunch #6 (In a dead end after circling Buzzes)" # 51
    buzzer_barrage_bananas_7 = "Buzzer Barrage - Banana Bunch #7 (Before red buzz trio before G)" # 75
    buzzer_barrage_coin_2 = "Buzzer Barrage - Bear Coin #2 (In a corner near circling Buzzes)" # 53
    buzzer_barrage_coin_3 = "Buzzer Barrage - Bear Coin #3 (Between two Buzzes)" # 92
    buzzer_barrage_coin_4 = "Buzzer Barrage - Bear Coin #4 (Below Kopter)" # 98
    buzzer_barrage_coin_5 = "Buzzer Barrage - Bear Coin #5 (No animal sign)" # 120
    buzzer_barrage_balloon_2 = "Buzzer Barrage - Balloon #2 (Above exit)" # 125
    buzzer_barrage_balloon_3 = "Buzzer Barrage - Balloon #3 (Cache below no animal sign)" # 4
    buzzer_barrage_coin_6 = "Buzzer Barrage - Bear Coin #6 (Above exit)" # 126
    buzzer_barrage_coin_7 = "Buzzer Barrage - Bear Coin #6 (Cache near exit)" # 3

    kongfused_cliffs_clear = "Kong-Fused Cliffs - Clear"
    kongfused_cliffs_bonus_1 = "Kong-Fused Cliffs - Bonus #1"
    kongfused_cliffs_bonus_2 = "Kong-Fused Cliffs - Bonus #2"
    kongfused_cliffs_dk_coin = "Kong-Fused Cliffs - DK Coin"
    kongfused_cliffs_kong = "Kong-Fused Cliffs - KONG"
    kongfused_cliffs_coin_1 = "Kong-Fused Cliffs - Bear Coin #1 (Next to K)" # 15
    kongfused_cliffs_coin_2 = "Kong-Fused Cliffs - Bear Coin #2 (Above Barrel Kannon)" # 71
    kongfused_cliffs_coin_3 = "Kong-Fused Cliffs - Bear Coin #3 (In hidden passage)" # 79
    kongfused_cliffs_coin_4 = "Kong-Fused Cliffs - Bear Coin #4 (In a detour before N)" # 3
    kongfused_cliffs_coin_5 = "Kong-Fused Cliffs - Bear Coin #5 (In a detour before N)" # 2
    kongfused_cliffs_bananas_1 = "Kong-Fused Cliffs - Banana Bunch #2 (Near G)" # 7
    kongfused_cliffs_bananas_2 = "Kong-Fused Cliffs - Banana Bunch #3 (Near G)" # 5

    floodlit_fish_clear = "Floodlit Fish - Clear"
    floodlit_fish_bonus_1 = "Floodlit Fish - Bonus #1"
    floodlit_fish_bonus_2 = "Floodlit Fish - Bonus #2"
    floodlit_fish_dk_coin = "Floodlit Fish - DK Coin"
    floodlit_fish_kong = "Floodlit Fish - KONG"
    floodlit_fish_bananas_1 = "Floodlit Fish - Banana Bunch #1 (At start)" # 0
    floodlit_fish_bananas_2 = "Floodlit Fish - Banana Bunch #2 (In Lurchin cluster)" # 43
    floodlit_fish_coin_1 = "Floodlit Fish - Bear Coin #1 (Near checkpoint)" # 48
    floodlit_fish_bananas_3 = "Floodlit Fish - Banana Bunch #3 (Behind two Red Kocos)" # 59
    floodlit_fish_bananas_4 = "Floodlit Fish - Banana Bunch #4 (Below Gleaming Bream)" # 58
    floodlit_fish_coin_2 = "Floodlit Fish - Bear Coin #2 (Inside Bounty Bass)" # 62
    floodlit_fish_bananas_5 = "Floodlit Fish - Banana Bunch #5 (In second branching path, left)" # 77
    floodlit_fish_bananas_6 = "Floodlit Fish - Banana Bunch #6 (In third branching path, right)" # 94
    floodlit_fish_coin_3 = "Floodlit Fish - Bear Coin #3 (Near exit)" # 96
    floodlit_fish_bananas_7 = "Floodlit Fish - Banana Bunch #7 (Near exit)" # 105
    floodlit_fish_bananas_8 = "Floodlit Fish - Banana Bunch #8 (No animal sign)" # 106

    pot_hole_panic_clear = "Pot Hole Panic - Clear"
    pot_hole_panic_bonus_1 = "Pot Hole Panic - Bonus #1"
    pot_hole_panic_bonus_2 = "Pot Hole Panic - Bonus #2"
    pot_hole_panic_dk_coin = "Pot Hole Panic - DK Coin"
    pot_hole_panic_kong = "Pot Hole Panic - KONG"
    pot_hole_panic_bananas_1 = "Pot Hole Panic - Banana Bunch #1 (In dead end near start)" # 3
    pot_hole_panic_bananas_2 = "Pot Hole Panic - Banana Bunch #2 (In dead end near start)" # 4
    pot_hole_panic_coin_1 = "Pot Hole Panic - Bear Coin #1 (Near circling Kopters)" # 12
    pot_hole_panic_bananas_3 = "Pot Hole Panic - Banana Bunch #3 (Near Enguarde box)" # 16
    pot_hole_panic_bananas_4 = "Pot Hole Panic - Banana Bunch #4 (In Bounty Bass near Enguarde box)" # 26
    pot_hole_panic_bananas_5 = "Pot Hole Panic - Banana Bunch #5 (Above Bounty Bass)" # 32
    pot_hole_panic_bananas_6 = "Pot Hole Panic - Banana Bunch #6 (Near Lurchin cluster)" # 34
    pot_hole_panic_bananas_7 = "Pot Hole Panic - Banana Bunch #7 (Behind Ellie Box)" # 44
    pot_hole_panic_bananas_8 = "Pot Hole Panic - Banana Bunch #8 (Behind Ellie Box)" # 43
    pot_hole_panic_coin_2 = "Pot Hole Panic - Bear Coin #2 (Above Kopter)" # 52
    pot_hole_panic_coin_3 = "Pot Hole Panic - Bear Coin #3 (Below N)" # 59
    pot_hole_panic_bananas_9 = "Pot Hole Panic - Banana Bunch #9 (Below N)" # 60
    pot_hole_panic_coin_4 = "Pot Hole Panic - Bear Coin #4 (Below N)" # 61
    pot_hole_panic_bananas_10 = "Pot Hole Panic - Banana Bunch #10 (In Booty Bird after Squitter box)" # 71
    pot_hole_panic_bananas_11 = "Pot Hole Panic - Banana Bunch #11 (No animal sign)" # 78

    ropey_rumpus_clear = "Ropey Rumpus - Clear"
    ropey_rumpus_bonus_1 = "Ropey Rumpus - Bonus #1"
    ropey_rumpus_bonus_2 = "Ropey Rumpus - Bonus #2"
    ropey_rumpus_dk_coin = "Ropey Rumpus - DK Coin"
    ropey_rumpus_kong = "Ropey Rumpus - KONG"
    ropey_rumpus_coin_1 = "Ropey Rumpus - Bear Coin #1 (Cache at start)" # 0
    ropey_rumpus_coin_2 = "Ropey Rumpus - Bear Coin #2 (At start)" # 2
    ropey_rumpus_bananas_1 = "Ropey Rumpus - Banana Bunch #1 (At start)" # 6
    ropey_rumpus_coin_3 = "Ropey Rumpus - Bear Coin #3 (Next to K)" # 19
    ropey_rumpus_bananas_2 = "Ropey Rumpus - Banana Bunch #2 (Above green Buzz near K)" # 28
    ropey_rumpus_coin_4 = "Ropey Rumpus - Bear Coin #4 (Next to O)" # 38
    ropey_rumpus_coin_5 = "Ropey Rumpus - Bear Coin #5 (Next to O)" # 39
    ropey_rumpus_bananas_3 = "Ropey Rumpus - Banana Bunch #3 (Next to red & green Buzz pair)" # 45
    ropey_rumpus_coin_6 = "Ropey Rumpus - Bear Coin #6 (Next to red & green Buzz pair)" # 44
    ropey_rumpus_coin_7 = "Ropey Rumpus - Bear Coin #7 (Next to red Buzz with a circling green Buzz)" # 48
    ropey_rumpus_bananas_4 = "Ropey Rumpus - Banana Bunch #4 (Next to a pair of circling green Buzzes)" # 54
    ropey_rumpus_balloon_1 = "Ropey Rumpus - Balloon #1 (In branching path)" # 71
    ropey_rumpus_bananas_5 = "Ropey Rumpus - Banana Bunch #5 (Above branching path)" # 73
    ropey_rumpus_bananas_6 = "Ropey Rumpus - Banana Bunch #6 (Above branching path)" # 72
    ropey_rumpus_bananas_7 = "Ropey Rumpus - Banana Bunch #7 (Next to circling green Buzzes after N)" # 91
    ropey_rumpus_bananas_8 = "Ropey Rumpus - Banana Bunch #8 (Next to circling green Buzzes after N)" # 90
    ropey_rumpus_bananas_9 = "Ropey Rumpus - Banana Bunch #9 (In hidden upper path)" # 102
    ropey_rumpus_balloon_2 = "Ropey Rumpus - Balloon #2 (In hidden upper path)" # 103
    ropey_rumpus_coin_8 = "Ropey Rumpus - Bear Coin #8 (In hidden upper path)" # 104
    ropey_rumpus_bananas_10 = "Ropey Rumpus - Banana Bunch #10 (Below hidden upper path)" # 109

    konveyor_rope_klash_clear = "Konveyor Rope Klash - Clear"
    konveyor_rope_klash_bonus_1 = "Konveyor Rope Klash - Bonus #1"
    konveyor_rope_klash_bonus_2 = "Konveyor Rope Klash - Bonus #2"
    konveyor_rope_klash_dk_coin = "Konveyor Rope Klash - DK Coin"
    konveyor_rope_klash_kong = "Konveyor Rope Klash - KONG"
    konveyor_rope_klash_coin_1 = "Konveyor Rope Klash - Bear Coin #1 (At start)" # 3
    konveyor_rope_klash_coin_2 = "Konveyor Rope Klash - Bear Coin #2 (Before checkpoint)" # 30
    konveyor_rope_klash_coin_3 = "Konveyor Rope Klash - Bear Coin #3 (Cache near rolling Bristles)" # 0
    konveyor_rope_klash_balloon_1 = "Konveyor Rope Klash - Balloon #1 (In small conveyor)" # 69
    konveyor_rope_klash_balloon_2 = "Konveyor Rope Klash - Balloon #2 (Cache near Koin)" # 1

    creepy_caverns_clear = "Creepy Caverns - Clear"
    creepy_caverns_bonus_1 = "Creepy Caverns - Bonus #1"
    creepy_caverns_bonus_2 = "Creepy Caverns - Bonus #2"
    creepy_caverns_dk_coin = "Creepy Caverns - DK Coin"
    creepy_caverns_kong = "Creepy Caverns - KONG"
    creepy_caverns_bananas_1 = "Creepy Caverns - Banana Bunch #1 (In Booty Bird at the start)" # 3
    creepy_caverns_coin_1 = "Creepy Caverns - Bear Coin #1 (Cache near first ascent)" # 1
    creepy_caverns_coin_2 = "Creepy Caverns - Bear Coin #2 (In secret ghost barrel trap before O)" # 43
    creepy_caverns_coin_3 = "Creepy Caverns - Bear Coin #3 (In secret ghost barrel trap before O)" # 44
    creepy_caverns_bananas_2 = "Creepy Caverns - Banana Bunch #2 (Near bonus #1 exit)" # 47
    creepy_caverns_coin_4 = "Creepy Caverns - Bear Coin #4 (No animal sign)" # 84
    creepy_caverns_coin_5 = "Creepy Caverns - Bear Coin #5 (Next to Krumples pair)" # 76
    creepy_caverns_coin_6 = "Creepy Caverns - Bear Coin #6 (Above G)" # 114
    creepy_caverns_balloon_1 = "Creepy Caverns - Balloon #1 (Cache next to Krumples pair)" # 0

    lightning_look_out_clear = "Lightning Look-Out - Clear"
    lightning_look_out_bonus_1 = "Lightning Look-Out - Bonus #1"
    lightning_look_out_bonus_2 = "Lightning Look-Out - Bonus #2"
    lightning_look_out_dk_coin = "Lightning Look-Out - DK Coin"
    lightning_look_out_kong = "Lightning Look-Out - KONG"
    lightning_look_out_balloon_1 = "Lightning Look-Out - Balloon #1 (Near start above Buzz trio)" # 3
    lightning_look_out_coin_1 = "Lightning Look-Out - Bear Coin #1 (Cache near trapped Knik-Knaks)" # 0
    lightning_look_out_coin_2 = "Lightning Look-Out - Bear Coin #2 (Above Buzz duo)" # 16
    lightning_look_out_bananas_1 = "Lightning Look-Out - Banana Bunch #1 (Behind Buzz pair)" # 21
    lightning_look_out_coin_3 = "Lightning Look-Out - Bear Coin #3 (Above right buzz next to N)" # 47
    lightning_look_out_balloon_2 = "Lightning Look-Out - Balloon #2 (Cache near end)" # 1

    koindozer_klamber_clear = "Koindozer Klamber - Clear"
    koindozer_klamber_bonus_1 = "Koindozer Klamber - Bonus #1"
    koindozer_klamber_bonus_2 = "Koindozer Klamber - Bonus #2"
    koindozer_klamber_dk_coin = "Koindozer Klamber - DK Coin"
    koindozer_klamber_kong = "Koindozer Klamber - KONG"
    koindozer_klamber_coin_1 = "Koindozer Klamber - Bear Coin #1 (Below O)" # 13
    koindozer_klamber_coin_2 = "Koindozer Klamber - Bear Coin #2 (Cache before Bazuka)" # 0
    koindozer_klamber_coin_3 = "Koindozer Klamber - Bear Coin #3 (Below checkpoint)" # 24
    koindozer_klamber_bananas_1 = "Koindozer Klamber - Banana Bunch #1 (Above Koindozer)" # 33
    koindozer_klamber_balloon_1 = "Koindozer Klamber - Balloon #1 (Cache below DK Barrel)" # 1

    poisonous_pipeline_clear = "Poisonous Pipeline - Clear"
    poisonous_pipeline_bonus_1 = "Poisonous Pipeline - Bonus #1"
    poisonous_pipeline_bonus_2 = "Poisonous Pipeline - Bonus #2"
    poisonous_pipeline_dk_coin = "Poisonous Pipeline - DK Coin"
    poisonous_pipeline_kong = "Poisonous Pipeline - KONG"
    poisonous_pipeline_coin_1 = "Poisonous Pipeline - Bear Coin #1 (Above water near start)" # 9
    poisonous_pipeline_bananas_1 = "Poisonous Pipeline - Banana Bunch #1 (Above Lurchin pair)" # 18
    poisonous_pipeline_bananas_2 = "Poisonous Pipeline - Banana Bunch #2 (Above Lurchin pair)" # 17
    poisonous_pipeline_coin_2 = "Poisonous Pipeline - Bear Coin #2 (Near O)" # 39
    poisonous_pipeline_balloon_1 = "Poisonous Pipeline - Balloon #1 (No animal sign)" # 71

    stampede_sprint_clear = "Stampede Sprint - Clear"
    stampede_sprint_bonus_1 = "Stampede Sprint - Bonus #1"
    stampede_sprint_bonus_2 = "Stampede Sprint - Bonus #2"
    stampede_sprint_bonus_3 = "Stampede Sprint - Bonus #3"
    stampede_sprint_dk_coin = "Stampede Sprint - DK Coin"
    stampede_sprint_kong = "Stampede Sprint - KONG"
    stampede_sprint_coin_1 = "Stampede Sprint - Bear Coin #1 (During sprint)" # 40
    stampede_sprint_coin_2 = "Stampede Sprint - Bear Coin #2 (Before no Ellie sign)" # 55

    criss_kross_cliffs_clear = "Criss Kross Cliffs - Clear"
    criss_kross_cliffs_bonus_1 = "Criss Kross Cliffs - Bonus #1"
    criss_kross_cliffs_bonus_2 = "Criss Kross Cliffs - Bonus #2"
    criss_kross_cliffs_dk_coin = "Criss Kross Cliffs - DK Coin"
    criss_kross_cliffs_kong = "Criss Kross Cliffs - KONG"
    criss_kross_cliffs_bananas_1 = "Criss Kross Cliffs - Banana Bunch #1 (At start)" # 79
    criss_kross_cliffs_coin_1 = "Criss Kross Cliffs - Bear Coin #1 (In open area after O)" # 50
    criss_kross_cliffs_bananas_2 = "Criss Kross Cliffs - Banana Bunch #2 (In open area after O)" # 49
    criss_kross_cliffs_coin_2 = "Criss Kross Cliffs - Bear Coin #2 (Below N)" # 36
    criss_kross_cliffs_coin_3 = "Criss Kross Cliffs - Bear Coin #3 (Cache near bonus #2)" # 0
    criss_kross_cliffs_coin_4 = "Criss Kross Cliffs - Bear Coin #4 (Cache near bonus #2)" # 2
    criss_kross_cliffs_bananas_3 = "Criss Kross Cliffs - Banana Bunch #3 (Upper left after Bonus #2 exit)" # 10
    criss_kross_cliffs_balloon_1 = "Criss Kross Cliffs - Balloon #1 (Near end)" # 4
    criss_kross_cliffs_balloon_2 = "Criss Kross Cliffs - Balloon #2 (Cache below goal)" # 1

    tyrant_twin_tussle_clear = "Tyrant Twin Tussle - Clear"
    tyrant_twin_tussle_bonus_1 = "Tyrant Twin Tussle - Bonus #1"
    tyrant_twin_tussle_bonus_2 = "Tyrant Twin Tussle - Bonus #2"
    tyrant_twin_tussle_bonus_3 = "Tyrant Twin Tussle - Bonus #3"
    tyrant_twin_tussle_dk_coin = "Tyrant Twin Tussle - DK Coin"
    tyrant_twin_tussle_kong = "Tyrant Twin Tussle - KONG"
    tyrant_twin_tussle_coin_1 = "Tyrant Twin Tussle - Bear Coin #1 (In Booty Bird near Squitter barrel)" # 11
    tyrant_twin_tussle_balloon_1 = "Tyrant Twin Tussle - Balloon #1 (Near K)" # 17
    tyrant_twin_tussle_balloon_2 = "Tyrant Twin Tussle - Balloon #2 (Cache in bottom path)" # 0
    tyrant_twin_tussle_coin_2 = "Tyrant Twin Tussle - Bear Coin #2 (In top path)" # 23
    tyrant_twin_tussle_bananas_1 = "Tyrant Twin Tussle - Banana Bunch #1 (In top path)" # 24
    tyrant_twin_tussle_coin_3 = "Tyrant Twin Tussle - Bear Coin #3 (In top path)" # 25
    tyrant_twin_tussle_coin_4 = "Tyrant Twin Tussle - Bear Coin #4 (No animal sign)" # 42
    tyrant_twin_tussle_bananas_2 = "Tyrant Twin Tussle - Banana Bunch #2 (Left to DK Barrel after checkpoint)" # 50
    tyrant_twin_tussle_coin_5 = "Tyrant Twin Tussle - Bear Coin #5 (In top path near end)" # 79
    tyrant_twin_tussle_coin_6 = "Tyrant Twin Tussle - Bear Coin #6 (In top path near end)" # 80
    tyrant_twin_tussle_bananas_3 = "Tyrant Twin Tussle - Banana Bunch #3 (In top path near end)" # 81

    swoopy_salvo_clear = "Swoopy Salvo - Clear"
    swoopy_salvo_bonus_1 = "Swoopy Salvo - Bonus #1"
    swoopy_salvo_bonus_2 = "Swoopy Salvo - Bonus #2"
    swoopy_salvo_bonus_3 = "Swoopy Salvo - Bonus #3"
    swoopy_salvo_dk_coin = "Swoopy Salvo - DK Coin"
    swoopy_salvo_kong = "Swoopy Salvo - KONG"
    swoopy_salvo_bananas_1 = "Swoopy Salvo - Banana Bunch #1 (In Booty Bird)" # 84
    swoopy_salvo_coin_1 = "Swoopy Salvo - Bear Coin #1 (Inside circling red Buzzes)" # 70
    swoopy_salvo_bananas_2 = "Swoopy Salvo - Banana Bunch #2 (Before an entrance blocking Buzz)" # 63

    rocket_rush_clear = "Rocket Rush - Clear"
    rocket_rush_dk_coin = "Rocket Rush - DK Coin"
    rocket_rush_bananas_1 = "Rocket Rush - Banana Bunch #1 (Falling section)" # 6
    rocket_rush_coin_1 = "Rocket Rush - Bear Coin #1 (Rising section after N, left side)" # 43
    rocket_rush_bananas_2 = "Rocket Rush - Banana Bunch #2 (Rising section in a narrow corridor, left)" # 44
    rocket_rush_bananas_3 = "Rocket Rush - Banana Bunch #3 (Rising section in a narrow corridor, right)" # 45
    rocket_rush_coin_2 = "Rocket Rush - Bear Coin #2 (Rising section in branching path, right side)" # 47
    rocket_rush_coin_3 = "Rocket Rush - Bear Coin #3 (Rising section in branching path, right side)" # 46
    rocket_rush_coin_4 = "Rocket Rush - Bear Coin #4 (Rising section in semi-open area)" # 48

    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)


class Regions(StrEnum):
    northern_kremisphere_south = "Northern Kremisphere - South"
    northern_kremisphere_center = "Northern Kremisphere - Center"
    northern_kremisphere_north = "Northern Kremisphere - North"
    northern_kremisphere_kore = "Northern Kremisphere - Kore"
    northern_kremisphere_flying = "Northern Kremisphere - Flying"

    lake_orangatanga = "Lake Orangatanga"
    kremwood_forest = "Kremwood Forest"
    cotton_top_cove = "Cotton-Top Cove"
    mekanos = "Mekanos"
    k3 = "K3"
    razor_ridge = "Razor Ridge"
    kaos_kore = "Kaos Kore"
    krematoa = "Krematoa"

    belchas_barn_level = "Belcha's Barn: Level"
    arichs_ambush_level = "Arich's Ambush: Level"
    squirt_showdown_level = "Squirt's Showdown: Level"
    kaos_karnage_level = "KAOS Karnage: Level"
    bleaks_house_level = "Bleak's House: Level"
    barbos_barrier_level = "Barbos's Barrier: Level"
    kastle_kaos_level = "Kastle KAOS: Level"
    knautilus_level = "Knautilus: Level"
    lakeside_limbo_level = "Lakeside Limbo: Level"
    doorstop_dash_level = "Doorstop Dash: Level"
    tidal_trouble_level = "Tidal Trouble: Level"
    skiddas_row_level = "Skidda's Row: Level"
    murky_mill_level = "Murky Mill: Level"
    barrel_shield_bust_up_level = "Barrel Shield Bust-Up: Level"
    riverside_race_level = "Riverside Race: Level"
    squeals_on_wheels_level = "Squeals on Wheels: Level"
    springing_spiders_level = "Springin' Spiders: Level"
    bobbing_barrel_brawl_level = "Bobbing Barrel Brawl: Level"
    bazzas_blockade_level = "Bazza's Blockade: Level"
    rocket_barrel_ride_level = "Rocket Barrel Ride: Level"
    kreeping_klasps_level = "Kreeping Klasps: Level"
    tracker_barrel_trek_level = "Tracker Barrel Trek: Level"
    fish_food_frenzy_level = "Fish Food Frenzy: Level"
    fireball_frenzy_level = "Fire-Ball Frenzy: Level"
    demolition_drain_pipe_level = "Demolition Drain-Pipe: Level"
    ripsaw_rage_level = "Ripsaw Rage: Level"
    blazing_bazukas_level = "Blazing Bazukas: Level"
    low_g_labyrinth_level = "Low-G Labyrinth: Level"
    krevice_kreepers_level = "Krevice Kreepers: Level"
    tearaway_toboggan_level = "Tearaway Toboggan: Level"
    barrel_drop_bounce_level = "Barrel Drop Bounce: Level"
    krackshot_krock_level = "Krackshot Krock: Level"
    lemguin_lunge_level = "Lemguin Lunge: Level"
    buzzer_barrage_level = "Buzzer Barrage: Level"
    kongfused_cliffs_level = "Kong-Fused Cliffs: Level"
    floodlit_fish_level = "Floodlit Fish: Level"
    pot_hole_panic_level = "Pot Hole Panic: Level"
    ropey_rumpus_level = "Ropey Rumpus: Level"
    konveyor_rope_klash_level = "Konveyor Rope Klash: Level"
    creepy_caverns_level = "Creepy Caverns: Level"
    lightning_look_out_level = "Lightning Look-Out: Level"
    koindozer_klamber_level = "Koindozer Klamber: Level"
    poisonous_pipeline_level = "Poisonous Pipeline: Level"
    stampede_sprint_level = "Stampede Sprint: Level"
    criss_kross_cliffs_level = "Criss Kross Cliffs: Level"
    tyrant_twin_tussle_level = "Tyrant Twin Tussle: Level"
    swoopy_salvo_level = "Swoopy Salvo: Level"
    rocket_rush_level = "Rocket Rush: Level"

    belchas_barn_map = "Belcha's Barn: Map"
    arichs_ambush_map = "Arich's Ambush: Map"
    squirt_showdown_map = "Squirt's Showdown: Map"
    kaos_karnage_map = "KAOS Karnage: Map"
    bleaks_house_map = "Bleak's House: Map"
    barbos_barrier_map = "Barbos's Barrier: Map"
    kastle_kaos_map = "Kastle KAOS: Map"
    knautilus_map = "Knautilus: Map"
    lakeside_limbo_map = "Lakeside Limbo: Map"
    doorstop_dash_map = "Doorstop Dash: Map"
    tidal_trouble_map = "Tidal Trouble: Map"
    skiddas_row_map = "Skidda's Row: Map"
    murky_mill_map = "Murky Mill: Map"
    barrel_shield_bust_up_map = "Barrel Shield Bust-Up: Map"
    riverside_race_map = "Riverside Race: Map"
    squeals_on_wheels_map = "Squeals on Wheels: Map"
    springing_spiders_map = "Springin' Spiders: Map"
    bobbing_barrel_brawl_map = "Bobbing Barrel Brawl: Map"
    bazzas_blockade_map = "Bazza's Blockade: Map"
    rocket_barrel_ride_map = "Rocket Barrel Ride: Map"
    kreeping_klasps_map = "Kreeping Klasps: Map"
    tracker_barrel_trek_map = "Tracker Barrel Trek: Map"
    fish_food_frenzy_map = "Fish Food Frenzy: Map"
    fireball_frenzy_map = "Fire-Ball Frenzy: Map"
    demolition_drain_pipe_map = "Demolition Drain-Pipe: Map"
    ripsaw_rage_map = "Ripsaw Rage: Map"
    blazing_bazukas_map = "Blazing Bazukas: Map"
    low_g_labyrinth_map = "Low-G Labyrinth: Map"
    krevice_kreepers_map = "Krevice Kreepers: Map"
    tearaway_toboggan_map = "Tearaway Toboggan: Map"
    barrel_drop_bounce_map = "Barrel Drop Bounce: Map"
    krackshot_krock_map = "Krackshot Krock: Map"
    lemguin_lunge_map = "Lemguin Lunge: Map"
    buzzer_barrage_map = "Buzzer Barrage: Map"
    kongfused_cliffs_map = "Kong-Fused Cliffs: Map"
    floodlit_fish_map = "Floodlit Fish: Map"
    pot_hole_panic_map = "Pot Hole Panic: Map"
    ropey_rumpus_map = "Ropey Rumpus: Map"
    konveyor_rope_klash_map = "Konveyor Rope Klash: Map"
    creepy_caverns_map = "Creepy Caverns: Map"
    lightning_look_out_map = "Lightning Look-Out: Map"
    koindozer_klamber_map = "Koindozer Klamber: Map"
    poisonous_pipeline_map = "Poisonous Pipeline: Map"
    stampede_sprint_map = "Stampede Sprint: Map"
    criss_kross_cliffs_map = "Criss Kross Cliffs: Map"
    tyrant_twin_tussle_map = "Tyrant Twin Tussle: Map"
    swoopy_salvo_map = "Swoopy Salvo: Map"
    rocket_rush_map = "Rocket Rush: Map"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)

class Events(StrEnum):
    k_rool_at_kore = "Defeated K. Rool at Kore"
    k_rool_at_knautilus = "Defeated K. Rool at Knautilus"

    lake_level = "Cleared Lake Orangatanga Level"
    forest_level = "Cleared Kremwood Forest Level"
    cove_level = "Cleared Cotton-Top Cove Level"
    mekanos_level = "Cleared Mekanos Level"
    k3_level = "Cleared K3 Level"
    ridge_level = "Cleared Razor Ridge Level"
    kore_level = "Cleared Kaos Kore Level"
    krematoa_level = "Cleared Krematoa Level"

    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)
    
from .data.Rules import *

from BaseClasses import Item, Entrance, EntranceType, Region
from .Options import PhantomHourglassOptions
from .data.Entrances import ENTRANCES
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .__init__ import PhantomHourglassWorld

def make_overworld_logic(world: "PhantomHourglassWorld"):
    required_rupees = world.required_rupees
    overworld_logic = [

        # Randomized start
        ["Menu", "Mercay SW", False, None],

        # ====== Mercay Island ==============

        ["Mercay SW", "Mercay SW Dig Spot", False, has_shovel],
        ["Oshus' House", "Oshus Gem", False, oshus_gem],
        ["Oshus' House", "Oshus Phantom Blade", False, has_phantom_blade & has_ph],
        ["Oshus Phantom Blade", "Oshus Gem", False, None],
        ["Mercay SW", "Mercay SW Bridge", True, None],
        ["Mercay SW", "Oshus' House", True, None],
        ["Mercay SW", "Apricot's House", True, None],
        ["Mercay SW", "Sword Cave", True, None],
        ["Mercay SW", "Mercay NW Chus", True, None],

        ["Mercay SW Bridge", "Mercay SE", True, None],
        ["Mercay SE", "Tuzi's House", True, None],
        ["Mercay SE", "Milk Bar", True, None],
        ["Mercay SE", "Mercay Shop", True, None],
        ["Mercay Shop", "Island Shop", False, None],
        ["Mercay SE", "Mercay SE Shipyard", False, Has("_beat_tof")  | open_post_dungeon],
            ["Mercay SE Shipyard", "Shipyard", False, Has("_beat_tof") | open_post_dungeon],
            ["Shipyard", "Mercay SE Shipyard", False, None],
            ["Mercay SE Shipyard", "Mercay SE", False, None],
        ["Mercay SE", "Mercay SE Treasure Teller", False, has_courage_crest],
            ["Mercay SE Treasure Teller", "Treasure Teller", False, has_courage_crest],
            ["Treasure Teller", "Mercay SE Treasure Teller", False, None],
            ["Mercay SE Treasure Teller", "Mercay SE", False, None],
        ["Mercay SE", "Mercay SE Ojibe", False, has_courage_crest],
        ["Mercay SE", "Mercay NE", True, None],
        ["Mercay SE Ledge", "Mercay SE", False, None],

        ["Mercay NW Chus", "Mercay NW Bamboo", True, can_cut_bamboo],
        ["Mercay NW Temple", "Eye Bridge Cave North", False, has_explosives],
        ["Eye Bridge Cave North", "Mercay NW Temple", False, None],
        ["Eye Bridge Cave North", "Eye Bridge Cave South", False, has_bow],
        ["Eye Bridge Cave South", "Mercay NE Ledge", True, None],
        ["Mercay NW Temple", "TotOK Lobby", True, None],

        ["Mercay NE", "Long Bridge Cave", False, has_explosives],
        ["Long Bridge Cave", "Mercay NE", False, None],
        ["Long Bridge Cave", "Mercay NW Freedle Island", True, None],
        ["Mercay NW Freedle Island", "Mercay NE", False, None],
        ["Long Bridge Cave", "Long Bridge Cave Chest", False, has_beam_range],
        ["Mercay NW Freedle Island", "Mercay NW Freedle Gift", False, has_sea_chart("SE")],
        ["Mercay NE", "Mercay NW Temple", True, None],
        ["Mercay NE Ledge", "Mercay NE", False, None],
        ["Mercay NE Ledge", "Mercay SE Ledge", True, None],

        ["Mercay NW Temple", "Mercay NW OoB High", False, sword_scroll_clip],
        ["Mercay NW OoB High", "Mercay NW Temple", False, None],
        ["Mercay NW OoB High", "Mercay NW OoB Low", False, None],
        ["Mercay NW OoB Low", "Mercay NW Chus", False, None],
        ["Mercay NW OoB Low", "Mercay NW Bamboo", False, None],
        ["Mercay NW OoB High", "Mercay NE OoB", True, None],
        ["Mercay NW OoB High", "Mercay SW OoB High", True, None],
        ["Mercay NW OoB High", "Mercay SW OoB East", True, None],
        ["Mercay NW OoB Low", "Mercay SW OoB Low", True, None],

        ["Mercay SW OoB High", "Mercay SW OoB Low", False, None],
        ["Mercay SW OoB Low", "Mercay SW", False, None],
        ["Mercay SW OoB East", "Mercay SW Bridge", False, None],
        ["Mercay SW OoB East", "Mercay SE OoB", True, None],

        ["Mercay SE OoB", "Mercay SE Ledge", False, None],
        ["Mercay SE OoB", "Mercay NE OoB", True, None],
        ["Mercay NE OoB", "Mercay NE Ledge", False, None],

        # ======== Mountain Passage =========

        ["Mercay NW Bamboo", "Mountain Passage 1", True, None],
        ["Mountain Passage 1", "Mountain Passage 2", False, can_reach_mp2],
        ["Mountain Passage 2 Exit", "Mountain Passage 2", False, mp2_top],
        ["Mountain Passage 1", "Mountain Passage 2 Exit", False, mp2_bypass_fore],
        ["Mountain Passage 2 Exit", "Mountain Passage 1", False, mp2_bypass],
        ["Mountain Passage 2 Exit", "Mountain Passage 3", True, None],
        ["Mountain Passage 3", "Mountain Passage Rat", False, mp_rat],
        ["Mountain Passage 3", "Mountain Passage 4", False, mp3],
        ["Mountain Passage 4", "Mountain Passage 3", False, mp3_back],
        ["Mountain Passage 4", "Mercay SE", True, None],
        ["Mountain Passage 4", "Mountain Passage 1", False, hard_logic],
        ["Mountain Passage 3", "Mountain Passage 1", False, hard_logic],

        # ========== TotOK ===================
        ["TotOK Lobby", "TotOK 1F", False, totok_1f],

        ["TotOK 1F", "TotOK 1F Chest", False, totok_1f_chest],
        ["TotOK 1F", "TotOK 1F Chart", False, totok_1f_chart],
        ["TotOK 1F", "TotOK B1", False, totok_b1],

        ["TotOK B1", "TotOK B1 Key", False, totok_b1_key],
        ["TotOK B1", "TotOK B1 Phantom", False, totok_b1_phantom],
        ["TotOK B1", "TotOK B1 Bow", False, totok_b1_bow],
        ["TotOK B1", "TotOK B2", False, totok_b2],

        ["TotOK B2", "TotOK B2 Key", False, totok_b2_key],
        ["TotOK B2", "TotOK B2 Phantom", False, totok_b2_phantom],
        ["TotOK B2", "TotOK B2 Chu", False, totok_b2_chu],
        ["TotOK B2", "TotOK B3", False, totok_b3],

        ["TotOK B3", "TotOK B3 NW Chest", False, totok_b3_nw],
        ["TotOK B3", "TotOK B3 SE Chest", False, totok_b3_se],
        ["TotOK B3", "TotOK B3 SW Chest", False, totok_b3_sw],
        ["TotOK B3", "TotOK B3 Bow", False, totok_b3_bow],
        ["TotOK B3", "TotOK B3 Key", False, totok_b3_key],
        ["TotOK B3", "TotOK B3 Phantom", False, totok_b3_phantom],
        ["TotOK B3", "TotOK B3.5", False, totok_b35],
        ["TotOK B3.5", "TotOK B4", False, totok_b4],

        ["TotOK B4", "TotOK B4 Key", False, totok_b4_key],
        ["TotOK B4", "TotOK B4 Eyes", False, totok_b4_eyes],
        ["TotOK B4", "TotOK B4 Phantom", False, totok_b4_phantom],
        ["TotOK B4", "TotOK B5", False, totok_b5],
        ["TotOK B4", "TotOK B5 Alt Path", False, totok_b5_alt],

        ["TotOK B5", "TotOK B5 Chest", False, totok_b5_chest],
        ["TotOK B5", "TotOK B6", False, totok_b6],
        ["TotOK B5 Alt Path", "TotOK B5 Alt Path Chest", False, totok_b5_alt_chest],
        ["TotOK B5 Alt Path", "TotOK B6", False, totok_b6],

        ["TotOK B6", "TotOK B6 Bow", False, totok_b6_bow],
        ["TotOK B6", "TotOK B6 Phantom", False, totok_b6_phantom],
        ["TotOK B6", "TotOK B6 Crest", False, totok_b6_crest],
        ["TotOK B6", "TotOK B6 Midway", False, totok_b7],
        ["TotOK B6 Midway", "TotOK B7", False, has_spirit("Courage")],

        ["TotOK B7", "TotOK B7 Crystal", False, totok_b7_crystal],
        ["TotOK B7", "TotOK B7 Switch", False, totok_b7_switch_chest],
        ["TotOK B7", "TotOK B8", False, totok_b8],

        ["TotOK B8", "TotOK B8 Phantom", False, totok_b8_phantom],
        ["TotOK B8", "TotOK B9", False, totok_b9],
        ["TotOK B8", "TotOK B8 2 Crystals Chest", False, totok_b8_2_crystals_chest],
        ["TotOK B8", "TotOK B7 Phantom", False, totok_b7_phantom],
        ["TotOK B8", "TotOK B9 Corner Chest", False, totok_b9_corner_chest],

        ["TotOK B9", "TotOK B9 Crystal", False, totok_b9_crystal],
        ["TotOK B9", "TotOK B9 Phantom", False, totok_b9_phantom],
        ["TotOK B9", "TotOK B9 Wizzrobes", False, totok_b9_wizzrobes],

        ["TotOK B9", "TotOK B9.5", False, totok_b10],
        ["TotOK B9.5", "TotOK B10", True, None],

        ["TotOK B10", "TotOK B10 Key", False, totok_b10_key],
        ["TotOK B10", "TotOK B10 Phantom", False, totok_b10_phantom],
        ["TotOK B10", "TotOK B10 Eyes", False, totok_b10_eyes],
        ["TotOK B10", "TotOK B10 Hammer", False, totok_b10_hammer],
        ["TotOK B10", "TotOK B11", False, totok_b11],

        ["TotOK B11", "TotOK B11 Phantom", False, totok_b11_phantom],
        ["TotOK B11", "TotOK B11 Eyes", False, totok_b11_eyes],
        ["TotOK B11", "TotOK B12", False, totok_b12],

        ["TotOK B12", "TotOK B12 NW Chest", False, totok_b12_nw],
        ["TotOK B12", "TotOK B12 NE Chest", False, totok_b12_ne],
        ["TotOK B12", "TotOK B12 Phantom", False, totok_b12_phantom],
        ["TotOK B12", "TotOK B12 Gem", False, totok_b12_gem],
        ["TotOK B12", "TotOK B12 Ghost", False, totok_b12_wizzrobes],
        ["TotOK B12", "TotOK B12 Hammer", False, totok_b12_hammer],
        ["TotOK B12", "TotOK B13", False, totok_b13],

        ["TotOK B13", "TotOK B13 Chest", False, totok_b13_chest],
        ["TotOK B13", "TotOK B14 South", False, totok_b13_door],
        ["TotOK B14 South", "TotOK B14", False, None],
        ["TotOK Lobby", "TotOK B14", False, Filtered(has_metals, options=bellum_access_warp)],
        # Bellum
        ["TotOK B14", "Bellum", False, has_metals],
        ["Bellum", "Ghost Ship Fight", False, can_defeat_bellum],
        ["Ghost Ship Fight", "Bellumbeck", False, has_cannon],

        # ============ Shops ====================

        ["Island Shop", "Island Shop Power Gem", False, has_restock_rupees(required_rupees, 4000)],
        ["Island Shop", "Island Shop Quiver", False, has_restock_rupees(required_rupees, 3000) & has_bow],
        ["Island Shop", "Island Shop Bombchu Bag", False, has_restock_rupees(required_rupees, 2000) & has_bow & has_chus],
        ["Island Shop", "Island Shop Heart Container", False, has_rupees(required_rupees) & has_bow & has_chus],

        ["Mercay Shop", "Mercay Shop Buy", False, has_rupees(required_rupees)],
        ["Molida Shop", "Molida Shop Buy", False, has_rupees(required_rupees)],
        ["Goron Shop", "Goron Shop Buy", False, has_rupees(required_rupees)],

        ["Mercay Shop Buy", "Mercay Shop Bombs", False, has_bombs],
        ["Molida Shop Buy", "Molida Shop Bombs", False, has_bombs],
        ["Molida Shop Buy", "Molida Shop Arrows", False, has_bow],
        ["Goron Shop Buy", "Goron Shop Arrows", False, has_bow],
        ["Goron Shop Buy", "Goron Shop Chus", False, has_chus],

        ["Mercay Shop Buy", "Mercay Shop Shield", False, shop_shield(required_rupees, 150)],
        ["Molida Shop Buy", "Molida Shop Shield", False, shop_shield(required_rupees, 150)],
        ["Goron Shop Buy", "Goron Shop Shield", False, shop_shield(required_rupees, 150)],

        ["SW Ocean East", "Beedle", False, None],
        ["SW Ocean West", "Beedle", False, None],
        ["NW Ocean", "Beedle", False, None],
        ["SE Ocean", "Beedle", False, None],
        ["NE Ocean", "Beedle", False, None],

        ["Beedle", "Beedle Gem", False, has_restock_rupees(required_rupees, 200)],
        ["Beedle", "Beedle Bomb Bag", False, has_bombs & has_restock_rupees(required_rupees, 800)],
        ["Beedle", "Masked Ship Gem", False, has_restock_rupees(required_rupees, 200)],
        ["Beedle", "Masked Ship HC", False, has_restock_rupees(required_rupees, 1500)],
        ["Beedle", "Beedle Shop", False, has_rupees(required_rupees)],

        ["Beedle", "Beedle Bronze Membership", False, beedle_bronze],
        ["Beedle", "Beedle Silver Membership", False, HasBeedlePoints(20)],
        ["Beedle", "Beedle Gold Membership", False, HasBeedlePoints(50)],
        ["Beedle", "Beedle Platinum Membership", False, HasBeedlePoints(100)],
        ["Beedle", "Beedle VIP Membership", False, HasBeedlePoints(200)],

        # ============ SW Ocean =================

        ["Mercay SE", "Mercay Boat", False, has_sea_chart("SW") | [OptionFilter(PhantomHourglassShuffleIslands, 0, "gt")] | [OptionFilter(PhantomHourglassBoatRequiresSeaChart, 0)]],
            ["Mercay Boat", "Mercay SE", False, require_sea_chart("SW")],
            ["Mercay Boat", "SW Ocean East", True, require_sea_chart("SW")],
        ["Cannon Boat", "Cannon Island", False, require_sea_chart("SW")],
            ["Cannon Island", "Cannon Boat", False, None],
            ["Cannon Boat", "SW Ocean East", True, require_sea_chart("SW")],
        ["Ember Boat", "Ember Port", False, require_sea_chart("SW")],
            ["Ember Port", "Ember Boat", False, None],
            ["Ember Boat", "SW Ocean East", True, require_sea_chart("SW")],
        ["SW Ocean East", "SW Ocean Crest Salvage", False, has_courage_crest & has_salvage],
        ["SW Ocean East", "SW Ocean West", False, has_cannon],
        ["SW Ocean West", "SW Ocean East", False, has_cannon],
        ["Molida Boat", "Molida South", False, require_sea_chart("SW")],
            ["Molida South", "Molida Boat", False, None],
            ["Molida Boat", "SW Ocean West", True, require_sea_chart("SW")],
        ["Spirit Boat", "Spirit Island", False, require_sea_chart("SW")],
            ["Spirit Island", "Spirit Boat", False, None],
            ["Spirit Boat", "SW Ocean West", True, require_sea_chart("SW")],
        ["SW Ocean West", "Nyave", False, has_cave_damage | clever_pots],
        ["Nyave", "Nyave Trade", False, Has("Guard Notebook")],
        ["SW Ocean West", "SW Ocean Frog Phi", False, has_cannon],
        ["SW Ocean East", "SW Ocean Frog X", False, has_cannon],
        ["SW Ocean West", "Frog Warps", False, None],
        ["SW Ocean East", "Frog Warps", False, None],

        # ============= Frog Warps ==================
        ["Frog Warps", "SW Ocean West", False, has_frog_phi],
        ["Frog Warps", "SW Ocean East", False, has_frog_x],
        ["Frog Warps", "NW Ocean", False, has_frog_n],
        ["Frog Warps", "NE Ocean", False, has_frog_square],
        ["Frog Warps", "SE Ocean", False, has_frog_se],

        # ============ Cannon Island ===============

        ["Cannon Island", "Fuzo's Workshop", True, None],
        ["Cannon Island", "Cannon Island Dig", False, has_shovel],
        ["Cannon Island", "Bomb Flower Cave South", True, None],
        ["Bomb Flower Cave South", "Bomb Flower Cave North", False, None],
        ["Bomb Flower Cave North", "Cannon Bomb Garden", True, None],
        ["Bomb Flower Cave North", "Bomb Flower Cave South", False, hard_logic],
        ["Cannon Bomb Garden", "Cannon Outside Eddo", False, None],
        ["Cannon Outside Eddo", "Cannon Bomb Garden", False, has_explosives],
        ["Cannon Bomb Garden", "Cannon Island", False, None],
        ["Cannon Outside Eddo", "Cannon Island", False, glitched_logic],
        ["Cannon Outside Eddo", "Eddo's Workshop", True, None],
        ["Fuzo's Workshop", "Eddo's Workshop", True, Has("_eddo_door")],
        ["Eddo's Workshop", "Eddo's Cannon", False, has_rupees(50)],
        ["Eddo's Cannon", "Eddo Salvage Arm", False, has_courage_crest & has_rupees(250)],
        ["Eddo's Workshop", "Eddo Event", False, None],
        ["Cannon Bomb Garden", "Cannon Bomb Garden Dig", False, has_shovel],

        # =============== Isle of Ember ================

        # ER
        ["Ember Port", "Astrid's House", True, None],
        ["Astrid's House", "Astrid's Basement", True, None],
        ["Astrid's Basement", "Astrid's Basement Dig", False, has_shovel],
        ["Ember Port", "Kayo's House", True, None],
        ["Ember Port", "Abandoned House", True, None],
        ["Astrid's House", "Astrid Post ToF", False, Has("_beat_tof") | open_post_dungeon],

        ["Ember Port", "Ember Grapple", False, ember_grapple_chest],
        ["Ember Grapple", "Ember Port", False, has_grapple],
        ["Ember Grapple", "Ember Coast North", True, has_grapple],

        ["Ember Coast North", "Ember Coast East", True, None],
        ["Ember Port", "Ember Coast East", True, None],
        ["Ember Climb West", "Ember Coast East", True, None],
        ["Ember Climb West", "Ember Outside Temple", True, None],
        ["Ember Outside Temple", "ToF 1F", True, None],
        ["Ember Summit West", "Ember Outside Temple", True, None],
        ["Ember Summit West", "Ember Summit East", True, None],
        ["Ember Outside Temple", "Ember Outside Temple Dig", False, has_shovel],

        ["Ember Summit West", "Ember Climb West", False, None],
        ["Ember Summit East", "Ember Outside Temple", False, None],
        ["Ember Climb West", "Ember Port", False, None],
        ["Ember Outside Temple", "Ember Coast East", False, None],

        ["Ember Climb East", "Ember Coast East", True, None],
        ["Ember Summit North", "Ember Summit East", True, None],
        ["Ember Climb East", "Ember Port", True, None],
        ["Ember Summit North", "Ember Summit West", True, None],

        # =============== Temple of Fire =================

        ["ToF 1F", "ToF 1F Keese Arena", False, can_kill_bat],
        ["ToF 1F", "ToF 1F Maze", False, tof_maze],
        ["ToF 1F Maze", "ToF 2F", False, can_hit_spin_switches],
        # 2F
        ["ToF 2F", "ToF 1F West", False, has_short_range],
        ["ToF 1F West", "ToF 1F SW", False, can_hit_spiral_switches],
        ["ToF 1F SW", "ToF 2F South", False, can_kill_bubble],
        ["ToF 2F South", "ToF 3F", False, tof_3f],
        # 3F
        ["ToF 3F", "ToF 3F Key Drop", False, tof_key_drop],
        ["ToF 3F", "ToF 3F Key Door", False, tof_key_door],
        ["ToF 3F Key Door", "ToF 3F OOB", False, grapple_glitch],
            ["ToF 3F OOB", "ToF 3F Boss Key", False, None],
            ["ToF 3F OOB", "ToF 4F", False, None],
        ["ToF 3F Key Door", "ToF 3F Boss Key", False, has_boomerang],
        ["ToF 3F Key Door", "ToF 4F", True, tof_bk],
        ["ToF 4F", "Blaaz", True, None],
        ["ToF 4F", "ToF 1F", False, None],  # warp or S+Q
        ["Blaaz", "Post Blaaz", False, has_sword & has_boomerang],
        ["Post Blaaz", "Post ToF", False, has_sword & has_boomerang],

        # =========== Molida Island ===============

        ["Molida South", "Molida Dig", False, has_shovel],
        ["Molida South", "Ocara's House", True, None],
        ["Molida South", "Potato's house", True, None],
        ["Molida South", "Molida Shop", True, None],
        ["Molida Shop", "Island Shop", False, None],
        ["Molida South", "Romanos' House", True, None],
        ["Romanos' House", "Archery Game", False, (Has("_beat_toc") | (open_post_dungeon & has_bow)) & has_rupees(500)],
        ["Molida South", "Sun Lake Cave", True, None],
        ["Molida South", "Sun Lake Cave Upper", False, has_shovel],

        ["Sun Lake Cave Upper", "Sun Lake Cave", False, None],
        ["Sun Lake Cave", "Sun Lake Cave Grapple", False, has_grapple],
        ["Sun Lake Cave", "Sun Lake Cave Geozard", False, None],
        ["Sun Lake Cave Geozard", "Sun Lake Cave Geozard Dig", False, has_shovel],
        ["Sun Lake Cave Geozard", "Sun Lake Cave Defeat Geozard", False, has_cave_damage],
        ["Sun Lake Cave Defeat Geozard", "Sun Lake Cave Post Geozard", False, None],
        ["Sun Lake Cave Post Geozard", "Sun Lake Cave Geozard", False, Has("_molida_cave_geozard")],
        ["Sun Lake Cave Post Geozard", "Octorok Cave", True, None],
        ["Sun Lake Cave", "Sun Lake Cave Back", False, has_bombs],
        ["Sun Lake Cave Back", "Sun Lake Cave", False, None],
        ["Sun Lake Cave Back", "Octorok Cave", True, None],
        ["Sun Lake Cave Back", "Shovel Hideout", True, None],
        ["Shovel Hideout", "Shovel Hideout Dig", False, has_shovel],
        ["Sun Lake Cave Back", "Molida Cliff North", True, None],

        ["Molida Cliff North", "Molida Cliff South", True, None],
        ["Molida Cliff South", "Molida South", False, None],
        ["Molida Cliff South", "Molida Cucco Dig", False, cucco_dig],

        ["Sun Lake Cave Upper", "Sun Lake Cave Sun Door", True, Has("Sun Key")],
        ["Molida North", "Sun Lake Cave North Drop", False, has_shovel],
        ["Sun Lake Cave North Drop", "Sun Lake Cave Sun Door", False, None],
        ["Sun Lake Cave Sun Door", "Molida North", True, None],
        ["Molida North", "Molida North Grapple", False, has_grapple],
        ["Molida North", "Molida Temple Doors", False, has_damage & (has_boomerang | has_bow)],
        ["Molida Temple Doors", "Molida Outside Temple", False, None],
        ["Molida Outside Temple", "ToC 1F", True, None],

        # =============== Temple of Courage ================

        ["ToC 1F", "ToC 1F Bomb Alcove", False, has_explosives],
        ["ToC 1F", "ToC B1", False, toc_door_1],
        ["ToC 1F", "ToC 1F Hammer Clips", False, hammer_glitch],
        ["ToC B1", "ToC B1 Grapple", False, has_grapple | boomerang_glitch],
        ["ToC B1", "ToC 1F West", False, has_explosives & has_mid_range],
        ["ToC B1 Grapple", "ToC 1F West", False, has_bow],
        ["ToC 1F Hammer Clips", "ToC 1F West", False, None],
        ["ToC 1F West", "ToC 1F Map Room", False, has_explosives],
        ["ToC 1F West", "ToC 2F Beamos Room", False, toc_door_2],
        ["ToC 1F West", "ToC B1 Invisible Maze", False, toc_crystal("North")],
        ["ToC 2F Beamos Room", "ToC B1 Invisible Maze", False, smart_keys & pedestals_vanilla],
        ["ToC 2F Beamos Room", "ToC South 1F", False, smart_keys & pedestals_vanilla & has_bow],
        ["ToC B1 Grapple", "ToC B1 Invisible Maze", False, None],
        ["ToC B1 Invisible Maze", "ToC South 1F", False, toc_crystal("South") & has_bow],

        ["ToC South 1F", "ToC 2F Spike Corridor", False, has_explosives],
        ["ToC 2F Spike Corridor", "ToC 2F Moving Platform Room", False, has_explosives & has_bow],
        ["ToC 1F Hammer Clips", "ToC 2F Spike Corridor", False, None],
        ["ToC South 1F", "ToC 2F Moving Platform Room", False, has_bow],
        ["ToC 2F Spike Corridor", "ToC B1 Torches Platforms", False, has_boomerang | (has_grapple & has_bow & ((hard_logic & Has("_toc_b1_maze")) |(ut_glitched & has_beam_sword)))],
        ["ToC B1 Torches Platforms", "ToC B1 Torches Chest", False, has_bow],
        ["ToC B1 Torches Platforms", "ToC 1F Pols NW", False, has_bow | toc_key_doors(2, 1)],
        ["ToC 1F Pols NW", "ToC 2F Scribble Platform Room", False, toc_door_3],
        ["ToC 2F Scribble Platform Room", "ToC 2F Scribble Platform Chest", False, has_bow],
        ["ToC 2F Scribble Platform Room", "ToC 3F", False, has_boss_key("Temple of Courage") | (ut_boss_keys_own_dungeon & toc_all_checks_door_3)],
        ["ToC 2F Scribble Platform Chest", "ToC 3F", False, simple_boss_key("Temple of Courage")],
        ["ToC 3F", "ToC 3F Chest", False, has_explosives],
        ["ToC 3F", "Crayk", True, None],
        ["ToC 3F", "ToC 1F", False, None],
        ["Crayk", "Post Crayk", False, has_bow],
        ["Post Crayk", "Post ToC", False, None],

        # ================ Spirit Island =====================

        ["Spirit Island", "Spirit Island Gauntlet", False, has_grapple],
        ["Spirit Island", "Spirit Shrine", True, None],
        ["Spirit Shrine", "Spirit Power 1", False, has_spirit_gems("Power", 10)],
        ["Spirit Shrine", "Spirit Power 2", False, has_spirit_gems("Power", 20)],
        ["Spirit Shrine", "Spirit Wisdom 1", False, has_spirit_gems( "Wisdom", 10)],
        ["Spirit Shrine", "Spirit Wisdom 2", False, has_spirit_gems("Wisdom", 20)],
        ["Spirit Shrine", "Spirit Courage 1", False, has_spirit_gems("Courage", 10)],
        ["Spirit Shrine", "Spirit Courage 2", False, has_spirit_gems("Courage", 20)],

        # ============ Ocean NW ===============
        ["SW Ocean West", "NW Ocean", False, has_sea_chart("NW")],
        ["NW Ocean", "SW Ocean West", False, has_sea_chart("SW")],
        ["NW Ocean", "SW Ocean East", False, has_sea_chart("SW")],
        ["NW Ocean", "Frog Warps", False, None],
        ["NW Ocean", "NW Ocean Frog N", False, has_cannon],
        ["Gust South", "Gust Boat", False, None],
            ["Gust Boat", "Gust South", False, require_sea_chart("NW")],
            ["Gust Boat", "NW Ocean", True, require_sea_chart("NW")],
        ["Bannan Island", "Bannan Boat", False, None],
            ["Bannan Boat", "Bannan Island", False, require_sea_chart("NW")],
            ["Bannan Boat", "NW Ocean", True, bannan_sea_monster],
        ["Zauz Boat", "NW Ocean", True, require_sea_chart("NW")],
            ["Zauz's Island", "Zauz Boat", False, None],
            ["Zauz Boat", "Zauz's Island", False, require_sea_chart("NW")],
        ["Uncharted Island", "Uncharted Boat", False, None],
            ["Uncharted Boat", "Uncharted Island", False, require_sea_chart("NW")],
            ["Uncharted Boat", "NW Ocean", True, require_sea_chart("NW")],
        ["NW Ocean", "Ghost Ship Boat", False, ghost_ship_access],
            ["Ghost Ship Boat", "NW Ocean", False, require_sea_chart("NW")],
            ["Ghost Ship Boat", "Ghost Ship 1F", False, ghost_ship_access],
            ["Ghost Ship 1F", "Ghost Ship Boat", False, None],
        ["NW Ocean", "PoRL", False, None],
        ["PoRL", "PoRL Item", False, has_sword],
        ["PoRL", "PoRL Trade", False, Has("Hero's New Clothes")],
        ["NW Ocean", "Pirate Ambush", False, pirate_ambush_nw],

        # ================= Isle of Gust ====================

        ["Gust South", "Tiled Hideout", True, None],
        ["Gust South", "Miniblin Cave", True, None],
        ["Miniblin Cave", "Miniblin Cave Damage", False, has_cave_damage],
        ["Miniblin Cave", "Gust South Cliffs", True, None],
        ["Gust South Cliffs", "Gust South", False, None],
        ["Gust South Cliffs", "Gust South Cliffs Dig", False, has_shovel],
        ["Gust South Cliffs", "Gust North Temple Road", True, None],
        ["Gust South Cliffs", "Gust North Above Temple", True, None],
        ["Gust North Above Temple", "Gust South NW", True, None],
        ["Gust South NW", "Gust South NW Chest", False, has_shovel | (grapple_glitch & has_chus)],
        ["Gust South NW", "Gust South NW Ledge", False, has_shovel],
        ["Gust South NW Ledge", "Gust South NW", False, None],
        ["Gust South NW Ledge", "Gust South NW Chest", False, has_grapple],
        ["Gust South NW Ledge", "Gust North", True, None],
        ["Gust North", "Gust North Dig", False, has_shovel],
        ["Gust North", "Gust North Sandworms", True, has_shovel],
        ["Gust North Sandworms", "Gust North Event", False, None],
        ["Gust North Sandworms", "Gust North Above Temple", True, Has("_windmills")],
        ["Gust North Above Temple", "Gust North Temple Road", False, None],
        ["Gust North Temple Road", "Gust North Outside Temple", False, Has("_windmills")],
        ["Gust North Outside Temple", "Gust North Temple Road", False, None],
        ["Gust North Outside Temple", "ToW 1F", True, None],

        # ================= Temple of Wind ====================

        ["ToW 1F", "ToW B1", False, can_kill_bat],
        ["ToW B1", "ToW B2", False, None],
        ["ToW B2", "ToW B2 Dig", False, has_shovel],
        ["ToW B2", "ToW B2 Bombs", False, has_explosives],
        ["ToW B2", "ToW B2 Key", False, tow_key],
        ["ToW B2 Bombs", "ToW 1F NE", False, has_bombs],
        ["ToW 1F", "ToW 2F", False, tow_bk],
        ["ToW 2F", "Cyclok", True, None],
        ["ToW 2F", "ToW 1F", False, None],
        ["Cyclok", "Post Cyclok", False, None],
        ["Post Cyclok", "Post ToW", False, None],

        # ================= Bannan Island ====================

        ["Bannan Island", "Bannan West Grapple", False, has_grapple],
        ["Bannan Island", "Bannan Dig", False, has_shovel],
        ["Bannan Island", "Wayfarer's House", True, None],
        ["Wayfarer's House", "Wayfarer Event", False, None],
        ["Bannan Island", "Keese Passage West", True, None],
        ["Keese Passage West", "Keese Passage East", True, has_bombs],
        ["Keese Passage East", "Bannan East", True, None],
        ["Bannan East", "Bannan East Grapple", False, has_grapple],
        ["Bannan East Grapple", "Bannan East Grapple Dig", False, has_shovel],
        ["Bannan East", "Bannan Cannon Game", False, has_cannon & has_rupees(500)],
        ["Wayfarer's House", "Wayfarer Trade Quest", False, bannan_scroll],
        ["Wayfarer's House", "Wayfarer Give Loovar", False, has_fish("Loovar")],
        ["Wayfarer's House", "Wayfarer Give Rusty Swordfish", False, has_rsf],
        ["Wayfarer's House", "Wayfarer Give Legendary Neptoona", False, has_neptoona],
        ["Wayfarer's House", "Wayfarer Give Stowfish", False, has_stowfish],
        ["Wayfarer's House", "Joanne Give Letter", False, Has("Jolene's Letter")],

        # ================= Zauz's Island ====================

        ["Zauz's Island", "Zauz Dig", False, has_shovel],
        ["Zauz's Island", "Zauz's House", True, None],
        ["Zauz's House", "Zauz's Blade", False, HasGroup("Metals", FromOption(PhantomHourglassZauzRequiredMetals))],
        ["Zauz's House", "Zauz's Crest", False, Has("_beat_ghost_ship") | open_post_dungeon],

        # ================= Uncharted Island ====================

        ["Uncharted Island", "Uncharted Dig", False, has_shovel],
        ["Uncharted Island", "Uncharted Puzzle", False, has_sword],
        ["Uncharted Puzzle", "Uncharted Outside Cave", False, None],
        ["Uncharted Outside Cave", "Descending Cave", True, None],
        ["Descending Cave", "Golden Chief Cave", True, None],
        ["Descending Cave", "Descending Cave Grapple", False, has_grapple],

        # ================= Ghost Ship ====================

        ["Ghost Ship 1F", "Ghost Ship B1", True, None],
        ["Ghost Ship B1", "Ghost Ship B1 Barrel", False, gs_barrel],
        ["Ghost Ship B1 Barrel", "Ghost Ship B2", False, gs_triangle],
        ["Ghost Ship B2", "Ghost Ship B2 Chests", False, can_hit_switches],
        ["Ghost Ship B2 Chests", "Ghost Ship B3", False, can_kill_bat],
        ["Ghost Ship B3", "Ghost Ship Warp", False, None],
        ["Ghost Ship Warp", "Cubus Sisters", False, Has("_rescue_4th_sister")],
        ["Cubus Sisters", "Ghost Ship Warp", False, has_sword],
        ["Ghost Ship Warp", "Ghost Ship 1F", False, None],
        ["Cubus Sisters", "Post Cubus Sisters", False, has_sword],
        ["Post Cubus Sisters", "Post Cubus Sisters Event", False, None],
        ["Ghost Ship B2", "Ghost Ship Tetra", False, Has("Ghost Key")],
        ["Ghost Ship Tetra", "Spawn Pirate Ambush", False, None],

        # ================= SE Ocean ====================

        ["SW Ocean East", "SE Ocean", False, has_sea_chart("SE")],
        ["SE Ocean", "SW Ocean East", False, has_sea_chart("SW")],
        ["SE Ocean", "Frog Warps", False, None],
        ["SE Ocean", "SE Ocean Frogs", False, has_cannon],
        ["SE Ocean", "Goron Boat", False, charted_sea_monster("SE")],
            ["Goron Boat", "SE Ocean", False, require_sea_chart("SE")],
            ["Goron Boat", "Goron SW",False, charted_sea_monster("SE")],
            ["Goron SW", "Goron Boat", False, None],
        ["SE Ocean", "SE Ocean Trade", False, Has("Kaleidoscope")],
        ["SE Ocean", "Frost Boat", False, charted_sea_monster("SE")],
            ["Frost Boat", "SE Ocean", False, require_sea_chart("SE")],
            ["Frost Boat", "Frost SW", False, charted_sea_monster("SE")],
            ["Frost SW", "Frost Boat", False, None],
        ["Harrow Island", "Harrow Boat", False, None],
            ["Harrow Boat", "Harrow Island", False, require_sea_chart("SE")],
            ["Harrow Boat", "SE Ocean", True, require_sea_chart("SE")],
        ["Dee Ess Island", "Dee Ess Boat", False, None],
            ["Dee Ess Boat", "Dee Ess Island", False, require_sea_chart("SE")],
            ["Dee Ess Boat", "SE Ocean", True, require_sea_chart("SE")],
        ["SE Ocean", "Pirate Ambush", False, unlock_ambush],
        ["SE Ocean", "SS Wayfarer", True, Has("Wood Heart") & Has("_wayfarer_gift")],
        ["SS Wayfarer", "SS Wayfarer Trade", False, Has("Wood Heart")],
        ["SS Wayfarer Trade", "SS Wayfarer Event", False, None],

        # ================= Goron Island ====================

        ["Goron SW", "Goron House Zero Rocks", True, None],
        ["Goron SW", "Goron Shop", True, None],
        ["Goron Shop", "Island Shop", False, None],
        ["Goron SW", "Goron House Three Rocks", True, None],
        ["Goron SW", "Goron House Left Rock", True, None],
        ["Goron SW", "Goron NW Shortcut", True, None],
        ["Goron SW Chu Ledge", "Goron Chus", False, goron_chus],
        ["Goron Chus", "Goron Chus Event", False, None],
        ["Goron SW Chu Ledge", "Goron SW Grapple", False, has_grapple],
        ["Goron SW", "Goron SE NW", True, None],
        ["Goron SW Chu Ledge", "Goron SW", False, None],
        ["Goron SE NW", "Goron SW Chu Ledge", True, None],
        ["Goron SE NW", "Goron House Right Rock", True, None],
        ["Goron SE", "Goron House Two Rocks", True, None],
        ["Goron SE", "Goron Chief House", True, None],
        ["Goron SE NW", "Goron SE Bridge Event", False, None],
        ["Goron SE", "Goron SE NW", False, None],
        ["Goron SE NW", "Goron SE", False, Has("_goron_bridge")],
        ["Goron Chief House", "Goron Quiz", False, Has("_goron_bridge") & Has("_goron_chus")],
        ["Goron Quiz", "Goron Chief Post Dungeon", False, Has("_beat_gt") | open_post_dungeon],
        ["Goron SE", "Goron NE", True, None],

        ["Goron NE", "Goron NE South", False, None],
        ["Goron NE South", "Goron NE Event", False, None],
        ["Goron NE South", "Goron NE", False, has_explosives],
        ["Goron NE South", "Goron NW South Dead End", True, None],
        ["Goron NE", "Goron NE Middle", False, None],
        ["Goron NE", "Goron NE Chu Chest", False, bombchu_switches],
        ["Goron NE Middle", "Goron NE", False, has_explosives],
        ["Goron NE Middle", "Goron NE Coast", True, has_explosives],
        ["Goron NE Middle", "Goron NW North Dead End", True, None],
        ["Goron NE Coast", "Goron NW Like Like", True, None],
        ["Goron NW Like Like", "Goron NW Outside Temple", False, has_damage],
        ["Goron NW Like Like", "Goron NE Spikes", True, None],
        ["Goron NE Spikes", "Goron NE Spike Chest", False, Has("_goron_maze_switch")],
        ["Goron NW Outside Temple", "Goron NW Like Like", False, clever_bombs],  # Hard logic

        ["Goron NW Shortcut", "Goron NW Outside Temple", False, hammer_glitch],
        ["Goron NW Outside Temple", "Goron NW Shortcut", False, None],
        ["Goron NW Outside Temple", "GT 1F", True, None],

        # ================= Goron Temple ====================
        ["GT 1F", "GT 1F Upper", False, has_shovel],
        ["GT 1F Upper", "GT 1F NW", False, has_explosives | has_hammer],
        ["GT 1F", "GT 1F NW", False, grapple_glitch & has_bow & has_chus],
        ["GT 1F NW", "GT 1F Bow", False, has_bow],
        ["GT 1F NW", "GT B1", False, has_explosives & has_sword & can_kill_eye_brute],
        ["GT B1", "GT B2", False, bombchu_switches],
        ["GT B2", "GT B3", False, None],
        ["GT B2", "GT B2 Back", False, has_explosives | has_boomerang],
        ["GT B2 Back", "GT B2 Back Chest", False, has_chus],
        ["GT B2", "GT B4", False, gt_bk],
        ["GT B4", "Dongorongo", True, None],
        ["GT B4", "GT 1F", False, None],
        ["Dongorongo", "Post Dongorongo", False, has_sword & has_chus],
        ["Post Dongorongo", "Post GT", False, None],

        # ================= Harrow Island ====================

        ["Harrow Island", "Harrow Sword", False, has_sword],
        ["Harrow Sword", "Harrow Minigame", False, has_shovel],
        ["Harrow Minigame", "Harrow Minigame NE Chart", False, has_sea_chart("NE")],

        # ================= Dee Ess Island ====================

        ["Dee Ess Island", "Dee Ess Dig", False, has_shovel],
        ["Dee Ess Island", "Dee Ess Eye Brutes", False, can_kill_eye_brute],
        ["Dee Ess Island", "Dee Ess Goron Race", False, (Has("_beat_gt") | open_post_dungeon) & has_rupees(500)],

        # ================= Isle of Frost ====================

        ["Frost SW", "Frost SW Grapple", False, has_grapple],
        ["Frost SW", "Frost SW Dig", False, has_shovel],
        ["Frost SW", "Smart Anouki's House", True, None],
        ["Frost SW", "Sensitive Anouki's House", True, None],
        ["Frost SW", "Anouki Chief's House", True, None],
        ["Frost SW", "Frost NW", True, None],
        ["Frost SW", "Frozen Cave", True, None],

        ["Frost NW", "Fofo's House", True, None],
        ["Frost NW", "Kumu's House", True, None],
        ["Frost NW", "Dobo's House", True, None],
        ["Frost NW", "Gumo's House", True, None],
        ["Frost NW", "Aroo's House", True, None],
        ["Frost NW", "Mazo's House", True, None],
        ["Frost NW", "Frost NW Dig", False, has_shovel],
        ["Frost NW Dig", "Frost NW Grapple Dig", False, has_grapple],

        ["Frozen Cave", "Frost SE", True, None],
        ["Frost SE", "Frost SE Yook", False, ice_field],
        ["Frost SE Yook", "Frost SE Exit", False, None],
        ["Frost SE", "Frost SE Upper East", False, has_grapple],
        ["Frost SE Upper East", "Frost SE", False, None],
        ["Frost SE Upper East", "Frost SE Upper Chests", False, has_grapple],
        ["Frost SE Upper East", "Frost SE East Ledge", False, None],
        ["Frost SE Upper East", "Frost SE Upper North", True, has_grapple],
        ["Frost SE Upper East", "Frost SE Exit", False, None],
        ["Frost SE Upper North", "Frost SE", False, None],
        ["Frost SE Upper North", "Frost SE Exit", False, None],
        ["Frost SE Exit", "Frost SE", False, Has("_beat_toi")],
        ["Frost SE Upper North", "Frost NE Above Temple West", True, None],
        ["Frost SE Upper East", "Frost NE Above Temple East", True, None],
        ["Frost SE Exit", "Frost NE Outside Arena", True, None],

        ["Frost NE Above Temple East", "Frost NE Outside Arena", False, None],
        ["Frost NE Above Temple West", "Frost NE Outside Arena", False, None],
        ["Frost NE Outside Arena", "Frost NE Arena", False, None],
        ["Frost NE Arena", "Frost NE Outside Arena", False, can_kill_dark_yook],
        ["Frost NE Arena", "Frost NE Outside Temple", False, can_kill_dark_yook],
        ["Frost NE Arena", "Frost NE Above Temple West", False, has_grapple],
        ["Frost NE Outside Temple", "Frost NE Arena", False, None],
        ["Frost NE Outside Temple", "ToI 1F", True, None],

        # ================= Ice Temple ====================

        ["ToI 1F", "ToI 1F Ascent", False, has_explosives | has_boomerang],
        ["ToI 1F Ascent", "ToI 2F Right", True, None],
        ["ToI 3F Right", "ToI 2F Right", True, None],
        ["ToI 3F Right", "ToI 3F", False, has_range | has_bombs],
        ["ToI 3F", "ToI 3F Right", False, has_range],
        ["ToI 3F", "ToI 3F Key Door", True, toi_door_1],
        ["ToI 3F", "ToI 3F Switch State", False, has_bombs | (hard_logic & (has_chus | has_boomerang))],
        ["ToI 3F Switch State", "ToI 3F Boomerang Key", False, toi_3f_boomerang],
        ["ToI 3F Key Door", "ToI 2F Arena", True, None],
        ["ToI 2F Arena", "ToI 2F Post Arena", False, can_kill_dark_yook],
        ["ToI 2F Arena", "ToI 2F Left", False, can_kill_dark_yook & has_grapple],
        ["ToI 2F Left", "ToI 1F Beetles", True, None],
        ["ToI 1F Beetles", "ToI 1F Shortcut", False, has_grapple],
        ["ToI 1F Shortcut", "ToI 1F Beetles", False, grapple_glitch],
        ["ToI 1F", "ToI 1F Shortcut", False, hammer_glitch],
        ["ToI 1F Shortcut", "ToI 1F", False, None],
        ["ToI 1F Shortcut", "ToI 1F Descent", False, has_grapple],
        ["ToI 1F Descent", "ToI B1 Ascent", True, None],

        ["ToI B1 Ascent", "ToI B1 Shore", False, None],
        ["ToI B1 Shore", "ToI B1 Ascent", False, hammer_glitch],
        ["ToI B1 Shore", "ToI B1 South", False, has_hammer | (has_explosives | has_grapple)],
        ["ToI B1 South", "ToI B1 Shore", False, None],
        ["ToI B1 South", "ToI B1 Mid", True, has_explosives],
        ["ToI B1 Mid", "ToI B1 Right", False, has_grapple],
        ["ToI B1 Right", "ToI B1 Switch", False, hammer_glitch],
        ["ToI B1 Right", "ToI B1 Switch Room", False, toi_door_2],
        ["ToI B1 Switch Room", "ToI B1 Switch", False, has_boomerang | has_hammer | has_explosives],
        ["ToI B1 Mid", "ToI B1 Boss Door", False, toi_b2],
        ["ToI B1 Boss Door", "ToI B1 Mid", False, has_grapple],
        ["ToI B1 Boss Door", "ToI B1 Before Boss", True, toi_bk],
        ["ToI B1 Before Boss", "Gleeok", True, None],
        ["Gleeok", "Post Gleeok", False, gleeok],
        ["Post Gleeok", "Post ToI", False, None],
        ["ToI B1 Before Boss", "ToI Blue Warp", True, None],
        ["ToI 1F", "ToI Blue Warp", True, Has("_toi_blue_warp")],
        ["ToI B1 Boss Door", "ToI B2", True, None],

        ["ToI B2", "ToI B2 North", False, can_kill_yook & has_grapple & can_hit_spin_switches],
        ["ToI B2 North", "ToI B2 BK Chest", False, hammer_glitch],
        ["ToI B2 North", "ToI B2 East", False, None],
        ["ToI B2 East", "ToI B2 Bow", False, has_bow],
        ["ToI B2 East", "ToI B2 East Arena", False, toi_door_3],
        ["ToI B2 East Arena", "ToI B2 BK Chest", False, None],

        # ================= NE Ocean ====================

        ["SE Ocean", "NE Ocean", False, has_sea_chart("NE")],
        ["NE Ocean", "SE Ocean", False, has_sea_chart("SE")],
        ["NE Ocean", "Frog Warps", False, None],
        ["NE Ocean", "NE Ocean Frog", False, has_cannon],
        ["NE Ocean", "NE Ocean Combat", False, can_kill_blue_chu],
        ["IotD Boat", "IotD Port", False, require_sea_chart("NE")],
            ["IotD Port", "IotD Boat", False, None],
            ["IotD Boat", "NE Ocean", True, require_sea_chart("NE")],
        ["Maze Boat", "Maze Island", False, require_sea_chart("NE")],
            ["Maze Island", "Maze Boat", False, None],
            ["Maze Boat", "NE Ocean", True, require_sea_chart("NE")],
        ["NE Ocean Inner", "Ruins Boat", False, None],
            ["Ruins Boat", "NE Ocean", False, require_sea_chart("NE")],
            ["Ruins Boat", "Ruins SW Port", False, Has("Regal Necklace")],
            ["Ruins SW Port", "Ruins Boat", False, None],
        ["NE Ocean", "Pirate Ambush", False, unlock_ambush],

        # ================= IotD ====================

        ["IotD Port", "McNay's Cave", True, None],
        ["Isle of the Dead", "IotD Port", False, None],
        ["McNay's Cave", "Rupoor Cave", False, has_bombs],
        ["Rupoor Cave", "McNay's Cave", False, None],
        ["McNay's Cave", "Isle of the Dead", True, None],
        ["Isle of the Dead", "Brant's Temple", True, None],
        ["Isle of the Dead", "Boulder Tunnel", False, has_shovel],
        ["Boulder Tunnel", "Stone Treasure Cave", False, has_bombs],
        ["Stone Treasure Cave", "Boulder Tunnel", False, None],
        ["Boulder Tunnel", "IotD Face", True, None],
        ["IotD Face", "Isle of the Dead", False, None],
        ["Brant's Temple", "IotD Crown", True, None],
        ["IotD Crown", "Isle of the Dead", False, None],

        # ================= Isle of Ruins ====================

        ["Ruins SW Port", "Sandy Geozard Cave East", True, None],
        ["Sandy Geozard Cave East", "Sandy Geozard Cave West", True, has_cave_damage | ruins_water],
        ["Sandy Geozard Cave West", "Ruins SW Maze Upper", True, None],
        ["Ruins SW Maze Upper", "Ruins SW Port", False, None],
        ["Ruins SW Maze Upper", "Ruins SW Maze Lower", False, ruins_water],
        ["Ruins SW Port Cliff", "Ruins SW Maze Upper", False, None],
        ["Ruins SW Maze Lower", "Ruins SW Maze Lower Exit", True, ruins_water],
        ["Ruins SW Maze Lower Exit", "Ruins NW Maze Lower Exit", True, None],
        ["Ruins SW Maze Upper", "Ruins NW Maze Upper Exit", True, None],
        ["Ruins SW Maze Lower Water", "Ruins NW Maze Lower Water", True, ruins_water],  # Separate the water logic from the transition
            ["Ruins SW Maze Lower", "Ruins SW Maze Lower Water", True, ruins_water],
            ["Ruins NW Maze Lower Water", "Ruins NW Maze Lower Chest", True, ruins_water],

        ["Ruins NW Maze Lower Exit", "Ruins NW Boulders", False, None],
        ["Ruins NW Maze Upper Exit", "Ruins NW Boulders", False, None],
        ["Ruins NW Boulders", "Ruins NW Dig", False, has_shovel],
        ["Ruins NW Port Cliff", "Ruins NW Maze Lower Chest", False, ruins_water],
        ["Ruins NW Boulders", "Ruins NW Across Bridge", True, None],
        ["Ruins NW Boulders", "Bremeur's Temple", True, None],
        ["Bremeur's Temple", "Bremeur's Temple Kings Key", False, Has("King's Key")],
        ["Bremeur's Temple Kings Key", "Bremeur's Temple Event", False, None],
        ["Ruins NW Boulders", "Ruins NW Port Cliff", False, None],
        ["Ruins NW Port Cliff", "Ruins SW Port Cliff", True, None],
        ["Ruins NW Port Cliff", "Ruins NW Port Cliff Tree", False, ruins_water],
        ["Ruins NW Boulders", "Ruins NW Lower", False, ruins_water],
        ["Ruins NW Across Bridge", "Ruins NW Cave", True, ruins_water],
            ["Ruins NW Cave", "Grassy Treasure Cave", False, ruins_water],
            ["Grassy Treasure Cave", "Ruins NW Cave", False, None],
        ["Ruins NW Across Bridge", "Ruins NW Alcove", False, ruins_water],
        ["Ruins NW Across Bridge", "Ruins NE Enter Upper", True, None],
        ["Ruins NW Return", "Ruins NW Boulders", False, None],
        ["Ruins NW Across Bridge", "Ruins NW Return", False, hard_logic],
        ["Ruins NW Lower", "Ruins NW Lower Water", True, ruins_water],
            ["Ruins NE Lower Water North", "Ruins NE Lower", True, ruins_water],
            ["Ruins NW Lower Water", "Ruins NE Lower Water North", True, ruins_water],

        ["Ruins NE Enter Upper", "Ruins NE Doylan Bridge", False, None],
        ["Ruins NE Doylan Bridge", "Ruins NE Lower", False, ruins_water],
        ["Ruins NE Doylan Bridge", "Ruins NE Behind Pyramids", True, ruins_water],
        ["Ruins NE Doylan Bridge", "Ruins NE Doylan Bridge North", False, ruins_water | can_kill_bat | hard_logic],
        ["Ruins NE Doylan Bridge North", "Ruins NE Doylan Bridge", False, ruins_water | can_kill_bat],
        ["Ruins NE Doylan Bridge North", "Ruins NW Return", True, None],
        ["Ruins NE Doylan Bridge", "Doylan's Temple", True, None],
        ["Doylan's Temple", "Doylan's Chamber", True, None],
        ["Ruins NE Lower Water South", "Ruins NW Alcove Water", True, ruins_water],
            ["Ruins NW Alcove Water", "Ruins NW Alcove", True, ruins_water],
            ["Ruins NE Lower", "Ruins NE Lower Water South", True, ruins_water],
        ["Ruins NE Lower", "Ruins NE Behind Pyramids", True, has_grapple],
        ["Ruins NE Lower Water Bay", "Ruins SE Lower Water Bay", True, ruins_water],
            ["Ruins NE Lower Water Bay", "Ruins NE Lower", True, ruins_water],
            ["Ruins SE Lower Water Bay", "Ruins SE Lower", True, ruins_water],
        ["Ruins NE Behind Pyramids Water", "Ruins SE Coast Water", True, ruins_water],
            ["Ruins NE Behind Pyramids", "Ruins NE Behind Pyramids Water", True, ruins_water],
            ["Ruins SE Coast Water", "Ruins SE Coast", True, ruins_water],
        ["Ruins NE Outside Temple", "Ruins NE Behind Pyramids", False, ruins_water],
        ["Ruins NE Outside Temple", "MT 1F", False, ruins_water],
            ["MT 1F", "Ruins NE Outside Temple", False, None],
        ["Ruins NE Outside Temple", "Ruins NE Geozard Arena", False, ruins_water],
        ["Ruins NE Geozard Arena", "Ruins NE Outside Temple", False, has_damage],

        ["Ruins SE Lower Water Wall", "Ruins NE Secret Chest Water", True, ruins_water],
            ["Ruins NE Secret Chest Water", "Ruins NE Secret Chest", True, ruins_water],
            ["Ruins SE Lower", "Ruins SE Lower Water Wall", True, ruins_water],
        ["Ruins SE Lower", "Ruins SE Return Bridge East", True, ruins_water],
        ["Ruins SE Return Bridge West", "Ruins SE Return Bridge East", False, has_hammer],
        ["Ruins SE Return Bridge East", "Ruins SE Return Bridge West", False, None],
        ["Ruins SE Lower", "Ruins SE Outside Pyramid", True, ruins_water],
            ["Ruins SE Outside Pyramid", "Max's Temple", False, ruins_water],
            ["Max's Temple", "Ruins SE Outside Pyramid", False, None],
        ["Ruins SE Return Bridge West", "Ruins SW Port Cliff", True, None],
        ["Ruins SE Lower", "Ruins SE King's Road", False, None],
        ["Ruins SE King's Road Water", "Ruins NE Geozards Water", True, ruins_water],
            ["Ruins NE Geozards Water", "Ruins NE Geozard Arena", True, ruins_water],
            ["Ruins SE King's Road", "Ruins SE King's Road Water", True, ruins_water],

        # ================= Mutoh's Temple ====================

        ["MT 1F", "MT Landing", False, mutoh_entrance],
        ["MT Landing", "MT Hammer", False, has_hammer],
        ["MT Hammer", "MT Lower Water", False, mutoh_water],
        ["MT Lower Water", "MT BK Chest", False, mutoh_bk_chest],
        ["MT Lower Water", "MT B3", False, mutoh_bk],
        ["MT B3", "Eox", True, None],
        ["MT B3", "MT 1F", False, None],
        ["Eox", "Post Eox", False, has_hammer],
        ["Post Eox", "Post MT", False, None],

        # ================= Maze Island ====================

        ["Maze Island", "Maze Island Minigame", False, has_sword & has_rupees(500)],
        ["Maze Island Minigame", "Maze Island Bomb Chest", False, has_explosives],
        ["Maze Island Minigame", "Maze Island Minigame Normal", False, has_bow],
        ["Maze Island Minigame Normal", "Maze Island Minigame Expert", False, has_grapple],
        ["Maze Island Minigame", "Maze Island Dig", False, has_shovel],

        # ========== Fishing ====================

        ["Frog Warps", "Fishing", False, has_fishing_rod],
        ["Fishing", "Fishing Big Catch Lure", False, has_lure],
        ["Fishing", "Fishing Rusty Swordfish", False, can_catch_rsf],
        ["Fishing", "Fishing Shadows", False, has_swordfish_shadows],
        ["Fishing", "Fishing Stowfish", False, can_catch_stowfish],

        # ========== Salvage ==============

        ["SW Ocean West", "SW Ocean West Salvage", False, has_salvage],
        ["SW Ocean East", "SW Ocean East Salvage", False, has_salvage],
        ["NW Ocean", "NW Ocean Salvage", False, has_salvage],
        ["SE Ocean", "SE Ocean Salvage", False, has_salvage],
        ["NE Ocean", "NE Ocean Salvage", False, has_salvage],
        ["NE Ocean", "NE Ocean Inner", False, Has("Regal Necklace")],
        ["NE Ocean Inner", "NE Ocean", False, None],
        ["NE Ocean Inner", "NE Ocean Salvage Inner", False, has_salvage],
        ["NE Ocean", "NW Ocean Corner Salvage", False, has_salvage & has_sea_chart("NW")],

        ["SW Ocean West Salvage", "Salvage 1", False, has_map(1)],
        ["SW Ocean East Salvage", "Salvage 2", False, has_map(2)],
        ["NW Ocean Salvage", "Salvage 3", False, has_map(3)],
        ["NW Ocean Corner Salvage", "Salvage 4", False, has_map(4)],
        ["SW Ocean West Salvage", "Salvage 5", False, has_map(5)],
        ["NW Ocean Salvage", "Salvage 6", False, has_map(6)],
        ["NW Ocean Salvage", "Salvage 7", False, has_map(7)],
        ["SW Ocean East Salvage", "Salvage 8", False, has_map(8)],
        ["SW Ocean East Salvage", "Salvage 9", False, has_map(9)],
        ["NW Ocean Salvage", "Salvage 10", False, has_map(10)],
        ["NW Ocean Salvage", "Salvage 11", False, has_map(11)],
        ["SE Ocean Salvage", "Salvage 12", False, has_map(12)],
        ["SE Ocean Salvage", "Salvage 13", False, has_map(13)],
        ["SE Ocean Salvage", "Salvage 14", False, has_map(14)],
        ["SE Ocean Salvage", "Salvage 15", False, has_map(15)],
        ["SE Ocean Salvage", "Salvage 16", False, has_map(16)],
        ["SE Ocean Salvage", "Salvage 17", False, has_map(17)],
        ["SW Ocean East Salvage", "Salvage 18", False, has_map(18)],
        ["NW Ocean Salvage", "Salvage 19", False, has_map(19)],
        ["NW Ocean Corner Salvage", "Salvage 20", False, has_map(20)],
        ["SW Ocean West Salvage", "Salvage 21", False, has_map(21)],
        ["SE Ocean Salvage", "Salvage 22", False, has_map(22)],
        ["SE Ocean Salvage", "Salvage 23", False, has_map(23)],
        ["NE Ocean Salvage", "Salvage 24", False, has_map(24)],
        ["NE Ocean Salvage", "Salvage 25", False, has_map(25)],
        ["NE Ocean Salvage Inner", "Salvage 26", False, has_map(26)],
        ["NE Ocean Salvage", "Salvage 27", False, has_map(27)],
        ["NE Ocean Salvage Inner", "Salvage 28", False, has_map(28)],
        ["NE Ocean Salvage", "Salvage 29", False, has_map(29)],
        ["NE Ocean Salvage", "Salvage 30", False, has_map(30)],
        ["NE Ocean Salvage", "Salvage 31", False, has_map(31)],

        # Goal stuff
        ["SW Ocean East", "Bellumbeck", False, can_defeat_bellumbeck & has_metals & bellum_access_wreck],
        ["Bellumbeck", "Defeat Bellumbeck", False, can_defeat_bellumbeck],
        ["Defeat Bellumbeck", "Goal", False, Filtered(True_(), options=goal_bellumbeck)],
        ["Goal", "Goal Event", False, None],  # Event stuff
        ["Goal", "Goal Event Triforce", False, None],  # Event stuff
        ["Goal", "Goal Event Bellumbeck", False, None],  # Event stuff
        ["TotOK B6 Midway", "Goal", False, Filtered(True_(), options=goal_midway)],
        ["Zauz's House", "Goal", False, win_on_metals],

    ]

    return overworld_logic

def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name


def create_connections(world: "PhantomHourglassWorld", player: int, origin_name: str, options):
    def create_entrance(r1: "Region", r2: "Region"):
        entrance_key = (r1.name, r2.name)
        name = None
        if entrance_key in test_entrances:
            entrance_data = test_entrances[entrance_key]
            name = entrance_data.name
            entrance = r1.connect(r2, name, rule)

            # Set entrance data
            rando_type_bool = entrance_data.two_way
            entrance.randomization_type = EntranceType.TWO_WAY if rando_type_bool else EntranceType.ONE_WAY
            entrance.randomization_group = entrance_data.direction | entrance_data.category_group | entrance_data.island
            world.entrances[entrance.name] = entrance  # add to world.entrances
            uncreated_entrances.remove(entrance.name)
        else:
            r1.connect(r2, name, rule)

        # if rule is not None:
        #     world.set_rule(entrance, rule)

    world.set_completion_rule(Has("_beaten_game"))
    all_logic = [
        make_overworld_logic(world)
    ]
    # UT creates alias regions
    if world.is_ut:
        from .data.Constants import region_aliases
        from .data.Regions import REGIONS
        alias_logic = []
        for region, aliases in region_aliases.items():
            for alias in aliases:
                alias_logic.append([region, alias, False, None])
        all_logic.append(alias_logic)
        all_logic.append([[entr.entrance_region, entr.name, False, None] for entr in ENTRANCES.values() if entr.name not in REGIONS])

    test_entrances = {(e.entrance_region, e.exit_region): e for e in ENTRANCES.values()}
    uncreated_entrances = [e.name for e in ENTRANCES.values()]

    # Create connections
    for logic_array in all_logic:
        for reg1, reg2, is_two_way, rule in logic_array:
            region_1 = world.get_region(reg1)
            region_2 = world.get_region(reg2)
            # print(f"Creating entrance: {reg1} -> {reg2}")
            create_entrance(region_1, region_2)
            if is_two_way:
                create_entrance(region_2, region_1)


    # print(f"Some entrances had no logical matches: ")
    # for i in uncreated_entrances:
    #     print(f"\t{i}")

if __name__ == "__main__":
    pass
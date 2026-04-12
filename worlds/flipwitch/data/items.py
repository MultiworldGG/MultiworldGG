from dataclasses import dataclass
from typing import List
from BaseClasses import ItemClassification

from ..strings.items import QuestItem, Upgrade, Coin, GachaItem, Unlock, Key, Costume, Power, Warp, GoalItem, Accessory, Custom, Trap


@dataclass(frozen=True)
class FlipwitchItemData:
    code: int
    name: str
    classification: ItemClassification

    def __repr__(self):
        return f"{self.code} {self.name} (Classification: {self.classification})"


all_items: List[FlipwitchItemData] = []


def create_item(code: int, name: str, classification: ItemClassification):
    item = FlipwitchItemData(code, name, classification)
    all_items.append(item)

    return item

# ID - Classification Data


# Uses a structure of BASE ITEM + type offset + pseudo value.  The base item ID will eventually be deprecated in favor of starting at 1.
ITEM_CODE_START = 0


base_start_id = 0
base_items = [
    create_item(ITEM_CODE_START + base_start_id + 1, Power.bomb, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 2, Power.ghost_form, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 3, Power.slime_form, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 4, Power.harpy_feather, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 5, Accessory.magnetic_hairpin, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 6, Accessory.sacrificial_dagger, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 7, Accessory.flutterknife_garter, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 8, Upgrade.health, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 9, Upgrade.mana, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 10, Upgrade.wand, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 11, Upgrade.peachy_peach, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 12, Upgrade.bewitched_bubble, ItemClassification.progression | ItemClassification.useful),
    # create_item(ITEM_CODE_START + base_start_id + 13, Upgrade.goblin_crystal, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 14, Upgrade.demon_wings, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 15, Upgrade.angel_feathers, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 16, Upgrade.mermaid_scale, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 17, Coin.lucky_coin, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 18, Coin.loose_change, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 19, Unlock.crystal_block, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 20, Unlock.goblin_crystal_block, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 21, Costume.navy, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 22, Costume.red_wizard, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 24, Costume.rat, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 25, Costume.angler, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 26, Costume.fairy, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 27, Key.rundown_house, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 28, Key.ghostly_castle, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 29, Key.beast, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 30, Key.secret_club, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 31, Key.slime_citadel, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 32, Key.frog_boss, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 33, Key.goblin_queen, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 34, Key.rose_garden, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 35, Key.collapsed_temple, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 36, Key.demon_boss, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 37, Key.slimy_sub_boss, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 38, Key.chaos_sanctum, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 40, Key.secret_garden, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 41, Key.demon_club, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 42, Key.slime_boss, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 43, Key.forgotten_fungal, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 45, GoalItem.chaos_piece, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 46, Custom.hp_heal, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 47, Custom.mp_heal, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 48, Custom.peach_recharge, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 49, Upgrade.barrier, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 50, Upgrade.peachy_upgrade, ItemClassification.useful),
]

gacha_item_id = 100
gacha_items = [
    create_item(ITEM_CODE_START + gacha_item_id + 1, GachaItem.special_promotion, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 2, GachaItem.animal_girl_1, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 3, GachaItem.animal_girl_2, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 4, GachaItem.animal_girl_3, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 5, GachaItem.animal_girl_4, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 6, GachaItem.animal_girl_5, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 7, GachaItem.animal_girl_6, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 8, GachaItem.animal_girl_7, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 9, GachaItem.animal_girl_8, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 10, GachaItem.animal_girl_9, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 11, GachaItem.animal_girl_10, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 12, GachaItem.bunny_girl_1, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 13, GachaItem.bunny_girl_2, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 14, GachaItem.bunny_girl_3, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 15, GachaItem.bunny_girl_4, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 16, GachaItem.bunny_girl_5, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 17, GachaItem.bunny_girl_6, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 18, GachaItem.bunny_girl_7, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 19, GachaItem.bunny_girl_8, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 20, GachaItem.bunny_girl_9, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 21, GachaItem.bunny_girl_10, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 22, GachaItem.angel_demon_1, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 23, GachaItem.angel_demon_2, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 24, GachaItem.angel_demon_3, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 25, GachaItem.angel_demon_4, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 26, GachaItem.angel_demon_5, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 27, GachaItem.angel_demon_6, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 28, GachaItem.angel_demon_7, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 29, GachaItem.angel_demon_8, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 30, GachaItem.angel_demon_9, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 31, GachaItem.angel_demon_10, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 32, GachaItem.monster_girl_1, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 33, GachaItem.monster_girl_2, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 34, GachaItem.monster_girl_3, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 35, GachaItem.monster_girl_4, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 36, GachaItem.monster_girl_5, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 37, GachaItem.monster_girl_6, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 38, GachaItem.monster_girl_7, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 39, GachaItem.monster_girl_8, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 40, GachaItem.monster_girl_9, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 41, GachaItem.monster_girl_10, ItemClassification.filler),
    create_item(ITEM_CODE_START + gacha_item_id + 42, Coin.animal_coin, ItemClassification.progression_deprioritized),
    create_item(ITEM_CODE_START + gacha_item_id + 43, Coin.bunny_coin, ItemClassification.progression_deprioritized),
    create_item(ITEM_CODE_START + gacha_item_id + 44, Coin.angel_demon_coin, ItemClassification.progression_deprioritized),
    create_item(ITEM_CODE_START + gacha_item_id + 45, Coin.monster_coin, ItemClassification.progression_deprioritized),
    create_item(ITEM_CODE_START + gacha_item_id + 46, Coin.promotional_coin, ItemClassification.progression_deprioritized),
]

shop_item_id = 150
shop_items = [
    create_item(ITEM_CODE_START + shop_item_id + 1, QuestItem.fairy_bubble, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 2, Power.frilly_panties, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 3, Power.disarming_bell, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 4, Power.demonic_cuff, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 5, Power.ring_of_the_moon, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 6, Power.magical_mushroom, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 7, Power.ring_of_the_sun, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 8, Power.slime_sentry, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 9, Power.haunted_scythe, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 10, Accessory.fortune_cat, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 11, Accessory.heart_necklace, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 12, Accessory.star_bracelet, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 13, Accessory.cursed_talisman, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 14, Accessory.yellow_frog_talisman, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 15, Accessory.blue_frog_talisman, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 16, Accessory.mind_mushroom, ItemClassification.useful),
    # create_item(ITEM_CODE_START + shop_item_id + 17, Upgrade.portable_portal, ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 18, Costume.cat, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 19, Costume.goblin, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 20, Costume.nun, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 21, Costume.priest, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 22, Costume.miko, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 23, Costume.farmer, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 24, Costume.nurse, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 25, Costume.postman, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 26, Costume.maid, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 27, Costume.pigman, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 28, Costume.dominating, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + shop_item_id + 29, Costume.alchemist, ItemClassification.progression | ItemClassification.useful),

]

quest_item_id = 200
quest_items = [
    create_item(ITEM_CODE_START + quest_item_id + 1, QuestItem.goblin_headshot, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 2, QuestItem.business_card, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 3, QuestItem.vip_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 4, QuestItem.cowbell, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 5, QuestItem.gobliana_luggage, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 6, QuestItem.summon_stone, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 7, QuestItem.delicious_milk, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 8, QuestItem.belle_milkshake, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 9, QuestItem.cherry_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 10, QuestItem.mono_password, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 11, QuestItem.clothes, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 12, QuestItem.heavenly_daikon, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 13, QuestItem.hellish_dango, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 14, QuestItem.soul_fragment, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 15, QuestItem.legendary_halo, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 16, QuestItem.demonic_letter, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 17, QuestItem.angelic_letter, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 18, QuestItem.silky_slime, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 19, QuestItem.red_wine, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 20, QuestItem.blue_jelly_mushroom, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 21, QuestItem.maid_contract, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 22, QuestItem.deed, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 23, QuestItem.mimic_chest, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 24, QuestItem.fungal, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 25, QuestItem.goblin_apartment, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 26, Custom.sex_experience, ItemClassification.progression_deprioritized),
    create_item(ITEM_CODE_START + quest_item_id + 27, Costume.bunny, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + quest_item_id + 28, Key.abandoned_apartment, ItemClassification.progression | ItemClassification.useful),
]

warp_item_id = 250
warp_items = [
    create_item(ITEM_CODE_START + warp_item_id + 1, Warp.sensei, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 2, Warp.witchy, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 3, Warp.goblin, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 4, Warp.spirit, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 5, Warp.shady, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 6, Warp.ghost_entrance, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 7, Warp.ghost_castle, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 8, Warp.jigoku, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 9, Warp.club_demon, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 10, Warp.tengoku, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 11, Warp.angelic_hallway, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 12, Warp.fungal_forest, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 13, Warp.slime_citadel, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 14, Warp.slimy_depths, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + warp_item_id + 15, Warp.umi_umi, ItemClassification.progression | ItemClassification.useful),
    # create_item(ITEM_CODE_START + warp_item_id + 16, Warp.chaos_castle, ItemClassification.progression | ItemClassification.useful),
]

ability_item_id = 275
ability_items = [
    create_item(ITEM_CODE_START + ability_item_id + 1, Upgrade.rose_ribbon, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + ability_item_id + 2, Upgrade.orb_of_avoidance, ItemClassification.progression | ItemClassification.useful),
]

trap_item_id = 300
trap_items = [
    create_item(ITEM_CODE_START + trap_item_id + 1, Trap.nothing, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_item_id + 2, Trap.sexual_thoughts, ItemClassification.trap)
]


item_name_to_item = {item.name: item for item in all_items}

filler_items = [item for item in all_items if item.classification == ItemClassification.filler and item not in gacha_items]


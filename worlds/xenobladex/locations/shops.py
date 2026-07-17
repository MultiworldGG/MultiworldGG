from ..Locations import Loc as Data

# https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_Blueprint.html
shop_blueprints_data: list[Data] = [

]

# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_WpnPC.html
shop_weapons_data: list[Data] = [

]

# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_AmrPC.html
shop_armor_data: list[Data] = [

]

# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_ItemSkill_inner.html
shop_augments_data: list[Data] = [

]

# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_AssetDL.html
shop_dolls_data: list[Data] = [

]

# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_WpnDL.html
shop_doll_weapons_data: list[Data] = [

]

# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_AmrDL.html
shop_doll_armor_data: list[Data] = [

]

# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_ItemSkill_doll.html
shop_doll_augments_data: list[Data] = [

]

shops_data: list[Data] = [
    *shop_blueprints_data,
    *shop_weapons_data,
    *shop_armor_data,
    *shop_augments_data,
    *shop_dolls_data,
    *shop_doll_weapons_data,
    *shop_doll_armor_data,
    *shop_doll_augments_data
]

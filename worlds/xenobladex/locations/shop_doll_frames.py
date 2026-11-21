from . import Loc as Data

# flake8: noqa
# https://xenoblade.github.io/xbx/bdat/common_local_us/SHP_AssetDL.html
shop_doll_frames_data: list[Data] = [
Data("AS0130 Formula ST", rules=["Blade License"], depends=["Chapter 1"]),
Data("AS0150 Formula ST - Sakuraba 5", rules=["Blade License", "FNet"], depends=["Chapter 1"]),
Data("US0230 Urban ST", rules=["Blade License"], depends=["Chapter 1"]),
Data("US0250 Urban ST - Sakuraba 5", rules=["Blade License", "FNet"], depends=["Chapter 1"]),
Data("AS0330 Verus ST", rules=["Blade License"], depends=["Chapter 1"]),
Data("AS0350 Verus ST - Sakuraba 5", rules=["Blade License", "FNet"], depends=["Chapter 1"]),
Data("AS0430 Lailah ST", rules=["Blade License"], depends=["Chapter 1"]),
Data("AS0450 Lailah ST - Sakuraba 5", rules=["Blade License", "FNet"], depends=["Chapter 1"]),
Data("AS0530 Inferno ST", rules=["Blade License"], depends=["Chapter 1"]),
Data("AS0550 Inferno ST - Sakuraba 5", rules=["Blade License", "FNet"], depends=["Chapter 1"]),
Data("XS0630 Mastema ST", rules=["Blade License"], depends=["Chapter 1"]),
Data("XS0650 Mastema ST - Sakuraba 5", rules=["Blade License", "FNet"], depends=["Chapter 1"]),
Data("XS0730 Amdusias ST", rules=["Blade License"], depends=["Chapter 1"]),
Data("XS0750 Amdusias ST - Sakuraba 5", rules=["Blade License", "FNet"], depends=["Chapter 1"]),
]

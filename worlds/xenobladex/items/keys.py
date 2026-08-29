from BaseClasses import ItemClassification
from . import Itm as Data

# flake8: noqa
keys_data:list[Data] = [
Data("Skell License", count=0),
Data("Flight Module", count=0),
Data("Overdrive"),
Data("FNet"),
Data("Progressive License", count=3),
Data("Death", count=0),
Data("Filler", count=0, progression=ItemClassification.filler),
Data("Victory", count=0),
Data("PLACEHOLDER", valid=False),
Data("PLACEHOLDER", valid=False),
Data("PLACEHOLDER", valid=False),
Data("PLACEHOLDER", valid=False),
Data("DEBUG Kill Enemy", count=0),
Data("Level", count=0),
]

from . import Loc as Data

tmp_data: list[Data] = [
    Data("Chapter 1", rules=["Lvl 4"]),
    Data("Chapter 2", rules=["Lvl 5"], depends=["Chapter 1"], pooled=False),
    Data("Chapter 3", rules=["Lvl 10"], depends=["Chapter 2"], pooled=False),
    Data("Chapter 4", rules=["Prim 15", "Lvl 16"], depends=["Chapter 3", "The Probe-fessional", "BLADE Level Basics"],
         pooled=False),
    Data("Chapter 5", rules=["Lvl 20"], depends=["Chapter 4", "Renewed Will"], pooled=False),
    Data("Chapter 6", rules=["Noct 20", "Lvl 24"], depends=["Chapter 5", "A Friend in Need"], pooled=False),
    Data("Chapter 7", rules=["Obli 25", "Lvl 28"], depends=["Chapter 6", "Close Comrades"], pooled=False),
    Data("Chapter 8", rules=["Mira 10", "Lvl 31"], depends=["Chapter 7", "The Matchmaker"], pooled=False),
    Data("Chapter 9", rules=["Lvl 34"], depends=["Chapter 8", "Spy Games"], pooled=False),
    Data("Chapter 10", rules=["Sylv 15", "Lvl 39"], depends=["Chapter 9", "Manhunt"], pooled=False),
    Data("Chapter 11", rules=["Caul 10", "Lvl 45"], depends=["Chapter 10", "Boot Camp", "Nine Lives"], pooled=False),
    Data("Chapter 12", rules=["Lvl 50", "Flight Module"], depends=["Chapter 11", "A Girls Wings"], pooled=False),
]

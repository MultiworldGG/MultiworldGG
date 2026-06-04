import typing

class SlotOptions(typing.TypedDict):
    goal: str
    dlcActive: bool
    vtShadeLock: int | bool
    rhombusHubUnlock: bool
    meteorPassage: bool
    closedGaia: int
    vtSkip: bool
    keyrings: list[int]
    chestReveal: bool
    allowBoosterGrinding: bool
    questRando: bool
    hiddenQuestRewardMode: str
    hiddenQuestObfuscationLevel: str
    questDialogHints: bool
    progressiveChains: dict[int, list[int]]
    shopSendMode: str
    shopReceiveMode: str
    shopDialogHints: bool
    chestClearanceLevels: dict[int, str]
    botanicsCompletionAmount: int

class SlotData(typing.TypedDict):
    mode: str
    dataVersion: str
    apworldVersion: str
    options: SlotOptions

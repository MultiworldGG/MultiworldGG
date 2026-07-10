from dataclasses import dataclass

# ----------- Mirror Upgrade Locations -----------
@dataclass
class MirrorUpgradeData:
    name:str
    max_level:int

mirror_upgrades = [
    MirrorUpgradeData("Shadow Presence", 5),
    MirrorUpgradeData("Chthonic Vitality", 3),
    MirrorUpgradeData("Death Defiance", 3),
    MirrorUpgradeData("Greater Reflex", 1),
    MirrorUpgradeData("Boiling Blood", 5),
    MirrorUpgradeData("Infernal Soul", 2),
    MirrorUpgradeData("Deep Pockets", 10),
    MirrorUpgradeData("Thick Skin", 10),
    MirrorUpgradeData("Privileged Status", 2),
    MirrorUpgradeData("Olympian Favor", 40),
    MirrorUpgradeData("Gods' Pride", 20),
    MirrorUpgradeData("Fated Authority", 8),
    MirrorUpgradeData("Fiery Presence", 5),
    MirrorUpgradeData("Dark Regeneration", 2),
    MirrorUpgradeData("Stubborn Defiance", 1),
    MirrorUpgradeData("Ruthless Reflex", 1),
    MirrorUpgradeData("Abyssal Blood", 5),
    MirrorUpgradeData("Stygian Soul", 2),
    MirrorUpgradeData("Golden Touch", 3),
    MirrorUpgradeData("High Confidence", 5),
    MirrorUpgradeData("Family Favorite", 2),
    MirrorUpgradeData("Dark Foresight", 10),
    MirrorUpgradeData("Gods' Legacy", 10),
    MirrorUpgradeData("Fated Persuasion", 4),
]
#Routine inspection level categories
mirror_ri_requirements = {
    "Fated Authority": 1,
    "Fated Persuasion": 1,
    "Gods' Pride": 1,
    "Gods' Legacy": 1,
    "Olympian Favor": 1,
    "Dark Foresight": 1,

    "Privileged Status": 2,
    "Family Favorite": 2,
    "Thick Skin": 2,
    "High Confidence": 2,
    "Deep Pockets": 2,
    "Golden Touch": 2,

    "Infernal Soul": 3,
    "Stygian Soul": 3,
    "Boiling Blood": 3,
    "Abyssal Blood": 3,
    "Greater Reflex": 3,
    "Ruthless Reflex": 3,

    "Death Defiance": 4,
    "Stubborn Defiance": 4,
    "Chthonic Vitality": 4,
    "Dark Regeneration": 4,
    "Shadow Presence": 4,
    "Fiery Presence": 4,
}
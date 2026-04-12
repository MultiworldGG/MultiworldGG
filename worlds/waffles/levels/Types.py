from BaseClasses import Location
from rule_builder.rules import Rule, True_
from dataclasses import dataclass
from Enemies import EnemyData
from collections.abc import Callable


@dataclass
class SMWLocation():
    id: int
    name: str
    rule: Rule

    def __init__(self, id: int, name: str, rule: Rule = True_()):
        self.id = id
        self.name = name
        self.rule = rule


@dataclass
class SMWScreen():
    id: int
    name: str


@dataclass
class SMWLevel():
    name: str
    replaces: list[int]
    exit_rules: list[Rule]
    locations: list[SMWLocation]
    screens: list[SMWScreen]

    def __init__(self, 
                 name: str, 
                 replaces: list[int],
                 locations: list[SMWLocation],
                 exit_rules: list[Rule] = [True_()]):
        self.name = name
        self.replaces = replaces
        self.locations = locations
        self.exit_rules = exit_rules


@dataclass
class SMWLevelPack():
    name: str
    levels: list[SMWLevel]

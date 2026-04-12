from BaseClasses import Item


_PROGRESSION_MODEL: str = "Cog"
_USEFUL_MODEL: str = "Zoomer"
_FILLER_MODEL: str = "Nothing"
_TRAP_MODEL: str = "Ice Trap"
_NOT_FOUND_MODEL: str = "NOT_FOUND"
_OFFWORLD_MODELS: dict[str, dict[str, str]] = {
    "Metroid Fusion": {
        "Morph Ball": "Morph Ball",
        "Bomb Data": "Morph Ball Bomb",
        "Power Bomb Data": "Power Bomb",
        "Charge Beam": "Charge Beam",
        "Wave Beam": "Wave Beam",
        "Ice Beam": "Ice Beam",
        "Plasma Beam": "Plasma Beam",
        "Space Jump": "Space Jump Boots",
        "Varia Suit": "Varia Suit",
        "Gravity Suit": "Gravity Suit",
        "Missile Data": "Shiny Missile",
        "Missile Tank": "Missile",
        "Super Missile": "Super Missile",
        "Energy Tank": "Energy Tank",
    },
    "Metroid Zero Mission": {
        "Morph Ball": "Morph Ball",
        "Bomb": "Morph Ball Bomb",
        "Power Bomb Tank": "Power Bomb Expansion",
        "Charge Beam": "Charge Beam",
        "Wave Beam": "Wave Beam",
        "Ice Beam": "Ice Beam",
        "Plasma Beam": "Plasma Beam",
        "Space Jump": "Space Jump Boots",
        "Varia Suit": "Varia Suit",
        "Gravity Suit": "Gravity Suit",
        "Missile Tank": "Missile",
        "Energy Tank": "Energy Tank",
    },
    "SMZ3": {
        "Morph": "Morph Ball",
        "Bombs": "Morph Ball Bomb",
        "PowerBomb": "Power Bomb Expansion",
        "Charge": "Charge Beam",
        "Wave": "Wave Beam",
        "Ice": "Ice Beam",
        "Plasma": "Plasma Beam",
        "Grapple": "Grapple Beam",
        "SpaceJump": "Space Jump Boots",
        "Varia": "Varia Suit",
        "Gravity": "Gravity Suit",
        "Missile": "Missile",
        "ETank": "Energy Tank",
    },
    "Super Metroid": {
        "Morph Ball": "Morph Ball",
        "Bomb": "Morph Ball Bomb",
        "Power Bomb": "Power Bomb Expansion",
        "Charge Beam": "Charge Beam",
        "Wave Beam": "Wave Beam",
        "Ice Beam": "Ice Beam",
        "Plasma Beam": "Plasma Beam",
        "Grappling Beam": "Grapple Beam",
        "Space Jump": "Space Jump Boots",
        "Varia Suit": "Varia Suit",
        "Gravity Suit": "Gravity Suit",
        "Missile": "Missile",
    },
    "Super Metroid Map Rando": {
        "Morph": "Morph Ball",
        "Bombs": "Morph Ball Bomb",
        "PowerBomb": "Power Bomb Expansion",
        "Charge": "Charge Beam",
        "Wave": "Wave Beam",
        "Ice": "Ice Beam",
        "Plasma": "Plasma Beam",
        "Grapple": "Grapple Beam",
        "SpaceJump": "Space Jump Boots",
        "VariaSuit": "Varia Suit",
        "GravitySuit": "Gravity Suit",
        "ProgMissile": "Shiny Missile",
        "Missile": "Missile",
        "ETank": "Energy Tank",
    },
}


def get_offworld_model(item: Item, match_series: bool) -> Item:
    if match_series:
        offworld_model = (
            _OFFWORLD_MODELS.get(item.game, {})
                            .get(item.name, _NOT_FOUND_MODEL)
        )

        if offworld_model != _NOT_FOUND_MODEL:
            return offworld_model

    if item.advancement:
        return _PROGRESSION_MODEL
    if item.useful:
        return _USEFUL_MODEL
    if item.trap:
        return _TRAP_MODEL

    return _FILLER_MODEL
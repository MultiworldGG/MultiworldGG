from dataclasses import dataclass
from enum import Enum, auto

from .frozendict import frozendict
from typing_extensions import Self

from .common_types import ItemMessagesType
from .text import Language


class ItemMessagesKind(Enum):
    CUSTOM_MESSAGE = auto()
    MESSAGE_ID = auto()


@dataclass(frozen=True)
class ItemMessages:
    kind: ItemMessagesKind
    item_messages: frozendict[Language, str]
    centered: bool
    message_id: int

    @classmethod
    def from_json(cls, data: ItemMessagesType) -> Self:
        item_messages: dict[Language, str] = {}
        centered = True
        kind = ItemMessagesKind[data["kind"]]
        message_id = 0
        if kind == ItemMessagesKind.CUSTOM_MESSAGE:
            for lang_name, message in data["languages"].items():
                lang = Language[lang_name]
                item_messages[lang] = message
            centered = data.get("centered", True)
        else:
            message_id = data["message_id"]

        return cls(kind, frozendict(item_messages), centered, message_id)

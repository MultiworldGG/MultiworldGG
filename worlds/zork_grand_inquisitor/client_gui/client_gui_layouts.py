from typing import Dict, List, Optional, Set, Tuple

import NetUtils

from kvui import SelectableLabel

from kivy.core.text.markup import MarkupLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from ..client import ZorkGrandInquisitorContext
from ..data.entrance_randomizer_data import randomizable_entrances, randomizable_entrances_subway
from ..data.location_data import location_data
from ..data.mapping_data import entrance_names, entrance_names_reverse, hotspots_for_regional_hotspot
from ..data_funcs import location_names_to_location

from ..enums import (
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
)


class NotConnectedLayout(BoxLayout):
    ctx: ZorkGrandInquisitorContext

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(orientation="horizontal", size_hint_y=0.12)

        self.ctx = ctx

        self.add_widget(
            Label(text="Please connect to an Archipelago server first to view this tab.", font_size="24dp")
        )

    def show(self):
        self.opacity = 1.0
        self.size_hint_y = 0.12
        self.disabled = False

    def hide(self):
        self.opacity = 0.0
        self.size_hint_y = None
        self.height = "0dp"
        self.disabled = True


class ItemLabel(Label):
    ctx: ZorkGrandInquisitorContext

    item: ZorkGrandInquisitorItems
    received: bool
    count: int

    def __init__(self, ctx: ZorkGrandInquisitorContext, item: ZorkGrandInquisitorItems) -> None:
        super().__init__(
            text=item.value,
            font_size="16dp",
            size_hint_y=None,
            height="22dp",
            halign="left",
            valign="middle",
        )

        self.ctx = ctx

        self.item = item
        self.received = False
        self.count = 1

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    @property
    def is_goal_item(self) -> bool:
        return self.item in (
            ZorkGrandInquisitorItems.ARTIFACT_OF_MAGIC,
            ZorkGrandInquisitorItems.DEATH,
            ZorkGrandInquisitorItems.LANDMARK,
        )

    def update(self, received_items: Dict[ZorkGrandInquisitorItems, int]) -> None:
        if self.is_goal_item:
            self.count = received_items.get(self.item, 0)
            self.received = self.count > 0
        else:
            self.received = self.item in received_items

        if self.received:
            self.opacity = 1.0
        else:
            self.opacity = 0.25

        if self.count > 1:
            self.text = f"{self.item.value} x{self.count}"
        else:
            self.text = self.item.value


class ItemsLayout(ScrollView):
    ctx: ZorkGrandInquisitorContext

    layout: BoxLayout

    item_labels: Dict[ZorkGrandInquisitorItems, ItemLabel]

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(size_hint=(0.2, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.item_labels = dict()

        title_label: Label = Label(
            text="[b]Items[/b]",
            markup=True,
            font_size="20dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        title_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(title_label)

        items_goal: List[ZorkGrandInquisitorItems] = list()

        if self.ctx.game_controller.option_goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            items_goal.extend([
                ZorkGrandInquisitorItems.COCONUT_OF_QUENDOR,
                ZorkGrandInquisitorItems.CUBE_OF_FOUNDATION,
                ZorkGrandInquisitorItems.SKULL_OF_YORUK,
            ])
        elif self.ctx.game_controller.option_goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
            items_goal.append(ZorkGrandInquisitorItems.ARTIFACT_OF_MAGIC)
        elif self.ctx.game_controller.option_goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
            items_goal.append(ZorkGrandInquisitorItems.LANDMARK)
        elif self.ctx.game_controller.option_goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
            items_goal.append(ZorkGrandInquisitorItems.DEATH)

        if len(items_goal):
            item: ZorkGrandInquisitorItems
            for item in items_goal:
                item_label: ItemLabel = ItemLabel(self.ctx, item)

                self.item_labels[item] = item_label
                self.layout.add_widget(item_label)

            self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_inventory: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.CIGAR,
            ZorkGrandInquisitorItems.COCOA_INGREDIENTS,
            ZorkGrandInquisitorItems.HAMMER,
            ZorkGrandInquisitorItems.HUNGUS_LARD,
            ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.MEAD_LIGHT,
            ZorkGrandInquisitorItems.MONASTERY_ROPE,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
            ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE,
            ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.PROZORK_TABLET,
            ZorkGrandInquisitorItems.SANDWITCH_WRAPPER,
            ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS,
            ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV,
            ZorkGrandInquisitorItems.SHOVEL,
            ZorkGrandInquisitorItems.SNAPDRAGON,
            ZorkGrandInquisitorItems.STUDENT_ID,
            ZorkGrandInquisitorItems.SUBWAY_TOKEN,
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.WELL_ROPE,
            ZorkGrandInquisitorItems.ZIMDOR_SCROLL,
            ZorkGrandInquisitorItems.ZORK_ROCKS,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_inventory:
            item_label: ItemLabel = ItemLabel(self.ctx, item)

            self.item_labels[item] = item_label
            self.layout.add_widget(item_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_spells: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.SPELL_BEBURTT,
            ZorkGrandInquisitorItems.SPELL_GLORF,
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
            ZorkGrandInquisitorItems.SPELL_IGRAM,
            ZorkGrandInquisitorItems.SPELL_KENDALL,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_OBIDIL,
            ZorkGrandInquisitorItems.SPELL_REZROV,
            ZorkGrandInquisitorItems.SPELL_SNAVIG,
            ZorkGrandInquisitorItems.SPELL_THROCK,
            ZorkGrandInquisitorItems.SPELL_YASTARD,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_spells:
            item_label: ItemLabel = ItemLabel(self.ctx, item)

            self.item_labels[item] = item_label
            self.layout.add_widget(item_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_totems: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.TOTEM_BROG,
            ZorkGrandInquisitorItems.TOTEM_GRIFF,
            ZorkGrandInquisitorItems.TOTEM_LUCY,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_totems:
            item_label: ItemLabel = ItemLabel(self.ctx, item)

            self.item_labels[item] = item_label
            self.layout.add_widget(item_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_brog: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            ZorkGrandInquisitorItems.BROGS_PLANK,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_brog:
            item_label: ItemLabel = ItemLabel(self.ctx, item)

            self.item_labels[item] = item_label
            self.layout.add_widget(item_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_griff: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP,
            ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_griff:
            item_label: ItemLabel = ItemLabel(self.ctx, item)

            self.item_labels[item] = item_label
            self.layout.add_widget(item_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_lucy: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_lucy:
            item_label: ItemLabel = ItemLabel(self.ctx, item)

            self.item_labels[item] = item_label
            self.layout.add_widget(item_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        self.add_widget(self.layout)

        self.update()

    def update(self) -> None:
        received_items: Dict[ZorkGrandInquisitorItems, int] = dict()

        network_item: NetUtils.NetworkItem
        for network_item in self.ctx.items_received:
            if network_item.item in self.ctx.id_to_items:
                item: ZorkGrandInquisitorItems = self.ctx.id_to_items[network_item.item]

                received_items[item] = received_items.get(item, 0) + 1

        item_label: ItemLabel
        for item_label in self.item_labels.values():
            item_label.update(received_items)


class DestinationsHotspotsLabel(Label):
    ctx: ZorkGrandInquisitorContext

    item: ZorkGrandInquisitorItems
    received: bool

    def __init__(self, ctx: ZorkGrandInquisitorContext, item: ZorkGrandInquisitorItems) -> None:
        super().__init__(
            text=item.value,
            font_size="16dp",
            size_hint_y=None,
            height="22dp",
            halign="left",
            valign="middle",
        )

        self.ctx = ctx

        self.item = item
        self.received = False

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def update(self, received_items: Dict[ZorkGrandInquisitorItems, int]) -> None:
        self.received = self.item in received_items

        if self.received:
            self.opacity = 1.0
        else:
            self.opacity = 0.25


class DestinationsHotspotsLayout(ScrollView):
    ctx: ZorkGrandInquisitorContext

    layout: BoxLayout

    destination_hotspot_labels: Dict[ZorkGrandInquisitorItems, DestinationsHotspotsLabel]

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(size_hint=(0.35, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.destination_hotspot_labels = dict()

        title_label: Label = Label(
            text="[b]Destinations / Hotspots[/b]",
            markup=True,
            font_size="20dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        title_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(title_label)

        items_destinations_subway: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_destinations_subway:
            destination_hotspot_label: DestinationsHotspotsLabel = DestinationsHotspotsLabel(
                self.ctx, item
            )

            self.destination_hotspot_labels[item] = destination_hotspot_label
            self.layout.add_widget(destination_hotspot_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_destinations_teleporter: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_destinations_teleporter:
            destination_hotspot_label: DestinationsHotspotsLabel = DestinationsHotspotsLabel(
                self.ctx, item
            )

            self.destination_hotspot_labels[item] = destination_hotspot_label
            self.layout.add_widget(destination_hotspot_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_destinations_totemizer: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_NEWARK_NEW_JERSEY,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_destinations_totemizer:
            destination_hotspot_label: DestinationsHotspotsLabel = DestinationsHotspotsLabel(
                self.ctx, item
            )

            self.destination_hotspot_labels[item] = destination_hotspot_label
            self.layout.add_widget(destination_hotspot_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_hotspots: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX,
            ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS,
            ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX,
            ZorkGrandInquisitorItems.HOTSPOT_BLINDS,
            ZorkGrandInquisitorItems.HOTSPOT_BUCKET,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER,
            ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT,
            ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER,
            ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND,
            ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH,
            ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW,
            ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS,
            ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE,
            ZorkGrandInquisitorItems.HOTSPOT_ELECTRIC_FENCE,
            ZorkGrandInquisitorItems.HOTSPOT_FENCE_POWER_CORD,
            ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS,
            ZorkGrandInquisitorItems.HOTSPOT_GARDEN_SHED,
            ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE,
            ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL,
            ZorkGrandInquisitorItems.HOTSPOT_GUARDS_TENT,
            ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS,
            ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.HOTSPOT_HARRY,
            ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY,
            ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH,
            ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG,
            ZorkGrandInquisitorItems.HOTSPOT_MIRROR,
            ZorkGrandInquisitorItems.HOTSPOT_MONASTERY_EXHIBIT_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE,
            ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS,
            ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE,
            ZorkGrandInquisitorItems.HOTSPOT_RADIO_TOWER_CABLE,
            ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE,
            ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE,
            ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON,
            ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER,
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM,
            ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM,
            ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE,
            ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
        ]

        item: ZorkGrandInquisitorItems
        for item in items_hotspots:
            destination_hotspot_label: DestinationsHotspotsLabel = DestinationsHotspotsLabel(
                self.ctx, item
            )

            self.destination_hotspot_labels[item] = destination_hotspot_label
            self.layout.add_widget(destination_hotspot_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        self.add_widget(self.layout)

        self.update()

    def update(self) -> None:
        received_items: Dict[ZorkGrandInquisitorItems, int] = dict()

        network_item: NetUtils.NetworkItem
        for network_item in self.ctx.items_received:
            if network_item.item in self.ctx.id_to_items:
                item: ZorkGrandInquisitorItems = self.ctx.id_to_items[network_item.item]

                if item in hotspots_for_regional_hotspot:
                    hotspot: ZorkGrandInquisitorItems
                    for hotspot in hotspots_for_regional_hotspot[item]:
                        received_items[hotspot] = received_items.get(hotspot, 0) + 1

                    continue

                received_items[item] = received_items.get(item, 0) + 1

        destination_hotspot_label: DestinationsHotspotsLabel
        for destination_hotspot_label in self.destination_hotspot_labels.values():
            destination_hotspot_label.update(received_items)


class ItemsTabLayout(BoxLayout):
    ctx: ZorkGrandInquisitorContext

    layout_content: BoxLayout

    layout_items: ItemsLayout
    layout_destinations_hotspots: DestinationsHotspotsLayout

    layout_not_connected: NotConnectedLayout

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(orientation="vertical")

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if self.ctx.game_controller.save_ids is None:
            self.layout_not_connected.show()
            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_items = ItemsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_items)

            self.layout_destinations_hotspots = DestinationsHotspotsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_destinations_hotspots)

        self.layout_items.update()
        self.layout_destinations_hotspots.update()


class EntranceLabel(Label):
    ctx: ZorkGrandInquisitorContext

    entrance_name: str
    entrance_markup: str

    def __init__(self, ctx: ZorkGrandInquisitorContext, entrance_name: str, entrance_markup: str) -> None:
        super().__init__(
            text=entrance_markup,
            markup=True,
            font_size="16dp",
            size_hint_y=None,
            height="22dp",
            halign="left",
            valign="bottom",
        )

        self.ctx = ctx

        self.entrance_name = entrance_name
        self.entrance_markup = entrance_markup

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def update(self) -> None:
        if self.ctx.data_storage_key is not None and self.ctx.data_storage_key in self.ctx.stored_data:
            if self.entrance_name in self.ctx.stored_data[self.ctx.data_storage_key].get("discovered_entrances", list()):
                destination_entrance_name: str = self.ctx.entrance_randomizer_data_by_name[self.entrance_name]
                destination_region: ZorkGrandInquisitorRegions = entrance_names_reverse[destination_entrance_name][1]

                self.text = self.entrance_markup + f" [b][color=AF99EF]{destination_region.value}[/color][/b]"
            else:
                self.text = self.entrance_markup


class EntrancesContent(ScrollView):
    ctx: ZorkGrandInquisitorContext

    layout: BoxLayout

    entrance_labels: Dict[str, EntranceLabel]

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__()

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.entrance_labels = dict()

        allowable_entrances: Set[Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]] = set(
            randomizable_entrances
        )

        if self.ctx.game_controller.option_entrance_randomizer_include_subway_destinations:
            allowable_entrances.update(randomizable_entrances_subway)

        entrance_data: List[Tuple[str, str]] = list()

        regions: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        entrance_name: str
        for regions, entrance_name in entrance_names.items():
            if regions in allowable_entrances:
                entrance_data.append(
                    (
                        entrance_name,
                        f"[b][color=00FF7F]{regions[0].value}:[/color][/b] {entrance_name} >>>",
                    )
                )

        data: Tuple[str, str]
        for data in sorted(entrance_data, key=lambda x: x[1]):
            entrance_label: EntranceLabel = EntranceLabel(self.ctx, data[0], data[1])

            self.layout.add_widget(entrance_label)
            self.entrance_labels[data[0]] = entrance_label

        self.add_widget(self.layout)

    def update(self) -> None:
        entrance_name: str
        entrance_label: EntranceLabel
        for entrance_name, entrance_label in self.entrance_labels.items():
            entrance_label.update()


class EntrancesTabLayout(BoxLayout):
    ctx: ZorkGrandInquisitorContext

    layout_content: BoxLayout
    layout_content_entrances: EntrancesContent

    layout_not_connected: NotConnectedLayout

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(orientation="vertical")

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if self.ctx.game_controller.save_ids is None:
            self.layout_not_connected.show()

            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_content_entrances = EntrancesContent(self.ctx)
            self.layout_content.add_widget(self.layout_content_entrances)

        self.layout_content_entrances.update()



class ExplainButton(Button):
    location: Optional[ZorkGrandInquisitorLocations]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.location = None

    def on_press(self):
        popup: Popup = Popup(
            title=f"How do I check {self.location.value}?",
            content=Label(text=location_data[self.location].description),
            size_hint=(0.9, 0.2),
        )

        popup.open()


class TrackerPageLocationLabel(SelectableLabel):
    locations_by_name: Dict[str, ZorkGrandInquisitorLocations] = location_names_to_location()

    explain_button: ExplainButton

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.explain_button = ExplainButton(
            text="?",
            font_size=self.font_size,
            line_height=self.line_height,
            halign="center",
            size_hint=(None, None),
            width="20dp",
            opacity=0.0,
            disabled=True,
        )

        self.explain_button.text_size = (self.explain_button.width, None)

        self.add_widget(self.explain_button)

        self.bind(pos=self.place_explain_button, size=self.place_explain_button)

    def refresh_view_attrs(self, rv: RecycleView, index: int, data: Dict[str, str]) -> None:
        super().refresh_view_attrs(rv, index, data)

        text: str = "".join(part for part in MarkupLabel(text=data["text"]).markup if not part.startswith("["))
        location_name: str = text.split(" | ")[-1]

        if location_name in self.locations_by_name:
            self.explain_button.location = self.locations_by_name[location_name]
            self.explain_button.opacity = 1.0
            self.explain_button.disabled = False

            self.padding = ["24dp", "0dp", "0dp", "0dp"]
        else:
            self.explain_button.location = None
            self.explain_button.opacity = 0.0
            self.explain_button.disabled = True

            self.padding = ["0dp", "0dp", "0dp", "0dp"]

    def place_explain_button(self, _label: Label, _value: List[float]) -> None:
        self.explain_button.pos = self.pos
        self.explain_button.height = self.height

from typing import Dict, List, Set, Tuple

import NetUtils

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from ..client import ZorkGrandInquisitorContext
from ..data.entrance_randomizer_data import randomizable_entrances, randomizable_entrances_subway
from ..data.location_data import ZorkGrandInquisitorLocationData, location_data
from ..data.mapping_data import entrance_names, entrance_names_reverse, hotspots_for_regional_hotspot

from ..enums import (
    ZorkGrandInquisitorDeathsanity,
    ZorkGrandInquisitorEntranceRandomizer,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLandmarksanity,
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


class ExplainButton(Button):
    popup: Popup

    def __init__(self, popup: Popup = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.popup = popup

    def on_press(self):
        self.popup.open()


class TrackerLocationLabel(Label):
    ctx: ZorkGrandInquisitorContext

    region: ZorkGrandInquisitorRegions
    location: ZorkGrandInquisitorLocations

    checked: bool

    def __init__(
        self,
        ctx: ZorkGrandInquisitorContext,
        region: ZorkGrandInquisitorRegions,
        location: ZorkGrandInquisitorLocations,
    ) -> None:
        super().__init__(
            text=f"[b][color=00FF7F]{region.value}:[/color][/b]  {location.value}",
            markup=True,
            font_size="16dp",
            size_hint_y=None,
            height="22dp",
            halign="left",
            valign="middle",
        )

        self.ctx = ctx

        self.region = region
        self.location = location

        self.checked = False

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def update(self, discovered_regions: Set[ZorkGrandInquisitorRegions]) -> None:
        if self.region not in discovered_regions:
            self.opacity = 0.1
            return

        self.checked = self.location in self.ctx.ui_locations_checked

        if self.checked:
            self.opacity = 0.1
        else:
            self.opacity = 1.0


class TrackerLocationsLayout(ScrollView):
    ctx: ZorkGrandInquisitorContext

    layout: BoxLayout

    title_label: Label
    location_labels: Dict[ZorkGrandInquisitorLocations, TrackerLocationLabel]

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(size_hint=(0.45, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing="2dp")
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.location_labels = dict()

        self.title_label = Label(
            text=f"[b]Locations  ({len(self.ctx.checked_locations)} / {len(self.ctx.server_locations)})[/b]",
            markup=True,
            font_size="20dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        self.title_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(self.title_label)

        note_label: Label = Label(
            text="This location tracker does not spoil region access.\nYou will need to gain access to each region in-game to activate its location checks below.\nWild VOXAM and Teleport Traps may falsify which regions you have discovered in-game.\n\nThe tracker isn't able to determine what is in logic at a given time\nIf you require such functionality, the Zork APWorld is fully compatible with Universal Tracker, including map tracking.",
            font_size="12dp",
            size_hint_y=None,
            height="100dp",
            halign="left",
            valign="top",
            opacity=0.5,
        )

        note_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(note_label)

        locations_core: List[ZorkGrandInquisitorLocations] = [
            ZorkGrandInquisitorLocations.DONT_GO_SPENDING_IT_ALL_IN_ONE_PLACE,
            ZorkGrandInquisitorLocations.OLD_SCRATCH_WINNER,
            ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE,
            ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST,
            ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE,
            ZorkGrandInquisitorLocations.INVISIBLE_FLOWERS,
            ZorkGrandInquisitorLocations.THE_UNDERGROUND_UNDERGROUND,
            ZorkGrandInquisitorLocations.UMBRELLA_FLOWERS,
            ZorkGrandInquisitorLocations.AN_EXCELLENT_POPPING_UTENSIL,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM,
            ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT,
            ZorkGrandInquisitorLocations.INFLATUS_THE_ETERNAL,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS,
            ZorkGrandInquisitorLocations.BOING_BOING_BOING,
            ZorkGrandInquisitorLocations.BONK,
            ZorkGrandInquisitorLocations.EGGPLANTS,
            ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON,
            ZorkGrandInquisitorLocations.I_DONT_THINK_YOU_WOULDVE_WANTED_THAT_TO_WORK_ANYWAY,
            ZorkGrandInquisitorLocations.IT_DOESNT_APPEAR_TO_BE_FOOLED,
            ZorkGrandInquisitorLocations.ITS_PLAYING_A_LITTLE_HARD_TO_GET,
            ZorkGrandInquisitorLocations.LIT_SUNFLOWERS,
            ZorkGrandInquisitorLocations.MUSHROOM_HAMMERED,
            ZorkGrandInquisitorLocations.NOTHIN_LIKE_A_GOOD_STOGIE,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES,
            ZorkGrandInquisitorLocations.PROZORKED,
            ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED,
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO,
            ZorkGrandInquisitorLocations.YOUR_PUNY_WEAPONS_DONT_PHASE_ME_BABY,
            ZorkGrandInquisitorLocations.CASTLE_WATCHING_A_FIELD_GUIDE,
            ZorkGrandInquisitorLocations.DENIED_BY_THE_LAKE_MONSTER,
            ZorkGrandInquisitorLocations.FROBUARY_3_UNDERGROUNDHOG_DAY,
            ZorkGrandInquisitorLocations.HELLO_THIS_IS_SHONA_FROM_GURTH_PUBLISHING,
            ZorkGrandInquisitorLocations.NATURAL_AND_SUPERNATURAL_CREATURES_OF_QUENDOR,
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU,
            ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG,
            ZorkGrandInquisitorLocations.RIGHT_HELLO_YES_UH_THIS_IS_SNEFFLE,
            ZorkGrandInquisitorLocations.RIGHT_UH_SORRY_ITS_ME_AGAIN_SNEFFLE,
            ZorkGrandInquisitorLocations.TAMING_YOUR_SNAPDRAGON,
            ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL,
            ZorkGrandInquisitorLocations.YAD_GOHDNUORGREDNU_3_YRAUBORF,
            ZorkGrandInquisitorLocations.A_SMALLWAY,
            ZorkGrandInquisitorLocations.ALARM_SYSTEM_IS_DOWN,
            ZorkGrandInquisitorLocations.DUNCE_LOCKER,
            ZorkGrandInquisitorLocations.EMERGENCY_MAGICATRONIC_MESSAGE,
            ZorkGrandInquisitorLocations.GETTING_SOME_CHANGE,
            ZorkGrandInquisitorLocations.ITS_ALMOST_AS_IF_IT_WERE_INFINITE,
            ZorkGrandInquisitorLocations.LOOK_AN_ICE_CREAM_BAR,
            ZorkGrandInquisitorLocations.MIKES_PANTS,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO,
            ZorkGrandInquisitorLocations.RESTOCKED_ON_GRUESDAY,
            ZorkGrandInquisitorLocations.SUCKING_ROCKS,
            ZorkGrandInquisitorLocations.GUE_TECH_ENTRANCE_EXAM,
            ZorkGrandInquisitorLocations.PLEASE_DONT_THROCK_THE_GRASS,
            ZorkGrandInquisitorLocations.ARTIFACTS_EXPLAINED,
            ZorkGrandInquisitorLocations.BEBURTT_DEMYSTIFIED,
            ZorkGrandInquisitorLocations.BETTER_SPELL_MANUFACTURING_IN_UNDER_10_MINUTES,
            ZorkGrandInquisitorLocations.CAVES_NOTES,
            ZorkGrandInquisitorLocations.CRISIS_AVERTED,
            ZorkGrandInquisitorLocations.HOW_TO_WIN_AT_DOUBLE_FANUCCI,
            ZorkGrandInquisitorLocations.THE_ONLY_WAY_TO_WIN_IS_NOT_TO_PLAY,
            ZorkGrandInquisitorLocations.TIME_TRAVEL_FOR_DUMMIES,
            ZorkGrandInquisitorLocations.HEY_FREE_DIRT,
            ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER,
            ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE,
            ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY,
            ZorkGrandInquisitorLocations.I_AM_NOT_IMPRESSED,
            ZorkGrandInquisitorLocations.NO_ONE_RETURNS_FROM_HADES,
            ZorkGrandInquisitorLocations.NOW_YOU_LOOK_LIKE_US_WHICH_IS_AN_IMPROVEMENT,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL,
            ZorkGrandInquisitorLocations.HAVE_A_HELL_OF_A_DAY,
            ZorkGrandInquisitorLocations.MAKE_LOVE_NOT_WAR,
            ZorkGrandInquisitorLocations.HMMM_INFORMATIVE_YET_DEEPLY_DISTURBING,
            ZorkGrandInquisitorLocations.PERMASEAL,
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL,
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC,
            ZorkGrandInquisitorLocations.ME_I_AM_THE_BOSS_OF_YOU,
            ZorkGrandInquisitorLocations.TOTEMIZED_DAILY_BILLBOARD,
            ZorkGrandInquisitorLocations.ELSEWHERE,
            ZorkGrandInquisitorLocations.ARREST_THE_VANDAL,
            ZorkGrandInquisitorLocations.CUT_THAT_OUT_YOU_LITTLE_CREEP,
            ZorkGrandInquisitorLocations.FIRE_FIRE,
            ZorkGrandInquisitorLocations.GO_AWAY,
            ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE,
            ZorkGrandInquisitorLocations.I_DONT_WANT_NO_TROUBLE,
            ZorkGrandInquisitorLocations.IM_COMPLETELY_NUDE,
            ZorkGrandInquisitorLocations.ITS_ONE_OF_THOSE_ADVENTURERS_AGAIN,
            ZorkGrandInquisitorLocations.MEAD_LIGHT,
            ZorkGrandInquisitorLocations.NO_AUTOGRAPHS,
            ZorkGrandInquisitorLocations.NO_BONDAGE,
            ZorkGrandInquisitorLocations.ONLY_YOU_CAN_PREVENT_FOOZLE_FIRES,
            ZorkGrandInquisitorLocations.TALK_TO_ME_GRAND_INQUISITOR,
            ZorkGrandInquisitorLocations.THATS_A_ROPE,
            ZorkGrandInquisitorLocations.THATS_THE_SPIRIT,
            ZorkGrandInquisitorLocations.WHAT_ARE_YOU_STUPID,
            ZorkGrandInquisitorLocations.YOU_ONE_OF_THEM_AGITATORS_AINT_YA,
            ZorkGrandInquisitorLocations.YOU_WANT_A_PIECE_OF_ME_DOCK_BOY,
            ZorkGrandInquisitorLocations.PLANETFALL,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE,
            ZorkGrandInquisitorLocations.DINGWHACKER_DELUXE,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER,
            ZorkGrandInquisitorLocations.UM_AH_UM_AH_UM_AH,
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO_PAST,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER,
            ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED,
            ZorkGrandInquisitorLocations.SPELL_CHECK_COMPLETE,
            ZorkGrandInquisitorLocations.ZIMDOR_IS_UNDAMAGED,
            ZorkGrandInquisitorLocations.FAT_LOT_OF_GOOD_THATLL_DO_YA,
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE,
            ZorkGrandInquisitorLocations.I_SPIT_ON_YOUR_FILTHY_COINAGE,
            ZorkGrandInquisitorLocations.PURPLE_BEAST_ALARM_SYSTEM,
            ZorkGrandInquisitorLocations.THATS_STILL_A_ROPE,
            ZorkGrandInquisitorLocations.YOU_DONT_GO_MESSING_WITH_A_MANS_ZIPPER,
            ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS,
            ZorkGrandInquisitorLocations.BRAVE_SOULS_WANTED,
            ZorkGrandInquisitorLocations.ENJOY_YOUR_TRIP,
            ZorkGrandInquisitorLocations.THATS_IT_JUST_KEEP_HITTING_THOSE_BUTTONS,
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE,
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY,
            ZorkGrandInquisitorLocations.FLOOD_CONTROL_DAM_3_THE_NOT_REMOTELY_BORING_TALE,
            ZorkGrandInquisitorLocations.SOUVENIR,
            ZorkGrandInquisitorLocations.USELESS_BUT_FUN,
            ZorkGrandInquisitorLocations.HOW_TO_HYPNOTIZE_YOURSELF,
            ZorkGrandInquisitorLocations.VOYAGE_OF_CAPTAIN_ZAHAB,
            ZorkGrandInquisitorLocations.WOW_IVE_NEVER_GONE_INSIDE_HIM_BEFORE,
            ZorkGrandInquisitorLocations.DOOOOOOWN,
            ZorkGrandInquisitorLocations.DOWN,
            ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL,
            ZorkGrandInquisitorLocations.UP,
            ZorkGrandInquisitorLocations.UUUUUP,
            ZorkGrandInquisitorLocations.BROG_DO_GOOD,
            ZorkGrandInquisitorLocations.BROG_EAT_ROCKS,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME,
            ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG,
            ZorkGrandInquisitorLocations.HMMM_BIG_TOOTHPICK,
            ZorkGrandInquisitorLocations.WHOOPS,
        ]

        if self.ctx.game_controller.option_goal != ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            locations_core.remove(ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT)
            locations_core.remove(ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG)
            locations_core.remove(ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP)

        location: ZorkGrandInquisitorLocations
        for location in locations_core:
            row_layout: BoxLayout = BoxLayout(orientation="horizontal", size_hint_y=None, height="22dp", spacing="6dp")

            data: ZorkGrandInquisitorLocationData = location_data[location]

            popup: Popup = Popup(
                title=f"How do I check {location.value}?",
                content=Label(text=data.description),
                size_hint=(0.6, 0.2),
            )

            explain_button: ExplainButton = ExplainButton(
                text="?",
                width="16dp",
                size_hint_x=None,
                popup=popup,
            )

            row_layout.add_widget(explain_button)

            location_label: TrackerLocationLabel = TrackerLocationLabel(
                self.ctx,
                data.region,
                location,
            )

            self.location_labels[location] = location_label
            row_layout.add_widget(location_label)

            self.layout.add_widget(row_layout)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        if self.ctx.game_controller.option_deathsanity == ZorkGrandInquisitorDeathsanity.ON:
            locations_deathsanity: List[ZorkGrandInquisitorLocations] = [
                ZorkGrandInquisitorLocations.DEATH_LOST_SOUL_TO_OLD_SCRATCH,
                ZorkGrandInquisitorLocations.DEATH_CLIMBED_OUT_OF_THE_WELL,
                ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON,
                ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES,
                ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES,
                ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE,
                ZorkGrandInquisitorLocations.DEATH_ZORK_ROCKS_EXPLODED,
                ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS,
                ZorkGrandInquisitorLocations.DEATH_JUMPED_IN_BOTTOMLESS_PIT,
                ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_INFINITY,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_NEWARK_NEW_JERSEY,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_SURFACE_OF_MERZ,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_STRAIGHT_TO_HELL,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_NEWARK_NEW_JERSEY,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_HALLS_OF_INQUISITION,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_INFINITY,
                ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_SURFACE_OF_MERZ,
                ZorkGrandInquisitorLocations.DEATH_ARRESTED_WITH_JACK,
                ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER,
                ZorkGrandInquisitorLocations.DEATH_SLICED_UP_BY_THE_INVISIBLE_GUARD,
                ZorkGrandInquisitorLocations.DEATH_EATEN_BY_A_GRUE
            ]

            self.layout.add_widget(
                Label(
                    text="[b]Deathsanity[/b]",
                    markup=True,
                    font_size="18dp",
                    size_hint_y=None,
                    height="36dp",
                    halign="left",
                    valign="top",
                )
            )

            location: ZorkGrandInquisitorLocations
            for location in locations_deathsanity:
                row_layout: BoxLayout = BoxLayout(orientation="horizontal", size_hint_y=None, height="22dp", spacing="6dp")

                data: ZorkGrandInquisitorLocationData = location_data[location]

                popup: Popup = Popup(
                    title=f"How do I check {location.value}?",
                    content=Label(text=data.description),
                    size_hint=(0.6, 0.2),
                )

                explain_button: ExplainButton = ExplainButton(
                    text="?",
                    width="16dp",
                    size_hint_x=None,
                    popup=popup,
                )

                row_layout.add_widget(explain_button)

                location_label: TrackerLocationLabel = TrackerLocationLabel(
                    self.ctx,
                    data.region,
                    location,
                )

                self.location_labels[location] = location_label
                row_layout.add_widget(location_label)

                self.layout.add_widget(row_layout)

            self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        if self.ctx.game_controller.option_landmarksanity == ZorkGrandInquisitorLandmarksanity.ON:
            locations_landmarksanity: List[ZorkGrandInquisitorLocations] = [
                ZorkGrandInquisitorLocations.LANDMARK_GREAT_UNDERGROUND_EMPIRE_ENTRANCE,
                ZorkGrandInquisitorLocations.LANDMARK_UMBRELLA_TREE,
                ZorkGrandInquisitorLocations.LANDMARK_UNDERGROUND_UNDERGROUND_ENTRANCE,
                ZorkGrandInquisitorLocations.LANDMARK_DRAGON_ARCHIPELAGO,
                ZorkGrandInquisitorLocations.LANDMARK_DUNGEON_MASTERS_HOUSE,
                ZorkGrandInquisitorLocations.LANDMARK_MIRROR_ROOM,
                ZorkGrandInquisitorLocations.LANDMARK_GUE_TECH_FOUNTAIN_INSIDE,
                ZorkGrandInquisitorLocations.LANDMARK_INFINITE_CORRIDOR,
                ZorkGrandInquisitorLocations.LANDMARK_GUE_TECH_FOUNTAIN_OUTSIDE,
                ZorkGrandInquisitorLocations.LANDMARK_GATES_OF_HELL,
                ZorkGrandInquisitorLocations.LANDMARK_HADES_SHORE,
                ZorkGrandInquisitorLocations.LANDMARK_TOTEMIZER,
                ZorkGrandInquisitorLocations.LANDMARK_INQUISITION_HEADQUARTERS,
                ZorkGrandInquisitorLocations.LANDMARK_PORT_FOOZLE,
                ZorkGrandInquisitorLocations.LANDMARK_JACKS_SHOP,
                ZorkGrandInquisitorLocations.LANDMARK_PAST_PORT_FOOZLE,
                ZorkGrandInquisitorLocations.LANDMARK_SPELL_CHECKER,
                ZorkGrandInquisitorLocations.LANDMARK_FLOOD_CONTROL_DAM_3,
                ZorkGrandInquisitorLocations.LANDMARK_WALKING_CASTLES_HEART,
                ZorkGrandInquisitorLocations.LANDMARK_WHITE_HOUSE,
            ]

            self.layout.add_widget(
                Label(
                    text="[b]Landmarksanity[/b]",
                    markup=True,
                    font_size="18dp",
                    size_hint_y=None,
                    height="36dp",
                    halign="left",
                    valign="top",
                )
            )

            location: ZorkGrandInquisitorLocations
            for location in locations_landmarksanity:
                row_layout: BoxLayout = BoxLayout(orientation="horizontal", size_hint_y=None, height="22dp", spacing="6dp")

                data: ZorkGrandInquisitorLocationData = location_data[location]

                popup: Popup = Popup(
                    title=f"How do I check {location.value}?",
                    content=Label(text=data.description),
                    size_hint=(0.6, 0.2),
                )

                explain_button: ExplainButton = ExplainButton(
                    text="?",
                    width="16dp",
                    size_hint_x=None,
                    popup=popup,
                )

                row_layout.add_widget(explain_button)

                location_label: TrackerLocationLabel = TrackerLocationLabel(
                    self.ctx,
                    data.region,
                    location,
                )

                self.location_labels[location] = location_label
                row_layout.add_widget(location_label)

                self.layout.add_widget(row_layout)

            self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        self.add_widget(self.layout)

        self.update()

    def update(self) -> None:
        discovered_regions: Set[ZorkGrandInquisitorRegions] = set()

        if self.ctx.data_storage_key is not None and self.ctx.data_storage_key in self.ctx.stored_data:
            region_name: str
            for region_name in self.ctx.stored_data[self.ctx.data_storage_key].get("discovered_regions", list()):
                discovered_regions.add(ZorkGrandInquisitorRegions(region_name))

        received_items: Set[ZorkGrandInquisitorItems] = set()

        network_item: NetUtils.NetworkItem
        for network_item in self.ctx.items_received:
            if network_item.item in self.ctx.id_to_items:
                received_items.add(self.ctx.id_to_items[network_item.item])

        location_label: TrackerLocationLabel
        for location_label in self.location_labels.values():
            location_label.update(discovered_regions)

        self.title_label.text = (
            f"[b]Locations  ({len(self.ctx.checked_locations)} / {len(self.ctx.server_locations)}, {len(discovered_regions) - 1} Region(s) Discovered)[/b]"
        )


class TrackerItemLabel(Label):
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


class TrackerItemsLayout(ScrollView):
    ctx: ZorkGrandInquisitorContext

    layout: BoxLayout

    item_labels: Dict[ZorkGrandInquisitorItems, TrackerItemLabel]

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
                item_label: TrackerItemLabel = TrackerItemLabel(self.ctx, item)

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
            item_label: TrackerItemLabel = TrackerItemLabel(self.ctx, item)

            self.item_labels[item] = item_label
            self.layout.add_widget(item_label)

        self.layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        items_spells: List[ZorkGrandInquisitorItems] = [
            ZorkGrandInquisitorItems.SPELL_BEBURTT,
            ZorkGrandInquisitorItems.SPELL_GLORF,
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
            ZorkGrandInquisitorItems.SPELL_IGRAM,
            ZorkGrandInquisitorItems.SPELL_KENDALL,
            ZorkGrandInquisitorItems.SPELL_OBIDIL,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_REZROV,
            ZorkGrandInquisitorItems.SPELL_SNAVIG,
            ZorkGrandInquisitorItems.SPELL_THROCK,
            ZorkGrandInquisitorItems.SPELL_YASTARD
        ]

        item: ZorkGrandInquisitorItems
        for item in items_spells:
            item_label: TrackerItemLabel = TrackerItemLabel(self.ctx, item)

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
            item_label: TrackerItemLabel = TrackerItemLabel(self.ctx, item)

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
            item_label: TrackerItemLabel = TrackerItemLabel(self.ctx, item)

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
            item_label: TrackerItemLabel = TrackerItemLabel(self.ctx, item)

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
            item_label: TrackerItemLabel = TrackerItemLabel(self.ctx, item)

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

        item_label: TrackerItemLabel
        for item_label in self.item_labels.values():
            item_label.update(received_items)


class TrackerDestinationsHotspotsLabel(Label):
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


class TrackerDestinationsHotspotsLayout(ScrollView):
    ctx: ZorkGrandInquisitorContext

    layout: BoxLayout

    destination_hotspot_labels: Dict[ZorkGrandInquisitorItems, TrackerDestinationsHotspotsLabel]

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
            destination_hotspot_label: TrackerDestinationsHotspotsLabel = TrackerDestinationsHotspotsLabel(
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
            destination_hotspot_label: TrackerDestinationsHotspotsLabel = TrackerDestinationsHotspotsLabel(
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
            destination_hotspot_label: TrackerDestinationsHotspotsLabel = TrackerDestinationsHotspotsLabel(
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
            ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS,
            ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE,
            ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL,
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
            ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE,
            ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS,
            ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE,
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
            destination_hotspot_label: TrackerDestinationsHotspotsLabel = TrackerDestinationsHotspotsLabel(
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

        destination_hotspot_label: TrackerDestinationsHotspotsLabel
        for destination_hotspot_label in self.destination_hotspot_labels.values():
            destination_hotspot_label.update(received_items)


class TrackerTabLayout(BoxLayout):
    ctx: ZorkGrandInquisitorContext

    layout_content: BoxLayout

    layout_locations: TrackerLocationsLayout
    layout_items: TrackerItemsLayout
    layout_destinations_hotspots: TrackerDestinationsHotspotsLayout

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
            self.layout_locations = TrackerLocationsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_locations)

            self.layout_items = TrackerItemsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_items)

            self.layout_destinations_hotspots = TrackerDestinationsHotspotsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_destinations_hotspots)

        self.layout_locations.update()
        self.layout_items.update()
        self.layout_destinations_hotspots.update()


class NoEntranceRandomizerLayout(BoxLayout):
    ctx: ZorkGrandInquisitorContext

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(orientation="horizontal", size_hint_y=0.08)

        self.ctx = ctx

        self.add_widget(
            Label(text="No entrances to track. This seed doesn't use the entrance randomizer.", font_size="24dp")
        )

    def show(self):
        self.opacity = 1.0
        self.size_hint_y = 0.08
        self.disabled = False

    def hide(self):
        self.opacity = 0.0
        self.size_hint_y = None
        self.height = "0dp"
        self.disabled = True


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
    layout_no_entrance_randomizer: NoEntranceRandomizerLayout

    def __init__(self, ctx: ZorkGrandInquisitorContext) -> None:
        super().__init__(orientation="vertical")

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_no_entrance_randomizer = NoEntranceRandomizerLayout(self.ctx)
        self.layout_no_entrance_randomizer.hide()
        self.add_widget(self.layout_no_entrance_randomizer)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if self.ctx.game_controller.save_ids is None:
            self.layout_not_connected.show()

            self.layout_content.clear_widgets()
            self.layout_no_entrance_randomizer.hide()

            return

        allowable_entrance_randomizer_values: Set[ZorkGrandInquisitorEntranceRandomizer] = {
            ZorkGrandInquisitorEntranceRandomizer.COUPLED,
            ZorkGrandInquisitorEntranceRandomizer.UNCOUPLED,
        }

        if self.ctx.game_controller.option_entrance_randomizer not in allowable_entrance_randomizer_values:
            self.layout_no_entrance_randomizer.show()

            self.layout_content.clear_widgets()
            self.layout_not_connected.hide()

            return

        self.layout_not_connected.hide()
        self.layout_no_entrance_randomizer.hide()

        if not len(self.layout_content.children):
            self.layout_content_entrances = EntrancesContent(self.ctx)
            self.layout_content.add_widget(self.layout_content_entrances)

        self.layout_content_entrances.update()

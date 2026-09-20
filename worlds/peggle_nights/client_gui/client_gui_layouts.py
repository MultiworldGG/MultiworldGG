from typing import Any, Dict, List, Optional

import io
import pkgutil

import NetUtils

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage

from kivy.graphics import Color, Line, Rectangle

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from ..client import PeggleNightsContext

from ..data.mapping_data import character_to_ids, level_to_stage_levels

from ..enums import (
    PeggleNightsAPGoals,
    PeggleNightsAPItems,
    PeggleNightsAPUsefulItems,
    PeggleNightsCharacters,
    PeggleNightsContexts,
    PeggleNightsLevels,
)

from ..game_state_manager import GameStateManager, GameState

from .. import client_gui


class NotConnectedLayout(BoxLayout):
    ctx: PeggleNightsContext

    def __init__(self, ctx: PeggleNightsContext) -> None:
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


class PeggleNightsLevelInformationLayout(BoxLayout):
    ctx: PeggleNightsContext

    game_state_manager: GameStateManager

    information_label: Label

    shadow_pegs_label: Label
    goal_label: Label

    level_information_level_image: Image
    level_information_master_image: Image
    level_information_title: Label
    level_information_subtitle: Label

    target_score_low_label: Label
    target_score_mid_label: Label
    target_score_high_label: Label

    item_full_clear_discount_label: Label
    item_score_multiplier_label: Label
    item_target_score_discount_label: Label

    score_label: Label
    shot_score_label: Label
    orange_peg_combo_label: Label
    peg_combo_label: Label
    pegs_cleared: Label

    level_locations_in_logic_label: Label
    level_locations_out_of_logic_label: Label

    last_seen_level: Optional[PeggleNightsLevels]
    last_seen_master: Optional[PeggleNightsCharacters]

    def __init__(self, ctx: PeggleNightsContext) -> None:
        super().__init__(orientation="vertical", size_hint_y=None, height="200dp", spacing="8dp",)

        self.bind(minimum_height=self.setter("height"))

        self.ctx = ctx

        self.game_state_manager = GameStateManager()

        # Game Information
        self.information_label = Label(
            text=f"[b]Game Information[/b]",
            markup=True,
            font_size="32dp",
            size_hint_y=None,
            height="38dp",
            halign="left",
            valign="middle",
        )

        self.information_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(self.information_label)

        goal_header_layout: BoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="74dp",
            spacing="8dp",
            padding=[0, 0, 0, 10]
        )

        goal_header_layout.bind(minimum_height=goal_header_layout.setter("height"))

        # Shadow Pegs
        self.shadow_pegs_label: Label = Label(
            text=(
                f"[b]Shadow Pegs[/b]\n"
                f"Retrieved [color=00FA9A]0[/color] of "
                f"[color=00FA9A]{self.ctx.game_controller.option_shadow_pegs_required}[/color] needed "
                f"([color=888888]{self.ctx.game_controller.option_shadow_pegs_total} total[/color])"
            ),
            markup=True,
            size_hint_x=40,
            size_hint_y=None,
            height="60dp",
            halign="left",
            valign="middle",
        )

        self.shadow_pegs_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        goal_header_layout.add_widget(self.shadow_pegs_label)

        # Goal
        self.goal_label: Label = Label(
            text=(
                f"[b]Goal[/b]\n"
                f"Retrieve the Shadow Pegs and Complete 11-5!"
            ),
            markup=True,
            size_hint_x=60,
            size_hint_y=None,
            height="60dp",
            halign="left",
            valign="middle",
        )

        self.goal_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        goal_header_layout.add_widget(self.goal_label)

        self.add_widget(goal_header_layout)

        # Level Information
        level_information_layout: BoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="163dp",
            spacing="8dp",
            padding=[0, 0, 0, 15]
        )

        level_information_layout.bind(minimum_height=level_information_layout.setter("height"))

        self.level_information_level_image = Image(
            size=(148, 148),
            size_hint=(None, None),
            allow_stretch=True,
            opacity=0.1
        )

        level_information_layout.add_widget(self.level_information_level_image)

        self.level_information_master_image = Image(
            size=(148, 148),
            size_hint=(None, None),
            allow_stretch=True,
            opacity=0.1
        )

        level_information_layout.add_widget(self.level_information_master_image)

        level_information_text_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="148dp",
            spacing="5dp",
        )

        level_information_text_layout.bind(minimum_height=level_information_text_layout.setter("height"))

        self.level_information_title = Label(
            text=f"[b]Begin Playing a Quick Play Level...[/b]",
            markup=True,
            size_hint_y=None,
            font_size="18dp",
            height="22dp",
            halign="left",
            valign="middle",
        )

        self.level_information_title.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_text_layout.add_widget(self.level_information_title)

        self.level_information_subtitle = Label(
            text=f"[b]This level is not included this seed.[/b]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="29dp",
            halign="left",
            valign="middle",
            padding=[0, 0, 0, 15]
        )

        self.level_information_subtitle.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_text_layout.add_widget(self.level_information_subtitle)

        level_information_text_sublayout: BoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="78dp",
            spacing="8dp",
        )

        level_information_text_sublayout.bind(minimum_height=level_information_text_sublayout.setter("height"))

        level_information_targets_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="78dp",
            spacing="4dp",
            size_hint_x=50,
        )

        level_information_targets_layout.bind(minimum_height=level_information_targets_layout.setter("height"))

        targets_label: Label = Label(
            text="[b]Target Scores[/b]",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        targets_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_targets_layout.add_widget(targets_label)

        self.target_score_low_label = Label(
            text="Low: [color=00FA9A]XXX,XXX[/color]",
            markup=True,
            size_hint_y=None,
            font_size="14dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.target_score_low_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_targets_layout.add_widget(self.target_score_low_label)

        self.target_score_mid_label = Label(
            text="Mid: [color=00FA9A]XXX,XXX[/color]",
            markup=True,
            size_hint_y=None,
            font_size="14dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.target_score_mid_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_targets_layout.add_widget(self.target_score_mid_label)

        self.target_score_high_label = Label(
            text="High: [color=00FA9A]XXX,XXX[/color]",
            markup=True,
            size_hint_y=None,
            font_size="14dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.target_score_high_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_targets_layout.add_widget(self.target_score_high_label)

        level_information_items_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="78dp",
            spacing="8dp",
            size_hint_x=50,
        )

        level_information_items_layout.bind(minimum_height=level_information_items_layout.setter("height"))

        items_label: Label = Label(
            text="",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="14dp",
            halign="left",
            valign="middle",
        )

        items_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_items_layout.add_widget(items_label)

        self.item_full_clear_discount_label = Label(
            text="Full Clear Discount: [color=00FA9A]Xx[/color]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="14dp",
            halign="left",
            valign="middle",
        )

        self.item_full_clear_discount_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_items_layout.add_widget(self.item_full_clear_discount_label)

        self.item_score_multiplier_label = Label(
            text="Score Multiplier: [color=00FA9A]Xx[/color]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="14dp",
            halign="left",
            valign="middle",
        )

        self.item_score_multiplier_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_items_layout.add_widget(self.item_score_multiplier_label)

        self.item_target_score_discount_label = Label(
            text="Target Score Discount: [color=00FA9A]Xx[/color]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="14dp",
            halign="left",
            valign="middle",
        )

        self.item_target_score_discount_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        level_information_items_layout.add_widget(self.item_target_score_discount_label)

        level_information_text_sublayout.add_widget(level_information_targets_layout)
        level_information_text_sublayout.add_widget(level_information_items_layout)

        level_information_text_layout.add_widget(level_information_text_sublayout)

        level_information_layout.add_widget(level_information_text_layout)

        self.add_widget(level_information_layout)

        in_level_information_layout: BoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            spacing="8dp",
            padding=[0, 0, 0, 10]
        )

        in_level_information_layout.bind(minimum_height=in_level_information_layout.setter("height"))

        statistics_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            pos_hint={"top": 1},
            spacing="6dp",
        )

        statistics_layout.bind(minimum_height=statistics_layout.setter("height"))

        score_label: Label
        shot_score_label: Label
        orange_peg_combo_label: Label
        peg_combo_label: Label
        pegs_cleared: Label

        self.score_label = Label(
            text="[b]Score:[/b] 0  [color=888888]0[/color]",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        self.score_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        statistics_layout.add_widget(self.score_label)

        self.shot_score_label = Label(
            text="[b]Shot Score:[/b] 0  [color=888888]0[/color]",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        self.shot_score_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        statistics_layout.add_widget(self.shot_score_label)

        self.orange_peg_combo_label = Label(
            text="[b]Orange Peg Combo:[/b] 0",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        self.orange_peg_combo_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        statistics_layout.add_widget(self.orange_peg_combo_label)

        self.peg_combo_label = Label(
            text="[b]Peg Combo:[/b] 0",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        self.peg_combo_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        statistics_layout.add_widget(self.peg_combo_label)

        self.pegs_cleared = Label(
            text="[b]Pegs Cleared:[/b] 0",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        self.pegs_cleared.bind(size=lambda label, size: setattr(label, "text_size", size))

        statistics_layout.add_widget(self.pegs_cleared)

        in_level_information_layout.add_widget(statistics_layout)

        locations_in_logic_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            pos_hint={"top": 1},
            spacing="6dp",
        )

        locations_in_logic_layout.bind(minimum_height=locations_in_logic_layout.setter("height"))

        locations_in_logic_label = Label(
            text="[b]In Logic Locations[/b]",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        locations_in_logic_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        locations_in_logic_layout.add_widget(locations_in_logic_label)

        self.level_locations_in_logic_label = Label(
            text="No locations accessible in logic",
            markup=True,
            size_hint_y=None,
            font_size="13dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.level_locations_in_logic_label.bind(texture_size=lambda label, texture_size: setattr(label, "height", texture_size[1]))
        self.level_locations_in_logic_label.bind(width=lambda label, width: setattr(label, "text_size", (width, None)))

        locations_in_logic_layout.add_widget(self.level_locations_in_logic_label)

        if self.ctx.tracker_loaded:
            in_level_information_layout.add_widget(locations_in_logic_layout)

        locations_out_of_logic_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            pos_hint={"top": 1},
            spacing="6dp",
        )

        locations_out_of_logic_layout.bind(minimum_height=locations_out_of_logic_layout.setter("height"))

        locations_out_of_logic_label = Label(
            text="[b]Out of Logic Locations[/b]",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        locations_out_of_logic_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        locations_out_of_logic_layout.add_widget(locations_out_of_logic_label)

        self.level_locations_out_of_logic_label = Label(
            text="No locations accessible out of logic",
            markup=True,
            size_hint_y=None,
            font_size="13dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.level_locations_out_of_logic_label.bind(texture_size=lambda label, texture_size: setattr(label, "height", texture_size[1]))
        self.level_locations_out_of_logic_label.bind(width=lambda label, width: setattr(label, "text_size", (width, None)))

        locations_out_of_logic_layout.add_widget(self.level_locations_out_of_logic_label)

        if self.ctx.tracker_loaded:
            in_level_information_layout.add_widget(locations_out_of_logic_layout)

        self.add_widget(in_level_information_layout)

        self.last_seen_level = None
        self.last_seen_master = None

    def update(self) -> None:
        ## Received Items
        received_items: Dict[str, int] = dict()

        network_item: NetUtils.NetworkItem
        for network_item in self.ctx.items_received:
            if network_item.item in self.ctx.id_to_items:
                item_name: str = self.ctx.id_to_items[network_item.item]

                if item_name not in received_items:
                    received_items[item_name] = 0

                received_items[item_name] += 1

        ## Game State
        game_state: GameState = None

        try:
            self.game_state_manager.is_process_still_running()

            if not self.game_state_manager.is_process_running:
                try:
                    self.game_state_manager.open_process_handle()
                except Exception:
                    pass

            if self.game_state_manager.is_process_running:
                game_state = self.game_state_manager.determine_game_state()
        except Exception:
            pass

        ## Updates

        # Shadow Pegs
        shadow_pegs_obtained: int = received_items.get(PeggleNightsAPItems.SHADOW_PEG.value, 0)

        self.shadow_pegs_label.text = (
            f"[b]Shadow Pegs[/b]\n"
            f"Retrieved [color=00FA9A]{shadow_pegs_obtained}[/color] of "
            f"[color=00FA9A]{self.ctx.game_controller.option_shadow_pegs_required}[/color] needed "
            f"([color=888888]{self.ctx.game_controller.option_shadow_pegs_total} total[/color])"
        )

        # Goal
        if self.ctx.game_controller.option_goal == PeggleNightsAPGoals.SHADOW_PEGS_FINAL_LEVEL:
            self.goal_label.text = (
                "[b]Goal[/b]\n"
                f"Retrieve the Shadow Pegs and Clear {self.ctx.game_controller.selected_goal_level.value.split(" ")[0]}!"
            )
        elif self.ctx.game_controller.option_goal == PeggleNightsAPGoals.SHADOW_PEG_HUNT:
            self.goal_label.text = (
                "[b]Goal[/b]\n"
                f"Retrieve the Shadow Pegs!"
            )

        # Level
        if game_state is not None:
            if game_state.context == PeggleNightsContexts.INVALID:
                self.level_information_level_image.texture = None
                self.level_information_level_image.opacity = 0.1

                self.level_information_master_image.texture = None
                self.level_information_master_image.opacity = 0.1

                self.level_information_title.text = f"[b]Begin Playing a Quick Play Level...[/b]"
                self.level_information_subtitle.text = f"[b]This level is not included this seed.[/b]"

                self.target_score_low_label.text = "Low: [color=888888]XXX,XXX[/color]"
                self.target_score_mid_label.text = "Mid: [color=888888]XXX,XXX[/color]"
                self.target_score_high_label.text = "High: [color=888888]XXX,XXX[/color]"

                self.item_full_clear_discount_label.text = "Full Clear Discount: [color=888888]Xx[/color]"
                self.item_score_multiplier_label.text = "Score Multiplier: [color=888888]Xx[/color]"
                self.item_target_score_discount_label.text = "Target Score Discount: [color=888888]Xx[/color]"

                self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"
                self.shot_score_label.text = "[b]Shot Score:[/b] 0  [color=888888]0[/color]"
                self.orange_peg_combo_label.text = "[b]Orange Peg Combo:[/b] 0"
                self.peg_combo_label.text = "[b]Peg Combo:[/b] 0"
                self.pegs_cleared.text = "[b]Pegs Cleared:[/b] 0"

                self.level_locations_in_logic_label.text = "[color=888888]No locations accessible in logic[/color]"
                self.level_locations_out_of_logic_label.text = "[color=888888]No locations accessible out of logic[/color]"

                self.last_seen_level = None
                self.last_seen_master = None
            else:
                if game_state.current_level is not None and game_state.current_character is not None:
                    level_unlock: str = f"Level Unlock: {game_state.current_level.value}"
                    master_unlock: str = f"Master Unlock: {game_state.current_character.value}"

                    item_full_clear_discount: str = f"{PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT.value}: {game_state.current_level.value}"
                    item_score_multiplier: str = f"{PeggleNightsAPUsefulItems.SCORE_MULTIPLIER.value}: {game_state.current_level.value}"
                    item_target_score_discount: str = f"{PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT.value}: {game_state.current_level.value}"

                    full_clear_discount_count: int = 0

                    if item_full_clear_discount in received_items:
                        full_clear_discount_count = received_items[item_full_clear_discount]

                    score_multiplier_count: int = 0

                    if item_score_multiplier in received_items:
                        score_multiplier_count = received_items[item_score_multiplier]

                    target_score_discount_count: int = 0

                    if item_target_score_discount in received_items:
                        target_score_discount_count = received_items[item_target_score_discount]

                    score_multiplier: float = 1.0 + (0.05 * score_multiplier_count)
                    target_score_multiplier: float = 1.0 - (0.05 * target_score_discount_count)

                    selected_levels: List[PeggleNightsLevels] = self.ctx.game_controller.selected_levels

                    if self.ctx.game_controller.selected_goal_level is not None:
                        selected_levels.append(self.ctx.game_controller.selected_goal_level)

                    is_in_seed: bool = game_state.current_level in selected_levels
                    is_goal: bool = False

                    if self.ctx.game_controller.selected_goal_level is not None:
                        if game_state.current_level == self.ctx.game_controller.selected_goal_level:
                            is_goal = True

                    is_level_unlocked: bool = False
                    is_master_unlocked: bool = False

                    if level_unlock in received_items and received_items[level_unlock] > 0:
                        is_level_unlocked = True
                    elif is_goal:
                        if shadow_pegs_obtained >= self.ctx.game_controller.option_shadow_pegs_required:
                            is_level_unlocked = True

                    if master_unlock in received_items and received_items[master_unlock] > 0:
                        is_master_unlocked = True

                    # Level Image
                    if self.last_seen_level != game_state.current_level:
                        stage, stage_level = level_to_stage_levels[game_state.current_level]
                        level_string = f"{stage + 1}-{stage_level + 1}"

                        image_path: str = f"assets/{level_string}.png"
                        image_bytes: bytes = pkgutil.get_data(client_gui.__name__, image_path)

                        image: CoreImage = CoreImage(io.BytesIO(image_bytes), ext="png")

                        self.level_information_level_image.texture = image.texture
                        self.level_information_level_image.opacity = 1.0

                        self.last_seen_level = game_state.current_level

                    # Master Image
                    if self.last_seen_master != game_state.current_character:
                        image_path: str = f"assets/{character_to_ids[game_state.current_character]}.png"
                        image_bytes: bytes = pkgutil.get_data(client_gui.__name__, image_path)

                        image: CoreImage = CoreImage(io.BytesIO(image_bytes), ext="png")

                        self.level_information_master_image.texture = image.texture
                        self.level_information_master_image.opacity = 1.0

                        self.last_seen_master = game_state.current_character

                    # Level Title
                    self.level_information_title.text = f"[b]{game_state.current_level.value}[/b]"

                    if is_in_seed:
                        # Level Subtitle
                        if is_level_unlocked:
                            if is_master_unlocked:
                                self.level_information_subtitle.text = f"[b]This level is included this seed, is unlocked and the master is available to play.[/b]"
                            else:
                                self.level_information_subtitle.text = f"[b]This level is included this seed, is unlocked, but the master is not available to play[/b]"
                        else:
                            self.level_information_subtitle.text = f"[b]This level is included this seed but has not been unlocked yet.[/b]"

                        if is_level_unlocked and is_master_unlocked:
                            # Target Scores
                            if game_state.current_level in selected_levels and game_state.current_level in self.ctx.game_controller.target_scores:
                                base_scores: List[int] = self.ctx.game_controller.target_scores[game_state.current_level]

                                target_score_low = int((base_scores[0] or 0) * target_score_multiplier)
                                target_score_mid = int((base_scores[1] or 0) * target_score_multiplier)
                                target_score_high = int((base_scores[2] or 0) * target_score_multiplier)

                                self.target_score_low_label.text = f"Low: [color=00FA9A]{target_score_low:,}[/color]  [color=888888][size=11]{round(self.ctx.game_controller.target_score_ratios[game_state.current_level], 2)}x Base + Items[/size][/color]".replace(" 0", " XXX,XXX").replace(": [color=00FA9A]0", ": [color=00FA9A]XXX,XXX")
                                self.target_score_mid_label.text = f"Mid: [color=00FA9A]{target_score_mid:,}[/color]  [color=888888][size=11]{round(self.ctx.game_controller.target_score_ratios[game_state.current_level], 2)}x Base + Items[/size][/color]".replace(" 0", " XXX,XXX").replace(": [color=00FA9A]0", ": [color=00FA9A]XXX,XXX")
                                self.target_score_high_label.text = f"High: [color=00FA9A]{target_score_high:,}[/color]  [color=888888][size=11]{round(self.ctx.game_controller.target_score_ratios[game_state.current_level], 2)}x Base + Items[/size][/color]".replace(" 0", " XXX,XXX").replace(": [color=00FA9A]0", ": [color=00FA9A]XXX,XXX")
                            else:
                                self.target_score_low_label.text = "Low: [color=888888]XXX,XXX[/color]"
                                self.target_score_mid_label.text = "Mid: [color=888888]XXX,XXX[/color]"
                                self.target_score_high_label.text = "High: [color=888888]XXX,XXX[/color]"

                            # Useful Items
                            self.item_full_clear_discount_label.text = f"Full Clear Discount: [color=00FA9A]{full_clear_discount_count}x[/color]"
                            self.item_score_multiplier_label.text = f"Score Multiplier: [color=00FA9A]{score_multiplier_count}x[/color]"
                            self.item_target_score_discount_label.text = f"Target Score Discount: [color=00FA9A]{target_score_discount_count}x[/color]"

                            # Stats
                            score: int = int(round(game_state.current_score * score_multiplier, -1))
                            self.score_label.text = f"[b]Score:[/b] {score:,}  [color=888888]{game_state.current_score:,}[/color]"

                            shot_score: int = int(round(game_state.current_shot_score * score_multiplier, -1))
                            self.shot_score_label.text = f"[b]Shot Score:[/b] {shot_score:,}  [color=888888]{game_state.current_shot_score:,}[/color]"

                            orange_peg_combo: int = game_state.current_orange_peg_combo
                            self.orange_peg_combo_label.text = f"[b]Orange Peg Combo:[/b] {orange_peg_combo}"

                            peg_combo: int = game_state.current_peg_combo
                            self.peg_combo_label.text = f"[b]Peg Combo:[/b] {peg_combo}"

                            pegs_cleared: int = game_state.pegs_cleared
                            self.pegs_cleared.text = f"[b]Pegs Cleared:[/b] {pegs_cleared}"

                            # Locations In / Out of Logic
                            if self.ctx.tracker_loaded:
                                level_shorthand: str = game_state.current_level.value.split(" ")[0]

                                locations_in_logic: List[str] = list()

                                if len(self.ctx.locations_in_logic):
                                    location_name: str
                                    for location_name in sorted(self.ctx.locations_in_logic):
                                        if not location_name.startswith(level_shorthand):
                                            continue

                                        locations_in_logic.append(f"[color=00FA9A]{location_name.split(' - ')[-1]}[/color]")

                                    if len(locations_in_logic):
                                        self.level_locations_in_logic_label.text = "\n".join(locations_in_logic)
                                    else:
                                        self.level_locations_in_logic_label.text = "[color=888888]No locations accessible in logic[/color]"
                                else:
                                    self.level_locations_in_logic_label.text = "[color=888888]No locations accessible in logic[/color]"

                                locations_out_of_logic: List[str] = list()

                                if len(self.ctx.locations_out_of_logic):
                                    location_name: str
                                    for location_name in sorted(self.ctx.locations_out_of_logic):
                                        if not location_name.startswith(level_shorthand):
                                            continue

                                        locations_out_of_logic.append(f"[color=FFD300]{location_name.split(' - ')[-1]}[/color]")

                                    if len(locations_out_of_logic):
                                        self.level_locations_out_of_logic_label.text = "\n".join(locations_out_of_logic)
                                    else:
                                        self.level_locations_out_of_logic_label.text = "[color=888888]No locations accessible out of logic[/color]"
                                else:
                                    self.level_locations_out_of_logic_label.text = "[color=888888]No locations accessible out of logic[/color]"
                        else:
                            self.target_score_low_label.text = "Low: [color=00FA9A]XXX,XXX[/color]"
                            self.target_score_mid_label.text = "Mid: [color=00FA9A]XXX,XXX[/color]"
                            self.target_score_high_label.text = "High: [color=00FA9A]XXX,XXX[/color]"

                            self.item_full_clear_discount_label.text = f"Full Clear Discount: [color=00FA9A]Xx[/color]"
                            self.item_score_multiplier_label.text = f"Score Multiplier: [color=00FA9A]Xx[/color]"
                            self.item_target_score_discount_label.text = f"Target Score Discount: [color=00FA9A]Xx[/color]"

                            self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"
                            self.shot_score_label.text = "[b]Shot Score:[/b] 0  [color=888888]0[/color]"
                            self.orange_peg_combo_label.text = "[b]Orange Peg Combo:[/b] 0"
                            self.peg_combo_label.text = "[b]Peg Combo:[/b] 0"
                            self.pegs_cleared.text = "[b]Pegs Cleared:[/b] 0"

                            self.level_locations_in_logic_label.text = "[color=888888]No locations accessible in logic[/color]"
                            self.level_locations_out_of_logic_label.text = "[color=888888]No locations accessible out of logic[/color]"
                    else:
                        self.level_information_subtitle.text = f"[b]This level is not included this seed.[/b]"

                        self.target_score_low_label.text = "Low: [color=888888]XXX,XXX[/color]"
                        self.target_score_mid_label.text = "Mid: [color=888888]XXX,XXX[/color]"
                        self.target_score_high_label.text = "High: [color=888888]XXX,XXX[/color]"

                        self.item_full_clear_discount_label.text = f"Full Clear Discount: [color=888888]Xx[/color]"
                        self.item_score_multiplier_label.text = f"Score Multiplier: [color=888888]Xx[/color]"
                        self.item_target_score_discount_label.text = f"Target Score Discount: [color=888888]Xx[/color]"

                        self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"
                        self.shot_score_label.text = "[b]Shot Score:[/b] 0  [color=888888]0[/color]"
                        self.orange_peg_combo_label.text = "[b]Orange Peg Combo:[/b] 0"
                        self.peg_combo_label.text = "[b]Peg Combo:[/b] 0"
                        self.pegs_cleared.text = "[b]Pegs Cleared:[/b] 0"

                        self.level_locations_in_logic_label.text = "[color=888888]No locations accessible in logic[/color]"
                        self.level_locations_out_of_logic_label.text = "[color=888888]No locations accessible out of logic[/color]"
        else:
            self.level_information_level_image.texture = None
            self.level_information_level_image.opacity = 0.1

            self.level_information_master_image.texture = None
            self.level_information_master_image.opacity = 0.1

            self.level_information_title.text = f"[b]Begin Playing a Quick Play Level...[/b]"
            self.level_information_subtitle.text = f"[b]This level is not included this seed.[/b]"

            self.target_score_low_label.text = "Low: [color=888888]XXX,XXX[/color]"
            self.target_score_mid_label.text = "Mid: [color=888888]XXX,XXX[/color]"
            self.target_score_high_label.text = "High: [color=888888]XXX,XXX[/color]"

            self.item_full_clear_discount_label.text = f"Full Clear Discount: [color=888888]Xx[/color]"
            self.item_score_multiplier_label.text = f"Score Multiplier: [color=888888]Xx[/color]"
            self.item_target_score_discount_label.text = f"Target Score Discount: [color=888888]Xx[/color]"

            self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"
            self.shot_score_label.text = "[b]Shot Score:[/b] 0  [color=888888]0[/color]"
            self.orange_peg_combo_label.text = "[b]Orange Peg Combo:[/b] 0"
            self.peg_combo_label.text = "[b]Peg Combo:[/b] 0"
            self.pegs_cleared.text = "[b]Pegs Cleared:[/b] 0"

            self.level_locations_in_logic_label.text = "[color=888888]No locations accessible in logic[/color]"
            self.level_locations_out_of_logic_label.text = "[color=888888]No locations accessible out of logic[/color]"


class PeggleNightsMastersLayout(BoxLayout):
    ctx: PeggleNightsContext

    master_label: Label

    master_images: List[Image]
    master_labels: List[Label]

    master_data: Dict[PeggleNightsCharacters, Dict[str, Any]]

    def __init__(self, ctx: PeggleNightsContext) -> None:
        super().__init__(orientation="vertical", size_hint_y=None, height="40dp", spacing="8dp")

        self.bind(minimum_height=self.setter("height"))

        self.ctx = ctx

        self.master_label = Label(
            text=f"[b]Peggle Masters[/b]",
            markup=True,
            font_size="32dp",
            size_hint_y=None,
            height="70dp",
            halign="left",
            valign="bottom",
        )

        self.master_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(self.master_label)

        self.master_images = list()
        self.master_labels = list()

        self.master_data = dict()

        master: PeggleNightsCharacters
        for master in self.ctx.game_controller.selected_masters:
            self.master_data[master] = {
                "image_path": f"assets/{character_to_ids[master]}.png",
                "unlock_item": f"Master Unlock: {master.value}",
            }

        grid_layout: GridLayout = GridLayout(
            cols=6,
            spacing=12,
            padding=0,
            size_hint_y=None,
        )

        grid_layout.bind(minimum_height=grid_layout.setter("height"))

        master: PeggleNightsCharacters
        data: Dict[str, Any]
        for master, data in self.master_data.items():
            master_layout: BoxLayout = BoxLayout(
                orientation="vertical",
                size_hint_x=None,
                size_hint_y=None,
                width="96dp",
                height="120dp",
                spacing="4dp",
            )

            master_layout.bind(minimum_height=master_layout.setter("height"))

            image_bytes: bytes = pkgutil.get_data(client_gui.__name__, data["image_path"])
            image: CoreImage = CoreImage(io.BytesIO(image_bytes), ext="png")

            master_image = Image(
                texture=image.texture,
                size=(96, 96),
                size_hint=(None, None),
                allow_stretch=True,
                opacity=0.4
            )

            self.master_images.append(master_image)

            master_layout.add_widget(master_image)

            master_label: Label = Label(
                text="Green Pegs: [color=00FA9A]1[/color]",
                markup=True,
                font_size="14dp",
                size_hint_y=None,
                height="20dp",
                halign="left",
                valign="middle",
            )

            master_label.bind(size=lambda label, size: setattr(label, "text_size", size))

            self.master_labels.append(master_label)

            master_layout.add_widget(master_label)

            grid_layout.add_widget(master_layout)

        self.add_widget(grid_layout)

    def update(self) -> None:
        received_items: Dict[str, int] = dict()

        network_item: NetUtils.NetworkItem
        for network_item in self.ctx.items_received:
            if network_item.item in self.ctx.id_to_items:
                item_name: str = self.ctx.id_to_items[network_item.item]

                if item_name not in received_items:
                    received_items[item_name] = 0

                received_items[item_name] += 1

        master: PeggleNightsCharacters
        data: Dict[str, Any]
        for i, (master, data) in enumerate(self.master_data.items()):
            is_unlocked: bool = False

            if data["unlock_item"] in received_items and received_items[data["unlock_item"]] > 0:
                is_unlocked = True

            self.master_images[i].opacity = 1.0 if is_unlocked else 0.4

            green_pegs_item: str = f"Progressive Green Pegs: {master.value}"
            green_pegs_item_count: int = received_items.get(green_pegs_item, 0) + 1

            if is_unlocked:
                self.master_labels[i].text = f"Green Pegs: [color=00FA9A]{green_pegs_item_count}[/color]"
            else:
                self.master_labels[i].text = f"[color=888888]Green Pegs: {green_pegs_item_count}[/color]"


class PeggleNightsLevelsLayout(BoxLayout):
    ctx: PeggleNightsContext

    level_label: Label

    level_images: List[Image]
    level_in_logic_labels: List[Label]
    level_out_of_logic_labels: List[Label]

    level_data: Dict[PeggleNightsLevels, Dict[str, Any]]

    def __init__(self, ctx: PeggleNightsContext) -> None:
        super().__init__(orientation="vertical", size_hint_y=None, height="40dp", spacing="8dp")

        self.bind(minimum_height=self.setter("height"))

        self.ctx = ctx

        self.level_label = Label(
            text=f"[b]Levels[/b]",
            markup=True,
            font_size="32dp",
            size_hint_y=None,
            height="70dp",
            halign="left",
            valign="bottom",
        )

        self.level_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(self.level_label)

        self.level_images = list()
        self.level_in_logic_labels = list()
        self.level_out_of_logic_labels = list()

        self.level_data = dict()

        levels: List[PeggleNightsLevels] = self.ctx.game_controller.selected_levels

        if self.ctx.game_controller.selected_goal_level is not None:
            levels.append(self.ctx.game_controller.selected_goal_level)

        level: PeggleNightsCharacters
        for level in levels:
            stage, stage_level = level_to_stage_levels[level]
            level_string = f"{stage + 1}-{stage_level + 1}"

            self.level_data[level] = {
                "image_path": f"assets/{level_string}.png",
                "unlock_item": f"Level Unlock: {level.value}",
                "is_goal": False,
            }

            if self.ctx.game_controller.selected_goal_level is not None:
                if level == self.ctx.game_controller.selected_goal_level:
                    self.level_data[level]["is_goal"] = True

        grid_layout: GridLayout = GridLayout(
            cols=6,
            spacing=12,
            padding=0,
            size_hint_y=None,
        )

        grid_layout.bind(minimum_height=grid_layout.setter("height"))

        level: PeggleNightsLevels
        data: Dict[str, Any]
        for level, data in self.level_data.items():
            height: int = 96

            if self.ctx.tracker_loaded:
                height = 140

            level_layout: BoxLayout = BoxLayout(
                orientation="vertical",
                size_hint_x=None,
                size_hint_y=None,
                width="96dp",
                height=f"{height}dp",
                spacing="4dp",
            )

            level_layout.bind(minimum_height=level_layout.setter("height"))

            image_bytes: bytes = pkgutil.get_data(client_gui.__name__, data["image_path"])
            image: CoreImage = CoreImage(io.BytesIO(image_bytes), ext="png")

            level_image = Image(
                texture=image.texture,
                size=(96, 96),
                size_hint=(None, None),
                allow_stretch=True,
                opacity=0.4
            )

            if data["is_goal"]:
                with level_image.canvas.after:
                    fill_color = Color(1, 0.85, 0.2, 0.15)
                    fill_rect = Rectangle(pos=level_image.pos, size=level_image.size)

                    line_color = Color(1, 0.85, 0.2, 1.0)
                    border = Line(rectangle=(*level_image.pos, *level_image.size), width=2)

                def _update_goal_decoration(*_) -> None:
                    fill_rect.pos = level_image.pos
                    fill_rect.size = level_image.size
                    border.rectangle = (*level_image.pos, *level_image.size)

                level_image.bind(pos=_update_goal_decoration, size=_update_goal_decoration)

            self.level_images.append(level_image)

            level_layout.add_widget(level_image)

            in_logic_text: str = "In Logic: [color=00FA9A]1[/color]"

            if data["is_goal"]:
                in_logic_text = ""

            in_logic_label: Label = Label(
                text=in_logic_text,
                markup=True,
                font_size="12dp",
                size_hint_y=None,
                height="16dp",
                halign="left",
                valign="middle",
            )

            in_logic_label.bind(size=lambda label, size: setattr(label, "text_size", size))

            self.level_in_logic_labels.append(in_logic_label)

            if self.ctx.tracker_loaded:
                level_layout.add_widget(in_logic_label)

            out_of_logic_text: str = "Out of Logic: [color=FFD300]1[/color]"

            if data["is_goal"]:
                out_of_logic_text = ""

            out_of_logic_label: Label = Label(
                text=out_of_logic_text,
                markup=True,
                font_size="12dp",
                size_hint_y=None,
                height="16dp",
                halign="left",
                valign="middle",
            )

            out_of_logic_label.bind(size=lambda label, size: setattr(label, "text_size", size))

            self.level_out_of_logic_labels.append(out_of_logic_label)

            if self.ctx.tracker_loaded:
                level_layout.add_widget(out_of_logic_label)

            grid_layout.add_widget(level_layout)

        self.add_widget(grid_layout)

    def update(self) -> None:
        received_items: Dict[str, int] = dict()

        network_item: NetUtils.NetworkItem
        for network_item in self.ctx.items_received:
            if network_item.item in self.ctx.id_to_items:
                item_name: str = self.ctx.id_to_items[network_item.item]

                if item_name not in received_items:
                    received_items[item_name] = 0

                received_items[item_name] += 1

        in_logic_location_counts_by_level_shorthand: Dict[str, int] = dict()
        out_of_logic_location_counts_by_level_shorthand: Dict[str, int] = dict()

        if self.ctx.tracker_loaded:
            location_name: str
            for location_name in self.ctx.locations_in_logic:
                level_shorthand: str = location_name.split(" ")[0]

                if level_shorthand not in in_logic_location_counts_by_level_shorthand:
                    in_logic_location_counts_by_level_shorthand[level_shorthand] = 0

                in_logic_location_counts_by_level_shorthand[level_shorthand] += 1

            location_name: str
            for location_name in self.ctx.locations_out_of_logic:
                level_shorthand: str = location_name.split(" ")[0]

                if level_shorthand not in out_of_logic_location_counts_by_level_shorthand:
                    out_of_logic_location_counts_by_level_shorthand[level_shorthand] = 0

                out_of_logic_location_counts_by_level_shorthand[level_shorthand] += 1

        level: PeggleNightsLevels
        data: Dict[str, Any]
        for i, (level, data) in enumerate(self.level_data.items()):
            is_unlocked: bool = False

            if data["unlock_item"] in received_items and received_items[data["unlock_item"]] > 0:
                is_unlocked = True
            elif data["is_goal"]:
                shadow_pegs_required: int = self.ctx.game_controller.option_shadow_pegs_required
                shadow_pegs_obtained: int = received_items.get(PeggleNightsAPItems.SHADOW_PEG.value, 0)

                if shadow_pegs_obtained >= shadow_pegs_required:
                    is_unlocked = True

            self.level_images[i].opacity = 1.0 if is_unlocked else 0.4

            if self.ctx.tracker_loaded:
                if data["is_goal"]:
                    continue

                level_shorthand: str = level.value.split(" ")[0]

                if is_unlocked:
                    in_logic_count: int = in_logic_location_counts_by_level_shorthand.get(level_shorthand, 0)
                    out_of_logic_count: int = out_of_logic_location_counts_by_level_shorthand.get(level_shorthand, 0)

                    if in_logic_count > 0:
                        self.level_in_logic_labels[i].text = f"In Logic: [color=00FA9A]{in_logic_count}[/color]"
                    else:
                        self.level_in_logic_labels[i].text = f"In Logic: [color=888888]0[/color]"

                    if out_of_logic_count > 0:
                        self.level_out_of_logic_labels[i].text = f"Out of Logic: [color=FFD300]{out_of_logic_count}[/color]"
                    else:
                        self.level_out_of_logic_labels[i].text = f"Out of Logic: [color=888888]0[/color]"
                else:
                    self.level_in_logic_labels[i].text = f"[color=888888]In Logic: 0[/color]"
                    self.level_out_of_logic_labels[i].text = f"[color=888888]Out of Logic: 0[/color]"


class PeggleNightsContent(ScrollView):
    ctx: PeggleNightsContext

    layout: BoxLayout

    layout_level_information: PeggleNightsLevelInformationLayout
    layout_masters: PeggleNightsMastersLayout
    layout_levels: PeggleNightsLevelsLayout

    timer: Clock

    def __init__(self, ctx: PeggleNightsContext) -> None:
        super().__init__()

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.layout_level_information = PeggleNightsLevelInformationLayout(ctx=self.ctx)
        self.layout.add_widget(self.layout_level_information)

        self.layout_masters = PeggleNightsMastersLayout(ctx=self.ctx)
        self.layout.add_widget(self.layout_masters)

        self.layout_levels = PeggleNightsLevelsLayout(ctx=self.ctx)
        self.layout.add_widget(self.layout_levels)

        self.add_widget(self.layout)

        self.timer = Clock.schedule_interval(self.update, 1.0 / 10.0)

    def update(self, *_) -> None:
        try:
            self.layout_level_information.update()
            self.layout_masters.update()
            self.layout_levels.update()
        except Exception:
            import traceback

            with open("peggle_nights_errors.log", "a") as f:
                f.write(traceback.format_exc() + "\n\n")


class PeggleNightsTabLayout(BoxLayout):
    ctx: PeggleNightsContext

    layout_content: BoxLayout
    layout_content_peggle_nights: PeggleNightsContent

    layout_not_connected: NotConnectedLayout

    def __init__(self, ctx: PeggleNightsContext) -> None:
        super().__init__(orientation="vertical", padding="8dp")

        self.bind(minimum_height=self.setter('height'))

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if self.ctx.game_controller.target_scores is None:
            self.layout_not_connected.show()

            if hasattr(self, "layout_content_peggle_nights"):
                self.layout_content_peggle_nights.timer.cancel()

            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_content_peggle_nights = PeggleNightsContent(ctx=self.ctx)
            self.layout_content.add_widget(self.layout_content_peggle_nights)

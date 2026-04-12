from typing import Any, Dict, List

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

from ..client import PinballFX3Context

from ..data.mapping_data import table_to_table_id

from ..enums import (
    PinballFX3APItems,
    PinballFX3APUsefulItems,
    PinballFX3Contexts,
    PinballFX3Tables,
)

from ..game_state_manager import GameStateManager, GameState

from .. import client_gui


class NotConnectedLayout(BoxLayout):
    ctx: PinballFX3Context

    def __init__(self, ctx: PinballFX3Context) -> None:
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


class PinballFX3TableInformationLayout(BoxLayout):
    ctx: PinballFX3Context

    game_state_manager: GameStateManager

    information_label: Label
    shiny_quarters_label: Label

    table_information_image: Image
    table_information_title: Label
    table_information_subtitle: Label

    target_scores_label: Label
    target_stars_label: Label

    item_score_multiplier_label: Label
    item_star_requirement_discount_label: Label
    item_target_score_discount_label: Label

    score_label: Label

    def __init__(self, ctx: PinballFX3Context) -> None:
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

        # Shiny Quarters
        self.shiny_quarters_label: Label = Label(
            text=(
                f"[b]Shiny Quarters[/b]\n"
                f"Retrieved [color=00FA9A]0[/color] of "
                f"[color=00FA9A]{self.ctx.shiny_quarters_required}[/color] needed "
                f"([color=888888]{self.ctx.shiny_quarters_total} total[/color])"
            ),
            markup=True,
            size_hint_y=None,
            height="60dp",
            halign="left",
            valign="middle",
        )

        self.shiny_quarters_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(self.shiny_quarters_label)

        # Table Information
        table_information_layout: BoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="140dp",
            spacing="8dp",
        )

        table_information_layout.bind(minimum_height=table_information_layout.setter("height"))

        self.table_information_image = Image(
            size=(128, 128),
            size_hint=(None, None),
            allow_stretch=True,
            opacity=0.1
        )

        table_information_layout.add_widget(self.table_information_image)

        table_information_text_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="140dp",
            spacing="5dp",
        )

        table_information_text_layout.bind(minimum_height=table_information_text_layout.setter("height"))

        self.table_information_title = Label(
            text=f"[b]Begin Playing a Pinball Table...[/b]",
            markup=True,
            size_hint_y=None,
            font_size="18dp",
            height="22dp",
            halign="left",
            valign="middle",
        )

        self.table_information_title.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_text_layout.add_widget(self.table_information_title)

        self.table_information_subtitle = Label(
            text=f"[b]This table is not included this seed.[/b]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="14dp",
            halign="left",
            valign="middle",
        )

        self.table_information_subtitle.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_text_layout.add_widget(self.table_information_subtitle)

        table_information_text_sublayout: BoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="78dp",
            spacing="8dp",
        )

        table_information_text_sublayout.bind(minimum_height=table_information_text_sublayout.setter("height"))

        table_information_targets_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="78dp",
            spacing="4dp",
            size_hint_x=70,
        )

        table_information_targets_layout.bind(minimum_height=table_information_targets_layout.setter("height"))

        targets_label: Label = Label(
            text="[b]Targets[/b]",
            markup=True,
            size_hint_y=None,
            font_size="16dp",
            height="20dp",
            halign="left",
            valign="middle",
        )

        targets_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_targets_layout.add_widget(targets_label)

        self.target_scores_label = Label(
            text="Scores: [color=00FA9A]X,XXX,XXX / X,XXX,XXX / X,XXX,XXX[/color]",
            markup=True,
            size_hint_y=None,
            font_size="14dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.target_scores_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_targets_layout.add_widget(self.target_scores_label)

        self.target_stars_label = Label(
            text="Stars: [color=00FA9A]X / X / X[/color]",
            markup=True,
            size_hint_y=None,
            font_size="14dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.target_stars_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_targets_layout.add_widget(self.target_stars_label)

        table_information_items_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="78dp",
            spacing="8dp",
            size_hint_x=30,
        )

        table_information_items_layout.bind(minimum_height=table_information_items_layout.setter("height"))

        items_label: Label = Label(
            text="[b]Useful Items[/b]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="14dp",
            halign="left",
            valign="middle",
        )

        items_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_items_layout.add_widget(items_label)

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

        table_information_items_layout.add_widget(self.item_score_multiplier_label)

        self.item_star_requirement_discount_label = Label(
            text="Star Requirement Discount: [color=00FA9A]Xx[/color]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="14dp",
            halign="left",
            valign="middle",
        )

        self.item_star_requirement_discount_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_items_layout.add_widget(self.item_star_requirement_discount_label)

        self.item_target_score_discount_label = Label(
            text="Target Score Discount: [color=00FA9A]Xx[/color]",
            markup=True,
            size_hint_y=None,
            font_size="12dp",
            height="16dp",
            halign="left",
            valign="middle",
        )

        self.item_target_score_discount_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        table_information_items_layout.add_widget(self.item_target_score_discount_label)

        table_information_text_sublayout.add_widget(table_information_targets_layout)
        table_information_text_sublayout.add_widget(table_information_items_layout)
        table_information_text_layout.add_widget(table_information_text_sublayout)
        table_information_layout.add_widget(table_information_text_layout)

        self.add_widget(table_information_layout)

        self.score_label = Label(
            text="[b]Score:[/b] 0  [color=888888]0[/color]",
            markup=True,
            size_hint_y=None,
            font_size="22dp",
            height="28dp",
            halign="left",
            valign="middle",
        )

        self.score_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(self.score_label)

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

        # Shiny Quarters
        shiny_quarters_obtained: int = 0

        if PinballFX3APItems.SHINY_QUARTER.value in received_items:
            shiny_quarters_obtained = received_items[PinballFX3APItems.SHINY_QUARTER.value]

        self.shiny_quarters_label.text = (
            f"[b]Shiny Quarters[/b]\n"
            f"Retrieved [color=00FA9A]{shiny_quarters_obtained}[/color] of "
            f"[color=00FA9A]{self.ctx.shiny_quarters_required}[/color] needed "
            f"([color=888888]{self.ctx.shiny_quarters_total} total[/color])"
        )

        # Table
        if game_state is not None:
            if game_state.context == PinballFX3Contexts.INVALID:
                self.table_information_image.texture = None
                self.table_information_image.opacity = 0.1

                self.table_information_title.text = f"[b]Begin Playing a Pinball Table...[/b]"
                self.table_information_subtitle.text = f"[b]This table is not included this seed.[/b]"

                self.target_scores_label.text = "Scores: [color=00FA9A]X,XXX,XXX / X,XXX,XXX / X,XXX,XXX[/color]"
                self.target_stars_label.text = "Stars: [color=00FA9A]X / X / X[/color]"

                self.item_score_multiplier_label.text = "Score Multiplier: [color=00FA9A]Xx[/color]"
                self.item_star_requirement_discount_label.text = "Star Requirement Discount: [color=00FA9A]Xx[/color]"
                self.item_target_score_discount_label.text = "Target Score Discount: [color=00FA9A]Xx[/color]"

                self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"
            else:
                if game_state.table is not None:
                    item_unlock: str = f"Table Unlock: {game_state.table.value}"

                    item_score_multiplier: str = f"{PinballFX3APUsefulItems.SCORE_MULTIPLIER.value}: {game_state.table.value}"
                    item_star_requirement_discount: str = f"{PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT.value}: {game_state.table.value}"
                    item_target_score_discount: str = f"{PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT.value}: {game_state.table.value}"

                    shiny_quarters_obtained: int = 0

                    if PinballFX3APItems.SHINY_QUARTER.value in received_items:
                        shiny_quarters_obtained = received_items[PinballFX3APItems.SHINY_QUARTER.value]

                    score_multiplier_count: int = 0

                    if item_score_multiplier in received_items:
                        score_multiplier_count = received_items[item_score_multiplier]

                    star_requirement_discount_count: int = 0

                    if item_star_requirement_discount in received_items:
                        star_requirement_discount_count = received_items[item_star_requirement_discount]

                    target_score_discount_count: int = 0

                    if item_target_score_discount in received_items:
                        target_score_discount_count = received_items[item_target_score_discount]

                    score_multiplier: float = 1.0 + (0.05 * score_multiplier_count)
                    target_score_multiplier: float = 1.0 - (0.05 * target_score_discount_count)

                    is_in_seed: bool = game_state.table in self.ctx.game_controller.target_scores
                    is_goal: bool = False

                    if self.ctx.game_controller.selected_goal_table is not None:
                        if game_state.table == self.ctx.game_controller.selected_goal_table:
                            is_goal = True

                    is_unlocked: bool = False

                    if item_unlock in received_items and received_items[item_unlock] > 0:
                        if is_goal:
                            if shiny_quarters_obtained >= self.ctx.shiny_quarters_required:
                                is_unlocked = True
                        else:
                            is_unlocked = True

                    is_being_played: bool = game_state.context in (PinballFX3Contexts.SINGLE_PLAYER, PinballFX3Contexts.CHALLENGE)

                    # Table Image
                    image_path: str = f"assets/{table_to_table_id[game_state.table]}.png"
                    image_bytes: bytes = pkgutil.get_data(client_gui.__name__, image_path)

                    image: CoreImage = CoreImage(io.BytesIO(image_bytes), ext="png")

                    self.table_information_image.texture = image.texture
                    self.table_information_image.opacity = 1.0

                    # Table Title
                    self.table_information_title.text = f"[b]{game_state.table.value}[/b]"

                    if is_in_seed:
                        # Table Subtitle
                        if is_unlocked:
                            self.table_information_subtitle.text = f"[b]This table is included this seed and is unlocked![/b]"
                        else:
                            self.table_information_subtitle.text = f"[b]This table is included this seed but has not been unlocked yet.[/b]"

                        if is_being_played and is_unlocked:
                            # Target Scores
                            if game_state.table in self.ctx.game_controller.target_scores:
                                base_scores: List[int] = self.ctx.game_controller.target_scores[game_state.table]

                                target_score_low = int((base_scores[0] or 0) * target_score_multiplier)
                                target_score_mid = int((base_scores[1] or 0) * target_score_multiplier)
                                target_score_high = int((base_scores[2] or 0) * target_score_multiplier)

                                self.target_scores_label.text = f"Scores: [color=00FA9A]{target_score_low:,} / {target_score_mid:,} / {target_score_high:,}[/color]  [color=888888][size=11]{round(self.ctx.target_score_ratios[game_state.table], 2)}x Base + Items[/size][/color]".replace(" 0", " X,XXX,XXX").replace(": [color=00FA9A]0", ": [color=00FA9A]X,XXX,XXX")
                            else:
                                self.target_scores_label.text = "Scores: [color=00FA9A]X,XXX,XXX / X,XXX,XXX / X,XXX,XXX[/color]"

                            # Target Stars
                            if game_state.table in self.ctx.game_controller.challenge_stars:
                                stars_low, stars_mid, stars_high = self.ctx.game_controller.challenge_stars[game_state.table]

                                if stars_high is None:
                                    stars_high = "X"

                                self.target_stars_label.text = f"Stars: [color=00FA9A]{stars_low} / {stars_mid} / {stars_high}[/color]"
                            else:
                                self.target_stars_label.text = "Stars: [color=00FA9A]X / X / X[/color]"

                            # Useful Items
                            self.item_score_multiplier_label.text = f"Score Multiplier: [color=00FA9A]{score_multiplier_count}x[/color]"
                            self.item_star_requirement_discount_label.text = f"Star Requirement Discount: [color=00FA9A]{star_requirement_discount_count}x[/color]"
                            self.item_target_score_discount_label.text = f"Target Score Discount: [color=00FA9A]{target_score_discount_count}x[/color]"

                            # Score
                            score: int = game_state.current_score

                            if game_state.context == PinballFX3Contexts.SINGLE_PLAYER:
                                score = int(score * score_multiplier)

                            self.score_label.text = f"[b]Score:[/b] {score:,}  [color=888888]{game_state.current_score:,}[/color]"
                        else:
                            self.target_scores_label.text = "Scores: [color=00FA9A]X,XXX,XXX / X,XXX,XXX / X,XXX,XXX[/color]"
                            self.target_stars_label.text = "Stars: [color=00FA9A]X / X / X[/color]"

                            self.item_score_multiplier_label.text = "Score Multiplier: [color=00FA9A]Xx[/color]"
                            self.item_star_requirement_discount_label.text = "Star Requirement Discount: [color=00FA9A]Xx[/color]"
                            self.item_target_score_discount_label.text = "Target Score Discount: [color=00FA9A]Xx[/color]"

                            self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"
                    else:
                        self.table_information_subtitle.text = f"[b]This table is not included this seed.[/b]"

                        self.target_scores_label.text = "Scores: [color=00FA9A]X,XXX,XXX / X,XXX,XXX / X,XXX,XXX[/color]"
                        self.target_stars_label.text = "Stars: [color=00FA9A]X / X / X[/color]"

                        self.item_score_multiplier_label.text = "Score Multiplier: [color=00FA9A]Xx[/color]"
                        self.item_star_requirement_discount_label.text = "Star Requirement Discount: [color=00FA9A]Xx[/color]"
                        self.item_target_score_discount_label.text = "Target Score Discount: [color=00FA9A]Xx[/color]"

                        self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"
        else:
            self.table_information_image.texture = None
            self.table_information_image.opacity = 0.1

            self.table_information_title.text = f"[b]Begin Playing a Pinball Table...[/b]"
            self.table_information_subtitle.text = f"[b]This table is not included this seed.[/b]"

            self.target_scores_label.text = "Scores: [color=00FA9A]X,XXX,XXX / X,XXX,XXX / X,XXX,XXX[/color]"
            self.target_stars_label.text = "Stars: [color=00FA9A]X / X / X[/color]"

            self.item_score_multiplier_label.text = "Score Multiplier: [color=00FA9A]Xx[/color]"
            self.item_star_requirement_discount_label.text = "Star Requirement Discount: [color=00FA9A]Xx[/color]"
            self.item_target_score_discount_label.text = "Target Score Discount: [color=00FA9A]Xx[/color]"

            self.score_label.text = "[b]Score:[/b] 0  [color=888888]0[/color]"


class PinballFX3TablesLayout(BoxLayout):
    ctx: PinballFX3Context

    table_label: Label
    table_images: List[Image]

    table_data: Dict[PinballFX3Tables, Dict[str, Any]]

    def __init__(self, ctx: PinballFX3Context) -> None:
        super().__init__(orientation="vertical", size_hint_y=None, height="40dp", spacing="8dp")

        self.bind(minimum_height=self.setter("height"))

        self.ctx = ctx

        self.table_label = Label(
            text=f"[b]Pinball Tables[/b]",
            markup=True,
            font_size="32dp",
            size_hint_y=None,
            height="70dp",
            halign="left",
            valign="bottom",
        )

        self.table_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(self.table_label)

        self.table_images = list()

        self.table_data = dict()

        table: PinballFX3Tables
        for table in self.ctx.game_controller.target_scores.keys():
            self.table_data[table] = {
                "image_path": f"assets/{table_to_table_id[table]}.png",
                "unlock_item": f"Table Unlock: {table.value}",
                "is_goal": False,
            }

            if self.ctx.game_controller.selected_goal_table is not None:
                if table == self.ctx.game_controller.selected_goal_table:
                    self.table_data[table]["is_goal"] = True

        grid_layout: GridLayout = GridLayout(
            cols=6,
            spacing=8,
            padding=0,
            size_hint_y=None,
        )

        grid_layout.bind(minimum_height=grid_layout.setter("height"))

        table: PinballFX3Tables
        data: Dict[str, Any]
        for table, data in self.table_data.items():
            image_bytes: bytes = pkgutil.get_data(client_gui.__name__, data["image_path"])
            image: CoreImage = CoreImage(io.BytesIO(image_bytes), ext="png")

            table_image = Image(
                texture=image.texture,
                size=(96, 96),
                size_hint=(None, None),
                allow_stretch=True,
                opacity=0.4
            )

            if data["is_goal"]:
                with table_image.canvas.after:
                    fill_color = Color(1, 0.85, 0.2, 0.15)
                    fill_rect = Rectangle(pos=table_image.pos, size=table_image.size)

                    line_color = Color(1, 0.85, 0.2, 1.0)
                    border = Line(rectangle=(*table_image.pos, *table_image.size), width=2)

                def _update_goal_decoration(*_) -> None:
                    fill_rect.pos = table_image.pos
                    fill_rect.size = table_image.size
                    border.rectangle = (*table_image.pos, *table_image.size)

                table_image.bind(pos=_update_goal_decoration, size=_update_goal_decoration)

            self.table_images.append(table_image)
            grid_layout.add_widget(table_image)

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

        table: PinballFX3Tables
        data: Dict[str, Any]
        for i, (table, data) in enumerate(self.table_data.items()):
            is_unlocked: bool = False

            if data["unlock_item"] in received_items and received_items[data["unlock_item"]] > 0:
                if data["is_goal"]:
                    required: int = self.ctx.game_controller.option_shiny_quarters_required

                    if PinballFX3APItems.SHINY_QUARTER.value in received_items and received_items[PinballFX3APItems.SHINY_QUARTER.value] >= required:
                        is_unlocked = True
                else:
                    is_unlocked = True

            self.table_images[i].opacity = 1.0 if is_unlocked else 0.4


class PinballFX3Content(ScrollView):
    ctx: PinballFX3Context

    layout: BoxLayout

    layout_table_information: PinballFX3TableInformationLayout
    layout_tables: PinballFX3TablesLayout

    timer: Clock

    def __init__(self, ctx: PinballFX3Context) -> None:
        super().__init__()

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.layout_table_information = PinballFX3TableInformationLayout(ctx=self.ctx)
        self.layout.add_widget(self.layout_table_information)

        self.layout_tables = PinballFX3TablesLayout(ctx=self.ctx)
        self.layout.add_widget(self.layout_tables)

        self.add_widget(self.layout)

        self.timer = Clock.schedule_interval(self.update, 1.0 / 10.0)

    def update(self, *_) -> None:
        try:
            self.layout_table_information.update()
            self.layout_tables.update()
        except Exception:
            import traceback

            with open("pinball_fx3_errors.log", "a") as f:
                f.write(traceback.format_exc() + "\n\n")


class PinballFX3TabLayout(BoxLayout):
    ctx: PinballFX3Context

    layout_content: BoxLayout
    layout_content_pinball_fx3: PinballFX3Content

    layout_not_connected: NotConnectedLayout

    def __init__(self, ctx: PinballFX3Context) -> None:
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

            if hasattr(self, "layout_content_pinball_fx3"):
                self.layout_content_pinball_fx3.timer.cancel()

            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_content_pinball_fx3 = PinballFX3Content(ctx=self.ctx)
            self.layout_content.add_widget(self.layout_content_pinball_fx3)

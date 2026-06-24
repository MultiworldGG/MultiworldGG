import os
from CommonClient import logger
from NetUtils import JSONMessagePart
from settings import get_settings
from . import game_data, mkdd_client, options
from .game_state import MkddGameState
from .settings import MkddSettings
from .ut_common_client_importer import ClientCommandProcessor, CommonContext


DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE = "DME_DOLPHIN_PROCESS_NAME"
settings: MkddSettings = get_settings().mario_kart_double_dash_options
if settings.dolphin_process_name:
    os.environ[DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE] = settings.dolphin_process_name
elif DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE in os.environ:
    del os.environ[DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE]


class MkddCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Mario Kart Double Dash client commands.

    This class handles commands specific to Mario Kart Double Dash.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)


    def _cmd_dolphin(self) -> None:
        """Display the current Dolphin emulator connection status."""
        if isinstance(self.ctx, mkdd_client.MkddContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


    def _cmd_dolphin_process_name(self, dolphin_process_name: str) -> None:
        """Specify the name of the Dolphin process to connect to. "" for system default."""
        settings.dolphin_process_name = dolphin_process_name
        get_settings().save()
        logger.info(f"Dolphin process name set to {dolphin_process_name or "default"}. You must open a new client for this to take effect.")


    def _cmd_launch(self) -> None:
        """Launch Dolphin running Mario Kart Double Dash."""
        import os
        if not os.path.isfile(settings.rom_path):
            new_path = settings.rom_path.browse([("Rom file", ["*.ISO", "*.RVZ", "*.GCZ"])])
            if new_path != None:
                settings.rom_path = new_path
                get_settings().save()
        if os.path.isfile(settings.rom_path) and os.path.isfile(settings.dolphin_path):
            os.startfile(settings.dolphin_path, arguments=f'"{settings.rom_path}"')
        else:
            logger.error("Dolphin or ROM path not valid.")


    def _cmd_reset_paths(self) -> None:
        """Reset file paths to Dolphin and ROM."""
        settings.rom_path = settings.RomPath()
        settings.dolphin_path = settings.DolphinPath()
        get_settings().save()


    def _cmd_error(self) -> None:
        """Shows the latest exception if any."""
        if self.ctx.latest_error:
            logger.info(self.ctx.latest_error)
        else:
            logger.info("No errors caught!")


    def _cmd_unlocked(self) -> None:
        """Show list of unlocked items."""
        if not isinstance(self.ctx, mkdd_client.MkddContext):
            return
        
        def _msg(title: str, val: str) -> list[JSONMessagePart]:
            return [
                {"type": "text", "text": str(title)},
                {"type": "color", "color": "cyan", "text": str(val)},
            ]
        
        gs: MkddGameState = self.ctx.game_state
        pr: function = self.ctx.ui.print_json
        goaltxt = ""
        if self.ctx.options.goal == options.Goal.option_all_cup_tour:
            goaltxt = (
                "All Cup Tour (" +
                ["50cc ", "100cc ", "150cc ", "Mirror "][self.ctx.options.all_cup_tour_min_cc] +
                ["Gold", "Silver", "Bronze", "Perfect"][self.ctx.options.all_cup_tour_min_rank] +
                f", {self.ctx.options.all_cup_tour_length} races)"
            )
        else:
            goaltxt = "Trophies"
        pr(_msg("Goal: ", goaltxt))
        pr(_msg("Trophies: ", f"{self.ctx.trophies}/{self.ctx.trophy_requirement}"))
        pr(_msg("Unlocked characters: ", ", ".join([game_data.CHARACTERS[c].name for c in gs.unlocked_characters])))
        pr(_msg("Unlocked karts (upgrades): ", ", ".join([f"{game_data.KARTS[c].name} ({(
            ", ".join(u.name for u in gs.kart_upgrades[c]))})" for c in gs.unlocked_karts])))
        pr(_msg("Speed upgrades: ", f"{gs.engine_upgrade_level} ({int(gs.calculate_speed_multiplier() * 100)} % speed)"))
        pr(_msg("Max vehicle class: ", ["50cc", "100cc", "150cc", "Mirror"][gs.unlocked_vehicle_class]))
        pr(_msg("Starting position: ", gs.starting_position + 1))
        pr(_msg("Unlocked cups: ", ", ".join([game_data.CUPS[c] for c in gs.unlocked_cups])))
        pr(_msg("Unlocked time trial courses: ", ", ".join([game_data.COURSES[c].name for c in gs.unlocked_courses])))
        item_box_msg = (_msg("Unlocked item box items", ""))
        if len(gs.global_items) > 0:
            item_box_msg.extend(_msg("\n    Everybody: ", ", ".join([item.name for item in gs.global_items])))
        for character, items in gs.character_items.items():
            if len(items) > 0:
                item_box_msg.extend(_msg(f"\n    {character.name}: ", ", ".join([item.name for item in items])))
        pr(item_box_msg)

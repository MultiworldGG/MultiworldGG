"""This module contains options for toggling the in game helpdesk"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class HelpDesk(DefaultOnToggle):
    """
    Determines if the in-game help desk should be enabled/disabled from the start.
    ------------------------------------------------------------------------------
    No:   Helpdesk is disabled when creating a new save.
    Yes:  Helpdesk is enabled when creating a new save.
    ------------------------------------------------------------------------------
    """
    display_name = RAC3OPTION.HELP_DESK

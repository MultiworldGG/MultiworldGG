import settings


class RACSizeMatterSettings(settings.Group):
    class GhostLinkEnabled(settings.Bool):
        """Host-level kill switch for Ghost Link: if disabled, no player's
        Ghost Link option has any effect regardless of what they set in
        their own YAML."""

    ghost_link: GhostLinkEnabled | bool = True

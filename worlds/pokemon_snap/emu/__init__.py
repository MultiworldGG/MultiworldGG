import abc

from typing import Sequence
from CommonClient import CommonContext, logger

from .ut_helper import universal_tracker_loaded
from ..client import PokemonSnapClient

if universal_tracker_loaded:
    from worlds.tracker.TrackerClient import TrackerCommandProcessor as ClientCommandProcessor
else:
    from CommonClient import ClientCommandProcessor

class PokemonSnapGenericEmuClient(abc.ABC):
    @abc.abstractmethod
    async def read(self, ctx: CommonContext, read_list: Sequence[tuple[int, int, str]]):
        ...

    @abc.abstractmethod
    async def write(self, ctx: CommonContext, write_list: Sequence[tuple[int, Sequence[int], str]]):
        ...

class PokemonSnapGenericCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext, server_address: str = None):
        if server_address:
            ctx.server_address = server_address
        super().__init__(ctx)

    def _get_client(self):
        if hasattr(self.ctx, 'client') and isinstance(self.ctx.client, PokemonSnapClient):
            return self.ctx.client
        if (
            hasattr(self.ctx, 'client_handler') and 
            hasattr(self.ctx.client_handler, 'client') and 
            isinstance(self.ctx.client_handler.client, PokemonSnapClient)
        ):
            return self.ctx.client_handler.client
        return None

    def _cmd_photo_log(self):
        """Gets the path to the photo log."""
        if (client := self._get_client()) is not None:
            logger.info(client.photo_log_path)

    def _cmd_invert_controls(self):
        """Toggles inverted camera controls (Y-axis only)."""
        if (client := self._get_client()) is not None:
            client.camera_inversion = 1 - client.camera_inversion if client.camera_inversion is not None else 1
            inversion = 'Inverted' if client.camera_inversion == 0 else 'Normal'
            logger.info(f'Camera controls set to {inversion}')
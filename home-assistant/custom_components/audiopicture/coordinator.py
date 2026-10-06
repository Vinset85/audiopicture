"""One bounded poll serves all sensor entities."""
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import AudioPictureError
from .const import DOMAIN

class AudioPictureCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry, client, info):
        super().__init__(hass, logging.getLogger(__name__), name=DOMAIN,
            config_entry=entry, update_interval=timedelta(seconds=30))
        self.client = client
        self.info = info

    async def _async_update_data(self):
        try:
            return await self.client.status(self.info["uuid"])
        except AudioPictureError as err:
            raise UpdateFailed(str(err)) from err

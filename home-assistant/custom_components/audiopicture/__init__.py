"""AudioPicture diagnostic integration."""
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import AudioPictureClient, AudioPictureError
from .coordinator import AudioPictureCoordinator

async def async_setup_entry(hass, entry):
    client = AudioPictureClient(async_get_clientsession(hass), entry.data[CONF_HOST], entry.data[CONF_PORT])
    try:
        info = await client.info()
        if info["uuid"] != entry.unique_id:
            raise AudioPictureError("Device identity changed")
    except AudioPictureError as err:
        raise ConfigEntryNotReady(str(err)) from err
    coordinator = AudioPictureCoordinator(hass, entry, client, info)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True

async def async_reload_entry(hass, entry):
    hass.config_entries.async_schedule_reload(entry.entry_id)

async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])

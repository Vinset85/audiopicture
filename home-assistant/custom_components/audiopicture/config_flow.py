"""Discover AudioPicture and verify its identity before adding it."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import AudioPictureClient, AudioPictureError
from .const import DOMAIN

class AudioPictureConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def _probe(self, host, port):
        client = AudioPictureClient(async_get_clientsession(self.hass), host, port)
        info = await client.info()
        await client.status(info["uuid"])
        await self.async_set_unique_id(info["uuid"])
        self._abort_if_unique_id_configured(updates={CONF_HOST: host, CONF_PORT: port}, reload_on_update=False)
        self.device_data = {CONF_HOST: host, CONF_PORT: port}
        self.device_title = f"AudioPicture {info['uuid'][:8]}"
        self.context["title_placeholders"] = {"name": self.device_title}

    async def async_step_zeroconf(self, discovery_info):
        try:
            await self._probe(discovery_info.host, discovery_info.port)
        except AudioPictureError:
            return self.async_abort(reason="cannot_connect")
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        if user_input is not None:
            # Recheck after user confirmation: an old discovery must not add a
            # different device that has inherited the DHCP address.
            expected = self.unique_id
            client = AudioPictureClient(async_get_clientsession(self.hass),
                self.device_data[CONF_HOST], self.device_data[CONF_PORT])
            try:
                info = await client.info()
                if info["uuid"] != expected:
                    return self.async_abort(reason="wrong_device")
                await client.status(expected)
            except AudioPictureError:
                return self.async_show_form(step_id="confirm", data_schema=vol.Schema({}),
                    errors={"base": "cannot_connect"})
            return self.async_create_entry(title=self.device_title, data=self.device_data)
        return self.async_show_form(step_id="confirm", data_schema=vol.Schema({}))

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                await self._probe(user_input[CONF_HOST], user_input.get(CONF_PORT, 80))
            except AudioPictureError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=self.device_title, data=self.device_data)
        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required(CONF_HOST): str, vol.Required(CONF_PORT, default=80): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
        }), errors=errors)

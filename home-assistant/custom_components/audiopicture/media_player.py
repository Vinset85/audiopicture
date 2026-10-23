"""Product media player surface for AudioPicture Rev.E.

Playback transport to the device is OPEN until firmware advertises capabilities.audio
and exposes stream endpoints. This entity still exposes role/group state and uses
room.py for planning so the HA product UI can ship ahead of the wire protocol.
"""
from __future__ import annotations
from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature, MediaPlayerState
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .room import RoomPlanError, RoomUnit, plan as plan_room

SUPPORT = MediaPlayerEntityFeature.VOLUME_SET | MediaPlayerEntityFeature.VOLUME_MUTE


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data
    async_add_entities([AudioPicturePlayer(coordinator, entry)])


class AudioPicturePlayer(CoordinatorEntity, MediaPlayerEntity):
    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_features = SUPPORT

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.unique_id}_player"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.unique_id)},
            "manufacturer": "Cinetyk",
            "model": coordinator.info.get("model", "OS-PF320-V22"),
            "sw_version": coordinator.info.get("firmware"),
        }
        self._volume = 0.4
        self._muted = False
        self._role = "solo"
        self._group_id = None

    @property
    def state(self):
        caps = self.coordinator.info.get("capabilities") or {}
        if not caps.get("audio"):
            return MediaPlayerState.OFF
        return MediaPlayerState.IDLE if not self._muted else MediaPlayerState.IDLE

    @property
    def volume_level(self):
        return self._volume

    @property
    def is_volume_muted(self):
        return self._muted

    @property
    def extra_state_attributes(self):
        return {
            "role": self._role,
            "group_id": self._group_id,
            "audio_capability": bool((self.coordinator.info.get("capabilities") or {}).get("audio")),
            "room_plan_ready": True,
        }

    async def async_set_volume_level(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, float(volume)))
        self.async_write_ha_state()

    async def async_mute_volume(self, mute: bool) -> None:
        self._muted = bool(mute)
        self.async_write_ha_state()

    async def async_apply_room_plan(self, units: list[dict], fill_delay_ms: float = 10.0, fill_trim_db: float = -3.0):
        """Validate a multi-unit plan with room.py; push to devices when API exists."""
        parsed = [
            RoomUnit(u["uuid"], u["role"], float(u["distance_m"]), int(u["firmware_major"]))
            for u in units
        ]
        members = plan_room(parsed, fill_delay_ms=fill_delay_ms, fill_trim_db=fill_trim_db)
        me = next((m for m in members if m.uuid == self._entry.unique_id), None)
        if me is None:
            raise RoomPlanError("This device is not in the plan")
        self._role = me.role
        self.async_write_ha_state()
        return [{"uuid": m.uuid, "role": m.role, "delay_us": m.delay_us, "trim_db": m.trim_db} for m in members]

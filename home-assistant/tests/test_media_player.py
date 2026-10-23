from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from homeassistant.const import CONF_HOST, CONF_PORT
from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.audiopicture.const import DOMAIN
from custom_components.audiopicture.media_player import AudioPicturePlayer
from custom_components.audiopicture.room import RoomPlanError
from .test_api import UUID, INFO, STATUS

pytestmark = pytest.mark.usefixtures("mock_async_zeroconf")
OTHER = "11111111-1111-4111-8111-111111111111"

@pytest.fixture
def client():
    with patch("custom_components.audiopicture.api.AudioPictureClient.info", new_callable=AsyncMock, return_value=INFO.copy()), patch("custom_components.audiopicture.api.AudioPictureClient.status", new_callable=AsyncMock, return_value=STATUS.copy()):
        yield

async def test_media_player_entity_off_without_audio(hass, client):
    entry = MockConfigEntry(domain=DOMAIN, unique_id=UUID, data={CONF_HOST: "ap.local", CONF_PORT: 80})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    players = hass.states.async_all("media_player")
    assert len(players) == 1
    assert players[0].state == "off"
    assert players[0].attributes["audio_capability"] is False
    assert players[0].attributes["role"] == "solo"

async def test_apply_room_plan_on_player():
    entry = MagicMock()
    entry.unique_id = UUID
    coord = MagicMock()
    coord.info = INFO
    player = AudioPicturePlayer(coord, entry)
    player.async_write_ha_state = MagicMock()
    result = await player.async_apply_room_plan([
        {"uuid": UUID, "role": "left", "distance_m": 2.0, "firmware_major": 1},
        {"uuid": OTHER, "role": "right", "distance_m": 3.0, "firmware_major": 1},
    ])
    assert result[0]["role"] == "left" and result[0]["delay_us"] > 0
    assert player._role == "left"
    with pytest.raises(RoomPlanError):
        await player.async_apply_room_plan([
            {"uuid": OTHER, "role": "solo", "distance_m": 2.0, "firmware_major": 1},
        ])

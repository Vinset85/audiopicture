from unittest.mock import AsyncMock, patch
import pytest
from homeassistant.config_entries import SOURCE_USER, SOURCE_ZEROCONF
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.audiopicture.api import AudioPictureError
from custom_components.audiopicture.const import DOMAIN
from .test_api import UUID, INFO, STATUS
pytestmark = pytest.mark.usefixtures("mock_async_zeroconf")

@pytest.fixture
def client():
    with patch("custom_components.audiopicture.api.AudioPictureClient.info",new_callable=AsyncMock,return_value=INFO.copy()) as info, patch("custom_components.audiopicture.api.AudioPictureClient.status",new_callable=AsyncMock,return_value=STATUS.copy()) as status:
        yield info,status

def discovery(host="192.0.2.12"):
    return ZeroconfServiceInfo(ip_address=__import__('ipaddress').ip_address(host),ip_addresses=[__import__('ipaddress').ip_address(host)],port=80,hostname="audiopicture.local.",type="_audiopicture._tcp.local.",name="AudioPicture._audiopicture._tcp.local.",properties={"uuid":UUID})

async def test_manual_retry_duplicate(hass,client):
    with patch("custom_components.audiopicture.async_setup_entry",return_value=True):
        flow=await hass.config_entries.flow.async_init(DOMAIN,context={"source":SOURCE_USER})
        assert flow["type"]==FlowResultType.FORM
        client[0].side_effect=AudioPictureError("offline")
        flow=await hass.config_entries.flow.async_configure(flow["flow_id"],{CONF_HOST:"ap.local",CONF_PORT:80})
        assert flow["errors"]=={"base":"cannot_connect"}
        client[0].side_effect=None
        flow=await hass.config_entries.flow.async_configure(flow["flow_id"],{CONF_HOST:"ap.local",CONF_PORT:80})
        assert flow["type"]==FlowResultType.CREATE_ENTRY
        await hass.async_block_till_done()
        again=await hass.config_entries.flow.async_init(DOMAIN,context={"source":SOURCE_USER},data={CONF_HOST:"ap.local",CONF_PORT:80})
        assert again["reason"]=="already_configured"

async def test_discovery_confirm(hass,client):
    with patch("custom_components.audiopicture.async_setup_entry",return_value=True):
        flow=await hass.config_entries.flow.async_init(DOMAIN,context={"source":SOURCE_ZEROCONF},data=discovery())
        assert flow["step_id"]=="confirm"
        client[0].side_effect=AudioPictureError("offline")
        retry=await hass.config_entries.flow.async_configure(flow["flow_id"],{})
        assert retry["errors"]=={"base":"cannot_connect"}
        client[0].side_effect=None
        done=await hass.config_entries.flow.async_configure(flow["flow_id"],{})
        assert done["type"]==FlowResultType.CREATE_ENTRY
        assert done["result"].unique_id==UUID
        await hass.async_block_till_done()

async def test_discovery_invalid(hass,client):
    client[1].side_effect=AudioPictureError("bad status")
    flow=await hass.config_entries.flow.async_init(DOMAIN,context={"source":SOURCE_ZEROCONF},data=discovery())
    assert flow["reason"]=="cannot_connect"

async def test_discovery_identity_changes(hass,client):
    flow=await hass.config_entries.flow.async_init(DOMAIN,context={"source":SOURCE_ZEROCONF},data=discovery())
    client[0].return_value=INFO|{"uuid":"33333333-3333-4333-8333-333333333333"}
    flow=await hass.config_entries.flow.async_configure(flow["flow_id"],{})
    assert flow["reason"]=="wrong_device"

async def test_setup_sensors_failure_recovery_unload(hass,client):
    entry=MockConfigEntry(domain=DOMAIN,unique_id=UUID,data={CONF_HOST:"ap.local",CONF_PORT:80})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    states=hass.states.async_all("sensor")
    assert len(states)==7
    temp=next(s for s in states if s.entity_id.endswith("temperature_raw"))
    assert temp.state=="21.5"
    assert sum(s.state=="unavailable" for s in states)==6
    coordinator=entry.runtime_data
    client[1].side_effect=AudioPictureError("offline")
    await coordinator.async_refresh(); await hass.async_block_till_done()
    assert hass.states.get(temp.entity_id).state=="unavailable"
    client[1].side_effect=None
    await coordinator.async_refresh(); await hass.async_block_till_done()
    assert hass.states.get(temp.entity_id).state=="21.5"
    from custom_components.audiopicture.diagnostics import async_get_config_entry_diagnostics
    diag=await async_get_config_entry_diagnostics(hass,entry)
    assert "uuid" not in str(diag) and "ap.local" not in str(diag)
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

async def test_setup_wrong_uuid(hass,client):
    entry=MockConfigEntry(domain=DOMAIN,unique_id="other",data={CONF_HOST:"ap.local",CONF_PORT:80})
    entry.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(entry.entry_id)

async def test_rediscovery_updates_address(hass,client):
    entry=MockConfigEntry(domain=DOMAIN,unique_id=UUID,data={CONF_HOST:"192.0.2.1",CONF_PORT:80})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    with patch.object(hass.config_entries,"async_reload",new_callable=AsyncMock,return_value=True) as reload:
        flow=await hass.config_entries.flow.async_init(DOMAIN,context={"source":SOURCE_ZEROCONF},data=discovery("192.0.2.2"))
        await hass.async_block_till_done()
        assert flow["reason"]=="already_configured"
        assert entry.data[CONF_HOST]=="192.0.2.2"
        reload.assert_awaited_once_with(entry.entry_id)
    await hass.config_entries.async_unload(entry.entry_id)

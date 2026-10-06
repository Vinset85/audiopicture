import json
from unittest.mock import AsyncMock
import pytest
from aiohttp import web, ClientSession
from custom_components.audiopicture.api import AudioPictureClient, AudioPictureError, endpoint, identity
from custom_components.audiopicture.const import METRICS
UUID = "22222222-2222-4222-8222-222222222222"
INFO = {"api_version":1,"uuid":UUID,"model":"OS-PF320-V22","firmware":"0.1.0","capabilities":{"environment":True}}
STATUS = {"api_version":1,"uuid":UUID,**dict.fromkeys(METRICS, None),"temperature_raw_c":21.5}

@pytest.mark.parametrize("host,port", [("http://127.0.0.1",80),("u@host",80),("host/path",80),("",80),("host",0),("host",True),("host",65536)])
def test_address_rejects_urls(host, port):
    with pytest.raises(AudioPictureError): endpoint(host,port)

def test_ipv6_and_uuid():
    assert str(endpoint("::1",80)) == "http://[::1]"
    assert identity(INFO) == UUID
    for value in (None, {}, [], {"api_version":True,"uuid":UUID}, {"api_version":1,"uuid":"bad"}):
        with pytest.raises(AudioPictureError): identity(value)

@pytest.mark.parametrize("mutation", [{"temperature_raw_c":float("nan")},{"temperature_raw_c":True},{"humidity_raw_percent":101},{"bus_voltage_v":-1},{"uuid":"33333333-3333-4333-8333-333333333333"},{"api_version":2},{"bus_voltage_v":10**1000}])
async def test_invalid_status(mutation):
    c=AudioPictureClient(None,"device.local"); c._get=AsyncMock(return_value=STATUS|mutation)
    with pytest.raises(AudioPictureError): await c.status(UUID)

async def test_incomplete_status():
    c=AudioPictureClient(None,"device.local"); c._get=AsyncMock(return_value={"api_version":1,"uuid":UUID})
    with pytest.raises(AudioPictureError): await c.status(UUID)

async def test_info_rejects_wrong_device():
    c=AudioPictureClient(None,"device.local")
    for data in (INFO|{"model":"different"}, INFO|{"capabilities":None}, INFO|{"firmware":False}):
        c._get=AsyncMock(return_value=data)
        with pytest.raises(AudioPictureError): await c.info()

async def test_real_http_transport(aiohttp_server, socket_enabled):
    async def info(request): return web.json_response(INFO)
    async def status(request): return web.json_response(STATUS)
    app=web.Application(); app.router.add_get("/api/v1/info",info); app.router.add_get("/api/v1/status",status)
    server=await aiohttp_server(app)
    async with ClientSession() as session:
        c=AudioPictureClient(session,"127.0.0.1",server.port)
        assert (await c.info())["uuid"]==UUID
        assert (await c.status(UUID))["temperature_raw_c"]==21.5

@pytest.mark.parametrize("kind",["redirect","large","invalid_json","array","html","error"])
async def test_bad_http(aiohttp_server, socket_enabled, kind):
    async def handler(request):
        if kind=="redirect": raise web.HTTPFound("/elsewhere")
        if kind=="large": return web.Response(body=b"{"+b" "*17000+b"}",content_type="application/json")
        if kind=="invalid_json": return web.Response(text="broken",content_type="application/json")
        if kind=="array": return web.json_response([])
        if kind=="html": return web.Response(text="<html>",content_type="text/html")
        return web.Response(status=503)
    app=web.Application(); app.router.add_get("/api/v1/info",handler); server=await aiohttp_server(app)
    async with ClientSession() as session:
        c=AudioPictureClient(session,"127.0.0.1",server.port)
        with pytest.raises(AudioPictureError): await c.info()

async def test_invalid_uuid_type():
    with pytest.raises(AudioPictureError): identity({"api_version":1,"uuid":17})
    with pytest.raises(AudioPictureError): endpoint("[broken",80)

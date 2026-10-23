import math
import pytest
from custom_components.audiopicture.room import (MAX_DELAY_US, RoomPlanError, RoomUnit, payload, plan, validate)
A = "11111111-1111-4111-8111-111111111111"
B = "22222222-2222-4222-8222-222222222222"
C = "33333333-3333-4333-8333-333333333333"

def unit(uuid=A, role="solo", distance=2.0, major=1):
    return RoomUnit(uuid, role, distance, major)

def test_solo_unit_is_untouched():
    [m] = plan([unit()])
    assert (m.role, m.delay_us, m.trim_db) == ("solo", 0, 0.0)

def test_stereo_pair_aligns_time_and_level():
    left, right = plan([unit(A, "left", 2.0), unit(B, "right", 3.0)])
    assert left.delay_us == round(1.0 / 343.0 * 1e6) == 2915
    assert right.delay_us == 0 and right.trim_db == 0.0
    assert left.trim_db == pytest.approx(-20 * math.log10(1.5), abs=0.01)

def test_fill_is_delayed_and_attenuated():
    members = plan([unit(A, "left", 3.0), unit(B, "right", 3.0), unit(C, "fill", 3.0)], fill_delay_ms=12.5)
    fill = members[2]
    assert fill.delay_us == 12500 and fill.trim_db == -3.0
    assert all(m.delay_us == 0 and m.trim_db == 0.0 for m in members[:2])

def test_group_of_fills_without_stereo():
    members = plan([unit(A, "fill", 1.0), unit(B, "fill", 4.0)], fill_delay_ms=0, fill_trim_db=0)
    assert members[0].delay_us == round(3.0 / 343.0 * 1e6)
    assert members[0].trim_db == pytest.approx(-12.04, abs=0.01)

@pytest.mark.parametrize("units", [
    [],
    [unit(role="left")],
    [unit(A, "solo"), unit(B, "fill")],
    [unit(A, "left"), unit(B, "fill")],
    [unit(A, "left"), unit(B, "right"), unit(C, "left")],
    [unit(A, "left"), unit(A, "right")],
    [unit(A, "left"), unit(B, "right", major=2)],
    [unit(role="center")],
    [unit(uuid="bad")],
    [unit(distance=0.1)],
    [unit(distance=float("nan"))],
    [unit(distance=True)],
    [unit(major=True)],
    [unit(major=-1)],
    [unit("%08d-1111-4111-8111-111111111111" % i, "fill") for i in range(9)],
])
def test_firmware_rules_are_mirrored(units):
    with pytest.raises(RoomPlanError):
        validate(units)

def test_uuid_case_is_duplicate():
    with pytest.raises(RoomPlanError):
        validate([unit(A, "left"), unit(A.upper(), "right")])

def test_limits_fail_closed():
    with pytest.raises(RoomPlanError, match="Trim"):
        plan([unit(A, "fill", 0.3), unit(B, "fill", 15.0)], fill_delay_ms=0)
    with pytest.raises(RoomPlanError, match="Delay"):
        plan([unit(A, "fill", 3.0), unit(B, "fill", 15.0)], fill_delay_ms=30)
    with pytest.raises(RoomPlanError, match="Invalid unit"):
        validate([{"uuid": A, "role": "solo"}])
    with pytest.raises(RoomPlanError):
        plan([unit(A, "left"), unit(B, "right")], fill_delay_ms=31)
    with pytest.raises(RoomPlanError):
        plan([unit(A, "left"), unit(B, "right")], fill_trim_db=1)
    far = plan([unit(A, "fill", 10.0), unit(B, "fill", 15.0)], fill_delay_ms=30)
    assert max(m.delay_us for m in far) <= MAX_DELAY_US

def test_payload_shape():
    body = payload("44444444-4444-4444-8444-444444444444", plan([unit(A, "left", 2.0), unit(B, "right", 2.5)]))
    assert body["api_version"] == 1 and len(body["members"]) == 2
    assert set(body["members"][0]) == {"uuid", "role", "delay_us", "trim_db"}
    with pytest.raises(RoomPlanError):
        payload("nope", [])

"""Room planner for several mono AudioPicture units; mirrors firmware ap_room rules.

Pure logic: no I/O and no device writes. Distances are listener-to-unit estimates;
acoustic calibration with the raw microphones must refine the result on site.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from uuid import UUID

ROLES = ("solo", "left", "right", "fill")
MAX_MEMBERS = 8
MAX_DELAY_US = 50_000
MIN_TRIM_DB = -30.0
SPEED_OF_SOUND_M_S = 343.0
DISTANCE_RANGE_M = (0.3, 15.0)
FILL_DELAY_RANGE_MS = (0.0, 30.0)
FILL_TRIM_RANGE_DB = (-12.0, 0.0)

class RoomPlanError(ValueError):
    """Room layout that the firmware would reject."""

@dataclass(frozen=True)
class RoomUnit:
    uuid: str
    role: str
    distance_m: float
    firmware_major: int

@dataclass(frozen=True)
class RoomMember:
    uuid: str
    role: str
    delay_us: int
    trim_db: float

def _number(value, low: float, high: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RoomPlanError(f"{name} must be a number")
    value = float(value)
    if not math.isfinite(value) or not low <= value <= high:
        raise RoomPlanError(f"{name} out of range")
    return value

def validate(units: list[RoomUnit]) -> None:
    if not isinstance(units, (list, tuple)) or not units:
        raise RoomPlanError("Room is empty")
    if len(units) > MAX_MEMBERS:
        raise RoomPlanError("Too many units")
    seen = set()
    for unit in units:
        if not isinstance(unit, RoomUnit):
            raise RoomPlanError("Invalid unit")
        try:
            key = UUID(unit.uuid)
        except (ValueError, TypeError, AttributeError) as err:
            raise RoomPlanError("Invalid UUID") from err
        if key in seen:
            raise RoomPlanError("Duplicate unit")
        seen.add(key)
        if unit.role not in ROLES:
            raise RoomPlanError("Invalid role")
        _number(unit.distance_m, *DISTANCE_RANGE_M, "distance_m")
        if isinstance(unit.firmware_major, bool) or not isinstance(unit.firmware_major, int) or unit.firmware_major < 0:
            raise RoomPlanError("Invalid firmware major")
    roles = [unit.role for unit in units]
    if len(units) == 1:
        if roles[0] != "solo":
            raise RoomPlanError("A lone unit must be solo")
        return
    if "solo" in roles:
        raise RoomPlanError("Solo is not allowed in a group")
    if roles.count("left") != roles.count("right") or roles.count("left") > 1:
        raise RoomPlanError("Stereo needs exactly one left and one right")
    if len({unit.firmware_major for unit in units}) != 1:
        raise RoomPlanError("Firmware major mismatch")

def plan(units: list[RoomUnit], fill_delay_ms: float = 10.0, fill_trim_db: float = -3.0) -> list[RoomMember]:
    """Align arrivals at the listener, equalise level by 1/r, then delay fills.

    The extra fill delay keeps localisation on the main units (precedence effect).
    """
    validate(units)
    fill_delay_us = _number(fill_delay_ms, *FILL_DELAY_RANGE_MS, "fill_delay_ms") * 1000.0
    fill_trim = _number(fill_trim_db, *FILL_TRIM_RANGE_DB, "fill_trim_db")
    farthest = max(float(unit.distance_m) for unit in units)
    members = []
    for unit in units:
        distance = float(unit.distance_m)
        delay = (farthest - distance) / SPEED_OF_SOUND_M_S * 1e6
        trim = -20.0 * math.log10(farthest / distance)
        if unit.role == "fill":
            delay += fill_delay_us
            trim += fill_trim
        delay_us = round(delay)
        trim = round(trim, 2)
        if delay_us > MAX_DELAY_US:
            raise RoomPlanError("Delay beyond firmware limit")
        if trim < MIN_TRIM_DB:
            raise RoomPlanError("Trim beyond firmware limit")
        members.append(RoomMember(str(UUID(unit.uuid)), unit.role, delay_us, 0.0 if trim == 0 else trim))
    return members

def payload(group_id: str, members: list[RoomMember]) -> dict:
    """JSON body for the future device room-plan endpoint (API v1 shape)."""
    try:
        group = str(UUID(group_id))
    except (ValueError, TypeError, AttributeError) as err:
        raise RoomPlanError("Invalid group id") from err
    return {"api_version": 1, "group_id": group, "members": [
        {"uuid": m.uuid, "role": m.role, "delay_us": m.delay_us, "trim_db": m.trim_db} for m in members]}

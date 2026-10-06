"""Shared protocol constants."""
DOMAIN = "audiopicture"
MODEL = "OS-PF320-V22"
METRICS = {
    "temperature_raw_c": (-45, 130),
    "humidity_raw_percent": (0, 100),
    "illuminance_raw_lux": (0, 83865.6),
    "bus_voltage_v": (0, 85),
    "current_nominal_shunt_a": (-5.12, 5.12),
    "power_calculated_w": (-435.2, 435.2),
    "monitor_die_c": (-256, 256),
}

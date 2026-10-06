"""Raw readings remain explicitly labelled until product calibration exists."""
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory, UnitOfTemperature, UnitOfElectricPotential, UnitOfElectricCurrent, UnitOfPower, PERCENTAGE, LIGHT_LUX
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
PARALLEL_UPDATES = 0
SENSORS = (
    ("temperature_raw_c", "Temperature raw", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ("humidity_raw_percent", "Humidity raw", SensorDeviceClass.HUMIDITY, PERCENTAGE),
    ("illuminance_raw_lux", "Illuminance raw", SensorDeviceClass.ILLUMINANCE, LIGHT_LUX),
    ("bus_voltage_v", "Supply voltage", SensorDeviceClass.VOLTAGE, UnitOfElectricPotential.VOLT),
    ("current_nominal_shunt_a", "Current nominal shunt", SensorDeviceClass.CURRENT, UnitOfElectricCurrent.AMPERE),
    ("power_calculated_w", "Power calculated", SensorDeviceClass.POWER, UnitOfPower.WATT),
    ("monitor_die_c", "Power monitor die temperature", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
)
async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities(AudioPictureSensor(entry.runtime_data, row) for row in SENSORS)

class AudioPictureSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    def __init__(self, coordinator, row):
        super().__init__(coordinator)
        key, name, device_class, unit = row
        self.entity_description = SensorEntityDescription(key=key, name=name,
            device_class=device_class, native_unit_of_measurement=unit,
            state_class=SensorStateClass.MEASUREMENT)
        info = coordinator.info
        self._attr_unique_id = f"{info['uuid']}_{key}"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, info['uuid'])},
            name=f"AudioPicture {info['uuid'][:8]}", manufacturer="AudioPicture",
            model=info["model"], sw_version=info["firmware"])
    @property
    def native_value(self):
        return self.coordinator.data.get(self.entity_description.key)
    @property
    def available(self):
        return super().available and self.native_value is not None

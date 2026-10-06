"""Export diagnostics without address, UUID or provisioning information."""
async def async_get_config_entry_diagnostics(hass, entry):
    coordinator = entry.runtime_data
    return {"model": coordinator.info["model"],
            "firmware": coordinator.info["firmware"],
            "stage": coordinator.info.get("stage"),
            "last_update_success": coordinator.last_update_success,
            "sensor_errors": coordinator.data.get("sensor_errors", {}),
            "inhibit_reason": coordinator.data.get("inhibit_reason")}

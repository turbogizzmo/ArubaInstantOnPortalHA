"""Binary sensors for Aruba Instant On infrastructure."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ArubaInstantOnConfigEntry
from .entity import ArubaInstantOnDeviceEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ArubaInstantOnConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up infrastructure connectivity sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        ArubaInstantOnDeviceConnectivity(coordinator, device)
        for device in coordinator.data["inventory"]
    )


class ArubaInstantOnDeviceConnectivity(
    ArubaInstantOnDeviceEntity, BinarySensorEntity
):
    """Connectivity state for an Instant On AP or switch."""

    _attr_name = "Connectivity"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator, device: dict[str, Any]) -> None:
        super().__init__(coordinator, device, "connectivity")

    @property
    def is_on(self) -> bool | None:
        device = self.device_data
        if device is None:
            return None
        return (
            device.get("status") == "up"
            or device.get("operationalState") == "up"
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        device = self.device_data or {}
        return {
            "device_type": device.get("deviceType"),
            "ip_address": device.get("ipAddress"),
            "mac_address": device.get("macAddress"),
            "operational_state": device.get("operationalState"),
        }

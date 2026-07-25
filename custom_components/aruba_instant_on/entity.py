"""Shared Aruba Instant On entities."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ArubaInstantOnCoordinator


class ArubaInstantOnSiteEntity(
    CoordinatorEntity[ArubaInstantOnCoordinator]
):
    """Base entity representing an Instant On site."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: ArubaInstantOnCoordinator, key: str
    ) -> None:
        super().__init__(coordinator)
        self._key = key
        site = coordinator.data["site"]
        self._site_id = site["id"]
        self._site_name = site.get("name", self._site_id)
        self._attr_unique_id = f"{self._site_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._site_id)},
            name=self._site_name,
            manufacturer="HPE Aruba Networking",
            model="Instant On Site",
            configuration_url=(
                "https://portal.arubainstanton.com/"
                f"#/sites/{self._site_id}"
            ),
        )


class ArubaInstantOnDeviceEntity(
    CoordinatorEntity[ArubaInstantOnCoordinator]
):
    """Base entity representing an Instant On network device."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ArubaInstantOnCoordinator,
        device: dict[str, Any],
        key: str,
    ) -> None:
        super().__init__(coordinator)
        self._device_id = str(
            device.get("id")
            or device.get("serialNumber")
            or device.get("macAddress")
        )
        self._key = key
        self._attr_unique_id = f"{self._device_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=device.get("name") or self._device_id,
            manufacturer="HPE Aruba Networking",
            model=device.get("model"),
            serial_number=device.get("serialNumber"),
            configuration_url="https://portal.arubainstanton.com/",
            via_device=(DOMAIN, coordinator.data["site"]["id"]),
        )

    @property
    def device_data(self) -> dict[str, Any] | None:
        """Return the latest data for this infrastructure device."""
        for device in self.coordinator.data["inventory"]:
            identity = str(
                device.get("id")
                or device.get("serialNumber")
                or device.get("macAddress")
            )
            if identity == self._device_id:
                return device
        return None

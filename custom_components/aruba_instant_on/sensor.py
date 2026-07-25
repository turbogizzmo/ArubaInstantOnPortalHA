"""Sensors for Aruba Instant On."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfDataRate,
    UnitOfInformation,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ArubaInstantOnConfigEntry
from .entity import ArubaInstantOnDeviceEntity, ArubaInstantOnSiteEntity


@dataclass(frozen=True, kw_only=True)
class ArubaSiteSensorDescription(SensorEntityDescription):
    """Describe a site-level sensor."""

    value_fn: Callable[[dict[str, Any]], int | str | None]


def _inventory(data: dict[str, Any]) -> list[dict[str, Any]]:
    return data["inventory"]


def _online_devices(
    data: dict[str, Any], device_type: str | None = None
) -> int:
    devices = _inventory(data)
    if device_type:
        devices = [
            device
            for device in devices
            if device.get("deviceType") == device_type
        ]
    return sum(
        1
        for device in devices
        if (
            device.get("status") == "up"
            or device.get("operationalState") == "up"
        )
    )


def _numeric_sum(items: list[dict[str, Any]], key: str) -> float:
    return sum(
        float(item.get(key) or 0)
        for item in items
        if isinstance(item.get(key), (int, float))
    )


def _numeric_average(
    items: list[dict[str, Any]], key: str
) -> float | None:
    values = [
        float(item[key])
        for item in items
        if isinstance(item.get(key), (int, float))
    ]
    if not values:
        return None
    return round(sum(values) / len(values), 1)


def _band_clients(data: dict[str, Any], key: str) -> int:
    return int(_numeric_sum(data["networks"], key))


SITE_SENSORS = (
    ArubaSiteSensorDescription(
        key="infrastructure_devices",
        translation_key="infrastructure_devices",
        name="Infrastructure devices",
        icon="mdi:access-point-network",
        native_unit_of_measurement="devices",
        value_fn=lambda data: len(_inventory(data)),
    ),
    ArubaSiteSensorDescription(
        key="devices_online",
        translation_key="devices_online",
        name="Devices online",
        icon="mdi:lan-check",
        native_unit_of_measurement="devices",
        value_fn=lambda data: _online_devices(data),
    ),
    ArubaSiteSensorDescription(
        key="access_points_online",
        translation_key="access_points_online",
        name="Access points online",
        icon="mdi:access-point",
        native_unit_of_measurement="APs",
        value_fn=lambda data: _online_devices(data, "accessPoint"),
    ),
    ArubaSiteSensorDescription(
        key="switches_online",
        translation_key="switches_online",
        name="Switches online",
        icon="mdi:switch",
        native_unit_of_measurement="switches",
        value_fn=lambda data: _online_devices(data, "switch"),
    ),
    ArubaSiteSensorDescription(
        key="wireless_clients",
        translation_key="wireless_clients",
        name="Wireless clients",
        icon="mdi:wifi",
        native_unit_of_measurement="clients",
        value_fn=lambda data: len(data["wireless_clients"]),
    ),
    ArubaSiteSensorDescription(
        key="wired_clients",
        translation_key="wired_clients",
        name="Wired clients",
        icon="mdi:ethernet",
        native_unit_of_measurement="clients",
        value_fn=lambda data: (
            None
            if data["wired_clients"] is None
            else len(data["wired_clients"])
        ),
    ),
    ArubaSiteSensorDescription(
        key="wireless_networks",
        translation_key="wireless_networks",
        name="Wireless networks",
        icon="mdi:wifi-cog",
        native_unit_of_measurement="networks",
        value_fn=lambda data: len(data["networks"]),
    ),
    ArubaSiteSensorDescription(
        key="major_alerts",
        translation_key="major_alerts",
        name="Major alerts",
        icon="mdi:alert-circle",
        native_unit_of_measurement="alerts",
        value_fn=lambda data: data["alerts"].get(
            "activeMajorAlertsCount", 0
        ),
    ),
    ArubaSiteSensorDescription(
        key="minor_alerts",
        translation_key="minor_alerts",
        name="Minor alerts",
        icon="mdi:alert",
        native_unit_of_measurement="alerts",
        value_fn=lambda data: data["alerts"].get(
            "activeMinorAlertsCount", 0
        ),
    ),
    ArubaSiteSensorDescription(
        key="info_alerts",
        translation_key="info_alerts",
        name="Information alerts",
        icon="mdi:information",
        native_unit_of_measurement="alerts",
        value_fn=lambda data: data["alerts"].get(
            "activeInfoAlertsCount", 0
        ),
    ),
    ArubaSiteSensorDescription(
        key="download_throughput",
        translation_key="download_throughput",
        name="Download throughput",
        icon="mdi:download-network",
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        suggested_display_precision=2,
        value_fn=lambda data: round(
            _numeric_sum(
                data["wireless_clients"],
                "downstreamThroughputInBitsPerSecond",
            )
            / 1_000_000,
            2,
        ),
    ),
    ArubaSiteSensorDescription(
        key="upload_throughput",
        translation_key="upload_throughput",
        name="Upload throughput",
        icon="mdi:upload-network",
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        suggested_display_precision=2,
        value_fn=lambda data: round(
            _numeric_sum(
                data["wireless_clients"],
                "upstreamThroughputInBitsPerSecond",
            )
            / 1_000_000,
            2,
        ),
    ),
    ArubaSiteSensorDescription(
        key="download_24h",
        translation_key="download_24h",
        name="Downloaded in 24 hours",
        icon="mdi:database-arrow-down",
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
        value_fn=lambda data: round(
            _numeric_sum(
                data["application_usage"],
                "downstreamDataTransferredDuringLast24HoursInBytes",
            )
            / 1_000_000_000,
            2,
        ),
    ),
    ArubaSiteSensorDescription(
        key="upload_24h",
        translation_key="upload_24h",
        name="Uploaded in 24 hours",
        icon="mdi:database-arrow-up",
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
        value_fn=lambda data: round(
            _numeric_sum(
                data["application_usage"],
                "upstreamDataTransferredDuringLast24HoursInBytes",
            )
            / 1_000_000_000,
            2,
        ),
    ),
    ArubaSiteSensorDescription(
        key="clients_24ghz",
        translation_key="clients_24ghz",
        name="2.4 GHz clients",
        icon="mdi:wifi",
        native_unit_of_measurement="clients",
        value_fn=lambda data: _band_clients(
            data, "wireless24GHzClientsCount"
        ),
    ),
    ArubaSiteSensorDescription(
        key="clients_5ghz",
        translation_key="clients_5ghz",
        name="5 GHz clients",
        icon="mdi:wifi",
        native_unit_of_measurement="clients",
        value_fn=lambda data: _band_clients(
            data, "wireless5GHzClientsCount"
        ),
    ),
    ArubaSiteSensorDescription(
        key="clients_6ghz",
        translation_key="clients_6ghz",
        name="6 GHz clients",
        icon="mdi:wifi",
        native_unit_of_measurement="clients",
        value_fn=lambda data: _band_clients(
            data, "wireless6GHzClientsCount"
        ),
    ),
    ArubaSiteSensorDescription(
        key="average_signal",
        translation_key="average_signal",
        name="Average client signal",
        icon="mdi:signal",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="dBm",
        value_fn=lambda data: _numeric_average(
            data["wireless_clients"], "signalInDbm"
        ),
    ),
    ArubaSiteSensorDescription(
        key="average_snr",
        translation_key="average_snr",
        name="Average client SNR",
        icon="mdi:signal-distance-variant",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="dB",
        value_fn=lambda data: _numeric_average(
            data["wireless_clients"], "snrInDb"
        ),
    ),
    ArubaSiteSensorDescription(
        key="poor_signal_clients",
        translation_key="poor_signal_clients",
        name="Poor signal clients",
        icon="mdi:wifi-alert",
        native_unit_of_measurement="clients",
        value_fn=lambda data: sum(
            1
            for client in data["wireless_clients"]
            if isinstance(client.get("signalInDbm"), (int, float))
            and float(client["signalInDbm"]) < -70
        ),
    ),
    ArubaSiteSensorDescription(
        key="poe_power",
        translation_key="poe_power",
        name="PoE power",
        icon="mdi:ethernet-cable",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=1,
        value_fn=lambda data: round(
            _numeric_sum(
                data["inventory"], "poePseConsumedPowerInWatts"
            ),
            1,
        ),
    ),
    ArubaSiteSensorDescription(
        key="firmware_updates",
        translation_key="firmware_updates",
        name="Devices needing firmware",
        icon="mdi:update",
        native_unit_of_measurement="devices",
        value_fn=lambda data: sum(
            1
            for device in data["inventory"]
            if device.get("isUpToDate") is False
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ArubaInstantOnConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Aruba Instant On sensors."""
    coordinator = entry.runtime_data
    entities: list[SensorEntity] = [
        ArubaInstantOnSiteSensor(coordinator, description)
        for description in SITE_SENSORS
    ]
    entities.extend(
        ArubaInstantOnDeviceUptimeSensor(coordinator, device)
        for device in coordinator.data["inventory"]
        if device.get("uptimeInSeconds") is not None
    )
    async_add_entities(entities)


class ArubaInstantOnSiteSensor(
    ArubaInstantOnSiteEntity, SensorEntity
):
    """Site-level Instant On sensor."""

    entity_description: ArubaSiteSensorDescription

    def __init__(
        self, coordinator, description: ArubaSiteSensorDescription
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> int | str | None:
        return self.entity_description.value_fn(self.coordinator.data)


class ArubaInstantOnDeviceUptimeSensor(
    ArubaInstantOnDeviceEntity, SensorEntity
):
    """Uptime sensor for an Instant On AP or switch."""

    _attr_name = "Uptime"
    _attr_icon = "mdi:timer-outline"
    _attr_native_unit_of_measurement = UnitOfTime.HOURS
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator, device: dict[str, Any]) -> None:
        super().__init__(coordinator, device, "uptime")

    @property
    def native_value(self) -> float | None:
        device = self.device_data
        if not device or device.get("uptimeInSeconds") is None:
            return None
        return round(float(device["uptimeInSeconds"]) / 3600, 1)

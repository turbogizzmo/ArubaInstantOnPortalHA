"""Aruba Instant On integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ArubaInstantOnClient
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_SITE_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import ArubaInstantOnCoordinator

type ArubaInstantOnConfigEntry = ConfigEntry[ArubaInstantOnCoordinator]


async def async_setup_entry(
    hass: HomeAssistant, entry: ArubaInstantOnConfigEntry
) -> bool:
    """Set up Aruba Instant On from a config entry."""
    client = ArubaInstantOnClient(
        async_get_clientsession(hass),
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        entry.data[CONF_SITE_ID],
    )
    interval = int(
        entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
    )
    coordinator = ArubaInstantOnCoordinator(
        hass,
        entry,
        client,
        timedelta(seconds=interval),
    )
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ArubaInstantOnConfigEntry
) -> bool:
    """Unload an Aruba Instant On config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_reload_entry(
    hass: HomeAssistant, entry: ArubaInstantOnConfigEntry
) -> None:
    await hass.config_entries.async_reload(entry.entry_id)

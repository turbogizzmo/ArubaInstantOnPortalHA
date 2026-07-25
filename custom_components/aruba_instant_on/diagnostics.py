"""Diagnostics for Aruba Instant On."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import ArubaInstantOnConfigEntry

TO_REDACT = {
    "password",
    "username",
    "serialNumber",
    "macAddress",
    "ipAddress",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ArubaInstantOnConfigEntry
) -> dict[str, Any]:
    """Return redacted diagnostics."""
    return {
        "config_entry": async_redact_data(dict(entry.data), TO_REDACT),
        "data": async_redact_data(entry.runtime_data.data, TO_REDACT),
    }

"""Diagnostics for Aruba Instant On."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import REDACTED
from homeassistant.core import HomeAssistant

from . import ArubaInstantOnConfigEntry

# Exact keys (case-insensitive) that are always redacted.
TO_REDACT = {
    "password",
    "username",
    "site_id",
    "id",
    "token",
    "access_token",
}
# Any key containing one of these fragments is also redacted, so identifiers
# the undocumented API returns under other names are covered too.
REDACT_FRAGMENTS = (
    "address",
    "email",
    "hostname",
    "ipv4",
    "ipv6",
    "latitude",
    "longitude",
    "mac",
    "name",
    "serial",
    "ssid",
)

# Client, network and application records describe the user's own devices
# and Wi-Fi networks, so only their size and field names are exported.
SUMMARIZE = (
    "wireless_clients",
    "wired_clients",
    "networks",
    "application_usage",
)


def _should_redact(key: str) -> bool:
    lowered = key.lower()
    if lowered in TO_REDACT or key.endswith(("Id", "_id")):
        return True
    return any(fragment in lowered for fragment in REDACT_FRAGMENTS)


def _redact(data: Any) -> Any:
    if isinstance(data, list):
        return [_redact(item) for item in data]
    if isinstance(data, dict):
        return {
            key: (
                REDACTED
                if isinstance(key, str) and _should_redact(key)
                else _redact(value)
            )
            for key, value in data.items()
        }
    return data


def _summarize(
    records: list[dict[str, Any]] | None,
) -> dict[str, Any] | None:
    if records is None:
        return None
    return {
        "count": len(records),
        "fields": sorted(
            {
                key
                for record in records
                if isinstance(record, dict)
                for key in record
            }
        ),
    }


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ArubaInstantOnConfigEntry
) -> dict[str, Any]:
    """Return redacted diagnostics."""
    data = dict(entry.runtime_data.data)
    for key in SUMMARIZE:
        if key in data:
            data[key] = _summarize(data[key])
    return {
        "config_entry": _redact(dict(entry.data)),
        "data": _redact(data),
    }

"""Data coordinator for Aruba Instant On."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import (
    ArubaInstantOnAuthenticationError,
    ArubaInstantOnClient,
    ArubaInstantOnConnectionError,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ArubaInstantOnCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate read-only Instant On polling."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: ArubaInstantOnClient,
        update_interval: timedelta,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=update_interval,
            config_entry=entry,
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.client.async_get_site_data()
        except ArubaInstantOnAuthenticationError as err:
            raise UpdateFailed(f"Authentication failed: {err}") from err
        except ArubaInstantOnConnectionError as err:
            raise UpdateFailed(f"Cloud update failed: {err}") from err

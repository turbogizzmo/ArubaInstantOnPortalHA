"""Config flow for Aruba Instant On."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    ArubaInstantOnAuthenticationError,
    ArubaInstantOnClient,
    ArubaInstantOnConnectionError,
)
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_SITE_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)


class ArubaInstantOnConfigFlow(
    config_entries.ConfigFlow, domain=DOMAIN
):
    """Handle an Aruba Instant On config flow."""

    VERSION = 1
    _available_sites: dict[str, dict[str, Any]]
    _pending_data: dict[str, Any]

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            client = ArubaInstantOnClient(
                async_get_clientsession(self.hass),
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
            )
            try:
                sites = await client.async_get_sites()
            except ArubaInstantOnAuthenticationError:
                errors["base"] = "invalid_auth"
            except ArubaInstantOnConnectionError:
                errors["base"] = "cannot_connect"
            else:
                configured_site_ids = {
                    entry.data.get(CONF_SITE_ID)
                    for entry in self._async_current_entries()
                }
                valid_sites = {
                    site_id: site
                    for site in sites
                    if isinstance((site_id := site.get("id")), str)
                    and site_id
                }
                self._available_sites = {
                    site_id: site
                    for site_id, site in valid_sites.items()
                    if site_id not in configured_site_ids
                }
                if not valid_sites:
                    errors["base"] = "no_sites"
                elif not self._available_sites:
                    return self.async_abort(
                        reason="all_sites_configured"
                    )
                else:
                    self._pending_data = dict(user_input)
                    if len(self._available_sites) == 1:
                        site_id, site = next(
                            iter(self._available_sites.items())
                        )
                        return await self._async_create_site_entry(
                            site_id, site
                        )
                    return await self.async_step_site()

        schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=DEFAULT_SCAN_INTERVAL,
                ): vol.All(
                    vol.Coerce(int),
                    vol.Range(
                        min=MIN_SCAN_INTERVAL,
                        max=MAX_SCAN_INTERVAL,
                    ),
                ),
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    async def async_step_site(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Let the user select one of the discovered sites."""
        errors: dict[str, str] = {}
        if user_input is not None:
            site_id = user_input[CONF_SITE_ID]
            site = self._available_sites.get(site_id)
            if site is not None:
                return await self._async_create_site_entry(site_id, site)
            errors[CONF_SITE_ID] = "invalid_site"

        names = [
            str(site.get("name") or site_id)
            for site_id, site in self._available_sites.items()
        ]
        duplicate_names = {
            name for name in names if names.count(name) > 1
        }
        choices = {
            site_id: (
                f"{name} ({site_id})"
                if name in duplicate_names
                else name
            )
            for site_id, site in self._available_sites.items()
            if (name := str(site.get("name") or site_id))
        }
        return self.async_show_form(
            step_id="site",
            data_schema=vol.Schema(
                {vol.Required(CONF_SITE_ID): vol.In(choices)}
            ),
            errors=errors,
        )

    async def _async_create_site_entry(
        self, site_id: str, site: dict[str, Any]
    ) -> FlowResult:
        """Create a config entry for a discovered site."""
        await self.async_set_unique_id(site_id)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=str(site.get("name") or site_id),
            data={**self._pending_data, CONF_SITE_ID: site_id},
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> ArubaInstantOnOptionsFlow:
        return ArubaInstantOnOptionsFlow(config_entry)


class ArubaInstantOnOptionsFlow(config_entries.OptionsFlow):
    """Handle polling options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        current = self._config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self._config_entry.data.get(
                CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
            ),
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL, default=current
                    ): vol.All(
                        vol.Coerce(int),
                        vol.Range(
                            min=MIN_SCAN_INTERVAL,
                            max=MAX_SCAN_INTERVAL,
                        ),
                    )
                }
            ),
        )

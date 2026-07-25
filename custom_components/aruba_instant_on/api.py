"""Asynchronous client for the Aruba Instant On portal API."""

from __future__ import annotations

import base64
import hashlib
import secrets
import time
from typing import Any
from urllib.parse import parse_qs, urlparse

from aiohttp import ClientResponseError, ClientSession

PORTAL_URL = "https://portal.arubainstanton.com"
SSO_URL = "https://sso.arubainstanton.com"
API_URL = "https://nb.portal.arubainstanton.com/api"
API_VERSION = "7"


class ArubaInstantOnError(Exception):
    """Base Aruba Instant On error."""


class ArubaInstantOnAuthenticationError(ArubaInstantOnError):
    """Authentication failed."""


class ArubaInstantOnConnectionError(ArubaInstantOnError):
    """The cloud API could not be reached."""


def _base64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


class ArubaInstantOnClient:
    """Read-only client for the undocumented Instant On portal API."""

    def __init__(
        self,
        session: ClientSession,
        username: str,
        password: str,
        site_id: str,
    ) -> None:
        self._session = session
        self._username = username
        self._password = password
        self.site_id = site_id
        self._access_token: str | None = None
        self._token_expires_at = 0.0

    async def _authenticate(self) -> None:
        try:
            settings_response = await self._session.get(
                f"{PORTAL_URL}/settings.json"
            )
            settings_response.raise_for_status()
            settings = await settings_response.json()
            client_id = settings["ssoClientIdAuthZ"]

            login_response = await self._session.post(
                f"{SSO_URL}/aio/api/v1/mfa/validate/full",
                data={
                    "username": self._username,
                    "password": self._password,
                },
            )
            if login_response.status in (401, 403):
                raise ArubaInstantOnAuthenticationError(
                    "Invalid Instant On credentials"
                )
            login_response.raise_for_status()
            login_data = await login_response.json()
            session_token = login_data.get("access_token")
            if not session_token:
                raise ArubaInstantOnAuthenticationError(
                    "Instant On did not return a login token"
                )

            verifier = _base64url(secrets.token_bytes(32))
            challenge = _base64url(
                hashlib.sha256(verifier.encode()).digest()
            )
            state = _base64url(secrets.token_bytes(24))
            authorization_response = await self._session.get(
                f"{SSO_URL}/as/authorization.oauth2",
                params={
                    "client_id": client_id,
                    "redirect_uri": PORTAL_URL,
                    "response_type": "code",
                    "scope": "profile openid",
                    "state": state,
                    "code_challenge_method": "S256",
                    "code_challenge": challenge,
                    "sessionToken": session_token,
                },
                allow_redirects=False,
            )
            location = authorization_response.headers.get("Location", "")
            authorization_code = parse_qs(
                urlparse(location).query
            ).get("code", [None])[0]
            if not authorization_code:
                raise ArubaInstantOnAuthenticationError(
                    "Instant On authorization did not return a code"
                )

            token_response = await self._session.post(
                f"{SSO_URL}/as/token.oauth2",
                data={
                    "client_id": client_id,
                    "redirect_uri": PORTAL_URL,
                    "code": authorization_code,
                    "code_verifier": verifier,
                    "grant_type": "authorization_code",
                },
            )
            token_response.raise_for_status()
            token_data = await token_response.json()
            self._access_token = token_data["access_token"]
            expires_in = int(token_data.get("expires_in", 300))
            self._token_expires_at = time.monotonic() + max(
                30, expires_in - 60
            )
        except ArubaInstantOnAuthenticationError:
            raise
        except (ClientResponseError, KeyError, ValueError) as err:
            raise ArubaInstantOnConnectionError(str(err)) from err

    async def _ensure_authenticated(self) -> None:
        if (
            self._access_token is None
            or time.monotonic() >= self._token_expires_at
        ):
            await self._authenticate()

    async def _get(
        self, endpoint: str, *, optional: bool = False
    ) -> dict[str, Any] | None:
        await self._ensure_authenticated()
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "x-ion-api-version": API_VERSION,
            "Accept": "application/json",
        }
        try:
            response = await self._session.get(
                f"{API_URL}{endpoint}", headers=headers
            )
            if response.status == 401:
                self._access_token = None
                await self._ensure_authenticated()
                headers["Authorization"] = f"Bearer {self._access_token}"
                response = await self._session.get(
                    f"{API_URL}{endpoint}", headers=headers
                )
            if optional and response.status == 404:
                return None
            response.raise_for_status()
            return await response.json()
        except ClientResponseError as err:
            if err.status in (401, 403):
                raise ArubaInstantOnAuthenticationError(
                    "Instant On rejected the session"
                ) from err
            raise ArubaInstantOnConnectionError(str(err)) from err

    async def async_get_sites(self) -> list[dict[str, Any]]:
        payload = await self._get("/sites/")
        return list((payload or {}).get("elements", []))

    async def async_validate(self) -> dict[str, Any]:
        sites = await self.async_get_sites()
        site = next(
            (item for item in sites if item.get("id") == self.site_id),
            None,
        )
        if site is None:
            raise ArubaInstantOnAuthenticationError(
                "The account cannot access the selected site"
            )
        return site

    async def async_get_site_data(self) -> dict[str, Any]:
        prefix = f"/sites/{self.site_id}"
        site = await self.async_validate()
        landing = await self._get(f"{prefix}/landingPage", optional=True)
        inventory = await self._get(f"{prefix}/inventory")
        clients = await self._get(
            f"{prefix}/clientSummary", optional=True
        )
        client_elements = list((clients or {}).get("elements", []))
        wireless_clients = [
            client
            for client in client_elements
            if client.get("clientType") == "wireless"
        ]
        wired_clients = [
            client
            for client in client_elements
            if client.get("clientType") == "wired"
        ]
        if not wired_clients:
            wired = await self._get(
                f"{prefix}/wiredClientSummary", optional=True
            )
            wired_clients = (
                None
                if wired is None
                else list(wired.get("elements", []))
            )
        networks = await self._get(
            f"{prefix}/networksSummary", optional=True
        )
        alerts = await self._get(
            f"{prefix}/alertsSummary", optional=True
        )
        application_usage = await self._get(
            f"{prefix}/applicationCategoryUsage", optional=True
        )
        return {
            "site": site,
            "landing": landing or {},
            "inventory": list((inventory or {}).get("elements", [])),
            "wireless_clients": wireless_clients,
            "wired_clients": wired_clients,
            "networks": list((networks or {}).get("elements", [])),
            "alerts": alerts or {},
            "application_usage": list(
                (application_usage or {}).get("elements", [])
            ),
        }

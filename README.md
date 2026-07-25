# Aruba Instant On for Home Assistant

[![Validate](https://github.com/turbogizzmo/ArubaInstantOnPortalHA/actions/workflows/validate.yml/badge.svg)](https://github.com/turbogizzmo/ArubaInstantOnPortalHA/actions/workflows/validate.yml)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://www.hacs.xyz/docs/faq/custom_repositories/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A read-only Home Assistant custom integration for cloud-managed
[Aruba Instant On](https://www.arubainstanton.com/) sites.

> [!WARNING]
> This project uses the private API consumed by the Instant On web portal.
> HPE Aruba Networking does not document or support that API. Endpoints,
> authentication, and response fields may change without notice.

## Why this project exists

Home Assistant's built-in `aruba` integration and the newer local Aruba
Instant AP device tracker target controller-based Aruba Instant deployments.
They do not provide monitoring for cloud-managed Aruba Instant On sites.

This integration fills that gap while remaining intentionally read-only. It
does not change networks, block clients, reboot hardware, control PoE, or
modify site configuration.

## Features

- Home Assistant UI config flow with site-access validation
- OAuth 2.0 Authorization Code flow with PKCE
- Automatic token renewal
- Configurable polling from 60 to 3600 seconds; default 300 seconds
- Site, AP, switch, client, SSID, alert, and firmware status
- Aggregate wireless download/upload throughput
- 24-hour transfer totals reported by Instant On
- 2.4, 5, and 6 GHz client distribution
- Client SNR and poor-signal counts
- Aggregate PoE consumption
- Connectivity and uptime entities for every AP and switch
- Device hierarchy linking infrastructure to its Instant On site
- Redacted diagnostics
- Graceful feature detection for unavailable portal endpoints

## Installation

### Manual

1. Copy `custom_components/aruba_instant_on` to
   `/config/custom_components/aruba_instant_on`.
2. Restart Home Assistant.
3. Open **Settings → Devices & services → Add integration**.
4. Search for **Aruba Instant On**.

### HACS

1. Open **HACS → Integrations**.
2. Open the menu and select **Custom repositories**.
3. Add
   `https://github.com/turbogizzmo/ArubaInstantOnPortalHA`
   with category **Integration**.
4. Install **Aruba Instant On** and restart Home Assistant.
5. Open **Settings → Devices & services → Add integration** and search for
   **Aruba Instant On**.

## Account preparation

Create a dedicated Instant On portal account:

- Grant access only to sites Home Assistant should monitor.
- Use a unique, randomly generated password.
- Do not reuse an administrator's password.
- The portal flow currently used by this project does not support MFA.

Home Assistant stores the credentials in its protected configuration-entry
storage, as it does for other integrations.

## Configuration

The setup form requires:

| Field | Description |
| --- | --- |
| Email | Dedicated Instant On portal account |
| Password | Password for that account |
| Site ID | UUID from the Instant On portal |
| Polling interval | 60–3600 seconds; 300 recommended |

The site ID is the UUID shown in the Instant On portal URL while viewing the
site. It is not the site name, account ID, or device serial number.

## Entities

Site entities include infrastructure totals, online APs/switches, wired and
wireless clients, SSIDs, alert counts, traffic, 24-hour transfer totals, radio-band
distribution, SNR, poor-signal clients, PoE load, and firmware status.

Each infrastructure device creates:

- A connectivity binary sensor
- An uptime sensor
- A Home Assistant device with model, serial, and relationship to the site

Current portal responses can include both wired and wireless clients in
`clientSummary`. The integration classifies those records by `clientType` and
uses the older `wiredClientSummary` endpoint only as a compatibility fallback.
If neither response supplies wired clients, the wired-client sensor is
`unknown` while the rest of the integration continues updating.

## Dashboard

Reusable cards are provided in:

- `dashboard/network-cards.json`
- `dashboard/network-view.yaml`

The live design combines Aruba Instant On with pfSense and NextDNS, but the
Aruba card group can be used independently.

The examples intentionally use placeholder entity IDs such as
`sensor.example_site_wireless_clients`. Replace them with the entity IDs
created for your site. Device-specific navigation paths are intentionally not
included because Home Assistant registry IDs are installation-specific.

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for authentication,
site-ID, unavailable-entity, API-change, and diagnostics guidance.

## Privacy

The coordinator receives client-level records from the portal to calculate
aggregate statistics. This release does not create client entities or expose
client names, IP addresses, or MAC addresses on the dashboard. Diagnostics
redact credentials and common device identifiers.

## Development

```bash
python3 -m compileall -q custom_components/aruba_instant_on
python3 -m json.tool custom_components/aruba_instant_on/manifest.json
python3 -m json.tool custom_components/aruba_instant_on/strings.json
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for protocol and component
design details.

## Compatibility

The integration is developed against current Home Assistant releases and the
current Instant On portal API. Because the upstream API is private, compatibility
cannot be guaranteed after portal changes. Release notes document known API
behavior changes.

| Component | Last verified |
| --- | --- |
| Home Assistant | 2026.7.4 |
| Aruba Instant On portal | 2026-07-25 |
| Integration | 0.1.0 |

## Credits

The design was informed by:

- [Home Assistant's legacy Aruba integration](https://www.home-assistant.io/integrations/aruba/)
- [Jam3s97's local Aruba Instant AP Device Tracker](https://github.com/Jam3s97/Aruba_Device_Tracker)
- [Luke Whitelock's Instant On portal API research](https://mspp.io/documenting-aruba-instant-on-sites-aruba-instant-on-api/)

These projects target different Aruba management planes and no code was
copied from them.

## License

[MIT](LICENSE)

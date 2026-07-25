# Troubleshooting

## Integration is not found

Confirm that the directory is:

```text
/config/custom_components/aruba_instant_on/
```

The directory must contain `manifest.json` directly. Restart Home Assistant
after installing or upgrading the integration, then clear the browser cache if
the integration does not appear in the Add Integration dialog.

## Authentication fails

- Sign in to the Instant On web portal with the dedicated account.
- Confirm the account has access to the requested site.
- Confirm the account does not require MFA; the automated portal flow does not
  currently support MFA.
- Do not reuse an administrator password. Use a dedicated, least-privilege
  account with access only to monitored sites.

Portal authentication is private and unsupported. A portal change can break
authentication without a Home Assistant or network configuration change.

## Site validation fails

Use the site UUID shown in the portal URL while viewing the site. Do not enter
the friendly site name, account ID, or a device serial number.

## Some sensors are unknown

The portal does not return every optional endpoint for every site or account.
The integration treats optional HTTP 404 responses as unsupported features
rather than failing the entire config entry.

Current `clientSummary` responses may contain both wired and wireless clients.
The integration classifies records by `clientType` and only queries the legacy
`wiredClientSummary` endpoint when no wired records are present.

## Updates stop after a portal change

1. Reload the config entry from **Settings → Devices & services**.
2. Enable debug logging for the integration.
3. Reproduce one update failure.
4. Disable debug logging and download the resulting log.
5. Download integration diagnostics.

Review and redact all material before sharing it. Never publish credentials,
tokens, cookies, site UUIDs, serial numbers, MAC addresses, IP addresses, or
client records.

## Reporting a problem

Open an issue at
<https://github.com/turbogizzmo/ArubaInstantOnPortalHA/issues> with:

- Home Assistant version
- Integration version
- Whether authentication or a specific endpoint failed
- A minimal redacted log excerpt
- Redacted diagnostics when relevant

Use a private security advisory instead of a public issue for credential,
privacy, or security problems.

# Architecture

## Scope

This integration monitors cloud-managed Aruba Instant On sites. It is not a
replacement for integrations targeting local Aruba Instant controllers or
Aruba Central.

## Authentication

The portal currently uses an OAuth 2.0 Authorization Code flow with PKCE:

1. Read the current client ID from the portal's `settings.json`.
2. Validate the dedicated portal account.
3. Generate a random PKCE verifier, challenge, and state.
4. Request an authorization code.
5. Exchange the code for a short-lived bearer token.
6. Renew before expiry.

Tokens remain in memory and are never added to entity attributes or
diagnostics.

## Data flow

```text
Instant On portal
      |
      v
ArubaInstantOnClient
      |
      v
DataUpdateCoordinator (default: 5 minutes)
      |
      +--> Site sensors
      +--> AP/switch connectivity
      +--> AP/switch uptime
      +--> Redacted diagnostics
```

## Endpoints

Required:

- `/api/sites/`
- `/api/sites/{site_id}/inventory`

Optional:

- `landingPage`
- `clientSummary`
- `wiredClientSummary`
- `networksSummary`
- `alertsSummary`
- `applicationCategoryUsage`

Optional endpoints may return 404 without failing the integration.

## Entity stability

- The site UUID is the config-entry unique ID.
- Infrastructure entities use portal device ID, then serial number, then MAC
  address as fallbacks.
- Client entities are deliberately not created.

## Polling

The default interval is five minutes. The minimum is one minute to avoid
unnecessary portal load and account throttling.

## Failure behavior

- Authentication errors fail the coordinator update without leaking details.
- Transient HTTP errors preserve the last known Home Assistant state.
- Unsupported optional endpoints yield unavailable/empty features rather than
  failing the whole entry.

## Dashboard design

The included cards are grouped into:

1. Site and infrastructure overview.
2. Traffic and radio health.
3. Radio-band and 24-hour transfer distribution.
4. AP/switch drill-down tiles.
5. Cross-platform history alongside pfSense and NextDNS.

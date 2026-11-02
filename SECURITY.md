# Security policy

## Supported versions

Until the first stable release, only the latest commit is supported.

## Reporting a vulnerability

Do not open a public issue containing credentials, tokens, cookies, site IDs,
serial numbers, MAC addresses, IP addresses, or client records.

Use the repository's
[private security-advisory feature](https://github.com/turbogizzmo/ArubaInstantOnPortalHA/security/advisories/new).

## Credential model

The integration requires a portal username and password because Instant On
does not publish a supported API or service-account token flow for this use
case. Use a dedicated, least-privilege account with a unique password and
access only to required sites. Give it the lowest portal role that can read
those sites; the integration only reads data.

Home Assistant stores the password unencrypted in
`.storage/core.config_entries`, and that file is included in Home Assistant
backups. Protect backups with encryption and limit who can read the
configuration directory.

The integration:

- Does not log credentials or bearer tokens.
- Redacts credentials, site and device identifiers, and client records from
  diagnostics.
- Excludes device IP and MAC attributes from the recorder history.
- Stops polling and asks for reauthentication when the portal rejects the
  saved password, instead of retrying it.
- Does not expose configuration-changing actions.
- Renews short-lived tokens in memory.

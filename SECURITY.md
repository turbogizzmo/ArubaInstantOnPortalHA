# Security policy

## Supported versions

Until the first stable release, only the latest commit is supported.

## Reporting a vulnerability

Do not open a public issue containing credentials, tokens, cookies, site IDs,
serial numbers, MAC addresses, IP addresses, or client records.

After publication, use the repository's private security-advisory feature.
Before publication, report findings privately to the repository owner.

## Credential model

The integration requires a portal username and password because Instant On
does not publish a supported API or service-account token flow for this use
case. Use a dedicated, least-privilege account with a unique password and
access only to required sites.

The integration:

- Does not log credentials or bearer tokens.
- Redacts credentials and device identifiers from diagnostics.
- Does not expose configuration-changing actions.
- Renews short-lived tokens in memory.

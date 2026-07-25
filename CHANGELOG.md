# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project intends to use semantic versioning.

## [Unreleased]

## [0.1.0] - 2026-07-25

### Fixed

- Correctly classify the current `/clientSummary` response, which contains
  both wired and wireless clients.
- Use `/wiredClientSummary` only as a compatibility fallback when the combined
  response contains no wired clients.

### Added

- Read-only Aruba Instant On portal client with OAuth PKCE authentication.
- Home Assistant config and options flows.
- Site health, inventory, alert, traffic, radio, PoE, and firmware sensors.
- AP and switch connectivity and uptime entities.
- Redacted diagnostics.
- Reusable combined-network dashboard cards.

### Known limitations

- The upstream portal API is undocumented and unsupported.
- MFA is not supported by the automated portal authentication flow.
- Wired-client data may be unavailable on older API variants where neither
  the combined nor legacy client-summary response includes wired clients.

[Unreleased]: https://github.com/turbogizzmo/ArubaInstantOnPortalHA/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/turbogizzmo/ArubaInstantOnPortalHA/releases/tag/v0.1.0

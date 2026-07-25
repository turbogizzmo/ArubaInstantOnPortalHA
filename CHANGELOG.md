# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project intends to use semantic versioning.

## [Unreleased]

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
- Wired-client summary is unavailable on sites where the legacy endpoint
  returns HTTP 404.

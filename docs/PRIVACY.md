# Privacy and Example Data

This repository is a reusable Home Assistant custom integration. Its source,
documentation, dashboard examples, issues, and Git history must not identify a
real home, person, network, or Aruba Instant On account.

## Use neutral examples

Use fictional, reusable labels:

- `Example Site`
- `Access Point 1`
- `Switch 1`
- `example_site`, `ap_1`, and `switch_1` in entity IDs

Do not use real site, room, household, account, client-device, or network
names. Avoid examples that can be traced back to a deployment even when the
value is not conventionally considered a secret.

## Never commit

- Portal credentials, tokens, cookies, API keys, or secrets
- Names or email addresses
- Site UUIDs or Home Assistant registry IDs
- Device serial numbers or MAC addresses
- Public or private IP addresses
- SSIDs, hostnames, VLAN names, or client inventories
- Unredacted diagnostics, logs, screenshots, or API responses

Home Assistant entity IDs copied from a live installation can contain serial
numbers or site names. Rewrite the complete ID before using it as an example.
Dashboard navigation paths can contain persistent registry IDs; examples
should link to generic dashboard views instead.

## Before committing

Run:

```bash
python3 .github/scripts/check_privacy.py
```

The check catches several common identifier formats but cannot recognize every
personal name or account-specific label. Review all example data manually as
well.

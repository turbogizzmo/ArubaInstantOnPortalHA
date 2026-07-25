# Contributing

Contributions are welcome, particularly redacted API compatibility reports,
tests, translations, and documentation improvements.

## Ground rules

- Never commit portal credentials, access tokens, cookies, site UUIDs, serial
  numbers, MAC addresses, public IP addresses, or client-identifying data.
- Keep all operations read-only unless a future proposal receives explicit
  security review and opt-in design.
- Treat every API field as optional.
- Preserve operation when optional endpoints return 404.
- Avoid creating entities for every client by default.

## Local checks

```bash
python3 -m compileall -q custom_components/aruba_instant_on
python3 -m json.tool custom_components/aruba_instant_on/manifest.json
python3 -m json.tool custom_components/aruba_instant_on/strings.json
python3 -m json.tool custom_components/aruba_instant_on/translations/en.json
```

Before submitting a pull request, also run Hassfest, HACS validation, and the
test suite once those workflows are enabled for the published repository.

## Pull requests

Describe:

1. The Instant On device/site behavior being addressed.
2. Whether the endpoint is required or optional.
3. How credentials and client data remain protected.
4. How failure and API-change behavior were tested.

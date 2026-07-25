# Dashboard design

The reference dashboard uses Home Assistant's responsive **Sections** view
instead of Masonry. Masonry places each new card beneath the shortest column,
which causes pfSense, Aruba, and NextDNS groups to interleave as card heights
change.

The Sections layout keeps three operational columns aligned:

| Section | Contents |
| --- | --- |
| Network Core | Overall status, pfSense health, gateways, interfaces |
| Aruba Instant On | Site health, throughput, radios, clients, APs, switches |
| Security & Performance | NextDNS, latency, firewall, WAN history, updates |

On narrower screens Home Assistant collapses these sections responsively.

## Files

- `network-cards.json` contains complete, importable Aruba card objects.
- `network-view.yaml` documents the combined-view structure.

## Drill-down behavior

- Site-summary tiles open standard Home Assistant entity details.
- Add installation-specific navigation paths after importing if direct device
  drill-down is desired.
- Traffic and history cards retain Home Assistant's standard More Info and
  History navigation.

## Portability

The sample uses sanitized placeholders such as `example_site`, `ap_1`, and
`switch_1`. Replace them with the entity IDs created by your installation.

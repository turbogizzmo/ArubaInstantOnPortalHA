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

- Site-summary tiles navigate to the Home Assistant site device.
- AP and switch tiles navigate directly to their corresponding device pages.
- Traffic and history cards retain Home Assistant's standard More Info and
  History navigation.

## Portability

The sample entity IDs contain the live display names assigned during initial
development. Home Assistant may generate different entity IDs when a site or
device has a different name. Update the IDs after installing the integration.

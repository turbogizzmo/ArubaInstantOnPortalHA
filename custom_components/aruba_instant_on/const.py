"""Constants for the Aruba Instant On integration."""

from datetime import timedelta

DOMAIN = "aruba_instant_on"

CONF_SITE_ID = "site_id"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 300
MIN_SCAN_INTERVAL = 60
MAX_SCAN_INTERVAL = 3600

DEFAULT_UPDATE_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

PLATFORMS = ["binary_sensor", "sensor"]


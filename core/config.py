"""Central configuration: monitored zones, thresholds, API settings.

Edit this file to add districts or change alert thresholds. No other file
needs to change.
"""
from dataclasses import dataclass

# ---- Alert thresholds (millimetres of rain in any rolling 24-hour window) ----
HIGH_RISK_MM_24H: float = 50.0   # triggers "HIGH RISK ALERT"
WATCH_MM_24H: float = 30.0       # early-warning tier

# ---- Open-Meteo settings (free, no API key needed) ----
API_URL: str = "https://api.open-meteo.com/v1/forecast"
TIMEZONE: str = "Asia/Karachi"
FORECAST_DAYS: int = 7
REQUEST_TIMEOUT_S: int = 10
MAX_RETRIES: int = 3
CACHE_TTL_S: int = 900  # 15 min: keeps us far below Open-Meteo free limits


@dataclass(frozen=True)
class Zone:
    """A monitored flood-prone location."""
    name: str
    province: str
    lat: float
    lon: float
    note: str


ZONES: dict[str, Zone] = {
    z.name: z
    for z in [
        Zone("Nowshera", "Khyber Pakhtunkhwa", 34.0153, 71.9747, "Kabul River; severe 2010 and 2022 floods"),
        Zone("Charsadda", "Khyber Pakhtunkhwa", 34.1453, 71.7308, "Kabul/Swat river confluence"),
        Zone("Swat (Mingora)", "Khyber Pakhtunkhwa", 34.7717, 72.3600, "Swat River; flash-flood prone"),
        Zone("Sukkur", "Sindh", 27.7052, 68.8574, "Indus River barrage"),
        Zone("Jacobabad", "Sindh", 28.2769, 68.4514, "Low-lying; poor drainage"),
        Zone("Dera Ismail Khan", "Khyber Pakhtunkhwa", 31.8626, 70.9019, "Indus floodplain; hill torrents"),
        Zone("Muzaffargarh", "Punjab", 30.0703, 71.1933, "Between Indus and Chenab"),
        Zone("Rajanpur", "Punjab", 29.1044, 70.3302, "Koh-e-Suleiman hill torrents"),
    ]
}

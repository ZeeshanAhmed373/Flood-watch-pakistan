"""Open-Meteo client. Pure Python (no Streamlit), so it is easy to test and reuse."""
from __future__ import annotations

import time
from dataclasses import dataclass

import pandas as pd
import requests

from core.config import API_URL, FORECAST_DAYS, MAX_RETRIES, REQUEST_TIMEOUT_S, TIMEZONE


class WeatherAPIError(RuntimeError):
    """Raised when Open-Meteo cannot be reached or returns bad data."""


@dataclass
class WeatherData:
    current: dict          # latest observation (temp, humidity, wind, rain...)
    hourly: pd.DataFrame   # time, precipitation, probability, temperature (past 24h + 7 days)
    daily: pd.DataFrame    # date, rain_sum, prob_max, tmax, tmin (7 days)


def fetch_weather(lat: float, lon: float) -> WeatherData:
    """Fetch current conditions plus hourly/daily forecast for one point.

    past_days=1 gives us the last 24h of observed/model rainfall so the
    'rain in last 24h' figure is real, not just forecast.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": TIMEZONE,
        "forecast_days": FORECAST_DAYS,
        "past_days": 1,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "hourly": "precipitation,precipitation_probability,temperature_2m",
        "daily": "precipitation_sum,precipitation_probability_max,temperature_2m_max,temperature_2m_min",
    }

    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT_S)
            r.raise_for_status()
            return _parse(r.json())
        except (requests.RequestException, KeyError, ValueError) as err:
            last_err = err
            time.sleep(1.5 * (attempt + 1))  # simple backoff
    raise WeatherAPIError(f"Open-Meteo unavailable after {MAX_RETRIES} tries: {last_err}")


def _parse(payload: dict) -> WeatherData:
    """Turn the raw JSON into small, typed DataFrames."""
    h = payload["hourly"]
    hourly = pd.DataFrame(
        {
            "time": pd.to_datetime(h["time"]),
            "precip_mm": h["precipitation"],
            "precip_prob": h["precipitation_probability"],
            "temp_c": h["temperature_2m"],
        }
    )
    hourly["precip_mm"] = hourly["precip_mm"].fillna(0.0).astype("float32")

    d = payload["daily"]
    daily = pd.DataFrame(
        {
            "date": pd.to_datetime(d["time"]),
            "rain_sum_mm": d["precipitation_sum"],
            "prob_max": d["precipitation_probability_max"],
            "tmax_c": d["temperature_2m_max"],
            "tmin_c": d["temperature_2m_min"],
        }
    )
    daily = daily[daily["date"] >= pd.Timestamp(payload["current"]["time"]).normalize()]
    return WeatherData(current=payload["current"], hourly=hourly, daily=daily.reset_index(drop=True))

"""Flood-risk alert logic. Pure Python: no UI, no network."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from core.config import HIGH_RISK_MM_24H, WATCH_MM_24H

HIGH, WATCH, NORMAL = "HIGH", "WATCH", "NORMAL"


@dataclass
class RiskAssessment:
    level: str                 # HIGH / WATCH / NORMAL
    past_24h_mm: float         # rain that already fell in the last 24h
    next_24h_mm: float         # forecast rain in the next 24h
    peak_24h_mm: float         # worst rolling 24h total in the forecast window
    peak_window_end: pd.Timestamp | None  # when that worst window ends
    message: str


def assess_risk(hourly: pd.DataFrame, now: pd.Timestamp) -> RiskAssessment:
    """Evaluate rolling 24h rainfall against thresholds.

    Rule: ANY 24-hour window (past or forecast, within the 7-day horizon)
    with total rain > HIGH_RISK_MM_24H triggers a HIGH RISK ALERT.
    """
    df = hourly.sort_values("time").reset_index(drop=True)
    df["rain_24h"] = df["precip_mm"].rolling(24, min_periods=24).sum()

    past = df[(df["time"] <= now) & (df["time"] > now - pd.Timedelta(hours=24))]
    nxt = df[(df["time"] > now) & (df["time"] <= now + pd.Timedelta(hours=24))]
    future_windows = df[(df["time"] >= now) & df["rain_24h"].notna()]

    past_mm = float(past["precip_mm"].sum())
    next_mm = float(nxt["precip_mm"].sum())

    if future_windows.empty:
        peak_mm, peak_end = max(past_mm, next_mm), None
    else:
        idx = future_windows["rain_24h"].idxmax()
        peak_mm, peak_end = float(df.loc[idx, "rain_24h"]), df.loc[idx, "time"]

    worst = max(past_mm, peak_mm)
    if worst > HIGH_RISK_MM_24H:
        level = HIGH
        when = f" around {peak_end:%a %d %b, %H:%M}" if peak_end is not None and peak_mm >= past_mm else ""
        msg = (f"HIGH RISK ALERT: up to {worst:.0f} mm of rain in 24 hours{when} "
               f"(threshold {HIGH_RISK_MM_24H:.0f} mm). Flash-flood and river-flood danger.")
    elif worst > WATCH_MM_24H:
        level = WATCH
        msg = f"Flood watch: up to {worst:.0f} mm in 24 hours. Monitor rivers and drains."
    else:
        level = NORMAL
        msg = f"No significant flood risk. Peak 24h rainfall: {worst:.0f} mm."

    return RiskAssessment(level, past_mm, next_mm, peak_mm, peak_end, msg)

"""Streamlit weather + alert component. Call render_weather_dashboard() from any page."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core.config import CACHE_TTL_S, HIGH_RISK_MM_24H, WATCH_MM_24H, ZONES
from core.risk import HIGH, WATCH, RiskAssessment, assess_risk
from services.weather import WeatherAPIError, WeatherData, fetch_weather


@st.cache_data(ttl=CACHE_TTL_S, show_spinner=False)
def get_weather(lat: float, lon: float) -> WeatherData:
    """Cached wrapper: repeat views within 15 min cost zero API calls and zero RAM growth."""
    return fetch_weather(lat, lon)


# ----------------------------- charts -----------------------------
def _hourly_chart(w: WeatherData, now: pd.Timestamp) -> go.Figure:
    df = w.hourly.copy()
    df["rain_24h"] = df["precip_mm"].rolling(24, min_periods=24).sum()
    fig = go.Figure()
    fig.add_bar(x=df["time"], y=df["precip_mm"], name="Hourly rain (mm)", marker_color="#4C9BE8")
    fig.add_scatter(x=df["time"], y=df["rain_24h"], name="Rolling 24h total (mm)",
                    line=dict(color="#E8743B", width=2), yaxis="y2")
    fig.add_hline(y=HIGH_RISK_MM_24H, line_dash="dash", line_color="red", yref="y2",
                  annotation_text=f"High risk {HIGH_RISK_MM_24H:.0f} mm", annotation_position="top left")
    fig.add_hline(y=WATCH_MM_24H, line_dash="dot", line_color="orange", yref="y2",
                  annotation_text=f"Watch {WATCH_MM_24H:.0f} mm", annotation_position="bottom left")
    fig.add_vline(x=now, line_color="gray", line_dash="dot")
    fig.update_layout(
        height=380, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.12),
        yaxis=dict(title="mm / hour"), yaxis2=dict(title="mm / 24h", overlaying="y", side="right"),
        hovermode="x unified",
    )
    return fig


def _daily_chart(w: WeatherData) -> go.Figure:
    d = w.daily
    colors = ["#D62728" if v > HIGH_RISK_MM_24H else "#F2A93B" if v > WATCH_MM_24H else "#4C9BE8"
              for v in d["rain_sum_mm"].fillna(0)]
    fig = go.Figure()
    fig.add_bar(x=d["date"], y=d["rain_sum_mm"], marker_color=colors, name="Daily rain (mm)")
    fig.add_scatter(x=d["date"], y=d["prob_max"], name="Max rain probability (%)",
                    mode="lines+markers", line=dict(color="#555"), yaxis="y2")
    fig.add_hline(y=HIGH_RISK_MM_24H, line_dash="dash", line_color="red")
    fig.update_layout(
        height=320, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.15),
        yaxis=dict(title="mm / day"), yaxis2=dict(title="%", overlaying="y", side="right", range=[0, 100]),
    )
    return fig


def _temp_chart(w: WeatherData) -> go.Figure:
    d = w.daily
    fig = go.Figure()
    fig.add_scatter(x=d["date"], y=d["tmax_c"], name="Max °C", line=dict(color="#D62728"))
    fig.add_scatter(x=d["date"], y=d["tmin_c"], name="Min °C", line=dict(color="#1F77B4"))
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.15))
    return fig


# ----------------------------- alert banner -----------------------------
def _show_alert(risk: RiskAssessment) -> None:
    if risk.level == HIGH:
        st.error(f"🚨 {risk.message}")
    elif risk.level == WATCH:
        st.warning(f"⚠️ {risk.message}")
    else:
        st.success(f"✅ {risk.message}")


# ----------------------------- all-zone scan -----------------------------
def _scan_all_zones() -> pd.DataFrame:
    rows = []
    for z in ZONES.values():
        try:
            w = get_weather(z.lat, z.lon)
            now = pd.Timestamp(w.current["time"])
            r = assess_risk(w.hourly, now)
            rows.append({"Zone": z.name, "Province": z.province, "Status": r.level,
                         "Past 24h (mm)": round(r.past_24h_mm, 1),
                         "Next 24h (mm)": round(r.next_24h_mm, 1),
                         "Peak 24h (mm)": round(r.peak_24h_mm, 1)})
        except WeatherAPIError:
            rows.append({"Zone": z.name, "Province": z.province, "Status": "NO DATA"})
    order = {"HIGH": 0, "WATCH": 1, "NORMAL": 2, "NO DATA": 3}
    df = pd.DataFrame(rows)
    return df.sort_values("Status", key=lambda s: s.map(order)).reset_index(drop=True)


# ----------------------------- public entry point -----------------------------
def render_weather_dashboard() -> None:
    """Draw the full weather + alert UI."""
    zone = ZONES[st.sidebar.selectbox("Monitored zone", list(ZONES))]
    if st.sidebar.button("🔄 Refresh data"):
        get_weather.clear()

    st.subheader(f"{zone.name}, {zone.province}")
    st.caption(f"{zone.note} · {zone.lat:.3f}, {zone.lon:.3f}")

    try:
        with st.spinner("Fetching Open-Meteo data..."):
            w = get_weather(zone.lat, zone.lon)
    except WeatherAPIError as err:
        st.error(f"Could not load weather data. Please try again shortly.\n\n{err}")
        return

    now = pd.Timestamp(w.current["time"])
    risk = assess_risk(w.hourly, now)
    _show_alert(risk)

    c = w.current
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Temperature", f"{c['temperature_2m']:.1f} °C")
    m2.metric("Humidity", f"{c['relative_humidity_2m']:.0f} %")
    m3.metric("Wind", f"{c['wind_speed_10m']:.0f} km/h")
    m4.metric("Rain, last 24h", f"{risk.past_24h_mm:.1f} mm")
    m5.metric("Rain, next 24h", f"{risk.next_24h_mm:.1f} mm")

    tab1, tab2, tab3 = st.tabs(["Hourly rain + 24h total", "7-day forecast", "Temperature"])
    with tab1:
        st.plotly_chart(_hourly_chart(w, now), width="stretch")
    with tab2:
        st.plotly_chart(_daily_chart(w), width="stretch")
    with tab3:
        st.plotly_chart(_temp_chart(w), width="stretch")

    with st.expander("🗺️ Scan all monitored zones"):
        if st.button("Run scan"):
            st.dataframe(_scan_all_zones(), width="stretch", hide_index=True)

    st.caption(f"Data: Open-Meteo · cached {CACHE_TTL_S // 60} min · last observation {now:%d %b %Y, %H:%M} PKT")

"""Streamlit satellite-map component for the Indus basin."""
from __future__ import annotations

from datetime import date, timedelta

import folium
import streamlit as st
from folium import plugins
from streamlit_folium import st_folium

from core.districts import ALL_BASIN, BARRAGES, BASIN_BOUNDS, DISTRICTS, INDUS_PATH
from services.map_layers import BASEMAP_NAMES, EOX_S2, GIBS_NAMES, add_basemaps

FOCUS_ZOOM = 9
FOCUS_RADIUS_M = 25_000  # ring drawn around the selected district


def build_map(selected: str, basemap: str, gibs_day: date,
              show_districts: bool = True, show_river: bool = True) -> folium.Map:
    """Build the folium map. Pure function: easy to test, no Streamlit calls."""
    if selected == ALL_BASIN:
        m = folium.Map(location=(30.5, 70.5), zoom_start=5, tiles=None, control_scale=True)
        m.fit_bounds(BASIN_BOUNDS)
    else:
        d = DISTRICTS[selected]
        m = folium.Map(location=(d.lat, d.lon), zoom_start=FOCUS_ZOOM, tiles=None, control_scale=True)

    add_basemaps(m, basemap, gibs_day)

    if show_river:
        river = folium.FeatureGroup(name="Indus River (approx.)", show=True)
        folium.PolyLine(INDUS_PATH, color="#00B4FF", weight=3, opacity=0.9,
                        tooltip="Indus River (approximate path)").add_to(river)
        for name, (lat, lon) in BARRAGES.items():
            folium.Marker((lat, lon), tooltip=name,
                          icon=folium.Icon(color="blue", icon="tint", prefix="fa")).add_to(river)
        river.add_to(m)

    if show_districts:
        dist = folium.FeatureGroup(name="Districts", show=True)
        for d in DISTRICTS.values():
            folium.CircleMarker(
                (d.lat, d.lon), radius=5, color="#FFFFFF", weight=1, fill=True,
                fill_color="#FF8C00", fill_opacity=0.9,
                tooltip=f"{d.name} ({d.province})",
                popup=folium.Popup(f"<b>{d.name}</b><br>{d.province}<br>{d.river}", max_width=220),
            ).add_to(dist)
        dist.add_to(m)

    if selected != ALL_BASIN:
        d = DISTRICTS[selected]
        folium.Circle((d.lat, d.lon), radius=FOCUS_RADIUS_M, color="#FF3B30", weight=2,
                      fill=True, fill_opacity=0.08).add_to(m)
        folium.Marker((d.lat, d.lon), tooltip=d.name,
                      icon=folium.Icon(color="red", icon="map-marker", prefix="fa")).add_to(m)

    plugins.Fullscreen().add_to(m)
    plugins.MousePosition(num_digits=3).add_to(m)
    folium.LayerControl(collapsed=True).add_to(m)
    return m


def render_map_dashboard() -> None:
    """Sidebar controls + map."""
    st.sidebar.header("Map controls")
    names = [ALL_BASIN] + sorted(DISTRICTS, key=lambda n: (DISTRICTS[n].province, n))
    selected = st.sidebar.selectbox(
        "District", names,
        format_func=lambda n: n if n == ALL_BASIN else f"{n} ({DISTRICTS[n].province})",
    )
    basemap = st.sidebar.selectbox("Base imagery", BASEMAP_NAMES, index=BASEMAP_NAMES.index(EOX_S2))

    gibs_day = date.today() - timedelta(days=1)
    if basemap in GIBS_NAMES:
        gibs_day = st.sidebar.date_input(
            "Imagery date", value=gibs_day, min_value=date(2015, 1, 1), max_value=date.today(),
            help="NASA publishes a new daily mosaic every day. Blank tiles = no data yet; try an earlier date.",
        )
    show_districts = st.sidebar.checkbox("Show districts", value=True)
    show_river = st.sidebar.checkbox("Show Indus River and barrages", value=True)

    st.subheader("Indus Basin satellite map" if selected == ALL_BASIN else f"{selected}, {DISTRICTS[selected].province}")
    if selected != ALL_BASIN:
        d = DISTRICTS[selected]
        c1, c2, c3 = st.columns(3)
        c1.metric("Province", d.province)
        c2.metric("Hazard context", d.river)
        c3.metric("Coordinates", f"{d.lat:.3f}, {d.lon:.3f}")

    m = build_map(selected, basemap, gibs_day, show_districts, show_river)
    # returned_objects=[] stops map pan/zoom from triggering Streamlit reruns (saves CPU and RAM).
    # The key forces a clean re-centre whenever the user changes a control.
    st_folium(m, height=620, use_container_width=True, returned_objects=[],
              key=f"map|{selected}|{basemap}|{gibs_day}|{show_districts}|{show_river}")

    st.caption("Layer switcher (top-right of map) lets you flip imagery without reloading. "
               "NASA daily imagery is ~375 m-1 km resolution (great for flood extent); "
               "Sentinel-2 mosaic is 10 m but a static 2021 composite. "
               "River line is schematic, not survey-grade.")

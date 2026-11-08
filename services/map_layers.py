"""Free, key-less satellite and base tile layers. Pure folium, no Streamlit.

Tiles are streamed straight from the providers to the user's browser, so they
cost our Streamlit app zero RAM and zero bandwidth.
"""
from __future__ import annotations

from datetime import date

import folium

EOX_S2 = "Sentinel-2 cloudless 2021 (EOX)"
ESRI = "Esri World Imagery (high-res)"
VIIRS = "NASA VIIRS true colour (daily)"
MODIS = "NASA MODIS Terra true colour (daily)"
TOPO = "OpenTopoMap (terrain)"
OSM = "OpenStreetMap"

BASEMAP_NAMES = [EOX_S2, ESRI, VIIRS, MODIS, TOPO, OSM]
GIBS_NAMES = {VIIRS, MODIS}  # layers that need a date

# name -> (url, attribution, max_native_zoom, max_zoom)
_STATIC = {
    EOX_S2: (
        "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2021_3857/default/g/{z}/{y}/{x}.jpg",
        "Sentinel-2 cloudless by EOX IT Services GmbH (contains modified Copernicus Sentinel data 2021)",
        13, 15,
    ),
    ESRI: (
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "Tiles © Esri: Maxar, Earthstar Geographics, and the GIS User Community",
        17, 18,
    ),
    TOPO: (
        "https://tile.opentopomap.org/{z}/{x}/{y}.png",
        "Map data © OpenStreetMap contributors, SRTM | Style © OpenTopoMap (CC-BY-SA)",
        17, 17,
    ),
    OSM: (
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "© OpenStreetMap contributors",
        19, 19,
    ),
}

# name -> NASA GIBS layer id (Web Mercator, daily, free, no key)
_GIBS_IDS = {
    VIIRS: "VIIRS_SNPP_CorrectedReflectance_TrueColor",
    MODIS: "MODIS_Terra_CorrectedReflectance_TrueColor",
}
_GIBS_URL = (
    "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/{layer}/default/{day}/"
    "GoogleMapsCompatible_Level9/{{z}}/{{y}}/{{x}}.jpg"
)


def add_basemaps(m: folium.Map, selected: str, gibs_day: date) -> None:
    """Add every base layer; only `selected` is visible, rest are in the layer switcher."""
    for name in BASEMAP_NAMES:
        if name in _STATIC:
            url, attr, native, maxz = _STATIC[name]
        else:
            url = _GIBS_URL.format(layer=_GIBS_IDS[name], day=gibs_day.isoformat())
            attr = "Imagery: NASA EOSDIS GIBS / Worldview"
            native, maxz = 9, 12
        folium.TileLayer(
            tiles=url, attr=attr, name=name, overlay=False, control=True,
            show=(name == selected), max_native_zoom=native, max_zoom=maxz,
        ).add_to(m)

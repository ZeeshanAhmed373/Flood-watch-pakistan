"""Streamlit tab: AI Damage Assessment (flood extent from drone / satellite images)."""
from __future__ import annotations

from io import BytesIO

import streamlit as st
from PIL import Image

from ml.demo_image import demo_png_bytes
from ml.flood_segmentation import (CLEAR_HSV, MODE_BOTH, MODE_CLEAR, MODE_MUDDY, MODE_RADAR,
                                   MODES, MUDDY_HSV, Assessment, ImageError, analyse, load_image)


@st.cache_data(show_spinner=False, max_entries=3, ttl=900)
def _run(data: bytes, mode: str, hsv_params, dark_thresh, min_blob_pct: float, m_per_px: float):
    """Cached pipeline. max_entries=3 keeps memory bounded on the 1 GB free tier."""
    rgb, scale = load_image(data)
    return rgb, analyse(rgb, scale, mode, hsv_params, dark_thresh, min_blob_pct, m_per_px)


def _sidebar_settings():
    """Collect analysis settings from the sidebar."""
    st.sidebar.header("Analysis settings")
    mode = st.sidebar.selectbox(
        "Detection mode", MODES,
        help="Pick the mode that matches your image. Pakistan floodwater is often muddy brown, "
             "so the default detects both clear and muddy water.",
    )
    hsv_params, dark = None, None

    if mode in (MODE_CLEAR, MODE_MUDDY):
        base = CLEAR_HSV if mode == MODE_CLEAR else MUDDY_HSV
        with st.sidebar.expander("Fine-tune colour thresholds"):
            h = st.slider("Hue", 0, 179, (base[0], base[1]), key=f"h-{mode}")
            s = st.slider("Saturation", 0, 255, (base[2], base[3]), key=f"s-{mode}")
            v = st.slider("Brightness", 0, 255, (base[4], base[5]), key=f"v-{mode}")
        hsv_params = (h[0], h[1], s[0], s[1], v[0], v[1])
    elif mode == MODE_RADAR:
        if not st.sidebar.checkbox("Auto threshold (Otsu)", value=True):
            dark = float(st.sidebar.slider("Darkness threshold", 0, 255, 60))
    else:
        st.sidebar.caption("Select a single mode to fine-tune colour thresholds.")

    min_blob = st.sidebar.slider("Ignore blobs smaller than (% of image)", 0.0, 2.0, 0.05, 0.05)
    m_per_px = st.sidebar.number_input(
        "Ground resolution (metres per pixel, optional)", min_value=0.0, max_value=1000.0, value=0.0, step=0.5,
        help="Enter it to get flooded area in km². Use the ORIGINAL image's resolution "
             "(drone photos: ~0.05-0.3 m, Sentinel-2: 10 m).",
    )
    return mode, hsv_params, dark, float(min_blob), float(m_per_px)


def _png_bytes(arr) -> bytes:
    buf = BytesIO()
    Image.fromarray(arr).save(buf, format="PNG")
    return buf.getvalue()


def _banner(a: Assessment) -> None:
    text = f"Flood severity: {a.label.upper()}, {a.flood_pct:.1f}% of the imaged area appears inundated."
    {"success": st.success, "info": st.info, "warning": st.warning, "error": st.error}[a.level](text)


def render_damage_assessment() -> None:
    """Draw the whole tab."""
    mode, hsv_params, dark, min_blob, m_per_px = _sidebar_settings()

    st.subheader("AI Damage Assessment")
    st.caption("Upload post-flood drone or satellite imagery. The tool highlights likely floodwater "
               "and scores how much of the image is inundated.")

    up = st.file_uploader("Upload image (JPG or PNG, max 10 MB)", type=["jpg", "jpeg", "png"])
    use_demo = st.checkbox("No image handy? Use the built-in demo scene", value=False)

    data = up.getvalue() if up is not None else (demo_png_bytes() if use_demo else None)
    if data is None:
        st.info("Upload an image to begin.")
        return

    try:
        with st.spinner("Analysing image..."):
            rgb, a = _run(data, mode, hsv_params, dark, min_blob, m_per_px)
    except ImageError as err:
        st.error(str(err))
        return

    _banner(a)
    c1, c2, c3 = st.columns(3)
    c1.metric("Flooding / inundation", f"{a.flood_pct:.1f} %")
    c2.metric("Severity", a.label)
    c3.metric("Flooded area", f"{a.flooded_km2:.2f} km²" if a.flooded_km2 is not None else "Enter m/pixel")

    left, right = st.columns(2)
    left.image(rgb, caption="Original", width="stretch")
    right.image(a.overlay, caption="AI processed: red = detected floodwater", width="stretch")

    d1, d2 = st.columns(2)
    d1.download_button("⬇️ Download processed map (PNG)", _png_bytes(a.overlay),
                       file_name="flood_assessment.png", mime="image/png")
    if a.dark_thresh is not None:
        d2.caption(f"Darkness threshold used: {a.dark_thresh:.0f}")

    with st.expander("Show binary water mask"):
        st.image(a.mask, caption="White = water", width="stretch")

    st.caption("Severity bands (share of image flooded): under 5% minimal, 5-20% moderate, 20-40% severe, "
               "over 40% critical. This is a colour-based estimate: bare soil, shadows, and dark roofs can be "
               "misclassified. Always verify against ground reports and official PDMA/NDMA assessments "
               "before making rescue or evacuation decisions.")

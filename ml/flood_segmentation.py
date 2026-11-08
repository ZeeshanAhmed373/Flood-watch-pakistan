"""Lightweight flood / inundation detection with OpenCV + NumPy.

No GPU, no model download, no network. Peak RAM is a few tens of MB because
every image is downscaled to MAX_SIDE pixels before processing.

IMPORTANT: this is colour/brightness thresholding, not a trained model. It is a
fast first-look estimate. Muddy floodwater and bare soil can look alike, so
results must be sanity-checked by a person before anyone acts on them.
"""
from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import cv2
import numpy as np
from PIL import Image

MAX_SIDE = 1024            # longest side after downscaling (keeps RAM tiny)
MAX_UPLOAD_MB = 10
MAX_PIXELS = 40_000_000    # refuse absurdly large images before decoding fully

MODE_BOTH = "Optical: clear + muddy water"
MODE_CLEAR = "Optical: clear / blue water"
MODE_MUDDY = "Optical: muddy (brown) floodwater"
MODE_RADAR = "Radar / grayscale: dark = water"
MODES = [MODE_BOTH, MODE_CLEAR, MODE_MUDDY, MODE_RADAR]

# HSV ranges in OpenCV scale (H 0-179, S 0-255, V 0-255):
# (h_lo, h_hi, s_lo, s_hi, v_lo, v_hi)
CLEAR_HSV = (85, 130, 40, 255, 40, 255)
MUDDY_HSV = (8, 28, 40, 150, 70, 200)

OVERLAY_RGB = (255, 30, 30)      # detected water is tinted red for contrast
CONTOUR_RGB = (255, 235, 0)


class ImageError(ValueError):
    """Raised for unreadable or oversized images (message is safe to show users)."""


@dataclass
class Assessment:
    overlay: np.ndarray        # RGB image with detected water highlighted
    mask: np.ndarray           # uint8 0/255
    flood_pct: float           # % of valid pixels classified as water
    flooded_px: int
    valid_px: int
    label: str                 # Minimal / Moderate / Severe / Critical
    level: str                 # UI level: success / info / warning / error
    flooded_km2: float | None  # only if ground resolution was given
    dark_thresh: float | None  # radar mode: threshold actually used


# ----------------------------------------------------------------- loading
def load_image(data: bytes) -> tuple[np.ndarray, float]:
    """Decode bytes -> RGB uint8 array, downscaled. Returns (rgb, scale_factor).

    scale_factor = original_width / new_width, used to keep area estimates correct.
    """
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise ImageError(f"Image is larger than {MAX_UPLOAD_MB} MB. Please upload a smaller file.")
    try:
        img = Image.open(BytesIO(data))
        orig_w, orig_h = img.size
        if orig_w * orig_h > MAX_PIXELS:
            raise ImageError("Image has too many pixels (over 40 MP). Please downscale it first.")
        img.draft("RGB", (MAX_SIDE, MAX_SIDE))  # JPEG only: decode at reduced size (huge RAM saver)
        img = img.convert("RGB")
        img.thumbnail((MAX_SIDE, MAX_SIDE))
    except ImageError:
        raise
    except (OSError, ValueError, Image.DecompressionBombError):
        raise ImageError("Could not read this file. Please upload a valid JPG or PNG image.")
    rgb = np.array(img)
    return rgb, orig_w / rgb.shape[1]


# --------------------------------------------------------------- detection
def _in_range(hsv: np.ndarray, p: tuple) -> np.ndarray:
    lo = np.array([p[0], p[2], p[4]], np.uint8)
    hi = np.array([p[1], p[3], p[5]], np.uint8)
    return cv2.inRange(hsv, lo, hi) > 0


def detect_water(rgb: np.ndarray, mode: str, hsv_params: tuple | None = None,
                 dark_thresh: float | None = None, min_blob_pct: float = 0.05):
    """Return (mask uint8 0/255, valid bool mask, dark threshold used or None)."""
    blur = cv2.GaussianBlur(rgb, (5, 5), 0)          # suppress speckle before thresholding
    hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)
    used_thresh = None

    if mode == MODE_RADAR:
        gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)
        valid = gray > 3                              # pure black = no-data border
        if dark_thresh is None:                       # Otsu on valid pixels only
            vals = gray[valid].reshape(-1, 1)
            dark_thresh = float(cv2.threshold(vals, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]) if vals.size else 0.0
        used_thresh = dark_thresh
        raw = gray < dark_thresh
    else:
        valid = hsv[:, :, 2] > 12                     # ignore black no-data borders
        if mode == MODE_BOTH:
            raw = _in_range(hsv, CLEAR_HSV) | _in_range(hsv, MUDDY_HSV)
        elif mode == MODE_MUDDY:
            raw = _in_range(hsv, hsv_params or MUDDY_HSV)
        else:
            raw = _in_range(hsv, hsv_params or CLEAR_HSV)

    mask = ((raw & valid).astype(np.uint8)) * 255

    # Clean up: remove salt-and-pepper noise, fill pinholes, drop tiny blobs.
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    _, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    min_area = max(25, int(min_blob_pct / 100.0 * mask.size))
    keep = stats[:, cv2.CC_STAT_AREA] >= min_area
    keep[0] = False                                   # label 0 = background
    mask = keep[labels].astype(np.uint8) * 255
    return mask, valid, used_thresh


# ------------------------------------------------------------------ scoring
def severity(pct: float) -> tuple[str, str]:
    """Map % of image flooded to (label, streamlit alert level)."""
    if pct < 5:
        return "Minimal", "success"
    if pct < 20:
        return "Moderate", "info"
    if pct < 40:
        return "Severe", "warning"
    return "Critical", "error"


def render_overlay(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Tint detected water and outline it so it stands out on any background."""
    tint = np.empty_like(rgb)
    tint[:] = OVERLAY_RGB
    blended = cv2.addWeighted(rgb, 0.55, tint, 0.45, 0)
    out = np.where(mask[:, :, None] > 0, blended, rgb).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, contours, -1, CONTOUR_RGB, 1)
    return out


def analyse(rgb: np.ndarray, scale: float, mode: str, hsv_params: tuple | None = None,
            dark_thresh: float | None = None, min_blob_pct: float = 0.05,
            m_per_px: float = 0.0) -> Assessment:
    """Full pipeline: detect -> score -> overlay."""
    mask, valid, used = detect_water(rgb, mode, hsv_params, dark_thresh, min_blob_pct)
    valid_px = int(valid.sum())
    flooded_px = int((mask > 0).sum())
    pct = 100.0 * flooded_px / valid_px if valid_px else 0.0
    label, level = severity(pct)
    km2 = flooded_px * (m_per_px * scale) ** 2 / 1e6 if m_per_px > 0 else None
    return Assessment(render_overlay(rgb, mask), mask, pct, flooded_px, valid_px, label, level, km2, used)

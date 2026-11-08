"""Synthetic test scene so the tab can be demoed without real imagery."""
from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np
from PIL import Image


def make_demo_image(return_truth: bool = False):
    """Green farmland + buildings + a blue pond + a brown floodwater area."""
    h, w = 480, 640
    rng = np.random.default_rng(7)
    img = np.empty((h, w, 3), np.uint8)
    img[:] = (95, 125, 65)                                   # farmland
    truth = np.zeros((h, w), np.uint8)

    for x, y in [(60, 60), (120, 90), (480, 70), (540, 120), (80, 380)]:
        cv2.rectangle(img, (x, y), (x + 40, y + 28), (150, 150, 150), -1)  # grey buildings

    cv2.ellipse(img, (200, 160), (110, 60), 0, 0, 360, (45, 95, 160), -1)  # clear blue water
    cv2.ellipse(truth, (200, 160), (110, 60), 0, 0, 360, 255, -1)
    poly = np.array([[330, 300], [620, 260], [630, 460], [300, 450]], np.int32)
    cv2.fillPoly(img, [poly], (150, 105, 70))                              # muddy floodwater
    cv2.fillPoly(truth, [poly], 255)

    noise = rng.normal(0, 6, img.shape)
    img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    rgb = img
    return (rgb, truth) if return_truth else rgb


def demo_png_bytes() -> bytes:
    buf = BytesIO()
    Image.fromarray(make_demo_image()).save(buf, format="PNG")
    return buf.getvalue()

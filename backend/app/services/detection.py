from __future__ import annotations

import imghdr
from dataclasses import dataclass

import cv2
import numpy as np


SUPPORTED_FORMATS = {"png", "jpeg", "webp"}


@dataclass
class PieceDetection:
    label: str
    confidence: float
    bbox: list[int]
    contour: list[list[int]]


def validate_image_format(data: bytes) -> None:
    image_type = imghdr.what(None, h=data)
    if image_type not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format: {image_type}")


def detect_garment_pieces(data: bytes) -> tuple[str, list[PieceDetection]]:
    """
    Lightweight contour-based fallback detector. Intended as MVP bridge
    before connecting SAM/YOLO models.
    """
    np_img = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image file")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    garment_guess = "Luxury Hoodie" if image.shape[0] >= image.shape[1] else "Joggers"

    labels = [
        "front body",
        "back body",
        "sleeve",
        "hood",
        "pocket",
        "cuff",
        "waistband",
    ]

    pieces: list[PieceDetection] = []
    for idx, contour in enumerate(sorted(contours, key=cv2.contourArea, reverse=True)[:7]):
        x, y, w, h = cv2.boundingRect(contour)
        if w * h < 1200:
            continue
        approx = cv2.approxPolyDP(contour, epsilon=0.01 * cv2.arcLength(contour, True), closed=True)
        points = [[int(pt[0][0]), int(pt[0][1])] for pt in approx]
        pieces.append(
            PieceDetection(
                label=labels[idx % len(labels)],
                confidence=round(0.7 - (idx * 0.05), 2),
                bbox=[x, y, x + w, y + h],
                contour=points,
            )
        )

    return garment_guess, pieces

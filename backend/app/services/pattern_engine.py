from __future__ import annotations

from copy import deepcopy

from shapely import affinity
from shapely.geometry import Polygon

from app.schemas.patterns import GeneratePatternRequest, PieceGeometry

SIZE_ORDER = ["XS", "S", "M", "L", "XL", "XXL"]


def _fit_multiplier(fit: str) -> float:
    return {"slim": 0.96, "regular": 1.0, "oversized": 1.08}[fit]


def build_base_pattern(payload: GeneratePatternRequest) -> list[PieceGeometry]:
    m = payload.measurements
    f = _fit_multiplier(payload.fit)

    body_w = m.chest * 0.26 * f
    body_h = m.garment_length * 0.8
    sleeve_w = m.bicep if hasattr(m, "bicep") else m.thigh_circumference * 0.4
    sleeve_h = m.sleeve_length * 0.55

    pieces = [
        PieceGeometry(
            name="Front Body",
            cut_instruction="Front Body - Cut 1 on Fold",
            points=[[0, 0], [body_w, 0], [body_w * 0.96, body_h], [0, body_h]],
            grainline=[[body_w * 0.5, 2], [body_w * 0.5, body_h - 2]],
            notches=[[body_w * 0.25, body_h * 0.35], [body_w * 0.75, body_h * 0.35]],
            fold_line=[[0, 0], [0, body_h]],
        ),
        PieceGeometry(
            name="Back Body",
            cut_instruction="Back Body - Cut 1 on Fold",
            points=[[0, 0], [body_w * 1.01, 0], [body_w, body_h], [0, body_h]],
            grainline=[[body_w * 0.5, 2], [body_w * 0.5, body_h - 2]],
            notches=[[body_w * 0.28, body_h * 0.35], [body_w * 0.72, body_h * 0.35]],
            fold_line=[[0, 0], [0, body_h]],
        ),
        PieceGeometry(
            name="Sleeve",
            cut_instruction="Sleeve - Cut 2",
            points=[[0, 0], [sleeve_w, 0], [sleeve_w * 0.9, sleeve_h], [sleeve_w * 0.1, sleeve_h]],
            grainline=[[sleeve_w * 0.5, 1], [sleeve_w * 0.5, sleeve_h - 1]],
            notches=[[sleeve_w * 0.2, sleeve_h * 0.2], [sleeve_w * 0.8, sleeve_h * 0.2]],
        ),
        PieceGeometry(
            name="Waistband",
            cut_instruction="Waistband - Cut 1",
            points=[[0, 0], [m.waist * 0.52, 0], [m.waist * 0.52, 4], [0, 4]],
            grainline=[[2, 2], [m.waist * 0.52 - 2, 2]],
            notches=[[m.waist * 0.26, 0]],
        ),
    ]

    return [add_seam_allowance(piece, payload.seam_allowance) for piece in pieces]


def add_seam_allowance(piece: PieceGeometry, seam_allowance: float) -> PieceGeometry:
    poly = Polygon(piece.points)
    buffered = poly.buffer(seam_allowance, join_style="mitre")
    if buffered.is_empty:
        return piece

    coords = list(buffered.exterior.coords)[:-1]
    updated = piece.model_copy(deep=True)
    updated.points = [[round(x, 3), round(y, 3)] for x, y in coords]
    return updated


def grade_pattern(base_pieces: list[PieceGeometry]) -> dict[str, list[PieceGeometry]]:
    increments = {
        "XS": -0.08,
        "S": -0.04,
        "M": 0.0,
        "L": 0.04,
        "XL": 0.08,
        "XXL": 0.12,
    }

    graded: dict[str, list[PieceGeometry]] = {}
    for size, factor in increments.items():
        pieces = []
        scale = 1 + factor
        for piece in base_pieces:
            poly = Polygon(piece.points)
            scaled = affinity.scale(poly, xfact=scale, yfact=scale, origin="centroid")
            sized = deepcopy(piece)
            sized.points = [[round(x, 3), round(y, 3)] for x, y in list(scaled.exterior.coords)[:-1]]
            pieces.append(sized)
        graded[size] = pieces

    return graded

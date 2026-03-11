from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.patterns import DetectionResponse, GeneratePatternRequest, GeneratePatternResponse
from app.services.detection import detect_garment_pieces, validate_image_format
from app.services.exporters import export_dxf, export_pdf, export_svg
from app.services.pattern_engine import build_base_pattern, grade_pattern

router = APIRouter()


@router.post("/detect", response_model=DetectionResponse)
async def detect(file: UploadFile = File(...)) -> DetectionResponse:
    raw = await file.read()
    try:
        validate_image_format(raw)
        guess, pieces = detect_garment_pieces(raw)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return DetectionResponse(
        garment_type_guess=guess,
        pieces=[
            {
                "label": p.label,
                "confidence": p.confidence,
                "bbox": p.bbox,
                "contour": p.contour,
            }
            for p in pieces
        ],
    )


@router.post("/patterns/generate", response_model=GeneratePatternResponse)
def generate_patterns(payload: GeneratePatternRequest) -> GeneratePatternResponse:
    base = build_base_pattern(payload)
    graded = grade_pattern(base)
    return GeneratePatternResponse(pieces=base, graded_sizes=graded)


@router.post("/patterns/export")
def export_patterns(payload: GeneratePatternRequest) -> dict[str, str]:
    base = build_base_pattern(payload)
    return {
        "pdf": export_pdf(base, "jcfits-pattern.pdf"),
        "svg": export_svg(base, "jcfits-pattern.svg"),
        "dxf": export_dxf(base, "jcfits-pattern.dxf"),
    }

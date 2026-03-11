from typing import Literal

from pydantic import BaseModel, Field


class Measurements(BaseModel):
    chest: float = Field(40, gt=0)
    waist: float = Field(34, gt=0)
    hip: float = Field(40, gt=0)
    inseam: float = Field(31, gt=0)
    rise: float = Field(11, gt=0)
    shoulder_width: float = Field(18, gt=0)
    sleeve_length: float = Field(25, gt=0)
    garment_length: float = Field(28, gt=0)
    thigh_circumference: float = Field(24, gt=0)
    ankle_opening: float = Field(12, gt=0)


class PieceGeometry(BaseModel):
    name: str
    cut_instruction: str
    points: list[list[float]]
    grainline: list[list[float]]
    notches: list[list[float]]
    fold_line: list[list[float]] | None = None


class GeneratePatternRequest(BaseModel):
    garment_type: Literal[
        "Luxury Hoodie",
        "Tech Jacket",
        "Joggers",
        "Sweatpants",
        "T-Shirt",
        "Cargo Pants",
        "Leggings",
        "Sports Bra",
        "Shorts",
    ] = "Luxury Hoodie"
    measurements: Measurements
    seam_allowance: float = Field(0.375, gt=0)
    fit: Literal["slim", "regular", "oversized"] = "regular"


class GeneratePatternResponse(BaseModel):
    base_size: str = "M"
    pieces: list[PieceGeometry]
    graded_sizes: dict[str, list[PieceGeometry]]


class DetectionPiece(BaseModel):
    label: str
    confidence: float
    bbox: list[int]
    contour: list[list[int]]


class DetectionResponse(BaseModel):
    garment_type_guess: str
    pieces: list[DetectionPiece]

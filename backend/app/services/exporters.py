from __future__ import annotations

from pathlib import Path

import ezdxf
import svgwrite
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.schemas.patterns import PieceGeometry


def ensure_export_dir() -> Path:
    out = Path("exports")
    out.mkdir(parents=True, exist_ok=True)
    return out


def export_svg(pieces: list[PieceGeometry], filename: str) -> str:
    out = ensure_export_dir() / filename
    drawing = svgwrite.Drawing(str(out), profile="tiny")
    for piece in pieces:
        drawing.add(drawing.polygon(piece.points, fill="none", stroke="black", stroke_width=0.4))
        drawing.add(drawing.text(piece.cut_instruction, insert=(piece.points[0][0], piece.points[0][1] - 2), font_size="3px"))
    drawing.save()
    return str(out)


def export_pdf(pieces: list[PieceGeometry], filename: str) -> str:
    out = ensure_export_dir() / filename
    c = canvas.Canvas(str(out), pagesize=letter)
    width, height = letter

    # tiled alignment markers and scale box
    c.rect(20, height - 80, 72, 72)
    c.drawString(25, height - 90, "1 in scale box")

    y = height - 140
    for piece in pieces:
        c.drawString(30, y, piece.cut_instruction)
        y -= 16

    for x in range(20, int(width), 100):
        c.line(x, 10, x, 20)
    c.showPage()
    c.save()
    return str(out)


def export_dxf(pieces: list[PieceGeometry], filename: str) -> str:
    out = ensure_export_dir() / filename
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    for piece in pieces:
        msp.add_lwpolyline(piece.points, close=True)
    doc.saveas(out)
    return str(out)

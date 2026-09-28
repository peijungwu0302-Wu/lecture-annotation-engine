"""Generate the copyright-safe synthetic input/output PDFs used by Phase 1."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples/synthetic-input/synthetic-lecture.pdf"
OUTPUT = ROOT / "examples/synthetic-output/synthetic-annotated.pdf"
PREVIEW = ROOT / "examples/preview/synthetic-annotated-page-1.png"

INK = HexColor("#171717")
ACCENT = HexColor("#164E63")
TRANSLATION = HexColor("#416F81")
PAPER_BLUE = HexColor("#E7F3F6")
RULE = HexColor("#454545")
SOFT = HexColor("#F5F1E8")
CJK_FONT = "LAE-CJK"
ARTIFACT_BOX_PT = (486.0, 679.0, 8.0, 8.0)
RIGHT_LANE_BOX_PT = (505.0, 610.0, 66.0, 95.0)


def _register_fonts() -> None:
    configured = os.environ.get("LAE_CJK_FONT")
    candidates = [
        Path(configured) if configured else None,
        Path("C:/Windows/Fonts/NotoSansTC-VF.ttf"),
        Path("C:/Windows/Fonts/kaiu.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
    ]
    for candidate in candidates:
        if candidate and candidate.is_file():
            pdfmetrics.registerFont(TTFont(CJK_FONT, str(candidate)))
            return
    raise RuntimeError("No embeddable CJK font found; set LAE_CJK_FONT to a TTF/TTC font")


def _wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    font: str = "Times-Roman",
    size: float = 9.2,
    leading: float | None = None,
    color: Color = INK,
) -> float:
    leading = leading or size * 1.28
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and pdfmetrics.stringWidth(candidate, font, size) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def _zh(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    size: float = 7.5,
    color: Color = TRANSLATION,
) -> float:
    font = CJK_FONT
    leading = size * 1.45
    line = ""
    lines: list[str] = []
    for character in text:
        candidate = line + character
        if line and pdfmetrics.stringWidth(candidate, font, size) > width:
            lines.append(line)
            line = character
        else:
            line = candidate
    if line:
        lines.append(line)
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for item in lines:
        pdf.drawString(x, y, item)
        y -= leading
    return y


def _label(pdf: canvas.Canvas, text: str, x: float, y: float, width: float) -> None:
    pdf.setStrokeColor(ACCENT)
    pdf.setLineWidth(0.7)
    pdf.rect(x, y - 4, width, 17, stroke=1, fill=0)
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(x + 5, y + 1, text)


def _frame(pdf: canvas.Canvas, annotated: bool) -> None:
    width, height = A4
    pdf.setTitle("Synthetic annotated lecture" if annotated else "Synthetic lecture")
    pdf.setAuthor("Lecture Annotation Engine contributors")
    pdf.setSubject("Copyright-safe synthetic fixture; contains no course-source material")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(92, height - 35, "SYNTHETIC LECTURE 01")
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawRightString(width - 92, height - 35, "Vectors and Linear Structure")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.7)
    pdf.line(92, height - 42, width - 92, height - 42)
    pdf.line(92, 43, width - 92, 43)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawString(92, 29, "OPEN SYNTHETIC FIXTURE - APACHE-2.0")
    pdf.drawCentredString(width / 2, 29, "1")
    pdf.drawRightString(width - 92, 29, "LECTURE ANNOTATION ENGINE")


def _source_artifact(pdf: canvas.Canvas) -> None:
    x, y, width, height = ARTIFACT_BOX_PT
    pdf.setFillColor(black)
    pdf.rect(x, y, width, height, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 4.8)
    pdf.drawRightString(x + width, y - 7, "SOURCE ARTIFACT")


def _figure(pdf: canvas.Canvas, x: float, y: float) -> None:
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(0.8)
    pdf.line(x, y, x + 105, y)
    pdf.line(x + 15, y - 25, x + 15, y + 48)
    pdf.setStrokeColor(ACCENT)
    pdf.setLineWidth(2)
    pdf.line(x + 15, y, x + 82, y + 33)
    pdf.setFillColor(ACCENT)
    path = pdf.beginPath()
    path.moveTo(x + 82, y + 33)
    path.lineTo(x + 74, y + 33)
    path.lineTo(x + 79, y + 26)
    path.close()
    pdf.drawPath(path, stroke=0, fill=1)
    pdf.setFont("Helvetica-Oblique", 7)
    pdf.drawString(x + 85, y + 32, "v")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 5.2)
    pdf.drawString(x + 24, y - 15, "Figure 1. A vector as directed displacement")


def _draw_source(pdf: canvas.Canvas, *, annotated: bool) -> None:
    width, height = A4
    _frame(pdf, annotated)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawCentredString(width / 2, height - 77, "Vector Spaces: a Compact Lecture")
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(width / 2, height - 92, "A fully synthetic demonstration page")

    main_x = 108 if annotated else 92
    main_w = 365 if annotated else 411
    y = height - 128

    _label(pdf, "Definition", main_x, y, 62)
    y -= 22
    y = _wrapped(
        pdf,
        "A vector space is a collection of objects that can be added and scaled without leaving the collection.",
        main_x,
        y,
        main_w,
    )
    _source_artifact(pdf)
    if annotated:
        y = _zh(pdf, "中譯｜向量空間是一個在向量加法與純量乘法下仍保持封閉的集合。", main_x, y - 1, main_w)
    y -= 11

    _label(pdf, "Example", main_x, y, 52)
    y -= 22
    y = _wrapped(
        pdf,
        "Pairs (x, y) form a vector space: add coordinates componentwise and multiply both coordinates by the same scalar.",
        main_x,
        y,
        main_w,
    )
    pdf.setFont("Times-Italic", 10)
    pdf.drawCentredString(main_x + main_w / 2, y - 1, "a(u + v) = au + av")
    y -= 16
    if annotated:
        y = _zh(pdf, "中譯｜每個運算都逐座標進行，因此結果仍是一組二維座標。", main_x, y, main_w)
    y -= 10

    _label(pdf, "Figure", main_x, y, 47)
    _figure(pdf, main_x + 8, y - 47)
    if annotated:
        _zh(pdf, "中譯｜箭頭同時表達方向與大小。", main_x + 128, y - 22, main_w - 128)
    y -= 82

    _label(pdf, "Result", main_x, y, 43)
    y -= 22
    y = _wrapped(
        pdf,
        "Two non-parallel vectors in the plane provide a basis for every planar vector.",
        main_x,
        y,
        main_w,
    )
    if annotated:
        y = _zh(pdf, "中譯｜平面中兩個不平行向量可唯一表示任意平面向量。", main_x, y - 1, main_w)
    y -= 10

    _label(pdf, "Proof", main_x, y, 40)
    y -= 22
    y = _wrapped(
        pdf,
        "Place the two vectors as columns of a 2 by 2 matrix. Non-parallel columns give a nonzero determinant, so the coordinate system has a unique solution.",
        main_x,
        y,
        main_w,
    )
    pdf.setFont("Times-Italic", 10)
    pdf.drawCentredString(main_x + main_w / 2, y - 1, "det[u  v] != 0")
    y -= 17
    if annotated:
        y = _zh(pdf, "中譯｜行列式非零等價於兩欄獨立，因此座標解存在且唯一。", main_x, y, main_w)
    y -= 10

    _label(pdf, "Exercise", main_x, y, 54)
    y -= 22
    _wrapped(
        pdf,
        "Decide whether u = (1, 1) and v = (2, -1) form a basis, then express w = (5, 1) in that basis.",
        main_x,
        y,
        main_w,
    )


def _annotation_layers(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 6.4)
    pdf.drawString(24, 704, "REVISION LANE")
    _wrapped(pdf, "Revision cue\nclosure -> operations stay inside", 24, 691, 70, font="Helvetica", size=6.2, leading=8, color=ACCENT)
    _wrapped(pdf, "Common mistake\nnonzero does not mean independent", 24, 535, 70, font="Helvetica", size=6.2, leading=8, color=ACCENT)
    _wrapped(pdf, "Checklist\n1. determinant\n2. solve coordinates\n3. interpret", 24, 337, 70, font="Helvetica", size=6.2, leading=8, color=ACCENT)

    right_x, _, right_width, _ = RIGHT_LANE_BOX_PT
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 6.4)
    pdf.drawString(right_x, 704, "EXPLANATION LANE")
    _wrapped(pdf, "Intuition\nA vector space is a sandbox closed under two moves.", right_x, 691, right_width, font="Helvetica", size=6.2, leading=8, color=ACCENT)
    _wrapped(pdf, "Figure guide\nRead tail, head, direction, then length.", right_x, 542, right_width, font="Helvetica", size=6.2, leading=8, color=ACCENT)

    pdf.setFillColor(SOFT)
    pdf.roundRect(166, 69, 270, 68, 5, stroke=0, fill=1)
    pdf.setStrokeColor(ACCENT)
    pdf.setLineWidth(0.6)
    pdf.roundRect(166, 69, 270, 68, 5, stroke=1, fill=0)
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawString(177, 122, "Derivation island - exercise solution")
    _wrapped(
        pdf,
        "det[[1, 2], [1, -1]] = -3, so the vectors form a basis. Solving c1 u + c2 v = w gives c1 = 7/3 and c2 = 4/3.",
        177,
        109,
        248,
        font="Helvetica",
        size=6.7,
        leading=8.4,
        color=ACCENT,
    )


def _write_pdf(path: Path, *, annotated: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    _draw_source(pdf, annotated=annotated)
    if annotated:
        _annotation_layers(pdf)
    pdf.showPage()
    pdf.save()


def _render_preview() -> None:
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    renderer = shutil.which("pdftoppm")
    if renderer is None:
        raise RuntimeError("pdftoppm is required to render the regression preview")
    prefix = PREVIEW.with_suffix("")
    subprocess.run(
        [renderer, "-f", "1", "-l", "1", "-singlefile", "-r", "150", "-png", str(OUTPUT), str(prefix)],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-preview", action="store_true")
    args = parser.parse_args()
    _register_fonts()
    _write_pdf(SOURCE, annotated=False)
    _write_pdf(OUTPUT, annotated=True)
    if not args.no_preview:
        _render_preview()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import os

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import BASE_DIR


def fill_line(limit, value):
    value = str(value or "")
    missing = max(0, limit - len(value))
    left = missing // 2
    right = missing - left
    return "_" * left + value + "_" * right


def register_fonts():
    font_dir = os.path.join(BASE_DIR, "fonts")
    pdfmetrics.registerFont(TTFont("Arial", os.path.join(font_dir, "Arial.TTF")))
    pdfmetrics.registerFont(TTFont("ArialBold", os.path.join(font_dir, "Arialbd.TTF")))


def create_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Titulo",
            parent=styles["Normal"],
            fontName="ArialBold",
            fontSize=12,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=50,
        ),
        "body": ParagraphStyle(
            "Corpo",
            parent=styles["Normal"],
            fontName="Arial",
            fontSize=12,
            leading=16,
            alignment=TA_JUSTIFY,
            firstLineIndent=0,
            spaceAfter=29,
        ),
        "center": ParagraphStyle(
            "Centro",
            parent=styles["Normal"],
            fontName="Arial",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            firstLineIndent=0,
            spaceAfter=29,
        ),
        "indent": ParagraphStyle(
            "Indent",
            parent=styles["Normal"],
            fontName="Arial",
            fontSize=12,
            leading=16,
            alignment=TA_JUSTIFY,
            firstLineIndent=15,
            spaceAfter=29,
        ),
    }

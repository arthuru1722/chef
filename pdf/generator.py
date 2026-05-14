import io
import re
import unicodedata

from reportlab.platypus import SimpleDocTemplate

from pdf.contract_template import criar_paragrafos
from pdf.styles import create_styles, fill_line, register_fonts


def clean_filename(name):
    name = unicodedata.normalize("NFKD", name or "")
    name = name.encode("ASCII", "ignore").decode("ASCII")
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
    words = name.strip().split()[:2]
    return "".join(word.capitalize() for word in words) or "SemNome"


def build_contract_pdf(values, image_source=None):
    register_fonts()
    styles = create_styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        leftMargin=50,
        rightMargin=50,
        topMargin=60,
        bottomMargin=60,
    )
    doc.build(criar_paragrafos(values, fill_line, {"Normal": styles["body"]}, img_path=image_source))
    buffer.seek(0)
    return buffer


def contract_download_name(values):
    return f"contrato{clean_filename(values.get('nomeContratante'))}.pdf"

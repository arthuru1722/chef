from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def preencher(limite, valor):
    valor = valor
    faltam = limite - len(valor)
    esquerda = faltam // 2
    direita = faltam - esquerda
    return "_" * esquerda + valor + "_" * direita

def criar_estilos():
    styles = getSampleStyleSheet()
    
    style_titulo = ParagraphStyle(
        "Titulo", 
        parent=styles["Normal"], 
        fontName="ArialBold", 
        fontSize=12, 
        leading=14, 
        alignment=TA_CENTER, 
        spaceAfter=50
    )
    style_corpo = ParagraphStyle(
        "Corpo", 
        parent=styles["Normal"], 
        fontName="Arial", 
        fontSize=12, 
        leading=16, 
        alignment=TA_JUSTIFY, 
        firstLineIndent=0, 
        spaceAfter=30
    )
    style_corpo_indent = ParagraphStyle(
        "Indent", 
        parent=styles["Normal"], 
        fontName="Arial", 
        fontSize=12, 
        leading=16, 
        alignment=TA_JUSTIFY, 
        firstLineIndent=15, 
        spaceAfter=30
    )
    
    return {
        "titulo": style_titulo,
        "corpo": style_corpo,
        "corpo_indent": style_corpo_indent,
        "styles": styles
    }

def configurar_fontes():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    
    font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    pdfmetrics.registerFont(TTFont("Arial", os.path.join(font_dir, "Arial.TTF")))
    pdfmetrics.registerFont(TTFont("ArialBold", os.path.join(font_dir, "Arialbd.TTF")))
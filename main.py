from pdf.generator import build_contract_pdf
from services.images import default_image_source
from values import VALORES


def gerar_contrato_pdf(valores, img_path=None):
    return build_contract_pdf(valores, image_source=img_path or default_image_source())


def main():
    pdf = gerar_contrato_pdf(VALORES)
    print(f"PDF gerado em memoria com {len(pdf.getvalue())} bytes.")


if __name__ == "__main__":
    main()

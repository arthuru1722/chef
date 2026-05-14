from reportlab.platypus import Paragraph, Image, PageBreak, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import os

def _valor(valores, chave, padrao="", antigas=None):
    if chave in valores:
        return valores.get(chave, padrao)
    for antiga in antigas or []:
        if antiga in valores:
            return valores.get(antiga, padrao)
    return padrao


def criar_paragrafos(VALORES, preencher, styles, img_path=None):
    #eu poderia colocar isso no utils.py ou criar um styles.py, pra se pensar ou ignorar no futuro
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
        spaceAfter=29
    )
    style_corpo_centro = ParagraphStyle(
        "centro",
        parent=styles["Normal"], 
        fontName="Arial", 
        fontSize=12, 
        leading=16, 
        alignment=TA_CENTER, 
        firstLineIndent=0, 
        spaceAfter=29
    )
    style_corpo_indent = ParagraphStyle(
        "Indent", 
        parent=styles["Normal"], 
        fontName="Arial", 
        fontSize=12, 
        leading=16, 
        alignment=TA_JUSTIFY, 
        firstLineIndent=15, 
        spaceAfter=29
    )
    
    def gerar_materiais():
        linhas = ""
        for i, mat in enumerate(VALORES["materiais"], start=1):
            linhas += f'{i}) {preencher(40, mat["nome"])} Custo de reposição: R$ {preencher(10, mat["custo"])}<br/>'
        return linhas

    PARAGRAPHOS = [
        Paragraph("CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE BUFFET", style_titulo),
        
        Paragraph('<font name="ArialBold">IDENTIFICAÇÃO DAS PARTES CONTRATANTES:</font>', style_corpo),

        Paragraph(
            f'<font name="ArialBold">Contratante:</font> {preencher(30, VALORES["nomeContratante"])} Nacionalidade {preencher(10, VALORES["nacionalidadeContratante"])} Estado Civil {preencher(10, VALORES["estadoCivilContratante"])}, Profissão {preencher(10, VALORES["profissaoContratante"])}, Carteira de Identidade n° {preencher(9, VALORES["rgContratante"])}, C.P.F/CNPJ nº {preencher(20, VALORES["cpfContratante"])}, localizado na Rua {preencher(20, VALORES["ruaContratante"])}, nº {preencher(4, VALORES["numeroContratante"])}, bairro {preencher(10, VALORES["bairroContratante"])}, Cep {preencher(9, VALORES["cepContratante"])}, Cidade {preencher(10, VALORES["cidadeContratante"])}, no Estado {preencher(2, VALORES["estadoContratante"])};',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Contratada:</font> {preencher(30, VALORES["nomeContratada"])} CNPJ nº {preencher(20, VALORES["cnpjContratada"])}, localizado na Rua {preencher(25, VALORES["ruaContratada"])}, nº {preencher(4, VALORES["numeroContratada"])}, bairro {preencher(10, VALORES["bairroContratada"])}, Cep {preencher(9, VALORES["cepContratada"])}, Cidade {preencher(10, VALORES["cidadeContratada"])}, no Estado {preencher(2, VALORES["estadoContratada"])};',
            style_corpo
        ),

        Paragraph(
            "As partes acima identificadas têm, entre si, justo e acertado o presente Contrato de Prestação de Serviços de Buffet, que se regerá pelas cláusulas seguintes e pelas condições de preço, forma e termo de pagamento descritas no presente.",
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 1ª.</font> É objeto do presente contrato a prestação pela CONTRATADA à CONTRATANTE dos serviços de Buffet, em evento que se realizará na data de {preencher(2, VALORES["diaEvento"])}/{preencher(2, VALORES["mesEvento"])}/{preencher(4, VALORES["anoEvento"])}, às {preencher(2, VALORES["horaEvento"])}:{preencher(2, VALORES["minutoEvento"])} horas, no salão de festas situado na Rua {preencher(30, VALORES["ruaEvento"])}, nº {preencher(4, VALORES["numeroEvento"])}, bairro {preencher(10, VALORES["bairroEvento"])}, Cep {preencher(9, VALORES["cepEvento"])}, Cidade {preencher(10, VALORES["cidadeEvento"])}, no Estado {preencher(2, VALORES["estadoEvento"])};',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 2ª.</font> O evento, para cuja realização são contratados os serviços de buffet, é um(a) {preencher(15, VALORES["tipoEvento"])}, e contará com a presença de {preencher(3, VALORES["qtdPessoas"])} pessoas.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 3ª.</font> A CONTRATANTE deverá fornecer à CONTRATADA todas as informações necessárias à realização adequada do serviço de buffet, devendo especificar os detalhes do evento, necessários ao perfeito fornecimento do serviço, e a forma como este deverá ser prestado.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 4ª.</font> É dever da CONTRATADA oferecer um serviço de buffet de acordo com as especificações da CONTRATANTE, devendo o serviço iniciar-se às {preencher(2, VALORES["inicioHora"])}:{preencher(2, VALORES["inicioMinuto"])} horas e terminar às {preencher(2, VALORES["terminoHora"])}:{preencher(2, VALORES["terminoMinuto"])} horas.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 5ª.</font> A CONTRATADA será responsável pela organização do local do evento, fornecendo os seguintes materiais necessários para o melhor desempenho da prestação do serviço de Buffet:',
            style_corpo
        ),

        Paragraph(gerar_materiais(), style_corpo),

        Paragraph(
            f'<font name="ArialBold">Cláusula 6ª.</font> A CONTRATADA compromete-se a chegar no local do evento às {preencher(2, VALORES["chegadaHora"])}:{preencher(2, VALORES["chegadaMinuto"])} horas, a fim de arrumar o local do evento com antecedência de {preencher(2, VALORES["antecedenciaHoras"])} horas.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 7ª.</font> A CONTRATADA se compromete a fornecer o cardápio escolhido pela CONTRATANTE, cujas especificações, inclusive de quantidade a ser servida, encontram-se em documento anexo ao final deste presente contrato, passando a integrar-lhe.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 8ª.</font> A CONTRATADA fornecerá {preencher(2, VALORES["qtdGarcons"])} garçons e {preencher(2, VALORES["qtdCopeiros"])} copeiros para a prestação dos serviços ora contratados.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 9ª.</font> A CONTRATADA será a única e exclusiva responsável por todos os seus funcionários que trabalharem no evento referido na cláusula 2ª, cabendo a ela o cumprimento das obrigações trabalhistas entre outras.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 10ª.</font> É dever da CONTRATADA manter todos os seus funcionários devidamente uniformizados durante a prestação dos serviços ora contratados, garantindo que todos eles possuam os requisitos de urbanidade, moralidade e educação. <br/><br/>'
            f'Parágrafo único. Caso algum funcionário seja afastado a pedido do CONTRATANTE, fica a critério da CONTRATADA substituí-lo ou não por outro, sem gerar multa ou danos à CONTRATADA.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 11ª.</font> O serviço contratado no presente instrumento será remunerado pela quantia de R$ {preencher(10, VALORES["valorTotalNumero"])} ({preencher(30, VALORES["valorTotalExtenso"])}).<br/><br/>'

            f'Parágrafo 1. O pagamento será realizado via {preencher(20, VALORES["tipoPagamento"])}, parcelado em 2 vezes.<br/>'

            f'1ª parcela - R$ {preencher(15, VALORES["parcela1Numero"])} ({preencher(30, VALORES["parcela1Extenso"])}) em {preencher(2, VALORES["parcela1Dia"])}/{preencher(2, VALORES["parcela1Mes"])}/{preencher(4, VALORES["parcela1Ano"])}<br/>'

            f'2ª parcela - R$ {preencher(15, VALORES["parcela2Numero"])} ({preencher(30, VALORES["parcela2Extenso"])}) em {preencher(2, VALORES["parcela2Dia"])}/{preencher(2, VALORES["parcela2Mes"])}/{preencher(4, VALORES["parcela2Ano"])}.',
            style_corpo
        ),

        Paragraph(
            f'Parágrafo 2. Em caso de desistência por parte da CONTRATANTE, não será concedido reembolso dos valores já pagos, visto que tais valores são retidos para cobrir custos administrativos e logísticos incorridos pela CONTRATADA devido à desistência.<br/><br/>'

            f'Parágrafo 3. Mesmo nos casos previstos no Parágrafo 2º desta cláusula, a CONTRATANTE poderá usar os valores já pagos como crédito para um novo agendamento, pelo prazo máximo de 6 (seis) meses a partir da data do cancelamento, desde que haja disponibilidade na agenda da CONTRATADA e que a solicitação seja feita com antecedência mínima de {preencher(2, VALORES["antecedenciaCredito"])} dias.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 12ª.</font> Em caso de inadimplemento por parte do CONTRATANTE quanto ao pagamento do serviço prestado, deverá incidir sobre o valor do presente instrumento multa pecuniária de 2%, juros de mora de 1% ao mês e correção monetária.<br/><br/>'

            f'Parágrafo único. Em caso de cobrança judicial, devem ser acrescidas custas processuais e 30% de honorários advocatícios.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 13ª.</font> Todos os utensílios e objetos fornecidos pela CONTRATADA, cujo a lista encontra-se na cláusula 5, deverão ser devolvidos em perfeito estado de conservação, sob pena da CONTRATANTE arcar com os respectivos custos de substituição mencionados na cláusula 5.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 14ª.</font> A CONTRATANTE assume a responsabilidade de cobrir os custos de substituição dos itens danificados ou perdidos durante o evento, com a obrigação de efetuar o pagamento ao término do evento.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 15ª.</font> Caso a parte CONTRATANTE opte pela desistência, será necessário um aviso formal por escrito, ocorrendo com pelo menos {preencher(2, VALORES["antecedenciaDesistencia"])} dias corridos de antecedência em relação à data prevista para o evento.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 16ª.</font> O cardápio foi elaborado de acordo com o número de convidados determinado pela CONTRATANTE.<br/><br/>'

            f'Parágrafo 1. Na hipótese de exceder o número de convidados, a CONTRATANTE compromete-se a pagar uma taxa de R$ {preencher(3, VALORES["valorExtraNumero"])} para cada novo convidado.<br/><br/>'

            f'Parágrafo 2. No caso do excesso de convidados, a CONTRATADA não será responsabilizada se atendidas as especificações, ocorrer a insuficiência da comida e/ou da bebida devido a esse excesso de pessoas.',
            style_corpo
        ),

        # Paragraph(
        #     f'<font name="ArialBold">Cláusula 17ª.</font> Fica a critério da CONTRATADA subcontratar serviços previstos neste instrumento sem a devida e expressa autorização da CONTRATANTE.',
        #     style_corpo
        # ),

        Paragraph(
            f'<font name="ArialBold">Cláusula 17ª.</font> O CONTRATANTE [AUTORIZA / NÃO AUTORIZA] o uso de imagens do evento, para divulgação em site, mostruários, portfólios e anúncios comerciais, respeitando-se a integridade e a moralidade do CONTRATANTE.<br/><br/>'

            f'({"X" if VALORES["autorizaImagem"] else "  "}) Sim, autorizo a divulgação de imagem<br/>'
            f'({"X" if not VALORES["autorizaImagem"] else "  "}) Não autorizo a divulgação de imagem<br/><br/>'
            f'Fotos e Filmagens por conta do cliente, mas a empresa passará o contato se houver interesse.',
            style_corpo
        ),

        Paragraph(
            '<font name="ArialBold">Cláusula 18ª.</font> Qualquer alteração, modificação, complementação, ou ajuste, somente será reconhecido e produzirá efeitos legais, se incorporado ao presente contrato mediante Termo Aditivo, devidamente assinado pelas partes contratantes',
            style_corpo
        ),

        Paragraph(
            '<font name="ArialBold">DO FORO</font><br/><br/>'

            f'Para dirimir quaisquer controvérsias oriundas do presente contrato, as partes elegem o foro da comarca da cidade de {preencher(10, VALORES["cidadeForo"])}; Por estarem assim justos e contratados, firmam o presente instrumento.',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Contratante:</font><br/>Nome: {preencher(60, VALORES["nomeContratante"])}<br/>Assinatura:{preencher(60, "")}',
            style_corpo
        ),

        Paragraph(
            f'<font name="ArialBold">Contratada:</font><br/>Nome: {preencher(60, VALORES["nomeContratada"])}<br/>Assinatura: {preencher(60, "")}',
            style_corpo
        ),

        Paragraph(
            f'{preencher(20, VALORES["cidadeForo"])}, {preencher(2, _valor(VALORES, "dataFinalDia", antigas=["diaDataFinal"]))} de {preencher(15, _valor(VALORES, "dataFinalMesExtenso", antigas=["mesDataFinalExtenso"]))} de 202{preencher(1, _valor(VALORES, "dataFinalAnoUltimoDigito", antigas=["anoDataFinalUltimoDigito"]))}.',
            style_corpo_centro
        ),
    ]

    if img_path:
        PARAGRAPHOS.extend([
            PageBreak(),
            Paragraph(
                "Anexo contendo as especificações sobre o tipo e a quantidade de alimentos que serão fornecidos no evento, de acordo com o disposto na 7ª Cláusula.",
                style_corpo
            ),
            Image(img_path, width=350, height=600, hAlign='CENTER')
        ])

    return PARAGRAPHOS

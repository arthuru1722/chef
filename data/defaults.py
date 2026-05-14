CONTRATANTE_DEFAULTS = {
    "nomeContratante": "",
    "nacionalidadeContratante": "",
    "estadoCivilContratante": "",
    "profissaoContratante": "",
    "rgContratante": "",
    "cpfContratante": "",
    "ruaContratante": "",
    "numeroContratante": "",
    "bairroContratante": "",
    "cepContratante": "",
    "cidadeContratante": "",
    "estadoContratante": "",
}

CONTRATADA_DEFAULTS = {
    "nomeContratada": "Ivanilda Caetano da Silva Santos",
    "cnpjContratada": "62.114.618/0001-30",
    "ruaContratada": "Alameda Euridice Placido de Araujo Ivo",
    "numeroContratada": "15",
    "bairroContratada": "J. Petropolis II",
    "cepContratada": "57062-090",
    "cidadeContratada": "Maceió",
    "estadoContratada": "AL",
}

EVENTO_DEFAULTS = {
    "diaEvento": "",
    "mesEvento": "",
    "anoEvento": "",
    "horaEvento": "",
    "minutoEvento": "",
    "ruaEvento": "",
    "numeroEvento": "",
    "bairroEvento": "",
    "cepEvento": "",
    "cidadeEvento": "",
    "estadoEvento": "",
    "tipoEvento": "",
    "qtdPessoas": "",
}

SERVICO_DEFAULTS = {
    "inicioHora": "",
    "inicioMinuto": "",
    "terminoHora": "",
    "terminoMinuto": "",
    "chegadaHora": "",
    "chegadaMinuto": "",
    "antecedenciaHoras": "",
    "qtdGarcons": "",
    "qtdCopeiros": "",
    "materiais": [
        {"nome": "", "custo": ""},
        {"nome": "", "custo": ""},
        {"nome": "", "custo": ""},
    ],
}

PAGAMENTO_DEFAULTS = {
    "valorTotalNumero": "",
    "valorTotalExtenso": "",
    "tipoPagamento": "",
    "parcela1Numero": "",
    "parcela1Extenso": "",
    "parcela1Dia": "",
    "parcela1Mes": "",
    "parcela1Ano": "",
    "parcela2Numero": "",
    "parcela2Extenso": "",
    "parcela2Dia": "",
    "parcela2Mes": "",
    "parcela2Ano": "",
    "antecedenciaCredito": "30",
    "antecedenciaDesistencia": "30",
    "valorExtraNumero": "",
}

FINALIZACAO_DEFAULTS = {
    "autorizaImagem": True,
    "cidadeForo": "Maceió",
    "dataFinalDia": "",
    "dataFinalMesExtenso": "",
    "dataFinalAnoUltimoDigito": "",
    "festaRealizada": False,
    "parcela1Paga": False,
    "parcela2Paga": False,
}


DEFAULT_VALUES = {
    **CONTRATANTE_DEFAULTS,
    **CONTRATADA_DEFAULTS,
    **EVENTO_DEFAULTS,
    **SERVICO_DEFAULTS,
    **PAGAMENTO_DEFAULTS,
    **FINALIZACAO_DEFAULTS,
}


def normalize_old_keys(values):
    aliases = {
        "diaDataFinal": "dataFinalDia",
        "mesDataFinalExtenso": "dataFinalMesExtenso",
        "anoDataFinalUltimoDigito": "dataFinalAnoUltimoDigito",
    }
    for old_key, new_key in aliases.items():
        if new_key not in values and old_key in values:
            values[new_key] = values[old_key]
    return values

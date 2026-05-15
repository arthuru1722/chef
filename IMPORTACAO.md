# Importacao Por CSV/Excel

Baixe o modelo pela lateral do site em **Importar planilha > Baixar modelo**.

Cada linha da planilha vira um contrato. Use preferencialmente CSV, que e o formato mais previsivel para esse fluxo.

## Campos Aceitos

Estes sao todos os campos que podem ser preenchidos pela importacao.

### Contratante

```text
nomeContratante
nacionalidadeContratante
estadoCivilContratante
profissaoContratante
rgContratante
cpfContratante
ruaContratante
numeroContratante
bairroContratante
cepContratante
cidadeContratante
estadoContratante
```

### Evento

```text
diaEvento
mesEvento
anoEvento
horaEvento
minutoEvento
ruaEvento
numeroEvento
bairroEvento
cepEvento
cidadeEvento
estadoEvento
tipoEvento
qtdPessoas
```

### Servico

```text
inicioHora
inicioMinuto
terminoHora
terminoMinuto
chegadaHora
chegadaMinuto
antecedenciaHoras
qtdGarcons
qtdCopeiros
```

### Materiais

```text
material1Nome
material1Custo
material2Nome
material2Custo
material3Nome
material3Custo
material4Nome
material4Custo
material5Nome
material5Custo
material6Nome
material6Custo
material7Nome
material7Custo
material8Nome
material8Custo
material9Nome
material9Custo
material10Nome
material10Custo
```

### Pagamento

```text
valorTotalNumero
valorTotalExtenso
tipoPagamento
parcela1Numero
parcela1Extenso
parcela1Dia
parcela1Mes
parcela1Ano
parcela2Numero
parcela2Extenso
parcela2Dia
parcela2Mes
parcela2Ano
valorExtraNumero
```

### Finalizacao

```text
dataFinalDia
dataFinalMesExtenso
dataFinalAnoUltimoDigito
```

## Atalhos Aceitos

Voce tambem pode usar estas colunas no lugar dos campos separados:

```text
dataEvento
horaEvento
dataParcela1
dataParcela2
dataAssinatura
```

Exemplo:

```text
dataEvento = 20/06/2026 18:30
dataParcela1 = 01/06/2026
dataParcela2 = 10/06/2026
dataAssinatura = 15/05/2026
```

## Campos Preenchidos Por Padrao

Estes campos existem no sistema, mas nao precisam estar na planilha porque ja vem preenchidos:

```text
nomeContratada
cnpjContratada
ruaContratada
numeroContratada
bairroContratada
cepContratada
cidadeContratada
estadoContratada
antecedenciaCredito
antecedenciaDesistencia
autorizaImagem
cidadeForo
festaRealizada
parcela1Paga
parcela2Paga
```

## Data Da Assinatura

A lista de contratos do site e ordenada pela data de assinatura:

```text
dataFinalDia
dataFinalMesExtenso
dataFinalAnoUltimoDigito
```

O mes pode ser escrito por extenso. O sistema entende acentos e alguns erros comuns:

```text
janeiro
fevereiro
março
marco
abril
maio
junho
julho
agosto
setembro
setempo
outubro
novembro
dezembro
```

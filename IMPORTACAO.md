# Importacao Por Excel

Baixe o modelo pela lateral do site em **Baixar modelo**.

O modelo traz todas as colunas que podem ser preenchidas pela importacao, exceto campos que o sistema ja preenche por padrao, como dados da contratada, foro e regras padrao.

Cada linha da planilha vira um contrato.

## Campos

Use preferencialmente os nomes exatos do modelo, por exemplo:

```text
nomeContratante
nacionalidadeContratante
diaEvento
mesEvento
anoEvento
horaEvento
minutoEvento
parcela1Dia
parcela1Mes
parcela1Ano
dataFinalDia
dataFinalMesExtenso
dataFinalAnoUltimoDigito
material1Nome
material1Custo
```

Tambem existem alguns atalhos aceitos:

```text
dataEvento
horaEvento
dataParcela1
dataParcela2
dataAssinatura
```

## Data da Assinatura

A lista de contratos do site agora e ordenada pela data de assinatura:

```text
dataFinalDia
dataFinalMesExtenso
dataFinalAnoUltimoDigito
```

O mes pode ser escrito por extenso. O sistema entende acentos e alguns erros comuns:

```text
março
marco
setembro
setempo
fevereiro
abril
maio
```

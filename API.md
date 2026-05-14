# API Cheffy

Todas as rotas retornam JSON e ficam em `/api`.

Se a variavel de ambiente `CHEFFY_API_TOKEN` estiver definida, envie:

```http
Authorization: Bearer seu-token
```

## Contratos

`GET /api/contracts`

Lista informacoes basicas para tela inicial.

Query opcional:

- `include_done=0`: esconde festas ja realizadas.

`GET /api/contracts/<id>`

Retorna o resumo e os dados completos do contrato.

## Evento

`GET /api/contracts/<id>/event-time`

Retorna data/hora do evento, segundos ate o evento e se a festa ja foi realizada.

`PATCH /api/contracts/<id>/event/done`

Marca a festa como realizada ou nao realizada.

```json
{"realizada": true}
```

## Pagamentos

`GET /api/contracts/<id>/payments/1`

Retorna data, valor e status de pagamento da primeira parcela.

`GET /api/contracts/<id>/payments/2`

Retorna data, valor e status de pagamento da segunda parcela.

`PATCH /api/contracts/<id>/payments/1/paid`

Marca a primeira parcela como paga ou nao paga.

```json
{"paga": true}
```

`PATCH /api/contracts/<id>/payments/2/paid`

Marca a segunda parcela como paga ou nao paga.

```json
{"paga": true}
```

## Status Geral

`PATCH /api/contracts/<id>/status`

Atualiza varios marcadores de uma vez.

```json
{
  "festaRealizada": true,
  "parcela1Paga": true,
  "parcela2Paga": false
}
```

## Notificacoes

`GET /api/notifications?days=7`

Retorna eventos proximos e pagamentos pendentes dentro da janela informada.

Essa rota nao envia push sozinha. Ela foi feita para um app, tela inicial ou automacao consultar de tempos em tempos.

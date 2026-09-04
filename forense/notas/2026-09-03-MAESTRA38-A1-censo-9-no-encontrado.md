# MAESTRA38-A1 · Censo de cierre — 9 reglas NO-ENCONTRADO contra los FD nuevos

Al cierre del acto, per encargo: "/mapea de las 9 reglas NO-ENCONTRADO
contra los FD nuevos indexados, sólo como censo — cero veredictos de
regla, eso es sucesor." Esto es exactamente eso: cuenta candidatas, no
las clasifica ni las cierra.

Universo examinado (A.13): `--tablas descargas_mx` →
`data/inventario-reactivos-descargas-mx-v1_0.tsv` (recién regenerado por
este acto sobre TODO `descargas_mx`, incluida la subcarpeta
`UNIVERSO-2026-09/` de los 20 payloads nuevos) — 28948 filas examinadas
por corrida. 27 corridas (9 reglas × 3 formulaciones), comando exacto de
cada una es `python3 tools/busca_reactivos.py [...] --tablas descargas_mx`.

## Resultado — 8 de 9 en cero, 1 con señal adyacente

| regla | candidatas | nota |
|---|---|---|
| `tramite.evasion.norma_inutil_sancion_improbable` | 0/0/0 | ya tiene A.4 directo por lectura completa del FD de ENCRIGE en Lote 1 (`EXISTE-NO-SATISFACE`) — el censo por palabra clave no encuentra nada adicional, consistente |
| `dinero.ahorro.seguro_deposito_atenua_aversion` | 0/0/0 | — |
| `dinero.credito.scoring_alternativo` | 0/0/0 | — |
| `dinero.credito.baja_friccion_usura_dano_downstream` (N34) | 0/**16**/0 | la formulación "cobranza" trae 16 candidatas, **todas** de la misma tabla: ENCRIGE 2020, `I_Cumplimiento_de_contratos_2020` — "Problemas de cobranza o contratos" es un ítem de **la empresa como acreedora** (dificultad para cobrar), no del consumidor como deudor sujeto a cobranza agresiva/BNPL que la regla nombra. Señal adyacente, no cierre — declarada para que el sucesor decida si vale la pena leer el FD completo |
| `civico.voto.agencia_con_secreto` | 0/0/0 | — |
| `civico.voto.clientelar_si_observable` | 0/0/0 | — |
| `civico.transferencia.atribucion_lider` | 0/0/0 | — |
| `civico.protesta.agravio_urbano` | 0/0/0 | — |
| `familia.cortejo.urbano_joven_apps` | 0/0/0 | — |

## Lectura

Los 12 payloads de este acto se eligieron por dominio público, no por
calce con estas 9 reglas específicas (la conexión real que este acto sí
encontró y registró por §32 es N15/N16/N18/N35, distinta de esta lista) —
el censo confirma que ninguna de las 9 se cierra de rebote. La única
señal (N34/cobranza) es del lado equivocado de la transacción
(acreedor-empresa, no deudor-consumidor) y se deja explícitamente para
que un acto sucesor decida si merece lectura completa del FD.

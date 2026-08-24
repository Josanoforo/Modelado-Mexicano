# PROPUESTA·PARCIAL — Especificación operativa coerción/adopción (v0.1)

*(`ACTO EMISOR-M-2`, 24/ago/2026. Fuente: `COERCION-Y-ADOPCION-rediseno-2026-08-20.md` §4, §6 — documento de mesa, **no commiteado**. Este acto no lo tiene adjunto; por `transfer §9` NO se reconstruye. Lo que sigue es solo el bloque operativo que dirección pegó inline en el encargo `2026-08-24-EMISOR-M-2.md`, copiado aquí verbatim. Rotulado `PROPUESTA·PARCIAL` porque es un fragmento, no el documento íntegro — ver la fila de tablero al final pidiendo a mesa el documento completo.)*

## Objeto

Hoy el motor funde en una sola conducta dos que la literatura y mesa separan: cumplir bajo mandato y adoptar por elección. `ACTO EMISOR-M-2` da al emisor las dos variables dependientes y los disparadores por componente para que ninguna celda futura pueda medir una diciendo que mide la otra.

## Variables dependientes (2)

- **`cumplimiento`** — conducta bajo mandato con sanción.
- **`adopcion`** — conducta de elección.

Toda celda-D del dominio tecnología/pagos/registros declara cuál mide; el emisor se niega ante una celda sin DV declarada (implementado en `milpa/src/emisor.py`, `valida_dv_celda_m2`).

## Disparadores por componente (6)

- `riesgo_fiscal_percibido` — booleano. **Existe** (Nota 3 de R3.4 / emisor); no se re-crea, se integra.
- `friccion_uso` — booleano.
- `utilidad_marginal_sobre_sustituto` — booleano.
- `lado_obligado` ∈ {`ninguno`, `oferta`, `usuario`}.
- `sancion` ∈ {`ninguna`, `suspension`, `bloqueo`}.
- `dato_sensible` ∈ {`no`, `identificador`, `biometrico`}.

## Tabla de casos — HIPÓTESIS DE CLASIFICACIÓN

*(Cada celda es una hipótesis a verificar contra fuente primaria en un acto futuro CON red; este acto no abre red y no afirma ninguna cifra.)*

| caso | coerción | sanción | dato_sensible | sustituto previo | lado_obligado | desenlace (hipótesis) |
|---|---|---|---|---|---|---|
| SPEI (2004–) | no | — | no | — (incumbente) | — | adoptado ampliamente |
| CoDi (2019–) | no | — | no | SPEI, fuerte | ninguno efectivo | validadas ≫ activas |
| DiMo (2023–) | no | — | no | SPEI/CoDi | — | adopción parcial |
| OXXO Pay / Spin | no | — | no | efectivo (integra) | — | adopción amplia |
| RENAUT (2008) | sí | suspensión | identificador | — | usuario | base vulnerada; suspendido |
| PANAUT (2021) | sí | suspensión | biométrico | — | usuario | anulado (SCJN) antes de operar |
| Registro 2026 | sí | bloqueo | identificador (sin biométricos) | — | usuario | EN CURSO — caso registrado; pre-registro DECLINADO por mesa 24/ago (`D4`, `ADR-145`) |
| Pix (Brasil) | sí | — | no | — | bancos/oferta | adopción masiva |

**Discrepancia CoDi conocida, no resuelta aquí** (sin red): `tramite.yaml:61` dice 3.09M cuentas backtest vs. el report de `corpus/reports/...:64` da 21.8M cuentas vs. Banxico >20M. Ya vive en `forense/hitoD-preregistro-v2_0.md`, sección "Discrepancia numérica encontrada al verificar la ancla" (≈línea 810, ficha de R3.4) — se cita, no se recorre aquí.

Pares de una sola variable, que consumirá la condición A re-especificada de `R3.4` (sucesor de este acto, no ejecutado aquí): PANAUT ↔ Registro-2026 (`dato_sensible`) · DiMo ↔ CoDi (`friccion_uso`) · Pix ↔ CoDi (`lado_obligado`) · CoDi ↔ SPEI (`utilidad_marginal_sobre_sustituto`).

## Lo que este documento deliberadamente NO tiene

Ninguna cifra de terceros del documento de mesa original — regla del propio documento. No es el `.md` íntegro: es el fragmento inline del encargo, transcrito una sola vez.

---
**Pendiente a mesa (A.12):** el documento íntegro `COERCION-Y-ADOPCION-rediseno-2026-08-20.md` no llegó adjunto a este acto. Fila añadida a `forense/firmas-pendientes.tsv` pidiéndolo — si llega, un acto futuro lo commitea íntegro, byte-idéntico, rotulado `PROPUESTA` (no `PROPUESTA·PARCIAL`), reemplazando este archivo.

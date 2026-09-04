# MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1 — resultados Lote 3 (COMMIT-2)

Spec congelada: `forense/notas/2026-09-03-MAESTRA38-A1-spec-lote-3.md`. Intercensal 2015 · CSES · Reuters DNR ·
Pew. Último lote del acto.

## (a)+(b)+(c) Resultado por candidata

| candidata | ruta verificada | resultado |
|---|---|---|
| Intercensal 2015 | pública, sin cuenta | **OBTENIDO** — muestra nacional (TR_PERSONA15 514 MB, TR_VIVIENDA15 120 MB descomprimidos) + FD (.xls), doble descarga hash-verificada, `testzip` OK. Descubierta vía `pestanaData.js`→`idBiinegi=1714`→API `descargamasiva` (mismo mecanismo de Lote 1/2, sin necesitar sub-agente) |
| CSES | cuenta | **PENDIENTE** — `cses.org/data-download/` exige registro gratuito, verificado sin enlace directo en el HTML servido (sólo el texto "Register") |
| Reuters DNR | solicitud | **PENDIENTE** — confirmado por fuente pública: microdato "available to academic or industry researchers on request"; sólo agregados de descarga libre |
| Pew (microdato) | cuenta | **PENDIENTE** — topline ya `OBTENIDO` desde antes de este acto (FP-29); microdato exige cuenta gratuita en pewresearch.org, verificado |

Las tres `PENDIENTE` tienen receta ≤1 minuto en
`forense/notas/2026-09-03-MAESTRA38-A1-PAQUETE-RECETAS-4.md`, firma
FP-291. Ninguna se rodeó (sin credenciales de terceros, sin scraping
autenticado) — se declara la cuenta/solicitud como lo que es, no se evita.

## Corrección de premisa — Pew, cerrada

El encargo afirmaba SIN-FETCH para las 12; para Pew era parcialmente falso
(declarado en `forense/notas/2026-09-03-MAESTRA38-A1-spec-lote-1.md` y reafirmado en `forense/notas/2026-09-03-MAESTRA38-A1-spec-lote-3.md`). Cerrado
aquí: fila `PEW_GLOBAL_ATTITUDES_MEXICO` en la cola cita ambos ids
existentes (`pew_gas2025_social_trust_topline`/`_shortread`, ya
`OBTENIDO`) y declara que sólo el microdato individual queda pendiente,
sin duplicar ni re-registrar el topline.

## Registro por las tres capas

- **Manifiesto**: 1251 → 1253 (+2: microdato nacional + FD de Intercensal
  2015; las tres `PENDIENTE` no generan entrada de manifiesto — no hay
  payload que hashear).
- **Cola**: 120 → 124 filas (+4: 1 `OBTENIDO`, 3 `PENDIENTE`). Vista
  regenerada (124 filas).
- **Alta GUÍA §32**: ninguna — las cuatro son exploratorias (Intercensal)
  o no llegaron a leer contenido (las tres `PENDIENTE`); no hay FD abierto
  que produzca un veredicto A.4 que registrar como relación.

## Anti-PR#77

Los 2 payloads de Intercensal 2015 en
`descargas_mx/UNIVERSO-2026-09/INTERCENSAL2015/`, fuera del worktree —
verificado.

## Contador movido por este lote

Candidatas sondeadas: 8 → 12 (las 12 completas). Veredictos A.4 con FD:
5 → 5 (Intercensal/CSES/Reuters/Pew no producen veredicto de regla — tres
por PENDIENTE, una por exploratoria). Payloads: +2 (total +20 en el acto).
Fuentes en cola: +4 (total +12). Relaciones nuevas: +0 (total +3 en el
acto, sin cambio este lote).

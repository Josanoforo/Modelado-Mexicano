# MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1 — resultados Lote 2 (COMMIT-2)

Spec congelada: `forense/notas/2026-09-03-MAESTRA38-A1-spec-lote-2.md`. CONEVAL, ENJUVE, ENVE, ENH.

*(Corrección aritmética 3/sep/2026: los totales de manifiesto de esta nota
usaban la base `1242` de la redacción original de
`forense/notas/2026-09-03-MAESTRA38-A1-resultados-lote-1.md`, que no
incluía las 3 entradas que el sub-agente resolvió después. Base real de
este lote: `1245`. Ver la corrección en esa nota y el recuento final en
`ADR-330` (renumerado desde 328 por colisión real con MAESTRA37-N8 al fusionar origin/main).)*

## (a) Sonda de alcanzabilidad (v2.2) — tres hallazgos distintos, sin colapsar

- **ENVE, ENH** (INEGI): mismo patrón que Lote 1 — portal SPA 200 con
  shell falso; FD real vía catálogo RNM; microdato real vía
  `datosabiertos/` (ENVE) o la API `descargamasiva/lista/archivoscompaginacion`
  con `idBiinegi` leído del sidecar `pestanaData.js` de cada programa (ENH,
  `idBiinegi=2785` → tres tablas vivienda/hogar/persona). Sin necesidad de
  sub-agente esta vez — mecanismo ya conocido de Lote 1.
- **CONEVAL**: portal server-rendered normal (no SPA); enlace real
  encontrado en la página de "versión completa" (`.rar`, 130 MB). El
  servidor **no honra `Range` requests** (un `curl -r 0-5` devolvió el
  archivo completo, no un fragmento) — advertencia operativa para
  cualquier acto futuro que sondee este dominio con un chequeo de firma de
  bytes por rango.
- **ENJUVE**: **hallazgo genuino, no artefacto de sonda.** La página oficial
  vigente (`gob.mx/imjuve/...`) responde 200 y su título promete "base de
  datos", pero sólo lista tres PDF de cuestionario — 2 de 3 dan **HTTP 404
  real** (verificado con `curl -v -L`, cabecera y cuerpo confirman error de
  `gob.mx`, no shell de INEGI). Ningún enlace a microdato en esa página. El
  host histórico de microdatos (`bdsocial.inmujeres.gob.mx`) da **502 Bad
  Gateway** (verificado con `curl -v`) — **NO ALCANZABLE**, distinto de
  "sin el dato". Ambos hechos se declaran por separado, sin colapsar
  (`ADR` v2.2/v2.4): la fuente vigente **responde pero no tiene el enlace**;
  la fuente histórica **no responde**.

## (b)+(c) Veredictos A.4

| candidata | FD | microdato | A.4 |
|---|---|---|---|
| ENVE | 2 PDF reales | zip real, 413 archivos, testzip OK | `EXISTE-NO-SATISFACE` para N16 (tramite.mordida.*) — Sección VII identifica incidencia y tipo de funcionario en corrupción a nivel empresa; no distingue discrecional vs con-registro (sin ítem de recibo). Refuerza el hallazgo de ENCUCI2020, no lo cierra |
| ENH | 1 PDF real | 3 zips reales (vivienda/hogar/persona), testzip OK | sin regla que cerrar (exploratoria); registrada por cobertura |
| CONEVAL | — (no aplica, es indicador no encuesta) | 1 RAR real, 130 MB, listable (`tar.exe` de Windows — no hay `unrar`/`7z` nativo en esta caja Linux), contiene `pobreza_20.dta` (indicador municipal 2020) + insumos de contexto (accesibilidad, elecciones, incidencia delictiva, bancos) | sin regla que cerrar (exploratoria); valor potencial para cruces municipales de actos futuros |
| ENJUVE | 1 PDF real de 3 (2 rotos) | **no obtenido** | `OBTENIDO-PARCIAL`; SIN-EL-DATO en la fuente vigente, NO-ALCANZABLE en la histórica |

## Registro por las tres capas

- **Manifiesto**: 1245 → 1254 (+9: 3 ENVE, 4 ENH, 1 CONEVAL, 1 ENJUVE).
  Doble descarga + hash coincidente + integridad verificada (`testzip` para
  zips, `tar.exe -tf` para el RAR) en los 8 payloads de dato; el PDF de
  ENJUVE con hash único (no token).
- **Cola**: 116 → 120 filas. ENVE y ENH `OBTENIDO`; CONEVAL `OBTENIDO`
  (aunque exploratoria, el archivo llegó completo); ENJUVE
  `OBTENIDO-PARCIAL` con receta para mesa (solicitar a IMJUVE/INMUJERES vía
  laboratorio de microdatos, o verificar depósito espejo en ICPSR/GESIS).
  Vista regenerada (120 filas).
- **Alta GUÍA §32**: sólo ENVE → N16 (`CANDIDATA`, `EXISTE-NO-SATISFACE`).
  ENH/CONEVAL/ENJUVE quedan fuera — ninguna tiene regla/necesidad
  hipotetizada que cerrar (criterio de COMMIT-1: cobertura no es cierre).
  `relaciones.tsv` 221→222, `evidencias.tsv` 222→223, `utilidad-modelo.tsv`
  221→222, `aliases-fuentes.tsv` 17→18. `baseline.py` **VERDE**.

## Anti-PR#77

Los 9 payloads nuevos en `descargas_mx/UNIVERSO-2026-09/<fuente>/`, fuera
del worktree — verificado.

## Contador movido por este lote

Candidatas sondeadas: 4 → 8 (de 12). Veredictos A.4 con FD: 4 → 5 (ENH,
CONEVAL, ENJUVE no producen veredicto de regla — exploratorias). Payloads:
+9 (total +21 en el acto). Fuentes en cola: +4 (total +8). Relaciones
nuevas: +1 (total +3 en el acto). Reglas NO-ENCONTRADO con candidata:
8 → 8 (N16 ya tenía candidata vía ENCUCI2020 — ENVE la refuerza, no abre
una regla nueva).

# DUELO-ENVIPE2026-MARGINALES · spec v1.0 · piso 2025 contra TENDENCIA-SERIE

ACTO `GEN2-DUELO-ENVIPE2026-MARGINALES-2` (22/sep/2026, CAJA). Encargo
archivado por A.3 en `forense/encargos/2026-09-22-GEN2-DUELO-ENVIPE2026-MARGINALES-2.md`
(sello de cuerpo `eaf54ead…`). CALC: `CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001`
(COMMIT-2) y `CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001` (COMMIT-3a/3).
Sucesor de `GEN2-DUELO-ENVIPE2026-EJECUCION-1` (`#1010`, ADR raíz `f57b`) para
lo que FP-`260921-GEN2-ENCIG-SERIE-Y-TENDENCIA-1-852f-01` (b) mandó al
«siguiente duelo»: TENDENCIA-SERIE entra como RETADOR.

## 0 · Universo — verificado contra el árbol, no supuesto del encargo

El encargo (§1) proponía nueve celdas (`con_seguro` × {nacional, sexo×2,
edad×4, cobertura_seguro×2} + «demás reglas ENVIPE con serie sellada»). La
verificación de premisas (v2.16 §2, `[SUPUESTO]` sin rótulo explícito en el
encargo) encontró un universo real mucho más chico:

1. **`civico.denuncia.con_seguro` no tiene eje sexo ni eje edad en ningún
   archivo del repo.** `milpa/tramite-ola5-propuesta-v0.yaml:1993-2033`
   (`civico.denuncia.con_seguro_ejes_envipe2025`) declara `ejes_ausentes:
   "ninguno adicional propuesto"` y trae un solo eje (`cobertura_seguro`).
   `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001/resultados.json` (116 RESULT)
   confirma: existen `DENUNCIA-COBERTURA-SEGURO-{ASEGURADO,NO-ASEGURADO}` y
   `DENUNCIA-TOTAL-TODOS`; no existe ninguna llave `DENUNCIA-SEXO-*` ni
   `DENUNCIA-EDAD-*` (a diferencia de `EVASION-*`, que sí las trae). →
   `civico.denuncia.con_seguro × sexo` y `× edad`: **NO-CONSTRUIBLE** — el
   piso mismo no existe, no sólo el retador.
2. **«Las demás reglas ENVIPE con serie sellada (`CALC-ENVIPE-SERIE-*`)»
   resuelve a CERO reglas adicionales.** `ls data/corrida0/CALC-ENVIPE-SERIE-*`
   da ocho directorios, los ocho de una sola serie: `p(C1,U1)` = proporción
   de delitos personales no denunciados por miedo/desconfianza (`no-denunciado`,
   `ENVIPE-SERIE-COMPLETA-spec-v1_0.md §1`), 2011→2022 por esa familia de
   CALC y 2023→2025 por `CALC-R-CIV-M-12/13` y `CALC-ENVIPE-0001`
   (`data/corrida0/envipe-serie-denuncia-v1_0.tsv`, columna `calc_id`). Es
   exactamente `p_c1_u1` **nacional**, y `data/corrida0/decisiones.tsv`
   fila `reserva:envipe2026-consumida-por-duelo` ya lo adjudicó por
   completo en `GEN2-DUELO-ENVIPE2026-EJECUCION-1` COMMIT-3
   (`CALC-DUELO-ENVIPE2026-ADJUDICACION-0001`, RESULT `R nacional
   no-denunciado (p_c1_u1)…`). No hay una segunda regla con ese patrón de
   nombre. → **Ninguna.**
3. **`civico.denuncia.con_seguro` nacional (total) tiene un solo punto
   sellado (2025).** `CALC-PISOS-ENVIPE2024-EJES-0002/resultados.json`
   trae `DENUNCIA-COBERTURA-SEGURO-{ASEGURADO,NO-ASEGURADO}` para 2024 pero
   **no** trae `DENUNCIA-TOTAL-TODOS` — el módulo del piso 2024 nunca
   computó el nacional para esta regla. TENDENCIA-SERIE exige ≥ 2 olas
   (`tools/duelo/tendencia_serie.py`). → `civico.denuncia.con_seguro`
   **nacional**: piso 2025 existe y se cita (§1), pero el retador es
   **NO-CONSTRUIBLE** — sin retador no hay duelo que adjudicar para esa
   celda.
4. **`civico.denuncia.con_seguro × cobertura_seguro` (asegurado / no
   asegurado) tiene exactamente 2 olas selladas** (2024, 2025) para cada
   celda — el mínimo exacto que exige TENDENCIA-SERIE. Son las **únicas
   dos celdas de este acto con duelo real**.

**Universo final: 2 celdas construibles** (`con_seguro×asegurado`,
`con_seguro×no_asegurado`); 3 declaraciones `NO-CONSTRUIBLE`
(`×nacional`, `×sexo`, `×edad`); 0 reglas adicionales de
`CALC-ENVIPE-SERIE-*`. Esto es hallazgo de este acto, no ajuste del
procedimiento: el estimando y el criterio de abajo no cambian, sólo el
universo al que se aplican — v2.16 §2, "encontrar un encargo mal fundado
es entregable".

## 1 · Pisos t−1 (sellados, verbatim)

| celda | RESULT (ola 2025, árbitro) | p | ic95 | n |
|---|---|---:|---|---:|
| asegurado | `RESULT-ARBITRO-ENVIPE2025-DENUNCIA-COBERTURA-SEGURO-ASEGURADO-{P,IC-LO,IC-HI,N}` | 0.7909064453831163 | [0.7416015684811433, 0.8373260492789095] | 402 |
| no_asegurado | `RESULT-ARBITRO-ENVIPE2025-DENUNCIA-COBERTURA-SEGURO-NO-ASEGURADO-{P,IC-LO,IC-HI,N}` | 0.6720144369290082 | [0.628703882046181, 0.7139265288703556] | 614 |
| nacional (sin duelo, §0.3) | `RESULT-ARBITRO-ENVIPE2025-DENUNCIA-TOTAL-TODOS-{P,IC-LO,IC-HI,N}` | 0.7239309870788496 | [0.6906923371856304, 0.7563228266804197] | 1016 |

Fuente: `data/corrida0/CALC-ARBITRO-MARGINALES-ENVIPE2025-0001/resultados.json`
(sha256 `732567d2c2…`), sellado por `ACTO GEN2-ARBITRO-MARGINALES-1`
(`forense/prereg-caja/ARBITRO-MARGINALES-ENVIPE2025-spec-v1_0.md`). Ningún
número se retipea a mano en el medidor: se lee del JSON por llave.

## 2 · Retador — TENDENCIA-SERIE

`tools/duelo/tendencia_serie.py::tendencia_serie(olas, objetivo)` (extraído
de `tools/encig_origen_movil.py`, §6 del encargo, decisión de mesa 22/sep:
extraer, no citar). Mínimos cuadrados en logit sobre **todas** las olas
sealed anteriores a la ola objetivo (aquí: exactamente 2 — 2024 y 2025 —
para cada una de las 2 celdas construibles); sin parámetro elegible.
Incertidumbre por el mismo método delta que `encig_origen_movil.py`: EE en
logit desde el IC95 sellado de cada ola, olas independientes,
`var(L̂) = Σ w_i² EE_i²`.

| celda | ola 2024 (piso módulo) | ola 2025 (árbitro) |
|---|---|---|
| asegurado | `RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-ASEGURADO-{P,IC-LO,IC-HI}` = 0.7740559546028694, [0.7108346601907894, 0.8330591470908341] | ver §1 |
| no_asegurado | `RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-NO-ASEGURADO-{P,IC-LO,IC-HI}` = 0.6335238483178248, [0.5849432161458518, 0.6817866400934546] | ver §1 |

Fuente 2024: `data/corrida0/CALC-PISOS-ENVIPE2024-EJES-0002/resultados.json`
(sha256 `a898a3cccf…`), sellado por `ACTO GEN2-...` (piso de persistencia
por eje, v2 — citado por objeto, no por nombre de acto: el archivo trae su
propio `sello.json`). Con exactamente 2 puntos, TENDENCIA-SERIE es
matemáticamente una recta por los dos puntos en logit extrapolada a 2026
— coincide con lo que `TENDENCIA-2` habría dado si esa variante existiera
aquí; se reporta bajo el nombre `TENDENCIA-SERIE` porque es el nombre que
FP-852f fija para el retador de este duelo, no porque haya más de dos
olas.

**Verificación por texto, FD 2026 (`[SUPUESTO]` del encargo §3,
EJECUTADO).** `pdftotext -layout` de `fd_envipe2026.pdf`
(sha256 `4a076ce356…`, manifiesto) contra `fd_envipe2025.pdf`
(sha256 no citado por el encargo, leído de `data/manifiesto.yaml`):
`BPCOD='01'` («Robo total de vehículo»), `BP1_20` («¿Acudió ante el
Ministerio Público…?», códigos 1/2) y `BP2_1` («¿El vehículo robado estaba
asegurado?», códigos 1/2/9/b) tienen **texto de pregunta y catálogo de
respuesta idénticos** entre 2025 y 2026 — sólo cambia el número de columna
consecutivo (`BP1_20`: col. 62→64; `BP2_1`: col. 103→110), que no afecta a
un medidor que lee por nombre de variable, no por posición. `[SUPUESTO]`
se sostiene: ninguna celda cae a `NO-CONSTRUIBLE` por este motivo.

## 3 · Criterio de adjudicación (COMMIT-3, congelado aquí, ejecutado sólo con firma de mesa §2)

**Vocabulario cerrado** (encargo §1): `VENCE-AL-PISO` ·
`PROPUESTA-CON-RESERVA` · `NO-VENCE` · `C-PISO-ADOPTADO`. Ninguna otra
palabra adjudica una celda construible; `NO-CONSTRUIBLE` no es parte de
este vocabulario — es lo que se declara cuando no hay comparación que hacer
(§0).

**Comparación primaria** (v2.16 §4, «diferencia de error medio con IC por
réplica»), aplicada por celda (n = 2 celdas, no hay agregación entre
ellas: cada una tiene su propio universo de réplicas — 10 000, semilla
`numpy.PCG64(42)`, mismo generador que `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001`
y `CALC-ARBITRO-PERSISTENCIA-ERROR-0001`, réplicas de UPM estratificado
sobre `EST_DIS`/`UPM_DIS` de `envipe2026_csv`, `tmod_vic`, universo
`BPCOD='01' ∧ BP1_20∈{1,2} ∧ BP2_1∈{1,2}`):

`ΔMAE_k = |piso_k − R_k| − |retador_k − R_k|` en pp, réplica k comparte el
sorteo de `R_k` entre piso y retador (mismo bootstrap de la celda); IC95 =
percentiles 2.5/97.5 de `{ΔMAE_k}`. Umbral: **0.5 pp**, heredado —no
inventado aquí— de la enmienda v0.3 del lote `GEN2-DUELO-ENVIPE2026-*`
(`forense/prereg-caja/DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.md:67`), único
umbral que este programa ya fijó para exactamente esta forma de
comparación piso-vs-retador en una celda ENVIPE; ningún encargo de este
acto ni de mesa fija uno distinto.

- `VENCE-AL-PISO` si `IC95inf(ΔMAE) > 0.5`.
- `PROPUESTA-CON-RESERVA` si `0 < IC95inf(ΔMAE) ≤ 0.5`.
- `NO-VENCE` si el IC95 incluye 0 y `IC95sup ≥ 0` con el retador **no**
  mejor (si el punto favorece al retador pero el IC cruza 0, sigue siendo
  `NO-VENCE`: el piso se sostiene por defecto — v2.16 §4, «un piso no
  vencido es el estimador adjudicado»).
- `C-PISO-ADOPTADO` es el rótulo que se emite cuando, además de
  `NO-VENCE`, el punto central de `ΔMAE` es ≤ 0 (el piso también gana en
  punto, no sólo por defecto de IC) — distingue «no hay evidencia
  suficiente» de «el piso gana claramente». Esta acta **no ejecuta** la
  adopción (encargo §7, PARO c): el rótulo describe el estado de la
  ciencia, no cambia `milpa/`.

**Además, sin colapsar** (diseño §5, heredado): por celda y candidato —
error en pp con signo, `|error|`, R dentro del IC95 del candidato,
punto del candidato dentro del IC95 de R (árbitro). `INDECIDIBLE`
verbatim: una celda cuyo `ΔMAE` no se puede bootstrapear porque
`envipe2026_csv` no trae ninguna fila con `BPCOD='01' ∧ BP2_1∈{1,2}` (soporte
vacío) — declarada así, nunca como `NO-VENCE`.

**Guardián `reservada=True` heredado** (duelo 1, copiado no reinventado):
`tools/celda_d/marginales_reproduccion.py::carga_ola(zip, anio,
reservada=...)`. COMMIT-2 (este spec, EMISIONES) **no abre microdato**:
piso y retador son aritmética sobre RESULT ya sellados (§1, §2). Sólo
`CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001` (COMMIT-3) llama
`carga_ola(envipe2026_csv, 2026, reservada=False)`; cualquier otro punto
del código que abra `envipe2026*` es PARO (g), código congelado no corre.

## 4 · B-bis

El primer resultado que produzca este procedimiento es el que se reporta.

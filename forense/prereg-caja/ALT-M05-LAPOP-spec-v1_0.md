# M05 · LAPOP México 2021 y 2018/19 · justificación de la mordida por sanción creíble, escolaridad y urbano/rural (ACTITUD)

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CALC-ALTERNOS-LOTE-1` (0-bis `795b1053`), filas 13 y 12 de
`canon/mapa-instrumentos-alternos-v1_0.tsv` (`propuesta = CALC-CAJA`). Firma
R07 A1 (b), 28/sep/2026: «M05 se acota a actitud y se encarga CALC-caja sobre
LAPOP 2021 (EXC18 × PR3DNR × escolaridad)». Gobierna dos CALC:
`CALC-ALT-M05-LAPOP2021-0001` (fila 13) y `CALC-ALT-M05-LAPOP2019-0001`
(fila 12, segunda vía del mapa para M05, misma incógnita y mismo rótulo
ACTITUD). Ninguno adopta, ninguno es retador ni lleva θ.

## Qué ya está medido y no se repite (E.5)

`python3 tools/ya_medido.py tramite.evasion_norma` → `MEDIDA-EN:
CALC-EVASION-NORMA-0001-v1_1, tramite-ola5-propuesta-v0.yaml, tramite.yaml`:
esa medida es ENVIPE 2025, unidad delito, conducta (no denuncia). Los pisos
LAPOP sellados (`CALC-LAPOP-PISOS-2019-0001/-0002`, `-2021-0001`) no tocan
`exc18` ni `pr3dnr` (barrido de 2 337 archivos de `data/corrida0` y
`forense/prereg-caja` por `EXC18|exc18|PR3DNR|pr3dnr`: 0 aciertos). Nada de
esto se recalcula aquí.

## Estimando, unidad, escala, universo

- **Unidad:** persona entrevistada del estudio nacional LAPOP de la ola.
- **Escala:** proporción ponderada en [0, 1]; contrastes en diferencia de
  proporciones.
- **Universo por reactivo:** entrevistas con código sustantivo, peso > 0
  finito, estrato y UPM presentes. No sabe / no responde / no aplica (códigos
  extendidos `.a/.b/.c` de Stata, que se leen como vacío) quedan fuera y se
  cuentan (`n_no_respuesta`). Un código fuera de la escala declarada vuelve el
  reactivo `ESCALA-DISCREPANTE` (no se imputa).
- **Estimando principal (2021):** `p(EXC18 = Sí)` nacional, por nivel de
  sanción creíble `PR3DNR`, por escolaridad `edr` y por el cruce
  `PR3DNR × edr`; contraste pre-registrado
  `p(EXC18=Sí | PR3 BAJO) − p(EXC18=Sí | PR3 ALTO)`.
- **Estimando (2018/19):** `p(EXC18 = Sí)` nacional, por escolaridad
  (años `ed` en tres bandas) y por urbano/rural `ur`, y su cruce.
- n mínimo por celda: 30; debajo, `NO-ESTIMABLE` con su n.

## Códigos por texto de pregunta (A.15)

- `exc18` — «¿Cree que como están las cosas a veces se justifica pagar una
  mordida (o soborno)?» (mapa, fila 12; etiqueta del .dta: «Justifica el
  pago de coimas o sobornos»). Válidos `{0 No, 1 Sí}`; evento `{1}`.
- `pr3dnr` (2021) — «¿Qué tan probable sería que alguien en su colonia sea
  castigado por las autoridades por construir o remodelar una vivienda sin
  licencia o permiso?» (mapa, fila 13). Válidos `{1 Nada, 2 Poco, 3 Algo,
  4 Muy probable}`. Grupos: `ALTO = {3, 4}`, `BAJO = {1, 2}`. Además se
  reporta su marginal `p(pr3dnr ∈ {3,4})`.
- `edr` (2021) — «Nivel de educación»: `{0 Ninguna, 1 Primaria}` →
  `BASICA-O-MENOS`; `{2 Secundaria o media superior}` → `MEDIA`;
  `{3 Universitaria/superior}` → `SUPERIOR`.
- `ed` (2018/19) — «Años de educación», 0–18 (`18 = 18+`): `0–6` →
  `HASTA-6`; `7–12` → `7-A-12`; `13–18` → `13-O-MAS`. Bandas fijadas por
  ciclo escolar mexicano (primaria 6, media 12), antes de ver valores.
- `ur` (2018/19) — `{1 Urbano}` / `{2 Rural}`.
- Etiquetas leídas con `pyreadstat.read_dta(..., metadataonly=True)` (sin
  valores): es lectura de ESTRUCTURA, declarada (ADR-46).

## Ponderador y diseño (codebook / metadatos del archivo)

`wt` («Peso de la muestra» 2021; «Peso del país» 2019), estrato `estratopri`
(4 regiones), UPM `upm`. IC95: bootstrap de UPM con reemplazo dentro de
estrato, 2 000 réplicas, semilla PCG64 `20260928`, percentiles 2.5/97.5,
mismas réplicas para todas las celdas y contrastes de un CALC (pareado).
2021 es CATI a celulares (RUPTURA-MODO-POBLACION, dictamen LAPOP de pisos):
2021 y 2019 **no** se comparan como serie.

## Agregador (E.1)

Media ponderada de la indicadora por celda (razón de sumas de `wt`). No hay
agregación entre olas ni entre celdas; cada celda se reporta sola.

## Pre-registro: qué pasa si el falsador no refuta

La regla `tramite.evasion_norma` predice más evasión donde la sanción no es
creíble. En ACTITUD, el contraste `BAJO − ALTO` de 2021:
- IC95 enteramente > 0 → la actitud es **consistente** con la regla; no la
  corrobora como conducta (A1 (b) la acota a actitud) y no adopta nada.
- IC95 que cubre 0, o < 0 → **no corrobora** en actitud; se reporta así, sin
  re-especificar cortes ni buscar otra partición.
Nada de lo anterior mueve el catálogo ni un contador distinto de
`cuenta_gen2`; la lectura la hace mesa.

## Auditoría v2.16

- **Unidad:** persona (actitud declarada), no trámite ni delito.
- **Escala:** proporción; contrastes en puntos de proporción.
- **RETROSPECTIVA:** olas vistas (2018/19, 2021); nada prospectivo.
- **¿Incentivo o psicología?** Mide justificación declarada (psicología /
  norma), no respuesta a un incentivo observado; `pr3dnr` es sanción
  percibida para UNA norma concreta (construir sin permiso), no la norma
  evadida en general.
- **¿Clase media urbana?** 2021 es telefónico a celulares: sesgo hacia
  población conectada; se declara. 2019 cara a cara, nacional.
- **HOLDOUT gastado:** ninguno. M05 es `AJUSTE` en
  `milpa/catalogo-momentos-v0_1.tsv`. `holdout_gastado = NINGUNO`.

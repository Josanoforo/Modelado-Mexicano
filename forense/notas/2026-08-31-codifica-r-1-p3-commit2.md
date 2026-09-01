# CODIFICA-R-1 · P3 · COMMIT-2 — arbitra produce CIV-M-01/06/08/09

ENCARGO: `forense/encargos/2026-08-31-MAESTRA33-C3-CODIFICA-R-1.md`. Specs
congeladas en COMMIT-1: `forense/prereg-duelo-v2/notas-arbitra/2026-08-31-lote-civ-m-01-06-08-09.md`
(commit `b299bf7`).

## Qué se agregó a `tools/arbitra.py` para este commit

- `parsea_codificacion_binaria()` ahora también reconoce el patrón de
  conjunto `y=1 si VAR en {c1,c2,...}; y=0 si VAR en {c3,...}` (además del
  patrón de un solo valor que P2 ya usaba) — necesario porque
  `denuncia_con_miedo_o_desconfianza` es la unión de 3 códigos por lado,
  no un valor único.
- `resuelve_miembro_zip()`: cuando `tabla` en la tabla de codificación es
  un nombre LÓGICO (el que cita el FD, ej. `TMod_Vic`) y no una ruta física
  ya conocida, busca dentro del zip el miembro cuyo nombre lo contiene.
  Si hay más de un candidato, descarta los que traen `diccionario` en la
  ruta (INEGI publica, junto al CSV de datos, un CSV de diccionario de
  datos con el mismo nombre de tabla en el nombre de archivo — distinción
  real y verificable en la ruta, no una elección arbitraria). Si tras eso
  sigue habiendo 0 o más de 1 candidato, no adivina: lo declara.
- `produce()`: calcula una celda NUEVA (sin JSON todavía) y la escribe con
  `correr-R.py::escribe()` (mismo esquema, reusado tal cual). **Rehúsa
  sobreescribir** un id que ya tenga `corridas-R/<id>.json` — eso es
  competencia de `regresion()` (P2), no de `produce()`.

**Antes de correr `produce()` sobre datos reales**, se re-verificó que
estos cambios no rompieron la regresión de P2 (`DIN-11`/`SFT-04`/`TIC-08`
siguen `COINCIDE` exacto, dos veces, después de cada extensión) — ninguno
de los tres cae por la rama de nombre lógico ni de conjunto, así que el
resultado no debía cambiar, y no cambió.

## Comando y resolución de tabla física (recién ahora se abrió microdato)

```
$ python3 tools/arbitra.py --produce forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv CIV-M-01 CIV-M-06 CIV-M-08 CIV-M-09
```

| celda | miembro físico resuelto dentro del zip |
|---|---|
| CIV-M-01 | `Tmod_Vic.DBF` (en `envipe2012/base_de_datos_envipe_2012_dbf.zip`) |
| CIV-M-06 | `BASE_DE_DATOS_ENVIPE_2017_en/TMod_Vic.dbf` (en `envipe2017/bd_envipe2017_dbf.zip`) |
| CIV-M-08 | `conjunto_de_datos_TMod_Vic_ENVIPE_2019/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2019.csv` (en `envipe2019_csv.zip`) — único descartando el `diccionario_de_datos_...csv` hermano |
| CIV-M-09 | `conjunto_de_datos_TMod_Vic_ENVIPE_2020/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2020.csv` (en `envipe2020_csv.zip`) — mismo caso |

## Resultado (las 4, `estado: COMPUTADO`)

| celda | ola | R | EE_R | n_efectivo | n_estratos | n_upm_total | n_estratos_singleton |
|---|---|---|---|---|---|---|---|
| CIV-M-01 | 2012 | 0.258999 | 0.006971 | 26848 | 358 | 9129 | 30 |
| CIV-M-06 | 2017 | 0.222668 | 0.004907 | 39480 | 589 | 10631 | 26 |
| CIV-M-08 | 2019 | 0.234696 | 0.004945 | 40768 | 231 | 10599 | 1 |
| CIV-M-09 | 2020 | 0.203809 | 0.005374 | 33717 | 598 | 9785 | 29 |

Las cuatro son proporciones plausibles (20.4%–25.9% de los delitos no
denunciados citan miedo o desconfianza como razón principal), sin
`SIN_FILAS`, sin error. Esquema de los 4 JSON verificado idéntico
(mismas llaves, ni de más ni de menos) al de `DIN-11.json` ya existente.

## Verificación post-escritura

```
git status --short
```
mostró exactamente `tools/arbitra.py` modificado + los 4
`corridas-R/CIV-M-0{1,6,8,9}.json` nuevos — nada más. `sha256sum` de
`marco-M-congelado-v1_1.tsv` y `marco-M-sorteado-v1_1.tsv` idéntico al de
COMMIT-1 y P1 (marco no tocado).

## CIEGO

Este commit no abrió `corridas-M/` ni `milpa/tramite.yaml` en ningún
punto. Los archivos de microdato abiertos por primera vez en todo este
acto fueron, exactamente: los 4 zips de la tabla de arriba (leídos por
`csv_zip`/`dbf_zip`, reusados de `correr-R.py`, nunca reimplementados) —
ningún otro archivo de `data/raw/` se abrió en modo lectura de datos.

## Nota sobre `n_estratos_singleton`

`CIV-M-01`/`CIV-M-06`/`CIV-M-09` tienen 26–30 estratos singleton (un solo
UPM); `CIV-M-08` solo 1. El campo ya existe en el esquema de referencia y
`prop_ultimate_cluster` (reusado sin cambios) ya sabe declararlo — no es
un caso nuevo que esta herramienta tenga que resolver, los 9 R que ya
existían en `corridas-R/` también traen este campo.

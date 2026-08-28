# Cierre — `ACTO MAESTRA31-E5 · CRUCE-INVERSO`

27/ago/2026. Encargo: `forense/encargos/2026-08-27-MAESTRA31-E5-CRUCE-INVERSO.md` (dirección, maestra-31, archivado por A.3 antes de ejecutar). Spec congelada: `forense/notas/2026-08-27-cruce-inverso-spec.md` (COMMIT-1). Resultado: `data/cruce-inverso-v1_0.tsv` (COMMIT-2). Universo: `main = 07b1452`, confirmado sin diferencia contra `origin/main` al arranque.

## Arranque (resumen)

Clon existente en `/home/user/Modelado-Mexicano`, rama `claude/cruce-inverso-variables-sjo2ex`, `git status` limpio al empezar. `git log -1` = `07b1452 Merge pull request #385...`, idéntico al declarado. `data/raw` ausente — no usado por este acto (sus dos insumos, `data/inventario-reactivos-v1_0.tsv` y `milpa/procedencia.yaml`+`tramite.yaml`, están versionados). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, como se esperaba; sin red ni API. Ningún dato de este acto sale del espejo.

## A.13 — denominadores (comando)

```
$ wc -l data/inventario-reactivos-v1_0.tsv          → 178247 (178246 filas + encabezado)
$ python3 -c "...set(r['variable_id'] ...)"           → 36809 variable_id distintos
$ python3 -c "...set(r['instrumento'] ...)"           → 74 instrumentos distintos
```

Lado motor: 79 tokens con la regex cruda de dirección sobre `milpa/procedencia.yaml`+`milpa/tramite.yaml`; **59** con la receta propia (co-ocurrencia con nombre de encuesta por bloque + descarte de `_XX` y `G1..G6`), declarada y congelada en COMMIT-1 antes de cruzar. Diferencia: 20 coincidencias de forma que son metadata interna del archivo (identificadores de generador, marcas de ADR/hito, notación estadística), no variables de encuesta.

## Q1 — ¿existe lo que el motor cita?

Sobre las 59 (comando: `awk -F'\t' 'NR>6{print $2}' data/cruce-inverso-v1_0.tsv | sort | uniq -c`):

| veredicto A.4 | n |
|---|---|
| `EXISTE-SATISFACE` | 27 |
| `EXISTE-NO-SATISFACE` | 20 |
| `NO-ENCONTRADO` | 12 |

**27 de 59 (46%) existen exactamente donde el motor dice que existen** (mismo token, misma familia de instrumento y año). Otras 20 (34%) existen en el corpus pero bajo un instrumento distinto al declarado — el caso más grande es `ENCUCI 2020`: ningún instrumento `encuci*` existe en los 74 del inventario, así que toda variable que el motor atribuye a ENCUCI aparece (si aparece) bajo otro instrumento (`envipe*`, `endireh*`, la propia carpeta raíz de un ZIP), nunca satisfaciendo. Las 12 `NO-ENCONTRADO` (`D1, D3, E1, R3, R3_2, W1, X2, IC95, IDG3, ENIF2024, AP7_3, TB33`) son, con una excepción, exactamente el residual de falsos positivos de forma que la spec ya declaró como limitación conocida (§1 de la spec) — el filtro de co-ocurrencia con encuesta no los excluyó del lado del motor, pero correctamente no encuentran token igual en el inventario porque no son variables. La excepción es `TB33` (ENNViH/MxFLS): instrumento real citado por el motor, pero ENNViH/MxFLS **no está entre los 74 instrumentos del inventario** — no es un falso positivo de extracción, es un hallazgo de cobertura del corpus (ver abajo).

**Hallazgo no pedido, verificado por comando:** `ENCUCI` y `ENIF` y `ENNViH/MxFLS` — tres de las cinco familias de encuesta que `milpa/procedencia.yaml` cita como fuente — no tienen **ningún** instrumento homónimo en `data/inventario-reactivos-v1_0.tsv`:

```
$ cut -f3 data/inventario-reactivos-v1_0.tsv | sort -u | grep -iE "enif|encuci|ennvih|mxfls"
(sin salida)
```

Esto no es una falla de este acto — es la razón estructural detrás de casi todo el `EXISTE-NO-SATISFACE` y de parte del `NO-ENCONTRADO`: no es que el token esté mal escrito, es que la encuesta que el motor cree consultar no fue adquirida (o no fue indexada) en el universo de `data/raw` que produjo el inventario.

## Q2 — ¿en cuántas olas vive cada una?

Para las 47 que existen (27+20), conteo de valores distintos de `instrumento` (comando: `awk -F'\t' 'NR>6 && $2!="NO-ENCONTRADO"{print $1,$7}' data/cruce-inverso-v1_0.tsv | sort -k2 -nr`). Resultado alto, no predecible desde el escritorio: `P4_10` vive en 17 instrumentos/olas distintas; `BP1_20`, `AP7_1`, `AP3_10` en 16; `BP1_23`, `AP7_3_11`, `AP7_3_10`, `AP3_8` en 15. La mediana del conjunto que existe está muy por encima de 1. Esto corrobora la lectura B-bis de la spec: el motor cita estas variables como si fueran de una sola ola (la que nombra su `fuente:`), sin saber que la mayoría vive en 8+ rondas del mismo instrumento — oportunidad de panel/réplica no explotada, no un artefacto del método.

## Q3 — ¿a cuántos de los 30 parámetros no puede llegar este método, y por qué?

Comando (por entrada individual de cada una de las cinco secciones que suman 30 en `forense/perimetro-alcanzable-v1_0.md`, filtrando `_XX` y `G1..G6`):

| sección | items | citan ≥1 token |
|---|---|---|
| `medidos` | 4 | 0 |
| `derivados` | 6 | 0 |
| `asignados_probabilidad` | 13 | 0* |
| `evidencia_experimental_terceros` | 1 | 0* |
| `asignados_coeficiente` | 6 | 0 |
| **total** | **30** | **0** |

(*cuatro entradas de `asignados_probabilidad` y la única de `evidencia_experimental_terceros` sólo producen coincidencias de forma del residual conocido — `ENIF2024`, `V1`, `R3`, `R3_2`, `IC95` — ninguna es un reactivo real; contadas como "0 citas reales" en la tabla.)

**Confirmado y ampliado respecto a lo que dirección esperaba.** Dirección predijo que los 13 `ASIGNADO_PROBABILIDAD` no citarían ninguna variable, por ser juicio puro. Eso se confirma exacto: sus únicas coincidencias de forma (`ENIF2024`, `V1`, `R3`, `R3_2`) son metadata, no reactivos — ninguna entrada de esa sección nombra un token de encuesta real. **Pero el mismo resultado se extiende a las otras 17: ninguno de los 30 parámetros del motor cita, en su propia entrada de `procedencia.yaml`, un token exacto de variable de encuesta.** La razón difiere por sección:

- `medidos` (4) y `derivados` (6): citan estudios/fuentes con nombre propio en prosa (`"Ascencio & Chang"`, `"INE, elección judicial 2025"`, `"ENVIPE, cifra negra"`) — la fuente es real y a veces incluso nombra la encuesta, pero nunca da el reactivo/código concreto; los `derivados` son aritmética sobre un `medido` y no añaden cita nueva.
- `asignados_probabilidad` (13): juicio puro, sin ruta — confirma exactamente la expectativa de dirección.
- `evidencia_experimental_terceros` (1): cita `cita` + `llave_id` (un experimento y una fila de registro), no un reactivo de encuesta.
- `asignados_coeficiente` (6): cita nombres de familias de encuesta genéricas en el diagnóstico (`"Pew, ENCIG, ENOE, ENIF, ENVIPE, ENSU, CEEY"`) y nombres internos de coeficiente del generador (`confianza_institucional`, `radio_confianza`, etc.), nunca un código de reactivo.

Los 59 tokens reales que sí existen en el archivo viven en secciones auxiliares (`condicionales_confianza_institucional`, `condicionales_escalares*`, `coeficientes_generador_medidos`) que **no son parte de los 30 parámetros contados** — son insumos de calibración de generador, no números del motor en sí.

**Esto no contradice el `N=12/30` de `FP-170`** (perímetro alcanzable por *ruta de estimabilidad de coeficiente*, ADR-89/RUTA-A/C/I/SIN-RUTA) — es un eje distinto: aquél mide si existe una ruta de estimación declarada para el coeficiente; éste mide si la entrada del parámetro cita, ella misma, un token de variable de encuesta verificable contra el corpus. Los dos pueden ser ciertos a la vez sin fricción: un parámetro puede tener ruta de estimabilidad (RUTA-A/C/I) sin que su propia entrada en `procedencia.yaml` lleve jamás un código de reactivo — la ruta vive en `coeficientes_generador_medidos`/`rutas_estimabilidad_coeficiente`, no en la entrada del parámetro. Se declara la distinción para que mesa no las confunda al firmar.

**Conclusión de Q3:** el techo del emparejamiento por token exacto no es un problema de cobertura de corpus — es estructural, y más amplio de lo que dirección anticipaba: 30 de 30 parámetros, no 13 de 30, son inalcanzables por esta vía directamente sobre su propia entrada. No se arregla con más `data/raw`.

## Lo que este acto no hizo

No emparejó por texto ni semántica. No propuso qué medir. No tocó el motor ni `milpa/`. No adjudicó ningún parámetro a ninguna fuente. No promovió nada a acto medidor. `construir_crosswalk` (`milpa/src/emisor.py`) no se usó ni se editó — el cruce se escribió como consulta propia sobre las dos tablas (declarado en COMMIT-1 §2), porque `construir_crosswalk` opera demanda→oferta con normalización propia de necesidad, no oferta→motor por token exacto de variable.

## Frase de sello

«El primer resultado que produjo este procedimiento es el que se reporta.» — 27/20/12 sobre 59, y 0/30 en Q3. Ninguno se ajustó después de verlo.

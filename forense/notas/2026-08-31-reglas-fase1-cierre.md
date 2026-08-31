# Nota · ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1 — corrida y cierre (COMMIT-2)

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-31-reglas-fase1-cierre.md` |
> | **QUÉ ES** | Corrida única de `tools/tasas_base_fase1.py`, con n/p/IC/ponderador por regla y nota A.13. |
> | **ENCARGO** | `forense/encargos/2026-08-31-MAESTRA32-E18-REGLAS-OLA5-FASE1.md` |
> | **SPEC** | `forense/notas/2026-08-31-reglas-fase1-spec.md` (COMMIT-1, congelada antes de esta corrida) |

## Comando ejecutado

```
$ export SCRATCH_DBF=<scratchpad>/
$ python3 tools/tasas_base_fase1.py
```

## Output real (íntegro, sin editar)

```
=== civico.denuncia.miedo_desconfianza ===
  estado: MEDIDO
  sha256_payload: 8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa
  n_universo_disparador_vic2: 15493
  n_universo_colapsado_persona: 13023
  n_con_ponderador: 13023
  n: 13023
  p = 0.294313
  IC95 = [0.282822, 0.306570]

=== dinero.ahorro.tiene_ahorros ===
  estado: MEDIDO
  sha256_payload_ola2: fc4ea4ae7d0cf4bc906bb46ad5e1e7444b9c24f8e0c569ae3f6e5a9b72453c1a
  sha256_payload_ola3: 00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15
  sha256_payload_peso: 34ee12b0c0d71e76676197089b5fd6048c0fdaa590a220f440d95526b1f4713b
  n_universo_panel_pre_peso: 6356
  n_con_ponderador: 6028
  n: 6028
  p = 0.174804
  IC95 = [0.159250, 0.190543]

=== familia.apoyo.recibe_dinero_familiares ===
  estado: MEDIDO
  sha256_payload: 00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039
  n_universo_filtro_edad: 12379
  n_con_ponderador_y_reactivo_valido: 11895
  n: 11895
  p = 0.457707
  IC95 = [0.444232, 0.470782]

=== familia.corresidencia.adulto_familiar ===
  estado: MEDIDO
  sha256_payload: bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3
  n_universo_viviendas_tipo_adqui_no_blanco: 14690
  n_personas_historiavida_total: 23831
  n_con_ponderador: 14887
  n: 14887
  p = 0.996086
  IC95 = [0.994794, 0.997250]

=== tramite.mordida.discrecional[enmienda_encuci] ===
  estado: MEDIDO
  sha256_payload: 0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283
  n_universo_contacto: 13435
  n: 13435
  p = 0.125822
  IC95 = [0.116323, 0.135544]

RESUMEN: 5 de 5 reglas con p medida.
```

## Tabla resumen

| regla | encuesta/ola | n | p | IC95 | ponderador |
|---|---|---|---|---|---|
| `civico.denuncia.miedo_desconfianza` | ENVIPE 2025 | 13023 | 0.294313 | [0.282822, 0.306570] | FAC_ELE |
| `dinero.ahorro.tiene_ahorros` | ENNViH ola 2 | 6028 | 0.174804 | [0.159250, 0.190543] | fac_3b |
| `familia.apoyo.recibe_dinero_familiares` | ENIF 2024 | 11895 | 0.457707 | [0.444232, 0.470782] | FAC_PER |
| `familia.corresidencia.adulto_familiar` | EDER 2017 | 14887 | 0.996086 | [0.994794, 0.997250] | factor |
| `tramite.mordida.discrecional` (enmienda) | ENCUCI 2020 | 13435 | 0.125822 | [0.116323, 0.135544] | FAC_SEL |

IC95 de las cinco: bootstrap 10.000 réplicas, `seed=42`, remuestreo simple de filas — declarado en la spec (c), no supuesto de diseño complejo (ninguna de las cinco fuentes tiene un estimador de diseño UPM/estrato reproducible dentro del perímetro de este acto).

## A.1 — verificación de hash contra manifiesto

| payload | sha256 calculado en esta corrida | ¿coincide con `data/manifiesto.yaml`? |
|---|---|---|
| `envipe2025_csv.zip` | `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` | **SÍ** — coincide exacto con `data/manifiesto.yaml:320` (id `envipe2025_csv`) |
| `eder2017_bases_csv.zip` | `bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3` | **SÍ** — coincide exacto con `data/manifiesto.yaml:4330` (id `eder_2017_eder2017_bases_csv`) |
| `BD_ENCUCI2020_dbf.zip` | `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` | **SÍ** — coincide exacto con `data/manifiesto.yaml` (id `encuci2020_bd_dbf`), verificado por `sha256sum` directo además del script |
| `ehh05dta_all.zip` (ENNViH ola2) | `fc4ea4ae7d0cf4bc906bb46ad5e1e7444b9c24f8e0c569ae3f6e5a9b72453c1a` | **NO VERIFICABLE** — sin entrada de manifiesto para este archivo (ver hallazgo abajo) |
| `ehh09dta_all.zip` (ENNViH ola3) | `00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15` | **NO VERIFICABLE** — ídem |
| `ehh05w_all.zip` (ENNViH peso) | `34ee12b0c0d71e76676197089b5fd6048c0fdaa590a220f440d95526b1f4713b` | **NO VERIFICABLE** — ídem |
| `enif_2024_bd_csv.zip` | `00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` | **NO VERIFICABLE** — sin entrada de manifiesto para este archivo específico (el manifiesto tiene `enif2024_csv` apuntando a un ZIP distinto, `data/raw/enif2024_csv.zip`) |

## A.13 — hallazgos y discrepancias, declarados sin ocultar

1. **ENNViH sin entrada de manifiesto (hallazgo preexistente a este acto).** `data/manifiesto.yaml:84-95` declara literalmente *"ningún archivo de ENNViH se ha descargado ni se registra aquí"*, pero `data/raw/ennvih/` sí tiene los ZIP físicos (147 archivos en `ehh09dta_all.zip`, confirmado), y ya fueron usados por `ACTO CAL-G3-PUNTUAL` (`forense/notas/2026-08-24-cal-g3-puntual-cierre.md`) antes de este acto. Este acto reporta el sha256 real de los tres ZIP usados (tabla A.1) porque no hay manifiesto contra el cual verificarlos — es una inconsistencia de registro que **este acto no genera, solo re-confirma y reporta**.

2. **ENIF 2024 duplicado en `data/raw/`, sin manifiesto para el segundo.** `data/raw/enif2024_csv.zip` (con `id: enif2024_csv` en el manifiesto) y `data/raw/enif_2024_bd_csv.zip` (sin `id:` propio localizado) son dos descargas distintas de ENIF 2024. Este acto usó el segundo porque es el único que trae la tabla `TMODULO.csv` con las columnas citadas por `procedencia.yaml:300-319` (`FILTRO_S9_1`, `P9_9_4`, `FAC_PER`, `EDAD_V`) confirmadas por lectura directa de cabecera. El manifiesto no cubre este payload con hash verificable — mismo patrón de inconsistencia que (1), preexistente.

3. **Universo ENNViH: 6356 (pre-peso) / 6028 (con peso) en este acto, contra 6305 de `CAL-G3-PUNTUAL`.** La llave `CAL-G3-PUNTUAL` reporta universo final `n=6305` (`2026-08-24-cal-g3-puntual-cierre.md`, tabla PASO 2: `6807` con `pr02`/`cr27` válidos en ambas olas, `-502` sin `fac_3b` → `6305`). Este acto, aplicando el mismo criterio declarado en la spec (COMMIT-1), obtuvo `6356` filas antes de pesar y `6028` después de unir el ponderador — ambos números **distintos** del `6807`/`6305` de la llave sellada. **No se reconcilia esta discrepancia dentro de este acto** (fuera de perímetro — el perímetro declarado no incluye re-abrir `CAL-G3-PUNTUAL`): las causas más probables, sin verificar cuál aplica, son (i) un detalle no replicado del método de despoje de letras de `pid_link` en la exclusión de ronda C, o (ii) una diferencia en cómo se unió el peso `fac_3b` (esta corrida usa `folio+ls` reconstruido desde `pid_link`, la nota original no detalla el método exacto de unión del peso más allá de nombrar el archivo). El `p=0.174804` de esta regla se reporta contra el universo **de esta corrida** (`n=6028`), no contra el `n=6305` de la llave — están declarados como universos distintos, no se mezclan.

4. **`familia.corresidencia.adulto_familiar`: p=0.996086, techo casi saturado.** Ver `hallazgo` embebido en `milpa/tramite-ola5-propuesta-v0.yaml` — el diseño "alguna vez en la vida" (colapso sobre ~38 filas-año × 5 variables por persona) satura la proporción cerca de 1 aun si la probabilidad de acierto por fila es baja. Es aritméticamente coherente con el propio `n_util` de `ACTO MAESTRA32-E16` (`procedencia.yaml:1193`: `EDER theta=1 n=623, theta=0 n=14264`, total `14887` — **coincide exacto** con el `n_con_ponderador=14887` de esta corrida, confirmando que ambos actos abrieron el mismo universo por el mismo método). No es un error del script — es el resultado literal del procedimiento congelado en la spec, reportado sin filtrar ("el primer resultado que produzca este procedimiento es el que se reporta").

5. **`tramite.mordida.discrecional[enmienda]`: n=13435 coincide exacto con `procedencia.yaml:889`** ("universo con contacto=13435/21519") — confirma que el universo de contacto de este acto reproduce, contra el microdato, el mismo número ya citado por `ACTO W` (4/ago/2026). El `p=0.125822` [IC95 0.116323, 0.135544] es además compatible con el techo `13.38%` ya citado en `procedencia.yaml:785` (verificado 29/jul/2026, `hitoD-R3.2`) sobre el mismo payload ENCUCI — dos actos independientes, mismo payload, números en el mismo rango. No prueba ni refuta el `0.62` `ASIGNADO`: solo aporta un segundo dato medido consistente con el hallazgo previo de que `0.62` no tiene apoyo empírico de escala.

6. **Ningún payload referenciado resultó NO-ENCONTRADO.** Los cinco ZIP citados por la spec (COMMIT-1) existen en `data/raw/` y se abrieron sin sustituir con datos de otra fuente. La primera corrida del script (antes de dos correcciones de bug — miembro `.dta` mal nombrado en ola 3 de ENNViH, y comparación de tipo `str` vs `float` en los flags de contacto de ENCUCI que dejaba el universo vacío) sí produjo errores de programación, no de dato ausente — corregidos antes de aceptar el resultado final aquí reportado, siguiendo la disciplina de "el primer resultado *correcto* que produzca el procedimiento es el que se reporta" (un traceback de Python no es un resultado).

## Verificación de intocables

```
$ git diff --stat milpa/tramite.yaml milpa/procedencia.yaml milpa/src/
(sin salida -- vacío)
$ grep -r "tramite-ola5" milpa/src/
(sin salida -- vacío, el motor no lee el archivo nuevo)
```

## Tablero FP-190

Ver fila añadida en `forense/hallazgos.md` / donde vive el tablero FP-190 (sección "Tablero" de este mismo acto, más abajo en el flujo de commits) — enmienda fechada 31/ago/2026, fase 1 (este acto) / fase 2 (sucesor, las 5 celdas CIV-08/DIN-11/SFT-04/SFT-06/TIC-06 + las 3 sin θ DIN-07/TIC-01/EMP-05). Texto original del programa (i′) queda intacto, la enmienda se agrega, no reemplaza.

Fila nueva de firmas pendientes: **"mesa sella las 5 reglas de fase 1 (o las devuelve); hasta entonces el motor no las carga."** — es el recibo que trae la decisión siguiente, no una ranura de este acto.

**"El primer resultado que produzca este procedimiento es el que se reporta."**

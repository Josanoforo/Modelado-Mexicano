# Nota · `ACTO ESCALA-ASIGNADOS`, 25/ago/2026 (`FP-141`, `L1-b`)

Entorno **NUBE** (`cloud_default`). Sin red externa ni microdato. Encargo archivado: `forense/encargos/2026-08-25-ESCALA-ASIGNADOS.md` (`CONSUMIDO`).

## 0 · Autorización de tocar `milpa/`

`FP-141` (`forense/firmas-pendientes.tsv`, `FIRMADA`, `firmada_en`: *"2026-08-25, mesa, hoja de las diez letras, L1/FP-127 opción b, verbatim: 'mantener con nota + acto de escalas'"*) es la fila que autoriza este acto y la única excepción viva a la regla general de no tocar `milpa/` — verificada leyendo la fila completa antes de escribir.

## 1 · Las 15 entradas ASIGNADO — rastreo de fuente y escala

Las 15 entradas viven en dos sitios que se corresponden 1-a-1: `milpa/procedencia.yaml:asignados_coeficiente.detalle` (valores, agrupados por generador) y `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle` (15 filas planas, una por coeficiente — es donde se añadieron los dos campos nuevos). Fuente única de asignación para las 15, verificada por `sed -n '454,460p' canon/modelo-decision-v4_0.md`:

```
| G1a | `confianza_institucional[financiera] −0.60` · `radio_confianza −0.35` |
| G1b | *a revisión — el generador está contradicho* |
| G2 | `sens_estatus 0.55` · `aversion_riesgo 0.20` |
| G3 | `horizonte_temporal −0.60` · `aversion_riesgo 0.40` · `familismo_apoyo 0.20` |
| G4 | `exposicion_violencia 0.70` · `confianza_institucional[justicia] −0.40` · `horizonte_temporal −0.20` · `sens_estatus −0.15` |
| G5 | `familismo_apoyo 0.50` · `familismo_obligacion` (signo negativo o no monotónico) · `radio_confianza 0.15` |
| G6 | `deferencia 0.45` |
```

Esa tabla (`canon/modelo-decision-v4_0.md:454-460`) es la única fuente de los 15 valores — ninguna otra entrada del canon les da número. **Ninguna línea de esa tabla, ni de §2 "Los generadores latentes" que la rodea, declara una forma funcional ni una función de enlace** para los coeficientes: no dice si son índice estandarizado, puntos porcentuales, log-odds o unidad natural de la condicional que multiplican. Verificado por lectura completa de §2 (líneas 422-490) y por grep dirigido:

```
$ grep -n "función de enlace\|log-odds\|logit\|puntos porcentuales\|índice estandarizado" canon/modelo-decision-v4_0.md
(sin resultados directos declarando la escala de estos 15 coeficientes)
```

La propia línea `:450` lo dice verbatim: **"El signo de los generadores está bien sostenido por el corpus. La magnitud no."** — es una afirmación sobre falta de escala, no solo de precisión. Y `milpa/procedencia.yaml` repite, en cada una de las cinco entradas donde ya existe un β̂ medido para comparar (`G1_radio_confianza`, `G1_confianza_institucional`, `G3_familismo_apoyo`, `G4_exposicion_violencia`, `G4_confianza_institucional_justicia`), la misma frase: *"no comparable en magnitud... (ningún ADR de `D-ABC` ha sellado función de enlace a la fecha)"*.

**Conclusión, para las 15: `ESCALA_NO_DERIVABLE`.** No es una entrada aislada — es la fuente entera (la única que existe) la que no declara ni permite derivar la escala, así que las 15 comparten el mismo veredicto y la misma cita. No se inventó una escala para ninguna.

| gen.coef | valor ASIGNADO | escala_asignado | escala_fuente |
|---|---|---|---|
| G1.confianza_institucional | −0.60 | ESCALA_NO_DERIVABLE | `canon/modelo-decision-v4_0.md:454-460`, `:450` |
| G1.radio_confianza | −0.35 | ESCALA_NO_DERIVABLE | ídem |
| G2.sens_estatus | 0.55 | ESCALA_NO_DERIVABLE | ídem |
| G2.aversion_riesgo | 0.20 | ESCALA_NO_DERIVABLE | ídem |
| G3.horizonte_temporal | −0.60 | ESCALA_NO_DERIVABLE | ídem |
| G3.aversion_riesgo | 0.40 | ESCALA_NO_DERIVABLE | ídem |
| G3.familismo_apoyo | 0.20 | ESCALA_NO_DERIVABLE | ídem |
| G4.exposicion_violencia | 0.70 | ESCALA_NO_DERIVABLE | ídem |
| G4.confianza_institucional | −0.40 | ESCALA_NO_DERIVABLE | ídem |
| G4.horizonte_temporal | −0.20 | ESCALA_NO_DERIVABLE | ídem |
| G4.sens_estatus | −0.15 | ESCALA_NO_DERIVABLE | ídem |
| G5.familismo_apoyo | 0.50 | ESCALA_NO_DERIVABLE | ídem |
| G5.familismo_obligacion | sin magnitud (ADR-30) | ESCALA_NO_DERIVABLE | ídem |
| G5.radio_confianza | 0.15 | ESCALA_NO_DERIVABLE | ídem |
| G6.deferencia | 0.45 | ESCALA_NO_DERIVABLE | ídem |

Cambio aplicado en `milpa/procedencia.yaml`: los dos campos `escala_asignado:`/`escala_fuente:` se añadieron a las 15 filas de `rutas_estimabilidad_coeficiente.detalle` (única edición al archivo — verificado, `git diff --stat milpa/procedencia.yaml` solo toca esas 15 líneas). No se tocó `asignados_coeficiente.detalle` (misma disciplina que `Encargo W`/`Encargo E-CE` ya declararon: sección nueva y paralela, no edición de `detalle`). `tools/censo_estimabilidad.py --reparto` corrido antes y después del cambio: mismo reparto (`RUTA-A=3 · RUTA-C=5 · RUTA-I=1 · SIN-RUTA=6`), el derivador solo lee `gen`/`coef`/`ruta`/`prioridad`/`nota` y no le afectan los campos nuevos.

## 2 · `CAL-G3` — la discrepancia de `−0.60` bajo la escala derivada

`CAL-G3` (`canon/estado-programa-v1_10.md`, línea de llaves de identificación; `forense/notas/2026-08-24-cal-g3-puntual-cierre.md`; `forense/registro-llaves-identificacion-v1_0.md` §11) midió, sobre `G3.horizonte_temporal`, un β=+0.0146 (IC95%=[+0.0047,+0.0245], primeras diferencias ponderadas, ENNViH olas 2-3, N=6,305, bajo supuesto MAS) — **signo opuesto** al `−0.60` que `G3.horizonte_temporal` trae ASIGNADO.

Con la escala del asignado declarada `ESCALA_NO_DERIVABLE` (§1), la lectura correcta de esta discrepancia es:

- **No es comparable con enlace.** No existe función de enlace sellada por ningún ADR de `D-ABC` entre la escala de β (diferencia de proporciones/primeras diferencias ponderadas, unidad de la condicional `horizonte_temporal` medida) y la escala del `−0.60` (índice del generador, forma no declarada) — no hay conversión posible entre las dos magnitudes, ni razón para esperar que el `0.0146` y el `0.60` vivan en la misma unidad.
- **Comparable solo en signo, con cautela.** El signo es lo único que ambas escalas comparten sin necesitar función de enlace — pero incluso esa lectura ya está hecha y documentada en el árbol (`registro-llaves-identificacion-v1_0.md` §11: *"signo opuesto"*) y este acto no la repite como si fuera nueva. La comparación de signo tampoco es gratis: `G3.horizonte_temporal` es el único generador con `RUTA-I` en el censo de estimabilidad (la llave de identificación (i) de `ADR-57(c)`, `ficha-id-g3-v1_0.md`) — el diseño intra-persona que produjo el β̂ es distinto en estructura del que hipotéticamente sostendría el `−0.60`, así que ni el signo se compara con la misma confianza con la que se compararía una réplica del mismo diseño.
- **En magnitud: inconmensurable.** El `0.0146` y el `−0.60` no se pueden restar, dividir ni razonar entre sí como si fueran dos números en la misma escala — hacerlo (por ejemplo, decir "la discrepancia es de 0.6146" o "el asignado sobreestima 40 veces") fabricaría una comparación que la fuente no sostiene. Esto es exactamente el estado que el tablero ya trae para esta fila (`FP-124`, β `PROPUESTO`, no escrito en `milpa/procedencia.yaml`) — este acto no lo cambia, solo lo funda en la escala derivada en vez de dejarlo implícito.

**Este párrafo no re-adjudica nada** — es la lectura que la mesa pidió para tenerla escrita antes de decidir qué hacer con `CAL-G3`/`FP-124`; la decisión sigue siendo de mesa.

## 3 · Fila nueva `A.12`

`instrucciones-proyecto-v2_11.md:354` (`A.12 · El tablero de firmas pendientes se deriva, no se recuerda`) exige una fila en `forense/firmas-pendientes.tsv` cuando algo así se hace visible. Como las 15 entradas quedaron `ESCALA_NO_DERIVABLE` y eso gatea toda comparación futura de magnitud (no solo `CAL-G3`), se añadió `FP-149` (`ABIERTA`) declarando el bloqueo y apuntando a esta nota y a `canon/modelo-decision-v4_0.md:454-460`.

## 4 · Tablero

`FP-141` recibe `ejecutada_en` (2026-08-25, este acto). `FP-149` nace `ABIERTA` (§3). Ninguna otra fila se toca.

## 5 · Lo que este acto NO hace

No re-adjudica `CAL-G3` ni `FP-124`. No escribe ninguna escala inventada. No toca `asignados_coeficiente.detalle` ni ningún otro bloque de `milpa/` fuera de las 15 filas de `rutas_estimabilidad_coeficiente.detalle`. No toca ningún directorio de espejo (no existe tal directorio en el árbol).

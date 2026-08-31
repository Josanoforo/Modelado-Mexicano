# Nota de cierre · ACTO MAESTRA32-E11 · COBERTURA-15 (re-emisión de E10)

Fecha de ejecución: 31/ago/2026. Clon `/home/user/Modelado-Mexicano` existente, rama `claude/maestra32-e11-reemision-bezu0m`, sin cambios pendientes al arrancar. `git log -1` → `2799132 Merge pull request #397 from Josanoforo/claude/maestra32-e9-launch-55zzlu` — exactamente el SHA que el encargo declara (merge `PR #397`/`ADR-225`), sin drift. `data/raw` ausente (esperado, no se creó ni enlazó: este acto no abre payloads). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coincide con NUBE declarado); `curl` a `www.inegi.org.mx` → sin conectividad (`000`, política de red del entorno), 0 archivos examinados por ese comando — sonda de red pura, no de árbol; este acto no toca microdato ni red, así que no gatea nada. Ninguna cifra de este cierre sale del espejo del proyecto.

`command grep -c "duelo\|prereg" data/INFRAESTRUCTURA-v1_0.md` → **5** — ya indexado, no aplica regla de conducto.

---

## Emisión ciega — archivos abiertos

Este acto no abrió `forense/prereg-duelo-v2/corridas-R/` ni ningún archivo con valores publicados de las 15 celdas. Del marco congelado se leyeron únicamente las columnas `id … estrato` (el header completo de la tabla — no existe columna de valor en `marco-congelado-piloto-v1_0.tsv`, verificado: 17 columnas, la última es `estrato`). Listado completo de archivos abiertos (lectura o grep) durante este acto:

- `forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv` (completo, 60 filas, todas las columnas — ninguna es valor)
- `forense/prereg-duelo-v2/CONGELADO-v1_0.sha256` (verificación de hash, coincide)
- `forense/prereg-duelo-v2/corridas-M/M-*.json` (las 15 fichas de la muestra — `estado_M`/`evidencia_pasada_1`, sin valor de celda)
- `forense/prereg-duelo-v2/enlace-M-v1_0.md` (resultado agregado "0 EMITE sobre las 15", sin valores de celda)
- `forense/crosswalk-pregunta-regla-v1_1.tsv` (pasada-1, `emisibilidad_p1` — sin valores de celda; nota: el encargo cita `data/crosswalk-pregunta-regla-v1_1.tsv`, la ruta real es `forense/crosswalk-pregunta-regla-v1_1.tsv`, discrepancia de cita heredada del encargo, no bloqueante)
- `forense/firmas-pendientes.tsv` (tabla completa, para re-derivar máximo y ver `FP-181`/`FP-182`)
- `canon/gobernanza-v1_15.md` (ADR-220 a ADR-225, para contexto de cascada y re-derivar máximo)
- `canon/modelo-decision-v4_0.md` (§1.6, §2.1, §2.2, §3.1-§3.10 completas — catálogo de 49 reglas, generadores, coeficientes)
- `milpa/tramite.yaml` (completo — único YAML con bloque `reglas:`)
- `milpa/procedencia.yaml` (secciones `condicionales_confianza_institucional`, `condicionales_escalares`, `condicionales_escalares_exposicion_violencia`, `asignados_probabilidad`, `asignados_coeficiente` — fichas de operacionalización de θ, sin valores de las 15 celdas)
- `data/inventario-reactivos-v1_2.tsv` (completo, 178 246 filas — `variable_id`/`texto_reactivo`/`instrumento`/`ola`, sin valores de encuesta)
- `data/inventario-fd-v1_1.tsv` (completo, 17 094 filas — misma naturaleza)
- `data/INFRAESTRUCTURA-v1_0.md` (grep de conteo únicamente)
- `forense/notas/2026-08-30-cobertura-15-cierre.md` (cierre de E10, obra previa citada por el propio encargo)
- `forense/encargos/2026-08-30-MAESTRA32-E10-COBERTURA-15.md` (encargo original de E10, para heredar la definición de `FP-183`/`FP-184`)
- `canon/estado-programa-v1_10.md`, `canon/registro-rotulos.tsv` (para la cascada, ver abajo)

Ninguno de estos archivos contiene una columna o campo con el valor medido de ninguna de las 15 celdas.

---

## COMMIT-1 / COMMIT-2

Receta congelada en `forense/notas/2026-08-30-cobertura-15-spec.md` **antes** de correr ninguna búsqueda de contenido sobre las tablas de inventario. Corrida única (script de este acto, no committeado — no está en el perímetro declarado) sobre `data/inventario-reactivos-v1_2.tsv` (178 246 filas) + `data/inventario-fd-v1_1.tsv` (17 094 filas), salida en `forense/prereg-duelo-v2/cobertura-15-v1_0.tsv` (18 filas, una por celda×candidato θ sobre las 15 celdas).

### Resumen por celda (vocabulario A.4, universo A.13 declarado en cada fila del TSV)

| Celda | Q1 regla | Q2 θ | Q3 operacionalización mismo instrumento+ola | Q4 payload | Veredicto |
|---|---|---|---|---|---|
| `CIV-08` | **NO** — sin id con punto en la frase; derivación de dominio `civico` (candidatos G4: `civico.protesta.agravio_urbano`/`civico.autodefensa.agravio_rural`, modelo:556-557) no produce "percepción de inseguridad" como conducta | `exposicion_violencia` (nombrada literal, no vía G#) | Informativo: familia de código `AP7_3_10..14` SÍ está en `envipe2023` (11 variable_id), pero `texto_reactivo` vacío en 100% de las 2657 filas del instrumento — búsqueda de texto censurada, no confirmación (A.13) | SÍ (4 filas, `AP4_4_03`) | **NO-ENCONTRADO** |
| `DIN-03` | **SÍ** `familia.seguro.volatilidad_ausencia_estado` (modelo:412,533) | G5: `familismo_apoyo`(0.50)/`radio_confianza`(0.15)/`norma_de_género` | `familismo_apoyo`: **CIRCULAR-EXCLUIDO** (precedente `procedencia.yaml:315-320`, la misma cita "ENIF p9_9_4" del encargo). `radio_confianza`/`norma_de_género`: 0 hits sobre 604 filas `enif2012` (253 con texto, 41.9%) | SÍ (1 fila, `P7_1`) | **EXISTE-NO-SATISFACE** |
| `DIN-05` | **SÍ**, dos reglas: `dinero.ahorro.informal_sin_puente` (modelo:499) y `cooperacion.tanda.conoce_organizadora` (modelo:563) | G1a→`confianza_institucional[financiera]` (citado); segunda regla sin cita G# (`radio_confianza` derivado) | 0 hits para ambas sobre 1328 filas `enfih2019` (664 con texto, 50%) | SÍ (2 filas, `P8_1_1`, con texto) | **EXISTE-NO-SATISFACE** |
| `DIN-07` | **SÍ** `dinero.planeacion.formal_estable` (modelo:406,498) | `NO-IDENTIFICADA` — el `PORQUE` no cita G# | No procede (sin θ) | SÍ — hallazgo colateral: el payload propio (`banxico_encuesta_competencias_financieras_2019.xlsx`) SÍ está en el corpus, bajo `instrumento=(sin-instrumento-derivable)` (uno de los 23 payloads que la regla de etiqueta v1.2 dejó sin resolver, `FP-180`); `SF2` presente literal (`INSPECT_XLSX`, `PRESENTE_EN_DATA_RAW`) | **EXISTE-NO-SATISFACE** |
| `DIN-11` | **NO**, explícito en la frase ("M no tiene ninguna regla que produzca conocimiento") — verificado contra las 7 reglas de dominio `dinero` | — | — | SÍ (3 filas, `P5_3`) | **NO-ENCONTRADO** |
| `SFT-04` | **NO** — derivación de dominio `salud` agotada (5 reglas revisadas, ninguna produce ABVD/asistencia funcional) | — | — | SÍ (1 fila, `H16D_18`) | **NO-ENCONTRADO** |
| `SFT-06` | **NO** — derivación de dominio `familia` (3 reglas) y del dominio adyacente `cooperación` (4 reglas) agotada | — | — | SÍ (2 filas, `F55_24`, con texto) | **NO-ENCONTRADO** |
| `TIC-01` | **SÍ** `cooperacion.comite.monitoreo_sancion_visible` (modelo:562) — coincide con el dominio propio de la celda | `NO-IDENTIFICADA` — el `PORQUE` no cita G# | No procede (sin θ) | SÍ (4 filas, `p3i`) | **EXISTE-NO-SATISFACE** |
| `TIC-06` | **NO**, explícito en la frase ("ninguna regla del motor distingue estacionalidad") — verificado contra las 4 reglas de dominio `trabajo` | — | — | SÍ (3 filas, `P2`) | **NO-ENCONTRADO** |
| `TIC-08` | **SÍ** `informacion.credibilidad.allegado_confianza` (modelo:571) — cruce de dominio (celda `comunicacion`, regla `informacion`), consistente con la propia frase | Sin cita G# (`radio_confianza` derivado de "confianza radial") | 0 hits sobre 967 filas `endutih2024` (477 con texto, 49.3%) | SÍ (2 filas, `P7_15`, con texto) | **EXISTE-NO-SATISFACE** |
| `TIC-12` | **SÍ** `cooperacion.confianza.puente_personal` (modelo:564) — cruce de dominio (celda `trabajo`, regla `cooperacion`) | `radio_confianza`, **cita explícita** (modelo-decision:462, enmienda 28/ago) | 0 hits — pero `enoe2024` T1 tiene `texto_reactivo` vacío en 100% de sus 1277 filas; barrido complementario de los 426 `variable_id` distintos (código, no prosa) no revela batería de confianza — son códigos de empleo/demografía/geografía | SÍ (1 fila, `p3n`) | **EXISTE-NO-SATISFACE** (declarado con censura de texto, A.13) |
| `EMP-02` | N/A — **(e)** unidad = empresa | — | — | — | **EXISTE-NO-SATISFACE** (por (e)) |
| `EMP-04` | N/A — **(e)** unidad = empresa (frase también declara explícito "ninguna regla del motor separa las dos") | — | — | — | **EXISTE-NO-SATISFACE** (por (e)) |
| `EMP-05` | **SÍ** `familia.union.baja_garantia_institucional` (modelo:535) | `NO-IDENTIFICADA` — el `PORQUE` no cita G# | 0 hits sobre 204 filas `cpv2020` (201 con texto, 98.5%) — consistente con CPV siendo censo sin batería actitudinal | SÍ (1 fila, `SITUA_CONYUGAL`) | **EXISTE-NO-SATISFACE** |
| `DOC-06` | N/A — **(e)** unidad = documento/emisora | — | — | Payload propio ausente del corpus (0 filas `hrratings\|bmv\|findep`+`IMOR`) — consistente: la ola arbitro 4T2026 aún no existe | **EXISTE-NO-SATISFACE** (por (e)) |

---

## Falsador del acto — DISPARADO

**5 de las 12 celdas evaluables** (fuera de las 3 excluidas por unidad, `EMP-02`/`EMP-04`/`DOC-06`) llegan a `regla_existe = NO` tras derivación de dominio agotada: `CIV-08`, `DIN-11`, `SFT-04`, `SFT-06`, `TIC-06`. El falsador declarado en el encargo se dispara en su umbral exacto (`≥5`): **se reporta como hallazgo sobre el alcance del motor, no se parcha la receta**. Una vuelta, cero iteración — no se buscó una sexta regla candidata para ninguna de las cinco, ni se relajó el criterio de coincidencia de conducta.

El hallazgo, en una línea: el motor de 49 reglas cubre bien los dominios `dinero`/`familia`/`cooperación` en lo que sí tiene regla, pero **no tiene regla ni generador que produzca, como conducta, ni "conocimiento declarativo sin acción" (`DIN-11`), ni "distinción de estacionalidad" (`TIC-06`), ni "asistencia funcional por dependencia/ABVD" (`SFT-04`), ni un desenlace de cooperación intrafamiliar entre hermanos sin regla de dominio propia (`SFT-06`), ni una regla-conducta que consuma directamente el parámetro `exposicion_violencia` para producir percepción de inseguridad, en vez de protesta/autodefensa (`CIV-08`)** — cinco vacíos de cobertura genuinos, no un defecto de la receta de búsqueda de este acto.

## Las 7 celdas restantes con regla: por qué ninguna llega a `EXISTE-SATISFACE`

De las 7 celdas con `regla_existe = SI` (`DIN-03`, `DIN-05`, `DIN-07`, `TIC-01`, `TIC-08`, `TIC-12`, `EMP-05`), ninguna alcanza `EXISTE-SATISFACE`: tres (`DIN-07`, `TIC-01`, `EMP-05`) tienen regla sin que `modelo-decision` §2.1-2.2 le cite un θ explícito (`PORQUE` sin `G#`); una (`DIN-03`) tiene su candidato más fuerte (`familismo_apoyo`, coeficiente dominante de G5) excluido por un precedente de circularidad ya sellado en `milpa/procedencia.yaml` — exactamente el precedente `ENIF p9_9_4` que el encargo anticipa citar; las tres restantes (`DIN-05`, `TIC-08`, `TIC-12`) sí tienen θ candidata (una con cita explícita, `TIC-12`), pero ninguna encuentra operacionalización dentro del instrumento+ola propio de la celda — con la salvedad declarada en `CIV-08`/`TIC-12` de que `envipe2023`/`enoe2024` traen `texto_reactivo` vacío al 100% en este inventario (censura de herramienta, no del instrumento real, A.13).

## B-bis

**0 de 15 celdas `EXISTE-SATISFACE`.** Bajo el umbral `≤2` del propio encargo: **`D1=(i)` no es viable con el corpus abierto hoy** — mesa recibe este número. La firma no obliga a inventar reglas, y este acto no las inventó.

---

## CONTADOR

**0 de 15 celdas con enlace sellable · 0 mini-specs de medición entregadas.**

## Lo que este acto NO hace

No mide. No emite puntos M. No escribe reglas nuevas en el motor ni en el canon. No re-sortea. No descongela. No lee `corridas-R/`. No edita nada de `MAESTRA32-E10` (encargo ni cierre, ambos quedan intactos como historia). No lanza ningún acto de caja sucesor (0 celdas `EXISTE-SATISFACE`, no hay mini-spec que congelar). No relaja el falsador disparado ni busca una sexta regla candidata para las 5 celdas sin cobertura.

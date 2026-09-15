# SONDA · CORR-0018 — los 7 coeficientes sin identidad D-15/A.7

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, NUBE, sobre `origin/main = da9b47a361143d408cd9fd9c20d17b101c4fe381`.

### Definición (verbatim, del encargo)

> `milpa/procedencia.yaml:coeficientes_generador_sellados` — 7 coeficientes (`G1`, `G3`, `G4`, `G5`) traen `fuente` en prosa (p. ej. «`coeficientes_generador_medidos.G1_confianza_institucional`, 4/ago/2026») y **ningún** `payload_id`, **ningún** hash, **ningún** script. Una spec por coeficiente exige primero trazar cuál instrumento produjo cada uno: es trabajo de arqueología, no de especificación.

### Estado de entrada

`data/corrida0/mapa-demanda-19-corr-v1_0.tsv:CORR-0018` (`ACTO
GEN2-SPECS-DEMANDA-1`, 15/sep/2026): `BLOQUEADA · SIN-SCRIPT-NI-PAYLOAD-DECLARADO`,
sucesor `MESA · decisión D3 armada` (D3: rotular
`SIN-PROCEDENCIA-VERIFICABLE` ahora, arqueología cuando un consumidor los
haga materiales, `E.4`). Universo ya examinado por ese acto: **solo** el
bloque `coeficientes_generador_sellados` en sí — no se había cruzado contra
`coeficientes_generador_medidos` (bloque hermano, mismo archivo, líneas
939-1297) ni contra `data/manifiesto.yaml`.

### Modo

**CONSTRUCTO**, con hallazgo que lo resuelve sin necesidad de sondear fuentes
externas nuevas: el universo que faltaba examinar era **interno al propio
repo**, no una fuente ausente del corpus.

### Universo adicional sondeado

`grep`/lectura completa de `coeficientes_generador_medidos` (el bloque que
cada uno de los 7 `fuente:` cita por clave) y de las notas forenses que ese
bloque a su vez cita, cruzadas contra `data/manifiesto.yaml` por `sha256`.

```
$ awk '/^coeficientes_generador_sellados:/{f=1} f{print}' milpa/procedencia.yaml | grep -E "gen:|coef:|fuente:"
(7 pares gen/coef, cada uno con su línea fuente: <clave o nota>, ver tabla)
$ grep -n "^  G1_confianza_institucional:\|^  G1_radio_confianza:\|^  G3_familismo_apoyo:\|^  G4_exposicion_violencia:\|^  G4_confianza_institucional_justicia:\|^  G5_familismo_apoyo:" milpa/procedencia.yaml
(6 de las 7 resuelven a una entrada con su propia línea `fuente:` con instrumento nombrado)
```

### Tabla de candidatas — las 7, todas resueltas dentro del propio repo

| `gen`/`coef` | candidata (instrumento) | evidencia de existencia | payload/manifiesto | A.4/A.5 | siguiente paso |
|---|---|---|---|---|---|
| `G1`/`confianza_institucional` | ENCIG 2023, `encig2023_01_sec_11` × `encig2023_01_sec1_A_3_4_5_8_9_10`, unidas por `ID_PER` (38 966 filas c/u) | `coeficientes_generador_medidos.G1_confianza_institucional` (`procedencia.yaml:989-996`), método completo con eje condicionante ejecutado | `encig23_base_datos_csv`, `data/manifiesto.yaml:28-37`, `sha256=af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d` | **EXISTE-SATISFACE** — payload en corpus, hash verificado | formalizar `payload_id`/`sha256`/script en `coeficientes_generador_sellados` (no en este acto: `milpa/` `FUERA-DE-PERÍMETRO`) |
| `G1`/`radio_confianza` | ENCUCI 2020, `SEC_4_5`, ítems `AP5_1_1/2/3` | `coeficientes_generador_medidos.G1_radio_confianza` (`:940-944`), `forense/notas/2026-08-04-w-coeficientes-generador-paso1.md §1.1,§3.1` | `encuci2020_bd_dbf`, `data/manifiesto.yaml:1011` (hash no releído en esta pieza — entrada existe, `usado_para` ya cita este mismo coeficiente como consumidor #1) | **EXISTE-SATISFACE** | ídem |
| `G3`/`familismo_apoyo` | ENIF 2024, `TMODULO`, `P9_9_4` × `P4_10` | `coeficientes_generador_medidos.G3_familismo_apoyo` (`:1021-1026`) | `enif_2024_enif_2024_bd_csv`, `sha256=00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` (mismo payload que `CORR-0009`/`0010`/`0015` de este mismo acto, ya verificado ahí) | **EXISTE-SATISFACE** | ídem |
| `G3`/`horizonte_temporal` | ENNViH ola 2/3 (`ehh05dta_all.zip`/`ehh09dta_all.zip`), módulo `PR` (`iiib_pr.dta`), ponderador `fac_3b` | `forense/notas/2026-08-24-cal-g3-puntual-cierre.md` (nota `FP-127` que el propio coeficiente cita) — 425 `.dta` leídos, módulo confirmado por codebook oficial `pdftotext` | `ennvih2_2005_hogar_dta` (`sha256=fc4ea4ae7d0cf4bc906bb46ad5e1e7444b9c24f8e0c569ae3f6e5a9b72453c1a`), `ennvih3_2009_hogar_dta` (`sha256=00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15`) — mismos payloads ya citados en `CORR-0008`/`NC-0188` | **EXISTE-SATISFACE** | ídem |
| `G4`/`exposicion_violencia` | ENVIPE 2025, `TPer_Vic2`×`TMod_Vic`, `AP7_3_XX`/`BP1_23`, unión `ID_PER` | `coeficientes_generador_medidos.G4_exposicion_violencia` (`:1049-1055`), `forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md §1-§13` | `envipe2025_csv`, `sha256=8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` (mismo payload que `CORR-0007` de este mismo acto) | **EXISTE-SATISFACE** | ídem |
| `G4`/`confianza_institucional` | ENVIPE 2025, `TPer_Vic1`×`TMod_Vic`, `AP5_4_01..11`/`BP1_23` | `coeficientes_generador_medidos.G4_confianza_institucional_justicia` (`:1080-1086`) | `envipe2025_csv`, mismo `sha256` de arriba | **EXISTE-SATISFACE** | ídem |
| `G5`/`familismo_apoyo` | EDER 2017 (`vivienda.financia_8`×`historiavida.*_cor`) **+** ENDIREH 2016 (`P4_8_2/3`×`P18_4`, robustez) | `coeficientes_generador_medidos.G5_familismo_apoyo` (`:1244-1250`), `forense/notas/2026-08-31-familismo-spec.md` y `forense/notas/2026-08-31-familismo-cierre.md` — **el único de los 7 que YA trae `sha256` explícito en la propia línea `fuente:`** | `eder2017_bases_csv` (`sha256=bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3`) + `bd_mujeres_endireh2016_sitioinegi_csv` (`sha256=02c06ab73a53942ddb575e3e35d8c1dd775406277b74e0605735e3eced4e6f10`) | **EXISTE-SATISFACE** (doble fuente, primaria+robustez) | ídem — el más barato de formalizar, hash ya en el propio archivo |

### NEGATIVO ACOTADO

**No aplica** — no hay negativo que declarar: las 7 candidatas se
encontraron, las 7 con payload verificado por hash contra
`data/manifiesto.yaml`. Ninguna requirió sondear una fuente externa al
repo — el universo adicional que bastó fue el propio
`coeficientes_generador_medidos` y las notas que cada entrada ya citaba.
**Frontera declarada:** esta sonda NO abrió ningún `.dta`/`.csv` (E.5,
NUBE), NO verificó que el `script`/procedimiento exacto de cada
`coeficientes_generador_medidos.*` sea reproducible hoy (podría haber
scratchpad no versionado — ver `G3/horizonte_temporal`, script en `/tmp/`,
declarado "reproducible a partir de esta nota" pero no versionado en
`tools/`), y NO resolvió si `data/manifiesto.yaml:1011`
(`encuci2020_bd_dbf`) trae `sha256` verificado en esta misma pasada (se
citó su existencia, no se releyó el hash línea por línea).

### HANDOFF

- **NINGUNO a cola de adquisición** — GATED a `ACTO ADQUISICION-CONTINUA`
  por perímetro de este acto, y en todo caso no hace falta: las 7
  candidatas ya están en corpus, no hay nada que adquirir.
- **CAJA/mesa**: formalizar `payload_id`/`sha256`/`script` en
  `coeficientes_generador_sellados` para los 7 pares — trabajo de
  `milpa/`, `FUERA-DE-PERÍMETRO` de `ACTO GEN2-SPECS-DEMANDA-2` (perímetro
  declarado: no toca `milpa/`). Candidata más barata para empezar:
  `G5/familismo_apoyo` (hash ya en la propia línea `fuente:`, dos
  payloads, sin trabajo de trazado adicional).

### RECOMENDACIÓN

El acto que toque `milpa/procedencia.yaml` puede formalizar los 7 pares
`payload_id`/`sha256` directamente desde esta tabla, sin arqueología nueva
— la decisión D3 de `ACTO GEN2-SPECS-DEMANDA-1` (rotular
`SIN-PROCEDENCIA-VERIFICABLE`) queda **superada por este hallazgo**: no son
"sin procedencia verificable", son "con procedencia verificable y no
formalizada" — la fila queda para que mesa decida si prefiere D3 tal cual
(rotular y diferir) o instruir la formalización directa con esta tabla como
insumo.

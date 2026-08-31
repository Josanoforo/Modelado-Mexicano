# Nota · ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1 — spec congelada (COMMIT-1)

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-31-reglas-fase1-spec.md` |
> | **QUÉ ES** | Spec B-bis (a)-(e) del encargo, congelada ANTES de abrir un solo payload de datos. |
> | **ENCARGO** | `forense/encargos/2026-08-31-MAESTRA32-E18-REGLAS-OLA5-FASE1.md` |

---

## Verificación previa del gate

El encargo declara: "Estado: GATED a que MAESTRA32-E16 · MEDIDOR-FAMILISMO fusione". Verificado contra el árbol antes de escribir esta spec:

- `git log -1` en la rama al iniciar el acto muestra `commit 42e8f17 Merge: 8d19eaf 68a0570` — *"Merge pull request #406 from Josanoforo/acto/maestra32-e16-medidor-familismo"*.
- `milpa/procedencia.yaml:1189-1230` (`coeficientes_generador_medidos.G5_familismo_apoyo`) ya trae `fuente: "ACTO MAESTRA32-E16, 31/ago/2026 -- eder2017 ... theta=vivienda.financia_8 ... x desenlace=historiavida.{padre_cor,madre_cor,hnos_cor,suegro_cor,suegra_cor}"`.
- `milpa/procedencia.yaml:1123` (`rutas_estimabilidad_coeficiente.detalle`, fila G5·familismo_apoyo) trae *"Paso 3, 31/ago, ADR-235 ... θ con fuente eder2017 financia_8 (ACTO MAESTRA32-E16 ...). β̂ EDER +0.0041, β̂ ENDIREH (robustez, reserva) -0.0461."*

**Gate SATISFECHO.** E16 fusionó (PR #406) antes del inicio de este acto. En consecuencia, `familia.corresidencia.adulto_familiar` (EDER 2017) NO se marca `PENDIENTE-E16` — se trata como candidata medible en la lista cerrada de (b), igual que las otras cuatro.

---

## (a) Plantilla: copia verbatim de `tramite.mordida.discrecional`

`milpa/tramite.yaml:40-50`:

```yaml
  - id: tramite.mordida.discrecional
    situacion: realiza_tramite_gobierno
    si:
      disparadores: {sancion_creible: false, quien_observa: "nadie"}
    entonces:
      - {conducta: paga_mordida, p: 0.62, clase: ASIGNADO}
      - {conducta: tramite_normal, p: 0.38, clase: ASIGNADO}
    porque: {generador: [G1], mecanismo: "trampa social: cada quien paga porque supone que los demás pagan"}
    tier: FUERTE
    falsable_si: "Si al digitalizar y agregar testigos la mordida no baja, no es trampa social sino otra cosa"
    fuente: ["ENCIG2023", "Rothstein_trampa_social", "report:politica"]
```

**Lista cerrada de campos que toda regla nueva debe llenar exactamente:**
`id`, `situacion`, `si.disparadores` (mapa de condiciones), `entonces` (lista de `{conducta, p, clase}`), `porque.generador` (lista), `porque.mecanismo` (texto), `tier`, `falsable_si`, `fuente` (lista).

Regla de llenado (declarada por el propio encargo, objeto): si un campo no se puede llenar desde el dato tal cual está en el árbol (p. ej. `si.disparadores` en términos de θ, que el motor no expone como variable de entrada categórica limpia), el campo se llena con el texto literal `PENDIENTE-DE-MESA` y se declara en esta nota — nunca se inventa una condición lógica que el dato no dicte.

---

## (b) Lista cerrada de reglas fase 1

Cinco candidatas, id en formato `dominio.tema.conducta`:

1. `civico.denuncia.miedo_desconfianza` — ENVIPE 2025, `BP1_23`, universo θ=G4 (exposición a violencia / confianza institucional, ya `MEDIDO` en `coeficientes_generador_medidos.G4_exposicion_violencia`, `procedencia.yaml:994-1024`).
2. `dinero.ahorro.tiene_ahorros` — ENNViH/MxFLS olas 2-3, `cr27`, universo θ=G3.horizonte_temporal ya `MEDIDO` (`procedencia.yaml:1060-1120` y `forense/notas/2026-08-24-cal-g3-puntual-cierre.md`).
3. `familia.apoyo.recibe_dinero_familiares` — ENIF 2024, `TMODULO`, `P9_9_4` ("dinero de familiares" del menú "¿con qué piensa cubrir su vejez?"), universo G3.familismo_apoyo (`procedencia.yaml:300-319`). Nombre de id elegido por el reactivo mismo (`p9_9_4`), declarado — no hay un nombre "oficial" de desenlace más allá del texto del ítem en el FD/cuestionario de ENIF.
4. `familia.corresidencia.adulto_familiar` — EDER 2017, panel `historiavida`, desenlace = corresidencia con algún ascendiente/suegro (`padre_cor∨madre_cor∨hnos_cor∨suegro_cor∨suegra_cor`==1), universo G5.familismo_apoyo, θ=`financia_8` ya `MEDIDO` por ACTO MAESTRA32-E16 (gate satisfecho, ver arriba — **NO** se marca `PENDIENTE-E16`).
5. `tramite.mordida.discrecional` (**enmienda**, no regla nueva) — ENCUCI 2020, desenlace `AP5_17='1' ∨ AP5_18='1'`, universo "con contacto" (`AP5_16_1..10`, al menos un contacto declarado con autoridad/trámite), ponderador `FAC_SEL`. Esta fila se propone como **enmienda propuesta** a la regla existente de `tramite.yaml` (no se toca `tramite.yaml`; la enmienda vive únicamente en el archivo propuesta nuevo, con el mismo `id` y una nota que la marca como candidata a reemplazar/complementar el `p: 0.62` `ASIGNADO`).

Contador: **5 de 5** candidatas de la lista cerrada tienen payload localizado en `data/raw/` y variable de desenlace identificable con nombre exacto — ninguna cae en `PENDIENTE-E16` porque el gate está satisfecho. Ver más abajo si alguna cae en `PENDIENTE-DE-MESA` por otra razón (universo/ponderador no reducible a una sola fila sin ambigüedad).

---

## (c) Por regla: encuesta, ola, payload, universo, ponderador, estimador

### 1. `civico.denuncia.miedo_desconfianza`
- **Encuesta/ola:** ENVIPE 2025.
- **Payload (manifiesto):** `envipe2025_csv` (`data/manifiesto.yaml:306-321`), archivo `data/raw/envipe2025_csv.zip`, `sha256: 8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa`. Tablas internas: `tper_vic2_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic2_envipe2025.csv` (universo, `AP7_3_05..15`, `ID_PER`, `FAC_ELE`), `tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv` (desenlace, `BPCOD`, `BP1_20`, `BP1_23`, `ID_PER`) — confirmado por lectura directa de cabeceras, `2026-08-31`.
- **Universo:** personas 18+ que dispararon `AP7_3_XX='1'` para algún `XX` en `{05,...,15}` (catálogo completo de delito personal) y con `BP1_20=2` (no denunció) para ese delito — mismo universo que `G4_exposicion_violencia` (`procedencia.yaml:997`, `n=13023`), re-derivado en este acto a partir del microdato, no copiado sin verificar.
- **Ponderador:** `FAC_ELE` (persona), de `tper_vic2_envipe2025` — confirmado columna presente, mismo criterio que `forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md §3`.
- **Desenlace:** `BP1_23` dicotomizado `miedo/desconfianza={01,02,06,08}` vs `práctica={03,04,05,07}` (códigos `09`,`99`,blanco excluidos, declarado por `procedencia.yaml:998`).
- **Estimador de p:** proporción ponderada de `desenlace=1` (miedo/desconfianza) sobre el universo definido, ponderando por `FAC_ELE` colapsado a nivel persona (regla de colapso de `procedencia.yaml:1009-1024`: si alguna fila de la persona califica con `BP1_23` en el conjunto miedo/desconfianza, `desenlace=1`).
- **IC95:** bootstrap 10k réplicas, `seed=42`, remuestreo simple por fila de persona (sin campo de diseño UPM/estrato declarado utilizable para HC1 de proporción simple sin regresión — declarado bootstrap, no supuesto de diseño complejo, siguiendo el patrón de `cal-g3-puntual-cierre.md §PASO 0`).

### 2. `dinero.ahorro.tiene_ahorros`
- **Encuesta/ola:** ENNViH/MxFLS, olas 2 (2005-06) y 3 (2009-12) — **ola de calibración de p: ola 2**, la misma que trae el ponderador `fac_3b` usado por la llave `CAL-G3` ya sellada.
- **Payload:** `ennvih_mxfls_licencia` (nota de licencia, `data/manifiesto.yaml:84-95` — **el manifiesto declara literalmente "ningún archivo de ENNViH se ha descargado ni se registra aquí"**, hallazgo del 30/jul/2026). Sin embargo el árbol SÍ tiene los ZIP físicos en `data/raw/ennvih/` (`ehh05dta_all.zip`, con miembro `ehh05dta_b3b/iiib_cr.dta` y `ehh05dta_b3b/iiib_pr.dta` — confirmado por lectura de `zipfile.namelist()`, 2026-08-31) y `data/raw/ennvih/ehh05w_all.zip` (ponderador `fac_3b`). **Hallazgo para el reporte final:** el manifiesto NO tiene una entrada `id:` para estos ZIP de ENNViH pese a que sí están en `data/raw/` y sí se usaron en `CAL-G3-PUNTUAL` (`forense/notas/2026-08-24-cal-g3-puntual-cierre.md`) — inconsistencia de registro preexistente a este acto, no generada por él. Este acto usa el archivo físico y reporta el sha256 real (A.1) en el cierre; no puede citar un `id` de manifiesto que no existe.
- **Universo:** individuos con `pid_link` presente en ambas olas, `pr02` válido (1-7) y `cr27` válido (1/3) en ambas olas simultáneamente, con `fac_3b` no faltante — mismo universo que `CAL-G3-PUNTUAL` (`n=6305`, `cal-g3-puntual-cierre.md` tabla PASO 2). Se reutiliza este universo (no uno más laxo) para que `p` sea comparable a la θ ya sellada de la misma llave.
- **Ponderador:** `fac_3b` (ola 2), `ehh05w_all.zip:ehh05w_all/ehh05w_b3b.dta`.
- **Desenlace:** `cr27` (ola 2) `=1` ("Sí" tiene ahorros) vs `=3` ("No").
- **Estimador de p:** proporción ponderada de `cr27_ola2=1` sobre el universo de `n=6305` (definido arriba), ponderando por `fac_3b`.
- **IC95:** bootstrap 10k réplicas, `seed=42` (mismo criterio de PASO 0 de `CAL-G3-PUNTUAL`: sin campo de diseño UPM/estrato declarado para ENNViH — AGOTADO, ver `cal-g3-puntual-cierre.md §PASO 0`).

### 3. `familia.apoyo.recibe_dinero_familiares`
- **Encuesta/ola:** ENIF 2024.
- **Payload (manifiesto):** `enif2024_csv` (`data/manifiesto.yaml:195-206`), archivo `data/raw/enif2024_csv.zip`, `sha256: a3507b4038888247f565f1640a718ef552bb8fc363378e3372a5bf2796bb2e4c`. **Nota:** el árbol trae DOS payloads ENIF2024 distintos: `enif2024_csv.zip` (id de manifiesto arriba) y `enif_2024_bd_csv.zip` (sin entrada de manifiesto localizada por búsqueda dirigida en este acto — mismo patrón de inconsistencia que ENNViH). Se usa `data/raw/enif_2024_bd_csv.zip` porque es el que trae la tabla `TMODULO.csv` con las columnas exactas citadas por `procedencia.yaml` (`FILTRO_S9_1`, `P9_9_4`, `FAC_PER`, `EDAD_V`) — confirmado por lectura directa de cabecera, 2026-08-31. Su hash se declara en el cierre (A.1); se reporta como hallazgo que el manifiesto no lo cubre con un `id:` propio.
- **Universo:** `FILTRO_S9_1=2` (aplica el módulo de vejez) y `EDAD_V<71` — mismo universo que `procedencia.yaml:304` (`n=12379` declarado ahí; re-derivado en este acto contra el microdato, no copiado sin verificar).
- **Ponderador:** `FAC_PER` (columna confirmada en `TMODULO.csv`).
- **Desenlace:** `P9_9_4='1'` ("dinero de familiares", entre las opciones de con qué piensa cubrir su vejez).
- **Estimador de p:** proporción ponderada de `P9_9_4=1` sobre el universo, ponderando por `FAC_PER`.
- **IC95:** bootstrap 10k réplicas, `seed=42` (ENIF no trae UPM/estrato de diseño verificado en este acto — mismo criterio declarado que las otras reglas; no se re-deriva PASO 0 completo de ENIF por estar fuera del perímetro de este acto, se declara el mismo default conservador).

### 4. `familia.corresidencia.adulto_familiar`
- **Encuesta/ola:** EDER 2017.
- **Payload (manifiesto):** `eder_2017_eder2017_bases_csv` (`data/manifiesto.yaml:4324-4336`), archivo `data/raw/eder2017/eder2017_bases_csv.zip`, `sha256: bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3` — mismo payload ya abierto por `ACTO MAESTRA32-E16` (`tools/medicion_familismo.py`).
- **Universo:** filas de `vivienda.csv` con `tipo_adqui` no blanco (mismo universo que E16, `tools/medicion_familismo.py:112-116`).
- **Ponderador:** `factor` (columna `vivienda.csv`).
- **Desenlace:** persona co-reside con algún ascendiente/suegro — colapso de `historiavida.csv` a nivel persona: `desenlace=1` si en cualquier fila del panel retrospectivo `padre_cor='1' ∨ madre_cor='1' ∨ hnos_cor='1' ∨ suegro_cor='1' ∨ suegra_cor='1'` (mismo colapso que E16, `tools/medicion_familismo.py:86,143-146`).
- **Estimador de p:** proporción ponderada de `desenlace=1` sobre el universo de personas con hogar en el universo `tipo_adqui` no blanco, ponderando por `factor` del hogar de esa persona — **a diferencia de E16 (que calculó la diferencia de proporciones θ=1 vs θ=0), aquí se calcula la tasa base incondicional** (todo el universo, sin condicionar en `financia_8`).
- **IC95:** bootstrap 10k réplicas, `seed=42` (mismo criterio: EDER trae `est_dis`/`upm` de diseño — **si el tiempo del acto lo permite se usa diseño real; si el script no logra construir un estimador de diseño reproducible en la corrida única, se declara bootstrap simple y se dice así explícitamente en el cierre**, siguiendo "el primer resultado que produzca este procedimiento es el que se reporta").

### 5. `tramite.mordida.discrecional` (enmienda ENCUCI)
- **Encuesta/ola:** ENCUCI 2020.
- **Payload (manifiesto):** `encuci2020_bd_dbf` (`data/manifiesto.yaml:992-1021`), archivo `data/raw/BD_ENCUCI2020_dbf.zip`. Sha256 se recalcula y compara contra manifiesto en el cierre (A.1).
- **Universo:** filas de `ENCUCI_2020_SEC_4_5.dbf` con contacto declarado (`AP5_16_1..10`, al menos uno `='1'`) — mismo universo que `G1_radio_confianza` (`procedencia.yaml:888-889`, `n≈13435` de `21519`), re-derivado contra el microdato.
- **Ponderador:** `FAC_SEL` (columna confirmada en `ENCUCI_2020_SEC_4_5.dbf`).
- **Desenlace:** `AP5_17='1' ∨ AP5_18='1'`.
- **Estimador de p:** proporción ponderada de `desenlace=1` sobre el universo de contacto, ponderando por `FAC_SEL`.
- **IC95:** bootstrap 10k réplicas, `seed=42` (mismo criterio declarado que las demás — ENCUCI no trae campo de diseño verificado en este acto, no se re-deriva PASO 0 completo, fuera de perímetro).

---

## (d) `ola_calibracion` y `clase`

Para las cinco reglas: `clase: "MEDIDO·p(tasa base ponderada)"`. `ola_calibracion` es la ola de la que sale `p` — declarada explícitamente por regla en (c) arriba (ENVIPE 2025 única ola; ENNViH ola 2 (2005-06); ENIF 2024 única ola; EDER 2017 única ola; ENCUCI 2020 única ola).

---

## (e) B-bis — candidatos de marco-M

Cada regla propuesta con `p` medida es candidata nueva de marco-M: `P0` en su propia ola de calibración, `P1` en otras olas por el criterio D-D (criterio no re-derivado aquí, solo aplicado por nombre — la adjudicación P0/P1 real de marco-M es de mesa, este acto solo cuenta cuántas celdas *habilitaría*, sin sellar nada).

Conteo de celdas de transferencia que cada regla habilitaría, contra el inventario de dominios/olas del motor (`milpa/tramite.yaml`: dominio `tramite` ya tiene 5 reglas; dominios `civico`, `dinero`, `familia` están vacíos hoy — 0 reglas en `tramite.yaml` con esos prefijos, verificado por `grep "^  - id: civico\.\|^  - id: dinero\.\|^  - id: familia\." milpa/tramite.yaml` → vacío):

| regla | dominio del motor | ¿dominio vacío hoy? | celdas de transferencia habilitadas (P0 propio + P1 nominal en las otras 4 olas de calibración de este acto) |
|---|---|---|---|
| `civico.denuncia.miedo_desconfianza` | `civico` | SÍ (0 reglas) | 1 P0 (ENVIPE 2025) + hasta 4 P1 nominales (ENNViH, ENIF, EDER, ENCUCI) = 5 |
| `dinero.ahorro.tiene_ahorros` | `dinero` | SÍ (0 reglas) | 1 P0 (ENNViH ola2) + hasta 4 P1 = 5 |
| `familia.apoyo.recibe_dinero_familiares` | `familia` | SÍ (0 reglas) | 1 P0 (ENIF 2024) + hasta 4 P1 = 5 |
| `familia.corresidencia.adulto_familiar` | `familia` | SÍ (0 reglas; comparte dominio con la anterior) | 1 P0 (EDER 2017) + hasta 4 P1 = 5 |
| `tramite.mordida.discrecional` (enmienda) | `tramite` | NO (5 reglas ya existen; esto enmienda, no abre dominio) | 0 nuevas (enmienda a fila existente) |

**Dominios del motor que dejarían de estar vacíos si mesa sella: hasta 3 (`civico`, `dinero`, `familia`)** — coincide con el CONTADOR declarado por el propio encargo. Este conteo es un inventario, no una propuesta de que marco-M efectivamente adopte las 20 celdas nominales — esa adjudicación P0/P1 real queda para el sucesor `MARCO-M-CONGELA-v1_1 (A″)` citado por el encargo.

---

**"El primer resultado que produzca este procedimiento es el que se reporta."**

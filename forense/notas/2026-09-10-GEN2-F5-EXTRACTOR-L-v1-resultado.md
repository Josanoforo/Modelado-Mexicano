# `ACTO GEN2-F5-EXTRACTOR-L-v1` — resultado del instrumento

**Esto NO es un veredicto del duelo.** Este acto construye y sella un
extractor de `valor_extraido` para el formato real de `corridas-L/
*__v1_3.json` y lo aplica a las 224 capturas. No calcula quién gana la
pareada primaria (TRANSFERENCIA) — eso sigue perteneciendo al `ENCARGO 5/5`
(sucesor `GEN2-F5-TRIADA-CALC`), que consumirá el TSV/manifiesto que este
acto sella como insumo, junto con el marco `R` y el snapshot `M` que el
propio encargo exige.

**Fecha:** 10/sep/2026 · **Entorno:** NUBE, cero microdato/cero red, cero
llamadas nuevas a Claude · **Base:** `origin/main = eab46ed24a60ff94835831698648ca8df1c07da7`
(`PR #674` fusionado) · **Encargo:** `forense/encargos/2026-09-10-GEN2-F5-EXTRACTOR-L.md`
(A.3, verbatim).

## 1 · El instrumento (P1, COMMIT-1 + ENMIENDA)

`tools/extrae_l_v1_3.py`, sucesor de `tools/extrae_l_v1_1.py` (histórico, no
editado). Regla completa en
`forense/prereg-duelo-v2/regla-extraccion-L-v1_3.md`. Resumen: dos familias
de ancla estructural/textual (encabezado Markdown `estimaci...`, y las
frases fijas "estimación puntual" / "mi punto" / "punto central"); **cero**
fallback de "primer número del documento"; anclas en conflicto (número
contra rechazo, o dos números distintos) resuelven `AMBIGUA`, nunca una
elección posterior a verlas; identidad (`id_celda`/`variante`/`indice`
dentro del JSON, contra el nombre de archivo y contra el manifiesto sellado
de `F5-RECAPTURA-L`, incluido su `sha256`) verificada antes de intentar
extracción — una discrepancia es `ERROR-IDENTIDAD`, un fallo material, no
una no-extracción.

19 pruebas dirigidas (`forense/prereg-duelo-v2/tests_extrae_l_v1_3.py`),
congeladas antes de correr sobre el universo completo, todas en verde:

- **Controles negativos obligatorios** (los tres ejemplos de contaminación
  que `PR #674`/`NC-0142` midieron a mano): `CIV-M-12__L-solo__01`,
  `CIV-M-13__L+corpus__04`, `CIV-M-01__L+corpus__02` — los tres vuelven
  `NO-EXTRAIBLE` vía `ANCLA-RECHAZO`. Ninguno vuelve a producir la "cifra
  negra" de contexto (0.90–0.94) que `tools/extrae_l_v1_1.py` capturaba.
- **Controles positivos** sobre formas reales con punto comprometido
  (encabezado `## Estimación` con `≈N%`, frase-ancla con "mi punto"
  desempatando un rango, tabla con "Abstención").
- **Sintéticos** (ausencia total de ancla, anclas en conflicto, rango sin
  punto declarado) e **identidad** (captura íntegra, JSON alterado,
  archivo fuera del manifiesto).
- **Independencia**: `tools/extrae_l_v1_3.py` no referencia `CALC-R`,
  `corridas-R` ni `CALC-DUELO` en su código ejecutable (verificado por
  `ast`, excluyendo el docstring de módulo que los menciona en prosa para
  declarar precisamente que no los abre).

Durante la corrida real sobre las 224 capturas (antes de comprometer este
P2) el propio instrumento atrapó dos defectos de identificación de formato
—ninguno dependiente de `R`/`M`, que no se abrieron— corregidos por una
ENMIENDA fechada al mismo P1 (ver el commit de esa enmienda): un párrafo de
"Razonamiento y calibración" que citaba una cifra histórica de contexto
dentro de una sección de encabezado "estimaci..." (dos falsos `AMBIGUA`,
`FAM-M-05`), y la forma conjugada "me abstengo" ausente del vocabulario de
rechazo (un caso mal etiquetado, mismo estado final). Un tercer efecto,
correcto y no buscado: con "me abstengo" reconocido, una captura que decía
literalmente *"Estimación puntual: me abstengo. Cualquier cifra que diera
(p. ej. ~30%) sería una fabricación plausible"* pasó de `EXTRAIBLE=0.30`
(la cifra hipotética de fabricación, capturada por error antes del fix) a
`AMBIGUA` — la clase exacta de contaminación que este acto existe para
evitar, atrapada por la propia regla antes de tocar el commit final.

## 2 · Ejecución sobre las 224 capturas (P2, COMMIT-2 — no edita P1)

`python3 tools/extrae_l_v1_3.py`, salida cruda:

```
total capturas examinadas: 224
por estado:
  EXTRAIBLE: 56
  NO-EXTRAIBLE: 164
  AMBIGUA: 4
  ERROR-IDENTIDAD: 0
distribucion de regla_de_extraccion:
  ANCLA-FRASE-PUNTO: 52
  ANCLA-HEADER-PUNTO: 4
  ANCLA-RECHAZO: 48
  ANCLAS-EN-CONFLICTO: 4
  SIN-ANCLA: 116
```

**Cobertura por brazo** (sobre el universo completo, no solo sobre
extraíbles): `L-solo`: 75 NO-EXTRAIBLE, 33 EXTRAIBLE, 4 AMBIGUA (n=112).
`L+corpus`: 89 NO-EXTRAIBLE, 23 EXTRAIBLE, 0 AMBIGUA (n=112).

**Cobertura por celda** — hallazgo central, que hereda y confirma lo que
`NC-0142` ya había medido a mano sobre tres ejemplos: **las 6 celdas con
árbitro `R` (`CIV-M-01/02/04/10/12/13`) vuelven 96/96 `NO-EXTRAIBLE`, 0
`EXTRAIBLE`, 0 `AMBIGUA`.** No es que el instrumento nuevo falle sobre
ellas — es que, verificado ahora de manera exhaustiva y no solo en tres
ejemplos, las 96 capturas reales de esas 6 celdas son, sin excepción,
rechazos explícitos de estimación (el modelo no identifica el reactivo
`denuncia_con_miedo_o_desconfianza` como existente en el cuestionario de la
ENVIPE con ese nombre, en ninguna de las 96). Las 8 celdas restantes
(`DIN-M-01`, `FAM-M-01/05/06/07`, `TRA-M-02/03/07`) sí producen respuestas
extraíbles en su mayoría — esas celdas no tienen árbitro `R` en el marco
actual y quedan fuera del universo pareado del duelo por construcción
(mismo límite que `F5-duelo-contemporaneo-spec-v1_0.md` §5 ya declaraba).

**Cobertura por réplica**: sin patrón — las 8 réplicas de cada (celda,
variante) se reparten de forma similar entre estados (ver el TSV completo
para el detalle exacto por réplica).

**Controles de P2, verificados**:
- *Positivo*: ejemplos claros (encabezado + `≈N%`, tabla con "Abstención")
  producen el valor/estado respaldado por su evidencia — confirmado por las
  pruebas dirigidas §1.
- *Negativo*: los tres ejemplos contaminados de `#674` no vuelven a devolver
  la cifra contextual incorrecta — confirmado, los tres `NO-EXTRAIBLE`.
- *Independencia*: confirmado por `ast` sobre el código ejecutable (§1) y
  por construcción — este acto no abrió `data/corrida0/CALC-R-*/`,
  `corridas-R/` ni `data/corrida0/CALC-DUELO-*/` en ningún paso.

## 3 · Producto sellado para el duelo (P3)

`forense/prereg-duelo-v2/L-extraido-v1_3.tsv` (224 filas: `id_celda ·
variante · replica · estado · valor_extraido · evidencia_textual ·
regla_de_extraccion · razon_no_extraible · archivo`) y
`forense/prereg-duelo-v2/manifiesto-extraccion-L-v1_3.json`, con:

- `extractor_sha256` (hash de `tools/extrae_l_v1_3.py` tal como corrió) —
  `ecfbd8491f9b353d…` (ver el archivo para el hash completo).
- `manifiesto_capturas_sha256` (hash del manifiesto sellado de
  `F5-RECAPTURA-L` que sirvió de insumo para la verificación de identidad)
  — `93f1ffdaa9a810ad…`.
- El resumen de cobertura de §2, embebido íntegro.
- Estado y regla de extracción por cada una de las 224 capturas.

**No se calcula aquí quién gana.** El siguiente paso mecánico —re-lanzar la
pareada primaria del duelo sobre las 6 celdas con árbitro, usando este TSV
en vez de `tools/extrae_l_v1_1.py`— es del `ENCARGO 5/5`. Este acto declara,
sin adjudicar: sobre las 6 celdas que importan para esa pareada, el
instrumento validado devuelve **0/96 `EXTRAIBLE`** — no hay, hoy, ningún
punto numérico defendible que oponer a `R` en esas 6 celdas. Eso no es un
defecto del instrumento (los controles de §1 lo confirman contra formas
reales y contra los tres contaminantes conocidos): es lo que el modelo
efectivamente respondió, medido sin el sesgo del extractor viejo.

## 4 · Límites, declarados sin adornos

- **No adjudica.** Este acto no calcula `dif_abs_pareada`, no compara contra
  `R`, y no toca `CALC-DUELO-0001/` ni ningún resultado del duelo.
- **0/96 EXTRAIBLE en las celdas con árbitro** significa que, si el
  `ENCARGO 5/5` re-lanza la pareada primaria con este instrumento, el
  universo pareado disponible para TRANSFERENCIA sobre esas 6 celdas será
  vacío o casi vacío — una limitación real del dato (el modelo se abstiene
  sistemáticamente en este reactivo), no algo que este acto pueda resolver
  inventando una regla de extracción más permisiva. La firma de mesa de
  este encargo prohíbe explícitamente eso: *"inventar una cifra para
  completar cobertura está prohibido."*
- **4 `AMBIGUA`** son casos donde el propio modelo da dos (o más)
  estimaciones condicionadas a interpretaciones distintas del reactivo
  (p. ej. "si es experiencia directa: ~12.6%; si es percepción: ~70-90%")
  sin que el formato permita elegir mecánicamente cuál corresponde al
  reactivo pedido — verificado a mano contra 3 de los 4 casos
  (`FAM-M-06__L-solo__07`, `TRA-M-03__L-solo__04`, `TRA-M-07__L-solo__07`).
- **116 `SIN-ANCLA`** incluye casos con rechazos genuinos sin ninguna de las
  frases-ancla fijas (p. ej. "no lo sé" sin decir "estimación puntual" ni
  usar un encabezado) — el mismo estado final (`NO-EXTRAIBLE`) que
  `ANCLA-RECHAZO`, solo que sin una frase-ancla reconocible; no se amplía el
  vocabulario de anclas después de ver este número, por la misma regla que
  prohíbe elegir reglas de agregación después de ver resultados.

## 5 · `NC-0142` — cierre parcial (componente instrumental)

`NC-0142` se abrió por *"el único extractor de valor_extraido... no está
validado contra el formato real-corpus"*. Ese componente instrumental
**CIERRA con este acto**: existe ahora un extractor validado contra el
formato real de `corridas-L/*__v1_3.json`, con controles negativos que
confirman que no repite la contaminación medida por `#674`. El componente
de **adjudicación** de la pareada primaria (GANA/PIERDE/EMPATE/INCONCLUSO
contra la escala B-bis) sigue sin correr — eso pertenece al `ENCARGO 5/5`
(sucesor `GEN2-F5-TRIADA-CALC`), y con el hallazgo de §3 (0/96 `EXTRAIBLE`
en las celdas con árbitro), ese acto puede encontrar que la pareada sigue
sin universo suficiente — una posibilidad declarada aquí, no resuelta.

## 6 · Sucesores

- **`ENCARGO 5/5` (`ACTO GEN2-F5-TRIADA-CALC`)**: re-lanzar la pareada
  primaria TRANSFERENCIA usando `L-extraido-v1_3.tsv` en vez del extractor
  viejo, cuando también existan el marco `R` y el snapshot `M` que ese
  encargo exige. Puede encontrar universo pareado vacío en las 6 celdas con
  árbitro (§3) — ese hallazgo, si ocurre, es del sucesor, no de este acto.
- **Si se quiere ampliar cobertura de las 8 celdas sin árbitro** (`DIN-M-01`,
  `FAM-*`, `TRA-*`): fuera de perímetro de este acto; el instrumento ya las
  cubre (las 56 `EXTRAIBLE` del universo completo caen todas dentro de
  estas 8 celdas, de 128 capturas posibles), no requiere trabajo adicional
  del extractor.

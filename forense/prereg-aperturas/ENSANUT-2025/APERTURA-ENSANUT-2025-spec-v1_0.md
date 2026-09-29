# Expediente de apertura · ENSANUT 2025 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (28/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [EJECUTADO] Ids reservados de la ola: fila `ENSANUT 2025` de `data/corrida0/aperturas-pendientes-v1_0.tsv`
  (derivada por `forense/prereg-aperturas/inventario_aperturas.py`, campo `estado_reserva` del manifiesto).
- [LEÍDO] Contendientes sellados (regla 6: ningún contendiente nuevo; E.6: una apertura sirve a todos los sellados antes):
  (1) `CALC-ENSANUT-PISOS-SALUD-0001` — piso 2024 con IC calibrado de persistencia ICC-LO/ICC-HI (spec `forense/prereg-caja/SALUD-ENSANUT-PISOS-spec-v1_0.md` §4), 13 conductas, `ola_reservada: ENSANUT 2025 (no es input)`.
  (2) `CALC-MC2-ENSANUT2024-0001` — pisos descriptivos 2024 (tipo `PISO-DESCRIPTIVO-RETROSPECTIVO`, acto GEN2-MEDICION-CARRILES-2; spec `forense/prereg-caja/MC2-ENSANUT2024-spec-v1_0.md`), 46 celdas con P, IC95-INF, IC95-SUP (bootstrap de UPM dentro de `est_sel`, 2 000 réplicas) y N; `spec.yaml` l.14 `ola_reservada: ENSANUT 2025 (no es input)`. Entró al fusionar origin/main (COMMIT-1 `883b869f`, COMMIT-2 `58899dba`, 28/sep); medidor sha `11e22394…dc6c` y `resultados.json` sha `69c41814…cf3c` = `sello.json`. Su medidor no importa receta del repo (sólo os, tempfile, zipfile, numpy, pandas; pyreadstat dentro de `_lee_dta`).
- [EJECUTADO] Duplicados entre contendientes: `RESULT-MC2-ENSANUT2024-BUSCO-{NAC,RURAL,URBANO,METRO}-P` y `RESULT-ENSANUT-PISOS-SALUD-BUSCO-ATENCION-2024-{TOTAL-TODOS,ESTRATO-RURAL,-URBANO,-METROPOLITANO}-P` coinciden a ≤ 1e-16 en los dos `resultados.json` sellados (2024, ola vista). Mismo estimando (h0404 = 1 vs 2 | h0401 = 1), mismo archivo, mismo filtro de diseño y mismo estrato 1/2/3; la única diferencia textual es que PISOS-SALUD exige edad `h0303` finita (inerte en 2024, según la coincidencia).
- [SUPUESTO→rama prevista] Mismo rol de archivo para MC2: 2024 `integrantes_ensanut2024_w_icb` (carpeta del portal «02-Información sobre los residentes») → 2025 `integrantes_2025_w` (misma carpeta); 2024 `adultos_ensanut2024_w` → 2025 `adultos_2025_w`. Los dos ya son payloads de este expediente: **no se añade ningún payload**. El `ensanut2025_icb` (carpeta «03-Indice de bienestar») no se usa. Si las columnas de MC2 no están en `integrantes_2025_w`, sus celdas salen NO-ESTIMABLE (§5), no se busca otro archivo.
- [EJECUTADO] Ninguna familia 2027 la usa como R (`familias-2027-estado-v1_0.tsv`: las 8 familias apuntan a olas 2027).
- [SUPUESTO→rama prevista] El cuestionario y el catálogo de 2025 están en el manifiesto como documentación,
  pero este acto corre en NUBE sin corpus montado: los códigos se fijan **sobre el cuestionario de la ola
  del piso** (la tabla del CALC contendiente), rotulado así; la diferencia se declara al abrir (§5).

## 1 · Estimandos

**PISOS-SALUD** (celdas `<conducta>-<eje>-<cat>`, conglomerado = conducta). Por cada conducta del contendiente y cada categoría de cada eje (TOTAL; SEXO; EDAD; ESTRATO; ESCOLARIDAD
donde el contendiente la tiene): **R = Σw·y / Σw** en ENSANUT 2025, con la misma recodificación 1/0/fuera
del contendiente (su spec §2 y su medidor sellado, importado por bytes con sha256 fijado en `APERTURA-ENSANUT-2025-spec.yaml`).
IC del contendiente: ICC-LO/ICC-HI 2024; punto: P 2024.

**MC2** (celdas `MC2-<celda>`, conglomerado = `CALC-MC2-ENSANUT2024-0001`). Por cada celda de nivel de su medidor
sellado (`celdas_inte`, `celdas_adul`), **R = Σw·y / Σw** en ENSANUT 2025 con su recodificación verbatim
(`frame_inte`, `frame_adul`, importados por bytes con sha fijado): y y universo de cada celda son los suyos —
BUSCO (h0404 1/2 | h0401 = 1); BUSCO-MENTAL (lo mismo | h0402 ∈ {47, 48, 50, 59}); ACCESO (algún H0405A-C ∈ {2, 3, 4} | no buscó con algún motivo 01–13); NO-GRAVE (algún motivo = 1 | ídem); DM-SUSPENDE (a0313 1/2 | 20+ con a0301 = 1 y a0307 ∈ 1–3); DM-ECON-ACCESO (a0314 ∈ {5, 6, 7, 10} | suspendió con a0314 válido); DM-PAGA (a0310a > 0 | tratado con 0 ≤ a0310a < 99 999) —
por segmento NAC, RURAL, URBANO, METRO, NORURAL (estrato 2|3), HOMBRE, MUJER, EDAD 0-19/20-59/60-MAS, PAGA, NOPAGA según la celda.
IC del contendiente: **IC95-INF/IC95-SUP que MC2 publica para 2024** (su última ola; bootstrap de diseño, no IC de
persistencia); punto: su P 2024. Las 46 celdas de MC2 con IC: 39 de nivel + 7 diferencias.
**Entran 35** (Σ = 167 de PISOS-SALUD + 35 de MC2 = 202 celdas). **Apartadas sin abrir (11)**, sin R calculada:
- 4 duplicados de PISOS-SALUD (mismo estimando, mismo universo; §0): `MC2-BUSCO-NAC` ≡ `BUSCO-ATENCION-TOTAL-TODOS`,
  `MC2-BUSCO-RURAL` ≡ `…-ESTRATO-RURAL`, `MC2-BUSCO-URBANO` ≡ `…-ESTRATO-URBANO`, `MC2-BUSCO-METRO` ≡ `…-ESTRATO-METROPOLITANO`.
  Su R es la de la celda de PISOS-SALUD, que ya entra; contarlas dos veces duplicaría la misma R. `MC2-BUSCO-NORURAL` sí entra (PISOS no tiene esa categoría).
- 7 diferencias (`BUSCO-DIF-RURAL-METRO`, `BUSCO-DIF-RURAL-NORURAL`, `ACCESO-DIF-RURAL-METRO`, `ACCESO-DIF-RURAL-NORURAL`,
  `ACCESO-MENOS-NOGRAVE-NAC`, `BUSCO-MENTAL-DIF-RURAL-NORURAL`, `DM-SUSPENDE-DIF-PAGA-NOPAGA`): cada una es contraste
  lineal de dos celdas que ya entran (misma R dos veces) y su escala es diferencia en [−1, 1], no proporción (§4 A-bis: escala declarada).

## 2 · Universo, unidad, ponderador, diseño

Unidad persona (los dos contendientes). Cuatro archivos (adultos 20+, integrantes todas las edades, utilizadores, adolescentes 10–19), ponderador `ponde_f`, registro válido `ponde_f > 0` con `est_sel` y `upm` no vacíos; escolaridad de adultos y utilizadores por llave `folio_i+folio_int` contra integrantes (la de `prepara()` del contendiente).
Payloads (ids del manifiesto): `ensanut_2025__adultos_2025_w_stata_stata_zip`, `ensanut_2025__integrantes_2025_w_stata_stata_zip`, `ensanut_2025__utilizadores_2025_w_stata_stata_zip`, `ensanut_2025__adolescentes_2025_w_stata_stata_zip`.
Celdas MC2: los dos archivos que MC2 lee en 2024 tienen su par 2025 en esta lista (integrantes, adultos; §0);
registro válido el de su `_estima`: `ponde_f` finito > 0, `est_sel` y `upm` no vacíos; sin filtro de edad salvo el de la celda (DM: 20+).
Una lectura por archivo con la **unión** de las columnas de los dos contendientes (MC2 añade `h0402`, `H0405A-C` en
integrantes y `a0307`, `a0310a`, `a0313`, `a0314` en adultos); el marco leído se entrega a la recodificación de MC2
en lugar de su `_lee_dta` (misma semántica que `lee_dta` de la receta: miembro .dta único, nombres sin distinguir
mayúsculas, `apply_value_formats=False`, minúsculas; LEÍDO `tools/dominios/salud/pisos_diseno.py` l.50-71 y medidor MC2 l.48-66).
R es un punto; no se calcula IC de R (la cobertura se mide contra el IC del contendiente).

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo:
`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera
de `lee_payload_reservado` → PARO. Celdas MC2: una llamada a `proporcion_por_grupo` por celda sellada, con UNA
variable de agrupación = el indicador de pertenencia a la celda (su máscara sellada: segmento dentro del universo de
la celda, p. ej. RURAL ∧ necesidad de salud mental en `BUSCO-MENTAL-RURAL`, dentro del diseño válido). Es la celda
pre-registrada por MC2, no un cruce nuevo: no se calcula ninguna otra combinación. Los diagnósticos internos
de `frame_inte`/`frame_adul` (conteos) se calculan dentro del código sellado y se descartan: no se emiten. Probado por mutación sobre sintético con el esquema de la ola:
`tests/test_prereg_aperturas.py` (las 9 mutaciones de `expediente_apertura.MUTACIONES` + borrado de la llamada a la auditoría; `corrida0._valida_outputs` sobre cada rama terminal de la adjudicación) y `tests/test_apertura_salud_2025.py` (sintético con el esquema de la ola: con soporte, conducta sin soporte, categoría vacía; y para MC2: con soporte, motivos/suspensión sin soporte, categoría vacía, reactivo ausente vacío y diseño ausente PARO, R = punto de `_estima` sellado sobre el mismo sintético, apartadas fuera del esquema).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. **Primaria** (una sola, sobre TODAS las celdas puntuadas de
los dos contendientes, hasta 202): cobertura k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson;
**SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Si dos
filas pudieran satisfacerse a la vez, manda el orden NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO
(son excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por conglomerado
(conducta de PISOS-SALUD; `CALC-MC2-ENSANUT2024-0001` para todas las MC2 — comparten muestra) y error absoluto medio punto-del-contendiente vs R.
El IC de MC2 es de diseño (incertidumbre muestral de 2024), no de persistencia: se espera más estrecho que el ICC de
PISOS-SALUD; esa diferencia se declara aquí, antes de abrir, y no cambia la regla ni el umbral.
B-bis: si el piso NO falla (CALIBRADO), el piso queda **corroborado en alcance** para esta ola; SOBRECUBRE
= piso **acotado** (IC conservador); SUBCUBRE = el piso no anticipa la ola.
Una apertura sirve a todos los sellados antes: `CALC-ENSANUT-PISOS-SALUD-0001` y `CALC-MC2-ENSANUT2024-0001`
(censo EJECUTADO: `grep -l "ENSANUT 2025" data/corrida0/CALC-*/spec.yaml` sobre 394 `spec.yaml` → 2, los dos con `ola_reservada: ENSANUT 2025 (no es input)`).
Lo imaginable se declara junto (§1) con UNA primaria; lo apartado sin abrir, en §1 con su razón.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- 2024 separó integrantes con sufijo `_icb`; 2025 trae `integrantes_2025_w` y un archivo aparte `ensanut2025_icb`: se usa `integrantes_2025_w` (mismo rol), declarado.
- 2025 añade archivos (menores, casa por casa, antropometría, frecuencias, lactancia, actividad física) que ningún contendiente usa: fuera.
- MC2 leyó en 2024 el integrantes con sufijo `_icb`; en 2025 usa `integrantes_2025_w` (§0). Si `h0402` o `H0405A-C`
  faltan ahí, sus celdas salen NO-ESTIMABLE; si faltan `a0307`/`a0310a`/`a0313`/`a0314` en adultos, lo mismo.

Regla fijada: si en caja, antes de correr, el catálogo de 2025 no trae una columna del contendiente con el
mismo texto de pregunta y códigos, **esa conducta sale NO-ESTIMABLE** (se omite R; no se recodifica ad hoc)
y se declara en la nota de apertura. Leer el catálogo y el cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENSANUT-2025-<conducta>-<eje>-<cat>-R` (167), `RESULT-APERTURA-ENSANUT-2025-MC2-<celda>-R` (35), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`,
`-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.

Contrato: `APERTURA-<X>-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-<X>-0001`; payloads con sha del manifiesto;
medidores sellados de los dos contendientes, sus `resultados.json`, la receta y la guardia como inputs `origen: repo` con sha;
`dependencias_materiales` numpy, pandas, pyreadstat).
La apertura es copiarlo a `data/corrida0/CALC-APERTURA-<X>-0001/spec.yaml` y correr (receta).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción, para los dos contendientes: cada uno se selló antes de que exista la R (sello del CALC contendiente anterior a cualquier apertura de la ola; la ola sigue RESERVADA en `data/manifiesto.yaml`). Ninguna frase mezcla esta cobertura con marcadores RETROSPECTIVOS. MC2 se rotuló RETROSPECTIVA para su propio estimando (describir 2024, ola vista); frente a 2025 su emisión es anterior a R y la cobertura es PROSPECTIVA; sus dictámenes B-bis 2024 no se tocan ni se mezclan con esta.
- Unidad: **persona** en R y en los dos contendientes (integrante o adulto); nada se promedia con unidades hogar, delito o trámite.
- Escala: proporción 0..1 en R y en los dos contendientes (las diferencias de MC2, escala [−1, 1], quedan apartadas); se compara «R dentro del IC del piso» (cobertura), no punto contra punto; el MAE de punto es descriptivo.
- Segmentación: un eje a la vez (sexo, edad, estrato de tamaño de localidad, escolaridad); ningún cruce — la guardia lo impide. El estrato rural/urbano/metropolitano es tamaño de localidad, no clase: el sesgo de clase media urbana no se corrige aquí y se declara.
- Pobreza, acceso y oferta de servicios confunden conductas de uso de servicios (atención, farmacia, curandero; en MC2 motivos de no búsqueda, pago y abandono de tratamiento): se leen como oferta antes que preferencia (§3), nunca como cultura; ACCESO y DM-ECON-ACCESO son medidas de exclusión por oferta/precio, no de actitud.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «la salud del mexicano cambió»; dice que el piso de la ola anterior, con su IC, no anticipa la ola nueva en esa proporción de celdas. Un IC95 de diseño 2024 (MC2) que no cubre R 2025 no es un error del estimador de 2024: su IC no fue construido para predecir otra ola; la cobertura por conglomerado lo separa.
- Cifras escritas a mano: ninguna; las constantes del medidor son hashes fijados y umbrales de la regla (0.95 nominal, z = 1.959964), declarados antes de abrir.

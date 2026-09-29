# Expediente de apertura · ENSANUT 2025 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (28/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [EJECUTADO] Ids reservados de la ola: fila `ENSANUT 2025` de `data/corrida0/aperturas-pendientes-v1_0.tsv`
  (derivada por `forense/prereg-aperturas/inventario_aperturas.py`, campo `estado_reserva` del manifiesto).
- [LEÍDO] Contendiente sellado (regla 6: ningún contendiente nuevo): `CALC-ENSANUT-PISOS-SALUD-0001` — piso 2024 con IC calibrado de persistencia ICC-LO/ICC-HI (spec `forense/prereg-caja/SALUD-ENSANUT-PISOS-spec-v1_0.md` §4), 13 conductas, `ola_reservada: ENSANUT 2025 (no es input)`.
- [EJECUTADO] Ninguna familia 2027 la usa como R (`familias-2027-estado-v1_0.tsv`: las 8 familias apuntan a olas 2027).
- [SUPUESTO→rama prevista] El cuestionario y el catálogo de 2025 están en el manifiesto como documentación,
  pero este acto corre en NUBE sin corpus montado: los códigos se fijan **sobre el cuestionario de la ola
  del piso** (la tabla del CALC contendiente), rotulado así; la diferencia se declara al abrir (§5).

## 1 · Estimandos

Por cada conducta del contendiente y cada categoría de cada eje (TOTAL; SEXO; EDAD; ESTRATO; ESCOLARIDAD
donde el contendiente la tiene): **R = Σw·y / Σw** en ENSANUT 2025, con la misma recodificación 1/0/fuera
del contendiente (su spec §2 y su medidor sellado, importado por bytes con sha256 fijado en `APERTURA-ENSANUT-2025-spec.yaml`).

## 2 · Universo, unidad, ponderador, diseño

Unidad persona. Cuatro archivos (adultos 20+, integrantes todas las edades, utilizadores, adolescentes 10–19), ponderador `ponde_f`, registro válido `ponde_f > 0` con `est_sel` y `upm` no vacíos; escolaridad de adultos y utilizadores por llave `folio_i+folio_int` contra integrantes (la de `prepara()` del contendiente).
Payloads (ids del manifiesto): `ensanut_2025__adultos_2025_w_stata_stata_zip`, `ensanut_2025__integrantes_2025_w_stata_stata_zip`, `ensanut_2025__utilizadores_2025_w_stata_stata_zip`, `ensanut_2025__adolescentes_2025_w_stata_stata_zip`.
R es un punto; no se calcula IC de R (la cobertura se mide contra el IC del contendiente).

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo:
`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera
de `lee_payload_reservado` → PARO. Probado por mutación sobre sintético con el esquema de la ola:
`tests/test_prereg_aperturas.py` (las 9 mutaciones de `expediente_apertura.MUTACIONES` + borrado de la llamada a la auditoría; `corrida0._valida_outputs` sobre cada rama terminal de la adjudicación) y `tests/test_apertura_salud_2025.py` (sintético con el esquema de la ola: con soporte, conducta sin soporte, categoría vacía).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con
lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson;
**SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Si dos
filas pudieran satisfacerse a la vez, manda el orden NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO
(son excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por conglomerado
(conducta: las celdas de una conducta comparten muestra) y error absoluto medio punto-del-piso vs R.
B-bis: si el piso NO falla (CALIBRADO), el piso queda **corroborado en alcance** para esta ola; SOBRECUBRE
= piso **acotado** (IC conservador); SUBCUBRE = el piso no anticipa la ola.
Una apertura sirve a todos los sellados antes: el único contendiente sellado es `CALC-ENSANUT-PISOS-SALUD-0001`; no hay otro.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- 2024 separó integrantes con sufijo `_icb`; 2025 trae `integrantes_2025_w` y un archivo aparte `ensanut2025_icb`: se usa `integrantes_2025_w` (mismo rol), declarado.
- 2025 añade archivos (menores, casa por casa, antropometría, frecuencias, lactancia, actividad física) que el contendiente no usa: fuera.

Regla fijada: si en caja, antes de correr, el catálogo de 2025 no trae una columna del contendiente con el
mismo texto de pregunta y códigos, **esa conducta sale NO-ESTIMABLE** (se omite R; no se recodifica ad hoc)
y se declara en la nota de apertura. Leer el catálogo y el cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENSANUT-2025-<conducta>-<eje>-<cat>-R`, `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`,
`-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.

Contrato: `APERTURA-<X>-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-<X>-0001`; payloads con sha del manifiesto;
medidor sellado del contendiente, su `resultados.json`, la receta y la guardia como inputs `origen: repo` con sha).
La apertura es copiarlo a `data/corrida0/CALC-APERTURA-<X>-0001/spec.yaml` y correr (receta).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: el contendiente se selló antes de que exista la R (sello del CALC contendiente anterior a cualquier apertura de la ola; la ola sigue RESERVADA en `data/manifiesto.yaml`). Ninguna frase mezcla esta cobertura con marcadores RETROSPECTIVOS.
- Unidad: **persona** en R y en el piso; nada se promedia con unidades hogar, delito o trámite.
- Escala: proporción 0..1 en R y en el piso; se compara «R dentro del IC del piso» (cobertura), no punto contra punto; el MAE de punto es descriptivo.
- Segmentación: un eje a la vez (sexo, edad, estrato de tamaño de localidad, escolaridad); ningún cruce — la guardia lo impide. El estrato rural/urbano/metropolitano es tamaño de localidad, no clase: el sesgo de clase media urbana no se corrige aquí y se declara.
- Pobreza, acceso y oferta de servicios confunden conductas de uso de servicios (atención, farmacia, curandero): se leen como oferta antes que preferencia (§3), nunca como cultura.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «la salud del mexicano cambió»; dice que el piso de la ola anterior, con su IC, no anticipa la ola nueva en esa proporción de celdas.
- Cifras escritas a mano: ninguna; las constantes del medidor son hashes fijados y umbrales de la regla (0.95 nominal, z = 1.959964), declarados antes de abrir.

# Expediente de apertura · ENASEM 2024 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Contendiente sellado (regla 6: ningún contendiente nuevo): `CALC-ENASEM-ESCOLARIDAD-2021-0001` — piso
  2021 con **IC95 de diseño** IC-LO/IC-HI (bootstrap de UPM dentro de estrato, 2000 réplicas; spec
  `forense/prereg-caja/COLA-ENASEM-ESCOLARIDAD-spec-v1_0.md` §4; una sola ola abierta, **sin IC de persistencia**),
  2 conductas, `olas: 2021 abierta; 2024 RESERVADA (E.6), no es input` (su `spec.yaml`, etiquetas). Sellado el
  26/sep/2026 (ejecución 18:49:58Z, `ejecucion.json`).
- [EJECUTADO] Payload de microdato de la ola: `enasem2024_bd_csv_zip` (`data/manifiesto.yaml`, lector YAML por id;
  sha256 `6712f1b0…`). No lleva `estado_reserva` en el manifiesto ni fila en `data/corrida0/aperturas-pendientes-v1_0.tsv`
  (hallazgo: la reserva E.6 de ENASEM 2024 vive sólo en la etiqueta del contendiente). `enasem2024_fd_xlsx` y los
  `cc1_…enasem_2024…` (variables, diagramas) son documentación, nunca payload.
- [EJECUTADO] Ninguna familia 2027 la usa como R (`forense/analisis/familias-2027/familias-2027-estado-v1_0.tsv`: las 8
  familias apuntan a olas 2027).
- [LEÍDO] Nombres (no valores) de 2024, del inventario de cabeceras `data/inventario-reactivos-v1_2.tsv` (acto
  MAESTRA32-E6, anterior a este): el miembro de la sección A-C-D-E-PC-F-H-I es `tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv`
  y trae `YRSCHOOL`, `SEX_24`, `AGE_24`, `FACTORI_24`, `EST_DIS_24`, `UPM_DIS_24` (en 2021 el mismo inventario da
  `SECT_A_C_D_E_PC_F_H_I_2021.csv` con las seis de `COLS_CRUDAS` del contendiente: la fuente casa con lo sellado).
  `data/inventario-fd-v1_1.tsv` rotula `YRSCHOOL` «Años de educación» en 2024.
- [SUPUESTO→rama prevista] El cuestionario y el FD de 2024 no están montados (NUBE): los **códigos** se fijan sobre la
  ola del piso (FD 2021 que citó el contendiente), rotulado así; la diferencia se declara al abrir (§5).

## 1 · Estimandos

Por cada conducta del contendiente y cada categoría de cada eje (TOTAL; SEXO; EDAD): **R = Σw·y / Σw** en ENASEM
2024, con la recodificación 1/0/fuera del contendiente sobre `YRSCHOOL` (años de educación, válidos 0–22):

| conducta | UNO | CERO |
|---|---|---|
| SIN-ESCOLARIDAD | 0 | 1–22 |
| SEIS-ANOS-O-MENOS | 0–6 | 7–22 |

Todo otro valor (blanco, fuera de rango) queda fuera. 2 conductas × (1 + 2 + 4) = **14 celdas**.

## 2 · Universo, unidad, ponderador, diseño

Unidad **persona entrevistada**. Registro válido: `FACTORI_24` > 0, `EST_DIS_24` y `UPM_DIS_24` no vacíos. Universo
`50 ≤ AGE_24 ≤ 120` (888 «no responde» y 999 «no sabe» fuera, como en el contendiente). Ponderador `FACTORI_24`.
Ejes: SEXO (`SEX_24`: 1 HOMBRE, 2 MUJER); EDAD (`AGE_24`: 50-59, 60-69, 70-79, 80-MAS = 80–130). Columnas de 2021 con
sufijo de ronda `_21` se leen con `_24`; `YRSCHOOL` no lleva sufijo. Payload: `enasem2024_bd_csv_zip`, miembro
`tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv` (comparado sin mayúsculas; si no hay exactamente uno → PARO, no NO-ESTIMABLE).
R es un punto; no se calcula IC de R (la cobertura se mide contra el IC del contendiente).

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce levanta
`ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo: `groupby`/`value_counts`
con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera de `lee_payload_reservado` → PARO.
Reuso por bytes con sha256 fijado: del medidor sellado, sólo sus datos (`CONDUCTAS`, `MAPAS`, `EDADES`, `COLS_CRUDAS`,
`PESO`, `ESTRATO`, `UPM`, `EJES_CATS`); del motor común `tools/dominios/confianza/motor_pisos.py`, `prepara_diseno`,
`recodifica`, `eje_mapa`, `eje_rango`, `num`, `rid`. La máscara de universo 50–120 está en línea en `mide()` del sellado
y se replica. Probado por mutación y sobre sintético con el esquema de la ola: `tests/test_prereg_aperturas.py` y
`tests/test_apertura_enasem_2024.py` (con soporte; conducta sin soporte; categoría vacía; universo 50+ contra cálculo a
mano; miembro ausente → PARO).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con
lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson;
**SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Si dos
filas pudieran satisfacerse a la vez, manda el orden NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO
(son excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por conglomerado
(conducta: las 7 celdas de una conducta comparten muestra) y error absoluto medio punto-del-piso vs R.
B-bis: si el piso NO falla (CALIBRADO), el piso 2021 queda **corroborado en alcance** para 2024; SOBRECUBRE
= piso **acotado** (IC conservador); SUBCUBRE = el piso no anticipa la ola. Declarado antes de abrir: el IC del
contendiente es de **diseño** (error muestral de 2021), no de persistencia entre olas; tres años de cambio de cohorte
en el panel 50+ (la escolaridad sube por reemplazo generacional) empujan hacia SUBCUBRE sin que eso sea un defecto del
piso como estimador de 2021. Con n = 14 celdas el Wilson es ancho: la lectura es de alcance, no de precisión.
Una apertura sirve a todos los sellados antes: el único contendiente que declara ENASEM 2024 como reservada es
`CALC-ENASEM-ESCOLARIDAD-2021-0001`; no hay otro.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Miembro: 2021 `SECT_A_C_D_E_PC_F_H_I_2021.csv`; 2024 `tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv` (prefijo `tr_enasem24_`,
  minúsculas, sin año al final).
- Sufijo de ronda `_21` → `_24` en sexo, edad, factor, estrato y UPM.
- Hallazgo para el preflight documental: en `data/inventario-fd-v1_1.tsv` la hoja de la sección del FD 2024 rotula
  `AGE_24` «Edad 2012» mientras la hoja MASTER lo rotula «Edad 2024»; el acto de apertura confirma en el FD que es la
  edad de la ronda 2024 antes de correr.
- ENASEM es panel: la población 50+ de 2024 incluye seguimiento y muestra nueva; el factor transversal 2024 la
  representa (igual que `FACTORI_21` en 2021).

Regla fijada: si en caja, antes de correr, el FD de 2024 no trae una columna del contendiente, esa conducta (o todo,
si es de diseño) sale **NO-ESTIMABLE**: el código la lee vacía, omite R y el dictamen lo refleja; no se recodifica ad hoc.
Si la columna existe pero cambió su texto o sus códigos, el código congelado no puede omitirla: eso no se parcha
(D-18), vuelve a mesa. Leer el FD y el cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENASEM-2024-<conducta>-<eje>-<cat>-R` (14), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`,
`-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.
Rama K = 0 con n = 14 (plausible aquí): Wilson sin acotar daba WILSON-LO ≈ −1.4e−17 y `corrida0._valida_outputs` lo
rechazaba; la guardia común lo acota a [0, 1] (commit `35675807`) y `tests/test_apertura_enasem_2024.py` ejerce la rama.

Contrato: `APERTURA-ENASEM-2024-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-ENASEM-2024-0001`; payload con
sha del manifiesto; medidor sellado del contendiente, su `resultados.json`, el motor, la guardia y la plantilla como
inputs `origen: repo` con sha). La apertura es copiarlo a `data/corrida0/CALC-APERTURA-ENASEM-2024-0001/spec.yaml` y
correr (receta `RECETA-APERTURA-ENASEM-2024.md`).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: el contendiente se selló (26/sep) antes de que exista la R; ninguna ola 2024 de
  ENASEM fue abierta por ningún CALC sellado. Ninguna frase mezcla esta cobertura con marcadores RETROSPECTIVOS.
- Unidad: **persona** 50+ en R y en el piso; nada se promedia con unidades hogar, delito o trámite.
- Escala: proporción 0..1 en R y en el piso; se compara «R dentro del IC del piso» (cobertura), no punto contra punto;
  el MAE de punto es descriptivo.
- Segmentación: un eje a la vez (sexo, edad); ningún cruce — la guardia lo impide. No hay eje de región, localidad ni
  clase: la escolaridad de 50+ es sobre todo huella de la oferta escolar rural de 1940–1970, no preferencia.
- Qué confunde cultura con estructura: «sin escolaridad» mide oferta y acceso históricos (y trabajo infantil), no un
  rasgo cultural; leerlo como valoración de la educación sería el error.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «los adultos mayores se educaron de golpe»; dice que el
  IC de diseño de 2021 no anticipa 2024 (cambio de cohorte y de muestra de panel incluidos).
- Cifras escritas a mano: ninguna; las constantes del medidor son hashes fijados, el nombre del miembro (inventario) y
  los umbrales de la regla (0.95 nominal, z = 1.959964), declarados antes de abrir.

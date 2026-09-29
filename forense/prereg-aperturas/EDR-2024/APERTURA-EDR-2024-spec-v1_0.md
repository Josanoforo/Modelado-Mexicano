# Expediente de apertura · EDR 2024 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Contendiente sellado (regla 6: ningún contendiente nuevo): `CALC-EDR-SUICIDIO-PISOS-0001` — piso 2023 con
  **IC calibrado de persistencia** ICC-LO/ICC-HI = expit(logit p₂₀₂₃ ± 1.959964·√τ²), τ² = media de Δ² en logit entre
  años de registro consecutivos 2015–2023, sin error de diseño (registro completo) (spec
  `forense/prereg-caja/EDR-SUICIDIO-PISOS-spec-v1_0.md`), 6 conductas, `olas: 2015-2023 abiertas; 2024 RESERVADA (E.6),
  no es input` (su `spec.yaml`). Sellado el 26/sep/2026 (ejecución 18:11:26Z).
- [EJECUTADO] Payload de microdato de la ola: `edr2024_bd_dbf_zip` (`data/manifiesto.yaml`, lector YAML por id; sha256
  `a8acb8f0…`). No lleva `estado_reserva` ni fila en `data/corrida0/aperturas-pendientes-v1_0.tsv` (hallazgo: la reserva
  E.6 de EDR 2024 vive sólo en la etiqueta y la guardia del contendiente, que rechaza toda ruta con 2024).
- [EJECUTADO] Ninguna familia 2027 la usa como R (`familias-2027-estado-v1_0.tsv`: las 8 familias apuntan a olas 2027).
- [LEÍDO] Nombres (no valores) de 2024, del inventario de cabeceras `data/inventario-reactivos-v1_2.tsv`: el ZIP trae
  `DEFUN24.dbf` con `ENT_RESID`, `TLOC_RESID`, `CAUSA_DEF`, `SEXO`, `EDAD`, `ANIO_OCUR`, `ANIO_REGIS`, `ESCOLARIDA` y
  `TIPO_DEFUN` (más catálogos que no se usan).
- [SUPUESTO→rama prevista] Los catálogos de 2024 no están montados (NUBE): los **códigos** se fijan sobre la ola del
  piso (2022–2023, los del contendiente), rotulado así; la diferencia se declara al abrir (§5).

## 1 · Estimandos

Por cada conducta del contendiente y cada categoría de cada eje: **R = conteo con la conducta / conteo en el universo**
(proporción exacta, w = 1) entre las defunciones **registradas en 2024**, con la recodificación del contendiente:

| conducta | UNO | universo |
|---|---|---|
| SUICIDIO-CIE | `CAUSA_DEF` CIE-10 X60–X84 (3 o 4 caracteres) | causa no vacía |
| SUICIDIO-PRESUNTO | `TIPO_DEFUN` = 3 | todas |
| SUIC-HOMBRE | `SEXO` = 1 | suicidios CIE con sexo 1 o 2 |
| SUIC-15-44 | edad 15–44 | suicidios CIE con edad válida |
| SUIC-15-29 | edad 15–29 | suicidios CIE con edad válida |
| SUIC-OCURRIDO-EN-OLA | `ANIO_OCUR` = 2024 | suicidios CIE |

Edad en años desde `EDAD` N(4): 1xxx horas, 2xxx días, 3xxx meses → 0 años (x098 fuera); 4001–4120 → años; resto fuera.
Ejes (uno a la vez): TOTAL; SEXO (1 HOMBRE, 2 MUJER); EDAD (0-9, 10-14, 15-19, 20-24, 25-29, 30-44, 45-59, 60-MAS);
ENT (`ENT_RESID` 01–32); TLOC (`TLOC_RESID`: MENOS-2500 1–3, 2500-14999 4–6, 15MIL-99MIL 7–12, 100MIL-MAS 13–17);
ESCOLARIDAD (`ESCOLARIDA`: PRIMARIA-O-MENOS 1–4, SECUNDARIA 5–6, MEDIA-SUPERIOR 7–8, SUPERIOR 9–10). SUIC-HOMBRE no va
por SEXO; SUIC-15-* no van por EDAD. Total: **288 celdas** (51 × 3 + 49 + 43 × 2).

## 2 · Universo, unidad, ponderador, diseño

Unidad **defunción registrada** (una fila viva de `DEFUN24.dbf`; las marcadas como borradas en el DBF, fuera). Registro
administrativo completo: sin diseño, sin ponderador (w = 1), sin error muestral. Payload `edr2024_bd_dbf_zip`, miembro
único `defun24.dbf` sin distinguir mayúsculas (si no hay exactamente uno → PARO, no NO-ESTIMABLE). Ola = año de
registro del archivo (no de ocurrencia). R es un punto exacto; la cobertura se mide contra el ICC del contendiente.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` con w = 1 — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo (`groupby`/
`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera de
`lee_payload_reservado` → PARO). Reuso por bytes con sha256 fijado del medidor sellado: `lee_dbf` (lector DBF, un campo
a la vez para tolerar ausencias), `miembro_ola`, `prepara` (recodificación, universos y ejes), `_ejes_de`, `_todas`,
`rid`, `rid_p`. `prepara` pide la variable de presunto por ola en `PRESUNTO`; el medidor añade en memoria
`PRESUNTO["2024"] = "TIPO_DEFUN"` (la del contendiente desde 2022). Probado por mutación y sobre sintético:
`tests/test_prereg_aperturas.py` y `tests/test_apertura_edr_2024.py` (DBF sintético; con soporte; conducta sin soporte;
categoría vacía; R idéntica a `_celdas` del sellado en las 288 celdas; miembro ausente → PARO).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con
lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson;
**SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Si dos
filas pudieran satisfacerse a la vez, manda el orden NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO
(son excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por conglomerado
(conducta: sus celdas comparten registro) y error absoluto medio punto-del-piso vs R.
B-bis: si el piso NO falla (CALIBRADO), el piso 2023 queda **corroborado en alcance** para 2024; SOBRECUBRE
= piso **acotado** (ICC conservador); SUBCUBRE = el piso no anticipa el año. 10 de las 288 celdas no tienen ICC en el
contendiente (p = 0 o 1, o τ² sin Δ definidos): salen sin puntuar por construcción (declarado antes de abrir).
Una apertura sirve a todos los sellados antes: el único contendiente que declara EDR 2024 reservada es
`CALC-EDR-SUICIDIO-PISOS-0001`; no hay otro.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Archivo: `DEFUN24.dbf` en `defunciones_base_datos_2024_dbf.zip` (mismo formato DBF que 2020–2023).
- Presunto: `TIPO_DEFUN` (código 3 = suicidio en 2022–2023); `PRESUNTO` no existe desde 2022.
- Registro tardío: una defunción registrada en 2024 puede haber ocurrido antes (la conducta SUIC-OCURRIDO-EN-OLA lo
  mide); el año de registro 2024 incluye rezagos de pandemia menores que 2020–2021.

Regla fijada: si en caja, antes de correr, el descriptor de 2024 no trae un campo del contendiente, **las conductas que
dependen de él salen NO-ESTIMABLE** (el código lo lee vacío y omite su R; dependencias: SUICIDIO-CIE ← CAUSA_DEF;
SUICIDIO-PRESUNTO ← TIPO_DEFUN; SUIC-HOMBRE ← CAUSA_DEF, SEXO; SUIC-15-* ← CAUSA_DEF, EDAD; SUIC-OCURRIDO-EN-OLA ←
CAUSA_DEF, ANIO_OCUR); un eje sin su campo queda sin categorías (R None). No se recodifica ad hoc. Si el campo existe
pero cambió su catálogo, el código congelado no puede omitirlo: no se parcha (D-18), vuelve a mesa.

## 6 · Salidas

`RESULT-APERTURA-EDR-2024-<conducta>-<eje>-<cat>-R` (288), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`,
`-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.

Contrato: `APERTURA-EDR-2024-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-EDR-2024-0001`; payload con sha
del manifiesto; medidor sellado del contendiente, su `resultados.json`, la guardia y la plantilla como inputs
`origen: repo` con sha). La apertura es copiarlo a `data/corrida0/CALC-APERTURA-EDR-2024-0001/spec.yaml` y correr
(receta `RECETA-APERTURA-EDR-2024.md`).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: el contendiente se selló (26/sep) antes de que exista la R; ningún CALC sellado leyó
  EDR 2024. Ninguna frase mezcla esta cobertura con marcadores RETROSPECTIVOS.
- Unidad: **defunción registrada**; nunca persona encuestada ni tasa por habitante (no hay población en corpus). Nada
  se promedia con unidades persona, hogar o trámite.
- Escala: proporción exacta 0..1 del registro en R y en el piso; «R dentro del ICC» (cobertura), no punto contra punto.
- Segmentación: un eje a la vez (sexo, edad, entidad, tamaño de localidad, escolaridad); ningún cruce. Tamaño de
  localidad y escolaridad no son clase; la escolaridad del fallecido mide oferta educativa de su cohorte.
- Qué confunde cultura con estructura: la proporción de suicidios entre defunciones depende del denominador (todas las
  causas: violencia, pandemia, crónicas); un cambio en homicidios o en mortalidad general mueve la proporción sin que
  cambie el suicidio. Además, codificación CIE y presunción del MP son prácticas institucionales, no conducta.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «los mexicanos se suicidan más»; dice que el piso 2023
  con su ICC no anticipa la composición del registro 2024.
- Cifras escritas a mano: ninguna; constantes = hashes fijados, el nombre de la variable de presunto (inventario y
  contendiente) y los umbrales de la regla (0.95, z = 1.959964), declarados antes de abrir.

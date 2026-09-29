# Expediente de apertura · EMAT 2024 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Contendiente sellado (regla 6: ningún contendiente nuevo): `CALC-EMAT-PAREJA-PISOS-0001` — piso 2023 con
  **IC calibrado de persistencia** ICC-LO/ICC-HI = expit(logit p₂₀₂₃ ± 1.959964·√τ²), τ² = media de Δ² en logit entre
  años de registro consecutivos 2010–2023, sin error de diseño (registro completo) (spec
  `forense/prereg-caja/EMAT-PAREJA-PISOS-spec-v1_0.md`), 4 conductas de matrimonio y 8 de contrayente,
  `olas: 2010-2023 abiertas; 2024 RESERVADA (E.6), no es input` (su `spec.yaml`). Sellado el 26/sep/2026 (18:09:43Z).
- [EJECUTADO] Payload de microdato de la ola: `cc1_inegi_emat_2024__matrimonios_base_datos_2024_dbf` (`data/manifiesto.yaml`,
  lector YAML por id; sha256 `3c65c064…`; `raiz: reserva_respondentes`, `estado_reserva: RESERVADA-NO-ABIERTA-NO-INDEXAR-L`;
  «ZIP-OK(3 miembros)»); fila `EMAT 2024` de `data/corrida0/aperturas-pendientes-v1_0.tsv`, que hoy dice
  «contendientes: NINGUNO» (hallazgo: la vista no ve a `CALC-EMAT-PAREJA-PISOS-0001`; la corrige quien tiene el
  inventario en su perímetro).
- [EJECUTADO] Ninguna familia 2027 la usa como R (`familias-2027-estado-v1_0.tsv`: las 8 familias apuntan a olas 2027).
- [SUPUESTO→rama prevista] Por `NO-INDEXAR` no hay inventario de cabeceras de 2024: se supone `MATRI24.dbf` con los
  doce campos del contendiente (`ENT_REGIS`, `TAM_LOC_RE`, `ANIO_REGIS`, `GENERO`, `SEXO_CON1/2`, `EDAD_CON1/2`,
  `ESCOL_CON1/2`, `CONACTCON1/2`), como 2010–2023; los **códigos** se fijan sobre la ola del piso, rotulado así; la
  diferencia se declara al abrir (§5).

## 1 · Estimandos

Por cada conducta y cada categoría de cada eje: **R = conteo con la conducta / conteo en el universo** (proporción
exacta, w = 1) en el registro 2024, con la recodificación del contendiente (edad válida 12–98):

| conducta | unidad | UNO | universo |
|---|---|---|---|
| M-MISMO-SEXO | matrimonio | `GENERO` = 2 | GENERO 1 o 2 |
| M-CON-MENOR-18 | matrimonio | algún contrayente con edad válida < 18 | ambas edades válidas, o alguna < 18 |
| M-AMBOS-TRABAJAN | matrimonio | `CONACTCON1` = `CONACTCON2` = 1 | ambos en {1, 2} |
| M-MISMA-ESCOLARIDAD | matrimonio | `ESCOL_CON1` = `ESCOL_CON2` | ambos en 1–7 |
| C-EDAD-<tramo> (12-19, 20-24, 25-29, 30-34, 35-39, 40-MAS=40–98) | contrayente | edad en el tramo | edad válida |
| C-TRABAJA | contrayente | `CONACTCON` = 1 | {1, 2} |

Ejes (uno a la vez): M-* por TOTAL, ENT (`ENT_REGIS` 01–32), TLOC (`TAM_LOC_RE`: MENOS-2500 1–3, 2500-14999 4–6,
15MIL-99MIL 7–12, 100MIL-MAS 13–17); C-* por TOTAL, SEXO (`SEXO_CON*` 1 HOMBRE, 2 MUJER), ESCOLARIDAD (`ESCOL_CON*`:
PRIMARIA-O-MENOS 1–4, SECUNDARIA 5, PREPARATORIA 6, PROFESIONAL 7), TLOC. Cada matrimonio aporta dos contrayentes
(`*_CON1` y `*_CON2`). **C-EDAD-MEDIA queda fuera**: es una media en años y el contendiente no le calcula ICC (se aparta
sin abrir: no hay IC contra el cual medir cobertura y su escala no es la de las demás celdas). Total: **225 celdas**
(4 × 37 + 7 × 11).

## 2 · Universo, unidad, ponderador, diseño

Unidades **matrimonio registrado** (M-*) y **contrayente** (C-*): cada celda es de una sola unidad, declarada arriba.
Registro administrativo completo: sin diseño, sin ponderador (w = 1), sin error muestral. Payload
`cc1_inegi_emat_2024__matrimonios_base_datos_2024_dbf`, miembro único `matri24.dbf` sin distinguir mayúsculas (si no hay
exactamente uno → PARO, no NO-ESTIMABLE). Ola = año de registro. R es un punto exacto.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` con w = 1 — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo (`groupby`/
`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera de
`lee_payload_reservado` → PARO). Reuso por bytes con sha256 fijado del medidor sellado: `lee_dbf` (un campo a la vez
para tolerar ausencias), `miembro_ola`, `matrimonios`, `contrayentes` (recodificación, universos, ejes), `_todas`,
`rid`, `rid_p`. Probado por mutación y sobre sintético: `tests/test_prereg_aperturas.py` y
`tests/test_apertura_emat_2024.py` (DBF sintético; con soporte; conducta sin soporte; categoría vacía; R idéntica a
`_celdas` del sellado en las 225 celdas; miembro ausente → PARO).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con
lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson;
**SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Si dos
filas pudieran satisfacerse a la vez, manda el orden NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO
(son excluyentes por construcción). K y N **cuentan celdas**, no promedian cantidades: la primaria junta celdas de
matrimonio y de contrayente sin mezclar sus proporciones. Secundarias, descriptivas, no adjudican: cobertura por
conglomerado (conducta) y error absoluto medio punto-del-piso vs R (**mezcla celdas de las dos unidades**: se reporta
sólo como descriptivo, y por conducta en la nota de apertura).
B-bis: si el piso NO falla (CALIBRADO), el piso 2023 queda **corroborado en alcance** para 2024; SOBRECUBRE
= piso **acotado** (ICC conservador); SUBCUBRE = el piso no anticipa el año. 32 de las 225 celdas no tienen ICC en el
contendiente (p = 0 o 1, o τ² sin Δ definidos, p. ej. mismo sexo en entidades sin registro previo): salen sin puntuar
por construcción (declarado antes de abrir).
Una apertura sirve a todos los sellados antes: el único contendiente que declara EMAT 2024 reservada es
`CALC-EMAT-PAREJA-PISOS-0001`; no hay otro.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Archivo: `MATRI24.dbf` [SUPUESTO] en `matrimonios_base_datos_2024_dbf.zip` (3 miembros; los otros dos se ignoran).
- [REPORTADO, no verificado en este acto] Cambios legales del periodo: matrimonio igualitario extendido a todas las
  entidades hacia fines de 2022 y prohibición del matrimonio de menores de 18 (reforma federal de 2019 y armonización
  estatal). Un cambio en M-MISMO-SEXO o M-CON-MENOR-18 por entidad es de **oferta legal**, no de preferencia; declarado
  antes de abrir.

Regla fijada: si en caja, antes de correr, el descriptor de 2024 no trae un campo del contendiente, **las conductas que
dependen de él salen NO-ESTIMABLE** (el código lo lee vacío y omite su R; dependencias: M-MISMO-SEXO ← GENERO;
M-CON-MENOR-18 y C-EDAD-* ← EDAD_CON1/2; M-AMBOS-TRABAJAN y C-TRABAJA ← CONACTCON1/2; M-MISMA-ESCOLARIDAD ←
ESCOL_CON1/2); un eje sin su campo queda sin categorías (R None). No se recodifica ad hoc. Si el campo existe pero
cambió su catálogo, el código congelado no puede omitirlo: no se parcha (D-18), vuelve a mesa.

## 6 · Salidas

`RESULT-APERTURA-EMAT-2024-<conducta>-<eje>-<cat>-R` (225), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`,
`-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.

Contrato: `APERTURA-EMAT-2024-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-EMAT-2024-0001`; payload con sha
del manifiesto; medidor sellado del contendiente, su `resultados.json`, la guardia y la plantilla como inputs
`origen: repo` con sha). La apertura es levantar la custodia del payload (`reserva_respondentes` → `data_raw`), copiar el
contrato a `data/corrida0/CALC-APERTURA-EMAT-2024-0001/spec.yaml` y correr (receta `RECETA-APERTURA-EMAT-2024.md`).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: el contendiente se selló (26/sep) antes de que exista la R; el payload sigue
  `RESERVADA-NO-ABIERTA` y ningún CALC sellado lo consume. Ninguna frase mezcla esta cobertura con marcadores
  RETROSPECTIVOS.
- Unidad: **matrimonio registrado** o **contrayente**, cada celda de una sola; ninguna es persona encuestada ni hogar.
  El MAE descriptivo mezcla las dos unidades y no se lee como una cantidad.
- Escala: proporción exacta 0..1 del registro en R y en el piso; «R dentro del ICC» (cobertura).
- Segmentación: un eje a la vez; ningún cruce. Tamaño de localidad es del lugar de registro, no de residencia ni clase.
- Qué confunde cultura con estructura: el registro civil mide matrimonios **registrados**; la unión libre (muy extendida
  y más en sectores populares y rurales) queda fuera, así que la composición del registro es selección, no «la pareja
  mexicana». Cambios legales (edad mínima, matrimonio igualitario) y de costo del trámite mueven las proporciones.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «cambió la familia mexicana»; dice que el piso 2023
  con su ICC no anticipa la composición del registro 2024.
- Cifras escritas a mano: ninguna; constantes = hashes fijados y umbrales de la regla (0.95, z = 1.959964).

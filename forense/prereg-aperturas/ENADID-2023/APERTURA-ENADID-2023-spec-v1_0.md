# Expediente de apertura · ENADID 2023 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), escrito en NUBE sobre `7393b17e`, sin corpus
montado. Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA para estas conductas (E.6); la levanta el código congelado de este expediente, en caja, en el
commit que mesa autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Dos contendientes sellados (regla 6: ninguno nuevo); una apertura sirve a los dos (E.6):
  `CALC-ENADID-FAMILIA-HOGARES-0001` (`spec.yaml:23` «ola_reservada: ENADID 2023 (E.6): no es input»; spec humana
  `forense/prereg-caja/FAMILIA-ENADID-PISOS-spec-v1_0.md`; 11 conductas, 5 de hogar y 6 de persona; piso 2018 con
  **IC calibrado de persistencia** 2009→2014→2018, salvo HOGAR-CON-MIGRANTE-INTERNACIONAL-5A, dos olas, sin ICC) y
  `CALC-ENADID-COLA-2018-0001` (`spec.yaml:24` «2018 abierta; 2023 RESERVADA (E.6), no es input»; spec humana
  `forense/prereg-caja/COLA-ENADID-PISOS-spec-v1_0.md`; 4 conductas, 2 de mujeres y 2 de hogares; piso 2018 con
  IC95 de **diseño**, sin persistencia).
- [EJECUTADO] Manifiesto por id (A.15; `yaml.CSafeLoader`, 7 198 entradas; filtro `enadid` en id o `archivo`): la
  ola 2023 tiene **un** payload de microdato, `enadid2023_base_datos_csv` (`base_datos_enadid23_csv.zip`); los
  otros cuatro `enadid2023_*` son documentación (dos cuestionarios, FD `.xlsx`, diseño muestral): no son payload.
- [EJECUTADO] Reserva: `enadid2023_base_datos_csv` no lleva `estado_reserva` en el manifiesto y
  `tools/corpus_loader.py` no lo reserva; **la reserva («para estas conductas») la declaran las specs selladas
  de los contendientes** (hallazgo; la receta §4a no tiene custodia que levantar).
- [EJECUTADO] **La ola no está virgen.** `grep` de los 390 `data/corrida0/*/spec.yaml` por
  `enadid2023_base_datos_csv` → 6 CALC la leen: `CALC-ENADID-0001` y `CALC-ENADID2023-UNION-SEXO-EDAD-0001..0004`
  (TSDEM, situación conyugal `p3_27`, 15+, por sexo y edad; LEÍDO `CALC-ENADID2023-UNION-SEXO-EDAD-0004/spec.yaml:43,58`),
  anteriores al sello de FAMILIA (su spec §0 los cita como ya medidos), y `CALC-PDR1-ENADID2023-0001` (TSDEM,
  autoadscripción indígena `p3_12` por sexo y edad; COMMIT-1 `fc7a4b74`, 28/sep, posterior a ambos sellos).
  Cruces vistos que tocan celdas de los contendientes: **PERSONA-15MAS-UNIDA y UNIDO-15MAS-EN-UNION-LIBRE en
  TOTAL, SEXO y EDAD** (R derivable de `p3_27` por sexo y edad, existente antes del sello del contendiente →
  no son PROSPECTIVA). Decisión fijada antes de abrir: esas 18 celdas se **apartan de la primaria** (R se
  reporta como descriptiva/RETROSPECTIVA, no se puntúa). Vecino declarado, no el mismo estimando:
  COLA-SEPARADA-ENTRE-UNION-LIBRE usa `p10_1` del módulo de la mujer (15–54) con «viuda de unión libre» en el
  denominador, que `p3_27` no distingue (5 = viuda); se queda en la primaria. PDR1 no toca ninguna celda.
- [LEÍDO] Renombre fijado antes de abrir: la situación conyugal de TSDEM es `p3_21` en 2018 (medidor sellado de
  FAMILIA, `PER["2018"]["conyu"]`) y `p3_27` en 2023, con los mismos códigos 1 unión libre · 2 separada de unión
  libre · 3 separada de matrimonio · 4 divorciada · 5 viuda · 6 casada · 7 soltera
  (`CALC-ENADID2023-UNION-SEXO-EDAD-0004/spec.yaml:43`, leído del FD 2023 por aquel acto). En 2023 `p3_21` existe y
  es otra pregunta (A.15: nemónico desplazado): leerla daría una conducta distinta con el mismo nombre.
- [REPORTADO] Miembros del ZIP 2023: `THOGAR.csv`, `TSDEM.csv`, `TMUJER1.csv`, `TMUJER2.csv`, `TMIGRANTE.csv`,
  `TVIVIENDA.csv`, `TFECHISEMB.csv` y una nota (`tests/test_pdr1_enadid2023.py:31-32`, «forma real»); cabecera de
  TSDEM con `llave_hog, paren, sexo, edad, niv, p3_27, ent, tam_loc, fac_viv, est_dis, upm_dis` (mismo archivo,
  l. 22-29). Los nombres 2018 (`THogar.csv`, `TSdem.csv`, `TMujer2.csv`, `TMigrante.csv`) casan sin distinguir
  mayúsculas (lector `lectores_familia`). Las columnas de THOGAR, TMUJER2 y TMIGRANTE 2023 no están verificadas
  aquí: los códigos se fijan **sobre la ola del piso 2018** (los de cada contendiente), rotulado así (§5).
- [SUPUESTO] Cifras de ENADID 2023 publicadas por INEGI y citadas en los reports no se leyeron aquí; si alguna
  coincide con una celda puntuada, el acto de apertura la rotula RETROSPECTIVA en su nota sin cambiar la primaria.

## 1 · Estimandos

Por cada conducta de cada contendiente y cada categoría de cada uno de sus ejes: **R = Σw·y / Σw** en ENADID 2023,
con la recodificación del contendiente (medidores sellados importados por bytes, sha256 fijado en
`APERTURA-ENADID-2023-spec.yaml`). **313 celdas**:
- `FAM-` (213). Hogar (THOGAR, `fac_viv`; 5 conductas × 15 celdas): HOGAR-UNIPERSONAL `cls_hog` 5, -NUCLEAR 1,
  -AMPLIADO 2 (universo `cls_hog` 1–6); HOGAR-JEFATURA-FEMENINA `sexo_jefe` 2 vs 1; HOGAR-CON-MIGRANTE-INTERNACIONAL-5A
  `migra_ho` 1 vs 2. Ejes: SEXO-JEFE (1/2), EDAD-JEFE (12-29, 30-44, 45-59, 60-MAS), ESCOLARIDAD-JEFE (`niv_jefe`
  HASTA-PRIMARIA 0–2, SECUNDARIA 3/5, MEDIA-SUPERIOR 4/6/7, SUPERIOR 8–11), TLOC (`tam_loc` 1 100MIL-MAS … 4
  MENOS-2500). Persona (TSDEM enlazado por `llave_hog`, peso y diseño del hogar; 6 conductas × 23 celdas):
  PERSONA-60MAS (`edad` ≥ 60); AM60-VIVE-SOLO (hogar de 1 integrante, `p2_5`, entre 60+); AM60-EN-HOGAR-AMPLIADO
  (`cls_hog` 2 vs 1/3/4/5/6, entre 60+); JOVEN-25-34-HIJO-DEL-JEFE (`paren` 3 vs 1–8, entre 25–34);
  PERSONA-15MAS-UNIDA (`p3_27` 1/6 vs 2/3/4/5/7, entre 15+); UNIDO-15MAS-EN-UNION-LIBRE (1 vs 6, entre 15+). Ejes:
  SEXO, EDAD (00-14, 15-29, 30-44, 45-59, 60-74, 75-MAS), ESCOLARIDAD (`niv`, mismos cortes), TLOC,
  TAMANO-HOGAR (1, 2, 3-4, 5-MAS), CONDICION-PAREJA (UNIDO/NO-UNIDO).
- `COLA-` (100). Mujeres (TMUJER2, `fac_per`, 15–54; 2 conductas × 13 celdas): SEPARADA-ENTRE-UNION-LIBRE (`p10_1`
  2 vs 1/5); SEPARADA-O-DIVORCIADA-ENTRE-MATRIMONIO (3/4 vs 6/7). Ejes: EDAD (15-24, 25-34, 35-44, 45-54), TAMLOC,
  ESCOLARIDAD (`niv` HASTA-PRIMARIA 0–2, SECUNDARIA 3–5, MEDIA-SUPERIOR 6–7, SUPERIOR 8–11). Jefaturas (TSDEM
  `paren` = 1, `fac_viv`; 2 conductas × 37 celdas): JEFATURA-FEMENINA-CON-MIGRANTE-VARON / -SIN- (`sexo` 2 vs 1 en
  hogares con / sin algún registro de TMIGRANTE con `p4_6` = 1 y `p4_15` ∈ {1, 3}). Ejes: TAMLOC, ENTIDAD (01–32).

## 2 · Universo, unidad, ponderador, diseño

Unidades **hogar** (FAM hogar, COLA jefaturas) y **persona** (FAM residentes, COLA mujeres 15–54), por celda,
nunca promediadas entre sí. Válido FAM: `fac_viv > 0`, `est_dis`, `upm_dis` no vacíos en THOGAR; residente sin
hogar válido por `llave_hog` → fuera (`prepara_hogar/prepara_persona` de FAMILIA). Válido COLA: peso finito > 0,
estrato y UPM no vacíos (`prepara_diseno` del motor). Payload: `enadid2023_base_datos_csv`. R es un punto; no se
calcula IC de R.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo
(`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack`, lectura fuera de
`lee_payload_reservado` → PARO). `lee_payload_reservado` PARA si el ZIP no es `*enadid23*`. Probado por mutación y
con sintético del esquema de los dos contendientes: `tests/test_apertura_enadid_2023.py` (con soporte, conducta
sin soporte, categoría vacía, conyugal desde `p3_27` y no desde `p3_21`, celdas apartadas sin puntuar, CSV en ZIP
con columnas ausentes, PARO por diseño ausente y por ola equivocada; cada mutación de
`expediente_apertura.MUTACIONES` detectada) y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. lo/hi: FAM = **ICC del piso 2018**
(`RESULT-ENADID-FAMILIA-HOGARES-<c>-2018-<eje>-<cat>-ICC-LO/-ICC-HI`; punto `-P`), salvo HOGAR-CON-MIGRANTE-5A (sin
ICC) y las 18 celdas apartadas (§0): lo/hi vacíos. COLA = **IC95 de diseño 2018**
(`RESULT-ENADID-COLA-2018-<c>-2018-<eje>-<cat>-IC-LO/-IC-HI`; punto `-P`). En los `resultados.json` sellados hay
lo/hi en 151 celdas FAM y 94 COLA (**245 candidatas**; el resto son categorías degeneradas del piso, lo que el
contendiente ya publicó sin IC). **Primaria** (una sola, E.6): cobertura k/n sobre las celdas puntuadas de los dos
contendientes, con IC de Wilson al 95 %. Dictamen: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95;
**SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Orden: NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE >
CALIBRADO (excluyentes). Secundarias, descriptivas, no adjudican: cobertura por conglomerado = **CALC contendiente**
(recalculable de R y lo/hi; se reporta aparte porque FAM trae IC de persistencia y COLA IC de diseño, que no son el
mismo objeto) y `-MAE-PUNTO`, que promedia celdas de hogar y de persona: **no se lee como una cantidad** (§4 v2.16),
sólo como resumen descriptivo; la lectura es por celda o por contendiente y unidad.
B-bis: CALIBRADO = pisos **corroborados en alcance** para 2023; SOBRECUBRE = **acotados** (IC conservador); SUBCUBRE
= los pisos de 2018 no anticipan 2023 en esa proporción de celdas (esperable en COLA: IC de muestreo sin
persistencia, cinco años de distancia). Contendientes servidos a la vez: los dos; no hay otro sellado antes.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Situación conyugal TSDEM: `p3_21` (2018) → `p3_27` (2023), mismo texto y códigos (§0, renombre fijado).
- Miembros en mayúsculas en 2023; mismo rol. `TMUJER1`, `TVIVIENDA`, `TFECHISEMB`: fuera (los contendientes no los usan).
- THOGAR, TMUJER2 y TMIGRANTE 2023: columnas no verificadas desde nube; si `cls_hog`, `p2_5`, `migra_ho`, `p10_1`,
  `p4_6` o `p4_15` cambiaron de nombre o de pregunta, el preflight documental (FD `fd_enadid23.xlsx` y cuestionarios)
  lo decide por texto.

Regla fijada, mecánica: columna de reactivo o de eje ausente → entra vacía → las celdas que la usan salen
NO-ESTIMABLE; en COLA, sin `p4_6` o `p4_15` las dos conductas de jefatura con/sin migrante salen NO-ESTIMABLE
(sin ellas «sin migrante» sería «todos»); columna de llave, peso, estrato o UPM ausente (o `paren` de TSDEM para
COLA), o miembro CSV ausente → **PARO**. Si en caja, antes de correr, el FD/cuestionario de 2023 no trae una
columna del contendiente con el mismo texto y códigos, esa conducta se declara NO-ESTIMABLE en la nota de apertura
(no se recodifica ad hoc). Leer el FD y los cuestionarios no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENADID-2023-{FAM,COLA}-<conducta>-<eje>-<cat>-R` (313), `-DICTAMEN`, `-K`, `-N`,
`-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA, de la primaria; las celdas apartadas no entran en ella).
None sólo en R de celdas NO-ESTIMABLE y en Wilson/MAE cuando n = 0. Contrato: `APERTURA-ENADID-2023-spec.yaml`
(calc_id `CALC-APERTURA-ENADID-2023-0001`; payload con sha del manifiesto; los dos medidores sellados, sus
`resultados.json`, la receta `pisos_diseno.py`, `lectores.py`, `motor_pisos.py`, la guardia y el expediente común
como inputs `origen: repo` con sha). La apertura es copiarlo a
`data/corrida0/CALC-APERTURA-ENADID-2023-0001/spec.yaml` y correr (receta).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA vs RETROSPECTIVA: la primaria es PROSPECTIVA (contendientes en main desde `bf5fc5e7`, 27/sep, antes
  de cualquier R de estas celdas); las 18 celdas conyugales ya vistas se apartan y se reportan como RETROSPECTIVA;
  ninguna frase mezcla las dos columnas.
- Unidad: hogar y persona por celda; el MAE global mezcla ambas y no se lee como cantidad (§4).
- Escala: proporción 0..1; se compara «R dentro del IC del piso» (cobertura), no punto contra punto.
- Segmentación: un eje a la vez; ningún cruce. TLOC es tamaño de localidad, no clase; el sesgo de clase media
  urbana no se corrige aquí.
- No confundir estructura con cultura: jefatura femenina con migrante varón fuera es, primero, efecto de la
  migración (adaptación a la ausencia), no «matriarcado»; hogar ampliado y adulto mayor en hogar ampliado mezclan
  precariedad de vivienda, ausencia de pensión y cuidado: un cambio de nivel no se lee como cambio de valores
  familiares (familismo es evidencia (b) si viene de diáspora).
- Qué sería peligroso leído simplista: un SUBCUBRE no dice «la familia mexicana cambió»: dice que los pisos de 2018,
  con su IC, no anticipan 2023 en esa proporción de celdas.
- Cifras escritas a mano: ninguna; constantes = hashes fijados y umbrales (0.95, z = 1.959964), antes de abrir.

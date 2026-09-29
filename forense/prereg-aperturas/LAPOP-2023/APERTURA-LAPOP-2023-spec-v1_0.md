# Expediente de apertura · LAPOP AmericasBarometer México 2023 (reactivos de capital social) · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: los reactivos siguen
RESERVADOS (E.6); los levanta el código congelado de este expediente, en caja, en el commit que mesa autorice,
o mesa por escrito. Entorno de redacción: NUBE, sin corpus montado; no se leyó microdato ni reporte de 2023.

## 0 · Premisas

- [LEÍDO] Contendiente sellado: `CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001` (`spec.yaml` l. 25: «2004/2006/2019
  abiertas; 2023 RESERVADA para estos reactivos (E.6); 2021 fuera»; `sello.json`, commit `bf5fc5e7`, 27/sep/2026).
  20 conductas; pisos por ola sin serie (FIRMAS-15 T: ni τ² ni ICC). Regla 6: ningún contendiente nuevo.
- [EJECUTADO] **La reserva es por estimando, no por payload.** El microdato de 2023 está en el manifiesto como
  `mex_2023_lapop_americasbarometer_v1_0_w` (`.dta`, `raiz: descargas_mx`, sha256 `4a9410a5…e6765c`) y su gemelo
  `mex_2023_lapop_americasbarometer_v1_0_w_2` (`.sav`, sha256 `a355e4ca…61fa2a`); búsqueda por id con patrones
  `lapop|abmex|americas` sobre las 7 198 entradas. El `.dta` ya lo abrieron tres CALC sellados para OTROS
  reactivos: de los 390 `spec.yaml` de `data/corrida0/`, lo citan `CALC-LAPOP-PISOS-2023-0001` (b18, b21, pol1,
  eff1, eff2, d3, d4, estratopri, upm, wt), `CALC-0002` (aoj11, b18, aoj12, vic1ext + diseño) y
  `CALC-ARBITRO-MARGINALES-2-LAPOP-0001` (clien1na, vb2, vb3n, prot3, **ur**, vic1ext, mexwf1_19, countfair3, vb20 +
  diseño). **Ninguno lista un reactivo del contendiente** (it1, b12, b13, b20, b37, cp6, cp7, cp8, cp13, jc10,
  jc13, d5, b10a, b14, cp9, cp5, aut1, e16, q5b, q5a). `ur` sí se leyó en 2023 como eje de otros reactivos: su
  marginal está vista; los cruces conducta×UR no. Ninguno cita el `.sav` gemelo. Se usa el `.dta` (el formato que
  el corpus ya verificó).
- [EJECUTADO] **Hallazgo:** ninguno de los dos ids lleva `estado_reserva` en `data/manifiesto.yaml` y
  `tools/corpus_loader.motivo_reserva` devuelve `''` para ambos: la reserva de estos reactivos **la declara la spec
  sellada del contendiente**; por eso el expediente no figura aún en `data/corrida0/aperturas-pendientes-v1_0.tsv`.
  La receta (paso 4a) no tiene custodia que levantar: `raiz: descargas_mx`.
- [LEÍDO] Diseño de 2023: `wt`, `estratopri`, `upm` existen en el `.dta` (variables de `CALC-LAPOP-PISOS-2023-0001`;
  su universo dice «autoponderada (wt=1)»). Los ejes `q1`, `q2`, `ed` no los leyó ningún CALC sellado en 2023.
- [SUPUESTO→rama prevista] Nombres y códigos de los reactivos en 2023 no se conocen aquí (NUBE): se fijan **sobre la
  ola del piso** de cada conducta (2019 o 2006), rotulado así; §5.

## 1 · Estimandos

Por cada conducta y categoría de cada eje: **R = Σw·y / Σw** en LAPOP México 2023, y = 1/0 según la tabla (todo
otro código, incluidos 888888/988888/999999 de no respuesta y faltantes extendidos, queda fuera). Códigos fijados
sobre la ola del piso:

| conducta | columna | 1 | 0 | piso |
|---|---|---|---|---|
| CONFIANZA-INTERPERSONAL | `it1` | 1,2 | 3,4 | 2019 |
| CONFIA-FFAA | `b12` | 6,7 | 1–5 | 2019 |
| CONFIA-CONGRESO | `b13` | 6,7 | 1–5 | 2019 |
| CONFIA-IGLESIA-CATOLICA | `b20` | 6,7 | 1–5 | 2019 |
| CONFIA-MEDIOS | `b37` | 6,7 | 1–5 | 2019 |
| ASISTE-ORG-RELIGIOSA | `cp6` | 1,2 | 3,4 | 2019 |
| ASISTE-ASOC-PADRES | `cp7` | 1,2 | 3,4 | 2019 |
| ASISTE-COMITE-MEJORAS | `cp8` | 1,2 | 3,4 | 2019 |
| ASISTE-PARTIDO | `cp13` | 1,2 | 3,4 | 2019 |
| GOLPE-JUSTIFICADO-DELINCUENCIA | `jc10` | 1 | 2 | 2019 |
| GOLPE-JUSTIFICADO-CORRUPCION | `jc13` | 1 | 2 | 2019 |
| APRUEBA-HOMOSEXUALES-CANDIDATOS | `d5` | 6–10 | 1–5 | 2019 |
| RELIGION-MUY-IMPORTANTE | `q5b` | 1 | 2,3,4 | 2019 |
| ASISTE-SERVICIO-MENSUAL | `q5a` | 1,2,3 | 4,5 | 2019 |
| CONFIA-JUSTICIA | `b10a` | 6,7 | 1–5 | 2006 |
| CONFIA-GOBIERNO | `b14` | 6,7 | 1–5 | 2006 |
| ASISTE-ASOC-PROFESIONAL | `cp9` | 1,2 | 3,4 | 2006 |
| AYUDO-RESOLVER-PROBLEMA-COMUNIDAD | `cp5` | 1 | 2 | 2006 |
| LIDER-FUERTE-NO-ELEGIDO | `aut1` | 1 | 2 | 2006 |
| APRUEBA-JUSTICIA-PROPIA-MANO | `e16` | 6–10 | 1–5 | 2006 |

Ejes (uno a la vez): TOTAL (TODOS); SEXO `q1` 1 HOMBRE, 2 MUJER; EDAD `q2` 18–29/30–44/45–59/60-MAS; ESCOLARIDAD
`ed` (años) 0–6 HASTA-PRIMARIA, 7–9 SECUNDARIA, 10–12 MEDIA-SUPERIOR, 13–30 SUPERIOR; UR `ur` 1 URBANO, 2 RURAL.
13 categorías por conducta: **260 celdas**, todas con intervalo del piso. Ids: `<conducta>-<eje>-<cat>`.

**Ola del piso** (regla fijada antes de abrir): la última ola del contendiente con la conducta y P TOTAL finito en su
`resultados.json` sellado (2019 para las 12 de BASE y las 2 de sólo-2019; 2006 para las 6 de sólo-2004/2006). Un piso
de 2006 contra 2023 es un piso 17 años atrás: se puntúa igual (una sola comparación primaria) y se reporta aparte
como secundaria.

**Intervalo del piso** (lo, hi): IC de diseño IC-LO/IC-HI de la ola del piso (bootstrap de UPM dentro de estrato,
percentiles 2.5/97.5; sin ICC por FIRMAS-15 T). Punto: su P. Se leen del `resultados.json` sellado; nada se recalcula.

## 2 · Universo, unidad, ponderador, diseño

Unidad persona. El archivo es sólo México (sin filtro de país). Registro válido: `wt` finito > 0, `estratopri` y
`upm` no vacíos (la regla `prepara_diseno` del contendiente, con el diseño de su ola 2019); universo `q2 ≥ 18`.
`wt`, `estratopri`, `upm` o `q2` ausentes en 2023 → PARO antes de leer una fila (sólo metadatos leídos); `q1`, `ed`
o `ur` ausentes → ese eje NO-ESTIMABLE. Payload: `mex_2023_lapop_americasbarometer_v1_0_w`. R es un punto.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo:
`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera
de `lee_payload_reservado` → PARO. La lectura trae sólo las columnas pedidas (reactivos del contendiente + diseño +
ejes). Probado por mutación sobre sintético: `tests/test_prereg_aperturas.py` y `tests/test_apertura_lapop_2023.py`
(con soporte, conducta sin soporte, categoría vacía, ejes ausentes como en 2021, conducto `medir()` completo sobre
un `.dta` sintético, PARO sin UPM).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del piso y R finitos. **Primaria** (una sola): cobertura k/n = #celdas con lo ≤ R ≤ hi, con
IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si
Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Orden: NO-ESTIMABLE > SUBCUBRE >
SOBRECUBRE > CALIBRADO (excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por
conglomerado (= conducta), por ola del piso (2019 / 2006) y error absoluto medio punto-del-piso vs R.
B-bis: CALIBRADO = pisos **corroborados en alcance** para 2023; SOBRECUBRE = pisos **acotados**; SUBCUBRE = los pisos
por ola, sin serie, no anticipan 2023. Prevista: SUBCUBRE (IC de muestreo sin τ², pisos de 4 y 17 años antes, y 2021
—ruptura de modo— en medio); se declara ahora. Un solo contendiente sellado; no hay otro que servir.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- [LEÍDO] El contendiente dejó fuera 2021 porque «no trae `q1`/`ed`/`ur` ni casi ningún reactivo de la lista»
  (ruptura de modo CATI). Si 2023 repite esa estructura, los ejes SEXO/ESCOLARIDAD salen NO-ESTIMABLE y el TOTAL y
  EDAD siguen; `ur` se sabe presente en 2023 (leído por `CALC-ARBITRO-MARGINALES-2-LAPOP-0001`).
- Regla fijada: **columna ausente en 2023 → esa conducta sale NO-ESTIMABLE** (se omite R; no se recodifica ad hoc).
  Los 6 reactivos de sólo-2004/2006 probablemente no están en 2023 (no estaban en 2019): NO-ESTIMABLE esperado.
- Nombre presente con otra pregunta o escala: la receta (paso 3, preflight documental con el cuestionario/libro de
  códigos de 2023, que no es abrir) compara texto y códigos contra la ola del piso; si alguno no casa, la apertura
  **no corre con v1.0**: se re-sella una v1.1 de esta spec y del medidor antes de abrir, y se declara.
- 2023 es autoponderada (`wt` = 1, LEÍDO del CALC sellado de 2023); 2019 traía `wt` variable: R ponderada con `wt`
  en los dos casos, sin cambio de regla.

## 6 · Salidas

`RESULT-APERTURA-LAPOP-2023-<conducta>-<eje>-<cat>-R` (260), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`, `-MAE-PUNTO`,
`-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.

Contrato: `APERTURA-LAPOP-2023-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-LAPOP-2023-0001`; payload
con sha del manifiesto; medidor sellado del contendiente, su `resultados.json`, `motor_pisos.py`, la guardia y la
plantilla común como inputs `origen: repo` con sha).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: el contendiente se selló (27/sep/2026) antes de que exista R para estos reactivos;
  los cruces que sí se vieron en 2023 (otros reactivos, marginal de `ur`) no entran. Ninguna frase mezcla esta
  cobertura con marcadores RETROSPECTIVOS.
- Unidad: **persona**; nada se promedia con hogar, delito o trámite. Escala: proporción 0..1 de cortes declarados
  (6–7 de 1–7; 6–10 de 1–10; semanal/mensual); no se compara con Latinobarómetro (1–4) ni Pew sin función de enlace.
- Procedencia (§3): **(a)** datos primarios en México (entrevistas a residentes). Los constructos son **(c)** marcos
  importados (capital social à la Putnam, confianza institucional, justificación de golpe): asistir a una
  «asociación de padres» o a un «comité de mejoras» es oferta de organizaciones en el entorno, no disposición cívica;
  la justificación de un golpe «ante mucha delincuencia» es evaluación de seguridad, no autoritarismo de carácter.
- Segmentación: un eje a la vez (sexo, edad, escolaridad, urbano/rural); UR aproxima lo rural; no hay eje de
  clase ni muestra indígena propia; el sesgo de clase media urbana no se corrige aquí y se declara.
- Estructura ≠ cultura: confianza en policía, jueces o congreso sigue a desempeño institucional medible; la
  participación sigue a oferta y a tiempo disponible (oferta antes que preferencia).
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «el capital social del mexicano cambió»; dice que
  los pisos de 2019/2006, con su IC de muestreo, no anticipan 2023 en esa proporción de celdas.
- Cifras escritas a mano: ninguna; constantes = hashes fijados, nombres y códigos leídos del medidor sellado,
  umbrales de la regla (0.95, z = 1.959964), declarados antes de abrir.

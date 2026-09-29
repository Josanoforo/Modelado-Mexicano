# Expediente de apertura · ENIGH 2024 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6) salvo las columnas ya leídas por código congelado (§0); la levanta el código congelado de este
expediente, en caja, en el commit que mesa autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Contendientes sellados que declaran `2024 RESERVADA (E.6), no es input` (etiqueta `olas` de su `spec.yaml`;
  regla 6: ninguno nuevo):
  - `CALC-ENIGH-CONSUMO-PISOS-0002` — pisos de consumo y gasto 2016–2022, unidad hogar, con **IC calibrado de
    persistencia** ICC-LO/ICC-HI sobre el piso 2022 (spec `forense/prereg-caja/CONSUMO-ENIGH-PISOS-spec-v1_1.md`).
    Sellado el 25/sep/2026 (20:30:34Z). Es SUCESOR de 0001 (`sucesion.json`: `repite_de`).
  - `CALC-ENIGH-CONSUMO-PISOS-0001` — mismo procedimiento e ids (spec v1.0), con `gastoshogar` 2016/2018 del ZIP
    integrado truncado en 1 048 575 filas (hallazgo que motivó 0002). Sellado 25/sep (20:23:15Z).
  - `CALC-PDR1-ENIGH2022-0001` — regla RG-cc1c9ab8f1 (escuela privada de la clase media urbana), unidad hogar, una
    ola (2022) con **IC95 de diseño** IC-LO/IC-HI (bootstrap UPM; spec `forense/prereg-caja/PDR1-ENIGH2022-spec-v1_0.md`).
    Sellado el 28/sep/2026 (20:16:17Z).
- [EJECUTADO] Ids de la ola: fila `ENIGH 2024` de `data/corrida0/aperturas-pendientes-v1_0.tsv` (18 ids; hoy dice
  «contendientes: NINGUNO» — hallazgo: la vista no ve a los tres de arriba). Payloads de este expediente (lector YAML
  del manifiesto por id; los cinco «ZIP-OK(1 miembros)», `raiz: data_raw`): `cc1_inegi_enigh_2024__enigh2024_ns_
  {concentradohogar,hogares,gastoshogar,poblacion,gastospersona}_csv`.
- [LEÍDO] Cruces ya vistos por código congelado (E.6: un cruce visto se declara): `CALC-AMAI-NSE-ENIGH-2024-0001`
  (25/sep, 19:56:00Z; C7) parseó de `enigh2024_nc_csv` `concentrado.{folioviv, foliohog, educa_jefe, ocupados, factor,
  est_dis, upm}`, `hogares.{folioviv, foliohog, conex_inte, num_auto, num_van, num_pick}` y `viviendas.{folioviv,
  cuart_dorm, bano_comp}` (su `RESULT-…-COLUMNAS-LEIDAS`) y emitió sólo la distribución nacional de NSE;
  `CALC-ENIGH-DUELO-EMISIONES-0001` (22/sep) leyó `concentradohogar.{folioviv, foliohog, factor, remesas, est_dis, upm}`
  y emitió sólo `remesas > 0` nacional. **Ninguna celda de los contendientes fue emitida** por esos CALC. Tocan columnas
  ya parseadas: `HOG-CONEX-INTERNET-*` y `HOG-COMPRA-INTERNET-SI-CONEXION-*` (conex_inte), todo el eje
  `ESCOLARIDAD-JEFE` (educa_jefe) y el diseño (factor, est_dis, upm). Las R de esas celdas no existían emitidas cuando
  se sellaron los contendientes, así que la marca sigue PROSPECTIVA, **con reserva «columna parseada por código
  congelado anterior»** (la distribución NSE es función, entre otras, de educa_jefe y conex_inte). Los contendientes
  CONSUMO se sellaron 27–35 min después de AMAI; PDR1, tres días después. `remesas` no entra en ninguna celda.
- [EJECUTADO] Ninguna familia 2027 la usa como R (`familias-2027-estado-v1_0.tsv`: las 8 familias apuntan a olas 2027).
- [SUPUESTO→rama prevista] Cuestionario y descriptor de 2024 no montados (NUBE): **columnas y códigos** se fijan sobre
  la ola del piso (2022, los de los contendientes), rotulado así; la diferencia se declara al abrir (§5). La lectura de
  AMAI confirma que existen en 2024 `folioviv`, `foliohog`, `educa_jefe`, `factor`, `est_dis`, `upm`, `conex_inte`.

## 1 · Estimandos

**CONSUMO** (34 conductas de `CALC-ENIGH-CONSUMO-PISOS-0002`, spec v1.1 §2, con su recodificación exacta): por cada
conducta y cada categoría de cada eje, R en ENIGH 2024 con el mismo peso que el contendiente:
- `PART-*` (20: nueve rubros de `gasto_mon`, comunicaciones, alimentos fuera y bebidas en alimentos, efectivo en gasto
  directo G1, siete canales de compra de alimentos A001–A242 por `lugar_comp`): **razón de totales** Σw·num / Σw·den
  entre hogares con den > 0 (se obtiene con y = num/den y peso w·den);
- `HOG-*` (14: proporción de hogares 0/1: gasto en alimentos fuera y en comunicaciones > 0; celular, internet y tarjeta
  de crédito = 1 de {1,2}; usa tarjeta en alimentos si tiene; pagos de tarjeta, deudas y préstamos > 0; gasto > ingreso;
  compra fiada (forma de pago 2), con tarjeta de crédito (5) o por internet (lugar 18); internet si hay conexión):
  **Σw·y / Σw**.
Ejes (uno a la vez): TOTAL; SEXO-JEFE (1, 2); EDAD-JEFE (HASTA-29, 30-44, 45-59, 60-MAS); ESCOLARIDAD-JEFE (`educa_jefe`
1–4, 5–6, 7–8, 9–11); TLOC (`tam_loc` 1 100MIL-MAS … 4 MENOS-2500); DECIL (deciles de hogares por `ing_cor`,
participación acumulada del factor, decil = ⌈10·acumulada⌉ acotado a 1..10); ENTIDAD (dos primeros dígitos de
`folioviv` a 10 posiciones, 01–32) sólo en PART-ALIMENTOS, PART-CANAL-SUPER-MEMBRESIA, HOG-TIENE-TARJETA-CREDITO,
HOG-COMPRA-INTERNET. **978 celdas** (4 × 57 + 30 × 25). `MEDIA-GASTO-MON-MENSUAL` queda fuera (media en pesos corrientes
sin ICC en el contendiente: se aparta sin abrir).

**PDR1** (`CALC-PDR1-ENIGH2022-0001`, spec §1–§3, con su recodificación exacta): universo = hogares con al menos un
integrante que asiste a la escuela (`poblacion.asis_esc` = 1). PRIV = hogar con gasto G1 en inscripción o colegiatura
(`gastospersona` claves E001–E007 con `inscrip` > 0 o `colegia` > 0) de un integrante en escuela privada
(`tipoesc` = 2); ASIPRIV = hogar con algún integrante que asiste a escuela privada; CARGA = Σw·gasto_tri(PRIV) /
Σw·ing_cor entre hogares PRIV con ing_cor > 0 (razón de totales). Celdas: PRIV y ASIPRIV × ámbito (TOTAL `tam_loc`
1–4, URBANO 1–3, RURAL 4) × (TODOS, D01–D10, B1-IV, B2-VIII, B3-X); CARGA × (TOTAL, URBANO) × lo mismo; PRIV por
segmento TLOC (4), SEXO-JEFE (2), EDAD-JEFE (4). **122 celdas** (2 × 3 × 14 + 2 × 14 + 10). Las seis diferencias DIF-*
y el dictamen RG-cc1c9ab8f1 quedan fuera de la primaria (combinaciones lineales de celdas ya puntuadas: su lectura con
R 2024 es derivable de las R emitidas y del IC sellado, como descriptivo).

Total: **1 100 celdas**, cada una con una sola unidad (hogar).

## 2 · Universo, unidad, ponderador, diseño

Unidad **hogar**. Registro válido: `factor` > 0, `est_dis` y `upm` no vacíos (en `concentradohogar`); llave hogar =
`folioviv` (10 posiciones) + `foliohog`; persona = llave hogar + `numren`. Ponderador `factor`; en PART-* y CARGA,
factor × denominador. Payloads: descarga **por tabla** de 2024 (cinco ZIP de un solo miembro .csv; se lee el único
.csv, `utf-8-sig`, por bloques de 200 000 filas; `gastospersona` filtrado por bloque a claves E001–E007). Se prefiere la
descarga por tabla al ZIP integrado `enigh2024_nc_csv` porque el integrado de 2016/2018 venía truncado (la razón de la
sucesión 0001 → 0002); decisión de logística, no de estimando. Un ZIP que no tenga exactamente un .csv → PARO. R es un
punto; la cobertura se mide contra el IC ya sellado de cada contendiente.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce levanta
`ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo (`groupby`/
`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera de
`lee_payload_reservado` → PARO). En PDR1 el **ámbito** es una restricción de universo pre-registrada por el
contendiente (R = NaN fuera del ámbito) y la agrupación es una sola variable (TODOS, decil o bloque); no se computa
ningún cruce que el contendiente no haya sellado. Reuso por bytes con sha256 fijado: de CONSUMO-0002 `prepara`
(uniones hogar–gasto, ejes, deciles), `conducta`, `ejes_de`, `CONDUCTAS`, columnas y `rid`; de PDR1 `prepara`
(universo, PRIV/ASIPRIV/monto, ámbitos, segmentos, deciles), columnas, claves, ámbitos, bloques, segmentos y `rid`; de la
receta `num`. Los `prepara` sellados suman renglones de gasto a su hogar con un `groupby` de UNA llave (la llave hogar):
construye la unidad, no cruza; su código está fijado por sha y no lo audita este archivo. Probado por mutación y sobre
sintético: `tests/test_prereg_aperturas.py` y `tests/test_apertura_enigh_2024.py` (cinco tablas sintéticas; con soporte;
conducta sin soporte; categoría vacía; R idéntica al punto de `mide_ola` de CONSUMO y de `mide` de PDR1 en las 1 100
celdas).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. **Primaria** (una sola, sobre las 1 100 celdas de CONSUMO-0002 y
PDR1 juntas): cobertura k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado:
**CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95;
**NO-ESTIMABLE** si n = 0. Si dos filas pudieran satisfacerse a la vez, manda el orden NO-ESTIMABLE > SUBCUBRE >
SOBRECUBRE > CALIBRADO (son excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por
conglomerado (`CONSUMO-<conducta>`, `PDR1-<conducta>`, `PDR1-PRIV-SEG`; todas las celdas comparten la muestra ENIGH
2024) y error absoluto medio punto-del-piso vs R.
B-bis: CALIBRADO = los pisos 2022 quedan **corroborados en alcance** para 2024; SOBRECUBRE = **acotados** (IC
conservador); SUBCUBRE = no anticipan la ola. Declarado antes de abrir: las dos familias de IC no son iguales — el ICC de
CONSUMO incorpora la deriva entre olas; el IC de PDR1 es sólo de diseño 2022 y tiende a SUBCUBRE ante cualquier cambio
real; la primaria los junta en una sola comparación (E.6: una sola comparación primaria por apertura) y la nota de
apertura reporta la cobertura por contendiente como secundaria.
**Contendientes servidos a la vez (E.6)**: CONSUMO-0002 y PDR1 en la primaria. **CONSUMO-0001 se aparta de la primaria
sin abrir**: SUSTITUIDO-POR 0002 (`sucesion.json`); sus celdas tienen los mismos ids y la misma R (procedimiento 2022–2024
idéntico), y su ICC difiere sólo por τ² calculado con `gastoshogar` 2016/2018 truncado; su cobertura queda servida por
las R emitidas y se reporta, si se pide, como descriptivo PROSPECTIVO secundario, nunca en la primaria (contarla dos
veces duplicaría celdas que no son independientes).

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Fuente: 2022 del ZIP integrado `enigh2022_nc_csv` (miembros `conjunto_de_datos_<tabla>_enigh2022_ns.csv`); 2024 de la
  descarga por tabla (un .csv por ZIP). Mismo contenido [SUPUESTO; 0002 aceptó la descarga por tabla como equivalente
  del integrado para `gastoshogar` 2016/2018]; ningún tabulado ni comunicado de 2024 se lee para comprobarlo.
- Deciles 2024: los de TODOS los hogares 2024 con su factor (no los cortes 2022).
- Pesos corrientes 2024 en todos los montos (no deflactados); en PART-* y CARGA la razón no depende del nivel de precios.

Regla fijada: si en caja, antes de correr, el descriptor de 2024 no trae una columna de un contendiente, **las celdas que
dependen de ella salen NO-ESTIMABLE** (el código la lee vacía y omite su R). Una ausencia que ya da NaN por construcción
(un monto o un código vacío) se deja así; las que darían un falso 0 se apagan explícitamente: gastoshogar
(`clave`, `tipo_gasto`, `forma_pag1–3`, `lugar_comp`, `gasto_tri`, llaves) → PART-EFECTIVO-EN-GASTO-DIRECTO,
HOG-COMPRA-FIADO, HOG-COMPRA-TARJETA-CREDITO, HOG-COMPRA-INTERNET, HOG-COMPRA-INTERNET-SI-CONEXION (esta también
`hogares.conex_inte`); gastospersona (llaves, `numren`, `clave`, `tipo_gasto`, `inscrip`, `colegia`, `gasto_tri`) o
`poblacion.{tipoesc, asis_esc, numren}` → PDR1-PRIV (y su segmento) y PDR1-CARGA (esta también `ing_cor`);
`poblacion.{tipoesc, asis_esc}` → PDR1-ASIPRIV. Un eje sin su columna queda sin categorías (R None). No se recodifica
ad hoc. Si la columna existe pero cambió su texto o códigos, el código congelado no puede omitirla: no se parcha
(D-18), vuelve a mesa.

## 6 · Salidas

`RESULT-APERTURA-ENIGH-2024-<id de celda>-R` (1 100; ids `CONSUMO-<conducta>-<eje>-<cat>`, `PDR1-<conducta>-<ámbito>-<cat>`,
`PDR1-PRIV-<eje>-<cat>`; tipo flotante porque CARGA es una razón), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`,
`-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE, Wilson y MAE cuando n = 0.

Contrato: `APERTURA-ENIGH-2024-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-ENIGH-2024-0001`; cinco payloads
con sha del manifiesto; medidores sellados de CONSUMO-0002 y PDR1, sus `resultados.json`, la receta, la guardia y la
plantilla como inputs `origen: repo` con sha). La apertura es copiarlo a `data/corrida0/CALC-APERTURA-ENIGH-2024-0001/
spec.yaml` y correr (receta `RECETA-APERTURA-ENIGH-2024.md`).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción (contendientes sellados antes de que exista cualquier R de sus celdas), con la reserva de
  §0 para las celdas que tocan columnas ya parseadas por AMAI. Ninguna frase mezcla esta cobertura con los marcadores
  RETROSPECTIVOS del duelo de remesas.
- Unidad: **hogar** en todas las celdas; nada se promedia con persona, delito o trámite (PDR1 usa personas sólo para
  construir la condición del hogar).
- Escala: proporción de hogares o razón de totales (0..1 en la práctica) en R y en los pisos; «R dentro del IC»
  (cobertura), no punto contra punto; el MAE de punto es descriptivo.
- Segmentación: un eje a la vez (sexo, edad y escolaridad del jefe, tamaño de localidad, decil, entidad); el decil es la
  única aproximación a clase y es ingreso corriente, no clase; PDR1 nombra «clase media urbana» por decil V–VIII urbano:
  el sesgo de clase media urbana formal es el objeto, no un supuesto.
- Oferta antes que preferencia (§3): canal de compra, tarjeta de crédito, compra fiada, internet y escuela privada son
  conductas de mercado; su lectura exige la oferta al lado (bancarización y terminales, conectividad, supermercados y
  escuelas por localidad). Una cobertura no dice nada de preferencia.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «el consumo del mexicano cambió» ni que «la clase media
  abandonó la escuela privada»; dice que los pisos 2022 con sus IC no anticipan 2024 en esa proporción de celdas
  (inflación, programas sociales y ciclo incluidos).
- Cifras escritas a mano: ninguna; constantes = hashes fijados, claves y códigos de los contendientes y umbrales de la
  regla (0.95, z = 1.959964), declarados antes de abrir.

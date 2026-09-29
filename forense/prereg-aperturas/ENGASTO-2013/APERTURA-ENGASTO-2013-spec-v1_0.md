# Expediente de apertura · ENGASTO 2013 · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), escrito en NUBE sobre `7393b17e`, sin corpus
montado. Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que mesa
autorice, o mesa por escrito.

## 0 · Premisas

- [LEÍDO] Contendiente sellado (regla 6: ningún contendiente nuevo): `CALC-ENGASTO-CONSUMO-PISOS-0001`,
  `spec.yaml:23` «olas: 2012 abierta; 2013 (carpeta engasto2013/) RESERVADA (E.6), no es input»; spec humana
  `forense/prereg-caja/CONSUMO-ENGASTO-PISOS-spec-v1_0.md` §0–§4; 22 conductas de hogares, IC95 de **diseño**
  (bootstrap UPM en `est_dis`, 1 000 réplicas), **sin IC de persistencia** (una sola ola abierta).
- [LEÍDO] Identidad de ola por contenido, no por rótulo: `forense/analisis/consumo-gasto/lista-cerrada-P1.md` §1
  (HOGAR de `engasto2013/`: sha `bb17939d…`, 58 371 filas, 173 campos con `num_cel1/2`, `recurso_1…6`,
  `cubr_gasto`, `ahorro`; no casa con el FD 2012). Esa lectura fue de metadatos `.dta` por otro acto: aquí es
  REPORTADO para el trazado de columnas y se re-verifica en caja con el preflight documental (§5).
- [EJECUTADO] Manifiesto por id (A.15; `yaml.CSafeLoader`, 7 198 entradas; filtro `archivo` empieza por
  `engasto2013/`: **21 ids**; ids `engasto_2013_*`: 19). Payloads elegidos por `archivo` y rol (mismo rol que los
  cuatro inputs 2012 del contendiente), sin abrirlos:
  `engasto_2012_hogar_dta` → `engasto2013/hogar_dta.zip` (sha `bb17939d…`, **id con rótulo 2012**; es el HOGAR
  2013 de la lista-cerrada §1); `engasto_2013_viviendas_dta` → `engasto2013/viviendas_dta.zip`;
  `engasto_2012_gasto_de_consumo_ajustado_dta` → `engasto2013/gasto_de_consumo_ajustado_dta.zip` (**id con
  rótulo 2012**). El defecto de rotulación ya estaba declarado (lista-cerrada §1) y no se edita aquí.
- [EJECUTADO] **LUGAR_COMPRA 2013: NO-ENCONTRADO** en el manifiesto (universo: las 21 entradas con `archivo`
  `engasto2013/`; términos `lugar`, `compra` en `archivo`: 0 aciertos). Sólo existe `engasto2012/lugar_compra_*`.
  Consecuencia fijada antes de abrir: las 20 conductas que leen `lc_*` salen **NO-ESTIMABLE** (§5).
- [EJECUTADO] Reserva: ninguno de los tres payloads lleva `estado_reserva` en el manifiesto y
  `tools/corpus_loader.py` no los reserva; **la reserva la declara la spec sellada del contendiente** (hallazgo;
  la receta §4a no tiene custodia que levantar: `raiz` actual del manifiesto).
- [EJECUTADO] Ninguna corrida lee la ola: `grep` de los 390 `data/corrida0/*/spec.yaml` por los tres ids y por
  `engasto2013/` → 1 archivo, el del contendiente, que la nombra sólo como reservada. Cruces vistos: ninguno.
- [SUPUESTO→rama prevista] El FD/cuestionario 2013 no está en corpus (lista-cerrada §1): los códigos se fijan
  **sobre el FD 2012** (los del contendiente), rotulado así; la diferencia se declara al abrir (§5).

## 1 · Estimandos

Por cada una de las 22 conductas del contendiente y cada categoría de cada eje (TOTAL; SEXO-JEFE 2; EDAD-JEFE 4;
ESCOLARIDAD-JEFE 4; TLOC 4 = 15 celdas por conducta, **330 celdas**): **R = Σw·y / Σw** en ENGASTO 2013, con la
recodificación del contendiente (medidor sellado importado por bytes, sha256 fijado en
`APERTURA-ENGASTO-2013-spec.yaml`). Códigos (FD 2012; `lista-cerrada-P1.md` §3, §5):
- `lc_granc` y los cinco productos (`lc_carne`, `lc_fruta`, `lc_verdura`, `lc_pan`, `lc_leche`): universo códigos
  01–18 (97 y nulo fuera); GRAN-COMPRA-SUPER-MEMBRESIA {6, 9}, MERCADO {1}, TIANGUIS-AMBULANTE {2, 3}, ABARROTES {4},
  CONVENIENCIA {10}, DEPARTAMENTAL {7}, INTERNET {18}, OTRO {5, 8, 11–17}; {producto}-EN-SUPER-MEMBRESIA {6, 9},
  -EN-MERCADO-TIANGUIS-AMBULANTE {1, 2, 3}.
- COMPRA-INTERNET-ALGUN-RUBRO: algún `lc_*` (76) = 18, universo algún `lc_*` en 01–18; -SI-CONEXION: además
  `conex_inte` = 1.
- TIENE-CELULAR: `num_cel` ≥ 1, universo 0–50. CONEX-INTERNET: `conex_inte` = 1, universo {1, 2}.
- Ejes: `sexo_je` 1 HOMBRE / 2 MUJER; `edad_je` HASTA-29, 30-44, 45-59, 60-MAS; `ned_je` 1 PRIMARIA-INCOMPLETA,
  2 PRIMARIA-COMPLETA, 3 SECUNDARIA-COMPLETA, 4 MEDIA-SUPERIOR-Y-SUPERIOR; `tam_loc` 1 100MIL-MAS, 2 15MIL-99MIL,
  3 2500-14999, 4 MENOS-2500.

## 2 · Universo, unidad, ponderador, diseño

Unidad **hogar**. HOGAR (`factor_hog`), llave `anio_reg+trimestre+folio+hog_ent_1+hog_ent_2`; VIVIENDAS por
`anio_reg+trimestre+folio` (`tam_loc`, `est_dis`, `upm`); jefe (`sexo_je`, `edad_je`, `ned_je`) de
GASTO_DE_CONSUMO_AJUSTADO, una fila distinta por hogar (inconsistente → fuera del eje). Válido: `factor_hog > 0`,
`est_dis` y `upm` no vacíos; uniones sólo por llaves únicas (`prepara()` del contendiente). R es un punto; no se
calcula IC de R (la cobertura se mide contra el IC del contendiente).

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo:
`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera de
`lee_payload_reservado` → PARO. `lee_payload_reservado` PARA si la ruta resuelta no está bajo `engasto2013/`
(inverso de la guardia del contendiente). Probado por mutación y con sintético del esquema del contendiente:
`tests/test_apertura_engasto_2013.py` (con soporte, conducta sin soporte, categoría vacía, `.dta` en ZIP con
columna ausente, PARO por ponderador ausente y por carpeta equivocada; cada mutación de
`expediente_apertura.MUTACIONES` detectada) y `tests/test_prereg_aperturas.py` (ramas terminales por
`corrida0._valida_outputs`).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del contendiente y R finitos. lo/hi = **IC95 de diseño del piso 2012**
(`RESULT-ENGASTO-CONSUMO-PISOS-<c>-2012-<eje>-<cat>-IC-LO/-IC-HI`; punto = `-P`); las 330 celdas lo tienen en el
`resultados.json` sellado. **Primaria** (una sola): cobertura k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al
95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95;
**SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0. Orden si dos pudieran satisfacerse:
NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO (excluyentes por construcción). Secundarias, descriptivas, no
adjudican: cobertura por conglomerado (conducta: sus 15 celdas comparten muestra), recalculable de R y lo/hi, y
error absoluto medio punto-2012 vs R (`-MAE-PUNTO`).
**Advertencia fijada antes de abrir**: el IC del contendiente es de muestreo de 2012, no un intervalo de
predicción entre olas; un año de distancia y un cambio de cuestionario lo hacen estrecho frente a la ola nueva.
B-bis: CALIBRADO = piso **corroborado en alcance** para 2013; SOBRECUBRE = piso **acotado** (IC conservador);
SUBCUBRE = el piso 2012 con IC de diseño no anticipa 2013 (resultado esperable de un IC sin persistencia; no
dice que la conducta cambió). Una apertura sirve a todos los sellados antes: el único contendiente sellado es
`CALC-ENGASTO-CONSUMO-PISOS-0001`.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- LUGAR_COMPRA 2013 sin id en el manifiesto: el medidor construye esa tabla con las llaves del hogar y las 76
  `lc_*` vacías → las 8 GRAN-COMPRA-*, las 10 {producto}-EN-* y las 2 COMPRA-INTERNET-* salen sin R (**NO-ESTIMABLE
  por construcción**). Si el acto de apertura consigue la tabla, es otro expediente, no una enmienda de éste.
- HOGAR 2013 trae `num_cel1/num_cel2` y no `num_cel` (REPORTADO, lista-cerrada §1) → TIENE-CELULAR sale
  NO-ESTIMABLE; no se recodifica desde `num_cel1/2`.
- Tabla de vivienda en plural (`viviendas`): mismo rol; se usan sus `anio_reg`, `trimestre`, `folio`, `tam_loc`,
  `est_dis`, `upm`.
- `recurso_*`, `cubr_gasto`, `ahorro` (nuevos en 2013): fuera; el contendiente no los usa.

Regla fijada, mecánica: columna de reactivo o de eje ausente del archivo → entra vacía (NaN) → las celdas que
la usan salen NO-ESTIMABLE; columna de llave, `factor_hog`, `est_dis` o `upm` ausente → **PARO** (no hay universo
que medir). Si en caja, antes de correr, el FD/cuestionario de 2013 no trae una columna del contendiente con el
mismo texto de pregunta y códigos, esa conducta se declara NO-ESTIMABLE en la nota de apertura (su R no se
lee como R de esa conducta; no se recodifica ad hoc). Leer el FD y el cuestionario no es abrir (E.6).

## 6 · Salidas

`RESULT-APERTURA-ENGASTO-2013-<conducta>-<eje>-<cat>-R` (330), `-DICTAMEN`, `-K`, `-N`, `-WILSON-LO/HI`,
`-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). None sólo en R de celdas NO-ESTIMABLE y en Wilson/MAE cuando n = 0.
Contrato: `APERTURA-ENGASTO-2013-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-ENGASTO-2013-0001`;
payloads con sha del manifiesto; medidor sellado del contendiente, su `resultados.json`, la receta
`pisos_diseno.py`, la guardia y el expediente común como inputs `origen: repo` con sha). La apertura es copiarlo a
`data/corrida0/CALC-APERTURA-ENGASTO-2013-0001/spec.yaml` y correr (receta).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: el contendiente se selló (en main desde `bf5fc5e7`, 27/sep) antes de que exista
  cualquier R de 2013; ninguna corrida lee la ola (§0). Ninguna frase mezcla esta cobertura con marcadores
  RETROSPECTIVOS.
- Unidad: **hogar** en R y en el piso; nada se promedia con persona, delito o trámite.
- Escala: proporción 0..1 en R y en el piso; se compara «R dentro del IC del piso» (cobertura), no punto contra
  punto; el MAE es descriptivo.
- Segmentación: un eje a la vez (sexo, edad y escolaridad del jefe; tamaño de localidad); ningún cruce. TLOC es
  tamaño de localidad, no clase; el sesgo de clase media urbana no se corrige aquí.
- Oferta antes que preferencia (§3): «dónde compra» es primero dónde **hay**; en esta ola esas conductas salen
  NO-ESTIMABLE, y si una apertura futura las mide, un SUBCUBRE en TLOC rural no se lee como gusto.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice «el consumo del mexicano cambió en un año»: dice que
  un IC de muestreo de 2012 no anticipa 2013. Y la cobertura de este expediente descansa en a lo sumo 30 celdas
  (TIENE-CELULAR y CONEX-INTERNET), o 15 si `num_cel` falta: n pequeño, Wilson ancho.
- Cifras escritas a mano: ninguna; las constantes del medidor son hashes fijados y umbrales de la regla (0.95
  nominal, z = 1.959964), declarados antes de abrir.

# C2 RESTRINGIDO A QUIEN TRABAJA · ENIF 2024 · los cinco pares con `formalidad` del lote — spec v1.0

**Universo, unidad y escala, en la primera línea.** Personas elegidas de 18 años y
más de ENIF 2024 (`TMODULO.csv`) **que llegan a la pregunta 3.13 y la contestan
con un código 1–7** —«quien trabaja», universo **T**—, ponderadas por `FAC_PER`,
con `EST_DIS` × `UPM_DIS` como estrato y conglomerado. La cantidad estimada es una
**proporción de personas de T en `[0,1]`**. Ninguna cifra de esta spec se compara
contra un marginal o un C2 del universo poblacional (A-bis 4): T no es la
población y el C2 de aquí no reconcilia con el C2 compuesto sellado.

> `ACTO GEN2-DIN-LOTE-C2-RESTRINGIDO-1`, 22/sep/2026, **CAJA**, rama
> `acto/gen2-din-lote-c2-restringido-1`, base `ccd7c0eb`, 0-bis `4e123a98`.
> Encargo archivado (A.3): `forense/encargos/2026-09-22-GEN2-DIN-LOTE-C2-RESTRINGIDO-1.md`
> (sello de cuerpo `53cd0775…`). CALC reservado:
> `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001`. Contrato ejecutable:
> `data/corrida0/CALC-C2-RESTRINGIDO-IC-ENIF2024-0001/spec.yaml`; código que mide:
> el `medidor.py` de ese directorio. **Ningún parámetro vive en dos sitios**: los
> números están en `spec.yaml`; aquí, las reglas.
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**
> No hay segunda corrida elegible, no hay recorte de réplicas, no hay sustitución
> de marginales y no hay ajuste post-hoc de la forma, del universo ni de los
> umbrales.

---

## 0 · Firma, exposición y lo que ya existe

**Firma que gobierna (A.12, viaja verbatim en el encargo y la asienta este acto):**
`FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-02`, opción **B** — «Los 5 pares
NO-EMITIBLE por universo restringido de formalidad se sellan aparte con un
C2-restringido a quien trabaja, con su universo declarado en cada RESULT, nunca
comparado contra el marginal poblacional.» Cita sellada del hallazgo:
`FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-02` (Q1).

**Exposición declarada (ADR-46).** Leídos antes de congelar: el dictamen
`data/corrida0/c2-compuesto-dictamen-v1_0.tsv`; la spec y el medidor sellados de
`CALC-C2-COMPUESTO-IC-ENIF2024-0001`; la spec y los `resultados.json` sellados de
`CALC-ARBITRO-MARGINALES-ENIF2024-0001` (incluidos sus marginales por eje de D9,
con sus cifras a la vista); el medidor sellado del piso
`CALC-PISOS-ENIF2021-EJES-0003/medidor.py`; el contrato sellado del lote
`CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/spec.yaml`; el árbitro GEN1
`tools/medidor_ahorro_enif24.py`; el FD `enif_2024_fd.xlsx` (hoja `TMODULO`,
filas 138–146). **NO abierto:** ninguna respuesta de `TMODULO.csv` de ENIF 2024
en esta sesión antes del COMMIT-2. Ninguna cifra esperada: ningún marginal
restringido a T existe sellado (abajo), así que no hay número contra el cual
ajustar.

**Ya hecho / ya decidido, buscado por objeto (A.4, A.13).** Sobre `ccd7c0eb`:
los 7 `resultados.json` distintos de `data/corrida0/CALC-*ENIF2024*` y `CALC-DIN-LOTE-*`
examinados por id con `FORMALIDAD|TRABAJ|RESTRING`: el único marginal sellado
con universo T es el propio eje `formalidad` del árbitro GEN2
(`RESULT-ARBITRO-ENIF2024-D9-FORMALIDAD-{SIN,CON}-SEGURIDAD-SOCIAL-*`); los
`…-FORMALIDADX…-C2-*` del lote están en `null` (NO-EMITIBLE). **Ningún marginal
de sexo, edad, escolaridad, localidad, cuenta_formal ni nacional dentro de T
existe sellado** → el `[SUPUESTO]` del encargo se sostiene: este CALC los deriva;
los dos de formalidad se **citan** (E.5) y re-derivarlos es el oro (§6).

## 1 · El universo T, por texto

FD 2024, hoja `TMODULO`, fila 138: «3.13 Por parte de su trabajo, ¿usted tiene
derecho a los servicios médicos...» (`P3_13`, alfanumérico, 1): `1` del Seguro
Social (IMSS) · `2` del ISSSTE · `3` del ISSSTE estatal · `4` de PEMEX, Defensa o
Marina · `5` de un seguro privado de gastos médicos · `6` de otra institución ·
`7` Entonces, ¿carece de derecho a servicios médicos por parte de su trabajo…? ·
`9` No sabe · `b` Blanco por secuencia.

**T := `P3_13 ∈ {1,…,7}`.** `9` y blanco quedan fuera de T. Es exactamente el
conjunto de filas que el eje `formalidad` del árbitro declara dentro
(`tools/medidor_ahorro_enif24.py`, `EJES_P2`, `formalidad`: `{1..6} → con
seguridad social`, `7 → sin seguridad social`, lo demás `(fuera)`), y el que el
árbitro GEN2 cuenta en `G-EJE-FORMALIDAD-FUERA` (blanco + no sabe). **Cobertura
declarada**: la del árbitro, leída del contrato sellado del lote
(`parametros.ejes.formalidad.cobertura_arbitro`), no tecleada; la cobertura
medida (filas y masa ponderada) se emite aparte.

Todo lo demás del universo es el del árbitro, sin un filtro más: `carga()` de
`tools/medidor_ahorro_enif24.py` (todas las filas de `TMODULO`; PARA si `EDAD_V`
no numérica o < 18, si `FAC_PER` no es numérico positivo o si alguien tiene las
15 variables de la sección 5 en blanco). Guardias propias que PARAN: `EST_DIS` o
`UPM_DIS` vacíos; columnas de eje ausentes; T vacío.

## 2 · Desenlace, ejes, pares y categorías — leídos, no tecleados

* **Desenlace único: `ahorra_solo_informal` (D9)** — el primario y único del lote
  (`DIN-lote-enif2024-spec-v1_0.md` §1): alguna `P5_1_1..6 == "1"` y ninguna
  `P5_6_1..9 == "1"`; `desenlaces()` del árbitro, importado. `informal_cualquiera`
  **no** se deriva: el lote no lo consume (se declara en NO-CORRIDO).
* **Ejes**: `Eje.deriva` del árbitro (`EJES_P2` + `EJE_CUENTA_PRINCIPAL`),
  importado — sexo, edad (18-29 / 30-44 / 45-59 / 60+ = 60..96), escolaridad
  (`ESC_ENIF[NIV]`), localidad (`TLOC` {1,2} / {3,4}), formalidad, cuenta_formal.
* **Pares, orden `(a, b)` y categorías**: del contrato sellado del lote
  (`CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/spec.yaml`, `parametros.pares` y
  `parametros.ejes.<eje>.orden`) — los pares cuyo `c2` empieza por `NO-EMITIBLE`
  y que contienen `formalidad`. **Guardias que PARAN**: que no sean exactamente 5;
  que no coincidan con las filas del dictamen con `ola = ENIF 2024`,
  `desenlace_id = ahorra_solo_informal`, `veredicto = NO-EMITIBLE`; que el
  `n_celdas` del dictamen ≠ producto de categorías del contrato; que el orden de
  categorías del contrato ≠ el `orden` del eje del árbitro.
  Resultado esperado de esas lecturas (se re-deriva en la corrida y se emite):
  `formalidadxsexo` (4) · `edadxformalidad` (8) · `escolaridadxformalidad` (8) ·
  `formalidadxlocalidad` (4) · `cuenta_formalxformalidad` (4) = **28 celdas**.

## 3 · La ola T y la guardia de una variable

La ola se construye **una vez** desde el DataFrame de `carga()` y lleva, por
eje, una columna derivada por el árbitro **y restringida a T**: en cada fila
fuera de T, la columna del eje vale `(fuera)`. La restricción es la del
universo, idéntica para todos los ejes, y se aplica en la construcción de la
ola (un solo lugar). La columna `nacional` vale `T` en T y `(fuera)` fuera. La
columna `formalidad` ya es `(fuera)` fuera de T por construcción del árbitro.
**Ninguna fila se quita**: el marco de diseño entero (todas las UPM de la ola)
es el que se remuestrea (§4), porque recortar antes cambia la secuencia de
sorteos.

`marginal_t(ola, grupo, *, desenlace, replicas)`: `grupo` es **un** `str`
posicional de `EJES_T = (sexo, edad, escolaridad, localidad, cuenta_formal,
formalidad, nacional)`; dos posicionales o una lista → `TypeError`; otro nombre
→ `ValueError`; la ola se re-huella (sha256 de `EST_DIS`, `UPM_DIS`, `_w`, las
siete columnas y el desenlace, en orden de archivo) y una ola filtrada,
reordenada o alterada → `ReservaRota`; réplicas de otra ola → `ReservaRota`. **No
existe `cruce()`.** Lo que `marginal_t` estima es `p(D9 │ eje = k, T)`: un eje
por llamada, dentro de T. La celda `formalidad = f` es `p(D9 │ f)` (f ⊂ T).

**Prohibición explícita (PARO a del encargo):** ningún código de este acto
deriva, ve o imprime una proporción de dos ejes de ENIF 2024 — en particular,
ninguna celda `formalidad × eje`. La auditoría del AST (§7) lo vigila.

## 4 · Marginales: punto, réplicas e IC — la receta del árbitro GEN2

Por celda `k` del eje: `n` = filas con `eje == k` (dentro de T), `numerador` =
filas con D9 = 1, `DEN-W` = Σ`FAC_PER`, `p = Σ(w·y) / Σw`.

**Plan de réplicas = el del piso que el árbitro GEN2 importó**
(`data/corrida0/CALC-PISOS-ENIF2021-EJES-0003/medidor.py::_estimate`, líneas
57-95, sha256 `d069f38b…`): llaves `f"{EST_DIS}\t{UPM_DIS}"` de todas las filas de
la ola, **ordenadas lexicográficamente**; estratos en orden lexicográfico; UN
generador `numpy.random.Generator(PCG64(seed))`; las réplicas se generan en
bloques de `replicas_bloque` (50) y, dentro de cada bloque, estrato por estrato,
`rng.integers(0, n_h, size=(bloque, n_h))` sobre las posiciones de sus UPM; la
multiplicidad de cada UPM en la réplica es el conteo de sus sorteos.
`p_k = (mult_k · Y) / (mult_k · W)` con `W`, `Y` totales ponderados por UPM de la
celda; `NaN` si el denominador es 0. **IC95 del marginal** =
`numpy.percentile(·, [2.5, 97.5])` sobre las réplicas finitas; `B-VALIDAS` = su
número; `P`/IC `null` si el punto no es finito o no hay réplica finita. Es la
receta con la que se sellaron los R del árbitro GEN2; por eso §6 puede exigir
reproducción a `1e-12`.

## 5 · C2 restringido por celda, réplicas degeneradas, IC

Para el par `(a, b)` y la celda `(i, j)`:

```
C2R(i, j) = expit( logit p_T(a = i) + logit p_T(b = j) − logit p_T )
```

con `p_T(eje = k) = p(D9 │ eje = k, T)`, `p_T = p(D9 │ T)` (la celda `nacional`)
y, para `formalidad`, `p_T(formalidad = f) = p(D9 │ f)`. La forma es
`piso_log_aditivo` de `tests/test_celda_d_c2.py`, **importada**. Rótulo del
supuesto: `ausencia de interaccion en escala logit`; rótulo prohibido:
`independencia`.

* **Punto**: `piso_log_aditivo(p_a, p_b, p_T)` con el marginal de `formalidad`
  **citado** del R sellado del árbitro GEN2 (`…-FORMALIDAD-<f>-P`, a precisión
  completa) y los demás **derivados en esta corrida** (los sella este CALC).
  `MarginalDegenerado` (algún marginal en {0,1}) o marginal `null` → punto `null`
  → `IC-NO-CONSTRUIBLE:PUNTO-SIN-DEFINIR`.
* **Réplica válida**: los tres marginales de la réplica en `(0,1)` y definidos,
  operado como `|p − 0.5| < 0.5` por marginal y las tres validaciones
  **multiplicadas**. Las inválidas se excluyen y se cuentan; nunca se recortan ni
  se sustituyen.
* `C2R_k = expit(logit p_k(a) + logit p_k(b) − logit p_k)` vectorizado sobre las
  réplicas válidas (réplica k con réplica k, un solo plan); su coincidencia con
  `piso_log_aditivo` se mide en la primera réplica válida de cada celda.
* **IC95** = percentiles 2.5 / 97.5 de `C2R_k` válidas **si son ≥
  `umbral_replicas_validas` (9 900 de 10 000)**; si no,
  `IC-NO-CONSTRUIBLE:REPLICAS-VALIDAS-<n><9900`. Rótulo:
  `IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS-UNIVERSO-T`.
* **Cada RESULT de celda lleva su universo**: la `unidad` declarada en
  `spec.yaml` lo escribe, y la celda emite además `…-UNIVERSO` (texto) con T, la
  cobertura declarada y la medida.

## 6 · El oro — los dos marginales de formalidad y el tamaño de T

Sobre la ola T, `marginal_t(ola, "formalidad")` debe reproducir los R sellados de
`CALC-ARBITRO-MARGINALES-ENIF2024-0001` para D9, en las dos celdas: `P`, `IC-LO`,
`IC-HI` a **`1e-12`** (misma receta, mismo plan, mismas filas: sólo cambia el orden
de suma), `N` y `B-VALIDAS` **exactos**, `DEN-W` a `1e-6` absoluto; y además
`G-FILAS-UNIVERSO` = `G-FILAS-PERSONAS` sellado y `G-FUERA-T` =
`G-EJE-FORMALIDAD-FUERA` sellado, **exactos**. Veredicto
`G-CONTROL-ARBITRO-VEREDICTO ∈ {REPRODUCE, NO-REPRODUCE}`, con cada delta con
signo.

**Si es NO-REPRODUCE**: todos los IC (de marginales y de C2R) salen `null`, cada
celda `IC-ESTADO = IC-NO-PUBLICADO:CONTROL-ARBITRO-NO-REPRODUCE`,
`G-IC-PUBLICADO = NO`; los puntos se emiten; la corrida se sella con ese hallazgo
y no se ajusta nada.

## 7 · Guardia E.6 en el AST

`auditoria_ast()` vive en el medidor; `medir()` la corre sobre su propio archivo
**antes** de abrir el zip y PARA (0 filas leídas) si hay una sola violación. Las
reglas son las de `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (spec §7), con los
nombres de este medidor: R1 imports en lista blanca · R2 `groupby`, `crosstab`,
`pivot*`, `merge`, `concat`, `read_*`, `ZipFile`, `open`, `getattr`, `eval`,
`apply`, `agg`, `query`, `cruce`… prohibidos · R3 `.df` sólo en el núcleo
(`_huella`, `_ola_desde_df`, `_carga_ola_enif`, `_verifica`, `replicas_t`,
`_reps_de_mascara`, `marginal_t`) · R4 ningún nodo combina dos comparaciones en
todo el archivo · R5 `OlaT(`, `carga()`, `desenlaces()`, `deriva()` y
`_importa` sólo donde van · R6 `marginal_t` con exactamente 2 posicionales,
grupo atómico, keywords en {`desenlace`, `replicas`} · R7 ninguna función con
`cruce` en el nombre · R8 ninguna constante de archivo fuera de
`enif_2024_bd_csv.zip`, `TMODULO.csv` y los cuatro módulos importados, ninguna
de otro instrumento u otra ola, ningún `inputs["…"]` no declarado.
`tests/test_c2_restringido_enif2024_guardia.py` le da **una mutación por regla**
(control positivo) y además: (a) prueba que el plan de réplicas de este medidor
es el de `_estimate` del piso — importado **en el test**, no en el medidor —
sobre datos fabricados, a `1e-12`; (b) corre el procedimiento entero sobre una
ola fabricada y pasa su salida por `corrida0._valida_outputs` en cada rama
terminal (§8).

## 8 · Ramas terminales y nulos (D-22)

Pasan por el conducto sobre sintético, antes del COMMIT-1: (i) oro REPRODUCE con
IC publicados; (ii) oro NO-REPRODUCE → IC `null`; (iii) una categoría sin filas
en T (`n = 0`, `P` `null`, sus celdas C2R `PUNTO-SIN-DEFINIR`); (iv) un marginal
degenerado (`p ∈ {0,1}`); (v) réplicas válidas bajo el umbral. Todo id que el
código pueda dejar `null` lleva `permite_no_estimable: true`; ninguno emite `NaN`.

**`cuenta_formal × formalidad` — la pregunta del encargo, contestada por texto
y por regla antes del dato.** No son colineales por definición: `P3_13` pregunta
por el derecho a servicios médicos por el trabajo; `P5_4_1..9`, por la tenencia
de una cuenta o producto formal. Si en el dato el par resulta degenerado —algún
marginal en {0,1}, o una categoría de `cuenta_formal` sin filas dentro de T— sus
celdas salen `NO-CONSTRUIBLE` con causa (opción recomendada por dirección) y se
lleva a mesa como pregunta; no se emite nada forzado. Sigue vigente la nota del
dictamen: en `sin cuenta`, D9 se reduce a `informal_cualquiera` por construcción
del cuestionario (P5_4 gatea a P5_6); la composición se emite, rotulada.

## 9 · Ejecución, registro y lo que no se hace

* Sin ejecución diagnóstica: el medidor se congela probado **sólo** contra datos
  fabricados (cero microdato; E.5) y corre una vez por `corrida0 preflight → run
  → verify`. `medidor_ejecutado_al_congelar: NO`.
* Registro en la vista y asiento de replay en el mismo acto (E.7).
* No adopta · no evalúa los pares (eso es el lote) · no compara nada contra el
  marginal ni el C2 poblacional · no toca `CALC-C2-COMPUESTO-IC-ENIF2024-0001`
  ni los CALC del lote · no deriva ningún cruce.
* `cuenta_gen2: SI`; no adopta; `celdas_validadas` no se mueve aquí.

## 10 · Módulo de auditoría (afirma sobre México)

¿Cuántos contadores mueve? Uno: +1 corrida sellada GEN2; ninguna adopción. T es
la población ocupada que llega a 3.13 (~69 % de las filas del árbitro): excluye a
quien no trabaja —desproporcionadamente mujeres dedicadas al hogar, personas
mayores y estudiantes—, así que `p(D9 │ mujer, T)` **no** es «las mujeres»: es
«las mujeres que trabajan», y leerlo como lo primero es el error peligroso. La
informalidad laboral (sin seguridad social) es estructura del mercado de trabajo
y de la oferta de servicios financieros, no rasgo cultural; el ahorro informal
es primero oferta bancaria y choque de ingreso, después conducta. El piso supone
ausencia de interacción en logit; su IC mide ruido muestral, no el error de ese
supuesto, que es mayor justo donde los ejes se refuerzan (informalidad con baja
escolaridad o localidad chica). La rejilla no ve región ni condición indígena.
Escala: proporción de personas de T; no se promedia con cifras de hogar, trámite
ni población total. Toda cifra aquí es PROSPECTIVA respecto de la R restringida
de cruce que el lote derive después.

**El primer resultado que produzca este procedimiento es el que se reporta.**

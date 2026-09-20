# IC RÉPLICA POR RÉPLICA DE LAS EMISIONES C2 COMPUESTAS DE ENIF 2024 — spec v1.0

**ACTO GEN2-C2-COMPUESTO-IC-ENIF2024-1** · 19/sep/2026 · base `a92126f0` · CAJA
Encargo archivado (A.3): `forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-IC-ENIF2024-1.md`
CALC reservado: `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (0 apariciones del id en
6/6 ramas remotas al abrir; control positivo `CALC-C2-COMPUESTO-RESERVADAS-0001`
→ 3 archivos en `origin/main`).

Esta spec congela el procedimiento **antes de abrir una sola respuesta de ENIF
2024**. Se escribió contra el dictamen de emisibilidad sellado, el yaml del
árbitro y los puntos sellados por `CALC-C2-COMPUESTO-RESERVADAS-0001`; el
COMMIT-1 la sella junto con el medidor y el test de guardia; los IC llegan en
el COMMIT-2.

> **El primer resultado que produzca este procedimiento es el que se
> reporta.** No hay segunda corrida elegible, no hay recorte de réplicas, no
> hay sustitución de marginales y no hay ajuste post-hoc de la forma ni de
> los umbrales.

---

## 0 · Hallazgo P0 y desviación autorizada (verbatim de la pregunta y la respuesta)

El encargo, P0: «¿El módulo guardado cubre esta ola y estos ejes? Léelo. Si
`marginal()` no admite alguno de los ejes del dictamen para ENIF 2024, no lo
parches: esa celda sale IC-NO-CONSTRUIBLE con causa, y el hueco es entregable.»

Leído contra `a92126f0`: `tools/celda_d/marginales_reproduccion.py` es
**ENVIPE-only por construcción**. `carga_ola()` (líneas 172-231) lee
`conjunto_de_datos_tmod_vic_envipe<anio>.csv` y `tsdem`, aplica el universo
`BP1_20 ∈ {1,2}` y pondera por `FAC_DEL`; `EJES = ("escolaridad_proxy",
"dominio_urbano_rural", "nacional")` (línea 99). Los cinco ejes de los pares
`EMITIBLE` de ENIF 2024 en el dictamen — `cuenta_formal`, `edad`,
`escolaridad`, `localidad`, `sexo` — reciben `ValueError` en `marginal()`:
**0 de 5 admitidos**, y no existe lector de TMODULO. Bajo la regla literal,
las 136 celdas saldrían `IC-NO-CONSTRUIBLE` y el acto no mediría nada.

Pregunta a mesa (19/sep/2026), con tres opciones y recomendación; respuesta
de mesa, verbatim de la opción elegida: **«Desviación escrita: medidor con
guardia propia (Recomendado) — El medidor, dentro del CALC, importa
medidor_ahorro_enif24 (universo/desenlaces/ejes del árbitro) y re-implementa
marginal() para ENIF con la MISMA guardia (str posicional, whitelist de 5
ejes, huella de la ola) + replicas_compartidas; el test AST del encargo lo
vigila. No toca marginales_reproduccion.py. Entrega las 136 con IC; la
desviación queda declarada en spec, nota y NO-CORRIDO.»**

Consecuencias, campo por campo:

* `marginales_reproduccion.py` **no se modifica**. Se importa: `cotejo()`
  (control 2) y `marginal()` como **sonda mecánica** del hallazgo —
  `RESULT-C2IC-ENIF2024-G-P0-MODULO-GUARDADO-<eje>` registra qué lanza con
  cada eje; `G-P0-MODULO-GUARDADO-EJES-ADMITIDOS` cuenta cuántos admite por
  nombre (se espera 1: `nacional`, y aun ese no admite la ola).
* La guardia de una variable vive en el medidor, **con la misma semántica**
  (§4) y **probada por mutación** (§6).
* Universo, desenlaces y ejes se **importan del árbitro**
  (`tools/medidor_ahorro_enif24.py`), el mismo objeto de código que selló los
  R marginales del yaml: no se copian.

## 1 · Qué gobierna, y qué no se toca

Gobiernan: el dictamen `data/corrida0/c2-compuesto-dictamen-v1_0.tsv` (filas
`ola = ENIF 2024`, regla `dinero.ahorro.via_informal_ejes_enif2024`);
`milpa/tramite-ola5-propuesta-v0.yaml` (marginales R sellados, con `ic95` y
`n`, líneas 1415-1599); `tools/c2_compuesto.py::NACIONALES` (los dos
nacionales de ENIF citados, no recalculados: `ahorra_solo_informal` 0.357153
sin IC propio, DERIVADO; `informal_cualquiera` 0.561920 IC [0.549922,
0.573502], MEDIDO); `CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json` (los
puntos sellados, control 1); las specs de los pilotos 1 y 2 como precedente
del método (`forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_2.md`,
`forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md`).

No se toca: `tools/celda_d/marginales_reproduccion.py` ·
`tools/marcador_segmento.py` · `estimadores-por-segmento.yaml` ·
`CALC-C2-COMPUESTO-RESERVADAS-0001/` · `tools/corrida0.py` · ningún payload
que no sea `enif_2024_bd_csv.zip` :: `TMODULO.csv`.

## 2 · Universo, unidad, ola, ponderador, desenlaces, ejes — del árbitro

* **Payload**: `enif_2024_bd_csv.zip` (manifiesto `enif_2024_enif_2024_bd_csv`,
  sha256 `00e4b0b4…f039`, 3 131 148 B), miembro `TMODULO.csv`, latin-1 — el
  que `tools/medidor_ahorro_enif24.py:30-31` lee. **Guardia**: el medidor
  compara el sha256 del zip que el árbitro abre con el del input resuelto por
  el manifiesto y PARA si difieren; identidad por hash, no por nombre.
* **Unidad**: PERSONA elegida 18+. **Ponderador** `FAC_PER`; estrato `EST_DIS`;
  UPM `UPM_DIS`.
* **Universo**: el de `carga()` del árbitro, sin un filtro más: todas las filas
  de TMODULO; PARA si `EDAD_V` no numérica o < 18, si `FAC_PER` no numérico
  positivo, si alguna persona tiene las 15 variables de la sección 5 en
  blanco. Guardias propias que PARAN: `EST_DIS` o `UPM_DIS` vacíos; columnas
  de eje ausentes (`SEXO`, `NIV`, `TLOC`, `P3_13`, `P5_4_1..9`).
* **Desenlaces** (`desenlaces()` del árbitro): `ahorra_solo_informal` = alguna
  `P5_1_1..6 == "1"` y ninguna `P5_6_1..9 == "1"`; `informal_cualquiera` =
  alguna `P5_1_1..6 == "1"`. El blanco por secuencia en `P5_6_*` cuenta como
  no haber ahorrado por esa vía (lectura de MAESTRA34-L5 P4 §1.3).
* **Ejes** (`Eje.deriva` del árbitro, `tools/medidor_ahorro_enif24.py:124-181` (`EJES_P2` en 130, `EJE_CUENTA_*` en 152-164, `_celda_cuenta` en 166, `desenlaces` en 173)):
  `sexo` {1 Hombre, 2 Mujer}; `edad` {18-29, 30-44, 45-59, 60+} (60..96;
  97+ → fuera); `escolaridad` `ESC_ENIF[NIV]` {hasta primaria, secundaria,
  media superior, superior} (99 → fuera); `localidad` `TLOC` {1,2 → 15 000 y
  mas; 3,4 → menor de 15 000}; `cuenta_formal` {sin cuenta, con cuenta} (nunca
  respondió → fuera) — misma `deriva` para los dos desenlaces. `formalidad`
  **no se admite** (NO-EMITIBLE, A-bis 4).
* **Categorías y lista de pares**: leídas del dictamen (`par`, `n_celdas`,
  `bloque_desenlace`, `desenlace_id`) y del yaml (`desenlaces.<bloque>.ejes[].
  celdas[].celda`), partiendo el par con `tools/c2_compuesto.py::_parte_el_par`
  — nada tecleado. **Guardias que PARAN**: `n_celdas` del dictamen ≠ producto
  de categorías del yaml; eje del par fuera de la whitelist; eje con
  `universo_restringido: true`; nombre del bloque ≠ `desenlace_id`.

## 3 · Réplicas compartidas: precedente, archivo y línea

`n_h` UPM con reemplazo dentro de cada estrato, **un** generador
`numpy.random.PCG64(42)`, estratos en orden lexicográfico de `EST_DIS` y UPM
en orden lexicográfico de `UPM_DIS`, **10 000** réplicas, `counts (n_rep ×
n_upm)`. Precedente: `tools/celda_d/marginales_reproduccion.py::
replicas_compartidas` (líneas 256-286);
`forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md:166` (réplicas
compartidas por ola, PCG64(42), 10 000);
`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/spec.yaml:171`
(`bootstrap_replicas: 10000`) y `:133-142` (seed 42, PCG64, orden de consumo
fijado). Se re-escribe en el medidor (`replicas_enif`) con esa receta porque
la firma del módulo exige una `Ola` de ENVIPE (huella por `ID_DEL`).

En cada réplica k y para cada (desenlace, eje, celda): `p_k = (counts_k @ Y) /
(counts_k @ W)` con `W`, `Y` totales ponderados por UPM del grupo; `NaN` si el
denominador es 0. Todos los grupos y celdas de la ola comparten `counts`.

## 4 · Guardia de una variable — semántica idéntica a la del módulo guardado

`marginal_enif(ola, grupo: str, *, desenlace: str, replicas=None)`:

* `grupo` es **un** `str` posicional; no hay `*grupos`; dos posicionales o una
  lista → `TypeError`.
* `grupo ∈ EJES_ENIF = (sexo, edad, escolaridad, localidad, cuenta_formal,
  nacional)`; cualquier otro → `ValueError`. La celda está **pre-derivada por
  el árbitro en su propia columna** al construir la ola; la función sólo
  compara esa columna con cada categoría.
* La ola se **re-huella** (sha256 de `EST_DIS`, `UPM_DIS`, `_w`, las cinco
  columnas de eje y las dos de desenlace, en orden de archivo) antes de contar;
  una ola filtrada, reordenada o alterada → `ReservaRota`. Réplicas de otra ola
  → `ReservaRota`.
* `desenlace` selecciona la variable `_y_<desenlace>`; no agrupa.
* No existe `cruce()`.

Por celda devuelve `n`, `numerador`, `poblacion`, `p` e `IC95` por
`wprop_ic_conglomerado` (la receta del árbitro, importada: seed 42, 10 000,
`default_rng`), `estratos`, `upm` y el vector `replicas`.

## 5 · C2 por réplica, tratamiento de réplicas degeneradas, IC

* **Punto**: `piso_log_aditivo(p_a_sellado, p_b_sellado, p_nac_citado)`
  (`tests/test_celda_d_c2.py`, importada) — el mismo número que el CALC de
  emisiones. `MarginalDegenerado` → punto `null` → `IC-NO-CONSTRUIBLE:
  PUNTO-SIN-DEFINIR`.
* **Réplica válida**: los tres marginales de la réplica están en el abierto
  (0, 1) y no son `NaN` — operado como `|p − 0.5| < 0.5` por marginal, y las
  tres validaciones **multiplicadas** (no combinadas por comparaciones: R4).
  Las inválidas se **excluyen** y se cuentan; no se recortan ni se sustituyen.
* **C2_k** = `expit(logit p_k(a) + logit p_k(b) − logit p_k)` vectorizado en
  numpy sobre las réplicas válidas (como el piloto 2,
  `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/medidor.py:304-307`); la
  coincidencia con `piso_log_aditivo` se mide en la primera réplica válida de
  cada celda (`G-C2-VECTORIZADO-VS-REFERENCIA-DELTA-MAX`).
* **IC95** = `numpy.percentile` 2.5 / 97.5 de C2_k sobre las válidas, **si las
  válidas son ≥ 9 900 de 10 000**; si no, `IC-NO-CONSTRUIBLE:REPLICAS-VALIDAS-
  <n><9900` con IC `null`. Umbral fijado aquí, antes del dato.
* Rótulo: `IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS`.
  Supuesto: `ausencia de interaccion en escala logit`. Rótulo prohibido:
  `independencia`.

## 6 · Dos controles de coherencia — los dos, o no se publica IC

1. **Control 1 · punto**: `…-P` = `RESULT-C2COMP-<desenlace>-<par>-<a>-X-<b>`
   del `resultados.json` sellado, a **1e-12**, en todas las celdas. Misma
   función, mismos sellados (6 decimales del yaml), mismo nacional: la
   tolerancia de redondeo es cero en la práctica. `G-CONTROL-1-PUNTO-VEREDICTO`
   ∈ {REPRODUCE, NO-REPRODUCE}; `G-CONTROL-1-DELTA-MAX-ABS`; un `…-CONTROL-1-
   DELTA` por celda; una celda sin punto o sin sellado → NO-REPRODUCE.
2. **Control 2 · árbitro**: la réplica base de cada marginal (la ola entera)
   reproduce el R sellado en `p` a **1e-6**, `IC95` a **1e-4** y `n` **exacto**
   — para **todas** las celdas de los ejes usados, por desenlace, y el nacional
   citado (`NACIONALES`: IC sólo para `informal_cualquiera`). Cotejo con
   `marginales_reproduccion.py::cotejo` (importado); el `n` exacto es guardia
   propia (cotejo emite `delta_n` pero no lo adjudica). Tolerancias, las del
   piloto 2 (`TRA-evade-norma-sxd12-spec-v1_0.md:102`): el yaml trae 6
   decimales, y `p`/IC salen de la **misma función** que el árbitro usó.
   `G-CONTROL-2-ARBITRO-VEREDICTO`; deltas con signo por celda; un `NO-
   ESTIMABLE` (celda sellada que aquí sale vacía) → NO-REPRODUCE.

**Si cualquiera de los dos es NO-REPRODUCE**: todos los IC salen `null`, cada
celda `IC-ESTADO = IC-NO-PUBLICADO:<causa>`, `G-IC-PUBLICADO = NO`,
`G-TIPO-INCERTIDUMBRE = NO-PUBLICADA`; la corrida se sella con ese hallazgo y
no se ajusta nada. Un NO-REPRODUCE no invalida las emisiones: invalida la
afirmación de que este medidor ejecuta la receta sellada.

## 7 · Guardia E.6 en el AST (NC-0328)

`auditoria_ast()` vive en el medidor; `medir()` la corre sobre su propio
archivo **antes** de abrir el zip y PARA (`SystemExit`, 0 filas leídas) si hay
una sola violación. `tests/test_c2_ic_enif2024_guardia.py` la corre igual y le
da a comer **una mutación por regla** (control positivo):

| regla | qué prohíbe |
|---|---|
| R1 | `import` fuera de la lista blanca (stdlib mínima + numpy/pandas/yaml) |
| R2 | `groupby`, `crosstab`, `pivot`, `pivot_table`, `unstack`, `stack`, `merge`, `concat`, `read_csv`, `read_excel`, `ZipFile`, `open`, `getattr`, `setattr`, `vars`, `globals`, `locals`, `eval`, `exec`, `__dict__`, `asdict`, `query`, `apply`, `applymap`, `transform`, `agg`, `iterrows`, `itertuples`, `MultiIndex`, `cruce`, `compile`, `__import__` |
| R3 | cualquier acceso a `.df` (el microdato) fuera del núcleo guardado (`_huella`, `_ola_desde_df`, `_carga_ola_enif`, `_verifica`, `replicas_enif`, `_reps_de_mascara`, `marginal_enif`) |
| R4 | cualquier nodo que combine **dos comparaciones** (`&`, `\|`, `^`, `*`, `and`, `or`) — una agrupación por dos variables es `mask_a & mask_b` — en **todo** el archivo |
| R5 | `OlaEnif(` fuera de `_ola_desde_df`; `carga()` del árbitro fuera de `_carga_ola_enif`; `desenlaces()`/`deriva()` fuera de `_ola_desde_df`; `_importa` de un módulo fuera de los cuatro autorizados |
| R6 | `marginal_enif` con ≠ 2 posicionales, con grupo no atómico (lista, tupla, expresión) o con keyword fuera de {`desenlace`, `replicas`} |
| R7 | cualquier función cuyo nombre contenga `cruce` |
| R8 | cualquier constante de archivo (`.zip`, `.csv`, …) fuera de {`enif_2024_bd_csv.zip`, `TMODULO.csv`, los cuatro módulos importados}; cualquier constante con token de otro instrumento u otra ola de ENIF; cualquier `inputs["…"]` no declarado |

Límite declarado: R4 es sintáctico — no distingue vectores por fila de vectores
por réplica; por eso R3 confina el microdato al núcleo y R4 se aplica también
dentro del núcleo. Lo que el AST no puede ver (p. ej. un cruce construido
fuera de este archivo) lo cubren R1/R2/R5 (nada entra que no esté en la lista)
y la revisión de mesa.

## 8 · Ejecución, registro y lo que no se hace

* Sin ejecución diagnóstica: el medidor se congela probado **sólo** contra el
  fixture fabricado del test (cero microdato; E.5) y corre una vez por
  `corrida0 preflight → run → verify`. `medidor_ejecutado_al_congelar: NO`.
* Registro en la vista y asiento de replay en el mismo acto (E.7): `registro
  --escribe --lote CALC-C2-COMPUESTO-IC-ENIF2024-0001` y fila propia en
  `forense/replay-evidencia.tsv` con el `verify` aislado.
* No adopta · no evalúa C2 contra ningún R de cruce · no actualiza el marcador
  (sucesor de nube, una línea) · no toca ENCIG 2025 ni ENVIPE 2025 · no deriva,
  no ve, no imprime ningún cruce; los pares siguen `RESERVADA`.
* `cuenta_gen2: SI` propuesto; nace `PENDIENTE-DE-MESA` salvo firma;
  `adoptados_activos` no se mueve.

## 9 · Módulo de auditoría (afirma sobre México; verbatim del encargo)

El IC que sale de aquí mide ruido muestral de un estimador que supone
no-interacción; no mide el error de ese supuesto, que es el que importa en las
celdas donde los ejes se refuerzan (mayor edad con baja escolaridad, localidad
chica sin cuenta formal). Un IC estrecho no es una celda bien estimada. En
ENIF, formalidad quedó NO-EMITIBLE por vivir en el universo de quien trabaja:
no se intenta rescatar. El ahorro informal es primero oferta bancaria y choque
de ingreso, después conducta. Los ejes son marcadores de estructura, no rasgos
culturales; la rejilla no ve región ni condición indígena. Ninguna cifra
esperada en este encargo. Peligroso leído simplista: «ya tiene intervalo» como
«ya está validado».

**El primer resultado que produzca este procedimiento es el que se reporta.**

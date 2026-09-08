# `ACTO GEN2-E5 · CALC-0001..0003` — las tres corridas, lo que sellaron y lo que no

**Acto:** `ACTO GEN2-E5 · CALC-0001..0003 — correr, sellar, verificar`, 8/sep/2026.
**Entorno:** UBUNTU (caja, corpus montado). **NO** se lanzó en nube.
**Base:** worktree nuevo desde `origin/main = fbce146d` (merge de `PR #629`,
`ACTO GEN2-E5-0`). **Encargo archivado (A.3):**
`forense/encargos/2026-09-08-GEN2-E5-CALC-0001-0003.md`.

Los números de abajo aparecen **por primera vez**. Todos salen de un `RESULT`
sellado de este acto, con su tipo y su unidad declarados en el `spec.yaml`
congelado por `GEN2-E5-0`, y con `etiquetas.generacion = GEN2`. **Ningún otro
número de esta nota es una cifra del modelo.**

---

## 0 · Entorno y compuerta (A.2 · A.13)

```
ENTORNO · commit=fbce146d113f · git_status=LIMPIO(0) · python=3.14.4
· numpy=2.3.5 pandas=2.3.3 scipy=1.16.3 yaml=6.0.3 pyreadstat=1.3.6
· CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=no-ejecutada
· raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=398)
```

La red **no** se sondeó: este acto no descarga nada. El corpus sí — `398`
archivos examinados por `tools/entorno.py`, que es lo que sostiene el positivo.

**Compuerta vigente, re-derivada contra `origin/main = fbce146d`** (no heredada
del mensaje de mesa, que verificó antes):

| cláusula | comando | salida |
|---|---|---|
| `E5-0` fusionado | `git ls-tree -r --name-only origin/main data/corrida0/CALC-000{1,2,3}/` | 9 blobs: `spec.yaml` + `spec.md` + `medidor.py` en los tres |
| `GEN2-E7` cerrado | `git show origin/main:forense/notas/2026-09-08-GEN2-E7-readiness-marcador.md \| grep -c GO-MARCADOR` | `2` (≥1 exigido) |
| tests de E3.1 en verde | `python3 tests/test_corrida0.py` | `59 casos · 59 ok · 0 FALLOS` |
| `preflight` en los tres | `python3 tools/corrida0.py preflight CALC-000{1,2,3}` | `VERDE` los tres |
| `cmd_status` en `main` (E6) | `tools/corrida0.py:3135` · `corrida0 status` | corre y emite los 14 contadores |
| suite | `python3 tests/check.py --baseline` | `LÍNEA BASE: VERDE` |
| caja limpia | `python3 tools/limpia_arbol.py --reporta` | **NO vacío** — ver §6 |

**`FP-352` reproducida, y era ella.** Dentro del sandbox de Bash de esta caja,
`preflight` devolvió `BLOQUEADO · input_manifiesto_AUSENTE` para los **seis**
payloads de `CALC-0001`/`CALC-0002` — todos con raíz lógica `descargas_mx`. No
era ausencia: `/mnt/c` es invisible ahí. Fuera del sandbox, los seis existen y
su `sha256` **COINCIDE** con el declarado por el manifiesto. Control de la
distinción, sobre el mismo archivo y en la misma sesión:

```
dentro : test -e ".../cide_cses2015_nacional_poselectoral.sav"  -> exit 1
fuera  : EXISTE  1864581  .../cide_cses2015_nacional_poselectoral.sav
```

Todo `run`/`verify` de este acto corrió **fuera** del sandbox. Los tres
`PRE-FLIGHT: VERDE` de la tabla son los de fuera.

---

## 1 · `CALC-0001` — `prereg-caja-S12` (CIDE-CSES 2015) · **SELLADA**

`corrida_id = CALC-0001--174c269a07b6` · 54 `RESULT` · sello
`aa48aac50e75b5cad3170649f1e46dcda0c18aeab5f8e3005b2e46abe221fbcf`.

**El contraste que S12 §4 pre-registra NO ES ESTIMABLE, y la corrida lo dice con
su propio número.** Los cuatro brazos (POSEL/PREEL × OFERTA/AMENAZA) salen
`VEREDICTO = NO-ESTIMABLE`:

| brazo | `N-T1` | `N-T0` | `N-NSNC` | `P-T1` (proporción ponderada) | `P-T0` |
|---|---|---|---|---|---|
| POSEL · OFERTA  | 42 | **0** | 12   | 0.37922545290553505 | — |
| POSEL · AMENAZA | 14 | **0** | 11   | 0.438740191776023   | — |
| PREEL · OFERTA  | 23 | **0** | 1207 | 0.2468700731109074  | — |
| PREEL · AMENAZA | 10 | **0** | 1213 | 0.18369940751162478 | — |

`N-T1`/`N-T0`/`N-NSNC`: **enteros**, unidad = personas. `P-T1`: **proporción**
ponderada por `PONDFIN`, en [0,1]. `DELTA` e `IC-LO`/`IC-HI`: `null` en los
cuatro — `NO-ESTIMABLE`, no cero.

**`N-T0 = 0` no es una n corta ni un filtro mal escrito: es estructural.** El
desenlace `ALINEADO` se construye sobre `pcyc13_1` / `pcyc14_1` («¿qué partido
le ofreció / lo amenazó?»), preguntas que **sólo existen para quien contestó
que sí**. El brazo control no tiene partido con el cual alinearse, así que el
desenlace está **indefinido ahí por construcción**. Control positivo sobre el
dato crudo, para separar esto de un código mal resuelto — el código `2 = No`
existe y es mayoritario:

```
poselectoral   pcyc13: {1: 58, 2: 1130, 9: 12}   NaN=0
               pcyc14: {1: 24, 2: 1165, 9: 11}   NaN=0
preelectoral   pcyc13: {1: 63, 2: 1130, 9: 7}    NaN=1200
               pcyc14: {1: 23, 2: 1164, 9: 13}   NaN=1200
```

Es decir: había 1130 y 1165 personas en el brazo control, y **ninguna podía
tener desenlace**. La spec no se editó (regla del encargo). Va a mesa como
`FP-357`.

**§2-bis (encuadre del secreto del voto).** `RESULT-C2BIS-COBERTURA` =
`pvoto1=0.1325; pvoto2=0.1325; pvoto3=0.1325` — por debajo del
`cobertura_split_min = 0.2` que la spec congeló. `RESULT-C2BIS-DISENO` =
`NO-ESTIMABLE-DISENO-NO-EXPERIMENTAL`: la guardia de diseño disparó y los tres
contrastes `VS-NEUTRAL` salen `null`. Lo que sí quedó medido son las tres
marginales, **proporciones ponderadas** sobre `N = 318` cada una:
`PVOTO1-P = 0.47891497945573047` · `PVOTO2-P = 0.5257479707577368` ·
`PVOTO3-P = 0.5989810241496706`.

---

## 2 · `CALC-0002` — `prereg-caja-S13` (LAPOP 2019/2021/2023) · **SELLADA**

`corrida_id = CALC-0002--f57ad1cd8f96` · 29 `RESULT` · sello
`066c2402b753c9e297c306304a24c711aed67eae673f477b5605ee9beff0b538`.

Mide el **antecedente** de `R10.3` (contexto institucional entre víctimas de
extorsión, `vic1ext = 1`), no la regla: `R10.3` **no se mueve** por este acto.
`veredicto_D2h` sigue `NO-CONSTRUIBLE`, decidido en `E5-0` y **no tocado aquí**.

| ola | `N-UNIVERSO` | `N-INDICADORES` | `P-ALTO` (proporción ponderada) | IC95 | veredicto |
|---|---|---|---|---|---|
| 2019 | 520 | 3 | **0.7862745098039216** | [0.75, 0.8230792682926829] | `MARGINAL-REPORTADO` |
| 2021 | 505 | **2** | `null` | `null` | `NO-ESTIMABLE-INDICE-INCOMPLETO` |
| 2023 | 428 | 3 | **0.7341176470588235** | [0.6843195210395104, 0.782010650766957] | `MARGINAL-REPORTADO` |

`N-UNIVERSO`: **entero**, unidad = víctimas con ponderador válido en la ola.
`P-ALTO`: **proporción** ponderada por `wt`, unidad = proporción de
`INDICE_CONTEXTO` ALTO entre víctimas, en [0,1]. Las olas **nunca** se agrupan.

Marginales por indicador (proporciones ponderadas): 2019 `aoj11 = 0.6595744680851063`,
`b18 = 0.7137330754352031`, `aoj12 = 0.7926356589147286`; 2021 `aoj11 = 0.6616565842663518`,
`b18 = 0.7352944680031022`, `aoj12 = null`; 2023 `aoj11 = 0.6197183098591549`,
`b18 = 0.6448598130841121`, `aoj12 = 0.8126463700234192`.

**Por qué 2021 no entrega índice: `aoj12` NO EXISTE en ese archivo.** El índice
exige los tres indicadores. Control positivo sobre el metadato del `.dta` (262
columnas), para distinguir «ausente» de «presente y vacía»:

```
aoj11 PRESENTE · b18 PRESENTE · vic1ext PRESENTE · wt PRESENTE
· upm PRESENTE · estratopri PRESENTE · aoj12 AUSENTE
```

---

## 3 · `CALC-0003` — `prereg-caja-S6-L16 v1.2` (ENNViH 2002) · **PARÓ, nada se selló**

```
RUN CALC-0003
RUN: FALLO -- nada se sella:
  medidor_fallo:MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```

`preflight` había salido **VERDE** (los dos `.zip` con `sha256` coincidente).
El fallo es del `medidor.py` congelado por `E5-0`, que **nunca se había
ejecutado** — es exactamente el riesgo que `NC-0042` dejó anotado.

**Causa raíz, medida.** `ehh02dta_bc/c_portad.dta` trae **8 441 filas, de las
cuales 3 están completamente vacías** (`folio`, `ls` y `estrato` todos `NaN` en
el archivo crudo, antes de cualquier conversión). `_llave()` las convierte a
`<NA>`; `duplicated(subset=["folio","ls"])` cuenta `NA == NA` como repetido, y
el `merge(..., validate="m:1")` contra `portad` levanta el `MergeError`.
Unicidad de llave `(folio, ls)` en las once tablas que el medidor abre:

| tabla | filas | duplicados |
|---|---|---|
| `c_portad` | 8441 | **2** |
| `iiib_hs1` | 1200 | 140 (se deduplica con `drop_duplicates`, no es el fallo) |
| `iiib_es` · `p_es` · `iiib_ec` · `iiib_hs` · `p_hs` · `iiib_ce` · `p_ce` · `w_b3b` · `w_bx` | 19804 · 1848 · 17728 · 19799 · 1848 · 19803 · 1848 · 35677 · 35677 | 0 |

**El medidor MIDE el caso y no lo usa.** Su propia guardia de fan-out recorre
`portad`, `w_b3b` y `w_bx` y escribe `RESULT-LLAVE-UNICA-PORTAD`, que habría
dicho `REPETIDA (2 filas duplicadas)`; pero la guardia **reporta y sigue**, y el
`validate="m:1"` de tres líneas más abajo revienta antes de que nada se selle.
Además la guardia cubre 3 de las 6 tablas que el código usa como lado derecho
de un merge.

Por regla del encargo la spec **no se editó** («Spec mal contra el dato: no se
edita»). Tampoco nació aquí el id sucesor: escribir un `spec.yaml` nuevo es
sustancia metodológica de la clase de `E5-0`, está fuera del perímetro de este
acto («No toca specs, `spec.yaml`…») y este acto «no decide nada». Va como
`FP-355` + `NC-0044`, con el diagnóstico completo para que el sucesor no lo
repita.

---

## 4 · `verify` — los dos ejes, sin mezclarlos

| CALC | CONTEXTO | RESULTADO | veredicto |
|---|---|---|---|
| `CALC-0001` | `DISTINTO` (`parametros_distintos`) | `NO-REPRODUCE` (22 de 54) | `NO-REPRODUCE · CONTEXTO-DISTINTO` |
| `CALC-0002` | **`IDENTICO`** | `NO-REPRODUCE` (4 de 29) | `NO-REPRODUCE` |
| `CALC-0003` | — | — | no hubo `verify`: `run` no selló |

**Ninguna de las cuatro etiquetas negativas es una divergencia numérica.** En
los 26 `RESULT` marcados `NO-REPRODUCE`, `sellado` es **igual** a `hoy`. Son dos
defectos de `tools/corrida0.py`, ambos fuera del perímetro de este acto:

**(a) `CONTEXTO` — `_evalua_contexto`, `FP-353`.** `run` serializa
`spec.parametros` a `ejecucion.json`, y JSON convierte toda llave de mapping en
cadena. `verify` compara ese dict contra el YAML recién parseado, donde las
llaves son enteros. `spec.yaml` sale `IDENTICO` (2/5) y los parámetros salen
`DISTINTO` en la misma corrida:

```
spec(yaml): {29: [2, 9]}          ejec(json): {'29': [2, 9]}
spec(yaml): {1: 1, 2: 2, 3: 4…}   ejec(json): {'1': 1, '2': 2, '3': 4…}
```

`CALC-0001` trae 12 llaves enteras (`crosswalk_partido`, `coaliciones`); por eso
le pega a él y no a los otros. **`CONTEXTO: IDENTICO` es inalcanzable, en
cualquier árbol, para toda spec con un mapping de llaves no-cadena.** Que
`CALC-0002` — cero llaves enteras — saliera `IDENTICO` es el control positivo.

**(b) `RESULTADO` — `_compara_result`, `FP-354`.** La función no tiene rama para
`None`. Un output que la propia spec autoriza como no estimable
(`permite_no_estimable: true`, que `_valida_outputs` respeta y `run` sella) se
cuenta `NO-REPRODUCE` con el mensaje ``tipo declarado `flotante` y
sellado=None``, aunque `sellado` y `hoy` sean los dos `None`. Las dos funciones
implementan contratos contradictorios sobre el mismo valor. Alcance: `CALC-0001`
declara 29 de 54 outputs `permite_no_estimable`, `CALC-0002` 18 de 29 y
`CALC-0003` 48 de 128 — **cualquier CALC con un solo output así no puede llegar
nunca a `REPRODUCE`**.

---

## 5 · `status` — el contador **no** dejó el cero, y por qué

```
# derivado de 99 corridas · 473 resultados · 205 usos
N_corridas_requeridas=86
N_corridas_selladas=0
N_resultados_activos=205
N_resultados_sellados=0
N_resultados_pendientes=205
dependencias_numericas_legacy_activas=205
N_resultados_gen2_sellados=0
N_resultados_gen2_pendientes_adopcion=0
N_resultados_gen2_adoptados_activos=0
resultados_con_validacion_independiente=0
diferencias_materiales=0
no_corrido_abiertas=25   # 22 al abrir el acto; -1 por NC-0042 CERRADA, +4 por NC-0044..0047
replays_legacy_sellados=2
corredores_envueltos_legacy=8
```

El encargo lo previó: «si no suben, algo del cableado falló y es hallazgo, no se
fuerza». **El cableado no falló.** `registro` sí incorporó las dos corridas
(`resultados.tsv` 390 → 473 filas, `+83 = 54 + 29`) y sí ve las cinco citas de
la propuesta. Lo que falta es una **firma de mesa**.

Los tres `spec.yaml` congelados por `E5-0` declaran
`etiquetas.cuenta_gen2: PENDIENTE-DE-MESA`. `_cuenta_gen2_resuelto` tiene cuatro
niveles de precedencia y el primero es `data/corrida0/decisiones.tsv` (D-1);
sin fila ahí, la etiqueta de la spec manda y `PENDIENTE-DE-MESA` **sobrevive
como valor propio** — el código dice, literal, que «no se colapsa a `NO` por
comodidad del contador». Y los contadores exigen `cuenta_gen2 == "SI"`.

**Control positivo, con la firma SIMULADA en memoria y nada escrito en disco**
(`_lee_decisiones` monkey-patched dentro de un `python3 -`; `git status
--porcelain` después sólo mostró los dos TSV que `registro` había re-derivado):

| contador | árbol real | con la firma simulada |
|---|---|---|
| `N_corridas_selladas` | 0 | **2** |
| `N_resultados_sellados` | 0 | **83** |
| `N_resultados_gen2_sellados` | 0 | **83** |
| `N_resultados_gen2_pendientes_adopcion` | 0 | **5** |

**Lo que mesa tiene que firmar** — dos filas en `data/corrida0/decisiones.tsv`,
que este acto NO escribe porque falsificaría una firma de mesa y porque ese
archivo está fuera de su perímetro:

```
CALC-0001	cuenta_gen2=SI · <motivo de mesa>	D-1 (mesa 2026-09-..)	2026-09-..
CALC-0002	cuenta_gen2=SI · <motivo de mesa>	D-1 (mesa 2026-09-..)	2026-09-..
```

El día que existan, `N_resultados_gen2_sellados` pasa de 0 a 83 sin volver a
correr un solo medidor. Va como `FP-356` + `NC-0045`.

**`dependencias_numericas_legacy_activas` = 205, no 162.** El encargo declaraba
«162 → 162−k». La cifra vigente del árbol es 205 y **no baja por sellar**: por
diseño (`ACTO GEN2-PRE-E5` P3) ese contador mide sólo lo que un consumidor
**activo** lee de verdad, y sellar un `RESULT` «no la mueve un bit por sí solo».
Se declara la diferencia en vez de absorberla.

---

## 6 · `T-REPRO` (T35) — de WARN a FAIL, con su límite dicho

`E6` dejó programado el cambio para «el cierre de E5» y aquí se ejecutó: los 18
`warn("T-REPRO", …)` de `t35_repro` son ahora `fail(…)`, y la etiqueta del test
pasó de `T35 T-REPRO [aviso]` a `T35 T-REPRO`. Los dos falsadores de
`tests/test_corrida0.py` que leían `chk.WARNS` ahora leen `FAILS + WARNS`:
siguen exigiendo lo mismo — que T35 señale el caso — sin depender de la
severidad vigente. `tests/test_corrida0.py`: **59 casos · 59 ok · 0 FALLOS**.

**El FAIL todavía no se ejerce sobre una cadena GEN2 real.** Mientras no exista
la firma de §5, los ramales (a), (b), (c) y (11.1) siguen con universo **vacío**;
el único con universo hoy es (11.2), inmutabilidad estructural, que sí cubre los
sellos nuevos. Se dice aquí y en el propio comentario del test, en vez de dejar
puesto el rótulo `[aviso]` sobre un test que ya no avisa.

**Suite al cierre:** `python3 tests/check.py --baseline` → `LÍNEA BASE: VERDE`,
`3 FAIL · 202 WARN`, nada nuevo frente a `tests/baseline.json`.

**La cláusula «caja limpia» de la compuerta no se cumplió y no es cumplible
desde el ejecutor.** `python3 tools/limpia_arbol.py --reporta` da 11 worktrees
vivos, 9 ramas locales ya fusionadas y 1 rama remota `fuera_de_politica`
(`claude/new-session-98j16e`), todas ajenas a esta sesión; `/acto` §1.0.d
prohíbe expresamente decidir su borrado desde aquí. Es el mismo limbo que
`E5-0` ya había declarado, sin sucesor asignado.

---

## 7 · Lo que este acto NO decidió

No editó ninguna spec ni ningún `spec.yaml`. No escribió `decisiones.tsv`. No
tocó `tramite.yaml`, `procedencia.yaml` ni canon. No corrigió `corrida0.py`
—los dos defectos de §4 quedan medidos, no parcheados—. No hizo nacer el id
sucesor de `CALC-0003`. No adoptó ninguna cifra: las dos entradas nuevas de
`milpa/tramite-ola5-propuesta-v0.yaml` (una por CALC sellada) son
`PENDIENTE-DE-MESA` y el motor no
carga ese archivo.

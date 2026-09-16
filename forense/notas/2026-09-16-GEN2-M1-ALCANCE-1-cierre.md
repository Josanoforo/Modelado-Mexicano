# ACTO GEN2-M1-ALCANCE-1 · nota de cierre

> | | |
> |---|---|
> | **ACTO** | `GEN2-M1-ALCANCE-1` · EL ESTIMADOR ES DE LA CELDA; LA MATRIZ COMPONE |
> | **ADR** | `ADR-531` |
> | **ENCARGO** | `forense/encargos/2026-09-16-GEN2-M1-ALCANCE-1.md` (0-bis A.3, verbatim) |
> | **BASE** | `b881ee6` (merge de `PR #820`) — la misma que el encargo declara, re-derivada al abrir: `git rev-list --count HEAD..origin/main` → `0` |
> | **ENTORNO** | NUBE, Opus. `tools/entorno.py`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, `corpus=NO (archivos_examinados=0)`, `raices=data_raw:NO`, sonda de red **no ejecutada** (opt-in; este acto no toca red de datos) |
> | **COMPUERTA** | `ninguna` — declaración explícita, no dispara verificación |
> | **FIRMA DE MESA** | rama **[B · precisar]**, verbatim en el mensaje de lanzamiento (A.12) |
> | **CONTADOR** | **cero mediciones**, dicho sin disfraz. `no_corrido_abiertas` +4 (`NC-0271`..`NC-0274`). `FP-377` nace y muere `FIRMADA` en el mismo acto |

---

## 0 · La firma, y qué rama abrió

Mesa confirmó **[B · precisar]**, verbatim:

> **FIRMA DE MESA, mesa, 17 de septiembre de 2026 — OBJETO (M1, ADR-91):** cada
> celda tiene su estimador, su ruta y su dato; el motor no tiene un estimador
> único. ADR-91 se mantiene con alcance precisado: el cómputo matricial es la
> forma de composición del ejecutable, no el estimador de ninguna celda. La
> estimación de cada insumo la gobierna el contrato celda-D (ADR-68); la matriz
> compite en él como candidato, nunca por defecto.

Consecuencias de rama, aplicadas: `ADR-91` recibe **estampa de alcance**, no
`REVOCADA`; `ADR-401` **no se toca**; `NC-0020` **no se toca** (su enmienda era
de la rama (A)); las filas y enmiendas dicen **«precisada»/«precisó»**, nunca
«revocada».

**Discrepancia de fecha, declarada y no corregida.** La firma se fecha **17 de
septiembre de 2026** y este acto corrió el **16 de septiembre de 2026**. Donde
el registro es de la firma (`decisiones.tsv:fecha`, `FP-377`, el texto de las
enmiendas que el encargo dicta verbatim) se escribe **17/sep**: la fecha con que
mesa firmó no es del ejecutor editar. Donde el registro es de la ejecución (el
ADR, el `creado` de `FP-377`, las cabeceras de enmienda) se escribe **16/sep**.
Las dos fechas conviven a la vista en cada sitio, que es lo contrario de
esconder la discrepancia. Reserva: `NC-0274`.

---

## 1 · A.8 re-derivada al abrir — dónde el encargo acierta y dónde se queda corto

El encargo pide re-derivar. Se re-derivó, y el veredicto de dirección se
sostiene: **EXISTE-NO-SATISFACE**. Tres correcciones de detalle, todas por
comando.

**(a) Los máximos coinciden, y los candidatos también.** `ADR` máximo `530`,
`FP` máximo `376`, `NC` máximo `0270` — los tres re-derivados con el comando de
la casa sobre el árbol, no heredados de la cabecera del encargo. Candidatos
`ADR-531` · `FP-377` · `NC-0271`+, exactamente como el encargo predecía.

**(b) Los 8 archivos existen, pero dos de las líneas que el barrido de
dirección alcanzó NO están vencidas — y otras dos que no alcanzó sí lo
están.** El barrido se rehízo en Python sobre los **1 841 `.md` versionados**
(de 5 253 archivos versionados), excluyendo los homónimos `ADV1-M1`,
`MARCO-M1-A`, `EMISOR-M1` y `M10`–`M19`. Resultado:

| archivo | líneas vencidas | nota |
|---|---|---|
| `propuesta-motor-adaptativo-celda-v0_1.md` | `:12`, `:164`, `:217` | |
| `propuesta-motor-adaptativo-celda-v0_2.md` | `:11`, `:123`, `:179`, `:187` | |
| `propuesta-motor-adaptativo-celda-v0_3.md` | `:13`, `:96`, `:184` | `:196` **excluida**: usa `M1-M9` como rango de numeración, no declara nada sobre M1 |
| `propuesta-motor-adaptativo-celda-v0_4.md` | `:13`, `:148` | |
| `propuesta-motor-adaptativo-celda-v0_5.md` | `:11`, `:104` | |
| `canon/estado-programa-v1_13.md` | `:218` | `:185` **excluida**: cita `ADR-91` **correctamente** («el motor es matricial por sello de mesa»), no está vencida |
| `canon/gobernanza-v1_15.md` | `:1232` | entrada `ADR-68`, *«sin adoptar M1»* |
| `forense/notas/2026-08-12-acto-v-vocabulario-celda-d.md` | `:45` | |
| `propuesta-motor-matriz-v0_1.md` | `:197`, `:214` | §9, la formulación original de M1 |

**El «8 archivos» es un piso, no un techo.** Dos archivos más traen la misma
declaración vencida, en futuro condicional, y quedan **fuera del perímetro**
declarado: `forense/CASCADA-M1-2026-08-14.md` (§«Qué cambia **si** M1 se
firma», seis menciones) y `forense/ADR-MOTOR-2-esqueleto-2026-08-14.md`
(`:35`, literalmente `[FIRMA M1 — VACÍA]` — la ranura sigue en blanco trece
meses después de que mesa la llenara). No se tocan aquí; `NC-0272`.

**(c) La cobertura retroactiva es como el encargo la describe.**
`data/corrida0/decisiones.tsv` arranca el `2026-09-07` y `ADR-91` es del
17/ago: la ausencia de M1 en esa tabla nunca probó nada. Este acto la asienta
por primera vez, como historia.

---

## 2 · A.13 — el negativo que no podía ser otra cosa

Dirección concluyó «M1 sigue abierta» de un `grep` con patrón
`M1 negativ|cierra M1|M1 RESUELTA|adopta M1|M1 se adopta` sobre
gobernanza/estado/modelo, que da **0**. Re-derivado: **el `0` es correcto y no
significa nada**, porque el patrón no puede encontrar la firma. El texto que
mesa firmó el 17/ago es *«cómputo matricial como definición del ejecutable»*, y
esa frase vive en **19 archivos versionados**:

```
git ls-files -z | xargs -0 grep -lE "c(ó|o)mputo matricial como definici(ó|o)n del ejecutable"
```

— `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_13.md` entre ellos.
El fragmento `adopta M1|adoptar M1` sí existe, en **3 archivos**
(`canon/estado-programa-v1_13.md`, `canon/gobernanza-v1_15.md`,
`propuesta-motor-adaptativo-celda-v0_3.md`), y en los tres dice *«sin adoptar
M1»*: la declaración vencida, no la firma.

El control que faltaba cuesta un comando: **antes de concluir de un `grep`
vacío, correr el mismo `grep` contra el texto que sí se sabe que existe.**
Línea asentada en `forense/hallazgos.md`.

---

## 3 · Lo que se escribió, pieza por pieza

### P1 · Propagar la firma — **completa**

- **(a)** `data/corrida0/decisiones.tsv`, **+2 filas, 0 borrados**. Objeto
  `M1:ADR-91` en las dos. La histórica (`fecha = 2026-08-17`) lleva el verbatim
  de la firma del 17/ago tal como `FP-01` y `ADR-91(b)` lo registran, y declara
  en su propia columna `fuente` que es un asiento **retroactivo**. La de hoy
  (`fecha = 2026-09-17`) lleva el verbatim de la precisión y la discrepancia de
  fecha declarada.
- **(b)** `FP-377` **nace FIRMADA** — no pide una decisión, registra una ya
  dada; existe porque `A.12`/`ADR-91` exigen que toda decisión de mesa tenga
  fila o no exista, y ésta no la tenía. `FP-01` recibe `ENMIENDA FECHADA` en
  `ejecutada_en`; **lo firmado no se edita**.
- **(c)** `canon/gobernanza-v1_15.md`: dos `ENMIENDA FECHADA` in situ, **0
  borrados**. Bajo `ADR-91`, la estampa de alcance con el verbatim del 17/sep.
  Bajo `ADR-68` — cuyo propio título dice *«sin adoptar M1»* desde el 11/ago y
  quedó vencido el 17/ago —, la estampa que nadie le había puesto, más lo que
  la precisión le devuelve: el contrato celda-D que ese ADR adoptó es, desde el
  17/sep, **la sede** de la competencia entre estimadores, no un formato al que
  la matriz hubiera dejado sin objeto.
- **(d)** `PARA-v2.14` en `forense/hallazgos.md`.
- **(e)** Línea `A.13` en `forense/hallazgos.md` (§2 de esta nota).

### P2 · Enmiendas fechadas donde M1 se declara abierta — **completa**

Nueve archivos (los 8 de A.8 + `propuesta-motor-matriz-v0_1.md` §9), cada uno
con una enmienda fechada que nombra **las líneas afectadas por número** y cita
las dos firmas. **Texto original intacto en los nueve, verificado
mecánicamente**: `git diff --numstat -- '*.md'` da **0 borrados** en prosa
(A.10 corolario 1). Los dos canónicos la reciben **in situ** bajo el bloque
afectado, no al pie: en un registro de ADR, un pie de archivo no es el sitio
donde alguien que lee `ADR-68` va a mirar.

### P3 · `g()` alineada con su docstring — **completa**

`milpa/src/matriz.py::g()` prometía lanzar `SinMagnitud` «si una celda
**participante** no tiene número» y recorría `B` entera. Con `G5 ×
familismo_obligacion` sin magnitud — la única celda sin magnitud de `B`, y la
hay por diseño —, **ningún** generador era computable, ni los que no la tocan.
El docstring y el código decían cosas distintas desde el sello, y la firma del
17/sep dice cuál de los dos tenía razón.

Nueva firma: `g(matriz, theta, celda, generadores=None)`.

- `None` → `B` entera, **contrato de siempre intacto, letra por letra**.
- subconjunto → participan esas celdas y nada más.
- generador ausente de `B` → **`KeyError`**. Devolver `{}` ante un nombre mal
  escrito sería la misma mentira silenciosa que el cero de `SinMagnitud`, un
  piso más arriba. **Esto no lo pidió el encargo**: es superficie nueva (ningún
  llamador existente pasa `generadores`), no toca el contrato sellado, y se
  declara aquí para que sea de mesa revertirlo si no lo quiere.

**`milpa/src/motor.py` NO se toca.** El encargo le reservaba «solo paso de
argumento»; verificado por `grep` sobre `milpa/`, `tests/` y `tools/`,
**`motor.py` no llama a `g()` en ninguna línea** — tiene su propio chequeo de
`matriz_B.sin_magnitud`. El paso de argumento resultó ser cero cambios, no uno
pequeño. Por tanto **no se dispara el PARO** que el encargo reservaba para el
caso contrario.

Tests (`tests/test_motor_matriz.py`, 7 → 10 pruebas): `G1` computable pese a
`G5`; pedir `G5` **sigue lanzando**; generador inexistente es `KeyError`.

Los cuatro tests del encargo, **verdes antes y después**: `T-MOTOR-MATRIZ`
`10 ok` · `T-MOTOR-EJECUTABLE` `6 ok` · `T-MATRIZ-SELLADOS` `6 ok` ·
`T-MOTOR-HOLDOUT` `6 ok`.

> **Antes de eso hubo un `FAIL` que no era un `FAIL`**, y vale la línea:
> `test_motor_holdout.py::test_c_roles_sellados_antes_que_todo_resultado` falló
> en la primera corrida con *«el catálogo y el motor entraron en el MISMO
> commit»*. No entraron. El clon de esta sesión nacía **`shallow`** (614
> commits; `git rev-parse --is-shallow-repository` → `true`) y
> `git log --diff-filter=A` devolvía, para los dos archivos, el mismo borde de
> injerto `8f47fe62`, listado en `.git/shallow`. La guarda que el test ya tiene
> (`saltar("sin historia de git en este entorno")`) sólo dispara si `git` falla
> o devuelve vacío, y una historia **truncada** no es ninguna de las dos:
> devuelve un SHA, sólo que el equivocado. Tras `git fetch --unshallow`
> (4 496 commits) el test pasa sin tocar una línea de código. Corregir el test
> queda fuera de perímetro: `NC-0273`.

### P4 · Re-rotular el bloqueador — **completa**

`NC-0239` recibe `ENMIENDA FECHADA`: el bloqueador del marcador por segmento
**no es «θ cargable» como interruptor global** — un booleano del motor que se
enciende una vez y desbloquea el marcador entero — sino **«celdas con estimador
adjudicado en el catálogo de momentos», contadas una por una**. Consecuencia
operativa: el marcador no espera a que θ cargue entera; avanza celda por celda,
y el conteo de celdas adjudicadas **es** la medida del avance. Sucesor →
`GEN2-CELDA-D-PILOTO-1`.

`NC-0024` y `NC-0076` **sí heredan** la lectura global — verificado por `grep`,
la traen literal (*«luego `g(B, theta(x))` no computa para ningún x»* y *«una
sola deuda con un solo bloqueador (theta)»*) — y reciben la misma enmienda. El
«para ningún x» de `NC-0024` era además consecuencia del defecto que P3
corrige, no de una imposibilidad de la composición. Las tres siguen `ABIERTA`:
esto re-rotula el bloqueador, no lo levanta.

`NC-0020` **no se toca** — su enmienda pertenecía a la rama (A), y mesa firmó (B).

### P5 · Insumo D-θ archivado — **PARA**

`D-THETA-DOCUMENTO-v1_1-post-adversarial.md` **no viajó**. Buscado por nombre
en todo el sistema de archivos (`find / -iname "*D-THETA*"`, `-iname
"*D_THETA*"`, `-iname "*post-adversarial*"`) y en el árbol versionado: cero
resultados. Sin adjunto no hay `sha256` que cotejar contra
`8a6472a72631dfdc…`, y archivar «verbatim» un documento que no se tiene es
exactamente lo que una cabecera de procedencia tipo 3 existe para impedir.
`forense/notas/insumos-direccion/` **no se crea vacío**. El encargo previó este
caso y lo acotó: *«P5 PARA y no tumba el lote»*. `NC-0271`.

---

## 4 · Perímetro

Todo lo escrito cae dentro del perímetro declarado. No se tocaron
`milpa/src/theta.py`, `milpa/src/motor.py`, `milpa/procedencia.yaml`,
`milpa/tramite.yaml`, `milpa/src/celdas.py` (`CORTES_C1`), specs, resultados ni
el marcador — verificable en el diff del PR. `tests/check.py` se tocó
**sólo** para la exención `T25` (el token pelado `M1`, precedente `ADR-530` con
`M2`, misma serie y misma razón), con el comentario que explica de dónde sale
cada mención.

## 5 · Lo que este acto NO hizo

No carga θ · no escribe ni corre celdas-D · no cambia un solo número del modelo
· no toca `CORTES_C1` ni `FP-53` · no reabre `F5` · no escribe D-θ v1.2 ni el
piloto · no revoca `ADR-91` ni toca `ADR-100`/`ADR-401` · no cierra ninguna
`NC`.

## 6 · Sucesores

- `GEN2-CELDA-D-PILOTO-1` (Opus; gated a este merge) — sucesor nombrado de
  `NC-0239`/`NC-0024`/`NC-0076`.
- D-θ v1.2 — dirección.
- `GEN2-D-THETA-CAREO-1` — sin urgencia.
- `NC-0271`..`NC-0274` — ver `## NO-CORRIDO / RESERVAS` del encargo archivado.

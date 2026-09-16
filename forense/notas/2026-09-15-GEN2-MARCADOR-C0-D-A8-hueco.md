# `ACTO GEN2-MARCADOR-C0-D` — nota de cierre

**15 de septiembre de 2026 · NUBE, Opus · cero microdato · cero medición del
modelo · cero adopción · cero cambio al motor, al emisor ni a ningún sello**

Encargo archivado verbatim (0-bis A.3):
`forense/encargos/2026-09-15-GEN2-MARCADOR-C0-D.md`.
Compuerta: ninguna. Base: `origin/main = 0cdbd72` (`PR #789`).

---

## 0 · El veredicto, primero

> **`RESULT-A8-C0-C` = `NO-ENCONTRADO`** — no existe ningún acto `C0-C` en el
> árbol, ni encargo, ni nota, ni rótulo censado, ni ADR. Por la propia cláusula
> del encargo («si no, **ese hueco es el entregable**») y por `A.8` pregunta
> (1) («si el índice no cubre el dominio, ese hueco es el entregable: se
> reporta y **el encargo se detiene ahí**, en vez de inventar una vía»), este
> acto **no corre el marcador por segmento**. Entrega el hueco, medido.
>
> **Y el hueco no es el que la etiqueta `C0-C` describía.** Lo medido hoy dice
> que el marcador por segmento está bloqueado por **tres** cosas
> independientes, y que la que muerde primero **no es «motor y emisor
> limpios»** — el motor arranca desde el 8/sep y el emisor tiene contrato GEN2
> desde el 11/sep. La que muerde es **θ**:
>
> ```
> theta.valor()  ->  lanza ThetaNoDisponible en 43 de 43 entradas
> ```
>
> `g(B, θ(x))` —la definición misma de «M por motor matricial» que `NC-0024`
> nombra— **no es computable para ningún `x`**, y no por cableado: `θ` es
> calibración —la fase que sigue al arranque del motor—, ley de mesa
> vigente, a la espera del cierre de `BARRIDO-2`. Redactar `C0-C` como «motor y emisor limpios» y esperar que de
> ahí salga el marcador por segmento **es esperar lo que esa pieza no produce.**

**Lo que sí se produjo aquí**, porque era derivable en nube y sin microdato:

1. El **sucesor de `NC-0078`**, ejecutado: el metadato de alcance derivado de
   las **dos familias de esquema** (§4). Y con él un hallazgo que el muestreo
   de una captura escondía: `modelo_real` es **`None` en las 648 capturas** que
   traen ese campo — el `modelo=None` del `RESULT` sellado **no era** artefacto
   de muestreo.
2. Una **corrección medida** sobre un `RESULT` sellado que tres documentos
   citan como premisa: `RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC = 74` **cuenta
   celdas, no celdas con IC**. Con IC son **64** (§5).
3. El **cruce que nadie había hecho** y que decide si el marcador por segmento
   tiene vocabulario: de los 74 puntos del árbitro, **6** caen sobre un eje con
   corte **sellado** en el modelo; 16 sobre uno **PENDIENTE**; **52 sobre ejes
   sin correspondencia alguna** (§6). La frase vigente *«el hueco es de
   cableado, no de dato»* **queda vencida**: también es de vocabulario.
4. La **readiness que `E.5` exige**, re-verificada hoy y no citada de memoria
   (§2).

---

## 1 · `A.8`, contestado con comando y salida

### (1) ¿Existe ya la estructura?

El dominio de este encargo es *el registro de actos y de deuda*. Las tablas
gobernantes son `canon/registro-rotulos.tsv` (qué actos existen),
`forense/no-corrido.tsv` (qué quedó sin correr) y `canon/gobernanza-v1_15.md`
(los ADR). Las tres existen y cubren el dominio. **No hay hueco de estructura.**

### (2) ¿Existe ya el contenido? — `C0-C`

```
$ cut -f2 canon/registro-rotulos.tsv | grep -c "C0-C"                 -> 0
$ ls forense/encargos forense/encargos/cola | grep -c "C0-C"          -> 0
$ ls forense/notas | grep -c "C0-C"                                   -> 0
$ grep -c "ACTO GEN2-C0-C\|ACTO C0-C" canon/gobernanza-v1_15.md       -> 0
```

**`NO-ENCONTRADO`** (`A.4`), buscado por rótulo en las tres tablas gobernantes
y por nombre de archivo en los dos directorios de actos. Coincide con lo que
`NC-0075` midió el 9/sep y lo extiende seis días: **`C0-C` nunca se redactó.**

`C0-C` sólo existe como **mención**: `PLAN-FINAL-GEN2-v2_0` §7 («`C0-D` corre
el marcador por segmento cuando `C0-C` entregue motor y emisor limpios»), la
cola de `ENCARGOS-GEN2-en-orden` y los sucesores de `NC-0022`/`NC-0024`. Es una
etiqueta en una lista de orden, no una pieza con perímetro.

### (3) ¿La estructura es posterior al trabajo que toca?

No: `no-corrido.tsv` y `registro-rotulos.tsv` son anteriores a las siete filas
de este encargo (la más vieja, `NC-0024`, es del 8/sep). **No hay brecha de
fechas que declarar.**

---

## 2 · `E.5` — la readiness del marcador, re-verificada hoy

`E.5` exige «readiness del marcador (M, R, L, agregado) … para lo que la
corrida vaya a alimentar». **Está hecha desde el 8/sep** (`ACTO GEN2-E7`,
`ADR-398`) y **sigue verde hoy**, corrida en esta sesión y no citada de
memoria:

```
$ python3 tests/gonogo_marcador.py
  [PASA] MARCO-VIGENTE-UNICO      [PASA] L-SPEC-v1_2
  [PASA] M-DESDE-CONTRATO         [PASA] AGREGADO-DERIVADO
  [PASA] R-SIN-HEURISTICA         [PASA] LEGACY-NO-LEIDO
GO-MARCADOR
```

**Lo que `GO-MARCADOR` acredita y lo que no.** Acredita que los cuatro
corredores (M, R, L, agregado) están envueltos, sin heurística y sin leer
legado. **No** acredita que el marcador **por segmento** pueda correr: ninguno
de los seis checks mira `θ`, ni el vocabulario de ejes, ni la columna de
segmento del marco. El informe interno que va a citar el marcador puede citar
`GO-MARCADOR` con esa distinción escrita; sin ella, un lector leerá «listo»
donde lo medido dice «listo el eje `x = ∅`».

---

## 3 · Las siete filas, re-medidas hoy contra el árbol

| fila | lo que afirmaba | medido el 15/sep | veredicto |
|---|---|---|---|
| `NC-0024` | marcador por segmento, `M` por motor matricial, `R` por IC de `_ejes_` | `theta.valor()` lanza en 43/43 · marco sin columna de segmento · 6/74 puntos sobre eje con corte sellado | **ABIERTA**, y su sucesor mal apuntado (§7) |
| `NC-0026` | las dos funciones puras existen, `emite_celda` no las llama | sigue exacto: `grep` de llamadas → sólo `tests/` y el medidor de `CALC-M-…-ola-v2`; `emite_celda` no las llama | **ABIERTA**, y **ya tiene consumidor sellado** (§3.a) |
| `NC-0070` | `N-CELDAS-MODULADAS-GEN2 = 0` | 6 celdas modulan por **ola** en `CALC-…-ola-v2`, pero con `cuenta_gen2: NO`; las 6 celdas con serie de C0-B siguen sin CALC sellado | **ABIERTA** |
| `NC-0072` | 442 `RESULT` GEN2 sin adoptar; la segunda silla necesita un CALC nuevo | el vocabulario cambió: `SELLADA-SIN-ADOPTAR` ya no se emite; hoy `3522` GEN2 sellados · `18` adoptados activos · `12` pendientes · `2` vetados | **ABIERTA**, cifras vencidas |
| `NC-0075` | `C0-C` no existe; cerrar `NC-0024`/`NC-0026` con cita sería cerrar deuda por decreto | confirmado seis días después, con los mismos comandos (§1.2) | **ABIERTA**, y su diagnóstico **se ratifica** |
| `NC-0076` | el marcador no tiene ranura; el registro reconoce cuatro clases | la superficie sigue siendo sólo `milpa/tramite.yaml` + `milpa/procedencia.yaml`; las clases hoy son **ocho**, no cuatro | **ABIERTA**, sustancia intacta (§3.b) |
| `NC-0078` | el `RESULT` de alcance muestrea una captura y sale pobre | **sucesor ejecutado aquí** (§4) | **ABIERTA** — el `RESULT` sellado no se retoca; lo derivado vive en esta nota |

### 3.a · `NC-0026` ya no es código muerto — y eso cambia su razón, no su estado

La fila dice que cablear las dos funciones a `emite_celda` *«cambiaría la M que
el emisor produce hoy, y con ella las corridas-M ya selladas»*, y que
escribirlas sin cablearlas *«sería código muerto»*. Medido hoy:

```
$ grep -rn "ola_previa_estricta\|origen_de_entrada_serie" --include="*.py" .
  tests/test_corredores_gen2.py                                    (7 casos)
  data/corrida0/CALC-M-marco-M-sorteado-v1_3-ola-v2/medidor.py     (las importa y las corre)
```

`CALC-M-marco-M-sorteado-v1_3-ola-v2` **las consume, sellado**, declarando
`tools/emite_m.py` como input con `sha256`. Es decir: **las dos reglas ya
tienen consumidor sellado por una vía que no toca `emite_celda` ni pisa ninguna
`corridas-M/*.json`** — exactamente la salida que la fila daba por imposible.
Lo que sigue abierto es lo otro que dice: la **M del camino de emisión
vigente** sigue sin modular. Son dos cosas y conviene no confundirlas.

### 3.b · `NC-0076` — la sustancia aguanta, el conteo no

```
$ sed -n '2830p' tools/corrida0.py
    for ruta in (TRAMITE, PROCEDENCIA):
```

La superficie de adopción que el registro reconoce **sigue siendo esas dos
rutas**, un año de actos después. Pero `cmd_demanda` enumera hoy **ocho**
clases, no cuatro: conductas, coeficientes, asignados-prob, celdas, cortes-π,
celdas-D, momentos y θ. Ninguna de las ocho es un error en pp, un MAE, un IC ni
un veredicto — **la conclusión de `NC-0076` se sostiene sobre un censo mayor
que el suyo**, que es la forma fuerte de sostenerse.

**Y hay una consecuencia que la fila no vio.** `NC-0076` pide como sucesor «un
CALC cuya cantidad **sea** una `p`, un coeficiente, un corte o un momento — no
otra cita». El marcador por segmento **es** ese CALC: su `M` por celda es una
`p` de conducta. `NC-0076` y `NC-0024` **no son dos deudas, son una**, y su
único bloqueador común es `θ`.

---

## 4 · `NC-0078`, ejecutado — el metadato de alcance sobre las **dos** familias

La fila pide «un acto sucesor del marcador que derive el metadato de alcance de
las **DOS** familias de esquema (`params` y `modelo_real`) en vez de muestrear
una captura». Derivado sobre las **648** capturas de
`forense/prereg-duelo-v2/corridas-L/`, y separando el universo que el marcador
consumió (**424**, las que no traen `estado_captura`) del resto:

**Las familias son tres, no dos** — la tercera es la intersección:

| familia | 648 | de ellas, las 424 del marcador |
|---|---|---|
| sólo `params` | 120 | 120 |
| sólo `modelo_real` | 176 | 176 |
| **ambas** | 352 | 128 |

**El metadato de alcance del marcador (universo = las 424):**

| campo | valor | n | % |
|---|---|---|---|
| `params.modelo_id` | `claude-opus-4-6` | 248 | 58.49 % |
| `params.modelo_id` | AUSENTE | 176 | 41.51 % |
| `params.fecha_congelacion` | `2026-08-26` | 120 | 28.30 % |
| `params.fecha_congelacion` | `2026-09-01` | 128 | 30.19 % |
| `params.fecha_congelacion` | AUSENTE (familia `modelo_real`) | 176 | 41.51 % |
| `variante` | `L-solo` | 272 | 64.15 % |
| `variante` | `L+corpus` | 152 | 35.85 % |

Donde `params` existe, es **homogéneo**: `version_declarada = claude-opus-4-6`,
`temperatura = 1.0`, `k_corridas = 8` en las 472 del árbol, sin una sola
excepción.

**El hallazgo que el muestreo escondía, y es el que importa:**

```
capturas con campo `modelo_real`                 -> 528
capturas con `modelo_real` NO nulo               ->   0
```

**`modelo_real` está a `None` en todas.** El `modelo=None` del `RESULT` sellado
`RESULT-C0D-ALCANCE-CORPUS-CAPTURA` **no era** un artefacto de haber muestreado
la captura equivocada, como `NC-0078` supuso de buena fe: es el valor real de
ese campo en todo el árbol. La lectura que la fila temía —«una lectura futura
podría tomarlo como que el brazo no declara modelo»— hay que **partirla en
dos**: por `modelo_real`, en efecto **ninguna captura declara modelo**; por
`params.modelo_id`, **472 de 648 sí**, y todas el mismo. La redacción correcta
del campo no es `modelo=None`; es **`modelo_real=None en todas · modelo_id
declarado en 248/424 (claude-opus-4-6) · ausente en 176/424`**.

El `RESULT` sellado **no se retoca** (la fila lo pide así y el perímetro lo
manda): sellado está y sellado se queda. Lo derivado vive aquí, fechado.

---

## 5 · Una premisa citada tres veces que está mal contada

`RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC = 74` es la cifra sobre la que descansan
`NC-0024` («74 puntos por eje con IC95 que existen del lado del árbitro»), la
nota de `GEN2-T9` §6.c y la nota de cierre de `C0-D`. Leído el medidor que la
produjo:

```
$ sed -n '114p' data/corrida0/CALC-AGG-marco-M-sorteado-v1_3-ola-v2/medidor.py
                n_puntos_eje += len(e.get("celdas") or [])
```

Cuenta **celdas**, no celdas **con IC**, pese a lo que el nombre del `RESULT`
afirma. Contadas por el campo:

```
celdas totales en las 7 entradas `_ejes_` · 24 ejes   -> 74
de ellas, con `ic95`                                  -> 64
sin `ic95`                                            -> 10
```

Las 10 son **una sola entrada y un solo eje**:
`familia.cuidado.reparto_mujeres40_ejes_enut2024`, eje `sexo_edad` (los diez
cortes `hombre|mujer × 12-17…60+`). No es un error de dato: es que **el nombre
del `RESULT` promete un filtro que su medidor no aplica**. La cifra defendible
es **64 con IC de 74 puntos**. El `CALC` sellado **no se toca** (fuera de
perímetro); la discrepancia queda asentada con su causa, mismo criterio que
`GEN2-E7` §3 usó con `diagnostico-14-celdas` y `aviso_M`.

---

## 6 · El cruce que decide si el marcador por segmento tiene vocabulario

Nadie había cruzado los ejes del **árbitro** contra los cortes del **modelo**
(`milpa/src/celdas.py::CORTES_C1`). Sin ese cruce, «cablear» no significa nada:
un punto del árbitro sólo es consumible por una celda del marcador si el eje
sobre el que está partido **existe como corte del modelo**.

| eje del árbitro | celdas | con IC | corte en `CORTES_C1` |
|---|---:|---:|---|
| `edad` | 16 | 16 | **PENDIENTE** (`FP-53`) |
| `escolaridad` | 12 | 12 | sin correspondencia |
| `sexo_edad` | 10 | 0 | sin correspondencia |
| `sexo` | 8 | 8 | sin correspondencia |
| **`formalidad`** | **6** | **6** | **SELLADO** |
| `localidad` | 4 | 4 | sin correspondencia |
| `cuenta_formal` | 4 | 4 | sin correspondencia |
| `escolaridad_proxy` | 4 | 4 | sin correspondencia |
| `cohorte_nacimiento` | 4 | 4 | sin correspondencia |
| `dominio_urbano_rural` | 3 | 3 | sin correspondencia |
| `cobertura_seguro` | 2 | 2 | sin correspondencia |
| `reparto_hogar` | 1 | 1 | sin correspondencia |

Y la simétrica, que es peor: de los cuatro cortes **sellados** del modelo
(`formalidad`, `urbanizacion`, `ingreso`, `acceso_digital`), **tres no tienen
un solo punto del árbitro con ese nombre**.

**Lectura.** `formalidad` es el **único** eje donde los dos lados se tocan hoy:
6 puntos, los 6 con IC. `localidad` y `dominio_urbano_rural` *parecen*
`urbanizacion`, pero decidir que lo son es un **crosswalk de vocabulario**, y
`A.4` prohíbe resolverlo por parecido de texto: es firma de mesa, no derivación
del ejecutor. Por eso la frase vigente —*«el hueco es de cableado, no de
dato»*— **queda vencida por medición**: es de cableado **y** de vocabulario
**y**, antes que las dos, de `θ`.

---

## 7 · El hueco, nombrado con precisión — que es el entregable

El marcador GEN2 por segmento necesita **tres** cosas, y ninguna es «motor y
emisor limpios»:

**(i) `θ(x)` computable.** Hoy `theta.valor()` lanza `ThetaNoDisponible` en las
43 entradas, por diseño explícito del propio módulo: *«en […] no hay condicional
cargable por celda … antes que devolver un default, LANZA: un default
silencioso es una cifra nueva al canon disfrazada de valor por omisión»*. Sin
`θ`, `matriz.g(B, θ, celda)` no computa para ninguna celda, y «`M` por motor
matricial» no existe. Esto es **calibración —la fase que sigue al arranque del
motor—, a la espera de `BARRIDO-2`**, y es ley de mesa vigente — no es una tarea de fontanería que un
acto de nube pueda cerrar. *Nota al margen, medida: la segmentabilidad
—`theta.segmentable`— sí está permitida para 31–41 de las 43 entradas según el
eje. El permiso existe; el valor no.*

**(ii) El crosswalk de ejes, firmado.** §6. Sin él, 68 de 74 puntos del árbitro
no tienen a dónde entrar.

**(iii) La columna de segmento en el marco.** `RESULT-AGGOLA-MARCO-TIENE-
COLUMNA-SEGMENTO = NO`, verificado hoy sobre las 32 columnas de
`marco-M-sorteado-v1_3.tsv`. Es lo único de los tres que sí es cableado, y es
también lo último que sirve hacer: una columna sin `θ` y sin crosswalk es una
columna vacía.

**El sucesor correcto, entonces, no es `C0-C`.** Es, en orden:
`θ` (calibración) → crosswalk de ejes (firma de mesa) → marcador por
segmento. **`C0-C` como «motor y emisor limpios» ya está, de hecho, entregado**
por otros actos y bajo otros rótulos —`AUTO-MOTOR-1` (el motor arranca:
`RESULT-MOTOR-ESTADO-B = CARGA`), `GEN2-MOTOR-SEMANTICA`,
`GEN2-MOTOR-Y-HERENCIA-EXPLICITA` (contrato GEN2 del emisor, `NO_COVERAGE` sin
`p` vieja)— y **no desbloqueó el marcador por segmento, porque nunca fue el
bloqueador.** Mantener `C0-C` como sucesor de `NC-0024` mantiene siete filas
esperando a una pieza que, aun escrita, no las cerraría.

Esa re-apuntación es **propuesta de este acto a mesa**, no decisión suya: las
filas conservan su texto y su estado, y la enmienda va fechada en la columna
`sucesor`, mismo patrón que `NC-0077` ya usó.

---

## 8 · Lo que este acto NO hizo, y por qué

- **No corrió el marcador por segmento.** `A.8` (1) manda detenerse en el
  hueco. Correrlo hoy exigiría inventar un `θ` o un crosswalk: las dos cosas
  son cifras nuevas al canon por la puerta de atrás.
- **No cerró ninguna de las siete filas.** Ninguna se cierra con cita —
  `NC-0075` ya adjudicó eso el 9/sep y este acto lo ratifica con los mismos
  comandos seis días después.
- **No retocó ningún sello.** Ni el `RESULT` de `NC-0078`, ni el `CALC-AGG`
  del §5, ni `diagnostico-14-celdas`. Las tres discrepancias quedan asentadas
  con su causa.
- **No tocó `milpa/`, el motor, el emisor, las capturas ni las corridas.**
- **Cero microdato, cero red, cero llamada a modelo.** Todo lo medido sale de
  archivos versionados del repo.

## 9 · Contador

**Cero GEN2 del modelo. Cero adopciones. Cero corridas selladas.** Este acto
produce **registro**: una verificación `A.8`, tres derivaciones medidas (§4,
§5, §6) y una re-apuntación de sucesores propuesta a mesa.

## 10 · Suite

| | FAIL | WARN |
|---|---:|---:|
| línea base al arrancar (`origin/main = 0cdbd72`) | 3 | 4351 |
| línea base refrescada (`origin/main = 1fac27a`, árbol limpio) | 3 | 4344 |
| cierre | **3** | **4348** |

La base se movió tres veces durante el acto (`PR #792`/`#793`, luego
`#794`/`#795`/`#798`/`#799`), y cada vez el WARN cambió por causa ajena: un
acto que cierra filas lo baja, uno que las abre lo sube. Por eso la
comparación válida es contra la base **vigente al cierre**, medida en árbol
limpio (`git worktree` sobre `origin/main`) y **no inferida restando**.

**Cero FAIL nuevos.** Los tres son heredados del corpus documental (`T06` ×2,
`T08`) y ajenos a este perímetro. Los **+4 WARN** son exactamente las cuatro
filas `NC-0239..0242` que este acto abre, gritando por `A.12` como deben — que
es el defecto que `A.12` existe para hacer visible, no uno nuevo.

**Un tercer defecto, y el más instructivo: el instrumento estaba
descalibrado.** Las cifras de arriba se declararon primero como `4346` /
`4342`, medidas en esta sandbox. `T16` las rechazó **en CI** (rojo en el head
`838c430`): el runner medía `4345`. La diferencia era exactamente 1 WARN y no
era del repo — esta sandbox **no tenía `jsonschema`**, que `requirements.txt`
declara, así que `T38 T-ALTA-RELACION` emitía aquí un `NO-CORRIDO` que en el
runner no ocurre. Se corrigió **el instrumento, no el número**: se instaló la
dependencia y se re-midió todo, base y cierre. La cifra que vale es la del
runner, porque `verify.yml` es la compuerta.

Dos FAIL propios más se cometieron y se corrigieron dentro del acto: `T25` (la nota
escribía un rótulo pelado al citar la fase de calibración; se reescribió sin el
token, sin pedir exención de archivo) y `T16` (el `ADR` declaraba la cifra de la
línea base como si fuera la del cierre; ahora declara la medida). Además, en
esta sesión:

```
$ python3 tests/gonogo_marcador.py    -> GO-MARCADOR (6/6)
```

## 11 · `A.14` · NO-CORRIDO / RESERVAS

Ver `forense/no-corrido.tsv`, filas `NC-0239`–`NC-0242`.

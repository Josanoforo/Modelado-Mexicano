# ACTO GEN2-INFORME-INTERNO-F5-1 · el programa se explica a un externo — nota de cierre

**Fecha:** 15/sep/2026 · **Entorno:** NUBE, Opus. `tools/entorno.py`:
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` · `git_status=LIMPIO(0)` ·
`python=3.11.15` · numpy/pandas/scipy/pyreadstat **AUSENTES** · `raices=data_raw:NO` ·
`corpus=NO(examinados=0)` · red **no ejecutada** (sonda opt-in; este acto no toca red).
**Base:** `origin/main = 5973f12` (merge de `PR #785`), `git rev-list --count HEAD..origin/main` → `0`.
**Rama:** `claude/zealous-dirac-ee0r14` (la fija el arnés de la sesión — ver §6).
**Encargo:** `forense/encargos/2026-09-15-GEN2-INFORME-INTERNO-F5-1.md` (0-bis A.3).
**Compuerta:** ninguna.

## 0 · Qué se pidió y qué salió

| pieza | pedido | salió |
|---|---|---|
| **Objeto** | documento del programa en `canon/informe-programa-v1_0.md` «o donde el índice de infraestructura diga; si no lo cubre, ese hueco es entregable» | **HECHO, con el hueco cobrado.** El índice **no** lo cubría (verificado con comando antes de escribir la ruta): se tomó la ruta del encargo y se añadió la fila al índice por regla de conducto `ADR-70(c)` |
| **Anexo** | tablas y sus universos, `A.10` en cada cifra | **HECHO.** `canon/informe-programa-v1_0-ANEXO.md`, 8 secciones; las dos derivaciones propias con comando pegado, salida cruda y **control positivo** |
| **Tesis fija** | `D1` verbatim, «el acto no la reinterpreta» | **HECHO.** En bloque de cita, §1, sin parafrasear; la traducción para el externo va aparte y marcada como tal |
| **Primaria** | `SIN-GANADOR-ÚNICO` con su dependencia de composición (68.88% cívico; inversión con igual peso por grupo) | **HECHO y derivado, no copiado.** §3.1 del informe y §A.2 del anexo |
| **Secundaria** | éxito local en dos celdas con paquetes preparados | **HECHO.** §A.4, con la frontera «local, no generalización» y la razón por la que el control abstuvo correctamente |
| **F6** | propuesta pendiente con su gate (lista nominal) | **HECHO.** §A.5: `FP-374` ABIERTA, 0 familias retenidas ejecutables, faltan 18/18, presupuesto **no** autorizado |
| **Cierre** | reglas de decisión + módulo de auditoría contestado, incluida la pregunta v2.3 | **HECHO.** §5 (nueve reglas SI-ENTONCES) y §6 (módulo contestado; v2.3 en una línea al inicio: **cero**) |
| **D-A** | «incorpora el sello cuando exista, **sin esperarlo**» | **NO EXISTE** — verificado con universo. Se entregó la tabla como derivación propia con procedencia declarada y re-sello previsto. `NC-0218` |

## 1 · La cifra que el informe existe para no dejar circular sola

El resultado primario del duelo F5 es `SIN-GANADOR-UNICO`. Leído sin contexto,
invita a dos conclusiones falsas simétricas («el motor no sirve» / «el LLM ya
sabe»). Lo que el panel realmente dice está en dos hechos:

```
$ python3 - <<'PY'   # (comando completo y salida cruda en el anexo §A.2)
...
l_solo   por_celda=3.957361  por_grupo=7.315040
l_corpus por_celda=3.889025  por_grupo=7.529373
m        por_celda=4.986673  por_grupo=5.028459
share civico en M = 68.88%
PY
```

**Con igual peso por celda M pierde; con igual peso por familia M gana.** Mismo
dato, dos composiciones, dos rankings — y el panel no distingue cuál de las dos
ponderaciones es la correcta. Ése es el contenido de `SIN-GANADOR-UNICO`: no una
adjudicación cerrada en empate, sino **una pregunta mal dimensionada** — 12
celdas en 5 familias, cuatro de ellas con una sola celda en `U3`, y el 68.88%
del error de M concentrado en la única familia con seis.

**Control positivo de la derivación.** La columna «por celda» reproduce
exactamente los tres MAE que la nota sellada de `GEN2-F5-APRENDIZAJES-Y-SUCESOR`
publica antes del redondeo tabular. Sin ese control la columna de la derecha
sería aritmética sin auditar; con él, es una propiedad del panel.

## 2 · La tabla de 9 celdas, y por qué NO es el sello de D-A

`D2` registra la comparación descriptiva de 9 celdas comunes como corrida de
registro. **`D-A` no existe todavía**, y el encargo manda no esperarlo (`D5`).
Se resolvió por el camino que no fabrica procedencia: `§A.3` del anexo trae la
tabla **derivada de notas selladas**, con su procedencia columna por columna
(`B` de `GEN2-B-MARCO`; `M`/`L`/`EE_R` copiados por esa misma nota desde
`CALC-C0D-MARCADOR-v3`, sellado y no re-corrido), y con control positivo: el
mismo código sobre el mismo insumo devuelve, para las 10 celdas,
`0.9229 · 4.3073 · 11.9400 · 21.3226` — idénticas al cuarto decimal a las
selladas. Sobre las **9 celdas comunes**: `B = 0.6750`, `M = 4.2232`,
`L_SOLO = 11.9400`, `L_CORPUS = 16.8715`, todas `n=9`.

Declarado tres veces, en el informe, en el anexo y aquí: **esto no es el sello
de D-A.** Cuando D-A selle, `§A.3` queda `VENCIDA EN ALCANCE` y se **re-sella
contra el universo nuevo, nunca editando la tabla actual** (`A.10`, corolario 1).
Fila `NC-0218`.

## 3 · El hueco del índice, cobrado

El encargo lo anticipaba («si no lo cubre, ese hueco es entregable») y era real:

```
$ grep -c "documento del programa\|informe del programa\|lector externo" data/INFRAESTRUCTURA-v1_0.md
0
```

(universo `A.13`: 1 archivo, 866 líneas). Las únicas rutas `canon/` que el índice
gobernaba eran `gobernanza`, `estado-programa` y `modelo-decision`. La fila nueva
dice dónde vive esta clase de documento, que son **dos** archivos y no uno (cuerpo
para leer de corrido, anexo para rederivar), que **carga el módulo de auditoría de
rigor extremo**, y —lo que evita el defecto de la próxima vez— qué **no** es: no es
una nota de `forense/notas/` (eso es lo que hizo *un acto*), no es
`estado-programa` (la fuente única de estado y sus contadores mecánicos) y no es
`gobernanza` (el registro de decisiones). **Un informe no entra a la cascada de
ADR por existir y no mueve ningún contador.**

## 4 · Contadores

| contador | antes | después | por qué |
|---|---:|---:|---|
| `N_corridas_selladas` | 72 | 72 | este acto no sella corridas |
| `N_resultados_gen2_sellados` | 3 255 | 3 255 | no emite RESULT |
| `N_resultados_gen2_adoptados_activos` | 18 | 18 | cero adopciones (16→18 lo movió `PR #788`, no este acto) |
| `dependencias_numericas_legacy_activas` | 189 | 189 | no toca `milpa/` (191→189 lo movió `PR #788`) |
| `no_corrido_abiertas` | 67 | 68 | `NC-0152` CERRADA · `NC-0218`/`NC-0219` nuevas |
| ADR | 514 | 515 | `ADR-515`, renumerado de `ADR-514` al integrar `main` |
| FP abiertas | 1 | 1 | `FP-374` intocada |

**Re-derivado, no heredado.** Las cifras de «antes» son las de
`origin/main = eba9fd2`, no las de la base original `5973f12`: al integrar
`main`, `PR #788` (`ACTO GEN2-RELEVO-USOS-1`) había movido `adoptados` 16→18 y
`legacy` 191→189 —la primera bajada de ese contador en el programa— y se tomó
`NC-0211`..`NC-0217` y el `ADR-514`. Este acto renumeró lo suyo (`ADR-515`,
`NC-0218`/`NC-0219`), re-corrió `corrida0 status` en vez de heredar números, y
volvió a comprobar que **ninguna cifra del duelo cambia**: los tres insumos
sellados de §A.2–§A.4 están intactos entre las dos bases y el comando de §A.2
reproduce su salida al dígito sobre el árbol fusionado.

**Contadores de medición movidos: cero.** Dicho en una línea, sin justificarlo,
al inicio del módulo de auditoría del propio informe — que es donde la pregunta
[NUEVO v2.3] manda decirlo.

## 5 · `NC-0152`, cerrada porque `D5` lo dice y `#764` lo sostiene

`D5`, verbatim: «NC-0152 CERRADA citando #764». Antes de escribirlo se verificó
que `#764` es el merge de `acto/gen2-f5-documental-run-2` (`ce16af3`) — el acto
que produjo exactamente la cobertura residual que la fila pedía: `DIN-M-01` 8/8
puntos válidos y trazables (15.5581%, deriva `cr27`/`fac_3b`), `TRA-M-07` 8/8
(7.1815%, deriva `P8_3_1`/`FAC_P18`), cero sustituciones semánticas, contra 0/8
del control contemporáneo en ambas. El alcance del cierre se declara en la propia
fila: **la cobertura residual, no la generalización.**

## 6 · Perímetro, desviaciones y lo que no se tocó

**Desviación 1 — la rama.** El Bloque D pide una rama rotulada con el acto; el
arnés de esta sesión fija `claude/zealous-dirac-ee0r14` y prohíbe empujar a otra.
Se respetó el arnés y **el rótulo se censó igual** en `canon/registro-rotulos.tsv`,
que es donde la casa lo busca (D-6/`ADR-128`). Una línea, no una capa nueva de
gobernanza.

**Desviación 2 — `forense/no-corrido.tsv`.** El encargo dice «No toca registro»;
«el registro» en este programa es `data/corrida0/` y sus vistas derivadas, que
**no** se tocaron. `no-corrido.tsv` es parte de la cascada de cierre que el propio
Bloque D exige (paso 10), y además `D5` manda cerrar `NC-0152` ahí.

**Defecto propio, corregido en la misma sesión.** La primera corrida de
`tests/check.py --baseline` salió **ROJO con 2 entradas nuevas**: `T13` exige
bloque de cabecera `ARCHIVO`/`NOMBRE ESTABLE` (`ADR-36`) en todo archivo de
`canon/`, y los dos archivos nuevos no lo traían. Se añadió a ambos y la suite
volvió a **VERDE**. Se reporta en vez de omitirse: era defecto introducido por
este acto, no heredado.

**NO se tocó:** `data/corrida0/` ni ninguna vista del registro · `milpa/` ·
`forense/prereg-duelo-v2/` ni `forense/prereg-caja/` · ninguna spec, medidor,
sello ni corrida · `forense/firmas-pendientes.tsv` · `tools/` · `tests/` ·
`canon/modelo-decision-v4_0.md`.

## 7 · A.13 — qué se examinó, con qué comando

| negativo | comando | archivos examinados | resultado |
|---|---|---|---|
| el índice no cubre «documento del programa» | `grep -c "documento del programa\|informe del programa\|lector externo" data/INFRAESTRUCTURA-v1_0.md` | 1 (866 líneas) | `0` |
| `D-A` no existe | `git ls-remote --heads origin \| grep -icE "d-a\|informe"` · `ls forense/encargos/ \| grep -c "GEN2-D-A"` | 1 remoto · 336 encargos | `0` y `0` |
| la *LECTURA ESTRATÉGICA F5 v1.1* no está en el árbol | `grep -rl "LECTURA ESTRAT" canon/ forense/` | 2 174 | `0` — documento de mesa; `NC-0219` |

Positivos verificados: `tools/corrida0.py status` y `tools/tablero_programa.py --json`
corridos en este acto sobre 180 corridas · 4 913 resultados · 207 usos; el comando
del anexo `§A.2` se extrajo del propio markdown y se ejecutó para comprobar que
reproduce la salida que el anexo publica.

## 8 · Suite

```
$ python3 tests/check.py --baseline
  3 FAIL · 4022 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

## 9 · Qué decisión permite, y qué falta

**Permite:** que mesa entregue a un tercero un documento que no exige reconstruir
el aparato para entenderse, con cada cifra rederivable; y fija por escrito las
tres lecturas que estaban circulando sin candado — la primaria no se cita sin su
composición, la secundaria no se lee junto a la primaria, y B no se lee como
tesis.

**Falta:** el sello de `D-A` (`NC-0218`), los dos documentos de mesa
(`NC-0219`), y —el bloqueo real del programa, no de este acto— la **lista nominal
de 6 + 12 familias reservadas** que `D4` pide y sin la cual `FP-374` no se mueve
ni una línea.

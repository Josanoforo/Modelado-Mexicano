# ENCARGO · ACTO `GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3` · al cerrar, todo id que el código pueda emitir nulo está declarado, y el conducto que sella acepta la salida de cada rama —incluida la celda rara—, sin tocar una línea de código

> ENTORNO: **CAJA** — el hook imprime `ENTORNO-DERIVADO`; si no dice `CAJA`, PARA en una línea. Este acto no abre ENCIG 2025: la toca sólo por su `sha256` en el preflight.

**CABECERA** · SHA de redacción `origin/main = 346ab2bc` (descendiente de `6b898108`, el que verificó dirección); re-deriva al abrir; si main se movió no es PARO · **una sola sesión, rama propia nueva** · **Congela la sesión de `#944`.** Ejecuta los COMMIT-2/3 la sesión de `#951` u otra nueva. **Quien congela no ejecuta** · **MODELO: Opus** · **MODO: RÍGIDO** — reserva viva sobre ENCIG 2025 · **CONTADOR:** `NO-APLICA` en este acto; `cuenta_gen2 = SI` se hereda para los COMMIT-2/3 (§2) · **FP/ADR/NC:** ids de raíz de acto, derivados al cierre · **Reemplaza** a los borradores `c1608141…` y `53395878…`, que quedan retirados.

---

## 1 · OBJETIVO

Que el COMMIT-2/3 del piloto 3 **selle**, sin que ningún camino del código produzca una salida que `corrida0` rechace. `#951` probó que el medidor corre sobre el payload real de 2025 y que `corrida0` rechaza 40 nulos no declarados (`tools/corrida0.py:1950-1952`). La lectura del código muestra más ids que pueden salir nulos. Uno de esos caminos —una réplica del bootstrap que vacía una celda rara— ocurriría en el COMMIT-3, **después de derivar el cruce**: el peor sitio posible para un PARO.

**«Hecho» significa**, con salida cruda pegada:
- **Declaraciones:** en cada `spec.yaml`, `permite_no_estimable: true` en **todo id que el código pueda emitir nulo por lectura estática**, con la línea de código citada en su `unidad`. Esperado: **292 en EMISIONES y 174 en ADJUDICACION** (§3).
- **Ensayo:** `corrida0._valida_outputs` devuelve **cero problemas** en cada camino de §5 P3, incluida la celda rara, sobre sintético y sobre oro 2023.
- **Guardarraíl:** ningún camino produce un valor **no finito** (NaN o ±inf) en lugar de un nulo.
- **Preflight:** EMISIONES en `VERDE`; ADJUDICACION `BLOQUEADO` sólo por las cuatro entradas `emisiones_*`.
- **Intactos:** los dos `.py`, la spec humana y su sidecar, **byte a byte iguales a `826bf3a1`**.

---

## 2 · FIRMA DE MESA — verbatim; cierra `FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01`; el lanzamiento de mesa es el sello

> «El v1.3 cambia solo declaraciones de los dos `spec.yaml`; `medidor.py`, `adjudicacion.py`, la spec humana y su sidecar no cambian. Los 8 controles 60-96 se declaran anulables y se recuperan al cierre como aritmética entre sellados. "Congelado" exige que `_valida_outputs` acepte la salida de cada rama terminal, incluida la celda rara, sobre sintético y sobre oro 2023, y que todo id anulable por código esté declarado. Re-correr EMISIONES es legítimo: procedimiento y semilla intactos, nadie vio cifras. `cuenta_gen2 = SI`, sea cual sea el veredicto, se hereda.»

**Quién hace qué** (dirección, 21/sep): congela la sesión de `#944`; ejecuta la sesión de `#951` (caja montada, P0 hecho) u otra nueva; quien congela no ejecuta.

**Heredadas:** `FP-389`, `FP-393`, `FP-399`, `FP-400`, `FP-407`, FIRMADAS; texto en `forense/firmas-pendientes.tsv`.

---

## 3 · LO QUE SE SABE — cada línea con su rótulo

- `[LEÍDO]` Nota de `#951`, líneas 59-69: `corrida0` rechazó **40** ids en la corrida real de EMISIONES: 32 `…-C1A-P-IC-{LO,HI}` y 8 `…-60-96-{ESC}-{CONTROL-C2COMP-P, C2-VS-CONTROL-ABS}`. Nada más salió nulo sobre el dato real.
- `[LEÍDO]` **El control 60-96 es el mismo universo que el de la casa; sólo cambia el rótulo.** `tools/ejes_maestra35_l1.py:60` define «60+» como 60 ≤ edad ≤ 96, y `CALC-C2-COMPUESTO-RESERVADAS-0001` lo sella como `…-60-X-…`, mientras `medidor.py:355` lo busca como `…-60-96-X-…`. Por eso los 8 se declaran anulables y **se recuperan al cierre del COMMIT-3 como aritmética entre dos sellados** (§5 P4).
- `[LEÍDO]` **La causa de fondo de los nulos por bootstrap.** `medidor.py:287-291`: `resumen()` devuelve `None, None, None` si **una sola** réplica es inválida. `medidor.py:283`: una réplica es inválida cuando la celda queda vacía en ese remuestreo. ADJUDICACION usa la misma función (`adjudicacion.py:116`, `:233`).
- `[EJECUTADO]` **Lectura estática, contada contra los ids de cada `spec.yaml`.**

  **EMISIONES** (565 ids; total anulables: **292**):
  | origen en `medidor.py` | ids |
  |---|---|
  | marginal `-P` (`:389`) | 9 |
  | marginal `-P-EE/IC-LO/IC-HI` (`:387` → `:291`) | 27 |
  | candidato C2/S-MEDIO/S-LAMBDA `-P` (`:410`) | 48 |
  | candidato `-P-EE/IC-LO/IC-HI` (`:409` → `:291`) | 144 |
  | C1A `-P-IC-LO/HI` (`:416`) | 32 |
  | control y `\|C2−control\|` (`:423-425`) | 32 |

  **ADJUDICACION** (349 ids; total anulables: **174**, coincide con la cuenta de dirección):
  | origen en `adjudicacion.py` | ids |
  |---|---|
  | `-R-P` (`:202`) | 16 |
  | `-R-P-EE/IC-LO/IC-HI` (`:200` ← `:116` → `M:291`) | 48 |
  | `-DELTA-25` (`:204`) | 16 |
  | `-{cand}-D-PP` (`:208`) | 80 |
  | MAE y ΔMAE de retadores y C2 (`:233-241`) | 11 |
  | MAE de C1A y C1B (`:243-245`) | 2 |
  | `-UMBRAL-VENCER-N` (`:219`) | 1 |

  **En EMISIONES la lectura estática da 252 ids más que los 40 que ya fallaron.** Dirección no los listó; se declaran por su misma regla («todo id anulable por código»), y **así se le dice**.
- `[EJECUTADO]` **Ensayo en seco de dirección PRODUCTO-DINERO** (worktree temporal sobre `ba5fafe5` y `346ab2bc`, descartado; sin ENCIG 2025; el mismo `_valida_outputs` que sella; recetas adjuntas: `ensayo-sellabilidad-piloto3.py` y `ensayo-rama5-celda-rara.py`):
  - **Cuatro ramas de soporte** de ADJUDICACION (15, 13-14, global con 10 y 4 puntuadas, 0 puntuadas): nulos sólo en la rama de 0 puntuadas, **14 ids**, todos dentro de los 174.
  - **Celda rara** (18-29 × hasta primaria concentrada en 3 UPM; n 2025 = 37): de 2 000 réplicas, **87 la vacían** → ADJUDICACION emite nulos en `-R-P-EE`, `-R-P-IC-LO` y `-R-P-IC-HI` de esa celda, **3 ids**, dentro de los 174. **Cero valores no finitos en todas las corridas.** La inferencia de dirección se confirma: la rama es alcanzable.
  - **Matiz sobre la probabilidad:** en las olas selladas, esa misma celda (n = 70 en 2023, n = 110 en 2021) tuvo **10 000 de 10 000 réplicas válidas** con el diseño real. En 2025 es posible, no probable. Se declara igual: el sello no puede depender de que el dato sea amable.
- `[EJECUTADO]` El ensayo no corrió oro 2023 (sin corpus). **La sesión lo corre.**
- `[LEÍDO]` Nota de `#951`, línea 17: el test sintético construye el fixture del control con la clave del propio medidor (circular), y nadie llamaba a `_valida_outputs`.
- `[LEÍDO]` `adjudicacion.py:210-211`: si el IC de R de una celda `PUNTUADA` sale nulo, esa celda se trata como `NO-PUNTUADA` para los retadores. **Es comportamiento congelado, no se toca.** Si ocurre en el COMMIT-3, el veredicto lo dice (§10).

---

## 4 · YA HECHO / YA DECIDIDO

`#926` (v1.1: código y oro) · `#944` (v1.2: cableado, secuencia 2/3a/3, filas de contador) · `#951` (PARO: 40 nulos; la ola quedó intacta) · dirección, 21/sep: la enmienda y la firma de §2. **Ningún acto ha declarado `permite_no_estimable` en estos CALC ni ha corrido `_valida_outputs` sobre su salida.** Repite la búsqueda por objeto con tu acceso.

---

## 5 · PIEZAS

**P1 · Las declaraciones, en los dos `spec.yaml`, con edición quirúrgica.** A cada id de §3, `permite_no_estimable: true`, y en su `unidad` la causa con la línea de código:
- «nulo si una réplica vacía la celda (`medidor.py:283,291`)»;
- «IC NO-DERIVABLE: sin réplicas selladas de 2023 (`medidor.py:416`)»;
- «control con rótulo `-60-X-` en la casa (`tools/ejes_maestra35_l1.py:60`), mismo universo; se recupera al cierre como aritmética entre sellados»;
- «nulo si no hay celdas puntuadas (`adjudicacion.py:239-245`)»;
- y así con cada origen.

No se reserializa el archivo; el diff muestra sólo esas llaves. **Deriva tú la lista**: si tu lectura encuentra otro sitio que emite `None` y aquí no está, lo declaras y lo dices. Si tu cuenta difiere de 292 / 174, gana la tuya y se declara la diferencia.

**P2 · La ejecución previa, declarada.** En el `spec.yaml` de EMISIONES, y sólo ahí: la ejecución de `#951` —fecha, duración, 565 RESULT producidos, 40 nulos, descartados por `corrida0` antes de escribirlos y no vistos—. Por la firma, re-correr es legítimo; asentarlo evita que el COMMIT-2 la confunda con un primer resultado (E.5).

**P3 · El ensayo, con el validador que sella.** Pasa por `_valida_outputs` —contra el `spec.yaml` ya declarado— la salida de cada camino:
1. EMISIONES sobre sintético;
2. EMISIONES sobre oro 2023;
3. ADJUDICACION, todas las celdas con soporte;
4. ADJUDICACION, soporte parcial;
5. ADJUDICACION, `FUERA-DE-SOPORTE` global con celdas puntuadas;
6. ADJUDICACION, cero celdas puntuadas;
7. **ADJUDICACION, celda rara**: pocos trámites en 2 o 3 UPM, con réplicas suficientes para que alguna la vacíe. Verifica que `-R-B-VALIDAS` < réplicas; si no, la rama no se ejercitó.

Si el código admite la adjudicación con la ola 2023 como R, se valida también; si no la admite, se declara y bastan los sintéticos. Los fixtures del control C2 se construyen **desde los ids reales** del `resultados.json` sellado, no desde la clave del medidor. **Esperado: cero problemas en los siete, y cero valores no finitos.** Escribe esa expectativa en la nota antes de correr.

**P4 · La recuperación del control, escrita en la secuencia.** En el bloque `secuencia_commits` del `spec.yaml` de ADJUDICACION —el único sitio donde vive la secuencia— se añade al `commit_3`: al cierre, las **cuatro restas** |C2 del piloto − control `-60-X-` de la casa| para las cuatro celdas 60-96, entre dos números sellados, rotuladas como **aritmética derivada**, no como RESULT de corrida.

**P5 · La prueba que se queda.** En `tests/test_piloto3_v11.py` o en un test hermano —lo que menos toque—, los siete caminos de P3 con su aserción de `_valida_outputs` vacía y cero no finitos. Así el ensayo deja de ser una receta de una sesión.

**P6 · Preflight e intactos.** Preflight de los dos CALC, con la salida esperada escrita antes de correrlo. `sha256sum` de los `.py`, la spec humana y su sidecar contra `826bf3a1`.

---

## 6 · LATITUD — carril libre

**Decides tú, y lo dices en la nota:** cómo construyes el sintético de la celda rara · el orden de los caminos del ensayo · si P5 vive en el test existente o en uno hermano · instalar `pytest` · un defecto adyacente de ≤ 10 líneas **fuera** de los dos CALC, declarándolo. Y si encuentras otro sitio que emite `None` y no está listado: lo declaras y lo dices.

**No decides:** nada de §7.

---

## 7 · PAROS — lista cerrada

- **(a)** Abrir, leer o derivar cualquier miembro de ENCIG 2025 más allá del `sha256` del preflight. **Correr el medidor sobre 2025 es abrirla.**
- **(b)** Tocar una línea de `medidor.py`, `adjudicacion.py`, la spec humana o su sidecar; o descubrir que algo sólo se arregla tocándolos.
- **(c)** **Un camino del ensayo produce un valor no finito en lugar de un nulo.** Eso ya no se arregla declarando: PARA y reporta el id, el camino y el valor.
- **(d)** Correr `corrida0 run`, o mover un contador.
- **(e)** Cambiar en un `spec.yaml` algo fuera de las llaves de P1 y los bloques de P2 y P4: parámetros, semilla, λ, tolerancias, rejilla, guardias, la lista `PUNTUADA` o B-bis.
- **(f)** `ENTORNO-DERIVADO ≠ CAJA`, o F3 violada.
- **(g)** Con P1 hecho, `_valida_outputs` sigue devolviendo problemas en algún camino.
- **(h)** El objetivo dejó de ser alcanzable, y eso es el entregable.

---

## 8 · COMPUERTAS

**«`_valida_outputs` vacía y cero no finitos en los siete caminos de P3, más el preflight con la salida esperada, pegados» protege: congelar spec.** Sin eso el v1.3 no se declara congelado y el COMMIT-2 no se lanza.

---

## 9 · PERÍMETRO

**Propio:** los dos `spec.yaml` (llaves de P1, bloques de P2 y P4) · el test de P5 · la fila de `FP-…-a6f5-01`, que pasa a `FIRMADA` con el PR de este acto · las NC `…-a6f5-*` que apuntan al v1.3 · la línea de la celda-D que cita la spec congelada · nota · el encargo archivado con su `.cuerpo.sha256` · la cascada de `/acto`.

**Ajeno:** los `.py`, la spec humana y su sidecar · `tools/` · `decisiones.tsv` · `fp399-firmada-826bf3a1.tsv` · el `resultados.json` de C2-COMPUESTO-RESERVADAS —se lee, no se edita— · ENCIG 2025 · D-22 ampliada como regla general —la escribe dirección como semilla de v2.16—.

**Perímetro de cierre (D-21):** `## NO-CORRIDO / RESERVAS` con «Ninguno.» si no hay, antes de `## CONSUMIDO`, añadidos al final; el cuerpo no se re-sella.

**«Si te encuentras escribiendo fuera de esta lista, PARA.»**

---

## 10 · LO QUE NO HACE · SUCESORES · CIERRE

**No hace:** no corre el piloto · no abre 2025 · no cambia ningún número —el permiso de nulo no altera ningún valor— · no escribe D-22 general.

**Sucesores:**
1. **COMMIT-2 / 3a / 3 del v1.3**, en la sesión de `#951` u otra nueva. Su encargo es el de `#951` (`50d4b0ef…`) con cuatro cambios: base v1.3; P0 añade «P5 del v1.3 en verde»; P1 reporta la ejecución previa ya declarada; **el cierre incluye las cuatro restas del control 60-96 como aritmética derivada, y lista cada nulo emitido por familia de id**. Si alguna celda `PUNTUADA` pierde su IC de R y pasa a `NO-PUNTUADA` (`adjudicacion.py:210-211`), el veredicto lo dice.
2. **D-22 ampliada**, que escribe dirección como semilla de v2.16, con la frase de la firma.
3. **El piloto de ahorro de PRODUCTO-DINERO**: no se congela sin este ensayo completo desde su COMMIT-1.

**Cierre:** cascada de `/acto` · primera línea de la nota: cuántos ids declaró por spec y por origen, y cuántos caminos pasan `_valida_outputs`.

---

**Falsador, a tres meses:** si el COMMIT-2/3 para en `corrida0` por un id que la lectura estática no listó, la lectura no fue completa, y D-22 ampliada tiene que exigir enumeración por herramienta, no a mano.

---

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3-5870-01` · P5 -- «La prueba que se queda»: los siete caminos con su asercion, en CI: tests/test_piloto3_v13_conducto.py existe, pasa en CAJA (7 passed, ocho caminos) y esta censado, pero en CI se salta en voz alta: NECESITA-DEPENDENCIA(pytest) -- el runner no instala numpy/pandas/pytest (misma fila que tests/test_piloto3_v11.py) | DECISIÓN-DE-MESA-PENDIENTE: FP-398 FIRMADA opcion (a) (instalar librerias en CI) con ejecucion en manos de mesa; este acto no toca requirements.txt ni verify.yml (fuera de perimetro §9: tools/ y CI ajenos) | la guardia del conducto solo protege al COMMIT-2/3 si quien lo ejecuta la corre en CAJA (P0 del sucesor la exige); ningun contador | ejecucion de FP-398 (a) por mesa; hasta entonces, P0 del COMMIT-2/3a/3 del v1.3 corre pytest tests/test_piloto3_v13_conducto.py en CAJA |
| `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3-5870-02` · §1 «Guardarrail: ningun camino produce un valor no finito» -- lectura estatica mas alla de los ocho caminos: adjudicacion.py:185-189,207 emite -{C2,S-MEDIO,S-LAMBDA}-P sin guardia de finitud: NaN si una marginal de UNA variable entera queda sin masa en 2025. Inalcanzable en los ocho caminos y en el dato real (miles de tramites por marginal en 2023); cero no finitos medidos. No es PARO (c) ni se arregla declarando (PARO b: no se toca codigo) | DIFERIDO-A:D-22 ampliada (direccion, semilla v2.16): la enumeracion por herramienta debe cubrir NaN ademas de None; reserva escrita en la nota §3 | ninguno hoy; si ocurriera en el COMMIT-3, corrida0 pararia con valor_no_finito y el sucesor lo reporta | D-22 ampliada (direccion); COMMIT-2/3a/3 del v1.3 lo vigila con la asercion de finitud del test |
| `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3-5870-03` · Cabecera: «Congela la sesion de #944»: congelo una sesion NUEVA (165ce648), no la de #944: el operador lanzo el encargo en esta sesion. F3 se cumple igual (no corrio el medidor sobre 2025, no abrio la ola, no leyo disenos A/B ni careo; quien congela no ejecuta). Premisa logistica, objetivo alcanzable: se siguio y se declara | DECISIÓN-DE-MESA-PENDIENTE: si mesa exigia literalmente la sesion de #944, que lo diga al fusionar; la salida no depende de que sesion tecleo | ninguno | MESA -- al fusionar el PR de este acto |

Corrido entero: P1 (292 + 174 declaraciones), P2, P3 (ocho caminos, incluida la adjudicación con oro 2023 como R), P4, P5 (en CAJA), P6. `## CONSUMIDO` se añade en el commit siguiente con el número real del PR.

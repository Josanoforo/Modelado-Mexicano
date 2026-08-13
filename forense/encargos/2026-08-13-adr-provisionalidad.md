# ENCARGO ADR-PROVISIONALIDAD · sellar la declaración y abrir el registro de recálculo

- **SHA de redacción**: `b17a6f6` (merge #195), derivado por `git log -1` contra clon fresco, 13/ago/2026.
- **Entorno asignado**: **NUBE.** Repo-only, sin red a dominios de datos, sin microdato, sin corpus. Firma `cloud_default` sin sonda es correcta (ADR-59(b)). **NO lo lances en la caja** — la caja tiene tres actos y este no la necesita.
- **Estado**: `CONSUMIDO` — ejecutado en la rama `claude/new-session-ls8v9e`, commits `e087e12` (este archivo) · `162789a` (COMMIT 1: sella ADR-72, abre `forense/registro-recalculo-v1_0.md`) · el commit de COMMIT 2 que sigue a este mismo cambio (enmienda de ADDENDA 5, nota de cierre, hallazgos, y este archivo). PR aún no abierto en esta sesión — ningún acto de esta convención exige que lo esté para marcar `CONSUMIDO`; el registro es el commit, no el PR. Detalle completo: `forense/notas/2026-08-13-adr-provisionalidad-cierre.md` (nombre distinto de este archivo a propósito — mismo slug habría colisionado con T02, nombre normalizado, entre `forense/notas/` y `forense/encargos/`; hallazgo encontrado y corregido en el propio COMMIT 2, ver esa nota §8).
- **Naturaleza**: acto de sellado. **La decisión ya está tomada por mesa.** El ejecutor propaga y deriva; **no decide, no reescribe el texto sellado, y no amplía el alcance.**

Archivado per `forense/encargos/convencion.md` (A.3) como **primer commit**, antes del ARRANQUE.

---

## §1 · PERÍMETRO Y CONCURRENCIA

**ESCRIBE:** `canon/gobernanza-v1_15.md` (§4: la entrada del ADR nuevo · §0.1: cabecera de conteo) · `canon/estado-programa-v1_10.md` (contador de ADR + las cifras de suite) · `forense/registro-recalculo-v1_0.md` (**archivo nuevo**, append-only) · `forense/notas/2026-08-13-adr-provisionalidad.md` (1 nota) · `forense/hallazgos.md` (append, **merge local siempre**) · `forense/encargos/2026-08-13-adr-provisionalidad.md` (este archivo, A.3).

**NO ESCRIBE:** `canon/modelo-decision-v4_0.md` (**este ADR no toca reglas ni tiers**) · `milpa/**` · `forense/hitoD-preregistro-v2_0.md` (**no adjudica ningún veredicto**) · `forense/censo-estimabilidad-*.md` (es la entrada 1 del registro, acto aparte) · `forense/registro-llaves-identificacion-v1_0.md` · `data/**` · `tools/**` · `tests/**`.

**Si te encuentras escribiendo fuera de la primera lista, PARA.**

**En paralelo:** APERTURA-ISSP · ENLACE-1 · SONDA-1 · CENSO-v1.1. **Ninguno toca `canon/`.** El único punto de contacto es `hallazgos.md` (`merge=union`). **GitHub no honra `merge=union`**: aparecerá como conflicto en la interfaz y auto-resuelve limpio en local. **El editor web de conflictos está prohibido** — es donde se borra la entrada ajena.

---

════════ ARRANQUE ════════

**1 · REPO.** Clon existente; si no hay, clona y dilo. Ruta absoluta · `git log -1 --format="%h %s"` · `git status`. No arranques desde el home.

**2 · SHA.** Base `b17a6f6`. Cuatro actos corriendo pueden haberlo movido — **especialmente si alguno selló un ADR.** Refresca. **NO es PARO**, pero re-deriva §2.1 antes de escribir el número.

**3 · `data/raw`.** No aplica: este acto no toca dato. Decláralo y salta.

**4 · ENTORNO.** Nube, `cloud_default`, sin sonda (ADR-59(b)). Decláralo.

**5 · ESPEJO.** Ninguna cifra del espejo. Todo del clon de (1), con el comando a la vista.

**PREMISAS (script — repórtalas crudas):**

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu | wc -l   # ADR únicos
grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu | tail -1  # el máximo
ls forense/registro-recalculo-v1_0.md 2>/dev/null && echo "YA EXISTE - PARA"
python3 tests/check.py | tail -3                                                              # la cifra REAL de suite
```

**Si `registro-recalculo-v1_0.md` ya existe: PARA y repórtalo — otro acto se adelantó.**

════════════════════════════════════════

---

## §2 · COMMIT 1 — la numeración y la trampa de la cifra de suite, derivadas antes de escribir

### 2.1 · El número del ADR se deriva, no se fija

**Contra el `main` real del momento**, no contra este encargo. En esta redacción: **71 únicos, máximo 71** → el siguiente sería **72**. **Verifícalo tú.** T15 falla sobre **huecos**, no solo sobre el máximo: si otro acto selló 72 mientras tanto, este va a 73 y **no** deja el 72 vacío.

*(ADR-70/71 se renumeraron tres veces por fijar el número antes de fusionar. La historia completa está en `gobernanza:938`. No la repitas.)*

### 2.2 · La cifra de suite tiene punto fijo, y hay que resolverlo antes de teclear nada

**Estado medido en esta redacción:**

- Corrida real: **22 FAIL · 104 WARN**, `--baseline` **VERDE** contra `e7cd99d`.
- **T16 (self-check) aporta 4 de esos 22 FAIL**, y son exactamente estos:
  ```
  canon/estado-programa-v1_10.md:130  declara 101 WARN  ·  real 104
  canon/estado-programa-v1_10.md:222  declara 18 FAIL · 101 WARN  ·  real 18 FAIL · 104 WARN
  canon/gobernanza-v1_15.md:760       declara 18 FAIL ·  95 WARN  ·  real 18 FAIL · 104 WARN
  canon/gobernanza-v1_15.md:852       declara 18 FAIL ·  95 WARN  ·  real 18 FAIL · 104 WARN
  ```
- Los otros 18: T09=8 · T05=5 · T06=2 · T07=1 · T08=1 · T11=1. **8+5+2+1+1+1 = 18.**

**La trampa:** si escribes `22 FAIL` en el canon, los 4 FAIL de T16 desaparecen (el canon ya coincide), la corrida real baja a 18, y **el canon vuelve a estar mal — ahora por exceso.**

**El punto fijo es `18 FAIL · 104 WARN`.** Escríbelo y T16 pasa, dejando exactamente 18 FAIL · 104 WARN. **Deriva esto tú corriendo la suite antes y después; no confíes en esta aritmética.**

**Y la consecuencia sobre el baseline, que hay que reportar y no resolver solo:** al corregirlo, la suite pasa de 22 FAIL a 18 FAIL. `--baseline` marca **fallos nuevos**, no fallos que desaparecen, así que debería seguir VERDE. **Si el baseline exige regeneración, PARA y repórtalo** — regenerar un baseline congelado es decisión de mesa, no de este acto.

### 2.3 · El texto del ADR, VERBATIM — se pega tal cual, sin reescribir

> ---
>
> **ADR-`<N derivado>` · Provisionalidad declarada del cuerpo de cálculo previo, y apertura del registro de recálculo.** Decisión de mesa del autor, 13/ago/2026.
>
> **Se declara `PROVISIONAL` todo veredicto, coeficiente, contador, reparto y cierre de búsqueda producido por este programa antes del 13/ago/2026.** Provisional **no** significa retirado ni falso: significa que se derivó contra un universo de corpus que no era el universo real, y que ninguno declaró ese universo. Siguen siendo el estado operativo del programa hasta que se recalculen. Lo que cambia es una sola cosa: **ninguna decisión nueva puede citarlos como asentados.**
>
> **Fundamento, con receta.** Se había abierto a nivel variable el **0.090%** del universo declarado (32 filas en `data/abrir4-variables-2026-08-08.tsv` + `data/verif3-variables-2026-08-08.tsv`, los dos únicos archivos de apertura del repo, contra 35,708 activos T0), cubriendo **8 de 550 payloads del manifiesto (1.45%)**. El corpus lo declaraba en su propio campo `usado_para`: **282 de 550 payloads (51%) dicen literalmente `"sin uso asignado"`**, y **321 de 550 (58%) no son alcanzables desde ningún `fuente_canonica_normalizada` de `relaciones.tsv`**. Ningún contador del programa apuntaba ahí: todos —`capa2 SI`, Hito D, condicionales, producciones, llaves— miden producto río abajo; ninguno medía explotación.
>
> **Caso testigo, verificado.** `forense/censo-estimabilidad-coeficientes-v1_0.md` §5 declara por escrito que `PR #107` (ENASEM 2018/2021/2024, seis payloads) se fusionó **2 min 28 s** después de su commit y *"no fue cruzado aquí"*, que ENASEM *"tiene la forma de una llave de identificación... sin haberse cruzado contra ninguno de los 15 coeficientes"*, y que su reparto *"se lee vigente al SHA `8cdabcb`, no como estado del programa"*. El contador `llaves de identificación ejercidas: 0 de 2` toma su **denominador** de ese censo. **El 2 es provisional.** El `v1.1` que lo revisaría se nombró el 4/ago y no corrió.
>
> **Precedente que agrava, no que atenúa.** `forense/encargos/2026-08-07-abrir-4.md` §0 ya había nombrado este defecto el 7/ago: *"ambas sobre un régimen de cinco instrumentos... Mientras tanto, esto estaba en el disco propio, hasheado, íntegro y registrado en el manifiesto desde antes de esos cierres."* Ese acto abrió los cuatro instrumentos que tenía delante. **Nadie preguntó cuántos más estaban en la misma condición. Había 546.**
>
> **Alcance, por clase.** **(A)** Contadores con denominador o universo provisional: `llaves 0 de 2` · el reparto `RUTA-A=3 / RUTA-I=1 / RUTA-C=2 / SIN-RUTA=9` de los 15 coeficientes · `condicionales 9 de 14` · `capa2 SI 24 de 197`. **(B)** Los **7 de 13** veredictos del Hito D archivados con letra `D` —`R1.1`, `R4.1`, `R4.2`, `R4.3`, `R7.2`, `R9.1`, `R9.2`— por ser archivo por hueco de diseño o muestra insuficiente, la clase que un corpus mayor puede mover; los otros 6 (`A`×2, `B`×2, `E`×2) **no** entran automáticamente. **(C)** Los cierres de búsqueda con universo declarado: **ADR-52 A** (`aversion_riesgo`) y **ADR-54** (`sens_estatus`), ambos sobre el mismo régimen de cinco instrumentos. **(D)** Las decisiones de motor apoyadas en ese censo: **ADR-50**, **ADR-51**, **ADR-57(c)**.
>
> **Fuera de alcance, declarado:** los reports temáticos de `corpus/reports/` y el integrador. Son síntesis de literatura, no cálculo sobre corpus propio; su clase de defecto es otra y ya tiene su módulo de auditoría. Mezclarlos aquí reproduciría la jornada del 30/jul/2026.
>
> **Criterio de salida.** Una entrada deja de ser provisional cuando un acto la re-examina contra el universo declarado completo y **escribe ese universo en la misma línea** (A.4). Tres desenlaces, los tres cierre válido: `RECALCULADO — SIN CAMBIO` (se sostiene, ahora con universo declarado) · `RECALCULADO — CAMBIA` (se propaga con su ADR) · `RECALCULADO — INDECIDIBLE` (y se dice qué haría falta). **No es cierre** *"se revisó y parece bien"* sin universo escrito: eso es lo que produjo esta situación.
>
> **Método.** Un acto por entrada; **el canon no se abre en bloque.** Rige la Regla de señal: **cada acto de recálculo produce un veredicto de los tres, o produce nada.** Un acto que vuelve con *"sigue pendiente"* no cierra su entrada. La cola vive en `forense/registro-recalculo-v1_0.md`, append-only, y su orden es por palanca, no por número de ADR.
>
> **Contador instituido, uno solo.** `payloads con apertura registrada / payloads en manifiesto` — hoy **8 de 550 = 1.45%**. Se deriva cruzando los `id_manifiesto` de los TSV de apertura a nivel variable contra las entradas con `archivo`+`sha256` del manifiesto. **Justificación bajo el impuesto de v2.3:** el defecto que atrapa ya ocurrió y su costo está medido — cálculos incompletos y decisiones de gobierno por reabrir, el defecto más caro que el programa ha registrado. Un contador derivable con dos `grep` lo paga; un módulo de auditoría no, y por eso este ADR instituye un número y **ninguna compuerta nueva**.
>
> **Lo que este ADR NO hace.** No retira ningún resultado. No audita el canon en bloque. No toca reports temáticos ni integrador. No añade preguntas al módulo de auditoría de rigor extremo. No promete que algo cambie: es igual de probable que la mayoría de las entradas cierren en `RECALCULADO — SIN CAMBIO`, **y eso también es el resultado** — ahora con universo declarado, que es lo que hoy no existe.
>
> **Cascada:** cabecera de conteo de ADR en `gobernanza-v1_15.md` · contador de ADR en `estado-programa-v1_10.md` · las cifras `N FAIL · M WARN` de ambos, **recalculadas por corrida real** · `forense/registro-recalculo-v1_0.md` (nuevo) · una línea en `forense/hallazgos.md`. **Ningún contador de medición sobre México se mueve con este ADR.**
>
> ---

### 2.4 · El registro, con sus cinco entradas iniciales

`forense/registro-recalculo-v1_0.md`, **append-only**, con cabecera de versión ADR-36 y esta tabla:

| # | entrada | clase | por qué va aquí | gate | estado |
|---|---|---|---|---|---|
| 1 | **Censo v1.1** — cruce de ENASEM (3 olas, 6 payloads) contra los 15 coeficientes, y universo de llaves declarado en las 9 `SIN-RUTA` | A | única entrada que puede mover un **denominador**; la nombró el propio censo v1.0 | ninguno | `ABIERTA — encargo emitido 13/ago` |
| 2 | **ADR-52 A y ADR-54** — reapertura acotada de las dos búsquedas cerradas | C | gatean 4 `SIN-RUTA`; APERTURA-ISSP produce el reporte con el que se deciden | reporte de APERTURA-ISSP fusionado | `ABIERTA` |
| 3 | **Los 7 veredictos `D` del Hito D** — uno por acto, ficha B-bis propia | B | archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco | entradas 1 y 2 | `ABIERTA` |
| 4 | **Censo de explotación** — apertura por payload sobre los 550 | A | instituye el contador del ADR y evita la repetición | ninguno | `ABIERTA` |
| 5 | **ADR-50 / ADR-51 / ADR-57(c)** | D | dependen del reparto de la entrada 1 | entrada 1 | `ABIERTA` |

**Cada entrada cierra con:** el acto que la cerró (PR), el veredicto de los tres, y **el universo declarado en la misma línea.**

---

## §3 · COMMIT 2 — la propagación, con cada cifra derivada

`tests/check.py --baseline` al cierre. **T15** (conteo y contigüidad de ADR) y **T16** (self-check de la cifra de suite) son los dos que vigilan este acto. **Si un test truena, ese es el hallazgo — no se maquilla.**

Reporta en el PR, uno por uno: el número de ADR derivado y contra qué `main` · los sitios de cascada tocados con línea · la cifra de suite antes y después con las dos corridas pegadas · y **los contadores que NO se mueven, declarados**: `13 de 27` · `15 coeficientes, 0 medidos` · `9 de 14` · `llaves 0 de 2` · `capa2 SI 24 de 197`. **Ninguno se mueve con este ADR, y decirlo es parte del acto.**

---

## §4 · CONTADOR

**Cero contadores de medición sobre México.** Este acto sella una decisión de gobierno y abre una cola. Su producto es que las cinco entradas del registro existan como cola citable, y que ningún acto futuro pueda citar un resultado previo como asentado sin recalcularlo.

Y la línea honesta, que va en la nota: **este acto no mide nada.** Lo que hace es impedir que se siga midiendo sobre una base que el programa ya sabe incompleta.

---

## Addenda recibida durante ejecución (mismo día, antes de COMMIT 1)

Las dos addenda siguientes llegaron juntas, en un solo mensaje, a mitad de ARRANQUE — antes de que este acto escribiera ningún archivo. Se archivan **verbatim, íntegras**, aunque solo la ADDENDA 5 pertenece a este acto (regla de A.3: el texto completo tal como se recibió, no un resumen, y no una selección silenciosa de qué parte "aplica"). La ADDENDA 4 es de **SONDA-1**, un acto paralelo distinto — no se ejecuta aquí, se archiva por fidelidad de lo recibido.

> ADDENDA 4 · SONDA-1 — dos precisiones sobre dónde escribes
> No cambia tu alcance.
> (a) No confundas tus filas con las 62 que ya están. data/universo-puertas-2026-08-12.tsv tiene 99 filas, de las cuales 62 son de clase gap_mapeo_map_b y las 62 declaran el mismo universo, verbatim:
> "buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)"
> Su universo son dos tablas internas del programa, no un portal. Tus filas sí sondean portales. Si tu sonda supersede una de esas 62 para la misma fuente, dilo explícitamente en tu fila —qué fila vieja queda stale y por qué— en vez de dejar dos filas contradictorias con la misma fuente. Precedente vivo: ISSP tiene hoy dos filas, una gap_mapeo_map_b con NO-ENCONTRADO y otra GESIS_ISSP con EXISTE-SATISFACE. No añadas un tercer caso de eso.
> (b) La línea de P4 al cerrar. Tu acto llega a la tabla consolidada de puertas (estación 2) y no actualiza data/cola-adquisicion-2026-08-12.tsv (estación 3). Declara en una línea por qué no —el TSV de cola no se edita a mano, nunca; su vía es el motor— y deja la propuesta de reordenamiento del Lote 2 derivada de lo que encontraste, para que la firma de mesa no sea una apuesta. Ese es tu entregable de mayor rendimiento.
>
> ADDENDA 5 · ADR-PROVISIONALIDAD — un contador más y una evidencia más
> Si el texto del ADR ya está pegado en tu commit 1, esto entra como enmienda en el commit 2, declarada. No reescribas el commit 1.
> (a) El contador que el ADR instituye es insuficiente, medido. El texto declara "payloads con apertura registrada / payloads en manifiesto — hoy 8 de 550 = 1.45%". Ese contador habría atrapado el 0.09%, pero no habría atrapado el defecto de ABRIR-4: ese acto sí abrió, sí registró, y su hallazgo murió igual — porque murió entre dos tablas consolidadas, no antes de la primera.
> Añade un segundo contador, y el ADR queda con dos, no con uno:
> filas de consolidación en desacuerdo entre sí / filas cotejadas
> hoy, medido: 3 filas del censo de coeficientes (12·familismo_apoyo, 13·familismo_obligacion,
> 14·radio_confianza) dicen SIN-RUTA "Ninguna llave aplica" mientras relaciones.tsv dice
> capa4=EXISTE-SATISFACE para las mismas necesidades (N12, N13, N14).
> Cotejos automáticos existentes: grep -rln "censo-estimabilidad" tests/ tools/ → 0.
> Justificación bajo el impuesto de v2.3, que este contador también debe pagar: el defecto ya ocurrió, tiene fecha (censo 4/ago vs. relaciones.tsv 7/ago vs. ABRIR-4 8/ago), y su costo está medido — tres filas del plan de coeficientes clasificadas SIN-RUTA durante seis días teniendo reactivo con texto literal, tabla y N. Es derivable con un awk que cruza dos archivos. No es un módulo de auditoría.
> (b) Una evidencia más para el §2 del ADR, con receta:
> git log --oneline -- data/curacion-registro/relaciones.tsv devuelve un solo commit (16180e6, 7/ago/2026). grep -rln "censo-estimabilidad" tests/ tools/ devuelve 0. Las dos tablas consolidadas del programa —el registro de demanda y el censo de coeficientes— no se cotejan entre sí por ningún mecanismo, y hoy se contradicen en tres filas.
> (c) Una entrada más en el registro de recálculo, y va primera por barata:
> #	entrada	clase	por qué	gate	estado
> 0	Cotejo censo ↔ relaciones.tsv — las 15 filas del censo contra capa4 de las necesidades correspondientes	A	mide el desacuerdo entre consolidadas; hoy son ≥3 filas y nadie lo vigila; lo cierra el mismo acto del censo v1.1	ninguno	ABIERTA — la absorbe CENSO-v1.1
> Lo que esta addenda NO añade: ninguna compuerta al módulo de auditoría, ningún test obligatorio, ninguna regla nueva a instrucciones-proyecto. Dos números derivables y una entrada de cola.

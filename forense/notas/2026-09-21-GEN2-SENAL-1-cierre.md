# ACTO GEN2-SENAL-1 · nota de cierre

**2026-09-21 · entorno NUBE · Opus 5 · rama `claude/clever-dirac-9nb7d8`**

## 0 · Arranque (Bloque D)

- **REPO.** Clon existente en `/home/user/Modelado-Mexicano`. `git log -1` al abrir:
  `b8438d76` (merge de PR #926). Árbol limpio.
- **SHA.** El encargo declara `bd9ed213` (PR #923). **Main se movió**: `origin/main`
  = `b8438d76` = PR #926 (`GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1`). No es PARO (ARRANQUE 2):
  se refrescó y se re-derivó todo contra `b8438d76`. La rama de trabajo salió nivelada
  con `origin/main` (0/0).
- **ENTORNO (A.2, tres partes).** (1) `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`;
  (2) sonda `curl` a inegi (sin `-I`): `http=000`, **DENEGADA-POR-POLÍTICA**, `http_connect=403`;
  (3) corpus `data/raw` **AUSENTE — 0 archivos examinados** (A.13). El hook imprimió
  `ENTORNO-DERIVADO = NUBE`, que es el que el encargo asigna. **Este acto no abre microdato
  ni usa red**: todo se deriva del árbol, así que ninguna de las tres partes lo bloquea.
- **ESPEJO.** No se consultó. Ninguna cifra de esta nota viene de otro sitio que el clon.

## 1 · Premisas del encargo que NO se sostuvieron

Cinco. Ninguna tocaba **qué se mide** ni una firma de mesa, así que ninguna fue PARO (§2,
v2.15): se replanteó, se siguió y se declara. **Encontrarlas es entregable.**

1. **«Las cinco de `data/curacion-registro/celdas-d/`»** — son **seis**.
   `GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml` nació con PR #926, que fusionó
   después de redactarse el encargo. Fuera de P3 por diseño (`champion_actual: NINGUNO`).
2. **«Las dos con `requiere_decision_mesa: true`»** — sólo `DIN`. `TRA…:92` ya decía
   `false` antes de este acto y **no se tocó**.
3. **«Filas del marcador `ADOPTADO-POR-FIRMA` con `M` y `R`»** — **conjunto vacío**. Las 20
   filas de cruce traen `M` sellado y **`R` vacío**. El error por celda no está en el
   marcador: vive en el CALC del árbitro del cruce. P1 lo lee de ahí. La premisa «todo lo
   que P1 necesita ya está en esa tabla» es cierta para persistencia y falsa para cruces.
4. **«que las 6 celdas de formalidad ya tienen su error»** `[SUPUESTO]` — **confirmado como
   el encargo temía**: tienen `piso` y **no** tienen `error_piso_pp`. No se cuentan como
   validadas, y se dice. Su error es un CALC sucesor (y su firma es FP-396).
5. **«una parte ya tiene su sucesor fusionado»** `[SUPUESTO]` — **casi enteramente falsa**.
   Ver §3.

Una premisa `[REPORTADO]` sí se verificó y era cierta: `corrida0.py demanda` listaba estas
celdas entre las que «el registro no decide». Ya no lo hace (§4).

## 2 · P1 · `celdas_validadas`, primera línea del bloque derivado

`tools/tablero_programa.py`: `_celdas_validadas()` + `_linea_celdas_validadas()`, cableado
como **primera viñeta** del bloque `<!-- TABLERO-DERIVADO -->`. Se deriva del marcador y de
tres CALC sellados. **Cero cifras tecleadas.**

**Total hoy: 73** (cruce 20 + persistencia 53). El duelo nacional (12) **se reporta y no se
suma**: otro universo, otro estimando (§4.4).

| clase | n | error mediano | brecha |
|---|---|---|---|
| cruce vs R · `DIN…localidad_x_edad` | 8 | 0.936 pp (máx 4.375) | 0 (misma ola) |
| cruce vs R · `TRA…escolaridad_x_dominio` | 12 | 1.224 pp (máx 5.436) | 0 (misma ola) |
| persistencia · ENIF 2024 | 28 | 2.145 pp | **3 años** |
| persistencia · ENCIG 2025 | 10 | **11.826 pp** | **2 años** |
| persistencia · ENVIPE 2025 (`tmod_vic`) | 13 | 2.340 pp | **1 año** |
| persistencia · ENVIPE 2025 (`conjunto_de_datos`) | 2 | 2.767 pp | **1 año** |
| duelo de tres, nacional | 12 | M 4.987 / L-solo 3.957 / L-corpus 3.889 pp | `SIN-GANADOR-UNICO` |

Las brechas van **al lado de cada fila y no se promedian**, que es justo lo que el encargo
prohíbe. Sub-cifra del dominio dinero: cruce 8 (0.936 pp), persistencia 28 (2.145 pp).

### Dos defectos reales encontrados en el árbol, no hipótesis

**(a) La lectura natural del marcador da 89 y es falsa.** Las 89 filas con `M` y `R` son
`IDENTICO` con `emisor_vs_arbitro = EMISOR=ARBITRO`: **`M` y `R` son el mismo número
copiado en dos columnas**. Quien derivara la métrica «filas con M y R» publicaría que el
programa tiene 89 celdas con predicción validada fuera de muestra cuando tiene 20 de cruce.
Quedan excluidas, declaradas con su universo, y con test que lo pina.

**(b) Trampa de escala (§4.3), no anticipada por el encargo.** El CALC de `DIN` guarda el
error en **PROPORCIÓN** (`0.004212…`) y el de `TRA` en **PUNTOS PORCENTUALES** (`5.435…`).
Fundirlos sin convertir da un **factor 100** en la métrica rectora del programa. La
conversión **se verificó derivando**, no tecleando: `media(DIN C2)×100 = 1.466786` y
`media(TRA C2) = 1.568052`, idénticos al `margen_material` sellado de cada YAML.

**Piloto 3 NO entra**, verificado en disco: `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/` sólo
tiene `spec.yaml` y `adjudicacion.py` — sin `resultados.json` ni sello. COMMIT-3 no sellado.
El encargo dice «si no, no lo esperes».

**D-21:** `tests/test_celdas_validadas.py`, 7 tests, **cableado en `verify.yml`** y
reconocido por el censo de guardias (`CORRE-EN-CI`). Cada aserción guarda uno de los dos
defectos de arriba; ninguna guarda una hipótesis.

## 3 · P2 · Las NC abiertas, por lo que les falta

`tools/nc_por_clase.py` → `forense/analisis/senal-1/nc-abiertas-por-clase.tsv`, **una fila
por NC abierta**, con token por prefijo (A.16). Entrega para mesa en
`forense/analisis/senal-1/PARA-MESA-firmas-y-lotes.md`.

| clase | n |
|---|---|
| `SIN-ASIGNAR` | 55 |
| `NO-CLASIFICABLE` | 33 |
| `ESPERA-ACTO-NOMBRADO` | 26 |
| `SUCESOR-YA-FUSIONADO` (candidato) | 18 |
| `ESPERA-FIRMA` | 14 |
| `BANDEJA-TITULAR` | 9 |

### El hallazgo: el campo `sucesor` no predice el cierre

El heurístico marcó **18** filas `SUCESOR-YA-FUSIONADO` leyendo el texto de `sucesor`. Se
verificaron **por producto, una por una**: **cero** resistieron. La razón es sistemática —
la mayoría de esos «sucesores» son *decisiones de mesa*, y un PR que fusiona no toma una
decisión. El veredicto de cada una quedó asentado en la columna
`verificado_por_producto_en_senal_1` del TSV, para que el siguiente acto no repita el
trabajo ni confíe en el heurístico.

### Cerradas: 2. `no_corrido_abiertas` **157 → 155 → 159**. Los dos tramos son de naturaleza distinta y no se colapsan: **−2 por los dos cierres verificados por producto** (NC-0379, NC-0390), que es el único movimiento que el encargo autoriza; **+4 por los asientos que A.14 obliga** (NC-0429..NC-0432), que no son deuda nueva descubierta sino las reservas de este mismo acto puestas por escrito. El neto sube, y se declara: el encargo previó que la cifra sólo bajara, y no contempló que cerrar un acto con reservas la suba por regla. **No es PARO** (la lista cerrada del §7 veda que cambien los otros contadores, y A.14 no es opcional); se declara para que mesa decida si quiere que el contador distinga asiento de deuda.

Una por una, con evidencia por producto escrita en `cerrado_por`. Nunca en bloque, nunca
por el hecho de que un PR fusionó.

- **NC-0379** — pedía que `tests/test_pisos_enut2019.py` corriera en CI. Verificado: el test
  existe, corre solo con `exit 0`, y el job `guardias` (PR #917) lo ejecuta; su fila del
  censo da `CORRE-EN-CI`, sin dependencia pendiente ni corpus.
- **NC-0390** — ídem para `tests/test_c2_ic_envipe2025_guardia.py`: `exit 0`, censo
  `CORRE-EN-CI`.

### Una que NO se cerró, y la diferencia es el producto

**NC-0381** pide lo mismo para `tests/test_c2_ic_enif2024_guardia.py`. El job lo descubre
pero **lo salta en voz alta**: `NECESITA-DEPENDENCIA(numpy)`, y `numpy` no está en
`requirements.txt` (NC-0332, abierta). Corrido aquí: `ModuleNotFoundError`. **El PR fusionó;
el producto no existe.** Es exactamente el caso que el encargo manda preguntar a mesa
(«una NC cuyo sucesor fusionó pero cuyo producto no me convence»). **Pregunta a mesa,
con recomendación: añadir `numpy` a `requirements.txt`** — una línea que destraba NC-0381,
NC-0332 y parte de NC-0331. Se sigue con lo demás, como manda D-19.

**NC-0331** tampoco cierra: de sus tres tests sólo uno está cableado.

### Para mesa

- **Las 14 `ESPERA-FIRMA`**, en lenguaje llano, con qué desbloquea cada firma. Ojo con
  **FP-374**: está **VENCIDA-EN-ALCANCE**, no ABIERTA. No se firma — **se re-sella** (A.10).
  Es la única de la tabla que pide una acción distinta, y bloquea cuatro filas que hoy no
  tienen a quién esperar. **FP-395 y FP-397 son gemelas** (el IC sellado que el marcador no
  publica, ENIF y ENVIPE): conviene firmarlas juntas o quedan desalineadas.
- **Lotes propuestos** para las 55 `SIN-ASIGNAR`: ocho lotes de ≤ 4 piezas afines del mismo
  entorno (D-11), seis de nube y dos de caja. **No se redactaron los encargos**, como manda
  el encargo. Se señala que **20 de las 55 no son lote**: esperan decisión, no ejecución, e
  inflan `no_corrido_abiertas` en un 13 % sin trabajo que hacer.

## 4 · P3 · La adopción del 17/sep propagada

En `DIN…` y `TRA…`: `estado_operativo: PENDIENTE → LISTO`; en `DIN` además
`requiere_decision_mesa: true → false`. **Aviso fechado nuevo** en cada archivo; los avisos
viejos quedan **intactos, verbatim**. Ningún campo de adjudicación se tocó.

**El token se verificó contra el contrato, no se supuso.** Dirección no lo halló en v0.6 —
y tenía razón, ahí no está. **Vive en `propuesta-motor-adaptativo-celda-v0_2.md:104`**:
`LISTO` = «existe un candidato `champion_actual` vigente, con `production_spec_refs`
ejecutados y auditables»; `:105`: `PENDIENTE` = «**ningún** champion vigente». Con
`champion_actual: C2` vigente desde la enmienda del 19/sep, `PENDIENTE` era **literalmente
falso**. Los `production_spec_refs` de C2 están EJECUTADOS y auditables en ambas.
`:109` declara `requiere_decision_mesa` **ortogonal** a los cuatro tokens.

**Las tres razones de `requiere_decision_mesa: true` re-verificadas POR ESTADO (A.17),** no
heredadas por nombre, en `forense/firmas-pendientes.tsv`: FP-376 **FIRMADA** (`:365`);
FP-379 D1/D5 **FIRMADA** más su enmienda (`:368`); FP-379 D6 («admisión de C2») **EJECUTADA**
por ADR-538 — «C2 salió PISO-ADMISIBLE sin repliegue».

**Verificación posterior que el encargo pide.** `corrida0.py demanda` **dejó de listar las
dos celdas**. La lista baja de 11 a 10 agrupaciones, y la única celda-D que queda es
`GOB.gobierno_digital.encig2025.edad_x_escolaridad`, **por el campo `estado_operativo`**,
que es `PENDIENTE` — correcto: es COMMIT-1 con `champion_actual: NINGUNO`, fuera de P3.

**Nada se movió en las emisiones**, verificado: `marcador_segmento.py --json` sigue dando
`evaluadas 20 / estimador_adoptado 20 / cobertura_de_piso 79 / sin_piso 15 / valor_anadido 0`
—idénticos a la premisa del encargo— y `data/corrida0/marcador-segmento.tsv` **no cambia un
byte**. El motor emite por `champion_actual == "C2"` y no consulta `estado_operativo`: el
motor no estaba roto, **el archivo se contradecía**.

## 5 · Módulo de auditoría de rigor extremo

Este artefacto afirma sobre el **programa**, y roza México en una línea.

- **¿Cuántos contadores movió este trabajo?** Uno: `no_corrido_abiertas` **157 → 155 → 159**. Los dos tramos son de naturaleza distinta y no se colapsan: **−2 por los dos cierres verificados por producto** (NC-0379, NC-0390), que es el único movimiento que el encargo autoriza; **+4 por los asientos que A.14 obliga** (NC-0429..NC-0432), que no son deuda nueva descubierta sino las reservas de este mismo acto puestas por escrito. El neto sube, y se declara: el encargo previó que la cifra sólo bajara, y no contempló que cerrar un acto con reservas la suba por regla. **No es PARO** (la lista cerrada del §7 veda que cambien los otros contadores, y A.14 no es opcional); se declara para que mesa decida si quiere que el contador distinga asiento de deuda. Los tres vedados **no se movieron**, verificado por
  comando al cerrar: `N_corridas_selladas` 102, `adoptados_activos` 57,
  `dependencias_numericas_legacy_activas` 173. `cuenta_gen2 = NO`: no mide, no adopta.
- **¿En qué escala está cada cantidad y contra qué se compara?** Todo error en **pp**. La
  conversión de la escala cruda de cada CALC se verificó contra el `margen_material`
  sellado. Las brechas temporales (1, 2, 3 años) van por fila y **no se promedian**. El
  duelo nacional **no se suma** a las otras dos clases.
- **¿Qué afirmación sobre el estado del corpus fue escrita a mano y no derivada?** Ninguna
  cifra. La única lista escrita a mano es `VERIFICADAS` en `nc_por_clase.py`, y es el
  **asiento de una lectura que ya ocurrió**, fila por fila, no una constante de conveniencia.
- **¿Qué sería peligroso leído simplista?** Dos cosas, y la línea del tablero las separa a
  propósito. **(1) «73 celdas validadas» no es «73 aciertos»:** es 73 celdas **con error
  conocido**, y algunos errores son malos — el pago de luz por canal digital (ENCIG,
  `N_TRA == '01'`) está validado y su persistencia falla por **11.8 pp**. **(2)
  `SIN-GANADOR-UNICO` no es «el motor no sirve»:** dice que en el duelo nacional de 12
  celdas el motor no se distingue de un LLM con o sin corpus y queda un punto por detrás en
  el estimado puntual, mientras los cruces C2 aciertan a ~1.2–1.5 pp. **Son afirmaciones
  distintas, en universos distintos**, y el tablero no deja que una tape a la otra.
- **¿Pobreza/violencia/informalidad confundidas con cultura?** No aplica: no hay afirmación
  psicológica aquí. La única sustantiva es que la evasión de norma y el ahorro informal
  **se predicen a ~1.2–1.5 pp desde marginales públicos sin interacción** — un hecho sobre
  la *estructura de la tabla*, no sobre los mexicanos. Que un piso sin interacción gane
  dice que el cruce aporta poco en esas celdas, **no** que haya un rasgo compartido.
- **¿Qué deuda «asumida a propósito» caducó?** `requiere_decision_mesa: true` en `DIN`:
  protegía tres decisiones que se firmaron entre el 16 y el 17 de septiembre. Se cargó cinco
  días de más. La caducidad se detectó re-verificando por estado (A.17), que es para lo que
  esa regla existe.
- **¿Dónde hay evidencia débil e intuición fuerte?** En la clase `NO-CLASIFICABLE` (33
  filas): el campo `sucesor` es prosa y la intuición dice que muchas ya están resueltas. **No
  se cerró ninguna por esa intuición.** El hallazgo de §3 es precisamente que la intuición
  falla: de 18 candidatas, cero.


## 5-bis · Dos hallazgos de la cascada de cierre, ninguno buscado

**(a) `dependencias_numericas_legacy_activas` vale 174 en el árbol, no 173.** El encargo lo
declara en 173 y lo pone en la lista de PARO. Al correr `corrida0.py demanda` —que P3 me
manda correr como verificación— los derivados `data/corrida0/demanda-corridas.tsv` y
`demanda-resultados.tsv` se regeneraron y el contador subió a 174. **Se midió si lo causaba
P3, en vez de suponerlo:** revertidos los dos `estado_operativo` a `PENDIENTE`, el contador
**sigue dando 174**. Luego **no lo causó este acto**: los derivados estaban committeados
desactualizados en `main`, y el `173` de la premisa se leía de esa versión rancia. Los dos
archivos **no están en el perímetro de este acto**, así que se revirtieron a `HEAD` y el
contador vuelve a leerse 173, como el encargo exige. **La deriva es real y preexistente, y
se reporta sin arreglarla**: un acto con `data/corrida0/` en perímetro debe re-derivarlos.
No es PARO, porque el PARO veda que *este acto* mueva el contador, y no lo movió.

**(b) Ocho afirmaciones de suite en `canon/` estaban sin marcar como históricas.** T16 las
destapó cuando el FAIL real dejó de ser 3. Son cifras de actos pasados, correctas al cierre
de cada uno. **No se editó ninguna cifra:** se les puso la marca `{cita-historica}` que la
casa ya usa en las otras veinte líneas iguales del mismo archivo (mecanismo de
`ACTO T16-HISTÓRICAS`). Defecto adyacente de menos de diez líneas que impedía cerrar: D-21
autoriza arreglarlo y declararlo.

**Firma abierta por este acto (A.12): FP-403** — añadir `numpy` a `requirements.txt`. Nace
ABIERTA con el hecho medido aquí, la recomendación del ejecutor y lo que **no** se
recomienda (cerrar NC-0381 sin la dependencia sería un cierre falso).

**Suite al cerrar: `python3 tests/check.py --baseline` → LÍNEA BASE VERDE, sin FAIL nuevos,
`EXIT=0`.** 20 WARN nuevos, que son estado y no adjudican (D-16).

## 6 · Perímetro

Escrito, todo dentro del perímetro propio: `tools/tablero_programa.py` ·
`forense/tablero/TABLERO-PROGRAMA.md` · `forense/analisis/senal-1/` (nuevo) ·
`forense/no-corrido.tsv` (2 cierres verificados) · las dos celdas-D nombradas (sólo los
campos de P3 y el aviso nuevo) · `tests/test_celdas_validadas.py` (propio) ·
`tools/nc_por_clase.py` (propio) · `.github/workflows/verify.yml` y
`forense/analisis/ci-guardias/censo-tests.tsv` (cableado del test propio, D-21, perímetro de
cierre permanente).

**No se tocó** `tools/corrida0.py` (sólo se ejecutó) · `milpa/**` · ningún CALC · las tres
celdas `G5.*` · `forense/prereg-duelo-v2/**` · el esquema de ids de NC/FP/ADR.

`tools/marcador_segmento.py` **no hizo falta**: el error de cruce vive en los CALC, no en el
marcador, así que no se expuso ningún campo nuevo en su `--json`.

**Dónde estorbó el esquema de ids (se anota, no se rediseña, es de la conversación
TUBERÍA):** en nada operativo. Una observación para quien lo gobierne: `FP-374` está
`VENCIDA-EN-ALCANCE`, un estado que el clasificador tuvo que tratar aparte porque no es
`FIRMADA` ni `ABIERTA`; cuatro NC la citan como si esperaran una firma que ya no puede
llegar.

## NO-CORRIDO / RESERVAS

- **`FUERA-DE-PERÍMETRO`** — `numpy` en `requirements.txt`. **Impacto:** NC-0381 no cierra y
  `tests/test_c2_ic_enif2024_guardia.py` sigue sin correr en CI. **Sucesor:** DECISIÓN-DE-MESA
  pedida en §3 y en la entrega para mesa; lote N1 propuesto.
- **`DECISIÓN-DE-MESA-PENDIENTE`** — los ocho lotes propuestos para las 55 `SIN-ASIGNAR`.
  **Impacto:** ninguno inmediato; la deuda queda clasificada y visible. **Sucesor:** dirección
  redacta los encargos a partir de la lista; este acto no los redacta, por mandato.
- **`FUERA-DE-PERÍMETRO`** — el error de persistencia de las 6 celdas de formalidad.
  **Impacto:** no cuentan en `celdas_validadas` y así se declara en la línea del tablero.
  **Sucesor:** CALC de error de persistencia para formalidad (nube, entradas selladas); su
  firma es FP-396.
- **`DIFERIDO-A`** — el piloto 3 en `celdas_validadas`. **Impacto:** ninguno; entra solo
  cuando selle COMMIT-3. **Sucesor:** COMMIT-2/COMMIT-3 del piloto 3, en CAJA.
- **`NO-VERIFICABLE-AQUÍ`** — nada. La red está denegada y el corpus ausente, pero **este
  acto no necesitó ninguno de los dos**.

## CONSUMIDO

`forense/encargos/2026-09-21-GEN2-SENAL-1.md` — CONSUMIDO por este acto.

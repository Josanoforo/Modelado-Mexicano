# ACTO GEN2-F5-CIERRE-Y-PANEL-1 · LA TABLA COMÚN SE CONGELA, Y EL PANEL NO LLEGA A SEIS — nota de cierre

**15/sep/2026 · entorno NUBE · Opus · cero llamadas a modelo · cero microdato abierto · cero adopciones.**
Sobre la **FIRMA DE MESA del 15 de septiembre de 2026** (`D-1`…`D-5`), la **LECTURA ESTRATÉGICA F5 v1.1** y el adversarial de Astra.

## 0 · Qué se pidió y qué salió

| | pedido | salió |
|---|---|---|
| **P1** | corrida de registro que congele la tabla común, spec en dos capas, `B-bis` declarado, `COMMIT-1` + `COMMIT-2` | **HECHO.** `CALC-TRIADA-B-PISO-0001` sellado, `verify REPRODUCE`. Los cuatro `MAE` reproducen al centésimo lo que dirección verificó |
| **P2** | lista corta de familias candidatas con los cuatro campos de la firma, auditada por exposición | **HECHO, Y NO ALCANZA.** 13 filas: 7 `RETENIDA`, 5 `EXPUESTA`, 1 `INDETERMINADA`. **Sólo 2 retenidas realistas para piloto**, no 6 |
| **P3** | ruteo de `NC-0161/0162`, cierre de `NC-0152`/`0180`/`0187`, enmienda in situ de `FP-374` | **HECHO**, con una salvedad mecánica: la vista derivada de adquisición no se puede regenerar por un defecto **preexistente** (`NC-0220`) |

**El titular honesto:** el producto que decide `F6` dice que `F6` todavía no puede empezar. La lista nominal existe, está auditada y tiene nombres y citas — y precisamente por eso se puede afirmar, por primera vez con causa y no con un hueco, que **las 18 familias disjuntas que `FP-374` exige no existen hoy**.

---

## 1 · P1 · La tabla común, congelada

**Dos capas, congeladas en el `COMMIT-1` (`f1cf4cc`) antes de que ningún medidor leyera un byte:**

- **Capa científica:** `forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md` — `prereg-caja-TRIADA-B-PISO`, `sha256 a1043b48…`.
- **Capa mecánica:** `spec.md`, `spec.yaml` (117 outputs declarados con tipo y unidad) y `medidor.py`, probado **sólo sobre datos sintéticos** (19 aserciones en `pruebas-sinteticas.py`).

El `COMMIT-2` (`7739feb`) sella: `preflight` **VERDE** → `run exit=0`, 117/117 outputs, sin faltantes ni sobrantes → `verify` **REPRODUCE** (`CONTEXTO=IDENTICO`) → sello `63310e1d…`.

### 1.1 · El control de derivación — el acto deriva, no hereda

Es la razón de ser del CALC. Recalculando desde `celdas.tsv` sobre `U3`, los tres `MAE` sellados de `CALC-TRIADA-0002` salen así:

| corredor | derivado | sellado 0002 | Δ (pp) | rama |
|---|---|---|---|---|
| `L_CORPUS` | 3.889025747 | 3.889025747 | 2.89e-09 | `REPRODUCE-AL-CENTESIMO` |
| `L_SOLO` | 3.957362250 | 3.957362182 | 6.84e-08 | `REPRODUCE-AL-CENTESIMO` |
| `M` | 4.986673250 | 4.986673240 | 1.02e-08 | `REPRODUCE-AL-CENTESIMO` |

`RESULT-TBP-U3-CONTROL-VEREDICTO = DERIVA`. **Y la rama importa:** ninguno cae en `REPRODUCE-EXACTO` porque `celdas.tsv` guarda seis decimales. Por eso el lanzamiento dijo *«reproducen al centésimo»* y no *«exacto»*, y por eso la spec declaró la rama del centésimo **antes** de correr en vez de descubrirla después. Si alguno hubiera salido `NO-REPRODUCE`, la tabla no se emitía y el acto entregaba un `NC` (`§4.1` de la sellada).

### 1.2 · La tabla, sobre las 9 celdas donde los cuatro compiten

`U_COMUN = U3 ∩ {celdas con B bajo PERSISTENCIA}` = **9 de 14**. Errores absolutos en pp:

| celda | `B` | `L_CORPUS` | `L_SOLO` | `M` | `B` < `M` |
|---|---|---|---|---|---|
| `CIV-M-01` · ENVIPE 2012 | 0.2485 | 0.8999 | 2.3999 | 3.5314 | sí |
| `CIV-M-02` · ENVIPE 2013 | 1.5599 | 0.3400 | 3.1600 | 5.0913 | sí |
| `CIV-M-04` · ENVIPE 2015 | 3.1544 | 0.6332 | 1.1332 | 5.0645 | sí |
| `CIV-M-10` · ENVIPE 2021 | 0.1125 | 2.5066 | 2.5066 | 8.9379 | sí |
| `CIV-M-12` · ENVIPE 2023 | 0.5014 | 3.1888 | 1.1888 | 8.6201 | sí |
| `CIV-M-13` · ENVIPE 2024 | 1.3500 | 2.5388 | 1.7888 | 9.9701 | sí |
| `FAM-M-05` · ENIGH 2016 | 0.6675 | 0.0041 | 0.2541 | 0.1765 | **no** |
| `FAM-M-06` · ENIGH 2018 | 0.0173 | 0.2715 | 0.2715 | 0.1591 | sí |
| `FAM-M-07` · ENIGH 2020 | 0.3510 | 0.6225 | 0.6225 | 0.1919 | **no** |
| **`MAE_pp` (n = 9)** | **0.884716** | 1.222815 | 1.480597 | 4.638093 | **7 / 9** |

Reproduce al centésimo lo que dirección verificó antes de encargar: **B 0.885 / L_CORPUS 1.223 / L_SOLO 1.481 / M 4.638**.

**Las cinco celdas fuera, con razón nominal y sin rellenar:** `TRA-M-07` `FUERA-DE-U3` (abstención válida de `L_CORPUS`, `NC-0152`); `FAM-M-01`, `TRA-M-02`, `TRA-M-03` `SIN-B-PERSISTENCIA`; `DIN-M-01` `FUERA-DE-U3-Y-SIN-B`.

### 1.3 · Lo que la tabla NO dice, declarado antes de verla (`B-bis §4.2`)

`RESULT-TBP-VEREDICTO = NO-ADJUDICA-POR-DISENO`. La ordenación sale rotulada `ORDEN-DESCRIPTIVA` y `SIN-GANADOR-UNICO` se cita intacto desde la `0002`. Cuatro medias sobre nueve celdas, sin IC y sin pareadas, no discriminan: la `0002` ya declaró `INCONCLUSO` las tres pareadas sobre un universo **mayor**, y recortar de 12 a 9 celdas quita poder, no lo añade.

**Y hay una lectura de composición que la tabla obliga a decir.** El orden global lo produce **un solo bloque**: las seis celdas `CIV-ENVIPE`, donde `M` yerra entre 3.5 y 10 pp. En las tres celdas `FAM-ENIGH`, `M` es el mejor o casi el mejor corredor (0.1765, 0.1591, 0.1919) y **le gana a `B` en dos de las tres**. `B` cubre justamente las celdas donde `M` va peor y no cubre `TRA` ni `DIN` en absoluto. Que `B` quede primero describe **qué celdas tienen `B`** tanto como describe a los corredores. Esto refuerza `D-1` en vez de contradecirlo: el valor predictivo añadido de `M` sigue **por demostrar**, y esta tabla no lo demuestra ni lo refuta.

### 1.4 · El contador, sin disfraz

`cuenta_gen2 = SI`, escrito en `data/corrida0/decisiones.tsv` citando el lanzamiento **verbatim**. Se declara lo que la firma pasa por encima: la regla `E.1` marca esta corrida **`envuelto_legacy = SI` por cadena** (consume `RESULT` de `CALC-B-MARCO-MAE-0001` y `CALC-TRIADA-0002`, lectores de `corridas-R/`), y **sin la firma el registro la resolvería `NO`**. `prereg-caja-B-MARCO §7.7` declinó firmar sobre un envuelto; este acto se aparta de ese precedente por decisión explícita y más reciente de mesa, que es la precedencia 1 del propio `corrida0.py`. Queda registrado en las dos capas, en `spec.yaml`, en la fila de `decisiones.tsv` y aquí, para que **nadie lea el contador como derivado por la máquina**.

`corrida0 registro` **en seco** confirma la declaración palabra por palabra:

```
CALC-TRIADA-B-PISO-0001--f1cf4cc7bbc6  OFERTA  CALC-TRIADA-B-PISO-0001  SELLADA  GEN2  SI  SI
  motivo: decision de mesa (`decisiones.tsv`): cuenta_gen2=SI
```

**Las vistas derivadas NO se escribieron.** `--escribe` regenera `corridas`/`resultados`/`usos` completas (~4 473 líneas, 229 objetos ajenos) y `usos.tsv` es de `RELEVO-USOS-1`, concurrente. Aporte propio proyectado: **118 filas** (1 corrida + 117 resultados) y **CERO** en `usos.tsv` — que es la comprobación material de que no adopta, junto a `RESULT-TBP-ADOPCIONES = 0` y `§5.5` de la sellada.

---

## 2 · P2 · La lista nominal, y por qué no llega a seis

**Entregable:** `forense/prereg-duelo-v2/F5-panel-candidatos-v1_1.tsv` — 13 filas, 17 columnas, con los cuatro campos de la firma (pregunta y dos celdas · qué emite `M` sin conocer el objetivo · material existente/faltante · exposición previa y cómo se preserva la reserva), más `estado` y `qué falta adquirir`.

### 2.1 · La auditoría de exposición, y cómo se hizo

Contra **cuatro** superficies, no tres: `milpa/` (qué fuentes calibraron reglas), el **corpus de L** (37 documentos), `traza-motor.tsv` (las fuentes propias del snapshot `M`) y **«no evaluada»** (`data/corrida0/`, el marco, `corridas-R/`, `prereg-caja/`).

**Un hallazgo de método que vale más que el resultado.** La primera pasada usó fronteras de palabra (`\bENGASTO\b`) y dio *cero* huella para ENGASTO. La segunda, por subcadena, encontró `milpa/procedencia.yaml:1434`: `"eder2017/engasto2012:edo_conyug"`. El token `engasto2012` no tiene frontera después de `engasto`, así que la primera pasada **habría declarado RETENIDA una familia expuesta**. Toda la auditoría se rehízo por subcadena y **cada coincidencia se adjudicó a mano**, porque la subcadena también produce falsos positivos: el único *hit* de ENAFIN es `milpa/src/emisor.py:1299`, un *docstring* que ilustra una función de normalización de nombres — no es calibración, ni elección de regla, ni contexto de `L`, y se resolvió **NO es exposición**. Igual se revisó y descartó «violencia digital» en el corpus (es violencia digital **de pareja**, no ciberacoso).

### 2.2 · Las siete retenidas, y qué falta de cada una

| familia | celdas propuestas | regla de `M` que emite a ciegas | falta | realista |
|---|---|---|---|---|
| **R01 · MOCIBA** | 2021 y 2023 (mismo bloque de diseño; 2024/2025 en reserva) | `civico.denuncia.miedo_desconfianza` — transferencia de **dominio** (delito → acoso digital) | leer el **FD** (ya adquirido) para confirmar la batería de denuncia y fijar variable/universo/codificación/ponderador | **sí**, con un paso |
| **R02 · WBES México** | 2010 y 2023 | `tramite.mordida.discrecional` | **nada material** (microdato `.dta` 2023 + DDI completo ya en el árbol). Falta una **firma**: cambio de unidad persona → establecimiento | **condicionada** |
| R03 · ENAPROCE | 2015 y 2018 | `tramite.mordida.*` | lo registrado son bases **de ejemplo cegadas**, no el microdato real; 0 FD | no |
| R04 · ENAFIN | ninguna | ninguna aplicable (mide financiamiento de empresas, no ahorro de personas) | microdato de respondente y un estimando que alguna regla emita | no |
| R05 · ENESTYC | ninguna | **ninguna** de las cinco reglas | — | no |
| R06 · ENJUVE | ninguna | no evaluable | microdato: sólo existe una presentación agregada de 2010 | no |
| R07 · ENEAC | una sola | `tramite.mordida.con_registro`, parcial | una segunda ola, que no existe | no |

### 2.3 · Las expuestas, con cita

`ENGASTO` (`milpa/procedencia.yaml:1434`) · `ENASEM` (`milpa/tramite-ola5-propuesta-v0.yaml:2465`, *«descarto ENASEM por medir afiliacion y no percepcion»* — descartar una fuente al elegir una regla **es** usarla) · `ICPSR 35024 Mexico Panel` (`milpa/…:2842-2866`, fuente de calibración declarada de clientelismo, con DOI y codebook: es la `A02` de `FP-374`, y cae por **exposición**, no por falta de acceso) · `ENVE` (el corpus de `L` cita su **cifra negra de 2024**, 90.3 % — el caso de libro: expuesta por el número, no sólo por el nombre) · y el bloque de 19 familias con huella medida en `milpa/` o en el corpus (`ENDUTIH`, `ENOE`, `ENSANUT`, `ENDIREH`, `EDER`, `ENUT`, `ENADID`, `ENCUP`, `ENSAFI`, `ENADIS`, `LAPOP`, `WVS`, `Latinobarómetro`, `CSES`, `Pew`, `ENFIH`, `ENASIC`, `MOTRAL`, `CNGMD`). `A01-OECD-TRUST` queda `INDETERMINADA`: el corpus cita «OECD» una vez, pero como **agregado** de comparación, no el *Trust Survey* — no alcanza para declararla expuesta **ni** para declararla limpia.

### 2.4 · La declaración, sin estirar la lista

**No llega a 6 retenidas realistas: llega a 2**, y una de ellas depende de una firma sobre cambio de unidad. Frente a las **18** (6 piloto + 12 confirmatorias) que `FP-374` exige, no hay ruta. Se declara, como el encargo ordenó, y se propone la **factibilidad acotada**:

> **Factibilidad NO CONFIRMATORIA de UNA familia (R01 · MOCIBA).**
> **Producto:** una spec congelable con reactivo, universo, codificación y ponderador fijados leyendo **sólo** el FD de MOCIBA 2021 y 2023 — nunca la base —, con 2024/2025 intactas como reserva confirmatoria.
> **Parada, explícita:** si el FD **no** trae batería de denuncia ante autoridad, MOCIBA cae, **no queda ninguna familia retenida ejecutable**, y eso se declara en vez de estirar la lista.
> **Lo que NO autoriza:** ni piloto, ni confirmación, ni llamadas, ni apertura de `F6`.

---

## 3 · P3 · Ruteo y cierres

| fila | antes | ahora |
|---|---|---|
| `NC-0152` | `ABIERTA` | **`CERRADA`** citando **`PR #764`** (`GEN2-F5-DOCUMENTAL-RUN-2`), por `D-5`. El sucesor que la fila declaró se ejecutó y lo superó: 16/16 `PUNTO` trazables en el brazo dirigido contra 0/16 en el control. Cierra por **recuperación documental, no por imputación**: las 16 abstenciones siguen válidas, `U3 = 12` no cambia |
| `NC-0180` | `ABIERTA` | **`CERRADA`** por `P1`. Pedía *«una corrida de tríada con `B` de cobertura real»*; ya existe. **Por producto, no por adjudicación**: sigue sin IC, sin pareadas, y `NO-DISCRIMINA`/`INCONCLUSO` no cambian |
| `NC-0187` | `ABIERTA` | **`CERRADA`** por `P1`, **por consumo en el consumidor declarado** (la tríada), que es literalmente lo que la fila exigía. Adopciones en cero, verificable por tres vías |
| `NC-0161` | `ESPERA_O_DELEGADA` | **ruteada** a adquisición dirigida con reserva: leer el FD de MOCIBA 2021/2023. Sigue `ABIERTA` |
| `NC-0162` | `ESPERA_O_DELEGADA` | **ruteada**: no se integra 17 ni el snapshot de 18 contra familias expuestas; espera a que `NC-0161` entregue una familia con reactivo confirmado. Sigue `ABIERTA` |
| `FP-374` | `ABIERTA` | **`ABIERTA`. No se re-sella.** Enmienda in situ fechada en `gatea` y `ejecutada_en`: registra `D-3` y `D-4`, y que **su compuerta ahora es la lista nominal**. La recomendación *NO AUTORIZAR EL PILOTO HOY* se mantiene, ahora con causa nominal |

**`NC` abiertas: 60 → 58** (tres cerradas, una nueva).

### 3.1 · `adq-demanda-activa`: bloqueada, luego desbloqueada por `main` (`NC-0220`, abierta y cerrada en el mismo acto)

El JSON declara `"generado": true` y `"fuente": "forense/no-corrido.tsv"`. **Es derivado**, así que el ruteo se hizo en su fuente. Regenerarlo aborta:

```
KeyError: 'NC-0088'   —   tools/adq_investigacion.py:649
```

`contratos` se arma sólo con `NC` **abiertas**, pero el bucle recorre `necesidades`, que todavía referencia `NC` cerradas; `NC-0088` la cerró `GEN2-FIRMAS-MESA-1` (`PR #785`) **hoy mismo**. **Verificado que es preexistente:** el mismo comando aborta con el mismo `KeyError` sobre el árbol sin los cambios de este acto (probado con `git stash`). **No se arregla aquí**: `tools/adq_investigacion.py` está fuera del perímetro, lo comparte el servicio `adq` concurrente, y un `.get(ident, {})` cambiaría la etapa proyectada de **todas** las filas. Tampoco se edita el JSON a mano: fabricaría un estado que ningún generador derivó, justo lo que el encargo evita al decir que *el ruteo se coordina por la tabla, no editando su cola*. **El ruteo en sí está hecho y verificado, no supuesto.** Se simuló el ruteador sobre las filas reales, importando `tools/adq_investigacion.py` y llamando `_etapa_faltante` / `_ruteo_automatico` / `_responsable` antes (`git show HEAD~1`) y después:

| fila | antes | después |
|---|---|---|
| `NC-0161` | `DECISION_O_IMPLEMENTACION` · **`ESPERA_O_DELEGADA`** · resp. `FP-374` | `FUENTE_O_VARIABLE` · **`LISTA_SONDA`** · resp. `servicio-gen2-38` |
| `NC-0162` | `DECISION_O_IMPLEMENTACION` · **`ESPERA_O_DELEGADA`** · resp. `FP-374` | `FUENTE_O_VARIABLE` · **`LISTA_SONDA`** · resp. `servicio-gen2-38` |

Es decir: la fuente ya dice lo que debe decir y la proyección lo recogerá sola en cuanto el generador corra. Queda en `NC-0220`, con el agravante de que **cada cierre agranda el defecto** — este acto cerró tres más.

**Y entonces `main` lo arregló.** Al resolver el conflicto de `PR #791` se trajo `origin/main`, que ya traía el trabajo de adquisición con **exactamente el guard diagnosticado**:

```python
# La conciliación conserva referencias históricas aunque una NC cierre.
# Sólo los contratos todavía vigentes entran a faltantes y ruteo.
necesidades = [ident for ident in grupo.get("necesidades_nc", []) if ident in contratos]
```

El dueño del generador llegó a la misma corrección por su cuenta, que es la mejor prueba de que no tocaba arreglarlo desde aquí. Con eso **la proyección se regeneró y el ruteo quedó materializado, no sólo declarado en la fuente**: `NC-0161` y `NC-0162` salen ahora en `data/adq-demanda-activa-v1_0.json` con `estado_ruteo = LISTA_SONDA`, `etapa_faltante = FUENTE_O_VARIABLE` y `responsable = servicio-gen2-38`. `NC-0162` queda fuera de `seleccion_siguiente` sólo por *«lista, fuera del tope máximo=3»* — que es estar **en** la lista, no fuera de ella.

El diff de la proyección toca 13 necesidades y las 13 se explican: las dos ruteadas, las tres que este acto cerró (`NC-0152`, `NC-0180`, `NC-0187`) que dejan de ser necesidad, y las siete de `GEN2-RELEVO-USOS-1` (`NC-0211`…`NC-0217`) cuya proyección en `main` era anterior a ellas. Ninguna se editó a mano. **`NC-0220` nació y murió dentro del mismo acto** y el perímetro queda completo.

---

## 4 · Contaminación declarada (ADR-46) y A.13

**TOTAL, y sin fingir ceguera.** El lanzamiento **ya traía** los cuatro `MAE` porque dirección los verificó antes de encargar, y esta sesión pudo ver y vio los cuatro insumos. Lo que sostiene la corrida no es el desconocimiento sino que **la regla no admite alternativas**: universo por intersección (no hay criterio que elegir), estadístico heredado, brazo `PERSISTENCIA` por cobertura, columnas preexistentes. Coste dicho sin descuento: **esta corrida no puede sorprender**; su valor es de registro, no de descubrimiento (`§0.2` de la sellada).

**Qué se leyó (A.13):** `celdas.tsv` (14 filas, por columna); `resultados.json` de `CALC-B-MARCO-MAE-0001` (155 `RESULT`) y de `CALC-TRIADA-0002` (cinco llaves); `marco-M-sorteado-v1_3.tsv`; `no-corrido.tsv` (206 registros) y `firmas-pendientes.tsv` (362); `tools/corrida0.py` y `tools/adq_investigacion.py` (reglas `E.1`, `_cuenta_gen2_resuelto`, `_ruteo_automatico`, `_etapa_faltante`); `milpa/*.yaml` (7 652 líneas) y `milpa/src/emisor.py`; los 37 documentos del corpus de `L`; `data/manifiesto.yaml` (1 608 entradas); y los tres inventarios de reactivos (**317 718 filas**). **No se abrió** microdato, `corridas-R/M/L`, `L-extraido-*` ni `M-*.json`. `data/raw/` está **vacío** en la sesión nube: ninguna verificación de este acto depende de un *payload*.

## 5 · Higiene e incidentes

1. **`no-corrido.tsv` tiene 22 filas con 10 columnas en vez de 12** (`NC-0029`, `NC-0033`, `NC-0038`…), todas anteriores a este acto. Se registra en una línea y se deja como está: fuera de perímetro. Por eso las ediciones se hicieron **empalmando registros** en el texto crudo en vez de reescribir el TSV — un `csv.writer` sobre todo el archivo re-entrecomillaba 21 filas ajenas. Diff final: **5 líneas modificadas + 1 añadida**, ninguna otra tocada.
2. **La prueba sintética del borde exacto estaba mal escrita** y se corrigió antes de congelar: comparaba `8.0 - 0.005` contra el umbral, lo que prueba la aritmética flotante, no la regla. Se sustituyó por un delta claramente por encima y se documentó que el umbral es `<` **estricto**.
3. **`U_COMUN` vacío** no estaba guardado en el medidor: habría sido una división por cero. Se añadió `NO-EMITE-UCOMUN-VACIO` **antes** del `COMMIT-1`, con su prueba. Un `MAE` de cero celdas no es un `MAE`.
4. **`spec-check` da 4 `FAIL`** para este CALC. Es estructural en los CALC derivados, no un defecto: el comando valida contra el inventario de reactivos de **microdato**, y este CALC no consume ninguno. El precedente `CALC-B-MARCO-MAE-0001` da 3 `FAIL` por lo mismo. La compuerta que aplica es `preflight`, que salió **VERDE**.

## 6 · Lo que este acto NO hizo

No lanzó llamadas · no abrió microdato · no adoptó nada al motor · no re-corrió la tríada ni tocó `SIN-GANADOR-UNICO` · no corrió pareadas ni IC nuevos · no usó el brazo `OPERATIVO` de `B` · no diseñó la recuperación documental · no abrió `F6` · no re-selló `FP-374` · no editó la cola del servicio `adq` · no escribió las vistas derivadas del registro · y **no estiró la lista de familias para llegar a seis**.

---

## 7 · Del perímetro: lo que se escribió fuera, y lo que este acto no cubre

**Tres archivos fuera del perímetro literal, los tres necesarios y ninguno silencioso:**

1. `data/corrida0/decisiones.tsv` — una fila. Es *donde vive* la «firma de contador embebida» que el lanzamiento ordena: la precedencia 1 de `_cuenta_gen2_resuelto` lee ese archivo y ningún otro. Sin la fila, `cuenta_gen2` se resolvería `NO`.
2. `forense/prereg-duelo-v2/F5-panel-candidatos-v1_1.tsv` — el entregable de `P2`, que el encargo pide sin darle ruta. Se puso como sucesor de `F5-panel-candidatos-v1_0.tsv`, junto a su antecesor.
3. `forense/notas/2026-09-15-…-cierre.md` — esta nota, por convención del programa.

**El perímetro queda completo.** `adq-demanda-activa` estuvo sin tocar mientras su generador estaba roto; al desbloquearse con `main` se regeneró, y las dos filas de ruteo que el encargo pedía están materializadas (§3.1).

**Lo que este acto NO cubre, y no le tocaba:** `D-5` de la FIRMA DE MESA pide además **un documento del programa, breve y legible para un externo, con detalles en anexo, iniciado ahora y sin esperar al sello de D-A**. El encargo de este acto sólo recoge de `D-5` el cierre de `NC-0152`; el informe no aparece en `P1`/`P2`/`P3` ni en el perímetro. No lo cubre este acto — pero **ya tiene dueño**: el segundo sync trajo `GEN2-INFORME-INTERNO-F5-1`, que es ese informe (§8).

---

## 8 · Cascada de renumeración y merge de `main` (`PR #791`)

La fila de este acto se renumeró **dos veces**, y las dos por la misma razón: otro acto fusionó antes.

| sync | quién llegó primero | qué tomó | mi fila pasa a |
|---|---|---|---|
| 1º (`eba9fd2`) | `GEN2-RELEVO-USOS-1` | `NC-0211`…`NC-0217` | `NC-0211` → **`NC-0218`** |
| 2º (`4acdae2`) | `GEN2-INFORME-INTERNO-F5-1` | `NC-0218`, `NC-0219` | `NC-0218` → **`NC-0220`** |

En los dos casos el lado de `main` queda **intacto** y se mueve el mío. Es la cascada de costumbre del programa, la misma que renumeró `ADR-504`→`ADR-507` y `NC-0186`→`NC-0190`, y la misma que `GEN2-INFORME-INTERNO-F5-1` aplicó a su propia fila (`ff2e679`: «renumera ADR-514→515 y NC-0211/0212→0218/0219»).

**Segundo sync — el otro choque, que no era de numeración.** `main` también cerró `NC-0152`, citando `#764` como mesa ordenó en `D-5`: la **misma decisión** que este acto, con otra redacción. No es un caso de «cada lado cambió la misma lógica»: los dos coinciden en `CERRADA`, misma fecha y misma cita. Se conserva **el texto de `main`**, que es el canónico y cita a mesa verbatim, y se le **anexa** la referencia cruzada de este acto — que consume el mismo residual desde el otro lado, dejando las dos celdas fuera de `U_COMUN` con razón nominal. Nada se pierde y nada se duplica.

**Y una nota que cierra un pendiente de §7:** el acto que tomó `NC-0218`/`NC-0219` es `GEN2-INFORME-INTERNO-F5-1`. Es decir, **el informe del programa de `D-5` ya tiene acto asignado** y está en marcha; este acto lo dejó anotado como pendiente sin dueño y ese pendiente queda resuelto por otra vía.

El primer merge de `origin/main` (`eba9fd2`) trajo `RELEVO-USOS-1`, `ADQUISICION-CONTINUA-2` y `EVIDENCIA-HABILITACION`; el segundo (`4acdae2`, 25 commits más) trajo `GEN2-INFORME-INTERNO-F5-1` y la investigación de ahorro. **Conflicto del primero:** `forense/no-corrido.tsv`, y sólo por esa colisión de identificador. Las cinco filas que este acto tocó (`NC-0152`, `NC-0161`, `NC-0162`, `NC-0180`, `NC-0187`) sobrevivieron intactas, verificado tras el merge. Tras el segundo: **215 registros, sin identificadores duplicados**, y las mismas cinco filas intactas.

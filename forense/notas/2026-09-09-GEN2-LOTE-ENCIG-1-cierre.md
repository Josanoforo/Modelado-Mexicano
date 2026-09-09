# `ACTO GEN2-LOTE-ENCIG-1` — cierre. El ciclo entero: medir, citar en el motor, probar el consumo

**Fecha:** 9/sep/2026 · **Entorno:** CAJA (Ubuntu/WSL2), corpus montado · **Base:** `origin/main = 606f6ee` (`PR #662`)
**Encargo:** `forense/encargos/2026-09-09-GEN2-LOTE-ENCIG-1.md` (A.3, verbatim, con su ADENDA DE PROPAGACIÓN)
**Spec sellada:** `forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md` (`prereg-caja-ENCIG-MORDIDA`, `sha 00c7c4a6…`)
**Corrida:** `data/corrida0/CALC-ENCIG-0001/` — `PRE-FLIGHT VERDE` → `run` → `verify: REPRODUCE` (108/108, `CONTEXTO=IDENTICO`)

---

## 0 · El titular, antes de nada

**El ciclo cierra entero por primera vez: se midió, se citó en el motor y se probó el consumo.** Cuatro de los seis consumidores «positivos» quedan adoptados con cita `corrida0_resultado_id` + `corrida0_generacion: GEN2`, la sonda de consumo pasa **4/4** contra `milpa.src.emisor`, y los contadores del programa se mueven: `adoptados_activos` **2 → 6**, `dependencias_legacy` **203 → 199**.

**El control positivo contra GEN1 sale `REPRODUCE-4/6`, y los dos que no reproducen son informativos, no un accidente:** son exactamente la rama **deduplicada**, que el propio proyecto ya había declarado superada.

**Y al montar la cadena aparecieron cinco cosas que ninguna de las doce cifras GEN1 dice.** Ninguna se buscó: las cinco salen de guardias pre-declaradas en el COMMIT-1.

---

## 1 · La compuerta y las premisas se re-derivaron antes de editar

| lo que el encargo declaró | lo real, verificado |
|---|---|
| `COMPUERTA: GATED a … R-SERIE-DBF` | reescrita por ADENDA (1) a «#661 **y** #662». **Las dos CUMPLIDAS, por producto**: `git merge-base --is-ancestor 435e60a8 origin/main` (rc 0) y `origin/main` = merge de `#662`, con `git cat-file -e origin/main:forense/notas/2026-09-09-GEN2-PREP-LOTE-identidad-migracion.md` existente. |
| base `4497029a` | base real **`606f6ee`**. Re-derivado todo lo que depende del perímetro. |
| `P0` · corregir el derivador | **SUPERSEDED-POR: `ACTO GEN2-PREP-LOTE` (`PR #662`)**, ADENDA (2). No se tocó `_instrumento()`. |
| «`CORR-0002`, **10** RESULT» | **12**, enumerados desde la demanda vigente (ADENDA 3): `+RES-0021`, `+RES-0022`. |
| «`_r2` = segunda **ronda del cuestionario**» | **FALSO.** ENCIG 2025 tiene **un** cuestionario y **un** reactivo `P8_4`. Ver §4. |
| «`CORR-0003`, 2 RESULT» | la demanda vigente dice **4** (`RES-0005/0006/0061/0062`). No es de este lote; se anota y no se toca. |

**Cobertura retroactiva:** `forense/prereg-caja/` — **0** aciertos de `encig` sobre el directorio completo. La spec no existía. Los doce valores GEN1 sí, sellados desde agosto: **lo que faltaba era la cadena, no los números.**

## 2 · La medición

Payload `encig25_base_datos_csv`, `sha256 47daf2f7…` **verificado byte a byte en la caja**. Universo heredado del manifiesto y estampado en cada `RESULT`: **82 áreas urbanas de 100 mil habitantes o más, 18 años y más, referencia 2025. Nada de esto es nacional.**

| familia | celda | valor | IC95 | n | unidad |
|---|---|---|---|---|---|
| **A** discrecional | `A-P-SOL1` (celda GEN1) | **0.085118** | [0.080867, 0.089021] | 40 042 personas | PERSONA, `FAC_P18` |
| **A** | `A-P-SOLANY` **(primaria)** | **0.115702** | [0.110744, 0.120602] | 40 027 | PERSONA |
| **B** con registro | `B-P-PRE-SD` (`_r2` presencial) | **0.141041** | [0.116385, 0.168478] | 11 167 eventos | EVENTO, `FAC_TRA` |
| **B** | `B-P-DIG-SD` (`_r2` digital) | **0.029868** | [0.021009, 0.039850] | 7 219 | EVENTO |
| **B** | `B-P-PRE-CD` (base presencial) | 0.115968 | [0.103014, 0.131338] | 9 942 | EVENTO |
| **B** | `B-P-DIG-CD` (base digital) | 0.027356 | [0.019011, 0.037903] | 6 339 | EVENTO |
| **C** gobierno digital | `C-P-ADOPTA` | **0.673393** | [0.662900, 0.684530] | 20 203 trámites | TRÁMITE `N_TRA=01` |

**Control positivo, `REPRODUCE-4/6`:** `A-P-SOL1` `+1.456e-07` · `B-P-PRE-SD` `−2.831e-07` · `B-P-DIG-SD` `−4.454e-07` · `C-P-ADOPTA` `+3.407e-08` — los cuatro dentro de `1e-6`. `B-P-PRE-CD` `−3.227e-05` y `B-P-DIG-CD` `−2.362e-06` **NO reproducen** (§4). Nada se ajustó hacia atrás.

**Corroboración de diseño que no se buscó:** la rama `SD` reproduce además los conteos de diseño de la enmienda `r2` **al entero** — presencial 381 estratos / 2 996 UPM, digital 362 / 2 518, idénticos a los sellados. Y la familia A reproduce `n = 40 042`, 442 estratos, 9 172 UPM, más las **94** filas fuera de universo que la enmienda declara.

### 2.1 · Hallazgo 1 — «presencial vs digital» deja fuera el 22% del peso

`B-VEREDICTO-CANAL = DICOTOMIA-ES-PROPIEDAD-DEL-RECORTE`.

`P7_3` tiene **ocho** categorías sustantivas. El par presencial `{1}` / digital `{3,4,5}` usa cuatro y deja fuera `2` (**banco, supermercado, tiendas o farmacias**) y `6` (**módulos, clínicas u oficinas temporales o móviles**), que no son residuo: son canales reales y masivos. Medido: **6 588 eventos, `B-P-RESIDUO-CANAL = 0.219818` — el 21.98% del peso de `U_B`.**

Es el mismo hallazgo 3.2 del lote ENVIPE en otra fuente: **la dicotomía es propiedad del recorte, no del instrumento.** La regla `tramite.mordida.con_registro` mapea «digital/registrado ≈ registro_o_testigos» y «presencial ≈ nadie observa»; ese mapeo **no cubre** a quien paga el predial en el banco ni a quien hace el trámite en un módulo móvil, y esos son más de un quinto del peso.

### 2.2 · Hallazgo 2 — el denominador de la familia B no es el que su nombre sugiere

`B-COBERTURA = 0.200895`. De las **124 314** filas de `sec_7`, solo **24 974** tienen pareja utilizable en `sec_8`: **1 062 533 de 1 083 672** filas de `sec_8` traen `P8_4` **en blanco**, porque 8.4 pregunta *«¿en cuál de los trámites se suscitaron **las anteriores circunstancias**?»* y esas circunstancias son las de 8.3.

GEN1 declaró esta reserva en prosa (*«no es p(mordida|canal) sobre el universo completo de trámites»*). **Aquí queda contada:** el estimando es `p(este trámite fue el señalado | trámite de alguien que ya declaró corrupción en 8.3)`, sobre el **20%** de los trámites. No es la prevalencia de mordida por canal, y no debe leerse así.

### 2.3 · Hallazgo 3 — el rótulo `paga_mordida` describe SOLICITUD, no pago

`X-VEREDICTO-PAGO = EL-ROTULO-PAGA-DESCRIBE-SOLICITUD-NO-PAGO`.

Los tres incisos del reactivo 8.3 preguntan si **le solicitaron o insinuaron**; ninguno pregunta si **pagó**. El reactivo que sí mide entrega es `P8_6` (`1 = No le dio nada`). Medido sobre quienes llegan a él (`n = 4 883`): **`X-P-DIO-ALGO = 0.662933`** — dos de cada tres solicitudes terminan en entrega, **una de cada tres no**.

Y dentro del propio 8.3, GEN1 usó **solo el primer inciso**. Los tres juntos dan **`A-P-SOLANY = 0.115702`** contra `0.085118`: **`A-DELTA-SOLANY-SOL1 = +0.030584`**, tres puntos que el coyote (`P8_3_2`) y la insinuación (`P8_3_3`) aportan y que la celda sellada no cuenta. Es un juicio, no un dato — y ahora está medido en vez de heredado.

### 2.4 · Hallazgo 4 — el descriptor está incompleto en la llave, y se comprobó

`G-VEREDICTO-ESTRUCTURA = DESCRIPTOR-INCOMPLETO-LLAVE-REAL-INCLUYE-NT-TIPO`.

El descriptor declara la llave primaria de `sec_6`/`sec_7`/`sec_8` como `CVE_ENT+UPM+V_SEL+R_ELE+N_TRA` y **omite `NT_TIPO`**, pese a definirlo él mismo como *«Número de trámite / Último evento», códigos `01-03`*. Medido: **la llave declarada NO es única — 113 717 grupos para 124 314 filas**; `(ID_TRA, NT_TIPO)` **sí** lo es; `ID_TRA` solo tampoco (**7 430** repetidos); `ID_TRA` en `sec_8` **sí** es única, así que el join es uno-a-muchos exacto.

Esta spec **no adoptó ninguna llave por autoridad** — ni la del descriptor ni la que `MAESTRA35-L1` verificó. Las midió las tres, con la rama `NO-ESTIMABLE-LLAVE-NO-UNICA` pre-escrita por si el join no era exacto. Coincide con `MAESTRA35-L1` en los 7 430, y confirma su diagnóstico desde el descriptor.

### 2.5 · Hallazgo 5 — las vistas del registro estaban desfasadas de la demanda

`PR #662` re-derivó `demanda-*.tsv` con la identidad corregida, pero **no** las vistas `data/corrida0/resultados.tsv` / `corridas.tsv`: **185 de 205** filas citaban un `CORR-*` anterior a la migración (`RES-0021` decía `CORR-0006` donde la demanda ya decía `CORR-0002`). Tras la re-derivación de este acto el desfase es **0/205**. Desaparecen `CORR-0083`…`CORR-0086`: las cuatro filas `DEMANDA` que el colapso 86→82 elimina, con veredicto de replay `NO-CORRIDA` (placeholder, **no** evidencia).

**`NC-0094` · protección de evidencia: SOSTIENE.** Auditadas las **52** celdas con veredicto REAL de replay en `corridas.tsv` antes de `registro --escribe`: **las 52 sobreviven byte a byte**, cero filas ajenas de `resultados.tsv` modificadas. La protección de `PR #660` hace lo que dice.

## 3 · P3 · Adopción y consumo — **esta vez adentro**

`milpa/` **sí** está en el perímetro de este encargo (el lote ENVIPE cerró bloqueado justo por no estarlo). Se escriben **cuatro** citas, con el `p` **intacto** — el patrón de la línea 583: *el `p` no se mueve, se declara de dónde viene*.

| `RES` | consumidor | cita | delta al grano de `milpa/` |
|---|---|---|---|
| `RES-0003` | `paga_mordida_encig2025` | `RESULT-ENCIG-MOR-A-P-SOL1` | `0.0` |
| `RES-0013` | `paga_mordida_encig2025_presencial_r2` | `RESULT-ENCIG-MOR-B-P-PRE-SD` | `0.0` |
| `RES-0015` | `paga_mordida_encig2025_digital_r2` | `RESULT-ENCIG-MOR-B-P-DIG-SD` | `0.0` |
| `RES-0021` | `adopta_encig2025_luz` | `RESULT-ENCIG-MOR-C-P-ADOPTA` | `0.0` |

**Sonda de consumo (solo lectura, patrón §4.1 del cierre ENVIPE): PASA 4/4.** `cargar_reglas() -> 21 reglas`; para los cuatro, `emitir_binaria()` devuelve `valor_punto` **igual** a `round(RESULT, 6)`. El árbol quedó intacto tras la sonda (`git status --porcelain` sin cambios nuevos). **La compatibilidad queda demostrada, no supuesta.**

**Contadores, salida cruda, sin cifra esperada (E.4):**

```
ANTES     N_resultados_gen2_adoptados_activos=2     dependencias_numericas_legacy_activas=203
DESPUES   N_resultados_gen2_adoptados_activos=6     dependencias_numericas_legacy_activas=199
```

### 3.1 · Los ocho que NO reciben cita, y por qué

- **`RES-0009` / `RES-0011`** (base, rama deduplicada): `NO-ADOPTABLE-POR-GRANO`, `−3.227e-05` y `−2.362e-06`. **No reproducen** al grano de seis decimales. Escribirles cita los presentaría como replicados cuando no lo están.
- **Los seis complementos** (`RES-0004/0010/0012/0014/0016/0022`): `COMPLEMENTO-CON-DENOMINADOR-RECORTADO`. El residuo de su par pesa `> 0` en las tres familias — **0.002258** (A: `P8_3_1 = 9`), **0.219818** (B: canal), **0.011176** (C: `P7_3 ∈ {3,7,8,9}`). Ninguno es «el complemento medido»: es `1 −` el primario sobre un denominador que excluye categorías reales del reactivo. Patrón `NC-0085`, heredado del lote ENVIPE y aquí aplicado por criterio **pre-declarado antes de medir**, no elegido a posteriori.

Aviso para quien los adopte después: `rechaza_servicio_encig2025_luz` (`RES-0022`) significa **«usó un canal físico»**, no «rechazó un servicio digital». El `alcance` de la regla ya lo estampa.

## 4 · Lo que de verdad separa la ronda base de la `_r2` — la premisa del encargo, corregida

El encargo pide declarar *«qué distingue la ronda base de la `_r2` (dos rondas del cuestionario)»*. **ENCIG 2025 tiene un solo cuestionario y un solo reactivo `P8_4`.** No hay dos rondas. Lo que separa las dos cifras selladas es la **deduplicación**:

- **`CD`** (base, `RES-0009`…`0012`) deduplica `sec_7` por `ID_TRA`; **`SD`** (`_r2`, `RES-0013`…`0016`) no.
- Medido aquí: la deduplicación borra **2 105** eventos del universo de medición.
- `SD` es la **primaria de esta spec por el codebook**, no por GEN1: el descriptor define `NT_TIPO` precisamente para distinguir eventos repetidos del mismo tipo hechos por la misma persona. Colapsarlos borra lo que el instrumento captó a propósito.

Por eso **ningún `_r2` sale `NO-CONSTRUIBLE`** y la decisión no sube a mesa por esa vía: los cuatro son construibles y los cuatro se midieron. Lo que sí sube es otra cosa — **la rama `CD` no se reproduce a `1e-6`** desde el procedimiento que esta spec declaró (`n = 9 942` y `6 339` contra las `n = 9 937` y `6 337` de la enmienda: 5 y 2 eventos de diferencia). La regla de desempate de `MAESTRA34-L1` para los `ID_TRA` cuyas filas **difieren en `P7_3`** (501 de los 7 430, según su propia nota) no está escrita en ningún artefacto reproducible. **Se reporta; no se adivina y no se ajusta.**

## 5 · El guardián que no habría guardado — `ya_medido.py`

Las tres reglas de este acto están medidas y selladas en `milpa/tramite.yaml`, y `tools/ya_medido.py` devuelve **`NUNCA-MEDIDA` para las tres**. Verificado contra el código, no supuesto:

1. **`_tiene_veredicto_real()` no reconoce `MEDIDO`.** Solo acepta los diez veredictos de falsación `R` o un campo `veredicto:` con valor. Una regla medida como **tasa base** —el patrón de todo el lote F4→F3— no deja ninguna de esas marcas.
2. **La ventana de ±260 caracteres pierde el veredicto que sí existe.** En `tramite.gobierno_digital.util_sin_coercion` el bloque mide 8 946 caracteres y trae `NO-DISCRIMINA` en el desplazamiento 5 472; `_ventana_de_terminos()` recorta a `[0, 268)` y no lo ve. Falso negativo **incluso bajo la semántica estrecha del propio script**.

`T-YAMEDIDO` existe para que ningún acto llame «territorio virgen» a una regla ya medida. Para estas tres, **el guardián habría dejado pasar exactamente ese error.** Este acto no repara `ya_medido.py` — fuera de perímetro. Queda como fila `NC` con sucesor.

## 6 · Límites declarados

- **Geográfico y poblacional.** 82 áreas urbanas de 100 mil habitantes o más, 18 años y más. **Ningún estimador es nacional.**
- **Temporal.** ENCIG 2025, referencia 2025. Las siete olas de `serie_olas` no se tocaron ni se promediaron.
- **Causalidad: ninguna.** `B-DIFERENCIA-PRE-DIG-SD = 0.111173` y `B-RAZON-PRE-DIG-SD = 4.7222` van rotuladas **`ASOCIACION`**: la elección de canal y la elegibilidad por canal confunden la comparación — quien puede hacer un trámite por internet no es una muestra aleatoria de quien lo hace en ventanilla. La regla `falsable_si` **no** se declara probada.
- **IC como límite inferior.** En la familia B, **71** (presencial) y **78** (digital) estratos quedan con una sola UPM; en C, **8**. `METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite inferior de la anchura verdadera**. La familia A no tiene ninguno: su IC es limpio.
- **Ranura no pre-registrada.** Nadie había pre-registrado el método de IC para estas series. Lo eligió el ejecutor sobre ranura vacía, declarado en §3.7 de la sellada, y **se eleva a mesa**.
- **Contaminación (ADR-46).** La corrida **no fue ciega**: al congelar, la sesión ya había leído los doce valores GEN1, sus IC95, sus `n` y **la codificación GEN1 completa**. Está declarado en §0.3 de la sellada y es la razón de que las primarias sean `SOLANY` y `SD`. Lo genuinamente desconocido al congelar —y lo que resultó ser el hallazgo— eran los pesos residuales, la cobertura del join y la unicidad de las llaves, que no aparecen en ninguna fuente leída.

## 7 · Contador

`cuenta_gen2` de `CALC-ENCIG-0001` queda en **`SI`**. A diferencia del lote ENVIPE, la firma que ordena este lote **sí tiene como objeto el contador**: el encargo trae, verbatim, *«cuenta_gen2 = SI para el CALC que este acto selle»*. Estándar `FP-367/368` satisfecho (autoridad + fecha + **OBJETO**). El merge de mesa la perfecciona.

**ADENDA (5) · asiento `NC-0097`:** se escriben además las tres filas de `cuenta_gen2=SI` de los `CALC-R` del CSV (`CALC-R-CIV-M-10`, `CALC-R-CIV-M-12`, `CALC-R-CIV-M-13`) citando la firma embebida en el encargo del `ACTO GEN2-R-SERIE-CSV` y su merge (`PR #657`) — **asiento, no re-firma**. Consecuencia mecánica que la propia fila `NC-0097` predijo y que aquí se verifica: `motivo_cuenta_gen2` de los tres pasa de *«etiqueta de la spec»* a *«decisión de mesa (`decisiones.tsv`)»*, así que las vistas se re-derivaron **después** de escribir `decisiones.tsv`. `NC-0097` **CIERRA**. `NC-0103` (trío DBF) **no** es de este acto y sigue abierta.

## 8 · A.13 — qué se examinó

**Microdato: 3 archivos**, abiertos por primera vez en el COMMIT-2, nunca antes de congelar — `encig2025_01_sec1_A_3_4_5_8_9_10.csv` (40 136 filas), `encig2025_04_sec_7.csv` (124 314), `encig2025_05_sec_8.csv` (1 083 672).
**Codebook y metadato (COMMIT-1):** el manifiesto (1 entrada, `sha256` verificado en la caja), el descriptor `encig25_estructura_base_datos.pdf` (4 540 líneas extraídas), la lista de 6 miembros del ZIP, `data/inventario-reactivos-v1_2.tsv` (477 filas de este payload, 6 miembros), `milpa/tramite.yaml` y `data/corrida0/demanda-*.tsv`.
**`forense/prereg-caja/`:** directorio completo, **0** aciertos de `encig` (negativo con universo declarado).
**Contrato del medidor:** verificado contra **fixture sintética** antes de tocar el payload — 108 declarados = 108 emitidos, cero huecos.
**Suite:** `python3 tests/check.py --baseline` → **VERDE**, 3 `FAIL` de línea base, ninguno nuevo.

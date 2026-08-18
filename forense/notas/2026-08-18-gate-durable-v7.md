# Nota del acto · ACTO GATE-DURABLE-V7 — el predicado, la reejecución y la muestra que faltaba

**Fecha:** 2026-08-18 · **Rama:** `gate-durable-v7` · **Base al arrancar:** `origin/main = ae25137` (merge de `#255`)
**Base al cerrar:** `origin/main = 93a4dd9` (merge de `#256`, INTEGRATE-T23), integrado por merge local
**ADR:** `ADR-103` · **PR:** ver cierre

---

## 1 · ARRANQUE

```
1 · REPO     /home/pc0/Modelado-Mexicano-barrido2 · rama gate-durable-v7 · arbol limpio
             PR #255 verificado MERGED (mergedAt 2026-08-18T19:21:40Z, merge ae25137)
2 · SHA      encargo declaraba 3e4c9f7; main real ae25137 (avance limpio: 3e4c9f7 es su ancestro)
3 · .barrido2 19G · snapshot-v4.json y ledger-v7.tsv presentes · tasks-v7 y staging-v7 presentes
             data/raw/ montado (20260813130000.export.CSV.zip)
4 · ENTORNO  [sin_variable] · 200 · corpus montado
             unshare -Urn probado: namespace OK y SIN salida a red, por sonda y no por ausencia
5 · ESPEJO   aceptado
```

**El ARRANQUE 1 fue PARO y se reportó como tal.** La primera vez que este encargo se leyó,
`PR #255` seguía `OPEN` (`mergedAt: null`), y su propio ARRANQUE ordena parar en ese caso.
No se continuó. Lo que desbloqueó la fusión fue el `COMMIT 0` de este mismo encargo,
ejecutado sobre la rama de `#255` — desviación de secuencia declarada en la enmienda in situ
de `ADR-98` y en la §7 de `forense/notas/2026-08-18-b2-v7.md`, forzada por una dependencia
circular medida: `#255` estaba `MERGEABLE` pero `BLOCKED` porque su job `check` fallaba **por
dos entradas y nada más** (log crudo de la corrida `32174058312`), y este encargo exige `#255`
fusionado para arrancar.

---

## 2 · Por qué el gate estaba roto — arqueología, no diagnóstico heredado

El encargo traía el diagnóstico hecho y pedía no repetirlo. Se re-derivó igual, porque la
pregunta que ningún documento contestaba era **por qué funcionaba antes**. La respuesta cambia
la lectura del defecto:

| momento | qué | gate |
|---|---|---|
| `ledger-v2` · `ledger-v5` (17/ago 21:13) | escritor y validador **igual de romos**: los dos redactaban el metadato de máquina | **672/672 VERDE** |
| **`abb978a` · 17/ago 22:33** | «la redacción deja de tratar metadatos de máquina como datos de persona» — mete `safe_text_compuesto` + `CAMPOS_MAQUINA` y los aplica **sólo al escritor** (`+187/+188/+189`); **no toca una línea del bloque PII del validador** | — |
| `ledger-v6` · 23:59 | primera corrida con los dos lados divergentes | 273/672 |
| `7ef2c0f` (contenido 00:03) | `exento_estructural()` — unifica el eje **estructural** | — |
| `ledger-v7` · 18/ago | sigue partido el eje **durable** | 296/672 |

**No era un bug oscuro: era media reforma.** Conservar `codigo_hex` y `crc` **es** el entregable
del bloque 2 — las cifras 1 y 2 de `ADR-98` —, así que `abb978a` hizo lo correcto en un lado y
dejó el otro sin enseñar. `7ef2c0f` arregló un eje distinto, y por eso no destrabó nada.

---

## 3 · El arreglo

**El validador deja de tener regla propia.** `activa_pii_compuesto(t)` es literalmente
`safe_text_compuesto(t)[1]` — no una copia equivalente, la misma función. Una copia se
desincroniza; una llamada no puede. Se aplica a los **tres** campos compuestos y sólo a esos
tres — `definicion`, `categorias`, `value_labels` —, que son exactamente los que el escritor
emite con `safe_text_compuesto`. `categorias` tiene cero activaciones medidas y entra igual:
lo que evita la próxima divergencia es que la lista espeje al escritor, no que cubra sólo lo
que ya dolió.

**Una distinción nueva que hace seguro el mecanismo: MÁQUINA ≠ ESQUEMA.** Un campo de máquina
se conserva **verbatim** (`crc` lo calcula `zipfile`, no puede contener a una persona). Uno de
esquema se exime **por FORMA**, la misma exención que `nombre`/`hoja`/`tabla` ya reciben. La
única llave de esquema medida es `variables`, y la diferencia no es teórica: en los `.dta`
electorales de Veracruz **cada candidato es una columna**, así que un nombre de variable
**puede** ser el nombre de alguien. `variables=EST_DIS` sobrevive; `variables=RAÚL GONZÁLEZ
GARCÍA` se redacta. Sin esta clase, satisfacer el control N1 habría destruido 168 registros de
nombre de variable SPSS.

Ambas clases van declaradas en el mismo producto durable, columna `clase` de
`campos-maquina-barrido2.tsv`, retrocompatible: un contrato sin la columna se lee como
`MAQUINA`, que es como nació el archivo. La guarda que rechaza `label` cubre **las dos**.

---

## 4 · Lo que la revisión adversarial encontró, y por qué se paró la corrida

La primera versión del arreglo se lanzó a corrida completa. A los 23 minutos (W3 125/396) llegó
la revisión adversarial —32 agentes, cinco lentes independientes más un refutador— con cuatro
defectos. **Tres eran del arreglo mismo.** Se paró en vez de dejarla terminar: pagar 67 minutos
una vez, no dos, y uno de los tres era una fuga de privacidad.

| # | defecto | de quién | cómo se cerró |
|---|---|---|---|
| 1 | `=calle;=5` → el escritor producía `calle;5`, que al revalidarse cae por la rama plana y activa el patrón de domicilio: **el gate rechazaba un expediente recién escrito** | del arreglo | un segmento no redactado sale **verbatim**; no se reconstruye |
| 2 | `ENT = 15` → `ENT=15`; y como sólo se parte por el PRIMER `=`, `(5.6 = 3 Y 5.8 = 7)` → `(5.6=3 Y 5.8 = 7)`, mutilado de forma inconsistente | del arreglo | mismo arreglo que (1) |
| 3 | `tipo=NUMERICO;crc=Ana Maria Lopez` sobrevivía verbatim — **fuga de PII**, y el validador viejo sí la cazaba (`PII_PATTERNS[7]`) | del arreglo | la exención verbatim exige que el **valor** tenga forma de máquina, no sólo la llave |
| 4 | `objeto_tipo` redactado en **1 650 224 de 1 833 802** filas durables (89.99 %) | preexistente | exención por forma de vocabulario, en predicado propio |

El (1) merece nombrarse sin adorno: **es la misma clase de defecto que este acto existe para
cerrar, reintroducida por comodidad de formato.** Que la encontrara una revisión adversarial y
no la corrida es la única razón de que no costara un tercer ciclo.

El (3) se cerró por **clase, no por emisor**: el emisor concreto existe
(`barrido2_material.py:1839` interpola los bytes crudos del bloque `<formats>` del `.dta` sin
`safe_text`), pero exigir forma de máquina al valor cierra también los emisores que nadie ha
auditado todavía.

El (4) es preexistente y se arregló con autorización de mesa en el acto. El daño no era sólo de
lectura: `write_barrido2_material.py` agrupa por esa clave, así que **clases distintas se
fusionaban en una sola fila publicada**. El predicado vive aparte a propósito — ensanchar
`exento_estructural()` para arreglar un cuarto campo habría relajado `nombre`/`hoja`/`tabla` de
paso, que es justo el error que este acto cierra. Medido contra el vocabulario real: **52 de 52
tipos distintos sobreviven**, y `RAÚL GONZÁLEZ GARCÍA` como tipo se sigue redactando.

**Y un defecto de operación, propio, que casi cuesta la corrida entera.** El primer intento de
matar la corrida usó `pkill -f "correr-olas-v7.py"`, que coincidió con la propia línea de
comando del shell y **mató el shell, no el driver**. Durante 24 minutos corrieron **dos
drivers** sobre el mismo `staging-v7`. Se detectó porque una línea del log decía `2321s` cuando
la corrida nueva llevaba 14 minutos. La regla que queda: **la muerte de una corrida se verifica
por la distribución de `build_sha256` en staging, no por el código de salida de `pkill`.**
Efecto colateral medido y benigno: el driver lanza un proceso por tarea, así que cada
subproceso importa el módulo tal como está en ese instante — hubo cuatro `build_sha256` en
vuelo, y la corrida final los barrió todos.

---

## 5 · Los controles y la prueba de vuelo

Ocho controles, seis del encargo y dos de la clase esquema. Salida cruda:

```
P1  crc=2719796586;zip_slip=NO             -> crc=2719796586;zip_slip=NO               red=False
P2  codigo_hex=0000000000c05840;label=Sí   -> codigo_hex=0000000000c05840;label=Sí     red=False
N1  label=RAÚL GONZÁLEZ GARCÍA             -> label=[REDACTADO-PRIVACIDAD]             red=True
N2  codigo_hex=abc;label=555 812 4930      -> codigo_hex=abc;label=[REDACTADO-PRIVACIDAD] red=True
N3  8711234567                             -> [REDACTADO-PRIVACIDAD]                   red=True
N4  telefono_contacto=8711234567           -> telefono_contacto=[REDACTADO-PRIVACIDAD] red=True
E1  variables=EST_DIS;categorias=4         -> variables=EST_DIS;categorias=4           red=False
E2  variables=RAÚL GONZÁLEZ GARCÍA         -> variables=[REDACTADO-PRIVACIDAD]         red=True
```

**La prueba de vuelo que faltaba la primera vez.** Antes de relanzar se corrió el invariante
—*el validador acepta todo lo que el escritor escribe*— sobre **116 712 valores compuestos
distintos del índice real**: **0 rupturas**. Eso es lo que convierte «espero 672 terminal · PII
0 · rc=0» en algo apostable en vez de una esperanza.

Y el **remedio de método** del encargo, aplicado dos veces: cuatro expedientes de ida y vuelta
completa antes de lanzar las olas (1 669 registros, 0 marcados), y el gate contra cuatro
expedientes antes del gate completo (0 errores, `matches_task=True` en los cuatro).

---

## 6 · La secuencia real corrida

| # | paso | resultado |
|---|---|---|
| 1 | congelar el `MATERIAL_BUILD_SHA256` | `4cc055a9…` → **`a8f7a548aca68db2d12d2b450dbadac593a5a81cc2b9b3588a02a7e6ca798db7`** |
| 2 | las cuatro olas | **672/672 ok · 0 fallas · 4 148 s** (W1 26/11 s · W2 246/468 s · W3 396/3 304 s · W4 4/367 s) |
| 3 | segundo `--barrido2-materialize` **con** `--staging-root` | `{"W1":26,"W2":246,"W3":396,"W4":4,"ok":true,"tasks":672}` |
| 4 | gate `validate.py --barrido2-material --require-complete` | **`ok:true` · 672 · 1 833 802 registros · 0 errores · `rc=0`** |
| 5 | W0 | `ok:true` · censo 627 · ledger 672 · fuera_de_disco 0 |
| 6 | material | `ok:true` · 672 representaciones · 1 833 802 registros · 2 717 reportes durables |
| 7 | productos durables | ledger durable **672 E2** · PRISMA ya no `PRELIMINAR-W0` · `index_sha256 6e87c034…` · `report_sha256 d7cba83f…` |

Respaldo del ledger antes de cada paso destructivo (`.pre-gate-durable.bak`, `.pre-mat-gd.bak`),
con su sha.

**Todos los 672 expedientes con el mismo build `a8f7a548aca6`** — verificado tras la corrida, así
que el riesgo de build mixto que dejaron los dos drivers no se materializó.

---

## 7 · Contadores de aparato movidos

| contador | antes | después |
|---|---|---|
| ledger terminal | 296 / 672 | **672 / 672** |
| activaciones PII falsas | 150 814 · 376 expedientes | **0 · 0** |
| errores del gate | 14 380 | **0** |
| `objeto_tipo` vivo en el producto durable | 183 578 / 1 833 802 (10.01 %) | **1 833 802 / 1 833 802 (100 %)** — y 2 717 / 2 717 en el TSV publicado |
| exigencia 4 del §15 (muestra adversarial) | insatisfecha | ver §9 |

**Contadores de medición sobre México: cero.** `13 de 27` · `11 de 15` · `0 de 15` · `1 de 2` ·
`4 de 144`, ninguno se mueve. Este acto arregla el aparato; no mide México.

**Corrección de cifra que arrastraba desde `#255`.** «13 953» es el número de **errores que
reporta el gate**, no de activaciones: `fail()` topa en 200 por expediente. Las cifras reales son
**23 281 registros afectados y 150 814 activaciones** sobre 376 de 672 expedientes. `ADR-98` y la
especificación de `#255` usan la cifra del gate; aquí se usan las reales y se declara la
diferencia en vez de reescribir el sello viejo.

---

## 8 · Las tres cifras, re-selladas contra el universo nuevo (A.10)

El procedimiento congelado en `COMMIT A` de `#255` se corrió **tal cual** —`sha256`
`94e0b5ebdd9fb6b5c5c241aef28fcde2d5c95f46e513f764895a35af7e75a7aa`, verificado idéntico antes de
invocarlo— contra el índice de esta generación.

| # | cifra | `#255` | esta generación |
|---|---|---|---|
| 1 | value labels de SAV conservados | 129 318 / 135 262 = 95.61 % | **idéntico** |
| 1-bis | contraste DTA | 103 161 / 103 712 = 99.47 % | **idéntico** |
| 2 | metadatos de miembro ZIP enteros | 25 713 / 25 713 = 100.00 % | **idéntico** |
| 2-ter | miembros con `zip_slip=SI` | 5 | **idéntico** |
| 3 | PDF cifrados que abrieron | 313 / 313 | **idéntico** |
| 3-bis | PDF abiertos, universo completo | 628 / 630 | **idéntico** |

**Estampa nueva:** generación `v7` · build `a8f7a548aca6` · 672 expedientes · 1 833 802 registros ·
worktree `50c9c31`. El sello de `#255` **no se edita**: queda como historia contra su propio
universo, y éste lo renueva contra el nuevo. Que las seis cifras reproduzcan exacto es un
resultado, no una casualidad: los arreglos tocan el validador y el `objeto_tipo` del producto
durable, no el contenido que las cifras miden.

---

## 9 · La muestra adversarial

Congelada en `e8ae840` **antes de que existiera el dato que la refutaría** — las olas estaban
corriendo mientras se escribía ese commit. Integridad verificada al usarla:
`sha256 31afb11561b656c570997d83b5601117916116213a00979dc035ea8e80fc6b5c`, idéntico al congelado.

Regla del §12, derivada y no tecleada: por ola `max(3, ceil(5 %))`, tope 20.

```
W1  poblacion 26   cupo 3    W2  poblacion 246  cupo 13
W3  poblacion 396  cupo 20   W4  poblacion 4    cupo 3      total 39
razones: PRIMER-LOTE-DE-LA-OLA 12 · FORMATO-COMPLEJO 27
semilla declarada: "3e4c9f7" — el SHA de redacción del encargo, reproducible desde el
propio expediente forense; el sorteo es hash(semilla ‖ tarea_id), sin random
```

**Veredicto: 39 de 39 `COINCIDE`. `rc=0`.**

Las 39 tareas se **re-inspeccionaron de forma independiente** en un staging aparte, con el
mismo módulo y el mismo contrato, y se compararon `report_sha256` e `index_sha256` contra el
expediente sellado. Reparto real: W1 3 · W2 13 · W3 20 · W4 3; por razón de selección, 12
`PRIMER-LOTE-DE-LA-OLA` y 27 `FORMATO-COMPLEJO`. `build_sha256` idéntico en las 39, en los dos
lados. Cero `NO-COINCIDE`, cero `NO-REINSPECCIONABLE`, así que el protocolo del §12 —cuarentena,
ampliar muestra, repetir lote— no se activó.

**La exigencia 4 del §15 queda satisfecha, y es la primera vez.** Lo que estaba abierto no era
que los hashes difirieran: era que la muestra sellada venía de `snapshot-v2` y, como
`tarea_id = sha256(snapshot ‖ representacion ‖ contrato)`, **ninguna de sus 41 tareas existía**
en la generación sellada. No había nada que rehashear; había que volver a sortear. Eso es lo que
`e8ae840` hizo, y contra el build correcto.

**Lo que este veredicto NO dice.** Prueba que el inspector es **reproducible**, no que su
contenido sea semánticamente correcto. Una inspección puede reproducirse perfectamente y estar
equivocada. Reproducibilidad es lo que el §15.4 exige y es lo único que este comparador cierra.

---

## 10 · Lo que este acto NO hizo

- **No corrió `--freeze`.** Prohibición explícita del encargo.
- **No tocó `integrate_barrido2.py` ni `tests/check.py`** — carril de nube, `ACTO INTEGRATE-T23`,
  fusionado como `#256` mientras esto corría. Cero archivos en común, verificado por diff.
- **No arrancó C4-semántico, C5 ni C6**, ni corrigió capa 4 de las 17 (exige la vía del §19).
- **No arregló el driver.** `correr-olas-v7.py` escribe `olas-v7.log` y `olas-v7-resumen.json`
  junto a sí mismo, o sea dentro del repo; se sacan del índice en cada corrida y el defecto queda
  declarado. No se toca porque su `sha256` (`ef5026f7…eaf22`) es lo que prueba que lo archivado es
  lo que corrió.
- **No cerró los riesgos vivos que la revisión adversarial dejó nombrados**, listados en el ADR.

---

## 11 · El delta 17→19 de `INDEXADO-NO-DESCARGADO`, derivado

El encargo pide saber si las 2 extra son de M-APERTURA o de otra cosa, porque la fase semántica
lo necesita sabido. Derivado de `relaciones.tsv` y de la lista de apertura, por identidad exacta:

```
filas de relaciones.tsv con capa4_apertura_mapeo = INDEXADO-NO-DESCARGADO:  19 de 199
  en la lista M-APERTURA CON payload (las 17):   17
  en la lista M-APERTURA SIN payload:             2
  ajenas a la lista por completo:                 0
```

**Las 2 extra sí son de M-APERTURA**, pero del subconjunto que la propia lista marca
`en_manifiesto=NO` / `destino=PROPUESTA-A-COLA`: `REL-0ccb1f487408f4999004b321` (`N24`,
`REPORTE_SOBRE_USO_Y_CONFIANZA_DE_SERVICIOS_FINANCIEROS_DIGITALES`) y
`REL-0e3c2a3a6afd1dae2297740e` (`N21`, `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND`).
Las dos declaran «no hay payload local de ninguna clase».

**Consecuencia para la fase semántica:** no son el mismo problema que las 17. Las 17 infringen
§18.8 porque su payload **fue observado** y la celda sigue cerrada — se cierran por evidencia.
Estas 2 no se pueden cerrar por observación porque no hay nada que observar: necesitan
adquisición, y su destino ya lo dice. Ningún acto semántico debe contarlas en el mismo
denominador que las 17.

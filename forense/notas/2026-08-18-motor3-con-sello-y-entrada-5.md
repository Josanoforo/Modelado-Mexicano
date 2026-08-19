# ACTO LANE-A-E0-E5 · la fase CON SELLO de MOTOR-3/E0, corrida — y la Entrada 5, cerrada

### 18 de agosto de 2026 · `cloud_default`, repo-only · base real `f3d3f95` · encargo `forense/encargos/2026-08-18-LANE-A-E0-E5.md`

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-18-motor3-con-sello-y-entrada-5.md` |
> | **QUÉ ES** | El detalle, comando por comando, de las dos mitades del encargo: la fase CON SELLO de `MOTOR-3/E0` (C1 catálogo · C2 rebanada · C3 cierre) y la Entrada 5 de `registro-recalculo`, con `FP-15` cerrada |
> | **QUÉ NO ES** | No es una medición. **Contadores de medición sobre México movidos: 0.** El único contador que nace es del programa: *momentos HOLDOUT reproducidos: 0 de 14* |
> | **VERIFICAS ASÍ** | Cada cifra trae su comando o su ancla derivada HOY. Donde el encargo, el plan de 14/ago o el lanzamiento discrepan del terreno, §7 lo dice con las dos cifras a la vista |

---

## 0 · ARRANQUE

1. **REPO.** Clon en `/home/user/Modelado-Mexicano`, rama `claude/launcher-lane-a-forense-ju9xg0`. Árbol limpio al iniciar.
2. **SHA — y la trampa que casi se traga el arranque, la misma que `ACTO MESA-18AGO` documentó.** `git rev-parse origin/main` **antes** de fetch devolvía `f8eb2e3` (`PR #182`), una referencia remota rancia del clon. `git fetch origin main` la corrigió a **`f3d3f95`** (`Merge pull request #263`, `ACTO COND-ATRIB`), que coincide con `HEAD` y del que la rama de trabajo es descendiente (`git merge-base --is-ancestor origin/main HEAD` → 0). **La base real de este acto es `f3d3f95`.** El SHA de redacción del encargo (`93a4dd9`) y el que el lanzamiento citó (`57984b5`) quedaron ambos atrás; se derivó, no se heredó, exactamente como el lanzamiento pedía.
3. **`data/raw`.** No se usó: este acto no abre microdato. Perímetro repo-only.
4. **ENTORNO.** Nube (`cloud_default`), como asigna el encargo. Sin red nueva más allá de `git fetch`.
5. **ESPEJO.** Ninguno. Toda cifra sale del clon, con comando o `archivo:línea`.

---

## 1 · El gate maestro, re-corrido — y el defecto de su propio predicado

El encargo de `MOTOR-3/E0` trae el gate escrito así:

```bash
grep -cE "^\*\*ADR-8[4-9] .*(motor|matriz|M1)" canon/gobernanza-v1_15.md
```

**Ese predicado ya no puede dar `≥1` aunque el sello exista**, y la razón es aritmética: sólo casa ADR de **dos** dígitos en el rango 84-89. `ADR-100` —el ADR que sella `ADR-MOTOR-2`— tiene tres dígitos y le es invisible. El encargo de `LANE-A` ya traía el rango corregido, y es el que se corrió:

```bash
$ grep -cE "^\*\*ADR-(8[4-9]|9[0-9]|10[0-9]) .*(motor|matriz|M1)" canon/gobernanza-v1_15.md
1
```

**`1 ≥ 1` = SELLADO.** El único que casa es `ADR-100` (`gobernanza:1811`), que cita "motor", "matriz" y "M1" en su propio título. **Se declara el defecto en vez de sólo saltarlo:** un gate escrito con un rango cerrado de dos dígitos caduca en silencio cuando el contador de ADR cruza los 100, y "caducar en silencio" es la clase de defecto que este programa persigue. El predicado del 14/ago habría devuelto `0` hoy —con el sello puesto— y habría vuelto a partir el acto en dos por segunda vez.

---

## 2 · C1 · El catálogo, constituido ANTES de escanear

**Producto:** `milpa/catalogo-momentos-v0_1.md` + `milpa/catalogo-momentos-v0_1.tsv`. Roles `rol_calibracion` **sellados en ese commit**, que es anterior en historia de git al commit del motor — `tests/test_motor_holdout.py::test_c` lo verifica por `git merge-base --is-ancestor`, no por declaración.

**Enumeración, y la regla que la vuelve pre-registro.** La regla de reparto se fijó **antes** de mirar el contenido de ninguna fila, y es función del **tipo de objeto**, no de su contenido: un objeto que es una predicción pre-registrada del Hito D (`R*`) es `HOLDOUT` —es exactamente lo que no puede usarse para ajustar sin destruir su valor probatorio—; todo lo demás es `AJUSTE`. Derivado por comando del libro de demanda (fuente única, M5):

```bash
$ awk -F'\t' 'NR>1 && $2 !~ /^G[1-6]\./ {n++} END{print n}' \
    data/curacion-registro/necesidad-objeto-modelo.tsv
22
```

De las 37 filas del libro se excluyen las 15 de coeficiente de generador —son demanda sobre `B`/`Θ`, lo que el ajuste *consume*, no lo que el motor *reproduce*—. Quedan **22 momentos: 8 `AJUSTE` · 14 `HOLDOUT` · 0 `DIAGNÓSTICO`**.

**Los cortes por eje (M2), sellados donde se puede y declarados donde no.** `ADR-100(2)` da el sello a este catálogo. Se ejerció con una regla: **se sella el corte que el propio instrumento ya trae en catálogo; no se inventa el que exige una decisión de datos nueva.** Sellados 4 (formalidad `segsoc`, urbanización `tam_loc`, ingreso `est_socio`, acceso digital); **PENDIENTE 2** (edad y migración) citando `FP-53`, que ya tiene abierta exactamente esa deuda —*"definir el corte exige dato mexicano propio y es acto por sí mismo"*—. Sellar aquí un corte de edad habría sido producir cifra nueva al canon por la puerta de atrás.

**Los tres ejes de hogar, respetados con dientes.** Urbanización, ingreso y acceso digital son coordenadas compartidas por todas las personas del hogar (`canon/modelo-decision-v4_0.md` §1.1.A). `milpa/src/celdas.py` rechaza **al construirse** —no al usarse— todo corte que pretenda contraste intra-hogar en esos tres. Un contrato que sólo se comprueba en el punto de uso ya se violó varias veces antes de fallar.

**Contador nuevo del programa, nacido aquí:** *momentos HOLDOUT reproducidos: **0 de 14***.

---

## 3 · C2 · La rebanada que corre

**Producto:** `milpa/src/` (10 archivos) + `tests/test_motor_*.py` (6 suites) + `tests/_motor_arnes.py`.

Cifras **derivadas por corrida**, no heredadas del plan del 14/ago:

| | Plan 14/ago | Corrida hoy |
|---|---|---|
| campos `clase:` en `procedencia.yaml` | 17 | **18** |
| entradas cargadas por el loader | — | **37** (19 `ASIGNADO` + 10 `MEDIDO·PARCIAL` + 5 `MEDIDO·β̂` + 2 `MEDIDO·NACIONAL` + 1 `GATE·ID`) |
| contador de condicionales medidas (fórmula T19b) | `10 de 15` | **`12 de 15`** |
| celdas no-cero de `B` | 15 | **15** (14 puntuales + 1 `SIN MAGNITUD`) |
| ancla de `asignados_coeficiente.detalle` | `:705-716` | **`:794-800`** (derivó otra vez) |

**Segundo hallazgo de forma, y es de los que cambian el diseño:** **dos de las siete clases no aparecen NUNCA como valor de un campo `clase:`.** `ASIGNADO` es la clase del **bloque** (`asignados_probabilidad`, `asignados_coeficiente`) y vive en el nombre del bloque y en sus comentarios, no en los datos. Un cargador que sólo buscara `clase:` reportaría **cero** entradas `ASIGNADO` en un archivo cuyo propio diagnóstico dice, textualmente, que *"los 15 coeficientes son todos ASIGNADO"*. La correspondencia se declara **explícita y auditable** en `milpa/src/procedencia.py` (`BLOQUES_CON_CLASE_IMPLICITA`), no se infiere del nombre del bloque en tiempo de ejecución: inferirla haría que un bloque nuevo entrara al motor sin que nadie lo decidiera.

**El contrato de clases, ejecutable.** Las cinco reglas del insumo 3 son código, con su test cada una: `MEDIDO·NACIONAL` lanza `SegmentacionProhibida`; `MEDIDO·PARCIAL(x)` lanza `EjeNoDeclarado` fuera de sus ejes; `ASIGNADO` devuelve punto con `banda=None` y `deuda="dispersion_no_declarada"` —**nunca fabrica un intervalo**, porque la banda no existe en el archivo (§7.1)—; `GATE·ID` lanza `GateDetiene` (*el gate detiene, no estima*); `PENDIENTE` se carga, se registra y no consume.

**Las tres celdas-semilla, corridas con su estado declarado.** Producen **veredicto de estado, no número**:

| celda-D | `estado_operativo` | veredicto (vocabulario A.4) |
|---|---|---|
| `G5.familismo_obligacion.actitud` | `LISTO` | **`EXISTE-NO-SATISFACE`** — `G5 × familismo_obligacion` es `SIN MAGNITUD`; el check obligatorio de `ADR-30` persiste inejecutable bajo la matriz (defecto **M1** de `RONDA-M`) |
| `G5.obligacion_medida.conducta` | `LISTO` | **`EXISTE-NO-VERIFICADO`** |
| `G5.radio_confianza.encuci_vs_enbiare` | `LISTO` | **`EXISTE-NO-VERIFICADO`** |

**Corrección al plan del 14/ago, declarada:** ese plan da la tercera celda por `estado_operativo: PENDIENTE`. **Hoy las tres están `LISTO`** — `G5.obligacion_medida.conducta` la resolvió `ACTO PROD-P638` el 13/ago (*"RESUELTO 13/ago/2026, ACTO PROD-P638"*, `:143` del propio YAML). El plan no se equivocaba al escribirse; la cifra venció. Se re-derivó por lectura, no se heredó.

**El muro del holdout, con tres verificaciones y no una** (`tests/test_motor_holdout.py`): (a) la firma de roles del árbol es idéntica a la del **commit de sello**, leída con `git show <sha_C1>:milpa/catalogo-momentos-v0_1.tsv` — si alguien reasignara un rol después de sellar, esto lo ve; (b) ningún valor `HOLDOUT` se lee, y la rebanada completa termina con los 14 intocados; (c) el commit del catálogo es ancestro del commit del motor. Hay una cuarta, estructural: **ninguna fuente de `milpa/src/` fuera de `momentos.py` menciona el catálogo**, para que el muro no se pueda rodear leyendo el TSV por cuenta propia. Se comprueba sobre el código **sin comentarios ni literales** (`tokenize`), porque si no, un docstring que menciona el tema hace fallar la prueba por hablar de él.

**Determinismo:** misma semilla ⇒ mismo hash, intra proceso **y entre procesos** con `PYTHONHASHSEED=random` — el orden de un `set` puede variar entre procesos y no dentro de uno, y probarlo sólo intra-proceso deja pasar justo ese defecto. Más una prueba estructural de que ninguna fuente usa reloj ni azar.

**Suites, corridas:**

```
T-MOTOR-CLASES:        10 ok · 0 saltadas
T-MOTOR-PROCEDENCIA:    7 ok · 0 saltadas
T-MOTOR-MATRIZ:         7 ok · 0 saltadas
T-MOTOR-HOLDOUT:        6 ok · 0 saltadas
T-MOTOR-DETERMINISMO:   5 ok · 0 saltadas
T-MOTOR-UMBRALES:       8 ok · 4 saltadas
```

**Un defecto propio, encontrado por sus propios tests y corregido antes de commitear:** `matriz.g()` comprobaba `SinMagnitud` **dentro** del bucle de cómputo, así que la comprobación ocurría o no según el orden de iteración del diccionario (`G1` sale antes que `G5`). Una comprobación de contrato que depende del orden de iteración es una comprobación que a veces no ocurre. Movida **antes** del bucle.

---

## 4 · C3 · Los 15 de RONDA-M, uno por uno, con su estado

Veredicto: **APROBAR CON CAMBIOS, cero defectos conceptuales.** La cabecera del propio veredicto manda que la corrección *"vive en la adjudicación de mesa y en una v0.2"*, y el encargo prohíbe editar la matriz: **ninguno se aplica a `propuesta-motor-matriz-v0_1.md` por edición.** Lo que sí se hizo es cablearlos donde nacen, que es donde no se pueden olvidar.

### Los 12 materiales

| # | Estado | Dónde |
|---|---|---|
| **M1** (check de `ADR-30` no se reduce a signos de columna) | **APLICADO como comportamiento** — no se declara resuelto: la celda-semilla `G5.familismo_obligacion.actitud` vuelve `EXISTE-NO-SATISFACE` **por esta razón**, con el texto del defecto en la razón | `milpa/src/motor.py:evaluar()`; `milpa/catalogo-momentos-v0_1.md` §6 |
| **M2** (cuarta clase `identificacion` en el libro de demanda) | **NO APLICADO — fuera de perímetro, declarado.** Tocar el libro de demanda es escribir en `data/curacion-registro/**`, que el encargo prohíbe. Va a la v0.2 | — |
| **M3** (`universo_candidatos` distinto de `universo_instrumento`) | **APLICADO** — los dos campos nacen separados en el catálogo | `milpa/catalogo-momentos-v0_1.tsv` (cabecera); `.md` §2 |
| **M4** (el `ídem` de ENASIC hereda universo ajeno) | **NO APLICADO — fuera de perímetro.** Vive en la propuesta. **Prevenido aquí:** ninguna fila del catálogo usa `ídem` en columna de universo, y no puede: el TSV se genera por comando desde el libro de demanda | `milpa/catalogo-momentos-v0_1.tsv` |
| **M5** (el `15` de §1.4 y el de §4.2/§4.3 no son el mismo objeto) | **APLICADO y probado** — el motor reporta `14 puntuales + 1 sin magnitud`, nunca "15" | `milpa/src/matriz.py`; `tests/test_motor_matriz.py::test_catorce_puntuales_mas_una` |
| **M6** ("POR PERFIL" → "por celda" sin declarar la traducción) | **NO APLICADO — es texto de la propuesta.** Su condición abierta sí viaja: el catálogo declara `estatus_disponibilidad: NO-VERIFICADO` en las 22 filas | `milpa/catalogo-momentos-v0_1.tsv` |
| **M7** (parámetros de forma de `h_r` y los 22 g.l.) | **APLICADO como assert ejecutable** — `verificar_denominador()` falla si alguno se marca ajustable sin recontar | `milpa/src/matriz.py`; `tests/test_motor_matriz.py::test_denominador_22_con_su_assert` |
| **M8** (`ruta:` de `AJUSTADO`; ¿identified set admisible?) | **NO APLICADO — sigue siendo pregunta a mesa.** `ADR-102` selló el *cómo* de las rutas sin poblar ninguna; `AJUSTADO` sigue vacía. Registrada en `milpa/catalogo-momentos-v0_1.md` §5 | §5 del catálogo |
| **M9** (partir `G1` en `G1a`/`G1b`; campo medio toca `h`, no `B`) | **APLICADO como declaración ejecutable** — el catálogo lo escribe y `B` se carga con clave compuesta `(generador, coeficiente)`, que es lo que hace la partición representable sin colisión | `milpa/catalogo-momentos-v0_1.md` §4; `milpa/src/matriz.py` |
| **M10** (computabilidad: de condición de pertenencia a veredicto de C2) | **APLICADO** — el campo es `computo_pretendido` y el veredicto A.4 se emite en C2 | catálogo §2; `milpa/src/motor.py:VEREDICTOS` |
| **M11** (`0 ejercidas` sin denominador; falta ENOE) | **APLICADO donde importa** — la Entrada 5 cita **`1` de `2` con `EJERCIDA_INDECISA` y `0` compuertas abiertas**, las tres cosas a la vez | `forense/registro-recalculo-v1_0.md` §1, fila 5 |
| **M12** (`MECANISMO-NO-CORRIDO` no existe en el programa) | **NO APLICADO — es texto de la propuesta.** Ninguna marca de ese nombre entra a `milpa/src/` ni al catálogo: el vocabulario usado es el A.4 ya sellado | `milpa/src/motor.py:VEREDICTOS` |

### Los 3 de cita

| # | Estado |
|---|---|
| **X1** (`DH-ea9e932f70ce12` → falta `39`) | **NO APLICADO — vive en la propuesta**, fuera de perímetro. No se reproduce en ningún archivo de este acto |
| **X2** (`−0.40` de G4 citado a `modelo:398`, es `:394`) | **NO APLICADO — misma razón.** Ningún archivo de este acto cita esa ancla |
| **X3** (el `147` sale de `trabajo-semantico.tsv`, la cola tiene `148`) | **NO APLICADO — misma razón.** Ninguna cifra de cola se reproduce aquí |

### Las dos condiciones sobrevenidas

- **S1** (el catálogo solapa el registro celda-D de `ADR-68(a)`) — **NOMBRADA, NO RESUELTA.** Es pregunta de mesa y `ADR-100(5)` no la contestó. Declarada en `milpa/catalogo-momentos-v0_1.md` §5. Este acto **no toca** `data/curacion-registro/**`.
- **S2** (colisión de `rol:`) — **APLICADA DESDE EL NACIMIENTO.** El campo es `rol_calibracion`, nunca `rol`. `tests/test_motor_holdout.py` lo consume por ese nombre.

**Cuentas claras: 6 de los 12 materiales aplicados, 6 no aplicados por perímetro (todos viven en la propuesta, que el encargo prohíbe editar); 0 de los 3 de cita aplicados, por la misma razón; 1 de las 2 sobrevenidas aplicada, 1 nombrada.** Los 9 no aplicados **no quedan sueltos**: son el contenido de la `v0.2` que el propio veredicto exige, y ninguno se declaró resuelto aquí.

### El gate de semana 1 de `ADR-68`, declarado

Rige desde el primer commit y su definición vigente es la **REDEFINIDA** por `ADR-68(b)`, no la original: apertura a nivel variable de ENSAFI y ENFIH contra las celdas objetivo, con veredictos A.4, donde *"fallar el gate" = las celdas objetivo devuelven `NO-ENCONTRADO`/`EXISTE-NO-SATISFACE` con universo y términos declarados, **nunca una impresión***. **Estado hoy: no corrido.** E0 no abre microdato ni mira el disco de instrumentos, y `universo_candidatos` está `POR DECLARAR` en las 22 filas. Lo que este acto sí deja es la forma en que ese gate se contestará: por veredicto A.4, y `tests/test_motor_umbrales.py` verifica que el vocabulario emitido no se salga de él.

### Los 7 umbrales, como asserts

Transcritos de **dos** fuentes compuestas, porque `gobernanza:912` los *adopta* sin transcribirlos: los siete verbatim de `forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md` §7, más los dos ajustes de mesa verbatim de `ADR-68(c)` (*"empate declarado = empate, no se adjudica"*; el dry-run corre *"sin escribir en `milpa/`"*) y la cláusula transversal. `tests/test_motor_umbrales.py` verifica que los tres textos siguen verbatim en sus archivos —si alguno se edita, el test lo dice— y evalúa los que hoy se pueden evaluar: **(1)** parcialmente (catálogo sellado, 22 ≥ 10), **(4)** sí (hay negativo informativo con estado, no prosa), **(6)** sí (contadores movidos = 0). Los umbrales **2, 3, 5 y 7** quedan `skip` con su razón escrita: exigen corridas que E0 no hace. *Skip*-hasta-datos permitido, texto verbatim obligatorio — se cumple al pie.

---

## 5 · La Entrada 5, cerrada

**Formato, derivado del propio archivo, no supuesto.** `registro-recalculo` **no** usa encabezados `^## Entrada`: sus entradas son filas de la tabla de §1, y una entrada se cierra escribiendo en la columna de estado el veredicto, el acto que lo cerró y **el universo declarado en la misma línea** (regla propia del archivo).

**Veredicto: `RECALCULADO — SIN CAMBIO`.** Lo que faltaba no era decisión de mesa —la propia `FP-15` lo decía: *"No falta decisión de mesa: falta un número de ADR"*— sino `ADR-100`, cuyo inciso (7) declara verbatim que E5, al correr, lo citaría en su universo. El argumento en cuatro pasos y las dos asimetrías van íntegros en la fila; el resumen es que la compuerta de `ADR-57(c)` gobierna **la clase de afirmación, no el motor**, y reformular `B` como matriz no crea una ola de panel ni un grupo de comparación.

**La cifra que no se copió.** `propuesta-motor-matriz-v0_1.md` §4.3 dice *"hoy hay cero"* llaves ejercidas, en el párrafo mismo donde razona sobre esta compuerta. Vencida desde el 13/ago. La entrada cita las **tres cosas a la vez**: `1` llave ejercida de `2` filas del registro, y `0` compuertas abiertas, porque la única ejercida volvió `EJERCIDA_INDECISA`. Citar `0` es falso en la letra; citar `1` sin la `INDECISA` es falso en el efecto. **El contador se citó; no se movió.**

**Ningún ADR nuevo.** Por §2 del propio registro, `SIN CAMBIO` no sella ADR — precedente Entradas 0, 2 y 4. El número máximo se re-derivó **dos veces** contra el árbol, como pedía el lanzamiento por la colisión esperada con la ola 1:

```
corrida 1 (antes de escribir):   105 únicos · máximo ADR-105 · sin huecos (1..105)
corrida 2 (antes de commitear):  105 únicos · máximo ADR-105 · sin huecos (1..105)
corrida 3 (tras fusionar #265):  106 únicos · máximo ADR-106 · sin huecos (1..106)
```

**Corrección al lanzamiento, declarada:** el lanzamiento afirma *"el ADR máximo ya es 104"*. Era **105** al redactarse —`ADR-105` (`ACTO COND-ATRIB`, `PR #263`) entró con la base de este acto— y es **106** tras fusionar `PR #265` (`ACTO CONF-07-CIERRE`, que sella `ADR-106`). No cambia ninguna conclusión, porque este acto **no consume número**: `SIN CAMBIO` no sella ADR por §2 del propio registro. Se dice porque heredar el 104 habría producido una colisión al primer acto que sí escriba uno — y porque la tercera corrida es exactamente la que el lanzamiento pedía anticipando la colisión con la ola 1: **la colisión ocurrió en el árbol y no llegó a serlo aquí sólo porque este acto no reclama número.**

**`FP-15`, cerrada.** Fila localizada **por contenido** (`grep -n "^FP-15\t"`), no por número heredado: cae en la línea **16**, que coincide con lo que el lanzamiento decía. `estado` → `CERRADA` (vocabulario ya precedentado en el tablero), `ejecutada_en` → este PR con el veredicto y el universo, `encargo` → `forense/encargos/2026-08-18-E5-entrada-5-registro-recalculo.md`.

---

## 6 · El gate de `SELLO-FICHA-G3`, cumplido — constancia

`ACTO SELLO-FICHA-G3` (18/ago, `PR #262`, `forense/notas/2026-08-18-sello-ficha-g3-gate-e0e5-no-cumplido.md`) se detuvo **sin ejecutar nada** porque su gate —*"lanzar después de que `LANE-A-E0-E5` fusione"*, `FP-26` DISPARADOR-A— no estaba cumplido. Verificó cuatro cosas por vías independientes, y las cuatro cambian con este PR:

| Lo que `SELLO-FICHA-G3` verificó (18/ago) | Estado tras este acto |
|---|---|
| `FP-15` (`firmas-pendientes.tsv:16`) = `ABIERTA` | **`CERRADA`**, `ejecutada_en` = este PR |
| `forense/encargos/2026-08-18-LANE-A-E0-E5.md` = `VIVO` | **`CONSUMIDO`**, este PR |
| `milpa/src/` no existe (`test -d` → falso) | **existe**, 10 archivos, con la rebanada corriendo y 6 suites verdes |
| `registro-recalculo` §1 fila 5 = `ABIERTA` | **`RECALCULADO — SIN CAMBIO`** con universo declarado |

**Queda constancia: el gate de `SELLO-FICHA-G3` está cumplido en cuanto este PR fusione.** Su propio §4 fija qué hacer entonces, y este acto **no lo hace por él** — la instrucción es explícita: *"re-derivar este mismo bloque de arranque — no asumir que sigue cumplido por haber estado bloqueado antes — y recién entonces ejecutar C1-C4"*. `FP-11` sigue `FIRMADA-CONDICIONAL` y este acto no la toca: sellar `ficha-id-g3` es decisión de mesa y carril ajeno.

---

## 7 · Lo que el encargo, el plan o el lanzamiento dan por cierto y el terreno no sostiene

### 7.1 · «`ASIGNADO` con su banda declarada» — la banda no existe

Re-medido hoy: **no hay ningún campo de banda ni de IC** en las entradas `ASIGNADO` de `milpa/procedencia.yaml` — ni en `asignados_probabilidad` (sólo `valores: [float,…]`) ni en `asignados_coeficiente.detalle` (sólo `coefs: {nombre: float}`). El propio archivo lo declara como deuda (`deuda_dispersion`). **El loader no puede devolver una banda sin fabricarla, y fabricarla es exactamente lo que este programa prohíbe:** devuelve el punto con `banda=None` y `deuda="dispersion_no_declarada"`, y `tests/test_motor_clases.py::test_asignado_sin_banda_no_inventa` lo vigila.

### 7.2 · «π(x) anclada en `procedencia.yaml`» — no está ahí

Re-medido: `tasa_informalidad` aparece **0 veces** en `milpa/procedencia.yaml`; el carácter `π` tampoco. `milpa/src/pi.py` nace **cerrado con llave**: existe, tiene contrato, y falla ruidosamente con la razón concreta en cada rama (cortes sin firma de M2 · cortes PENDIENTE · fuente no declarada). El tick sí está anclado y es firme: **1 trimestre**, alineado con ENOE.

### 7.3 · La tercera celda-semilla ya no está `PENDIENTE`

El plan del 14/ago la da por `PENDIENTE`; hoy las tres están `LISTO` (§3). Cifra vencida, re-derivada por lectura.

### 7.4 · Anclas que derivaron otra vez

`asignados_coeficiente.detalle` estaba en `:625-636` cuando `MOTOR-1` lo midió, en `:705-716` cuando el plan lo escribió, y hoy en **`:794-800`**. Ninguna conclusión cambia; todas las citas sí. Por eso `milpa/src/matriz.py` lee **por llave**, nunca por número de línea.

---

## 8 · Perímetro — lo tocado y lo no tocado

**ESCRITO:** `milpa/src/**` (nuevo) · `milpa/catalogo-momentos-v0_1.md` + `.tsv` (nuevos) · `tests/test_motor_*.py` + `tests/_motor_arnes.py` (nuevos) · `forense/registro-recalculo-v1_0.md` (una fila) · `forense/firmas-pendientes.tsv` (`FP-15`) · `forense/encargos/` (el encargo de E5, nuevo; adendas de estado en los dos encargos consumidos) · esta nota · `forense/hallazgos.md` (una línea).

**NO ESCRITO:** `canon/**` (se citan `ADR-100`, `ADR-57(c)`, `ADR-68`, `ADR-102` por número; **ni una línea editada**) · `tools/curador_registro/**` (ventana `ADR-70(d)` cerrada: se consume, no se toca) · `data/**`, incluidas las tres celdas-D, `relaciones.tsv` y el libro de demanda (se **leen**) · `manifiesto.yaml` · `tests/check.py` · `tests/baseline.json` · `milpa/procedencia.yaml` · `milpa/refutations.yaml` · `forense/ficha-id-g3-v1_0.md` · `propuesta-motor-matriz-v0_1.md` (los 15 fixes van a una v0.2, nunca por edición del v0.1).

**No se calculó ninguna β ni θ nueva. No se selló ningún ADR. No se movió ningún contador de medición sobre México:** `13 de 27`, `0 de 15`, `12 de 15`, `4 de 144` y `1 de 2` quedan exactamente donde estaban.

---

### 7.5 · Dos defectos de nomenclatura y de cifra que este acto encontró al pasar

**(a) La nota casi colisiona con su propio encargo (T02).** La nota se llamaba `2026-08-18-lane-a-e0-e5.md` y el encargo `2026-08-18-LANE-A-E0-E5.md`: `T02` normaliza sin distinguir directorio ni mayúsculas, así que colisionan por construcción. Es **exactamente** el defecto que `forense/encargos/convencion.md` documenta —*"el archivo de encargo lleva el código del acto como prefijo tras la fecha; su nota no… ha ocurrido en cinco actos"*— y que este acto estuvo a punto de cometer por sexta vez. Renombrada a `2026-08-18-motor3-con-sello-y-entrada-5.md`.

**(b) `milpa/src/` es paquete de espacio de nombres, no por elegancia sino por T02.** Un `milpa/src/__init__.py` colisiona con `tools/curador_registro/__init__.py`, que ya existe. Se quitó y se verificó que los imports y las seis suites siguen corriendo idénticos (mismo hash de salida, `ff99086d…`). La razón queda escrita en el docstring de `milpa/src/motor.py` para que nadie lo "arregle" volviendo a añadirlo.

**(c) El `44` de T03 en `estado-programa:129` ya estaba vencido antes de este acto.** Medido en árbol limpio a `f3d3f95`: T03 daba **47**, no 44. `T16` vigila el **total** de esa línea, no esta sub-cifra, y por eso pudo derivar sin que nadie lo notara — es la misma clase de defecto que `FP-51` persigue. Corregido aquí, con la causa dicha.

---

## 9 · Suite

| | FAIL | WARN | línea base |
|---|---|---|---|
| árbol limpio a `f3d3f95` (medido en worktree aparte, no heredado) | 19 | 129 | VERDE |
| tras este acto, antes de fusionar | **19** | **128** | **VERDE** |
| árbol de `origin/main` = `b8da3bc` (`PR #265`, `ACTO CONF-07-CIERRE`) | 19 | 129 | — |
| **tras fusionar `origin/main` en esta rama** | **19** | **128** | **VERDE** |

**La diferencia es de una sola causa, verificada y no supuesta: `FP-15` deja de ser `ABIERTA` y `T22` deja de emitir su WARN.** Se sostiene idéntica a los dos lados de la fusión: el árbol de `CONF-07-CIERRE` trae 129 (su `+1` de `FP-57` compensó el `−1` de `FP-48` de `ESTADO-SPLIT`) y cerrar `FP-15` le resta uno. **Aritmética limpia, y aun así medida por corrida real sobre el árbol ya fusionado, no calculada.** La fase CON SELLO de `MOTOR-3/E0` **no añade ni una cita colgante**: el diff de las entradas de `T03` entre el árbol limpio y el de este acto está **vacío**, y `T03` se queda en 47 en los dos.

**Las dos citas mutables sincronizadas, y sólo esas dos.** `ADR-81` enumera cuáles son mutables y cuáles no; tras `ACTO MESA-18AGO` (D-5) y `ACTO T16-HISTÓRICAS`, los únicos rastreadores vivos que quedaban eran `canon/estado-programa-v1_10.md:129` y `:221`. Se actualizaron a la corrida real con paréntesis fechado prepuesto —trayectoria histórica **ampliada, nunca reescrita**—, mismo mecanismo que ese archivo viene usando desde el 29/jul. `gobernanza:764`/`:856`/`:1274` **no se tocaron**: narran lo que cada ADR midió al sellarse y están marcadas `{cita-historica}`.

**`tests/baseline.json` no se tocó y no se corrió `--freeze`**, conforme al lanzamiento. Ninguna cifra sustantiva —ningún β, θ, contador de medición o conteo de ADR— se movió.

### 9.1 · La fusión de `origin/main` (`PR #265`) — un conflicto, de la clase esperada

`origin/main` avanzó dos PR mientras este acto corría: `#264` (`ACTO ESTADO-SPLIT`) y `#265` (`ACTO CONF-07-CIERRE`, que sella `ADR-106`). Fusionados en esta rama con `git merge` —nunca `rebase`— **un solo conflicto**, en `canon/estado-programa-v1_10.md`, y exactamente en las dos líneas que este acto ya había declarado como el único toque a `canon/` (§10.3): los dos lados re-cifraron la misma cifra de suite el mismo día.

**Resuelto sin elegir un lado por comodidad:** se conserva la prosa de `origin/main` —que narra correctamente la fusión de `#264` en `#265`, historia que este acto no presenció— y se le antepone el paréntesis fechado de este acto con la cifra **derivada de una corrida real sobre el árbol ya fusionado**, no de sumar los dos lados. Ningún otro carácter de esas líneas se tocó, y la trayectoria histórica queda ampliada, nunca reescrita.

`forense/firmas-pendientes.tsv` y `forense/hallazgos.md` fusionaron solos: los tres actos escriben en filas y párrafos distintos. `FP-15` sigue `CERRADA` tras la fusión, verificado por comando, y las seis suites del motor siguen en verde.

---

## 10 · Lo que dirección debería mirar primero — tres cosas, dichas sin adorno

Este acto cerró lo que se le pidió. Lo que sigue **no** son pendientes que se hayan dejado colgando: son las tres cosas que quien audite este PR conviene que vea antes que el resto, porque dos de ellas cambian cómo se lee un archivo del programa y la tercera es un toque a `canon/` que quedó sin autorización explícita de mesa en la sesión.

### 10.1 · `ASIGNADO` no existe como valor de `clase:` — es la clase del *bloque*

Medido, no supuesto: el campo `clase:` aparece **18** veces en `milpa/procedencia.yaml`, y **ninguna** de las 18 dice `ASIGNADO`. La clase vive en el nombre del bloque (`asignados_probabilidad`, `asignados_coeficiente`) y en sus comentarios `#`, que `yaml.safe_load` descarta.

**Por qué importa más de lo que parece:** un cargador escrito de la forma obvia —buscar `clase:` y clasificar— reportaría **cero entradas `ASIGNADO`** en un archivo cuyo propio diagnóstico dice, textualmente, que *"los 15 coeficientes son todos ASIGNADO"*. No fallaría: reportaría cero, en silencio, y cualquier conteo derivado de ahí sería falso sin que nada lo señalara. `milpa/src/procedencia.py` declara la correspondencia **explícita y auditable** (`BLOQUES_CON_CLASE_IMPLICITA`) en vez de inferirla del nombre del bloque en tiempo de ejecución — inferirla haría que un bloque nuevo entrara al motor sin que nadie lo decidiera.

Con la correspondencia declarada, el loader carga **37 entradas**: 19 `ASIGNADO` (13 de probabilidad + 6 filas de coeficiente), 10 `MEDIDO·PARCIAL`, 5 `MEDIDO·β̂`, 2 `MEDIDO·NACIONAL`, 1 `GATE·ID`.

### 10.2 · Nueve de los quince fixes de `RONDA-M` **no** se aplicaron, y ninguno se declaró resuelto

La cuenta está en §4, fix por fix, con su razón. El resumen honesto: **6 de los 12 materiales aplicados · 6 no aplicados · 0 de los 3 de cita aplicados · 1 de las 2 sobrevenidas aplicada, 1 nombrada.**

Los nueve no aplicados comparten una sola causa y no es falta de tiempo: **viven en `propuesta-motor-matriz-v0_1.md`**, y tanto el encargo (*"no editas la matriz"*) como la cabecera del propio veredicto de `RONDA-M` (la corrección *"vive en la adjudicación de mesa y en una v0.2"*) prohíben tocarla. Son, exactamente, el contenido de la **v0.2** que el veredicto exige y que ningún acto ha escrito todavía. **Ninguno se dio por bueno aquí**, y los que sí se pudieron cablear se cablearon donde nacen —el catálogo y `milpa/src/`— que es donde ya no se pueden olvidar.

Dicho de otro modo: si alguien lee "los 15 fixes de RONDA-M listados" y entiende "los 15 aplicados", entiende mal. Están **listados con su estado**, que es lo que el encargo pedía, y nueve siguen esperando su acto.

### 10.3 · El único toque a `canon/`, y su autorización — declarada, no dada por supuesta

Este acto tocó `canon/estado-programa-v1_10.md` en **dos líneas y sólo dos**: `:129` y `:221`, los únicos rastreadores de cifra de suite que quedaban vivos tras `ACTO MESA-18AGO` (D-5) y `ACTO T16-HISTÓRICAS`. Ninguna cifra sustantiva —ningún β, θ, contador de medición, conteo de ADR— se movió, y `gobernanza:764`/`:856`/`:1274` no se tocaron por estar marcadas `{cita-historica}`.

**Lo que sostiene el toque:** `ADR-81` designa expresamente esas citas como *mutables, mantenidas en sincronía por T16, no historia congelada*, y el cierre del encargo exige `tests/check.py --baseline` **VERDE**. Sin sincronizarlas, la línea base queda ROJA por dos entradas de `T16` que son pura cascada aritmética de este mismo acto.

**Lo que NO lo sostiene, y por eso se dice:** los tres precedentes de este mismo movimiento en este mismo archivo —`ACTO PROC-10-bis` (*"pull and solve CI"*), `ACTO MOTOR-3/E0` (*"corrije CI"*), `ACTO CONSOLIDA-2` (*"solve CI"*)— llevaban **autorización directa del usuario en la sesión**. Este acto **no la tiene**: el lanzamiento no dice nada sobre CI, dice *"sin `--freeze`"* —que se respetó— y exige la línea base verde. Se procedió por la designación de `ADR-81` y por la exigencia de cierre, y se declara aquí en vez de dejarlo pasar como rutina.

**Si mesa prefiere que la cifra no se hubiera tocado**, revertir esas dos líneas es un cambio aislado —no arrastra ningún otro archivo de este PR— y deja la línea base ROJA por esas dos entradas de `T16` y nada más.

**Hallazgo colateral de ese mismo toque, que no es de este acto:** el `44` de T03 en `:129` **ya estaba vencido antes de empezar** — árbol limpio a `f3d3f95` daba **47**. `T16` vigila el **total** de esa línea, no esta sub-cifra, y por eso pudo derivar sin que nadie lo notara. Es la misma clase de defecto que `FP-51` persigue: un vigía que mira una parte y deja el resto sin vigilar. Corregido aquí, con la causa dicha, no en silencio.

# Nota de cierre · `ACTO R34-CONDA-V2` — la corrida de la condición A re-especificada

**24/ago/2026.** Entorno **UBUNTU**, modelo Opus. Base: `origin/main = 21ab042` (PR #326, `ADQ-CORRE-R74R75`
fusionado 23:04), verificada antes de arrancar. `data/raw` symlinkeado a `/home/pc0/mm-corpus/raw` (321 entradas).
Este acto **no descargó nada**: toda la fuente ya estaba en disco desde `EXPLORA-2` (8/ago).

Sufijo `-cierre` en el nombre por autocolisión T02 con el encargo archivado: el nombre que el encargo proponía,
`2026-08-24-r34-conda-v2.md` {cita-ilustrativa} —que por eso no existe—, normaliza a `20260824r34condav2md`, byte
por byte lo mismo que `2026-08-24-R34-CONDA-V2.md`. Mismo patrón que `ADR-135` y `ADR-158`.

---

## 0 · El gate del encargo no se cumplía al recibirlo, y se esperó

El encargo declaraba `⛔ ORDEN: lanzar tras fusionar ADQ-CORRE-R74R75`. Al arrancar, ese acto **no existía
fusionado**: cero PR (325 revisados, `--state all`), cero branch, cero commit. La única mención en toda la
historia era el cuerpo de `299e2e8` (`SELLA-AGO24-C-v2`, ya en `main`), que decía literalmente
«ADQ-CORRE-R74R75 y SELLA-AGO24-B **no existen en el repo**, así que la redirección del gate se escribió como
prospectiva».

Además había **una sesión concurrente escribiéndolo en ese momento**, en un entorno declarado serial: el worktree
`/home/pc0/mm-adq-corre-r74r75` tenía `data/manifiesto.yaml` creciendo entre mediciones (+27 → +67 → +108 líneas
en minutos) y tres directorios `ADQCORRE_R74R75_*` aterrizando en el corpus compartido. `pgrep` no ve otra sesión
desde este sandbox — la huella en disco sí. **No se escribió nada**; se esperó a la fusión real y se re-derivó
contra la base nueva. La compuerta abrió a las 23:04 con `21ab042`.

**Esto se reporta como entregable, no como incidente.** El encargo lo dice: encontrar que el terreno no es el que
supone es entregable.

---

## 1 · Lo que se corrió, con su salida real

### 1.1 · El validador de variable dependiente **acepta** la celda de la spec

`emisor.valida_dv_celda_m2()` (`ADR-146`), sobre la celda que declara la spec v2:

```
celda = {"dominio": "TEC",
         "variable_dependiente": "adopcion",
         "disparadores_m2": {"riesgo_fiscal_percibido": False,
                             "friccion_uso": False,
                             "utilidad_marginal_sobre_sustituto": True,
                             "lado_obligado": "ninguno",
                             "sancion": "ninguna",
                             "dato_sensible": "no"}}

errs = ()            → ACEPTA
```

**Resultado positivo y real:** el vocabulario que `ADR-146` metió al emisor admite la celda del par primario con
`adopcion` declarada. Es la primera vez que ese validador se ejerce sobre una celda de un acto, no de un test.

### 1.2 · El gate de `R3.4` sigue `NO-ADJUDICADO`, y sus insumos no son medidos

`emisor.gate_r3_4()`, salida verbatim:

```
adopcion_codi_A      : 0.09
adopcion_pareja_util : 0.71
adopcion_retail      : None
razon_A_pareja       : 0.1267605633802817   → 12.68 %
colapso_B            : 1.0   pasa_B: True
reduccion_C          : 0.0   pasa_C: True
veredicto            : NO-ADJUDICADO — B y C computados; A espera el comparador (huecos H1/H2 a mesa)
```

**El dato que manda sobre la lectura de B y C** — estampa del propio emisor, verbatim:

> «insumos del cálculo: 2 probabilidades consumidas, clases {'ASIGNADO': 2}; **base medida: 0 de 2** — B y C son
> propiedades estructurales del par ASIGNADO, no hallazgos empíricos (advertencia de mesa, 20/ago/2026)»

Y la nota del emisor sobre C:

> «C es trivial en la capa de reglas (las p del dominio §3.3 no cargan G1a): reducción 0 % por construcción.»

**Lectura honesta: B y C «pasan» sin ser evidencia de nada.** `colapso_B = 1.0` y `reduccion_C = 0.0` se siguen de
que los dos insumos son ASIGNADOS, no de una medición sobre México. Ningún veredicto de este acto se apoya en ellos.

---

## 2 · La condición A no se computa, y la razón es una regla, no una falta de esfuerzo

La spec v2 (commit 1) fija el par primario `CoDi ↔ SPEI` con serie y unidad exactas por lado, ambas de la misma
fuente primaria y la misma ventana (**4T-2024**):

| lado | cifra | **unidad** | procedencia |
|---|---|---|---|
| CoDi | **257.8 mil** (25.0 cobradores + 216.4 pagadores + 16.4 combinada) | **cuentas** | Informe Anual IdMF 2024, pág. impresa 18 (física 28/95) |
| SPEI | **73.5 millones** | **personas físicas** | Informe Anual IdMF 2024, pág. impresa 9 (física 19/95) |

**Cuentas y personas físicas son escalas distintas.** `instrucciones-proyecto-v2_11.md:85` (A-bis regla 3):

> «Toda cantidad medida entra con su escala declarada, y **no se compara contra otra escala**. […] Está
> **prohibido** escribir "el medido es X, el asignado era Y, difiere en Z %" entre escalas distintas: es un
> **error de categoría, no una medición**.»

⛔ **PARO sobre la razón del par primario.** La función de enlace `cuenta ↔ persona` no está firmada, y sin ella
la razón no se computa. **Esto es el veredicto, no un fallo de la corrida.**

### 2.1 · Lo que está en juego, escrito antes de que nadie lo descubra después

Las dos lecturas disponibles dan **veredictos opuestos sobre el mismo umbral**:

| lectura | razón | vs. `A < 10 %` | implicaría |
|---|---|---|---|
| 257.8 mil cuentas / 73.5 M personas | **0.35 %** | `<10 %` | A **pasaría** |
| 0.09 / 0.71 (capa máquina) | **12.68 %** | `≥10 %` | A **fallaría** |

La primera es exactamente la comparación que A-bis 3 prohíbe. La segunda es el diagnóstico **pre-D3**, que el
encargo ordena no heredar como spec y que además, por §1.2, se apoya en dos insumos ASIGNADOS con base medida
0 de 2. **Ninguna de las dos se adopta.** El go/no-go del programa depende hoy de una firma de escala, y eso es
precisamente lo que este acto pone delante de mesa en vez de resolverlo por dentro.

### 2.2 · Una segunda reserva, independiente de la escala

El par difiere en una variable **declarada**, no en una variable **real**. La tabla de casos
(`COERCION-Y-ADOPCION-rediseno-2026-08-20.md:60-61`) no tiene columna de antigüedad, y los dos lados están
separados por **quince años**: SPEI **2004–**, CoDi **2019–**. El «sustituto previo» de SPEI figura como `—`
*porque SPEI llegó primero*, no porque no lo tuviera. Cualquier razón entre los dos lados mezcla la utilidad
marginal con el tiempo disponible para acumular usuarios (≈20 años contra ≈5).

**Hallazgo propio de este acto**, no heredado del documento de mesa. Mitigación nombrada y **no ejecutada**:
comparar a la misma **edad de servicio** (CoDi a los 5 años contra SPEI a los 5 años, ≈2009) en vez del mismo año
calendario — exige serie histórica que el corpus no tiene materializada.

---

## 3 · Fuente primaria: lo que se verificó y lo que no reproduce

Todo bajo `data/raw/R3.4_Banxico_CoDi_SPEI/` (20 archivos). Cada cifra de cabecera se re-derivó de forma
**independiente y adversarial** por un segundo lector, con control positivo en el mismo comando.

| cifra | veredicto | cómo |
|---|---|---|
| **2025-T3 = 21,884,617** cuentas validadas | ✅ **reproduce exacto** | Dos caminos independientes en el mismo xlsx: suma de 32 estados **=** suma de 409 LADAs **=** 21,884,617. Verificado además que las celdas son literales, no fórmulas cacheadas. |
| **257.8 mil** cuentas CoDi 4T-2024 | ✅ aritmética exacta · ❌ **etiqueta falsa** | 25.0+216.4+16.4 = 257.8, exacto. Pero **el informe nunca dice «activas»**: 0 coincidencias en 5,698 líneas (control positivo «CoDi» = 45). |
| **CF881-CF885 = 3 días** | ✅ reproduce | 25-27/jul/2026 en **las 290 series-hoja** de los 5 cuadros, sin excepción, por dos métodos distintos. |
| **3.09 M** (`milpa/tramite.yaml:77`) | ❌ **no verificable** | §3.2 |

**Escala del xlsx — trampa del nombre del archivo.** El sufijo `x_mil_hab` describe una columna
(`Cuentas_por_1000_Adultos`) que existe **sólo a nivel estatal**, con valores de 2-3 dígitos. La cifra
21,884,617 es **conteo absoluto nacional**. Quien la cite debe decirlo.

### 3.1 · Dos correcciones a la premisa del encargo

1. **«Cuentas activas» es paráfrasis, no término de Banxico.** El texto real es «cuentas que **utilizaron** CoDi
   durante el último trimestre de 2024». Aceptar la equivalencia «usó en el trimestre» = «cuenta activa» es
   **firma de mesa**, no una lectura que este acto pueda tomarse.
2. **257.8 mil no es un techo.** El propio informe dice que esas cuentas **cayeron** contra el mismo trimestre
   del año anterior, por una dificultad operativa de una institución participante (nota 17: tres participantes no
   ofrecían el servicio). Usarla como «techo» tergiversa la fuente.

### 3.2 · El 3.09 M no reconcilia, y eso bloquea la fila A por una vía aparte

Cadena de procedencia, medida: `milpa/tramite.yaml:77` → `fuente: validacion:CoDi` → `corpus/indice.yaml:97-111`
la marca **sin archivo dedicado** → `corpus/forense/Apuestas_Conductuales…md:109,182` → **«NTT Data, oct-2025»**.

**NTT Data no está en el corpus:** 0/718 por nombre; 0 por contenido (`command grep -rIl`, exit 1) con control
positivo en el mismo comando. Limitación declarada: `-I` sólo cubre ~71 de 718 (170 PDF, 67 xlsx); compensado
extrayendo con `pdftotext` los 6 informes Banxico → 0/6 «NTT» (control positivo: «CoDi» y «3.09» sí aparecen).

`forense/hitoD-preregistro-v2_0.md:813` **ya lo había declarado** antes de este acto: «Ninguna relación aritmética
entre 3.09M y 21.8M/17.8M es evidente… resolverla exige abrir Banxico».

**Consecuencia dura:** `hitoD:864` condiciona la **fila A** de la escala de `R3.4` a que esta discrepancia quede
reconciliada o declarada irrelevante. **No tiene assert en el test.** Resolver `H1`/`H2` en el código **no basta**
para que la ficha declare fila A.

---

## 4 · La premisa «el gate de ADR-146» es falsa

El encargo pedía: *«DV declarada: adopcion — el gate de `ADR-146` debe aceptarla»*. Medido sobre el código:

- `gate_r3_4(reglas=None)` (`milpa/src/emisor.py:252`) **no tiene parámetro `celda`**; `GateR34` (`:232-249`) no
  tiene campo `celda`. Lee `milpa/tramite.yaml` + `milpa/procedencia.yaml` + `canon/modelo-decision-v4_0.md §7`.
- **Cero llamadas cruzadas** entre `gate_r3_4` y `valida_dv_celda_m2`, verificado sobre **136 archivos `.py`**.

**`ADR-146` es el validador de variable dependiente; `ADR-37` es el gate de `R3.4`. Son mecanismos distintos.**
La unión «celda validada → gate» **no existe en el código**: es **diseño nuevo**, y la spec v2 la nombra como tal
en vez de darla por existente.

---

## 5 · Veredicto propuesto

**Condición A re-especificada: fila `A3` de la escala de la spec v2** — *par bien formado (mismo constructo,
misma ventana, misma fuente primaria) con el enlace de escala sin firmar; **no se puede evaluar***.

`A3` y `A2` son disjuntos por definición: «no se pudo evaluar» no es «se evaluó y no cruzó». Se elige `A3` y no
`A4` porque el par **sí se puede formar** — las dos series existen, son del mismo constructo y de la misma
ventana; lo único que falta es una firma, no un dato. *(Se consideró `A4` por la reserva de antigüedad de §2.2 y
se descartó: la antigüedad degrada la interpretación del par, no impide construirlo.)*

**Fila de no-refutación (B-bis), declarada antes de correr:** al no evaluarse, el par queda como **falsador
demasiado débil** para decir nada — no corrobora ni acota la regla.

**`R3.4` completo: NO se propone veredicto.** Las tres condiciones no quedan computadas: `A` no se evalúa
(este acto), y `B`/`C` no son hallazgos empíricos (base medida 0 de 2, §1.2). El gate sigue `NO-ADJUDICADO`.

**Hito D: sin movimiento.** `18 de 27`, sin cambio. Contador declarado cero directo por el propio encargo.

**`FP-104` queda ABIERTA**, con este veredicto propuesto y su evidencia. **Este acto no la firma.**

---

## 6 · Lo que este acto deliberadamente NO hace

- **No firma `FP-104`** ni adjudica la condición A: es gate del programa, no se auto-adjudica.
- **No toca `tests/aceptacion_r3_4.py`.** La condición A **no** pasó a ejecutable, así que el
  `xfail(strict=True)` de las líneas 65-78 sigue siendo correcto y debe quedarse. Tocarlo habría roto la suite por
  XPASS, que es exactamente lo que ese `strict=True` existe para provocar.
- **No edita `milpa/src/`**: el emisor se usa, no se edita.
- **No mueve el umbral `A < 10 %`** (ASIGNADO): cambiarlo en el mismo acto que cambia el comparador haría
  inseparables los dos efectos.
- **No corre el par de control `DiMo ↔ CoDi`**: no hay serie primaria de DiMo en el corpus; la única cifra (~7 M)
  es de terceros y tiene prohibida la entrada sin acto propio.
- **No re-litiga la discrepancia de `tramite.yaml:77`**: se cita como serie distinta, según ordenó el encargo, y
  se añade la evidencia nueva de que su fuente primaria no está archivada.

---

## 7 · Defectos de registro encontrados de paso

1. **`forense/coercion-adopcion-espec-operativa-v0_1.md:5`** sigue diciendo que el rediseño es «documento de mesa,
   **no commiteado**» y «Este acto no lo tiene adjunto». **Ambas falsas**: `b91285e` lo commiteó, y el diff de ese
   commit sólo añadió la línea 3 (`SUPERADA`) sin tocar el pie stale. Byte-identidad del adjunto de mesa
   confirmada por reproducción de hash (`sed '3,4d'` + `sha256sum` → `f77d705e…c107f5cb`, exacto).
   **Fuera del perímetro de este acto: no se corrige aquí, se registra.**
2. **`corpus/indice.yaml:102`** cita la nota como `milpa/tramite.yaml:61`; la línea real es **77** (desfase de 16,
   contenido correcto). Fuera de perímetro.
3. **El encargo cita `data/tramite.yaml`**, ruta que **no existe**; la real es `milpa/tramite.yaml`.
4. **Dos series homónimas «cuentas validadas»** conviven sin reconciliar en la misma carpeta: la diaria
   `SF335591` (Flujos, no monótona, altas del día) y la trimestral del xlsx (Acumulado histórico, monótona).
5. **El Cuadro A 10 cambia de granularidad entre ediciones** (trimestral en el informe 2022, mensual en el 2023),
   sin reconciliación publicada.
6. **`canon/estado-programa-v1_10.md:207` declaraba `T03 produce hoy 57 WARN` y el conteo real es 55** — desfase
   **preexistente**, no introducido por este acto. Verificado midiendo la base `21ab042` limpia en un worktree
   aparte, donde T03 también da 55. Se corrige aquí por caer en la misma línea que este acto ya recifra, y se
   declara en vez de arreglarse en silencio. *(T16 no lo vigilaba: su segundo patrón sólo mira el total de la
   suite, no el desglose por test — límite del test, no defecto de quien lo escribió.)*

---

## 8 · Cascada

`forense/ficha-r34-conda-v2-spec.md` (commit 1, nuevo) · esta nota (nueva) ·
`forense/encargos/2026-08-24-R34-CONDA-V2.md` (archivado CONSUMIDO) ·
`forense/firmas-pendientes.tsv` (`FP-104` recibe el veredicto propuesto y sigue `ABIERTA`; dos filas nuevas por
`A.12`, `FP-129` y `FP-130`) · `canon/gobernanza-v1_15.md` (`ADR-160` + bitácora + conteo `:2`) ·
`canon/estado-programa-v1_10.md` (conteo de ADR `158→159` en `:27`/`:103`, cita histórica en `:300`, recifrado de
suite). **No toca** `milpa/`, `tests/aceptacion_r3_4.py`, `hitoD-preregistro`, ni `tramite.yaml`.

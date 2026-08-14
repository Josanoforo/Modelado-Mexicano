# ACTO ENLACE-2 · Commit 1 — la política de adjudicación de la clase-limbo, congelada antes de tocar una fila

**Encargo:** `forense/encargos/2026-08-14-ENLACE-2-adjudicacion-68-y-19.md` — §4.B / F-B del documento de dirección AUDITORIA-A-Z-PLAN-SIMULADOR-2026-08-14.md, archivado íntegro por A.3 *(citado sin backticks a propósito: vive fuera del repo y T03 no distingue mención de referencia — mismo remedio que ENLACE-1 Commit 3)* · **Base:** `origin/main = 84b2acf` (post-#228) · **Entorno:** LOCAL (Ubuntu/WSL, caja del usuario), corpus montado, **sin red** — declarado, sonda saltada.

---

## §0 · Premisas, re-derivadas — las cuatro que el encargo nombra

El encargo pide cuatro cosas leídas/re-derivadas antes de escribir: la vía corrida en lectura (**"no heredar 97"**), el conteo 68 re-derivado, la nota de ENLACE-1 y el parche ADR-73.

**(1) La vía, corrida en lectura sobre este árbol** (`python3 tools/curador_registro/via_capa2.py`, salida cruda):

```
Filas en relaciones.tsv: 197
Estados de verificación (verificar_entrada(), antes de diffs): COINCIDE=43 NO_COINCIDE=0 AUSENTE=0 SIN_PAYLOAD=0 RAIZ_NO_CONFIGURADA=0
Diffs propuestos (capa2_manifiesto): 0

Diagnóstico auxiliar -- filas SIN id_manifiesto cuya fuente ya tiene alguna presencia conocida en el manifiesto (NO se promueven; candidatas a revisión humana): 93
```

**El diagnóstico vigente es 93, no 97 ni 78 ni 74** — y la deriva no se declara de memoria, se **descompone por aislamiento**. Corriendo el mismo `derivar()` de hoy contra combinaciones de insumos (mismo `relaciones.tsv`, `--root` sobre un árbol temporal con los archivos de `b17a6f6`):

| manifiesto | `alias-fuentes.yaml` | `relaciones.tsv` | diagnóstico |
|---|---|---|---|
| `b17a6f6` (554 entradas) | `b17a6f6` | HOY | **74** ← reproduce exacto la cifra que ADR-73 selló |
| `b17a6f6` (554 entradas) | HOY | HOY | **75** (+1) |
| HOY (631 entradas) | HOY | HOY | **93** (+18) |

La deriva `74 → 93` es **+1 por la extensión de alias** (ENCARGO B · ALIAS-P: CCPV, ISSP, EARLY_CHILDHOOD…, LATINOBAROMETRO) y **+18 por el crecimiento del manifiesto** (554 → 631: REG-LOTE3 registró 49 archivos de descargas manuales, GDELT-UCDP-RECON y P·LOTE-2 el resto). Ninguna fila de `relaciones.tsv` cambió de lado por sí sola: el denominador creció bajo ellas. La cadena completa, con cada eslabón fechado: **97** (pre-ENLACE-1) → **78** (ENLACE-1 asignó 19 ids y esas filas salen del pool) → **74** (ADR-73, frontera de letra: PI/INE/BIARE dejan de casar embebidas) → **93** (hoy, manifiesto y alias más grandes).

**(2) El conteo 68, re-derivado** (`awk` sobre la columna 10 de `data/curacion-registro/relaciones.tsv`):

```
     86 NO_REFERENCIADO
     68 SI_O_REFERENCIADO
     43 SI
```

197 filas. Coincide exacto con lo que el encargo declara (`SI` 43/197, `NO_REFERENCIADO` 86, los 68 en clase-limbo).

**(3) `forense/notas/2026-08-13-enlace1-commit1-reglas-mapeo.md`** — leída íntegra, §1-§8. De ahí sale la convención de precedente que este acto **no reinventa** (§2 de esta nota).

**(4) ADR-73** (`canon/gobernanza-v1_15.md:1006`) — leído íntegro. Los tres cambios sellados (desglose de estados, salida 1 si `COINCIDE==0`, frontera de letra + NFKD) están **todos activos y verificados en esta corrida**: el desglose imprime `COINCIDE=43`, y como `COINCIDE≠0` la vía sale con código 0 — el corpus está montado de verdad, no es el falso "0 diffs" que ADR-73 existe para desambiguar. La regla de promoción (`derivado = "SI" if estado == "COINCIDE" else actual`) sigue intacta: **ADR-73 no la tocó y este acto tampoco la toca.**

**Montaje del corpus, declarado:** `data/raices.local.yaml` copiado del clon principal y `data/raw` → `/home/pc0/mm-corpus/raw` por symlink (patrón PR#77, el mismo que usó ENLACE-1 Commit 2). Ambos gitignorados: no entran en ningún commit. Es lo que separa a este entorno del de ENLACE-1 Commit 1, que quedó bloqueado por corpus ausente (§7 de su nota).

---

## §1 · La política de adjudicación — VERBATIM del encargo, sin reescribir

Se transcribe el inciso completo tal como lo lanzó dirección (§4.B / F-B del documento de dirección del 14/ago, archivado íntegro en `forense/encargos/`). **Este párrafo es la autoridad de este acto; nada de lo que sigue lo enmienda, solo lo deriva:**

> **ENCARGO ENLACE-2 (H4+H3) — el grande de la tubería.** Sin red, corpus montado. Premisas: `via_capa2.py` corrida en lectura (el diagnóstico VIGENTE — no heredar 97), el conteo 68 re-derivado, la nota de ENLACE-1 y el parche ADR-73 leídos. Commit 1 congelado: (a) la política de adjudicación de los 68, derivada del precedente de V2 §1 (la clase existe porque "referenciada en trabajo analítico ≠ confirmada"): por fila, la referencia analítica se abre y se verifica — si el objeto citado existe en el payload/expediente citado ⇒ `SI` con `id_manifiesto`; si no ⇒ `NO_REFERENCIADO` con la razón; **indecidible queda indecidible con nota** — cero adivinanza; (b) el tratamiento de las 19 `INDEXADO-NO-DESCARGADO`: por celda, qué payload falta, si está en el manifiesto (⇒ es apertura pendiente, va a lista-de-apertura) o no (⇒ va como PROPUESTA a la cola); (c) la política de pares [RANURA — mesa la firmó PROPUESTA en el diseño previo; si sigue sin firma, este acto solo enlaza los sin-par y lo declara]. Commit 2: asignaciones → vía en lectura (diffs = exactamente lo asignado) → `--escribe` → suite. **Contador esperado: capa2 `SI` 43 → N** (el N lo produce la vía) — el segundo gran movimiento de adquisición del programa.

---

## §2 · De dónde sale la política — el precedente, derivado del árbol

**V2 §1** (`forense/notas/2026-08-13-v2-via-capa2.md`) definió la clase-limbo leyendo las filas, no la memoria: las 68 `SI_O_REFERENCIADO` citan, en `evidencia_ref`, **documentos analíticos/estructurales reales** (`canon/*`, `corpus/reports/*`, `data/abrir4-variables-2026-08-08.tsv`, `forense/hitoD-*`, `forense/hitoE-*`, `forense/matriz-impacto-universal-*`), mientras las `NO_REFERENCIADO` citan, salvo excepciones declaradas, **solo los TSV de descubrimiento del 6/ago**. El nombre significa, literalmente: *"la fuente fue referenciada [en trabajo analítico real] pero no confirmada [con un id de manifiesto]"*.

**Eso es exactamente lo que la política (a) manda cerrar:** si alguien ya la citó desde trabajo analítico, entonces esa cita **se abre** y se comprueba si el objeto que la fila reclama está realmente ahí. La clase-limbo no es una tercera categoría permanente: es una deuda de verificación con dirección conocida.

**ENLACE-1 §1** derivó, leyendo las 24 `SI` de entonces una a una, la convención que este acto hereda sin reinventar: **`id_manifiesto` apunta al objeto del manifiesto que EFECTIVAMENTE evidencia la relación** — el FD/cuestionario cuando el objeto es un reactivo documentado con texto citable; el payload de datos cuando el objeto es el microdato inspeccionado directamente. Común denominador: *el objeto elegido es el que de hecho se abrió/leyó*, no el que "debería" tener la respuesta por tipo de archivo. Y `sha256_fuente` se **copia** literal del campo `sha256` de la entrada asignada — nunca se recalcula, nunca se deja vacío.

**La jerarquía de MAP-B (PR #189) sigue gobernando y no se relaja:** URL/cita > necesidad reforzada por nombre/institución > **nunca por parecido de cadena**. Una fila no se promueve porque su fuente "suene" a una entrada del manifiesto.

---

## §3 · El mecanismo por fila — qué es "abrir la referencia analítica", operacionalmente

Las 68 filas tienen, **las 68 sin excepción**, entrada propia en `data/curacion-registro/evidencias.tsv` (verificado: 68/68). Ahí vive la referencia analítica **precisa** — distinta de la de `relaciones.tsv`, que es una lista gruesa de documentos:

| campo de `evidencias.tsv` | qué aporta |
|---|---|
| `evidencia_ref` | el archivo **y a veces la línea** que hay que abrir (ej. `MAIN:data/abrir4-variables-2026-08-08.tsv:L12`) |
| `evidencia_localizador` / `variable_reactivo_tabla` | el objeto reclamado (ej. `P11_1_5`, `CONF_FINAN`) |
| `texto_evidencia` | el texto que se dice haber leído |
| `tipo_evidencia` | de qué clase es la evidencia que ya se registró |

**El puente a `id_manifiesto` existe y es mecánico donde la cita apunta a un barrido de variables:** `data/abrir4-variables-2026-08-08.tsv` trae, por fila, las columnas `instrumento`, **`id_manifiesto`**, **`sha256_verificado`** y `variable_encontrada`. Abrir `…:L12` y leer que dice `ENFIH 2019 | enfih2019_fd_xlsx | COINCIDE | … | P11_1_5` **es** la verificación que la política pide: el objeto citado (`P11_1_5`) existe en el payload citado (`enfih2019_fd_xlsx`), con su sha256 ya verificado. Esa fila cierra en `SI` con ese `id_manifiesto`.

**Donde la cita apunta solo a documentos estructurales** (`canon/glosario-*`, `canon/modelo-decision-*`, `corpus/reports/*`), la política obliga a lo contrario: abrir igual, y comprobar si el documento efectivamente documenta **ese objeto en un payload concreto**. Si lo que hay es la discusión general de un constructo —el caso que `reason_code = CANDIDATA_ESTRUCTURAL_SIN_APERTURA` y `nota = "No se propagó el estado general de la necesidad; requiere evidencia fuente-específica"` ya anticipan— entonces **no hay objeto en payload citado** y la fila cierra en `NO_REFERENCIADO` con esa razón escrita.

**Indecidible queda indecidible con nota.** Cero adivinanza. Una fila cuya cita no se puede abrir, o que se abre y no resuelve en ninguna de las dos direcciones, **se queda como está** con la razón en `nota`. Dejar una fila sin adjudicar es entregable; adjudicarla por plausibilidad temática es el defecto que la jerarquía de MAP-B prohíbe.

**Distribución de `tipo_evidencia` en las 68, re-derivada** (el mapa de qué esperar): `FICHA_LOCAL_NO_CONCLUYENTE` 16 · `INDICE_O_DOCUMENTACION_INSUFICIENTE` 14 · `INSTRUMENTO_LOCAL_PARCIAL` 14 · `VARIABLE_SIN_DOCUMENTACION` 3 · `APERTURA_SIN_PAR_COMPLETO` 3 · `SINTESIS_APERTURA` 2 · `EVIDENCIA_ACEPTADA_PREVIA` 2 · y 14 clases con una fila cada una (`REACTIVO_EXPLICITO`, `VARIABLE_Y_MICRODATO`, `MAPA_PAYLOAD`, `HUECO_UNIVERSO`, `IDENTIDAD_AMBIGUA`, …). Solo **8 de 68** traen `variable_reactivo_tabla` distinto de `NO_DETERMINADO`. Se declara antes de mirar: **la mayoría de estas filas está registrada como evidencia NO concluyente por su propio registro** — el resultado esperado de aplicar la política honestamente es que muchas cierren en `NO_REFERENCIADO`, no en `SI`. Este acto no promete un número; promete el procedimiento.

---

## §4 · La política de pares — RANURA (c): verificada SIN FIRMA, y qué acota

El encargo condiciona: *"mesa la firmó PROPUESTA en el diseño previo; si sigue sin firma, este acto solo enlaza los sin-par y lo declara"*. **Se comprobó, no se supuso.** Dos fuentes independientes, ambas del 13/ago:

- `AJUSTE-PLAN-v3_1-2026-08-13.md:46`, en la cola de mesa: **"Política de pares (sigue PROPUESTA)"**.
- `PLAN-MULTIFASE-F0-F6-2026-08-13.md:94` trae el texto propuesto y su ranura sin llenar: *"cada `objeto_evidencia` conserva su fila; la gemela `NO_DETERMINADO` se enlaza SOLO si su objeto es evidenciable con una entrada distinta del manifiesto… `[MESA FIRMA la política aquí o el acto la deja PROPUESTA y solo enlaza los casos sin par]`"*.
- Búsqueda en `canon/gobernanza-v1_15.md` (los 80 ADR) y en `forense/`: **cero firmas** sobre pares. El único texto en repo es la instrucción de ENLACE-1 de declararla y no resolverla.

**Conclusión: la ranura sigue vacía. Este acto NO adjudica pares. Enlaza los sin-par y lo declara — literal.**

**Qué es un "par", derivado del precedente literal, no de una lectura amplia.** ENLACE-1 §5 lo define citando el caso: *"N3: 2 filas `SI` + 2 filas `NO_DETERMINADO`, mismo `necesidad_id`, distinto `objeto_evidencia_id_canonico`"*. Verificado fila a fila en el árbol:

```
REL-eca053bf7ea89319271a2788 ENSAFI capa2=SI                OE=OE-e7969017… id_manif=ensafi2023_bd_csv_zip
REL-ed3674d93fbcd45914630569 ENSAFI capa2=SI_O_REFERENCIADO OE=OE-fb259558… id_manif=NO_DETERMINADO
REL-f995dd9800e710f436335657 ENFIH  capa2=SI                OE=OE-2964c990… id_manif=enfih2019_fd_xlsx
REL-3b746c49c7c051083df6ee81 ENFIH  capa2=SI_O_REFERENCIADO OE=OE-7419790… id_manif=NO_DETERMINADO
```

Reproduce el precedente exacto. **Un par es, entonces: misma `necesidad_id` + MISMA `fuente_canonica_normalizada`, con una fila ya `SI` y su gemela todavía `SI_O_REFERENCIADO`, distinto `objeto_evidencia`.** Es la mitad-resuelta cuya política de cierre está sin firmar.

Se midieron y se descartan explícitamente las otras tres lecturas posibles, para que nadie las herede como si fueran ésta: (i) "necesidades donde ENSAFI y ENFIH coexisten" → 10 necesidades, 27 filas; (ii) "fila cuya necesidad ya tiene ≥1 `SI` de cualquier fuente" → 42 filas; (iii) "fila que comparte necesidad con otra de las 68" → 58 filas. **Ninguna de las tres es el precedente que ENLACE-1 describió**; la lectura (ii) en particular llamaría "par" a una fila de GPS porque WVS resolvió la misma necesidad — dos fuentes distintas no son un par, son dos fuentes.

**Alcance resultante, contado:**

| | filas |
|---|---|
| **SIN PAR — este acto las adjudica** | **48** |
| **CON PAR — verdicto se registra como PROPUESTA, no se escribe** | **20** (ENSAFI 9 · ENFIH 8 · ENBIARE 3) |
| total clase-limbo | 68 |

Las 20 con par se examinan igual —el trabajo no se tira— y su veredicto queda escrito en esta nota como propuesta para cuando mesa firme; lo que no ocurre es la escritura. Las necesidades afectadas: N3, N4, N10, N12, N13, N14.

---

## §5 · La cuestión mecánica del `NO_REFERENCIADO` — un conflicto aparente, resuelto y declarado

La política (a) manda escribir `NO_REFERENCIADO` en las filas que la verificación tumba. **La vía no puede hacer eso**: `via_capa2.py:168` es `derivado = "SI" if estado == "COINCIDE" else actual` — solo promueve, nunca degrada, y una fila sin `id_manifiesto` ni siquiera entra a esa rama. Y el perímetro de ENLACE-1 decía *"`capa2` la escribe LA VÍA, no tú"*.

**No es contradicción, es división de trabajo — y así se resuelve, declarándolo antes de escribir:**

1. La prohibición de ENLACE-1 protege contra una **promoción** no ganada: escribir `SI` a mano saltándose la verificación de payload contra disco. Ese riesgo aquí no existe: **ningún `SI` de este acto se escribe a mano.** Se escribe `id_manifiesto` + `sha256_fuente`, y **la vía** decide si eso vale `SI`, verificando sha256 y tamaño contra el disco real. El contador lo produce la vía, no yo — como el encargo exige.
2. La **degradación** `SI_O_REFERENCIADO → NO_REFERENCIADO` es la dirección opuesta y no tiene mecanismo automático: es precisamente el juicio humano que H4 lleva abierto y que este encargo, del 14/ago, ordena emitir. El encargo posterior gobierna.
3. **`capa3_disco_real` se mueve con `capa2_manifiesto`.** Crosstab re-derivado sobre las 197 filas, **biyección perfecta, cero excepciones**: `SI`↔`EXISTE;COINCIDE;INTEGRO` (43) · `SI_O_REFERENCIADO`↔`SI_O_PARCIAL` (68) · `NO_REFERENCIADO`↔`NO_REFERENCIADO` (86). Degradar capa2 sin capa3 rompería un invariante que hoy se cumple sin excepción y que ya costó un acto propio mantener (CAPA3-RECONCILIA, PR #202, 19 desacuerdos → 0). Las filas adjudicadas a `NO_REFERENCIADO` reciben el par completo.
4. **`capa4_apertura_mapeo` NO se toca.** No es biyectiva con capa2 (las 86 `NO_REFERENCIADO` tienen 10 valores distintos de capa4, 42 vacías) y su dominio es apertura, no enlace. Fuera de perímetro.

---

## §6 · Los tres lotes — división por fuente, congelada antes de repartir

Las 68 se reparten **por fuente**, en tres lotes coherentes por familia de origen. La división es de trabajo, no de criterio: **los tres lotes reciben la misma política verbatim de §1 y el mismo mecanismo de §3.**

| lote | familia | filas | fuentes |
|---|---|---|---|
| **A** | ENSAFI + ENFIH — el dominio de dinero, donde viven los pares | **28** | ENSAFI 14 · ENFIH 14 |
| **B** | INEGI / oficial mexicano | **28** | ENBIARE 5 · FINANZAS 5 · ENVIPE 3 · ENIF 3 · ENCIG 3 · ENCOAP 2 · BIARE · CCPV · ENCUCI · ENIGH · ENNVIH · ENOE · IMSS |
| **C** | externas, académicas y residuales | **12** | GPS · GLOBAL_PREFERENCES_SURVEY · LATINOBARÓMETRO · FABLE · PUB · SE · RELLABORALES · RELLABORALESPRUEBA · REPOSITORIOS_UNAM_COLMEX_ITAM_DATAVERSE_ICPSR · VOTAR_ENTRE_BALAS · EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009 · SIN_CANDIDATO_IDENTIFICADO |

28 + 28 + 12 = 68 ✓

**Disciplina de ejecución de este acto, declarada por adelantado porque cambia cómo debe auditarse:** los tres lotes se instruyen en paralelo, cada uno con su lote, la política verbatim y la orden de **proponer, nunca escribir** — devuelven, por fila, `veredicto · evidencia_abierta (archivo:línea) · id_manifiesto o razón`. **Ninguna propuesta se acepta sin verificación propia contra el repo**: se abren al azar ≥3 evidencias por lote y se confirman byte a byte contra el archivo citado; **un lote con una sola evidencia falsa se descarta entero y se rehace en primer plano.** Lo que se escriba en Commit 2 será exactamente lo verificado, ni una fila más.

---

## §7 · Las 19 `INDEXADO-NO-DESCARGADO` — política (b), congelada

**Hallazgo que cambia la forma del paso, verificado antes de tocarlo: las 19 y las 68 son conjuntos DISJUNTOS — solapamiento 0.** De las 19 (`capa4_apertura_mapeo = INDEXADO-NO-DESCARGADO`): **7 ya son `capa2 = SI`** (las que ENLACE-1 enlazó: ISSP ×4 — N2, N12, N13, N30 — y CSES ×3 — N17, N25, N26) y **12 son `NO_REFERENCIADO`**. **Cero** están en la clase-limbo. Es un paso independiente, no un subconjunto del anterior — el encargo lo trata aparte con razón.

Regla congelada, del inciso (b) verbatim: **por celda, qué payload falta**; si ese payload **está en el manifiesto** ⇒ es apertura pendiente, va a **lista-de-apertura**; si **no está** ⇒ va como **PROPUESTA a la cola de adquisición** (la palanca y la firma de lote son de mesa, no de este acto). Este paso lo ejecuta el orquestador fila por fila, sin repartir: son pocas y cada una decide destino propio.

---

## §8 · Lo que este acto NO hace

No descarga nada (sin red) · no escribe `capa2 = SI` a mano —eso lo produce la vía, siempre— · **no adjudica los 20 pares** (RANURA (c) sin firma, §4) · no toca `alias-fuentes.yaml` (acto de alias aparte) · no toca `capa4` · no toca `tools/curador_registro/` (la ventana ADR-70(d) sigue abierta pero este acto **consume** la vía, no la mantiene) · no toca el crosswalk ni el puntero de puertas (eso es SANEA-MAPEO, carril paralelo) · no resuelve la anomalía de catálogo de N17 que ENLACE-1 declaró.

**La frase:** el primer resultado que produzca este procedimiento es el que se reporta.

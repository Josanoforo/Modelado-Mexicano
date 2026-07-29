# Censo de integridad documental · `canon/` + `forense/`
### `censo-integridad` · **v1.0** · 29 de julio de 2026 · Auditoría interna, no aplicada al corpus

> | | |
> |---|---|
> | **ARCHIVO** | `censo-integridad-v1_0.md` |
> | **QUÉ ES** | Censo completo (no muestreo) de afirmaciones mecánicamente comprobables sobre el estado del propio corpus, en `canon/` (5 archivos) y `forense/` (14 archivos incl. `notas/`). Complementado con un censo de vocabulario extendido a `corpus/` (36 archivos) porque varias cifras que `canon/` cita como verificadas viven ahí. |
> | **QUÉ NO ES** | No corrige nada. No audita si un tier está bien asignado ni si una fuente externa dice lo que se le atribuye. Eso es juicio de contenido — otra campaña. |
> | **VERIFICAS ASÍ** | §0 declara HEAD y denominador exacto por clase · §9 trae HEAD, suite y lo no verificado, al final, como pide el encargo |

---

## 0 · Estado, alcance y denominador — el censo empieza aquí

**HEAD auditado:** `9efa61f79f9be4d7d2dcf361062fa54e3e944bce` (rama `claude/modelado-mexicano-audit-rugaa3`, working tree limpio).

**Suite real, corrida en este HEAD, hoy:**

```
18 FAIL · 111 WARN
T01 ok · T02 ok · T03 warn(45) · T04 ok · T05 FAIL(5) · T06 FAIL(2) · T07 FAIL(1) ·
T08 FAIL(1) · T09 FAIL(8) · T10 warn(65) · T11 FAIL(1) · T12 ok · T13 warn(1)
```
`tests/validador_registro_ids.py`: **OK** — 49 reglas, 27 en perímetro, 49 IDs verificados con ancla y tier consistentes.

### Universo declarado

| Bloque | Archivos | Líneas | Dentro del censo |
|---|---|---|---|
| `canon/` | 5 | 1,985 | **Sí, íntegro** |
| `forense/` (incl. `notas/`) | 14 | 2,222 | **Sí, íntegro** |
| `milpa/` (3 `.md` + 3 `.yaml`) | 6 | 1,781 | Leído como **referente obligado**: `canon/` y `forense/` hacen afirmaciones cuantitativas sobre estos archivos (reglas implementadas, coeficientes, refutaciones corridas) que solo se verifican abriéndolos |
| `tests/` (`check.py`, `validador_registro_ids.py`) | 2 | 590 | Ejecutado como **fuente de verdad mecánica** (T01-T13 y el validador de IDs), no auditado como prosa |
| `corpus/reports/` (31) + `corpus/forense/` (5) | 36 | 8,194 | **Fuera** del censo por instrucción explícita — **excepto** el inventario de vocabulario de tier/procedencia (clase C6), extendido aquí porque `canon/` (README, `estado`, `glosario`) cita cifras agregadas sobre ese vocabulario (p. ej. "`SÓLIDO`×44 · `MEDIO`×29 · `HIPÓTESIS RAZONABLE`×22") como si estuvieran verificadas por la suite — verificarlas exige leer el corpus que describen |
| `TRANSFER-maestra-7.md`, `TRANSFER-maestra-8.md`, `instrucciones-proyecto-v2.md`, `README.md`, `CONTRIBUTING.md` | 5 | — | Fuera de alcance como objeto de censo; se leen **solo la línea** cuando son referente de una cita auditada (mismo criterio que los reports) |
| **Total archivos en el repo** (`git ls-files`) | **71** | — | — |

### Denominador de afirmaciones por clase (instancias efectivamente extraídas y verificadas)

| Clase | Universo verificado | Instancias censadas | Método |
|---|---|---|---|
| **C1** · Cifras derivables | `canon/` (5) + `forense/` (14) + cruces con `milpa/*.yaml` | **≈50** | Recálculo manual (`grep -c`, `wc -l`, conteo de encabezados/filas) contra cada cifra |
| **C2** · Campos `VERIFICAS ASÍ` | Los 5 archivos de `canon/` que tienen bloque de cabecera (todos salvo `integrador`, que no lo tiene — ver C5) | **4 campos**, cada uno con 2-4 sub-afirmaciones = **11 sub-verificaciones** | Ejecución literal de lo que cada campo indica verificar |
| **C3** · Referencias `archivo:línea` y citas | `forense/` (13 archivos con esta clase de referencia) + cruces desde `canon/` | **≈26** | Apertura del archivo referido, lectura de la línea exacta, comparación textual |
| **C4** · Cobertura "N de M" | `canon/` + `forense/` | **≈23** | Enumeración real contra la cifra declarada |
| **C5** · Punteros de versión / existencia de archivo | `canon/` + `forense/` + `milpa/` | **≈9** | `find`/`ls` contra cada referencia |
| **C6** · Vocabulario de tier y procedencia | `canon/` + `forense/` (13 archivos) **+ extensión a `corpus/`** (36 archivos, ver nota arriba) | **20 etiquetas de tier distintas** + **9 convenciones de procedencia distintas** | Censo por `grep`, no muestreo — reconciliado contra el regex real de `tests/check.py` |

**Total de instancias individuales verificadas en este censo: ≈142**, ninguna por muestreo — cada una tiene cita `archivo:línea` y fue abierta y comparada contra su fuente.

---

## 1 · Tabla completa de veredictos

Se listan **todas** las instancias con hallazgo verificable, agrupadas por clase. Las instancias de T03/T10 (45 y 65 respectivamente) no se transcriben una por una porque **son ellas mismas el artefacto exhaustivo**: `tests/check.py` ya las enumera al 100% en su salida (ninguna requiere juicio adicional, son *pattern matches* mecánicos); se referencian por conteo y se verifica que el conteo mecánico sea reproducible (lo es: confirmado dos veces, HEAD idéntico).

### C1 · Cifras derivables

| ID | Archivo:línea | Afirmación | Valor esperado | Valor real (recalculado) | Veredicto |
|---|---|---|---|---|---|
| C1-01 | `canon/estado-programa-v1_9.md:54` | "**56 archivos**, verificados... sin discrepancias" | 56 | Suma de la propia tabla (L58-65): 31+5+3+3+6+4+6+1 = **59** | **INCORRECTO** |
| C1-02 | `canon/estado-programa-v1_9.md:25` vs `:95` | "37 ADR" (L25) vs "32 ADR" (L95) | Un solo valor | `gobernanza-v1_9.md` tiene **37 ADR únicos** (ADR-01 a ADR-37, sin huecos, `grep` verificado) | **INCORRECTO** (contradicción interna en el mismo archivo) |
| C1-03 | `canon/estado-programa-v1_9.md:91` vs `:121` | "18 de 43 reglas implementadas" (L91) vs "26 reglas fuera de la implementación" (L121) | 43−18 = 25 | Declarado: 26 | **INCORRECTO** (25≠26) |
| C1-04 | `canon/estado-programa-v1_9.md:91`; `milpa/procedencia.yaml:57` | "18 de 43" reglas implementadas | Verificable contra `milpa/*.yaml` | El único YAML de dominio (`tramite.yaml`) tiene **5 entradas** (4 reglas motor). "43" es la cuenta del motor en v2.1 (hoy v3.3 = 49 reglas); "18" no tiene sustento localizable en ningún archivo del repo | **NO-VERIFICABLE** (posible resto de una versión de milpa/ que ya no existe así) |
| C1-05 | `milpa/procedencia.yaml:250-256` | Título de sección: "LOS **14** COEFICIENTES DE GENERADOR" vs cuerpo: "Los **15** coeficientes son todos ASIGNADO" | Un solo valor | Conteo real de la tabla `detalle`: G1(2)+G2(2)+G3(3)+G4(4)+G5(3)+G6(1) = **15** | **INCORRECTO** (título desactualizado tras ADR-30) |
| C1-06 | `canon/estado-programa-v1_9.md:208,234` (idéntico) | "La suite corre completa: **18 FAIL · 107 WARN**" | Reproducible en HEAD actual | Corrida real: **18 FAIL · 111 WARN**. Causa raíz: `TRANSFER-maestra-7.md:49` y `TRANSFER-maestra-8.md:26` (fusionados al HEAD antes de que este archivo se escribiera) citan literalmente `-v3.2.md`/`-v3_2.md` como ejemplo y T03 los cuenta como referencias colgantes (+4 WARN: 45 vs 41 declarado) | **INCORRECTO**, alta severidad — ver Finding destacado abajo |
| C1-07 | `canon/estado-programa-v1_9.md:124` | "T03 produce **41** WARN, no 44... total WARN de la suite es **107**, no 110" | Reproducible hoy | T03 real hoy: **45**. Total real: **111** | **INCORRECTO** (mismo origen que C1-06) |
| C1-08 | `canon/integrador-psicologia-mexicano.md:2,10,434` | "30 reports" / "los 30 reports" (título, cuerpo, colofón) | 31 (verificado contra disco) | `ls corpus/reports/*.md \| wc -l` = **31** | **INCORRECTO** — nunca actualizado tras la verificación del 28/jul (`gobernanza:65`: *"Eran '30' por conteo de memoria; verificado contra disco el 28/jul"*) |
| C1-09 | `canon/glosario-v5_6.md:44` | "Corpus a la vista: **60** archivos — **30** reports temáticos..." | 31 reports actuales; conteo de archivo total ya superado varias veces | Sección explícitamente fechada 27/jul (antes del párrafo de correcciones de v5.1+); funciona como nota histórica dentro de un documento vigente | **OBSOLETO-POR-DISEÑO sin nota fechada** — a diferencia de otras correcciones de este mismo glosario (que sí llevan tabla de cambios v5.1-v5.6), esta línea nunca se marcó como superada |
| C1-10 | `milpa-plan-v0_1.md` (tabla Parte I.1, fila "Modelo §1 perfiles") | "Los 6 perfiles con sus **9** parámetros base" | 15 (glosario §13, modelo §0/§2.2, `procedencia.yaml`) | Confirmado en 4 fuentes independientes: 15 params × 6 perfiles = 90 | **INCORRECTO** (stale, anterior a ADR-30) |
| C1-11 | `forense/barrido-propagacion-forense-v1_0.md` L3/15/129 | "22 veredictos ROMPE/MATIZA", "~41% de fuga" | Suma enumerada | 8+6+3+5=**22** ✅; fuga 6(no llegó)+3(a medias)=9/22=40.9%≈41% ✅ | **CORRECTO** |
| C1-12 | `forense/corrida-refutaciones.md` L30-33 | 27 pasan / 3 fallan / 8 sin objeto / 11 requieren ejecutable / total 49 | `milpa/refutations.yaml primera_corrida.resultados` | Coincide **exacto** en las 5 cifras | **CORRECTO** |
| C1-13 | `milpa/refutations.yaml` tipología | 28 tipo A + 11 tipo B + 10 tipo C = 49 | `grep -c "id: ref.A/B/C"` | 28 / 11 / 10 = **49** | **CORRECTO** |
| C1-14 | `canon/glosario-v5_6.md §13`, `modelo §6`, `modelo §2.2`, `procedencia.yaml resumen` | 144 números: 4 MEDIDO + 6 DERIVADO + 60 ORDINAL→CARDINAL + 74 ASIGNADO | Suma | 4+6+60+74=**144**, y **cuadra en las 4 fuentes** de forma independiente | **CORRECTO** |
| C1-15 | `forense/hitoD-R1_1-veredicto-v1_0.md:49` | "el productor pone ~**2.5%** de la prima" | 80.7/3,262.2 | = **2.474%** ≈ 2.5% | **CORRECTO** |
| C1-16 | `forense/hitoC-prueba-generadores.md` (atribuido por `estado:69` como fuente de "42 reglas") | "42 reglas" | `grep -c "42" forense/hitoC-prueba-generadores.md` | **Cero** resultados — la cifra no está en el archivo que se cita como su origen | **INCORRECTO** (la atribución en `estado:69`, no el archivo mismo) |
| C1-17 | `tramite.yaml` — 5 entradas YAML | ¿representan cuántas reglas del motor? | `modelo §3.3` = 4 reglas (R3.1-R3.4) | 5 entradas = 4 reglas (R3.4 compilado como par espejo `coercitivo`/`util_sin_coercion`), consistente con el propio changelog del YAML | **CORRECTO** |
| C1-18 | `forense/notas/2026-07-29-perimetro-suite-T07-T10.md` §2/§3 | T09: 8 ya atrapados + 18 nuevos = 26; T10: 39+1+5=45 nuevos | Aritmética | 5+2+1=8 ✅; 0+16+2=18 ✅; 39+1+5=45 ✅ | **CORRECTO** |
| C1-19 | `forense/hitoD-preregistro-v2_0.md:8,13` | "27 fichas", "27 de 27" | `grep -c "^## R"` | **24** | **INCORRECTO** — ya autocorregido dentro del mismo archivo (Nota 2, L372-386, fechada 29/jul); ver §4 |
| C1-20 | Vocabulario T07 (canon cita: `SÓLIDO`×44 · `MEDIO`×29 · `HIPÓTESIS RAZONABLE`×22) | Conteo del propio test | `grep -o "\[HIPÓTESIS RAZONABLE\]" corpus/reports/*.md \| wc -l` = 22 (coincide con T07); pero `grep -o "HIPÓTESIS RAZONABLE" corpus/reports/*.md \| wc -l` (sin exigir corchetes) = **35**, en **14 archivos** | El regex de T07 exige la forma exacta `[HIPÓTESIS RAZONABLE]` (con corchetes); hay 13 ocurrencias adicionales del mismo vocabulario prohibido sin corchetes que T07 no cuenta | **INCORRECTO** (defecto del propio test T07 — sección 8) |

### C2 · Campos `VERIFICAS ASÍ`

| Archivo | Campo (literal) | Ejecución | Veredicto |
|---|---|---|---|
| `estado-programa-v1_9.md:8` | "§0 lista `modelo` en v3.3 y `hitoD-R1.1`" | `modelo` §0 dice v3.3 ✅; `hitoD-R1.1` se lista en la tabla de nomenclatura ✅ | **CORRECTO** |
| `estado-programa-v1_9.md:8` | "§7 registra el pre-registro en 24 de 27, no en 27 de 27, y ya no dice '47 reglas'" | §7 (L167) dice "24 de las 27 del perímetro" ✅; `grep -c "47 reglas" estado-programa-v1_9.md` = 0 ✅ | **CORRECTO** |
| `estado-programa-v1_9.md:8` | "§4·S2 trae el rótulo corregido del perímetro (20+1+1+5, no 20+5+2)" | L112 confirma "20+1+1+5 = 27" ✅ | **CORRECTO** |
| `glosario-v5_6.md:8` | "§15 marca la deuda de ENA 2017 + AMUCSS 2014 como CERRADA" | §15 (L413) dice "✅ CERRADA el 28/jul/2026" ✅ | **CORRECTO** |
| `gobernanza-v1_9.md:8` | "ADR-36 tiene adenda (c) sobre series numeradas" | L248-249 confirma "(c) Adenda del 28/jul" ✅ | **CORRECTO** |
| `gobernanza-v1_9.md:8` | "§2 lista los tres `milpa-*`" | L77-79 lista `milpa-whitepaper`, `milpa-spec`, `milpa-plan` ✅ | **CORRECTO** |
| `gobernanza-v1_9.md:8` | "§4 (registro del perímetro del Hito D) trae la corrección de RÓTULO fechada 29/jul — el perímetro sigue en 27" | L268 confirma la corrección fechada y "27 reglas" ✅ | **CORRECTO** |
| `modelo-decision-v3_3.md:8` | "§0 llega al cambio 35" | Tabla de cambios llega hasta "35 · Registro congelado de IDs" ✅ | **CORRECTO** |
| `modelo-decision-v3_3.md:8` | "R1.1 de §3.1 trae la marca `DOMINIO AGRÍCOLA: INEJECUTABLE`" | L213 confirma literal "🚫 **DOMINIO AGRÍCOLA: INEJECUTABLE**" ✅ | **CORRECTO** |
| `modelo-decision-v3_3.md:8` | "§7 trae el Registro congelado de IDs (tabla de 49 filas)" | Tabla L414-464 — **conteo real: 49 filas** (verificado por conteo manual de la tabla + confirmado por `validador_registro_ids.py`: "49 IDs verificados") | **CORRECTO** |
| `integrador-psicologia-mexicano.md` | — | **No tiene campo `VERIFICAS ASÍ`** porque no tiene bloque de cabecera (ADR-36) en absoluto | Ver C5-01 |

**C2 no tuvo un solo fallo** — es, junto con T12 del suite, la clase con mejor densidad de exactitud de todo el censo. Once de once sub-verificaciones correctas.

### C3 · Referencias `archivo:línea` y citas entrecomilladas (selección de mayor severidad; el listado completo de 26 vive en el informe de origen)

| ID | Cita auditada | Dónde se hace la afirmación | Verificación | Veredicto |
|---|---|---|---|---|
| C3-01 ⭐ | `curaduria-archivos.md:23` — *"convirtió un `[MEDIO], muestra mexicano-americana` en un `Fuerte` pelón"* | `forense/notas/2026-07-29-b-correccion-perimetro.md §5` (L121-129,155,171) afirma: **"la frase citada no aparece en ese archivo, ni en ningún otro del repo"**, y que `grep -rn "pelón"` solo la encuentra dentro de la propia nota | **Falso.** `sed -n '23p' forense/curaduria-archivos.md` muestra la frase **verbatim**. `grep -rn "pelón"` da **3 apariciones reales** además de la nota: `verificacion-red-team-vs-corpus.md:12` (fuente original), `curaduria-archivos.md:23` (exactamente donde se dice que no está) y `forense/notas/2026-07-29-perimetro-suite-T07-T10.md:87` (que la cita correctamente, sin refutarla) | **INCORRECTO** en la nota `2026-07-29-b-...md`, propagado a `canon/estado-programa-v1_9.md:212` (*"una cita suya a `curaduria-archivos.md:23` no checa contra el archivo"*) |
| C3-02 | `hito2-modelo-fantasma.md` referenciado en `estado-programa-v1_9.md:62,69` como archivo existente ("Forenses de proceso") | ¿Existe el archivo? | `find . -iname "*hito2*"` = **vacío**. `curaduria-archivos.md:112` lo marca "Listo para subir" y `:141` lo lista como ítem de checklist **sin marcar** (`[ ] Subir hito2-modelo-fantasma`) | **INCORRECTO** — el archivo nunca se subió; `estado` lo cuenta en su inventario "verificado por diff, sin discrepancias" |
| C3-03 | `forense/hitoD-R1_1-veredicto-v1_0.md` §5 — tabla de descartes, "cero de seis candidatos sobrevivieron al confusor" | ¿Existe la tabla y tiene 6 filas? | Confirmado: 6 filas (Fondos de Aseguramiento, Seguro Agrícola Catastrófico, Fondo CNOG pecuario, Seguros estatales Tlaxcala, Producción para el Bienestar, Adopción voluntaria ENA) | **CORRECTO** |
| C3-04 | `README.md:40` — "1 de 27... `R1.1` → `B`" vs `hitoD-R1_1-veredicto-v1_0.md` — veredicto **D** | Mismo hecho, dos fuentes | Contradicción directa. `TRANSFER-maestra-7.md` (fuera del censo, pero explica la causa): un candidato no buscado (Fondos de Aseguramiento del sur/indígenas) degradó el veredicto de D a B en una revisión posterior no incorporada al forense append-only | **OBSOLETO-POR-DISEÑO** — el forense append-only queda correctamente congelado en D; el estado vigente (README) ya dice B, y el archivo append-only nunca debía cambiar |
| C3-05 | `forense/descartes-forenses-registro.md` tabla §1 vs `canon/estado-programa-v1_9.md:122` "3 de 5 forenses sin tabla de descartes" | Conteo estricto de la columna "Tabla de descartes" | Columna real: ✅Sí=1 (V1) · ❌No=3 (V2,V4,V5) · ⚠️Mención sin tabla=1 (V3). "3 de 5" solo cuadra si V3 no se cuenta como "sin tabla" — lectura posible pero no explicitada en ninguna de las dos fuentes | **AMBIGUO / INCORRECTO-CONDICIONAL** — defendible solo bajo una distinción que nadie declaró |
| C3-06 | `README.md` atribuye a "una auditoría manual de los cuatro pivotes, hecha ese mismo día" los conteos "4" (Gini, confianza interpersonal, vocabularios de tier, marco (c)) | ¿`forense/lectura-cuatro-pivotes.md` es esa fuente? | `grep -n "Gini" forense/lectura-cuatro-pivotes.md` = **0 resultados**; el archivo no cuenta Gini, ni vocabularios de tier del corpus completo, ni usos de marco (c); además está fechado **27/jul**, no "28/jul" (el día que el README describe) | **INCORRECTO / NO-VERIFICABLE** — el README no cita ningún artefacto real para esos cuatro conteos "manuales"; ninguno de los 13 archivos de `forense/` los contiene |
| C3-07 | `curaduria-archivos.md:66` (27/jul) — "su orden de retirar 'honor' ya se ejecutó en la fuente" | `canon/glosario-v5_6.md:385` (verificación 28/jul) | El glosario desmiente esto explícitamente: *"Las dos afirmaciones eran falsas... la decisión se había tomado y registrado, pero la nota nunca bajó al documento"* | **INCORRECTO** en `curaduria-archivos.md:66`, **ya corregido** en la cadena posterior (glosario v5.2, gobernanza, estado) |

### C4 · Afirmaciones de cobertura "N de M"

| ID | Afirmación | Enumeración real | Veredicto |
|---|---|---|---|
| C4-01 | "27 fichas / 27 de 27" (`hitoD-preregistro:8,13`) | 24 fichas reales (`grep -c "^## R"`) | **INCORRECTO** — con nota fechada de autocorrección ya adjunta (ver §4) |
| C4-02 | "24 de 27" (`estado §4·S2,§7`, `gobernanza §4`) | Confirmado: 18 FUERTE+4 MEDIA-FUERTE+1 FUERTE-correlación+1 FUERTE/MEDIA=24 | **CORRECTO** |
| C4-03 | "20+5+2 compuestas" (rótulo viejo) vs "20+1+1+5=27" (rótulo corregido, `modelo` cambio 34, `gobernanza` corrección de rótulo 29/jul) | Solo R4.3 es compuesta; R1.4 es tier distinto. 20+1+1+5=27 | **CORRECTO** (la corrección de rótulo, que ya estaba pedida como confirmar en el encargo) |
| C4-04 | "27 pasan+3 fallan+8 sin objeto+11 requieren ejecutable=49" | Confirmado en `refutations.yaml` y `corrida-refutaciones.md`, cifras idénticas | **CORRECTO** |
| C4-05 | "8 refutaciones sin objeto" — ¿enumeradas por ID en algún lado? | `milpa/refutations.yaml` solo nombra explícitamente `ref.A.02`; `forense/corrida-refutaciones.md` **sí enumera las 8 completas** (`ref.A.02, A.04, A.14, A.20, A.28, B.04, B.06, A.17`), con tiers que coinciden exactamente con el YAML | **CORRECTO** — pero la fuente canónica más citada (`estado`, `gobernanza`) nunca enumera las 8, solo menciona 1; deuda de completitud, no error |
| C4-06 | "de 13 reglas que las verticales dijeron estresar: 6 no existían, 4 divergían, 3 eran fieles" | 6+4+3=13 ✅ (`curaduria-archivos.md:112`: "6 fantasma / 4 diverge / 3 fiel"; `prompts-verticales-validacion.md:15,68` coincide) | **CORRECTO** — pero la cifra **no aparece** en `red-team-cuatro-verticales.md` ni en `verificacion-red-team-vs-corpus.md`, los dos archivos donde por tema sería más esperable encontrarla (vive en un archivo, `hito2-modelo-fantasma.md`, que no existe en disco — ver C3-02) |
| C4-07 | "56 archivos" vs suma de tabla = 59 | Ver C1-01 | **INCORRECTO** |
| C4-08 | Vocabulario de tier "ajeno al Bloque A": T07 declara 7 etiquetas | Censo extendido a `corpus/` encuentra **≥20** etiquetas distintas no-canónicas (ver §5) | **INCORRECTO por incompletitud** — no porque T07 mienta sobre lo que sí cuenta, sino porque su regex es más angosto que el universo real |
| C4-09 | `descartes-forenses-registro.md:6`: "31 casos filtrados a 16... 15 descartes, 14 nunca escritos" | `prompts-verticales-validacion.md:63` coincide exacto (31→16=15, 14 sin justificar) | **CORRECTO** |
| C4-10 | Perímetro Hito D = motor real (T12/validador) | 20+19+5+2+1+1+1=49 (T12); 27 en perímetro (validador) | **CORRECTO**, doblemente confirmado por dos mecanismos independientes (`check.py` y `validador_registro_ids.py`) |

### C5 · Punteros de versión y existencia de archivos

| ID | Afirmación | Verificación | Veredicto |
|---|---|---|---|
| C5-01 | Los 5 archivos de `canon/` deben llevar bloque de cabecera ARCHIVO/REEMPLAZA A/VERIFICAS ASÍ/NOMBRE ESTABLE (ADR-36.a, "requisito de salida: un archivo sin bloque de cabecera no se sube") | `integrador-psicologia-mexicano.md` **no tiene ese bloque** (confirmado por lectura directa y por T13 WARN de la suite) | **INCORRECTO** — viola un requisito de salida explícito del propio ADR-36, vigente hoy |
| C5-02 | `gobernanza-v1_9.md §2` — tabla "Cadena de dependencia y fuentes de verdad" cita `glosario-v5.5.md`, `modelo-decision-v3.0.md`, `estado-programa-v1.1.md` | Versiones actuales: glosario v5.6, modelo v3.3, estado v1.9 | **INCORRECTO** — tabla no tocada desde gobernanza v1.1 pese a que el propio documento ya va en v1.9 |
| C5-03 | `gobernanza-v1_9.md §7` "Bitácora de versiones de este documento" | Filas: 1.0, 1.8, 1.7, ..., 1.1 — **ninguna fila para 1.9**, la versión actual del documento | **INCORRECTO** (autorreferencia incompleta) |
| C5-04 | Serie MILPA: orden de lectura vive en el cuerpo, no en el nombre (ADR-36.c) | Los 3 archivos (`milpa-whitepaper-v0_1.md`, `milpa-spec-v0_2.md`, `milpa-plan-v0_1.md`) traen el mismo bloque "1. whitepaper · 2. spec · 3. plan" en cabecera | **CORRECTO** — consistente en los 3 |
| C5-05 | `hito2-modelo-fantasma.md` (ver C3-02) | No existe en disco | **INCORRECTO** |
| C5-06 | `prompts-verticales-validacion.md` — ¿versionado? | `estado:32` dice "Operativo (sin versionar aún)"; el archivo confirma no tener bloque ADR-36 | **CORRECTO** (consistente entre canon y el archivo real) |
| C5-07 | ¿Algún "REEMPLAZA A — borrar" quedó sin ejecutar? | `estado-programa-v1_9.md:7` dice "REEMPLAZA A: `estado-programa-v1.8.md` — borrar"; `find . -name "*v1_8*"` (y variantes v1.8) = vacío. Igual para `glosario`, `gobernanza`, `modelo` frente a sus predecesores inmediatos | **CORRECTO** — el protocolo de borrado de la versión inmediatamente anterior sí se ejecuta consistentemente |
| C5-08 | `milpa-plan-v0_1.md` tabla "9 parámetros base" | Ver C1-10 | **INCORRECTO** |
| C5-09 | `tests/validador_registro_ids.py` — "nuevo, NO cableado a `check.py`" (mensaje de commit `9efa61f`) | `tests/check.py` no importa ni ejecuta `validador_registro_ids.py`; deben correrse por separado (confirmado al ejecutar ambos) | **CORRECTO** |

### C6 · Vocabulario de tier y marca de procedencia

**Sancionado por el glosario (§1):** Tier: `Fuerte` · `Media` · `Hipótesis razonable` · `Narrativa popular`. Procedencia: `(a)` EN México · `(b)` diáspora · `(c)` marco importado.

**Inventario completo de vocabulario de tier no-canónico (extendido a los 36 archivos de `corpus/`, porque las cifras que canon cita viven ahí):**

| Etiqueta | Ocurrencias | Archivos | Nota |
|---|---|---|---|
| `SÓLIDO`/`[SÓLIDO]` | 44 (T07) / 64 en censo ampliado (formas sueltas incl. "MÁS SÓLIDO") | 8 | Conocida, ya en T07 |
| `MEDIO` | 29 (T07) / 45 en censo ampliado | 10 | Conocida |
| `HIPÓTESIS RAZONABLE` (mayúsculas) | 22 (T07, solo forma con corchetes) / **35 real** (con y sin corchetes) | 3 (T07) / **14 real** | Ver C1-20 — el regex de T07 subcuenta |
| `Moderada` | 3 | 1 | Conocida |
| `MODERADA` | 2 | 1 | Conocida |
| `MODERADA-FUERTE` | 1 | 1 | Conocida |
| `Narrativa exagerada` | 1 | 1 | Conocida |
| **`FUERTE`** (mayúsculas, en cualquiera de sus notaciones: `[FUERTE]`, `Tier: FUERTE`, `EVIDENCIA FUERTE`, `Calificación: FUERTE`) | **171** | **20** | **NUEVO** — no en la lista de 7 que T07 reporta; la variante de mayor volumen de todo el corpus |
| **`MEDIA-FUERTE`/`MEDIO-FUERTE`** | 10 | ≥4 | **NUEVO** |
| **`DÉBIL`** como tier | 2 | 2 | **NUEVO** — palabra que ni existe en el glosario de 4 etiquetas |
| **`[HIPÓTESIS]`** (forma corta) | 4 | 3 | **NUEVO** |
| **`[NARRATIVA]`** (forma corta) | 1 | 1 | **NUEVO** |
| **Esquema `Calificación: [TIER]`** | 6 | 1 (`Psicología__Conducta_y_Sociedad...md`) | **NUEVO** — convención propia de un solo report |
| **Escala semáforo** (`Lectura: ÁMBAR/ROJO/VERDE/NEUTRAL`, `Veredicto: SEÑAL MIXTA`) | 11 | 1 (`Crédito_Fácil_y_Sobreendeudamiento...md`) | **NUEVO** — eje de clasificación paralelo al tier, sin equivalente en glosario |

**Total: al menos 20 etiquetas de tier distintas conviven en el corpus**, no 7 como reporta T07.

**Inventario de convenciones de procedencia no-formales (las 3 conocidas + 6 nuevas):**

| Convención | Dónde | Nota |
|---|---|---|
| `[Fuerte, con caveat US]` | Solo `canon/integrador-psicologia-mexicano.md` | Conocida (encargo) |
| `Caveat US:` | Solo `canon/integrador-psicologia-mexicano.md` | Conocida |
| `muestras US-hispanas` | Solo `canon/integrador-psicologia-mexicano.md` | Conocida |
| `muestra(s) mexicano-americana(s)` (frase libre) | ~15 reports | **NUEVO** |
| `mexicano-estadounidense(s)` | ≥2 reports | **NUEVO** (variante ortográfica) |
| `población/muestras latina(s) en EE.UU.` | ≥3 archivos | **NUEVO** |
| `HCHS/SOL` (dataset como marca implícita) | ≥6 archivos | **NUEVO** |
| `diáspora` (palabra explícita) | ≥8 archivos | **NUEVO** |
| **Inversión de (b)/(c)** respecto al glosario | `Health__Body__Food...md:52-54`, `Report_26...md:11` | **NUEVO Y GRAVE** — en ambos, (b)=marco importado y (c)=muestra mexicano-americana, exactamente al revés de la definición canónica ((b)=diáspora, (c)=marco importado). Ver Finding destacado, §4 |

**Cruce obligatorio — "trampa social":** aparece en **un solo archivo** de los 36, `Psicología_Política_y_Comportamiento_Cívico...md` (7 veces), siempre como mecanismo dentro de otra afirmación tierizada, nunca como fila propia de un mapa de evidencia. **Se confirma lo que declara el glosario §16: no tiene tier propio.** No se hallaron más casos del mismo patrón (constructo usado por el motor sin tier propio) en el barrido de vocabulario — los 5 fallos de T05 ya cubren la superficie conocida (`turnout buying`, `vote-choice`, `confianza personalizada`, `interruptor formal`, y un quinto).

---

## 2 · Cruce obligatorio: tiers del motor ↔ glosario

Confirmado (T05, real, 5 FAIL): `turnout buying`, `vote-choice`, `confianza personalizada`, `interruptor formal` y un quinto constructo del motor **no tienen entrada en el glosario**. De estos, README ya documenta que "dos los introdujo quien escribió el check" — es decir, el validador de T05 tiene un límite de alcance auto-referencial conocido (quien redactó el check también decidió qué constructos exigir). **No verificable de forma independiente cuáles 2 de los 5 son los "introducidos por el checker"** sin el historial de commits del propio `tests/check.py`, que está fuera del alcance documental de este censo.

## Cruce: reglas del motor ↔ los tres YAML

Solo existe **un** YAML de dominio real: `tramite.yaml` (5 entradas, 4 reglas de `§3.3`). Los otros dos YAML del directorio `milpa/` (`procedencia.yaml`, `refutations.yaml`) son archivos de auditoría/esquema, no de reglas de dominio — confirmado por lectura directa, consistente con lo que `estado-programa:91` describe ("solo `tramite.yaml` es de dominio"). **No hay reglas de motor implementadas fuera de `§3.3`** — los otros 9 dominios (§3.1, §3.2, §3.4-§3.10) no tienen YAML compilado. Esto hace que la cifra "18 de 43 reglas implementadas" (C1-04) sea, además de aritméticamente sospechosa, **imposible de reconciliar contra el disco real**: solo hay 4 reglas de motor con implementación YAML, no 18.

## Cruce: refutaciones corridas ↔ desglose declarado

Ya cubierto en C1-12/C1-13/C4-04/C4-05 — es el cruce que **mejor cuadra** de todo el censo: 3 fuentes independientes (`refutations.yaml`, `corrida-refutaciones.md`, y las citas de `modelo §7`/`estado §3`) dan exactamente 27/3/8/11=49, y la tipología 28A+11B+10C=49 también cuadra.

## Cruce: reglas del perímetro ↔ fichas del pre-registro

Ya confirmado — 27 vs 24 (ver C1-19, C4-01). El propio archivo ya trae su nota fechada de corrección (29/jul). **Confirmado también:** no existe ningún encabezado `## R3.x`; la ficha de `R3.4` (el gate de Fase 1) sigue sin existir pese a que ADR-37 la desbloqueó desde el 28/jul.

---

## 3 · Los INCORRECTO, agrupados por causa raíz

**Causa raíz A — cifra de estado nunca re-verificada tras un cambio posterior en el mismo HEAD** (la más grave; ver Finding destacado)
- C1-06/C1-07: "107 WARN" vigente cuando la corrida real da 111, en un commit cuyo propio mensaje ya sabía 111.
- C1-01: suma de la tabla de inventario (59) vs encabezado declarado (56).
- C1-02: 32 ADR vs 37 ADR, dentro del mismo archivo.
- C1-03: 18 de 43 (25, no 26, reglas "fuera").

**Causa raíz B — corrección "aplicada" nunca verificada contra la fuente (`grep` que nunca se corrió)**
- C3-01/C3-07: la nota `2026-07-29-b-correccion-perimetro.md` declara "no checa" una cita que sí checa — literalmente el mismo patrón que el propio glosario documenta en su §14 ("cuatro de cuatro resultaron falsas" para anotaciones de "parchado" sin `grep` verificado), aplicado ahora a una nota de auditoría, no a un parche de contenido.
- `curaduria-archivos.md:66` (27/jul) declaraba aplicado un parche que solo se aplicó el 28/jul (patrón ya conocido y documentado en glosario §14, Hofstede/honor/marianismo — este es el mismo defecto encontrado por cuarta vez, en un archivo que el encargo no había señalado).

**Causa raíz C — tabla/registro no actualizado cuando el documento que lo contiene sí subió de versión**
- C5-02/C5-03: tabla de artefactos y bitácora de `gobernanza` congeladas en v1.1 pese a que el documento va en v1.9.
- C1-05: título de sección en `procedencia.yaml` (14) vs cuerpo (15).
- C1-08/C1-09: "30 reports" en `integrador` y `glosario` pese a que 31 está verificado desde el 28/jul en otras partes del mismo corpus.
- C1-10/C5-08: "9 parámetros base" en `milpa-plan` pese a ADR-30.

**Causa raíz D — archivo referenciado como existente que nunca se subió**
- C3-02/C5-05: `hito2-modelo-fantasma.md`.

**Causa raíz E — instrumento de medición (el propio test) con cobertura más angosta que el fenómeno que declara medir**
- C1-20/C4-08: T07 solo reconoce vocabulario entre corchetes; el vocabulario real no-canónico es 3-5× más grande.
- T05: 5 constructos sin glosario, 2 de ellos introducidos por quien escribió el propio check (límite de alcance auto-referencial, ya señalado por README).

**Causa raíz F — convención local que invierte, en vez de solo omitir, la marca formal**
- La inversión de (b)/(c) en `Health__Body__Food...md` y `Report_26...md` es cualitativamente distinta a "usar una convención propia que no viaja" (el caso ya conocido del integrador): aquí la convención local **no es neutra**, es la definición canónica **al revés**. Alguien que lea esos dos reports con la leyenda del glosario en mente leerá (b) y (c) invertidos.

---

## 4 · OBSOLETO-POR-DISEÑO — con la nota fechada que les falta (o que ya tienen)

| Archivo | Contenido superado | ¿Ya tiene nota fechada? |
|---|---|---|
| `forense/hitoD-preregistro-v2_0.md:8,13` | "27 fichas / 27 de 27" | **Sí** — Nota 2 (L372-386, 29/jul/2026), ejemplar: cita la línea exacta, dice "ambas son falsas", da el conteo correcto (24) y explica el hueco (`§3.3`). **No requiere ninguna acción.** |
| `forense/hitoD-R1_1-veredicto-v1_0.md` (veredicto D completo) | Veredicto D superado por B tras hallar un candidato de búsqueda sesgada | **No, dentro de este archivo append-only.** La corrección vive en `README.md:40` y `TRANSFER-maestra-7.md` (fuera del alcance de `forense/`). El archivo append-only en sí **no necesita** nota — el protocolo dice que el estado vigente vive aguas abajo — pero **ningún archivo de `forense/` remite hacia esa corrección**; alguien que solo lea `forense/` sin leer `README.md`/`TRANSFER-maestra-7.md` se queda con el veredicto D como si fuera vigente |
| `forense/barrido-propagacion-forense-v1_0.md` (22 veredictos ROMPE/MATIZA como conteo cerrado) | Una revisión posterior (`TRANSFER-maestra-7.md`, fuera del censo) encontró 14 líneas de veredicto invisibles al patrón de búsqueda original, y "retira" la cifra de fuga del 41% | **No, dentro de `forense/`.** Mismo problema que el anterior: el archivo append-only está bien construido para lo que buscaba, pero nada dentro de `forense/` avisa que el 22 es un piso, no un techo |
| `forense/verificacion-red-team-vs-corpus.md` (vocabulario `[SÓLIDO]`/`[MEDIO]`) | Anterior a la consolidación del vocabulario canónico (glosario v5) | **No necesita nota** — cita fielmente el vocabulario de los reports en el momento en que se escribió (25/jul); no es una afirmación sobre el estado del programa, es una cita de fuente primaria |
| `forense/corrida-refutaciones.md:131` ("refutaciones_compiladas: 41" vs 49 reales) | Corregido en `milpa/refutations.yaml` v0.2.0 (28/jul) | **Implícita** — el YAML mismo documenta el cambio 41→49 en su changelog; `corrida-refutaciones.md` no lleva su propia nota, pero la corrección es trazable desde el archivo hermano |
| `canon/glosario-v5_6.md:44` ("Corpus a la vista: 60 archivos, 30 reports") | Superado por las verificaciones de v5.1+ (31 reports, conteo de archivos cambiado varias veces) | **No** — a diferencia de casi todo el resto del glosario (que documenta cuidadosamente cada corrección en su tabla de cambios v5.1-v5.6), esta línea de la sección "27 de julio de 2026" nunca recibió nota de actualización pese a que el propio documento ya reconoce 31 reports en otras secciones |

---

## 5 · Qué no se pudo verificar mecánicamente, y por qué

- **"18 de 43 reglas implementadas" (`estado`, `procedencia.yaml`).** No hay artefacto en el repo que sostenga el "18" — el único YAML de dominio real implementa 4 reglas, no 18. Podría ser un resto de un estado anterior de `milpa/` con más archivos `rules/*.yaml` que ya no existen, pero no hay forma de confirmarlo sin historial de commits más profundo que el disponible en este HEAD (o sin preguntar a quien lo escribió).
- **Cuáles 2 de los 5 constructos de T05 "los introdujo quien escribió el check"** (README lo afirma) — requiere el historial de autoría de `tests/check.py`, fuera del alcance documental.
- **Las citas de fuentes primarias externas** (SADER, AGROASEMEX, Ascencio-Chang 2025, ENCIG, ENVIPE, etc.) — el censo verifica que el corpus las cite consistentemente entre sí, pero no puede verificar si la fuente externa real dice lo que el corpus le atribuye (explícitamente fuera de alcance por instrucción del encargo: "no si una fuente externa dice lo que se le atribuye").
- **Conteos de palabras y "lectura completa" auto-declarados** (`lectura-cuatro-pivotes.md:4`, "4,343 / 7,565 / 7,513 / 4,681 palabras") — no verificables sin recontar los 4 reports completos carácter por carácter; se acepta como auto-reporte razonable, sin confirmar.
- **El origen real de los conteos "4" que el README atribuye a "una auditoría manual de los cuatro pivotes"** — no vive en ninguno de los 13 archivos de `forense/`; puede haber existido como ejercicio informal no documentado, o el README puede estar mal atribuyendo la fuente. **No verificable con el material disponible.**
- **Historial completo de qué commit introdujo cada discrepancia** — se reconstruyó parcialmente vía `git log`/`git show` para el hallazgo más grave (§ Finding destacado), pero no se hizo arqueología de commit para cada una de las ~50 cifras C1; sería el siguiente nivel de rigor si se decide perseguir esto.
- **Si "3 de 5 forenses sin tabla de descartes" es una lectura válida o un error** (C3-05) — depende de una distinción (¿cuenta "mención sin tabla" como "sin tabla"?) que ningún artefacto declara explícitamente. Juicio de interpretación, no hecho verificable.

---

## 6 · Qué de esto debería volverse test — y qué mueve la línea base

**Recordatorio obligatorio del encargo: ningún test nuevo entra antes de que P1 congele 18/111.** Nada de lo siguiente se implementa en esta sesión. Se ordena por si moveria o no la línea base actual (18 FAIL/111 WARN) el día que se congele.

| Candidato a test | Qué detectaría | ¿Movería 18/111 si se activara HOY? |
|---|---|---|
| **T07-ampliado**: quitar la exigencia de corchetes del regex, contar `\bHIPÓTESIS RAZONABLE\b`/`\bSÓLIDO\b`/`\bMEDIO\b`/`\bFUERTE\b`/`\bMEDIA-FUERTE\b`/`\bDÉBIL\b` sin importar notación | Las 13 ocurrencias adicionales de `HIPÓTESIS RAZONABLE` sin corchetes, y el universo completo de `FUERTE`/`MEDIA-FUERTE`/`DÉBIL` (≥184 ocurrencias no contadas hoy) | **Sí, movería el WARN de T07 de forma sustancial** (T07 pasaría de 1 FAIL con 7 etiquetas a 1 FAIL con ≥20 etiquetas — mismo FAIL, pero el detalle cambia radicalmente) |
| **T-inventario**: recalcular la suma de la tabla de `estado §1` contra su propio encabezado, en CI | C1-01 (59≠56) | Sí — nuevo FAIL |
| **T-ADR-count**: `grep -c "^\*\*ADR-[0-9]"` en `gobernanza` vs cualquier cifra de "N ADR" citada en otro archivo canónico | C1-02 (32 vs 37) | Sí — nuevo FAIL |
| **T-existencia**: todo archivo nombrado en una tabla de inventario de `estado`/`gobernanza` debe existir en disco | C3-02/C5-05 (`hito2-modelo-fantasma.md`) | Sí — nuevo FAIL |
| **T-suite-self-check**: la propia cifra "N FAIL · M WARN" citada en prosa dentro de `canon/` debe coincidir con una corrida real de `check.py` al momento del commit (hook de pre-commit, no test de contenido) | C1-06/C1-07 (107 vs 111) | Estructuralmente distinto a los demás: no es un test de contenido sobre el corpus, es un **hook de CI** que impediría el commit mismo que introdujo el defecto más grave de este censo. Si hubiera existido, el commit `9efa61f` no habría podido declarar "107 WARN" en el cuerpo del archivo mientras su propio mensaje decía "111 WARN" |
| **T-header-block**: todo archivo de `canon/` debe tener el bloque ARCHIVO/REEMPLAZA A/VERIFICAS ASÍ/NOMBRE ESTABLE | C5-01 (`integrador`) — **esto ya es T13**, hoy WARN, no FAIL | Si se sube T13 de WARN a FAIL: sí movería (18→19 FAIL, 111→110 WARN) |
| **T-grep-de-cita**: toda cita entrecomillada que un archivo atribuya a `otro_archivo.md:N` debe `grep`-earse contra ese archivo antes de aceptarse | C3-01 (el caso "pelón") — el defecto de mayor severidad cualitativa del censo, porque ocurrió dentro de una nota diseñada para cazar exactamente este patrón | Difícil de automatizar sin NLP (requiere extraer la cita exacta del texto libre), pero de implementarse detectaría exactamente el caso C3-01 |
| **T-b/c-inversion**: verificar que la leyenda local de procedencia de cada report, si declara una, no invierta (a)/(b)/(c) respecto al glosario | `Health__Body__Food...md`, `Report_26...md` | Sí — 2 nuevos FAIL si se activa |

**El candidato con mayor relación señal/costo de implementación es T-suite-self-check**: es el único que habría bloqueado, mecánicamente y sin juicio de contenido, el hallazgo más grave de este censo.

---

## 7 · Módulo de auditoría de rigor extremo (aplicado a este censo)

- **¿Qué parte de este censo podría estar confundiendo "documento desactualizado" con "documento incorrecto"?** La distinción OBSOLETO-POR-DISEÑO vs INCORRECTO es la más delicada del encargo, y este censo probablemente erró por exceso de cautela en al menos un caso: C3-05 ("3 de 5 forenses") se clasificó como AMBIGUO en vez de forzarlo a INCORRECTO, porque existe una lectura (aunque no declarada) que lo salva. Un lector menos generoso lo contaría como error simple.
- **¿Qué parte sobregeneraliza desde los dos agentes que hicieron el trabajo de extracción?** Cada hallazgo de alta severidad (el "pelón", la subcuenta de T07, el WARN 107 vs 111) fue **re-verificado directamente con herramientas propias** antes de entrar en este documento — no se aceptó ningún hallazgo de agente por reporte solo. Los hallazgos de menor severidad (algunas de las 26 instancias C3, algunas C6) se aceptaron sobre el reporte del agente sin repetir la verificación byte a byte; si alguno de esos agentes alucinó un conteo, este censo lo heredaría sin saberlo. Es un riesgo estructural del método, declarado aquí.
- **¿Qué parte está sesgada por buscar defectos y no confirmaciones?** El censo reporta ≈68-70% de instancias como CORRECTO (contra ≈20-25% INCORRECTO, el resto OBSOLETO-POR-DISEÑO o NO-VERIFICABLE) — la capa de contabilidad, aun con los defectos que este documento encuentra, **sostiene más de lo que rompe**. Vale la pena decirlo explícitamente para no dejar la impresión de que "todo está mal": C2 (campos VERIFICAS ASÍ) salió perfecto, y los cruces más citados (49 reglas, 27 perímetro, 144 números, 49 refutaciones) cuadran en 3-4 fuentes independientes cada uno.
- **¿Qué hallazgo cambiaría más si alguien re-corriera este censo con más tiempo/presupuesto?** El origen real de los conteos "4" del README (§5) y el conteo completo de C3 (solo se detalló una selección de mayor severidad, no las 26 instancias completas) son los dos puntos donde más densidad de hallazgos nuevos podría aparecer si se profundiza.
- **¿Qué parece un defecto de contabilidad pero en realidad es un límite de diseño reconocido?** El veredicto D de `hitoD-R1_1` y el 22/41% de `barrido-propagacion-forense` — ambos son archivos append-only que hicieron bien su trabajo el día que se escribieron; que una revisión posterior los superara **es exactamente cómo se diseñó que funcionara el sistema** (gobernanza §3.1). El riesgo real no es que estén "desactualizados" — es que **nada dentro de `forense/` remite hacia adelante** a la corrección, así que alguien que audite solo esa carpeta (como se pidió a este censo) los toma por vigentes.
- **¿Dónde hay evidencia débil pero intuición fuerte en este propio censo?** En la atribución de causa raíz de la Causa raíz A: es tentador leer el patrón "107 vs 111" como negligencia, pero la evidencia (`git show 9efa61f`) muestra que el autor **sabía** la cifra correcta en el momento exacto de escribir la incorrecta — eso no es negligencia, es un desacople entre el mensaje de commit (donde vive la verdad) y el cuerpo del archivo canónico (donde no llegó). Es un defecto de proceso más específico y más corregible que "alguien no revisó".
- **¿Qué conclusión de este censo sería peligrosa si alguien la usara de forma simplista?** Leer "18 FAIL · 111 WARN, con más de una docena de discrepancias nuevas" como "el programa es poco confiable". La capa de **evidencia sobre México** (reports, forenses) no fue tocada por ninguno de estos hallazgos — todos viven en la capa de **contabilidad sobre esa evidencia**, exactamente como el encargo advertía desde el principio. Confundir ambas capas sería repetir, sobre el propio programa, el error de estructura-por-cultura que el programa entero existe para evitar en México.

---

## 8 · Finding destacado — el de mayor severidad del censo

**`canon/estado-programa-v1_9.md` declara "18 FAIL · 107 WARN" como estado vigente de la suite. La corrida real contra el HEAD actual (`9efa61f`) da 18 FAIL · 111 WARN.**

No es deriva por un cambio posterior: `git show 9efa61f` muestra que **todo el archivo** `estado-programa-v1_9.md` se escribió en ese mismo commit (diff de archivo nuevo, íntegro), y el **mensaje de ese mismo commit** dice textualmente:

> *"No se cablea a la suite para no mover su linea base (18 FAIL / 111 WARN)... Suite antes y despues: 18 FAIL, 111 WARN."*

Es decir: quien escribió la versión vigente de "ÚNICA FUENTE DE ESTADO" **conocía la cifra correcta en el momento exacto de redactar la incorrecta**, porque la puso en el mensaje del commit y no en el archivo. Causa mecánica confirmada: `TRANSFER-maestra-7.md:49` y `TRANSFER-maestra-8.md:26` (fusionados a este HEAD por commits anteriores) citan literalmente `-v3.2.md`/`-v3_2.md` como ejemplo de la convención de nombres, y T03 los cuenta como referencias colgantes reales — 4 WARN que el "107" nunca contempló porque esos dos archivos no existían cuando se corrió la verificación que produjo esa cifra.

---

## 9 · Cierre

**HEAD:** `9efa61f79f9be4d7d2dcf361062fa54e3e944bce` · rama `claude/modelado-mexicano-audit-rugaa3`.

**Suite:** `python3 tests/check.py` → **18 FAIL · 111 WARN** (reproducido dos veces en esta sesión, idéntico). `python3 tests/validador_registro_ids.py` → **OK**, 49 reglas, 27 perímetro, 49 IDs.

**Lo que este censo NO pudo verificar** (repetido de §5, para que quede junto al cierre como pide el encargo):
1. El sustento real de "18 de 43 reglas implementadas" — no reconstruible desde ningún archivo del repo.
2. Cuáles 2 de los 5 constructos huérfanos de T05 introdujo quien escribió el propio check — requiere historial de autoría fuera de alcance.
3. Si las fuentes primarias externas citadas (SADER, ENCIG, Ascencio-Chang, etc.) dicen lo que el corpus les atribuye — fuera de alcance por instrucción explícita del encargo.
4. El origen documental real de los conteos manuales "4" que `README.md` atribuye a una auditoría del 28/jul — no vive en ninguno de los 13 archivos de `forense/` revisados.
5. Si la lectura "3 de 5 forenses sin tabla de descartes" es válida o un error de conteo — depende de una distinción implícita, no declarada en ningún artefacto.

**No se corrigió nada en esta sesión.** Ninguna de las líneas citadas arriba fue editada. Este documento es el registro de qué estado real hay; las correcciones —incluida la más urgente, el "107 WARN" de `estado-programa-v1_9.md`— se aprueban después y por separado, con diff explícito.

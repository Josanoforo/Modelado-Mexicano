# FICHA `ID-G3` · diseño intra-persona para `G3·horizonte_temporal` (RUTA-I)
### `ficha-id-g3` · **v1.0** · 5 de agosto de 2026 · Encargo S2-IDG3, promovida de borrador

> | | |
> |---|---|
> | **ARCHIVO** | `ficha-id-g3-v1_0.md` |
> | **REEMPLAZA A** | `forense/notas/2026-08-04-e-mxfls-ficha-borrador.md` — el propio borrador, `git mv`ido a este archivo (no hay dos copias; la nota de proceso original, `forense/notas/2026-08-04-e-mxfls-nota-proceso.md`, queda intacta y sin tocar) |
> | **VERIFICAS ASÍ** | Condiciones (1)/(3) de sello: `forense/notas/2026-08-05-s-idg3-verificacion-no-sello.md` §2(1),(3) — citas verbatim contra `canon/gobernanza-v1_15.md:623` y contra el Paso 2(8)/fila `E` de esta misma ficha, no re-verificadas aquí. Condición (2): 9 invocaciones `python3 tests/manifiesto.py --verifica --id <id>`, las 9 `COINCIDE`, salida cruda en `forense/notas/2026-08-05-s2-idg3-sello.md` §2. Condición (4): `python3 tests/idx_g3.py` (barrido de 6 escenarios ICC×pares-de-olas, las 6 `<1.25`), salida completa en `forense/notas/2026-08-05-s2-idg3-sello.md` §3 y reproducible corriendo el script. |
> | **NOMBRE ESTABLE** | **`ficha-id-g3`** — cítalo así, no por nombre de archivo |

**Estado: PROPUESTA DE SELLO COMPLETA — pendiente decisión de mesa (PLAN-MAESTRO v1.5 §1: "sellarla es decisión de mesa").** Este documento es el entregable que ADR-57(c) pidió y no concedió — el diseño de la promoción de `CAL-G3` (descriptivo, Fase C ya corrida) a un intento de identificación bajo la llave (i) ("panel con el desenlace en el instrumento, mismos sujetos entre olas"). Las cuatro condiciones de sello (`forense/notas/2026-08-05-s-idg3-verificacion-no-sello.md` §8, retomadas por el Encargo S2-IDG3) verifican limpias — ver tabla `VERIFICAS ASÍ` arriba y `forense/notas/2026-08-05-s2-idg3-sello.md` para la evidencia completa. **Este acto no corre la estimación, no abre microdato, no promueve nada** en `milpa/procedencia.yaml` ni en ningún canon — correr la estimación en la misma sesión que sella contaminaría el pre-registro contra MxFLS (ADR-46).

Redactado originalmente en worktree `~/mm-e-mxfls-g3-horizonte`, rama `sesion/e-mxfls-g3-horizonte-ficha`, contra `origin/main` en `bd2c975`. Verificado sin sellar por S-IDG3 en `~/Modelado-Mexicano` (nube), rama `claude/g3-horizonte-temporal-id-s88z1w`, contra `origin/main` en `06d04be`. Esta promoción a artefacto propio se redactó en worktree `~/mm-s2-idg3-sello`, rama `sesion/s2-idg3-sello`, contra `origin/main` en `08b8b6c` (PR #121, el mismo que fusionó la nota de S-IDG3).

---

## PASO 0 · Inventario de contaminación

**La trampa, nombrada.** Quien diseña la promoción de `CAL-G3` ya ha visto, por diseño de este mismo acto (Paso 0 exige leerlo), el resultado de Fase C. "Un protocolo escrito por quien ya vio el resultado no vale" (Encargo Q, `forense/hallazgos.md:98-99`). La disciplina no es evitar leer Fase C — es leerla exhaustivamente, declarar con precisión qué cantidades quedan contaminadas, y diseñar el Paso 2 exclusivamente sobre lo que quede fuera de esa lista.

**Qué NO cuenta como contaminación (distinción necesaria antes de la lista).** Consultar el manual de codificación / cuestionario (estructura, no resultado) es exactamente lo que el ARRANQUE de este encargo asigna ("consultará FD/cuestionarios de las olas") y lo que ADR-46 permite si se declara ("exploración de estructura... contamina parcialmente, declarar hasta dónde" — nivel distinto de "exploración de resultado"). Una frecuencia marginal de un ítem del codebook (p. ej. "1,136 de 9,045 hogares marcan Sí en `ah03h`") no es una cantidad sobre la relación `G3→horizonte_temporal`: es un hecho sobre el instrumento, del mismo tipo que `CAL-G3` (Nota 7, punto 7) ya usó libremente para fijar sus propios umbrales antes de abrir microdato. La superficie contaminada de abajo es específicamente **resultados de Fase C sobre la relación bajo prueba** — no "todo lo que este acto leyó".

### 0.1 · Superficie contaminada — resultados de Fase C, con archivo:línea

**A. `forense/hitoD-preregistro-v2_0.md`, Nota 7 (líneas 478–522) + Adenda 1 (525–550) — el PRE-REGISTRO de `CAL-G3`, sellado en `c9e67bd`, 29/jul/2026.**
No es un resultado (antecede a la apertura de microdato), pero fija la superficie que Fase C iba a tocar y por tanto la superficie que este acto debe evitar duplicar:
- Objeto: `G3 → horizonte_temporal`, `-0.60`, `ASIGNADO` (línea 484, cita `procedencia.yaml:272`; verificado también contra `procedencia.yaml:627`).
- Desenlace primario: composición del ahorro del hogar vía `CRH01` (`crh01_1a`–`crh01_1k`), recodificada a 4 estados por Adenda 1(b)-(c): solo informal · mixto · solo formal · ninguno (líneas 488, 525–544).
- Desenlace secundarios **nombrados y declarados NO sustituibles/NO promovibles** (línea 489): (i) `ah03h`, `ah04h_1/2`, módulo `AH` (activos financieros/AFORE); (ii) `se05_1j`, módulo `SE` (ahorro como mecanismo ante choques); (iii) módulo `CR` de Libro IIIB (crédito formal/informal). **Ninguno de los tres fue estimado** — ver parte C más abajo, verificado contra el propio código.
- Identificación: efectos fijos de hogar, exposición = formalidad del jefe vía `TB33` (`tb33p_a ∨ tb33p_b ∨ tb33p_d`), con sensibilidad "cualquier miembro formal" (líneas 491–493).
- Confundidor 5 (oferta local), exclusión de diáspora, criterio en razón (RR, no pp), ponderadores por familia, ejes de segmentación, límite de época 2002–2012 (líneas 495–513).

**B. `forense/hitoD-preregistro-v2_0.md`, Nota 8 (554–628), Fase B, 30/jul/2026.** Solo lectura de codebook/cuestionario/ponderadores. **No estimó nada.** Encuentra dos condiciones de parada (estructura multi-selección de `CRH01`; premisa de criterio asimétrico) — estructura, no resultado sobre `G3`.

**C. `forense/hitoD-preregistro-v2_0.md`, Nota 9 (632–647), decisiones de mesa, 30/jul/2026.** D-10: restringe a olas 2–3. D-09: el entregable es descriptivo puro, sin veredicto CAL-A/B/C/D/X, no entra al conteo del Hito D. Cita el cálculo de poder de `tests/calx_g3.py` (parte E abajo).

**D. `forense/hitoD-preregistro-v2_0.md`, Nota 10 (649–686), Fase C ejecutada, 30/jul/2026 — EL RESULTADO PRINCIPAL, exhaustivo:**
- Exposición ejecutada: `FORMAL = tb33p_a ∨ tb33p_b ∨ tb33p_d` (línea 655) — **incluye `tb33p_d` (IMSS)**.
- Desenlace ejecutado: `P(mixto o solo formal)` sobre `CRH01` (línea 655).
- Muestra: `jefes_ola2=8294`, `jefes_ola3=9068`, filtrados por ronda C `=192`, en ambas olas `=6817`, elegibles basal `=4194`, muestra analítica `=2404` (=29.0% de jefes ola 2) (líneas 657–665; idéntico en `forense/notas/2026-07-30-calg3-fasec-salida.txt:20–32`).
- Atrición 42.7% (1790/4194), descomposición 65.5%/32.5%/resto (línea 667).
- Composición basal perdidos vs. retenidos completa: sexo, formalidad basal, acceso formal basal, edad, educación (línea 669; `salida.txt:45–63`).
- Resultado: "algún acceso formal" 9.11% (2005-06) → 7.49% (2009-12) (línea 671; `salida.txt:76-77`). Matriz de transición de 4 estados completa (`salida.txt:66-88`). Transición de formalidad del jefe, 9 celdas (`salida.txt:79-88`).
- **Las 60 estimaciones** (3 exposiciones × 2 desenlaces × 5 ponderadores × 2 estimadores): todas cruzan el nulo; rango de signo `+0.60pp` a `-4.20pp` según especificación; `n.inf` (hogares informativos) entre 7 y 81 según exposición/ponderador, **7–14 bajo la exposición literal** (líneas 671–675; `salida.txt:100-221`, tabla completa).
- Confundidor 5 no aplicado (módulo `OC` de ola 3 fuera del manual de codificación) — degradación declarada: ninguna cifra se lee como preferencia temporal (línea 677).
- Enlace `pid_link`, filtrado de ronda C, traslape de hogares 88.2% (línea 657).
- Insumos ampliados declarados: roster (`ls05_1`, `ls04`, `ls02_2`, `ls14`), portada Libro IIIA (`ent`), ponderadores longitudinales (línea 681).
- Incidencia de "Otro" (`crh01_1k`): 45/8134 (0.55%) ola 2, 30/9092 (0.33%) ola 3 (línea 679; `salida.txt:39-42`).

**E. `tests/calx_g3.py` + `forense/notas/2026-07-30-calx-g3-salida.txt`, 30/jul/2026 — chequeo de potencia, citado explícitamente por Nota 9 (línea 636) como su insumo.** Solo codebook, ningún `.dta`. Reporta, para el desenlace `CRH01`-`algún acceso formal`: tasas base por ola (9.94%/7.95%/7.23%, `salida:11,17,23`); veredicto de alcanzabilidad CAL-A/B alcanzables, CAL-C/9b **NO alcanzables por construcción** en ninguna ola sola (`salida:75-78`); extensión de apilar dos transiciones — mejor caso de toda la matriz (ICC=0, tres olas) `IC95%sup=1.281`, **sigue sin alcanzar el `<1.25`** de CAL-C (`salida:129-160`). Este es el hallazgo que cierra la puerta a "solo cambiar de par de olas" como ruta limpia: **ningún wave-pairing del mismo par exposición/desenlace alcanza potencia**, con cualquier supuesto de ICC.

**F. `forense/metodologia-identificacion-vs-ajuste-v0_1.md` (31/jul/2026) — propuesta sin sellar, NO es canon** (`§0` del propio archivo lo declara). No añade cantidades nuevas: restata los resultados de D-E ("7 a 14 hogares informativos, las 60 estimaciones cruzando el nulo", línea 59) como argumento para reencuadrar identificación→ajuste. Se lista aquí por exhaustividad, no porque aporte superficie nueva.

**G. `milpa/procedencia.yaml:787` y `forense/censo-estimabilidad-coeficientes-v1_0.md` (04/ago/2026) — metadato de estado, no resultado empírico.** Clasifican `G3·horizonte_temporal` como `RUTA-I`, prioridad `ALTA`, "llave sellada ENNViH/MxFLS vía CAL-G3, Fase C descriptiva ya corrida". No es una cantidad sobre la relación — es el pointer que este mismo encargo ejecuta.

### 0.2 · Corrección encontrada al verificar (no heredar, por instrucción explícita del encargo)

`forense/censo-estimabilidad-coeficientes-v1_0.md:36` afirma: *"`CAL-G3` ... sí cita su propio ponderador/estrato/UPM por ola"*. **Verificado contra Notas 7–10 completas: es falso para estrato/UPM.** `CAL-G3` cita ponderadores (`ehh02w_*`; `fac_2l`/`fac_3al` por ola, Nota 7 punto 7 y Nota 10 punto j) pero **no cita ni estrato ni UPM en ningún punto de su ficha ni en su salida** — ninguna de las 60 estimaciones usa diseño muestral complejo; los EE reportados son HC1/sandwich (heterocedasticidad-robustos), no ajustados por conglomeración. Esto coincide con `data/diseno-muestral.yaml:390-410`, que registra ENNViH como `PENDIENTE` con estrato/UPM "no confirmado como nombre de columna". Se reporta como hallazgo de este acto en la nota de proceso; no se edita `censo-estimabilidad-coeficientes-v1_0.md` (append-only, fuera del perímetro de este acto).

### 0.3 · Consecuencia para el Paso 1

Quedan **fuera** de la superficie contaminada, y por tanto disponibles: (a) cualquier desenlace que no sea `CRH01`/composición del ahorro; en particular los tres nombrados-no-corridos en A — `AH`, `SE`, `CR`; (b) la exposición `TB33` en sí (es estructura del instrumento, no un resultado — y de todos modos su reutilización no revela nada sobre `G3`, ver más abajo); (c) cualquier par de olas — con la salvedad de que E ya cerró la puerta a "solo cambiar de olas" como estrategia de potencia, así que un diseño limpio necesita además un desenlace distinto, no solo otra ventana temporal.

---

## PASO 1 · La cantidad limpia, elegida y justificada

**Tres candidatos nombrados por la propia Nota 7 (§0.1-A) y nunca corridos.** Se examinan los tres, con el mismo estándar de rigor que Fase C se exigió a sí misma — nombrar el confundidor antes de ver dato, no después:

**`CR` (crédito formal/informal, Libro IIIB) — DESCARTADO.** El crédito formal (tarjeta bancaria, `cr01b` etc.) exige, como criterio de suscripción del prestador, comprobante de ingreso formal — la misma variable que define la exposición. Es un confundidor mecánico de primer orden, más severo que el de oferta local que `CAL-G3` ya nombró para `CRH`: aquí la vía de "acceso al producto" y la vía de "exposición" comparten la misma causa administrativa (formalidad del ingreso como requisito de originación). No se lleva al Paso 2.

**`SE` (`se05_1j`, ahorro como mecanismo ante un choque) — considerado, no elegido como primario.** Verificado contra el manual de codificación de ola 3 (`data/raw/ennvih/doc/ehh09cb_b2.pdf`, sección `ii_se`): `se05_1j` es un ítem de selección múltiple ("CIRCULE TODAS LAS QUE APLIQUEN"-estilo, misma familia que `CRH01` antes de Adenda 1) dentro de una batería de doce mecanismos de afrontamiento, condicional a que el hogar haya reportado ≥1 evento adverso en `se01a`–`se01f` (muertes, enfermedad, fracaso de negocio/cosecha, y tres categorías más no leídas en detalle por este acto). Positivos: `se05_1j=156` en ola 3 (ehh09cb_b2.pdf, sección `ii_se`) — **sin confundidor mecánico con la exposición** (no hay vínculo administrativo entre tener contrato formal y usar ahorro ante un choque). Negativos, declarados antes de elegir: (i) universo condicional a experimentar un choque —reduce validez externa—; (ii) ajuste teórico más débil a `horizonte_temporal` específicamente — "usar ahorro ante un choque" es más próximo a comportamiento de amortiguador/precaución (aversión al riesgo, el OTRO coeficiente de `G3`) que a preferencia temporal; (iii) tasa base más baja (156 sobre un denominador que este acto no terminó de acotar con precisión — la unión de `se01a`-`f` no se leyó completa) — probablemente **peor potencia** que el propio `CRH` que ya falló CAL-X. Se declara aquí, no se descarta del todo: si mesa prefiere `SE` sobre `AH` por su limpieza mecánica, este acto deja el candidato nombrado y verificado para que otra ficha lo desarrolle.

**`AH` (`ah03h`, tenencia de Activos Financieros/AFORE) — ELEGIDO, con una modificación necesaria de la exposición.** Verificado contra `data/raw/ennvih/doc/ehh0{5,9}cb_b2.pdf`, sección `ii_ah`: ítem binario único (Sí/No, sin la ambigüedad multi-selección de `CRH01`), pregunta agregada del hogar dentro de un inventario general de activos (junto con casa, bicicleta, vehículo, electrodomésticos, maquinaria, ganado) — no comparte pregunta ni sección con `CRH01`. Tasas base, **nunca abiertas por `calg3_fasec.py`** (verificado: `grep -c "ah03h\|ah04h" tests/calg3_fasec.py` = 0 coincidencias) ni citadas en ningún punto de Notas 7–10 más allá del nombre en la lista de no-sustituibles:

| ola | Sí (`ah03h`) | No | Total | % Sí |
|---|---|---|---|---|
| 1 · 2002 | 1,332 | 6,708 | 8,040 | 16.6% |
| 2 · 2005-06 | 1,117 | 7,015 | 8,132 | 13.7% |
| 3 · 2009-12 | 1,136 | 7,909 | 9,045 | 12.6% |

*(fuente: `ehh02cb_b2.pdf:1104-1106`, `ehh05cb_b2.pdf:1310-1312`, `ehh09cb_b2.pdf:1430-1432`, extraídas con `pdftotext -layout`, verificables una por una contra el PDF — misma disciplina que `tests/calx_g3.py` declara en su cabecera.)*

**El confundidor que esto obliga a nombrar, y que ninguna ficha previa de este corpus enfrentó — más severo que el de oferta local.** El sistema AFORE mexicano abre cuenta individual **obligatoria** a todo trabajador afiliado al IMSS (reforma SAR 1997), con o sin ninguna decisión de ahorro de por medio. `tb33p_d` —la afiliación IMSS— es uno de los tres componentes de la definición `FORMAL` que `CAL-G3` usó (`tb33p_a ∨ tb33p_b ∨ tb33p_d`, Nota 10 línea 655). Un jefe que transita a formal exactamente por la vía IMSS **abre mecánicamente una cuenta AFORE**, sin que medie ninguna preferencia temporal. A diferencia del confundidor de oferta local de `CRH` —que **atenúa** el efecto hacia el nulo (sesgo conservador, declarado en Nota 7 punto 5)—, este confundidor **empuja hacia el signo que `G3` predice**, con dirección de sesgo contraria: no hay lectura conservadora posible si se usa la definición literal de `CAL-G3`.

**Tratamiento, declarado aquí, antes de ver ningún dato:**
1. **Exposición modificada para esta ficha**, distinta de la de `CAL-G3` por razón declarada, no por conveniencia: `FORMAL_CONTRATO = tb33p_a ∨ tb33p_b` (contrato escrito, indefinido u obra determinada) — **excluye `tb33p_d` explícitamente**. Verificado contra `ehh09cb_b3a.pdf:4283-4299`: `tb33p_a`="Contrato escrito por tiempo indefinido" (n=2582), `tb33p_b`="Contrato escrito por... obra determinada" (n=658), `tb33p_c`="Contrato verbal... no tiene contrato" (n=1470, ancla de INFORMAL), `tb33p_d`="Seguro social (IMSS)" (n=2687, EXCLUIDO de esta definición). Esto rompe el canal administrativo directo — un jefe puede conseguir contrato escrito sin que eso, por sí solo, abra ninguna cuenta.
2. **Riesgo residual, declarado y no resuelto por (1):** un mismo empleo formal con frecuencia bunde contrato escrito **y** afiliación IMSS a la vez (correlación de instrumento, no error de diseño) — (1) reduce el canal mecánico, no lo elimina. Por eso la interpretación de la fila `ID-A` de la escala (Paso 2) queda degradada de forma **asimétrica**, declarada aquí antes de medir: un resultado que corrobora el signo de `G3` **no** se lee como evidencia de `horizonte_temporal` (el canal administrativo residual ya predeciría ese signo sin ninguna preferencia); un resultado que **no** corrobora, o que sale de signo contrario, sí es informativo — va contra un sesgo que empuja hacia la confirmación, no a favor de uno que empuja hacia el nulo.
3. Con esta definición, `ah03h`/`ah04h` **nunca fueron abiertos, contados por esta transición ni estimados** por ningún acto anterior — ni con la exposición literal de `CAL-G3` ni con la modificada de este acto. Queda fuera de la superficie del Paso 0 bajo cualquier lectura.

---

## PASO 2 · FICHA `ID-G3` · horizonte_temporal vía tenencia de activos financieros del hogar (AFORE) — Bloque B-bis v2.4

> **Objeto:** `G3 → horizonte_temporal`, hoy `-0.60`, clase `ASIGNADO` (`milpa/procedencia.yaml:627`). **Llave de identificación bajo prueba:** (i) de `ADR-57(c)` (`canon/gobernanza-v1_15.md:623`) — panel con el desenlace en el instrumento, mismos sujetos entre olas. **Fuente:** ENNViH/MxFLS, panel de tres olas, dominio público (misma fuente y misma disciplina de cita que `CAL-G3`, Nota 7 línea 484). **Relación con `CAL-G3`:** ficha hermana, NO edición — `CAL-G3` (Notas 7-10) queda intacta y sellada; ninguna cifra de aquella se reutiliza como resultado, solo se reutiliza la exposición de `TB33` como estructura de instrumento (modificada, ver Paso 1) y la infraestructura de enlace entre olas (`pid_link`).

### (1) Escala — declaración obligatoria (misma que `CAL-G3` punto 2, hereda la razón, no la cifra)

Se declara la opción **(b): no existe mapeo defendible** a la escala del `-0.60` — mismo argumento que `CAL-G3`: el `-0.60` no tiene unidades declaradas, `ASIGNADO` solo sostiene dirección, y una regla de conversión inventada sería una segunda asignación disfrazada de medición. El entregable es una elasticidad autónoma en razón (RR/OR), que informa sobre **signo** dentro-de-unidad y **orden relativo**, no sobre magnitud del `-0.60`.

### (2) Universo y olas

Olas **2 (2005-06) y 3 (2009-12)** únicamente — **hereda la restricción de D-10** (`hitoD-preregistro-v2_0.md:638`), y por razón que aplica igual a esta ficha: el módulo `TB` de la ola 1 no es comparable (el instrumento fabrica transiciones), una limitación del lado de la EXPOSICIÓN que no depende de qué desenlace se le empareje. No es evitar contaminación — es una restricción estructural heredada porque sigue siendo válida, declarada así y no como blindaje.

Universo analítico: jefes de hogar en ambas olas, con batería `TB33` aplicable (mismo filtro estructural que `CAL-G3` — excluye campesino de su parcela y trabajador familiar sin retribución, a quienes el instrumento no aplica `TB33` bajo ninguna definición de formalidad) y con `ah03h` no faltante en ambas olas. **El tamaño exacto de esta muestra no se conoce hasta ejecutar** — será menor que los 2,404 de `CAL-G3`, porque `FORMAL_CONTRATO` (a∨b, sin d) es un subconjunto más pequeño que `FORMAL` literal (a∨b∨d: 2582+658 antes de traslape, contra un universo donde `tb33p_d` solo ya cubre 2,687) — se reporta el tamaño real al ejecutar, no se teclea de memoria (v2.4, regla de procedencia).

### (3) Exposición — MODIFICADA de `CAL-G3`, por la razón del Paso 1, no por preferencia

`FORMAL_CONTRATO` = `tb33p_a ∨ tb33p_b` (contrato escrito, indefinido u obra determinada). `INFORMAL` = `tb33p_c` (contrato verbal / sin contrato). **`tb33p_d` (IMSS) queda excluido de la definición de exposición en esta ficha — declarado y justificado en el Paso 1, no se renegocia después de ver dato.** Jefes sin trabajo o sin `TB33` aplicable: estado aparte, excluidos del contraste principal (mismo tratamiento que `CAL-G3`).

**Sensibilidad pre-registrada, única:** exposición alternativa "cualquier miembro del hogar tiene `FORMAL_CONTRATO`" frente a "jefe tiene `FORMAL_CONTRATO`" — misma lógica que la sensibilidad de `CAL-G3` (Nota 7 punto 4), adaptada a la exposición modificada. Se reportan ambas; no se elige una después de ver resultados.

**No se ofrece una sensibilidad que reincorpore `tb33p_d`.** Hacerlo reabriría exactamente el confundidor mecánico que el Paso 1 declaró — sería la clase de "ajuste después de ver que no alcanza" que el Bloque C prohíbe.

### (4) Desenlace

`ah03h` = 1 si el hogar posee o es dueño de Activos Financieros/AFORE, 0 si no. **Ítem binario único — no requiere la reconstrucción de estados que `CRH01` exigió (Adenda 1)**, verificado contra cuestionario (no solo codebook, misma disciplina que enseñó Adenda 1 (g)): `ehh09q_b2.pdf` sección de activos del hogar, ítem "H. Dinero ahorrado, activos financieros, valores, cuentas de cheques, AFORES, monedas y otros" — Sí/No/NS, sin estructura de selección múltiple. El total de `ah03h` reconcilia sin residuo en las tres olas (Sí+No = Total exacto), consistente con NS≈0 o no capturado como categoría separada en la variable liberada.

Cambio dentro-de-unidad del desenlace cuando cambia el estado de exposición entre olas 2 y 3 — efectos fijos de hogar, mismo diseño de `CAL-G3`.

**No se declara sensibilidad de desenlace** — a diferencia de `CRH01`, `ah03h` no tiene categoría ambigua que reasignar (no hay equivalente al problema Caja de Ahorro/Cooperativa de Adenda 1).

### (5) Identificación

Efectos fijos de hogar, exposición = estado de `FORMAL_CONTRATO` del **jefe de hogar** (mismo individuo seguido entre olas vía `pid_link`, la condición "mismos sujetos" se cumple igual que en `CAL-G3`). Estimadores: **probabilidad lineal con EF de hogar** (MCO en primeras diferencias, EE robusto HC1) y **logit condicional de Chamberlain** — idénticos a `CAL-G3`, por continuidad metodológica ya validada (los estimadores de `tests/calg3_fasec.py` se autoprueban contra forma cerrada; se reutiliza el método, no ningún resultado).

- **SUPUESTO DECLARADO, mismo que `CAL-G3`:** que la tenencia de AFORE del hogar responde a la formalidad contractual del JEFE y no del conjunto de miembros. Sesgo: atenúa (mismo argumento, dirección CONTRA encontrar el efecto).
- **Enlace entre olas:** mismo esquema `pid_link` de `Nota 10` (c) — filtrado de folios de ronda C de ola 3 (no enlazables), verificado ahí (192 jefes), reutilizado como estructura de instrumento, no como resultado.

### (6) Confundidores nombrados, con tratamiento

1. **Circularidad mecánica AFORE↔IMSS** (nombrado en Paso 1). Tratamiento: exclusión de `tb33p_d` de la exposición (mitiga, no elimina) + interpretación asimétrica de la escala (punto 8 abajo): `ID-A` no corrobora `horizonte_temporal` por sí solo; `ID-C` sí es informativo.
2. **Oferta local** (heredado de `CAL-G3` punto 5, versión más débil aquí): AFORE es de administración federal —no depende de sucursal bancaria local, a diferencia de `CRH`— pero el USO/APORTACIÓN voluntaria sí puede beneficiarse de acceso a agente o sucursal. Mismo procedimiento de descarte que `CAL-G3`: si el cuestionario de localidad (`eloc09q_bcc1.pdf`) no cubre presencia de administradoras/agentes AFORE, el confundidor queda sin descartar y **ninguna cifra se lee como preferencia temporal** — se lee como conducta bajo restricción de oferta, igual que `CAL-G3`. No verificado en este acto (fuera del perímetro declarado, punto 10).
3. **Selección migratoria** (heredado, Nota 7 punto 6): se excluyen observaciones-persona levantadas en EE.UU., mismo criterio y misma limitación de que el marcador es cota inferior (Nota 10 (i)).
4. **Atrición**: se espera del mismo orden que `CAL-G3` (42.7%, Nota 10 (e)) porque el filtro dominante —aplicabilidad de `TB33`— es el mismo lado de exposición; se reporta la atrición efectiva real al ejecutar, no se asume la cifra de `CAL-G3`.

### (7) Criterio en razón, ponderador/estrato/UPM — verificado contra FD, no heredado

**Criterio en RR, no en pp** — misma lección de `R3.2`/`CAL-G3` punto 7: con tasas base 12.6%-16.6%, un criterio en puntos porcentuales sería vulnerable al mismo modo de falla. Los umbrales (abajo, punto 8) son idénticos en forma a los de `CAL-G3` (RR≥1.5 / RR≤1 con IC95%sup<1.25 / banda [0.80,1.25]) — reutilizados por continuidad metodológica declarada, no derivados de nuevo, porque la forma del criterio no depende del desenlace.

**Ponderador** — verificado, no heredado sin más: `fac_2l` (Libro II, longitudinal, hogar) y `fac_3al` (Libro IIIA, longitudinal, individual), las mismas familias que `CAL-G3` reporta haber usado en su salida (`forense/notas/2026-07-30-calg3-fasec-salida.txt:110-113`) — se reutiliza el NOMBRE de columna, ya validado por la ejecución de `CAL-G3` (no es una cifra de resultado, es una etiqueta de instrumento). Se corre sin ponderar y con cada ponderador longitudinal disponible, mismo criterio de reportar todos.

**Estrato** — **verificado independientemente en este acto, CORRIGE una cita existente** (ver Paso 0.2): columna `estrato` confirmada en el Libro C (Control) de las tres olas — `ehh02cb_bc.pdf:105` (N=8,441), `ehh05cb_bc.pdf:116` (N=8,437, media 2.51), `ehh09cb_bc.pdf:124` (N=10,104, media 2.55). Campo de portada del cuestionario ("5. Estrato:", `ehh09q_b2.pdf:18`), llenado por el encuestador. Se declara disponible para estratificar el error estándar si se ejecuta esta ficha con diseño muestral complejo.

**UPM** — **no confirmado como nombre de columna**, verificado en este acto contra el Libro C completo de ola 3 (variables `folio`/`ls`/`rel`/`reh`/`ent`/`mpio`/`loc`/`edad`/`estrato` — sin `upm`/`conglomerado`) y contra `data/raw/ennvih/calculo-de-factores-de-expansion.pdf` y `guia_de_usuario_ennvih-3.pdf` (mismo hallazgo que `data/diseno-muestral.yaml:397-405` ya registra: el método está documentado —diseño bietápico región→estrato→UPM→USM→vivienda— pero ningún documento leído nombra la columna real). El campo "A.G.E.B." existe en la portada del cuestionario pero no aparece como variable liberada en el Libro C. **Límite declarado, no resuelto:** los EE de esta ficha, igual que los de `CAL-G3`, no ajustan por conglomeración de primera etapa — son HC1/sandwich, potencialmente anti-conservadores si el efecto de diseño por UPM es alto (mismo punto que `tests/calx_g3.py` cuantificó para el desenlace `CRH`: DEFF hasta 1.80 con ICC=0.8). No se finge una corrección que el instrumento no documenta.

### (8) Rejilla de celdas — escala propia de esta ficha, con fila `E` (ADR-58) y regla de precedencia (ADR-58(b)/59(a), declarada al sellar)

- **`ID-A`** · RR≥1.5 dentro-de-unidad (informal→formal sube tenencia de AFORE), IC95% excluye 1. **Declarado antes de ver dato, por el confundidor (6.1): un `ID-A` NO corrobora `horizonte_temporal`.** El canal administrativo residual (contrato formal correlacionado con afiliación IMSS concurrente) predeciría este mismo signo sin ninguna preferencia temporal de por medio. Se archiva como "consistente con, no distingue entre, canal mecánico y preferencia" — nunca como confirmación de `G3`.
- **`ID-B`** · Señal en dirección predicha sin cruzar magnitud, o cruza pero sin descartar el confundidor de oferta (6.2). Sostenida, no cerrada. Misma advertencia de `ID-A` si aplica.
- **`ID-C`** · Signo contrario o nulo estricto dentro-de-unidad (RR≤1, IC95%sup<1.25), **en la submuestra con oferta local verificada**. **Es la fila informativa por excelencia de esta ficha**: rompe contra un sesgo que empuja hacia la confirmación, no a favor de uno que empuja hacia el nulo — evidencia más fuerte que un `CAL-C` ordinario.
- **`ID-D`** · Inejecutable: el panel no arma la muestra analítica, o el cuestionario de localidad no cubre el confundidor de oferta y mesa decide que sin eso no informa.
- **`ID-X`** · GATE INALCANZABLE POR CONSTRUCCIÓN — chequeo previo, mismo molde que `CAL-X`. **Pre-calculado en este acto, mostrando el trabajo** (mismo método que `tests/calx_g3.py`, aplicado a `ah03h`): techo duro de hogares discordantes en el desenlace, olas 2-3 = Sí(ola2)+Sí(ola3) = 1,117+1,136 = **2,253** (cota flojísima, mismas advertencias que `calx_g3.py` declara: traslape cero, sin exigir cambio de exposición, antes de atrición). Con `p` agrupada = 2,253/17,177 = 13.12%: `SE(log RR) = sqrt(2·(1-p)/((techo/2)·p)) = 0.1084` → `IC95%sup = exp(1.96·0.1084) = 1.237`. **Esto SÍ cruza el umbral `<1.25` de `ID-C`** — a diferencia del desenlace `CRH` (que no lo cruzaba ni en su mejor escenario, 1.281 apilando tres olas) — pero por un margen mínimo (1.237 contra 1.25), en el escenario más favorable posible, antes de aplicar exactamente los mismos filtros de atrición/enlace/aplicabilidad de `TB33` que en `CAL-G3` redujeron el techo nominal de 1,457 a un número real de 7-14 informativos (dos órdenes de magnitud). **Expectativa declarada antes de medir:** es plausible, y no debe leerse como fracaso del diseño, que el número real de hogares informativos quede de nuevo por debajo de lo necesario para decidir `ID-A`/`ID-C` con IC95% que despeje el umbral — la ficha está construida para que ese desenlace tenga dónde anotarse (fila `E`, abajo), no para forzar una fila.
- **`ID-9b` (nulo estricto con poder)** · IC95% enteramente dentro de `[0.80, 1.25]` — mismo criterio que `CAL-G3` punto 9b, misma submuestra con oferta verificada.

**Fila `E`, prospectiva (ADR-58(a), plantilla de `hitoD-preregistro` Nota 26).** *"El falsador corrió limpio y no se satisfizo — la regla sobrevive a esta prueba."* Declarado aquí, antes de ver dato, qué significa ese desenlace para ESTA ficha específicamente: dado que `ID-A` ya está degradado por el confundidor (6.1) y no puede leerse como corroboración plena, una fila `E` en esta ficha no acota tanto como acotaría en una ficha sin ese confundidor — significa "el diseño no tuvo potencia para alcanzar siquiera `ID-C` (la fila informativa), y por tanto esta ruta tampoco puede decir, con este panel y esta ventana, si `horizonte_temporal` opera o no". No se lee como "`G3` sobrevive fortalecido" — se lee, honestamente, como una segunda confirmación (independiente de `CRH`) de que **el panel ENNViH 2005-2012 no tiene, para este constructo, las transiciones necesarias para decidir por la vía intra-persona** — el mismo hallazgo estructural que `metodologia-identificacion-vs-ajuste-v0_1.md §1` ya nombró, ahora verificado con un segundo desenlace independiente en vez de asumido de uno solo.

**Regla de precedencia, declarada al sellar (ADR-58(b)/59(a)):** la especificación **primaria** decide la fila — exposición `FORMAL_CONTRATO`-jefe (no la sensibilidad de "algún miembro"), desenlace `ah03h` sin ponderar **y** con `fac_2l` ola 2 (ancla, mismo ponderador que `CAL-G3` usó como referencia principal en su propia tabla). Las demás combinaciones (sensibilidad de exposición, otros ponderadores, logit vs. lineal) se reportan **todas**, sin excepción, pero como corroboración — no compiten por la fila. Si la especificación primaria y alguna secundaria caen en filas distintas, gana la primaria y se anota la discrepancia en la línea del veredicto, verbatim — mismo criterio que `ADR-58(c)` usó para `R5.1`/`R5.2`.

### (9) Límite de época y de población (heredados, misma razón)

Ventana **2005-2012**, no extrapolable al México de 2026 — misma degradación que `CAL-G3` punto 9c, misma razón (bancarización fintech posterior). Población: jefes de hogar con adherencia ocupacional continua a un empleo que `TB33` interroga — no es México, no es el México ocupado. Toda cifra de una eventual corrida de esta ficha lleva ambos calificadores pegados, sin excepción.

### (10) Restricción de lectura al ejecutar

Si esta ficha se sella y se corre, se abren únicamente: `TB` (Libro IIIA, exposición), `AH` sección `ii_ah` de Libro II (desenlace), roster del Libro C (`ls05_1`, `ls04`, `ls02_2`, `ls14` — jefatura y composición, mismos campos que `CAL-G3` ya declaró necesarios), portada de Libro IIIA (`ent`), ponderadores longitudinales, y localidad (`eloc*`) solo para el confundidor de oferta (punto 6.2). **No se abre `CRH`, `SE` ni `CR`** — mantiene el perímetro de esta ficha auditable y distinto del de `CAL-G3`.

---

## Declaración de exploración de esta sesión (ADR-46, perímetro de este acto)

Esta sesión abrió, en `data/raw/ennvih/doc/` (manuales de codificación y cuestionarios — documentación pública, no microdato de fila-por-persona): `ehh02cb_b2.pdf`, `ehh05cb_b2.pdf`, `ehh09cb_b2.pdf`, `ehh09cb_b3a.pdf`, `ehh09cb_b3b.pdf`, `ehh02cb_bc.pdf`, `ehh05cb_bc.pdf`, `ehh09cb_bc.pdf`, `ehh09q_b2.pdf` (vía `pdftotext -layout`, extracción completa a texto, sin abrir ningún `.dta`/`.zip` de microdato). **Ningún archivo `*dta*` fue abierto.** Esto es exploración de estructura (ADR-46, nivel 2: "contamina parcialmente, declarar hasta dónde") — declarado aquí en su totalidad: conteos marginales de `ah03h`/`ah04h`/`se05_1*`/`tb33p_*`/`estrato`, ninguno de los cuales es un resultado sobre `G3→horizonte_temporal` (Paso 0, distinción declarada arriba). Una sesión futura que quiera pre-registrar OTRA ficha usando estos mismos módulos (`AH`, `TB`) parte de esta misma declaración, no de cero.

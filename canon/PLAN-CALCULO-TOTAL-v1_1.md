# PLAN DE CÁLCULO TOTAL v1.0 — todos los valores, el mapeo completo de fuentes, y el orden de fuego
### 12/ago/2026 · derivado contra clon sincronizado a `origin/main = 0c4d52a` (post-#178) · sustituye como plan vigente a los planes parciales anteriores; los encargos ya emitidos (J, U1-U3) siguen válidos y aquí se ordenan

> **Nota de procedencia (20/ago/2026 · `T-SELLO`, `ADR-130`):** este documento vivía solo en el espejo del proyecto de claude.ai — nunca estuvo en el repo (`APERTURA-FASE-CALCULO-v1_1.md`, cabecera, textual: "ese plan NO está en el repo; sellarlo es la tarea T-SELLO"). Llega como adjunto de la compuerta de arranque de `T-SELLO`, no se lee de ningún `/mnt/project/` (P5 del ARRANQUE, espejo prohibido; este entorno NUBE no tiene siquiera esa ruta montada). sha256 del adjunto tal como se recibió, declarado aquí por primera vez, sin hash previo contra el cual verificar (mismo patrón que `CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`): `3f9efc4be842c7143828be082b9062cc392c5b14357d7ea135ba88ab3aaf1693` — 8 753 bytes, 46 líneas. Archivado como `canon/PLAN-CALCULO-TOTAL-v1_1.md` — v1.0 pasa a v1.1 porque gana, al final del cuerpo, la tabla `§1` de `APERTURA-FASE-CALCULO-v1_1.md` como delta fechado (`§5` nuevo, abajo); el cuerpo v1.0 original queda **intacto** arriba, sin una sola línea tocada (`A.10`, corolario 1). `diff` contra el adjunto: sin diferencia hasta el cierre del cuerpo original — las únicas líneas nuevas son esta cabecera y el `§5` añadido al final; el salto final es el mismo. Primera entrada al repo, confirmado por `git ls-files | grep -i calculo-total` contra tu SHA: cero resultados, universo árbol completo menos `.git`, **1 727 archivos** (recontado hoy; no heredado del **1 717** que declaró quien escribió el encargo — la diferencia son los archivos que entraron con `PR #295`/`PR #296` después de esa cuenta).

> | | |
> |---|---|
> | **FOTO VERIFICADA** | main `0c4d52a` · 71 ADR · **#177 CABLEADO fusionado** (propuesta en repo, `documentacion_fuente` en FORBIDDEN+schema+validate con lista cerrada, `test_celdas_d.py`, MAP-1b marcado en `manifiesto.py:95`) · **#178 ADR-71 "cuatro decisiones firmadas"** (entre ellas: las 8 de `radio_confianza` **siguen bloqueadas por compuerta correcta del motor** — `integrate_production.py:284-289` —, la escala de `R5.1-D2` **ganó su fila de corroboración** pre-dato en el pre-registro, y J quedó autorizado) · baseline recongelada · Ramas vivas: `e4c/r5-1-d2` (commit 5: corrige varianza de la **DDD**), `mesa/s-svystat-4celdas` (**ACTO S**: `diff4_ultimate_cluster`, el estimador de triple diferencia que e4c necesita), `cuatro-decisiones-…` (residuo de #178) · **J corriendo** en caja · Contadores: 13/27 · 9/14 · 0/15 · llaves **0 de 2** · producciones 10 `CALCULO_REPRODUCIBLE` + 1 `NO_DETERMINADO` · celdas-D: 2 |
> | **¿QUEDA CABLEADO?** | **Nada estructural.** Restos, nombrados: ACTO S en vuelo (estimador, pre-requisito de la corrida e4c) · P2 (fichas como activos T0) — verificar en el cierre de #177 si quedó hecho o `EN-ESPERA-DE-VIA`; si es lo segundo, es una vía de motor menor, no bloquea nada · integración celda-D↔motor = post-GO (ADR-68(a) enmendado: el congelamiento rige desde E0) · **catálogo de momentos** = la única pieza de estructura restante, y pertenece a la OLA 5, se sella cuando el piloto abra |

---

## §1 · El mapa de TODOS los valores del motor — qué es, dónde está, qué lo destraba

| Valor | Estado hoy (derivado) | Qué lo destraba | Ola |
|---|---|---|---|
| **Θ · 14 condicionales** | 9 `MEDIDO·PARCIAL` · 5 sin medir | **U1** da la 10ª (`familismo_obligacion`, ENASIC, ficha 922) · las 4 restantes cuelgan de aperturas (ENFIH/ENSAFI/GPS) y del piloto | 1-3 |
| **Θ · 8 distribuciones de `radio_confianza` (ENBIARE)** | Calculadas, **bloqueadas por compuerta correcta** (ADR-71(a)) | Acto de liberación conforme a lo que ADR-71(a) disponga — leerlo completo antes; el uso *sustitutivo* además espera el acto de vinculación-invarianza ENCUCI↔ENBIARE (ADR-67(a)) | 1 |
| **15 β de generador** | 0 medidos · censo: 3 `RUTA-A` · 1 `RUTA-I` · 2 `RUTA-C` · 9 `SIN-RUTA` | RUTA-A/C: co-observaciones ya nombradas → celdas del piloto · RUTA-I: la llave ENNViH · de los 9 SIN-RUTA: **hasta 4** salen con la apertura de ENFIH/ENSAFI/GPS (vía E-CE v1.1), 1 ya tiene θ vía U1, 1 con DESC-1, **2-3 son estructurales** (sin muestra común — se dice, no se promete) | 2-4 |
| **Momentos m-lado** | Sin catálogo sellado · candidato nuevo: brecha actitud-conducta (ADR-67(b)) | Commit 1 del catálogo (motor-matriz M4) al abrir el piloto | 5 |
| **Hito D · 27 fichas** | 13 archivadas (7D·2B·2A·2E) + **`R5.1-D2` en renglón propio con su fila de corroboración ya sellada pre-dato (ADR-71(b))** | La corrida de e4c (espera el estimador de ACTO S) · las 14 restantes, por acto con la compuerta documental nueva | 0 y sig. |
| **Llaves de identificación · 0 de 2** | `R5.1-D2` sembrada `SELLADA_NO_EJERCIDA` · ENNViH `RUTA-I` | **e4c corrida → 0→1** (el titular) · ENNViH → acto propio pre-registrado, post-piloto | 0 · 4+ |
| **Validación externa** | Ninguna producción cruzada contra lo oficial | **U2 (EV-1)**: XLS CV/EE/IC de ENBIARE-730 y ENASIC-922, dos columnas de veredicto, `NO-CRUZABLE` default | 1 |
| **Integridad del join ENIGH** | Defecto medido en 2018; 4 olas sin mirar; **J corriendo** | J entrega magnitud por ola + arreglo + plan; **mesa adjudica** si `R5.1→A` y `D5` reciben entrada nueva con estampa (ADR-67:862); re-corridas solo si la magnitud lo pide | 0 → mesa |

## §2 · El mapeo completo de fuentes, por estación del conducto (ya cableado)

**T0 declarado:** 35,708 activos / 958 programas · catálogo v2.0: 128 fuentes únicas, 43 operables. **Puertas consolidadas:** RNM dentro (P1, #177), puntero = snapshot de fecha máxima. **Adquirido e íntegro (calcula sin descargar):** ENIGH ×6 olas (2012-2022) · ENBIARE 2021 · ENASIC 2022 · ENCUCI 2020 · ENVIPE · ENCIG · **ENFIH 2019 · ENSAFI 2023 (íntegras, jamás abiertas a nivel variable — la palanca más grande dormida del corpus)**. **Documentación oficial:** fichas 922/730 abiertas; backfill de las 8 restantes = U3; indicadores CV/EE/IC publicados = insumo de U2. **Por adquirir (DESC-1):** GPS/briq · ISSP 2017 · WVS-7 · ENCOAP · Latinobarómetro (con `SIN_DISEÑO_PUBLICADO` ya declarado). **Semillas del universo desconocido (INDICE-3):** EMOVI (CEEY) · LAPOP — entran como insumos T0 nuevos, no como fuentes sueltas. **Estructurales sin arreglo por documentación:** filas 10 y 14 del censo (reactivo y desenlace sin muestra común) — exigen fuente nueva o puente, y queda escrito.

## §3 · ORDEN DE FUEGO — olas, entorno y qué mueve cada una

**OLA 0 · EN VUELO (cierra esta semana).** `J` (caja, midiendo folioviv) · `ACTO S` (estimador `diff4_ultimate_cluster`; mesa fusiona) · **e4c corrida** (caja, tras S) → **llaves 0→1** → mesa adjudica el veredicto D2 con la fila de corroboración que ADR-71(b) ya dejó sellada pre-dato. Mesa recibe de J el plan de remediación y decide sobre `R5.1→A`/`D5`.

**OLA 1 · CALCULAR CON LO QUE ESTÁ EN DISCO (caja; encargos ya emitidos).** `U1` → **primera θ de `familismo_obligacion`** (10ª condicional) · `U2` → **primera validación externa** (las 10 de ENBIARE + la de ENASIC) · `U3` → backfill documental de las 8 fichas · + acto corto de **liberación de las 8 de radio** conforme ADR-71(a). Cero descargas, cero decisiones nuevas: solo sesiones.

**OLA 2 · APERTURAS QUE REABREN DECISIONES (caja → mesa).** ABRIR ENFIH/ENSAFI **a nivel variable** contra las celdas objetivo (términos pre-registrados) → alimenta **E-CE v1.1**; si aparece reactivo: **mesa** reabre acotadamente ADR-52A/54 (la condición que Ronda 1 y el barrido dejaron idéntica) → hasta **4 SIN-RUTA** dejan de serlo. Es la ola con mayor β-por-sesión del tablero.

**OLA 3 · DESCARGAS (caja).** DESC-1 (5 fuentes, sonda A.5 en sesión, sha256 al corpus, PR#77 verificado al cierre) + INDICE-3 (EMOVI/LAPOP como insumos T0). Cada payload nuevo entra ya por el conducto completo (puerta → activo → ficha → apertura).

**OLA 4 · EL PILOTO CELDA-D (E0-E2 nube · E3 caja).** E0: agentes + cola emitida como celdas-D (validador `test_celdas_d.py` ya en main) + las 3 semillas primero · E1-E2 con auditor y veto · E3 = gate de semana 1 (ENFIH/ENSAFI ya abiertas por OLA 2 lo vuelven casi gratis) · 10-15 celdas FIN · **los 7 umbrales con conteos por comando → mesa firma GO/NO-GO.** Desde E0 rige el congelamiento del motor (ADR-68(a) enmendado).

**OLA 5 · EL AJUSTE (post-GO).** Catálogo de momentos commit 1 (motor-matriz M4, con la brecha actitud-conducta como candidato) → primer ejercicio `AJUSTADO` con la matriz entrando como **challenger de `estrategia: momentos`** → ahí, y solo ahí, entran NROY (condición ADR-68(d)) y la decisión M1. Re-corridas de FIX-JOIN si J dio magnitud. ENNViH ejerce la segunda llave.

## §4 · Qué se necesita para "ahora sí, calcular" — la respuesta corta

**Nada nuevo de estructura.** Para la OLA 0-1 el único insumo es **sesiones de caja** (J ya corre; e4c espera solo el merge de S; U1-U3 tienen encargos finales emitidos y sin gates estructurales). Para β nuevos: **aperturas** (OLA 2) y **una decisión de mesa** (la reapertura acotada 52A/54, condicionada a lo que las aperturas encuentren). Para el ajuste conjunto: el **catálogo de momentos** y el **GO del piloto** — ambos de OLA 4-5, ninguno bloquea las olas 0-3. Todo lo demás que este programa necesitaba —conducto documental, validadores, estimadores, reglas de tránsito, contrato celda-D, fila de corroboración, renglón de llaves— **ya está en main.**

**Reglas que gobiernan todas las olas (sin cambio):** cada sesión produce una medición o filas nuevas, o nada y lo dice · R1 cero citas fuera del repo · R2 premisas como script · R3 paralelo con merge local (union; botón solo limpios) · dos commits POST-DATO para toda estimación · escalas y universos declarados (A-bis) · veredictos PROPUESTOS, mesa adjudica · estampa de universo sobre todo sello (ADR-67:862) · y si algo desbloquea un cálculo a mitad de un acto, eso vale más que terminar el acto.

---

## §5 · DELTA FECHADO — 20/ago/2026 (`T-SELLO`, `ADR-130`), citado verbatim de `canon/APERTURA-FASE-CALCULO-v1_2.md §1`

**No es re-escritura de §1-§4 de arriba — es lo que se derivó del árbol siete días después de esta foto, tabla OLA por OLA. El original arriba no se toca; esto se lee al lado, no en su lugar (`A.10`, corolario 1).**

| OLA | Plan decía | Hoy, derivado | Queda |
|---|---|---|---|
| **0** | J · ACTO S · corrida e4c → llaves 0→1 · mesa adjudica D2 | **HECHA**: llaves = 1/2 ejercida; R5.1-D2 adjudicada; R5.1-D3 corrió (fila B, EJERCIDA_INDECISA) | FP-68/FP-69 (firmas en LOTE-NUBE T6) |
| **1** | U1 (10ª θ) · U2 (validación externa) · U3 (backfill) · liberar las 8 de radio (ADR-71(a)) | U1 ✓ (condicionales 9→**12/15**) · U3 ✓ (#288) · U2 **parada en adquisición** (FP-67; material → LOTE-UBUNTU T1) · liberación-8-radio: **estado no derivado** | T1 del LOTE-UBUNTU · en LOTE-NUBE T4, el ejecutor lee ADR-71(a) y declara si la liberación quedó hecha o pendiente |
| **2** | **Abrir ENFIH/ENSAFI a nivel variable** → hasta 4 SIN-RUTA ganan ruta → mesa reabre 52A/54 acotado | **NO HECHA.** Sigue siendo "la palanca más grande dormida del corpus" (palabras del plan). El census de β del plan quedó superado por `coef-universo` (50 filas, 21 co-observables) — se re-deriva de ahí | **APERTURA-ENFIH-ENSAFI** (§3, el encargo que faltaba) |
| **3** | DESC-1 (5 fuentes) + INDICE-3 | Mayormente hecha por otra vía: ADQ-15 (#277, 89 payloads), WVS/ISSP/Latinobarómetro en manifiesto; LAPOP "sin reactivo" (ADR-111) | Verificación puntual de EMOVI en LOTE-UBUNTU (una línea en T2) |
| **4** | **Piloto celda-D**: E0 nube → E1-E2 auditor/veto → E3 caja → 10-15 celdas FIN → **7 umbrales por comando → mesa firma GO/NO-GO** | E0 **aterrizado** (#266: `milpa/src/celdas.py`, `clases.py`, validador en main). E1-E3: **sin correr**. `milpa-spec`/`plan` cargan banner de incompatibilidad parcial (gobernanza:754) — declarado, no bloquea | **PILOTO-E1E3** (§4) — esto ES abrir la fase de cálculo |
| **5** | Catálogo de momentos · AJUSTADO · ENNViH ejerce llave (ii) | Catálogo v0.1 en `milpa/` · **ENNViH murió como llave (ADR-107)**; FP-64/T3 deriva candidatos | Post-GO, como el plan manda |

*(Tabla verbatim, incluida la grafía "census" de la fila OLA 2 — no se corrige aquí, mismo trato que cualquier otra cita textual; y los "§3"/"§4" de las columnas "Queda" refieren a `APERTURA-FASE-CALCULO-v1_2.md`, no a este documento.)*

**⚠️ Contradicción registrada sobre OLA 4, no resuelta aquí — ver `ADR-130(c)`:** los "7 umbrales por comando → GO/NO-GO" que esta fila cita como criterio de OLA 4 son el mismo `ADR-68(c)` que `ADR-128` (20/ago/2026) declaró VENCIDO EN ALCANCE salvo su umbral (1), mientras que `M6` del careo (`CAREO-ADV-DUELO-diseno-v2-2026-08-19.md §B`, adoptado por `D-4`) dice *"De los 7 umbrales, ≥3 de resultado"* — conserva y endurece tres, no los siete ni solo el uno. Los tres textos (esta fila, `ADR-128`, `M6`) están vigentes y dicen cosas distintas sobre el mismo GO. `ADR-130(c)` abre fila de tablero, no adjudica.

**Traducción vigente hoy, sin editar la de arriba:** de los tres actos y un marcador que el plan original pedía para "ahora sí, calcular", **D3 (PILOTO-E1E3)** y **D4 (DUELO-PREREGISTRO)** son los que faltan — ver `APERTURA-FASE-CALCULO-v1_2.md §2`.

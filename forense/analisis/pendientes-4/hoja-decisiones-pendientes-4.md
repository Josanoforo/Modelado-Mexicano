# Hoja de decisiones de mesa · GEN2-PENDIENTES-4

Generada por `arma_hoja_decisiones_pendientes_4.py` a partir de la evidencia archivada en `evidencia/` y adjudicada por el ejecutor. Cada renglón es una decisión que ningún ejecutor puede tomar (D-19): adoptar, editar o retirar algo sellado o una firma, abrir una ola reservada, o cambiar el criterio de adopción en bloque. Lo reversible ya lo decidió el acto por delegación y consta en `decididas-por-delegacion-pendientes-4.tsv`. Cada NC de estos renglones lleva `MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D<n>)` como dueño. Cuando la firma cae, el acto que la ejecuta cierra las NC del renglón citando la firma. Los renglones con «FP existente» ya tienen su ranura en `forense/firmas-pendientes.tsv`; los demás la reciben en este mismo PR (A.12).

## D1 · Régimen de aislamiento de la sesión ciega de C1 (767 identidades ENDIREH 2021)

**NC que decide (4):** `NC-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-03`, `NC-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-04`, `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-10`, `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-03`

**Situación.** La sesión ciega de las 767 identidades ENDIREH 2021 (paquetes c1-ventana-v1) tiene ya el acceso firmado (ee49-01) y la ventana transportada por R24, pero R32 autorizó el reconstructor opción A (sin broker) solo para el lote 3 y R15 exige los cuatro gates por paquete; sin régimen de aislamiento firmado no se lanza ni se anuncian 859 listos.

**Opciones.**

- **(a)** Extender R32 a la sesión de las 767 con la receta de LANZAMIENTO-LOTE3 §3 y la configuración de la sonda 3 (§4): namespace con /tmp vacío, herramientas sin red, transcript archivado y auditado antes de revelar; rótulo CIEGA-POR-CONTEXTO-NUEVO. — *Costo:* La ceguera no es por broker: el proceso claude sale a la API (misma reserva que el lote 3).
- **(b)** Exigir broker de red acreditado antes de lanzar (receta-sesion-futura.md paso 5; NC beee-08). — *Costo:* Un acto de infraestructura en CAJA sin fecha (EJECUTOR-AISLADO-3 dejó el broker sin provisionar); las 767 siguen sin validación independiente mientras tanto.
- **(c)** No validar las 767 a ciegas: quedan SOSTENER-SIN-CORROBORACION con la ventana transportada por R24. — *Costo:* 767 identidades (COM 100, ESC 96, LAB 100, NF 471) sin validación independiente de forma permanente.

**Recomendación.** (a) Mesa ya aceptó la opción A para el lote 3 con transcript auditado; el broker no tiene acto que lo provisione. (a) convierte 767 NO-HECHA en validación rotulada, sin presentarla como aislamiento por broker.

**Plazo.** Antes de redactar GEN2-ASTRA6-C1-LOTE-4 (MESA 2026-10-05)

**Texto de firma.** «Extiendo la autorización del reconstructor de opción A (R32) a la sesión ciega de las 767 identidades ENDIREH 2021 de los paquetes c1-ventana-v1, con la receta de LANZAMIENTO-LOTE3 §3 y la configuración de la sonda 3 (§4): namespace con /tmp vacío, herramientas sin red, transcript archivado y auditado antes de revelar. Sus resultados llevan el rótulo CIEGA-POR-CONTEXTO-NUEVO y no se presentan como aislamiento por broker. El broker sigue como meta.»

*Fuente del renglón: investigador (adjudicada).*

## D2 · Contratos nuevos de C1: escolaridad NIV-terminal-v1 y P14_22_14

**NC que decide (1):** `NC-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-03`

**Situación.** El carril «contrato nuevo» de C1 ENDIREH 2021 (escolaridad NIV-terminal-v1 en 31 dominios; P14_22_14 leyes frente a servicios en ayuda 115) quedó «pendiente de firma por bloque» en R24; sin firma no hay contrato nuevo que entregar a validadores. La exclusión EDAD 98/99 de los sucesores ya la firmó R25.

**Opciones.**

- **(a)** Firmar por bloque NIV-terminal-v1 y P14_22_14 como contrato NUEVO con identidades sucesoras. — *Costo:* Un acto de preparación en CAJA más una sesión ciega; cifras nuevas sobre ola vista, no equivalentes al histórico.
- **(b)** No abrir el carril nuevo: C1 sigue solo por transporte (R24) con el método anterior; EDAD 98/99 queda como la firmó R25 para los sucesores 2011/2021. — *Costo:* Escolaridad y ayuda conservan el bin histórico y su D-15 de recodificación NIV/GRA (23 + 8 llaves en specs-insuficientes-v1_2), que se resuelve por adenda de spec, no por contrato nuevo.
- **(c)** Diferir hasta que un consumidor (informe o catálogo) pida escolaridad terminal o desconocimiento de leyes. — *Costo:* La fila queda abierta sin fecha.

**Recomendación.** (b) C1 existe para reproducir cifras ya selladas; un contrato nuevo crea estimandos nuevos sobre una ola vista sin consumidor que los pida, y el transporte de R24 ya cubre las 767. La recomendación es del ejecutor; el contenido lo decide mesa.

**Plazo.** Antes de redactar GEN2-ASTRA6-C1-LOTE-4 (MESA 2026-10-05)

**Texto de firma.** «NC-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-03: opción (b). No firmo los contratos nuevos NIV-terminal-v1 ni P14_22_14; C1 sigue por el carril de transporte de R24 con el método anterior. La exclusión de EDAD 98/99 queda como la firmó R25 (FP-260926-ASTRA6-C1-ADJUDICACION-PUNTOS-1-39de-01) para los sucesores 2011/2021. Si un consumidor pide escolaridad terminal o desconocimiento de leyes, se abre hoja nueva.»

*Fuente del renglón: investigador (adjudicada).*

## D3 · Margen de equivalencia y control simultáneo para los IC de C1

**NC que decide (2):** `NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-04`, `NC-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01`

**FP existente:** `FP-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01` (la decisión ya tiene su ranura; este renglón no acuña otra).

**Situación.** Las 1 873 llaves SOSTENER del lote 1 de C1 (RECIBO-ASTRA6-1, no del lote 2) coinciden en el punto (|Δ| ≤ 1e-10) y no en el IC (Δ típico 2e-4, bootstrap con otra semilla). R23 (FIRMADA) hace diagnóstico al IC reimplementado y no recertifica IC históricos, así que ninguna es PASA. Están repartidas en 9 RESULT que ya tienen fila NO-PASA en la vista, y solo 2 de esos RESULT (DEC 138 y FAM 50) tienen todas sus llaves SOSTENER: el contador no se mueve por 1 873, se mueve por filas RESULT.

**Opciones.**

- **(a)** Dejarlas sin PASA. La FP 2385-01 se firma solo para conjuntos sin revelar (con su margen o sin él) y no se extiende nada a las 1 873. — *Costo:* Ninguno: el contador queda como está (215) y la NC se cierra como aceptada; si mesa quiere extenderlo después, se reabre.
- **(b)** Firmar la opción (b) de la FP (IC diagnósticos para siempre; asiento por punto con alcance INFERENCIA-NO-COMPROBADA) y extenderla expresamente a las 1 873. — *Costo:* Cambia el criterio de PASA (punto e IC) para C1; exige un acto que reemplace las filas NO-PASA de DEC y FAM (la vista no admite dos validaciones por (spec, RESULT)) y rotule el alcance; el contador sube en a lo sumo 2 filas, no en 1 873; toda frase de producto debe repetir el alcance.
- **(c)** Margen en unidades de SE (opción (a) de la FP) aplicado también a las 1 873. — *Costo:* Fijaría el umbral con los Δ ya a la vista: incumple v2.16 §4 (la regla y el umbral se fijan antes de abrir el dato). Mismo efecto máximo (2 filas).
- **(d)** Exigir igualdad de marco y totales por UPM y relanzar los paquetes (opción (c) de la FP). — *Costo:* Contrato nuevo y relanzamiento; la más cara; el efecto sobre el contador sigue acotado por las mismas 9 filas.

**Recomendación.** (a) R23 ya firmó que el IC reimplementado no adjudica y que no recertifica históricos; extender un criterio a llaves ya reveladas para mover a lo sumo 2 filas RESULT no compensa el cambio de criterio. La decisión sobre conjuntos sin revelar (lote 3 y lote 4) sigue en la FP 2385-01 sin cambios.

**Plazo.** 2026-10-05 (la fecha MESA que ya llevan las NC hermanas 2385-0x)

**Texto de firma.** «Sobre NC-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01 y FP-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01: opción (__). Con (a): las 1 873 llaves SOSTENER del lote 1 quedan sin PASA por R23, sin extenderles margen ni asiento por punto; la NC 26a2-01 se cierra; el margen o el asiento por punto de la FP 2385-01 valen solo para conjuntos sin revelar.»

*Fuente del renglón: investigador (adjudicada).*

## D4 · Publicabilidad frágil de 10 celdas ENDIREH del lote 1

**NC que decide (1):** `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-07`

**Situación.** 10 celdas ENDIREH del lote 1 cambian de publicabilidad según la realización del bootstrap (margen al umbral ≤ banda Monte Carlo 0.100); hoy están ACOTADA con el rótulo «publicabilidad frágil al RNG» (beee-02, catálogo v1.3). La regla de supresión sellada no fija el RNG.

**Opciones.**

- **(a)** Dejar las 10 en ACOTADA de forma permanente, sin regla nueva. — *Costo:* 10 celdas quedan con rótulo en vez de dictamen; no requiere trabajo.
- **(b)** Firmar una regla de publicación con margen para los CALC sucesores: publicable solo si el margen al umbral supera la banda Monte Carlo, o con semilla y orden de RNG fijados en la spec sucesora. — *Costo:* Spec sucesora y CALC nuevo en CAJA por paquete, congelados antes de abrir el dato; el criterio ya no se ajusta.
- **(c)** Decidirla junto con FP 2385-01 (margen de IC de C1). — *Costo:* Espera a esa firma.

**Recomendación.** (a) El trato en producto ya está firmado y ejecutado (beee-02, #1227). La regla solo cambiaría un rótulo en olas vistas y ningún consumidor la pide. Es coherente con la opción (b) que recomienda FP 2385-01: sin consumidor, diagnóstico.

**Plazo.** Con FP-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01 (MESA 2026-10-05)

**Texto de firma.** «NC-260927-GEN2-RECIBO-ASTRA6-1-beee-07: opción (a). Las 10 celdas de publicabilidad frágil quedan ACOTADA como firmó FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02; no fijo regla de publicación con margen mientras ningún consumidor la pida. El sello no se toca.»

*Fuente del renglón: investigador (adjudicada).*

## D5 · Coercitivo digital (RES-0017/0018) y M03: HISTÓRICO-SIN-RELEVO

**NC que decide (3):** `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-09`, `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-10`, `NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-02`

**FP existente:** `FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-02` (la decisión ya tiene su ranura; este renglón no acuña otra).

**Situación.** RES-0018 (tramite.gobierno_digital.coercitivo, adopta p 0.09, complemento de RES-0017, clase ASIGNADO) no tiene medición GEN2 ni instrumento que distinga un servicio digital obligatorio (tramite.yaml:254). Mesa ya firmó conservar la p ASIGNADO 0.91/0.09 (FP-273, D10 del 3/sep); el dictamen #1275 lo deja SIN-BASE-GEN2 y la ranura B2 (c133-02) sigue ABIERTA.

**Opciones.**

- **(a)** RES-0017/0018 quedan HISTÓRICO-SIN-RELEVO con rótulo ASIGNADO-CONSERVADO, junto con M03 (B2 a), conforme a FP-273. — *Costo:* La regla sigue emitiendo un ASIGNADO rotulado y el motor conserva 2 lecturas legacy rotuladas. Cero caja, cero sello.
- **(b)** Mesa fija un instrumento (p. ej. un proxy de trámite en línea de ENCIG 2025) y se encarga un CALC de caja descriptivo que releve la proporción. — *Costo:* Un acto de caja; el estimando cambia a un proxy (tramite.yaml:254 declara EXISTE-NO-SATISFACE en ENCIG 2025): riesgo de medir otra cosa y de contradecir FP-273.

**Recomendación.** (a) Sin instrumento no hay qué medir. (a) es la misma decisión de B2, es coherente con FP-273 (conservar el ASIGNADO hasta tener adopción vigente) y con la regla FIRMAS-16 B1 vía e760-01 («donde no coinciden, se conserva con rótulo»). Si aparece un instrumento, entra como momento nuevo.

**Plazo.** 2026-10-05

**Texto de firma.** «Firmo B2 (a) con sus lecturas: M03 y las proporciones ASIGNADO RES-0017/0018 (tramite.gobierno_digital.coercitivo: rechaza_servicio 0.91 / adopta 0.09) quedan HISTÓRICO-SIN-RELEVO con rótulo ASIGNADO-CONSERVADO, conforme a la conservación firmada en FP-273 (D10, 3/sep/2026); si aparece un instrumento que distinga la obligatoriedad del canal, entran como momento nuevo con CALC de caja.»

*Fuente del renglón: investigador (adjudicada).*

## D6 · ITER del Censo 2020: levantar la reserva E.6

**NC que decide (1):** `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-02`

**Situación.** Cinco afirmaciones (TIME-027, RURAL-026/027, FAM-037, AUTOR-021) necesitan el ITER del Censo 2020 (payload cpv2020_iter_nal_csv). Está RESERVADO para proteger la lectura de hogares 2015→2020 (COLA-EIC-HOGARES:108) y mesa firmó el 26/sep con esa reserva vigente (FP 3a49-01). La corrida -0001 leyó el payload y el conducto la rechazó sin escribir valores; los artefactos -0001/-0002 no están en origin/main.

**Opciones.**

- **(A)** Levantar por escrito la reserva completa del Censo 2020 ITER, volver a congelar el CALC y correrlo. — *Costo:* Un acto CAJA de dos commits. El Censo 2020 deja de servir como ola de contraste de la serie EIC-hogares.
- **(B)** Levantar solo las columnas ITER de las cinco afirmaciones (religión, indigeneidad, lengua, edad) con guardia de columnas en el medidor y prueba por mutación. Las columnas de hogar y jefatura siguen RESERVADAS y se declara lo que se aparta. — *Costo:* Un acto CAJA de dos commits, más la prueba por mutación de la guardia de columnas.
- **(C)** Mantener la reserva. — *Costo:* JUVENTUD sin estimador y RURAL_INDIGENA sin dictamen: la huella indígena difusa queda sin mapear.

**Recomendación.** (B) La reserva protege la tendencia de hogares 2015→2020 (spec:108). Religión, indigeneidad, lengua y edad no son ese estimando, y E.6 pide declarar lo que se aparta sin abrir; la guardia de columnas conserva el contraste de hogares.

**Plazo.** 2026-10-05

**Texto de firma.** «PISOS-DOMINIOS-Y-REGLAS-1 7cd0-02 (Censo 2020 ITER): opción (__). Si (B): levanto por escrito la reserva E.6 del Censo 2020 ITER solo para las columnas de TIME-027, RURAL-026, RURAL-027, FAM-037 y AUTOR-021, con guardia de columnas congelada en COMMIT-1; las de hogar y jefatura siguen RESERVADAS para COLA-EIC-HOGARES. Si (A): se levanta la reserva completa. Si (C): se mantiene.»

*Fuente del renglón: investigador (adjudicada).*

## D7 · Qué significa que una regla SI-ENTONCES «se confirma»

**NC que decide (1):** `NC-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-03`

**FP existente:** `FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01` (la decisión ya tiene su ranura; este renglón no acuña otra).

**Situación.** Una regla SI-ENTONCES ¿«se confirma» cuando solo su parte descriptiva (el SI) está medida, o solo cuando también lo está la recomendación (el ENTONCES)? De eso depende que el primer bloque de adopción tenga 1 regla (alimentos ENIGH 2022: decil 1 = 0.511 [0.483, 0.539] frente a 0.283 [0.260, 0.308] del decil 10; hogar; RETROSPECTIVA) o 0. El usuario pidió antes el insumo del prompt de búsqueda; no hay respuesta en main.

**Opciones.**

- **(a)** CONFIRMA cubre la conducta descriptiva (SI): el bloque 1 adopta la regla de alimentos como conducta descriptiva. — *Costo:* Se adopta (por merge) una regla cuyo ENTONCES prescriptivo nadie ha medido y cuyo PORQUE no está identificado; riesgo de convertir una asociación en recomendación (v2.16 §4).
- **(b)** CONFIRMA exige la regla completa; la regla pasa a MATIZA y el bloque 1 queda en 0. — *Costo:* Cero adopciones por ahora; el bloque espera cruces medidos en caja.
- **(c)** Vocabulario partido: CONFIRMA-SI (descriptiva: se registra, no se adopta) frente a CONFIRMA (regla completa: se adopta). El bloque 1 queda en 0 y la regla de alimentos queda rotulada CONFIRMA-SI. — *Costo:* Una palabra más en el vocabulario cerrado del dictamen y su test; ninguna adopción.
- **(d)** Esperar el insumo antes de firmar. Receta de un minuto: pegar forense/analisis/reglas-y-result-1/prompt-criterio-confirma.md en una sesión con búsqueda web y devolver la tabla. — *Costo:* Retrasa la FP a3cc-01 sin plazo mientras nadie corra el prompt; la receta la ejecuta una persona (o una sesión con búsqueda web que mesa designe).

**Recomendación.** (c (y d solo si mesa quiere el insumo antes de firmar)) Conserva lo medido (el SI, con IC disjuntos) sin adoptar una recomendación no medida, y es el tipo de vocabulario cerrado que v2.16 §5 prefiere. No exige esperar la búsqueda: el prompt pregunta justo por una distinción como «supported-descriptive» y (c) es reversible en una línea si el insumo dice otra cosa.

**Plazo.** 2026-10-05

**Texto de firma.** «Criterio de CONFIRMA (a3cc-03): opción (__). Con (c): CONFIRMA exige la regla completa; un SI descriptivo sostenido por RESULT se rotula CONFIRMA-SI y no se adopta; el bloque candidato 1 queda en 0 reglas.» Con (d): «Espero el insumo de prompt-criterio-confirma.md antes de firmar a3cc-01 y a3cc-03.»

*Fuente del renglón: investigador (adjudicada).*

## D8 · EDER 2025 (JUV-001/002): levantar la reserva E.6

**NC que decide (1):** `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-03`

**Situación.** JUV-001 y JUV-002 (salida del hogar y primera unión por cohorte, EDER 2025) necesitan una ola RESERVADA por E.6, sin apertura escrita y que no se abrió. Pero ambos cruces ya se vieron: un extracto web del comunicado EDER los expuso (revision-material.md:24) y mesa firmó el 28/sep (FP b544-02, R11 opción 2) que lo visto se declara consumido y solo sirve en retrospectiva. Una marca PROSPECTIVA ya no es posible para estos dos cruces.

**Opciones.**

- **(A)** Mesa levanta por escrito la reserva E.6 de EDER 2025 solo para JUV-001/002 (columnas edad_dejar, edo_civil1 y cohorte, con guardia de columnas congelada en COMMIT-1 y prueba por mutación). GEN2-PISOS-DOMINIOS-Y-REGLAS-2 (CAJA) los mide como pisos RETROSPECTIVA. — *Costo:* Un acto CAJA de dos commits más la prueba de la guardia. El resto de EDER 2025 sigue reservado para una prueba pre-registrada; estos dos cruces ya no pueden servir como prueba prospectiva.
- **(B)** Como A, pero antes de abrir se sella, como emisión punto-fijo con IC, el piso por cohorte de EDER 2017 (misma forma que las familias 2027) y la ola la abre el código congelado de esa prueba. — *Costo:* Un commit de spec más (NUBE) y un acto CAJA de tres commits. No cambia el rótulo de JUV-001/002 (siguen RETROSPECTIVA por b544-02); solo deja lista la ola para otros cruces. Ya existen CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001/-0002, pero su estimando declarado es el perfil de primera unión (p(libre)), no la edad de salida del hogar.
- **(C)** Mantener la reserva sin medir. — *Costo:* JUVENTUD sin estimador.

**Recomendación.** (A) Los dos cruces están consumidos por b544-02, así que protegerlos ya no compra una comparación prospectiva; la guardia de columnas deja reservado el resto de la ola. B suma un commit sin cambiar el rótulo de estos dos cruces.

**Plazo.** 2026-10-05

**Texto de firma.** «PISOS-DOMINIOS-Y-REGLAS-1 7cd0-03 (EDER 2025, JUV-001/002): opción (__). Si (A): levanto por escrito la reserva E.6 de EDER 2025 solo para las columnas de JUV-001 y JUV-002, con guardia de columnas congelada en COMMIT-1 de GEN2-PISOS-DOMINIOS-Y-REGLAS-2; se rotulan RETROSPECTIVA (cruces consumidos por FP b544-02) y el resto de la ola sigue RESERVADO. Si (B): la reserva la levanta solo el código congelado de esa spec, después de sellar como emisión con IC el piso por cohorte de EDER 2017. Si (C): se mantiene la reserva.»

*Fuente del renglón: investigador (adjudicada).*

## D9 · ENCO (ahorro percibido): medir P10 y aceptar un puente

**NC que decide (1):** `NC-0318`

**Situación.** Para medir con ENCO (dos olas reservadas, junio 2025 y junio 2026) el ahorro percibido faltan tres permisos: medir P10, aceptar un puente con dinero.ahorro.tiene_ahorros (el propio encargo declara que no está identificado) y fijar cómo se calcula la varianza entre años. Abrir P10 consume la reserva que ENCO guarda para F6/B y el puente adopta una equivalencia.

**Opciones.**

- **(a)** Autorizar las tres piezas: medición descriptiva de P10, puente con dinero.ahorro.tiene_ahorros y contrato de varianza interanual. — *Costo:* Abre ENCO reservada (E.6, tres commits en CAJA) y consume su valor prospectivo; adopta un puente que el propio encargo declara no identificado.
- **(b)** Solo el contrato de varianza interanual, documental y sin abrir microdato. — *Costo:* Un acto sin dato; la reserva queda intacta, pero la medición sigue sin punto y la NC sigue viva para las otras dos piezas.
- **(c)** Mantener la reserva de ENCO, no autorizar P10 ni el puente, y cerrar la NC por decisión de mesa; lo preparado queda como historia. — *Costo:* Cero. El ahorro percibido se queda sin punto GEN2 desde ENCO mientras la reserva siga.

**Recomendación.** (c) ENCO figura en las reservas vigentes, la hoja de familias 2027 tampoco abre ENCO (:39) y el puente con tiene_ahorros no está identificado según su propio encargo. Si mesa quiere avanzar sin abrir dato, (b) es compatible y barata.

**Plazo.** 2026-10-05

**Texto de firma.** NC-0318: opción (c). ENCO sigue reservada; no se autorizan la medición descriptiva de P10 ni el puente con dinero.ahorro.tiene_ahorros; lo preparado en forense/produccion/enco-dos-olas-reservadas-1/ queda como historia y la fila se cierra por decisión de mesa.

*Fuente del renglón: investigador (adjudicada).*

## D10 · Ahorro ENNViH (RES-0029/0030) y la ola 3 reservada

**NC que decide (2):** `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-15`, `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-16`

**FP existente:** `FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-01` (la decisión ya tiene su ranura; este renglón no acuña otra).

**Situación.** dinero.ahorro.tiene_ahorros (RES-0030, no_tiene_ahorros p 0.8252, complemento de RES-0029) es una medición GEN1 con las olas 2 y 3 de ENNViH. Los payloads están en el corpus, pero la ola 3 (2009) es la más reciente del programa en el manifiesto y está reservada. Mesa ya la conservó como historia (firma c1, tramite.yaml:663) y la dejó SIN-RECETA (FP-339, decisiones.tsv:6-7); la lectura ENIF 2024 (RES-0031, GEN2) la sustituye en el cálculo. FP-339 se firmó cuando el payload figuraba NO-LOCALIZADO; hoy está localizado (tramite.yaml:681), por eso B1 pide firma nueva.

**Opciones.**

- **(a)** HISTÓRICO-SIN-RELEVO: sale del pendiente y se conserva como GEN1 rotulado (RES-0029/0030 juntas). — *Costo:* El motor conserva 2 lecturas GEN1 rotuladas. Cero caja; no gasta la reserva.
- **(b)** Spec de caja solo con la ola 2 (2005). — *Costo:* Un acto de caja; el estimando cambia (una ola en vez de dos) y así se declara; contradice la conservación como historia de la firma c1.
- **(c)** Mesa abre la ola 3 de ENNViH para esta conducta. — *Costo:* Irreversible: consume la reserva de la ola más reciente de ENNViH (D-19) por una medición que el cálculo ya no usa.

**Recomendación.** (a) Coincide con lo que mesa ya firmó en sustancia (firma c1 y FP-339), no gasta la reserva de la ola 3 y no exige acto de caja; B1 solo le pone el rótulo GEN2 de HISTÓRICO-SIN-RELEVO.

**Plazo.** 2026-10-05

**Texto de firma.** «Firmo B1 (a): `dinero.ahorro.tiene_ahorros` (RES-0029/0030) queda HISTÓRICO-SIN-RELEVO, igual que sus celdas por FP-339 y como ya la conservó la firma c1; la ola 3 de ENNViH sigue reservada.»

*Fuente del renglón: investigador (adjudicada).*

## D11 · ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato

**NC que decide (1):** `NC-260921-GEN2-ADQUIERE-ENVIPE2026-ENIGH2024-1-dd08-01`

**Situación.** El overlay de reactivos no trae texto de ENVIPE 2026 (0 de 43 024 líneas) porque indexarla exige leer su FD y sus dos cuestionarios, y la reserva de ENVIPE 2026 (decisiones.tsv:181) no dice si los documentos de instrumento se pueden leer; la de ENIGH 2024 (:192) sí lo dice. Además la herramienta sobrescribe el overlay completo con 0 filas si el objeto no está indexado (hallazgos.md:1031) y sigue sin guarda.

**Opciones.**

- **(a)** Confirmar para ENVIPE 2026 el mismo alcance de lectura que reserva:enigh2024 (:192): cuestionarios, descriptor de archivos y nota metodológica se pueden leer; microdato, tabulados, comunicados y presentaciones de resultados siguen reservados. Un acto NUBE indexa envipe2026 desde el FD, sin abrir el CSV, y publica el overlay. — *Costo:* Expone texto de instrumento (no respuestas) de una ola reservada, y una lectura no se deshace. Precedentes en main: el PARO b) del encargo ENIGH (:36) aplica «lo mismo con ENVIPE 2026» solo a microdato y resultados; el encargo del duelo (:18) abre el FD 2026; el mapa de instrumentos (M16) cita el cuestionario 2026.
- **(b)** Mantener la reserva íntegra: el overlay espera a que una prueba con código congelado o mesa por escrito levante la reserva; la NC pasa a APERTURA. — *Costo:* Búsqueda de reactivos sin ENVIPE 2026 hasta la apertura; deuda viva sin plazo.
- **(c)** Cerrar por diseño: ninguna medición abierta necesita el overlay de una ola reservada. — *Costo:* Se pierde la traza; al levantarse la reserva alguien debe redescubrir el hueco.

**Recomendación.** (a) El precedente ENIGH 2024 ya separa documentos de instrumento de resultados, y el propio texto de reserva de ENIGH declara que hereda los términos de ENVIPE 2026; indexar no deriva ninguna cifra. En cualquier opción, la guarda anti-sobrescritura de la herramienta (defecto real: main() de origin/main no tiene ninguna) la agrega el primer acto que toque tools/actualiza_reactivos_contexto.py, como defecto adyacente (D-21).

**Plazo.** 2026-10-05

**Texto de firma.** «ENVIPE 2026, overlay de reactivos: opción (a). Confirmo para ENVIPE 2026 el alcance de lectura de reserva:enigh2024: su cuestionario, descriptor de archivos y nota metodológica se pueden leer; microdato, tabulados, comunicados y presentaciones de resultados siguen reservados. Un acto NUBE indexa envipe2026 en las tablas de fuentes de tools/actualiza_reactivos_contexto.py y publica el overlay.»

*Fuente del renglón: investigador (adjudicada).*

## D12 · Familia F6 (transferencia de M): retirar o reactivar

**NC que decide (3):** `NC-0161`, `NC-0162`, `NC-0324`

**Situación.** F6 (probar que M transfiere a familias de encuesta no usadas para afinar M) está EN-ESPERA-PANEL desde el 16/sep por dos firmas vigentes (FP-380 y el re-sello dfbe-01 del 22/sep). Hoy hay 0 familias elegibles (tarjetas.yaml: R01-MOCIBA y R09-ISSP CANDIDATO-NO-ELEGIBLE), cero llamadas autorizadas y la adquisición pública quedó agotada (la cola marca OBTENIDO los FD de MOCIBA 2021/2023; falta lectura en CAJA). NC-0161 (piloto y confirmación) sigue abierta con un dueño, ADQUISICION, que ya no puede moverla.

**Opciones.**

- **(a)** Retirar F6 por decisión de mesa: NC-0161 y NC-0162 pasan a CERRADA con cita a esta firma; FP-380 y el re-sello dfbe-01 quedan como historia (no se editan). La pregunta de transferencia se replantea, si hace falta, con las familias 2027. — *Costo:* Se abandona la única vía diseñada para probar transferencia de M a familias nunca vistas; la hoja de familias 2027 dice que sus seis familias no son evidencia de transferencia confirmatoria (:41). Enmienda una espera firmada, por eso decide mesa. Se reabre con una fila nueva si una familia 2027 lo pide.
- **(b)** Mantener F6 en EN-ESPERA-PANEL sin acto que la mueva: ambas filas pasan a dueño MESA-DECISION y se revisan cuando se abra la primera familia 2027. — *Costo:* Dos filas abiertas durante meses sin trabajo asociado; no cuesta nada más y conserva la pregunta.
- **(c)** Reactivar F6: mesa lanza un encargo CAJA (a redactar) que lea el FD de MOCIBA 2021/2023 e ISSP v26 y traiga las firmas que faltan: enlace predictivo pre-R para R01 y R09 (hoy CANDIDATO-NO-ELEGIBLE), y las de tarjetas, modelo, presupuesto y llamadas (tarjetas.yaml, firma PENDIENTE-DE-MESA). — *Costo:* Una sesión de caja, varias firmas de mesa y una excepción explícita a la etapa de retadores cerrada; además leer el FD no basta para volver elegible a R01 (falta el enlace).

**Recomendación.** (a) Con 0 familias elegibles, la adquisición pública agotada y varias firmas nuevas de mesa como requisito para siquiera correr F6, mantener las dos filas no produce nada; (a) es la única opción que baja la deuda y se reabre con una fila nueva. No cierra «por regla 6» (habla de olas ya vistas y las familias de F6 son retenidas): cierra por decisión de mesa.

**Plazo.** 2026-10-05

**Texto de firma.** «Firmo: F6 (transferencia de M a familias no usadas para afinar M) se retira. NC-0161 y NC-0162 pasan a CERRADA por esta firma; FP-380 y FP-260922-GEN2-FP374-RESELLO-1-dfbe-01 quedan como historia sin editarse. La pregunta de transferencia se replantea, si hace falta, con las familias 2027.»

*Fuente del renglón: investigador (adjudicada).*

## D13 · Firma de contenido de los sucesores ENDIREH 2006 y 2016

**NC que decide (1):** `NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02`

**Situación.** R21 firmó solo el recibo de los dictámenes ENDIREH 2006 (P7_4 de MD pregunta después de separarse, no el último año; 225 celdas: 5 RETIRAR-MD-ANUAL y 220 SUCESOR-MC-ANUAL-SIN-POOL-MD) y ENDIREH 2016 (bins NIV propios, 2 identidades); el contenido de los sucesores sigue sin firma y sin CALC.

**Opciones.**

- **(A)** Firmar por separado las tres líneas del dictamen: (1) ENDIREH2006-PAREJA-VENTANAS-V3 con retiro de la interpretación anual de las 5 llaves MD; (2) bins NIV de endireh-pisos-2016-discriminacion-0001; (3) ídem endireh-pisos-2016-restantes-0001. Sellos y llaves históricas intactos. — *Costo:* Habilita un encargo de CALC sucesores en caja. Retirar la interpretación anual de 5 llaves selladas no se deshace en la práctica. Los sucesores son convención nueva, no reproducción del histórico.
- **(B)** Firmar solo ENDIREH 2006 (defecto de validez del estimando) y dejar los bins de ENDIREH 2016 sin firmar. — *Costo:* Las 2 identidades ENDIREH 2016 siguen con D-15 de escolaridad y sin sucesor; menos superficie firmada.
- **(C)** No firmar: los dictámenes quedan recibidos y los sucesores sin fecha. — *Costo:* 225 celdas ENDIREH 2006 conservan una ventana anual que el cuestionario MD no respalda, sin sucesor; nada nuevo se mide.

**Recomendación.** (A, con las tres líneas firmadas por separado para que mesa pueda vetar cada una.) El dictamen contesta validez del estimando, no coincidencia numérica (dictamen L5-L13). R21 ya lo aceptó como base; falta solo el paso que autoriza crear el sucesor. Firmar por línea conserva el veto por identidad.

**Plazo.** MESA 2026-10-05, antes de escribir el encargo de sucesores ENDIREH en caja.

**Texto de firma.** «Firmo A: (1) acepto el dictamen P7_4 MD postseparación, retiro su interpretación anual y autorizo crear sucesor con separación MC anual/MD postseparación conforme a impedimentos-lote2-p2-dictamen-y-hoja-firma.md; (2) adopto exclusivamente para nueva cohorte los bins NIV propuestos para endireh-pisos-2016-discriminacion-0001; (3) ídem para endireh-pisos-2016-restantes-0001. Mantengo los históricos; no adopto resultados ni cambio llaves ni sellos históricos.»

*Fuente del renglón: investigador (adjudicada).*

## D14 · G1-B: partir resultados.tsv ya sin objeto

**NC que decide (1):** `NC-260928-GEN2-TUBERIA-Y-CURACION-1-247d-01`

**Situación.** Mesa firmó (G1, opción B) partir resultados.tsv porque pasaba de 100 MB y GitHub lo rechazaba. Otro acto ya lo dejó en 15.6 MB y la CI falla a 50 MB, tal como mesa había firmado el 24/sep. La partición ya no hace falta, pero la firma sigue vigente y sin ejecutar.

**Opciones.**

- **(a)** Retirar G1-B como SIN-OBJETO, citando el tamaño de hoy y la guarda de 50 MB; si la guarda salta, se re-litiga. — *Costo:* Cero trabajo; si el archivo crece, la CI falla en voz alta a 50 MB y obliga a decidir entonces.
- **(b)** Mantener G1-B como plan de contingencia sin ejecutar, con un aviso temprano (por ejemplo a 40 MB) en el lote de tubería. — *Costo:* Un test o guarda pequeño (acto NUBE de tubería) que duplica la alarma de 50 MB; la partición no se construye mientras no haga falta.
- **(c)** Ejecutar la partición de todos modos. — *Costo:* Migrar a todos los lectores (consulta.py, vistas, tableros) sin beneficio actual; el acto NUBE más caro.

**Recomendación.** (a) El riesgo que motivó la firma (GH001 a más de 100 MB) ya lo resolvió otro mecanismo medido, y la guarda de 50 MB es la alarma. Construir la partición ahora sería trabajo sin demanda (§1).

**Plazo.** 2026-10-05

**Texto de firma.** «G1 (247d-01): opción (__). Con (a): G1-B queda SIN-OBJETO porque resultados.tsv pesa 15.6 MB con guarda de 50 MB en verify.yml; si la guarda salta, se re-litiga.»

*Fuente del renglón: investigador (adjudicada).*

## D15 · Guarda 4.1: relevo de champion compuesto que ingiere resultados ajenos

**NC que decide (2):** `NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-06`, `NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-07`

**Situación.** Cinco lecturas antiguas de celdas-D siguen sin relevo. Dos (RES-0171 ahorro informal ENIF 2024, RES-0175 evasión de norma ENVIPE 2025) ya tienen champion C2 con punto GEN2 sellado, pero ese CALC se arma con resultados de otros tres CALC y la regla 4.1 no deja pinar eso (comprobado por comando, no supuesto). Las otras tres (G5, RES-0172/0173/0174) son baseline GEN1 sin CALC GEN2.

**Opciones.**

- **(a)** Firmar un criterio nuevo para champions compuestos: se puede pinar cuando TODO lo ingerido son RESULT de CALC sellados que cuentan, con replay afirmativo y sin GEN1 (varios padres y crudo declarado). Alcance: RES-0171, RES-0175 y RES-0211 (e760-07). — *Costo:* Cambia el contrato de relevo para todos los consumidores (E.2/E.3, regla 4.1): reescribir _valida_derivado y la guarda (d) con tests y un acto NUBE, y esperar a que el [deriva] registre los CALC ARBITRO-CRUCE-0002. Baja 3 lecturas; las 3 G5 siguen aparte.
- **(b)** Mantener la guarda 4.1 como está. Las 5 quedan legacy con rótulo; el punto GEN2 vigente de RES-0171/0175 sigue citado en el yaml de su celda; las 3 G5 quedan en GEN1 hasta que un consumidor vivo pida su medición GEN2 (CALC nuevo de CAJA, RETROSPECTIVA). La NC se cierra como aceptada. — *Costo:* El contador celdas_D no baja por estas 5 lecturas (queda visible, no se maquilla). Si un consumidor lo pide después, se reabre.
- **(c)** Declarar las 5 HISTÓRICO-SIN-RELEVO, como mesa hizo con las 42 lecturas del duelo (FP e760-03). — *Costo:* El contador baja por declaración y no por medición; se renuncia al relevo de tres champions vivos y de tres baselines que aún alimentan celdas LISTO.

**Recomendación.** (b) Los números vigentes de RES-0171/0175 ya son GEN2 y visibles en su celda; el pin solo quita 3 lecturas legacy del contador. Aflojar 4.1 (fijada por test) para eso abre la puerta a cadenas de varios padres que la firma 7bf5-02 cerró a propósito. Para las 3 G5 no hay CALC ni consumidor que lo pida; medirlas sin demanda sería trabajo sin lector (§1). La hoja 21 ya recomendaba mantener el rechazo hasta ver el caso concreto: este es el caso.

**Plazo.** 2026-10-05

**Texto de firma.** «e760-06 y e760-07: opción (__). Con (b): la guarda 4.1 no se toca; RES-0171, RES-0172, RES-0173, RES-0174, RES-0175 y RES-0211 quedan legacy con rótulo; las NC e760-06 y e760-07 se cierran como aceptadas; si un consumidor vivo pide un número GEN2 de los tres baselines G5, entra como CALC nuevo de CAJA.»

*Fuente del renglón: investigador (adjudicada).*

## D16 · Solicitud de microdato ENCRIGE 2020 al Laboratorio de INEGI

**NC que decide (2):** `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-09`, `NC-260927-GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1-4b11-03`

**Situación.** R03 (pago informal en trámites por empresa) sale hoy por tamaño y por sector, por separado, desde los tabulados de ENCRIGE 2020 (CALC-ALT-R03-ENCRIGE2020-0001). El cruce tamaño × sector y las horas por trámite (est. 3) solo existirían en el microdato ENCRIGE 2020, que INEGI entrega por Laboratorio. R10 (FIRMADA) dejó esa solicitud como opcional y de mesa aparte; exige titular, así que ningún ejecutor la firma ni la tramita. No hay solicitud redactada (g-inegi-lm-enaproce.md:22).

**Opciones.**

- **(a)** Solicitar al Laboratorio de Microdatos de INEGI (procesamiento remoto) el TR_ENCRIGE2020 y el TR_ENCRIGE2020_TRAMITES, con un titular de mesa. Un acto sucesor redacta la solicitud sobre el formato registrado (id inegi_laboratorio_microdatos_solicitud_uso) y registra el acuse. — *Costo:* Trámite con identidad y semanas de espera. La salida queda sujeta a confidencialidad y el acceso es a tabla procesada, no a microdato en el corpus (según FP e7be-01). Nadie ha redactado esta solicitud.
- **(b)** No solicitar. El cruce tamaño × sector y el est. 3 de R03 quedan NO-ACCESIBLE-SIN-LABORATORIO; la NC se cierra con esta firma y se reabre solo si una regla o afirmación adoptada lo exige. — *Costo:* R03 se queda sin el cruce y sin las horas por trámite; hoy sale por tamaño y por sector por separado, rotulada.
- **(c)** Diferir sin fecha: la NC sigue abierta hasta que la demanda (corrida0 demanda) la pida. — *Costo:* Una fila abierta más sin dueño ejecutable.

**Recomendación.** (b) R10 ya descartó el trámite de identidad con el Laboratorio para ENAPROCE por ser costo alto para un dato marginal; R03 ya tiene fuente descriptiva sellada (CALC-ALT-R03-ENCRIGE2020-0001 y -ENVE2024-0001); los encargos salen de la demanda (§1). La opción (b) deja la puerta abierta sin cargar el libro y se deshace con una firma posterior.

**Plazo.** Sin urgencia; próximo corte de mesa (2026-10-05).

**Texto de firma.** «Firmo R03-LM ___ (a: se solicita al Laboratorio de Microdatos de INEGI el TR_ENCRIGE2020/TR_ENCRIGE2020_TRAMITES con titular ___ · b: no se solicita; el cruce tamaño × sector y el est. 3 de R03 quedan NO-ACCESIBLE-SIN-LABORATORIO y NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-09 se cierra con esta firma, reabrible solo si una regla o afirmación adoptada lo exige · c: se difiere sin fecha).»

*Fuente del renglón: investigador (adjudicada).*

## D17 · Legado explícito de RESULT-L8CONV en tramite.yaml

**NC que decide (1):** `NC-0253`

**Situación.** Tres probabilidades de participación electoral (mínimo, máximo y media de p0) que milpa/tramite.yaml lleva tecleadas con clase MEDIDO·Δ tienen un gemelo GEN2 sellado con delta 0.0 contra GEN1 (CALC-L8-CONVERSION-0001), pero de origen HEREDADO: el linaje solo lo admite bajo un uso como DESCRIPTIVO, no como MEDICION-GEN2. Citarlo es adoptar.

**Opciones.**

- **(a)** Citar RESULT-L8CONV-A-P-MINIMO, -MAXIMO y -MEDIA en milpa/tramite.yaml como legado explícito de origen HEREDADO con uso DESCRIPTIVO (linaje APTA-CON-HERENCIA-DECLARADA). — *Costo:* Un acto pequeño (tools/escribe_relevo_consumo.py) cuyo merge es la adopción. No cuenta como MEDICION-GEN2 y no se promete que baje dependencias_numericas_legacy_activas.
- **(b)** Dejarlos sin cita GEN2 y cerrar la NC por decisión de mesa. — *Costo:* Cero trabajo; los tres consumidores siguen con el valor tecleado, sin cadena GEN2 visible aunque el gemelo sellado exista.
- **(c)** CALC nuevo que derive p0 desde las boletas sin pasar por data/l8-resultados-tipo-boleta-v1_0.json (origen NUEVO). — *Costo:* Acto CAJA con dos commits y microdato electoral; es la única vía que habilita MEDICION-GEN2 y baja el contador legacy.

**Recomendación.** (a) Es la propuesta del acto que corrigió el linaje (GEN2-L8-LINAJE-HEREDADO-1) y hace visible la cadena GEN2 sin presentarla como medición nueva; es coherente con FP-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-2-e0db-01, que no consume origen HEREDADO como MEDICION-GEN2. (c) solo si mesa necesita que cuente como MEDICION-GEN2.

**Plazo.** 2026-10-05

**Texto de firma.** NC-0253: opción (a). Cítense RESULT-L8CONV-A-P-MINIMO, RESULT-L8CONV-A-P-MAXIMO y RESULT-L8CONV-A-P-MEDIA (CALC-L8-CONVERSION-0001) en milpa/tramite.yaml para participa_p0_minimo/maximo/media con uso DESCRIPTIVO, como legado explícito de origen HEREDADO; no cuenta como MEDICION-GEN2.

*Fuente del renglón: investigador (adjudicada).*

## D18 · Latinobarómetro 2024: levantar la reserva E.6

**NC que decide (1):** `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-01`

**Situación.** HUM-006 (satisfacción con la democracia, Latinobarómetro 2024 P12STGBS.A) exige la ola 2024, RESERVADA por E.6 (COLA-/CONFIANZA-LATINOBAROMETRO-PISOS-spec) y ya abierta por defecto en #1292, cerrado sin fusionar (mesa eligió retirar y seguir). El cruce está visto: solo puede medirse RETROSPECTIVA. AUTOR-026 no depende de esto: usa la ola 2023, LIBRE y ya sellada.

**Opciones.**

- **(A)** Mesa levanta por escrito la reserva E.6 de Latinobarómetro 2024 solo para HUM-006 (columna P12STGBS.A de México, con guardia de una sola variable congelada en COMMIT-1). GEN2-PISOS-DOMINIOS-Y-REGLAS-2 (CAJA) lo mide rotulado RETROSPECTIVA. — *Costo:* Un acto CAJA. La ola ya se derivó en #1292 antes de cualquier emisión nueva, así que no puede dar marca PROSPECTIVA y no se pierde valor prospectivo adicional en esa columna. Las demás columnas siguen RESERVADAS; POL-030 y TIME-030 (que también citan la ola 2024 en tabla-apertura-mc2) no quedan cubiertas por esta firma.
- **(B)** Mantener la reserva. HUM-006 espera a una ola posterior del Latinobarómetro, con emisión sellada antes de abrirla. — *Costo:* HUMOR sin estimador de forma indefinida: el manifiesto solo trae las olas 2023 y 2024 (4 ids latinobarometro*).
- **(C)** Declarar consumida la ola 2024 para este cruce (E.6) y dejar HUM-006 SIN-CIFRA, sin medir. — *Costo:* Ningún acto, pero HUMOR queda sin estimador y la afirmación sin dictamen.

**Recomendación.** (A. AUTOR-026 se absorbe en GEN2-PISOS-DOMINIOS-Y-REGLAS-2 citando CALC-LATINOBAROMETRO-PISOS-2023-0001 (E.5), sea cual sea la opción.) E.6 permite usar un cruce visto para describir y evaluar en retrospectiva, siempre que se rotule así; el valor prospectivo de esa columna se perdió con el defecto y la guardia de una variable deja reservado el resto de la ola.

**Plazo.** 2026-10-05

**Texto de firma.** «PISOS-DOMINIOS-Y-REGLAS-1 7cd0-01 (Latinobarómetro 2024, HUM-006): opción (__). Si (A): levanto por escrito la reserva E.6 de Latinobarómetro 2024 solo para la columna P12STGBS.A de México, rotulada RETROSPECTIVA, con guardia de una sola variable congelada en el COMMIT-1 de GEN2-PISOS-DOMINIOS-Y-REGLAS-2; el resto de la ola sigue RESERVADO. Si (B): se mantiene la reserva. Si (C): la ola 2024 se declara consumida para este cruce y HUM-006 queda SIN-CIFRA.»

*Fuente del renglón: investigador (adjudicada).*

## D19 · M12, M14, M15, M16 y M17: fecharlos o dejarlos sin fecha (R08 b)

**NC que decide (5):** `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-01`, `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-02`, `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-03`, `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-04`, `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-05`

**Situación.** M12 (CoDi/trámite en línea: ENCIG 2023/2025, ENIF 2021, ENDUTIH 2023/2024) tiene su vía documentada en el mapa (filas 24–29), pero R08 (b) lo dejó sin fecha y su HOLDOUT sigue intacto; la NC espera que mesa decida si se gasta.

**Opciones.**

- **(a)** Mantener «sin fecha» (R08 b) como estado estable: la NC se cierra con esta firma y se reabre solo si una spec o una familia 2027 pide M12. — *Costo:* M12 sigue sin piso GEN2 en el catálogo de momentos.
- **(b)** Fecharlo: encargar los CALC-caja descriptivos de M12 en GEN2-CALC-ALTERNOS-LOTE-2 y gastar su HOLDOUT como piso RETROSPECTIVO (R01 b), con censo previo de familias 2027. — *Costo:* Irreversible: el HOLDOUT de M12 se pierde para siempre (E.6). La fila de ENCIG 2025 sale del árbitro y la de ENIF 2024 m7 (R06) está RESERVADA, así que quedan fuera salvo otra firma.
- **(c)** Convertir M12 en familia 2027 (R01 d), con emisión sellada antes de la ola. — *Costo:* Un expediente por momento y esperar a 2027; a cambio, la prueba sería PROSPECTIVA.

**Recomendación.** (a) Mesa ya eligió «sin fecha» dos veces (R08 b y ADENDA-1). Ningún consumidor pide M12 (0 de 87 corridas de demanda). Conservar el HOLDOUT deja (b) y (c) disponibles, mientras que gastarlo no tiene vuelta. Una NC sin plazo real solo engorda el libro.

**Plazo.** 2026-10-05 (MESA, del campo sucesor de la NC)

**Texto de firma.** «Sobre M12 (NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-01) firmo la opción (__). (a): queda sin fecha por R08 (b), con su vía documentada en canon/mapa-instrumentos-alternos-v1_0.tsv filas 24–29 y HOLDOUT intacto; la NC se cierra con esta firma. (b): se encarga en GEN2-CALC-ALTERNOS-LOTE-2 y su spec declara en COMMIT-1 que consume el HOLDOUT de M12. (c): pasa a expediente de familia 2027.»

*Fuente del renglón: investigador (adjudicada).*

## D20 · Cuarta condición del bin 1 de la regla de adopción en bloque

**NC que decide (1):** `NC-0290`

**Situación.** La regla que adopta relevos GEN1→GEN2 con solo fusionar el PR de un bloque ya falló en su bin 1: GEN2-RELEVO-USOS-1 adoptó 2 de 7 slots NO-MATERIAL porque un sellado o una firma vigente prohibía citar el resto. decisiones.tsv:119 declara que la regla se estrecha con una cuarta condición y la deja a dirección; ningún encargo la redacta ni la sella (0 de 1223 archivos en forense/encargos de origin/main).

**Opciones.**

- **(a)** Sellar la 4ª condición del bin 1: «(iv) ningún sellado ni firma vigente prohíbe la cita del slot, con independencia de su materialidad», con ADR propio (raíz de acto) y fila en data/corrida0/decisiones.tsv. — *Costo:* Un acto NUBE pequeño de redacción y ADR, sin dato. El bin 1 se estrecha: algunos slots pasan a revisión uno por uno (bin 2).
- **(b)** Dejar la regla sin cambio. — *Costo:* Cero hoy. El texto sellado sigue refutado y cada relevo tiene que atrapar a mano la prohibición por firma o sello; ya falló una vez (2 de 7 adoptados).
- **(c)** Diferir el sello hasta que GEN2-RELEVO-CONSUMIDORES-4 traiga un caso concreto. — *Costo:* La fila sigue abierta y ningún bloque nuevo se fusiona con la regla corregida mientras tanto.

**Recomendación.** (a) El defecto ya ocurrió y la propia regla prevé estrecharse ante un caso así (adenda :69; decisiones.tsv:119). La condición ya está redactada y el costo es un acto de redacción sin dato.

**Plazo.** 2026-10-05

**Texto de firma.** NC-0290: opción (a). Sello como cuarta condición del bin 1 de la regla de adopción en bloque: «(iv) ningún sellado ni firma vigente prohíbe la cita del slot, con independencia de su materialidad». Se asienta con ADR propio (GEN2-TRAMITE-REGLA-ADOPCION-BLOQUE-1) y fila en data/corrida0/decisiones.tsv.

*Fuente del renglón: investigador (adjudicada).*

## D21 · ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?

**NC que decide (1):** `NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-07`

**Situación.** ENADID 2023 (11 conductas de hogar/persona sin derivar) y Pew GAS Spring 2025 (6 de migración) figuran 'reservadas por diseño' solo en la nota de PISOS-1: ni una firma ni el manifiesto las reservan, aunque MEMORIA las cubre.

**Opciones.**

- **(A)** Reservarlas por escrito (fila reserva:* en decisiones.tsv + estado_reserva en el manifiesto, en los términos de reserva:envipe2026); la NC sigue en APERTURA hasta un encargo con spec congelada que las consuma. — *Costo:* Una firma y una marca; no se mide nada hoy y los 17 pisos adoptados siguen sin validación prospectiva hasta ese encargo.
- **(B)** Declararlas abiertas (retirar la reserva de diseño de PISOS-1) y validar ya los 17 pisos contra ENADID 2023 y Pew 2025. — *Costo:* Consume el holdout de forma irreversible (D-19), fuera del frente prospectivo de las familias 2027; exige antes un encargo CAJA con spec congelada.
- **(C)** Cerrar la fila sin marcar nada. — *Costo:* Cero trámite, pero las dos olas quedan reservadas solo de palabra: una sesión de caja puede abrirlas sin violar ninguna firma.

**Recomendación.** (A) Es reversible y barato, escribe la reserva donde hoy no está y no consume el holdout hasta que exista una spec congelada; B es irreversible y C deja la decisión tácita.

**Plazo.** Antes del próximo encargo de CAJA que toque enadid2023_* o pew_gas_spring2025; no bloquea nada hoy.

**Texto de firma.** Firmo A: ENADID 2023 (las conductas de GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1 no derivadas) y Pew GAS Spring 2025 quedan RESERVADAS por escrito, en los términos de reserva:envipe2026: bajar y hashear está permitido; abrirlas, derivar de ellas o leer sus tabulados, no, fuera del código congelado de una prueba pre-registrada o de mesa por escrito. El acto que ejecute esta firma escribe estado_reserva en el manifiesto.

*Fuente del renglón: investigador (adjudicada).*

## D22 · Adendas de mesa sin rastro (19–21/sep): archivo retroactivo

**NC que decide (1):** `NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-02`

**Situación.** La firma del 21/sep ordena no archivar retroactivamente las adendas sin rastro, pero NC-…-3d08-02 declara que solo se cierra si mesa aporta el texto de dos (GEN2-CELDA-D-PILOTO-3-P0: 4d4131df, 352c7aed; GEN2-LIMPIEZA-RAMAS-LOCALES-3: 2802e63b, adbdb3c0).

**Opciones.**

- **(a)** Mantener la firma: el texto no se archiva. El hueco queda escrito en forense/notas/2026-09-21-sello-de-cuerpo-y-adendas-sin-rastro.md §3 (ya en main) y NC-…-3d08-02 se cierra por esta decisión de mesa. — *Costo:* Una auditoría futura de PILOTO-3-P0 lee la paráfrasis del ejecutor (nota del paro, ENMIENDA §E.1-E.2) y no el texto literal de mesa; nada de lo que el repo ya tenía se pierde.
- **(b)** Levantar la prohibición solo para las dos adendas de PILOTO-3-P0: mesa pega el texto literal; un trámite lo archiva como forense/encargos/<encargo>-ADENDA-N.md con su .cuerpo.sha256, sellada al recibirse (A.3). LIMPIEZA-RAMAS-LOCALES-3 se cierra como en (a). — *Costo:* Mesa recupera dos textos de su chat del 20/sep y un trámite los archiva; retira parcialmente una firma (D-19). Es la única de las cuatro que gobernó una compuerta de medición (P0 gatea COMMIT-2).
- **(c)** Levantarla para las cuatro adendas: mesa pega los cuatro textos y un trámite los archiva. — *Costo:* El mayor esfuerzo de mesa; dos de las cuatro son de mantenimiento de ramas (sin efecto sobre ninguna cifra).

**Recomendación.** (a) Mesa firmó «no se archivan retroactivamente» con el hueco a la vista. La sustancia de la adenda de PILOTO-3-P0 (reorden P0 -> COMMIT-2 y el procedimiento 3a-3b, reproducible por comando) ya está en la nota del paro; recuperar el texto no cambia ninguna medición ni decisión (§1, D-14).

**Plazo.** 2026-10-05

**Texto de firma.** «NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-02: opción (a). Se mantiene «no se archivan retroactivamente»; el hueco queda escrito en forense/notas/2026-09-21-sello-de-cuerpo-y-adendas-sin-rastro.md §3; se cierra la fila.»

*Fuente del renglón: investigador (adjudicada).*

## D23 · Sidecar del insumo codex que cita un archivo ausente

**NC que decide (1):** `NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-01`

**Situación.** Un insumo externo (rama codex, pisos ENIF 2021 0002) trae un sidecar que nombra mal su archivo; el contenido está íntegro y su SHA256SUMS lo nombra bien. Hay que decidir si alguien lo re-sella o si se acepta como hallazgo permanente.

**Opciones.**

- **(a)** Quien envió la rama codex re-envía el paquete con la cita corregida; entra como insumo nuevo con fecha nueva. — *Costo:* Acción con identidad (pedirlo a Codex/remitente) y un acto NUBE de recepción; ningún número cambia.
- **(b)** Mesa autoriza un sidecar hermano nuevo con el nombre correcto y nota de procedencia; el original no se edita. — *Costo:* Commit NUBE pequeño; el sidecar viejo sigue HUÉRFANO y su excepción en verifica_sidecars.py sigue necesaria.
- **(c)** Aceptar la cita rota como hallazgo permanente: ya la cubren la excepción declarada (verifica_sidecars.py:75-80) y SHA256SUMS.txt, que nombra bien el archivo; la NC se cierra. — *Costo:* Cero trabajo; si alguien borra la excepción del verificador, vuelve el FAIL.

**Recomendación.** (c) El payload está verificado dos veces (sidecar y SUMS, mismo hash 96fd07bc). Editar el sidecar rompería SUMS, que también lo hashea (6aeb26cb). El encargo de origen ordenó «No se toca».

**Plazo.** 2026-10-05

**Texto de firma.** «3d08-01: opción (__). Con (c): la cita rota del sidecar de pisos-enif2021-0002 queda como hallazgo permanente, cubierto por verifica_sidecars.py y por SHA256SUMS.txt; no se re-sella y la NC se cierra.»

*Fuente del renglón: investigador (adjudicada).*

## D24 · Anexo A del lote ENIF 2024 archivado con otro sha256

**NC que decide (1):** `NC-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-04`

**Situación.** El diseño v0.1 del lote ENIF 2024 se archivó con un sha distinto del que declaró el encargo, porque el chat cambió los tabuladores. El lote ya corrió con su spec v1.0 sellada. Falta decidir qué hacer con el testigo original.

**Opciones.**

- **(a)** Mesa aporta el Anexo A original byte a byte (si lo conserva); un acto NUBE lo archiva como hermano con su sha f9ea6d4f; el v0.1 archivado no se toca. — *Costo:* Acción con identidad de mesa (buscar el archivo) más un commit NUBE; no cambia ningún resultado.
- **(b)** Aceptar el v0.1 archivado (bd1dcfd8) como el Anexo A vigente; f9ea6d4f queda VENCIDO EN ALCANCE (ya asentado) y la NC se cierra. — *Costo:* Cero trabajo; se pierde para siempre la verificación byte a byte del texto original del chat.
- **(c)** Rehacer el Anexo A desde las tablas del §4 del encargo. — *Costo:* Trabajo sin consumidor: el lote corrió sobre la spec v1.0 sellada, no sobre el v0.1; un texto rehecho tampoco reproduciría f9ea6d4f.

**Recomendación.** (b (o a, si mesa tiene el original a mano)) Ningún número depende del v0.1: gobierna la spec v1.0 sellada (64bb52f2, verificada) y E.1 dice que manda el agregador que declara la spec sellada. El testigo ya está vencido en alcance, no refutado.

**Plazo.** 2026-10-05

**Texto de firma.** «a98a-04: opción (__). Con (b): el Anexo A vigente es el v0.1 archivado (sha256 bd1dcfd8…); el testigo f9ea6d4f queda VENCIDO EN ALCANCE y la NC se cierra.»

*Fuente del renglón: investigador (adjudicada).*

## D25 · Envoltura por celda de emite_m.py (regla de ola previa estricta)

**NC que decide (1):** `NC-0026`

**Situación.** `tools/emite_m.py` tiene dos funciones puras de «ola previa estricta», probadas y consumidas por el CALC de demostración, pero `emite_celda` no las consume: NC-0026 pide esa envoltura por celda. Su consumidor previsto (C0-D, el marcador por ola) lo sustituyó GEN2-MARCADOR-REDISENO-1, cuya firma (1) deriva el marcador del catálogo y las celdas-D, nunca del emisor. Cablearlas cambiaría la M que el emisor produce hoy y, con ella, las corridas-M. Dos verificadores independientes rechazaron cerrarla por diseño: la firma (5) de MARCADOR-REDISENO-1 cierra otras cuatro NC y omite ésta, y `emite_m` sigue vivo (ADR-520: sigue abierto que la M vigente no modula).

**Opciones.**

- **(a)** No cablear: las dos funciones quedan puras y probadas; NC-0026 se cierra por firma de mesa citando la firma (1) de MARCADOR-REDISENO-1. — *Costo:* Ninguno de código. La M vigente sigue sin modular (ya declarado en ADR-520); si algún día se quiere modular por ola, será un CALC nuevo.
- **(b)** Encargar el cableado de la envoltura a `emite_celda`. — *Costo:* Cambia la M emitida: hay que re-emitir corridas-M y adoptar en bloque (E.2): irreversible en la práctica. Mide sobre olas vistas (regla 6).
- **(c)** Retirar las dos funciones (E.1/regla 6). — *Costo:* Toca código con un consumidor vivo (el CALC de demostración) y sellos asociados; no se puede hacer sin un CALC nuevo.

**Recomendación.** (a) El consumidor que la justificaba ya no existe y la vía prospectiva son las familias 2027; cablearla mediría sobre olas vistas, que la regla 6 no autoriza para retadores.

**Plazo.** 2026-10-05

**Texto de firma.** «NC-0026: opción (a); las dos funciones de ola previa estricta de tools/emite_m.py quedan puras y no se cablean a emite_celda; se cierra citando la firma (1) de GEN2-MARCADOR-REDISENO-1.»

*Fuente del renglón: MANUAL (supervisor).*

## D26 · [COLA] y [ADQ]: ¿categoría exenta o excepción rotulada aparte?

**NC que decide (1):** `NC-0170`

**Situación.** La firma del 16/sep encargó retro-sellar 18 EXCEPCIONES del censo de PR sin `## CONSUMIDO`: los 8 actos GEN2 reales ya están retro-sellados (#759, #795; NC-0227 CERRADA). Falta decidir el estatus de las 10 filas [COLA]/[ADQ] (PR cuyo título es `[COLA] …` o `[ADQ] …`, el mecanismo que entrega encargos): ¿una cuarta categoría exenta, como `censo/*` y `claude/tramite-*`? El censo ya las rotula EXCEPCIÓN-COLA/ADQ aparte, pero `tools/digesto_tramite.py` no las trata (0 coincidencias) y no existe una lista viva de exentos en tools, tests, .github, canon ni gobierno (1047 archivos examinados). Los verificadores rechazaron cerrarla por diseño: la fila pedía una firma entre dos opciones.

**Opciones.**

- **(a)** Mantenerlas como EXCEPCIÓN EXPLÍCITA rotulada aparte, sin tocar canon. — *Costo:* Reversible. Un acto de tubería debe hacer que el digesto lea la etiqueta EXCEPCIÓN-COLA/ADQ (hoy no la lee).
- **(b)** Sumarlas a la lista de exentas por ADR. — *Costo:* Toca canon (regla de exentos) y las saca de todo control futuro: un PR [COLA] mal formado ya no se vería.
- **(c)** Retro-sellar las 10 una por una con `## CONSUMIDO`. — *Costo:* Diez ediciones sobre encargos ya archivados y sellados; choca con A.3 (el cuerpo no se toca) y con la firma ADENDAS.

**Recomendación.** (a) Es la única opción que no toca canon ni sellos y que conserva la visibilidad de los PR del mecanismo de entrega.

**Plazo.** 2026-10-05

**Texto de firma.** «NC-0170: opción (a); [COLA] y [ADQ] no se suman a los exentos, quedan como EXCEPCIÓN-COLA/ADQ rotulada aparte, sin tocar canon.»

*Fuente del renglón: MANUAL (supervisor).*

## D27 · Auto-merge del [deriva] (P4 de GEN2-TUBERIA-3)

**NC que decide (1):** `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01`

**FP existente:** `FP-260928-GEN2-TUBERIA-3-f18c-01` (la decisión ya tiene su ranura; este renglón no acuña otra).

**Situación.** dejar implementada la opción (a), (b) o (c) de FP-260928-GEN2-TUBERIA-3-f18c-01 en .github/workflows/automerge-rutinas.yml — DECISIÓN-DE-MESA-PENDIENTE -- la FP f18c-01 sigue ABIERTA (firmada_en vacío en forense/firmas-pendientes.tsv); fusionar sin revisión humana es regla de mesa (TUBERIA-3 lo intentó y el clasificador de permisos lo negó) y este acto no la rodea

**Opciones.**

- **(FP)** Las que trae la firma pendiente, verbatim: «P4 · el [deriva] no se fusiona solo: (a) automerge-rutinas.yml gana schedule (cada 15 min) que fusiona PR derivados/auto-* con su último SHA verde y con el derivador ya terminado [recomendada; NO implementada: el clasificador de permisos negó «Merge Without Review», la regla es de mesa]; (b) el job derivados espera su último dispatch y fusiona [ocupa runner, choca con el tope de 30 min]; (c) auto-merge nativo del PR si mesa activa «Allow auto-merge» y el check requerido en main. P2 · (d) publicar demanda-corridas.tsv y demanda-resultados.tsv por el canal: EJECUTADA en el PR #1294 (verify.yml, job derivados); su adopción es el merge de mesa y mueve legacy 67→82 y pendientes 158→63 al primer [deriva]; (e) no publicarlas queda descartada si mesa fusiona» — *Costo:* El de cada opción según el texto de la FP.

**Recomendación.** (la que marca la FP) La decisión ya está formulada con sus opciones en `FP-260928-GEN2-TUBERIA-3-f18c-01` (ABIERTA); este renglón la trae para que la hoja sea autónoma y no acuña otra ranura.

**Plazo.** 2026-10-05

**Texto de firma.** «Firmo la opción (__) de FP-260928-GEN2-TUBERIA-3-f18c-01.»

*Fuente del renglón: FP existente (verbatim).*

## D28 · Regla del semáforo del tablero de carriles: SIN-UNION

**NC que decide (1):** `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-02`

**FP existente:** `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (la decisión ya tiene su ranura; este renglón no acuña otra).

**Situación.** cambiar la regla del semáforo (opción b: sacar SIN-UNION de la precedencia y del conteo de stoppers) — DECISIÓN-DE-MESA-PENDIENTE -- §10 del encargo: sin la firma de 5-bis no se cambia la regla y ninguna firma vino verbatim

**Opciones.**

- **(FP)** Las que trae la firma pendiente, verbatim: «§5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, mesa decide). SIN-UNION cuenta como stopper ADQUISICION en 31 de 31 carriles (re-derivado el 29/sep con python3 forense/analisis/tablero-insumos-1/simula_opcion_b.py), 7 carriles son ROJO y en 15 SIN-UNION es la siguiente acción. (a) no tocar la regla: el tablero ordena mal la palanca de cada carril; (b) sacar SIN-UNION de la precedencia y del conteo y mostrarlo aparte [recomendada por dirección]: cambia la siguiente acción de esos 15 carriles (6 → LISTO, 3 → familia 2027, 3 → otro stopper de ADQUISICION, 3 → NC-PARO) y deja a dos carriles ROJO (CARRIL-13, CARRIL-17) con siguiente = LISTO, matiz que el encargo no decía; (c) (b) más un crosswalk núcleo→catálogo (segmento joven, ENUT, ENCUCI) en una spec nueva, como acto propio [sucesor si se elige]. Texto de firma: «Firmo la opción (b) para tools/tablero_carriles.py.»» — *Costo:* El de cada opción según el texto de la FP.

**Recomendación.** (la que marca la FP) La decisión ya está formulada con sus opciones en `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (ABIERTA); este renglón la trae para que la hoja sea autónoma y no acuña otra ranura.

**Plazo.** 2026-10-05

**Texto de firma.** «Firmo la opción (__) de FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01.»

*Fuente del renglón: FP existente (verbatim).*


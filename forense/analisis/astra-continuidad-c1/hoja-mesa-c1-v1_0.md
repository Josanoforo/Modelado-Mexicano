# Hoja para mesa · qué necesita C1 para volver a correr · ACTO GEN2-ASTRA-CONTINUIDAD-C1-1

Fecha: 28/sep/2026 · Dirección resuelve, mesa sella · La asienta FIRMAS-21 · Nada de esta hoja abre dato, adopta cifras ni toca sellos.
Filas FP de esta hoja: `FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01..05` (append en `forense/firmas-pendientes.tsv`, A.12).

## En una frase

C1 (la validación ciega del catálogo) está parada por tres cosas que solo mesa puede destrabar: **quién recalcula sin haber visto los resultados**, **qué contrato firma**, y **qué paquetes se autorizan**. Sin eso, el contador de validaciones independientes no puede subir de forma legítima. Hoy, con la regla del encargo aplicada, **no sube** (ver nota del acto, P1).

---

## §a · Reconstructor sin historial (FP 26a2-02)

**Situación.** [LEÍDO] Transfer de Astra, P3: «la sesión central de Astra ya vio resultados; no sirve de reconstructor ciego. La sesión de Claude que recibe resultados tampoco». [LEÍDO] NC 8c5c-10: el circuito de ceguera v2 no corrió aislado (nube sin bubblewrap; caja falla por NETLINK_ROUTE). [LEÍDO] NC 8c5c-03: broker no provisionado, `CONTEXTO-NUEVO-ACREDITADO=PENDIENTE`. [LEÍDO] NC beee-08: el lote 1 tuvo red acreditada solo por transcript.

| Opción | Qué es | Costo | Qué protege | Qué no protege |
|---|---|---|---|---|
| **A** | Sesión nueva de Claude Code creada solo para esto: prompt + paquete + lista cerrada de herramientas; su transcript se archiva y se audita | Bajo: una sesión por lote; auditoría de transcript por dirección | Que el reconstructor no haya visto resultados (contexto nuevo) | Red y sistema de archivos: si el contenedor ve el repo, puede leer los sellados. La ceguera es por disciplina auditada, no por aislamiento |
| **B** | Pausar C1 hasta que exista el broker v3 (`provision-broker-v3.md`) | Alto en tiempo: C1 no produce nada hasta la provisión | Ceguera por construcción (el reconstructor no alcanza los sellados) | Nada mientras tanto: el contador de validación independiente sigue quieto |

**Recomendación: A, con rótulo propio.** Razón: da validación ya, y la reserva queda declarada en el rótulo (`CIEGA-POR-CONTEXTO-NUEVO`, distinto de `CIEGA-POR-SEPARACIÓN`), igual que beee-01 hizo con el lote 1. B sigue como meta para cuando el broker exista; A no la sustituye.

**Texto de firma.** «Autorizo el reconstructor de opción A para el lote 3 de C1: una sesión nueva de Claude Code, sin historial, con solo el prompt, el paquete y la lista cerrada de herramientas, con el transcript archivado y auditado antes de revelar. Sus resultados llevan el rótulo CIEGA-POR-CONTEXTO-NUEVO y no se presentan como aislamiento de red. El broker v3 sigue como sucesor.»

## §b · Contrato v3 vs v2 (FP 26a2-01; decisiones de `hoja-firma-ejecutor-v3.md`, NC 8c5c-02)

**Qué cambia.** [LEÍDO `catalogo-1-ejecutor-v3/CONTRATO-v3.md` L3, L9, L46–52] v3 se monta sobre el contrato v2 de #1221 (`catalogo-1-aislamiento-v2/`) y los residuales v2 de #1229. Conserva los alias de v2. Lo nuevo: estados por fila con `estado_ic` y `motivo_ic` explícitos; un número es un JSON finito o un decimal estricto (nunca NaN ni booleano); lector JSON que rechaza nombres duplicados; conversión `from_v2` conservadora que rechaza un `RECONSTRUIDO` v2 sin `estado_ic`; el orquestador congela original, derivada, código, contrato y tolerancias con hash **antes** de revelar referencias.

**¿Hay que firmar por SHA?** Sí. Advertencia del transfer de Astra, verbatim: «una firma para v2 no abre v3». Una firma sin hash se hereda a versiones que mesa no leyó.

**Texto de firma (26a2-01).** «Mesa firma CONTRATO-v3.md con sha256 821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb como contrato de estados de C1. Esta firma no acredita contexto nuevo ni autoriza acceso: cualquier C1 real exige además CONTEXTO-NUEVO-ACREDITADO y ACCESO-AUTORIZADO por paquete. Una corrección material se hace en una versión sucesora con sello nuevo.» (Dictamen RECOMENDAR-FIRMAR-CON-CAMBIO, de `forense/analisis/recibo-astra6-3/hoja-para-mesa-recibo-astra6-3.md`.)

## §c · FP abiertas de C1, un renglón cada una

El dictamen es el del recibo que las revisó; el texto de firma completo está en la hoja citada.

| FP | Qué decide | Dictamen del recibo | Dónde está el texto |
|---|---|---|---|
| fb50-01 | Contratos sucesores del lote 2 por identidad | FIRMAR-CON-CAMBIO: recibirlos sin adoptar; firmar por identidad y hash después | `recibo-astra6-2/hoja-para-mesa-recibo-astra6-2.md` L70–77 |
| fb50-02 | Dictámenes ENDIREH 2006/2016 y retiro ENVIPE 2015 | FIRMAR-CON-CAMBIO | misma hoja, L79–86 |
| fb50-03 | Inventario custodial y proyección en dos etapas | FIRMAR-CON-CAMBIO | misma hoja, L88–95 |
| fb50-04 | Tolerancias ENDUTIH/MOCIBA | FIRMAR-TAL-CUAL | misma hoja, L97–104 |
| 157c-01 | Protocolo inferencial para IC reimplementados | FIRMAR-CON-CAMBIO (sin margen de equivalencia todavía) | misma hoja, L106–113 |
| 157c-02 | Transporte de ventana a las 767 identidades; contratos nuevos aparte | FIRMAR-CON-CAMBIO | misma hoja, L115–122 |
| 157c-03 | Publicabilidad con CV .30 y ancho .20 | FIRMAR-TAL-CUAL | misma hoja, L124–131 |
| 157c-04 | Recibo de #1194 | YA-CUBIERTA-POR ADR-260927-GEN2-RECIBO-ASTRA6-2-627e-01 | misma hoja, L133; falta cambiar el estado de la fila, que sigue ABIERTA |
| 39de-01 | Retiro temporal, denominador institucional, elegibilidad nacional 99, sucesores | FIRMAR-CON-CAMBIO (no está cubierta por beee-02) | misma hoja, L151– |
| ee49-01 / ee49-02 | Permiso de nueva lectura ENDIREH 2021 / 2016 | dictaminadas en la misma hoja | misma hoja |
| 1653-01 | Contrato ENBIARE edades/CESD-7 y receta IC sucesora | FIRMAR-CON-CAMBIO: separar (a) y (b), atar a hash | `recibo-astra6-3/hoja-para-mesa-recibo-astra6-3.md` |
| **26a2-04** (nueva) | 126 COINCIDE ENBIARE no ciegas del lote 2 (NC 627e-07; las 4 ENCIG de la NC ya tienen PASA de otra validación) | **Recomendación: re-comparar en el lote 3** con adaptador congelado antes de revelar. Razón: rotularlas no ciegas para siempre pierde 126 validaciones que pueden recuperarse a bajo costo. Texto: «Las 126 COINCIDE de ENBIARE del lote 2 quedan CONCUERDA-NO-APROBADA con rótulo NO-CIEGA-PENDIENTE; se re-comparan en el lote 3 con el adaptador v3 congelado antes de revelar.» | esta hoja |
| **26a2-05** (nueva) | 2 NO-PASA ENIGH2020 remesas bajo tolerancia 0.0 (NC 627e-08) | **Recomendación: dejar el NO-PASA formal** y abrir una spec sucesora con tolerancia de coma flotante. Razón: la tolerancia de una spec sellada no se enmienda hacia atrás; Δ de 1e-12 es redondeo, no desacuerdo. Texto: «Queda el NO-PASA formal de los dos RESULT de remesas ENIGH2020. Autorizo una spec sucesora con tolerancia absoluta 1e-10 para su próxima validación; la spec sellada no se edita.» | esta hoja |

Las cinco FP nuevas de RECIBO-ASTRA6-3 que no son de C1 (3a1f-01, b544-01, b544-02, 310e-01) son de C2/C3 y van en su propia hoja.

## §d · Autorización por paquete para el lote 3 (FP 26a2-03) — sin abrir nada

Cuatro gates por paquete. Los cuatro deben estar en SÍ antes de lanzar ese paquete:

| Gate | Qué exige | Estado hoy | Qué lo pone en SÍ |
|---|---|---|---|
| APTO-TECNICAMENTE | paquete con identidad completa (ventana incluida) y ejecutor v3 que pasa su suite en su runtime fijado | Paquetes `-ventana-v1` listos (#1203); suite v3 NO-VERIFICABLE-AQUÍ (NC 8c5c-01) | correr la suite v3 en la caja y pegar la salida |
| CONTEXTO-NUEVO-ACREDITADO | reconstructor sin historial | PENDIENTE | firma de §a |
| CONTRATO-FIRMADO | contrato v3 firmado por SHA | PENDIENTE | firma de §b (26a2-01) |
| ACCESO-AUTORIZADO | permiso de lectura de la ola y el módulo del paquete | PENDIENTE (ee49-01/02, fb50-03) | firma por paquete |

**Texto de firma (26a2-03).** «La reserva se conserva hasta que haya autorización por paquete y cohorte. El lote 3 de C1 se lanza paquete por paquete, y cada uno solo cuando tenga en SÍ los cuatro gates (APTO-TECNICAMENTE, CONTEXTO-NUEVO-ACREDITADO, CONTRATO-FIRMADO, ACCESO-AUTORIZADO). Esta firma no autoriza ningún paquete concreto.»

**Primer paquete recomendado:** las 767 identidades ENDIREH 2021 con ventana (`-ventana-v1`). Razón: ya están empaquetadas, su spec basta (P3: no son D-15) y son la mayor parte de las 799 que hoy no tienen corroboración.

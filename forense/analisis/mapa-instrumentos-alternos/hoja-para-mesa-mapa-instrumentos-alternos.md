# Hoja para mesa · qué otros instrumentos del corpus responden las 17 incógnitas · GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1

**Contadores movidos: cero.** Este trabajo no mide, no adopta y no abre reservas. Revisa, pregunta por pregunta, qué encuestas que ya tenemos responden cada incógnita y deja las opciones listas para firmar A1, A2, D1 e I1 (FIRMAS-21).

**En una línea.** De 64 pares incógnita × instrumento × ola revisados:

- 2 satisfacen la incógnita (EXISTE-SATISFACE);
- 36 la satisfacen en parte (EXISTE-SATISFACE-PARCIAL);
- 15 existen pero no la satisfacen (EXISTE-NO-SATISFACE);
- 10 no se encontraron en todo el corpus (NO-ENCONTRADO);
- 1 no se puede verificar sin tocar una reserva.

Por incógnita: **11 de 17 tienen al menos una vía parcial dentro del corpus** (una de ellas, M23, completa), 1 (M18, tandas) tiene instrumentos que no bastan y 5 (M09, M10, M11, M20, M21) no tienen nada en el corpus. Esas cinco, más los 11 pares que dependen de conseguir algo afuera (OBTENER/SOLICITUD), van a OBTENCION-EXTERNA-1.

Detalle fila por fila: `canon/mapa-instrumentos-alternos-v1_0.tsv`. Cada fila cita archivo, página y texto literal de la pregunta.

---

## Antes de firmar: dos avisos que valen para varias letras

1. **Calcular estas incógnitas «gasta» su papel de prueba.** En `milpa/catalogo-momentos-v0_1.tsv`, M09 a M23 tienen `rol_calibracion = HOLDOUT`: su valor se reservaba para evaluar el modelo, no para ajustarlo. Cualquier CALC de caja propuesto abajo consume ese papel. Además, la regla 6 de la memoria operativa prohíbe retadores, pilotos y duelos sobre olas ya vistas. Por eso cada CALC propuesto es **descriptivo** y su spec tiene que decir que consume el HOLDOUT. Esa decisión es de mesa, una sola vez para todo el bloque.
2. **Cinco olas tienen el estado de reserva sin decidir y el mapa las necesita.** Ninguna tiene campo `estado_reserva` en el manifiesto, pero por la letra de E.6 («la ola más reciente de un programa con historia nace reservada») podrían estarlo. Mientras mesa no decida, el mapa las trata como no abiertas:

| ola | por qué está en duda | qué la usaría |
|---|---|---|
| ENCRIGE 2020 | es la más reciente; sus tabulados ya los usó #826 | R03 |
| ENVE 2024 | es la más reciente (2020 y 2022 no están en el corpus); F5 la declara EXPUESTA | R03, M22 |
| CSES Módulo 5 | es el módulo más reciente del corpus | M13, M14 |
| ENDUTIH 2025 | es la más reciente | M12 |
| ENIF 2024, módulo 7 (pagos) | hay reservas por módulo vigentes | M12 |

---

## A1 · M05 (evadir normas) y M23 (ahorro solo informal)

**Qué cambió.** La recomendación vigente (a), «HISTÓRICO-SIN-RELEVO porque no hay con qué responder», no se sostiene: OBTENCION-PREVIA-1 ya lo mostró y este mapa lo amplía.
- **M05.** Lo más cercano en el corpus es LAPOP 2021. En el mismo entrevistado pregunta si «se justifica pagar una mordida» (`EXC18`) y qué tan probable es que castiguen a quien construye sin permiso (`PR3DNR`, la «sanción creíble» que pide la regla). Mide actitud, no conducta. ENCIG 2023 y 2025 miden corrupción sufrida al hacer trámites: esa es la pregunta de M01/M02, no la de M05.
- **M23.** ENIF 2024 ya la responde (EXISTE-SATISFACE, pero su papel de prueba ya se consumió). ENSAFI 2023 permite construir la misma definición como contraste (`P6_1_*` informal, `P6_2/P6_3` formal, con diseño muestral).

**Opciones.**
- (a) HISTÓRICO-SIN-RELEVO para las dos, como hoy.
- (b) M05: acotar la pregunta a **actitud** y medirla con LAPOP 2021 (CALC de caja). M23: relevo descriptivo con el resultado sellado de ENIF 2024, rotulado RETROSPECTIVA (ya lo propuso P1), más ENSAFI 2023 como contraste de definición.
- (c) M05 en unidad persona con ENVIPE 2025, el recálculo que propuso P1.

**Recomendación: (b).** Las dos preguntas tienen respuesta dentro del corpus. M05 queda acotada y dicha como actitud; M23 queda descrita, no ajustada.

**Texto de firma listo:** «Firmo A1 (b): M05 se acota a actitud y se encarga CALC-caja sobre LAPOP 2021 (EXC18 × PR3DNR × escolaridad); M23 recibe relevo descriptivo con el RESULT sellado de ENIF 2024, rotulado RETROSPECTIVA, y ENSAFI 2023 como contraste. Ambas specs declaran que consumen HOLDOUT.»

---

## A2 · Momentos 09 a 22 (catorce incógnitas del motor)

**Qué cambió.** La recomendación vigente (b) decía que 13 de 14 necesitan un estudio de campo nuevo. Cruzando con instrumentos que nadie había revisado (ENCUCI, CSES, CIDE-CSES, ENIGH, ENVIPE, ENSAFI, ENCIG, ENIF, ENDUTIH, LAPOP), **8 de las 14 tienen una vía parcial en el corpus**:

| momento | qué hay en el corpus | qué le falta |
|---|---|---|
| M12 · CoDi rechazado vs SPEI adoptado | uso de CoDi en ENIF 2021/2024 y ENDUTIH 2023–2025; trámites y pagos en línea en ENCIG | nadie pregunta por riesgo fiscal percibido |
| M13 · peso del acto y participación | **CIDE-CSES 2015 (elección intermedia)**: votó (`p3`), «importa qué partido gobierna» (`p17`) y «el voto hace diferencia» (`p18`), por estado | la lista oficial de estados con elección local el mismo día en 2015 (calendario INE) |
| M14 · pensión y voto | ENIGH 2018/2020/2022: recibe la pensión (`P044`/`P104`) y edad → primera etapa; CSES 2018 y LAPOP: voto y edad | voto y pensión en la misma encuesta |
| M15 · agravio urbano → protesta | ENCUCI 2020: protesta y bloqueo por urbano/rural | el agravio; la unidad es persona, no caso |
| M16 · vacío rural → autodefensa | ENVIPE 2025: acciones con vecinos y armas en el hogar; LAPOP 2023 (reservada): acudiría a autodefensas | autodefensa organizada y el agravio |
| M17 · comités sin sanción | ENCUCI 2020: organización vecinal y trabajo comunitario | monitoreo, sanción y persistencia de dos años |
| M19 · confianza en desconocidos | ENCUCI 2020: confianza en «la mayoría de las personas» frente a «las que conoce» | disposición a transar; antes hay que cerrar conf.06 (cifras de ENCUCI en conflicto) |
| M22 · miedo y no denuncia | ENVIPE 2025: no denunció por miedo al agresor (`BP1_23`), por entidad | fecha y alcance de la protección efectiva a testigos |

- M18 (tandas entre desconocidos): ENSAFI 2023 y ENNViH 2002/2005/2009 miden si la persona participa, pero no con quién ni si alguien le quedó mal.
- M09, M10, M11, M20 y M21: NO-ENCONTRADO en todo el corpus (índice de 314 256 reactivos, más ENCUCI, ENCRIGE y ENVE completos). Son estudios de campo o datos de empresas privadas.

**Opciones.**
- (a) Encargar un CALC descriptivo de caja por cada uno de los 8 momentos con vía parcial (consume su HOLDOUT, aviso 1). Los otros 6 pasan a OBTENCION-EXTERNA-1 y a «estudio nuevo».
- (b) Lo mismo que (a), pero solo para los tres donde la vía es más directa: **M13** (CIDE-CSES 2015), **M22** (ENVIPE 2025) y **M19** (ENCUCI 2020, después de conf.06). Los otros cinco con vía parcial quedan documentados en el mapa y sin fecha.
- (c) La recomendación anterior (13 de 14 a estudio nuevo). **Ya no se sostiene con lo verificado.**

**Recomendación: (b).** Concentra el costo donde el corpus casi responde la pregunta tal como la regla la escribe. Deja constancia de los demás sin gastar su papel de prueba todavía.

**Texto de firma listo:** «Firmo A2 (b): se encargan CALC-caja descriptivos para M13 (CIDE-CSES 2015 con clasificador de concurrencia del calendario INE), M22 (ENVIPE 2025, no denuncia por miedo por entidad) y M19 (ENCUCI 2020, tras reconciliar conf.06). Cada spec declara que consume el HOLDOUT de su momento. M12, M14, M15, M16 y M17 quedan con su vía documentada en canon/mapa-instrumentos-alternos-v1_0.tsv, sin fecha. M09, M10, M11, M18, M20 y M21 pasan a OBTENCION-EXTERNA-1.»

---

## D1 · Reserva de ENCRIGE 2016 (dentro de los cuatro «programas descontinuados»)

**Qué cambió, solo para ENCRIGE.**
- ENCRIGE **no está descontinuada**: el catálogo de microdatos de INEGI (RNM) lista 2016 y 2020, y 2020 ya está en el corpus.
- La ola 2016 está guardada **a propósito**: el panel F5 (familia R08) dice «La ola 2016 no se toca ni en documentación hasta la fase confirmatoria». Por eso este acto no leyó su cuestionario.
- ENCRIGE 2020 no tiene campo de reserva, aunque por la letra de E.6 sería la ola que se reserva; sus tabulados ya los usó #826.

**Opciones para ENCRIGE.**
- (a) Mantener la preservación de 2016 (F5 R08) y declarar ENCRIGE 2020 abierta (ya se vio).
- (b) Levantar la reserva de 2016 junto con las otras tres, como propone la hoja D1 vigente. Esto rompe el plan de R08.

**Recomendación: (a) para ENCRIGE.** Las otras tres (CAAS, ENG, MIGRACIÓN) siguen como las dejó la hoja D1; este acto no las revisó.

**Texto de firma listo:** «Firmo D1 para ENCRIGE (a): ENCRIGE 2016 conserva la preservación de F5 R08; ENCRIGE 2020 se declara ABIERTA. CAAS, ENG y MIGRACIÓN siguen la opción que mesa firme en D1.»

---

## I1 · R03 (carga regulatoria y mordida en la MIPYME, ENAPROCE)

**Qué cambió.**
- La mordida en la empresa **sí se mide en el corpus**, pero no en ENAPROCE:
  - ENCRIGE 2020: experiencia en trámites (`P9_3`) y «otra empresa lo vivió» (`P9_2`);
  - ENVE 2024: `P6_1..P6_4`;
  - World Bank Enterprise Survey 2023: `j5`, `j7a` y otros, con microdato en el corpus.
- Detalle en `propuesta-R03.md`.
- La firma F-19 de mesa (15/sep) ya decidió que una encuesta de empresas no se traslada a la regla de personas. Por eso R02 (WBES) y R08 (ENCRIGE) quedaron como familias **descriptivas**. R03 cae en el mismo caso.

**Opciones.**
- (a) Designar titular para el Laboratorio de INEGI por ENAPROCE; solo serviría para la carga regulatoria.
- (b) Cerrar ENAPROCE como NO-ACCESIBLE.
- (d, nueva) (b), más fundir R03 con R08 como familia descriptiva: ENCRIGE 2020, con ENVE 2024 y WBES 2023 de apoyo. Lo publicado ya lo sacó #826; el cruce carga × corrupción requiere microdato de ENCRIGE (solicitud a INEGI).

**Recomendación: (d).** No abre trámite de identidad por ENAPROCE, la pregunta de mordida queda respondida en unidad empresa y respeta F-19.

**Texto de firma listo:** «Firmo I1 (d): ENAPROCE queda NO-ACCESIBLE para R03; R03 se funde con R08 como familia descriptiva UNIDAD-DISTINTA-NO-TRANSFERENCIA sobre ENCRIGE 2020 (ENVE 2024 y WBES 2023 de apoyo), según forense/analisis/mapa-instrumentos-alternos/propuesta-R03.md. La solicitud de microdato ENCRIGE 2020 al Laboratorio es opcional y la decide mesa aparte.»

---

## Llaves de CALC candidatos para caja

Se citan por llave (D-24). Ninguno está congelado; cada uno necesita spec y COMMIT-1 antes de abrir dato.

| llave propuesta | instrumento (en el corpus) | estimando | antes de congelar |
|---|---|---|---|
| `CALC-CIV-PESO-ACTO-CIDECSES2015-CONCURRENCIA` | CIDE-CSES 2015 poselectoral (+ preelectoral `dominio2`) | participación declarada y `p17`/`p18` por concurrencia local, por estado | clasificador de concurrencia (calendario INE); HOLDOUT M13 |
| `CALC-CIV-NODENUNCIA-MIEDO-ENVIPE2025-ENTIDAD` | ENVIPE 2025 | proporción de delitos no denunciados por miedo (`BP1_23` ∈ {01,02}) por entidad, unidad delito | HOLDOUT M22; fechas de protección (externo) |
| `CALC-CIV-CONFIANZA-PUENTE-ENCUCI2020` | ENCUCI 2020 | diferencia `AP5_1_2 − AP5_1_1` por confianza en policía y DOMINIO | reconciliar conf.06; HOLDOUT M19 |
| `CALC-TRA-EVADE-NORMA-ACTITUD-LAPOP2021` | LAPOP 2021 | `EXC18` condicional a `PR3DNR`, por escolaridad (actitud) | firma A1 (b) |
| `CALC-DIN-AHORRO-SOLO-INFORMAL-ENSAFI2023-CONTRASTE` | ENSAFI 2023 | informal ∧ ¬formal, persona, `FAC_ELE` con diseño | firma A1 (b); rotular RETROSPECTIVA |
| `CALC-CIV-PENSION-PRIMERA-ETAPA-ENIGH` | ENIGH 2018/2020/2022 | recepción `P044`/`P104` por edad en el umbral | HOLDOUT M14; firma A2 |
| `CALC-TRA-GOBDIGITAL-ENCIG` · `CALC-DIN-CODI-ENDUTIH2023-2024` | ENCIG 2023/2025 · ENDUTIH 2023/2024 | trámite o pago en línea; uso de CoDi entre quienes pagan por internet | HOLDOUT M12; firma A2 |

---

## Módulo de auditoría (v2.16) · qué se afirma aquí sobre México

- **Contadores:** cero.
- **Procedencia:** todas las filas son (a), dato primario en México. WBES y LAPOP son proyectos internacionales con muestra mexicana: siguen siendo (a). No hay (b) ni (c).
- **Cifras propias:** ninguna. Los tamaños de muestra citados (ENCRIGE 34 919 empresas de diseño; CSES México 2018, 1 239) vienen de la documentación, no de las bases. Nada es PROSPECTIVO; lo que se describa con ENIF 2024 sería RETROSPECTIVA.
- **Unidades que no se mezclan:**
  - persona: ENCIG, ENCUCI, LAPOP, CSES, ENSAFI, ENIF, ENDUTIH;
  - hogar: ENVIPE 4.11, ENIGH ingresos por persona dentro del hogar;
  - delito: ENVIPE `BP1_23`, ENVE módulo;
  - empresa: ENCRIGE;
  - establecimiento: ENVE, WBES.

  Ningún CALC propuesto promedia unidades distintas.
- **Riesgo de lectura simplista:**
  - «Justificar la mordida» (M05) es actitud, no conducta.
  - Participar en una tanda no dice nada de confiar en desconocidos (M18).
  - Protestar (persona) no es un «caso» de respuesta a un agravio (M15).
  - La acción colectiva vecinal contra la delincuencia no es autodefensa (M16).
- **Sesgo urbano:** ENCIG solo cubre localidades de 100 mil habitantes o más, así que no sirve para lo rural. Para M15, M16 y M17 conviene preferir ENCUCI (con dominio rural) y ENVIPE (con tamaño de localidad).
- **Afirmaciones sobre el corpus escritas a mano:** ninguna sin comando. Universo por id: `universo-por-instrumento.tsv`; acceso: `acceso-rnm.tsv`; verbatim verificado por script, con control positivo (`lotes/AUDITORIA-LOTES.md`).

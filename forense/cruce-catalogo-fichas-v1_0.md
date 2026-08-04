# Cruce catálogo × fichas — v1.0

**Clase: propuesta. No es decisión y no autoriza ninguna medición.**

> **LÍMITE DURO.** Ninguna celda de esta tabla afirma que una variable exista.
> Afirma que un instrumento cubre un dominio. La viabilidad real solo se
> confirma abriendo el instrumento, y eso va después del pre-registro.

Reconstruido —no copiado— el 4/ago/2026, contra el estado de hoy del repo:
`data/catalogo-fuentes-v1_0.md` (119 fuentes, dedup) y
`forense/hitoD-preregistro-v2_0.md` (27 fichas, R1.1–R10.3 + R3.1/R3.2/R3.4).
El insumo `cruce-catalogo-fichas-2026-07-30.md` del espejo (tipo 2) se usó
como hipótesis a re-derivar, nunca como cifra a copiar. Donde sus números no
coinciden con los de aquí, la discrepancia se reporta en §4.

Sesión Nube, sin red, sin instrumento abierto. Toda afirmación de "candidata"
es del tipo **cubre el dominio — sin verificar a nivel de variable**, nunca
"la variable existe".

---

## §1 · Recetas — comando a la vista

```
grep -cE "^## R[0-9]" forense/hitoD-preregistro-v2_0.md
```
→ **27**. La receta ingenua `grep -c "^## R"` da **28**: cuenta también
`## Registro de veredictos archivados`. Verificado en esta sesión — no se
reusa la cifra del espejo (25), que es de una versión anterior del
pre-registro con menos fichas.

**Criterio de "declara fuente"**, fijado antes de contar: una ficha declara
fuente si su falsador, Umbral, o alguna de sus columnas A–D **nombra un
instrumento identificable** (acrónimo o nombre propio de encuesta/registro
administrativo) como la vía prevista o ya usada para probarla. No cuenta
mencionar en abstracto "un panel" o "una intervención" sin nombrar el
instrumento — eso se trata como *no declara*.

Con ese criterio, contadas a mano sobre las 27 (comando de verificación:
`grep -nE "ENIGH|ENVIPE|ENCIG|ENUT|ENSANUT|CONSAR|ENIF|ENDUTIH|Banxico|ENCUCI"
forense/hitoD-preregistro-v2_0.md`, filtrado a apariciones dentro del cuerpo
de una ficha, no de una nota fechada que revisa otra):

- **Declaran fuente: 9** — R1.2 (CONSAR/ENIF), R3.1 (ENCIG), R3.2 (ENCIG),
  R3.4 (Banxico/SPEI-CoDi, respaldo ENIF/ENDUTIH), R4.2 (ENSANUT), R5.1
  (ENIGH), R5.2 (ENUT), R7.2 (ENVIPE), R8.3 (ENCUCI, vía conf.06).
- **No declaran: 18** — el resto.

Este **9/18** no es el **15/10** del espejo. No se ajusta: el espejo contaba
sobre 25 fichas con un criterio que su propio documento no escribe. Aquí el
criterio queda escrito arriba y el denominador es 27. Ambas cifras son
correctas para lo que cada una mide; no son la misma pregunta.

---

## §2 · Sellado del cruce original — fichas SIN fuente declarada (18)

Pregunta: ¿el catálogo trae algo que cubra el dominio de esta ficha, sin
verificar a nivel de variable? Dominios tomados de los 10 inventarios
(`data/inventarios/README-inventarios.md`): FIN, MIG, TEC, CAP, CUL, SAL,
SEG, TRA, EST (trámites), TIE (uso del tiempo). **No hay un dominio
"electoral/cívico-participación" entre los 10** — hallazgo que se declara
antes de la tabla, no después: donde el falsador es electoral, no puede
haber candidata por diseño del inventario, no por ausencia de búsqueda.

| Ficha | Dominio del falsador | ¿Candidata en catálogo? | Candidata(s) | Nota |
|---|---|---|---|---|
| R1.1 | FIN (fondos de aseguramiento agrícola) | Parcial | ENIF, ENIGH | Cubren FIN general; ninguna cataloga productores de temporal/fondos de aseguramiento específicamente — el hueco que la propia ficha declara (D probable) es de padrón, no solo de encuesta general |
| R1.3 | FIN, TEC (canal de adopción fintech) | Parcial | ENIF, ENDUTIH | Miden adopción/uso, no "canal de alta" desagregado — dato propietario de la fintech sigue siendo el hueco real |
| R1.4 | FIN/consumo, CUL | No | — | Ninguna fuente del catálogo trae panel de consumo D/E con marca — confirma el D probable pre-registrado |
| R2.1 | TRA (organizacional) | No | — | Tasa de disenso ascendente por tipo de organización es dato propietario; ninguna encuesta pública del catálogo lo cubre |
| R2.2 | TRA (clima organizacional) | No | — | Mismo hueco que R2.1 |
| R4.1 | SAL | Sí | ENSANUT, ENIGH (SAL) | ENSANUT cubre acceso y uso de servicios de salud; **candidata pública real**, sin verificar si trae medición de "trato" (el confusor que la propia ficha marca CONFUNDIDO) |
| R4.3 | SAL | Parcial | ENSANUT | Adherencia por surtimiento (no auto-reporte) es el hueco — ENSANUT es candidata de dominio, no se sabe si mide surtimiento |
| R7.1 | cívico-electoral | **No** | — | Dominio no inventariado. Coincide con el `C`/`D` de la propia ficha (hueco de granularidad municipal) |
| R7.3 | cívico-electoral | **No** | — | Mismo hueco estructural que R7.1 — el RDD que pide no puede nacer de estos 10 inventarios |
| R7.4/R7.5 | cívico-electoral/conflicto | **No** | — | Mismo hueco. Consistente con el D "probable" ya pre-registrado |
| R8.1 | CAP | Sí | ENCUCI, ENVIPE, ENSU | Miden capital social/participación comunitaria; ninguna cataloga comités específicos con/sin sanción — candidata de dominio únicamente |
| R8.2 | FIN, CAP | Parcial | ENIF (participación en tandas) | ENIF pregunta ahorro informal/tandas pero no diferencia tandas digitales de tradicionales — el hueco de plataforma persiste |
| R9.1 | SAL | Sí | ENSANUT | Igual que R4.1 — la propia ficha ya nota la simetría con R4.1 |
| R9.2 | SAL | Sí | ENSANUT | Cobertura de vacunación/servicio — candidata directa de dominio; el requisito "auditada, no autorreportada" es lo no verificado |
| R10.1 | CUL (comunicación) | No | — | Ningún inventario cataloga actos de habla/estilo comunicativo; el ancla sigue siendo el estudio académico (Félix-Brasdefer), no una encuesta del catálogo |
| R10.2 | TRA (organizacional) | No | — | Mismo hueco que R2.1/R2.2 |
| R10.3 | SEG | Parcial | ENVIPE, ENSU | Miden percepción de seguridad/confianza en autoridad, no disposición a testificar bajo protección — y la propia ficha prefiere D por riesgo ético, no solo por dato |

**Cifra re-derivada:** de las 18 fichas sin fuente declarada, **8 tienen
candidata de dominio real** (R4.1, R4.3, R8.1, R8.2, R9.1, R9.2, R10.3 —
parcial/sí — más ninguna adicional), **4 no tienen ninguna posible por
diseño del inventario** (R7.1, R7.3, R7.4/R7.5, agrupadas: 3 fichas), y el
resto queda sin candidata verificable en este barrido. Esto **no coincide**
con el "11 de 15" del espejo — denominador distinto (18, no 15) y criterio
de candidata más estricto aquí (exige nombrar el instrumento, no solo "hay
algo del dominio"). Se reporta como discrepancia, no se reconcilia.

---

## §3 · El complemento — fichas CON fuente declarada (9)

Pregunta invertida: no "¿hay alguna fuente?" sino "¿es la mejor que
tenemos, y qué otras candidatas del catálogo no consideró el falsador?"
"Mejor" se argumenta contra el umbral concreto de cada ficha, no en
abstracto.

| Ficha | Fuente declarada | Candidatas en el catálogo no consideradas | ¿Alguna es mejor para ESTE umbral, y por qué? |
|---|---|---|---|
| **R5.1** | ENIGH (corte transversal repetido; también citada como límite en la propia ficha, columna D) | **ENASEM/MHAS** (panel, 50+, olas 2018 y 2021 — flanquean la reforma de la Pensión del Bienestar de 2019); ENNViH/MxFLS (panel, 3 olas 2002–2012) | **Ver caso de prueba abajo.** ENASEM sí es mejor *si* el falsador exige panel con corresidencia observada en las mismas unidades — que es literalmente lo que dice la columna C de la ficha (`forense/hitoD-preregistro-v2_0.md:149`). ENNViH **no** sirve para R5.1: sus olas terminan en 2012, siete años antes del choque de 2019 — no hay "después" que observar. Nota aparte: `forense/hitoD-preregistro-v2_0.md:890` (Nota 16, 4/ago/2026) ya corrió el falsador con ENIGH transversal repetida y propone fila `A`, señalando explícitamente que el Umbral de la ficha (línea 143) "pide literalmente la comparación transversal", no panel — es decir, la columna C de la propia ficha pudo estar sobre-especificada respecto a su propio Umbral. Eso no invalida a ENASEM como candidata **mejor para una prueba de panel genuina**; sostiene que la ficha admite dos diseños válidos y el catálogo no se había cruzado contra ninguno de los dos hasta ahora. |
| **R5.2** | ENUT (corte transversal) | ENNViH/MxFLS (panel; trae módulos de composición del hogar y ocupación, `TB`/`CRH`, según `hitoD-preregistro-v2_0.md:517`); ENOE (panel rotativo corto, transiciones de empleo) | **Sin verificar a nivel de variable — se reporta como candidata, no como hallazgo.** El umbral de R5.2 pide observar el mismo individuo antes/después de pasar a empleo formal de tiempo completo: eso es un diseño de panel, y ENUT es transversal. ENNViH cubre TRA y tiene estructura de panel, pero no está verificado aquí si trae horas de cuidado (el módulo de uso del tiempo específico); ENOE tiene panel de transición laboral pero no mide horas de cuidado en absoluto. Ninguna de las dos se puede llamar "mejor" sin abrir el cuestionario — se deja como candidata pendiente, no como sustitución. |
| **R1.2** | CONSAR/ENIF | ENIGH (FIN); ENASEM (FIN, 50+) | El umbral es transversal (`<15% hacen aportación voluntaria`), no pre/post — así que un panel no es "mejor", es distinto, y no aplica aquí la ventaja de ENASEM que sí aplica en R5.1. ENIGH podría triangular gasto en aportaciones/seguros como cruce, pero CONSAR ya es fuente administrativa directa de aportación voluntaria — más autorizada que cualquier encuesta para esa variable puntual. No se identifica candidata mejor. |
| **R4.2** | ENSANUT | ENIGH (SAL); ENASEM (SAL, pero restringida a 50+) | ENASEM queda descartada por edad: R4.2 habla de hombres trabajadores en general, no población 50+. ENIGH no es encuesta de conducta de salud. ENSANUT sigue siendo la candidata correcta de dominio; no se identifica una mejor. |
| **R7.2** | ENVIPE | ENDIREH, ENCIG, ENCUCI, ENSU (todas con dominio SEG) | Ninguna cruza cobertura de seguro con tipo de delito — es exactamente el eje que ENVIPE tampoco cruza, y por eso la ficha ya archivó veredicto **D** (`hitoD-preregistro-v2_0.md:693`, verificado empíricamente: `BP2_1` solo existe para robo de vehículo, 1,028/40,280 filas). El veredicto ya se obtuvo abriendo el instrumento — este acto no reabre nada, solo confirma que ninguna candidata alternativa del catálogo resuelve el hueco que causó el D. |
| **R8.3** | ENCUCI (vía conflicto conf.06) | LAPOP, Latinobarómetro (ambas CUL/CAP, confianza interpersonal) | El bloqueo declarado de la ficha no es falta de fuente — es que **cinco cifras de confianza interpersonal circulan y no se reconcilian** (`conf.06`). LAPOP y Latinobarómetro añadirían una sexta cifra sin resolver el conflicto; no son "mejores", son más del mismo problema. La ficha lo dice explícito: "el falsador exige medición propia o una fuente nueva reconciliada" — ninguna candidata del catálogo reconcilia por sí sola. |
| **R3.1** | ENCIG 2023 | ninguna otra fuente del catálogo cubre trámites/EST con la granularidad de discrecionalidad que pide la ficha | Ya verificado por apertura directa del instrumento (no en este acto): techo de 13.38% de incidencia presencial, veredicto pendiente de adjudicación pero con dato ya corrido. No hay candidata alternativa útil. |
| **R3.2** | ENCIG 2023 | ídem R3.1 | Veredicto **B** ya archivado (`hitoD-preregistro-v2_0.md:901`). No aplica cruce — ya se abrió el instrumento y se resolvió. |
| **R3.4** | Banxico (series SPEI/CoDi, no es un instrumento del catálogo de encuestas) + respaldo ENIF/ENDUTIH | — | La propia ficha ya declara y descarta ENIF/ENDUTIH como respaldo (`hitoD-preregistro-v2_0.md:829-840`) — no hay candidata "no considerada"; el catálogo no aporta nada nuevo aquí. |

### Caso de prueba — por qué R5.1 tenía que marcarse

R5.1 declara ENIGH. Su columna C (`hitoD-preregistro-v2_0.md:149`) dice
textualmente: *"exigiría panel de hogares pre/post con corresidencia
observada"*. El catálogo (`data/catalogo-fuentes-v1_0.md:41`) trae ENASEM
— panel, 5 dominios (FIN MIG SAL TRA TIE), población 50+, con olas
documentadas que flanquean la reforma de 2019 de la Pensión del Bienestar.
Si el procedimiento de este documento no marcara esa fila, el procedimiento
estaría mal, no el resultado — así que se marca, arriba.

**Sobre la premisa de este encargo** (§0 del encargo): afirma que "mesa #19
adjudicó A [para R5.1] afirmando que ningún panel existía". Verificado
contra el estado del repo a la fecha de este acto: el **Registro de
veredictos archivados** de `hitoD-preregistro-v2_0.md` (única sección que
un test puede leer para el conteo real, por ADR-40) contiene tres líneas —
`R1.1 → D`, `R3.2 → B`, `R7.2 → D` — y **no contiene una línea para
`R5.1`**. Lo que sí existe es la Nota 16 (línea 876), fechada 4/ago/2026,
que **propone** fila `A` sobre ENIGH transversal repetida y dice
explícitamente: *"El veredicto archivado... y el contador... no cambian
por esta nota... esta nota propone, no emite."* No se encontró, en este
repo, evidencia de que R5.1 haya sido adjudicada. Se reporta la
discrepancia entre la premisa del encargo y el estado verificado del repo;
no se resuelve aquí — adjudicar es acto de mesa aparte (§4 de este
encargo) y no corresponde a este documento.

### Caso de control — por qué ENNViH NO sirve para R5.1

ENNViH/MxFLS ya está declarada como fuente en el pre-registro
(`hitoD-preregistro-v2_0.md:484`, ficha `CAL-G3`, para `G3 →
horizonte_temporal`), descrita ahí mismo como panel longitudinal de tres
olas 2002, 2005-06, 2009-12. Es panel real, en disco, verificado. Pero sus
olas **terminan en 2012** — siete años antes del choque exógeno que R5.1
necesita observar (universalización de la Pensión del Bienestar, 2019). No
hay "después" que ENNViH pueda medir para este falsador específico: un
panel que no cubre la ventana temporal del choque no es candidato, sin
importar cuán bueno sea su diseño. Donde sí podría servir es en reglas de
§3.5 y §3.1 que no dependen de ese choque de 2019 — es exactamente la
fuente que `CAL-G3` ya usa para `G3`, y quedó señalada como candidata para
R1.2 (afore/seguro) y R5.1-adyacente en `hitoD-preregistro-v2_0.md:517`,
con la advertencia explícita de que cualquier hallazgo colateral sobre esas
reglas "NO cuenta para sus fichas" sin abrir sus propias fuentes y
umbrales.

---

## §4 · Discrepancias con el insumo del espejo (tipo 2, re-derivado)

| Cifra del espejo | Cifra re-derivada aquí | Razón de la diferencia |
|---|---|---|
| 25 fichas totales | **27** | El pre-registro creció entre el 30/jul (25) y hoy (27): `R3.1` y `R3.4` se agregaron por Notas 1-2, `R3.2` ya estaba. Denominador distinto, no error. |
| 15/10 (declara/no declara fuente) | **9/18** | Denominador distinto (27 vs. 25) y criterio explícito aquí (nombrar el instrumento), no reconstruible del documento del espejo, que no escribió su criterio. |
| 11 de 15 sin fuente sí tienen candidata | **8 de 18** (parcial/sí), 3 sin candidata posible por diseño del inventario | Mismo problema de denominador; además esta tabla distingue "candidata de dominio" de "candidata verificada a nivel de variable" con más disciplina que la cifra citada del espejo, que no declara su propio criterio de candidata. |
| ~21 de 27 perímetro falsable (estimado, §6 del encargo) | No re-derivado en este acto | Esa cifra es aritmética sobre inferencias de cobertura, no un conteo de este documento — corresponde a un acto de mesa que decida qué candidatas de §2/§3 se promueven a instrumento abierto. Este documento no la produce ni la ratifica. |

---

## §5 · Lo que este documento no hace

No edita ninguna ficha del pre-registro (sellado). No adjudica ni retira
ningún veredicto — R5.1 sigue sin adjudicar, con o sin la Nota 16. No
descarga ninguna fuente; ninguna candidata mencionada aquí pasó de
"aparece en el catálogo" a "se abrió". No escribe un test — este cruce se
corre a mano, cuando alguien lo decide, y así queda documentado.

# Catálogo unificado de fuentes de datos — v2.0

> | | |
> |---|---|
> | **ARCHIVO** | `catalogo-fuentes-v2.0.md` |
> | **REEMPLAZA A** | `catalogo-fuentes-v1_0.md` — **borrar** |
> | **VERIFICAS ASÍ** | corre `python3 tests/catalogo.py && python3 tests/dedup.py` desde la raíz del repo; la cifra "Inventarios leídos" debe dar **11**, no 10; `SIN_RESOLVER` debe imprimirse primero (ver §"Corrección de identidad" — hoy da 4, y esos 4 son deliberados, no un defecto pendiente); y "RECETA: consistente" debe imprimirse antes de creer cualquier otra cifra |
> | **NOMBRE ESTABLE** | **`catalogo-fuentes`** |

**Qué cambia respecto a v1.0, y por qué es cambio de MAYOR, no de menor (ADR-36):** v1.0 se
construyó enteramente sobre 10 inventarios de encuestas. Encargo AA, mesa #19, 4/ago/2026,
encontró que esa base excluía por diseño una dimensión entera — **clase de fuente** — que es
donde viven acceso, abasto, cobertura verificada y padrones (registro administrativo, padrón de
programa, transparencia/sociedad civil, regulador o sectorial no-INEGI, encuesta institucional
no de hogares, internacional con dato de México). Detalle del defecto y su procedencia:
`forense/notas/2026-08-04-aa-taxonomia-clase-fuente.md`. Esto es cambio de **alcance** del
catálogo, no solo de contenido — de ahí v2.0, no v1.1.

**Este archivo sigue siendo derivado. No se edita a mano la sección "Cifras derivadas".** Se
regenera con:

```
python3 tests/catalogo.py && python3 tests/dedup.py
```

Insumo: los **11** inventarios de `data/inventarios/` — los 10 originales (30/jul/2026) más
`inventario_fuentes_clase-fuente-mexico.md` (4/ago/2026, Encargo AA).

**Verificación de receta**, igual que en v1.0: `catalogo.py` imprime, antes de cualquier cifra,
la comparación entre lo que parsea y el conteo crudo de encabezados numerados de cada archivo.
Corrida en este acto: **`RECETA: consistente`** para los 11 archivos, incluido el nuevo.

**Nota de lectura, heredada de v1.0:** las cifras de este archivo salen de `dedup.py`
(agrupa por acrónimo *y* nombre normalizado), no de `catalogo.py` (conteos intermedios sin
deduplicar).

**Corrección de identidad, ENCARGO MAP-1 (2026-08-06):** entre 4/ago y 6/ago, `acron()` —
la función que ambos scripts usan para derivar el acrónimo/identidad de cada título — producía
identidades falsas: fragmentos truncados a 30 caracteres, y hasta tres identidades distintas
para la misma fuente real (CPV, ENNVIH, LAPOP, ENADID y 15 más, encontradas por lectura
sistemática de los 11 inventarios, no solo los 4 casos que se sospechaban). Las cifras "v2.0"
de la tabla de abajo ya están corregidas contra `data/inventarios/alias-fuentes.yaml` (tabla de
identidad canónica, nueva). Detalle completo, incluidas las 2 identidades que se dejaron
deliberadamente sin resolver por ser ambiguas (el mismo string truncado lo produce más de una
fuente real distinta — no se adivinó cuál): `forense/notas/2026-08-06-map1-lector.md`.

---

## Cifras derivadas (11 inventarios)

**Cifras vigentes al 2026-08-06 (post-MAP-1); se re-derivan con:
`python3 tests/catalogo.py && python3 tests/dedup.py`.** (Esta tabla es anterior
al cruce contra `data/manifiesto.yaml` -- ese cálculo, qué de esto ya está en
disco, vive aparte en `python3 tests/cruce_operables.py`, encadenado tras los
comandos de arriba; se congela esta tabla con el mismo criterio de todos modos,
porque un número impreso es un número que se puede quedar atrás de su comando.)
**La columna "v2.0" reemplaza los valores que tenía este documento entre 4/ago y 6/ago
(131/55/34/42/43/17/97) — esos números venían de la misma identidad fragmentada que MAP-1
corrigió; no se repiten aquí, quedan en el historial de git y en el baseline congelado de
`forense/notas/2026-08-06-map1-lector.md`.**

| Magnitud | v1.0 (10 inventarios) | v2.0 (11 inventarios, post-MAP-1) |
|---|---|---|
| Inventarios leídos | 10 | **11** |
| Entradas de fuente (con repetición entre dominios/clases) | 183 | **201** (197 resueltas + **4 SIN_RESOLVER**, deliberado — ver arriba) |
| **Fuentes únicas** | **119** | **128** |
| Con microdatos declarados | 52 | 53 |
| Sin microdatos (solo agregados) | 32 | 33 |
| Microdatos indeterminado | 35 | 42 |
| **Operables** (microdato + acceso libre/sin registro) | **38** | **43** |
| Transversales (3+ dominios/clases) | 16 | 17 |
| Mono-dominio/clase | 88 | 95 |

**Lectura del incremento neto (+9 fuentes únicas, no +12):** el +12 que este documento citaba
entre 4/ago y 6/ago (119→131) se apoyaba en el mismo `dedup.py` cuya deduplicación por
título normalizado absorbía *parte* del defecto de `acron()` de forma inconsistente y no
auditada — corrigiendo la identidad (MAP-1), la cifra correcta es **119→128 (+9)**. De las 18
entradas del nuevo inventario de clase, **5 ya existían en el catálogo** por dominio temático
(SAEH, SINAVE/Anuarios de Morbilidad, Global Findex, LAPOP, Latinobarómetro). Las **13
restantes son fuentes genuinamente nuevas**: CLUES, SINERHIAS, Padrón Único de Beneficiarios,
Cero Desabasto, Encuesta MCCI, CONSAR (extensión ya citada en R1.2, cuenta distinto como entrada
de clase), INE (cómputos), CONEVAL, COFEPRIS, ESTAD/"ENSATD", ENCAL, familia de instrumentos
IMSS, y OCDE Health at a Glance LAC — **no se afirma una cifra más precisa que la que el propio
`dedup.py` imprime**, misma disciplina que v1.0 fijó contra el conteo de ~61 sin auditar.

---

## La dimensión nueva — clase de fuente (Tarea A, Encargo AA)

**Las seis clases, verificadas y completadas contra búsqueda activa (no solo los ejemplos
semilla del encargo). Fuente completa de cada fila: `data/inventarios/inventario_fuentes_clase-fuente-mexico.md`.**

### Registro administrativo

| Fuente | Acrónimo | Granularidad | Enlazable con encuesta | Independiente del prestador | Nueva/ya en catálogo |
|---|---|---|---|---|---|
| Clave Única de Establecimientos de Salud | CLUES | Establecimiento (domicilio/localidad/municipio) | Parcial — llave CLUES↔localidad/institución, sin confirmar que ENSANUT la libere en microdato público | No (Secretaría de Salud) | **Nueva** |
| Subsistema de Equipamiento, RRHH e Infraestructura | SINERHIAS | Establecimiento (agregado de capacidad) | Sí, parcial — vía CLUES de la unidad | No (Secretaría de Salud) | **Nueva** |
| Subsistema Automatizado de Egresos Hospitalarios | SAEH | Individuo (egreso), con CLUES de unidad | Sí — CLUES↔localidad | No (Secretaría de Salud) | Ya en catálogo v1.0:91 |
| SINAVE / Anuarios de Morbilidad | SINAVE/SUIVE | Entidad (agregado); microdato de caso no confirmado | Parcial — entidad×año | No (Secretaría de Salud) | Ya inventariado (salud ítem 4), sin clase asignada hasta este acto |

### Padrón de programa

| Fuente | Acrónimo | Granularidad | Enlazable con encuesta | Independiente del prestador | Nueva/ya en catálogo |
|---|---|---|---|---|---|
| Padrón Único de Beneficiarios de Bienestar | PUB | **No verificada con precisión — ambiguo, declarado** | Potencialmente sí — ENIGH ya identifica beneficiarios por clave de programa (Nota 16, R5.1) | No (el propio operador del programa) | **Nueva** |

### Transparencia / sociedad civil

| Fuente | Acrónimo | Granularidad | Enlazable con encuesta | Independiente del prestador | Nueva/ya en catálogo |
|---|---|---|---|---|---|
| Cero Desabasto | — | **No verificada con precisión — ambiguo, declarado** (posible entidad, no confirmado nivel unidad médica) | Parcial — potencial entidad×año con ENSANUT | **Sí** | **Nueva** |
| Encuesta Nacional MCCI sobre Corrupción e Impunidad | Encuesta MCCI | No verificado con precisión (nacional, posible desagregación) | Parcial — tema corrupción en salud, no verificado a nivel de variable | Sí (ONG) | **Nueva** |

### Regulador o sectorial no-INEGI

| Fuente | Acrónimo | Granularidad | Enlazable con encuesta | Independiente del prestador | Nueva/ya en catálogo |
|---|---|---|---|---|---|
| CONSAR — series ampliadas | CONSAR | AFORE/entidad-agregado | Parcial | Sí | Serie ya citada en R1.2; esta entrada añade clase |
| INE — cómputos y resultados electorales | INE | **Casilla, sección, distrito, municipio, entidad** — confirmado por el propio INE | Sí, parcial — sección electoral↔localidad/AGEB, no verificado a nivel de instrumento | Sí | **Nueva** — hallazgo relevante para R7.1, ver cruce v2.0 |
| CONEVAL (medición de pobreza) | CONEVAL | Individuo/hogar (ENIGH-derivado) | Sí — deriva de ENIGH | **Reclasificación declarada, no cerrada:** absorbido por INEGI el 17/jul/2025 según una sola fuente de búsqueda, no re-verificada por segunda fuente independiente en este acto — si se confirma, deja de ejemplificar esta clase | Ya inventariado (salud, sin verificar fecha de absorción) |
| COFEPRIS — Visor de Registros Sanitarios | COFEPRIS | Por registro sanitario/medicamento (no por establecimiento) | No — registro de producto, no de conducta | Sí | **Nueva** — descartada explícitamente para R9.2 (regula producto, no audita existencias en unidad) |

### Encuesta institucional (no de hogares)

| Fuente | Acrónimo | Granularidad | Enlazable con encuesta | Independiente del prestador | Nueva/ya en catálogo |
|---|---|---|---|---|---|
| Encuesta de Satisfacción, Trato Adecuado y Digno ("ENSATD" del encargo → nombre real ESTAD/SESTAD) | ESTAD | Establecimiento (unidad médica) | No | Parcial (Aval Ciudadano + institucional) | **Nueva** — con discrepancia de nomenclatura declarada, ver hallazgo abajo |
| Encuesta Nacional de Calidad de la Atención del Servicio de Salud (IMSS) | ENCAL | Regional, no confirmada por unidad | No | No (IMSS) | **Nueva** |
| Familia de instrumentos IMSS (ENSAT, ES-HR) | — | No verificada con precisión | No verificado | No (IMSS) | **Nueva, registrada como clase vacía de detalle** |

### Internacional con dato de México

| Fuente | Acrónimo | Granularidad | Enlazable con encuesta | Independiente del prestador | Nueva/ya en catálogo |
|---|---|---|---|---|---|
| Global Findex Database | — | Nacional (agregado por país) | No | N/A | Ya en catálogo v1.0:89 |
| Barómetro de las Américas | LAPOP | Individuo, agregable a nacional | Sí — comparable con ENCUCI | N/A | Ya en catálogo v1.0:53 |
| Latinobarómetro | — | Individuo | Sí | N/A | Ya en catálogo v1.0:54 |
| Health at a Glance: Latin America and the Caribbean (OCDE) | — | **Nacional (país) — descalifica para Umbrales de conducta individual** | No | N/A | **Nueva** |

**Ninguna de las seis clases quedó vacía** — criterio de suficiencia de §7 del encargo, cumplido.

---

## Hallazgo declarado — "ENSATD" no existe con ese nombre

El encargo (§1, procedencia tipo 3) cita "ENSATD" como ejemplo de encuesta institucional de
salud. Búsqueda activa (11 consultas WebSearch + 5 WebFetch, más sondeo directo del host
resultante) no encontró ese acrónimo en ninguna fuente institucional. El instrumento real,
verificado por lectura directa del instructivo oficial (`calidad.salud.gob.mx`), es la
**Encuesta de Satisfacción, Trato Adecuado y Digno (ESTAD)**, con variante estatal SESTAD. Se
reporta como hallazgo de nomenclatura, no como fuente inexistente — la clase que "ENSATD" venía
a ejemplificar sí existe y sí queda cubierta (ver tabla arriba), solo que bajo otro nombre.

---

## Las 35 indeterminadas (heredado de v1.0, sin cambio en este acto)

Esta sección no se re-deriva aquí — sigue igual que en v1.0. Ver `catalogo-fuentes-v1_0.md §"Las
35 indeterminadas"` para el detalle; no se repite por brevedad, y porque ninguna de las 35 se
tocó en este acto (fuera de perímetro: Tarea A busca fuentes nuevas de clase, no resuelve
indeterminaciones de v1.0).

---

## Espina dorsal — 3 o más dominios/clases (re-derivada, 11 inventarios, post-MAP-1)

| Acrónimo | Dominios/clases | micro | libre | Nombre |
|---|---|---|---|---|
| **CPV** | 8 | sí | sí | Censo de Población y Vivienda (CPV) |
| **ENIGH** | 6 | sí | sí | Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) |
| **ENASEM** | 5 | sí | sí | Encuesta Nacional sobre Salud y Envejecimiento en México (ENASEM) / MHAS |
| **ENCIG** | 5 | sí | sí | Encuesta Nacional de Calidad e Impacto Gubernamental (ENCIG) |
| **LAPOP** | 5 | sí | sí | Barómetro de las Américas / AmericasBarometer (LAPOP) — **sube de 4 a 5 en MAP-1**: el inventario de capital_social cita "AmericasBarometer / LAPOP" sin la forma en español y `acron()` lo fragmentaba en una identidad aparte; la tabla de alias lo une |
| **ENCUCI** | 4 | sí | sí | Encuesta Nacional de Cultura Cívica (ENCUCI) |
| **ENNVIH** | 4 | sí | sí | Encuesta Nacional sobre Niveles de Vida de los Hogares (ENNViH) / MxFLS |
| **ENSANUT** | 4 | sí | sí | Encuesta Nacional de Salud y Nutrición (ENSANUT) |
| **ENVIPE** | 4 | sí | sí | Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública (ENVIPE) |
| **LATINOBARÓMETRO** | 4 | sí | sí | Latinobarómetro — muestra de México |
| **ENADID** | 3 | sí | sí | Encuesta Nacional de la Dinámica Demográfica (ENADID) |
| **ENDIREH** | 3 | sí | sí | Encuesta Nacional sobre la Dinámica de las Relaciones en los Hogares (ENDIREH) |
| **ENIF** | 3 | sí | sí | Encuesta Nacional de Inclusión Financiera (ENIF) |
| **ENOE** | 3 | sí | sí | Encuesta Nacional de Ocupación y Empleo (ENOE) |
| **ENSU** | 3 | sí | sí | Encuesta Nacional de Seguridad Pública Urbana (ENSU) |
| **ENUT** | 3 | sí | sí | Encuesta Nacional sobre Uso del Tiempo (ENUT) |
| **WVS** | 3 | sí | ? | World Values Survey (WVS) — muestra de México — **nueva en la tabla, MAP-1**: la mención de cultura_valores_opinion no tenía paréntesis con la sigla y `acron()` la dejaba como fuente aparte |

**Ninguna de las nuevas 13 fuentes de clase (Encargo AA) entra a la espina dorsal** — es
esperable: son registros/padrones/reguladores mono-clase o bi-clase por diseño, no encuestas de
dominio amplio. **La afirmación que este documento traía aquí ("la única fuente que cambia de
posición... es CPV") quedó falsa tras MAP-1 y se retira**: LAPOP sube de posición (4→5) y WVS
entra por primera vez a esta tabla (era 2 dominios, no 3) — ninguno de los dos por una fuente
nueva, ambos por una identidad que estaba mal fragmentada. Detalle fila por fila, incluida una
tercera composición que cambió sin alterar el conteo total (17→17): `forense/notas/2026-08-06-map1-lector.md`.

---

## Lo que este documento no hace

No adjudica ningún veredicto del Hito D. No confirma que ninguna fuente nueva de clase resuelva
un hueco de variable específico — cubre dominio/clase, no variable (misma disciplina que
`forense/cruce-catalogo-fichas-v1_0.md` ya fijó). El cruce contra las 27 fichas, con la pregunta
correcta, vive en `forense/cruce-catalogo-fichas-v2_0.md`, acto separado de este mismo encargo.

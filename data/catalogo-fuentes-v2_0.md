# Catálogo unificado de fuentes de datos — v2.0

> | | |
> |---|---|
> | **ARCHIVO** | `catalogo-fuentes-v2.0.md` |
> | **REEMPLAZA A** | `catalogo-fuentes-v1_0.md` — **borrar** |
> | **VERIFICAS ASÍ** | corre `python3 tests/catalogo.py && python3 tests/dedup.py` desde la raíz del repo; la cifra "Inventarios leídos" debe dar **11**, no 10, y "RECETA: consistente" debe imprimirse antes de creer cualquier otra cifra |
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

---

## Cifras derivadas (11 inventarios)

| Magnitud | v1.0 (10 inventarios) | v2.0 (11 inventarios) |
|---|---|---|
| Inventarios leídos | 10 | **11** |
| Entradas de fuente (con repetición entre dominios/clases) | 183 | **201** |
| **Fuentes únicas** | **119** | **131** |
| Con microdatos declarados | 52 | 55 |
| Sin microdatos (solo agregados) | 32 | 34 |
| Microdatos indeterminado | 35 | 42 |
| **Operables** (microdato + acceso libre/sin registro) | **38** | **43** |
| Transversales (3+ dominios/clases) | 16 | 17 |
| Mono-dominio/clase | 88 | 97 |

**Lectura del incremento neto (+12 fuentes únicas):** de las 18 entradas del nuevo inventario de
clase, **5 ya existían en el catálogo** por dominio temático (SAEH, SINAVE/Anuarios de
Morbilidad, Global Findex, LAPOP, Latinobarómetro) — `dedup.py` las fusiona por acrónimo/nombre
normalizado, no las cuenta dos veces (verificado: las 5 aparecen una sola vez en la salida de
`dedup.py`, ahora con un dominio/clase adicional). Las **13 restantes son fuentes genuinamente
nuevas** para el catálogo: CLUES, SINERHIAS, Padrón Único de Beneficiarios, Cero Desabasto,
Encuesta MCCI, CONSAR (extensión ya citada en R1.2, no nueva como fuente pero sí como entrada de
clase — cuenta distinto en el acrónimo por institución vs. serie), INE (cómputos), CONEVAL,
COFEPRIS, ESTAD/"ENSATD", ENCAL, familia de instrumentos IMSS, y OCDE Health at a Glance LAC. La
cifra exacta de "genuinamente nuevas" depende de cómo `dedup.py` trate acrónimos ya presentes por
otro motivo (p. ej. CONEVAL ya aparecía en el inventario de salud sin clase asignada — ver abajo)
— **no se afirma una cifra más precisa que la que el propio `dedup.py` imprime**, siguiendo la
misma disciplina que v1.0 fijó contra el conteo de ~61 que circulaba sin auditar.

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

## Espina dorsal — 3 o más dominios/clases (re-derivada, 11 inventarios)

| Acrónimo | Dominios/clases | micro | libre | Nombre |
|---|---|---|---|---|
| **CPV** | 8 | sí | sí | Censo de Población y Vivienda (CPV) |
| **ENIGH** | 6 | sí | sí | Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) |
| **ENASEM** | 5 | sí | sí | Encuesta Nacional sobre Salud y Envejecimiento en México (ENASEM) / MHAS |
| **ENCIG** | 5 | sí | sí | Encuesta Nacional de Calidad e Impacto Gubernamental (ENCIG) |
| **ENCUCI** | 4 | sí | sí | Encuesta Nacional de Cultura Cívica (ENCUCI) |
| **ENNVIH** | 4 | sí | sí | Encuesta Nacional sobre Niveles de Vida de los Hogares (ENNViH) / MxFLS |
| **ENSANUT** | 4 | sí | sí | Encuesta Nacional de Salud y Nutrición |
| **ENVIPE** | 4 | sí | sí | Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública |
| **LAPOP** | 4 | sí | sí | Barómetro de las Américas / AmericasBarometer — **sube de 3 a 4 dominios/clases en v2.0** (añade "Internacional con dato de México") |
| **LATINOBARÓMETRO** | 4 | sí | sí | Latinobarómetro — muestra de México — **sube de 3 a 4, mismo motivo que LAPOP** |
| **ENADID** | 3 | sí | sí | Encuesta Nacional de la Dinámica Demográfica (ENADID) |
| **ENDIREH** | 3 | sí | sí | Encuesta Nacional sobre la Dinámica de las Relaciones en los Hogares |
| **ENIF** | 3 | sí | sí | Encuesta Nacional de Inclusión Financiera (ENIF) |
| **ENOE** | 3 | sí | sí | Encuesta Nacional de Ocupación y Empleo (ENOE) |
| **ENSU** | 3 | sí | sí | Encuesta Nacional de Seguridad Pública Urbana (ENSU) |
| **ENUT** | 3 | sí | sí | Encuesta Nacional sobre Uso del Tiempo (ENUT) |

**Ninguna de las nuevas 13 fuentes de clase entra a la espina dorsal** — es esperable: son
registros/padrones/reguladores mono-clase o bi-clase por diseño, no encuestas de dominio amplio.
La única fuente que cambia de posición en esta tabla respecto a v1.0 es CPV, que ya era 8
dominios y no varía.

---

## Lo que este documento no hace

No adjudica ningún veredicto del Hito D. No confirma que ninguna fuente nueva de clase resuelva
un hueco de variable específico — cubre dominio/clase, no variable (misma disciplina que
`forense/cruce-catalogo-fichas-v1_0.md` ya fijó). El cruce contra las 27 fichas, con la pregunta
correcta, vive en `forense/cruce-catalogo-fichas-v2_0.md`, acto separado de este mismo encargo.

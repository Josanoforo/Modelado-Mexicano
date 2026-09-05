# SONDA-INSTRUMENTOS-DE-PERCEPCION — COMMIT-2 · sonda, lectura, cobertura

Continúa `forense/notas/2026-09-05-MAESTRA38-N12-spec.md` (COMMIT-1, congela
19 instrumentos mínimos + 4 fuentes cerradas + criterio de acierto). Este
commit ejecuta la sonda contra esas 4 fuentes y clasifica las 19 filas.

## 0 · Entorno, verificado antes de sondear nada

```
$ echo $CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE
cloud_default
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://losmexicanos.unam.mx/
000
$ ls data/raw/ 2>/dev/null | head -1
(vacío — data/raw ausente, esperado en NUBE, no es PARO)
```

`000` de `curl` es ambiguo por sí solo (podría ser timeout, DNS, o política)
— este acto no se detiene ahí (A.13: un negativo sin comando que examine la
causa no es un negativo). Segunda sonda, mecanismo distinto:

```
$ curl -sS "$HTTPS_PROXY/__agentproxy/status"
...
"recentRelayFailures": [
  {"kind": "connect_rejected", "host": "www.inegi.org.mx:443",
   "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)"},
  {"kind": "connect_rejected", "host": "losmexicanos.unam.mx:443",
   "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)"}
]
```

Tercera sonda, mecanismo distinto otra vez (la propia herramienta de fetch,
no `curl`):

```
WebFetch(https://www.inegi.org.mx/)      → EGRESS_BLOCKED
WebFetch(https://losmexicanos.unam.mx/)  → EGRESS_BLOCKED
```

**Tres mecanismos independientes, mismo veredicto: la política de egreso de
esta sesión NUBE bloquea ambos hosts, no solo uno.** Esto es más fuerte que
el precedente de `MAESTRA38-N11` (que solo corrió `curl` y leyó `000`) — no
dejamos la causa ambigua entre "el host no responde" y "el proxy corta".

## 1 · Sonda de alcanzabilidad — los tres hallazgos distintos (SPEC (a))

1. **INEGI, bloqueado.** Afecta a `ECOPRED` (única de las 4 fuentes alojada
   en `inegi.org.mx`). Fetch imposible desde NUBE hoy — pasa a CAJA (cláusula
   ENTORNO del encargo).
2. **UNAM, bloqueado.** Afecta a *Los mexicanos vistos por sí mismos* y a
   *Cultura Constitucional* (ambas UNAM-IIJ, `losmexicanos.unam.mx` y sin
   URL conocida respectivamente). Fetch imposible desde NUBE hoy — pasa a
   CAJA.
3. **`MxFLS`/`ENNViH` no necesita sonda de red.** Ya está en el corpus
   (`data/inventario-reactivos-ext-v1_0.tsv`, 17 181 filas) y ya fue
   exhaustivamente buscada por `MAESTRA34-N5`/`MAESTRA38-N10` contra estas
   mismas 19 reglas, antes de que se clasificaran
   `HIPÓTESIS-SIN-INSTRUMENTO` (`spec.md §2.2`). El «cruce contra el
   corpus» que el ENTORNO del encargo promete seguir corriendo en NUBE
   aunque la red falle **es exactamente este**: no hay bytes nuevos que
   cruzar, hay una lectura ya hecha que se hereda y se cita.

**Resultado de la sonda: 2 de 4 fuentes bloqueadas por red (100% de las que
dependían de red), 1 de 4 no depende de red y ya está agotada, 0 de 4 con
lectura nueva posible desde NUBE hoy.**

## 2 · Lectura de cuestionario/codebook por fuente (SPEC (b))

### 2.1 · `ECOPRED` (INEGI, 2014) — SIN-FETCH

No se pudo abrir. `data/inventarios/inventario_fuentes_seguridad_justicia_
mexico.md:243` es la única referencia local: nombre, institución, año con
signo de interrogación — sin URL, sin muestra, sin confirmación de
microdatos. Este acto no completa esos huecos por conjetura (violaría A.4:
un veredicto de acceso sin comando que lo haya examinado no es un
veredicto). **Declarado SIN-FETCH, deferido a CAJA** — ficha en `§4.2`.

### 2.2 · Los mexicanos vistos por sí mismos (UNAM-IIJ, 2015) — SIN-FETCH, con una declaración adicional

No se pudo abrir el portal (`losmexicanos.unam.mx`, bloqueado). El SPEC (b)
pide, específicamente para esta fuente, nombrar **una por una** las 25
encuestas de la colección. **Este acto declara explícitamente que no
cumple esa parte de la cláusula**, en vez de reconstruir la lista de
memoria: nombrar 25 títulos de encuesta sin haber abierto el índice del
portal sería una afirmación sin comando que la examine — el mismo defecto
que A.4/A.13 existen para prevenir, aplicado a una lista en vez de a un
número. El único módulo de esta colección que el catálogo local sí trae
verificado por institución/URL es el de migración
(`data/inventarios/inventario-fuentes-migracion-mexico.md:283-290`), y ese
módulo está fuera del universo de percepción de este acto (etiquetado
`NO-EN-ESTE-APARTADO` desde antes de `N12`). **Naming-the-25 queda
declarado como parte pendiente de CAJA**, junto con la lectura de
cuestionario/codebook — no se separan, porque no se puede nombrar cuál
encuesta cubre qué instrumento sin primero ver el índice.

### 2.3 · Cultura Constitucional (UNAM-IIJ) — SIN-FETCH, sin ficha previa que abrir

No se pudo abrir. A diferencia de `ECOPRED` y de *Los mexicanos vistos por
sí mismos*, esta fuente **no tiene ninguna entrada previa en ningún
catálogo local** — ni en `data/inventarios/*`, ni en `data/mapa-fuentes-
*.tsv`, ni en el resto del repositorio (`grep -rIn` general por
«constituc», 27 archivos con coincidencia, los 27 ruido de «Controversia
Constitucional»/«pensión constitucional»/«Constitución de 1917», ninguno
la encuesta — verificado, ver `spec.md §2.1`). Es la candidata de las 4
sobre la que el programa sabía **menos que cero**: ni siquiera una pista
de existencia catalogada, solo el nombre que el propio encargo trae.

### 2.4 · `MxFLS`/`ENNViH` — ya leída, heredada, no releída

Ver `§1.3`. No se abre ni un byte nuevo esta sesión: la lectura que
resuelve si esta fuente cubre las 19 filas ya está hecha (`N5`/`N10`,
3 formulaciones × 25 reglas contra `v1_2`/`ext`) y su resultado (0 de las
19 con instrumento encontrado — por eso son `HIPÓTESIS-SIN-INSTRUMENTO`
hoy) se hereda directo a la tabla de `§3`.

---

## 3 · Cobertura por instrumento mínimo (SPEC (c))

**Veredicto único, mismo para las 19: `SIN-COBERTURA-EN-ESTAS-FUENTES`.**
No porque el criterio de acierto (`spec.md §3`) se haya evaluado y fallado
ítem por ítem contra contenido leído — sino porque, de las 4 fuentes
cerradas, ninguna aporta hoy una lectura que permita evaluarlo: 3 están
`SIN-FETCH` (red bloqueada, `§1`/`§2`) y la cuarta (`MxFLS`/`ENNViH`) ya
fue evaluada por actos anteriores con resultado negativo para estas mismas
19 filas. **Universo declarado, no ocultado:** `0` fuentes con lectura
nueva posible hoy, de `4` cerradas — el mismo número que `§1` ya reporta.

| id | R-n | dominio | veredicto | universo (por qué) |
|---|---|---|---|---|
| `trabajo.jerarquia.deferencia_iniciativa_suprimida` | R2.1 | trabajo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | 3 fuentes SIN-FETCH; `MxFLS`/`ENNViH` ya buscada (`N5`/`N10`), 0/241591 y 0/42536 |
| `trabajo.liderazgo.benevolencia_legitima` | R2.2 | trabajo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `trabajo.prestaciones.formalidad_pesa_mas_que_salario` | R2.3 | trabajo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem; además sin frase-pregunta verbatim en `N10` (`spec.md §1.1`) |
| `trabajo.rotacion.joven_urbano_sin_culpa` | R2.4 | trabajo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `salud.atencion.leve_sin_imss` | R4.1 | salud | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `salud.prevencion.hombre_sin_permiso` | R4.2 | salud | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `salud.consumo.sellos_precio_similar` | R4.5 | salud | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `tiempo.puntualidad.formal_vs_social` | R6.1 | tiempo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `tiempo.compromiso.si_voy_incierto` | R6.2 | tiempo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `tiempo.bomberazo.recursos_escasos_urgencias` | R6.3 | tiempo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `tiempo.cumplimiento.recordatorio_baja_barrera` | R6.4 | tiempo | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `cooperacion.tanda.conoce_organizadora` | R8.2 | cooperación | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem; desenlace ya medido dos veces (`ENNVIH`+panel Compartamos), *driver* 0 veces |
| `cooperacion.confianza.puente_personal` | R8.3 | cooperación | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `informacion.credibilidad.allegado_confianza` | R9.3 | información | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `informacion.deferencia.costo_acceso_experto` | R9.1 | información | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `informacion.escuela.miedo_a_caer_clase_media` | R9.4 | información | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem; *driver* declarado "no observado" por el propio canon (`N10 §2.5`) |
| `comunicacion.rechazo.indirecto_face` | R10.1 | comunicación | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `comunicacion.retroalimentacion.privada_publica_capital_social` | R10.2 | comunicación | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |
| `comunicacion.directividad.regional_generacional` | R10.4 | comunicación | `SIN-COBERTURA-EN-ESTAS-FUENTES` | ídem |

**Ninguna fila es `CUBIERTO-POR` ni `PARCIAL`** — ambos veredictos exigen
haber leído contenido de al menos una fuente contra el criterio de `spec.md
§3`, y este acto no logró leer contenido nuevo de ninguna (`§1`/`§2`). No se
fuerza un `PARCIAL` para simular avance donde no lo hay.

---

## 4 · Fichas de adquisición — SPEC (d)

Las 3 fuentes bloqueadas por red siguen siendo **candidatas plausibles, no
descartadas** — el bloqueo es de esta sesión NUBE, no un veredicto sobre su
contenido. Se fichan para que CAJA las abra; `MxFLS`/`ENNViH` no lleva
ficha nueva (ya `OBTENIDO`, ya buscada, no hay acción de adquisición
pendiente sobre ella).

### 4.1 · Los mexicanos vistos por sí mismos (UNAM-IIJ, 2015)

- **Acceso:** no verificado desde NUBE (bloqueada). El módulo de migración
  de esta misma colección está catalogado sin licencia ni portal de datos
  confirmados (`[no verificado]`, mismo patrón que el resto de
  `data/inventarios/inventario_fuentes_cultura_valores_opinion_mexico.md`
  para proyectos UNAM de la misma época) — no se presume «público» ni
  «solicitud» sin abrir el portal.
- **Receta propuesta (≤1 min, NO verificada por ejecución — red
  bloqueada):** (1) abrir `https://losmexicanos.unam.mx/` en navegador;
  (2) buscar el índice de las 25 encuestas de la colección 2015 (o el
  listado de publicaciones del Área de Investigación Aplicada y Opinión,
  IIJ); (3) anotar si hay portal de descarga de microdato por encuesta o
  solo el libro/PDF agregado.
- **Cola:** fila `PENDIENTE` — `§5` de este documento, vía escritor
  canónico.

### 4.2 · ECOPRED (INEGI, 2014)

- **Acceso:** no verificado desde NUBE (bloqueada); el patrón de INEGI para
  encuestas de esta familia (`ENADIS`, `ENVIPE`) es microdato público sin
  registro — **probable, no confirmado** para `ECOPRED` específicamente
  (el propio catálogo local ya trae el año entre signos de interrogación).
- **Receta propuesta (≤1 min, NO verificada por ejecución — red
  bloqueada):** (1) abrir `https://www.inegi.org.mx/programas/ecopred/` o
  buscar «ECOPRED» en el buscador de programas de `inegi.org.mx`; (2)
  confirmar año(s) de levantamiento y ciudades cubiertas; (3) localizar el
  cuestionario (PDF) y la sección de percepción/cohesión social.
- **Cola:** fila `PENDIENTE` — `§5`.

### 4.3 · Cultura Constitucional (UNAM-IIJ)

- **Acceso:** no verificado — ni siquiera la existencia del portal está
  confirmada (`§2.3`).
- **Receta propuesta (≤1 min, NO verificada por ejecución — red
  bloqueada):** (1) buscar «Cultura de la Constitución» + «UNAM IIJ» en
  buscador (candidato de nombre completo: el IIJ-UNAM ha publicado
  encuestas nacionales sobre cultura de la legalidad/constitucional en
  colaboración con el Departamento de Estudios de Opinión — sin confirmar
  título ni edición exactos en esta sesión); (2) confirmar título exacto,
  institución responsable y año(s); (3) localizar cuestionario o
  microdato.
- **Cola:** fila `PENDIENTE` — `§5`. Nota explícita en la fila: de las 3,
  esta es la que menos se puede fichar con precisión — el propio nombre
  podría no ser el título exacto de publicación.

**Recetas verificadas de ≤1 minuto: 0 de 3 — declarado, no encubierto**
(mismo patrón que `PAQUETE-RECETAS-6`/`PAQUETE-RECETAS-7`: sin red, una
receta no verificada por ejecución no se presenta como verificada).
Detalle en `forense/notas/2026-09-05-MAESTRA38-N12-PAQUETE-RECETAS-8.md`.

## 5 · Cola — 3 filas nuevas

Vía `tools/curador_registro/tsv_crudo.py::upsert_fila`, clave
`fuente_canonica` (mismo patrón que `PAQUETE-RECETAS-6`, no `fila_origen`:
estas filas identifican una fuente candidata, no una regla ya fichada por
otro acto), sobre `data/curacion-registro/cola-adquisicion-registro.tsv`;
vista regenerada con `python3 tools/vista_cola_adquisicion.py`. Detalle de
las 3 filas (`fuente_canonica`, `estado_A4A5`, nota) en `§4` arriba y en el
propio TSV — no se transcriben aquí para no mantener dos copias que puedan
desincronizarse.

---

## 6 · MxFLS — SPEC (e), premisa corregida

> «MxFLS: si su texto no está indexado, el hallazgo es "fuente en corpus
> fuera del inventario" y se pide indexación en caja (no se indexa desde
> nube).» — encargo, verbatim.

**Esta premisa no se cumple — declarado, no forzado.** El texto de
`MxFLS`/`ENNViH` **sí** está indexado, en `data/inventario-reactivos-ext-
v1_0.tsv` (17 181 filas), no en `data/inventario-reactivos-descargas-mx-
v1_1.tsv` (0 filas, la tabla que el encargo señalaba). No se pide
indexación en caja: ya existe, ya se usó. El hallazgo real, distinto del
que el encargo anticipaba, es el de `§1.3`/`spec.md §2.2` — evidencia
disponible pero ya agotada, no evidencia ausente.

---

## 7 · Cierre — tabla 19 × veredicto, por dominio

| dominio | n hipótesis | cubierto | parcial | sin cobertura | hipótesis de N10 que cambiarían de clase si se adquieren las 3 fuentes SIN-FETCH |
|---|---|---|---|---|---|
| `trabajo` | 4 | 0 | 0 | 4 | **no estimable desde NUBE hoy** |
| `salud` | 3 | 0 | 0 | 3 | **no estimable** |
| `tiempo` | 4 | 0 | 0 | 4 | **no estimable** |
| `cooperación` | 2 | 0 | 0 | 2 | **no estimable** |
| `información` | 3 | 0 | 0 | 3 | **no estimable** |
| `comunicación` | 3 | 0 | 0 | 3 | **no estimable** |
| **total** | **19** | **0** | **0** | **19** | **no estimable** |

**«No estimable» es la respuesta honesta, no un hueco.** Estimar cuántas de
las 19 cambiarían de clase si `ECOPRED`/*Los mexicanos vistos por sí
mismos*/*Cultura Constitucional* se adquieren exigiría saber qué preguntan
esas 3 fuentes — que es exactamente lo que la red bloqueada impide
verificar hoy (`§1`/`§2`). Poner un número aquí sin haber leído una sola de
las 3 sería la misma clase de afirmación sin comando que A.4/A.13 prohíben,
solo que sobre un conteo en vez de sobre un veredicto individual. La
pregunta queda **abierta, con nombre, para CAJA** — no cerrada con una
cifra inventada.

**Enmienda a FP-303 (append, fechada 5/sep/2026):**

> N12 corrió: **0 de 19** con cobertura confirmada fuera del SNIEG hoy
> desde NUBE. 3 de las 4 fuentes candidatas (`ECOPRED`/INEGI, *Los
> mexicanos vistos por sí mismos*/UNAM-IIJ, *Cultura Constitucional*/
> UNAM-IIJ) quedaron `SIN-FETCH` por bloqueo de red de esta sesión (tres
> mecanismos de sonda independientes, mismo veredicto) — el conteo `k`
> puede subir una vez CAJA las abra; no se puede acotar cuánto sin
> abrirlas. La cuarta (`MxFLS`/`ENNViH`) no aporta cobertura nueva: ya fue
> exhaustivamente buscada por `MAESTRA34-N5`/`MAESTRA38-N10` contra estas
> mismas 19 filas, con el mismo resultado negativo. Detalle completo en
> `forense/notas/2026-09-05-MAESTRA38-N12-sonda.md`.

(Texto puesto en `forense/tablero/TABLERO-PROGRAMA-v1_1.md`, junto al
recibo de este acto — `forense/firmas-pendientes.tsv` no se edita en la
fila de `FP-303`, fuera del perímetro explícito de este encargo, que solo
autoriza tocar «tablero».)

---

## 8 · Hallazgos — una línea por fuente que el programa no conocía

**(a) *Los mexicanos vistos por sí mismos* (UNAM-IIJ, 2015, 25 encuestas)**
— el programa solo conocía el módulo de migración de esta colección
(`NO-EN-ESTE-APARTADO`, catalogado para otro dominio); las otras ≥24
encuestas de la misma colección, potencialmente relevantes para percepción
laboral, cortesía, confianza interpersonal, nunca habían sido evaluadas
para Ola 6 antes de este acto.

**(b) `ECOPRED` (INEGI, 2014)** — catalogado antes de este acto solo como
«pista» (nombre, institución, año incierto), nunca cruzado contra ninguna
regla del motor ni contra ningún instrumento mínimo; este acto es el
primero en intentarlo.

**(c) *Cultura Constitucional* (UNAM-IIJ)** — la más nueva de las tres:
cero catalogación previa en cualquier forma, en cualquier archivo del
repositorio. El programa no solo no la había evaluado — no sabía que
existía como candidata hasta que este encargo la nombró.

---

## 9 · Qué NO hace este acto

No mide nada de México (medición: cero, declarado por el propio encargo).
No abre ningún microdato (`data/raw` ausente, no se enlaza — no aplica a
este acto). No descarga ningún payload (anti-PR#77: nada que verificar en
el corpus compartido, porque no se intentó ninguna descarga). No sella
ninguna clasificación de `N10`. No decide si las 3 fuentes `SIN-FETCH`
serán adquiridas — eso es de mesa/CAJA, con las fichas de `§4` como
insumo. No edita `canon/modelo-decision-v4_0.md`, `milpa/**`,
`forense/prereg-caja/`, ni `data/manifiesto.yaml`. No indexa nada en
`inventario-reactivos-*` (`MxFLS`/`ENNViH` ya estaba indexada, `§6`). El
subproducto `…N12-modulo-propio-v0.md` se declara, no se lanza (`§10`,
propio de ese archivo).

## 10 · Verificación

`python3 tools/ya_medido.py` corrido sobre las 19 ids antes de escribir
este documento: `NUNCA-MEDIDA` en las 19, sin excepción, sin discrepancia
contra `N10` (A.8). `python3 tests/check.py --baseline`: ver `## CONSUMIDO`
del encargo archivado.

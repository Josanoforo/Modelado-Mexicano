# Universo mínimo de búsqueda por fuente — v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `UNIVERSO-MINIMO-FUENTE-v1.0.md` |
> | **REEMPLAZA A** | Nada — creación. |
> | **VERIFICAS ASÍ** | `grep -c -E "^[0-9]\." data/UNIVERSO-MINIMO-FUENTE-v1_0.md` da **6** (los seis niveles de la lista); el ADR que lo sella es **ADR-69** (`canon/gobernanza-v1_15.md`) |
> | **NOMBRE ESTABLE** | **`universo-minimo-fuente`** — cítalo así, nunca por nombre de archivo |

**Qué es.** La lista de sitios que un acto debe recorrer **antes** de declarar `NO-ENCONTRADO` sobre un campo material de una fuente. Un campo es material cuando bloquea un cálculo, cierra una ficha o gatea una regla — no cualquier dato posible de una fuente.

**Qué no es.** No es una lista de dónde buscar fuentes nuevas — eso es `data/inventarios/` y `catalogo-fuentes-v2_0.md`, y no se toca aquí. Este documento no decide qué fuentes existen; decide qué recorrido demuestra que un `NO-ENCONTRADO` sobre una fuente ya identificada agotó lo barato antes de declararse.

**El caso que lo motiva.** ENASIC 2022, 11/ago/2026, PR #173 (`8df61b0`, "E4b SELLO-B"): el acto declaró `periodo_levantamiento = NO_DETERMINADO` tras barrer, con rigor y universo declarado, el descriptor de 6 hojas (`enasic_2022_fd_xlsx`) y el PDF de 26 páginas (`889463927082.pdf`) — ninguno de los dos trae la fecha. El acto hizo todo bien dentro de su universo; el universo mismo era incompleto: le faltó el tercer sitio, la ficha de la Red Nacional de Metadatos, porque ningún documento del programa se lo exigía como paso obligatorio.

---

## La lista, para fuentes INEGI, en orden de costo creciente

1. **El payload y su descriptor**, en `data/raw` — el ZIP de microdatos y el FD (`*_fd.xlsx` o equivalente).

2. **El PDF "Conociendo la base de datos"** de la edición, si existe.

3. **La ficha de la Red Nacional de Metadatos** — `https://www.inegi.org.mx/rnm/index.php/catalog/{id}`. Contiene, en secciones estructuradas: *Muestreo* (marco, estratificación, tamaño y selección de muestra), *Recolección de Datos* (**periodo de ejecución, periodo de levantamiento y periodo de referencia, en tablas con fecha inicio/fin**), factores de expansión **por tabla, con nombre exacto de columna**, tasa de respuesta, cuestionarios por sección, y política de acceso. Metadatos exportables en `/rnm/index.php/metadata/export/{id}/json` y `/ddi`.

4. **Los indicadores de calidad publicados** de esa ficha — coeficiente de variación, error estándar e intervalo de confianza oficiales, típicamente en `/rnm/index.php/catalog/{id}/download/{n}`. **Son un validador externo del estimado propio**, del mismo tipo que `validar_contra_publicado()` es para ENIGH. Nota de mecanismo, con la reserva que §"Hecho de mecanismo" abajo detalla: un enlace `/download/{n}` catalogado no garantiza que el recurso sea el documento buscado — verificar `Content-Type`/`Content-Disposition` antes de registrar.

5. **Los documentos de la biblioteca** que la ficha cite: Diseño muestral, Informe operativo y de procesamiento, Diseño conceptual — en `https://www.inegi.org.mx/app/biblioteca/ficha.html?upc={id}`.

6. **El DOF**, cuando la cifra buscada sea un umbral, un índice o una regla de programa — no un dato de encuesta.

**La regla, en una frase:** *un acto que declare `NO-ENCONTRADO` sobre un campo material de una fuente INEGI enumera cuáles de estos seis niveles recorrió y cuáles no, con el mecanismo y la fecha. Un nivel no recorrido no es un hallazgo negativo: es un pendiente.*

---

## Hecho de mecanismo ya documentado (no lo re-descubras)

`/rnm/index.php/catalog/` responde HTML real y es navegable por `curl`, con enlaces directos (`/catalog/{id}/download/{n}`, `/catalog/{id}/data-dictionary`); `/programas/`, en cambio, es una SPA y no. Fuente: `forense/notas/2026-07-31-perimetro-descarga.md` §4, título literal *"El catálogo de microdatos (`/rnm/index.php/catalog/`) SÍ es navegable por curl"*.

**Corrección de cita, declarada aquí porque el borrador de este encargo la tenía mal.** La redacción original de este acto atribuía este hecho a `forense/notas/2026-08-07-explora1.md` y `2026-08-08-explora2.md` — verificado en el PASO 1 de este mismo acto (`grep -rn "navegable por curl\|SPA\|api/catalog/search" forense/notas/2026-08-07-explora1.md forense/notas/2026-08-08-explora2.md` → sin resultados), esas dos notas no contienen esas frases; leídas completas, documentan lo contrario para *esa sesión* (`explora1.md:7`: nueve intentos de `curl` a `inegi.org.mx`, los nueve `000`, bloqueo total de proxy; `explora2.md:82,114`: el buscador interno de RNM es "JS/AJAX, no reproducible por curl"). La cita correcta es `2026-07-31-perimetro-descarga.md` (arriba). Ver `forense/hallazgos.md` para el registro completo de esta corrección.

**Los IDs con descarga directa verificados el 31/jul** (`forense/notas/2026-07-31-cola-descarga-rederivada.md:110-111`) son **ENDIREH (801), ENADID (981), ENASEM (861), ENSU (1100)** — no "ENDIREH, ENADID, ENUT y ENCUP" como decía el borrador original de este acto. Y el matiz importa más que el nombre: esos cuatro enlaces resultaron ser el mismo **producto-señuelo** ya documentado para ENOE/catálogo 1121 — tablas de indicadores agregados con su margen de error, no microdato — y la nota es explícita en que **no se registraron** bajo esos acrónimos (`forense/notas/2026-07-31-cola-descarga-rederivada.md:147`, *"ENDIREH, ENASEM, ENSU — nada bajado"*). El hecho de mecanismo (RNM navegable por curl) es sólido; el ejemplo de qué se bajó ahí no lo es — no había nada que registrar, y el defecto de la premisa original fue tratar "se verificó navegable" como "se usó para obtener microdato".

La API de búsqueda (`/rnm/index.php/api/catalog/search`) sí tiene uso registrado, con resultado mixto: `forense/notas/2026-08-03-cbis-deferencia-externas.md:180` la usó para buscar "Cultura Política"/"Encuesta Nacional sobre Cultura Política"/"Practicas Ciudadanas" — devolvió resultados, pero **ninguno para ENCUP**: *"ENCUP no está indexado en el catálogo de metadatos de INEGI, a diferencia de sus encuestas hermanas"*. Citar ENCUP como ejemplo de "uso registrado" de la API es correcto para el acto de buscar, no para el de encontrar — la propia nota adjudica el resultado en negativo.

**El programa tocó la RNM en al menos cuatro actos antes del 11/ago sin que ninguno se convirtiera en receta:** 31/jul (`forense/notas/2026-07-31-cola-descarga-rederivada.md`, navegabilidad confirmada + cuatro IDs de descarga); 7/ago (`forense/notas/2026-08-07-explora1.md:106`, hallazgo estructural — la RNM es una puerta distinta de Descarga Masiva, con catálogo propio 330/518 para ENAPROCE); 8/ago (`forense/notas/2026-08-08-explora2.md:82`, buscador interno `catalog/search`, más un `HTTP 500` documentado en un enlace de descarga). Cuatro contactos, con IDs numéricos en mano cada vez, y el 11/ago un acto declaró `NO-ENCONTRADO` sin ir ahí — el defecto no era que el mecanismo fuera desconocido, era que ningún documento lo exigía como paso.

---

## Caso resuelto — ejemplo trabajado

ENASIC 2022, ficha RNM 922, abierta el 11/ago/2026:

- `periodo_levantamiento` = `2022-10-24/2022-12-16` (sección *Recolección de Datos*, tabla con fecha inicio/fin).
- `periodo_referencia` para variables sin ventana retrospectiva = *"El mismo día de la entrevista, de acuerdo a la variable"*.
- `FAC_ELE` confirmado como *"Ponderador de la población de 15 a 60 años. Tabla TPER_ELE"*.

**Con la discrepancia interna declarada, no resuelta aquí:** el apartado *Supervisión* de esa misma ficha dice *"del 24 de octubre al 10 de diciembre de 2022"* — seis días antes que la tabla estructurada de *Recolección de Datos*. Se registran las dos y se dice cuál se toma y por qué. **No la resuelve este acto ni la oculta** — es material para el tercer commit de E4b sobre su propio campo, no para éste.

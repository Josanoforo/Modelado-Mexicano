# Declaración de fuente · `R4.1` + `R9.1` · Encargo Z, commit 1

*(Escrita antes de abrir un solo ZIP de microdato. Se registran juntas por la propia ficha de `R9.1` (`hitoD-preregistro-v2_0.md:258`, "Nota de simetría con R4.1"): si ambas fallan por el mismo lado, no son dos refutaciones independientes.)*

## Candidatas del catálogo — todas, con la razón de la elección

Dominio del falsador de ambas: **SAL** (acceso y uso de servicios de salud). Del cruce ya reconstruido (`forense/cruce-catalogo-fichas-v1_0.md:84,91`, §2/§3), las candidatas con presencia en `data/catalogo-fuentes-v1_0.md` son:

| Candidata | Cubre el dominio | Por qué se descarta o se elige |
|---|---|---|
| **ENSANUT CONTINUA 2024** | Sí — módulo dedicado de utilización de servicios de salud (Cuestionario de Utilizadores) + sección IV del Cuestionario Hogar | **Elegida.** Única fuente del catálogo con variable de institución de atención que distingue explícitamente "farmacia con consultorio" (código 12) de IMSS/ISSSTE/privado/informal, y con variables cuantitativas de costo, tiempo de traslado y espera en el mismo cuestionario. |
| ENIGH | Parcial (SAL, gasto en salud) | Descartada: mide gasto de bolsillo en salud, no institución de atención ni motivo de elección — no construye la variable de conducta que el falsador necesita. |
| ENASEM/MHAS | Parcial (SAL, restringida a 50+) | Descartada por edad: ambas fichas hablan de población general, no específicamente adultos mayores. |

No hay otra candidata con presencia en el catálogo para este dominio a nivel de variable de utilización.

## La elegida, contra el Umbral concreto de cada ficha

**Fuente elegida: ENSANUT CONTINUA 2024** (INSP/Secretaría de Salud), Cuestionario de Utilizadores de Servicios de Salud + sección IV del Cuestionario Hogar. Verificado por lectura directa de `1 VFINAL Cuestionario Hogar ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` y `5 VFINAL Cuestionario utilizadores ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` (raíz `descargas_mx`, registrados en `data/manifiesto.yaml`), **no de sus catálogos de nombre solamente** — mismo estándar que exigió Nota 17 (`R4.2`).

**R4.1 — Umbral (línea 106):** "Reducción <25% en uso de consultorio adyacente a farmacia tras una **mejora documentada de acceso público** (tiempo de espera y distancia), en población sin seguridad social."
- `U0201`/`H0409` (código 12 = "Consultorios pertenecientes a farmacias/Farmacias con consultorio médico") da la variable de conducta.
- `U0204` (tiempo de traslado), `U0205` (tiempo de espera en el sitio) y `U0203`/`U0207`/`U0208` (costo) dan los tres drivers del `PORQUE` — pero como **nivel**, no como cambio.
- `U0202`/`U0202c` (motivos espontáneos de elección/no-elección de lugar) incluye ítems de trato ("Le gusta cómo lo(a) atienden" / "No me gusta la atención que dan/no son amables") — es la única pieza que toca el **confusor trato**, y es una mención categórica espontánea (máx. 3 códigos), no una escala de satisfacción administrada. Débil, no ausente.

**R9.1 — Umbral (línea 256):** "Tasa de consulta a experto <50% en decisiones de salud de consecuencia media-alta, en población con acceso documentado (distancia <2 km, sin costo, espera <1 día)."
- `U0201` distingue proveedor formal (códigos 01-19, 24-26) de informal (20 curandero/hierbero/naturista, 21 homeópata/partera/acupunturista) — da la variable de conducta.
- El Cuestionario de Utilizadores **solo entrevista a quien SÍ fue atendido** (filtro `U0103`/`1.3`; ver también nota de programación en la página 1 del cuestionario: "el cuestionario de Utilizadores es solo para las personas que SÍ recibieron atención médica"). Quien tuvo necesidad de salud y **no consultó a nadie** —el caso puro de "prevalece 'yo sé por experiencia'"— no entra a este cuestionario.
- El Cuestionario Hogar (sección IV, `H0407`) sí captura motivos de no-atención para la población completa, pero su lista de 16 motivos es enteramente institucional/estructural (unidad cerrada, no cubierto, sin ficha, costo, trámites, espera) — **no tiene una categoría de "preferí resolverlo por mi cuenta/con un allegado"**. Verificado por lectura completa de la lista (`1 VFINAL Cuestionario Hogar...pdf`, sección IV, pregunta 4.7).

## Qué condición del Umbral no está cubierta

**R4.1:** la condición decisiva no es el confusor de trato (que al menos tiene un proxy débil) — es que **ninguna fuente del catálogo construye la comparación antes/después que el Umbral exige literalmente** ("tras una mejora documentada de acceso público"). ENSANUT CONTINUA 2024 es corte transversal repetido, no panel de los mismos individuos ni de las mismas localidades ancladas a un evento de apertura de clínica fechado. ENIGH, la otra candidata de dominio, también es transversal. No existe en el catálogo un diseño que observe la misma población/localidad antes y después de una mejora de acceso documentada — es exactamente el tipo de ausencia que el §5 del encargo define como `D` ("ninguna fuente del catálogo construye una condición del Umbral"), verificada contra el cuestionario, no contra el nombre de la variable.

**R9.1:** dos condiciones no cubiertas, independientes entre sí:
1. **Distancia en km.** Ninguna variable mide distancia en kilómetros; solo existe tiempo de traslado (`U0204`), un proxy relacionado pero distinto (confundido por modo de transporte).
2. **Población que no consulta a nadie.** El único cuestionario con las variables de acceso objetivo (`U0203`-`U0205`) es Utilizadores, que por diseño excluye a quien no buscó ninguna atención — precisamente la subpoblación donde "prevalece 'yo sé por experiencia'" sería más visible. El Cuestionario Hogar cubre a toda la población pero no distingue esa preferencia de una barrera estructural.

## Variables exactas, universo, ponderador, estrato, UPM

- Tabla: `adultos_ensanut2024_w_ICB` (sección de utilización) e `integrantes_ensanut2024_w_ICB` (roster + sección IV de Hogar); raíz `descargas_mx`, no `data/raw/` integrada.
- Universo previsto: personas con necesidad de salud reportada en los últimos 3 meses (`H0402`/`4.1`), sin seguridad social (derivado de `3.10` Hogar) para `R4.1`; personas atendidas con necesidad de consecuencia media-alta para `R9.1`.
- Variables de conducta: `U0201`/`H0409` (institución de atención).
- Variables de acceso: `U0203` (costo transporte), `U0204` (tiempo traslado), `U0205` (tiempo de espera en sitio), `U0207`/`U0208` (cobro por atención).
- Variable de trato (proxy): `U0202`/`U0202c` (motivos codificados, hasta 3, espontáneos).
- Diseño muestral: ponderador `ponde_f`, estrato `estrato`/`est_sel`, UPM `upm` — misma convención verificada en Nota 17/`forense/notas/2026-08-04-y3-operacionalizacion-r4-2-ensanut.md` para la misma encuesta.

## Compromiso de pre-registro

**El primer resultado que produzca este procedimiento es el que se reporta.**

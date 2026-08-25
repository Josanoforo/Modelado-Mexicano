# Nota · ACTO CAL-G3-PUNTUAL — llaves 3 de 3 y el primer coeficiente propio

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-24-cal-g3-puntual-cierre.md` |
> | **NOMBRE ESTABLE** | **`cal-g3-puntual`** |
> | **QUÉ ES** | La spec B-bis (PASO 1, Commit 1) y la corrida (PASO 2, Commit 2) del ACTO que ejerce por primera vez la llave `CAL-G3` con un diseño intra-persona nuevo, distinto del descriptivo de `hitoD-preregistro-v2_0.md` Nota 10. |
> | **ENCARGO** | `forense/encargos/2026-08-24-CAL-G3-PUNTUAL.md` |

---

## PASO 0 · Agotar la búsqueda del campo de diseño

**Resultado: AGOTADO** (universos a+b+c, con conteos). Esta búsqueda **reproduce**, de forma independiente y en este mismo acto, el hallazgo ya escrito por `ACTO RECENSO-DISEÑO-14` en `data/diseno-muestral.yaml:412-439` (`estado: SIN_DISEÑO_PUBLICADO`) — no lo cita sin verificar, lo repite contra el árbol.

**(a) Cabeceras + etiquetas de variable de los 425 `.dta`.** Script: `pandas.io.stata.StataReader` en modo lectura de 1 fila, sobre las tres olas comprimidas (`ehh02dta_all.zip` 137 archivos, `ehh05dta_all.zip` 147, `ehh09dta_all.zip` 141 — **425 archivos, 425 leídos sin fallo**, exit 0). Filtro `upm|conglomer|estrato|muestreo|primaria|psu|cluster|strat` sobre nombre **y** etiqueta: **93 aciertos**, de los cuales **92 son falso-cognado** (`primaria` = escuela primaria, en baterías de educación — `ed*`, `edn12p*`). El único acierto sustantivo: columna `estrato` en `c_portad.dta` de las tres olas, etiqueta Stata `"ESTRATO"`. Verificado su contenido: **4 valores son clases de tamaño de localidad** (`<2500` · `2,500-14,999` · `15,000-99,999` · `≥100,000`, con una errata de la propia fuente en el tercer corte), **no** un estrato de diseño muestral. Cero columnas de `upm`/`conglomerado`/`psu` en los 425 archivos. Script: `/tmp/.../scan_dta.py` (scratchpad, no en el perímetro — reproducible a partir de esta nota).

**(b) Texto de las tres guías, doble extractor (lección FP-111).** `guiausuariov1.pdf` (ola 1, 74 págs), `guiausuariov2.pdf` (ola 2, 38 págs), `guia_de_usuario_ennvih-3.pdf` (ola 3, 62 págs) — extraídas con `pdftotext` **y** `pypdf` (6 extracciones, 0 fallos). Búsqueda del mismo filtro: **guiausuariov1** trae la única mención sustantiva — narrativa de diseño ("probabilística, estratificada, polietápica y por conglomerados") **sin nombre de campo**, más una entrada de glosario que **nombra** `Estrato` y lo define exactamente como la clasificación de tamaño de localidad de (a) — confirma (a), no la contradice. `guiausuariov2` y `guia_de_usuario_ennvih-3`: 3 coincidencias cada una, las tres el sustantivo "estrategias" (falso-cognado por subcadena `strat`), 0 aciertos sustantivos. Ningún documento nombra un campo de UPM/conglomerado.

**(c) Espejo académico MxFLS (RAND/ICPSR), universo declarado por el ENCARGO.** `https://www.rand.org/labor/FLS/MxFLS.html`, `https://www.icpsr.umich.edu/web/ICPSR/studies`, `https://www.icpsr.umich.edu/web/ICPSR/series/00259` — **3 URLs**, `curl` con sandbox de red deshabilitado explícitamente (`dangerouslyDisableSandbox`) para descartar que el 403 fuera artefacto de este entorno: **las tres devuelven HTTP 403 real, cuerpo `AWS WAF "Request blocked"`** — el mismo patrón de bloqueo que `SONDA-1` ya documentó para hosts nuevos. Cero páginas leídas, cero campo aportado. Universo declarado **agotado por bloqueo de red confirmado, no simulado ni asumido**.

**Consecuencia para PASO 1 (heredada de RECENSO-DISEÑO-14, no re-derivada):** sobre ENNViH se pueden calcular estimaciones puntuales ponderadas (`fac_*` existe y está completo) pero no hay con qué declarar `strata`/`cluster` en un diseño muestral formal. **Plan B firmado por el propio encargo**: supuesto MAS + sensibilidad por remuestreo de hogar, rotulada informal.

---

## PASO 1 · Spec B-bis (congelada antes de correr — Commit 1)

**θ y desenlace, con escala declarada cada uno — hallazgo nuevo de este acto, no el de Nota 10.**

La Nota 10 de `hitoD-preregistro-v2_0.md` (30/jul/2026) ya corrió una Fase C descriptiva sobre las olas 2-3 con exposición = formalidad del jefe (`TB33`) y desenlace = acceso formal del hogar (`CRH01`) — explícitamente **sin veredicto** y **sin operacionalizar `horizonte_temporal` directamente** (medía transición de formalidad, no preferencia temporal). Este acto busca, y encuentra, un reactivo **literal** de horizonte temporal, no un proxy de formalidad:

- **Módulo `PR` ("Piensa en el futuro para tomar decisiones de gasto/ahorro")**, presente en `iiib_pr.dta` de **ola 2 (`ehh05dta_all.zip`) y ola 3 (`ehh09dta_all.zip`)**, ausente de ola 1. Confirmado por codebook oficial (`ehh05cb_b3b.pdf`, `ehh09cb_b3b.pdf`, extraídos con `pdftotext`):
  - `pr01` — "¿Piensa en el futuro al tomar decisiones de gasto/ahorro?": `1=Sí · 2=No tengo suficiente dinero · 3=No pienso en el futuro`.
  - `pr02` — "¿Con qué periodo de tiempo piensa el gasto/ahorro?": escala ordinal **`01=Unos cuantos días → 02=Unas cuantas semanas → 03=Unos cuantos meses → 04=El próximo año → 05=Unos cuantos años → 06=Los próximos cinco años → 07=Más de 10 años`**, más `08=Nunca he pensado en planear para el futuro` y `98=NS` (no sustantivos, excluidos declarados, no re-etiquetados). Idéntico esquema de categorías en ambas olas (verificado línea por línea contra los dos codebooks).

**θ (generador `G3 → horizonte_temporal`) = `pr02` recodificada 1-7** (entero, mayor = horizonte más largo), dominio restringido a las 7 categorías sustantivas; `8` y `98` se excluyen del universo analítico (declarado, no imputado).

**Desenlace = `cr27` ("Tiene ahorros"), binario `1=Sí` vs `3=No`**, presente en `iiib_cr.dta` de ambas olas (codebook `ehh05cb_b3b.pdf`: `1. Sí · 3. No · 8. NS`). Escala: proporción (0/1).

**Universo (regla A-bis 4, declarado, no reconciliado contra marginales poblacionales):** individuos con `pid_link` presente en ambas olas (ver corrección de enlace abajo), **con `pr02` válido (1-7) y `cr27` válido (1/3) en AMBAS olas simultáneamente**. El resultado queda acotado a esta subpoblación — personas que respondieron sustantivamente a la pregunta de horizonte temporal y a la de ahorro en los dos levantamientos donde el módulo existe (2005-06 y 2009-12). No es "México", no es "los adultos de México": es la intersección de panel-retenido × módulo-aplicable × respuesta-sustantiva en ambas mediciones.

**Corrección de enlace intra-persona (heredada del método de Nota 10 (c), re-verificada contra el microdato de este universo, no asumida):** `pid_link` de ola 3 intercala un código de 2 letras (ronda de apertura `A`/`B`/`C` + tipo `P`/`H`) que ola 2 no graba — confirmado: `AP` 23,284 filas, `CP` 1,089, `BP` 549, `CH` 7 (sobre las 24,927 filas de `iiib_pr.dta` ola 3). Las **1,096 filas de ronda `C`** (`CP`+`CH`) son personas registradas por primera vez en 2009: se **excluyen antes de emparejar** (no después) para no arriesgar una coincidencia espuria por dígitos con una persona distinta de ola 2 — la misma protección que Nota 10 documentó para su propio universo de jefes. El resto se despoja del código de letras para reconstruir la llave numérica compartida con ola 2.

**Ponderador:** `fac_3b` (ola 2), "FACTOR DE EXPANSIÓN LIBRO 3B", citado a la fila ENNViH de `data/diseno-muestral.yaml:405-411` (patrón `fac_<libro>`; libro `3b` es el libro que contiene tanto `PR` como `CR`) — vive en `ehh05w_all.zip:ehh05w_all/ehh05w_b3b.dta`, unión por `folio`+`ls`.

**Estimando:** par intra-persona por **primeras diferencias ponderadas**: `Δahorro = β₀ + θ·Δhorizonte + ε`, con `Δahorro = ahorro_ola3 − ahorro_ola2 ∈ {−1,0,1}` y `Δhorizonte = horizonte_ola3 − horizonte_ola2 ∈ {−6,...,6}`. Es un diseño de efectos fijos de persona por construcción (cada individuo es su propio control) — la misma familia de diseño que Nota 10 usó para su exposición, aplicada aquí al reactivo correcto.

**Varianza (PASO 0 → AGOTADO, plan B firmado por el encargo):**
1. **Primaria, MAS declarado:** error estándar tipo HC1 (heterocedasticidad-robusto) sobre el WLS de primeras diferencias, bajo el supuesto explícito de muestreo aleatorio simple. **Ficha: este IC subestima el error de diseño (no hay UPM/estrato para corregirlo); magnitud no cuantificable sin esos campos — hallazgo de PASO 0, no invención de esta spec.**
2. **Sensibilidad informal (rotulada así, no sustituye a la primaria):** remuestreo por hogar (`folio`, no por persona — el hogar es el clúster plausible más próximo sin campo de diseño) con reemplazo, 500 réplicas, IC percentil 2.5/97.5.

**Escala de falsación (B-bis) y precedencia, declarada antes de correr:**
- **`EJERCIDA_CORROBORA`** si el IC excluye 0 **y** el signo coincide con el asignado (−0.60, comparado solo en signo por instrucción del encargo).
- **`EJERCIDA_ACOTA`** si el IC excluye 0 pero el signo **no** coincide con el asignado, **o** si coincide en signo pero la escala es tan distinta que no sostiene comparación de magnitud (nada entre escalas sin enlace) — el resultado es información acotada a esta subpoblación, co-observación intra-persona, **no** un coeficiente causal.
- **`EJERCIDA_REFUTA`** si el IC excluye 0, el signo es opuesto, **y** las escalas fueran comparables por enlace explícito (no es el caso aquí — no hay tal enlace).
- **`EJERCIDA_INDECISA`** si el IC (primario o de sensibilidad) incluye 0.
- Precedencia: si primaria y sensibilidad discreparan en cruzar 0, **gana la sensibilidad** (es la cota conservadora, no la optimista) para decidir entre `INDECISA` y cualquier otra fila.

**«El primer resultado que produzca este procedimiento es el que se reporta.»**

Reglas A-bis recordadas para PASO 2: co-observación no es identificación (se rotula asociación intra-persona); condicionado tampoco es correcto (no se controla por nada fuera de la persona-como-su-propio-control); nada entre escalas sin enlace (comparación con el asignado, solo en signo); punto que cumple umbral con IC que no lo despeja no adjudica (propuesta con reserva).

---


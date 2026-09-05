# S7 · Pre-registro de `salud.vacunacion.disponible` — medible como está (id de §3.9, dominio información)

### `prereg-caja-S7-L17` · **v1.0** · 5 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S7-L17-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S7-L17`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`, de tres falsadores paralelos para `salud.vacunacion.disponible` (`R9.2`, regla de §3.9 información — `canon/registro-rotulos.tsv`, corrección de mapa de este mismo acto, P3): Rama A (`ENNVIH`, ficha original de `N5`/`N10`), Rama B (`ENSANUT2024` adultos, **hallazgo nuevo de esta pieza** — un reactivo de razón-de-no-vacunación que prueba el `PORQUE` de la regla más directamente que la Rama A), Rama C (`ENSANUT2024` adolescentes, corroboración de tasa de aceptación, sin antecedente propio, per `N10 §2.5`). |
> | **QUÉ NO ES** | No abre ningún `.dta` — los payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el tier de `salud.vacunacion.disponible` (hoy `[FUERTE]`, línea 575) ni sella `MEDIBLE-COMO-ESTÁ`. No reclasifica el dominio de la regla en `canon/modelo-decision-v4_0.md` — la corrección de §3.9 vs. §3.4 es de `canon/registro-rotulos.tsv` (P3 de este mismo acto), no de este documento. |
> | **VERIFICAS ASÍ** | Caja confirma, antes de calcular la Rama A, si `ce19d_2`/`hs16d_2` (costo de la vacuna) están condicionadas en el `.dta` a haber **recibido ya** la vacuna — si es así, no son antecedente sino post-tratamiento, y la Rama A queda `NO-CONSTRUIBLE` tal como está diseñada (§0.3); la Rama B no depende de esa resolución. |

**Acto:** `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`, 5/sep/2026, entorno **NUBE**, sobre `origin/main = b17d19bd1d566220ac81ebbac47c1c80ae14d66e` (SHA de redacción del encargo).

---

## 0 · Ficha bajo prueba y corrección de premisa (A.8/D-13)

### 0.1 · Definición vigente

`canon/modelo-decision-v4_0.md:575` (§3.9 Información y creencia), verbatim:

> *SI la vacuna/servicio está disponible y la campaña llega ENTONCES la mayoría acepta — PORQUE el default es aceptación y el hueco es logístico (no actitudinal) — `[FUERTE]`.* · **id:** `salud.vacunacion.disponible` ⚠️ *id ya existente en `procedencia.yaml`, con dominio equivocado (`salud.*` en un id de §3.9, no §3.4) — no se corrige, ver `forense/hallazgos.md`*

Verificación previa (A.8, `tools/ya_medido.py`, corrida el 5/sep/2026 desde `origin/main = b17d19bd`):

```
$ python3 tools/ya_medido.py salud.vacunacion.disponible
=== ya_medido: salud.vacunacion.disponible ===
  resuelto por canon: salud.vacunacion.disponible -> R9.2
-- milpa/tramite.yaml -- (sin apariciones)
-- milpa/tramite-ola5-propuesta-v0.yaml -- (sin apariciones)
-- canon/modelo-decision-v4_0.md §7 -- R9.2 | L289 | ... | [FUERTE] | Sí
-- forense/notas/*-L*-*.md -- MAESTRA37-L1-censo.md:90, -remapeo.md:56,80
-- forense/prereg-caja/S*-spec-*.md -- (sin apariciones)
-- canon/registro-rotulos.tsv (alias) -- (sin apariciones)
========================================
NUNCA-MEDIDA
```

`NUNCA-MEDIDA`, sin discrepancia contra `N5`/`N10` (ambos también declaran existencia de reactivo, no falsación corrida).

### 0.2 · Corrección de fuente de inventario (A.8/D-13)

`N10 §2.5` cita `cen12_1a`/`he25c`/`ce19d_2`/`hs16d_2` como del "mismo instrumento, `ENNVIH`" sin decir en qué inventario viven. **Verificado: ninguna de las cuatro aparece en `data/inventario-reactivos-descargas-mx-v1_1.tsv`** (0 filas, búsqueda exacta y por substring, `ENNVIH` tampoco aparece como `payload_id` en ese archivo). Viven en `data/inventario-reactivos-ext-v1_0.tsv` — el universo `v1_2`/`ext` de `241 591` filas que `MAESTRA34-N5` usó originalmente (mismo defecto de cita que `S6 §0` (`salud.atencion.grave`, mismo lote) ya corrigió para `es09`/`cen10*`, que están, de hecho, en los **mismos tres archivos ZIP** que estas cuatro variables — confirmado, mismo `payload_id`/`sha256`). §1 cita el archivo correcto en cada fila.

Las tres variables de `ENSANUT2024` (`d0321j`/`d0321p`, tercer instrumento de `N10`, y el hallazgo nuevo de esta pieza — Rama B, §2) **sí** están en `data/inventario-reactivos-descargas-mx-v1_1.tsv` — mismo universo `descargas_mx_v1_1` que el resto del acto `N10` usó.

### 0.3 · Corrección de diseño — el disparador de la Rama A puede ser post-tratamiento, no antecedente (declarada, no resuelta)

`ce19d_2`/`hs16d_2` («COSTO VACUNA CONSULTA»/«COSTO VACUNA HOSPITAL») preguntan **cuánto costó** la vacuna. Un reactivo de costo de un servicio típicamente solo tiene respuesta válida para quien **ya recibió** ese servicio — si es así, `ce19d_2`/`hs16d_2` no miden "¿estaba disponible?" como antecedente independiente del desenlace, sino que son **parte del mismo evento** que `cen12_1a`/`he25c` (recibir la vacuna). Esto no está confirmado ni refutado por el inventario (que no trae patrones de salto/`skip`) — se declara como riesgo de diseño de la Rama A, a resolver por caja contra el codebook de `ENNVIH` antes de tratarla como un falsador válido de antecedente-y-desenlace independientes. **Es exactamente el mismo tipo de corrección que `S6 §0.3` hizo para `cen10*`** — un reactivo que la ficha original supone que mide una cosa, y que el texto verbatim, mirado con cuidado, podría medir otra.

---

## 1 · Rama A — `ENNVIH` (ficha original de `N5`/`N10`)

Búsqueda contra `data/inventario-reactivos-ext-v1_0.tsv`, exacta por `variable_id`, en los mismos tres ZIP que `S6 §1.1` ya usa para `es09`/`cen10*`:

| variable | libro/módulo | ola 2002 (línea, texto) | ola 2005 (línea, texto) | ola 2009 (línea, texto) |
|---|---|---|---|---|
| `ce19d_2` | `b3b`/`iiib_ce1.dta` | 34784, «COSTO VACUNA CONSULTA» | 38024, «COSTO VACUNA CONSULTA» | 45886, «COSTO VACUNA» |
| `hs16d_2` | `b3b`/`iiib_hs1.dta` | 35091, «COSTO VACUNA HOSPITAL» | 38381, «COSTO VACUNA HOSPITAL» | 46293, «COSTO VACUNACION/INMUNIZACION» |
| `cen12_1a` | `b5`/`v_cen1.dta` | 35877, «CONSULTA RECIBIO:VACUNACION» | 39265, «CONSULTA RECIBIO:VACUNACION» | 47213, «QUE SERV RECIBIO:INMUNIZACION/VAC» |
| `he25c` | `b4`/`iv_he2.dta` | 35618, «SERV EMBARAZO:VACUNA TETANOS» | 38999, «SERV EMBARAZO:VACUNA TETANOS» | 46934, «SERVICIOS EMBARAZO:VACUNA TETANOS» |

El texto de 2009 difiere del de 2002/2005 en tres de las cuatro variables (`hs16d_2`, `cen12_1a`, y de forma menor `he25c`) — declarado, no homogeneizado a ciegas. `ce19d_2`/`hs16d_2` viven en el mismo libro (`b3b`) que `es09` (`S6 §1.1`); `cen12_1a` vive en el mismo libro (`b5`) que `cen10*` (`S6 §1.2`) — el vínculo entre disparador y desenlace de esta rama exige unir libros distintos por folio, igual que `S6` ya declaró para su propio diseño.

### 1.1 · Universo y ponderador — Rama A

Mismos hechos que `S6 §1.3` ya estableció para este payload (no re-derivados aquí):

- **Ponderador:** el ZIP de hogar (`ehh0Xdta_all.zip`) **no trae ningún ponderador** — factor de expansión en un payload separado, no indexado en `v1_1` (`ennvih1_2002_ponderador`/`ennvih3_2009_ponderador_transversal`, ver §6). Para 2009, libro `b3b` (`ce19d_2`/`hs16d_2`/`es09`) tiene ponderador único (`fac_3b`); libro `bx` no aplica aquí (esta rama no usa `p_es.dta`). Libro `b5` (`cen12_1a`): ponderador no verificado en esta pieza, mismo criterio de reserva que `S6`.
- **Estrato:** `estrato` («ESTRATO»), única variable, en `c_portad.dta`. **Sin `upm`/`cluster`.**

**Universo:** personas de la muestra `ENNVIH` con código válido en `ce19d_2` o `hs16d_2` (disparador) y en `cen12_1a` o `he25c` (desenlace) de la misma ola — sujeto a la reserva de §0.3 sobre si el disparador es realmente antecedente.

---

## 2 · Rama B — `ENSANUT2024` adultos, razón de no vacunación (hallazgo nuevo de esta pieza)

**No citado por `N5`/`N10` — encontrado al buscar, en `data/inventario-reactivos-descargas-mx-v1_1.tsv`, un reactivo que probara el `PORQUE` de la regla ("el hueco es logístico, no actitudinal") de forma directa, no solo el `SI...ENTONCES`.**

`adultos_ensanut2024_w.dta` trae un bloque de razón-de-no-vacunación, por vacuna nombrada (Influenza/Neumococo/Tétanos/Otra), cinco motivos declarados por reactivo, líneas 27885-27904:

| sufijo | motivo verbatim (patrón, cinco por vacuna) |
|---|---|
| `a0927?1` | «¿Qué vacuna fue la que no le aplicaron porque **no había vacunas**…» — **disponibilidad, antecedente negado directamente observado** |
| `a0927?2` | «…por **no ser derechohabiente**…» — barrera institucional/logística |
| `a0927?3` | «…porque **no estaba la persona que aplica**…» — barrera de personal, logística |
| `a0927?4` | «…porque **estaba enfermo**…» — contraindicación médica, no logística ni actitudinal |
| `a0927?5` (letra `e`, `?`=a-e por vacuna) | «…por **otra razón**…» — residual, sin discriminar |

*(sufijos exactos `a0927a1`…`a0927e4`, `data/inventario-reactivos-descargas-mx-v1_1.tsv:27885-27904` — caja confirma contra el codebook la asignación letra→vacuna, que el inventario no despliega en una sola fila legible)*

**Por qué esta rama es una mejora, no solo una cita.** La regla predice que, entre quienes **no** se vacunaron, la razón dominante debe ser logística (`a0927?1`/`a0927?3`, disponibilidad/personal) y no actitudinal (rechazo, miedo, desconfianza — ninguna de las cinco categorías nombradas es explícitamente actitudinal, lo cual es en sí mismo un dato: si `ENSANUT2024` no ofrece una categoría de rechazo, eso también es una restricción a declarar, no a inventar). Es una prueba **de una sola muestra** (proporción de razones dentro de los no vacunados), no un cruce antecedente×desenlace — más simple y más directamente ligada al `PORQUE` que la Rama A, que depende de un supuesto de diseño no confirmado (§0.3).

### 2.1 · Universo y ponderador — Rama B

`adultos_ensanut2024_w.dta`, personas de **20 años o más** (`manifiesto.yaml:1232-1236`, sección del cuestionario confirmada). Ponderador/estrato/UPM: `ponde_f`/`estrato`/`est_sel`/`upm` — mismo diseño muestral que `S6 §2.3` ya estableció para los módulos de persona de `ENSANUT2024`, no re-derivado.

**Universo del falsador:** personas de 20+ que reportan **no** haber recibido alguna de las vacunas nombradas (`a0904`/`a0906`/`a0917`/`a0919a`, etc., §2.2) y que por tanto responden el bloque `a0927`.

---

## 2.2 · Rama C — `ENSANUT2024` adolescentes (corroboración de tasa, sin antecedente propio, per `N10 §2.5`)

`adolescentes_ensanut2024_w.dta`, personas de **10-19 años** (`manifiesto.yaml:1208-1211`), sección `NOTA5 SECCIÓN 5. VACUNACIÓN` (`data/inventario-reactivos-descargas-mx-v1_1.tsv:27250-27318`):

| variable | línea | texto verbatim |
|---|---|---|
| `d0321j` | 27185 | «Durante el embarazo, te vacunaron contra el tétanos?» |
| `d0321p` | 27186 | «Durante el embarazo, te vacunaron Tdap (contra tosferina)?» |
| `d0508` | 27264 | «Te han aplicado la vacuna contra el VPH…» |
| `d05041`/`d05051` | 27256/27258 | «Antes/A partir de los 10 años de edad, ¿te han aplicado la vacuna contra el Tétanos?» |

Sin disparador de disponibilidad propio en este bloque (`N10 §2.5` ya lo declaró así: "refuerza lo que N5 ya tenía por otra vía, no lo cambia"). Se cita como **tercer instrumento de tasa de aceptación** (§4), población adolescente embarazada/en edad de esquema, no como falsador antecedente×desenlace independiente.

---

## 3 · Dicotomizaciones y celdas

**Rama A** (sujeta a §0.3): `DISPONIBLE` = costo reportado (`ce19d_2`/`hs16d_2`) = 0 (gratis) vs. `>0` (pagó) — corte conceptual, pendiente de codebook para confirmar unidades/moneda. `ACEPTA` = `cen12_1a`=1 (recibió vacunación en consulta) o `he25c`=1 (recibió vacuna tétanos en embarazo).

**Rama B** (falsador de una sola muestra, no de cruce): `RAZON_LOGISTICA` = 1 si la razón marcada es `a0927?1` (no había vacunas) o `a0927?3` (no estaba quien aplica); `RAZON_NO_LOGISTICA` = 1 si es `a0927?2` (no derechohabiente — institucional, se reporta aparte, ni logística de suministro ni actitudinal), `a0927?4` (enfermedad) u `a0927?5` (otra). Proporción de `RAZON_LOGISTICA` sobre el total de razones declaradas, por vacuna y agregada.

**Rama C:** proporción de `d0321j`/`d0321p`/`d0508`/etc. = 1 (aceptó), sin cruce contra disponibilidad — descriptivo, corrobora la magnitud de aceptación que la regla predice ("la mayoría acepta").

**Cota de n mínima por celda:** numerador `<10` ⇒ `NO-ESTIMABLE`, misma guardia que el resto de esta serie.

---

## 4 · Falsador `B-bis`

| | Rama A | Rama B (primaria de esta pieza) | Rama C |
|---|---|---|---|
| **Signo esperado** | `ACEPTA` mayor donde `DISPONIBLE`=1 (gratis) que donde `DISPONIBLE`=0 (pagó) — **si §0.3 confirma que el disparador es post-tratamiento, esta fila queda `NO-CONSTRUIBLE`, no `NO-DISCRIMINA`: son cosas distintas** | `RAZON_LOGISTICA` > 50% de las razones declaradas (mayoría del hueco es logístico) | proporción de aceptación alta (>50%), sin signo direccional que refutar — solo magnitud |
| **`CORROBORADA`** | IC95 de la diferencia excluye 0 en signo positivo | IC95 de la proporción `RAZON_LOGISTICA` excluye 50% por arriba | proporción con IC95 por arriba de 50% |
| **`CONTRARIA`** | IC95 excluye 0 en signo negativo | IC95 excluye 50% por abajo — mayoría de razones **no** logísticas (`enfermedad`/`otra`/`no derechohabiente` dominan) | proporción con IC95 por debajo de 50% |
| **`NO-DISCRIMINA`** | IC95 contiene 0 | IC95 contiene 50% | IC95 contiene 50% |
| **`NO-ESTIMABLE`** | numerador `<10` en alguna celda, **o** `NO-CONSTRUIBLE` si §0.3 confirma post-tratamiento — **fila que `B-bis` exige, qué pasa si no refuta:** el veredicto de esta pieza sale de la Rama B, que no depende de la resolución de §0.3; la Rama A queda declarada como pendiente de diseño, no como refutación | numerador total `<10` (poco probable, dado que `N10` ya reporta 268 filas de `vacun\w+` solo en el inventario, aunque eso cuenta variables, no observaciones) | numerador `<10` |

**Qué significaría corroborar la Rama B.** Sería la primera prueba directa del `PORQUE` de esta regla en todo el corpus — ni `N5` ni `N10` llegaron a este reactivo (ninguno de los dos cita `a0927` ni el módulo de razón-de-no-vacunación). Confirmaría, con el texto exacto del propio instrumento, que el default es aceptación y que el hueco, cuando ocurre, es mayormente de suministro/personal — no de rechazo. Refutarla (mayoría `enfermedad`/`otra`/`no derechohabiente`) no necesariamente contradice el `SI...ENTONCES` de la regla (disponibilidad→aceptación), pero sí debilitaría el `PORQUE` tal como está escrito.

**Reserva, declarada antes de medir.** Todas las ramas son transversales, sin identificación causal. Rama B es de una sola muestra (no compara grupos) — mide la composición de razones, no un contraste; se declara así para que caja no intente forzar un IC95 de diferencia donde no hay dos grupos que comparar. El corte de `DISPONIBLE` en Rama A y la asignación letra→vacuna en Rama B quedan pendientes de codebook.

---

## 5 · `se_mueve_si`

**Rama B (primaria):** si entre las personas de 20+ que no recibieron una vacuna nombrada, la razón declarada **no** es mayoritariamente logística (suministro/personal) sino actitudinal o de otro tipo, la regla se rompe en su `PORQUE`. **Rama A** (si §0.3 confirma que es construible): si `ACEPTA` no es mayor donde el servicio es gratuito que donde tiene costo, se rompe en el `SI...ENTONCES`. **Rama C:** si la proporción de aceptación cae sustancialmente por debajo de "la mayoría", el `ENTONCES` de la regla ("la mayoría acepta") pierde soporte descriptivo, aunque esta rama no cruza contra disponibilidad.

---

## 6 · Archivos que la caja necesita abrir

**Rama A:**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `ennvih1_2002_hogar_dta` | `ennvih/ehh02dta_all.zip` | `8b9b51904ca8790421d82a8a81f7f4edbce9a296cba2ce86fef74f8f379b5923` |
| `ennvih2_2005_hogar_dta` | `ennvih/ehh05dta_all.zip` | `fc4ea4ae7d0cf4bc906bb46ad5e1e7444b9c24f8e0c569ae3f6e5a9b72453c1a` |
| `ennvih3_2009_hogar_dta` | `ennvih/ehh09dta_all.zip` | `00a7649a1839a3523be22612c2fa3555d5e743cf5329d6bcdc432b901e98bd15` |
| `ennvih1_2002_ponderador` | `ennvih/ehh02w_all.zip` | `bbe8006844f715c19b724ebb74f1408c4cfa07e2efdfe7d6748b5182ef214587` |
| `ennvih3_2009_ponderador_transversal` | `ennvih/ehh09w_all.zip` | `e7929b49a7cd4f1eae5aa17da77c7eea4794d0f26265fbd40dde5e9c8e3ef8b8` |

**Rama B/C:**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `adultos_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/adultos_ensanut2024_w.stata.stata.zip` | `0fa8f4436fa427cc23d1d43164d449462c09eb787cb45ad20961576cb095a6c4` |
| `adolescentes_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/adolescentes_ensanut2024_w.stata.stata.zip` | `47251c90bd411e6d8c6f12dd5761ff928341eee310fe9dd5ba0c841e83e2bb27` |

No hay codebook de `ENNVIH` registrado por separado en esta pieza (mismo pendiente que `S6 §6`). `ENSANUT2024` trae cuestionarios PDF ya citados por actos anteriores (`MAESTRA37-L1`/`L3`) — no re-listados aquí.

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6. No calcula ninguna celda, proporción ni IC95. No mueve el tier de `salud.vacunacion.disponible` (`[FUERTE]`, línea 575) ni sella `MEDIBLE-COMO-ESTÁ`. No corrige el dominio de la regla en `canon/modelo-decision-v4_0.md` — la corrección de mapa (§3.9, no §3.4) vive en `canon/registro-rotulos.tsv` (P3 de este mismo acto `MAESTRA38-N11`), no aquí. No confirma ni descarta si la Rama A es construible (§0.3) — declara el riesgo, caja lo resuelve. No reclasifica `salud.atencion.grave` ni `comunicacion.inseguridad.ver_oir_callar` (`S6`/`S8`, mismo lote, piezas separadas). No toca `canon/modelo-decision-v4_0.md`, `milpa/**`, `data/**` ni `forense/hallazgos.md`.

**Medición: caja, acto `MAESTRA38-L17`** (rótulo derivado por continuidad de la serie `L`, máximo registrado hoy `L14`; `L15` deliberadamente sin usar — `N10 §2.4`; `L16`/`L18` van a `S6`/`S8` de este mismo lote, contiguos).

**El primer resultado que produzca este procedimiento es el que se reporta — de cada rama, por separado.**

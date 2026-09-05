# S8 · Pre-registro de `comunicacion.inseguridad.ver_oir_callar` — medible como está (hallazgo nuevo de `N10`)

### `prereg-caja-S8-L18` · **v1.0** · 5 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S8-L18-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S8-L18`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`/`.sav`, de un falsador **de una sola ola (LAPOP México 2004)** para `comunicacion.inseguridad.ver_oir_callar` (`R10.3`): contexto de inseguridad/autoridad no confiable (`AOJ11`/`B18`/`AOJ12`) × denuncia (`aoj1`), sobre el subuniverso de víctimas (`vic1`) que el propio módulo `AOJ` de LAPOP filtra. |
> | **QUÉ NO ES** | No abre ningún `.dta`/`.sav` — los payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el tier de `comunicacion.inseguridad.ver_oir_callar` (hoy `[FUERTE]`, `canon/modelo-decision-v4_0.md:585`) — la clasificación `MEDIBLE-COMO-ESTÁ` que `forense/notas/2026-09-05-MAESTRA38-N10-cobertura-ola6.md §2.6` propone sigue **propuesta, dirección/mesa revisa**; este documento no la sella. No extiende el falsador a 2006/2019/2021/2023 — §0.1 corrige por qué esas cuatro olas no satisfacen el criterio (a) para esta regla, aunque sí contribuyan a la batería de antecedente como contexto. |
> | **VERIFICAS ASÍ** | Caja, al abrir el payload de §6, compara variable y texto contra §1; confirma si `aoj1` está, en efecto, condicionado en el `.dta` al filtro de victimización (`vic1`) que `L9`/`L11`/esta pieza asumen por diseño de cuestionario LAPOP, y reporta como hallazgo — no como guardia ya sabida — el tamaño real del subuniverso de víctimas 2004 (nadie en el corpus lo ha contado todavía, ver §0.2). |

**Acto:** `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`, 5/sep/2026, entorno **NUBE**, sobre `origin/main = b17d19bd1d566220ac81ebbac47c1c80ae14d66e` (SHA de redacción del encargo).

---

## 0 · Ficha bajo prueba y corrección de premisa (A.8/D-13)

### 0.1 · Definición vigente y cadena de clasificación

`canon/modelo-decision-v4_0.md:585` (§3.10 Comunicación y conflicto), verbatim:

> *SI el contexto es de inseguridad/autoridad no confiable ENTONCES "ver, oír y callar" — PORQUE G4 (adaptación racional, no timidez) — `[FUERTE]`.* · **id:** `comunicacion.inseguridad.ver_oir_callar`

Verificación previa (A.8, `tools/ya_medido.py`, corrida contra este `id` el 5/sep/2026 desde `origin/main = b17d19bd`):

```
$ python3 tools/ya_medido.py comunicacion.inseguridad.ver_oir_callar
=== ya_medido: comunicacion.inseguridad.ver_oir_callar ===
  resuelto por canon: comunicacion.inseguridad.ver_oir_callar -> R10.3
-- milpa/tramite.yaml -- (sin apariciones)
-- milpa/tramite-ola5-propuesta-v0.yaml -- (sin apariciones)
-- canon/modelo-decision-v4_0.md §7 -- R10.3 | L299 | ... | [FUERTE] | Sí
-- forense/notas/*-L*-*.md -- MAESTRA37-L1-censo.md:96, -remapeo.md:60
     (EXISTE-NO-SATISFACE como máximo, no verificado — ENDIREH `denunci*`)
-- forense/prereg-caja/S*-spec-*.md -- (sin apariciones)
-- canon/registro-rotulos.tsv (alias) -- (sin apariciones)
========================================
NUNCA-MEDIDA
```

`NUNCA-MEDIDA`, sin discrepancia: `MAESTRA34-N5` (`EXISTE-NO-SATISFACE`, ENDIREH `p6_19_1..4`, universo de violencia contra la mujer, no de inseguridad general) y `MAESTRA36-N6` (`EXISTE-NO-SATISFACE`, CNGMD, sesgo de selección — solo denuncias que ocurrieron, sin denominador de quienes callaron) coinciden en que ninguno de los dos midió esta regla; ninguno de los dos tenía asignado `descargas_mx_v1_1`, el universo donde `MAESTRA38-N10 §2.6` encuentra el módulo `AOJ` de LAPOP AmericasBarometer — **hallazgo nuevo de ese acto**, no de `N5`/`N6` (`forense/notas/2026-09-05-MAESTRA38-N10-cobertura-ola6.md:602-651`).

### 0.2 · Corrección de premisa, verificada contra el inventario (A.8/D-13) — "mismas cinco olas" no es exacto

`N10 §2.6` describe la batería de antecedente (`AOJ11`/`B18`/`B10A`/`AOJ12`) y el desenlace (`aoj1`/`aoj1a`/`aoj1b`) como medidos "en la misma encuesta, mismas cinco olas" (2004/2006/2019/2021/2023). Verificado variable por variable, ola por ola, contra `data/inventario-reactivos-descargas-mx-v1_1.tsv` (búsqueda exacta por `variable_id`, ambas capitalizaciones):

| variable | 2004 | 2006 | 2019 | 2021 | 2023 |
|---|---|---|---|---|---|
| `aoj1` (desenlace, denunció) | **X** | — | — | — | — |
| `aoj1a` (ante qué institución) | **X** | — | — | — | — |
| `aoj1b` (por qué no denunció) | **X** | — | — | — | — |
| `aoj11`/`AOJ11` (inseguridad barrio) | X | X | X | X | X |
| `b18`/`B18` (confianza policía) | X | X | X | X | X |
| `b10a`/`B10A` (confianza sist. justicia) | X | X | — | — | X |
| `aoj12`/`AOJ12` (confianza castigo) | X | X | X | — | X |

**Lo que sí es cierto:** `AOJ11` y `B18` sí están en las cinco olas. **Lo que no es exacto:** `B10A` falta en 2019/2021, `AOJ12` falta en 2021, y sobre todo — **el desenlace completo (`aoj1`/`aoj1a`/`aoj1b`) existe únicamente en la ola 2004**; ninguna de 2006/2019/2021/2023 trae la variable de denuncia del módulo `AOJ` (0 filas en las cuatro, misma búsqueda exacta). Esto no contradice la clasificación `MEDIBLE-COMO-ESTÁ` que `N10` propone — el criterio (a) (antecedente y desenlace en la misma persona, mismo instrumento) **sí se satisface**, pero **solo en 2004**, no en "las mismas cinco olas" como la prosa de `N10` sugiere de corrido. Esta pieza corrige el alcance antes de que caja lo dé por hecho: **el falsador de esta spec es de una sola ola.** 2006/2019/2021/2023 se citan en §1 solo como evidencia de que el antecedente (percepción de inseguridad/desconfianza) es un ítem estable de la batería `AOJ`/`B` a través del tiempo — no como parte del falsador.

### 0.3 · Universo del filtro de victimización — tamaño no verificado, declarado

El módulo `AOJ` de LAPOP es contingente: `aoj1` ("¿Denunció el hecho ante alguna institución?") presupone un "hecho" ya reportado — en el diseño estándar de LAPOP, la pregunta de filtro es la de victimización (`vic1` en 2004: *"¿Ha sido víctima de algún acto de delincuencia en los últimos 12 meses?"*, `forense/prereg-caja/S5-L5-spec-v1_0.md §1.1`, mismo payload). **Nadie en el corpus ha contado todavía cuántos casos de 2004 caen en ese subuniverso** — a diferencia de 2019, donde `L9 §0.5` ya reportó el marginal de `vic1ext`/`prot3` (n=1576, "sí" 112). Se pre-registra la expectativa, no el número: por la tasa de victimización típica de LAPOP México (~5-10% en otras olas ya medidas), el subuniverso de 2004 que responde `aoj1` es previsiblemente **pequeño frente a la muestra total** (~1500-1600 en la ola completa) — razón por la que §3 decompone el falsador en una celda principal y tres diagnósticas, mismo criterio que `S5 §3.1` aplicó ante el mismo riesgo.

---

## 1 · Variables, texto de reactivo verbatim (ola 2004, `1658622845Mexico 2004 Export Version.sav` / `642348348mexico 2004 export version.dta`, gemelos byte-a-byte)

**Búsqueda contra `data/inventario-reactivos-descargas-mx-v1_1.tsv`, exacta por `variable_id`, verificada por archivo:**

| variable | línea (`.sav`) | línea (`.dta`) | etiqueta verbatim |
|---|---|---|---|
| `aoj1` | 20383 | 20843 | «¿Denunció el hecho ante alguna institución?» |
| `aoj1a` | 20384 | 20844 | «¿A quién o ante qué institución denunció el hecho?» |
| `aoj1b` | 20385 | 20845 | «¿Por qué no denunció el hecho?» |
| `aoj11` | 20392 | 20852 | «Hablando del lugar o barrio donde vive, y pensando en la posibilidad de ser víctima de un asalto o robo, ¿se siente…» *(etiqueta truncada en la fuente misma — `.sav` a 117 caracteres sin puntuación de cierre, `.dta` a 81; artefacto de extracción `INSPECT_SPSS` vs. `INSPECT_STATA`, no diferencia de dato entre los dos gemelos — mismo patrón que `S5 §1.1` ya documentó para otras variables de esta misma pareja de archivos)* |
| `aoj12` | 20394 | 20854 | «Si fuera víctima de un robo o asalto, ¿cuánto confiaría en que el sistema judicial castigaría al culpable?» (`.sav`, completa, 111 caracteres; `.dta` trunca a 84) |
| `b10a` | 20407 | 20867 | «¿Hasta qué punto tiene confianza en el sistema de justicia?» |
| `b18` | 20413 | 20873 | «¿Hasta qué punto tiene confianza en la Policía?» |
| `vic1` | — | — | «¿Ha sido víctima de algún acto de delincuencia en los últimos 12 meses?» *(verbatim de `S5-L5-spec-v1_0.md §1.1`, mismo payload — no re-buscado aquí, reusado)* |

### 1.1 · Antecedente en el resto del corpus — contexto, no falsador (§0.2)

Citado como evidencia de estabilidad temporal del antecedente, **no** como parte del falsador de §4:

| ola | `AOJ11`/`aoj11` | `B18`/`b18` | `B10A`/`b10a` | `AOJ12`/`aoj12` | archivo |
|---|---|---|---|---|---|
| 2006 | `AOJ11` («AOJ11.Hablando del lugar o barrio/colonia donde vive… ¿se siente usted muy seguro, algo seguro, algo inseguro o muy inseguro?») | `B18` («B18.¿Hasta qué punto tiene confianza usted en la Policía?») | `B10A` («B10A.¿Hasta qué punto tiene confianza en el sistema de justicia?») | `AOJ12` («AOJ12.Si fuera víctima de un robo o asalto…») | `1008973606Mexico_LAPOP_final 2006 data set 092906.sav` / `518939279…dta` — **`aoj1`/`AOJ1`/`AOJ1A`/`AOJ1B`: 0 filas, verificado, ambas capitalizaciones** |
| 2019 | `aoj11` («Percepción de inseguridad en el barrio») | `b18` («Confianza en la Policía Nacional») | ausente | `aoj12` («Confianza en que el sistema judicial castigue a los culpables») | `Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` — sin `.sav` en el corpus; `aoj1`/`aoj1a`/`aoj1b`/`b10a`: 0 filas |
| 2021 | `aoj11` («Percepción de inseguridad en el barrio») | `b18` («Confianza en la policía») | ausente | ausente | `MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta` — único payload de esa ola en el corpus (sin `.sav`); `aoj1`/`aoj1a`/`aoj1b`/`aoj12`/`b10a`: 0 filas |
| 2023 | `aoj11` («Percepción de seguridad en el vecindario») | `b18` («Confianza en la policía nacional») | `b10a` («Confianza en el sistema de justicia») | `aoj12` («Si es víctima de un crimen, la fe en el sistema de justicia») | `MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta`/`.sav` (+ duplicado byte-idéntico `(1).dta`, deliberadamente fuera de todo grupo por el propio manifiesto) — `aoj1`/`aoj1a`/`aoj1b`: 0 filas en las tres |

---

## 2 · Universo y ponderador — 2004, reusado de `S5` (mismo payload, no re-derivado)

**Universo:** personas de 18+ encuestadas en LAPOP México 2004 que respondieron `vic1=1` (víctimas de delincuencia en los últimos 12 meses) y, dentro de ese subgrupo, con código válido en `aoj1` y en las variables de antecedente (§1). Tamaño real del subuniverso: **no verificado, pendiente de que caja lo cuente** (§0.3).

**Ponderador, estrato y UPM — mismos hechos que `S5-L5-spec-v1_0.md §2` ya estableció para este payload, citados, no re-buscados:**

| elemento | hallazgo (`S5 §2`) |
|---|---|
| ponderador | `wt` existe (ambos formatos), **sin etiqueta** en el inventario; nombre consistente con la convención LAPOP, **no confirmado por codebook** — ninguna corrida real lo ha verificado todavía |
| estrato | `mestrat` (estrato), sin UPM/clúster visible en la búsqueda |
| UPM/clúster | ausente en 2004 (a diferencia de 2006, que sí trae `ESTRATOPRI`/`UPM`/`CLUSTER` explícitos) |

Si caja no logra confirmar `wt` por codebook, la corrida sale **sin ponderar**, declarado — mismo criterio que `S2-L2-spec-v1_0.md §1.0` y `S5 §2` ya fijaron para payloads con ponderador no determinable.

---

## 3 · Dicotomizaciones y celdas

**`DENUNCIA`** = 1 si `aoj1` indica que sí denunció el hecho; 0 en caso contrario (la escala exacta de códigos de `aoj1` no está confirmada sin codebook — se pre-registra la regla conceptual: "sí" = 1, cualquier variante de "no" = 0; caja declara el mapeo real de códigos antes de calcular, mismo criterio que el resto de esta pieza).

**Los tres proxies del antecedente se tratan como operacionalizaciones alternativas de un mismo constructo** —"contexto de inseguridad/autoridad no confiable"—, no como antecedentes conjuntos que deban cumplirse todos a la vez (a diferencia de `civico.protesta.agravio_urbano` en `S5`, donde los cuatro antecedentes son términos distintos del mismo `SI`). El texto de la regla no exige que las tres fuentes de inseguridad/desconfianza coincidan; exige que el contexto, medido por cualquiera de sus caras, esté presente:

- **`INSEGURO_BARRIO`** = 1 si `aoj11` cae en la mitad de la escala que indica "algo inseguro"/"muy inseguro" (corte exacto pendiente de codebook, misma regla conceptual que `S5 §3` usa para sus propias dicotomizaciones: mitad inferior de la escala de seguridad = inseguro).
- **`DESCONFIA_POLICIA`** = 1 si `b18` cae en la mitad inferior de confianza.
- **`DESCONFIA_JUSTICIA`** = 1 si `aoj12` (confianza en que el sistema castigaría al culpable) cae en la mitad inferior de confianza. (`b10a`, confianza general en el sistema de justicia, se reporta en paralelo como verificación cruzada de `aoj12` — ambas existen en 2004 — sin sustituir la dicotomización principal, mismo criterio que `S5 §3` aplicó a `ur`/`TAMANO`.)

**`INDICE_CONTEXTO`** (celda principal) = número de los tres indicadores de arriba en la dirección de inseguridad/desconfianza (0 a 3). Dicotomizado: `ALTO` = 2 o 3 de 3; `BAJO` = 0 o 1 de 3.

### 3.1 · Celdas

**Celda principal:**

```
C_completo = P(DENUNCIA=0 | INDICE_CONTEXTO=ALTO) − P(DENUNCIA=0 | INDICE_CONTEXTO=BAJO)
```

(la variable de interés es el **silencio** — "ver, oír y callar" — no la denuncia; `DENUNCIA=0` es el desenlace que la regla predice bajo contexto de inseguridad alto).

**Guardia de celda, anticipada (§0.3):** el subuniverso ya es víctimas únicamente (probablemente 5-10% de la muestra 2004); exigir además `INDICE_CONTEXTO=ALTO` reduce más el numerador. Es razonable esperar que una o ambas celdas caigan bajo la guardia de `n<10` — se declara ahora, no después, mismo criterio que `S5 §3.1`.

**Celdas diagnósticas (2×2 cada una, contra `DENUNCIA`), para que la caída de `C_completo` no deje la pieza sin nada que reportar:**

- `C_barrio` = `INSEGURO_BARRIO` × `DENUNCIA` (el proxy presente en las cinco olas — si `C_completo` cae por guardia, esta es la celda con más posibilidad de sobrevivir por tener el numerador más grande de las cuatro, al exigir un solo indicador en vez de dos de tres).
- `C_policia` = `DESCONFIA_POLICIA` × `DENUNCIA`.
- `C_justicia` = `DESCONFIA_JUSTICIA` × `DENUNCIA`.

**Cota de n mínima por celda:** numerador `<10` ⇒ `NO-ESTIMABLE`, misma guardia que `S4 §3`/`S5 §3.1`/`L9 §1.3` fijan.

---

## 4 · Falsador `B-bis`

| | |
|---|---|
| **Signo esperado** | `C_completo > 0`, `C_barrio > 0`, `C_policia > 0`, `C_justicia > 0` — el silencio (`DENUNCIA=0`) es más frecuente entre quienes perciben el contexto como inseguro/la autoridad como no confiable que entre quienes no |
| **`CORROBORADA`** | `C_completo` estimable, con IC95 que **excluye** 0 en signo positivo |
| **`CONTRARIA`** | `C_completo` estimable, con IC95 que excluye 0 en signo **negativo** — el silencio es **menos** frecuente bajo contexto inseguro, contra lo que el `SI` predice |
| **`NO-DISCRIMINA`** | IC95 de `C_completo` contiene 0 |
| **`NO-ESTIMABLE`** | alguna de las dos celdas de `C_completo` (víctimas con `INDICE_CONTEXTO` alto o bajo) cae bajo la guardia de numerador — **fila que `B-bis` exige, qué pasa si no refuta:** el veredicto sale de las tres celdas diagnósticas tomadas juntas, no de `C_completo`, y se declara explícitamente que **el corazón de la regla — que el contexto, no un antecedente aislado, es lo que canaliza el silencio — no se midió**; mismo criterio de declaración que `S5 §4`/`L9 §4.1` fijaron para sus propios diseños compuestos que cayeron por guardia |
| **Precedencia entre las tres diagnósticas** | si las tres van limpias y en el mismo signo positivo, se reporta como corroboración **convergente por proxy**, nunca como corroboración de `C_completo` — no se sustituye lo compuesto por la suma de lo simple (mismo criterio que `S5 §4`). Si alguna diagnóstica da signo negativo limpio, manda `CONTRARIA` sobre esa pieza específica y se reporta el desacuerdo entre proxies, sin forzar un veredicto único |

**Qué significaría corroborar `C_completo`.** Sería la primera falsación real de esta regla — nadie, en `N5`, `N6` ni `N10`, ha corrido un número contra ella (§0.1, `NUNCA-MEDIDA`; verificado además por barrido de `forense/notas/*.md` que ningún acto anterior corrió el contraste `AOJ11`/`B18`/`AOJ12`/`B10A` → `aoj1` para este `id`). Cerraría, con reserva de instrumento (una sola ola, universo de víctimas no contado — §0.3), el hueco que `N5`/`N6` dejaron sobre este `id` por examinar universos ajenos (ENDIREH restringido a violencia de género; CNGMD con sesgo de selección).

**Reserva, declarada antes de medir.** Asociación transversal, sin identificación causal — mismo tipo de limitación que `S4`/`S5` ya declararon. El `PORQUE` de la regla ("adaptación racional, no timidez") es mecanismo, no antecedente exigible — no se mide en este falsador, mismo criterio que `N10 §2.6` aplicó y que `S1-A2`/`salud.atencion.grave` (§4 de `S6`, este mismo lote) también siguen. El corte de las tres dicotomizaciones (`INSEGURO_BARRIO`/`DESCONFIA_POLICIA`/`DESCONFIA_JUSTICIA`) queda pendiente de codebook; si el codebook revela una escala con orden distinto al asumido, la recodificación **no se hereda a ciegas** — caja lo declara como hallazgo antes de calcular.

---

## 5 · `se_mueve_si`

Si entre las víctimas de 2004 la tasa de silencio (no denuncia) en contexto de alta inseguridad/desconfianza (`INDICE_CONTEXTO=ALTO`) **no es mayor** que en contexto bajo, la regla se rompe. Si `C_completo` cae por guardia (`NO-ESTIMABLE`), `se_mueve_si` se lee sobre las tres diagnósticas juntas, per §4.

---

## 6 · Archivos que la caja necesita abrir

**Requeridos para el falsador (ola 2004):**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `1658622845mexico_2004_export_version` | `Descargas Manuales/1658622845Mexico 2004 Export Version.sav` | `e725383552753223d263a1d65e2aaf9549a59859eb1b5777b666f32728700c99` |
| `642348348mexico_2004_export_version` | `Descargas Manuales/642348348mexico 2004 export version.dta` | `ef46b8f5a3c565c931d8ab1d173b2ee34f9f9459987159861ee4e24bf01b9880` |
| `1671516622cam_mexico_questionnaire_2004` | `Descargas Manuales/1671516622CAM Mexico Questionnaire 2004.pdf` (cuestionario 2004, para confirmar códigos de `aoj1`/`aoj1a`/`aoj1b` y las escalas de `aoj11`/`b18`/`aoj12`) | `452677a69fe522b8ae9f4eaa779bb62f1b9a8a7df0ca8a359d3028715dd55843` |
| `682647031technical_information_mexico_2004` | `Descargas Manuales/682647031Technical information_Mexico_2004.pdf` | `327716b8bc4eee1f4efe011cd41c18ef80c7416e279294807eedf3fffa48d8da` |

**No requeridos para el falsador — solo contexto de §1.1 (tendencia del antecedente, no del desenlace):**

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `1008973606mexico_lapop_final_2006_data_set_092906` | `Descargas Manuales/1008973606Mexico_LAPOP_final 2006 data set 092906.sav` | `f43fcf78533febabe4eacb539f0ed03470c8320d606f29f54c220cda5abb3039` |
| `518939279mexico_lapop_final_2006_data_set_092906` | `Descargas Manuales/518939279mexico_lapop_final 2006 data set 092906.dta` | `e426210067f9dba8aca87a0df2161bc7389cc5aaf9e5516aa7ebf9cb52f149fa` |
| `mexico_lapop_americasbarometer_2019_v1_0_w` | `Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` | `c88f79ebb8e73c473cd78d894eb093261f172e736a35bd7bc677b4e8b1454a57` |
| `mex_2021_lapop_americasbarometer_v1_2_w` | `Descargas Manuales/MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta` | `153fb0f81acfffb41bbe247b7fce81159350e1fdfcb342a14bb034bcb7d95566` |
| `mex_2023_lapop_americasbarometer_v1_0_w` | `Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta` | `4a9410a53cde9d11edeb23465bdbadce8a6abcc18330b6eebe2a4493be6e765c` |
| `mex_2023_lapop_americasbarometer_v1_0_w_2` | `Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.sav` | `a355e4ca93476d66a4138ec7f565574214fbba517de219d71ff1c2851a61fa2a` |

No hay codebook 2004 registrado por separado en el manifiesto — el "technical information" de arriba es el único documento de estructura disponible para esa ola; si no trae el mapa de valores de `aoj1`/`aoj11`/`b18`/`aoj12`, los cortes de §3 quedan sin confirmar hasta que caja abra el `.dta`/`.sav` mismo. Ninguno de los payloads de 2021/2023 trae codebook en el manifiesto tampoco (verificado, `grep -in codebook data/manifiesto.yaml` solo devuelve el de 2019) — irrelevante para este falsador, relevante solo si un acto futuro quisiera extender el antecedente-de-tendencia de §1.1.

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6. No calcula ninguna celda ni IC95. No mueve el tier de `comunicacion.inseguridad.ver_oir_callar` (`[FUERTE]`, línea 585) ni sella la clasificación `MEDIBLE-COMO-ESTÁ` que `N10` propone — dirección/mesa revisa esa propuesta por separado. No extiende el falsador a 2006/2019/2021/2023 — §0.2 declaró por qué esas olas no satisfacen el criterio (a) para esta regla (el desenlace no existe ahí), y §1.1 las cita solo como evidencia de estabilidad del antecedente en el tiempo. No cuenta el subuniverso real de víctimas de 2004 — §0.3 declara la expectativa, no el número; ese conteo es trabajo de caja. No resuelve los cortes de `INSEGURO_BARRIO`/`DESCONFIA_POLICIA`/`DESCONFIA_JUSTICIA` — quedan pendientes de codebook, declarado, no inventado. No reclasifica `salud.atencion.grave` ni `salud.vacunacion.disponible` (`S6`/`S7`, mismo lote, mismo acto — piezas separadas). No toca `canon/modelo-decision-v4_0.md`, `milpa/**`, `data/**` ni `forense/hallazgos.md`.

**Medición: caja, acto `MAESTRA38-L18` (rótulo derivado por continuidad de la serie `L` — máximo registrado hoy en `canon/registro-rotulos.tsv` es `L14`; `L15` queda deliberadamente sin usar aquí porque `N10 §2.4` ya lo propuso en prosa para el acto sucesor de las candidatas `CNGMD`/`R8.1`/`R8.4` — sin registrar todavía, pero nombrado; `L16`/`L17` van a `S6`/`S7` de este mismo lote, contiguos).**

**El primer resultado que produzca este procedimiento es el que se reporta.**

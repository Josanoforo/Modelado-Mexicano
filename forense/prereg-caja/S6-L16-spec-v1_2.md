# S6 · Pre-registro de `salud.atencion.grave` — **Rama A′**: el desenlace sí existe en ENNViH 2002, en `HS`/`CE` del Libro IIIB

### `prereg-caja-S6-L16` · **v1.2** · 7 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S6-L16-spec-v1_2.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S6-L16`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro nuevo, congelado antes de abrir ningún `.dta`, de una **Rama A′** para `salud.atencion.grave` (`R4.4`) sobre `ENNViH` 2002: **dos disparadores** (`es09`; `ec01*`) × **dos desenlaces** (`HS` hospitalización; `CE` consulta externa) = **4 celdas de contraste**, cada una en **dos brazos** de universo (`b3b` directo, `bx` proxy) que nunca se agrupan. Existe porque el universo creció (A.10): `data/inventario-reactivos-ext-v1_0.tsv` trae las secciones `HS`/`CE` del Libro IIIB, que `v1.0` y `v1.1` **no citaron** — miraron `cen10*` (sección `CEN`, libro de niños) y de ahí concluyeron `NO-CONSTRUIBLE`. |
> | **QUÉ NO ES** | **No abre ningún `.dta`/`.pdf`** — NUBE, sin corpus montado (A.2, tercera parte: `ls data/raw/` → 0 entradas). No mide, no calcula ninguna proporción ni ningún IC95. **No edita ni retira `v1.0` ni `v1.1`** — quedan íntegras en sus rutas (A.10); `v1.2` las **enmienda con fecha**, no las reescribe. No mueve el tier de `R4.4` (hoy `[MEDIA]`, `canon/modelo-decision-v4_0.md:747`) ni toca el canon. **No reabre `FP-332`** (esa firma es de `SELLO-3`). **No pre-registra 2005 ni 2009** — ver §7, donde se corrige el hecho que el encargo afirmó sobre esas olas y se declara, aun así, que no entran. |
> | **RELACIÓN CON `v1.1`** | `v1.1` **no queda mal**: su Rama A (disparador `es09` + desenlace `cen10*`/`clave1`/`clave2`) corrió, cumplió su propia cláusula de PARO y produjo `NO-ESTIMABLE` por dos causas. `v1.2` **no rescata esa rama**: abre una **distinta**, con **otro desenlace**, que el barrido de aquel acto no examinó (§0.3). |

---

## 0 · Corrección de premisa (A.8 / A.10 / A.13)

### 0.1 · Definición vigente bajo prueba

`canon/modelo-decision-v4_0.md:241` (§3.4 Salud y cuerpo), verbatim:

> *SI el síntoma es **grave o crónico complejo** ENTONCES busca el **sistema público** pese a la espera — PORQUE la complejidad excede al consultorio — `[MEDIA]`.* · **id:** `salud.atencion.grave`

**A.8 contra medición ya corrida (`ADR-340`) — salida cruda, corrida al redactar esta pieza (7/sep/2026, `origin/main = 604793fa`):**

```
$ python3 tools/ya_medido.py R4.4
=== ya_medido: R4.4 ===
  resuelto por canon: R4.4 -> id `salud.atencion.grave` (canon/modelo-decision-v4_0.md §3, tag **id:**)
  términos de búsqueda (match exacto): R4.4, salud.atencion.grave

-- milpa/tramite.yaml --
  (sin apariciones)

-- milpa/tramite-ola5-propuesta-v0.yaml --
  :3649  situacion=PENDIENTE-DE-MESA tier=PENDIENTE-DE-MESA
         veredicto=veredicto_Bbis=NO-DISCRIMINA; veredicto_del_acto=> p=0.522295
      id: salud.atencion.grave_ensanut2024
  :3818  situacion=PENDIENTE-DE-MESA tier=PENDIENTE-DE-MESA
         veredicto=veredicto_Bbis=NO-ESTIMABLE; veredicto_del_acto=>
      id: salud.atencion.grave_ennvih2002

-- canon/modelo-decision-v4_0.md §7 --
  :747  tier=[MEDIA]
      | `R4.4` | L241 | Grave/crónico complejo → sistema público pese a la espera | `[MEDIA]` | No |

-- forense/notas/*-L*-*.md --
  MAESTRA37-L1-censo.md:70 · MAESTRA37-L1-remapeo.md:25 ·
  MAESTRA37-L3-BIS-veredictos.md:59,67,248
```

Resuelve `R4.4 → salud.atencion.grave` y lista, en `milpa/tramite-ola5-propuesta-v0.yaml`, **dos** entradas del mismo id ya con veredicto:

| entrada | situación | veredicto |
|---|---|---|
| `salud.atencion.grave_ensanut2024` (Rama B, `v1.0`/`v1.1`) | `PENDIENTE-DE-MESA` | `NO-DISCRIMINA` |
| `salud.atencion.grave_ennvih2002` (Rama A, `v1.1`) | `PENDIENTE-DE-MESA` | `NO-ESTIMABLE` |

**El `ENTONCES` de `R4.4` no tiene hoy ninguna medición que lo sostenga.** Esa es la vacante que esta Rama A′ se pre-registra para llenar o para cerrar.

### 0.2 · Qué dijeron `v1.1` §0.3 y §3 — cita literal

`v1.1` §0.3, verbatim:

> *«**`cen10d_1`/`cen10l_1`/`cen10m_1`/`cen10e_1`/`cen10p_1` son, sin excepción, identificadores geográficos** — dirección, localidad, municipio, estado, país del lugar de consulta — **ninguno codifica tipo de institución** (IMSS/ISSSTE/privado/Seguro Popular). Las únicas variables de ese mismo módulo que sí nombran una institución (`clave1` "ID CLINICA COMUNITARIO", `clave2` "ID PROVEEDOR SALUD COMUNITARIO") existen **solo en la ola 2002** […]. **El desenlace "sistema público" del `SI...ENTONCES` no está en `cen10*` por sí solo** — requeriría cruzar contra un directorio externo de establecimientos […].»*

`v1.1` §3, verbatim:

> *«`BUSCA_PUBLICO` — no construible directamente de `cen10*` (§0.3); se pre-registra como **`NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO`** salvo que caja confirme `clave1`/`clave2` (solo 2002) como suficiente.»*

**Las dos afirmaciones son ciertas sobre `cen10*`, `clave1` y `clave2`, y se sostienen.** `clave1`/`clave2` son, en efecto, llaves de entrada a un directorio comunitario externo, no una clasificación público/privado. Lo que **no** se sostiene es la **conclusión más ancha** que se derivó de ellas — que el desenlace de `R4.4` no existe en `ENNViH` 2002. Corolario 2 de A.10, aplicado a esta pieza: *la conclusión de un cierre no puede ser más ancha que su universo declarado.* El universo de aquel barrido fue la **sección `CEN` del libro de niños** (`v_cen1.dta`) más el rastreo de `clave1`/`clave2`; el desenlace vive en **otras dos secciones del Libro IIIB de adultos** que ese universo no incluyó.

### 0.3 · El recibo `FP-332` `D2`, reclasificado: `NO-ENCONTRADO POR ESE BARRIDO`, no `NO-EXISTE`

`forense/notas/2026-09-07-MAESTRA38-L16-BIS-2-resultados.md`, disparador `D2`, verbatim:

> *«**Control positivo del barrido:** se recorrieron las etiquetas de todos los `.dta` de 2002 buscando `PUBLIC|PRIVAD|IMSS|ISSSTE|SSA|SEGURO SOCIAL|SECTOR`. El barrido **sí encuentra** aciertos —`iiib_ca.dta` `ca02a`/`ca02b`/`ca02e`/`ca02f` («TIENE SEGURO IMSS/ISSSTE/PRIVADO…»), `iiia_tb.dta` `tb33p_d-f`, `ii_nna1.dta` `nna20c/d`, `iiia_ed.dta` `ed241-244` («PRIMARIA PUBLICA/PRIVADA/ABIERTA»)—, así que no es un falso negativo del método. Pero **todos** son **stock de aseguramiento** o **tipo de escuela**: ninguno pregunta **a dónde acudió** tras el síntoma.»*
>
> *«**El desenlace de `R4.4` no existe en `ENNVIH` 2002.**»*

**Ese barrido, corrido de nuevo hoy sobre el inventario `ext`, contradice su propia lista.** Comando y salida verbatim, sobre las **5 425** filas de `ehh02dta_all.zip` del inventario (**137** miembros `.dta` distintos — A.13, el negativo declara qué examinó):

```
$ awk -F'\t' '$5 ~ /^ehh02dta_all\// {print}' data/inventario-reactivos-ext-v1_0.tsv > /tmp/o2002.tsv
$ wc -l < /tmp/o2002.tsv                      # 5425 filas
$ cut -f5 /tmp/o2002.tsv | sort -u | wc -l    # 137 miembros .dta
$ grep -ciE "PUBLIC|PRIVAD|IMSS|ISSSTE|SSA|SEGURO SOCIAL|SECTOR" /tmp/o2002.tsv
162
$ grep -iE "PUBLIC|PRIVAD|IMSS|ISSSTE|SSA|SEGURO SOCIAL|SECTOR" /tmp/o2002.tsv \
    | cut -f5 | sed 's#.*/##' | sort | uniq -c | sort -rn
     41 iiib_ca.dta
     30 p_ca.dta
     14 p_ce.dta
     13 iiia_tb.dta
     10 iiib_ce.dta
      9 v_cen.dta
      9 p_tb.dta
      9 p_hs.dta
      8 v_hsn.dta
      7 iiib_hs.dta
      4 iiia_ed.dta
      3 ii_nna1.dta
      2 c_cv.dta
      1 v_hsn1.dta
      1 v_cen1.dta
      1 iiib_ce1.dta
```

**El mismo regex del control positivo devuelve 40 aciertos en `iiib_ce`/`iiib_hs`/`p_ce`/`p_hs`** — exactamente las variables de «a dónde acudió» —, y el recibo `D2` **no listó ninguno** de esos cuatro archivos. Muestra literal de esos aciertos:

```
ehh02dta_b3b/iiib_hs.dta   hs02a  INTERNADO SSA
ehh02dta_b3b/iiib_hs.dta   hs02c  INTERNADO ISSSTE
ehh02dta_b3b/iiib_hs.dta   hs02e  INTERNADO HOSPITAL PRIVADO
ehh02dta_b3b/iiib_ce.dta   ce04a  CONSULTA SSA
ehh02dta_b3b/iiib_ce.dta   ce04b  CONSULTA IMSS
ehh02dta_b3b/iiib_ce.dta   ce04c  CONSULTA ISSSTE
ehh02dta_b3b/iiib_ce.dta   ce04e  CONSULTA CLINICA PRIVADA
ehh02dta_b3b/iiib_ce.dta   ce04f  CONSULTA MEDICO PRIVADO
ehh02dta_bx/p_hs.dta       hs02a  INTERNADO SSA
ehh02dta_bx/p_ce.dta       ce04a  CONSULTA SSA
```

**Convergencia independiente, registrada al sincronizar con `origin/main = d9533129` (nota fechada, 7/sep/2026).** `ACTO MAESTRA38-SELLO-3` (`PR #594`) fusionó mientras esta pieza se redactaba y **llegó por su cuenta a la misma reclasificación**, con la misma razón: su firma de `FP-332` dice, verbatim, *«D2 se corrige: la clasificacion pasa de "no existe" a NO-ENCONTRADO POR ESE BARRIDO — el recibo no declaro cuantos archivos examino y el inventario lo contradice (A.13; ver `data/inventario-reactivos-ext-v1_0.tsv`, `iiib_hs.dta`/`iiib_ce.dta`)»*, y `FP-332` quedó **`FIRMADA-PARCIAL`** (`D1` firmada como conducta correcta). **La reclasificación no la hace esta spec: ya está firmada en `main`.** Lo que esta pieza añade sobre ella es el conteo del barrido que `SELLO-3` no publicó —162 aciertos en 16 archivos, 40 en los cuatro archivos del desenlace, sobre 5 425 filas y 137 miembros `.dta`— y las dos lecturas posibles de la discrepancia. Dos caminos independientes que coinciden en el mismo hecho es corroboración, no duplicación; y **ninguno de los dos reabre `FP-332`**.

**Reclasificación, y sólo esta.** El `D2` de `FP-332` pasa de **`NO-EXISTE`** a **`NO-ENCONTRADO POR ESE BARRIDO`** (A.13 + A.5 aplicada a un artefacto: el fallo de un barrido es un hecho sobre el barrido, no sobre la fuente). Se reclasifica **el veredicto de existencia del desenlace**, nada más: el `NO-ESTIMABLE` de `v1.1` **no se toca** — su disparador `D1` (el chequeo de consistencia del ponderador) falló por su cuenta y era suficiente por sí solo (§3.3). `FP-332` **no se reabre**: su firma es de `SELLO-3`, y esta pieza no la pide.

⚠️ **La causa raíz, nombrada.** El regex del barrido `D2` sí habría encontrado estas variables; lo que no cuadra es la **lista de aciertos que el recibo publicó**. Dos lecturas posibles, ninguna adjudicable desde la nube sin re-correr el barrido contra el `.dta` real: (a) el barrido examinó menos archivos de los que dijo, o (b) examinó todos y el reporte de aciertos se truncó a mano. La spec **no adjudica cuál**; deja el hecho medido —el regex del propio control positivo devuelve 40 aciertos en los cuatro archivos que el recibo omitió— y el trabajo de re-correrlo contra el `.dta` a `L21`, que abre esos mismos archivos de todas formas.

### 0.4 · Nota de etiquetas (léela antes de escribir un regex sobre esta encuesta)

`iiib_hs.dta`/`iiib_ce.dta` escriben **`IMMS`**, no `IMSS`, en las etiquetas de 2002 del libro `b3b` (`hs02b` «INTERNADO IMMS», `ce04b` «CONSULTA IMSS» — sí, difieren entre secciones del **mismo libro**). `iiib_hs.dta` `hs02f` escribe «INTERNADO **CONsultorio** PRIVADO», con mayúsculas mezcladas. Un barrido por etiqueta que busque `IMSS` pierde `hs02b`. **Esta spec clasifica por `variable_id`, nunca por etiqueta** — las etiquetas se citan como evidencia, no como criterio.

---

## 1 · Disparadores — **dos, POR SEPARADO**

**No se combinan en un índice.** La regla dice «grave **o** crónico complejo»: son **dos lecturas** de la misma cláusula, y se reportan como dos disparadores independientes. Sumarlas en un índice haría irrecuperable cuál de las dos mueve el resultado.

### T1 · «grave» — `es09`

| brazo | archivo | variable | etiqueta verbatim |
|---|---|---|---|
| `b3b` | `ehh02dta_all/ehh02dta_b3b/iiib_es.dta` | `es09` | «HA TENIDO PROBLEMA SERIO SALUD» |
| `bx` | `ehh02dta_all/ehh02dta_bx/p_es.dta` | `es09` | «HA TENIDO PROBLEMA SALUD GRAVE» |

`T1 = 1` si `es09 == 1`; `T1 = 0` si `es09 == 0`; NS/NC y faltante quedan **fuera** de los dos grupos y **se cuentan** en el reporte (`v1.1` midió 15 NS/NC en `p_es.dta`). **El adjetivo difiere por brazo** («SERIO» en `b3b`, «GRAVE» en `bx`) — ya declarado en `v1.1` §1.1, se hereda con la cita, no se borra: es una razón más para no agrupar los brazos.

### T2 · «crónico complejo» — `ec01*`

`T2 = 1` si **al menos una** de las nueve variables de `iiib_ec.dta` (brazo `b3b`) vale 1:

| variable | etiqueta verbatim |
|---|---|
| `ec01a` | TIENE DIABETES |
| `ec01b` | TIENE HIPERTENSION |
| `ec01c` | TIENE ENFERMEDAD CORAZON |
| `ec01d` | TIENE CANCER |
| `ec01e` | TIENE ARTRITIS REUMATISMO |
| `ec01f` | TIENE ULCERA GASTRICA |
| `ec01g` | TIENE MIGRANA |
| `ec01h_1` | TIENE ENFERMEDAD CRONICA_1 (abierta) |
| `ec01i_1` | TIENE ENFERMEDAD CRONICA_2 (abierta) |

⚠️ **Corrección al encargo, declarada:** el encargo escribió «`ec01a-i`». Los nombres reales en el inventario son `ec01a`…`ec01g` más **`ec01h_1`** y **`ec01i_1`** (sufijo `_1`, las dos abiertas). Se usan los nombres reales. **`T2` no tiene brazo `bx`**: `p_ec.dta` no existe en el inventario de 2002 — el brazo proxy no preguntó crónicas. Declarado ahora: **las celdas de `T2` se reportan sólo en `b3b`**, y su ausencia en `bx` no es un `NO-ESTIMABLE`, es una ausencia de instrumento.

⚠️ **`T2` no es «complejo», es «crónico».** Ninguna de las nueve variables gradúa complejidad; migraña y diabetes entran con el mismo peso. La regla dice «crónico **complejo**». **Esta spec pre-registra `T2` como la lectura más cercana disponible y lo declara como aproximación por defecto, no como equivalencia** — si `T2` corrobora, corrobora «crónico», no «crónico complejo», y así debe reportarse.

---

## 2 · Desenlaces — **dos, POR SEPARADO**, con la tabla de clasificación congelada

### 2.1 · Regla de clasificación, y por qué hay **tres** tablas y no una

La batería de instituciones **no es la misma** en los tres archivos que la traen. Congelarla una vez y aplicarla a los tres sería el defecto exacto que esta pieza corrige en otro sitio. Verificado columna por columna en el inventario:

**Tabla A — `iiib_hs.dta` (brazo `b3b`, hospitalización). 12 categorías.**

| variable | etiqueta verbatim | clase congelada |
|---|---|---|
| `hs02a` | INTERNADO SSA | **PÚBLICO** |
| `hs02b` | INTERNADO IMMS *(sic)* | **PÚBLICO** |
| `hs02c` | INTERNADO ISSSTE | **PÚBLICO** |
| `hs02d` | INTERNADO PEMEX SEDENA | **PÚBLICO** |
| `hs02g` | INTERNADO CENTRO RURAL | **PÚBLICO** |
| `hs02e` | INTERNADO HOSPITAL PRIVADO | **PRIVADO** |
| `hs02f` | INTERNADO CONsultorio PRIVADO *(sic)* | **PRIVADO** |
| `hs02h` | INTERNADO CRUZ ROJA | OTRO |
| `hs02i` | INTERNADO CASA PRACTICANTE | OTRO |
| `hs02j` | INTERNADO CASA | OTRO |
| `hs02k_1` | INTERNADO OTRO LUGAR | OTRO |

**Tabla B — `p_hs.dta` (brazo `bx`, hospitalización). 14 categorías — batería DISTINTA de la Tabla A.**

| variable | etiqueta verbatim | clase congelada |
|---|---|---|
| `hs02a` | INTERNADO SSA | **PÚBLICO** |
| `hs02b` | INTERNADO IMSS | **PÚBLICO** |
| `hs02c` | INTERNADO ISSSTE | **PÚBLICO** |
| `hs02d` | INTERNADO PEMEX SEDENA | **PÚBLICO** |
| `hs02g` | INTERNADO **DIF** | **PÚBLICO** |
| `hs02i` | INTERNADO UNIDAD MOVIL | **PÚBLICO** |
| `hs02k` | INTERNADO DISPENSARIO MEDICO | **PÚBLICO** |
| `hs02e` | INTERNADO HOSPITAL PRIVADO | **PRIVADO** |
| `hs02f` | INTERNADO CASA MEDICO | **PRIVADO** |
| `hs02l` | INTERNADO FARMACIA | **PRIVADO** |
| `hs02h` | INTERNADO ENFERMERA | OTRO |
| `hs02j` | INTERNADO CRUZ ROJA | OTRO |
| `hs02m` | INTERNADO PRACTICANTE TRAD. | OTRO |
| `hs02n_1` | INTERNADO OTRO LUGAR | OTRO |

🛑 **La trampa que esta tabla existe para impedir, nombrada antes de abrir el dato.** El encargo prescribió, para `D-HS`, «PÚBLICO = `hs02a|b|c|d|g` vs PRIVADO = `hs02e|f`». Esa fórmula es **correcta en `iiib_hs.dta` y falsa en `p_hs.dta`**: en el brazo proxy `hs02g` es **DIF** (no «centro rural»), `hs02f` es **CASA MÉDICO** y existen `hs02h`…`hs02n_1`, que la fórmula del encargo ni siquiera nombra. Aplicar una sola fórmula a los dos brazos clasificaría mal el brazo `bx` **y coincidiría en signo por construcción**, que es justo lo que la regla de ponderadores en pareja (§3.2) pide verificar. **La corrección es de hecho verificado, no de criterio:** las clases (público/privado/otro) siguen siendo las que la dirección firmó; sólo se aplican a los nombres reales de cada archivo.

**Tabla C — `iiib_ce.dta` (brazo `b3b`) y `p_ce.dta` (brazo `bx`), consulta externa. 14 categorías, IDÉNTICAS en los dos archivos** (verificado variable por variable):

| variable | etiqueta verbatim | clase congelada |
|---|---|---|
| `ce04a` | CONSULTA SSA | **PÚBLICO** |
| `ce04b` | CONSULTA IMSS | **PÚBLICO** |
| `ce04c` | CONSULTA ISSSTE | **PÚBLICO** |
| `ce04d` | CONSULTA PEMEX SEDENA MARINA | **PÚBLICO** |
| `ce04g` | CONSULTA DIF | **PÚBLICO** |
| `ce04i` | CONSULTA UNIDAD MOVIL | **PÚBLICO** |
| `ce04k` | CONSULTA DISPENSARIO MEDICO | **PÚBLICO** |
| `ce04e` | CONSULTA CLINICA PRIVADA | **PRIVADO** |
| `ce04f` | CONSULTA MEDICO PRIVADO | **PRIVADO** |
| `ce04l` | CONSULTA FARMACIA | **PRIVADO** |
| `ce04h` | CONSULTA ENFERMERA/PARAMEDICO | OTRO |
| `ce04j` | CONSULTA CRUZ ROJA | OTRO |
| `ce04m` | CONSULTA PRACTICANTE TRADICION | OTRO |
| `ce04n_1` | CONSULTA OTRO LUGAR | OTRO |

**Congelado, y qué hace caja si no cuadra.** Estas tres tablas se cierran **aquí, antes de abrir el dato**. Si al leer el codebook (§6) caja encuentra que una etiqueta no corresponde a su clase —el caso nombrado por la dirección: que «CENTRO RURAL» no sea un establecimiento de la SSA, o que «DISPENSARIO MEDICO» resulte privado—, **lo reporta y NO reclasifica**: reclasificar después de ver el dato es elegir el resultado. La consecuencia de un desajuste es una fila de reserva en el reporte, no una tabla nueva.

**Dos decisiones de clasificación que la dirección firmó y esta spec sólo hace explícitas.** (i) `CRUZ ROJA` va a `OTRO` en las tres tablas, pese a ser asistencia no lucrativa: no es «el sistema público» del `ENTONCES`. (ii) `FARMACIA` va a `PRIVADO` en las Tablas B y C: es atención comercial, y es además la vía barata que el `PORQUE` de la regla («la complejidad excede al consultorio») predice que el caso grave **no** debería tomar.

### 2.2 · `D-HS` — desenlace **primario**

Es el que corresponde a «grave»: hospitalización.

**Universo de la celda:** personas con `hs01 == 1` (`iiib_hs.dta` / `p_hs.dta`) **y** al menos un episodio en `iiib_hs1.dta` con `hs08_1a == 1` (**ENFERMEDAD**) o `hs08_1e == 1` (**OPERACIÓN**).

**Exclusiones, declaradas una por una** (`iiib_hs1.dta`, batería completa `hs08_1a`…`hs08_1h`): `hs08_1b` ACCIDENTE, `hs08_1c` PARTO, `hs08_1d` AGRESION FIS, `hs08_1f` ANALISIS, `hs08_1g` ABORTO, `hs08_1h` OTRO. **Ninguna es «síntoma grave o crónico complejo»** — parto y accidente son las dos que el encargo nombró; las otras cuatro se excluyen por el mismo criterio y se nombran aquí para que la exclusión sea auditable, no implícita. **Se reportan sus `n`**: cuántas hospitalizaciones quedaron fuera y por qué motivo.

⚠️ **Nivel de observación, declarado antes de correr.** `iiib_hs.dta` es **una fila por persona** (`folio`+`ls`) con la batería `hs02*` de respuesta múltiple; `iiib_hs1.dta` es **una fila por episodio** (`folio`+`ls`+`secuencia`). El motivo (`hs08_*`) pertenece al **episodio**; la institución (`hs02*`) pertenece a la **persona**. Esta spec **no puede** ligar institución a episodio, y no finge poder: el filtro de motivo se aplica **a nivel persona** («la persona tuvo al menos un episodio por enfermedad u operación») y la clasificación se lee de la batería de persona. **Limitación declarada, no descubierta después:** una persona con dos episodios —uno por parto y otro por enfermedad— entra al universo con la batería de instituciones de los dos. Si `L21` mide que las personas con ≥2 episodios de motivos mixtos son una fracción no trivial del universo, **lo reporta como reserva**; no las reasigna.

### 2.3 · `D-CE` — desenlace **secundario**

**Universo de la celda:** personas con `ce01 == 1` («HA IDO AL DOCTOR SIN HOSPITAL» en `b3b`; «FUE AL DOCTOR» en `p_ce.dta`). Clasificación por la **Tabla C**. Sin filtro de motivo: `ce10_1` («RAZON CONSULTA») vive en `iiib_ce1.dta` con el mismo desajuste de nivel de §2.2 y **no** se usa como filtro en esta versión — se declara como candidato para una `v1.3`, no se cuela por la puerta de atrás.

### 2.4 · El estimando, congelado

Para cada persona del universo de la celda, la batería `hs02*`/`ce04*` es de **respuesta múltiple**. Se construye una variable `LUGAR` de cuatro niveles **mutuamente excluyentes**:

| `LUGAR` | definición |
|---|---|
| `SOLO-PÚBLICO` | ≥1 marca en la clase PÚBLICO **y** 0 marcas en PRIVADO |
| `SOLO-PRIVADO` | ≥1 marca en PRIVADO **y** 0 en PÚBLICO |
| `AMBOS` | ≥1 marca en PÚBLICO **y** ≥1 en PRIVADO |
| `SOLO-OTRO` | 0 marcas en PÚBLICO y 0 en PRIVADO (sólo clase OTRO, o ninguna) |

**Estimando primario, pre-registrado:**

> `P_PUB(G)` = `n(SOLO-PÚBLICO | G)` / `n(SOLO-PÚBLICO | G)` + `n(SOLO-PRIVADO | G)`, ponderado, para el grupo `G`.

`AMBOS` y `SOLO-OTRO` quedan **fuera del cociente** y **se cuentan y se publican** — es el «fuera del contraste, contada» del encargo, hecho operable.

**Contraste pre-registrado:** `Δ = P_PUB(T=1) − P_PUB(T=0)`, con **IC95 por celda y para `Δ`**.

**Sensibilidad declarada AHORA, no después de ver el dato:** el mismo `Δ` recalculado contando `AMBOS` como público (`P_PUB' = (SOLO-PÚBLICO + AMBOS) / (SOLO-PÚBLICO + AMBOS + SOLO-PRIVADO)`). **Se corren las dos, se reportan las dos, y el veredicto de la celda sólo cuenta si coinciden en signo** — misma doctrina que los ponderadores en pareja de §3.2. Si discrepan, la celda es `NO-ESTIMABLE` por indeterminación de definición, declarada.

### 2.5 · Las 4 celdas de contraste

| # | disparador | desenlace | brazos |
|---|---|---|---|
| **C1** | `T1` (`es09`) | `D-HS` | `b3b` (Tabla A) · `bx` (Tabla B) |
| **C2** | `T1` (`es09`) | `D-CE` | `b3b` (Tabla C) · `bx` (Tabla C) |
| **C3** | `T2` (`ec01*`) | `D-HS` | `b3b` (Tabla A) — **sin brazo `bx`** (§1) |
| **C4** | `T2` (`ec01*`) | `D-CE` | `b3b` (Tabla C) — **sin brazo `bx`** (§1) |

**Hasta 4 contrastes × 2 brazos = 6 filas efectivas** (`C3`/`C4` no tienen brazo `bx`), cada una con su `Δ`, su IC95, su sensibilidad de §2.4, y —en `bx`— su pareja de ponderadores (§3.2). **Nunca se agrupan, nunca se promedian, nunca se combinan en un índice.**

⚠️ **Multiplicidad, declarada y no corregida.** Seis filas, ningún ajuste por comparaciones múltiples. La razón: no son seis pruebas de la misma hipótesis, son **seis lecturas declaradas por separado** de una regla con dos antecedentes y dos desenlaces, y la spec ya declara cuál es primaria (`C1`, `b3b`). **`C1`/`b3b` es la fila que decide el veredicto de la regla; las otras cinco son corroboración o discrepancia, y se reportan como tales.** Un veredicto que se apoye sólo en una fila secundaria se declara `PROPUESTA con reserva`, no `CORROBORADA`.

---

## 3 · Universo, llaves y ponderadores

### 3.1 · Los dos brazos, nunca agrupados (`A-bis 4`)

| brazo | libro | archivos | quién responde | ponderador |
|---|---|---|---|---|
| **`b3b`** (**principal**) | Libro IIIB, adultos presentes | `iiib_es.dta`, `iiib_ec.dta`, `iiib_hs.dta`, `iiib_hs1.dta`, `iiib_ce.dta` | la persona | `fac_3b` (`ehh02w_all/ehh02w_b3b.dta`) |
| **`bx`** (brazo aparte) | Libro Proxy, miembros ausentes | `p_es.dta`, `p_hs.dta`, `p_ce.dta` | otro miembro del hogar | **pareja** `fac_3b_px` **y** `fac_3a_px` (§3.2) |

`b3b` es el **principal**: es el universo directo, tiene los dos disparadores y los dos desenlaces, y no depende de una respuesta por proxy. `bx` se corre y se reporta **aparte**; su etiqueta de `es09` dice «GRAVE» (más cercana al `SI` de la regla) y la de `b3b` dice «SERIO» — la diferencia se cita en cada fila, no se resuelve promediando.

### 3.2 · Ponderadores del `bx`, **en pareja** — la decisión de dirección, congelada antes del dato

`v1.1` §1.3 adjudicó `fac_3b_px` por correspondencia sección→libro y por `n_no_nulo_gt0` sobre el libro `bx` **completo** (21 645 ≥ 21 631 ≥ 9 037). `MAESTRA38-L16-BIS-2` midió el **subconjunto real** (`es09` no nulo) y el orden se invirtió: `fac_3a_px` = **5 128**, `fac_3b_px` = **5 103** — **25 observaciones de diferencia**, en sentido contrario.

**Decisión de dirección que esta spec propaga (el ejecutor propaga, no decide — `SELLA-3`):**

1. **Se corren los DOS**, `fac_3b_px` y `fac_3a_px`, sobre cada celda del brazo `bx`. Los dos resultados se reportan, con su IC95, uno al lado del otro.
2. **El veredicto del brazo `bx` sólo cuenta si los dos coinciden en signo.** Si discrepan, el brazo `bx` es `NO-ESTIMABLE por ponderador indeterminado`, declarado, y el veredicto de la regla se lee de `b3b` (§3.1).
3. **Esta cláusula se declara aquí, antes de abrir el dato** — es exactamente lo que impide elegir el ponderador después de verlo, que es lo que `L16-BIS-2` se negó a hacer y por lo que paró.
4. `fac_4_px` (9 037 / 1 972) **no entra**: cobertura muy inferior y el libro que replica es el de niños. Declarado, no omitido.

**El chequeo de consistencia de `v1.1` §1.3 deja de ser `assert` y pasa a diagnóstico reportado.** Caja calcula `n_no_nulo_gt0` de `fac_3b_px`, `fac_3a_px` y `fac_4_px` sobre el subconjunto real de cada celda y **lo publica en la tabla de resultados** — pero **no PARA** por ello: bajo la regla de pareja de arriba, cuál de los dos tiene más cobertura ya no decide nada por sí solo. Esta es la única cláusula de `v1.1` que `v1.2` deroga, y se deroga **explícitamente y con su razón**, no por omisión.

### 3.3 · Qué NO cambia de `v1.1`

El `NO-ESTIMABLE` de `v1.1` **se mantiene y no se retira**. Su disparador `D1` (el chequeo de consistencia sobre `cen10*`/`es09`) falló por su cuenta y bastaba por sí solo; su disparador `D2` se reclasifica en su alcance (§0.3) sin tocar el veredicto. `v1.2` **no es una corrección de `v1.1`: es una rama distinta con otro desenlace.**

### 3.4 · Llaves

**`folio` y `ls` se normalizan a entero antes de todo join** (defecto medido por `C1` y confirmado por `L16-BIS-2`: sin normalizar, `folio` como cadena contra `float64` da **0 filas** en el join y ningún error). `iiib_hs1.dta`/`iiib_ce1.dta` añaden `secuencia`. Los joins que esta spec necesita:

| join | llave | para qué |
|---|---|---|
| `iiib_es` × `iiib_hs` | `folio`+`ls` | `T1` × `D-HS` |
| `iiib_ec` × `iiib_hs` | `folio`+`ls` | `T2` × `D-HS` |
| `iiib_es`/`iiib_ec` × `iiib_ce` | `folio`+`ls` | `T1`/`T2` × `D-CE` |
| `iiib_hs` × `iiib_hs1` | `folio`+`ls` | filtro de motivo (§2.2), agregado a persona |
| cualquiera × `ehh02w_b3b`/`ehh02w_bx` | `folio` | ponderador |

**Se reporta, por cada join, cuántas filas entraron y cuántas resolvieron.** Un join que resuelva 0 filas es el bug de `folio`, no un hallazgo sobre la encuesta (A.5 aplicada a un artefacto).

### 3.5 · Varianza y escala

**Escala de reporte (`A-bis 3`): proporción ponderada**, en los términos de §2.4. **Diseño real, heredado de `MAESTRA38-L16-BIS`, sin cambio:** `ENNViH` 2002 **no trae UPM/PSU** en ninguno de los archivos (buscado, cero); hay estrato en `c_portad.dta`. Se declara el diseño usado: **conglomerado = hogar (`folio`), estrato = el de `ehh02dta_bc/c_portad.dta`, IC95 por bootstrap de hogares dentro de estrato**. La unidad primaria real de `ENNViH` (localidad) **no está en los archivos**, de modo que el IC por hogar **subestima la varianza** respecto del diseño verdadero. **Consecuencia pre-registrada: un `Δ` cuyo IC95 apenas excluya 0 se reporta como `PROPUESTA con reserva`, nunca como `CORROBORADA`.**

### 3.6 · Ventanas de referencia — **se leen del cuestionario y se citan con página, antes de calcular**

Las etiquetas de 2002 en el inventario **no traen la ventana** (las de 2009 sí: `hs01` = «ULT 12MES INTERNADO EN HOSP/CLINICA?», `ats01a1` = «ULT 4SEM CONSUMIDO S/RECETA…»). **Caja lee la ventana de `es09`, `hs01`, `ec01*` y `ce01` del cuestionario y del manual de codificación del Libro IIIB (§6) y las cita con número de página en su recibo, antes de calcular una sola celda.**

⚠️ **Y la declara aunque no le guste lo que lea.** Si la ventana del desenlace **no cubre** la del disparador —por ejemplo, `ce01` a 4 semanas contra un `es09` a 12 meses—, el contraste mide **co-ocurrencia, no secuencia**: no dice que la persona acudió *por* ese síntoma. **Eso se declara en la fila, no se corrige con una restricción inventada después.** Esta limitación aplica a las cuatro celdas: **`ENNViH` 2002 no ordena temporalmente síntoma y atención dentro de la ventana**, y ninguna medición de esta spec puede sostener una afirmación causal.

---

## 4 · Escala de veredicto — las cuatro filas

Se aplica **por fila** (celda × brazo), nunca al conjunto. `T` = el disparador de esa celda.

| fila | condición | qué significa |
|---|---|---|
| **`CORROBORADA`** | `Δ > 0` con IC95 que excluye 0, **en las dos definiciones de §2.4** y —en `bx`— **con los dos ponderadores de §3.2 coincidiendo en signo** | entre quienes reportan el antecedente, la proporción que acude a institución pública es **mayor** que entre quienes no lo reportan: el `ENTONCES` de `R4.4` se sostiene en este instrumento |
| **`NO-DISCRIMINA`** | IC95 de `Δ` **incluye 0** | el antecedente no mueve la elección público/privado. No es evidencia de la regla ni contra ella: es evidencia de que **este** contraste no la distingue |
| **`CONTRARIA`** | `Δ < 0` con IC95 que excluye 0 | entre quienes reportan el antecedente, **menos** acuden a lo público. La regla **se rompe** para esa fila (§5) |
| **`NO-ESTIMABLE`** | **numerador `< 10` en alguna de las dos celdas del cociente** (`SOLO-PÚBLICO` o `SOLO-PRIVADO`, en `T=1` o en `T=0`) · **o** las dos definiciones de §2.4 discrepan en signo · **o** —en `bx`— los dos ponderadores discrepan en signo · **o** el join resuelve 0 filas y no se corrige con la normalización de §3.4 | la fila **no se construye**. Se publican los `n` crudos como diagnóstico, **nunca una proporción** |

**`NO-ESTIMABLE` no se rescata bajando el umbral.** El umbral de 10 es de esta spec, congelado antes del dato.

### 4.1 · Qué significaría corroborar, dicho antes de saberlo

**Sería la primera medición mexicana de `R4.4` con síntoma y lugar de atención en el mismo instrumento y en la misma persona.** La Rama B (`ENSANUT2024`, `NO-DISCRIMINA`) construyó su corte de severidad con una variable **administrativa** (hospitalización/urgencias vs. consulta externa) — el desenlace y el disparador salían del mismo hecho administrativo. Aquí no: `es09`/`ec01*` son **auto-reporte de la persona sobre su cuerpo** y `hs02*`/`ce04*` son **auto-reporte de la persona sobre dónde la atendieron**, dos preguntas distintas del mismo cuestionario a la misma persona.

**Y lo que corroborar NO significaría, dicho con el mismo énfasis:** (i) no sostiene causalidad — §3.6 lo prohíbe explícitamente; (ii) **es un instrumento sin réplica**: una fila `CORROBORADA` en `ENNViH` 2002 **no mueve el tier** de `R4.4` por sí sola, por la misma doctrina que `MAESTRA38-L16-BIS` ya escribió («`CORROBORADA` en un instrumento, sin réplica: no mueve tier»); (iii) **choca con la Rama B**, que midió `NO-DISCRIMINA` — dos instrumentos discrepando es materia de mesa, no del ejecutor, y esta spec no la resuelve; (iv) si `T2` corrobora, corrobora «crónico», no «crónico complejo» (§1).

---

## 5 · `se_mueve_si` — sustituye a la de `v1.1` Rama A

`v1.1` §5, Rama A, verbatim (lo que esta cláusula sustituye):

> *«si entre quienes reportan síntoma grave (`es09=1`, 2002/2005) la proporción que acude a institución pública (vía `clave1`/`clave2`, 2002) **no es mayor** que la que acude a privada, la regla se rompe para esa rama.»*

Esa formulación es inejecutable: `clave1`/`clave2` no clasifican (§0.2), y el criterio «pública > privada» era un **nivel**, no un **contraste** — una población donde el 90 % acude a lo público con o sin síntoma la habría «corroborado» sin que el antecedente hiciera nada.

**`se_mueve_si` de `v1.2`, congelada:**

> **`R4.4` se mueve si, en la fila primaria `C1`/`b3b` (`T1` = `es09`, `D-HS`, Tabla A, `fac_3b`), `Δ = P_PUB(es09=1) − P_PUB(es09=0)` resulta `CONTRARIA` o `NO-DISCRIMINA` bajo las dos definiciones de §2.4.** El `ENTONCES` de la regla —«busca el sistema público»— predice que el antecedente **desplaza** la elección hacia lo público; un `Δ` que no lo haga, medido sobre el instrumento que sí tiene síntoma y lugar en la misma persona, es evidencia contra la regla, no contra el instrumento.
>
> **Con `NO-DISCRIMINA` en `C1`/`b3b` y `NO-DISCRIMINA` ya medido en la Rama B (`ENSANUT2024`), `R4.4` queda con dos instrumentos independientes que no la sostienen** — y eso es la propuesta de bajar su tier, que **esta spec no ejecuta**: es firma de mesa (§7).
>
> **Y lo que NO la mueve, declarado para que nadie lo fuerce:** un `NO-ESTIMABLE` en `C1`/`b3b` **no** es evidencia contra la regla — es ausencia de medición, y se reporta como tal. Una fila secundaria (`C2`/`C3`/`C4`, o cualquier fila de `bx`) que salga `CONTRARIA` mientras `C1`/`b3b` sale `CORROBORADA` **no** rompe la regla: se reporta como discrepancia entre lecturas, y la decisión es de mesa.

---

## 6 · Archivos que la caja necesita abrir

**Microdato y ponderadores** (ids y sha256 de `data/manifiesto.yaml`, los mismos que `v1.1` §6 Rama A cita para 2002 — verificados de nuevo al redactar):

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `ennvih1_2002_hogar_dta` | `ennvih/ehh02dta_all.zip` | `8b9b51904ca8790421d82a8a81f7f4edbce9a296cba2ce86fef74f8f379b5923` |
| `ennvih1_2002_ponderador` | `ennvih/ehh02w_all.zip` | `bbe8006844f715c19b724ebb74f1408c4cfa07e2efdfe7d6748b5182ef214587` |

Miembros concretos, dentro de `ehh02dta_all.zip`: `ehh02dta_b3b/{iiib_es,iiib_ec,iiib_hs,iiib_hs1,iiib_ce}.dta` · `ehh02dta_bx/{p_es,p_hs,p_ce}.dta` · `ehh02dta_bc/c_portad.dta` (estrato, §3.5). Dentro de `ehh02w_all.zip`: `ehh02w_b3b.dta`, `ehh02w_bx.dta`.

**Documentación para §3.6 (ventanas) y para el chequeo de etiquetas de §2.1** — **ya está en la raíz, no se pide** (regla del `/acto` paso 3: *«Si el censo lista el archivo, no se pide — se registra»*):

| id de manifiesto | archivo | sha256 | qué aporta |
|---|---|---|---|
| `ennvih1_2002_hogar_q` | `ennvih/ehh02q_all.zip` | `40af29bd864e967200dbbde2c9744795b33c0a23cdbb19902dd2ecdb7beb3cac` | **ZIP con los cuestionarios PDF de todos los libros de hogar de ENNViH-1**, el Libro IIIB incluido — es la fuente de las ventanas de `es09`/`hs01`/`ec01*`/`ce01` |
| `ennvih1_2002_hogar_cb` | `ennvih/ehh02cb_all.zip` | `a3220412505d6684e50548bdd1e01ce816d3af99ed846e4e27f30f35e9b506b2` | manuales de codificación. ⚠️ **deflate64** (`C1`: `zipfile` de Python lo rechaza; `tar.exe` de Windows lo extrae relleno de ceros **sin avisar** — usar `zipfile-deflate64` o equivalente) |
| `ehh02cb_b3b` | `ennvih/doc/ehh02cb_b3b.pdf` | `fa022876e336e975efebae7afb91e6beca3f92c915a57238de79f71db2f1ed6b` | **manual de codificación del Libro IIIB suelto, 265 382 bytes, ya descargado el 30/jul/2026** — la vía más corta a §3.6 |

⚠️ **Corrección al §6 que el encargo pidió, con su razón.** El encargo instruyó citar `ehh02q_b3b.pdf` por **URL pública** y, si el agente no la alcanzaba, registrar `NO OBTENIDO POR ESTE AGENTE` con receta manual (A.5). **No hace falta pedir nada:** el manifiesto ya trae `ehh02q_all.zip` (los cuestionarios completos, 3 750 632 B, descargado el 30/jul/2026) **y** `ehh02cb_b3b.pdf` suelto. `L21` corre en UBUNTU con el corpus montado y los abre desde la raíz. **Registrado, no pedido.**

**A.5, aun así, sobre lo que este agente sí intentó y no pudo** — porque el benchmark web que el encargo cita como hecho no se pudo reproducir desde aquí:

> **`https://ennvih-mxfls.org/…` — NO OBTENIDO POR ESTE AGENTE EN 3 INTENTOS.** Salida cruda: `curl -s -o /dev/null -w "%{http_code}" --max-time 20 https://ennvih-mxfls.org/ennvih-1.html` → `000`; ídem con `www.` → `000`; `WebFetch` → `EGRESS_BLOCKED`. Causa declarada por el propio proxy (`curl -s "$HTTPS_PROXY/__agentproxy/status"`): `connect_rejected · gateway answered 403 to CONNECT (policy denial or upstream failure) · ennvih-mxfls.org:443`. **Es un hecho sobre la red de esta sesión, no sobre el sitio.**
>
> **Receta manual (< 1 minuto, navegador):** abrir `https://ennvih-mxfls.org/assets/ehh02q_b3b.pdf` (o `…/ehh02cb_b3b.pdf`), buscar las secciones `ES`, `EC`, `CE` y `HS`, y leer la ventana de referencia de `es09`, `ec01`, `ce01` y `hs01`. **No es necesaria para `L21`** — los dos PDFs están en la raíz (tabla de arriba); la receta queda para quien quiera verificar contra el sitio.
>
> **Lo que sí se obtuvo por búsqueda web (7/sep/2026), y su límite:** el índice de secciones del Libro IIIB se confirma —`ES` (estado de salud), `SM` (estado de ánimo), `EC` (enfermedades crónicas), `ATS` (autotratamiento), `CE` (consulta externa), `HS` (utilización de servicios de hospitalización)—. **Dos precisiones frente al encargo:** el índice trae también **`SM`**, que el encargo no listó, y la búsqueda **no confirmó `CA`** en esa enumeración (aunque `iiib_ca.dta` existe en el microdato, §0.3). **Las ventanas de referencia NO se obtuvieron por web** — se leen del PDF de la raíz, §3.6. Fuente: [ennvih-mxfls.org/ennvih-1.html](https://ennvih-mxfls.org/ennvih-1.html) (vía resultados de búsqueda; la página no se pudo abrir desde esta sesión).

---

## 7 · Qué NO hace esta pieza, y las dos correcciones al encargo que quedan declaradas

**No abre ningún archivo de §6.** No calcula ninguna celda, ninguna proporción, ningún IC95. No mueve el tier de `R4.4` ni toca `canon/`. No edita `v1.0` ni `v1.1`. **No reabre `FP-332`** — la reclasificación de §0.3 es del alcance de un veredicto de existencia, no de la firma. No corre el brazo `ENDIREH` de `v1.1` (sigue como está: corroboración de otro antecedente, nunca sumada). No propone bajar el tier de `R4.4` (§5 dice cuándo eso sería materia de mesa; proponerlo aquí sería el ejecutor decidiendo). **No adjudica el ponderador del `bx`** — lo corre en pareja, que es lo contrario de adjudicar.

**Corrección 1 — el conteo del encargo.** La verificación A.8 del encargo declaró *«`grep -iE "iiib_(hs|ce)\.dta|p_(hs|ce)\.dta" data/inventario-reactivos-ext-v1_0.tsv | wc -l` → 524»*. **Ese comando, corrido literal contra `origin/main = 604793fa`, devuelve 434**, no 524. Desglose (`iiib_hs` 76 · `iiib_ce` 102 · `p_hs` 113 · `p_ce` 143 = **434**). Las otras dos cifras del encargo **sí se reproducen exactas**: 63 346 filas en el inventario `ext` (`grep -vc '^#'`) y 317 721 en los tres inventarios vigentes (178 247 + 63 346 + 76 128). **Nada del diseño de esta spec depende del 434 ni del 524** — las variables se verificaron una por una, no por conteo agregado —, pero la cifra se corrige donde se escribió.

**Corrección 2 — 2005 y 2009 sí están en el inventario, y aun así no entran.** El encargo declaró: *«el inventario ext no las trae a nivel de variable (`grep` → 0 con esos nombres)»*. **Falso, verificado:**

```
$ awk -F'\t' '$5 ~ /(iiib_(hs|ce|es|ec)|p_(hs|ce|es))\.dta/ {split($5,a,"/"); print $1" | "a[2]}' \
    data/inventario-reactivos-ext-v1_0.tsv | sort -u
ennvih/ehh02dta_all.zip | ehh02dta_b3b
ennvih/ehh02dta_all.zip | ehh02dta_bx
ennvih/ehh05dta_all.zip | iiib_ce.dta        ← 2005
ennvih/ehh05dta_all.zip | iiib_ec.dta
ennvih/ehh05dta_all.zip | iiib_es.dta
ennvih/ehh05dta_all.zip | iiib_hs.dta
ennvih/ehh05dta_all.zip | p_ce.dta
ennvih/ehh05dta_all.zip | p_es.dta
ennvih/ehh05dta_all.zip | p_hs.dta
ennvih/ehh09dta_all.zip | ehh09dta_b3b       ← 2009
ennvih/ehh09dta_all.zip | ehh09dta_bx
```

Las tres olas están, con variable y etiqueta; las de 2009 incluso traen la ventana en la propia etiqueta («ULT 12MES INTERNADO EN HOSP/CLINICA?»). **Aun así, 2005 y 2009 NO se pre-registran aquí** — la instrucción de dirección es explícita y esta spec la propaga, no la discute. Se corrige el **hecho**, no la **decisión**: 2005/2009 quedan como sucesor declarado (§8), con la nota de que sus baterías de instituciones **cambian entre olas** (en el bloque de 2005 de `iiib_hs.dta`, «OTRO LUGAR» es `hs02j_1` y `hs02k_1` no existe; en 2002 es `hs02k_1`) y por tanto necesitarían **tablas de clasificación propias**, no las de §2.1.

---

## 8 · Sucesores declarados, no lanzados

- **`L21`** (caja, UBUNTU, corpus montado): corre las 4 celdas × brazos de §2.5 contra esta spec, gateado **por producto** al sha256 de este archivo. Dos commits: (1) spec citada antes de abrir un `.dta`, (2) resultados. **Si `L21` corrobora con `T2`, es el primer dato que vuelve medible el «crónico complejo» de la regla, hoy sin ninguna medición.**
- **Re-correr el barrido `D2`** contra el `.dta` real para adjudicar entre las dos lecturas de §0.3 — `L21` abre esos archivos de todas formas.
- **2005/2009** (§7): requiere tablas de clasificación propias por ola, y una spec propia.
- **`ce10_1` como filtro de motivo de `D-CE`** (§2.3): requiere resolver el desajuste de nivel persona/episodio.

---

**El primer resultado que produzca este procedimiento es el que se reporta — de cada celda y de cada brazo, por separado.**

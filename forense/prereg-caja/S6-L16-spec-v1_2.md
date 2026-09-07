# S6 · Pre-registro de `salud.atencion.grave` — Rama A′: el desenlace de `R4.4` sí existe en ENNViH 2002, en HS/CE del Libro IIIB

### `prereg-caja-S6-L16` · **v1.2** · 7 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S6-L16-spec-v1_2.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S6-L16`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`, de una **Rama A′** para `salud.atencion.grave` (`R4.4`) sobre ENNViH-1 2002: dos disparadores (`es09`; `ec01*`) × dos desenlaces (hospitalización `hs02*`; consulta externa `ce04*`), corridos **por separado**, sobre dos brazos de universo (`b3b` directo, `bx` proxy) que **nunca** se agrupan. Nace de una corrección de premisa verificada: `v1.0` y `v1.1` declararon el desenlace `NO-CONSTRUIBLE` mirando `cen10*` (sección CEN, libro de niños) y `clave1`/`clave2`; la clasificación por institución vive en las secciones **HS** y **CE** del Libro IIIB, que ninguna de las dos specs citó (§0). |
> | **QUÉ NO ES** | No abre ningún `.dta`. No mide, no calcula proporciones ni IC95. No mueve el tier de `salud.atencion.grave` (`[MEDIA]`, `canon/modelo-decision-v4_0.md:527`). No reescribe `v1.1` — la enmienda con fecha, `v1.1` queda íntegra en su ruta (A.10). No reabre `FP-332` (esa firma es de `SELLO-3`); lo que hace con `FP-332 D2` es reclasificarlo como **NO-ENCONTRADO por el barrido que lo produjo**, no retirarlo. No pre-registra 2005 ni 2009. No adjudica cuál de los dos linajes `EXISTE-SATISFACE` de `v1.1 §0.2` es el canónico. |
> | **VERIFICAS ASÍ** | Caja corre las 4 celdas de contraste (§2.4) × 2 brazos (§3), reporta las 8 filas por separado, y **antes** de calcular una sola celda: (a) lee del cuestionario la ventana de `hs01` y de `es09` (§1.1, `ennvih1_2002_hogar_q`, en corpus) y la declara; (b) lee del descriptor del `.dta` las etiquetas de `hs02*`/`ce04*` del libro que va a usar y las coteja contra la tabla congelada de §2.2/§2.3 — **si una etiqueta no corresponde, lo reporta y NO reclasifica**; (c) corre los dos ponderadores del brazo `bx` en pareja (§3.3) y sólo emite veredicto de ese brazo si coinciden en signo. |

**Acto:** `ACTO MAESTRA38-N22 · S6 v1.2 — RAMA A′ DE R4.4 SOBRE ENNViH 2002 CON HS/CE`, 7/sep/2026, entorno **NUBE sin corpus montado**, sobre `origin/main = 604793fa` (`PR #591`). Linaje: `v1.0` (`MAESTRA38-N11`, 5/sep) → `v1.1` (`MAESTRA38-N19`, 7/sep) → **`v1.2` (esta pieza)**. Patrón S6: cada versión enmienda a la anterior con fecha, ninguna la reescribe.

---

## 0 · Corrección de premisa — el desenlace existía y dos specs no lo vieron (A.8/D-13)

### 0.1 · Lo que `v1.1` declaró, verbatim

`forense/prereg-caja/S6-L16-spec-v1_1.md` §0.3, verbatim:

> *`N5`/`N10` describen `cen10*` como "desenlace, lugar de consulta" — leído como si permitiera distinguir sistema público de privado. Verificado contra las tres olas de `data/inventario-reactivos-ext-v1_0.tsv` (…): **`cen10d_1`/`cen10l_1`/`cen10m_1`/`cen10e_1`/`cen10p_1` son, sin excepción, identificadores geográficos** … **ninguno codifica tipo de institución** (IMSS/ISSSTE/privado/Seguro Popular). Las únicas variables de ese mismo módulo que sí nombran una institución (`clave1` "ID CLINICA COMUNITARIO", `clave2` "ID PROVEEDOR SALUD COMUNITARIO") existen **solo en la ola 2002** … **El desenlace "sistema público" del `SI...ENTONCES` no está en `cen10*` por sí solo** — requeriría cruzar contra un directorio externo de establecimientos por dirección/municipio, que este repo no tiene registrado, o depender de `clave1`/`clave2`, solo disponibles en una de las tres olas.*

Y `v1.1` §3, verbatim:

> *`BUSCA_PUBLICO` — no construible directamente de `cen10*` (§0.3); se pre-registra como **`NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO`** salvo que caja confirme `clave1`/`clave2` (solo 2002) como suficiente.*

### 0.2 · La corrección, con comando

Las dos afirmaciones sobre `cen10*` y sobre `clave1`/`clave2` **son ciertas y no se retiran**: `cen10*` es geografía, y `clave1`/`clave2` son llaves de entrada a un directorio de proveedores (`iiib_hs1.dta:35105-35106` del inventario ext: `clave1` = `ID CLINICA COMUNITARIO`, `clave2` = `ID PROVEEDOR SALUD COMUNITARIO`). Lo que no se sostiene es la **conclusión** que se derivó de ellas — que por eso el desenlace no existe en ENNViH 2002. Existe, en otras dos secciones del mismo Libro IIIB, que ninguna de las dos specs citó:

```
$ grep -icE "iiib_(hs|ce)\.dta|p_(hs|ce)\.dta" data/inventario-reactivos-ext-v1_0.tsv
434
$ wc -l data/inventario-reactivos-ext-v1_0.tsv
63350 data/inventario-reactivos-ext-v1_0.tsv
```

**Corrección al encargo que lanzó esta pieza (A.8, verificada, no heredada):** el encargo cifra ese `grep` en **524** y el inventario ext en **63 346** filas. Contra el árbol en `604793fa` las cifras son **434** y **63 350**. Se escribe la cifra medida, no la del encargo. (Añadiendo `iiib_hs1.dta`/`iiib_ce1.dta` al patrón, **780**.)

**El desenlace, a nivel de variable, en el inventario** (`data/inventario-reactivos-ext-v1_0.tsv`, columna 5 = `archivo_miembro`, columna 6 = variable, columna 7 = texto verbatim; número = línea del TSV):

| archivo (2002, libro `b3b`) | variable | texto verbatim | línea |
|---|---|---|---|
| `ehh02dta_all/ehh02dta_b3b/iiib_hs.dta` | `hs01` | ESTUVO HOSPITALIZADO | 35025 |
| ídem | `hs02a`…`hs02j`, `hs02k_1` | INTERNADO SSA / IMMS / ISSSTE / PEMEX SEDENA / HOSPITAL PRIVADO / CONsultorio PRIVADO / CENTRO RURAL / CRUZ ROJA / CASA PRACTICANTE / CASA / OTRO LUGAR | 35026-35036 |
| ídem | `hs03a`…`hs03k`, `hs04` | VECES INTERNADO … / #VECES INTERNADO TOTAL | 35037-35048 |
| `…/iiib_hs1.dta` | `hs08_1a`…`hs08_1h` | HOSPITALIZADO: ENFERMEDAD / ACCIDENTE / PARTO / AGRESION FIS / OPERACION / ANALISIS / ABORTO / OTRO | 35051-35058 |
| ídem | `hs10`, `hs11_1`, `hs11_21`, `hs11_22` | # NOCHE INTERNADO · ID/HRS/MIN LLEGAR AL HOSPITAL | 35064-35067 |
| `…/iiib_ce.dta` | `ce01` | HA IDO AL DOCTOR SIN HOSPITAL | 34708 |
| ídem | `ce04a`…`ce04m`, `ce04n_1` | CONSULTA SSA / IMSS / ISSSTE / PEMEX SEDENA MARINA / CLINICA PRIVADA / MEDICO PRIVADO / DIF / ENFERMERA-PARAMEDICO / UNIDAD MOVIL / CRUZ ROJA / DISPENSARIO MEDICO / FARMACIA / PRACTICANTE TRADICION / OTRO LUGAR | 34711-34724 |
| ídem | `ce05a`…`ce05n`, `ce06` | #CONSULTAS … · # TOTAL CONSULTAS EXTERNAS | 34725-34739 |
| `…/iiib_ce1.dta` | `ce10_1`, `ce13_1a`…`ce13_1n`, `ce15_1/21/22` | RAZON CONSULTA · SERVICIOS:… · IDEN/HRS/MIN EN LLEGAR CONSULTA | 34742-34766 |
| `…/iiib_es.dta` | `es09` | HA TENIDO PROBLEMA SERIO SALUD | 34929 |
| `…/iiib_ec.dta` | `ec01a`…`ec01g`, `ec01h_1`, `ec01i_1` | TIENE DIABETES / HIPERTENSION / ENFERMEDAD CORAZON / CANCER / ARTRITIS REUMATISMO / ULCERA GASTRICA / MIGRANA / ENFERMEDAD CRONICA_1 / CRONICA_2 | 34888-34896 |
| `…/iiib_ats.dta` | `ats01a1`…`ats01c` | HA TOMADO ANALGESICOS / ANTIHISTAMINICOS / ANTIBIOTICOS / GOTAS-YESO / MEDICINAS TRADICIONALES | 34612-34616 |

**Dos correcciones al encargo dentro de esta misma tabla, verificadas antes de congelar:**

1. El encargo escribe `ec01a-i` como si las nueve fueran diagnósticos nombrados («diabetes, hipertensión, corazón, cáncer, artritis, úlcera, migraña, otras»). El árbol dice que son **siete nombradas** (`ec01a`…`ec01g`) más **dos abiertas** con nombre de variable distinto: `ec01h_1` y `ec01i_1` («TIENE ENFERMEDAD CRONICA_1/_2»), **no** `ec01h`/`ec01i`. Caja que teclee `ec01h` no encuentra la columna.
2. El encargo escribe `ce04a … ce04f` como «MÉDICO PRIVADO». Verbatim: `ce04e` = `CONSULTA CLINICA PRIVADA`, `ce04f` = `CONSULTA MEDICO PRIVADO`. Ambas privadas — la clasificación no cambia, el texto sí.

### 0.3 · `FP-332 D2` — reclasificado como NO-ENCONTRADO por ese barrido, no retirado

`forense/firmas-pendientes.tsv`, `FP-332`, verbatim:

> *D2: `BUSCA_PUBLICO` queda `NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO`. … Barrido de etiquetas de todos los `.dta` de ENNVIH 2002 por `PUBLIC|PRIVAD|IMSS|ISSSTE|SSA|SEGURO SOCIAL|SECTOR` CON CONTROL POSITIVO (si encuentra: `iiib_ca.dta ca02a-f`, `iiia_tb.dta tb33p_d-f`, `ii_nna1.dta nna20c/d`, `iiia_ed.dta ed241-244`): todos son stock de aseguramiento o tipo de escuela, NINGUNO pregunta a donde acudio tras el sintoma. **EL DESENLACE DE R4.4 NO EXISTE EN ENNVIH 2002.***

Esa última oración no se sostiene contra §0.2, y la causa es medible. El propio patrón del barrido (`IMSS|ISSSTE|SSA|PRIVAD`) **debería** haber devuelto `ce04b` (`CONSULTA IMSS`), `ce04c` (`CONSULTA ISSSTE`), `ce04a` (`CONSULTA SSA`), `ce04e`/`ce04f` (`CLINICA PRIVADA`/`MEDICO PRIVADO`), `hs02a` (`INTERNADO SSA`), `hs02c` (`INTERNADO ISSSTE`), `hs02e`/`hs02f` (`HOSPITAL PRIVADO`/`CONsultorio PRIVADO`) — y la lista de aciertos que el recibo publica **no contiene ninguno de esos archivos**. Es decir: el barrido no examinó `iiib_ce.dta` ni `iiib_hs.dta`, o los examinó y no reportó el acierto. No se puede distinguir cuál de las dos cosas pasó, **porque el recibo no declara los archivos examinados** — el requisito de `A.13` que `MAESTRA38-C1` sí cumplió el mismo día en el mismo dataset («`ehh02dta_all.zip`: **137** miembros `.dta` examinados, **0** con columna `fac*`»).

Anotación lateral, para quien re-corra el barrido: `hs02b` está etiquetada **`INTERNADO IMMS`** (línea 35027), con la transposición `IMMS`. Un patrón `IMSS` no la encuentra; `ce04b` (`CONSULTA IMSS`, correcta) sí. Un solo typo del instrumento no explica el `NO-ENCONTRADO` — las otras once etiquetas están bien escritas — pero explica por qué un barrido por marca de institución puede perder filas reales sin levantar excepción.

**Qué hace esta spec con `FP-332`:** nada, salvo lo declarado. `FP-332` está `ABIERTA -- pendiente de firma de mesa` y su firma es de `SELLO-3`. `D1` (fallo del CHEQUEO DE CONSISTENCIA del ponderador) **se sostiene íntegro** y es el que §3.3 propaga. `D2` se reclasifica aquí como **NO-ENCONTRADO POR ESE BARRIDO** — un hecho sobre el barrido, no sobre el corpus, exactamente la distinción que `MAESTRA38-LOTE-CRUCE` ya dejó como regla candidata en `forense/hallazgos.md` («un `NO-ENCONTRADO` es un hecho sobre la fuente que se abrió, no sobre el corpus»).

### 0.4 · Benchmark web (7/sep/2026) y cobertura retroactiva

**Benchmark web, declarado con su límite.** El sitio oficial `https://ennvih-mxfls.org` **no es alcanzable desde este entorno** (`EGRESS_BLOCKED` por el proxy de red de la sesión — registrado, no rodeado). La búsqueda web sí devuelve, desde el propio dominio y desde su documentación, que el Libro IIIB de ENNViH lista las secciones **ES, EC, ATS, CE (Utilización de consulta externa) y HS (Utilización de servicios de hospitalización)**, y que en la sección `ce1` `secuencia=1` es la última consulta y `secuencia=2` la penúltima, sobre visitas **en las últimas 4 semanas** ([ennvih-mxfls.org/documentacion1.html](https://ennvih-mxfls.org/documentacion1.html), [guía de usuario ENNViH-3](https://www.ennvih-mxfls.org/assets/guia_de_usuario_ennvih-3.pdf)). Esto **corrobora la existencia de las secciones**; no basta para congelar una ventana con cita de página, y por lo tanto la ventana **no se congela aquí** — §1.1 la deja como lectura obligatoria de caja contra el cuestionario que ya está en corpus (§6). El encargo pedía citar `ehh02q_b3b.pdf` con página antes de sellar; este acto no puede leerlo, así que no lo cita: lo pasa a caja como requisito previo, con el archivo del manifiesto, no con una URL.

**Cobertura retroactiva.** El inventario ext nació el 5/sep (`MAESTRA38-C1`); `v1.0` (`N11`, 5/sep) y `v1.1` (`N19`, 7/sep) se escribieron sin consultarlo **por sección** — consultaron `es09` y `cen10*` por nombre de variable, que es una consulta distinta.

**Corrección al encargo, verificada:** el encargo afirma que para 2005/2009 «el inventario ext no las trae a nivel de variable (`grep` → 0 con esos nombres)». **Falso contra el árbol.** Las siete secciones están en las tres olas:

```
$ awk -F'\t' '$5 ~ /iiib_(hs|hs1|ce|ce1|es|ec|ats)\.dta$/ {print $1}' \
    data/inventario-reactivos-ext-v1_0.tsv | sort -u
ennvih/ehh02dta_all.zip
ennvih/ehh05dta_all.zip
ennvih/ehh09dta_all.zip
```

(`ehh05dta_b3b/iiib_hs.dta:38316` = `hs01 ESTUVO HOSPITALIZADO`, mismo patrón en 2009.) **Aun así, esta spec NO pre-registra 2005 ni 2009** — el perímetro que el encargo fija es 2002 y el ejecutor propaga, no amplía. Lo que cambia es la **razón**: no se omiten porque el dato no exista, se omiten porque están fuera del perímetro de esta pieza. Réplica en 2005/2009 = acto sucesor con spec propia, que además tendrá que verificar el mapa de letras de `hs02*` en cada ola (§2.2 muestra por qué eso no es formalidad).

---

## 1 · Disparadores — dos, POR SEPARADO

Los dos leen la misma regla («SI el síntoma es **grave o crónico complejo**»); ninguno la lee entera. **No se combinan en un índice, no se suman, no se promedian.** Se corren como dos lecturas independientes y se reportan como dos filas.

### 1.1 · T1 — `es09` («problema serio de salud»)

`T1 = 1` si `es09 == 1`; `T1 = 0` si `es09` toma el valor de "no" del instrumento; **filas con `es09` nulo salen del universo del contraste, contadas y declaradas** (no se recodifican a 0).

| libro | archivo | texto verbatim de `es09` | línea (ext) |
|---|---|---|---|
| `b3b` (directo) | `ehh02dta_all/ehh02dta_b3b/iiib_es.dta` | HA TENIDO PROBLEMA SERIO SALUD | 34929 |
| `bx` (proxy) | `ehh02dta_all/ehh02dta_bx/p_es.dta` | HA TENIDO PROBLEMA SALUD GRAVE | 37019 |

La asimetría de adjetivo (SERIO vs GRAVE) es la misma que `v1.1 §1.1` documentó y **no se resuelve aquí**: es una razón más para que los dos brazos no se agrupen (§3).

**Ventana: PENDIENTE-DE-LECTURA-POR-CAJA, no congelada.** `es09` no trae `es09a` en 2002 (verificado: `es09a` aparece en 2005 y 2009, no en 2002 — líneas 38187/40698/46104/48579, ninguna de 2002). La ventana de referencia de `es09` **se lee del cuestionario** (`ennvih1_2002_hogar_q`, §6) y **se declara con página antes de calcular la primera celda**. Si caja no puede abrir el cuestionario, lo registra como `NO OBTENIDO POR ESTE AGENTE` con `N` intentos y receta manual (`A.5`) y reporta las celdas con la ventana marcada `NO DECLARADA` — no la inventa ni la hereda del texto de otra ola.

### 1.2 · T2 — «crónico complejo» = al menos una crónica

`T2 = 1` si **al menos una** de `ec01a`, `ec01b`, `ec01c`, `ec01d`, `ec01e`, `ec01f`, `ec01g`, `ec01h_1`, `ec01i_1` toma el valor de "sí" del instrumento (`ehh02dta_all/ehh02dta_b3b/iiib_ec.dta`, líneas 34888-34896). `T2 = 0` si todas toman "no". Fila con **todas** nulas → fuera del universo, contada.

Las dos abiertas (`ec01h_1`/`ec01i_1`, «ENFERMEDAD CRONICA_1/_2») **cuentan como crónica** bajo esta definición congelada — es la lectura literal de «al menos una de `ec01a-i`» que la mesa firmó. Caja reporta **por separado** el conteo de `T2=1` que depende exclusivamente de una de esas dos, para que se vea cuánto del disparador descansa en un campo abierto.

**`ec01*` no existe en el libro `bx`.** Verificado: el inventario ext no trae ningún `p_ec.dta`. Consecuencia congelada: **`T2` sólo corre en el brazo `b3b`**; en el brazo `bx`, `T2` es `NO-CONSTRUIBLE-EN-ESTE-LIBRO`, declarado, y las celdas `T2 × ·` del brazo `bx` se reportan vacías con esa razón — no se sustituye `T2` por otra cosa.

**Reserva declarada:** «al menos una crónica» es una lectura **generosa** de «crónico complejo»; el instrumento no gradúa complejidad. Se congela así, con la reserva escrita, para que nadie la lea después como si el instrumento hubiera medido complejidad.

---

## 2 · Desenlaces — dos, POR SEPARADO

### 2.1 · D-HS (primario) — hospitalización

Es el desenlace que corresponde a «grave»: la hospitalización es el uso de servicio que la regla predice cuando «la complejidad excede al consultorio».

**Universo del desenlace:** personas con `hs01 == 1` (`ESTUVO HOSPITALIZADO`) **cuyo motivo** en `iiib_hs1.dta` sea `hs08_1a == 1` (ENFERMEDAD) **o** `hs08_1e == 1` (OPERACION).

**Exclusiones declaradas, no silenciosas:** `hs08_1c` (PARTO) y `hs08_1b` (ACCIDENTE) **se excluyen** — ninguno de los dos es «síntoma grave o crónico complejo» en el sentido de la regla. Se excluyen también, por el mismo criterio y por simetría de que la lista es exhaustiva, `hs08_1d` (AGRESION FIS), `hs08_1f` (ANALISIS), `hs08_1g` (ABORTO) y `hs08_1h` (OTRO), salvo que la fila también marque `hs08_1a` o `hs08_1e`. **Caja reporta el conteo de cada motivo excluido**, no sólo el total.

**Desenlace binario:** proporción `PÚBLICO` sobre el universo de arriba, con la tabla de §2.2.

### 2.2 · Tabla de clasificación de D-HS — **DOS tablas, una por libro** (corrección verificada al encargo)

El encargo congela **una** tabla: `PÚBLICO = hs02a|b|c|d|g`, `PRIVADO = hs02e|f`, `OTRO = hs02h|i|j|k`. Verificado contra el inventario: **esa tabla es correcta para el libro `b3b` y sería gravemente incorrecta aplicada al libro `bx`, porque el mapa de letras no es el mismo archivo a archivo.**

**Tabla A — libro `b3b`, `ehh02dta_all/ehh02dta_b3b/iiib_hs.dta` (líneas 35026-35036).** Es la tabla que la mesa firmó, verbatim del inventario:

| variable | etiqueta verbatim | clase congelada |
|---|---|---|
| `hs02a` | INTERNADO SSA | **PÚBLICO** |
| `hs02b` | INTERNADO IMMS *(sic, transposición del instrumento)* | **PÚBLICO** |
| `hs02c` | INTERNADO ISSSTE | **PÚBLICO** |
| `hs02d` | INTERNADO PEMEX SEDENA | **PÚBLICO** |
| `hs02g` | INTERNADO CENTRO RURAL | **PÚBLICO** |
| `hs02e` | INTERNADO HOSPITAL PRIVADO | **PRIVADO** |
| `hs02f` | INTERNADO CONsultorio PRIVADO *(sic, caja mixta del instrumento)* | **PRIVADO** |
| `hs02h` | INTERNADO CRUZ ROJA | OTRO |
| `hs02i` | INTERNADO CASA PRACTICANTE | OTRO |
| `hs02j` | INTERNADO CASA | OTRO |
| `hs02k_1` | INTERNADO OTRO LUGAR | OTRO |

**Tabla B — libro `bx`, `ehh02dta_all/ehh02dta_bx/p_hs.dta` (líneas 37241-37255). El mapa de letras es OTRO.** No es una variante menor: `hs02f` pasa de `CONsultorio PRIVADO` a `CASA MEDICO`, `hs02g` de `CENTRO RURAL` a `DIF`, `hs02h` de `CRUZ ROJA` a `ENFERMERA`, y el libro tiene **catorce** categorías (`a`…`n_1`) donde `b3b` tiene once. Aplicar la Tabla A al brazo `bx` clasificaría `DIF` con la letra de `CENTRO RURAL` y `ENFERMERA` con la de `CRUZ ROJA` — el resultado no sería un error de etiqueta, sería una proporción falsa. La clasificación de la mesa (qué instituciones son públicas) se propaga **por institución**, no por letra:

| variable | etiqueta verbatim | clase congelada |
|---|---|---|
| `hs02a` | INTERNADO SSA | **PÚBLICO** |
| `hs02b` | INTERNADO IMSS | **PÚBLICO** |
| `hs02c` | INTERNADO ISSSTE | **PÚBLICO** |
| `hs02d` | INTERNADO PEMEX SEDENA | **PÚBLICO** |
| `hs02g` | INTERNADO DIF | **PÚBLICO** |
| `hs02i` | INTERNADO UNIDAD MOVIL | **PÚBLICO** |
| `hs02k` | INTERNADO DISPENSARIO MEDICO | **PÚBLICO** |
| `hs02e` | INTERNADO HOSPITAL PRIVADO | **PRIVADO** |
| `hs02f` | INTERNADO CASA MEDICO | **PRIVADO** |
| `hs02l` | INTERNADO FARMACIA | **PRIVADO** |
| `hs02h` | INTERNADO ENFERMERA | OTRO |
| `hs02j` | INTERNADO CRUZ ROJA | OTRO |
| `hs02m` | INTERNADO PRACTICANTE TRAD. | OTRO |
| `hs02n_1` | INTERNADO OTRO LUGAR | OTRO |

La Tabla B **no es una decisión nueva de dirección**: es la misma asignación institución→clase que la mesa firmó para `ce04*` (§2.3, donde `DIF`, `UNIDAD MOVIL` y `DISPENSARIO` van a PÚBLICO; `FARMACIA` a PRIVADO; `ENFERMERA`, `CRUZ ROJA` y `PRACTICANTE` a OTRO), aplicada a las etiquetas verificadas del otro archivo. Donde la firma de mesa no habla, esta spec no inventa: **`bx` no tiene ninguna categoría equivalente a `CENTRO RURAL`, y `b3b` no tiene `DIF`, `UNIDAD MOVIL`, `DISPENSARIO` ni `FARMACIA` en `hs02*`** — cada tabla clasifica sólo lo que su archivo trae.

**Nota de asimetría, declarada:** la clasificación de mesa manda `CRUZ ROJA` a OTRO en `hs02*` y también en `ce04*`; manda `FARMACIA` a PRIVADO en `ce04*`. La Tabla B hereda ambas. Si caja lee el descriptor del `.dta` y encuentra que alguna etiqueta no corresponde a lo escrito aquí — el caso que la mesa nombró explícitamente («p. ej. `CENTRO RURAL` no es SSA») — **lo reporta y no reclasifica**; la celda se emite con la tabla congelada y la discrepancia va al recibo.

### 2.3 · D-CE (secundario) — consulta externa

**Universo del desenlace:** personas con `ce01 == 1` (`HA IDO AL DOCTOR SIN HOSPITAL` en `b3b:34708`; `FUE AL DOCTOR` en `bx:36833` — texto distinto, misma variable, declarado).

**Tabla de clasificación, idéntica en los dos libros** (verificado letra por letra: `b3b:34711-34724` y `bx:36836-36849` traen el mismo mapa `a`…`n_1`; ésta es la razón por la que la divergencia de §2.2 pasó inadvertida — en `ce04*` no hay divergencia):

| variable | etiqueta verbatim (`b3b`) | clase congelada |
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

**Ventana de D-CE:** el benchmark web indica «últimas 4 semanas» (§0.4). **Se lee y se declara con página** desde el cuestionario en corpus antes de calcular; mismo trato que §1.1. La spec **no** la congela sobre el benchmark web.

### 2.4 · Reglas comunes a los dos desenlaces, congeladas

1. **`OTRO` queda fuera del contraste y se cuenta.** El denominador de la proporción es `PÚBLICO + PRIVADO`; `OTRO` se reporta como conteo y como fracción del total de usuarios del servicio, en su propia columna. Nunca se reparte, nunca se imputa.
2. **Respuestas múltiples.** Las baterías `hs02*` y `ce04*` son marcas independientes, no una categórica: una persona puede marcar público y privado a la vez. Congelado: **la unidad es la persona-desenlace**, y una fila que marca ambos entra en una cuarta columna **`AMBOS`**, fuera del numerador y fuera del denominador del contraste, **contada**. Caja reporta `PÚBLICO`, `PRIVADO`, `AMBOS`, `OTRO` y `NINGUNO` como cinco conteos que suman el universo. La proporción pre-registrada es `PÚBLICO / (PÚBLICO + PRIVADO)` sobre las filas exclusivas.
3. **`hs03*`/`ce05*`/`hs04`/`ce06` (conteos de veces) NO entran en el desenlace de esta spec.** Se citan como existentes (§0.2) y quedan para un sucesor si mesa quiere un desenlace por intensidad. Congelar dos definiciones y elegir después es lo que el pre-registro impide.
4. **Contraste pre-registrado:** `P(PÚBLICO | T) − P(PÚBLICO | no T)`, sobre usuarios del servicio, **con su IC95**, por disparador × desenlace:

| | D-HS (primario) | D-CE (secundario) |
|---|---|---|
| **T1** (`es09`) | celda 1 | celda 2 |
| **T2** (`ec01*`) | celda 3 | celda 4 |

**4 celdas de contraste × 2 brazos de universo (§3) = 8 filas reportadas**, cada una con su IC95 — menos las `T2 × ·` del brazo `bx`, `NO-CONSTRUIBLE-EN-ESTE-LIBRO` (§1.2). Es decir: **6 filas estimables como máximo**, y las 2 restantes se emiten con su razón escrita, no en blanco.

---

## 3 · Universo y ponderador

### 3.1 · Brazo principal — `b3b`, universo directo

Archivos `iiib_*` (`ehh02dta_all/ehh02dta_b3b/`), ponderador **`fac_3b`** (sin `_px`), `ehh02w_all/ehh02w_b3b.dta`, `n_no_nulo_gt0 = 19 809` — cifra medida por `MAESTRA38-C1` y **reproducida exacta** por `L16-BIS-2` (`FP-332`). Universo de personas presentes del Libro IIIB (`es09` = «SERIO»). Es el brazo **principal** de esta Rama A′, y el único donde corren las 4 celdas.

### 3.2 · Brazo aparte — `bx`, proxy

Archivos `p_*` (`ehh02dta_all/ehh02dta_bx/`), subpoblación de **miembros ausentes respondidos por proxy** (`es09` = «GRAVE»). **Nunca se agrupa con `b3b`, nunca se promedia con él, nunca se compara contra un marginal poblacional** (`A-bis 4`, `instrucciones-proyecto-v2_12.md`). Se reporta como brazo separado, con su declaración de subpoblación escrita en cada fila. Si caja necesita un marginal de referencia para `bx`, lo recalcula restringido al mismo universo `bx`.

### 3.3 · Ponderadores del brazo `bx` — **en pareja, los dos, declarado ANTES de ver el dato**

Éste es el punto que `FP-332 D1` obliga a rediseñar, y se rediseña **antes** de abrir dato, no después.

| candidato | archivo | `n_no_nulo_gt0`, libro `bx` completo (`C1`) | `n_no_nulo_gt0`, subconjunto `es09` no nulo (`L16-BIS-2`) |
|---|---|---|---|
| `fac_3b_px` | `ehh02w_all/ehh02w_bx.dta` | 21 645 | **5 103** |
| `fac_3a_px` | ídem | 21 631 | **5 128** |
| `fac_4_px` | ídem | 9 037 | 1 972 |

`v1.1 §1.3` adjudicó `fac_3b_px` por correspondencia sección→libro y por su ventaja de 14 observaciones sobre el libro completo, y escribió el `assert` que lo comprobaría sobre el subconjunto real. `L16-BIS-2` corrió ese `assert` y **falló**: sobre las filas de `p_es.dta` con `es09` no nulo (1 524 folios, 7 467 filas de ponderador resueltas con el join normalizado a entero), `fac_3a_px` lidera por **25** observaciones y el orden que `v1.1` exigía se invierte. `L16-BIS-2` hizo lo correcto: **paró y no sustituyó** — elegir ponderador después de ver el dato es exactamente lo que un pre-registro existe para impedir.

**Congelado aquí, antes de abrir dato:** el brazo `bx` se corre con **los dos** ponderadores, `fac_3b_px` **y** `fac_3a_px`, y **se reportan los dos**, fila por fila, lado a lado. **El veredicto del brazo `bx` sólo cuenta si los dos coinciden en signo** (los dos con IC95 enteramente por encima de cero, o los dos enteramente por debajo, o los dos conteniendo el cero). Si discrepan en signo, el brazo `bx` se emite como **`NO-CONCLUYENTE-POR-PONDERADOR`**, con las dos filas a la vista y sin elegir ninguna. `fac_4_px` queda descartado por cobertura en las dos mediciones (≈42% y ≈38% del líder) y no se corre.

**El chequeo de consistencia de `v1.1 §1.3` deja de ser `assert` y pasa a diagnóstico reportado.** Caja calcula los tres `n_no_nulo_gt0` sobre el subconjunto real de cada celda y los **imprime en el recibo**; ya no paran el proceso. Razón: el orden entre `fac_3b_px` y `fac_3a_px` ya se midió y ya se sabe que se invierte — que un hecho conocido dispare un `PARO` no añade información, sólo impide medir. Lo que sustituye a la guardia es la regla de coincidencia de signo de arriba, que es más estricta en lo que importa (el veredicto) y menos en lo que no (llegar a calcular).

### 3.4 · Llave de join

`folio` y `ls` se normalizan a **entero** en los dos lados **antes** de unir (`int(folio)`, sin ceros a la izquierda, sin punto decimal). Sin esto el join da 0 filas — hallazgo de `MAESTRA38-C1`, reproducido por `L16-BIS-2`: en `ehh02w_all.zip` `folio` es cadena con ceros a la izquierda (`'00001000'`) y en el microdato es `float64` (`2000.0`). **Un join de 0 filas no es un hallazgo de que el ponderador no aplica; es este bug.** Los `.dta` de HS/CE traen `folio` y `ls` (verificado: `iiib_hs.dta:35024`/`35049`, `iiib_ce.dta:34740`/`34741`), y `iiib_hs1.dta`/`iiib_ce1.dta` traen además `secuencia` (`35104`) — la llave de HS1 hacia HS es `folio`+`ls`+`secuencia`, no `folio`+`ls` sola; **caja verifica la cardinalidad del join HS→HS1 y la reporta** antes de usarlo (si `hs08_1*` viene por episodio y `hs02*` por persona, colapsar sin declararlo cambia el denominador).

---

## 4 · Escala de veredicto y qué significaría corroborar

Cada una de las 8 filas (§2.4 × §3) recibe **una** de estas cuatro:

| veredicto | condición |
|---|---|
| **CORROBORADA** | `P(PÚBLICO \| T) − P(PÚBLICO \| no T) > 0` y el IC95 excluye el cero |
| **CONTRARIA** | la diferencia es `< 0` y el IC95 excluye el cero |
| **NO-DISCRIMINA** | el IC95 contiene el cero |
| **NO-ESTIMABLE** | numerador `< 10` en cualquiera de las celdas que la diferencia necesita (guardia de n mínima, misma que `S4`/`S5`/`S8`/`v1.1 §3`); **o** `T2` en el brazo `bx` (§1.2); **o** el brazo `bx` completo si los dos ponderadores discrepan en signo (§3.3, se emite como `NO-CONCLUYENTE-POR-PONDERADOR`, subcaso declarado de esta fila) |

**Qué significaría corroborar.** Sería **la primera medición mexicana de `R4.4` con el síntoma y el lugar de atención en el mismo instrumento y en la misma persona**. La Rama B (`ENSANUT2024`, ya corrida por `MAESTRA38-LOTE-ENSANUT`, veredicto `NO-DISCRIMINA`) construyó su corte de severidad de forma **administrativa** — hospitalización/urgencias vs. consulta externa, es decir, el tipo de servicio usado como proxy de la gravedad — que es circular respecto del desenlace. Aquí el disparador (`es09` autorreportado, o una crónica diagnosticada) y el desenlace (a qué institución acudió) son preguntas distintas del mismo cuestionario a la misma persona. Eso no vuelve causal el resultado (§reservas), pero sí lo vuelve una medición de la regla y no de su propia definición.

**Reservas, declaradas antes de medir.** Asociación transversal, sin identificación causal. El `PORQUE` de la regla («la complejidad excede al consultorio») es mecanismo, no antecedente exigible — no se mide, mismo criterio que el resto de la serie. `T1` es autorreporte no anclado a diagnóstico; `T2` es diagnóstico reportado sin gradación de complejidad; ninguno de los dos es «gravedad» medida. Los cortes de §2.2/§2.3 están congelados **sobre etiquetas del inventario**, no sobre el codebook — caja los coteja contra el descriptor del `.dta` y reporta discrepancias sin reclasificar (§2.2).

---

## 5 · `se_mueve_si` — sustituye a la de `v1.1` para la Rama A

`v1.1 §5` escribió, para la Rama A: *«si entre quienes reportan síntoma grave (`es09=1`, 2002/2005) la proporción que acude a institución pública (vía `clave1`/`clave2`, 2002) **no es mayor** que la que acude a privada, la regla se rompe para esa rama»* — una cláusula que **nadie podía disparar**, porque `clave1`/`clave2` no clasifican institución (§0.1) y `L16-BIS-2` lo confirmó al abrir el dato. Es el defecto que `MAESTRA38-LOTE-CRUCE` ya dejó como regla candidata en `forense/hallazgos.md`: *«un `se_mueve_si` que nadie puede disparar es un cierre con otra cara»*.

**La sustituye, para la Rama A′ y sólo para ella:**

> **`R4.4` se mueve si**, en el brazo principal `b3b` de ENNViH-1 2002, la celda **T1 × D-HS** (§2.4, celda 1 — el disparador y el desenlace que más literalmente leen «grave» y «la complejidad excede al consultorio») resulta **CONTRARIA** o **NO-DISCRIMINA** con numeradores suficientes (`≥ 10` en las cuatro casillas de la diferencia). Es decir: si entre quienes reportan problema serio de salud la proporción que se hospitaliza en institución pública **no es mayor** que entre quienes no lo reportan, el `ENTONCES` de la regla no se sostiene en el único instrumento mexicano que pregunta las dos cosas a la misma persona.

**Lo que NO mueve la regla, declarado para que no se lea de más:** un `NO-ESTIMABLE` por n (no es evidencia en ninguna dirección); un resultado del brazo `bx` solo (subpoblación proxy, `A-bis 4`); una discrepancia de signo entre los dos ponderadores de `bx` (§3.3); un resultado de D-CE sin D-HS (D-CE es secundario: la consulta externa es precisamente el escenario que la regla **no** describe). Las celdas de `T2` **no** disparan por sí solas el movimiento de la regla, pero son las primeras que dan una medición al «crónico complejo» del antecedente, que hoy no tiene ninguna (§7).

**Lo que ya no aplica:** la cláusula de `v1.1 §5` «Fila B-bis (ponderador)», que hacía del `assert` de `§1.3` un `se_mueve_si`. Ese `assert` ya se corrió y ya falló (`FP-332 D1`); su sucesor está en §3.3 como regla de coincidencia de signo, que es un criterio de veredicto, no una cláusula de movimiento de la regla.

---

## 6 · Archivos que la caja necesita abrir

**Los de `v1.1 §6` Rama A que esta pieza usa**, mismos ids y mismos sha256 (`data/manifiesto.yaml`, verificados al redactar):

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `ennvih1_2002_hogar_dta` | `ennvih/ehh02dta_all.zip` | `8b9b51904ca8790421d82a8a81f7f4edbce9a296cba2ce86fef74f8f379b5923` |
| `ennvih1_2002_ponderador` | `ennvih/ehh02w_all.zip` | `bbe8006844f715c19b724ebb74f1408c4cfa07e2efdfe7d6748b5182ef214587` |
| `ennvih1_2002_hogar_cb` | `ennvih/ehh02cb_all.zip` | `a3220412505d6684e50548bdd1e01ce816d3af99ed846e4e27f30f35e9b506b2` |

Miembros concretos: `ehh02dta_all/ehh02dta_b3b/{iiib_es,iiib_ec,iiib_hs,iiib_hs1,iiib_ce,iiib_ce1}.dta` · `ehh02dta_all/ehh02dta_bx/{p_es,p_hs,p_ce}.dta` · `ehh02w_all/{ehh02w_b3b,ehh02w_bx}.dta`.

**Aviso heredado de `MAESTRA38-C1`, no re-derivado:** `ehh02cb_all.zip` usa **deflate64** en 9 de sus 11 miembros. `zipfile` de Python aborta limpio; `tar.exe` de Windows extrae el miembro con el tamaño correcto y **el contenido todo `00`** sin avisar. Usar `zipfile-deflate64` o equivalente, y comprobar la firma `%PDF` antes de leer. Un codebook de ceros se lee igual que un codebook que no dice nada.

**Cuestionario — corrección al encargo, verificada.** El encargo pedía añadir `ehh02q_b3b.pdf` citando su URL pública, con la receta `A.5` por si caja no lo alcanza. **No hace falta: el cuestionario ya está en corpus, registrado en el manifiesto desde el 30/jul/2026**, y es la fuente correcta para las ventanas de §1.1 y §2.3:

| id de manifiesto | archivo | sha256 | tamaño |
|---|---|---|---|
| `ennvih1_2002_hogar_q` | `ennvih/ehh02q_all.zip` | `40af29bd864e967200dbbde2c9744795b33c0a23cdbb19902dd2ecdb7beb3cac` | 3 750 632 B |

Es el `.zip` de los cuestionarios PDF de **todos** los libros de hogar de ENNViH-1; el del Libro IIIB va dentro. Se cita por id de manifiesto, con sha256, no por URL — el sitio oficial además **no es alcanzable desde el entorno de esta pieza** (`EGRESS_BLOCKED`, §0.4), lo que hace del payload en corpus la única vía verificable. **Si caja no logra extraerlo** (mismo riesgo de deflate64 que el codebook): registra `NO OBTENIDO POR ESTE AGENTE` con `N` intentos y receta manual (`A.5`), y emite las celdas con la ventana marcada `NO DECLARADA` — no las omite y no inventa la ventana.

**No se listan** `ehh05dta_all.zip`, `ehh09dta_all.zip`, `ehh09w_all.zip` ni el `.sav` de ENDIREH 2016: fuera del perímetro de esta pieza (§0.4, §7).

---

## 7 · Qué NO hace este acto

No abre ningún `.dta`. No mide, no calcula ninguna celda ni ningún IC95. No mueve el tier de `salud.atencion.grave` (`[MEDIA]`, `canon/modelo-decision-v4_0.md:527`) ni sella `MEDIBLE-COMO-ESTÁ`. No toca `v1.0` ni `v1.1` — quedan íntegras en sus rutas (A.10). No reabre `FP-332`: `D1` se propaga íntegro (§3.3) y `D2` se reclasifica como `NO-ENCONTRADO` por su barrido (§0.3), sin retirar la firma, que es de `SELLO-3`. No pre-registra 2005 ni 2009, aunque el dato exista (§0.4). No adjudica cuál de los dos linajes `EXISTE-SATISFACE` de `v1.1 §0.2` es el canónico. No toca la propuesta, el motor, `milpa/**` ni `canon/**`.

**Sucesor declarado, no lanzado:** `L21` (caja, medición: hasta 4 contrastes × 2 brazos), gateado **por producto** al sha256 de esta pieza. Si `L21` corrobora con `T2`, es el primer dato que vuelve medible el «crónico complejo» del antecedente de `R4.4`, hoy sin ninguna medición.

**El primer resultado que produzca este procedimiento es el que se reporta — de cada celda y de cada brazo, por separado.**

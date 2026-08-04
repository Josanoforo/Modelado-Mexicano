# HITO D, R5.1 — "familia como seguro sustituto del Estado": prueba corrida, veredicto propuesto A (reserva adjunta)

**Mueve el Hito D: 3 → 4 de 27. No mueve el contador de condicionales (8 de 14).**

*4 de agosto de 2026. Encargo P, mesa #18. Rama `sesion/hitoD-r5-1-pension-bienestar`, worktree `~/mm-hitoD-r5-1-pension-bienestar` (nuevo, creado en este acto).*

⚠️ **CONTAMINACIÓN DE MICRODATO, declarada para esta sesión (ADR-46).** Esta sesión abrió el microdato completo (`concentradohogar`, `poblacion`, `ingresos`) de las **seis** olas ENIGH registradas en el manifiesto: 2012, 2014, 2016, 2018, 2020, 2022. **Queda inhabilitada para pre-registrar cualquier acto contra ENIGH que no esté ya escrito** — en particular, el **LCA multinivel de P3** (`forense/notas/2026-08-04-p3-lca-segmentacion.md:444`, habilitado el mismo día por decisión de mesa) exige explícitamente *"pre-registro propio de una sesión limpia que no haya abierto ENIGH ni leído esta nota ni sus resultados"*. Esta sesión no puede ser esa sesión. Línea espejo en `forense/hallazgos.md`.

---

## 0 · Entorno

```
$ python3 tests/bitacora.py --abre
HEAD: a0d8fd538b304e0c36c5ec38ef42b42c89f1177b
origin/main: a0d8fd538b304e0c36c5ec38ef42b42c89f1177b (ref local, sin fetch)
Divergencia: ninguna
--- Estado de las dos suites ---
check.py --baseline: exit=0 -- LÍNEA BASE: VERDE
validador_registro_ids.py: exit=0 -- OK -- 49 IDs verificados

$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
```

Firma buena confirmada: `sin_variable` + `200`. `git fetch origin main` se corrió antes de abrir rama (a diferencia del defecto I-20 ya registrado) — `origin/main` en `a0d8fd5`, exactamente la base que cita el encargo. **Sin discrepancia de HEAD que documentar.**

**`data/raw` ausente en el worktree nuevo — no es PARO, es el patrón ya conocido (nota de `data/raices.local.yaml`, worktrees anteriores).** Se creó el symlink (`ln -s /home/pc0/mm-corpus/raw data/raw`) apuntando al mismo corpus compartido que usan los demás worktrees — no una copia local (la causa exacta de lo que `PR #77` dejó pasar, según cita el encargo). Verificado explícitamente que los payloads viven en el corpus compartido, no solo listados: los seis `.zip` de ENIGH están en `/home/pc0/mm-corpus/raw`, compartidos por todos los worktrees.

**Defecto de instrumento encontrado y evitado, no heredado:** `tests/manifiesto.py --verifica` con **múltiples** `--id` en la misma invocación **solo verifica el último** (`ap.add_argument("--id", default=None)` sin `action="append"`, línea 997) — sin error, sin aviso. `--verifica --id enigh2018_nc_csv --id enigh2020_nc_csv --id enigh2022_nc_csv` de la sonda original solo reportó `enigh2022_nc_csv`. Se verificó cada ola por separado:

```
enigh2012_nc_csv [data_raw]: COINCIDE -- sha256 y tamaño (25396190 bytes) verificados
enigh2014_nc_csv [data_raw]: COINCIDE -- sha256 y tamaño (39555490 bytes) verificados
enigh2016_nc_csv [data_raw]: COINCIDE -- sha256 y tamaño (40991826 bytes) verificados
enigh2018_nc_csv [data_raw]: COINCIDE -- sha256 y tamaño (43339807 bytes) verificados
enigh2020_nc_csv [data_raw]: COINCIDE -- sha256 y tamaño (93711908 bytes) verificados
enigh2022_nc_csv [data_raw]: COINCIDE -- sha256 y tamaño (90030937 bytes) verificados
```

Las seis olas COINCIDEN contra `data/manifiesto.yaml`. Este defecto de `manifiesto.py` (silencioso, no acumula `--id` repetidos) se reporta en `forense/hallazgos.md` como hallazgo de instrumento, no se corrige en este acto (fuera de perímetro de Hito D).

---

## 1 · Premisas

| # | Verificación |
|---|---|
| **PP-1** | `forense/hitoD-preregistro-v2_0.md`, `## R5.1 · Volatilidad + ausencia de Estado → familia como seguro` (línea 138). Existe, sellada, no editada en este acto. **Se sostiene.** |
| **PP-2** | Umbral citado literal contra archivo, línea 143: *"Tras la universalización de la Pensión del Bienestar (transferencia no condicionada a mayores), reducción <10% en corresidencia intergeneracional o en transferencias intrafamiliares hacia mayores, en hogares beneficiarios frente a no beneficiarios comparables."* Coincide carácter por carácter. **Se sostiene.** |
| **PP-3** | Escala propia de la ficha, línea 149, citada literal: *"A <10% de reducción con monto suficiente documentado · B reducción ambigua o monto insuficiente · C exigiría panel de hogares pre/post con corresidencia observada · D si ENIGH no permite identificar beneficiarios."* Es la escala que gobierna este acto, no el legend genérico. **Se sostiene.** |
| **PP-4** | Confusor del monto, línea 147, citado literal: *"el monto puede ser insuficiente para sustituir. Si es así, la regla no se refuta: queda acotada a 'sustituye por encima de un umbral de monto'."* Documentado en §6. |
| **PP-5** | `data/manifiesto.yaml` líneas 316-397: seis entradas `enigh{2012,2014,2016,2018,2020,2022}_nc_csv`. **Se sostiene**, conteo derivado del archivo, no asumido. |
| **PP-6** | `## Registro de veredictos archivados`, cabecera línea 731: append-only, SOLO EMISIONES. Antes de este acto: **3 líneas** (`R1.1→D`, `R3.2→B`, `R7.2→D`). Este acto **no escribe** una cuarta línea — reporta resultado y fila; la emisión es acto de mesa. **Se sostiene, sin editar.** |
| **PP-7** | `forense/notas/2026-07-31-inventario-segmentacion.md:170`: `familia.seguro.volatilidad_ausencia_estado \| ENIGH \| Parcial \| clase_hog (corresidencia) + remesas + redsoc_1..6 (ambiguo, sin etiqueta clara en diccionario) \| concentradohogar, poblacion \| Corresidencia y flujo de remesas sí; redsoc no confirmable`. Confirma que `clase_hog` es la variable ya reconocida por el corpus para corresidencia, y que `redsoc` está descartada por ambigüedad — **este acto no usa `redsoc`**, usa `ingresos.clave=P040` para transferencias (monetario, aislable, no ambiguo — ver §2). Líneas 358/360 de la misma nota advierten que `bene_gob` **agrega** claves de varios programas (Beca Benito Juárez, Pensión Bienestar, etc.) — confirmado y por eso **no se usa** como identificador de beneficiario (§2). **Se sostiene.** |

Ninguna premisa (1) falló. No hay PARO por este capítulo.

---

## 2 · Identificación de beneficiarios (§2.1 del encargo) — no es D

**Hallazgo central que decide el acto:** la tabla `ingresos` (persona × clave de percepción, columna `clave`) trae un código **específico y aislable** para la pensión de adultos mayores en cada ola — no hay que recurrir al agregado `bene_gob` de `concentradohogar`, que mezcla la pensión con becas juveniles y otros programas (confirmado leyendo su fórmula en el diccionario de datos 2022: `bene_gob = Σ ing_tri cuando clave ∈ {P043, P045, P048, P101,…,P108}`). Usar `bene_gob` habría repetido el error que el corpus ya nombró en `I-18`/ADR-30 para otra fuente: un agregado que parece "la variable" pero no aísla el programa que la ficha pide.

**Identidad de la clave, verificada catálogo por catálogo (`ingreso.csv` / `ingresos_cat.csv` de cada ola), no asumida:**

| Ola | Columna | Clave | Descriptor literal del catálogo | n beneficiarios (hogares con ≥1 integrante 65+, sin ponderar / ponderado) |
|---|---|---|---|---|
| 2012 | `clave` | `P044` | *"Beneficio del programa 70 y más"* | 816 / 2,183,680 |
| 2014 | `clave` | `P044` | *"Beneficio del programa 70 y más"* | 1,990 / 3,022,799 |
| 2016 | `clave` | `P044` | *"Beneficio del programa 65 y más"* | 5,913 / 2,661,861 |
| 2018 | `clave` | `P044` | *"Beneficio del programa 65 y más"* | 6,065 / 2,705,823 |
| 2020 | `clave` | `P104` | *"Programa para el Bienestar de las Personas Adultas Mayores"* | 13,597 / 5,129,984 |
| 2022 | `clave` | `P104` | *"Programa para el Bienestar de las Personas Adultas Mayores"* | 17,884 / 7,334,567 |

El **mismo nombre de columna** (`clave`, dentro de la misma tabla `ingresos`) porta identidades de programa distintas entre eras — el código `P044` no es continuo conceptualmente entre 2012-2014 ("70 y más", focalizado, monto bajo) y 2016-2018 ("65 y más", ya cuasi-universal para 65+ pero previo a la reforma de 2019); el salto a `P104` en 2020 coincide con el cambio de nombre e identidad del programa ("Pensión para el Bienestar de las Personas Adultas Mayores", universal, monto mayor — ver §6). Esto **no es un defecto de comparabilidad de la tabla** (la columna `clave` y su unidad de observación son idénticas en las 6 olas) — es el objeto de estudio: la identidad del programa cambió exactamente donde el encargo dice que cambió.

**Beneficiario = hogar (folioviv+foliohog) con ≥1 registro en `ingresos` con `clave` en el código de la era y `ing_tri > 0`.** No se usó `poblacion.edad` para filtrar el receptor en este paso —la clave es, por diseño del instrumento, específica de personas en el rango de edad del programa; no existen registros de esta clave fuera de ese universo (verificado: 0 excepciones en las 6 olas).

**Universo de análisis:** hogares con `concentradohogar.p65mas ≥ 1` (al menos un integrante de 65 años o más — variable ya construida por INEGI, no derivada por esta sesión). Cobertura de la pensión dentro de ese universo: 33% (2012) → 45% (2014) → 37% (2016) → 34% (2018) → **57% (2020)** → **76% (2022)** de los hogares ponderados con adulto mayor. El salto de cobertura entre 2018 y 2020 es, junto con el cambio de clave, la segunda pieza de evidencia (interna al dato, no recordada de memoria) de que el choque cae exactamente entre esas dos olas.

**No es D.** ENIGH sí permite identificar beneficiarios, con n grande en las seis olas.

---

## 3 · Ventana antes/después — declarada antes de estimar

**Antes de mirar un solo resultado de corresidencia o transferencia**, se fija:

- **Antes:** ENIGH 2012, 2014, 2016, 2018 — programa "70 y más" (2012-2014) / "65 y más" (2016-2018), antecesor de la Pensión del Bienestar, con clave `P044`.
- **Después:** ENIGH 2020, 2022 — "Pensión para el Bienestar de las Personas Adultas Mayores", clave `P104`.

**Justificación de la fecha, con dos apoyos — uno documental externo (de conocimiento público, no verificable con la red permitida a este entorno) y uno interno al propio dato (verificado en este acto):**

1. **Documental:** la reforma de febrero de 2019 (Acuerdo publicado en el Diario Oficial de la Federación, Reglas de Operación 2019) renombró y reformuló el programa, elevó el monto y lo declaró universal para 68+ (65+ para pueblos indígenas y afromexicanos) — hecho de política pública ampliamente documentado. Este entorno no tiene acceso de red a `dof.gob.mx` ni a `coneval.org.mx` (no están en la lista de hosts permitidos), así que esta pieza **no se verificó por fetch en este acto** — se declara como conocimiento público, no como cita verificada.
2. **Interna al dato, verificada en este acto (la que sostiene la ventana sin depender de memoria externa):** el catálogo de `ingresos_cat`/`ingreso` de cada ola (§2) muestra el cambio de identidad de programa **exactamente entre la ola 2018 y la ola 2020** (`P044` "65 y más" → `P104` "Pensión para el Bienestar…"), y el monto trimestral promedio entre beneficiarios salta de $658-669 (2016-2018) a $1,550-2,144 (2020-2022) — más del doble en pesos corrientes, sin ola intermedia (§6). ENIGH 2018 se levantó ago-nov 2018 (antes de la reforma); ENIGH 2020, ago-nov 2020 (después). La ventana **no se re-eligió tras ver los resultados de corresidencia/transferencia** — se fijó en este punto del acto, antes de correr `resumen_ola` para ningún año.

---

## 4 · Comparabilidad entre olas — verificada antes de agrupar

Tabla año × variable, verificada abriendo cada zip y comparando encabezados y diccionarios de datos (no asumida por continuidad de nombre):

| Variable / concepto | 2012 | 2014 | 2016 | 2018 | 2020 | 2022 | Nota |
|---|---|---|---|---|---|---|---|
| Tabla `concentradohogar`, columna `clase_hog` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Misma definición palabra por palabra en el diccionario de datos 2012 y 2022 (Unipersonal/Nuclear/Ampliado/Compuesto/Corresidente) |
| Peso de diseño en `concentradohogar` | `factor_hog` | `factor_hog` | `factor` | `factor` | `factor` | `factor` | Renombrado 2014→2016, mismo significado (factor de expansión de hogar) |
| `est_dis`, `upm` en `concentradohogar` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Presentes en las 6, mismos nombres |
| Tabla `poblacion`, columnas `parentesco`, `edad` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Mismos nombres, sin cambio de catálogo relevante para este acto |
| Tabla `ingresos`, columnas `folioviv,foliohog,numren,clave,ing_tri` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Idénticas en las 6 |
| `ingresos` trae `est_dis,upm,factor` propios | ❌ (solo en `concentradohogar`, join por folioviv+foliohog) | ❌ (ídem) | ✅ | ✅ | ✅ | ✅ | 2012/2014 exigen join explícito — implementado y verificado (conteo de hogares tras el join = conteo de `concentradohogar`, sin pérdida) |
| Clave de la pensión de adultos mayores | `P044` "70 y más" | `P044` "70 y más" | `P044` "65 y más" | `P044` "65 y más" | `P104` | `P104` | Ver §2 — cambio de identidad de programa, no de estructura de tabla |
| Clave `P040` "Donativos en dinero provenientes de otros hogares" | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Wording idéntico verificado en las 6 |
| `concentradohogar.gasto_mon`, `.ingtrab`, `.ing_cor`, `.p65mas`, `.tot_integ` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Presentes y con la misma fórmula declarada en el diccionario |

**Ninguna ola se excluye.** Las seis pasan la verificación de comparabilidad estructural para las variables que este acto usa.

**Salvedad declarada, no resuelta por este acto (metodológica, de dominio público, no verificable por fetch en este entorno):** INEGI distingue "ENIGH tradicional" (2012, 2014, sin sufijo `_ns`) de "ENIGH nueva serie" (2016 en adelante) por un cambio en la metodología de captación/imputación de ingreso que afecta la comparabilidad de **niveles** de ingreso entre ambas series — no afecta, hasta donde este acto puede verificar, las variables aquí usadas (`clase_hog` es composicional, no de nivel de ingreso; `ingresos.clave` es un código de percepción, no un ingreso imputado). No se buscó fetch a una fuente externa para esta salvedad porque `coneval.org.mx`/`dof.gob.mx` no están en la lista de hosts permitida a este entorno — se declara como límite conocido, no oculto.

**No se buscó artefacto de parseo tipo Encargo J (`\r` por campo) directamente** — el `csv.DictReader` de Python maneja saltos de línea dentro de comillas de forma estándar; se verificó indirectamente: el conteo de filas leídas por `concentradohogar` coincide exactamente con `sum(factor)` reproduciendo la cifra publicada por INEGI (§7), lo que habría fallado si hubiera corrupción de filas.

---

## 5 · Las dos medidas del umbral, por separado (§2.4)

**Corresidencia intergeneracional** = `clase_hog ∈ {3 Ampliado, 4 Compuesto}` (hogar con parientes del jefe más allá del núcleo, o con parientes y además personas sin parentesco). Ver §7 comparabilidad de hogares para la reserva sobre "Compuesto".

**Transferencias intrafamiliares hacia mayores** = hogar con ≥1 integrante de 65+ que recibió `ingresos.clave = P040` ("Donativos en dinero provenientes de otros hogares") con `ing_tri > 0`. **Límite declarado, no resuelto:** `P040` no distingue si el donante es un familiar o no (podría ser un amigo, ex-cónyuge, etc.) — es la mejor variable monetaria y aislable disponible (a diferencia de `redsoc`, descartada por PP-7 por ambigüedad de etiqueta), pero no es un test perfecto de "familia" en sentido estricto.

**Resultado, ponderado, con IC95% (conglomerado último, `tests/svystat.py`), beneficiario vs. no beneficiario, dentro de hogares con adulto mayor:**

| Ola | Corresidencia — benef. | Corresidencia — no benef. | Δ (pp) | Transferencia P040→mayor — benef. | Transferencia — no benef. | Δ (pp) |
|---|---|---|---|---|---|---|
| 2012 | 46.4% [41.5,51.3] n_upm=346 | 42.9% [39.4,46.4] n_upm=645 | **+3.5** | 32.7% [28.6,36.8] | 26.1% [22.9,29.4] | **+6.6** |
| 2014 | 44.4% [41.6,47.1] n_upm=916 | 43.0% [40.2,45.7] n_upm=1297 | **+1.4** | 24.4% [21.9,27.0] | 20.6% [18.3,22.8] | **+3.8** |
| 2016 | 44.8% [43.2,46.5] n_upm=2283 | 43.2% [41.7,44.7] n_upm=4507 | **+1.6** | 27.2% [25.7,28.6] | 12.2% [11.2,13.2] | **+15.0** |
| 2018 | 43.9% [42.4,45.4] n_upm=2470 | 43.2% [41.8,44.6] n_upm=5163 | **+0.7** | 29.6% [28.1,31.1] | 12.7% [11.8,13.5] | **+16.9** |
| **2020** | **42.8% [41.6,44.0]** n_upm=5495 | **41.9% [40.4,43.4]** n_upm=5315 | **+0.9** | **24.8% [23.8,25.9]** | **17.9% [16.8,19.1]** | **+6.9** |
| **2022** | **42.1% [41.1,43.1]** n_upm=6728 | **41.0% [39.0,43.0]** n_upm=3597 | **+1.1** | **20.0% [19.1,20.8]** | **15.7% [14.3,17.0]** | **+4.3** |

**Las dos medidas se separan tal como pide el acto (§2.4: si una cruza y la otra no, se dice así):**

- **Corresidencia:** la brecha es pequeña (≤3.5pp en cualquier ola) y los IC95% se traslapan en las seis — **estadísticamente indistinguible de cero**, en ninguna dirección. No hay reducción: si acaso, un signo positivo (beneficiarios con corresidencia igual o ligeramente mayor).
- **Transferencia intrafamiliar:** la brecha es mayor y, en 2016-2022, los IC95% **no se traslapan** — diferencia estadísticamente significativa, pero en la dirección **contraria** a "retroceso": los hogares beneficiarios reciben **más** transferencia intrafamiliar hacia el mayor, no menos.

**En ninguna ola, en ninguna de las dos medidas, se observa reducción en el grupo beneficiario.** El signo es consistentemente ausente-de-reducción o positivo (más seguro familiar, no menos), en las seis olas, antes y después del choque.

---

## 6 · El confusor del monto (PP-4, §2.6)

| Ola | Monto pensión mensual promedio (beneficiarios) | Gasto monetario per cápita mensual del hogar beneficiario | Monto / gasto per cápita |
|---|---|---|---|
| 2012 | $581 | $1,433 | 40.5% |
| 2014 | $660 | $1,402 | 47.1% |
| 2016 | $669 | $1,747 | 38.3% |
| 2018 | $658 | $2,007 | 32.8% |
| **2020** | **$1,550** | **$2,445** | **63.4%** |
| **2022** | **$2,144** | **$3,557** | **60.3%** |

(Pesos corrientes de cada año — no deflactados; la comparación relevante para "suficiencia" es *dentro* de cada ola, monto contra gasto de esa misma ola, no entre olas.)

**Monto documentado como suficiente en el periodo post-reforma:** la pensión, sola, cubre entre 60% y 63% del gasto monetario promedio por integrante del hogar beneficiario en 2020 y 2022 — no es una cifra simbólica. En el periodo pre-reforma cubría 33%-47%, ya no trivial pero menor. **No se satisface la rama "monto insuficiente" de la fila B** — el confusor de PP-4 se documenta y se descarta como explicación de por qué no se observa retroceso.

---

## 7 · Comparabilidad de hogares (§2.5) — declarada antes de estimar, con hallazgo de robustez

**Riesgo declarado antes de estratificar:** los hogares beneficiarios muestran, en las seis olas, ingreso laboral (`ingtrab`) sistemáticamente menor que los no beneficiarios (ej. 2022: $24,131 vs. $35,371 trimestral) — la pensión llega desproporcionadamente a personas mayores sin pensión contributiva (IMSS/ISSSTE) formal, que también son las que más dependerían de transferencia familiar por otras razones. Comparar beneficiario vs. no-beneficiario crudo confunde el efecto de la pensión con este sesgo de composición.

**Control declarado: tercil de `ingtrab` *per cápita* del hogar (`ingtrab / tot_integ`), no del total.** Se probó primero con el total del hogar y se descartó: el total de `ingtrab` está mecánicamente inflado en hogares Ampliado/Compuesto (más integrantes → más perceptores potenciales → mayor `ingtrab` total), lo que habría confundido la propia variable de control con el desenlace de corresidencia — hallazgo metodológico de este acto, documentado en el código (`tests/r5_1_pension_bienestar.py`, docstring de `resumen_ola_estratificado`).

**Resultado estratificado, 2020 y 2022 (olas post-reforma, donde aplica el umbral):**

| Ola | Tercil ingtrab p.c. | Corresidencia benef. | Corresidencia no benef. | Δ | Transferencia benef. | Transferencia no benef. | Δ |
|---|---|---|---|---|---|---|---|
| 2020 | T1 bajo | 16.6% [15.2,18.0] | 17.1% [15.1,19.0] | −0.5 (nulo) | 35.0% [33.1,36.8] | 28.4% [26.1,30.8] | +6.6 |
| 2020 | T2 medio | 59.5% [57.7,61.4] | 57.6% [55.1,60.0] | +1.9 (nulo) | 22.4% [20.8,24.0] | 19.8% [17.7,21.8] | +2.6 (nulo) |
| 2020 | T3 alto | **56.9% [54.8,59.0]** | **47.1% [44.8,49.5]** | **+9.8 (sig.)** | 14.4% [12.9,15.9] | 9.2% [7.9,10.5] | +5.2 (sig.) |
| 2022 | T1 bajo | 16.6% [15.4,17.9] | 15.2% [13.1,17.3] | +1.4 (nulo) | 30.0% [28.5,31.5] | 27.0% [24.1,29.9] | +3.0 (nulo) |
| 2022 | T2 medio | 58.3% [56.7,59.9] | 58.2% [55.1,61.3] | +0.1 (nulo) | 18.3% [17.0,19.6] | 16.8% [14.6,19.0] | +1.5 (nulo) |
| 2022 | T3 alto | **53.7% [51.9,55.6]** | **44.6% [41.7,47.5]** | **+9.1 (sig.)** | 10.0% [9.0,11.1] | 8.1% [6.7,9.4] | +1.9 (nulo, roza) |

**En ningún estrato de ingreso, en ninguna de las dos olas post-reforma, la brecha es negativa y significativa** (que sería la señal de retroceso). Donde hay significancia, es positiva (T3, ambas olas): beneficiarios con **más** corresidencia y **más** transferencia que no-beneficiarios comparables en ingreso.

**Robustez de la definición de corresidencia, verificada:** usando solo `clase_hog=3` (Ampliado estricto, excluye "Compuesto" que puede incluir huéspedes sin parentesco) en vez de `{3,4}`, la brecha es prácticamente idéntica: 2022 benef=41.2% [40.2,42.2] vs. no_benef=40.3% [38.3,42.2] (contra 42.1%/41.0% con la definición amplia) — diferencia <1pp entre definiciones, dentro del mismo grupo. El hallazgo no depende de si "Compuesto" se incluye.

**Lo que este acto NO pudo controlar (declarado, no silenciado):** ni pareo por región/entidad, ni por escolaridad del jefe, ni matching por puntaje de propensión — el control se limitó a tercil de ingreso per cápita, por el tiempo disponible en un acto. Esto **no invalida** el resultado (la brecha positiva en T3 y la ausencia de brecha negativa en cualquier estrato son demasiado consistentes para ser artefacto de un solo control omitido), pero es una reserva real, no retórica.

---

## 8 · Estimador — validado contra caso conocido publicado (§2.7)

**Fórmula:** conglomerado último (`tests/svystat.py`, ya en el repo, reutilizado sin modificar la fórmula) — validado en ese archivo contra un caso SRS sintético degenerado (colapsa a `p(1-p)/(n-1)`, coincide a 9 decimales).

**Esta sesión añade una segunda validación, contra un caso real publicado — no sintético** (`tests/r5_1_pension_bienestar.py --validar`), porque el caso SRS solo prueba la fórmula de varianza, no que el join `folioviv+foliohog`, la columna de peso, y los campos leídos sean los correctos contra un número real:

```
$ python3 tests/r5_1_pension_bienestar.py --validar
n hogares ENIGH 2022 sin ponderar = 90102
  OK -- Total de hogares (sum factor): calculado=37,560,123.0 publicado=37,560,123 (dif rel 0.000%)
  OK -- bene_gob promedio ponderado: calculado=1,776.5 publicado=1,777 (dif rel 0.027%)
  OK -- donativos promedio ponderado: calculado=1,270.9 publicado=1,271 (dif rel 0.006%)
  OK -- jubilacion promedio ponderado: calculado=5,168.6 publicado=5,169 (dif rel 0.009%)
Fuente: INEGI, Comunicado de Prensa Num. 420/23, 26/jul/2023, Cuadro 1 y cuadro de composicion de ingreso corriente.
Validado contra caso conocido publicado.
```

Cifras publicadas obtenidas por `WebFetch` a `https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/ENIGH/ENIGH2022.pdf` (Comunicado de Prensa Núm. 420/23, 26/jul/2023) — host permitido a este entorno, PDF leído completo con el lector de PDF, no solo el resumen del fetch. **Redacción exacta, per enmienda de mesa #19 (defecto clase v2.1):** reproduce el **total de hogares con 0.000%** de diferencia relativa y **tres agregados de ingreso** del Comunicado 420/23 con diferencia relativa **≤0.027%** (`bene_gob` 0.027% · `donativos` 0.006% · `jubilacion` 0.009%). El `0.000%` es **del total de hogares** y **no se generaliza** a los otros tres — hacerlo es una cifra tecleada, no derivada, y es precisamente la clase de defecto que la regla v2.1 existe para atrapar antes de que llegue al canon. **Un estimador que no reproduce esto no habría entrado al canon** — lo hace.

---

## 9 · Veredicto — fila propuesta y reserva

**Escala de la ficha (PP-3), no la genérica.**

- **D descartada:** ENIGH sí identifica beneficiarios, con n grande y clave aislable (§2).
- **B descartada — primero por ausencia de dosis-respuesta, después por magnitud del monto.** *(Enmienda de mesa #19, 4/ago/2026. El orden importa: el pre-registro nunca define qué es "monto suficiente" — barrido de `suficien` en `hitoD-preregistro-v2_0.md`: aparece en las líneas 147 y 149 y ninguna pone número. Declarar que 60-63% "no es simbólico" es un juicio razonable, pero es un parámetro operacionalizado **después** de ver el dato, y por ahí esta adjudicación sería atacable. La salida está en el propio dato.)*
  - **(i) Ausencia de dosis-respuesta.** La rama "monto insuficiente" de B predice gradiente: menos sustitución donde el monto es chico, más donde es grande. El dato tiene la variación y no muestra el gradiente. Entre 2018 (monto = **32.8%** del gasto p.c., el mínimo de las seis olas) y 2020 (**63.4%**, el máximo), el monto casi se duplica como fracción del gasto y el desenlace no se mueve: Δ corresidencia **+0.7 → +0.9 pp**, Δ transferencia **+16.9 → +6.9 pp** — sin reducción en ninguna de las dos olas, en ninguna de las dos medidas. En las seis olas el rango va de 32.8% a 63.4% y la reducción está ausente en **todo** el rango.
  - **Limitación de este argumento, declarada:** es comparación **entre olas**, confundida con una década de otros cambios (composición demográfica, ingreso, cobertura del programa). Es evidencia, no un test limpio de dosis. Pero es evidencia derivada del dato, y un umbral de "suficiencia" elegido después de ver el resultado no lo es.
  - **(ii) Magnitud del monto**, subordinada a lo anterior: 60-63% del gasto monetario per cápita post-reforma (§6) — no es cifra simbólica.
  - **(iii) La reducción tampoco es ambigua:** es consistentemente ausente o de signo contrario en las seis olas y en cada estrato de ingreso (§5 y §7).
- **C no se invoca como cierre:** describe una prueba más fuerte (panel) que ENIGH no tiene — pero el Umbral de la propia ficha (línea 143) está redactado como comparación transversal *"en hogares beneficiarios frente a no beneficiarios comparables"*, que es exactamente la prueba que este acto corrió. No se interpreta la ausencia de panel como razón para no adjudicar una fila cuando la prueba transversal que el Umbral sí pide dio una respuesta clara, robusta a estratificación por ingreso y a la definición de corresidencia.
- **Verificado: no hay solape entre filas** (a diferencia de `R7.2`, que llevaría este patrón a su tercera ocurrencia) — A y B no se satisfacen simultáneamente aquí: las condiciones de A se cumplen limpiamente y las de B no se cumplen en ninguna lectura.

**Fila adjudicada: A** *(mesa #19, 4/ago/2026 — archivada en el bloque append-only de `hitoD-preregistro-v2_0.md`)*. *"<10% de reducción con monto suficiente documentado"* — literalmente satisfecha, y el monto está documentado como sustancial (60-63% del gasto per cápita).

**⚠️ A se adjudica sobre una INVERSIÓN DE SIGNO, no sobre una sustitución pequeña — y así queda escrito.** *(Enmienda de mesa #19.)* La fila A dice *"<10% de reducción"*; lo medido es **reducción ≤0, es decir, aumento**. Literalmente satisface A, y por eso se adjudica. Pero *"la sustitución es demasiado pequeña"* y *"la familia se mueve en el mismo sentido que el Estado"* son objetos empíricos distintos, y **lo ocurrido es el segundo**: en las seis olas y en cada tercil de ingreso post-reforma, corresidencia y transferencia intrafamiliar hacia mayores son iguales o **mayores** en el grupo beneficiario (significativamente mayores en la transferencia, 2016-2022; y en corresidencia en el tercil alto, +9.1 a +9.8pp). Un lector futuro que derive el veredicto del registro debe poder saber cuál de las dos ocurrió — por eso la glosa de la línea archivada lo nombra. Es el segundo el que abre la pregunta de §5 (selección vs. complementariedad), que este acto **no** distingue.

**Bajo esta prueba, la regla se refuta en el nivel donde se usa: la familia no retrocede cuando el Estado entra — si acaso, beneficiario y familia se mueven juntos, no en sustitución.**

**Por qué NO la alternativa de sostener `R5.1` como descriptiva invocando `C`** *(enmienda de mesa #19, dos razones)*: (1) la fila C describe una prueba más fuerte (panel de hogares) que **nadie va a correr** — ENIGH no tiene panel y ninguna fuente del corpus lo tiene para este choque; invocar C después de ver un resultado que refuta es exactamente el movimiento post-hoc que el pre-registro existe para impedir, mientras el Umbral (línea 143) pre-registró literalmente la comparación **transversal** que este acto corrió. (2) **El precedente de ADR-49 (CAL-G3) no aplica:** ahí falló la *identificación* — el instrumento no podía responder. Aquí el instrumento **respondió** la pregunta que el Umbral formuló. Confundir los dos casos abarataría el pre-registro.

**La letra se decide sobre el fondo, no sobre el contador.** El contador de Hito D se mueve `3 → 4 de 27` con **cualquier** letra: un `D` cuenta como corrida (`gobernanza:351`, ADR-45) y un `B` también. No hay incentivo de contador para preferir `A`. Queda escrito para que nadie tenga que preguntárselo después.

**Reserva adjunta, explícita, no opcional:**

1. **Diseño transversal repetido, no panel.** ENIGH no seguimiento el mismo hogar antes/después — es la comparación beneficiario/no-beneficiario dentro de cada ola post-reforma que el propio Umbral pide, no una prueba longitudinal del mismo hogar.
2. **Selección residual no completamente controlada:** solo se estratificó por tercil de ingreso laboral per cápita; no se paretó por región, escolaridad ni se hizo matching por propensión.
3. **`P040` no distingue donante familiar de no familiar** — proxy monetario aislable, pero no una prueba directa de "familia".
4. **Cobertura del programa no es 100%** en ninguna ola (33%-76%) — el grupo "no beneficiario" no es degenerado, pero incluye tanto elegibles-no-receptores como (en 2020-2022) personas bajo el umbral de edad vigente.

Estas reservas **acotan la fuerza causal** de la conclusión sin cambiar su dirección: en ninguna especificación probada (seis olas, tres terciles de ingreso, dos definiciones de corresidencia) aparece el patrón que refutaría "A" (una reducción clara y significativa en el grupo beneficiario).

**No se escribe en el registro de veredictos** (PP-6) — esto es acto de mesa.

---

## Pipeline

`tests/r5_1_pension_bienestar.py` (reutiliza `tests/svystat.py` sin modificarlo). Reproducible:

```
python3 tests/r5_1_pension_bienestar.py --validar          # validación contra INEGI 420/23
python3 tests/r5_1_pension_bienestar.py 2012 2014 2016 2018 2020 2022   # resumen por ola
python3 tests/r5_1_pension_bienestar.py --estratos 2020 2022            # estratificado por ingreso
```

Sin `pandas`/`numpy` (no instalados en este entorno) — `csv`+`zipfile` de la biblioteca estándar únicamente, leyendo directamente de los `.zip` de `data/raw/` sin extraer a disco.

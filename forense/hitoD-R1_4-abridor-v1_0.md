# HITO D · Falsador `R1.4` — ficha-abridor: resultados y **propuesta** de veredicto

### `hitoD-R1.4-abridor` · **v1.0** · 25 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R1_4-abridor-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R1.4-abridor`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La corrida (COMMIT 2) del falsador de `R1.4` sobre el panel ENNViH bajo la spec congelada en `hitoD-R1.4-especificacion`, y la **propuesta** de fila que de ella se sigue. |
> | **QUÉ NO ES** | **No archiva nada.** No escribe en el bloque `## Registro de veredictos archivados`. **No mueve el contador de Hito D.** |
> | **VERIFICAS ASÍ** | que cada negativo de aquí viene con su control positivo y con el número de archivos examinados, y que la cantidad NO-UMBRAL está rotulada como tal en todas sus apariciones. |

**Acto:** `ACTO PACK-UBUNTU-2` (abridor 2 de 2), 25/ago/2026, entorno **UBUNTU**, sobre `origin/main = 151cf04`. Salida cruda: `forense/notas/2026-08-25-r1-4-abridor-salida.txt`.

---

## 1 · PARTE A (rectora) — el Umbral no es construible, y la razón está medida

Barrido de las cabeceras de **425 archivos `.dta`** de las tres olas (ENNViH-1 2002 · ENNViH-2 2005 · ENNViH-3 2009), **0 fallos de lectura**:

| pieza del Umbral | patrón | columnas halladas |
|---|---|---|
| **Q1/Q2 · marca o sustituto funcional** | `marca\|brand\|generic\|genéric\|sustitut\|substitut` | **1**, y es **falso positivo** |
| **Q3 · métrica de compra/gasto** *(control positivo)* | `precio\|gasto\|compr\|cantidad` | **1274** |
| **Q4 · estratos D/E vs A/B** | `socioecon\|amai\|nivel social\|estrato social\|clase social` | **0** |
| **Q6 · presión de estatus** | `estatus\|aspirac\|prestigio\|posicion social` | **0** |

El único acierto de `Q1/Q2` es `iiib_gh.dta::gh01_1e`, *"FIESTAS GUSTA TOMAR: RON/BRANDY"* — la cadena `brand` dentro de **brandy**, un tipo de bebida en una pregunta sobre fiestas. **No es una variable de marca.** Descontado ése, la cobertura de marca en las tres olas es **cero**.

El control positivo es el que da valor al negativo: el mismo barrido, sobre los mismos 425 archivos, devuelve **1274** columnas de compra/gasto. El barrido lee etiquetas de verdad; los ceros son **ausencia medida, no barrido roto**.

**Conclusión de la PARTE A:** ENNViH **no puede construir** «prima pagada por marca sobre sustituto funcional equivalente». Faltan a la vez el sujeto de la cantidad (`Q1`), el término de comparación (`Q2`), los dos segmentos que el Umbral nombra (`Q4`) y el antecedente de presión de estatus (`Q6`). Lo que sí tiene en abundancia es justo lo que el Umbral **no** discute: gasto.

### 1.1 · El casi-acierto, medido y descartado por cobertura

ENNViH sí registra un **precio unitario** para diez rubros: `i_cs.dta::cs13a`–`cs13j` (*MONTO ESTIMADO KG/LT*), con su cantidad (`cs11*`) y su unidad (`cs12*_1`) — tortilla de maíz, bolillo/telera, pollo, bistec/milanesa, leche pasteurizada, huevo, jitomate rojo, frijoles, azúcar y refrescos. Es lo más parecido a una prima que este instrumento ofrece.

No sirve, y por **dos** razones independientes:

1. **No es la cantidad del Umbral.** Un precio unitario más alto por el mismo rubro mezcla marca, tamaño de empaque, tipo de establecimiento y calidad. Sin marca ni par de sustitutos, no hay «prima por marca». Sustituirlo sería re-anclar la regla — precisamente lo que la ficha prohíbe con *"No repetir"*, y la spec dejó esa prohibición escrita **antes** de saber si el ancla original era construible.
2. **Cobertura casi nula, medida:**

| ola | hogares | tortilla | pollo | leche | huevo | refrescos |
|---|---|---|---|---|---|---|
| 2002 | 8051 | 44 (0.5%) | 193 (2.4%) | 91 (1.1%) | 208 (2.6%) | 340 (4.2%) |
| 2005 | 8116 | 32 (0.4%) | 242 (3.0%) | 58 (0.7%) | 175 (2.2%) | 272 (3.4%) |
| 2009 | 9072 | 46 (0.5%) | 401 (4.4%) | 91 (1.0%) | 560 (6.2%) | 166 (1.8%) |

Entre **0.4% y 6.2%** de los hogares según rubro y ola: es una sub-pregunta residual, no una medición poblacional. **Aun sin la prohibición de re-anclar, no sostendría una comparación entre segmentos.**

---

## 2 · PARTE B (subordinada, NO-UMBRAL) — corrida, y no estimable

Se ejecutó como la spec la definió y **no produjo ninguna cifra utilizable**: las diez celdas quedaron por debajo del mínimo de 30 pre-declarado (el mayor par fue huevo, `n=25` bloqueadas contra `n=62` ascendentes), consecuencia directa de la cobertura de §1.1. **No se reporta ninguna diferencia de precio**, porque no la hay que reportar.

Lo que sí quedó construido y es reutilizable: **1383** personas de ENNViH-3 con escolaridad propia y de ambos padres, de las cuales **398** tienen movilidad educativa bloqueada y **985** ascendente; 1353 con ponderador `fac_3b`, 1329 ligadas al precio de su hogar.

### 2.1 · Defecto que la corrida encontró en la propia spec — declarado, no corregido hacia atrás

La spec escribió el criterio como `ed05 ≤ max(tp11m, tp11p)`. **Esas dos variables no comparten codificación:**

- `ed05` (escolaridad propia) usa **10 códigos** — `05` = *Secundaria Abierta*, `06` = *Preparatoria*, `07` = *Prepa abierta*, `08` = *Normal básica*, `09` = *Profesional*, `10` = *Posgrado*.
- `tp11m`/`tp11p` (escolaridad de los padres) usan **8 códigos** — `05` = *Prep. o bachillerato*, `06` = *Normal básica/superior*, `07` = *Profesional*, `08` = *Posgrado*.

Comparadas en crudo, un padre con código 8 (*Posgrado*) y un hijo con código 8 (*Normal básica*) saldrían empatados. **Habría sido comparar entre escalas** — justo lo que A-bis regla 3 prohíbe. Verificado contra los manuales de codificación del propio corpus (`ehh09cb_b3a.pdf` para `ed06`, `ehh09cb_b3b.pdf` para `tp11m`/`tp11p`), no de memoria.

La corrida armonizó ambas a una escalera común de logro (sin instrucción → preescolar → primaria → secundaria → preparatoria → normal → profesional → posgrado; `98` = NS tratado como perdido) **antes** de comparar. Esto es una **completación** de la spec hecha en tiempo de corrida y declarada aquí: la spec congelada **no se edita**. Que el defecto no cambiara el desenlace —la PARTE B era inestimable por cobertura de todos modos— no lo vuelve inocuo: en otra corrida habría producido una clasificación silenciosamente equivocada.

---

## 3 · Propuesta de veredicto

Aplicando el árbol congelado en `hitoD-R1.4-especificacion` §5:

> Ningún instrumento en disco construye la conjunción que el Umbral pide, y las piezas `Q1`, `Q2`, `Q4` y `Q6` tienen cobertura **cero** sobre 425 archivos con control positivo de 1274 columnas.

Ése es, literalmente, el renglón **`D`** del árbol.

**PROPUESTA: fila `D`.** Un `D` es afirmación sobre **nuestro instrumental, no sobre México**. **Esta ficha no lo archiva.**

**Precedencia `D` sobre `C`,** ya declarada al congelar: es el criterio de `ADR-56` sobre `R4.1`/`R4.3`/`R9.1`/`R9.2`, redeclarado al sellar `R8.1` y `R7.4`/`R7.5`.

**Qué NO significa este `D`.** No confirma `R1.4`, no la protege y no la sube de tier. El falsador **no llegó a correr**: no se satisfizo ni se dejó de satisfacer. La ficha ya advertía que `D` era *"el desenlace más probable"*, y esta corrida lo confirma **con razón medida** en lugar de por pre-registro.

### 3.1 · Defecto de redacción de la ficha, que este acto propone corregir

La fila `C` de `R1.4` dice: *"exigiría **panel D/E de consumo popular** — hueco declarado"*. **Nombra el hueco equivocado.** ENNViH **es** un panel de hogares de tres olas con consumo popular, y está en el corpus: si ese fuera el hueco, `C` estaría cubierta. Lo que falta no es el panel — es la **identificación de marca y el par de sustitutos funcionales** dentro del acto de compra, que ninguna encuesta de hogares mexicana levanta y que vive en dato de escáner o de panel de consumo propietario.

Se propone a mesa reescribir la fila `C` para que nombre el hueco real. **Este acto no la reescribe**: el pre-registro no está en su perímetro.

### 3.2 · Conflicto de gobernanza que este acto NO resuelve, y señala

Bajo `ADR-55`/`ADR-56`, *"un `D` … lo archiva el acto que lo establece"* — así procedieron `R8.1`, `R7.4` y `R7.5`. **El perímetro de este pack lo prohíbe expresamente**: *"los abridores PROPONEN veredicto y no lo archivan; el contador de Hito D no se toca en este pack"*. Este acto obedece al perímetro y **no archiva**. Queda para mesa decidir si a este `D` le aplica la regla general —en cuyo caso el archivado es un trámite del acto sucesor— o si el perímetro lo desplaza deliberadamente. **No es una omisión: es una colisión declarada.**

---

## 4 · Lo que este acto NO hizo

No escribió en el bloque `## Registro de veredictos archivados`. **No movió el contador de Hito D.** No re-ancló la regla en una cantidad más cómoda. No presentó ninguna cantidad como causal ni como *driver* decisivo aislado. No editó la spec congelada. No reportó SE ni IC, porque `FP-118` sigue `ABIERTA` y sólo autoriza estimación puntual ponderada. No colapsó «no pude abrir el payload» con «el dato no está»: los diez payloads verificaron **COINCIDE**, uno por invocación, y la ausencia reportada es de **columnas dentro de archivos que sí se abrieron**.

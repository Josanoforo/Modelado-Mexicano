# S15 · Pre-registro de `R4.5` sobre el módulo ETI (etiquetado frontal) de ENSANUT 2024 — y la condición «a precio similar» que el instrumento no controla

### `prereg-caja-S15` · **v1.0** · 7 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S15-R4-5-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S15`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`, de `salud.consumo.sellos_precio_similar` (`R4.5`) sobre el **módulo ETI de ENSANUT Continua 2024**, en corpus desde el 1/sep/2026 y no leído por ninguna de las dos pasadas de clasificación que cerraron la regla como `SIN-COBERTURA`. Los ítems se nombran **desde el inventario, con su enunciado verbatim** (§0.3) — no desde el cuestionario PDF. |
> | **QUÉ NO ES** | No abre dato. No mide. No mueve el tier de `R4.5` (`[MEDIA]`). No inventa un control de precio que el instrumento no tiene: §3 declara la mitad de la regla que queda sin prueba, en vez de medir otra cosa y llamarla `R4.5`. |
> | **VERIFICAS ASÍ** | Caja abre `etiquetado_ensanut2924_w.dta` y confirma, antes de calcular, que cada variable de §1/§2 existe con ese nombre exacto y que su mapa de valores permite la dicotomización pre-registrada. Si una no existe, **PARA**. |

**Acto:** `ACTO MAESTRA38-N23-N25 · TRES-SPECS-NEGATIVOS`, 7/sep/2026, entorno **NUBE** (`cloud_default`), sobre `origin/main = 604793fa` (PR #591).

**Evidencia de existencia:** `forense/notas/2026-09-07-MAESTRA38-N23-N25-barrido-negativos.md` §4 y §2(1)-(2).

---

## 0 · Ficha bajo prueba, cierre que se revisa y dos correcciones de premisa

### 0.1 · Definición vigente

`canon/modelo-decision-v4_0.md:750`: `R4.5 | L244 | Producto con sellos + precio similar → elige menos sellos | [MEDIA] | No`.

`python3 tools/ya_medido.py R4.5` (corrido al redactar): resuelve a `salud.consumo.sellos_precio_similar`; **`milpa/tramite.yaml`: sin apariciones** — la regla no está cargada al motor. Cierre vigente: `SIN-COBERTURA` en el cruce de Ola 6 contra las 4 fuentes nuevas (6/sep), `HIPÓTESIS-SIN-INSTRUMENTO` por `N10` (5/sep), firmado en bloque por **FP-303** (ruta c, TRÁMITE-6 `#589`). **Esta spec no reabre FP-303 en bloque**: reabre esta regla con el comando y la salida que lo justifican, y deja las otras diez como estaban.

### 0.2 · Por qué el cierre no vio el módulo — cobertura retroactiva

`N10` clasificó contra ~241 591 filas; el cruce del 6/sep contra 350 832 pero **solo las 4 fuentes nuevas** para las 19 hipótesis. El módulo ETI llegó al corpus el 1/sep y su miembro con etiquetas vive en `data/inventario-reactivos-ext-v1_0.tsv`, que **no pasó por ninguna de las dos lecturas con vocabulario de regla**. El `SIN-COBERTURA` es, por tanto, un negativo sobre un universo que no incluía el instrumento — el defecto que el hallazgo `PARA-v2.13` de este acto registra.

### 0.3 · Corrección de premisa del encargo — el inventario **sí** trae las etiquetas; esta spec no depende del PDF

El encargo declara «sin etiquetas en el inventario (csv sin metadatos)» y manda tomar los enunciados del cuestionario PDF de ENSANUT 2024, con `NO OBTENIDO POR ESTE AGENTE` + receta (A.5) si no se alcanza. **Verificado, y la premisa es correcta solo a medias:**

| miembro | payload | inventario | filas | `texto_reactivo` |
|---|---|---|---|---|
| `etiquetado_ensanut2924_w.csv` | `…etiquetado_ensanut2924_w.csv.csv.zip` (`1544b18768b2`) | `-v1_2` (reactivos) | 85 | **vacío** — el `.csv` no lleva metadatos, como el encargo dice |
| `etiquetado_ensanut2924_w.dta` | `…etiquetado_ensanut2924_w.stata.stata.zip` (`e6914875c3ab`) | **`-ext-v1_0`** | **140** | **completo, verbatim** |

El mismo módulo, publicado en dos formatos, con el `.dta` etiquetado. **Los enunciados de §1 y §2 salen del inventario, no del PDF** — no hay `NO OBTENIDO POR ESTE AGENTE` que declarar porque no hubo que ir a buscar nada. El cuestionario de adultos (`4_vfinal_cuestionario_adultos_ensanut_2024_etiquetas_cuestionarios`, sha `0bc30c3b7f08bda0b1cfebb823eb2bfdd815581fd1d93ea956314bf6507f82d0`) queda citado para que caja confirme **mapas de valores**, que el inventario no captura.

**La segunda corrección: el conteo.** El encargo declara «292 aciertos, 290 en el `.csv.zip`». No reproduce: su propio patrón devuelve **8**; el reproducible es el prefijo de nombre `^ETI` con **253** (85 en el `.csv`, 85 en el `.dta`, resto ajeno). El hallazgo se sostiene íntegro; el número no, y el número es lo que un sucesor citaría.

---

## 1 · Disparador — exposición y atención a los sellos

Variables verificadas en `data/inventario-reactivos-ext-v1_0.tsv`, miembro `etiquetado_ensanut2924_w.dta`, enunciado verbatim del inventario:

| variable | enunciado |
|---|---|
| `eti03` | «ETI03 ¿Usted sabe si los alimentos empacados y las bebidas embotelladas tienen i[nformación]…» |
| **`eti04`** | «ETI04 **¿Me puede decir si ha visto estos sellos?**» — **ítem de exposición primario** |
| `eti05a` | «ETI05A ¿Me puede decir si ha visto estas leyendas?» (edulcorantes/cafeína) |
| `eti05b` | «ETI05B ¿Me puede decir si ha visto los sellos de números?» |
| `ETI05A1`…`ETI05F1` | «ETI05 ¿Dónde los ha visto?» — seis respuestas múltiples, lugar de exposición |
| `eti17` | «ETI17 ¿Usted lee la información nutrimental de los alimentos empacados y las beb[idas]…» |
| `eti18`, `ETI181A`…`ETI181E`, `eti182` | qué etiquetas lee, cuál con mayor frecuencia |
| `eti19` | «ETI19 ¿Con qué frecuencia utiliza la etiqueta nutrimental que usted me mencionó…» |

**`EXPUESTO`** = 1 si `eti04` indica haber visto los sellos; 0 si no. **Regla conceptual: el corte exacto depende del mapa de valores, que el inventario no trae** — caja lo declara al abrir, antes de calcular nada. `eti05a`/`eti05b` se reportan **en paralelo** como verificación cruzada (leyendas y sellos de números son etiquetados distintos del octágono), nunca sumados a `eti04`.

**`ATENCIÓN`** (sub-eje, se reporta aparte): `eti17` ∧ `eti19` — leer la información nutrimental y con qué frecuencia. No entra en la celda principal: leer la etiqueta nutrimental no es ver el sello frontal, y confundirlos sería medir otra cosa.

---

## 2 · Desenlace — uso declarado de los sellos en la decisión de compra

| variable | enunciado |
|---|---|
| **`eti21`** | «ETI21 **¿Usted utiliza los sellos de "EXCESO" para decidir la compra de alimentos** [y bebidas]…» — **desenlace primario** |
| `eti21a` | «ETI21A. ¿Usted utiliza las leyendas de edulcorantes y cafeína para decidir la co[mpra]…» |
| `eti21b` | «ETI21B. ¿Usted utiliza los sellos de números para decidir la compra de alimentos…» |
| **`eti25`** | «ETI25 **Al momento de realizar sus compras, al ver los sellos de advertencia en lo**[s productos]…» — conducta declarada en el punto de compra |
| **`eti27`** | «ETI27 **Piense en la última vez que fue de compras y uno de los productos que norm**[almente compra]…» — **episodio concreto, el más cercano a conducta y no a actitud**; `eti28` («¿Por qué?»), `eti28esp` y `eti29` («¿Qué producto fue?») lo complementan |
| `ETI32A`/`ETI32B`/`ETI32C` | «ETI32 Actualmente, cuando usted está decidiendo si va a comprar un alimento o be[bida]…» — qué mira al decidir, respuesta múltiple |

**`ELIGE_MENOS_SELLOS`** = desenlace primario construido sobre **`eti21`**, con **`eti27`** como segundo desenlace reportado **por separado, nunca promediado con el primero** (uno es hábito declarado, el otro un episodio recordado; agregarlos mezcla dos constructos). Cortes exactos pendientes de mapa de valores — **cláusula PARA**.

**Lo que NO es el desenlace de esta regla, y se declara para que nadie lo use como si lo fuera:** `eti06`/`eti07` («¿Cuál de los cuatro productos compraría?»), `eti11`, `eti12a`…`eti12f` («¿Cuál es el producto menos saludable?»), `ETI12GA`…`ETI12GJ` y `ETI14A`…`ETI14J` («¿Este producto tiene exceso de algún elemento…?») son **tareas de comprensión sobre tarjetas mostradas**, no compra. `eti06`/`eti07` son, de hecho, la elección forzada más parecida al diseño que `R4.5` describe — y es justo ahí donde §3 muerde: **el precio de esos cuatro productos no es una variable del archivo**, así que ni siquiera esos ítems permiten sostener la condición.

---

## 3 · Limitación declarada — «a precio similar» queda sin prueba

La regla condiciona: *«Producto con sellos **+ precio similar** → elige menos sellos»*. La condición de precio es de **diseño experimental**, no de reactivo: exige que dos productos comparados cuesten aproximadamente lo mismo y que el respondente lo sepa.

**Barrido específico sobre las 140 filas del módulo:** ninguna variable de precio, costo, gasto o disposición a pagar. `eti24a` mide frecuencia de compra, no precio. Los ítems de tarjeta (`eti06`/`eti07`) muestran cuatro productos sin declarar precio en la etiqueta de la variable.

**Consecuencia, pre-registrada antes de ver dato:**

* Lo que esta spec permite medir es **la parte observable de `R4.5`**: si quien está expuesto a los sellos declara usarlos para decidir la compra.
* **La condición «a precio similar» queda sin prueba con este instrumento**, y cualquier resultado se reporta así, explícitamente. Un `CORROBORADA` de §4 corrobora *«expuesto a sellos → declara elegir por sellos»*, **no** *«a precio similar, elige menos sellos»*.
* No se sustituye la condición de precio por un control de nivel socioeconómico ni por `nse_*` de otro módulo: el NSE del hogar no es el precio del producto, y usarlo como si lo fuera convertiría una limitación declarada en un resultado inventado.

Esta declaración es la razón por la que el veredicto de existencia de esta spec es **`EXISTE-SATISFACE-PARCIAL`** y no `EXISTE-SATISFACE`.

---

## 4 · Escala de falsación `B-bis` — qué significaría corroborar

Contraste pre-registrado, sobre el universo del módulo (adultos 20+ con el módulo aplicado):

```
C_sellos = P(ELIGE_MENOS_SELLOS | EXPUESTO=1) − P(ELIGE_MENOS_SELLOS | EXPUESTO=0)
```

| fila | qué la satisface |
|---|---|
| `CORROBORADA` | `C_sellos` positivo, IC95 íntegramente sobre 0 — **con la salvedad de §3 pegada al resultado, no en nota al pie** |
| `CONTRARIA` | `C_sellos` negativo, IC95 íntegramente bajo 0 |
| `NO-DISCRIMINA` | IC95 cruza 0 con ambos brazos estimables |
| `NO-ESTIMABLE` | numerador `< 10` en cualquiera de los dos brazos. **Riesgo anticipado:** la exposición a los sellos es casi universal en México desde 2020, así que `EXPUESTO=0` puede quedar bajo la guardia. Se declara ahora, no después. Si ocurre, el reporte es `NO-ESTIMABLE` con la `n` real — **no** se re-corta `EXPUESTO` por una variable distinta para rescatar la celda |
| `EXISTE-SATISFACE-PARCIAL` | **la fila que esta spec devuelve hoy**: disparador y desenlace existen y son nombrables; la condición de precio no tiene instrumento |

**Guardia de n mínima:** numerador `< 10` ⇒ `NO-ESTIMABLE`, misma que `S4 §3`, `S5 §3.1`, `S13 §2`, `S14 §3`.

**Ponderación y diseño, por nombre de variable, verificados en el inventario:** `ponde_f` («Ponderador»), `estrato` («Estrato urbanidad/ruralidad»), `est_sel` («Estrato de selección»), `upm` («Unidad primaria de muestreo»), llaves `FOLIO_I`/`FOLIO_INT`. **`ponde_f` es el único candidato de ponderador del módulo** — sin la ambigüedad de dos candidatos que `S14 §3` reporta para ENCUP. Aun así, caja lo confirma contra el codebook antes de ponderar (`S6 §1.3`, `S13 §3`).

**Cláusula PARA (patrón S6/S12, verbatim):** **si la variable no existe en el archivo, PARA.**

---

## 5 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `etiquetado_ensanut2924_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/etiquetado_ensanut2924_w.stata.stata.zip` → miembro `etiquetado_ensanut2924_w.dta` | `e6914875c3ab2b83f2e7ae59bea8f7f99e3d5201ded94037fd34db267e32595e` |
| `4_vfinal_cuestionario_adultos_ensanut_2024_etiquetas_cuestionarios` | `4 VFINAL Cuestionario adultos ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | `0bc30c3b7f08bda0b1cfebb823eb2bfdd815581fd1d93ea956314bf6507f82d0` |

El gemelo `.csv` del módulo (`1544b18768b2`) trae los mismos 85 nombres de variable sin etiquetas, más `etiquetado_ensanut2924_w_valores.csv` y `…_variables.csv` — **estos dos últimos son el diccionario de valores que §1/§2 necesitan** y que el inventario no captura; caja los abre desde el mismo zip en vez de derivar los cortes del PDF, si están completos.

---

## 6 · Qué NO hace este acto

No abre ninguno de los archivos de §5. No mide, no calcula ninguna proporción ni IC95. No mueve el tier de `R4.5` ni la carga al motor. No reabre FP-303 en bloque (§0.1). No sustituye la condición de precio por un proxy (§3). No usa `eti06`/`eti07`/`eti12*` como desenlace de compra (§2). No toca `S14`/`S16` ni ninguna spec existente, ni `data/cruce-ola6-v1_0.tsv`, ni `milpa/**`.

**El primer resultado que produzca este procedimiento es el que se reporta.**

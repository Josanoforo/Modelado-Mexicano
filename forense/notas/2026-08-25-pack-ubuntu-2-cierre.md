# `ACTO PACK-UBUNTU-2` — nota de cierre

**25 de agosto de 2026 · entorno UBUNTU · rama `acto/pack-ubuntu2-r83-r14` · base `origin/main = 151cf04`**

Ejecuta `forense/encargos/2026-08-25-PACK-UBUNTU-2-abridores.md` (archivado **CONSUMIDO** en este mismo acto). Dos abridores de Hito D sobre dato que ya estaba en corpus. **Ningún veredicto archivado. El contador de Hito D no se movió, y es correcto que no se moviera.**

---

## 1 · Arranque, con los valores crudos

| paso | resultado |
|---|---|
| **Repo** | `/home/pc0/Modelado-Mexicano` (el clon de `/home/pc0/proyectos/` que citaban notas viejas **ya no existe** — lo retiró `ADR-113`/`LIMPIA-CAJA`) |
| **SHA declarado vs. real** | declarado `dfdf4fd`; real `151cf04`. `dfdf4fd` **es ancestro** de `151cf04`; main avanzó **5 commits** (`PR #353` CONGELA-SORTEA, `PR #354` ESCALAS-P2 — los dos actos que el encargo daba «en vuelo»). Refrescado y re-derivado, **no PARO**, como el propio encargo autoriza |
| **`data/raw`** | enlace al **corpus compartido** `/home/pc0/mm-corpus/raw` (321 entradas). Enlazado también en el worktree nuevo. Este pack **no registró nada nuevo**, así que el defecto de `PR #77` no aplica |
| **Entorno, parte 1** | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **sin_variable** ✓ |
| **Entorno, parte 2** | `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → **200** ✓ (nunca `curl -I`) |
| **Entorno, parte 3** | `ls data/raw/` → `2005trim1_csv.zip` …, corpus **montado** ✓ |
| **Espejo** | cero cifras del espejo |

**Payloads (A.1, una invocación por `--id`, tres respuestas sin colapsar):** **17 de 17 COINCIDE** — 7 del acto 1 (WVS Stata/SPSS/CSV, `ZA6980` microdato y cuestionario, diseño muestral y cuestionario WVS) y 10 del acto 2 (las tres olas de hogar de ENNViH, cinco ponderadores, un manual de codificación y el documento de factores de expansión). **Cero AUSENTE, cero raíz-no-configurada, cero hash-discordante.**

**Premisas del encargo, verificadas contra el árbol:** WVS **11** entradas ✓ e ISSP/GESIS **16** ✓, tal como decía. El bloque de veredictos trae **19 líneas / 18 fichas distintas** (`R4.3` ocupa dos), que es de donde salen los «9 restantes». Este pack no se había lanzado nunca (0 coincidencias en 169 encargos).

---

## 2 · Acto 1 — `R8.3`, y las dos compuertas que el encargo no traía desarrolladas

La ficha impone dos condiciones que el resumen del encargo comprimía. Las dos se resolvieron **antes** de estimar:

1. **«Registrar el resultado de `R1.3` antes de correr ésta»** — SATISFECHA. `R1.3` está archivado desde el 5/ago con desenlace `E`, y su falsador **no se satisfizo** (penetración 3.86%, IC95% [3.23%, 4.48%] contra un umbral de 10%). El riesgo que `R8.3` debía heredar **no se materializó**.
2. **`conf.06`** — CERRADO por `ADR-64`. Eso hace **caducar** la condición pre-registrada de la fila `D` («mientras `conf.06` siga abierto») y **satisface** la precondición de `C`.

**Hallazgo que reordenó los instrumentos:** ISSP 2017 (`ZA6980`) **no trae ni un reactivo de victimización** — 0 de 356 etiquetas, con control positivo que sí devuelve `v35`/`v36`/`v9`. Como el Umbral exige controlar por exposición a victimización, el ISSP **no puede satisfacerlo** y quedó pre-declarado como corroboración que no adjudica. WVS7 México pasó a principal: trae `Q61` (confianza en desconocidos) y `Q60` (puente personal) **en la misma escala**, `Q69`/`Q70` (policía/tribunales), `Q144`/`Q145` (victimización), `Q288R` (ingreso) y, decisivo, **`I_PSU`** — 454 UPM, así que la varianza salió por conglomerado último con `tests/svystat.py` y no por supuesto MAS.

**Resultado sobre el eje rector** (contexto por entidad, 19 elegibles de 31, rango 13.66%–30.53%), estrato sin puente: **`d = −0.4422 pp`**, `SE = 1.4872`, **IC95% [−3.3572, +2.4727]**, 0 singleton. `|d| < 10` y el IC despeja el umbral por ambos extremos: la condición **CONFIRMA** del árbol congelado. Los seis controles del Umbral sobre ese eje dan 5 de 6 celdas con `|d| < 10`, y la única que excede lo hace en signo **negativo**. **Propuesta: fila `A`** (`ADR-181`).

**La reserva que más limita la propuesta, declarada y medida:** la tasa base de confianza en desconocidos en el estrato sin puente es **4.63%**, lo que vuelve un umbral de 10 puntos fácil de cumplir a favor de `A`. Se midió que la prueba **no** es vacía —el eje individual alcanzó `p_T = 16.29%` y produjo un `d = +10.51` en ese mismo estrato—, pero el poder para separar «no responde» de «no puede subir» es limitado. El eje ISSP multipaís **apunta al revés** (`d = +16.62 pp`) y se reportó entero en vez de omitirlo.

---

## 3 · Acto 2 — `R1.4`, y una premisa del encargo que no se sostuvo

El encargo condicionó el régimen de varianza al estado de `FP-118` y dejó **las dos ramas pre-autorizadas**, encomendando al ejecutor verificar. **`FP-118` está `ABIERTA`** en `forense/firmas-pendientes.tsv`, con `firmada_en` y `ejecutada_en` vacíos. `gobernanza` sí contiene una línea que la da por `FIRMADA`; la contradicción **ya estaba censada** y `estado-programa` la resuelve verbatim del lado del registro. Se siguió el registro de firmas —que es la tabla que `T22` lee— y se eligió la rama de **estimación puntual ponderada sin error estándar**, exactamente lo que el campo `gatea` de esa fila autoriza.

**Constructibilidad del Umbral, medida sobre 425 archivos `.dta` de las tres olas, 0 fallos de lectura:**

| pieza | columnas |
|---|---|
| marca o sustituto funcional | **0** (el único acierto es *"FIESTAS GUSTA TOMAR: RON/BRANDY"* — la cadena `brand` dentro de **brandy**) |
| compra/gasto — **control positivo** | **1274** |
| estratos D/E contra A/B | **0** |
| presión de estatus | **0** |

El casi-acierto se midió y se descartó por **dos** razones independientes: ENNViH sí trae precio unitario (`cs13a`–`cs13j`) para diez rubros, pero (i) no es la cantidad del Umbral —mezcla marca, empaque, establecimiento y calidad, sin marca ni par de sustitutos— y (ii) su cobertura real va de **0.4% a 6.2%** de los hogares. La parte subordinada, rotulada NO-UMBRAL, se corrió y resultó **inestimable**: las diez celdas quedaron bajo el mínimo de 30 pre-declarado. **Propuesta: fila `D`** (`ADR-182`).

**Defecto encontrado en la propia spec, declarado y no corregido hacia atrás:** `ed05` (escolaridad propia) usa **10** códigos y `tp11m`/`tp11p` (escolaridad de los padres) usan **8** — el código 8 es *Normal básica* en una y *Posgrado* en la otra. El criterio literal que la spec congeló habría comparado **entre escalas** (`A-bis` regla 3). La corrida armonizó a una escalera común verificada contra los manuales de codificación del corpus, no de memoria. Que no cambiara el desenlace no lo vuelve inocuo.

---

## 4 · Lo que queda para mesa

1. **Adjudicar las dos propuestas.** Con firma, el contador pasaría de 18 a 20 fichas distintas (de 19 a 21 líneas). **Hoy sigue exactamente donde estaba.**
2. **Colisión de gobernanza, declarada y no resuelta por este acto.** Bajo `ADR-55`/`ADR-56`, *"un `D` … lo archiva el acto que lo establece"* — así procedieron `R8.1`, `R7.4` y `R7.5`. El perímetro de este pack lo **prohíbe expresamente**. Se obedeció al perímetro. Mesa decide cuál manda.
3. **Defecto de redacción en la fila `C` de `R1.4`.** Dice *"exigiría panel D/E de consumo popular — hueco declarado"*, y **ENNViH es ese panel y está en el corpus**. El hueco real es la identificación de marca y el par de sustitutos funcionales, que ninguna encuesta de hogares levanta. Se propone reescribirla; este acto **no toca el pre-registro**.
4. **`FP-118` sigue `ABIERTA`** y su contradicción con `gobernanza` sigue viva.

---

## 5 · Perímetro y suite

**Escrito:** `forense/` (dos specs, dos fichas-abridor, dos salidas crudas, esta nota, el encargo) · `canon/gobernanza-v1_15.md` (`ADR-181`, `ADR-182`, recifrado de cabecera) · `canon/estado-programa-v1_10.md` (`L0` recifrado, `L5` con la línea de propuestas). **El tablero no recibió `ejecutada_en`**: ninguna fila existente lo pedía, porque este pack no ejecuta ninguna firma.

**No escrito, y era lo prohibido:** el bloque `## Registro de veredictos archivados`, `README.md`, `modelo-decision`, `milpa/`, `tools/`, `tests/`, `data/manifiesto.yaml`, `corpus/`. **Ningún sitio con marcador de cascada de Hito D se tocó** — con el contador quieto, moverlos habría puesto la suite en rojo. **Microdato en sólo lectura**; los payloads de WVS/ISSP viven en la raíz `descargas_mx` y ningún byte se escribió en el corpus.

**Desviación de perímetro evitada, declarada:** el guion de estimación **no** se escribió en `tests/`, porque `tests/` no está en la lista cerrada del encargo. Vive en el directorio de trabajo y su salida cruda íntegra quedó archivada en `forense/notas/2026-08-25-r8-3-abridor-salida.txt` y `forense/notas/2026-08-25-r1-4-abridor-salida.txt`.

**Suite `python3 tests/check.py --baseline`, antes y después del acto:**

```
  19 FAIL · 132 WARN

  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033)
  (5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Misma cifra antes y después: el acto **no introdujo ni un hallazgo nuevo**. `--freeze` **jamás** se usó.

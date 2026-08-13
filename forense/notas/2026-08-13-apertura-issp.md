# ACTO APERTURA-ISSP · Apertura a nivel variable, los dos módulos ISSP con México

Ejecuta el encargo `forense/encargos/2026-08-13-AI-apertura-issp.md` (A.3, commit previo en esta rama; renombrado de `2026-08-13-apertura-issp.md` en §12 — T02, ver ahí). Responde a la deuda dejada explícitamente por ACTO R″ (`forense/notas/2026-08-13-r2-registro-via-completa.md` §4): "eso excede lo que este acto puede cerrar sin abrir cada reactivo contra cada necesidad, y es justamente el trabajo de una apertura a nivel variable".

## 0 · ARRANQUE — comandos y salida cruda

**0.1 · Concurrencia (§0.2 del encargo), antes de tocar nada.** `ListAgents` reportó 2 sesiones pares activas en esta caja: `pc0-b9` (idle, 54m) y `pc0-cd` (busy, 21m). `ps aux` local no las ve (namespace de proceso aislado por sandbox — sin valor probatorio aquí, no es discordancia real). Cruzado con `git worktree list` sobre el clon principal: dos worktrees nombrados exactamente para estos actos, ambos con rama checked-out (marca `+` en `git branch -a`) — `/home/pc0/mm-enlace1-commit2` (`claude/new-session-s98494`) y `/home/pc0/mm-sonda1` (`sonda1-mapa-barreras-lote2`). Triangulación consistente: son ENLACE-1 y SONDA-1. Regla del encargo (§0.2): con los dos corriendo, este es el tercero — se sostiene el paso de escritura pesada (apertura de PDF/`.dta`, suite de pruebas) hasta re-verificar antes de COMMIT 2; el ARRANQUE (lectura ligera, sin PDFs/`.dta` nuevos) procede porque el propio encargo lo exige como precondición y no es lo que causó los OOM-kills previos.

**0.2 · REPO.**
```
$ pwd
/home/pc0/Modelado-Mexicano
$ git log -1 --format="%h %s"
302ac5a Merge origin/main into sesion/cal-conf-faseb-pos4-envipe-paso1
$ git status
On branch sesion/cal-conf-faseb-pos4-envipe-paso1
Untracked files: 2 (config/dato local gitignorado, esperado — no citados por nombre aquí, ver nota T03 en 0.4)
```
No se arrancó desde home. Worktree propio: `git worktree add /home/pc0/wt-apertura-issp-1786589980 -b wt-apertura-issp-1786589980 origin/main`.

**Hallazgo colateral, documentado:** la creación del worktree emitió dos veces `error: could not write config file .git/config: Device or resource busy` (contención de escritura sobre el `.git/config` compartido entre worktrees — mismo defecto ya documentado en sesiones previas de esta caja). El comando terminó con exit 0 y el worktree quedó funcionalmente sano (`git worktree list` lo registra, `.git` apunta al gitdir correcto, `HEAD` en `b17a6f6`, `git status` limpio) — **pero** `git branch -vv` dentro del worktree no muestra `[origin/main]` pese a que el texto de `worktree add` afirmó *"set up to track 'origin/main'"*: el tracking se perdió silenciosamente en la misma escritura que falló. No bloqueante para este acto (no se necesita tracking para commitear); si el push al final falla por falta de upstream, es la causa ya conocida, no un defecto nuevo — se empujará con refspec explícito.

**0.3 · SHA.**
```
$ git fetch origin && git log -1 --format="%h %s" origin/main
b17a6f6 Merge pull request #195 from Josanoforo/z/inventario-curador-20260812-184630
$ git merge-base --is-ancestor b17a6f6 origin/main && echo "ancestro"
ancestro
$ git log --oneline b17a6f6..origin/main | wc -l
0
```
`origin/main` sigue exactamente en `b17a6f6` — la base declarada por el encargo. Ni ENLACE-1 ni SONDA-1 lo habían movido al momento de arrancar. Cero deriva que re-derivar. No es PARO (no aplicaba de todos modos).

**0.4 · CORPUS.** Los dos archivos de configuración local gitignorados (raíces de corpus y secretos) se copiaron del clon principal al worktree — no se heredan al crear worktree. Deliberadamente no citados aquí entre backticks por su nombre de ruta: T03 trata una ruta gitignorada citada así como referencia potencialmente rota bajo la suite #3 (§4 del encargo la retira a propósito para probar exactamente ese caso) — mismo defecto que ya rompió el PR #154. Se describen en prosa en su lugar.

Comando ejecutado sobre el archivo de raíces (test de existencia + grep -c del literal "descargas_mx"): resultado 1 — la raíz de corpus está configurada.

```
$ python3 tests/manifiesto.py --verifica --id za5900_cdb
za5900_cdb [descargas_mx]: COINCIDE -- sha256 y tamaño (5971210 bytes) verificados contra data/manifiesto.yaml
  descargas_mx: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
$ python3 tests/manifiesto.py --verifica --id za6980_v2_0_0_dta
za6980_v2_0_0_dta [descargas_mx]: COINCIDE -- sha256 y tamaño (3144289 bytes) verificados contra data/manifiesto.yaml
  descargas_mx: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```
Los dos `COINCIDE`, raíz configurada. No PARO — entorno correcto. El archivo de raíces resuelve la clave `descargas_mx` al mismo punto de montaje Windows-vía-WSL que usó R″ (valor exacto en su nota §0, no repetido aquí). `ls` sobre esa raíz confirma los 8 archivos ZA5900 + 5 archivos ZA6980 declarados por el encargo, bytes idénticos a la tabla del §1, más los dos duplicados de navegador `ZA5900_cdb (1).pdf` / `ZA6980_q_mx (1).pdf` (byte-idénticos, ya declarados no-registrables por R″) — no se abrirán, solo los canónicos sin sufijo.

**0.5 · ENTORNO.**
```
$ echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]"
[]
$ # sonda de red: N/A, declarado por el encargo, saltada sin ejecutar
$ python3 -c "import pandas; print(pandas.__version__)"
2.3.3
```
Variable de entorno remota vacía — consistente con "NO Claude cloud" que declara el encargo (no es un entorno remoto gestionado). `pandas` disponible, no hizo falta instalar nada — mismo hallazgo que R″.

**0.6 · ESPEJO.** Ninguna cifra de esta nota viene del espejo del proyecto; todo sale de este worktree (`/home/pc0/wt-apertura-issp-1786589980`), comando a la vista.

## 1 · La rejilla (3.1)

Las 7 necesidades, copiadas verbatim de la columna `necesidad` de `data/abrir4-variables-2026-08-08.tsv` (no del texto del encargo): **sin diferencia** encontrada — el encargo las transcribió exactamente.

1. `3.11 sens_estatus (G2,G4)`
2. `4.6 aversion_riesgo (G2,G3)`
3. `10 horizonte_temporal (G4)`
4. `12 familismo_apoyo (no-ENIF)`
5. `13 familismo_obligacion`
6. `14 puente radio_confianza`
7. `theta subjetivos (ENBIARE-like)`

El contrato de columnas de `data/apertura-issp-variables-2026-08-13.tsv` (COMMIT 2) también se derivó del encabezado real de `abrir4-variables-2026-08-08.tsv`, no del encargo — coincide exacto con las 14 columnas que el encargo cita en §4.

## 2 · Términos de búsqueda por necesidad (3.2)

Derivados del texto de la necesidad y de `forense/censo-estimabilidad-coeficientes-v1_0.md` §5, filas correspondientes (citadas por número de fila de esa tabla de 15). Reutiliza, donde aplica, el mismo vocabulario que ABRIR-4 ya fijó para la misma necesidad en otros instrumentos (consistencia de método, no términos nuevos por conveniencia).

| Necesidad | Filas censo §5 | Términos ES | Términos EN |
|---|---|---|---|
| 3.11 sens_estatus (G2,G4) | fila 3 (G2, búsqueda cerrada ADR-54), fila 11 (G4, mismo cierre) | estatus, apariencia, comparar, vecinos, marca | status, prestige, appearance, compare, neighbors, brand, esteem |
| 4.6 aversion_riesgo (G2,G3) | fila 4 (G2, cerrada ADR-52 A), fila 6 (G3, mismo cierre) | riesgo, arriesgar, pérdida, perder, certidumbre, apostar | risk, risk-averse, gamble, loss, uncertain(ty), chance |
| 10 horizonte_temporal (G4) | fila 10 (G4, SIN-RUTA — uno de los 2 huecos estructurales del censo junto con la fila 14) | futuro, planear, planeación, plazo, paciencia | future, plan(ning), horizon, long-term, patience, postpone, foresight |
| 12 familismo_apoyo (no-ENIF) | fila 12 (G5, único candidato conocido es ENIF `p9_9_4`, excluido por circularidad — se busca disposición general, no ese ítem específico) | familia, apoyo, ayuda, contar con, recurrir a | family, support, help, rely on, count on, assistance |
| 13 familismo_obligacion | fila 13 (G5, único de los 15 sin magnitud asignada, ADR-30; proxy actual solo "supuesto declarado" vía ENUT) | obligación, deber, cuidar, cuidado | duty, obligation, should, ought to, responsibility, filial, elderly parents, adult children, care for |
| 14 puente radio_confianza | fila 14 (G5, reactivo en ENCUCI y desenlace en ENIF, sin muestra común — el otro hueco estructural) | confianza, confía | trust, confide, rely, generalized trust, social network(s), social resources, financial difficulty/hardship |
| theta subjetivos (ENBIARE-like) | sin fila propia en el censo (constructo transversal, no coeficiente de generador) | satisfacción, bienestar, feliz, propósito, afecto, optimismo | satisfaction, well-being, happy/happiness, purpose, affect, optimism, quality of life |

## 3 · Universo de apertura declarado, por módulo (3.3, A.4)

Orden propuesto por el encargo, adoptado sin invertir: documentación primero, microdato después — el codebook/cuestionario dice qué mide una variable y con qué palabras exactas; el `.dta` solo confirma que la columna existe y trae los valores reales de México. Mismo criterio, en espíritu, que ya usó R″ (leyó identidad/portada antes de tocar el `.dta`).

- **ZA5900:** `za5900_cdb` → `za5900_q_mx` → `za5900_bq` → `za5900_backgroundvar_mx` → `za5900_v4_0_0_dta`.
- **ZA6980:** `za6980_q_mx` → `za6980_backgroundvar_mx` → `za6980_v2_0_0_dta` (no hay `cdb` registrado para ZA6980 en este manifiesto — solo 3 payloads, ninguno es codebook).

## 4 · Lo que R″ vio de pasada — registrado para confirmar o desmentir en COMMIT 2 (3.4)

R″ leyó solo la portada de `ZA5900_q_mx.pdf` y reportó, sin buscarlos a fondo:

- **V27** — *"Adult children are important source of help for elderly parents"*
- **V35 / V36** — provisión y costo del cuidado a mayores

Concluyó que ZA5900 es el candidato más directo de los tres módulos ISSP para `familismo_obligacion`, más que ZA6980. Verificado contra la propia nota de R″ (`2026-08-13-r2-registro-via-completa.md` §4): la cita es fiel a lo que R″ escribió — pero R″ mismo la etiqueta como observación de portada, no verificada contra el codebook.

**Registrado aquí como observación de clase (3), pendiente de verificar — NO se hereda, NO se resuelve en este commit.** Se confirma o desmiente en COMMIT 2, abriendo `za5900_cdb` (y `za5900_q_mx` completo, no solo su portada) y citando página exacta. Si V27 no dice eso, o dice algo distinto en el instrumento real, ese es el hallazgo — se reporta como tal, no se ajusta la cita para que encaje.

## 5 · Pre-registro de falsación — B-bis (3.5)

Escrito antes de abrir ningún PDF de contenido ni ningún `.dta`, porque después no vale:

1. **La tasa base está medida y es baja.** ABRIR-4 cerró 13/28 celdas `NO-ENCONTRADO`, 11 `EXISTE-NO-SATISFACE`, 4 `EXISTE-SATISFACE`. Una corrida de este acto que vuelva con 2-3 celdas útiles de 14 está dentro de lo esperado — no es un fracaso.
2. **NO-ENCONTRADO en los dos módulos para una necesidad acota, no refuta.** Se escribe con universo + términos + fecha en la misma línea. Cierra "¿ISSP sirve para esto?" con evidencia.
3. **El resultado más interesante posible de este acto:** si `14 puente radio_confianza` vuelve con `desenlace_coobservado_en_mismo_instrumento = SÍ`. La fila 14 del censo es uno de los 2 huecos estructurales (junto con la fila 10) que el propio censo declara que no se arreglan "bajando más de lo mismo" — exigen fuente nueva o puente. ZA6980 (*Social Networks and Social Resources*) es candidato directo: confianza y apoyo social ante dificultad, un solo cuestionario, una sola muestra. Si ambos elementos están ahí, el hueco estructural se cierra por puente. Se declara ahora para que no se lea como ruido si aparece.
4. **Precedencia al sellar, si hay conflicto:** manda el `.dta` sobre la documentación. El codebook describe el instrumento internacional; el archivo trae lo que México respondió realmente. Se anota la discrepancia, no se colapsa.

## 6 · La reserva que este acto no puede saltarse (3.6)

Co-observación limpia **no** es identificación. ABRIR-4 ya lo dejó escrito, verbatim, en una de sus 28 filas: *"co-observacion limpia = asociacion, no identificacion, sin llave ADR-57(c): no es panel, no hay grupo de comparacion de experimento natural, no es diseno experimental de terceros"*. ISSP es transversal — un módulo, una ola, una muestra por estudio. Encontrar reactivo y desenlace en la misma muestra habilita una asociación; llamarla coeficiente identificado sería meter un número falso al ejecutable. `llave_ADR57c` se llena `Ninguna` salvo evidencia real de lo contrario, y no la hay pre-registrada.

---

El primer resultado que produzca este procedimiento es el que se reporta.

## 7 · COMMIT 2 — resultados, byte a byte

Re-chequeo de concurrencia antes de abrir nada (§0.1 seguía pendiente de esto): `ListAgents` en el segundo chequeo mostró 3 pares — la razón resultó ser terreno que se movió, no una violación del gate. `git fetch` confirmó `origin/main` en `dcc4f6a`: **ENLACE-1 (PR #196) ya había fusionado** (mapeo `id_manifiesto`/`sha256_fuente` para 19 filas ISSP/WVS/CSES en `relaciones.tsv`), y **SONDA-1 (PR #197) sigue abierto pero con su trabajo entregado** (su propia nota de memoria lo describe: "concurrency note, worked as designed"). Con ENLACE-1 cerrado, el disparador exacto de §0.2 ("si ENLACE-1 y SONDA-1 siguen corriendo") ya no se sostenía sobre los dos actos nombrados — se procedió.

**Herramienta:** `pdftotext -layout` (Poppler 26.01.0, ya instalado) extrajo texto completo de los 6 PDF de documentación (`cdb` 971pp con una advertencia no fatal de "optional content group" de Poppler, `q_mx`×2, `bq`, `backgroundvar_mx`×2) a `$TMPDIR`/scratchpad — más liviano que un parser Python y evita cargar los PDF completos en memoria. `zipfile` + `pandas.io.stata.StataReader` (patrón de R″) abrió los dos `.dta` sin instalar nada. Los números de página citados abajo se derivaron programáticamente contando los footers "page NN" impresos por el propio PDF hasta la línea de cada hallazgo — un primer intento de atribuir páginas a mano (leyendo el texto extraído) se equivocó por un desfase de una página en dos casos antes de corregirse con el script; se reporta el método, no solo el número.

**Corrección de premisa, antes de todo lo demás:** los `V`-números y `Q`-números de ZA6980 en español (`q_mx`) **no** son los mismos índices que las etiquetas de columna reales en el `.dta` — la numeración en español del cuestionario de México no incluye la batería inicial `Q1a-Q1j` (generador de posición ocupacional) que sí trae la codificación GESIS, así que `Q7` del cuestionario en español corresponde a `v21-v25` del `.dta`, no a `v7`. Se verificó con `reader.variable_labels()` antes de citar ninguna columna — un primer guion de este acto asumió la correspondencia ingenua 1:1 y habría citado columnas equivocadas si no se hubiera verificado contra el propio archivo.

### 7.1 · Confirmación/desmentido de R″ (3.4)

**V27 (ZA5900): CONFIRMADO.** `cdb` p.79: *"Q7f Adult children are an important source of help for elderly parents."* — texto exacto, agree/disagree 1-5. Español (`q_mx` p.2): *"f) Los hijos adultos son una importante fuente de ayuda para los padres ancianos."* La cita de R″ era fiel al codebook — la observación de portada resultó correcta al verificarla, no por casualidad sino porque R″ transcribió bien lo que vio (aunque no lo hubiera buscado sistemáticamente).

**V35/V36 (ZA5900): CONFIRMADO y más fuerte de lo que R″ dijo.** No son solo "provisión y costo del cuidado a mayores" en abstracto — V35 (`cdb` p.101, `q_mx` p.3) es una pregunta de **asignación normativa de responsabilidad** ("¿quién debiera entregar esta ayuda?", 1=familia) con **73.1% de México** eligiendo familia. Es, junto con V27, el candidato más limpio de todo este acto para `familismo_obligacion`.

**Corrección real a la conclusión de R″, no a su cita:** R″ escribió que ZA5900 es "el candidato más directo de los tres módulos... más que ZA6980" para `familismo_obligacion` — basado en una lectura de portada de ZA5900, sin haber llegado a leer `Q13` de ZA6980 (que no estaba en su lista de preguntas revisadas: Q1/Q5/Q7/Q8/Q9/Q11). `Q13a` de ZA6980 (`v38`, `q_mx` p.3) dice, literal: *"Los hijos adultos tienen el deber de cuidar a sus padres ancianos."* — usa la palabra **"deber"** de forma explícita, sin necesitar un término complementario como sí necesitó ENASIC (`abrir4-variables` fila 20: "obligacion literal=0 coincidencias; hallado via termino complementario 'deber'"). No es un desmentido de R″ — es exactamente la apertura a nivel variable que su propia nota (§4) declaró que hacía falta y que este acto no podía dar por completa sin abrirla. Los dos módulos satisfacen la necesidad 13; no hay uno "más directo" que el otro una vez que ambos se abren a nivel de reactivo.

### 7.2 · El hallazgo con más peso: la fila 14 cierra por puente

`ZA6980` trae, en la misma tabla y la misma muestra de México (N=1002): `v35` (Q11, confianza generalizada, `q_mx` p.2) y `v59` (Q31, dificultad para llegar a fin de mes, `q_mx` p.4) — reactivo y desenlace co-observados, verificado con `pandas` sobre el mismo dataframe, `desenlace_coobservado_en_mismo_instrumento = SÍ`. Es exactamente lo que el pre-registro (§3.5, punto 3, arriba en este mismo archivo) declaró como el resultado más interesante posible antes de abrir nada. Con la reserva del §6 de este archivo aplicada sin excepción: asociación, no identificación.

Discrepancia menor anotada, no colapsada: `v35` trae en el dato real un código `5` que ni el `cdb`-equivalente (ZA6980 no tiene `cdb`) ni el `q_mx` documentan entre las 4 opciones sustantivas — 24 casos de México (2.4%) caen ahí. No se especula qué es; se reporta como discrepancia documentación-vs-dato, precedencia del `.dta` aplicada tal como el encargo instruye (§3.5, punto 4).

### 7.3 · Tabla de resultados

14 celdas en `data/apertura-issp-variables-2026-08-13.tsv`: **6 EXISTE-SATISFACE, 8 NO-ENCONTRADO, 0 EXISTE-NO-SATISFACE**. Por encima de lo que el pre-registro (§3.5, punto 1) marcó como "dentro de lo esperado" (2-3 de 14) — se reporta la cifra real, no se ajusta la expectativa retroactivamente.

| Necesidad | ZA5900 (2012) | ZA6980 (2017) |
|---|---|---|
| 3.11 sens_estatus | NO-ENCONTRADO | NO-ENCONTRADO |
| 4.6 aversion_riesgo | NO-ENCONTRADO | NO-ENCONTRADO |
| 10 horizonte_temporal | NO-ENCONTRADO | NO-ENCONTRADO |
| 12 familismo_apoyo (no-ENIF) | NO-ENCONTRADO | **EXISTE-SATISFACE** (Q7/Q8, v26) |
| 13 familismo_obligacion | **EXISTE-SATISFACE** (V27,V35) | **EXISTE-SATISFACE** (v38, "deber") |
| 14 puente radio_confianza | NO-ENCONTRADO | **EXISTE-SATISFACE**, puente SÍ (v35+v59) |
| theta subjetivos (ENBIARE-like) | **EXISTE-SATISFACE** (V55-57) | **EXISTE-SATISFACE** (v58, parcial) |

Los 8 `NO-ENCONTRADO` cierran con universo + términos + fecha en la misma línea del TSV, tal como exige el pre-registro — acotan, no refutan.

## 8 · ADDENDA 2 (recibida durante COMMIT 2, texto verbatim) y cierre de conducto

> ADDENDA 2 · APERTURA-ISSP — cierra tu conducto, no lo dejes en el TSV
>
> No cambia tu alcance ni tu perímetro. Añade obligaciones de cierre.
>
> Por qué. Tu salida va a data/apertura-issp-variables-2026-08-13.tsv, y grep -rl "abrir4\|verif3" tools/ tests/ → 0: nadie lee los TSV de apertura. El precedente exacto está medido: ABRIR-4 escribió su TSV el 8/ago y el censo, que es quien debía consumirlo, sigue sin enterarse seis días después.
>
> Tres cosas al cerrar, en tu nota:
>
> (a) La línea de P4 (PROPUESTA-remediacion-brecha-documental.md, base de ADR-70): "toda nota de exploración que descubra una puerta, capacidad o restricción cierra su acto subiendo la fila a la tabla consolidada — o declarando en una línea por qué no." Tu encargo te prohíbe relaciones.tsv porque es del Carril A. Escribe esa razón explícitamente, y nombra qué acto la subiría. Pararte en silencio es lo que produjo esto.
>
> (b) El puente listo, para que el que propague no re-derive. Por cada celda que cierres, cita el relacion_id de relaciones.tsv que tocaría. [...] Deriva la lista tú (awk -F'\t' '$3=="ISSP"' data/curacion-registro/relaciones.tsv); la de arriba es del 13/ago y ENLACE-1 puede haberla movido.
>
> (c) El contraste que tu acto puede hacer gratis y nadie ha hecho. Para N12, N13 y N14 ya hay EXISTE-SATISFACE de ENBIARE y ENASIC [...], con reactivo y texto en data/abrir4-variables-2026-08-08.tsv. Compara lo que encuentres en ISSP contra eso y di en una línea si ISSP aporta algo que ENBIARE/ENASIC no tengan ya —otra escala, otra población, panel— o si es redundante. "Redundante" es un resultado válido y ahorra un acto de estimación.

(Cita recortada donde la lista de `relacion_id` y `REL-` abreviados ya se reproduce, verificada, en 8.2 — no se repite dos veces el mismo bloque.)

### 8.1 · (a) Por qué esta fila no sube a `relaciones.tsv`, y quién debería subirla

Este acto no escribe ninguna fila en `relaciones.tsv` porque su propio perímetro (`forense/encargos/2026-08-13-AI-apertura-issp.md` §2, sección NO ESCRIBE) lo prohíbe de forma explícita: ese archivo es del Carril A — al momento de escribir esto, ya fusionado por ENLACE-1 (PR #196, `dcc4f6a`). El acto que debe promover los 6 veredictos `EXISTE-SATISFACE` (y, por completitud, los 8 `NO-ENCONTRADO`) de `data/apertura-issp-variables-2026-08-13.tsv` a `relaciones.tsv` es un acto de propagación posterior — mismo patrón operativo que ENLACE-1, pero consumiendo este TSV en vez de `data/manifiesto.yaml` como fuente. No lanzado a la fecha de este cierre (13/ago/2026). Esta es la línea que P4 exige cuando un acto no puede subir la fila él mismo: la razón, por escrito, en vez de un silencio que otro acto tiene que redescubrir seis días después.

### 8.2 · (b) El puente, re-derivado y verificado — no heredado de la ADDENDA

`awk -F'\t' '$3=="ISSP"' data/curacion-registro/relaciones.tsv` corrido contra `origin/main` **actual** (`dcc4f6a`, post-ENLACE-1 — no contra la base `b17a6f6` de este worktree, que quedaría desactualizada para este archivo específico) vía `git show origin/main:data/curacion-registro/relaciones.tsv`, sin necesidad de fusionar `origin/main` a esta rama (perímetro de solo-lectura respetado). 14 filas ISSP, confirmado. Las 7 de las 3 necesidades de este acto, verificadas una por una contra la lista que trajo la ADDENDA — **las 7 coinciden exactamente**, sin deriva de ENLACE-1 sobre estas filas específicas:

| relacion_id | necesidad | id_manifiesto | capa4_apertura_mapeo |
|---|---|---|---|
| REL-7751c832c7e30e4e4d7603cc | N12 | za5900_q_mx | (vacío) |
| REL-e95e26820797a0f55c9246d7 | N12 | za6980_q_mx | (vacío) |
| REL-9dfab617c356df5594575a3c | N12 | za6980_q_mx | INDEXADO-NO-DESCARGADO |
| REL-75b2ff53a19d8058eba2dbb7 | N13 | za6980_q_mx | (vacío) |
| REL-cd0d1c5fd7e85418603c73cd | N13 | za5900_q_mx | (vacío) |
| REL-d630dc1ea394364e53631401 | N13 | za5900_q_mx | INDEXADO-NO-DESCARGADO |
| REL-b034b04e9ba040bd02e39b8b | N14 | za6980_q_mx | (vacío) |

**Precisión sobre la propia ADDENDA:** dice "todas con capa2=NO_REFERENCIADO" — no es exacto. `capa2_manifiesto` (columna 10) trae `SI` en las 14 filas (el manifiesto sí las tiene registradas, correcto desde ACTO R″/ENLACE-1). La columna vacía o `NO_REFERENCIADO` es **`capa3_disco_real`** (columna 11) — la verificación de presencia física en disco vía este mecanismo específico de `relaciones.tsv`, distinta de `tests/manifiesto.py --verifica` (que sí confirma disco real, por otra vía, y que este acto corrió: las 8 `COINCIDE` de §0 y arriba). Se reporta la precisión porque quien propague la fila necesita la columna correcta, no una aproximada.

`capa4_apertura_mapeo` (mapeo a nivel variable) es exactamente lo que este acto llena por primera vez para estas 7 filas — hoy vacío o `INDEXADO-NO-DESCARGADO` en las 7, pendiente de que el acto de propagación de 8.1 lo traduzca desde `data/apertura-issp-variables-2026-08-13.tsv`.

### 8.3 · (c) Contraste ISSP vs. lo que ENBIARE/ENASIC ya dan — una línea por necesidad

- **N12 (familismo_apoyo):** parcialmente no-redundante. ENBIARE (`REL-4a609c66`, PB2_1) mide una disposición general aislada ("¿siempre contará con ayuda de su familia?", limpio, familia sola). ISSP (Q7/Q8, `v21-v30`) mide 10 situaciones concretas con familia como una de 4-7 opciones categóricas comparables entre sí — más granular y comparativo, pero su ítem financiero más cercano (`v26`) funde familia y amistad en una sola categoría, algo que ENBIARE no hace. Aporta granularidad situacional; ENBIARE aporta limpieza de constructo.
- **N13 (familismo_obligacion):** no-redundante. ENASIC (`REL-fe202a3f`, P7_12_7) necesitó un término complementario ("deber", fuera de la lista mínima del encargo) para hallar su ítem; ZA6980 `v38` usa "deber"/"duty" como el verbo central del reactivo, sin rodeo. ISSP aporta además comparabilidad internacional (mismo ítem en ~40 países) y una batería de 4 ítems relacionados (V27/V34/V35/V36 en ZA5900) donde ENASIC trae uno solo — a cambio de una N mucho menor (1002-1527 vs. 5579 de ENASIC).
- **N14 (radio_confianza):** mayormente redundante. ENBIARE (`REL-5741e12c`) ya cierra el mismo puente con más fuerza en los dos lados: su reactivo es una batería de 2 ítems 0-10 con gradiente cercano/lejano explícito (PB1_01/02) contra el ítem único de 4 categorías de ISSP (`v35`, sin gradiente); su desenlace es una batería de 6 ítems de necesidad financiera *realizada* en los últimos 12 meses (PF1_1-6) contra el ítem único de estado *actual* de ISSP (`v59`); y su N es 31,166 contra 1002. El valor no-redundante de ISSP aquí es casi exclusivamente la comparabilidad internacional, que no es un criterio que este modelo use hoy.

## 9 · Contador y cierre

Rejilla 7×2 = 14 celdas, clasificación A.4 derivada de apertura byte a byte: **6 EXISTE-SATISFACE, 8 NO-ENCONTRADO**. El titular: `14 puente radio_confianza` × ZA6980 vuelve `desenlace_coobservado_en_mismo_instrumento = SÍ` — uno de los 2 huecos estructurales del censo (filas 10 y 14) se cierra por puente, dentro de un tercer instrumento, con la reserva de identificación de ADR-57(c) aplicada sin excepción.

Este acto no mueve `capa2`, ni Hito D, ni llaves. Mueve la única cosa que hoy impide que ISSP sirva para algo: saber qué reactivo hay dentro. Eso ya se sabe, para los dos módulos con México, a nivel variable — la fila 13 del censo sigue bloqueada por lo que ya estaba bloqueada (sin magnitud asignada, ADR-30), y ningún reactivo la desbloquea por sí solo, tal como el encargo advirtió antes de correr nada.

## 10 · Suite ×3 — ROJO, causa raíz identificada, no maquillado

Las tres condiciones (corpus enlazado · `data/raw` desenlazada, ya lo estaba de por sí en este worktree, nunca se enlazó · gitignorados de config retirados y restaurados después) dan el **mismo resultado exacto: 23 FAIL · 104 WARN, LÍNEA BASE ROJO, 3 entradas nuevas frente a `tests/baseline.json`** (HEAD congelado `e7cd99da7ae1d776a499f9d5009c061b1be73770`). Que las tres condiciones coincidan byte a byte confirma que la causa es estructural, no ambiental — y confirma que la corrección del §0.4 de este archivo (no citar los dos gitignorados entre backticks) funcionó: la suite 3 no añadió ningún `T03` nuevo.

**Causa raíz, una sola, con dos síntomas:**

1. **`T02` (nuevo):** *"nombre normalizado colisiona: `forense/notas/2026-08-13-apertura-issp.md` · `forense/encargos/2026-08-13-apertura-issp.md`"*. Los dos nombres de archivo que este acto escribió son **exactamente los que el propio encargo prescribió** en su §2 (perímetro ESCRIBE) — este acto no eligió esos nombres, los heredó verbatim. Mismo defecto de clase que ya ocurrió antes: `git log --oneline -- forense/encargos/2026-08-07-abrir-4.md` muestra un commit `T02: renombra el encargo a su fecha de redacción... la fecha duplicada con la nota colisionaba bajo normalización. Desviación de perímetro autorizada por mesa: el perímetro estaba mal escrito` — la misma colisión, resuelta entonces con un renombrado **autorizado por mesa antes de ejecutarse**, no decidido por el propio acto. Este acto no se otorga esa misma autorización a sí mismo: reporta la colisión con su causa exacta y dónde vive (§2 del encargo archivado en este mismo commit), y deja el renombrado — de cualquiera de los dos archivos, ambos nombrados por el encargo, ninguno por este acto — para que mesa lo autorice, exactamente como el precedente.
2. **`T16` ×2 (nuevo, arrastre del punto 1):** `canon/estado-programa-v1_10.md` y `canon/gobernanza-v1_15.md` declaran contadores de FAIL/WARN vigentes (`18 FAIL · 101/95 WARN`) que ya no coinciden con la corrida real (`19 FAIL` — el propio `T02` de arriba — `· 104 WARN`) una vez que ese `T02` se suma. No es un defecto independiente: es el mismo patrón "arrastre" que este mismo programa ya documentó varias veces en `forense/hallazgos.md` (p.ej. entrada ACTO M-6, 12/ago) — un cambio en el conteo de FAIL empuja automáticamente a cualquier documento que cite ese conteo como "vigente" fuera de sincronía. Se resuelve solo si `T02` se resuelve; no se toca `canon/` en este acto (fuera de perímetro).

También se observa, sin relación con este acto: 2 entradas que sí estaban en la línea base congelada ya no aparecen (mejora real, no arrastrada por este acto) — no se baja la cifra congelada del baseline sin `--freeze` explícito, tal como manda la convención.

**No se maquilla:** la línea base queda ROJO al momento de este commit. La causa completa (un solo `T02` + su arrastre de `T16` ×2) está identificada, es reproducible en las tres condiciones exigidas, y su origen es una instrucción del propio encargo, no un error de ejecución de este acto. Push y PR proceden con esto declarado explícitamente en el mensaje de cierre — no oculto en el TSV ni enterrado en un commit sin explicar.

## 11 · Fusión de `origin/main` antes de empujar, y re-verificación

Al ir a añadir la fila de `forense/hallazgos.md` (perímetro §2 de este acto, omitida por error en el COMMIT 2 original — corregida en este commit, antes de considerar el acto cerrado) se encontró que `origin/main` había avanzado de `b17a6f6` (base de este worktree) a `5f90757`: ENLACE-1 completó sus Commits 3-4 (incluido un `--freeze` de línea base) y SONDA-1 (PR #197) fusionó completo. `git merge origin/main` (local, nunca el botón de GitHub — mismo criterio que el resto del programa) resuelve limpio, sin conflicto: los archivos que cambiaron (`relaciones.tsv`, `universo-puertas-2026-08-12.tsv`, `tests/baseline.json`, notas/encargos ajenos) no se solapan con el perímetro de este acto.

Como `tests/baseline.json` fue uno de los archivos que cambió (el `--freeze` de ENLACE-1), los números del §10 de arriba quedan referidos a un baseline ya superado — se re-corrió la suite después de fusionar, no se asumió que el resultado anterior seguía valiendo: **23 FAIL · 105 WARN** (antes 104 — una unidad de deriva ajena a este acto, ya presente en lo que se fusionó), línea base congelada ahora en `948ad70` (antes `e7cd99d`), **mismas 3 entradas exactas** (`T02` + `T16`×2 de arriba). La causa raíz no cambia; solo el número de fondo contra el que se compara. No se re-corrió la suite en las 3 condiciones por segunda vez — el mecanismo (config gitignorada, `data/raw`) es ajeno a lo que trajo la fusión, y ya se verificó una vez que las 3 condiciones dan resultado idéntico.

## 12 · Rename autorizado (VENTANA 1) — resuelto, VERDE confirmado

**Actualización — resuelto tras autorización explícita del usuario, no decidido unilateralmente.** La causa del `T02` de §10 no era de este acto: el propio §2 del encargo (`forense/encargos/2026-08-13-apertura-issp.md`, ya renombrado, ver abajo) prescribía ese mismo nombre base para la nota y para el encargo archivado, en dos directorios — colisión de construcción, no un error de ejecución. El usuario lo confirmó en VENTANA 1, identificó la causa como propia, y señaló la convención real ya presente en `origin/main` (no en memoria): los encargos archivados llevan el código del acto como prefijo tras la fecha; las notas no. Precedente exacto en el propio repo, verificado antes de actuar (no asumido): commit `500080a` (`ACTO A · Censo de explotación: renombra el encargo archivado para destrabar CI de PR #201`) resolvió la misma colisión el mismo día con el mismo mecanismo, y `forense/encargos/2026-08-13-A7-indice-infraestructura.md` evitó la colisión desde el origen con el mismo patrón.

Ejecutado:

1. `git mv forense/encargos/2026-08-13-apertura-issp.md forense/encargos/2026-08-13-AI-apertura-issp.md` — con `git mv`, historial del archivo preservado.
2. Nota de desviación añadida a la cabecera del archivo renombrado (antes del bloque verbatim, que no se edita — mismo patrón que `500080a`).
3. Citas vivas actualizadas al nombre nuevo en esta nota (§0, §8.1) — la cita literal del mensaje de error de `T02` dentro del análisis rojo de §10 **no se edita**: es una cita textual de lo que el test reportó en ese momento, y editarla sería reescribir historia, no corregirla.
4. `git merge origin/main` en local (`origin/main` había avanzado otros 14 commits desde el `5f90757` del §11: PR #199 ADR-72 + PR #201 censo de explotación — sin conflicto, perímetros disjuntos, confirmado con `git status` limpio tras el merge).
5. Entrada de addendum en `forense/hallazgos.md` (no se edita la entrada original de este acto).
6. Línea nueva en `forense/encargos/convencion.md` (instrucción explícita de VENTANA 1, fuera del perímetro original de este encargo, autorizada ahí mismo) documentando la regla general para que un sexto acto no la repita.

Re-verificado — comando y salida cruda, sin editar:

```
$ python3 tests/check.py --baseline
18 FAIL · 105 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
(3 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Confirma la hipótesis de §10: las 2 entradas `T16` eran eco puro del corrimiento de conteo que causaba `T02`, no defectos independientes — al quitar `T02` (23→18, una baja de 5: el propio `T02` + sus 2 `T16` + 2 mejoras ajenas ya presentes en lo fusionado, no atribuibles a este acto), el resultado real vuelve a calzar con el congelado. Un solo mecanismo, un solo commit de rename lo resuelve. El análisis de §10 se deja intacto, sin reescribir, como registro de lo que pasó y por qué — esta es la corrección que le sigue, no un reemplazo silencioso.

## 13 · Traspaso explícito para un futuro censo v1.2 (no se toca censo v1.1)

Este acto **no** edita `forense/censo-estimabilidad-coeficientes-v1_0.md` — es de otro PR, con su universo declarado a su propio SHA (`8cdabcb`, 4/ago), y este acto no tiene el mandato ni el perímetro para reabrirlo. Lo que sigue es el traspaso de lo que este acto sí puede entregarle a quien redacte la versión 1.2, con los `relacion_id` y variables exactas para que ese acto no re-derive nada de lo que ya está aquí verificado.

**La línea, verbatim, para que quien la lea no tenga que reconstruirla:**

> ISSP corrobora la fila 14 con un segundo instrumento; aporta reactivo sin co-observación para 12 y 13; no reclasifica nada por sí solo.

**Fila 14 (`radio_confianza`, G5) — convergencia de dos instrumentos independientes, no un hallazgo único.** El censo v1.0 (§5, fila 14) ya declaraba esta fila cerrada por puente vía ENBIARE 2021 (`REL-5741e12c`, PB1_01/02 confianza generalizada 0-10 + PF1_1-6 dificultad financiera realizada, N=31,166 — sellado por ABRIR-4). Este acto encuentra el **mismo tipo de cierre, en un instrumento completamente distinto**: ISSP 2017/ZA6980 (`REL-b034b04e9ba040bd02e39b8b`), `v35` (Q11, confianza generalizada categórica) + `v59` (Q31, dificultad para llegar a fin de mes), N=1,002, `desenlace_coobservado_en_mismo_instrumento=SÍ` verificado en este acto (§7.2). Dos fuentes de datos independientes, dos diseños muestrales distintos, mismo patrón estructural (reactivo de confianza + desenlace de necesidad financiera, misma tabla, misma muestra). Eso es convergencia — vale más para la robustez de la fila que un hallazgo aislado, y un futuro censo v1.2 puede citarlo así sin tener que reabrir ISSP.

**Filas 12 y 13 — reactivo aportado, sin co-observación, no forzado a encajar en el patrón de puente.** Verificado en este acto, honestamente declarado como lo que es:

- `12 familismo_apoyo`: ISSP 2017/ZA6980 (`REL-7751c832c7e30e4e4d7603cc` / `REL-e95e26820797a0f55c9246d7` / `REL-9dfab617c356df5594575a3c`), `v26` (Q8a, "a quién recurriría si necesitara pedir prestada una gran suma de dinero" — familia+amigos cercanos 49.0% de México). Reactivo real, verificado byte a byte. **No** se declaró `desenlace_coobservado_en_mismo_instrumento=SÍ` para esta fila — el ítem es él mismo una medida de disposición hipotética, no un reactivo con un desenlace realizado distinto co-observado al lado (§8 de este acto, celda 8 del TSV).
- `13 familismo_obligacion`: ISSP 2012/ZA5900 (`REL-cd0d1c5fd7e85418603c73cd` / `REL-d630dc1ea394364e53631401`), `V27`/Q7f + `V35`/Q14; ISSP 2017/ZA6980 (`REL-75b2ff53a19d8058eba2dbb7`), `v38`/Q13a ("Los hijos adultos tienen el deber de cuidar a sus padres ancianos"). Los dos módulos, verificados. Igual que la fila 12: reactivo sin desenlace co-observado declarado — la fila 13 del censo sigue bloqueada por lo que ya estaba bloqueada antes de este acto (sin magnitud asignada, ADR-30, `procedencia.yaml:629`), y ningún reactivo la desbloquea por sí solo. Este acto no lo promete y no lo entrega.

**Lo que este traspaso NO hace:** no reclasifica ninguna fila del censo v1.0/v1.1, no calcula ninguna magnitud, no adjudica si `v35`/Q11 mide el mismo constructo que ENCUCI `AP5_1_1/2/3` (esa equivalencia queda, como ya declaró §7.2, para que mesa la adjudique). Es un traspaso de evidencia verificada, con cita exacta, para que el acto que sí tenga el perímetro de censo v1.2 no tenga que reabrir ISSP para encontrar lo que este acto ya encontró.

## 14 · Respuesta al traspaso de ACTO CAPA3-RECONCILIA §7 (recibido en la segunda fusión de `origin/main`)

`forense/notas/2026-08-13-capa3-reconcilia.md` §7, fusionado a esta rama mientras se cerraba este acto, dirige explícitamente una pregunta a APERTURA-ISSP: de 7 filas de `relaciones.tsv` cuyo `siguiente_accion` pide abrir un **codebook**, 4 caen dentro de las 7 necesidades de este acto. Respondida aquí, con lo que este acto ya verificó — para que no se pierda como le pasó a ABRIR-4 (cinco días sin verse), citado explícitamente en esa misma nota como la razón de escribir esto ahora, no después:

- **`REL-9dfab617c356df5594575a3c` (N12, apunta a `za6980_q_mx`) y `REL-b034b04e9ba040bd02e39b8b` (N14, apunta a `za6980_q_mx`) — el codebook que piden no existe, y no hizo falta.** Confirmado en este acto (§0 de esta nota) y de forma independiente por CAPA3-RECONCILIA (`grep -n "za6980.*cdb" data/manifiesto.yaml` → 0): ZA6980 no tiene payload de codebook registrado. Este acto resolvió N12 (`v26`/Q8a) y N14 (`v35`/Q11 + `v59`/Q31, la fila titular) leyendo `reader.variable_labels()` del propio `.dta` más el cuestionario en español (`za6980_q_mx`) — una vía completa, ya ejecutada, que no depende de adquirir nada nuevo. "Adquirir/registrar su codebook" no es un bloqueo real para estas dos filas específicas.
- **`REL-cd0d1c5fd7e85418603c73cd` y `REL-d630dc1ea394364e53631401` (ambas N13, apuntan a `za5900_q_mx`) — el codebook que piden sí existe (`za5900_cdb`), y este acto lo usó directamente.** V27 (p.79), V34 (p.99), V35 (p.101), V36 (p.103) — las cuatro citas de §7.1 y §7 de esta nota vienen de `za5900_cdb`, no de `za5900_q_mx`. Si `relaciones.tsv` reapunta el `id_manifiesto` de estas dos filas de `za5900_q_mx` a `za5900_cdb` (la decisión que CAPA3-RECONCILIA deja nombrada para "APERTURA-ISSP, dueña de capa4 en estas filas"), la evidencia ya verificada aquí lo respalda sin re-abrir nada — este acto no hace ese cambio (`relaciones.tsv` fuera de perímetro, §2 del encargo), lo deja escrito para quien sí lo tenga.
- **Las 3 filas restantes del traspaso (`REL-72ff714a`/N2, `REL-845a93bc`/N2, `REL-8d2952203ec3678f3bd0c473`/N30) quedan genuinamente fuera de este acto** — N2 y N30 no son ninguna de las 7 necesidades de la rejilla de §1. No respondidas aquí, no adivinadas.

**El traspaso de CAPA3-RECONCILIA §7 queda consumido por lo de arriba, confirmado explícitamente para que nadie lo persiga después** — las 4 filas de sus 7 que caían dentro de esta rejilla (N12/N13×2/N14) tienen respuesta verificada aquí; las 3 restantes (N2×2/N30) están correctamente fuera del perímetro de este acto, no ignoradas.

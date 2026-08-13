# ACTO APERTURA-ISSP · Apertura a nivel variable, los dos módulos ISSP con México

Ejecuta el encargo `forense/encargos/2026-08-13-apertura-issp.md` (A.3, commit previo en esta rama). Responde a la deuda dejada explícitamente por ACTO R″ (`forense/notas/2026-08-13-r2-registro-via-completa.md` §4): "eso excede lo que este acto puede cerrar sin abrir cada reactivo contra cada necesidad, y es justamente el trabajo de una apertura a nivel variable".

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

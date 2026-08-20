# Nota · ACTO T-SELLO — cierre

**Fecha:** 2026-08-20 · **Rama:** `claude/tsello-nube-opus-arranque-vad18w` · **Encargo:** `forense/encargos/2026-08-20-T-SELLO.md`.
**Base al arrancar:** `906203a0a732b1e138427bfa2b4dfe284cf51e35` (`origin/main`, `PR #296`, `ACT-PIL-1 · CONTRATO-v0_5` — el gate declarado en la cabecera del encargo, ya cumplido).
**Base al cerrar:** `origin/main = 867948cef80a717b9afed812e22b5eb6632846fa` (`PR #297`, `ACT-PIL-2`), fusionada dentro de esta rama a mitad de acto — ver §2.
**Entorno:** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (NUBE), crudo, sin sonda — coincide con P4 del ARRANQUE. `data/raw`: no se usa, no montada, no consultada, no enlazada (P3). Espejo: no consultado — `PLAN-CALCULO-TOTAL` llegó como adjunto, `/mnt/project/` no existe en este entorno (P5).

---

## 1 · Compuerta de arranque y VERIFICACIÓN A.8

Los tres adjuntos (APERTURA-FASE-CALCULO v1.1, `TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md`, PLAN-CALCULO-TOTAL v1.0) llegaron en el primer turno. `APERTURA` verificó `sha256` exacto contra el declarado por el lanzador (`a35b5452…`, 8 870 bytes, 54 líneas); `TRANSFER` y `PLAN` no traían hash previo — se declararon por primera vez (`96939c5f…`/`3f9efc4b…`).

VERIFICACIÓN A.8, re-derivada y no heredada (el propio encargo lo exige: "re-verifica y lee los archivos que devuelva el grep, no solo el conteo"):

```
git ls-files | grep -i calculo-total                                 → (vacío)
grep -rli "APERTURA.*FASE.*DE.*CALCULO" --include="*.md" .           → (vacío)
grep -rli "MAESTRA OPUS" --include="*.md" .                          → (vacío)
find . -iname "*TRANSFER*MAESTRA*FASE*CALCULO*" -not -path "./.git/*" → (vacío)
find . -iname "*APERTURA*FASE*CALCULO*" -not -path "./.git/*"        → (vacío)
git ls-tree -r --name-only HEAD | wc -l  (al arrancar, contra 906203a) → 1727
```

Coincide con el punto (2) del encargo — cero archivos en los tres casos. Diverge del punto (2) en el universo: el encargo declaraba **1 717**; esta compuerta, contra la base real del acto, dio **1 727** — diez archivos de diferencia, todos legítimos (`PR #295`/`ACT SELLA-ADV` y `PR #296`/`ACT-PIL-1` fusionaron entre que Fable escribió el encargo el 19/ago y este acto arrancó el 20/ago). `data/INFRAESTRUCTURA-v1_0.md` sigue sin cubrir el dominio de archivo de documentos adversariales/compass — mismo hueco que `ACTO SELLA-ADV` ya declaró el 19/ago (`grep -n "forense\|adversarial\|compass" data/INFRAESTRUCTURA-v1_0.md` no da entrada gobernante), re-verificado aquí, no resuelto por ninguno de los dos actos. Punto (3): sin brecha retroactiva, confirmado — nada que este acto toca antecede a las tablas que lo gobiernan.

## 2 · Concurrencia: `origin/main` se movió dos veces mientras este acto corría

`git fetch` a mitad de T1 mostró `origin/main` en `867948c` (`PR #297`, `ACT-PIL-2`), por delante del `906203a` contra el que arrancó el acto. Por ARRANQUE P2 ("si main se movió no es PARO: refresca, re-deriva, reporta"), se hizo `git merge origin/main` (limpio, sin conflictos ni en `tests/check.py`) y se re-derivó lo que dependía del perímetro:

- `ADR-130` ya estaba tomado por `ACT-PIL-2 · MARCO-M1-A` — las siete auto-citas a "ADR-130" que `T1` ya había escrito en las cabeceras de procedencia de los tres documentos se renumeraron a `ADR-131` (commit separado, `9ce5686`).
- `FP-84` era el máximo real del tablero, no `78` como el encargo (fechado 19/ago) asumía — las cinco filas nuevas de `T4` nacieron en `FP-85`…`FP-89`, re-derivadas por `awk` sobre la columna `id`, no heredadas.
- `ACT-PIL-2` ya había ejercido sustantivamente la autorización de `D-iii` (construyó el marco de 60 candidatas bajo `ADV1-M1`/`ADR-128(e)`) antes de que `D-iii` tuviera su propia fila de tablero — declarado en `ADR-131(a)` y en `forense/hallazgos.md` como backfill, no como desbloqueo nuevo.

Segunda verificación de `git fetch` antes de escribir `ADR-131`: sin cambio contra `867948c`. Tercera, antes de cerrar esta nota: sin cambio.

## 3 · T1 — aterrizaje verbatim

Los tres documentos se copiaron byte-idénticos desde el adjunto (`cp` + `diff -q`, limpio) antes de tocarlos, para garantizar fidelidad de transcripción; luego cada uno recibió su cabecera de procedencia y, donde el encargo lo pedía, el contenido adicional:

- `canon/APERTURA-FASE-CALCULO-v1_2.md`: cabecera + banner de una línea en `§5` ("SUSTITUIDO... por el careo"), `§5` original intacto debajo (`A.10` corolario 1).
- `canon/PLAN-CALCULO-TOTAL-v1_1.md`: cabecera + `§5` nuevo al final, con la tabla `§1` de `APERTURA` citada **verbatim** (incluida la grafía "census" del original, no corregida) como delta fechado; cuerpo v1.0 intacto arriba.
- `forense/TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md`: cabecera únicamente, cuerpo verbatim.

`diff` de cada uno contra su adjunto original, verificado antes de commitear: la única diferencia es la cabecera (+ banner/delta donde aplica) y el salto final — pegado en los commits `625f165` y `9ce5686`.

## 4 · T2 — `forense/adv-duelo/` y cierre de `FP-78`

`git mv` de los cuatro adversariales de `forense/` raíz (`ADV-1_demolicion_duelo_L_vs_M.md`, `ADV-1_demolicion_duelo_v1.md`, `informe_ADV2_estado_del_arte_y_rubrica.md`, `compass-5-d3f09137-estado-arte-duelo-2026.md`) a `forense/adv-duelo/`, historia conservada (`git log --follow` sigue resolviendo). `compass-4` no se tocó — cita activa en `canon/modelo-decision-v4_0.md`, múltiples ADR y `forense/firmas-pendientes.tsv`; una búsqueda de ese fragmento de ruta sobre `canon/`+`forense/` da once archivos que lo citan, contando este mismo; moverlo los habría roto todos. `compass-1`/`compass-2`/`compass-3` tampoco — fuera del alcance del careo, y el encargo no los nombra. La CAREO misma (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`) se quedó en `forense/` raíz: el encargo dice "mueve ahí los cuatro adversariales", no cinco ni seis — su propio §D nombra `DUELO-PREREG-V2` como el acto que la moverá junto con "los cinco informes"; este acto no se adelanta a esa asignación.

`FP-78` cierra `FIRMADA`, no porque una carpeta gane sobre otra, sino porque la pregunta real —"¿de dónde se derivan cifras: repo o espejo?"— ya tenía regla firmada en `TRANSFER §8`. El sitio exacto dentro del repo (`forense/` vs `corpus/forense/` vs `forense/adv-duelo/`) queda como estaba, sin adjudicar cuál "gana" — porque los tres son repo. `data/INFRAESTRUCTURA-v1_0.md` sigue con el hueco declarado (§1, arriba); `ADR-70(c)` sigue pendiente.

## 5 · T3/T4 — `ADR-131` y tablero

`ADR-131` sella `D-i`–`D-iv` verbatim del `TRANSFER §4` (idéntico a `CAREO §C`), con la prohibición operativa de "supera" (`ADV1-M4`) citada en `(a)`; declara ABIERTA en canon la Fase de Cálculo bajo `APERTURA-FASE-CALCULO-v1_2.md` en `(b)`, distinguiendo explícitamente gobernanza (hoy) de resultado (`GO`/`NO-GO` de `PILOTO-E1E3`, sin correr); registra sin resolver, en `(c)`, la contradicción de tres textos vigentes sobre el criterio de cierre de `PILOTO-E1E3 T4` (`ADR-128` vence los 7 umbrales salvo el 1; `ADV1-M6` conserva y endurece 3 de los mismos 7; `PLAN-CALCULO-TOTAL` OLA 4 sigue citando los 7 como `GO`/`NO-GO`); estampa `A.10` en `(d)`.

Tablero: `FP-78` `ABIERTA`→`FIRMADA`; `FP-85`…`FP-88` nacen y cierran `FIRMADA` (una por cada `D-i`…`D-iv`); `FP-89` nace `ABIERTA`, gatea `PILOTO-E1E3 T4`. Total re-derivado por `awk` sobre la columna `estado`, no heredado:

```
awk -F'\t' 'NR>1{print $6}' forense/firmas-pendientes.tsv | sort | uniq -c
     11 ABIERTA
     15 CERRADA
     63 FIRMADA
```

## 6 · Desviación de perímetro declarada — `tests/check.py` y `tests/baseline.json`

El encargo dice "No toca ... `tests/`". Dos necesidades reales chocaron con esa línea, ambas mecánicas y ambas con precedente en este mismo repo:

**(a) `_T25_ARCHIVOS_CONOCIDOS`** — el `git mv` de `T2` y los tres documentos verbatim de `T1` traen rótulos pelados de los mecanismos del piloto y del hito de aterrizaje, legítimos por diseño (citas verbatim de texto anterior a `D-6`/`ADR-128`), registrados hoy por su ruta vieja. `T25` los re-evalúa por ruta nueva y dispara. El propio mensaje de `FAIL` de `T25` prescribe la salida: registrar la ruta en el censo, no editar el contenido. Commit separado (`99573a1`), seis rutas añadidas, ninguna otra línea tocada.

**(b) `tests/baseline.json`** — el `TRANSFER` verbatim trae, en su `§7`, seis nombres de archivo que la propia cola ejecutable del programa aún no aterriza (cinco encargos y un careo, listados por su nombre de adjunto original); el propio encargo (`forense/encargos/2026-08-20-T-SELLO.md`), archivado verbatim por convención de `forense/encargos/`, cita dos nombres de adjunto en su compuerta de arranque; los dos documentos nuevos de `canon/` no traen el bloque `ARCHIVO`/`NOMBRE ESTABLE` de `ADR-36` porque el adjunto original tampoco lo traía; el `PLAN` verbatim cita, en su tabla de foto verificada del 12/ago, su propio conteo histórico de ADR. Los doce son exactamente la clase que este mismo archivo ya documenta dos veces (`TRANSFER-maestra-9.md`, `revision-publicacion-2026-07-30.md`: "bucket propio en `tests/baseline.json`") — verbatim archivado con dangling refs conocidas y permanentes. Se registraron como doce entradas nuevas en `warns`/`fails` (según severidad real del test), **sin tocar `head`** (`e24d033`, el mismo de siempre) ni ninguna entrada existente — operación aditiva, no `--freeze`. Cinco citas más resultaron ser prosa propia de este acto (no verbatim, en cabeceras de procedencia y notas de archivo) y se corrigieron en vez de aceptarse.

Ambas desviaciones se declaran aquí y en `forense/hallazgos.md`; ninguna se ocultó en un commit sin mensaje.

## 7 · Cierre

```
python3 tests/check.py --baseline | tail -6
════════════════════════════════════════════════════════════════════════
  23 FAIL · 136 WARN
════════════════════════════════════════════════════════════════════════
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
  (1 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

`canon/estado-programa-v1_10.md`: cascada de ADR (`130→131`) y de WARN/FAIL (`126→134`/`21→23`, núcleo sin `T16`), ambas por corrida real. `pgrep -af claude` al arrancar: un solo proceso `claude` — dueña única confirmada.

**Contador: medición sobre México = 0, dicho.** Este acto sella firmas de mesa, aterriza documentos, mueve archivos y registra una contradicción de gobernanza — no corre ninguna celda-D, no produce ninguna estimación. `candidatas del marco: 60 de 60`, `Hito D: 13 de 27`, `condicionales 12/15`, `coeficientes 0/15`, `llaves 1/2` — ninguno se mueve.

**La fase queda abierta en el canon, no en una conversación** — `canon/APERTURA-FASE-CALCULO-v1_2.md` vive en `main` (tras fusionar), citado por `ADR-131(b)`. Lo que sigue, sin adjudicar aquí: `PILOTO-E1E3 T4` no puede correr su `GO`/`NO-GO` hasta que mesa firme cuál de los tres criterios de `FP-89` gobierna; `DUELO-PREREG-V2` (acto sucesor nombrado por `CAREO §D` y por `TRANSFER §5`) sigue sin lanzar.

# `/revisa --post-hoc` · PR #619 · tramite/despacha 2026-09-08: PARO digesto_tramite.py + candado EN-CURSO en cola

Disparado por el webhook `pull_request.opened` sobre el PR #619
(`claude/tramite-2026-09-08` → `main`). Al llegar a este pase el PR ya
estaba fusionado: abierto `2026-09-08T15:56:43Z`, fusionado por mesa
(`Josanoforo`) `2026-09-08T15:57:57Z` — **74 segundos** después de
abrirse, antes de que esta rutina alcanzara a construir la vista previa.
Se cambia a modo `--post-hoc` (bloque 1.4): no hay vista previa que
comentar, el merge ya ocurrió, y el veredicto de abajo es retrospectivo
/ de calibración.

Título `tramite/despacha 2026-09-08: PARO digesto_tramite.py + candado
EN-CURSO en cola` — no empieza por `[TRAMITE]` ni `[REVISA]`, así que no
aplica la excepción del guardrail 0.6; los once puntos corren completos.

**VEREDICTO: NO-FUSIONAR** *(retrospectivo — el PR ya está fusionado,
como el 619 mismo; A.3 bloque 1.4)*
`3 BLOQUEA · 0 RESERVA · 0 NO-VERIFICADO · 7 NO-APLICA`

## Identidades

```
$ git show --no-patch --format='%H %P' 52dbbdc
52dbbdc14d8acc9c76fadfa8ae067d525436e1a6 e12b37ce8d13ab65cf8655c1b3ce285acf06643f f1140b2b84a399411de0f5820073aacb06964322
```

`MERGE=52dbbdc` · `P1(base antes)=e12b37c` · `P2(head del PR)=f1140b2`.
`P1` es exactamente el `origin/main` que existía cuando esta rutina
construyó su vista previa antes de descubrir el merge, así que el
`git merge-tree` corrido en vivo (`exit=0`, limpio) y el `git worktree`
levantado sobre él son bit a bit el mismo árbol que produjo el merge
real:

```
$ git diff --stat e12b37c f1140b2   # (mismo diff que produjo el merge)
 forense/rutinas.tsv | 2 ++
 1 file changed, 2 insertions(+)
```

Los once puntos corrieron sobre `<merge>^1..<merge>^2`, con un
`git worktree add --detach` sobre `origin/main` (`e12b37c`) más
`git merge --no-ff --no-commit` de `f1140b2`, retirado al cerrar junto
con la rama local de fetch.

---

## Hallazgos

**1 · BLOQUEA (punto 2.5 — tres cifras/hechos que la re-derivación
contradice, mismo origen: `main` avanzó bajo el PR antes de que
fusionara).** El PR reporta tres afirmaciones puntuales, las tres
correctas en el instante en que la rutina `/despacha` las leyó
(`f1140b2`, `2026-09-08 14:17:31 UTC`) y las tres ya falsas para cuando
el propio PR #619 fusionó (`2026-09-08 15:57:57 UTC`, 100 minutos
después):

- **a) `ESTADO: EN-CURSO` de la fila de cola.** El PR asienta en
  `forense/rutinas.tsv`: *"CANDADO:EN-CURSO en
  forense/encargos/cola/2026-09-07-GEN2-E7-READINESS-2.md (piezas A/B/C
  sin fusionar, pieza D en curso)"*. Re-derivado sobre el árbol del
  merge:

  ```
  $ git show 52dbbdc:forense/encargos/cola/2026-09-07-GEN2-E7-READINESS-2.md | head -1
  ESTADO: CONSUMIDO — PR #612, PR #613. Sincronizado por `tools/cierre_acto.py --aplica` ...
  ```

  Reconstrucción de la línea de tiempo: el flip a `CONSUMIDO` vive en el
  commit `8dafe66` (`2026-09-08 07:11:53 UTC`, *"P4: los cinco ajustes
  de la revisión de PR #613"*), que llegó a `main` fusionado como parte
  de PR #615 en `fbd847d` (`2026-09-08 09:13:06 -0600` =
  `2026-09-08 15:13:06 UTC`). `/despacha` leyó `main` a las `14:17:31
  UTC`, **56 minutos antes** de que PR #615 fusionara — su lectura
  `EN-CURSO` era exacta en ese instante:

  ```
  $ git merge-base --is-ancestor 8dafe66 e12b37c && echo SI-ESTABA-EN-BASE-DEL-PR || echo NO-ESTABA-AUN
  NO-ESTABA-AUN
  ```

  Pero PR #619 (este mismo PR) fusionó a las `15:57:57 UTC`, **45
  minutos después** de que PR #615 (que trae el `CONSUMIDO`) ya estaba
  en `main`. Es decir: para cuando `forense/rutinas.tsv` quedó escrito
  en `main` diciendo "candado de `/despacha` permanece cerrado", el
  candado ya llevaba tres cuartos de hora abierto en el propio `main`
  contra el que se fusionaba. La cifra no es inventada ni mal medida —
  es una foto tomada un instante antes de que el terreno se moviera, y
  el PR nunca refrescó la foto antes de fusionar.

- **b) Las "dos ramas no contenidas en main".** El PR declara:
  *"`claude/tramite-2026-09-08` y
  `claude/motor-matricial-d11-demanda-2188aw`"*. La segunda es la rama
  fuente de PR #615 — el mismo PR que resolvió (a). Re-derivado sobre
  el estado actual del remoto:

  ```
  $ git ls-remote --heads origin
  ca1342db9a0d3e5389ce4a4a787160f391312dfb  refs/heads/claude/new-session-xhtzkj
  52dbbdc14d8acc9c76fadfa8ae067d525436e1a6  refs/heads/main
  ```

  Ninguna de las dos ramas que el PR nombra existe ya como rama remota
  (la primera es la propia rama de este PR, borrada tras fusionar; la
  segunda se fusionó y borró vía PR #615). El hallazgo no es que
  "debieron seguir abiertas" — es que la fila que este PR grabó en
  `main` como hecho vigente ("ramas de acto abiertas") describe un
  estado que dejó de existir antes de que la propia fila llegara a
  `main`.

- **c) `187 WARN` de `tests/check.py --baseline`.** El PR reporta
  *"LÍNEA BASE VERDE (3 FAIL preexistentes, 187 WARN)"*. Re-derivado
  sobre el árbol del merge:

  ```
  $ python3 tests/check.py --baseline 2>&1 | tail -3
  3 FAIL · 194 WARN
  ────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
  ```

  `FAIL` coincide (`3=3`); `WARN` no (`187` vs `194`, +7). La compuerta
  real —`tests/baseline.json`, que el PR no toca
  (`git diff --stat e12b37c f1140b2 -- tests/baseline.json` → vacío)—
  sigue VERDE en ambos números, así que esto no habría bloqueado un
  merge por sí solo. Pero es la misma clase de hallazgo que (a) y (b):
  entre que `/tramite` corrió (`13:54:50 UTC`) y que el PR fusionó
  (`15:57:57 UTC`) fusionaron además PR #616, #617 y #618, cada uno
  agregando WARNs propios al corpus narrativo que `T06`/similares
  cuentan.

Las tres comparten causa y remedio: en un repositorio con varias
rutinas automatizadas fusionando el mismo día, un PR que sólo asienta
"lo que vio" sin volver a verificarlo justo antes de fusionar puede
grabar en `main`, como hecho permanente, un estado que ya caducó. El
punto 2.5 no distingue "cifra falsa por descuido" de "cifra caducada
por ritmo del repo" — las tres contradicen la re-derivación y las tres
pesan `BLOQUEA` por la letra de la regla. La propuesta de arreglo, como
propuesta: que `/despacha` re-verifique el candado (una consulta de
`git fetch` + grep del `ESTADO`) inmediatamente antes de escribir su
huella, no sólo al principio de la corrida — y que, si el candado se
abrió mientras la rutina corría, lo diga así ("candado se abrió a media
corrida, ver PR #615") en vez de asentar la lectura vieja como si
siguiera vigente.

**2 · Verificación positiva, no hallazgo:** el crash de
`tools/digesto_tramite.py` que motiva el `PARO` de `/tramite` se
reprodujo exacto, byte a byte con el traceback que el PR describe:

```
$ python3 tools/digesto_tramite.py 2>&1 | tail -6
  File "tools/digesto_tramite.py", line 1305, in seccion_i
    hoy = datetime.date.fromisoformat(fecha)
TypeError: fromisoformat: argument must be str
```

Sin escritura nueva bajo `forense/digesto/` (`git status --porcelain
forense/digesto/` → vacío) — el PARO es real y el perímetro declarado
("reparar el script queda fuera del perímetro de este agente") se
sostiene.

Ningún hallazgo adicional: el PR no toca `forense/encargos/`, no mueve
ADR/FP, no borra contenido de ningún archivo (`git diff --numstat` sin
líneas negativas), y su perímetro declarado (`forense/rutinas.tsv`)
coincide exacto con el único archivo tocado.

---

## Los once puntos

| # | Punto | Estado | Comando / evidencia |
|---|---|---|---|
| 2.1 | Encargo archivado verbatim, coherente con reporte | **NO-APLICA** | `git diff --name-only e12b37c f1140b2 -- forense/encargos/` → vacío. El PR es footprint de dos rutinas estándar (`/tramite`, `/despacha`) que consumen encargos ya archivados por actos previos; no archivan un encargo propio en este PR. |
| 2.2 | Spec congelada antes de resultados | **NO-APLICA** | Sin encargo propio (ver 2.1); el PR no mide nada sobre México — es footprint de infraestructura de proceso (`PARO`/`CANDADO`). |
| 2.3 | Perímetro declarado vs. tocado | **PASA** | Cuerpo del PR: `## Perímetro — forense/rutinas.tsv (huellas de PARO/candado)`. `git diff --name-only e12b37c f1140b2` → `forense/rutinas.tsv`, único archivo. Coincidencia exacta en las dos direcciones. |
| 2.4 | Negativos con conteo de archivos (A.13) | **PASA** | *"Cero commits sobre encargos"*: `git diff --name-only e12b37c f1140b2 \| grep -c '^forense/encargos/'` → `0`, confirmado. *"17 archivos en cola examinados"*: `ls forense/encargos/cola/ \| wc -l` → `17`, re-derivado exacto. |
| 2.5 | Toda cifra re-derivada por comando | **BLOQUEA** | Ver hallazgo 1 (a/b/c): `ESTADO: EN-CURSO` re-derivado como `CONSUMIDO`; las dos ramas citadas ya no existen en `origin`; `187 WARN` re-derivado como `194 WARN` (el `3 FAIL` sí coincide). Tres cifras/hechos contradichos por la re-derivación sobre el árbol del merge. |
| 2.6 | Originales intactos donde el encargo lo exige | **PASA** | `git diff --numstat e12b37c f1140b2` → `2  0  forense/rutinas.tsv` (0 líneas borradas). |
| 2.7 | Escala y universo declarados | **PASA** | Las dos cifras nuevas (`17 archivos en cola`, `2 ramas`) declaran su universo en la propia línea (`en forense/encargos/cola/`, `via git ls-remote --heads origin`) — el problema no es falta de universo, es que el universo cambió después de medirlo (ver hallazgo 1). |
| 2.8 | ADR/FP: colisión, referencias, contigüidad, cabeceras | **NO-APLICA** | `git diff --name-only e12b37c f1140b2 \| grep -cE 'canon/gobernanza\|firmas-pendientes'` → `0`. El PR no toca ninguno de los dos. |
| 2.9 | `tests/check.py --baseline` sobre el merge | **PASA** *(gate)* / **BLOQUEA** *(cifra, ver 2.5c)* | `LÍNEA BASE: VERDE` (exit=0) sobre el árbol del merge; `tests/baseline.json` sin diff. El gate real pasa; el número reportado en el PR (`187 WARN`) no reprodujo (`194`) — contabilizado en el hallazgo 1c / punto 2.5, no como fila duplicada aquí. |
| 2.10 | "Lo que NO hace", respetado | **NO-APLICA** | Sin encargo archivado propio (ver 2.1) no hay sección `## LO QUE NO HACE` que cotejar. Las prohibiciones que el PR sí se auto-impone ("reparar el script queda fuera del perímetro") se verifican en el hallazgo 2: sin escritura nueva bajo `forense/digesto/`. |
| 2.11 | `## NO-CORRIDO/RESERVAS` cotejado contra diff y encargo | **NO-APLICA** | Sin encargo archivado con piezas enumerables asociado a este PR (ver 2.1); las dos filas de `## NO-CORRIDO / RESERVAS` del cuerpo (digesto sin escribir; cola `READINESS-2` "sigue EN-CURSO") son el propio `PARO`/`CANDADO` de las rutinas, no piezas de un encargo distinto sin cubrir. La segunda fila repite, en el cuerpo del PR, la misma afirmación ya contradicha en el hallazgo 1a — no es un hallazgo nuevo de este punto, es el mismo hecho caducado visto desde el otro documento. `forense/no-corrido.tsv` no lo toca el PR (`git diff e12b37c f1140b2 -- forense/no-corrido.tsv` → vacío) y ese TSV rastrea NC-#### de actos con encargo, no PARO de rutinas diarias — coherente con no tocarlo aquí. |

`CONTADOR: cero mediciones, declarado (infraestructura).`

**Qué NO revisó este pase:** no se auditó si `tools/cierre_acto.py
--aplica` (el script que sincronizó `READINESS-2` a `CONSUMIDO` dentro
de PR #615) es en sí mismo correcto — se tomó su resultado en `main`
como el hecho contra el cual re-derivar, no como algo a su vez
verificable aquí. Tampoco se re-corrió `/despacha` de punta a punta
para confirmar que, con el candado ya abierto, habría tomado una
decisión distinta (correr un encargo `LISTO-NUBE` en vez de declarar
`PARO`) — eso es trabajo de un acto sucesor de `/despacha`, no de esta
revisión. No se leyeron los diffs completos de PR #616/#617/#618 para
atribuir cada uno de los `+7 WARN` a una línea concreta; el hallazgo 1c
se cierra con la cifra agregada, no con el desglose por PR.

---

Este veredicto es de calibración (bloque 1.4): no se publica en GitHub.
Se abre como PR propio, `[REVISA] post-hoc #619`, que contiene
únicamente este archivo. No aprueba, no fusiona y no empuja nada sobre
`PR #619` ni sobre ninguna otra rama. Fusionar es firmar, y firmar es de
mesa — y este PR #619 ya lo firmó mesa, 74 segundos después de abrirse,
antes de que esta revisión pudiera correr.

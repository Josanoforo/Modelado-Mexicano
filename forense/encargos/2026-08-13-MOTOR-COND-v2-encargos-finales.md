# ENCARGOS FINALES · MOTOR + CONDICIONALES — v2 consolidada

**Archivado por A.3** (`instrucciones-proyecto-v2_5.md` Bloque D-bis) al ejecutar el acto **PROC-11** (§2), primero de los seis que este encargo lanza.

## Cabecera obligatoria (`forense/encargos/convencion.md`)

- **SHA de redacción.** El encargo declara «corte verificado por dirección: `origin/main` post-#220 (PROC-10 fusionado)». El `origin/main` **real** al arrancar PROC-11 es **`1cb6e3e`** (`Merge pull request #219 from Josanoforo/triage-63`), un merge más allá: `dc75d74` (#220, PROC-10) es ancestro suyo y #219 (TRIAGE-63) fusionó después. PROC-10 sí está en el terreno. TRIAGE-63 no toca `canon/`, `milpa/` ni `tests/check.py` — la divergencia no movió nada del acto ejecutado. Declarada, no silenciada.
- **Entorno asignado.** Seis actos con entornos distintos, ver la tabla maestra §1 del texto: PROC-11 y MOTOR-1 a **nube** (repo-only, sin red); RONDA-M a **sesión NUEVA de Opus** (explícitamente **NO** la de MOTOR-1, **NO** linaje Fable); PROD-P638 a **caja con corpus**; ranuras D3 y MOTOR-2 a **mesa**.
- **Estado.** *(Repasado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS — cabecera ambigua para un grep de una sola línea, y cuatro de las seis partes habían avanzado sin que esta lista se actualizara. Solo esta lista se toca; el resto del archivo no se edita.)*
  - **§2 · PROC-11 — `CONSUMIDO`.** Ejecutado 13/ago/2026 en `cloud_default`, rama `claude/encargos-motor-v2-consolidada-4c2evp`, tres commits (`95d926d` mapa congelado · `1224c37` ejecución · `f986ce6` error de mapa y hallazgos). Nota: `forense/notas/2026-08-13-proc-11.md`.
  - **§3 · PROD-P638 — `CONSUMIDO — PR #235`.** *(`git merge-base --is-ancestor 2f2125c f3873c2` OK; commits `57a730b`/`7f91782` — REPRODUCE; contador → 11 de 15, `canon/modelo-decision-v4_0.md:287`.)*
  - **§4 · MOTOR-1 — `CONSUMIDO PARCIAL — PR #232`**, ejecutado como `forense/encargos/2026-08-14-MOTOR-1-consolidado.md` (su §3 declara ser el cuerpo completo de MOTOR-1; ver ese archivo, no está en el ANEXO de este acto). *(`git merge-base --is-ancestor 732d918 f3873c2` OK. Ese archivo declara "CONSUMIDO PARCIAL": los 5 archivos compass/red-team siguen sin llegar — inciso 2 de su Commit 1 sigue sin correr, tercera sesión consecutiva sin ellos, per ese mismo documento.)*
  - **§5 · RONDA-M — `CONSUMIDO — PR #233`.** *(`git merge-base --is-ancestor 4513798 f3873c2` OK; commit `dc67ad6` "ACTO RONDA-M: veredicto adversarial sobre propuesta-motor-matriz v0.1 §1-§5" en el árbol.)*
  - **§6 · MOTOR-2 — `VIVO`.** Sigue esqueleto sin sellar (commit `324d6c0`, "esqueleto del ADR del sello del motor, SIN sellar"); `forense/firmas-pendientes.tsv` trae FP-06/M6 todavía `ABIERTA` (`[FIRMA M6 — VACÍA]` en `forense/ADR-MOTOR-2-esqueleto-2026-08-14.md`, verificado por lectura al 14/ago) — sin evidencia en el árbol de sello posterior al 17/ago.
  - **Ranuras D3 — `RESUELTA`, ya no "sin firma".** La firma `D3: «Correr sin D3»` (registrada más abajo en este mismo archivo) más `D-A`/ADR-79(a) (`PROC-10-bis`) sellaron `MEDIDO·NACIONAL` y movieron el contador a `10 de 15`; `PROD-P638` (§3, arriba) lo llevó a `11 de 15` — `canon/modelo-decision-v4_0.md:287`, verificado 17/ago/2026.
- **Bloque VERIFICACIÓN DE EXISTENCIA (A.8), contestado.** Contestado íntegro en `forense/notas/2026-08-13-proc-11.md` §0.9 contra el árbol real. **Resultado no trivial: el segundo comando del bloque produce un FALSO PARA** — `ls data/curacion-registro/celdas-d/ | grep -c obligacion` da `1`, pero lo que matchea es la celda hermana `G5.familismo_obligacion.actitud.yaml`, que el propio encargo nombra como el molde a copiar. El predicado discriminante (`grep -c obligacion_medida`) daba `0`. Ver `forense/hallazgos.md`, entrada del 13/ago/2026.

## Advertencias de dirección para los actos que siguen `VIVO`

Levantadas al ejecutar PROC-11, sin editar el texto del encargo (abajo va verbatim):

1. **El predicado `grep -c obligacion` está roto como gate, en dos sitios más.** El §3 (GATE de PROD-P638) y el §4 (gate de la cascada del commit 2 de MOTOR-1) lo usan. En ambos **ya estaba satisfecho antes de que PROC-11 escribiera nada**: son gates que siempre pasan y por tanto no gatean. Usar `grep -c obligacion_medida` o `ls data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml`.
2. **El perímetro de `tests/check.py` del §2 no podía satisfacer su propio criterio de cierre.** Decía «SOLO la constante `_CONTADOR_14`»; T19c tiene una regex gemela del mismo contador, sobre `README.md`. Mesa firmó extenderlo. Ya ejecutado y con comentario cruzado en las dos.
3. **La cifra «las 7 apariciones» de `milpa/procedencia.yaml` es 8.** Heredada de `ACTO PROC-10` §1; falta `:630`. No cambia ninguna acción (las ocho son del coeficiente, todas NO-TOCAR), sí la cifra declarada.
4. **La pregunta del nombre de generador de G5 sale con dueño.** Por firma de mesa del 13/ago, entra a la cascada de MOTOR-1 y se firma en MOTOR-2. Detalle y la inconsistencia concreta que la motiva en `forense/notas/2026-08-13-proc-11.md` §A.4.
5. **RT-B y RT-D: subidos y verificados, NO commiteados.** Los dos red teams que §4/2.2 declara ausentes se subieron a la sesión de PROC-11 y su `sha256` se verificó contra el que el encargo declara — **coinciden los dos**: `7342ffbf2a1341eb1403ebb8ed218c12b742a85252a86f048732df29ace94614` (RT-B) y `2f5dfaa50610dbb1af41e5eb5258c3af17c74c740e09bd42d2fe6b9cc0fe88eb` (RT-D). **No se commitearon**: pertenecen al perímetro de MOTOR-1, no al de PROC-11. Hay que volver a subirlos a la sesión que ejecute MOTOR-1. La divergencia del espejo que §4 manda declarar también se verificó y **cuadra**: RT-A repo `17766f8f612d58c77abe2e1e7e4e8c24db4fba394dcf837f7fcc9ee35159b849` (`forense/auditoria_adversarial_benchmarks.md`) contra espejo `8bae9213…`; RT-C repo `12f0c8726a82d23e950b4cb0c00a314005ddaf00d876bd96f5c303141d7e1358` (`forense/red-team-auditoria-benchmarks.md`) contra espejo `01d47405…`. El repo manda.
6. **El texto de abajo llegó truncado.** Termina a mitad de frase, en «*…y un*». Se archiva tal como llegó, sin completar la frase — inventar el cierre sería peor que declarar el corte.

---

## Texto del encargo, verbatim

ENCARGOS FINALES · MOTOR + CONDICIONALES — v2 consolidada (sustituye a ENCARGOS-PROC-MOTOR1-RONDAM y a ADENDA-DECISIONES-D1-D2)

13/ago/2026 (noche) · corte verificado por dirección: origin/main post-#220 (PROC-10 fusionado) · línea base congelada 3d0d1e5 (ADR-76(f)) · suite 20 FAIL · 107 WARN — VERDE · ADR 78, cero huecos

QUÉ CAMBIÓ Y POR QUÉ ESTA VERSIÓN. Dos cosas, ambas verificadas contra el árbol: (1) PROC-10 (#220, redactado por el otro carril) ya corrió con desenlace (B): la décima condicional NO entró a procedencia.yaml porque la clase MEDIDO·PARCIAL(x) exige eje condicionante y la θ es marginal nacional (x = ∅) — el contador sigue 9 de 14 con la razón taxonómica escrita, y su §7 nombra la decisión que solo mesa toma (D3, abajo). El mismo muro aplica a P6_38 (también marginal). (2) El HANDOFF-MOTOR se integró con sus correcciones verificadas: los productos de Ronda 1 SÍ son canon vía ADR-68 (gobernanza:906,912,916); CAREO cita cuatro red teams y solo dos están en el repo; la Entrada 5 la cierra E5 del otro carril (gate por el número del ADR del motor — MOTOR-2 ya NO la cierra, solo notifica); el glosario celda-D/x/B sigue SIN hacerse (verificado). Hallazgo de dirección al empaquetar: las copias del espejo de RT-A y RT-C divergen del repo (hashes distintos, pares abajo) — el repo manda; queda declarado.

§0 · LA DECISIÓN NUEVA — D3 (taxonomía de condicionales) · las ranuras corren sin ella, nada se detiene

El problema, en una línea: el reglamento de conteo dice que una condicional "cuenta" solo si está medida POR SEGMENTOS (al menos un eje: edad, formalidad, urbanización…). Las dos nuevas (norma_de_género y obligación_medida) están medidas NACIONALMENTE — reproducidas, adjudicadas, impecables — pero la casilla "¿qué segmentos?" no se puede llenar sin inventar. PROC-10 §7 nombra las tres salidas:

D3-A (recomendada por dirección): se abre la clase MEDIDO·NACIONAL (o el nombre que mesa firme) en procedencia.yaml + su fila en modelo §1.1.F — ambas cuentan; contador → 10 de 15 y luego 11 de 15. La taxonomía crece para describir la realidad medida. D3-B: se corre la medición CONDICIONADA de cada θ (por los ejes que sus tablas traigan — por derivar del diccionario, no lo afirmo) — cuentan como MEDIDO·PARCIAL(x) legítimo; más trabajo, dato más rico; compatible con A (A ahora, B como refinamiento con dueño). D3-C: se acepta que no cuentan para el denominador — honesto pero perverso: una θ medida y adjudicada contaría menos que un proxy pendiente.

Firma de ejemplo: "D3: A — clase MEDIDO·NACIONAL, y B queda como refinamiento nombrado sin fecha." La ranura vive en §2; PROD-P638 (§3) trae la suya espejo.

§1 · TABLA MAESTRA — qué corre, dónde, gate, y en qué orden

| # | Acto | Dónde corre | Gate | Estado |
|---|---|---|---|---|
| 1 | PROC-11 (§2) | nube (cloud_default) o worktree de caja — repo-only, SIN red | ninguno | LANZA YA |
| 2 | MOTOR-1 (§4) | nube — repo-only | ninguno (su commit 2 se auto-gatea por comando) | LANZA YA — el usuario le sube compass ×3 + RT-B + RT-D |
| 3 | RONDA-M (§5) | sesión NUEVA de Opus (nube o worktree de caja) — NO la de MOTOR-1, NO linaje Fable | ninguno | LANZA YA |
| 4 | PROD-P638 (§3) | caja con corpus (concurrencia con INV-DESCMX declarada: archivos disjuntos — él toca tests/corpus.py, tú no tocas tests/) | PROC-11 fusionado (celda existe, D=15) | al fusionar #1 |
| 5 | Ranuras D3 de §2/§3 | quien tenga el archivo (serializa en procedencia/modelo — no junto a PROC-11/PROD-P638 activos) | firma D3 de mesa | al firmar |
| 6 | MOTOR-2 (§6) | mesa | MOTOR-1 c3 + veredicto RONDA-M en mesa (D3 NO lo gatea: es carril de condicionales, no del ejecutable) | al cerrar 2 y 3 |
| — | E5 (otro carril) | suyo | el NÚMERO del ADR de MOTOR-2 (aviso obligado) | fuera de este paquete — ver §6 |

Colisiones: procedencia.yaml/modelo-decision = un escritor (PROC-11 → PROD-P638 → ranuras-D3, en ese orden) · tests/check.py solo PROC-11 (una constante) · forense/ de MOTOR-1/RONDA-M disjuntos · hallazgos = union, merge local siempre.

§2 · ACTO PROC-11 — lo firmado que PROC-10 dejó explícitamente sin ejecutar, más la ranura D3 (repo-only · dos commits + A.3)

Insumo rector, se LEE antes que este encargo: forense/notas/2026-08-13-proc-10.md — su §5.2 declara el renombre "no ejecutado, no hace falta resolverlo porque nada se escribe" (aquí SÍ se escribe), su §4 encontró la cita obsoleta de modelo:271, su §3 fija la razón taxonómica que la ranura D3 resuelve.

════ ARRANQUE íntegro (v2.8) · SIN red · REMOTO verificado ════ Verificación de existencia (A.8):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"; git fetch -q origin
grep -c "norma_de_género" canon/modelo-decision-v4_0.md            # 0 = renombre pendiente (esperado); ≥1 = YA HECHO, PARA
ls data/curacion-registro/celdas-d/ | grep -c obligacion            # 0 = celda no existe (esperado); ≥1 = PARA
grep -n "_CONTADOR_14" tests/check.py | head -1                     # la constante existe — re-deriva su línea (hoy :869), check.py cambió 52 líneas en #218
grep -in "proc-11" forense/hallazgos.md forense/notas/*.md | wc -l  # 0 = no corrió antes
```

PERÍMETRO. ESCRIBE: canon/modelo-decision-v4_0.md (renombre + §1.1.F + los sitios de contador + la CITA de :271) · milpa/procedencia.yaml (renombre en las 7 apariciones del coeficiente donde aplique per enmienda; la ranura D3 si firmada) · la celda nueva G5.obligacion_medida.conducta.yaml · README.md:37 · canon/estado-programa-v1_10.md:97 (re-deriva líneas) · tests/check.py SOLO la constante _CONTADOR_14 (regex de\s*14→de\s*15 + comentario; diff completo en la nota) · nota · A.3 · hallazgos. NO ESCRIBE: gobernanza (historia; las citas "de 14" de ADRs viejos quedan) · tools/** · expedientes. Fuera de la lista, PARA.

Commit 1 — el mapa congelado: (a) enmienda ADR-75(b) (gobernanza:~874-896, re-deriva) verbatim como rector del renombre; lista grep -n "familismo_obligacion" en modelo+procedencia clasificada EDITAR/NO-TOCAR con razón (las llaves de celda y citas históricas NO se tocan — PROC-10 §1 ya mapeó las 7 de procedencia como del coeficiente: usa ese mapa, cítalo); (b) la celda: molde de la hermana con los campos del split (§2.1-§2.3 verbatim: P6_38, TPOB_CUI/FILTRO6_10, FAC_CUI, EST_DIS/UPM_DIS, periodo "semana anterior" ≠ hermana, la separación de escalas 7.65%-vs-69.33% en límites), requiere_decision_mesa: false, estado_operativo: PENDIENTE razón "expediente por la vía — PROD-P638"; (c) D 14→15: los seis sitios re-derivados + la línea nueva en §1.1.F citando ADR-75(b) y la firma D1; (d) el fix de modelo:271: SOLO la cita (ENUT→ENASIC P7_12_7, con ADR-67(b)/75(a)) — el RÓTULO de la fila espera D3, dilo; (e) [RANURA D3 — SOLO con firma pegada verbatim: si A, la definición de la clase nueva en el header de procedencia.yaml (junto a las seis, mismo formato), la entrada de norma_de_género con esa clase (θ, IC, n, fuente, límite de constructo de ADR-75(a), antes: la fila obsoleta), y la fila reescrita de §1.1.F Paso 5 → contador 10 de 15; si B, cero taxonomía aquí + traspaso nombrado a dos actos de medición condicionada; si C, la nota de exclusión con la razón]. Frase de siempre.

Commit 2 — ejecución: exactamente lo congelado (error de mapa ⇒ tercer commit) → suite --baseline cruda antes/después contra 3d0d1e5 — T19b [ ok ] con la regex nueva es criterio de cierre; contador declarado en una línea: 9 de 15 sin D3 (la razón: PROC-10 (B) + D3 pendiente — un "9 de 15" honesto vale más que un "10" inventado) o 10 de 15 con D3-A.

§3 · ACTO PROD-P638 v2 — el expediente de la θ ya calculada (caja con corpus · dos commits + A.3)

Sin cambio de núcleo respecto a la adenda: spec verbatim del pre-registro del split (§1.5, sellado ANTES de calcular) + parámetros §2.2 · documentacion_fuente poblado (ADR-70(b)) · pipeline prepare→produce→integrate con hashes_analista_confiados: false · criterio pre-escrito: reproducir las cinco proporciones e IC a los decimales de la nota · REPRODUCE ⇒ celda LISTO + fila 12 CALCULO_REPRODUCIBLE (la firma condicional D1 es tu autorización — no vuelve a mesa); NO-REPRODUCE o reserva nueva ⇒ celda PENDIENTE + paquete a mesa, la discrepancia es el entregable.

GATE: ls data/curacion-registro/celdas-d/ | grep -c obligacion ≥1 y grep -c "de 15" canon/modelo-decision-v4_0.md ≥1 (PROC-11 fusionado). CAMBIO ÚNICO (por PROC-10): el paso de procedencia/contador queda en ranura D3 espejo — con D3-A firmada: entrada con la clase nueva → 11 de 15; sin firma: se declara patrón PROC-10 ("entrada pendiente de clase, razón x=∅, decisión D3 nombrada") y el contador NO se toca. Concurrencia: paralelo con MOTOR-1/RONDA-M; con INV-DESCMX en caja sí (archivos disjuntos, cero tests/); con PROC-11/ranuras NO (mismo procedencia).

§4 · ACTO MOTOR-1 v2 — deltas sobre el encargo original (que sigue siendo el cuerpo)

2.2 se amplía — la cadena A.3 de CAREO se cierra aquí. Además de los tres compass (hashes del encargo original, sin cambio), commitea verbatim los DOS red teams ausentes que el usuario te sube: forense/red-team-A_auditoria-adversarial.md (RT-B, sha256 7342ffbf2a1341eb…) y forense/red_team_A_auditoria.md (RT-D, sha256 2f5dfaa50610dbb1…) — verifica hash ANTES de commitear, discordante ⇒ PARA; procedencia (proyecto/espejo, tipo (3) hasta este commit) en mensaje y nota. Y declara el hallazgo de dirección, sin tocar nada: las copias del espejo de RT-A y RT-C divergen del repo (RT-A: espejo 8bae9213… vs repo 17766f8f… · RT-C: espejo 01d47405… vs repo 12f0c872…) — el repo manda; el espejo queda documentado como divergente también aquí. Con esto, si el ADR del sello cita CAREO, ya no cita ausentes.

2.3 se reescribe (acuerdo del handoff): MOTOR-1 ya NO redacta el cierre de la Entrada 5 — E5 (otro carril) la cierra, gateado por el número del ADR. Lo que 2.3 entrega ahora: (a) la derivación de QUÉ debe citar E5 en su universo (los párrafos de ADR-50/51 tal como el sello los deja, y el veredicto sobre 57(c)); (b) hallazgo verificado por dirección: el encargo de E5 NO está en forense/encargos/ (grep -rln "Entrada 5" forense/encargos/ → vacío) — el aviso del número debe incluir "archívese E5 (A.3) antes de correr"; el paquete a mesa lo dice.

2.4 con la nuance de canon del handoff, verificada: los PRODUCTOS de Ronda 1 (siete umbrales, disposición de modelos elegibles) ya son canon vía ADR-68 (gobernanza:906,912,916) — la rúbrica de RONDA-M sale del VEREDICTO (las ocho clases, forense/RONDA1-…-veredicto-…), y el PROTOCOLO como método sigue sin sellar; cítalo con esa distinción, no con la del dossier.

Gate del commit 2 (cascada), como la adenda: grep norma_de_género ≥1 y celda obligacion ≥1 (PROC-11 fusionado). PROD-P638 y D3 NO gatean la cascada (tocan resultados/taxonomía, no la definición del ejecutable) — se declara cuál era su estado al derivar.

Commit 3 (paquete): + estado de D3 (firmada/pendiente) y el hallazgo del glosario celda-D/x/B: NO hecho (verificado — cero hits en glosario), como insumo del inciso (8) de MOTOR-2.

§5 · RONDA-M v2 — dos precisiones, mismo método

Entorno y exclusiones sin cambio (Opus, sesión nueva; no MOTOR-1; no linaje Fable). Precisión (a): suite/base al citar = 3d0d1e5, 20 FAIL · 107 WARN. Precisión (b): en su encabezado, la distinción del §4.3 — juzga con la rúbrica del veredicto (forense), sin presentar el protocolo como sellado ni como inexistente. Benchmark: sigue NO haciendo falta, misma razón.

§6 · MOTOR-2 v2 — el sello (mesa), con los incisos ajustados

ADR de ocho incisos: (1-6) M1-M6 con firma verbatim — M1 COMPLETO (banner ADR-62 + disyuntiva "antes del gate de Fase 1 o espera su veredicto") · (7) reformulado (acuerdo E5): declara que ADR-50/51 quedan reescritos por este ADR y el veredicto derivado sobre 57(c); NO cierra la Entrada 5 — obliga el AVISO del número al carril E5 (con "archívese E5 por A.3 antes de correr") y deja escrito que E5 citará este ADR en su universo · (8) opcional-nombrado: la nota de glosario celda-D/x/B (pendiente de ADR-68(g), verificado sin hacer) — el ADR la anexa o la re-nombra con dueño, pero no la deja huérfana otra vez. Precondiciones en el cuerpo: compass ×3 + RT-B/RT-D en repo (cadena A.3 cerrada, con la divergencia A/C del espejo declarada) · veredicto RONDA-M sobre la mesa · numeración derivada AL SELLAR con la receta de T15 contra el main real, sin hueco (cinco colisiones históricas — el número no se hereda de ningún documento, incluido éste).

El costo de esta versión, contado: cero reglas nuevas; una decisión nueva (D3) que el terreno impuso — con sus ranuras cableadas para que NADA espere a la firma salvo las dos líneas que la firma escribe; dos archivos rescatados del espejo con hash; y un

*(— el texto llegó truncado aquí, a mitad de frase. Se archiva tal como llegó.)*

---

## Firmas de mesa recibidas durante la ejecución de PROC-11 (13/ago/2026)

Las tres se pidieron porque el terreno las exigía y ninguna venía firmada en el texto de arriba. Verbatim:

1. **D-perímetro (`check.py`):** *«Extender a la gemela»* — el perímetro de `tests/check.py` se extiende a la regex de T19c y sus dos mensajes; mismo cambio mecánico, cero cambio de lógica de test.
2. **D-renombre:** *«Opción 1. Se renombra toda aparición que denote la CONDICIONAL medida por P7_12_7 (:245, :251, :224, y el nombre en la fila de :271); NO se toca ninguna aparición de coeficiente/generador (:87, :375, :395, :598) ni prosa histórica. Precisión sobre procedencia.yaml: sus 7 apariciones son todas del coeficiente per el mapa de PROC-10 §1 — NO-TOCAR las 7, cero renombres ahí en este acto. La pregunta del generador NO se decide aquí ni se difiere al vacío: entra con nombre a la cascada de MOTOR-1 (qué tocaría desdoblar o renombrar G5 a nivel generador/coeficiente, con archivos y contadores medidos) y mesa la firma en MOTOR-2 con esa cascada enfrente — mismo criterio de ADR-72: no se decide una reescritura estructural sin conocer su universo.»*
3. **D-cascada (denominador):** *«Cascada completa»* — toda afirmación vigente de `D`=14 se mueve a 15, con la derivación nombrada. Ejecutada por la vía del Paso 6 y no extendiendo el Paso 1; desviación y razón declaradas en `forense/notas/2026-08-13-proc-11.md` §A.3.
4. **D3:** *«Correr sin D3»* — la ranura queda cableada y vacía; contador `9 de 15`.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-13-MOTOR-COND-v2-encargos-finales.md" canon/gobernanza-v1_15.md` cita ADR-100, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-100 en canon/gobernanza-v1_15.md.

# ENCARGO ACTO PROC-10-bis — clase séptima y el `10 de 15`, con dos anexos (AJUSTES A PROD-P638 · MOTOR-1 CONSOLIDADO)

**Archivado por A.3** (`forense/encargos/convencion.md`) al ejecutar el acto **PROC-10-bis** (§1), primero de los tres que este encargo trae.

## Cabecera obligatoria (`forense/encargos/convencion.md`)

- **SHA de redacción.** El encargo no declara un SHA explícito de corte. `origin/main` real al arrancar este acto es **`560d305`** (merge PR #224, "encargos-motor-v2-consolidada"), verificado por `git fetch origin && git rev-parse origin/main` contra el HEAD local, sin divergencia.
- **Entorno asignado.** §1 (PROC-10-bis) y §3 (MOTOR-1) → **nube**, repo-only, sin red (declarado dentro del propio texto, "ARRANQUE íntegro · SIN red · REMOTO verificado"). §2 (PROD-P638) → **caja con corpus** (heredado de la tabla maestra del encargo v2 consolidada archivado en `forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md`), entorno que esta sesión no tiene.
- **Estado.**
  - **§1 · PROC-10-bis — `CONSUMIDO`.** Ejecutado 13/ago/2026 en `cloud_default`, rama `claude/proc-10-bis-clase-septima-taa5nj`. Nota: `forense/notas/2026-08-13-proc-10-bis.md`.
  - **§2 · AJUSTES A PROD-P638 — `VIVO`, no ejecutado aquí.** Los dos ajustes que el texto pide (GATE corregido; ranura D3 declarada RESUELTA) son correcciones al **cuerpo del encargo PROD-P638**, que vive archivado en `forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md` §3 — un encargo ya consumido en parte (por `PROC-11`) y por convención **no se reescribe**. Este acto **declara** los dos ajustes (ver «Advertencias» abajo) sin editar ese archivo ni ningún otro fuera de su perímetro declarado; quedan como instrucción para quien lance `PROD-P638`, mismo criterio que las «Advertencias de dirección» que `PROC-11` dejó sobre ese mismo encargo. `PROD-P638` requiere `caja con corpus`, entorno que esta sesión (`nube`, repo-only) no tiene — no ejecutable aquí aunque el perímetro lo permitiera.
  - **§3 · MOTOR-1 CONSOLIDADO — `VIVO`, PARADO por precondición incumplida.** El encargo exige verificar por hash, ANTES de cualquier commit, cinco archivos que "el lanzador sube a la sesión": `compass-1-7edaceda.md`, `compass-2-8b198c56.md`, `compass-3-d72e6a97.md`, `red-team-A_auditoria-adversarial.md`, `red_team_A_auditoria.md`. **Ninguno de los cinco llegó a esta sesión** — verificado `find . -iname "*compass*" -not -path "./.git/*"` → 0 resultados, y ningún archivo adjunto en el turno que lanzó este encargo. El propio encargo fija la regla: "discordante ⇒ PARA". Ausencia total no es un caso más laxo que discordancia — es el caso que la regla existe para atrapar. Este acto **para** en §3 sin commitear nada de MOTOR-1.
- **Bloque VERIFICACIÓN DE EXISTENCIA (A.8), contestado.**
  ```
  $ grep -c "de 15" canon/modelo-decision-v4_0.md
  6                                    # ≥1 → PR #224 fusionado (GATE cumplido)
  $ grep -cE "MEDIDO·NACIONAL|séptima clase|clase séptima" milpa/procedencia.yaml
  0                                    # esperado -- la clase no existía
  $ grep -c "norma_de_género" milpa/procedencia.yaml
  0                                    # esperado -- PROC-11 no tocó procedencia.yaml
  $ grep -in "proc-10-bis" forense/hallazgos.md forense/notas/*.md | wc -l
  9                                    # todas "nombrado, no ejecutado aquí" -- verificado por lectura,
                                        # no es evidencia de una corrida previa de este acto
  $ ls data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml
  (existe)                             # GATE de PROD-P638 satisfecho (celda de PROC-11)
  $ grep -cE "MEDIDO·NACIONAL" milpa/procedencia.yaml   # (tras Commit 1 de este acto)
  1                                    # ≥1 → PROC-10-bis fusionado (dentro de esta misma rama)
  $ find . -iname "*compass*" -not -path "./.git/*" | wc -l
  0                                    # los 5 archivos de MOTOR-1 nunca llegaron a la sesión -- PARA
  $ ls forense/ | grep -c "RONDA-M\|CASCADA-M1"
  0                                    # nada de RONDA-M/MOTOR-1 corrió antes
  $ ls forense/red-team-A_auditoria-adversarial.md forense/red_team_A_auditoria.md 2>/dev/null | wc -l
  0
  ```

## Texto completo del encargo, verbatim tal como se lanzó

> §1 · ENCARGO ACTO PROC-10-bis — ejecuta ADR-79(a)+(h): la clase séptima y el `10 de 15` (nube · repo-only · dos commits + A.3)
> Qué es. El sucesor que ADR-79 nombra por rótulo: escribe en `milpa/procedencia.yaml` la clase que la firma D-A autorizó verbatim ("crear una clase séptima para marginales medidas sin eje") y mueve el contador per el linkage D-H ("el ajuste del contador ocurre en el mismo acto que crea la clase"). Aritmética sellada que gobierna, no se re-decide: PROC-10 §5.3 ("si (A), el titular habría sido 10 de 14, nunca 10 de 15") + PROC-11 §5 ("10 tras la primera, 11 tras PROD-P638") ⇒ este acto escribe UNA entrada (`norma_de_género`) → `10 de 15`; la de `obligación_medida` la escribe PROD-P638 con su expediente en mano.
> ════ ARRANQUE íntegro (v2.8) · SIN red · REMOTO verificado ════ Verificación de existencia (A.8):
> ```bash
> set -u; cd "$(git rev-parse --show-toplevel)"; git fetch -q origin
> grep -c "de 15" canon/modelo-decision-v4_0.md                        # ≥1 = #224 fusionado (GATE); 0 = ESPERA
> grep -cE "MEDIDO·NACIONAL|séptima clase|clase séptima" milpa/procedencia.yaml   # 0 = la clase NO existe (esperado); ≥1 = YA HECHO, PARA
> grep -c "norma_de_género" milpa/procedencia.yaml                     # 0 esperado (PROC-11 no tocó procedencia); ≥1 = PARA y reporta
> grep -in "proc-10-bis" forense/hallazgos.md forense/notas/*.md | wc -l   # 0 = no corrió
> ```
> PERÍMETRO. ESCRIBE: `milpa/procedencia.yaml` (header de clases + UNA entrada) · `canon/modelo-decision-v4_0.md` SOLO: los sitios del numerador (`9→10 de 15`, los seis re-derivados) + la fila de Paso 5 y el rótulo de `:271` que PROC-11 dejó "nombrando D3" (se reescriben citando ADR-79(a), ya sin condicional pendiente) · `README.md` y `estado-programa` (numerador) · nota · A.3 · hallazgos (union). NO ESCRIBE: `tests/` (T19b/T19c derivan el numerador de `procedencia` — se mueven solos) · `gobernanza` · celdas-d · expedientes. Fuera de la lista, PARA. Concurrencia: NO junto a PROD-P638 ni a ninguna ranura (mismo `procedencia`); SÍ con MOTOR-1(c1)/RONDA-M.
> Commit 1 — la clase y la entrada, congeladas. (a) Definición de la clase, en el header de `procedencia.yaml`, mismo formato que las seis vigentes. Nombre fijado por este encargo: `MEDIDO·NACIONAL` — descriptivo del hecho (marginal medida sobre población nacional del instrumento, sin eje condicionante), coherente con la familia `MEDIDO·*`; ADR-79(a) autorizó la clase y delegó la escritura al sucesor sin fijar rótulo — si mesa objeta el nombre es un rename de una línea, no una re-decisión. La definición incluye, verbatim como cláusulas: qué la distingue de `MEDIDO·PARCIAL(x)` (x=∅ declarado, no omitido), y que no habilita segmentación: quien necesite la condicional POR eje corre la medición condicionada (la puerta D3-B queda nombrada dentro de la definición, con dueño "acto futuro por θ"). (b) La entrada de `norma_de_género`: clase `MEDIDO·NACIONAL` · θ 0.6933, IC95 [0.6725, 0.7140], n=5,579 · fuente ENASIC 2022 `P7_12_7`/`TPER_ELE`, expediente `ESP-OPACA-B-d13ec4fe`, `PROD-cca3ea0…` · el límite de constructo de ADR-75(a) VERBATIM en la entrada (norma de deber de cuidado diferenciada por sexo, no obligación genérica) · `antes:` la fila de proxy-ENUT obsoleta, citada como historia. (c) El texto nuevo de la fila de Paso 5 y de `:271` (plantilla: la que PROC-11 §3.5 congeló "nombrando D3", ahora resuelta). Frase de siempre.
> Commit 2 — ejecución y cierre: los edits exactos → suite cruda antes/después (`T19b`/`T19c` deben derivar 10 y quedar `[ ok ]` — es el criterio de cierre; si truena, hallazgo, no maquillaje) → contador declarado: `10 de 15`, con la línea "la oncena entra con PROD-P638".
>
> §2 · AJUSTES A PROD-P638 (dos, quirúrgicos — el cuerpo de la v2 sigue vigente)
>
> 1. GATE corregido (el hueco 6.1 de PROC-11: el predicado viejo siempre pasaba):
> ```bash
> ls data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml   # existe = #224 fusionado
> grep -cE "MEDIDO·NACIONAL" milpa/procedencia.yaml                       # ≥1 = PROC-10-bis fusionado (la clase que tu entrada usa)
> ```
> 2. La ranura D3 queda RESUELTA: con la clase en el árbol, el paso de `procedencia` deja de ser condicional — al REPRODUCIR, además del expediente/fila-12/celda-`LISTO`, escribe la entrada de `obligación_medida` con clase `MEDIDO·NACIONAL` (distribución 5-categorías; la de interés 0.0765 [0.0661, 0.0868] "obligación"; universo `TPOB_CUI`; el "no-comparar contra la hermana" verbatim) → contador `11 de 15`. Al NO-reproducir: todo el bloque de procedencia se abstiene, patrón PROC-10, y a mesa.
>
> §3 · MOTOR-1 CONSOLIDADO — cuerpo autocontenido (resuelve el hallazgo del A.3 de #224: "el encargo original no está en el directorio")
> Este §3 ES el encargo completo de MOTOR-1 — sustituye a "cuerpo original + deltas". El lanzador sube a la sesión CINCO archivos, verificables por hash ANTES de cualquier commit (discordante ⇒ PARA): `compass-1-7edaceda.md` `5408aacc7c6e1ce0…` · `compass-2-8b198c56.md` `66ba8a6aa878b1b7…` · `compass-3-d72e6a97.md` `71ce41d244adfb29…` · `red-team-A_auditoria-adversarial.md` (RT-B) `7342ffbf2a1341eb…` · `red_team_A_auditoria.md` (RT-D) `2f5dfaa50610dbb1…`.
> ════ ARRANQUE íntegro (v2.8) · nube, SIN red · REMOTO verificado ════ Existencia (A.8): `find . -iname "*compass*" -not -path "./.git/*" | wc -l` (0 esperado; ≥1 = reporta y salta esos) · `ls forense/ | grep -c "RONDA-M\|CASCADA-M1"` (0 = nada corrió) · `ls forense/red-team-A_auditoria-adversarial.md forense/red_team_A_auditoria.md 2>/dev/null | wc -l` (0 esperado). PERÍMETRO. ESCRIBE: los cinco archivos de arriba bajo `forense/` (verbatim, cero ediciones) · `forense/CASCADA-M1-<fecha>.md` · su nota · A.3 (este §3 verbatim, primer commit) · hallazgos (union). NO ESCRIBE: `canon/` · `milpa/` · `data/` · `propuesta-motor-matriz-v0_2.md` salvo pedido de mesa (hoy NO) · el registro de recálculo (lo LEE). Fuera de la lista, PARA.
> COMMIT 1 (inmediato — no espera nada):
> 1. Cifras del dossier, con comando: scripts del curador (`ls tools/curador_registro/*.py | wc -l` — dirección midió 19; reporta el tuyo) · "22 g.l." citado por `modelo-decision-v4_0.md:628` ("ADR-51: 7 + 15") con la línea verificada.
> 2. Los cinco archivos, commiteados verbatim con procedencia en mensaje y nota ("proyecto/espejo, tipo (3) hasta este commit; hash verificado contra la extracción de dirección del 13/ago"). Y el hallazgo declarado, sin tocar nada: las copias del espejo de RT-A/RT-C divergen del repo (`RT-A espejo 8bae9213… vs repo 17766f8f…` · `RT-C espejo 01d47405… vs repo 12f0c872…`) — el repo manda. Con esto la cadena A.3 de CAREO queda cerrada para el sello.
> 3. Entrada 5 / E5 (acuerdo del handoff + ADR-79(c)): MOTOR-1 NO redacta su cierre — deriva (a) qué debe citar E5 en su universo (los párrafos de ADR-50/51 como el sello los deje + el veredicto sobre 57(c), derivado leyendo `gobernanza:619-627` contra matriz §1.4: ¿la compuerta de llaves depende de la forma matricial? `CAMBIA` o `SIN CAMBIO` con argumento — es el insumo del inciso (7) de MOTOR-2); (b) el hallazgo verificado: el encargo de E5 NO está en `forense/encargos/` — el aviso del número del ADR incluye "archívese E5 (A.3) antes de correr".
> 4. Rúbrica Ronda (una página) extraída del VEREDICTO (`forense/RONDA1-…-veredicto-…`: las ocho clases), con la distinción canon verificada: los PRODUCTOS de Ronda 1 ya son canon vía ADR-68 (`gobernanza:906,912,916`); el protocolo como método, no. Frase de siempre.
>
> COMMIT 2 — LA CASCADA (auto-gateado por comando, predicados CORREGIDOS):
> ```bash
> git fetch -q origin && git merge origin/main 2>/dev/null
> grep -c "norma_de_género" canon/modelo-decision-v4_0.md                       # ≥1 (#224)
> ls data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml          # existe (#224)
> grep -cE "MEDIDO·NACIONAL" milpa/procedencia.yaml                              # ≥1 (PROC-10-bis) — la cascada se deriva sobre la taxonomía FINAL
> # 0 en cualquiera = ESPERA; el estado de PROD-P638 se declara, no gatea
> ```
> `forense/CASCADA-M1-<fecha>.md`, por pieza, qué-cambia-a-qué-y-qué-contador: banner ADR-62 (`milpa-spec:4-6` — el sello lo resuelve o reescribe; renombre a v0_3 decidido) · gate Fase 1 de `milpa-plan` (la disyuntiva DENTRO de M1) · sitios del ejecutable en `modelo` (22 g.l. `:260,:628`: cambian de forma, no de número) · `procedencia.yaml` post-bis · titular `4 de 144` (`estado:97`/`modelo:17`, congelado 31/jul): veredicto DERIVADO de si M1 lo descongela · `README:36-38`/T15/T19b-c · bloque AJUSTE `gobernanza:461-465` + el catálogo de momentos que M4 CONSTITUYE (archivo nuevo, roles AJUSTE/HOLDOUT en su commit 1) · la pregunta del generador (PROC-11 la mandó aquí con nombre): qué tocaría desdoblar/renombrar G5 a nivel generador/coeficiente, archivos y contadores medidos — mesa la firma en MOTOR-2 con esta cascada enfrente. Cada M1-M6 cierra con su cascada en ≤3 líneas. Cero ediciones: solo el mapa.
> COMMIT 3 — el paquete a mesa: las seis M (M1 COMPLETO: banner + "antes del gate o espera su veredicto") con cascada al lado · el inciso (7) listo (declara+notifica, NO cierra — E5 cierra citando el ADR) · inciso (8) glosario celda-D/x/B (verificado sin hacer) · estado de RONDA-M por comando (`ls forense/ | grep RONDA-M` — si fusionó se incorpora línea-por-defecto; si no, EN-VUELO y MOTOR-2 no se firma sin él) · estado de PROC-10-bis/PROD-P638 declarado. Contador: 0 — es preparación, y lo dice.

## Advertencias de dirección para los actos que siguen `VIVO`

Levantadas al ejecutar PROC-10-bis (§1), sin editar el texto del encargo (arriba va verbatim):

1. **§2 (PROD-P638), ajuste 1 (GATE corregido) — adoptado formalmente, no aplicado a ningún archivo.** El predicado nuevo (`ls .../G5.obligacion_medida.conducta.yaml` / `grep -c obligacion_medida`) reemplaza al viejo `grep -c obligacion`, que PROC-11 §6.1 ya había encontrado roto (siempre pasa). Este acto verifica que el predicado nuevo también da lo esperado hoy: `ls data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml` existe, `grep -cE "MEDIDO·NACIONAL" milpa/procedencia.yaml` da `1` (tras Commit 1 de este acto) — el gate de PROD-P638, con el predicado corregido, está satisfecho.
2. **§2 (PROD-P638), ajuste 2 (ranura D3 resuelta) — la premisa que lo activa ya se cumple tras este acto.** La clase `MEDIDO·NACIONAL` existe en `milpa/procedencia.yaml` desde el Commit 1 de este acto. Cuando `PROD-P638` corra (entorno `caja con corpus`, no disponible en esta sesión `nube`), la ranura D3 de su propio encargo ya no es condicional — reproduce y escribe la entrada de `obligación_medida` bajo `MEDIDO·NACIONAL`, numerador a `11 de 15`.
3. **§3 (MOTOR-1) sigue bloqueado por la misma razón que el A.3 de #224 ya declaró.** Los cinco archivos *compass*/red-team no llegaron a esta sesión tampoco. Cero commits de MOTOR-1 en este acto. El hallazgo de PROC-11 §6.1 sobre el predicado `grep -c obligacion` roto en el gate de la cascada del commit 2 de MOTOR-1 (§4 del encargo v2 original) sigue vigente y sin corregir — MOTOR-1, cuando corra, debe usar `grep -c obligacion_medida` ahí también.
4. **Hallazgo nuevo de este acto, para quien corrija `tests/check.py` en el futuro:** `T19b`/`T19c` derivan el numerador contando la subcadena literal `'clase: "MEDIDO·PARCIAL'` — no reconocen `MEDIDO·NACIONAL`. Tras este acto, ese conteo sigue en `9`, no `10`; la suite queda ROJA (`T19b`, `T19c`, y `T16` en cascada). Ver `forense/notas/2026-08-13-proc-10-bis.md` §4 y `forense/hallazgos.md`, entrada del 13/ago/2026.

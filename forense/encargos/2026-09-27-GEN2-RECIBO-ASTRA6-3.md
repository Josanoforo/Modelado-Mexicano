# ENCARGO · ACTO GEN2-RECIBO-ASTRA6-3 · Recibo de Codex en dos modos a la vez: post-merge de los siete PR que entraron sin recibo después de RECIBO-ASTRA6-2 (#1221, #1222, #1226, #1229, #1232, #1237, #1243) y **pre-merge** de los tres PR abiertos de tanda 5 (ramas `codex/astra6-c1-ejecutor-v3-1`, `codex/astra6-c3-autoridad-civismo-comunalidad-1`, `codex/astra6-c3-salud-juventud-tiempo-1`), que mesa no fusiona hasta que su `pr-N.md` exista con veredicto

> ENTORNO: **NUBE** — lee `origin/main` y las tres ramas de Codex; RESULT sellados, paquetes, hojas de firma. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.
> Instancia de `forense/encargos/2026-09-26-GEN2-RECIBO-ASTRA6-N.md`: hereda sus criterios comunes y de carril; lo que RECIBO-ASTRA6-2 fijó como método (nota principal y `tools/recibo/`) se reúsa, no se reinventa.

CABECERA · SHA de redacción `3ac3ab7d` (re-deriva al abrir; las ramas de Codex se mueven: cita el commit que recibes) · una sesión, rama propia (varias si separas lotes, declaradas) · MODELO: **Opus** (C1 y C2 no bajan) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0 `3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica.
CONTADOR: cero mediciones; no adopta. Puede añadir filas a `data/corrida0/validaciones-independientes.tsv` (declarado).

## 1 · OBJETIVO
(P1) **Post-merge, siete PR.** Vocabulario de ASTRA6-1/2: `RECIBIDO-POST-MERGE` · `RECIBIDO-POST-MERGE-CON-NC` · `PROPONER-REVERTIR`. Primera pregunta por PR: `git diff --name-only <merge>^1..<merge>` contra sellos, catálogo, `decisiones.tsv`, `milpa/`, vistas, `verify.yml`, `check.py`. Carriles: **C1** #1221 (aislamiento-v2: la ceguera nueva; criterio C1 completo), #1229 (entradas residuales) · **C2** #1222 (ENOE inferencia: sin retadores sobre olas vistas; olas reservadas intactas) · **C3** #1243 (interacción/emociones/humor/sanción) · **archivo/tubería** #1226 (`codex/adq-…`: 5 archivos, 103+/10−; verificar qué tocó y si cambia qué se verifica), #1232 (revisión tanda 4), #1237 (archivo tanda 5).
(P2) **Pre-merge, tres PR abiertos.** Por rama, contra `origin/main` al momento del recibo: **C1** `c1-ejecutor-v3-1` (PR #1241 según su último commit; 14 archivos; es el ejecutor aislado de caja: criterio C1 y la pregunta de si algún recálculo se hizo sin paquete archivado antes) · **C3** `c3-autoridad-civismo-comunalidad-1` (37 archivos) y `c3-salud-juventud-tiempo-1` (PR #1242; 32 archivos). Vocabulario pre-merge de la plantilla N: `RECIBIDO` · `RECIBIDO-CON-NC` · `NO-RECIBIDO (qué falta)`. Si mesa fusiona antes de que exista el `pr-N.md`, el veredicto pasa a post-merge y se dice en la primera línea.
(P3) **FP nuevas de estos diez PR**: listar por id, dictaminar con el vocabulario de ASTRA6-2 P2 (`RECOMENDAR-FIRMAR-TAL-CUAL` · `-CON-CAMBIO` · `RECOMENDAR-NO-FIRMAR` · `YA-CUBIERTA-POR`) y sumarlas a **una** hoja `forense/analisis/recibo-astra6-3/hoja-para-mesa.md`, que FIRMAS-21 asienta junto con la de ASTRA6-2.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: 10 notas `pr-N.md` (7 post + 3 pre) con tabla criterio × veredicto · `grep -c PROPONER-REVERTIR` = 0 o lista exacta en la nota principal · hoja de P3 con un dictamen por FP nueva · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
MISION-ASTRA-6 + ADENDA-1 · R(a) FIRMAS-15 y **FIRMAS-20 D (recibo obligatorio antes de fusionar)**: los siete de P1 lo incumplen y el recibo lo dice en su primera línea sin más comentario; los tres de P2 son la primera oportunidad de cumplirlo desde el 26/sep · regla 6 (sin retadores sobre olas vistas) · E.2, E.6, D-22 · firma de mesa 27/sep sobre las 15 FP de Codex (ADENDA-1 de ASTRA6-2): lo que ya está firmado ahí es `YA-CUBIERTA-POR` aquí.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `3ac3ab7d` · notas de recibo existentes (`forense/notas/**/pr-N.md`): 1, 1166, 1170–1174, 1180, 1194–1197, 1199, 1200, 1202, 1203, 1205, 1214. PR de Codex fusionados **sin** nota desde #1214: #1221 `astra6-c1-aislamiento-v2`, #1222 `astra6-c2-enoe-inferencia-1`, #1226 `adq-2026-09-27`, #1229 `astra6-c1-entradas-residuales-1`, #1232 `astra6-tanda4-revision-1`, #1237 `astra6-tanda5-archivo-20260927`, #1243 `astra6-c3-interaccion-emociones-humor-sancion-1`.
- [EJECUTADO] `git diff --name-only origin/main...origin/<rama>` en las tres ramas abiertas: rutas sensibles (sellos, catálogo, `decisiones.tsv`, `milpa/`, `verify.yml`, `check.py`) = **0** en las tres. Es un barrido, no el recibo.
- [EJECUTADO] `forense/analisis/recibo-astra6-2/hoja-para-mesa-recibo-astra6-2.md` existe; veredictos de ASTRA6-2: 4 `RECIBIDO-POST-MERGE`, 9 `RECIBIDO-POST-MERGE-CON-NC`, 0 revertir. Su método y `tools/recibo/` son el punto de partida.
- [LEÍDO] `forense/encargos/fuentes/ASTRA6-tanda5-20260927/`: 01 C1-EJECUTOR-AISLADO-3 (caja), 02 C3 autoridad/civismo/comunalidad, 03 C3 salud/juventud/tiempo, 04 C3 interacción/emociones/humor/sanción, 05 revisión solo PR propios. Codex lanzó los cuatro; #1243 ya fusionó.
- [REPORTADO] Commits de las ramas abiertas dicen «registra PR 1241 en cierre y recibo» y «cierra encargo y recibo del PR 1242»: el recibo de Codex (`recibo-para-claude.md`) **no sustituye** al de Claude (regla 7 del transfer del 26/sep).

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'RECIBO-ASTRA6-3'` → 0. Consumidos: RECIBO-ASTRA6-N (plantilla), -1, -2. En vuelo: MAPA-INSTRUMENTOS-ALTERNOS-1 y OBTENCION-EXTERNA-1 (caja; `canon/mapa-…`, `data/manifiesto.yaml`: no se tocan aquí) · Codex sigue abriendo PR: los que abran después de tu 0-bis van al `-4`, no aquí.

## 5 · PIEZAS
P2 primero (desbloquea a mesa), luego P1, luego P3. Lotes D-11 de hasta cuatro PR por PR de recibo. Rama prevista: si una rama de Codex se mueve mientras la recibes, recibes el commit que citas y lo dices; si mesa fusiona a mitad, cambias el modo de esa nota y sigues.

## 6 · LATITUD
Orden, lotes, cuántos PR: tuyos. PREGUNTA A MESA prevista: ninguna (hoja de P3). NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato reservado · b) editar lo de Astra, un sello, una fila FIRMADA · c) adoptar; `PASA` sin compuerta de tolerancia · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«El recibo lee; no corrige» protege **borrar** · «Sin paquete archivado antes de la sesión no es validación ciega» protege **adoptar** · «Ninguna ola reservada en C2» protege **abrir dato** · «Recomendar a mesa solo con razón escrita» protege **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/notas/<acto>/` (10 `pr-N.md` + principal), `forense/analisis/recibo-astra6-3/`, `tools/recibo/` (reutilizable), `data/corrida0/validaciones-independientes.tsv` (append), TSV de gobierno (append), L0, cascada. Ajeno: `canon/`, `milpa/`, sellos, las ramas de Codex (se leen, no se editan), `firmas-pendientes.tsv` fuera del append. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No fusiona, no revierte (propone), no adopta, no recibe PR abiertos después de su 0-bis (`-4`). Sucesores: RECIBO-ASTRA6-4; FIRMAS-21 (hojas de ASTRA6-2 y -3). Sin módulo de auditoría propio. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-27-GEN2-RECIBO-ASTRA6-3-ADENDA-N.md`, selladas al recibirse.

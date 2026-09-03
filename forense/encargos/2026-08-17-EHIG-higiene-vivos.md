# ENCARGO E-HIG · HIGIENE-VIVOS — reconciliar el estado de los encargos archivados contra el árbol

- **SHA de redacción:** `f3873c2` (`origin/main`, verificado contra el clon de esta sesión al arrancar — `git log -1 --format="%h %s"` coincide exacto, `git status` limpio, `git diff f3873c2 HEAD --stat` vacío).
- **Entorno asignado:** NUBE. **NO** en la caja de Codex. Sin gate, sin ADR (clase "higiene de registro", precedente ACTO C: "sin gate ni ADR").
- **Estado:** CONSUMIDO — ACTO E-HIG/HIGIENE-VIVOS, `PR #243` (`4c9da5b`, 20 archivos), 17/ago/2026. *(Rótulo puesto por ACTO CONF-07-CIERRE, 18/ago/2026: el propio encargo pedía "marcar `CONSUMIDO` con el PR que fusione este acto" y el acto que fusionó nunca volvió a hacerlo — el vigía no lo ve porque el defecto está en la línea que el vigía usa como fuente. Evidencia: `git merge-base --is-ancestor a9fc0a7 origin/main` → cierto; `7740015` "Commit 2: aplica los 17 veredictos"; y el entregable `forense/notas/2026-08-17-higiene-vivos.md` existe en el árbol.)* Historia previa: Commit 1 (criterios congelados: `forense/notas/2026-08-17-higiene-vivos.md`) y Commit 2 (los 17 veredictos, aplicados a las cabeceras de `Estado` de cada archivo del ANEXO) ejecutados en esta rama. Marcar `CONSUMIDO` con el PR que fusione este acto — **JAMÁS auto-fusión**.

---

## Bloque VERIFICACIÓN DE EXISTENCIA — contestada por dirección, 2026-08-17, contra `f3873c2`

1 · ESTRUCTURA. Gobierna `forense/encargos/convencion.md` (leída): ciclo de vida VIVO → CONSUMIDO con el PR que lo ejecutó; un encargo consumido NO se borra. Ninguna tabla de `data/` gobierna aquí.
2 · CONTENIDO. Derivado hoy (bucle sobre `grep -m1 "Estado"` en `forense/encargos/*.md`, filtrando CONSUMIDO/SUPERADO): **17 candidatos** con Estado no-consumido, pegados abajo como ANEXO. La clase de defecto EXISTE y ya se corrigió antes: `forense/notas/2026-08-13-e2-cierre.md` §5 corrigió tres `VIVO` falsos (p.ej. `VP-verifica-puertas` → `CONSUMIDO — PR #205`).
3 · COBERTURA RETROACTIVA. `convencion.md` nació 2026-08-05 (`829f927`); el candidato más viejo (m5bis) es del mismo día — todos los candidatos nacieron bajo la convención, sin brecha.

---

## Texto del encargo, verbatim tal como se recibió

PERÍMETRO Y CONCURRENCIA. Este acto toca EXACTAMENTE: las líneas de cabecera de Estado (+una línea de evidencia) de los archivos del ANEXO · `forense/hallazgos.md` (una entrada, union solo en merge local) · `forense/notas/<fecha>-higiene-vivos.md` · `forense/encargos/<fecha>-EHIG-higiene-vivos.md` (A.3). NO edita el cuerpo de ningún encargo. "Si te encuentras escribiendo fuera de esta lista, PARA."

**Concurrencia declarada por el encargo:** BARRIDO-2 (Codex) y E-A10 corren en paralelo. PROHIBIDO tocar la lista de colisión de BARRIDO-2 (`data/**`, `tools/curador_registro/**`) y PROHIBIDO tocar: `forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo*.md` (Codex escribe ahí el SUPERADO de M-APERTURA §6) · cualquier archivo `*BARRIDO-2*` · los encargos de esta tanda (E-A10/E-HIG/E-RUTA).

### Cuerpo

**Commit 1 — criterios congelados ANTES de adjudicar** (en la nota):
(i) la lista de candidatos = el ANEXO, cerrada; (ii) vocabulario, sin inventos: `CONSUMIDO — PR #N` (exige merge verificado: `git log`/`merge-base --is-ancestor` + correspondencia acto↔encargo leída, no supuesta) · `SUPERADO POR <acto> · decisión de mesa <fecha>` (exige cita textual de la decisión; único precedente utilizable hoy: las decisiones del encargo BARRIDO-2) · `VIVO` se queda `VIVO` anotando razón + gate vigente (los gateados por la ley de mesa —todo lo que calcule: E4a, E4b, E4c-commit4, B-estimador-contraste, r5-1-d3, BE-benchmark— NO se consumen: se anotan "VIVO — gateado por ley de mesa hasta cierre de BARRIDO-2" con su gate propio si además lo tienen); (iii) NADA se marca por memoria, espejo o transfer: cada veredicto lleva su comando; (iv) la frase: "el primer resultado que produzca este procedimiento es el que se reporta".

**Commit 2 — aplicación.** Un veredicto por archivo del ANEXO con su evidencia en una línea. Casos que la dirección ya huele CONSUMIDO pero que TÚ debes ganar por comando, no heredar: `censo-v1_1` (¿PR #198?), `enlace1-mapeo` (ENLACE-1 fusionado), `encargo-c-capa3-reconcilia` (¿PR #202?), `RECONCILIA-SPEC` (¿PR #238?), `MOTOR-COND-v2` y `PROC-10-BIS` (cabecera "Estado." ambigua — repárala con el estado real). Entrada única en hallazgos con el conteo final (N consumidos, N supersedidos, N vivos con razón).

**Suite** VERDE (`tests/check.py --baseline`; ojo T02: no renombres archivos) · `git diff --check`.

**Contadores del programa: 0.** **Cierre:** PR, reporte corto, JAMÁS auto-fusión.

### ANEXO — los 17 candidatos (derivados 2026-08-17 contra f3873c2)

2026-08-05-m5bis-cierre-inventarios-catalogo-cruce · 2026-08-11-A-renglon-llaves · 2026-08-11-E4b · 2026-08-12-B-estimador-contraste · 2026-08-12-C-universo-minimo · 2026-08-12-sonda1-mapa-barreras-lote2 · 2026-08-12-veredicto-pr185-mapeo-universo-map-b (§2/MAP-A) · 2026-08-13-BE-benchmark-enlace-invarianza · 2026-08-13-ENASIC-SPLIT · 2026-08-13-MOTOR-COND-v2-encargos-finales · 2026-08-13-PROC-10-BIS-clase-septima · 2026-08-13-RP-reconcilia-puertas · 2026-08-13-censo-v1_1 · 2026-08-13-encargo-c-capa3-reconcilia · 2026-08-13-enlace1-mapeo-id-manifiesto · 2026-08-13-r5-1-d3 · 2026-08-14-RECONCILIA-SPEC-encargo.

---

## Cierre — lo que este acto entregó

Qué cambió: cabeceras de `Estado` de los 17 archivos del ANEXO, corregidas contra el árbol real (`f3873c2`), no contra memoria ni contra la clasificación de partida del propio encargo. Por qué importa: 13 de 17 estaban ya fusionados y seguían apareciendo como candidatos activos a un futuro auditor — incluidos tres que el propio encargo presumía bloqueados por una ley de mesa que nunca les aplicó. Qué habilita: el ANEXO queda resuelto; un futuro `grep -m1 "Estado"` sobre estos 17 ya no los vuelve a listar (salvo `m5bis` y `r5-1-d3`, que siguen `VIVO` con razón vigente, y los dos mixtos, que quedan desglosados por sección). Qué falta: `MOTOR-2` (dentro de `MOTOR-COND-v2` §6) sigue sin sellar — no es defecto de registro, es que mesa no ha firmado; `R5.1-D3` sigue sin ejecutarse — gateado por BARRIDO-2. Pruebas: `python3 tests/check.py --baseline` y `git diff --check`, salida cruda en el cierre del PR. Reservas: sin decisión de BARRIDO-2 archivada todavía, ningún veredicto de este acto usó `SUPERADO POR` — si BARRIDO-2 archiva una decisión que reclasifica alguno de los 17, ese archivo se corrige en un acto aparte, no aquí. **Contadores sustantivos movidos: 0, explícito.**

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-17-EHIG-higiene-vivos.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-17-cierra.md, forense/notas/2026-08-17-higiene-vivos.md, forense/notas/2026-08-18-sello-conf07-y-rotulos.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.

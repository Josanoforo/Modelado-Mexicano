# ENCARGO · ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-3 · Los diez RESULT pendientes entran al consumidor vivo del motor, `milpa/tramite.yaml`, escritos solo por el escritor, un RESULT por regla existente, con diff seco y merge de mesa: `pendientes_adopcion` baja a cero por primera vez

> ENTORNO: **NUBE** — RESULT sellados y el escritor; cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `3d138c66` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-adopcion-bloque-y-pines-3` (o la que la plataforma fije: se declara en el 0-bis, D-19) · MODELO: Opus · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones. Mueve por derivación: `N_resultados_gen2_pendientes_adopcion` 10 → 0 y `N_resultados_gen2_adoptados_activos` +10 (medidos en rama con `status`; en `main` cuando el canal publique). Escribir en `milpa/tramite.yaml` **es** la adopción (E.2): este PR lo fusiona mesa, nunca el auto-merge.

## 1 · OBJETIVO
Hallazgo 1 de ADOPCION-1 y W de ADOPCION-2: los diez RESULT (`RESULT-BANXICO-2024-*` ×5, `RESULT-CTX-2019-P-ALTO`, `RESULT-CTX-2023-P-ALTO`, `RESULT-MOTRAL15-*` ×3) ya están citados en `milpa/tramite-ola5-propuesta-v0.yaml`, que el motor **no carga**; solo cuentan como adoptados cuando la regla que los cita vive en `milpa/tramite.yaml`. Este acto extiende el escritor (`tools/escribe_relevo_consumo.py`, hoy solo RES-0028) para escribir en `tramite.yaml` la etiqueta `corrida0_resultado_id`/`corrida0_generacion` en la regla existente que corresponde a cada RESULT, y lo aplica.
«Hecho» sobre el commit final con origin/main fusionado: `git diff` de `milpa/tramite.yaml` = solo las diez etiquetas (ni un valor numérico cambia: la regla ya tenía su `p`; si el `p` de la regla no coincide con el RESULT, esa regla **no se etiqueta** y va a NC) · diff seco pegado en la nota antes del `--apply` · test por RESULT (`tests/test_escribe_relevo_consumo.py` extendido) · `status` en rama: `pendientes_adopcion` 0 · `T-REPRO` VERDE · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA — dadas («firmado», 24/sep/2026), verbatim
- **Decisión 2 de ADOPCION-2 (W):** «Los diez RESULT pendientes se adoptan escribiendo en milpa/tramite.yaml, solo por el escritor de consumo, un RESULT por regla existente, con diff seco en la nota; el PR lo fusiona mesa.» (cierra `FP-…-e0db-02`, `NC-…-FIRMAS-7-369b-01`, `NC-…-ADOPCION-1-ec71-01`)
- **Bloque de diez (FIRMAS-7, 21/sep, `…369b-01`):** ya ADOPTADOS por firma; faltaba el acto con `milpa/tramite.yaml` en perímetro. Este es.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` Cierre de ADOPCION-2: W «premisa falsa: el motor no carga la propuesta ola 5; el contador solo baja si entran a milpa/tramite.yaml». Cierre de ADOPCION-1 l.90-104: los diez ids, verificados con `_resultados_citados_en`.
- `[LEÍDO]` `tools/escribe_relevo_consumo.py` docstring: V1 solo RES-0028; escribe etiqueta en regla existente; no firma pines; el merge de mesa materializa la adopción. Precedente: #1080 (auditado LIMPIO por AUDITORIA-POST-HOC: «no a mano; con herramienta y test»).
- `[SUPUESTO]` que cada uno de los diez RESULT tiene una regla en `tramite.yaml` cuyo `p` es exactamente el valor del RESULT (fue el criterio para citarlos en la propuesta). **Se verifica por comando antes del diff seco**; una regla con `p` distinto = NC `NO-CONSTRUIBLE-SIN-DECISION` (cambiar un `p` es otra firma).
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c 'RESULT-BANXICO-2024\|RESULT-CTX-20\|RESULT-MOTRAL15' milpa/tramite.yaml` → reporta (esperado 0). `git ls-remote --heads origin | grep -i 'adopcion'` → reporta (ADOPCION-2 en `claude/new-session-uq2blk` hasta que mesa fusione; no comparte archivos con este acto salvo TSV de gobierno: union).

## 5 · PIEZAS
P1 · Tabla RESULT → regla de `tramite.yaml` (llave, `p` actual, valor del RESULT, ¿coincide?). P2 · Escritor extendido a `tramite.yaml` (mismo contrato que RES-0028: solo etiqueta; nunca valor). P3 · Diff seco → nota → `--apply` → test por RESULT → `status`. P4 · Cierre de NC/FP citadas.

## 6 · LATITUD
Orden y forma del test: tuyos. ≤ 10 líneas adyacentes: sí. Pregunta a mesa (sigues con las que coincidan): una regla cuyo `p` no coincide con su RESULT — con el par de valores y recomendación (regla de oro §2: el RESULT manda; cambiar el `p` es adopción de otro valor y necesita firma propia).

## 7 · PAROS — lista cerrada
a) no aplica · b) editar `tramite.yaml` a mano, cambiar un `p`, tocar un sello · c) etiquetar una regla cuyo `p` no coincida; mover contadores a mano · d) no aplica · e) CAJA · f) los diez ya están etiquetados en `tramite.yaml`.

## 8 · COMPUERTAS
«Solo etiquetas; ningún valor cambia; diff seco antes de aplicar» protege: **adoptar / congelar**. «Merge de mesa, no auto-merge» protege: **adoptar** (E.2).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `milpa/tramite.yaml` (solo vía escritor, solo etiquetas), `tools/escribe_relevo_consumo.py` + `tests/test_escribe_relevo_consumo.py`, `no-corrido.tsv`/`firmas-pendientes.tsv`, nota, L0, cascada. Ajeno: `milpa/tramite-ola5-propuesta-v0.yaml`, `decisiones.tsv`, catálogo, procedencia (CATALOGO-CONTRATO-Y-TEST-1), CALC. En vuelo: ADOPCION-2 (PR pendiente), CATALOGO-CONTRATO-Y-TEST-1 (no toca `tramite.yaml`), VISTA-NORMALIZADA-2.

## 10 · LO QUE NO HACE · SUCESORES
No cambia valores, no releva legacy del motor (34) más allá de estas diez etiquetas si coinciden con lecturas legacy (si una etiqueta releva una lectura legacy, se declara y `legacy_activas_por_consumidor__motor` baja: se reporta). Sucesor: `-4` para reglas con `p` discordante, con la firma que mesa dé.

## NO-CORRIDO / RESERVAS

- **qué:** P1-P3 — «los diez RESULT pendientes entran al consumidor vivo del motor, milpa/tramite.yaml, escritos solo por el escritor, un RESULT por regla existente» · **por qué:** PARO-PREMISA — ninguna de las diez conductas tiene regla en milpa/tramite.yaml (0 de 22; solo en la propuesta ola 5 como proxy_descriptivo que el motor no carga); etiquetar exige crear reglas, que la firma no autoriza · **impacto:** N_resultados_gen2_pendientes_adopcion sigue en 10; adoptados_activos sigue en 72 · **sucesor:** FP-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-3-d164-01 (NC-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-3-d164-01).

## CONSUMIDO

PR #1114 (PARO-PREMISA; ADR-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-3-d164-01). Merge de mesa.

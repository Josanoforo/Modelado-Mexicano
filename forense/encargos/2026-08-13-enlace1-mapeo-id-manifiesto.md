- **SHA de redacción:** `b17a6f6` (`origin/main`, post-#195 — confirmado contra el clon en esta sesión)
- **Entorno asignado:** cualquiera, sin red (declarado por el propio encargo; sonda saltada). Ejecutado en esta ocasión en un entorno de nube efímero — ver `forense/notas/2026-08-13-enlace1-commit1-reglas-mapeo.md` §7 para la limitación de corpus que ese entorno concreto expuso (Commit 2 pendiente de un entorno con `data/raw`/`data/raices.local.yaml` montados).
- **Estado:** VIVO — Commit 1 (reglas + mapeo de las 21 filas, congelado por lectura) ejecutado en `forense/notas/2026-08-13-enlace1-commit1-reglas-mapeo.md`. Commit 2 (escritura en `relaciones.tsv` + corrida de la vía + `--escribe`) no ejecutado — bloqueado por falta de corpus montado en el entorno de esta sesión, pendiente de decisión de usuario/mesa.

---

Texto completo del encargo, tal como se lanzó (verbatim, el documento completo `PLANENLACECAPA220260813.md` subido por el usuario — incluye la adjudicación §0, el estado del repo §1, el encargo ACTO ENLACE-1 §2 que este acto ejecuta, y la secuencia posterior §3):

---

# PLAN DE SIGUIENTES PASOS — el contador de adquisición, destrabado con evidencia
### 13/ago/2026 · base verificada en sesión: `origin/main = b17a6f6` (post-#195) · Adjudica la corrección de la sesión de Opus con el árbol enfrente, y entrega el encargo que ninguna de las dos lecturas anteriores tenía bien: ACTO ENLACE-1

> **PROCEDENCIA.** Todo lo de abajo fue verificado por comando contra el clon en esta sesión: la vía corrida en modo lectura (197 filas, 0 diffs, 97 candidatas), la distribución de `id_manifiesto` (173 `NO_DETERMINADO` / 24 con id real — cero excepciones), las 14 filas ISSP leídas una a una, los 16 ids ISSP del manifiesto listados, y la spec V2 (`forense/notas/2026-08-13-v2-via-capa2.md`) leída del árbol.

---

## §0 · LA CORRECCIÓN, ADJUDICADA — quién tenía razón en qué

**Lo que Opus corrige bien, y acepto:** el bloqueo VIGENTE del contador de adquisición no es código. La vía existe (`tools/curador_registro/via_capa2.py`, ACTO V2, PR #192), corre, propone 0 diffs, y su negativa a promover por nombre de fuente (citando la jerarquía de MAP-B) es exactamente lo que la hace confiable. Con la vía construida, lo que falta es dato y asignación. Mi formulación de "cuello de botella #1" quedó vencida en el momento en que V2 fusionó.

**Lo que mi diagnóstico decía, y el propio repo confirma:** el 12/ago la vía NO existía — no es memoria mía, es el §0 de la spec de V2, que re-derivó la premisa antes de escribir código: `grep -rn "capa2" tools/ tests/ | wc -l → 0`. El acto V2 se autorizó y ejecutó precisamente por esa decisión de la cola (ventana ADR-70(d), autorización de mesa citada en su nota). Ambos diagnósticos fueron correctos en su fecha; el de Opus es el vigente.

**Lo que la sesión de Opus trae impreciso, verificado contra el árbol — y cambia la forma del encargo:** las 173 filas NO tienen "id_manifiesto escrito pero el archivo no está bajado". **Las 173 tienen `id_manifiesto = NO_DETERMINADO` — cero excepciones** (probado programáticamente por la propia spec V2 §1, y re-verificado por mí hoy: 173 `NO_DETERMINADO`, 24 con id real, y los 24 con id son exactamente las 24 `SI`). Las 14 filas de ISSP (no 6 — son 14: N2×2, N3×2, N12×3, N13×3, N14, N28, N30×2) traen todas `NO_DETERMINADO`.

**Por tanto la pregunta de Opus ("¿corro `--escribe` o reconcilio ids inventados?") tiene una tercera respuesta, que es la correcta: ninguno de los dos.** No hay ids inventados que reconciliar, y `--escribe` con la llave vacía escribe cero. El acto pendiente es **ASIGNAR la llave** — poblar `id_manifiesto` fila por fila, por correspondencia semántica bajo la jerarquía de evidencia de MAP-B, y SOLO DESPUÉS correr la vía. Es el acto delicado que Opus anticipó, en la variante que ninguna de las dos sesiones había verificado. Ya no hay nada que verificar antes de escribir el encargo: está abajo, completo (§2).

---

## §1 · LO QUE EL REPO YA RESOLVIÓ SOLO (estado, verificado)

- **La cascada de fusión se ejecutó exactamente en el orden entregado:** #185 → #187(+#186) → #188 → #189, con la reconciliación de MAP-B hecha en su rama (`bcd8a66`: resolvió el conflicto real del puntero Y reconcilió contra #186/#187). Los cinco en main.
- **V2 construyó la vía** con la disciplina completa: spec derivada del corpus ANTES del código, la semántica de `SI`/`SI_O_REFERENCIADO`/`NO_REFERENCIADO` resuelta con evidencia (68 = "referenciada en trabajo analítico real, no confirmada"; 105 = solo barridos de descubrimiento del 6/ago; 10 excepciones declaradas sin re-clasificar), y modo lectura por defecto.
- **ISSP: el usuario lo bajó** (la acción manual #1 del assessment — hecha). Registrado (ACTO R), **RETRACTADO formalmente** (R-RETRACCIÓN — el registro inicial de ZA6980 se retiró), y re-registrado por la vía completa (**R″**: 3 módulos, 16 archivos — ZA6980/2017 Social Networks, ZA5900/2012 Family & Gender, ZA7600/2019 Social Inequality — con México verificado EN EL DATO REAL, no por nombre de archivo). La secuencia registro→retracción→re-registro es el sistema funcionando, no un tropiezo.
- Mantenimiento: ACTO W/W′ (worktrees 37→26, universo del inventario corregido), ACTO Z (inventario pre-purga del repo curador: nada que rescatar), índice de infraestructura (#191).
- **La vía, corrida hoy en modo lectura por mí:** 197 filas · **0 diffs propuestos** · **97 filas de diagnóstico auxiliar** (sin `id_manifiesto`, con fuente presente en el manifiesto vía `alias-fuentes.yaml`) — la lista de trabajo humana. Incluye mucho más que el Lote 1: ENIF, ENVIPE, ENIGH, ENSAFI/ENFIH (los pares), FINANZAS, CSES…

---

## §2 · ENCARGO ACTO ENLACE-1 — asignación de `id_manifiesto`, alcance Lote-1 (caja o nube, SIN red · dos commits)

**Qué es:** el acto que toca la llave de enlace de `relaciones.tsv` — por primera vez desde que las 24 `SI` nacieron — para las filas cuya fuente YA tiene payload íntegro en el corpus: **ISSP (14 filas), WVS (2: N5, N15), CSES (5: N17, N25, N26×2, N27)** ≈ 21 filas. Es deliberadamente acotado: prueba el mecanismo en el lote donde la evidencia es más fresca antes de abrir las ~76 candidatas restantes del diagnóstico (eso es ENLACE-2, después).

════════ ARRANQUE — íntegro (bloque de `forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md`): REPO · SHA contra `b17a6f6` o posterior · data/raw enlazada al corpus (la verificación de payload la hace la vía contra disco — SÍ necesitas el corpus montado) · ENTORNO: cualquiera, SIN red — decláralo y salta la sonda · ESPEJO nada · REMOTO `Josanoforo/Modelado-Mexicano` ════════

**PREMISAS (script literal — si algo no cuadra, PARA y repórtalo):**
```bash
set -u; cd "$(git rev-parse --show-toplevel)"
python3 tools/curador_registro/via_capa2.py | head -4      # esperado: 197 filas, 0 diffs, diagnóstico 97
awk -F'\t' 'NR>1 && $7=="NO_DETERMINADO"' data/curacion-registro/relaciones.tsv | wc -l   # esperado 173
awk -F'\t' 'NR>1 && $3=="ISSP"' data/curacion-registro/relaciones.tsv | wc -l             # esperado 14
grep -cE "^- id: za(6980|5900|7600)" data/manifiesto.yaml                                  # esperado 16
```

**PERÍMETRO Y CONCURRENCIA:** `data/curacion-registro/relaciones.tsv` (SOLO columnas `id_manifiesto`, `sha256_fuente`, `evidencia_ref`/`nota` de las filas del alcance; `capa2` la escribe LA VÍA, no tú) · `forense/notas/` (1) · `forense/encargos/` (A.3) · hallazgos (union). **NADIE MÁS toca `relaciones.tsv` mientras este acto corre — y M-APERTURA no se lanza hasta que este acto fusione** (escribe `capa4` del mismo archivo). **Fuera de la lista, PARA.**

**Commit 1 — las reglas de correspondencia, congeladas ANTES de tocar una sola fila.** Declara, derivándolo del árbol y no de este encargo:
1. **La convención del precedente:** qué clase de entrada reciben las 24 `SI` existentes como `id_manifiesto` — léelas (ej. `enasic2022_fd_xlsx`, `enbiare2021_fd_pdf`, `ensafi2023_bd_csv_zip`): la fila apunta al **objeto del manifiesto que evidencia ESA relación** (el FD/cuestionario si el `objeto_evidencia_id_canonico` es un reactivo/variable documentada; el payload de datos si el objeto es el microdato). Deriva la regla del precedente, escríbela, y aplícala igual a las ~21 — no inventes una nueva.
2. **El mapeo módulo↔necesidad de ISSP — la parte delicada.** ISSP tiene TRES módulos en el manifiesto (ZA6980/2017 redes, ZA5900/2012 familia-género, ZA7600/2019 desigualdad) y 14 filas que sirven 7 necesidades. La asignación es POR FILA, por la jerarquía de MAP-B (URL/cita > necesidad reforzada > nunca parecido de nombre): lee `evidencia_ref` y `objeto_evidencia_id_canonico` de cada fila y decide qué módulo evidencia ESE objeto (ej.: un reactivo de redes de apoyo → ZA6980; uno de roles de género → ZA5900; uno de percepción de desigualdad → ZA7600). **Pre-registra el mapeo de las 14 antes de escribir cualquiera.** Si una fila no se deja decidir con la evidencia del repo: queda `NO_DETERMINADO` con la razón en `nota` — dejar una fila sin asignar es entregable; asignarla por plausibilidad temática es el defecto que la jerarquía prohíbe.
3. **La cuestión de los pares (declárala, NO la resuelvas):** el precedente ENSAFI/ENFIH muestra pares fila-`SI`/fila-`NO_DETERMINADO` para la misma necesidad (distinto `objeto_evidencia`). Si el alcance de este acto produce un patrón análogo, se sigue el precedente (cada objeto su fila, cada fila su evidencia); la política general de pares es de ENLACE-2/mesa.
4. `sha256_fuente` de cada fila asignada: se copia del manifiesto (la entrada asignada), no se recalcula ni se deja vacía — mira cómo lo traen las 24 `SI` y haz lo mismo.
5. La frase: **"el primer resultado que produzca este procedimiento es el que se reporta."**

**Commit 2 — la asignación y la vía.** (a) Escribe `id_manifiesto` (+`sha256_fuente`) en las filas pre-registradas, exactamente como el commit 1 lo congeló — si al ejecutar descubres que un mapeo del commit 1 estaba mal, NO lo corrijas en silencio: tercer commit que lo diga. (b) Corre `python3 tools/curador_registro/via_capa2.py` (lectura) y pega su salida cruda: los diffs propuestos deben ser EXACTAMENTE tus filas asignadas, ninguna más. (c) `--escribe`. (d) Re-corre en lectura: 0 diffs restantes sobre tus filas. (e) Suite `--baseline` y `test_celdas_d` — cruda. (f) La nota cierra con el contador en una línea: **capa2 `SI`: 24 → N** (el N lo produce la vía, no este encargo), y el diagnóstico auxiliar actualizado (97 → M).

**Qué NO hace:** no descarga nada (sin red) · no toca `capa2` a mano (eso es de la vía, siempre) · no resuelve los pares ni las otras ~76 candidatas (ENLACE-2) · no toca los alias (`alias-fuentes.yaml` — acto de alias aparte, ya en cola de mesa) · no adjudica: si alguna asignación depende de una lectura discutible del objeto, va como PROPUESTA con la fila en `NO_DETERMINADO`.

**Contador:** el primer movimiento de capa2 del programa entero. Y si al leer los objetos ISSP una fila resulta evidenciar directamente un SIN-RUTA abierto (N12/N13/N14 lo son): titular del cierre.

---

## §3 · LA SECUENCIA COMPLETA DESPUÉS DE ENLACE-1

| # | Qué | Quién | Gate |
|---|---|---|---|
| 1 | **ENLACE-1** (§2) | ejecutor, sin red | ninguno — listo para lanzar |
| 2 | **M-APERTURA** (encargo §6 del plan de descargas, vigente) | ejecutor, caja | ENLACE-1 fusionado (mismo archivo) + decisión acotada de mesa por los dos `NO-ENCONTRADO` de M-ADQ |
| 3 | **ENLACE-2** — las ~76 candidatas restantes del diagnóstico + política de pares | ejecutor | ENLACE-1 fusionado (el mecanismo probado); encargo se redacta con sus lecciones |
| 4 | **Correo del usuario** (minutos): activación World Bank → microdato EARLY_CHILDHOOD; correo GPS/briq | usuario | — |
| 5 | **Firma Lote 2** — ya sin condición de vía; candidatas GDELT (una de la familia), ENCOAP, WB_ENTERPRISE_2023 | mesa | lo aprendido del Lote 1 ya está escrito |
| 6 | **U2/EV-1** (fila ENASIC obligatoria) y **U3** (con sus dos señalizaciones) | ejecutores | vigentes, sin re-emisión |
| 7 | Cola de mesa que sigue abierta: **llave K (desde fila B)** · **reserva ADR-67(b)** (décima condicional) · **rótulo de cota** (MAP-A §7) · **acto de alias** (CSES/GPS duplicados — ahora alimenta directamente el diagnóstico de la vía) · **A.7 → v2.7** · backfill A.3 de K-L-M-N | mesa | sin evidencia en los commits nuevos de que alguna se haya tomado — siguen pendientes |

**El costo de este documento, contado:** un encargo nuevo (ENLACE-1), cero reglas nuevas — la regla de transición es la de V2, la jerarquía es la de MAP-B, la convención es la de las 24 filas que ya existen. Y una adjudicación de corrección donde las dos partes quedan con lo suyo: la vía faltaba cuando lo dije, sobra desde el 13, y el acto que ambos diagnósticos apuntaban no era ninguno de los dos que estaban sobre la mesa.

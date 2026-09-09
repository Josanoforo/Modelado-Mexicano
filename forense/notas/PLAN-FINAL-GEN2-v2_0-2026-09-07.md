# PLAN FINAL · GEN2 (CORRIDA-0 + AUTOMATIZACIÓN + LIMPIEZA) · v2.0
### Programa «Psicología del Mexicano Contemporáneo» · dirección (Fable, Maestra 48) · 7/sep/2026 · **GEN1 cerrado: `origin/main = 03bcd6f6` (PR #597, M13 v1.3, 01:29 CST)** · sella con el merge de mesa · integra y sustituye: PROPUESTA-CORRIDA-0 v1.1, PLAN-FINAL-CORRIDA-0 v1.1, AUTOMATIZACIÓN-GEN2-y-LIMPIEZA, y el «PLAN FINAL · AUTOMATIZACIÓN Y LIMPIEZA» externo (ChatGPT, 7/sep)

> | | |
> |---|---|
> | **QUÉ ES** | El único documento operativo de GEN2: qué se aprueba, en qué orden se ejecuta, qué automatiza la máquina y qué queda humano, cómo se limpia el terreno, y con qué contadores se sabe dónde va. Los documentos anteriores quedan como historia y argumento; este manda. |
> | **BASELINE** | Derivado hoy: ADR máx 388 · FP máx 337 · specs con gate en `main`: S6 v1.2 `c1cd3b63…`, S12 `870522a3…`, S13 `c41235b8…` · `corridas-M/*__v1_3.json` 3 · marco v1.3 en `main` · checkout 246 MB, `.git` 61 MB (pack 38 MB) · cola de encargos 7 · una rama remota viva (`sello-3-6y5e0z`, PARO). Todo acto re-deriva contra el `origin/main` vigente al arrancar; este SHA fija contra qué se redactó, no sustituye el `fetch`. |
> | **PRINCIPIO** | El humano decide qué medir. La máquina registra, verifica y conecta mecánicamente lo que ocurrió. El cálculo no termina hasta producir su propia procedencia. |

---

## 1 · Decisión

1. `GEN1` queda cerrado y congelado como `LEGACY-GEN1` (íntegro; no se reescribe; no se declara falso).
2. `GEN2` se construye solo con corridas nuevas y selladas; el perímetro se deriva desde los consumidores activos hacia atrás (cierre transitivo), no desde inventarios históricos.
3. Se aprueban las doce automatizaciones (§4) como arquitectura, con implementación escalonada (§8): la infraestructura no bloquea la medición.
4. Se aprueba la política de higiene de árboles (§6).
5. Ningún valor GEN1 elige receta, filtro, ponderador ni alternativa; la comparación con legacy se calcula después y por script.
6. Solo diferencias materiales suben a mesa, evaluadas por consumidor.

---

## 2 · Cadena obligatoria de toda cifra activa GEN2

```
SPEC (md + yaml) → CALC → INPUTS + HASHES → CÓDIGO FIJADO (commit/blob) → ENTORNO MATERIAL → EJECUCIÓN → RESULT → USO/CONSUMIDOR
```
El sistema responde mecánicamente: qué se midió, con qué inputs y hashes, con qué código y commit, con qué parámetros, en qué entorno, qué resultado, qué consumidores, si la cadena está completa. Tres preguntas distintas y separadas: **¿se reproduce?** (automatizable) · **¿pasó validación independiente?** (instrumentable) · **¿se adopta?** (humana).

## 3 · Specs en dos capas

- **`spec.md`** (`forense/prereg-caja/S*-spec-v*.md` + sidecar por `tools/sella_sha256.py`): el pre-registro humano — pregunta, argumento, reactivo, justificación de universo y ponderador, alternativas descartadas, límites.
- **`spec.yaml`** (`data/corrida0/CALC-NNNN/spec.yaml`): el **contrato ejecutable normativo** — `spec_id · corrida_id · script · inputs · variable · universo · filtros · ponderador · transformacion · estimando · parametros · seed · tolerancia · outputs`. El cálculo corre contra el yaml; el md explica por qué. Unidos por `spec_id` y sha; **ningún parámetro ejecutable vive en dos sitios**. `preflight` verifica que el sha del md en `main` coincide con el citado en el yaml.

## 4 · Las doce automatizaciones (defecto ya ocurrido → pieza), con su fase

| # | Pieza | Qué automatiza | Defecto GEN1 que atrapa | Fase |
|---|---|---|---|---|
| B-1 | `tools/corrida0.py` — `demanda · spec-check · negativo · preflight · run · verify · registro · status · vigencia · delta` | IDs, hashes (vía `sella_sha256.py` y `manifiesto.py`), commit/blob, entorno, captura de resultados, sello, reejecución con tolerancia | 1 script citado en 50 conductas; 7 coeficientes sin cadena; agregado sin fuente por celda; 0 reejecuciones sistemáticas | I (núcleo) · II (`registro/status`) · III (`vigencia/delta`) |
| B-2 | `spec-check` | Cada `(archivo, variable)` del yaml contra el **inventario canónico vigente** por instrumento completo (nunca versiones superadas): FAIL si no existe; WARN por casi-coincidencia (`IMMS`→¿`IMSS`?) sin nunca darla por hallada; lista secciones del instrumento; imprime patrón y filas | R4.4 (`cen10*` vs `iiib_hs/ce`), mapa de letras `hs02*` entre libros, R7.4/R4.5/R9.3 | I |
| B-3 | `negativo` | Todo NO-ENCONTRADO/SIN-COBERTURA material sale de un barrido declarativo con patrón, archivos, filas, secciones, aciertos con contexto y la línea para el recibo; T25 avisa si falta | L16-BIS-2 «ningún .dta…» sin conteo; A.13 nació de tres casos | I |
| B-4 | `tools/entorno.py` | Firma A.2 tres partes + `git_commit/status` + Python/librerías + raíces **lógicas** (`raiz_logica · configurada · config_sha256`), sin rutas físicas privadas en artefactos commiteados | nube «coherente» sin corpus (E-ENCIG, S-IDG3); payloads solo en un worktree (PR #77) | I |
| B-5 | Integridad completa del corpus | `manifiesto.py --verifica` completo → `bytes-<fecha>.tsv`, cuatro estados sin colapsar; periodicidad decidida **tras medir** duración y ruido | En septiembre solo verificaciones de 1 archivo por acto | IV |
| B-6 | `vigencia` | Detecta `CANDIDATO-VENCIDO` por fecha e instrumento; nunca declara `VENCIDO` | Ninguna medición GEN1 tiene vigencia por fila | III |
| B-7 | `delta` | `valor_legacy · valor_gen2 · delta · delta_relativo`; **tolerancia en la spec, materialidad en el uso** (`usos.tsv: reglas_impacto` por consumidor); salida `SIN-CAMBIO-ESTRUCTURAL · CAMBIO-SIGNO · CRUCE-UMBRAL · CAMBIO-CATEGORIA · MUEVE-MARCADOR · NO-COMPARABLE` | Marcador v1.2 puntuó M con un valor ya sustituido y nadie lo vio hasta leer el YAML | III |
| B-8 | Replay determinista en CI | Solo corridas con `ci_replayable: true` (inputs versionados, código fijado, dependencias fijadas, sin dependencia de `main` vivo, runtime razonable); tolerancia declarada | `3·10⁻¹⁵` entre sesiones equivalentes: byte a byte es condición inadecuada para flotantes | III |
| B-9 | Peso y limpieza del árbol activo | Retirar de HEAD `inventario-reactivos-v1_0/v1_1.tsv` (63 MB de los 246 del checkout; la historia no se reescribe; el pack de 38 MB no cambia); optimizar clon solo si se mide material | Conté 745 737 filas porque las tres versiones estaban ahí; búsquedas sobre versiones muertas | IV |
| B-10 | `tools/limpia_arbol.py --reporta / --aplica` | Inventario e higiene de clones, worktrees, ramas, raíces (§6) | Lanzamientos duplicados (N22 ×2, SELLO-3 ×2), rama apilada, base atrasada, PARO vivo, payloads únicos en worktree | I (guard mínimo) · IV (cron) |
| B-11 | Tablero derivado de `status` | Contadores GEN2 (§9) leídos del CLI; `N` nunca transcrito | Tarjetas narradas a mano (`coercitivo`) | II |
| B-12 | `/acto` como vehículo | ARRANQUE: `fetch --prune`, guard de duplicado (rama/PR/worktree con el mismo rótulo), `entorno`, `limpia --reporta` focal, base confirmada · COMMIT-1: `spec-check`, `preflight` · EJECUCIÓN: `run` · COMMIT-2: `verify`, `registro`, `status`, `delta` · CIERRE: linaje completo, consumidor enlazado, sin huérfanos | D-10: 120 líneas transcritas 17 veces; una CLI que hay que recordar es el mismo defecto | I (guard) · II (resto) |

**Registro GEN2 (§5)**, **T-REPRO** (§7) y **validación independiente** (§7.1) completan el aparato. Después de estas doce, ninguna pieza entra sin responder sí a las tres preguntas de §11.

## 5 · Registro derivado — dos lados, tres vistas
- **Demanda** (`corrida0.py demanda`, = C0-A): desde consumidores activos → `RESULT` pendientes, `CALC` candidatos, `depende_de`, consumidor, `valor_legacy` comparativo, clausura activa de payloads. Entrega `N_resultados_activos · N_corridas_requeridas · N_resultados_pendientes`. Los «~24 payloads», «~7 coeficientes», «21 reglas», «14 celdas» de los documentos previos son **estimaciones** hasta que `demanda` derive.
- **Oferta**: las carpetas `data/corrida0/CALC-*/` (`spec.yaml · ejecucion.json · resultados.json · sello.sha256`) demuestran qué se ejecutó.
- **Vistas** (`corrida0.py registro`, cabecera `# DERIVADO — NO EDITAR`): `corridas.tsv` (corrida_id, spec_id, estado, spec_sha256, script_path, codigo_commit, script_blob_sha256, fecha, n_resultados, reproduce) · `resultados.tsv` (resultado_id, corrida_id, valor, unidad, estado, tolerancia, validacion_independiente, valor_legacy, delta_legacy) · `usos.tsv` (resultado_id, consumidor, tipo_uso, activo, reglas_impacto). Un resultado con varios usos es una medición.
- **Validaciones de `registro`** (paran): ids duplicados, resultado sin corrida, uso hacia RESULT inexistente, CALC sin spec, RESULT sin sello, hash ausente, ciclo, consumidor activo apuntando a LEGACY donde debe ser GEN2. Avisan: RESULT sin consumidor, CALC sin consumidor activo, legacy sin sucesor.

## 6 · Higiene de árboles
- **C-1 Inventario** (solo lectura, antes de cualquier política): clones (`find "$HOME" -maxdepth 4 -name .git`, declarando universo), worktrees (`git worktree list --porcelain`: rama, HEAD, merge-base con `origin/main`, `status --porcelain`, commits no empujados, estado de `data/raw`), raíces (config local; por raíz real, `tools/barrido_descargas_vs_manifiesto.py`: presentes no registrados / registrados ausentes), remoto (`ls-remote --heads`: fusionada · PR abierto · trabajo vivo · PARO · sin utilidad). Entregable: `forense/notas/<fecha>-limpieza-arboles.md`. Cero acciones.
  - **ENMIENDA 2026-09-07 (in situ, no borra lo de arriba):** verificado por `ACTO GEN2-E1 · LIMPIEZA-C1` sobre 598 PRs del historial completo (no solo ramas vivas en `origin`), `gh pr list --limit 500` **trunca en silencio** cuando el repositorio tiene más de 500 PRs — no avisa, no pagina solo, simplemente devuelve los primeros 500. El inventario de C-1 que cruce ramas locales contra el historial de PRs debe usar `gh pr list --limit 1000` (o paginar explícitamente con `--json` + cursor) — nunca el valor por defecto ni `--limit 500` a ciegas. `tools/limpia_arbol.py` se corrige en este mismo acto (GEN2-T7) para usar `--limit 1000` y avisar si el conteo devuelto sugiere truncamiento.
- **C-2 Poda** (mesa firma la lista): ramas remotas fusionadas/consumidas/PARO → borrar (hoy: `sello-3-6y5e0z`); activar *Automatically delete head branches*; locales fusionadas → borrar; con commits únicos → **empujar o reportar**, nunca borrar en silencio; worktrees CONSUMIDO → `remove` + `prune` tras revisar cambios, commits y payloads únicos; clones extra → borrables solo con 0 commits únicos, 0 payloads únicos, 0 trabajo útil (no se exige tar).
  - **ENMIENDA 2026-09-07 (in situ, no borra lo de arriba):** verificado por `ACTO GEN2-E1 · LIMPIEZA-C1` sobre 598 PRs reales: GitHub **ya borra la rama remota al fusionar** cuando el repositorio tiene activado *Automatically delete head branches* — de las ramas de tarea revisadas por E1, solo 3 seguían vivas hoy y ninguna con worktree local. El paso «activar *Automatically delete head branches*» de C-2 es, en la práctica de este repositorio, verificación de un estado ya vigente y automático, no una acción manual pendiente por acto — se deja aquí para que la siguiente sesión no lo trate como bloqueo si lo encuentra ya activado.
- **C-3 Política prospectiva**: worktree por acto desde `origin/main` HEAD tras `fetch --prune`; **base congelada durante el acto** (si `main` avanza, no se auto-mezcla en mitad de una corrida: se integra antes del PR y se reejecuta si afecta materialmente); datos: la condición es `payload_id + raíz configurada + hash verificado` — el symlink `data/raw → corpus` es política operacional de la caja, no condición conceptual; nunca se acepta un payload solo por «estar en data/raw»; guard de duplicado antes del 0-bis (rama, PR o worktree con el mismo rótulo → PARA/RESUELVE); árbol limpio al arrancar; `limpia --reporta` al cron cuando su reporte sea estable; métrica `arboles_fuera_de_politica → 0`.
- **C-4 Nunca**: borrar commits únicos no empujados, borrar datos únicos sin inventario, tocar el corpus sin manifestarlo, reescribir historia, auto-merge de `main` en corrida activa, convertir una discrepancia local en auditoría general.
  - **ENMIENDA 2026-09-08 (in situ, no borra lo de arriba; `ACTO GEN2-T8`, A.14, `forense/encargos/2026-09-08-GEN2-T8-A14-CERO-RAMAS-RETROFIT.md`, `NC-0004` de `forense/no-corrido.tsv`):** «commits únicos no empujados» sigue sin borrarse nunca, pero la vía que `ACTO GEN2-E4 · LIMPIEZA-C2 · PODA` (D1) usó para cumplirlo — crear una rama `historico/` que se preserva indefinidamente, sin PR, sin fusionar — queda **derogada**. La política de cero ramas dice: un acto termina con su rama fusionada o borrada; trabajo único sin PR se absorbe en `main` como histórico rotulado (`## HISTÓRICO — NO EJECUTADO` con origen y fecha) o se borra con decisión explícita, nunca se preserva como rama. Medido: `[TRAMITE] absorbe historico` (`PR #605`) ya absorbió los dos commits que `historico/maestra37-l2-mps-codebook-y-p3` e `historico/maestra38-v1-corrobora-y-reconcilia` preservaban, y las dos ramas ya no existen en el remoto (`git ls-remote --heads origin | grep -i historico` → 0, 8/sep/2026) — la derogación documenta un estado ya alcanzado, no ordena una acción nueva. `canon/registro-rotulos.tsv` marca la fila `historico/` `RETIRADO`.

## 7 · Gates y validación
- **T-REPRO** (dentro de `tests/check.py`, no como gobernanza paralela; se activa cuando una corrida representativa haya atravesado el formato): cada RESULT activo GEN2 tiene id, CALC, spec, script, código fijado, inputs, hashes, parámetros, sello y consumidor; cada consumidor resuelve a RESULT y cada RESULT a CALC; `valor materializado == RESULT` dentro de tolerancia (`p: 0.083742` + `corrida0_resultado_id: RESULT-0001`); cambiar el valor sin cambiar el RESULT → FAIL. No decide estimando, fuente, tier ni adopción: impide números huérfanos. No se aplica a GEN1.
- **7.1 Validación independiente** (eje aparte de `verify`; estados `PASA · FALLA · NO-HECHA`): reservada a resultados que pueden cambiar signo, tier, clasificación, marcador, coeficiente central o decisión; métodos: implementación alternativa, identidad matemática, estimador alternativo, tabulación externa, revisión focalizada. Sin doble implementación universal.

## 8 · Fases de implementación (la infraestructura no bloquea la medición)

| Fase | Contenido | Compuerta de salida |
|---|---|---|
| **I · antes del primer lote C0-B** | C-1 inventario · B-1 núcleo (`demanda · preflight · run · verify`) · B-2 · B-3 · B-4 mínimo · guard mínimo B-10/B-12 en `/acto` · **smoke**: `REPLAY-SMOKE` del agregado v1.3 (`generacion = LEGACY-GEN1 · cuenta_gen2 = NO`) | `preflight` VERDE y `verify` REPRODUCE sobre el smoke; C0-A derivado |
| **II · con las dos primeras corridas reales** | B-1 `registro/status` · vistas TSV · B-11 · T-REPRO activado | una corrida real atraviesa todo el formato |
| **III · al primer caso real** | B-6 (primera fuente potencialmente superada) · B-7 (primer par legacy/GEN2) · B-8 (dos corridas `ci_replayable`) | — |
| **IV · periódico, tras medir coste** | B-5 periodicidad · B-9 · B-10 en cron | — |

## 9 · Contadores (todos derivados)
Núcleo: `N_corridas_requeridas · N_corridas_selladas · N_resultados_activos · N_resultados_sellados · N_resultados_pendientes · dependencias_numericas_legacy_activas`. Calidad: `resultados_con_validacion_independiente · resultados_materiales_sin_validar`. Comparación: `diferencias_no_materiales · diferencias_materiales · resultados_no_comparables`. Corpus: `payloads_activos_verificados · payloads_totales_verificados`. Higiene: `arboles_fuera_de_politica · ramas_consumidas_vivas · worktrees_consumidos · payloads_locales_no_manifestados`. Un replay GEN1 nunca incrementa `N_resultados_sellados`.

**Estados de una salida GEN2:** `PENDIENTE → SPEC-FIJADA → PRE-FLIGHT-VERDE → EJECUTADA → SELLADA`, con `REPRODUCE / NO-REPRODUCE / NO-EJECUTABLE` como eje de reejecución; `PASA / FALLA / NO-HECHA` como eje de validación; `LEGACY-GEN1` como eje de generación.

## 10 · Políticas transversales
- **Negativos**: sostienen una decisión solo con patrón, archivos, filas, secciones y aciertos; cero aciertos no es ausencia conceptual.
- **Vigencia**: la máquina descubre candidatos; el humano declara vencimiento.
- **Legacy**: íntegro; `SIN-PROCEDENCIA-VERIFICABLE` vive en el registro derivado; un consumidor histórico se toca solo si sigue operativo y necesita reserva explícita durante la migración.
- **Retiro**: las **reglas** de instrucciones conservan su cláusula de caducidad (tres meses sin atrapar → se retiran); las **herramientas** se evalúan a los tres meses por coste de mantenimiento + fricción contra coste esperado del defecto: un guard barato que protege un defecto material conocido puede quedarse con contador cero.
- **Lo humano, siempre**: variable, reactivo, universo, ponderador, transformación, estimando, equivalencia entre olas y fuentes, `VENCIDO`, materialidad epistemológica, tier, adopción, firma.
- **Lo que no se construye**: base de datos central, servidor de provenance, dashboard complejo, motor de workflows, plugins, framework universal de specs, contenedores antes de necesitarlos, lockfile total, DAG engine, ADR por subcomando trivial.

## 11 · Gate para automatizaciones futuras
Solo entra una pieza nueva si: (1) evita un defecto real ya observado; (2) ese defecto puede cambiar una medición, conclusión o decisión; (3) automatizarlo cuesta menos que corregirlo si reaparece. Un «no» → no se automatiza.

## 12 · Orden de ejecución (encargos en `ENCARGOS-GEN2-en-orden`)
1. **E0 · ENCOLA-GEN2** (nube, Sonnet): este plan, la propuesta v1.1, el plan de automatización, y los encargos E1–E5 a `forense/encargos/cola/` con sidecars; PR `[COLA]`.
2. **E1 · LIMPIEZA-C1** (caja, Sonnet): inventario de árboles, solo lectura.
3. **E2 · C0-A DEMANDA** (nube, Opus): `corrida0.py demanda` + N reales.
4. **E3 · AUTOMATIZA-GEN2-1** (nube, Opus): B-1 núcleo, B-2, B-3, B-4, guard en `/acto`, `REPLAY-SMOKE`.
5. **E4 · LIMPIEZA-C2 PODA** (caja, Sonnet; mesa firma la lista de E1) + ajuste en GitHub.
6. **E5 · CALC-0001..0003 = L19 · L20 · L21** (caja, Opus): las tres specs con gate en `main` corren como primeras corridas GEN2 vía `corrida0.py`, cadena completa antes de ejecutar.
7. **E6 · AUTOMATIZA-GEN2-2** (nube, Opus): `registro/status`, vistas TSV, B-11, T-REPRO — con las corridas de E5 como caso real.
8. **C0-B lotes** — se redactan sobre `corridas.tsv` de E2, no antes. Luego C0-C, C0-D, B-6/B-7/B-8, y la Fase IV.

**La firma de este plan autoriza E0 y E1 de inmediato.**

**Contadores movidos por este documento: cero.** Declarado.

---

## ENMIENDA FECHADA — 8/sep/2026 · `ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`

*Enmienda, no reescritura: el cuerpo de arriba queda verbatim y su
`.sha256` sigue siendo el del documento tal como se firmó.*

**§D11 — REVOCADA.** `D11` (propagada por `ADR-396`, `ACTO GEN2-E3-1`) decía
que `milpa/src/{motor,theta,pi,celdas,momentos}.py` son «scaffold/calibración
histórica» y que el sistema numérico activo es `tramite.yaml + emisor +
matriz B`. Contradice a `ADR-91` (17/ago/2026, `PR #246`), cuya firma de mesa
verbatim es *«M1 cómputo matricial como definición del ejecutable»*, adoptada
**antes** del gate de Fase 1. `D11` se dictó contra el árbol sin cotejarla con
ese sello. **Rige `ADR-91`.** El emisor no es el motor: es el emisor binario
de reglas que alimenta al marcador, una de las salidas del motor.

Consecuencia inmediata y medida: `procedencia.cargar()` **lanza** hoy sobre
`milpa/procedencia.yaml`, así que el ejecutable sellado no arranca. Declarar
«scaffold» a un ejecutable es dejar de correrlo, y dejar de correrlo es dejar
de saber si corre.

**§4 `C0-D` — la unidad de celda queda decidida (D-2, 8/sep/2026).** La celda
del marcador es **`regla × segmento (x, sobre los seis ejes del modelo) × ola
× instrumento`**. Las 14 celdas de hoy son el caso `x = ∅` y se conservan; **no
se colapsan olas**; la dimensión que falta es el segmento. `C0-D` corre el
marcador por segmento cuando `C0-C` entregue motor y emisor limpios — y no
antes de que el motor arranque.

**§8 `C0-B`** se redacta sobre la demanda **re-derivada** (`N_resultados_activos
= 205`, `N_corridas_requeridas = 86`), que ahora incluye Θ, π, celdas-D y
momentos.

Detalle, cifras y comandos:
`forense/notas/2026-09-08-GEN2-T9-motor-matricial-y-unidad-de-celda.md`.

---

**(Enmienda, 9/sep/2026, ACTO GEN2-OBRA-V11)** Fases I-III cumplidas el 8/sep
con compuertas citadas (preflight VERDE, corridas reales, T-REPRO activo,
primer par legacy↔GEN2 en mesa). La obra se gobierna desde hoy en
PLAN-DE-OBRA-GEN2 v1.1; este documento queda como historia del taller.

# Nota de cierre — `ACTO DUELO-PREREG-V2`, 20/ago/2026

**Entorno:** NUBE, repo-only. NO Ubuntu, sin research vivo fuera del repo. **Modelo:** Opus. **Gate de arranque:** `T-SELLO` + `ACT-PIL-2` fusionados (verificado: ambos consumidos, `forense/encargos/2026-08-20-T-SELLO.md` y `forense/encargos/2026-08-20-ACT-PIL-2.md`, ambos `CONSUMIDO`).

## Lectura obligatoria previa (Paso 0), confirmada

1. `forense/TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md` §5, punto 6 — leída completa.
2. `forense/marco-candidatas-piloto-v1_0.tsv` (60 candidatas, `ACT-PIL-2`) — leído, **no reconstruido, no editado**.
3. `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B `ADV1-M5` (tabla verbatim) y §C `D-ii` — leídos, citados.
4. `D-iv` — localizada en `TRANSFER §4` y `CAREO §C`, texto idéntico.
5. `FP-70` — localizada en `forense/hallazgos.md` (entrada 2026-08-19) y en `forense/notas/2026-08-19-lote-ubuntu-adq-1-cierre.md`; **leída como fuente de EE, NO editada, NO tocada** (perímetro respetado — verificable por `git diff` sobre `forense/hallazgos.md`: la única entrada nueva es la de este acto, la de `FP-70` no cambia una letra).
6. `forense/prereg-duelo-v2/` no existía — creado por este acto.
7. Patrón de cierre de actos previos revisado en `forense/bitacora.md`, `forense/hallazgos.md`, `forense/encargos/convencion.md`, y los encargos `2026-08-20-ACT-PIL-2.md`/`2026-08-20-T-SELLO.md` como modelos directos de estructura.

## Entregables producidos, uno por uno

- **T1** — `forense/escala-cinco-casillas-piloto-v1_0.md`. `ADV1-M5` copiada VERBATIM, `D-ii` citada. **NO SELLADA** — COMPUERTA B-bis activada: "el falsador no refute" no tiene definición en el corpus fundacional (verificado por comando, cero coincidencias en los cinco documentos) y la precedencia entre las cinco casillas no está declarada. Opciones abiertas documentadas en `mesa-pendientes.md` §1-§2, sin decidir por este acto.
- **T2** — `forense/prereg-duelo-v2/pipeline-L-adv1-m2.py`. Spec+script de `ADV1-M2`: sin humano en el bucle, modelo+versión+fecha+temperatura como parámetros explícitos (`ParametrosCorredorL`), k=5-10 corridas todas registradas sin descarte con dispersión (`agregar_continua`/`agregar_categorica`), dos variantes `L-solo`/`L+corpus`, y compromiso por hash de los cuatro corredores L/M/B/E antes de R (`commit_hash_registry`). `llamar_modelo` lanza `NotImplementedError` a propósito — el script nunca se ejecutó.
- **T3** — `forense/prereg-duelo-v2/scoring-adv1-m3.py`. `skill = 1 - error/error(B)`, CRPS/interval-score y Brier evaluados contra R como distribución (`ArbitroR`, nunca contra el punto), `INDECIDIBLE` con sus dos condiciones exactas separadas (`es_indecidible`), calibración al 80% como resultado independiente (`calibracion_80`), y `ADV1-M3-bis` distribucional (KS, Wasserstein, razón de varianzas, cortes por subgrupo).
- **T4** — `forense/prereg-duelo-v2/banda-tost-margen-v1_0.md`. Deriva banda TOST (`±0.5·EE(R)`) y margen material sin calcular ningún punto sobre México. Las cinco vías de `NO-ENCONTRADO` del artefacto oficial de EE se enumeran con su verificación de comando. `FP-70` citada como fuente de los dos EE reales disponibles, no editada. Marcado explícitamente **PROPUESTA PARA MESA**, sin firma propia.
- **T5** — `forense/prereg-duelo-v2/corredor-B-tasa-base.py` (tasa base de última ola pública o persistencia, con precedencia mecánica declarada) y `forense/prereg-duelo-v2/corredor-E-combinacion-LM.py` (combinación `L⊕M`, operador sin definición formal en el corpus — propuesta simple documentada como no-sellada en `mesa-pendientes.md` §3).
- **Mesa** — `forense/prereg-duelo-v2/mesa-pendientes.md`, nuevo, con las tres ambigüedades sin resolver (§1 "el falsador no refute", §2 precedencia de `ADV1-M5`, §3 definición de `⊕`).

## Compuertas activadas

**COMPUERTA B-bis: ACTIVADA.** Ver arriba (T1). Este es el único gate del encargo que se disparó; ninguna otra ambigüedad de las nombradas explícitamente en el encargo (T2-T5) careció de especificación suficiente en el corpus salvo la de `⊕` (T5), tratada con el mismo principio (documentar, no decidir) aunque no estaba nombrada como compuerta formal.

## Contador

Medición sobre México: **0**. Pre-registro por diseño — ningún estimado puntual se calculó en ningún entregable (T4 lo declara explícitamente al cierre de su propio texto). Fila añadida en `forense/hallazgos.md` (entrada de cierre de este acto) con "Contadores movidos: 0", siguiendo la convención de cierre de acto que el resto del tablero usa.

## Perímetro respetado, verificación

Archivos tocados por este acto: `forense/escala-cinco-casillas-piloto-v1_0.md` (nuevo) · `forense/prereg-duelo-v2/*` (nuevo, seis archivos) · `forense/hallazgos.md` (una entrada añadida, nada más) · `forense/notas/2026-08-20-duelo-prereg-v2-cierre.md` (este archivo) · `forense/encargos/2026-08-20-DUELO-PREREG-V2.md` (archivo del encargo, nuevo). **No tocado:** `milpa/`, `forense/marco-candidatas-piloto-v1_0.tsv`, `FP-70` (ninguna fila de `hallazgos.md` distinta a la nueva), `data/`, `corpus/`, `canon/`. Ningún script de `forense/prereg-duelo-v2/` se ejecutó — los cinco terminan en `raise SystemExit(...)` bajo `if __name__ == "__main__"` como salvaguarda explícita. Sin `--freeze` en ningún comando git de esta sesión.

**Estado:** `CONSUMIDO` por este mismo acto al cerrar.

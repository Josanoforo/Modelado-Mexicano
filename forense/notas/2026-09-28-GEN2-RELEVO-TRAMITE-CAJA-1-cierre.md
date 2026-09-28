# ACTO GEN2-RELEVO-TRAMITE-CAJA-1 · cierre por PARO (f)

Contadores movidos: **cero**. Ninguna spec, ningún COMMIT-1, ningún microdato abierto, ningún CALC, ningún RESULT, ninguna escritura en `milpa/`. `N_corridas_requeridas` (demanda) 0 → 0; `dependencias_numericas_legacy_activas` 67 → 67; `celdas_validadas` 219 → 219 (Δ0) @ `e2f9cb0f`.

- Encargo: `forense/encargos/2026-09-28-GEN2-RELEVO-TRAMITE-CAJA-1.md` (0-bis `e2f9cb0f`, `.cuerpo.sha256` = `fb4cd181…`, idéntico byte a byte al adjunto recibido).
- ADR: `ADR-260928-GEN2-RELEVO-TRAMITE-CAJA-1-e2f9-01`.
- Entorno: CAJA (`tools/entorno.py --arranque --sonda-red` → `ENTORNO-DERIVADO = CAJA`, `senal-corpus: montado=SI archivos_examinados=515`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, red `http_code=200`). Modelo: Opus 5.5.
- Compuerta de arranque («espera a que PISOS-Y-ADENDAS-1 cierre»): se esperó con la sesión viva. `gh pr list --state all --head acto/gen2-pisos-y-adendas-1` → `1277 MERGED 2026-09-28T18:09:30Z`. Rama creada después, sobre `origin/main` = `565032332` (merge de #1277); `git rev-list --count HEAD..origin/main` → 0.
- SHA de redacción `723b62c1` → base `565032332`. Entre los dos se fusionaron, entre otros, **#1275 GEN2-DEMANDA-DICTAMEN-1** (17:37Z) y #1277. El primero es el que cambia el terreno.
- Guard 0.c: sin rama remota, worktree ni PR abierto con el rótulo; `git ls-tree -r --name-only origin/main forense/encargos | grep -c 'RELEVO-TRAMITE\|RELEVO-CONSUMIDORES-4\|RELEVO-MOTOR-35'` → 0 (igual que el §4 del encargo).

## 1 · Qué se encontró

**La demanda de la que sale el encargo ya no pide ninguna corrida.** Es el PARO (f) de la lista cerrada (§7 f, «objetivo inalcanzable»). El criterio de «Hecho» exige que `corrida0 demanda` en el commit final muestre `N_corridas_requeridas` **menor** que en la apertura, y en la apertura ya es 0:

```
$ python3 tools/corrida0.py demanda        # sobre 565032332 (apertura de este acto)
N_resultados_activos = 236
N_corridas_requeridas = 0  (de apertura 105; no requeridas por dictamen 105)
N_resultados_pendientes = 63  (cerrados por dictamen 173)
```

Las 105 corridas salen por dictamen de `data/corrida0/demanda-dictamen-v1_0.tsv` (GEN2-DEMANDA-DICTAMEN-1, PR #1275, fusionado por mesa). Las 10 corridas del §1 del encargo están entre ellas, con dictamen `CORRIDA-NO-REQUERIDA`. Sus **49 RESULT** tienen cada uno un dictamen citado (join por `resultado_id`, que es alias estable; el `CORR-` no es citable, D-24):

| corrida (apertura) | instrumento | n | dictamen de sus RESULT |
|---|---|---|---|
| CORR-0002 | ENCIG 2025 | 12 | 8 `YA-RELEVADO-GEN2` · 4 `NO-RELEVAR-POR-FIRMA` (RES-0009..0012: `rol_uso: historico`, firma B2 `FP-260924-GEN2-RELEVO-MOTOR-34-1-a157-02`, FIRMADA) |
| CORR-0003 | ENCUCI 2020 | 4 | 4 `YA-RELEVADO-GEN2` |
| CORR-0007 | ENVIPE 2025 | 8 | 8 `YA-RELEVADO-GEN2` |
| CORR-0009 | ENIF 2024 (medidos) | 9 | 9 `YA-RELEVADO-GEN2` |
| CORR-0011 | ENIGH 2022 | 2 | 2 `YA-RELEVADO-GEN2` |
| CORR-0012 | ENFIH 2019 | 2 | 2 `YA-RELEVADO-GEN2` |
| CORR-0013 | EDER 2017 | 2 | 2 `YA-RELEVADO-GEN2` |
| CORR-0014 | ENUT 2024 | 1 | 1 `YA-RELEVADO-GEN2` |
| CORR-0015 | ENIF 2024 (asignados, orden 3) | 7 | 7 `YA-RELEVADO-GEN2` |
| CORR-0018 | LAPOP MEX 2019/2023 | 2 | 2 `YA-RELEVADO-GEN2` |
| **total** | | **49** | **45 · 4** |

**Las 45 citas `YA-RELEVADO-GEN2` se verificaron contra la fuente, no se heredaron.** Para cada una se extrajo el `corrida0_resultado_id` citado y se buscó en `data/corrida0/resultados.tsv` (lector CSV) y en los `resultados.json` de los CALC:

- **40 de 45** están en `resultados.tsv` con `estado=SELLADA · generacion=GEN2 · cuenta_gen2=SI`. Las 6 que citan una línea de `milpa/tramite.yaml` casan con esa línea (±3).
- **5 de 45** (`RESULT-ENCIGDER-A-Q`, `-B-PRE-SD-Q`, `-B-DIG-SD-Q`, `-C-Q`, `RESULT-ENCUCIDER-A-Q`) no están en `resultados.tsv`. Viven en `data/corrida0/CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001/` y `CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001/`, cada uno con `sello.json`, sellados el 24/sep por GEN2-RELEVO-MOTOR-34-1 (`729fadd5e`, `6eab41b40`). Los dos CALC no tienen fila en `corridas.tsv` (`tools/consulta.py corrida …` → NO-ENCONTRADO, 357 filas examinadas). **Sí están** en el lote de pendientes del canal: `tools/lote_desde_asientos.py --incluir-pendientes --csv` los lista a los dos entre 104 ids, y el último `[deriva]` (`1f4bf1cc3`) dice «20 CALC, quedan 101». GEN2-DEMANDA-DICTAMEN-1 ya asentó el defecto en `forense/hallazgos.md` (28/sep, «Seis RESULT derivados…») y lo asignó a «canal [deriva]». No es de este acto (§9: vistas = canal).
- `RESULT-CTX-2019-P-ALTO` / `-2023-P-ALTO` (LAPOP): están en `data/corrida0/CALC-0002/resultados.json` y en `milpa/tramite.yaml:1651,1654`. `usos.tsv` aún no los refleja (`SIN-FILA`); le toca al mismo canal.

**Tampoco queda materia de caja fuera de esas 10 corridas.** De los RESULT de la demanda con consumidor `milpa/tramite.yaml` cuyo dictamen no es `YA-RELEVADO-GEN2`, **ninguno** pide medición:

| RESULT | tipo | dictamen | dueño |
|---|---|---|---|
| RES-0001/0002/0007/0008/0017/0018 | conducta_p_asignado | SIN-BASE-GEN2 (gemelo en `procedencia.yaml`) | GEN2-RELEVO-CONSUMIDORES-4 |
| RES-0009..0012 | medido/derivado | NO-RELEVAR-POR-FIRMA (B2) | ninguno (histórico) |
| RES-0023/0024 | conducta_p_asignado | ESPERA-FIRMA-MESA (A1, momento ENCIG del catálogo) | GEN2-TRAMITE-FIRMAS-21 |
| RES-0029/0030 | conducta_p_medido | ESPERA-FIRMA-MESA (B1, ENNViH ola 3 reservada) | GEN2-TRAMITE-FIRMAS-22 |
| RES-0050..0052 | conducta_p_medido | RELEVAR-DESDE-RESULT (`CALC-L8-CONVERSION-0001`, REPRODUCE-GEN1) | mesa (adopción) → pin por el canal |

La nota de GEN2-DEMANDA-DICTAMEN-1 lo dice así: «Lo que queda es firma (A1, A2, B1, B2) y pin (RELEVO-CONSUMIDORES-4), no caja» (`canon/L0/ADR-260928-GEN2-DEMANDA-DICTAMEN-1-c133-01.md`).

## 2 · Por qué el encargo pidió lo que ya estaba

1. El encargo y GEN2-DEMANDA-DICTAMEN-1 se redactaron sobre la **misma** demanda (`723b62c1`, 105 corridas) y salieron en paralelo. El §4 del encargo los declara «disjuntos». No lo eran: el dictamen cubre las 105 corridas, incluidas las 10 de caja de este acto.
2. El encargo de DEMANDA-DICTAMEN-1 le ordenaba citar las 10 de orden 1 «como EN-CURSO» (por este acto). Ese acto encontró que ya eran GEN2 o `rol_uso: historico`, no usó EN-CURSO y dejó `NC-260928-GEN2-DEMANDA-DICTAMEN-1-c133-01` (ABIERTA, «NO-VERIFICABLE-AQUÍ: el acto no está en forense/encargos/»). **Este acto aporta la evidencia que a esa NC le faltaba:** RELEVO-TRAMITE-CAJA-1 existe (0-bis `e2f9cb0f`) y confirma, RESULT por RESULT, que no había nada de orden 1 por medir. La fila es de otro acto (sucesor declarado: RELEVO-TRAMITE-CAJA-2) y no se edita aquí. Quien la herede puede cerrarla citando esta nota.
3. La demanda de 105 existía porque `corrida0 demanda` no derivaba estado desde la vista: contaba como pendiente un RESULT que `usos.tsv` ya daba por GEN2. Eso es `NC-…-c133-02` → GEN2-DEMANDA-DICTAMEN-2.

**Discrepancia de contadores, declarada y ajena.** `corrida0 status` sobre la misma base da `N_corridas_requeridas=87` y `N_resultados_pendientes=211`, contra 0 / 63 de `corrida0 demanda`. `status` no lee el dictamen. Ya está asentado como `NC-260928-GEN2-DEMANDA-DICTAMEN-1-c133-03` (FUERA-DE-PERÍMETRO: GEN2-TUBERIA-Y-CURACION-1, dueño de `status`). El criterio de «Hecho» de este encargo se mide con `corrida0 demanda`, y ahí no hay unidad que bajar.

## 3 · Qué no se hizo y por qué

- **(i)–(iv) por instrumento** (specs humanas, spec.yaml, COMMIT-1, corrida, RESULT, relevo por el escritor): no se hizo nada. Los 45 RESULT ya son GEN2 sellados y las 4 ENCIG 2025 salen del consumo vivo por firma. Una corrida nueva sería un segundo «primer resultado» de lo ya sellado (E.5: «lo ya sellado se cita, no se re-mide»). Ningún microdato se abrió: la sesión no leyó cuestionario, descriptor ni dato de ninguna de las nueve olas. ADR-46: la sesión queda **sin contaminar** para todas.
- **Relevo en `tramite.yaml` por el escritor**: no aplica. Las líneas citadas ya llevan `corrida0_generacion: GEN2`.
- **`corrida0 demanda` en el commit final**: se corrió al abrir (salida arriba). Reescribe `demanda-corridas.tsv`/`demanda-resultados.tsv`, que son derivados del canal: el diff se descartó con `git checkout --` y no viaja en el PR.
- **Sucesor `RELEVO-TRAMITE-CAJA-2`** (§10 del encargo): hoy tampoco tendría materia de caja. Lo que DEMANDA-DICTAMEN-1 dejó decidible son firmas y pins, no mediciones. Recomendación a dirección: no lanzarlo hasta que una firma de FIRMAS-21/22 abra un RESULT medible (p. ej. B1 si mesa abre ENNViH ola 3). Es orden sugerido, no pregunta a mesa.

## 4 · Módulo de auditoría (v2.16)

No aplica: no se escribió spec ni se afirma nada sobre México. ¿Cuántos contadores movió este trabajo? **Cero.**

NC: `forense/no-corrido.tsv` → `NC-260928-GEN2-RELEVO-TRAMITE-CAJA-1-e2f9-01..02`. Sin FP: nada de este acto espera firma de mesa.

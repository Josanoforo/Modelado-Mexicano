# `GEN2-M-SNAPSHOT-TRIADA` (ENCARGO 4/5) — nota de resultado

**Fecha:** 10/sep/2026 · **Entorno:** NUBE, cero microdato, cero adquisición
nueva, cero apertura de `corridas-R/` · **Base:** `origin/main = da08846`
(merge de `PR #676`, `ACTO GEN2-F5-EXTRACTOR-L-v1`; `PR #674` es ancestro) ·
**Encargo:** `forense/encargos/2026-09-10-GEN2-M-SNAPSHOT-TRIADA.md`
(verbatim) · **Producto:** `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.py`
(script sellado) + `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json`
(snapshot/CALC, las 14 celdas).

---

## 1 · P1 · Identidad del motor congelada

`git rev-parse HEAD` = `da088463dbca096470caf7364148778a1c93b4b0` (idéntico a
`origin/main` al arrancar — `git rev-list --count HEAD..origin/main` = `0`).
`git rev-parse HEAD:milpa` = `1669f8bc3f90e1def2044d740faa03f33a265392`.
Hashes SHA-256 material (íntegros en
`snapshot-M-triada-v1_0.json.identidad_del_motor`):
`milpa/tramite.yaml`, `milpa/procedencia.yaml`, `milpa/src/emisor.py`,
`tools/emite_m.py`, `marco-M-sorteado-v1_3.tsv`, `candidatos-marco-M-v1_1.tsv`.
Python `3.11.15`.

**Referencia histórica (PR #674, `eab46ed`).** `git diff --stat
eab46ed..HEAD -- milpa/` → **vacío**: el árbol que alimenta a `M` es
**idéntico** al estado que dejó `PR #674`. Nada material cambió entre esa
referencia y este acto — no hay nada que declarar en ese tramo. (`PR #676`,
que sí se fusionó en ese intervalo, tocó únicamente `tools/extrae_l_v1_3.py`
— instrumento de `L`, fuera del árbol de `M`.)

**Hallazgo declarado, no ocultado tras el SHA general:** el emisor vivo
(`emite_celda`, corrido en este acto) reproduce **exactamente** `regla`,
`conducta`, `p`, `valor_punto`, `clase`, `estado_M`, `ola_calibracion` y
`grado_DD` de los 14 archivos `corridas-M/` ya sellados que la resolución
v1.3 (`ACTO MAESTRA38-M13` §16, orden `M-<id>__v1_3.json > M-<id>.json >
M-<id>__v1_2.json`) selecciona para cada celda — pero **no** son bit-a-bit
idénticos en el campo `cita_p`/`cita_ola_calibracion` para 9 de las 14
(las seis `CIV-M-*`, las tres `FAM-M-05/06/07`, las tres `TRA-M-02/03/07`):
`milpa/tramite.yaml` fue **enriquecido**, en algún punto **anterior** a
`PR #674` (por `ACTO GEN2-LOTE-ENVIPE-1`, `ACTO GEN2-PRIMERA-SILLA` y `ACTO
GEN2-LOTE-ENCIG-1`), con claves de proveniencia `corrida0_resultado_id` /
`corrida0_generacion` anexadas **al mismo dict** de cada conducta —
verificado mecánicamente: el dict original `{conducta, p, clase}` aparece
**intacto como prefijo** del dict vivo en los nueve casos, y las tres
remediciones (`RESULT-ENVIPE-DEN-P-C2-U4`, `RESULT-B-ENIGH-2022-P`,
`RESULT-ENCIG-MOR-A-P-SOL1`) **reproducen** el mismo `p` publicado al grano
de seis decimales con deltas del orden de `1e-7`–`1e-8`, con el propio texto
de la enmienda declarando explícitamente *"el `p` NO se movió: se declara de
dónde viene"*. Ninguna de las tres remediciones cita un valor de `R` ni un
resultado del duelo: son remediciones independientes bajo `corrida0`/GEN2,
anteriores a este contrato y anteriores a `#674`. Ningún valor de `M`
consumido por este acto proviene de un objetivo de evaluación.

## 2 · P2 · Reusar o reemitir: 14/14 REUTILIZADAS, 0 reemitidas

`snapshot-M-triada-v1_0.py` re-deriva en vivo, con `tools.emite_m.emite_celda`
(la misma función, no reimplementada) sobre el estado congelado de §1, cada
una de las 14 filas de `marco-M-sorteado-v1_3.tsv`, y compara campo a campo
contra el archivo que la resolución de `MAESTRA38-M13` §16 ya selecciona.
**Las 14 celdas coinciden en todo campo sustantivo** (exentos declarados,
nunca forzados: `fuente`/`archivos_abiertos` citan el acto que corre;
`correcciones_aplicadas_por_referencia` solo difiere en qué versión de
`marco-M-sorteado-v1_X.tsv` se cita, nunca en la corrección misma;
`cita_p`/`cita_ola_calibracion` toleran la proveniencia GEN2 anexada de §1;
`DIN-M-01` trae en el original dos claves narrativas propias,
`aviso_F_DD`/`razon_DD_marco`, que el emisor genérico no reproduce y que no
tocan `p`/`regla`/`conducta`). **Regla de elección aplicada: solo identidad
de snapshot** — en ningún momento se comparó ninguna celda contra `R` para
decidir si reutilizar o reemitir (`ciego_a_R` verificado: el script jamás
abre `corridas-R/`). Dos corridas frescas del script producen el mismo
contenido sustantivo (difiere solo `fecha_snapshot`, el timestamp de
ejecución — verificado explícitamente, ver `identidad_del_motor` de ambas
corridas comparadas sin ese campo).

| id | archivo fuente (reutilizado) | p |
|---|---|---|
| CIV-M-01 | `M-CIV-M-01.json` | 0.294313 |
| CIV-M-02 | `M-CIV-M-02__v1_2.json` | 0.294313 |
| CIV-M-04 | `M-CIV-M-04__v1_2.json` | 0.294313 |
| CIV-M-10 | `M-CIV-M-10__v1_2.json` | 0.294313 |
| CIV-M-12 | `M-CIV-M-12.json` | 0.294313 |
| CIV-M-13 | `M-CIV-M-13.json` | 0.294313 |
| DIN-M-01 | `M-DIN-M-01__v1_2.json` | 0.174804 |
| FAM-M-01 | `M-FAM-M-01.json` | 0.457707 |
| FAM-M-05 | `M-FAM-M-05__v1_2.json` | 0.045694 |
| FAM-M-06 | `M-FAM-M-06__v1_2.json` | 0.045694 |
| FAM-M-07 | `M-FAM-M-07__v1_2.json` | 0.045694 |
| TRA-M-02 | `M-TRA-M-02__v1_3.json` | 0.085118 |
| TRA-M-03 | `M-TRA-M-03__v1_3.json` | 0.085118 |
| TRA-M-07 | `M-TRA-M-07__v1_3.json` | 0.085118 |

Ningún archivo de `corridas-M/` se creó, editó ni sobrescribió por este
acto — `git status --porcelain -- forense/prereg-duelo-v2/corridas-M/` vacío
en todo momento.

## 3 · P3 · Firewall de objetivo: 14/14 `LIMPIO-DE-OBJETIVO`

Señal mecánica primaria: `grado_DD` (F-DD, `ADR-237`), recomputado en vivo
por celda — `P0 VERIFICACION` (misma encuesta+ola que la calibración de `M`)
habría marcado `CONTAMINADO-POR-OBJETIVO`; **las 14 celdas dan `P1 PUNTUA`**
(la `ola_calibracion` de la conducta que emite `M` es distinta a la
`(encuesta,ola)` que la propia celda evalúa) — cero disparos de `P0`.

Para las 6 celdas de `UR` (`CIV-M-01/02/04/10/12/13`, con árbitro `R`
sellado) se añade la cadena de payload, censada por `F5-contrato-triada-spec-v1_0.md`
§1.4 y verificada de nuevo aquí: `M` calibra `civico.denuncia.miedo_desconfianza`
de `payload_manifiesto_id: envipe2025_csv`; `R` de cada una de las 6 celdas
se computa de `Tmod_Vic.DBF` de **su propia ola** (2012/2013/2015/2021/
2023/2024) — payloads distintos, con no-comparabilidad declarada por
escrito en la propia regla (`milpa/tramite.yaml:488`). Ningún valor
consumido por `M` en estas 6 celdas es el árbitro de esa misma celda ni una
materialización directa de su ola/variable objetivo.

Para las 8 celdas fuera de `UR` (`DIN-M-01`, `FAM-M-01/05/06/07`,
`TRA-M-02/03/07`): no existe `R` sellado (`NO-EXISTE-ARBITRO`, censado por
`universo-triada-v1_0.tsv`) — no hay, por tanto, ningún resultado árbitro
que `M` pudiera haber consumido para esas celdas. El firewall se declara
`LIMPIO-DE-OBJETIVO` **solo por la vía mecánica de F-DD** (calibración de
ola distinta a la ola evaluada); esta verificación **no cierra la pregunta
para siempre** si en el futuro se calcula `R` para alguna de ellas — se
repite entonces contra este mismo snapshot, no se hereda por default (mismo
principio que `F5-contrato-triada-spec-v1_0.md` §1.4 ya declaró para `UR`).

Ninguna celda se etiquetó `CONTAMINADA-POR-OBJETIVO` ni
`INDETERMINADO-POR-PROCEDENCIA`. Ninguna celda queda excluida de `U3` por
este acto (`razon_exclusion` vacía en las 14 filas del snapshot).

## 4 · P4 · Producto sellado

`forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json` — por celda: `id_celda`,
`punto_M` (`p`), `regla`/`conducta`/`clase`/`estado_M`/`ola_calibracion`/
`grado_DD`, `identidad_confirmada` + `divergencias_vs_snapshot_previo` +
`notas_declaradas_no_fatales` (evidencia de §1–2), `corrida_M` (`REUTILIZADA`
en las 14), `archivo_fuente` + su `sha256` + su `fuente`/procedencia
original, `en_UR`, `estado_firewall` + `razon_firewall`, `razon_exclusion`.
Más, a nivel de acto: `identidad_del_motor` completa (§1),
`archivos_abiertos` (ciego a R, verificado), `contador_gen2: "SI"`. No se
calculó ningún error contra `R` en ningún punto del script ni de esta nota.
Este producto puede entregarse a `ENCARGO 5/5` sin volver a abrir `milpa/`.

## 5 · P5 · Sonda de inmutabilidad

Antes y después de correr el snapshot: `git status --porcelain` y
`git diff --stat -- milpa/` **vacíos** en ambos momentos — cero cambios al
perímetro del motor. Los únicos artefactos nuevos de esta sesión son el
encargo archivado (0-bis), el script y el JSON del snapshot, y esta nota —
todos fuera de `milpa/`. Este acto **mide** al motor; no lo modificó.

## 6 · Consistencia con la firma de mesa (overfitting)

Ningún valor adoptado por este acto proviene de `R`: el script nunca abre
`corridas-R/` (verificado, listado en `archivos_abiertos`), la elección
reutilizar/reemitir se decidió únicamente por identidad de snapshot (§2), y
el hallazgo de §1 (remediciones GEN2 `corrida0`) es anterior a este
contrato y no cita ningún resultado del duelo. El motor que compite en
`ENCARGO 5/5` es el motor congelado en este commit.

## Sucesor

`ENCARGO 5/5` — ejecutor de P2 del contrato `F5-CONTRATO-TRIADA` (`U3`,
`MAE_X`, las tres `Δ(A,B)`, la escala de adjudicación), una vez que también
exista el extractor validado (`NC-0143`, componente de adjudicación,
`tools/extrae_l_v1_3.py` ya sellado por `ACTO GEN2-F5-EXTRACTOR-L-v1`).

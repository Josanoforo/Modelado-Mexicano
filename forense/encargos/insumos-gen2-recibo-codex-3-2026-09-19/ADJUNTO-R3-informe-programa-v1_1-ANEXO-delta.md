# Informe del programa v1.1 · ANEXO TÉCNICO · DELTA §A.9–A.13
**Se añade verbatim al final de `canon/informe-programa-v1_0-ANEXO.md`, que se renombra `…-v1_1-ANEXO.md` sin editar §A.1–A.8 (historia correcta para su fecha). Derivado contra `origin/main = 9eff694`, 17/sep/2026, sin corpus. Cada fila: cifra → comando o cita.**

---

## A.9 · Estado del registro al 17/sep, derivado

```
$ python3 tools/corrida0.py status        # 9eff694
N_corridas_requeridas=83
N_corridas_selladas=82
N_resultados_activos=208
N_resultados_sellados=5006
N_resultados_pendientes=208
dependencias_numericas_legacy_activas=184
N_resultados_gen2_sellados=4405
N_resultados_gen2_pendientes_adopcion=12
N_resultados_gen2_vetados_por_decision=2
N_resultados_gen2_adoptados_activos=24
resultados_con_validacion_independiente=215
diferencias_materiales=0
no_corrido_abiertas=109
```

| cifra del informe | valor | comando / cita |
|---|---|---|
| corridas en la vista | 82 | `status` (arriba) |
| CALC en disco con sello | 115 de 120 | `ls -d data/corrida0/CALC-* \| wc -l`; `ls data/corrida0/CALC-*/sello.json \| wc -l` |
| selladas sin fila en la vista | **16** | `for d in data/corrida0/CALC-*/; do n=$(basename $d); [ -f $d/sello.json ] && ! grep -q "$n" data/corrida0/corridas.tsv && echo $n; done \| wc -l` |
| publicadas `REPRODUCE` sin asiento de evidencia | **24** | cruce de `corridas.tsv` (`resultado_replay`) con `forense/replay-evidencia.tsv` (`calc_id`), script en `ADR-540` §P2; asientos totales 77 |
| por qué no se escribe la vista | guardia `REPLAY-PISADO (NC-0094)` | `forense/notas/nota-2026-09-17-gen2-registro-caja-1.md` §P2; reproducido en `…-PILOTO-2-cierre.md` §5 |
| `N_resultados_pendientes = N_resultados_activos` por construcción | 208 = 208 | `tools/corrida0.py:3757`, `:243`; `grep "SATISFECH\|ATENDID\|CUBIERT" tools/corrida0.py` → 0 |
| ADR máximo / conteo | 543 / 543 | `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md \| grep -oE '[0-9]+' \| sort -n \| tail -1`; `grep -cE …` |

## A.10 · Los dos pilotos celda-D

| cifra | valor | fuente sellada |
|---|---|---|
| DIN: celda-D, 8 celdas, reserva | `DIN.ahorro_solo_informal.enif2024.localidad_x_edad` | `data/curacion-registro/celdas-d/…yaml`; `ADR-538` (`PR #849`) |
| DIN: MAE por candidato (pp) | C2 **1.47** · C1 2.64 · C3 (L-solo) 10.64 · C5 emisor 2.3–13.4 | `forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md` §2 |
| DIN: veredicto | `SIN-CANDIDATO-SUPERIOR`, 8/8 `PUNTUADA`, 0 fuera de soporte, `champion_actual: NINGUNO` | ídem §2; yaml de la celda-D |
| DIN: brecha D9−D7 | máx 0.5 pp | ídem (`BRECHA D9-D7`) |
| TRA: celda-D, 12 celdas, reserva con guardia | `TRA.evade_norma.envipe2025.escolaridad_x_dominio` | yaml; `ADR-542` (`PR #858`); `tests/test_marginales_una_variable.py` |
| TRA: MAE por candidato (pp) | C2 **1.5681** · C7 2.6650 · C6 2.8529 · C1 4.3146 | `forense/notas/2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md` §2.1 |
| TRA: interacciones inestables | `I₂₄` 4/12 y `I₂₃` 5/12 con IC que excluye 0; `S1xD2` cambia de signo (−0.250 → +0.014) | ídem §2 |
| TRA: soporte | `n₂₀₂₅` 769–13 858; `n₂₀₂₄` 859–12 116 | ídem §2.1 |
| control de reproducción | `|Δp|` máx 4.79e-07 (TRA); deltas 1e-4–1e-3 con causa a la fila (DIN, exclusión `EDAD` 98) | ídem §3.3 (DIN), §3 (TRA) |
| reservas consumidas | `localidad × edad` ENIF 2024 (piloto); `escolaridad × dominio` ENVIPE 2025 (piloto); `edad × dominio` ENVIPE 2025 **sin piloto** | `NC-0328`; `ADR-542` §9 |
| capturas L bajo spec superada | 18, checkpoint `SUPERADO-POR-SPEC`, no borradas | `ADR-538` (rama del piloto 1, commits 3422a30…3385ea5) |

## A.11 · Régimen de estimación por celda: M1, emisor, crosswalk, capa E1

| cifra | valor | fuente sellada |
|---|---|---|
| M1 precisada (rama B) | la matriz compone, no estima; `g()` por generador | `ADR-531` (`PR #822`); `data/corrida0/decisiones.tsv` objeto `M1:ADR-91` (2 filas: 17/ago histórica, 17/sep) |
| emisor = árbitro | **89 IDÉNTICO** / 3 INDEPENDIENTE / 5 SIN-CONTRAPARTE de 97 | `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv`, columna `veredicto`; `ADR-536` |
| líneas «copiada verbatim» en el emisor | 12 | `grep -c "copiada verbatim" milpa/tramite.yaml` |
| emisor fuera del marcador | `FP-383` FIRMADA | `forense/firmas-pendientes.tsv`; `decisiones.tsv` objeto `marcador:emisor-fuera` |
| crosswalk de ejes | 1 `EQUIVALENTE` (edad) · 2 `MAPEO-N-A-1` (localidad, formalidad) · 1 `NO-EQUIVALENTE` (dominio) · 11 `SIN-CORRESPONDENCIA` | `awk -F'\t' 'NR>1{print $12}' data/crosswalk-ejes-arbitro-modelo-v1_0.tsv \| sort \| uniq -c`; `FP-376`, `ADR-530`, `ADR-537` |
| celdas del árbitro por eje / con celda del modelo vía `edad` | 74 / 16 | `n_celdas_total_arbitro` en la fila `edad` del crosswalk; `MARCADOR-C0-D` §6 |
| `formalidad` no es identidad | árbitro corta por ENIF `P3_13` sobre quien trabaja (cobertura 0.6897) | fila `formalidad` del crosswalk; `FP-376` (3) |
| capa E1: 43 θ | 24 `AUSENCIA_DE_FACTO` · 8 `AUSENCIA_DECLARADA` · 4 `ASOCIACION-MEDIDA·*` · **0** `ARGUMENTO_EXPLICITO` | `milpa/theta-esquema-e1-v1_0.yaml`, campo `identificacion` (yaml.safe_load, conteo); `ADR-535`; test `tests/test_theta_esquema_e1.py` |
| dispersión | 15 familias `NO-DECLARADA` (no 90 parámetros) | ídem, sección `dispersion:`; `modelo-decision-v4_0.md:806` |
| F6 / FP-374 | `VENCIDA-EN-ALCANCE`; 0 familias elegibles (R01 `CANDIDATO-NO-ELEGIBLE`, R09 `CONDICIONADA`) | `forense/firmas-pendientes.tsv` FP-374; `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/tarjetas.yaml:125,128` |
| D-A | sellada | `data/corrida0/CALC-TRIADA-B-PISO-0001/` |

## A.12 · La firma del 17/sep y el marcador (insumos de dirección, citados por sha)

| objeto | sha256 (16) | qué fija |
|---|---|---|
| Firma «el piso no vencido es el estimador adjudicado» + delta v1.1 del marcador | `248dd77af9804282` | adopción de las 20 celdas; retadores como credencial |
| Diseño del marcador v1.0 | `dc66b3b73fba0346` | tabla derivada, dos pisos, estados, tres guardias |
| cuatro números del marcador, derivados sin medir | 117 celdas (97 + 20) · 20 evaluadas · 0 con valor añadido · 20 adoptadas · 74 `SIN-PISO` | 97: censo `ADR-536`; 20: dos yaml; 0: veredictos `SIN-CANDIDATO-SUPERIOR`; 74: crosswalk (`n_celdas_total_arbitro` por eje, suma) y censo (0 `MISMO-INSTRUMENTO-OTRA-OLA`) |
| pisos por eje construibles | ≈40 de 74 (ENVIPE 2024: 13 + 2; ENCIG 2023: 10; ENIF 2021: ≈14 sin `formalidad`) | ejes por entrada en `milpa/tramite-ola5-propuesta-v0.yaml` (`_ejes_`); olas en `data/manifiesto.yaml`; `P3_13` ausente en 2021 (`ADR-538` §4) |

**Estos insumos no están en el árbol al escribirse esto** (viven en `forense/notas/insumos-direccion/` cuando el acto que selle esta versión los archive). Hasta entonces son procedencia tipo 3 y se citan como tales, con sha.

## A.13 · Negativos de este informe, con su universo (A.13)

| negativo | universo examinado | comando |
|---|---|---|
| ningún piso por eje sellado | `data/corrida0/` (120 CALC) | `ls data/corrida0/ \| grep -i "ejes\|piso\|persist"` → solo `CALC-TRIADA-B-PISO-0001` |
| ninguna herramienta ni tabla del marcador por segmento | `tools/`, `data/`, `forense/` | `ls tools/ \| grep -i marcador` → 0; `ls data/ forense/ \| grep -i marcador` → 0 |
| ningún cruce `escolaridad × dominio` derivado antes del piloto 2 | 4 762 archivos md/tsv/yaml/json (sin `.git`, sin `data/raw`) | `grep -rln "escolaridad_proxy × dominio\|escolaridad × dominio\|…"` → 0 |
| FP-379 y FP-385 sin fila en `decisiones.tsv` | `data/corrida0/decisiones.tsv` (123 filas) | `grep -c "FP-379\|FP-385\|nueve"` → 0 |
| ninguna θ con `ARGUMENTO_EXPLICITO` | `milpa/theta-esquema-e1-v1_0.yaml` (43 entradas) | conteo del campo `identificacion` |

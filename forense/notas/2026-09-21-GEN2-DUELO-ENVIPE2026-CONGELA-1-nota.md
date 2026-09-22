# Nota de cierre · GEN2-DUELO-ENVIPE2026-CONGELA-1

**Acto:** GEN2-DUELO-ENVIPE2026-CONGELA-1 (PARTE A del encargo dual) · **Fecha:** 21/sep/2026 · **Entorno:** CAJA (`ENTORNO-DERIVADO = CAJA`, corpus montado, 436 archivos examinados) · **Rama:** `acto/gen2-duelo-envipe2026-congela-1` · **Sonnet 5, sin sub-agentes.**

**Premisas verificadas.** `[EJECUTADO]` `envipe2026_csv` en `data/manifiesto.yaml:30381` con `sha256 dd79f589…`, `descargado_por: agente` 2026-09-21 (PR #977) — confirmado. `[LEÍDO]` `congelado: NO` en línea 16 de los dos `spec.yaml` sobre `origin/main` (`6901853c`) — confirmado, coincidía verbatim con la cita del encargo antes de editar.

**Objetivo cumplido.** `corrida0 preflight CALC-DUELO-ENVIPE2026-EMISIONES-0001` sobre el commit final (`03100ee6`, `origin/main` fusionado, 0 commits de diferencia):

```
[COINCIDE] envipe2026_csv  origen=manifiesto  raiz=data_raw
          sha256 esperado = dd79f589eb6ed7d3675cc86e21ac9bbdbf269913963091d8698d6e28e0540a17
          sha256 actual   = dd79f589eb6ed7d3675cc86e21ac9bbdbf269913963091d8698d6e28e0540a17
...
PRE-FLIGHT: VERDE
```

`CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` sobre el mismo commit:

```
PRE-FLIGHT: BLOQUEADO input_repo_ausente=emisiones_selladas:.../resultados.json input_repo_no_commiteado=emisiones_selladas
```

— exactamente los bloqueos de las emisiones aún inexistentes que el criterio de «hecho» del encargo preveía; ningún otro bloqueo.

**Única edición.** El campo `congelado` pasó de `NO` a `SI` en los dos `spec.yaml` (commit `03100ee6`), citando esta salida cruda. Nada más se tocó en los CALC, la spec humana ni el `.py`.

**NC ya cerrada por otro acto.** `NC-260921-GEN2-DUELO-ENVIPE2026-COMMIT-1-8796-01` («congelar cuando el payload entre») ya está `CERRADA` — la cerró `ACTO GEN2-ADQUIERE-ENVIPE2026-ENIGH2024-1` (PR #977) al lograr el preflight VERDE, declarando el COMMIT-1 "CONGELADO según D-22 ampliada" en sustancia, pero su propio ADR dice explícitamente "ninguna otra edición a esos CALC": no tocó el campo `congelado` de los `spec.yaml`. Este acto hace exactamente esa edición literal, diferida a la PARTE A de este encargo dual — no reabre ni re-cierra la NC.

**PARTE B (`GEN2-DUELO-ENVIPE2026-COMMIT-2-3-1`) no corre en este acto** — es de otra sesión por diseño explícito del encargo (F3: quien congela no ejecuta). Ver `## NO-CORRIDO / RESERVAS` del encargo archivado.

**Suite:** `tests/check.py --rapido` VERDE (ver commit de cascada).

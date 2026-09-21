# ACTO GEN2-TUBERIA-CI-MEDICION-1 · nota de cierre

**Encargo archivado (A.3):** `forense/encargos/2026-09-21-GEN2-TUBERIA-CI-MEDICION-1.md`, 0-bis `dc8c2357`, sello de cuerpo `b84267808615418bb4cbff9805cd114eb755765c501ad0912825d6d18e5f948e`.
**SHA de redacción del encargo:** `13129c05`. **SHA al abrir la rama:** `8535a977` (origin/main se había movido; no fue PARO). **SHA tras fusionar main durante el cierre:** `6b898108`.
**Entorno:** CAJA, `gh auth status` logueado como `Josanoforo`, `gh api rate_limit` → `core.limit=5000` (no 60 — confirma que no corre en la nube). Cero microdato: este acto no abre `data/raw`.
**Modo:** ABIERTO. **Compuerta:** ninguna (no abre dato, no congela spec, no adopta, no borra — D-20). **CONTADOR:** `cuenta_gen2 = NO`.

---

## 0 · ARRANQUE (Bloque D, ejecutado por `/acto`)

Worktree nuevo `/home/pc0/mm-gen2-tuberia-ci-medicion-1` sobre `origin/main` fresco (`git worktree add`). `data/raw` ausente — no hace falta (este acto no abre microdato, lo declara y salta el punto). Guard 0.c: rótulo `tuberia-ci-medicion` ausente en `git ls-remote --heads origin`, en `git worktree list` y en `gh pr list --search "tuberia-ci-medicion" --state open` — sin duplicado. `python3 tools/limpia_arbol.py --reporta` (0.d, informativo): 12 worktrees vivos, 10 ramas locales ya fusionadas y vivas, base al día. Rama creada y empujada de inmediato con el 0-bis.

## 1 · Objeto del acto

Medir, con datos reales de la API de GitHub Actions (sólo lectura, ningún workflow relanzado/cancelado/disparado), lo que nadie había medido todavía: cuánto tarda el CI por corrida/job/paso, cuánto tarda cada test de `tests/check.py` en el runner, qué ha fallado alguna vez en CI (y si fue en rama de PR o en `main`), cuánto espera cada PR fusionado desde el 18/sep, y construir con esa evidencia una lista de mantener/abaratar/eliminar para los 53 tests de `check.py`, los 37 pasos de `verify.yml`, los 17 pasos de la cascada de `/acto` y los 44 archivos de test no cableados.

**El detalle completo, con cada cifra y el comando que la produjo, vive en el informe** — este documento no lo repite: [`forense/analisis/ci-medicion-1/INFORME-ci-medicion-1-v1_0.md`](../analisis/ci-medicion-1/INFORME-ci-medicion-1-v1_0.md). Resumen de lo medido:

- **P1** (universo): 330 corridas de `verify.yml` desde el 18/sep, 330/330 leídas.
- **P2** (jobs/pasos): `verify.yml` cambió de arquitectura de jobs 3 veces en la ventana medida (18 commits al archivo desde el 18/sep) — corrigió una mezcla de eras del análisis inicial agrupando por la firma real de jobs de cada corrida, no por nombre (un job `check` monolítico viejo y un job `check` de compuerta rápida de hoy comparten nombre y no comparten nada más). Corrida completa: mediana 198s/p90 286s. `adicionales` (no `suite`) es hoy el job más lento en paralelo.
- **P3** (tests en runner): 283/283 logs leídos. Instrumentación `[tiempo]` por test sólo existe desde el commit `01b35f9f` (PR #901, 20/sep ~02:00 UTC) — 140 corridas cubiertas para el desglose test-por-test, declarado (A.13). T16 y T32 son los tests más caros del runner.
- **P4** (espera por PR): 83 PR fusionados desde el 18/sep (TUBERÍA midió 78 — la diferencia son PR fusionados entre esa medición y ésta), 83/83 con corrida indexada.
- **P5** (barrido): 151 filas, 1 ELIMINAR (T16, decisión ya tomada por dirección — este acto sólo aporta la evidencia), 2 ABARATAR (paso "marcador por segmento" a job propio; paso 1 de la cascada de `/acto`), 6 FUERA-DE-ALCANCE (reglas de contenido §3, excluidas por el encargo), 8 DEFECTO-ABIERTO-NO-SE-TOCA-AQUI (los FALLA-DE-VERDAD del censo, PARO de este acto prohíbe tocarlos), el resto MANTENER.
- **P6** (metas de dirección): ninguna de las cinco se cumple hoy en el runner — el falsador del encargo (§10) no se dispara.

## 2 · Hallazgos declarados (no bloquean, se anotan)

1. La premisa de TUBERÍA "54 tests, incluido T16" no calza: son 53 (52 registrados + T16 condicional). Verificado mecánicamente (`awk '/^def main/,/^if __name__/' tests/check.py`).
2. La premisa "134 archivos" del censo no calza: son 135 (91 CORRE-EN-CI + 36 NECESITA-DEPENDENCIA + 8 FALLA-DE-VERDAD).
3. `verify.yml` cambió de arquitectura de jobs 3 veces en 3 días — contextualiza por qué "cuánto tarda el CI" no tiene una sola respuesta esta semana; fuera de perímetro de este acto (no se toca `verify.yml`).

Ninguno de los tres cambia qué se mide ni exige PARO; se declaran y se sigue (§2 instrucciones-proyecto, "premisa falsa no es, por sí sola, PARO").

## 3 · Perímetro

Escrito en: `forense/analisis/ci-medicion-1/` (43 archivos: scripts de un solo uso, TSV con universo y conteo declarado, JSON crudo de `gh api`, el informe), `forense/encargos/` (0-bis), `forense/notas/` (esta nota), más la cascada de gobernanza. No se tocó `tests/`, `.github/workflows/`, `.claude/commands/`, `tools/`, `data/`, `milpa/` ni ningún CALC — verificado con `git diff --stat origin/main...HEAD` antes de cerrar.

## 4 · Anti-PR#77

No aplica: este acto no descargó ningún payload de corpus/microdato. Los `gh api` que descargó (runs, jobs, logs de CI) están en `forense/analisis/ci-medicion-1/` del propio repo, no en un corpus compartido aparte.

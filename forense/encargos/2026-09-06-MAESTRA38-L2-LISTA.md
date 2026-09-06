# ENCARGO · ACTO MAESTRA38-L2-LISTA · MPS-2012 LISTA DE PRIMERA MANO

*Archivado verbatim por A.3 (0-bis) — no se edita en ningún otro punto.*

---

ENCARGO · ACTO MAESTRA38-L2-LISTA · MPS-2012 LISTA DE PRIMERA MANO — caja, Opus, invoca /acto

SHA a5350e59 · COMPUERTA: N15 fusionado. Entra en la cola de caja donde mesa lo ponga (candidato: después de LAPOP, antes de ENSANUT — es corto y mide). COMMIT-1 = citar S10 y su sha. COMMIT-2: (a) git clone --depth 1 https://github.com/SensitiveQuestions/list fuera del sandbox; verificar git rev-parse HEAD = e088e5f… y sha256 de data/mexico.tab = fe1014…c04488 (si difiere: A.7, registrar los dos y reportar qué cambió); (b) registrar data/mexico.tab + man/mexico.Rd por las tres capas, raíz descargas_mx/ACADEMICO-list-cran/, url_origen = repo + commit, hermana en aliases-fuentes.tsv de ICPSR_35024 (firma A.7 de mesa: se pide aquí); (c) medir según S10; (d) B, si el tiempo alcanza: /adquiere sobre los dos DOI de Dataverse (≥4 rutas, salida cruda; NO-OBTENIDO sólo con las cuatro), sin medir nada de ellos en este acto; (e) enmienda append a FP-263: «P3 medido de primera mano en subconjunto; (i)-(ii) siguen dependiendo del .dta completo». PERÍMETRO: manifiesto (+2, +N si Dataverse) · staging · aliases-fuentes (1 fila) · data/l2lista-* · propuesta (append, entrada nueva junto a L12, no edita las suyas) · notas · hallazgos · tablero · A.3 · cascada. NO toca: milpa/tramite.yaml · canon (salvo ADR) · specs S1–S9 · salidas de L12 · L2 (sigue gateado a A4). Si te encuentras escribiendo fuera de esta lista, PARA. CONTADOR: piezas de L12 con dato de primera mano 0 → 1 (P3) · payloads +2 (+N) · medición: sí.

---

## COMMIT-1 · Spec de caja citada (no editada)

| | |
|---|---|
| **NOMBRE ESTABLE** | `prereg-caja-S10-L2-LISTA` |
| **ARCHIVO** | `forense/prereg-caja/S10-L2-LISTA-spec-v1_0.md` |
| **sha del blob (git)** | `260847fff9cffd8573b6a8598482242cabd20741` |
| **Introducida por** | `ca45483 ACTO MAESTRA38-N15 · SPEC-L2-LISTA: sella S10-L2-LISTA-spec-v1_0` |
| **Fusionada en `main` por** | `3908484` (PR #550) — `git merge-base --is-ancestor 3908484 origin/main` → sí |

## COMPUERTA · verificada por producto

`COMPUERTA: N15 fusionado`. Rótulo `N15` resuelto sin ambigüedad: `grep -ohE "MAESTRA[0-9]+-N15" -r .` → una sola forma, `MAESTRA38-N15`.

Verificación **por producto**, no por `grep` de asunto de commit (`ADR-277`):

```
$ git cat-file -e origin/main:forense/prereg-caja/S10-L2-LISTA-spec-v1_0.md && echo OK
OK
$ git rev-parse origin/main:forense/prereg-caja/S10-L2-LISTA-spec-v1_0.md
260847fff9cffd8573b6a8598482242cabd20741
$ git merge-base --is-ancestor 3908484 origin/main && echo "SI, fusionado"
SI, fusionado
```

**COMPUERTA CUMPLIDA.**

## ARRANQUE (Bloque D)

| # | Punto | Valor |
|---|---|---|
| 0 | Guard de rama | `git ls-remote --heads origin` → **1 línea** (`main` = `b0c2a80`); cero ramas `acto/*` vivas, cero coincidencias con `L2-LISTA`. Rama creada: `acto/maestra38-l2-lista` |
| 1 | Repo | `/home/pc0/mm-l2-lista` (worktree nuevo sobre `origin/main`) · `b0c2a80 Merge pull request #551` · limpio |
| 2 | SHA | Encargo declara `a5350e59` (PR #549). `origin/main` real = `b0c2a80` (PR #551, LOTE-LAPOP). `git merge-base --is-ancestor a5350e59 origin/main` → sí: main avanzó un merge. **No es PARO** (Bloque D punto 2); perímetro re-derivado contra `b0c2a80` |
| 3 | `data/raw` | **La enlacé** a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiado del clon padre. Control positivo A.13: `find -L data/raw -maxdepth 1 -type f \| wc -l` → **271** |
| 4 | Entorno (A.2, tres partes) | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable` · `curl` INEGI → `200` · `ls data/raw/ \| head -1` → `2005trim1_csv.zip` (corpus montado). Caja Ubuntu — correcta para microdato |
| 5 | Espejo | Toda cifra de este acto sale de `/home/pc0/mm-l2-lista`, con el comando a la vista |

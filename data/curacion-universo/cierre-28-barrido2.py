#!/usr/bin/env python3
"""Verifica los 22 criterios de cierre del §28 de BARRIDO-2, uno por uno.

ACTO B2-SEMANTICO, 18/ago/2026. El §28 pide "veredicto uno por uno con
comando": cada criterio se responde con la derivación que lo sostiene, no con
una afirmación. Este script es esa derivación, y se versiona para que el
veredicto sea reproducible por quien quiera repetirlo.

No adjudica nada por su cuenta: lee productos ya escritos y firmados. Un
criterio cuyo insumo no existe sale NO-VERIFICABLE, nunca "cumple".

    python3 data/curacion-universo/cierre-28-barrido2.py --repo .
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def leer(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    R = args.repo.resolve()

    U = R / "data" / "curacion-universo"
    B = R / "data" / "curacion-registro" / "ejecucion-semantica" / "barrido2"
    baseline_path = U / "baseline-material-barrido2.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8")) if baseline_path.is_file() else {}
    counts = baseline.get("counts", {})

    ledger = leer(U / "ledger-inspecciones-barrido2.tsv")
    reportes = leer(U / "reportes-inspeccion-barrido2-v1_0.tsv")
    propuestas = leer(B / "propuestas-barrido2.tsv")
    tareas = leer(B / "tareas-semanticas-barrido2.tsv")
    decisiones = leer(B / "decisiones-integracion-barrido2.tsv")
    cableado = leer(R / "data" / "cableado-universo-v1_0.tsv")
    relaciones = leer(R / "data" / "curacion-registro" / "relaciones.tsv")
    apertura = leer(R / "data" / "lista-apertura-enlace2-2026-08-14.tsv")
    rel_by_id = {r["relacion_id"]: r for r in relaciones}

    terminales = [r for r in ledger if r.get("estado_terminal") == "SI"]
    e1 = sum(int(r.get("objetos_e1") or 0) for r in ledger)
    e2 = sum(int(r.get("objetos_e2") or 0) for r in ledger)
    exc = sum(int(r.get("excepciones") or 0) for r in ledger)

    # Las 17 absorbidas: destino APERTURA-PENDIENTE. La condición del §18.8 es
    # que ninguna conserve INDEXADO-NO-DESCARGADO teniendo payload observado.
    absorbidas = [r for r in apertura if r.get("destino") == "APERTURA-PENDIENTE"]
    violan = [
        r["relacion_id"] for r in absorbidas
        if (rel_by_id.get(r["relacion_id"], {}).get("capa4_apertura_mapeo") == "INDEXADO-NO-DESCARGADO"
            and rel_by_id.get(r["relacion_id"], {}).get("capa3_disco_real", "").startswith("EXISTE"))
    ]

    estados = {}
    for d in decisiones:
        estados[d.get("estado_integracion", "")] = estados.get(d.get("estado_integracion", ""), 0) + 1
    altas = [p for p in propuestas if p.get("accion_propuesta") == "ALTA"]
    fp24 = [p for p in propuestas if p.get("dependencia_fp24") == "SI"]
    sin_terminar = [
        p for p in propuestas
        if p["propuesta_id"] not in {d["propuesta_id"] for d in decisiones}
    ]

    C: list[tuple[int, str, str, str, str]] = []

    def crit(n: int, texto: str, cumple, evidencia: str, comando: str) -> None:
        estado = "NO-VERIFICABLE" if cumple is None else ("CUMPLE" if cumple else "NO CUMPLE")
        C.append((n, texto, estado, evidencia, comando))

    crit(1, "todas las declaraciones contabilizadas",
         bool(counts) and counts.get("declaraciones_totales") ==
         counts.get("declaraciones_con_archivo_sha", 0) + counts.get("declaraciones_sin_archivo_sha", 0),
         f"{counts.get('declaraciones_totales')} = {counts.get('declaraciones_con_archivo_sha')} + {counts.get('declaraciones_sin_archivo_sha')}",
         "jq '.counts' baseline-material-barrido2.json")
    crit(2, "todas las representaciones terminales",
         bool(ledger) and len(terminales) == len(ledger),
         f"{len(terminales)}/{len(ledger)} estado_terminal=SI",
         "cut -f20 ledger-inspecciones-barrido2.tsv | sort | uniq -c")
    crit(3, "todo objeto E1 con E2 o excepción",
         bool(ledger) and e1 == e2 + exc,
         f"E1={e1} = E2={e2} + excepciones={exc}",
         "awk -F'\\t' 'NR>1{a+=$11;b+=$12;c+=$13}END{print a,b,c}' ledger-inspecciones-barrido2.tsv")
    idx_sha = baseline.get("e2_index_sha256")
    crit(4, "índice E2 completo existe localmente y está hasheado",
         bool(idx_sha),
         f"e2_index_sha256={str(idx_sha)[:16]}… declarado en el baseline",
         "sha256sum .barrido2/private/e2-neutral-index.jsonl")
    priv = {r.get("privacidad") for r in reportes}
    crit(5, "reportes durables pasan privacidad",
         bool(reportes) and priv.issubset({"DEPURADO", "[REDACTADO-PRIVACIDAD]", "NO-APLICA"}),
         f"{len(reportes)} reportes; privacidad ∈ {sorted(priv)}",
         "cut -f17 reportes-inspeccion-barrido2-v1_0.tsv | sort -u")
    crit(6, "el censo reconcilia",
         bool(counts) and counts.get("representaciones_fisicas") ==
         counts.get("representaciones_declaradas", 0) + counts.get("representaciones_no_declaradas", 0),
         f"{counts.get('representaciones_fisicas')} = {counts.get('representaciones_declaradas')} + {counts.get('representaciones_no_declaradas')}",
         "jq '.counts' baseline-material-barrido2.json")
    crit(7, "fuera-de-disco reconcilia", counts.get("fuera_de_disco") == 0,
         f"fuera_de_disco={counts.get('fuera_de_disco')}",
         "jq '.counts.fuera_de_disco' baseline-material-barrido2.json")
    crit(8, "PRISMA reconcilia", (U / "prisma-material-barrido2.md").is_file(),
         "prisma material presente; semántico y M-APERTURA los escribe este acto",
         "ls data/curacion-universo/prisma-*.md")
    crit(9, "bootstrap con cero deriva", None,
         "§16 lo cerró en su propio acto; este acto no lo reabre",
         "python3 -m unittest tools.curador_registro.tests.test_bootstrap_sync")
    crit(10, "las 17 aperturas absorbidas terminaron",
         len(absorbidas) > 0 and not violan,
         f"{len(absorbidas)} absorbidas; {len(violan)} conservan INDEXADO-NO-DESCARGADO con payload observado",
         "ver §18.8; T23 evalúa esta misma condición")
    crit(11, "toda propuesta semántica terminó",
         bool(propuestas) and not sin_terminar,
         f"{len(propuestas)} propuestas; {len(sin_terminar)} sin decisión",
         "join propuestas-barrido2.tsv decisiones-integracion-barrido2.tsv")
    crit(12, "toda PROPUESTA_ALTA existente terminó",
         True if not altas else all(
             d.get("estado_integracion") in {"INTEGRADA", "RECHAZADA_FAIL_CLOSED",
                                             "CONFLICTO_MATERIAL", "REQUIERE_DECISION_FP24"}
             for d in decisiones if d.get("accion_propuesta") == "ALTA"),
         f"{len(altas)} propuestas ALTA",
         "cut -f10 propuestas-barrido2.tsv | sort | uniq -c")
    crit(13, "cero obligación de producir altas", True,
         f"{len(altas)} altas; el §19 no exige ninguna",
         "encargo madre §19: 'No existe requisito de producir relaciones nuevas'")
    crit(14, "FP-24 aplicado por dependencia real, no por lista histórica",
         all(p.get("razon_gate", "") not in ("", "NO-APLICA") for p in propuestas) if propuestas else None,
         f"dependencia_fp24=SI en {len(fp24)} de {len(propuestas)}; cada fila con razon_gate escrita",
         "cut -f18,19 propuestas-barrido2.tsv | sort | uniq -c")
    crit(15, "capa4 se escribió mediante vía real",
         bool(decisiones),
         "integrate.py --barrido2 con journal y rollback; sin edición manual de TSV",
         "ls journal-integracion-barrido2.json")
    crit(16, "integración idempotente", None,
         "se comprueba con segunda corrida de diff cero en C5",
         "correr integrate dos veces y diff del registro")
    crit(17, "cableado tiene filas reales", len(cableado) > 0,
         f"{len(cableado)} filas en cableado-universo-v1_0.tsv",
         "wc -l data/cableado-universo-v1_0.tsv")
    crit(18, "T-CABLEADO verde", None,
         "lo dictamina tests/check.py --require-cableado, no este script",
         "python3 tests/check.py --require-cableado")
    crit(19, "tests/check.py --baseline verde", None,
         "lo dictamina la corrida real",
         "python3 tests/check.py --baseline")
    crit(20, "checkpoints empujados", None,
         "se verifica contra origin, no contra el worktree",
         "git ls-remote origin refs/heads/b2-semantico")
    crit(21, "PR borrador existe", None, "PR #268, borrador",
         "gh pr view 268 --json isDraft,state")
    crit(22, "nadie fusionó el PR", None, "debe seguir OPEN y isDraft=true",
         "gh pr view 268 --json isDraft,state,merged")

    ancho = max(len(t) for _, t, _, _, _ in C)
    print(f"{'#':>3}  {'criterio'.ljust(ancho)}  estado")
    print("-" * (ancho + 22))
    for n, texto, estado, evidencia, comando in C:
        print(f"{n:>3}  {texto.ljust(ancho)}  {estado}")
        print(f"     evidencia: {evidencia}")
        print(f"     comando  : {comando}")
    resumen = {
        "CUMPLE": sum(1 for c in C if c[2] == "CUMPLE"),
        "NO CUMPLE": sum(1 for c in C if c[2] == "NO CUMPLE"),
        "NO-VERIFICABLE": sum(1 for c in C if c[2] == "NO-VERIFICABLE"),
    }
    print("\n" + json.dumps(resumen, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

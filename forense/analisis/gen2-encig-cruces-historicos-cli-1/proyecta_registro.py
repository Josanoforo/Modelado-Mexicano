#!/usr/bin/env python3
"""Proyecta sólo los dos CALC ENCIG propios; preserva todas las filas ajenas."""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools import corrida0 as C  # noqa: E402


CALCS = {
    "CALC-ENCIG2023-CRUCES-HISTORICOS-0002",
    "CALC-ENCIG2021-CRUCES-HISTORICOS-0003",
}


def _merge(current: list[dict], proposed: list[dict], key: str) -> list[dict]:
    old = {row[key]: row for row in current}
    additions = []
    for row in proposed:
        serialized = {field: str(value) for field, value in row.items()}
        prior = old.get(row[key])
        if prior is not None:
            if prior != serialized:
                raise SystemExit(f"fila propia previa contradictoria: {key}={row[key]}")
            continue
        additions.append(serialized)
    return current + additions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--escribe", action="store_true")
    args = parser.parse_args()
    derived = C._filas_registro(verifica=False)
    selected_runs = [row for row in derived["corridas"] if row["spec_id"] in CALCS]
    if {row["spec_id"] for row in selected_runs} != CALCS or len(selected_runs) != 2:
        raise SystemExit("la derivación no contiene exactamente los dos CALC autorizados")
    run_ids = {row["corrida_id"] for row in selected_runs}
    selected_results = [row for row in derived["resultados"] if row["corrida_id"] in run_ids]
    declared = sum(int(row["n_resultados"]) for row in selected_runs)
    if len(selected_results) != declared:
        raise SystemExit(f"cardinalidad RESULT no coincide: {len(selected_results)} != {declared}")
    result_ids = {row["resultado_id"] for row in selected_results}
    selected_uses = [row for row in derived["usos"]
                     if row["corrida0_resultado_id"] in result_ids]
    if selected_uses:
        raise SystemExit("PARO: estos CALC no autorizan adopción ni usos activos")

    current_runs = C._leer_tsv_derivado(C.VISTA_CORRIDAS)
    current_results = C._leer_tsv_derivado(C.VISTA_RESULTADOS)
    current_uses = C._leer_tsv_derivado(C.VISTA_USOS)
    projected_runs = _merge(current_runs, selected_runs, "corrida_id")
    projected_results = _merge(current_results, selected_results, "resultado_id")
    projected_uses = list(current_uses)
    if args.escribe:
        C._escribe(C.VISTA_CORRIDAS, C.COLS_VISTA_CORRIDAS, projected_runs)
        C._escribe(C.VISTA_RESULTADOS, C.COLS_VISTA_RESULTADOS, projected_results)
        C._escribe(C.VISTA_USOS, C.COLS_VISTA_USOS, projected_uses)
        # Las filas ajenas deben sobrevivir como multiconjunto: algunas vistas
        # históricas admiten IDs repetidos, por lo que un índice simple pierde
        # información y produciría un falso positivo.
        for path, before in (
            (C.VISTA_CORRIDAS, current_runs),
            (C.VISTA_RESULTADOS, current_results),
            (C.VISTA_USOS, current_uses),
        ):
            after = C._leer_tsv_derivado(path)
            columns = list(before[0]) if before else []
            old_multiset = Counter(tuple(row[column] for column in columns) for row in before)
            new_multiset = Counter(tuple(row[column] for column in columns) for row in after)
            if any(new_multiset[row] < count for row, count in old_multiset.items()):
                raise SystemExit(f"PARO: cambió una fila ajena en {path}")
    print(f"corridas_propias={len(selected_runs)}")
    print(f"resultados_propios={len(selected_results)}")
    print(f"usos_propios={len(selected_uses)}")
    print(f"escribe={'SI' if args.escribe else 'NO'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

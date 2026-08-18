#!/usr/bin/env python3
"""Corredor de olas para la reejecución E2 de BARRIDO-2 (generación v7).

Efímero a propósito: no entra a tools/ porque la lista cerrada de ADR-92(a) no
lo incluye. El comando exacto que ejecuta por tarea queda declarado en el PRISMA.

Respeta la concurrencia del §10 del encargo: W1 máx 3, W2 máx 3 (PDF/XLS máx 2),
W3 máx 2, W4 1. Cada tarea corre en su propio proceso bajo `unshare -Urn`.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path("/home/pc0/Modelado-Mexicano-barrido2")
LEDGER = REPO / ".barrido2/private/t0/ledger-v7.tsv"
TASKS = REPO / ".barrido2/tasks-v7"
STAGING = REPO / ".barrido2/staging-v7"
CONTRATO = REPO / "data/curacion-universo/contrato-barrido2-v1_0.json"
RAICES = REPO / "data/raices.local.yaml"
BITACORA = Path(__file__).with_name("olas-v7.log")
RESUMEN = Path(__file__).with_name("olas-v7-resumen.json")

CONCURRENCIA = {"W1": 3, "W2": 2, "W3": 2, "W4": 1}


def registra(mensaje: str) -> None:
    linea = f"{time.strftime('%H:%M:%S')} {mensaje}"
    with BITACORA.open("a", encoding="utf-8") as handle:
        handle.write(linea + "\n")
    print(linea, flush=True)


def corre(tarea_id: str) -> tuple[str, bool, str]:
    destino = STAGING / tarea_id
    proceso = subprocess.run(
        [
            "unshare", "-Urn", "--", sys.executable, "-m",
            "tools.curador_registro.inspect_assets", "--barrido2-inspect",
            "--task", str(TASKS / f"{tarea_id}.json"),
            "--roots-config", str(RAICES),
            "--contract", str(CONTRATO),
            "--staging-dir", str(destino),
        ],
        cwd=REPO, capture_output=True, text=True, timeout=2400,
    )
    if proceso.returncode != 0:
        return tarea_id, False, (proceso.stderr or proceso.stdout)[-400:]
    return tarea_id, True, ""


def main() -> int:
    with LEDGER.open(encoding="utf-8-sig", newline="") as handle:
        filas = list(csv.DictReader(handle, delimiter="\t"))
    por_ola: dict[str, list[str]] = {}
    for fila in filas:
        por_ola.setdefault(fila["wave_initial"], []).append(fila["tarea_id"])
    resultado: dict[str, object] = {"olas": {}, "fallas": []}
    inicio = time.time()
    for ola in ("W1", "W2", "W3", "W4"):
        tareas = sorted(por_ola.get(ola, []))
        if not tareas:
            continue
        registra(f"=== {ola}: {len(tareas)} tareas, concurrencia {CONCURRENCIA[ola]}")
        ok = fallo = 0
        arranque = time.time()
        with ThreadPoolExecutor(max_workers=CONCURRENCIA[ola]) as pool:
            for indice, (tarea_id, bien, error) in enumerate(pool.map(corre, tareas), 1):
                if bien:
                    ok += 1
                else:
                    fallo += 1
                    resultado["fallas"].append({"ola": ola, "tarea_id": tarea_id, "error": error})
                    registra(f"    FALLA {tarea_id}: {error[:160]}")
                if indice % 25 == 0 or indice == len(tareas):
                    registra(f"    {ola} {indice}/{len(tareas)} · ok={ok} falla={fallo} · {time.time()-arranque:.0f}s")
        resultado["olas"][ola] = {"tareas": len(tareas), "ok": ok, "falla": fallo,
                                  "segundos": round(time.time() - arranque)}
    resultado["segundos_total"] = round(time.time() - inicio)
    RESUMEN.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    registra(f"=== FIN · {json.dumps(resultado['olas'], ensure_ascii=False)} · fallas={len(resultado['fallas'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

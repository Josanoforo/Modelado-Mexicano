#!/usr/bin/env python3
"""Re-inspecciona la muestra adversarial congelada y la compara POR HASH.

Qué prueba, dicho sin adorno: que el inspector es **reproducible**. Se vuelve a
correr cada tarea de la muestra en un staging aparte, con el mismo módulo y el
mismo contrato, y se comparan `report_sha256` e `index_sha256` contra el
expediente sellado. Si un par no coincide, la evidencia del expediente no es
derivable del material y aplica el protocolo del §12 —cuarentena del parser,
ampliar la muestra, repetir el lote—, no el pánico.

Lo que NO prueba: que el contenido sea semánticamente correcto. Una inspección
puede ser perfectamente reproducible y estar equivocada. Reproducibilidad es la
exigencia 4 del §15, y es lo único que este comparador cierra.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/pc0/Modelado-Mexicano-barrido2")
MUESTRA = REPO / "data/curacion-universo/muestra-adversarial-barrido2.tsv"
SELLADO = REPO / ".barrido2/staging-v7"
TASKS = REPO / ".barrido2/tasks-v7"
CONTRATO = REPO / "data/curacion-universo/contrato-barrido2-v1_0.json"
RAICES = REPO / "data/raices.local.yaml"


def reinspecciona(tarea_id: str, destino: Path) -> tuple[bool, str]:
    proceso = subprocess.run(
        ["unshare", "-Urn", "--", sys.executable, "-m",
         "tools.curador_registro.inspect_assets", "--barrido2-inspect",
         "--task", str(TASKS / f"{tarea_id}.json"),
         "--roots-config", str(RAICES), "--contract", str(CONTRATO),
         "--staging-dir", str(destino)],
        cwd=REPO, capture_output=True, text=True, timeout=2400,
    )
    if proceso.returncode != 0:
        return False, (proceso.stderr or proceso.stdout)[-300:]
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--staging-verificacion", type=Path, required=True)
    args = ap.parse_args()
    raiz = args.staging_verificacion.resolve()
    raiz.mkdir(parents=True, exist_ok=True)

    with MUESTRA.open(encoding="utf-8-sig", newline="") as handle:
        muestra = list(csv.DictReader(handle, delimiter="\t"))

    filas: list[dict[str, object]] = []
    for fila in muestra:
        tid = fila["tarea_id"]
        ok, error = reinspecciona(tid, raiz / tid)
        if not ok:
            filas.append({"ola": fila["ola"], "tarea_id": tid, "payload_id": fila["payload_id"],
                          "veredicto": "NO-REINSPECCIONABLE", "detalle": error})
            continue
        a = json.loads((SELLADO / tid / "resumen.json").read_text(encoding="utf-8"))
        b = json.loads((raiz / tid / "resumen.json").read_text(encoding="utf-8"))
        coincide = (a.get("report_sha256") == b.get("report_sha256")
                    and a.get("index_sha256") == b.get("index_sha256"))
        filas.append({
            "ola": fila["ola"], "tarea_id": tid, "payload_id": fila["payload_id"],
            "razon_de_seleccion": fila["razon_de_seleccion"],
            "report_sha256_sellado": a.get("report_sha256", "")[:16],
            "report_sha256_reinspeccion": b.get("report_sha256", "")[:16],
            "index_sha256_sellado": a.get("index_sha256", "")[:16],
            "index_sha256_reinspeccion": b.get("index_sha256", "")[:16],
            "build_sellado": a.get("build_sha256", "")[:12],
            "build_reinspeccion": b.get("build_sha256", "")[:12],
            "veredicto": "COINCIDE" if coincide else "NO-COINCIDE",
        })

    from collections import Counter
    conteo = Counter(f["veredicto"] for f in filas)
    print(json.dumps({"muestra": len(filas), "veredictos": dict(conteo),
                      "filas": filas}, ensure_ascii=False, indent=1, sort_keys=True))
    return 0 if conteo.get("COINCIDE", 0) == len(filas) else 1


if __name__ == "__main__":
    raise SystemExit(main())

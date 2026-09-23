"""Congela el inventario mínimo de consumidores U1 pertinentes a U5.

El insumo es un commit explícito de la rama de U1, aún sin fusionar.
No lee microdatos ni copia cifras de sus estimadores al producto regional.
"""
from __future__ import annotations

import csv
import io
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
U1_COMMIT = "3d8e82fb"
U1_PATH = "forense/analisis/catalogo/inventario-consumo-gen2.tsv"
OUT = ROOT / "forense/analisis/region/alcance-u1-v1_0.tsv"
MEASURED = {
    ("ENVIPE", "evade_norma_envipe2025"),
    ("ENVIPE", "cumple_norma_envipe2025"),
    ("ENIF", "tiene_ahorros_enif2024"),
    *(("ENIF", c) for c in (
        "no_tiene_ahorros_enif2024", "informal_cualquiera", "formal_cualquiera",
        "ahorra_solo_informal", "ahorra_solo_formal", "ahorra_ambas_vias", "no_ahorra")),
}
FIELDS = ("instrumento", "conducta_u1", "estados_u1", "result_consumidor_u1",
          "estado_regional_u5", "nota")


def genera():
    p = subprocess.run(["git", "show", f"{U1_COMMIT}:{U1_PATH}"], cwd=ROOT,
                       capture_output=True, check=True, text=True)
    inventario = csv.DictReader(io.StringIO(p.stdout), delimiter="\t")
    grupos = defaultdict(lambda: {"estados": set(), "results": set()})
    for r in inventario:
        inst = r["instrumento_ola"].split()[0]
        if inst not in ("ENVIPE", "ENCIG", "ENIF"):
            continue
        estado = r["estado_adopcion"]
        if estado.startswith(("PISO-HISTORICO", "SELLADO-CONTEXTO")):
            continue
        k = (inst, r["conducta"])
        grupos[k]["estados"].add(estado)
        if r["result_punto"]:
            grupos[k]["results"].add(r["result_punto"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for (inst, conducta), v in sorted(grupos.items()):
            pseudo = conducta == "R" or (len(conducta) == 5 and conducta[2] == "x")
            state = "MEDIDO-REGION" if (inst, conducta) in MEASURED else "PENDIENTE-DICTAMEN-REGIONAL"
            if pseudo:
                state = "IDENTIDAD-CONSUMIDOR-POR-DESDOBLAR"
            nota = ("El código U1 es una identidad de celda/interacción, no una conducta simple; "
                    "requiere vincular su estimando antes de declarar expectativa geográfica."
                    if pseudo else "El piso ENIF 18+ se distingue de la serie histórica 18–70."
                    if inst == "ENIF" and state == "MEDIDO-REGION" else
                    "Última ola o serie regional no medida, salvo estado MEDIDO-REGION.")
            w.writerow(dict(zip(FIELDS, (inst, conducta, ";".join(sorted(v["estados"])),
                                      ";".join(sorted(v["results"])), state, nota))))
    print(f"{len(grupos)} identidades U1, fuente {U1_COMMIT}:{U1_PATH}")


if __name__ == "__main__":
    genera()

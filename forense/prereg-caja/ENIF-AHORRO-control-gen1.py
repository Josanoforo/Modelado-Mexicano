#!/usr/bin/env python3
"""Control positivo POSTERIOR de `ACTO GEN2-LOTE-ENIF-1` contra los 8 GEN1.

Corre DESPUES de sellar `CALC-ENIF-0001`. NO puede tocar el medidor, la spec
ni ningun `RESULT`: solo lee `resultados.json` y emite el veredicto.

`DELTA-VS-GEN1 = medido - sellado`, con signo.
  REPRODUCE      si |delta| <= 1e-6
  NO-REPRODUCE   en otro caso
  NO-COMPARABLE  si el estimando salio NO-ESTIMABLE

A-bis.3 -- SOLO se compara el PUNTO. Fase 1 midio sin diseno y esta corrida
si lo estima: los IC no son comparables y este script no los imprime juntos.

Uso:  python3 forense/prereg-caja/ENIF-AHORRO-control-gen1.py [--json]
"""
from __future__ import annotations

import json
import pathlib
import sys

RES = pathlib.Path("data/corrida0/CALC-ENIF-0001/resultados.json")
UMBRAL = 1.0e-6
P = "RESULT-ENIF-AHO-"

# valores GEN1 sellados, copiados de data/corrida0/demanda-resultados.tsv
GEN1 = {
    "RES-0046": (0.3306,    "A-P-CORTO-SIN"),
    "RES-0047": (0.6694,    "A-P-NOCORTO-SIN"),
    "RES-0048": (0.1734,    "A-P-CORTO-CON"),
    "RES-0049": (0.8266,    "A-P-NOCORTO-CON"),
    "RES-0057": (0.284927,  "B-P-FORMAL"),
    "RES-0058": (0.56192,   "B-P-INFORMAL"),
    "RES-0059": (0.06078,   "C-P-DESCONFIA-CONOCE"),
    "RES-0060": (0.054767,  "C-P-DESCONFIA-NOCONOCE"),
}

# celdas de sensibilidad: el corte de GEN1 en la familia A (P4_10 = {1}).
# Se comparan APARTE, para que la discrepancia del corte primario sea
# ATRIBUIBLE y no misteriosa (spec sellada §5.1).
S1 = {
    "RES-0046": "A-P-CORTO-SIN-S1",
    "RES-0048": "A-P-CORTO-CON-S1",
}


def _valor(d, celda):
    v = d.get(P + celda + "-P")
    if v is None:
        v = d.get(P + celda)
    return v


def main() -> int:
    if not RES.exists():
        print(f"NO-EJECUTABLE · falta {RES}", file=sys.stderr)
        return 2
    bruto = json.loads(RES.read_text())
    d = bruto.get("resultados", bruto)

    filas = []
    for rid, (sellado, celda) in GEN1.items():
        medido = _valor(d, celda)
        if not isinstance(medido, (int, float)):
            filas.append((rid, celda, sellado, medido, None, "NO-COMPARABLE"))
            continue
        delta = float(medido) - sellado
        ver = "REPRODUCE" if abs(delta) <= UMBRAL else "NO-REPRODUCE"
        filas.append((rid, celda, sellado, float(medido), delta, ver))

    sfilas = []
    for rid, celda in S1.items():
        medido = _valor(d, celda)
        sellado = GEN1[rid][0]
        if not isinstance(medido, (int, float)):
            sfilas.append((rid, celda, sellado, medido, None, "NO-COMPARABLE"))
            continue
        delta = float(medido) - sellado
        ver = "REPRODUCE" if abs(delta) <= UMBRAL else "NO-REPRODUCE"
        sfilas.append((rid, celda, sellado, float(medido), delta, ver))

    if "--json" in sys.argv:
        print(json.dumps({
            "umbral": UMBRAL,
            "solo_el_punto": True,
            "nota_a_bis_3": ("fase 1 midio sin diseno; esta corrida si lo "
                             "estima. Los IC no son comparables y no se "
                             "comparan."),
            "primario": [dict(zip(
                ("result", "celda", "gen1", "medido", "delta", "veredicto"),
                f)) for f in filas],
            "sensibilidad_S1": [dict(zip(
                ("result", "celda", "gen1", "medido", "delta", "veredicto"),
                f)) for f in sfilas],
        }, indent=1, ensure_ascii=False))
        return 0

    print("CONTROL POSITIVO GEN1 · CALC-ENIF-0001 · SOLO EL PUNTO (A-bis.3)")
    print(f"  umbral |delta| <= {UMBRAL}\n")
    print(f"  {'RESULT':<10} {'celda':<24} {'GEN1':>10} {'medido':>10} "
          f"{'delta':>12}  veredicto")
    for rid, celda, g, m, dl, v in filas:
        ms = f"{m:.6f}" if isinstance(m, float) else str(m)
        ds = f"{dl:+.6f}" if dl is not None else "—"
        print(f"  {rid:<10} {celda:<24} {g:>10.6f} {ms:>10} {ds:>12}  {v}")

    print("\n  SENSIBILIDAD S1 (corte de GEN1: P4_10 = {1}) — declarada ANTES")
    for rid, celda, g, m, dl, v in sfilas:
        ms = f"{m:.6f}" if isinstance(m, float) else str(m)
        ds = f"{dl:+.6f}" if dl is not None else "—"
        print(f"  {rid:<10} {celda:<24} {g:>10.6f} {ms:>10} {ds:>12}  {v}")

    n_rep = sum(1 for f in filas if f[5] == "REPRODUCE")
    print(f"\n  RESUMEN PRIMARIO: {n_rep}/{len(filas)} REPRODUCE")
    print("  NO-REPRODUCE no invalida la corrida, no autoriza tocar el "
          "medidor\n  y no se ajusta hacia atras.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

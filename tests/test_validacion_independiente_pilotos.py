#!/usr/bin/env python3
"""Guardia de `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/`.

ACTO GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1 (21/sep/2026). La validación independiente
de los tres pilotos celda-D produjo, a ciegas (commit 19d35aba, antes de abrir los
sellados), R y C2 por celda y los comparó contra los seis CALC sellados. Este test pina
que el veredicto archivado sigue siendo el que el árbol contiene:

  · comparacion-pilotos.json trae los tres pilotos con 8 / 12 / 16 celdas;
  · toda fila R y C2 es IDÉNTICO (|Δ| ≤ 1e-6) y toda fila R-IC es COINCIDE;
  · los n sin ponderar propios y sellados son iguales, fila por fila;
  · el valor «sellado» que la comparación archivó sigue siendo el que hoy trae el
    resultados.json del CALC (si alguien re-sella un CALC, este test lo delata: un
    veredicto COINCIDE contra un sello que ya no existe es un veredicto vencido, A.10).

Defecto real que atrapa: un `resultados.json` re-generado bajo otro contrato dejaría el
informe afirmando COINCIDE sobre cifras que ya no están en el árbol. D-22: primero corre
sobre un caso sintético (una comparación mínima válida y tres mutaciones que deben
fallar), después sobre el archivo real. Cero microdato; no requiere corpus.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "forense", "validaciones", "GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0")
COMP = os.path.join(DIR, "comparacion-pilotos.json")
CELDAS = {"piloto1": 8, "piloto2": 12, "piloto3": 16}
CALC = {
    "piloto1": ("CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001", "RESULT-DIN-LXE8-ARB-R-D9-P-{c}"),
    "piloto2": ("CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001", "RESULT-TRA-SXD12-ARB-R-P-{c}"),
    "piloto3": ("CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001", "RESULT-GOB-EXE15-ADJ-2025-{c}-R-P"),
}


def valida(comp: dict, sellados: dict) -> list[str]:
    """Devuelve la lista de defectos (vacía = VERDE). `sellados[piloto][celda] = R sellado hoy`."""
    errores = []
    for pil, n_esp in CELDAS.items():
        if pil not in comp.get("pilotos", {}):
            errores.append(f"{pil}: ausente")
            continue
        filas = comp["pilotos"][pil]["filas"]
        celdas_R = [f for f in filas if f["tipo"] == "R"]
        if len(celdas_R) != n_esp:
            errores.append(f"{pil}: {len(celdas_R)} celdas R, esperadas {n_esp}")
        for f in filas:
            if f["tipo"] in ("R", "C2") and f["clase"] != "IDÉNTICO":
                errores.append(f"{pil}/{f['celda']}/{f['tipo']}: clase {f['clase']}")
            if f["tipo"] == "R-IC" and f["clase"] != "COINCIDE":
                errores.append(f"{pil}/{f['celda']}/R-IC: clase {f['clase']}")
            if "n_propio" in f and f["n_propio"] != f["n_sellado"]:
                errores.append(f"{pil}/{f['celda']}: n propio {f['n_propio']} ≠ sellado {f['n_sellado']}")
            if f["tipo"] == "R":
                hoy = sellados.get(pil, {}).get(f["celda"])
                if hoy is None or abs(hoy - f["sellado"]) > 1e-12:
                    errores.append(f"{pil}/{f['celda']}: R sellado archivado {f['sellado']} ≠ árbol hoy {hoy}")
    return errores


def _fila(celda, tipo, prop, sel, clase, n=None):
    f = {"celda": celda, "tipo": tipo, "propio": prop, "sellado": sel, "clase": clase, "d_pp": (prop - sel) * 100 if isinstance(prop, float) else None}
    if n is not None:
        f["n_propio"] = f["n_sellado"] = n
    return f


def sintetico() -> None:
    comp = {"pilotos": {}}
    sel = {}
    for pil, n in CELDAS.items():
        filas, sel[pil] = [], {}
        for i in range(n):
            c = f"c{i}"
            filas += [_fila(c, "R", 0.4, 0.4, "IDÉNTICO", n=300), _fila(c, "C2", 0.41, 0.41, "IDÉNTICO"),
                      {"celda": c, "tipo": "R-IC", "propio": [0.3, 0.5], "sellado": [0.3, 0.5], "clase": "COINCIDE"}]
            sel[pil][c] = 0.4
        comp["pilotos"][pil] = {"filas": filas}
    assert valida(comp, sel) == [], "el caso sintético válido debe pasar"
    # mutación 1: una celda C2 con DIFERENCIA
    m = json.loads(json.dumps(comp))
    m["pilotos"]["piloto2"]["filas"][1]["clase"] = "DIFERENCIA"
    assert any("C2: clase DIFERENCIA" in e for e in valida(m, sel))
    # mutación 2: n distinto
    m = json.loads(json.dumps(comp))
    m["pilotos"]["piloto3"]["filas"][0]["n_sellado"] = 299
    assert any("n propio" in e for e in valida(m, sel))
    # mutación 3: el árbol ya no trae el sello archivado
    s2 = json.loads(json.dumps(sel))
    s2["piloto1"]["c0"] = 0.40001
    assert any("árbol hoy" in e for e in valida(comp, s2))


def sellados_hoy(comp: dict) -> dict:
    out = {}
    for pil, (calc, patron) in CALC.items():
        p = os.path.join(ROOT, "data", "corrida0", calc, "resultados.json")
        r = json.load(open(p, encoding="utf-8"))["resultados"]
        if isinstance(r, list):
            r = {it["id"]: it.get("valor") for it in r}
        else:
            r = {k: (v.get("valor") if isinstance(v, dict) else v) for k, v in r.items()}
        out[pil] = {}
        for f in comp["pilotos"][pil]["filas"]:
            if f["tipo"] == "R":
                out[pil][f["celda"]] = r.get(patron.format(c=f["celda"].replace("|", "-")))
    return out


def main() -> int:
    sintetico()
    print("sintético: OK (1 válido, 3 mutaciones detectadas)")
    comp = json.load(open(COMP, encoding="utf-8"))
    errores = valida(comp, sellados_hoy(comp))
    for e in errores:
        print("FAIL", e)
    n = sum(len([f for f in comp["pilotos"][p]["filas"] if f["tipo"] == "R"]) for p in CELDAS)
    print(f"real: {n} celdas R comparadas, {len(errores)} defectos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())

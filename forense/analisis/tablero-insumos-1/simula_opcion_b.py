#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simula la opción (b) de §5-bis del encargo GEN2-TUBERIA-TABLERO-INSUMOS-1: sacar SIN-UNION
de la precedencia y del conteo de stoppers de tools/tablero_carriles.py. SOLO LEE: no escribe
nada y no cambia la regla (§10 del encargo: sin la firma de 5-bis no se toca el semáforo).

    python3 forense/analisis/tablero-insumos-1/simula_opcion_b.py

Imprime lo que la firma de mesa necesita ver ANTES de firmar: en cuántos carriles SIN-UNION es
stopper ADQUISICION, cuántos son ROJO, y para cada carril cuya siguiente acción HOY es SIN-UNION,
cuál sería sin él (y con qué semáforo). La derivación es la del propio tablero (`derivar()`); la
simulación solo repite su regla de siguiente acción sin los ítems SIN-UNION.
"""
import os
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
os.chdir(RAIZ)
import tablero_carriles as TC  # noqa: E402


def siguiente_sin_sin_union(c):
    for cat in TC.PRECEDENCIA:
        its = [x for x in c["stoppers"].get(cat, []) if not (cat == "ADQUISICION" and x.get("id") == "SIN-UNION")]
        if its:
            return cat, its[0]["id"]
    return ("2027", c["familias"][0]["familia"]) if c["familias"] else ("LISTO", "")


def main():
    cs = TC.derivar()["carriles"]
    con = [c for c in cs if any(x.get("id") == "SIN-UNION" for x in c["stoppers"].get("ADQUISICION", []))]
    print(f"carriles: {len(cs)} · con SIN-UNION como stopper ADQUISICION: {len(con)} · "
          f"semáforo: {dict(Counter(c['semaforo'] for c in cs))}")
    cambian = []
    for c in cs:
        if c["siguiente"].get("id") == "SIN-UNION":
            cambian.append((c["carril"], c["semaforo"], siguiente_sin_sin_union(c)))
    print(f"carriles cuya siguiente acción hoy ES SIN-UNION (y que cambiarían con (b)): {len(cambian)}")
    for carril, sem, (cat, ident) in cambian:
        print(f"  {carril} · {sem} · sin SIN-UNION: {cat}{(':' + ident) if ident else ''}")
    print("de esos: " + " · ".join(f"{k} {v}" for k, v in sorted(Counter(cat for _, _, (cat, _) in cambian).items())))
    raros = [carril for carril, sem, (cat, _) in cambian if sem == "ROJO" and cat in ("LISTO", "2027")]
    print(f"ROJO que quedarían con siguiente sin stopper (LISTO/2027): {len(raros)} {raros}")


if __name__ == "__main__":
    main()

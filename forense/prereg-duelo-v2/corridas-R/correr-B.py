#!/usr/bin/env python3
"""Corredor B sobre las 15 celdas del piloto. COMMIT-2 de ACTO E7 R-SCORING.

Importa corredor-B-tasa-base.py y lo invoca conforme a su propia firma
(elegir_baseline); cero reimplementacion. El historial publico de cada
celda se toma de la columna `publicada` del marco congelado, que es el
unico insumo sellado que dice si el reactivo tiene cifra publicada.
"""
import importlib.util, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("corredorB", os.path.join(AQUI, "..", "corredor-B-tasa-base.py"))
B = importlib.util.module_from_spec(spec)
sys.modules["corredorB"] = B  # dataclasses exige el modulo registrado
spec.loader.exec_module(B)

MARCO = os.path.join(AQUI, "..", "marco-congelado-piloto-v1_0.tsv")
L = open(MARCO, encoding="utf-8").read().split("\n")
H = L[0].split("\t"); IX = {x: n for n, x in enumerate(H)}
FILAS = {r[0]: r for r in (l.split("\t") for l in L[1:] if l.strip())}

CELDAS = "CIV-08 DIN-03 DIN-05 DIN-07 DIN-11 DOC-06 EMP-02 EMP-04 EMP-05 SFT-04 SFT-06 TIC-01 TIC-06 TIC-08 TIC-12".split()
out = {}
for cid in CELDAS:
    pub = FILAS[cid][IX["publicada"]]
    veredicto = pub.split("::")[0].strip().upper()
    # historial publico: solo lo habria si la prueba del bibliotecario hubiera
    # ENCONTRADO el reactivo publicado. NO => lista vacia, no se supone una cifra.
    historial = []
    if veredicto.startswith("SI"):
        # una cifra publicada de la PROPIA ola no es "ola anterior"; el corredor
        # exige ola previa del mismo reactivo, y el marco no la trae. Se declara.
        historial = []
    res = B.elegir_baseline(historial, None)
    out[cid] = {"id_celda": cid, "veredicto_publicada_marco": veredicto,
                "historial_publico_n": len(historial),
                "valor_ola_inmediatamente_anterior": None, **res}

with open(os.path.join(AQUI, "_corredor-B.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True); fh.write("\n")

from collections import Counter
print("metodos:", dict(Counter(v["metodo"] for v in out.values())))
for cid in CELDAS:
    print(f"  {cid:7} publicada={out[cid]['veredicto_publicada_marco']:3} -> B={out[cid]['metodo']} valor={out[cid]['valor']}")

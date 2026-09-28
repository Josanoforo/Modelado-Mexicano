#!/usr/bin/env python3
"""ACTO GEN2-ASTRA6-C1-LOTE-3 · P3. Construye la referencia v3 del paquete
endireh-pisos-2016-pareja-fisica-0002 desde el RESULT sellado, DESPUÉS de congelar la
exportación de la reconstructora (freeze sha eae56077…d5a7, commit 585a0135).

Guardia que PARA: la celda i del RESULT sellado debe casar con la llave `#i` de
estimandos.tsv del paquete por (eje, segmento, ventana); si no, no hay referencia.
Los números se copian como repr(float) del JSON sellado, sin redondear.
Uso: construye_referencia.py <estimandos.tsv> <salida.json>"""
import csv, json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[3]
SELLADO = R / "data/corrida0/CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002/resultados.json"
IDENT = json.loads((Path(__file__).resolve().parent /
                    "endireh-pisos-2016-pareja-fisica-0002/entrada/identidad.json").read_text())
est = {int(r["celda"]): r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t")}
tabla = json.loads(json.loads(SELLADO.read_text())["resultados"]["RESULT-ENDIREH2016-PF-TABLA"])
if len(tabla) != len(est) or set(est) != set(range(len(tabla))):
    raise SystemExit("PARO · número de celdas distinto entre sellado y estimandos")
filas = []
for i, c in enumerate(tabla):
    e = est[i]
    if (c["eje"], c["categoria"], c["ventana"]) != (e["eje"], e["segmento"], e["ventana"]):
        raise SystemExit(f"PARO · celda {i}: sellado {(c['eje'], c['categoria'], c['ventana'])} ≠ "
                         f"estimandos {(e['eje'], e['segmento'], e['ventana'])}")
    lo, hi = c["ic95"]
    filas.append({"llave": e["llave"], "unidad": e["unidad"], "estado": "RECONSTRUIDO",
                  "punto": repr(float(c["p"])), "estado_ic": "CALCULADO",
                  "ic95_inf": repr(float(lo)), "ic95_sup": repr(float(hi))})
doc = {"version": 3, "identidad": IDENT, "filas": filas}
Path(sys.argv[2]).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(filas), "filas")

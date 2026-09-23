"""Exporta la vista legible de un RESULT agregado ya sellado."""
import csv
import json
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[3]
CALC = "CALC-ENOE-PERSISTENCIA-0001"
carpeta = RAIZ / "data/corrida0" / CALC
resultado = json.loads((carpeta / "resultados.json").read_text())
filas = json.loads(resultado["resultados"]["RESULT-ENOE-PERSISTENCIA-TABLA"])
sello = (carpeta / "sello.sha256").read_text().strip()
salida = RAIZ / "forense/analisis/dominios/enoe/persistencia-v1_0.tsv"
campos = list(filas[0]) + ["result_id", "calc_id", "sello_sha256"]
with salida.open("w", newline="") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=campos, delimiter="\t")
    escritor.writeheader()
    for fila in filas:
        fila.update(result_id="RESULT-ENOE-PERSISTENCIA-TABLA", calc_id=CALC,
                    sello_sha256=sello)
        escritor.writerow(fila)
print(f"{salida}: {len(filas)} pares")

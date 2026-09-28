#!/usr/bin/env python3
"""ACTO GEN2-C1-SUCESORES-Y-LOTE-3 · P2 · R22 (FP-…-fb50-04).

Deriva la tabla de tolerancias por identidad de los ocho paquetes ENDUTIH/MOCIBA
de C1 (lote 2 preparado) desde `estimandos.tsv` de cada contenedor. No abre
microdato ni resultados: lee solo la lista de identidades y su unidad.

Regla firmada (verbatim): «proporciones abs 1e-8 rel 0, enteros y estados exactos,
pesos expandidos abs 1e-8 / rel 1e-12; el plan de IC va aparte».

Uso: r22_tolerancias.py <salida.tsv>   (sin argumento: imprime conteos)
"""
import csv
import hashlib
import io
import sys
import tarfile
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
ENTRADAS = RAIZ / "forense/validacion-independiente/catalogo-1-preparacion-lote2/entradas"
PAQUETES = [
    "endutih-empleo-15mas-2023-0001", "endutih-empleo-15mas-2024-0001",
    "endutih-empleo-15mas-2025-0001", "endutih-pisos-2023-0001",
    "endutih-pisos-2024-0001", "endutih-pisos-2025-0001",
    "mociba-pisos-2016-0001", "mociba-pisos-2017-0001",
]
# unidad -> (clase, abs, rel); campos punto. Estados de fila se comparan literales.
REGLA = {
    "proporcion": ("PROPORCION", "1e-8", "0"),
    "entero": ("ENTERO-EXACTO", "0", "0"),
    "conteo": ("ENTERO-EXACTO", "0", "0"),
    "peso_expandido": ("PESO-EXPANDIDO", "1e-8", "1e-12"),
}
COLS = ["paquete", "contenedor_sha256", "llave", "result_id", "calc", "instrumento", "ola",
        "unidad", "clase_tolerancia", "campo", "abs", "rel", "estados", "ic"]


def filas():
    for p in PAQUETES:
        tars = sorted((ENTRADAS / p).glob("*.tar.gz"))
        if len(tars) != 1:
            raise SystemExit(f"PARO · {p}: {len(tars)} contenedores")
        sha = hashlib.sha256(tars[0].read_bytes()).hexdigest()
        with tarfile.open(tars[0]) as t:
            texto = t.extractfile("estimandos.tsv").read().decode("utf-8")
        for r in csv.DictReader(io.StringIO(texto), delimiter="\t"):
            if r["unidad"] not in REGLA:
                raise SystemExit(f"PARO · {p}/{r['llave']}: unidad sin regla firmada {r['unidad']!r}")
            clase, a, rel = REGLA[r["unidad"]]
            yield [p, sha, r["llave"], r["result_id"], r["calc"], r["instrumento"], r["ola"],
                   r["unidad"], clase, "punto", a, rel, "EXACTOS",
                   "PLAN-APARTE (R23: diagnóstico; sin margen firmado no adjudica)"]


def main():
    todas = list(filas())
    llaves = Counter(f[2] for f in todas)
    if any(v > 1 for v in llaves.values()):
        raise SystemExit("PARO · llave repetida entre paquetes")
    print(len(todas), "identidades ·", dict(Counter(f[0] for f in todas)), "·",
          dict(Counter(f[8] for f in todas)))
    if len(sys.argv) > 1:
        texto = "\t".join(COLS) + "\n" + "".join("\t".join(f) + "\n" for f in todas)
        Path(sys.argv[1]).write_text(texto, encoding="utf-8")
        print("escrito", sys.argv[1], hashlib.sha256(texto.encode()).hexdigest())


if __name__ == "__main__":
    main()

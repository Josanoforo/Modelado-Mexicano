"""Escribe salida/SELLO.txt con el sha256 de cada archivo de salida/ (excepto el propio sello)."""
import hashlib
import os
import shutil

shutil.rmtree("salida/codigo/__pycache__", ignore_errors=True)
rutas = []
for raiz, _, archivos in os.walk("salida"):
    for a in archivos:
        p = os.path.join(raiz, a)
        if p != os.path.join("salida", "SELLO.txt"):
            rutas.append(p)
lineas = []
for p in sorted(rutas):
    with open(p, "rb") as fh:
        lineas.append("%s  %s" % (hashlib.sha256(fh.read()).hexdigest(), p))
with open("salida/SELLO.txt", "w") as fh:
    fh.write("\n".join(lineas) + "\n")
print("\n".join(lineas))

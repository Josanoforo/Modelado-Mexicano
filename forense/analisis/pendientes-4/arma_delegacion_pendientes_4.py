#!/usr/bin/env python3
"""arma_delegacion_pendientes_4.py -- ACTO GEN2-PENDIENTES-4: deriva `decididas-por-delegacion-pendientes-4.tsv`
(id · opcion · razon) de `dictamen-pendientes-4.tsv`, la única fuente. Lo reversible lo decidió el acto por la
delegación de PENDIENTES-3, reafirmada en ADENDA-1; lo irreversible o de mesa lleva `DECISION-DE-MESA` y sus
opciones viven en `hoja-decisiones-pendientes-4.md`.

    python3 forense/analisis/pendientes-4/arma_delegacion_pendientes_4.py
"""
import csv
import os
import re

QUI = os.path.dirname(os.path.abspath(__file__))
csv.field_size_limit(10**9)


def opcion(r):
    a, s = r["accion"], r["nuevo_sucesor"]
    if a == "CERRAR":
        return "CIERRA"
    if a == "NADA":
        return "MANTIENE-DUENO"
    for pref, nombre in (("DIRECCION-ENCARGO", "ABSORBE-EN-ENCARGO"), ("MESA-ACCION", "RECETA-DE-MESA"),
                         ("MESA-DECISION", "DECISION-DE-MESA"), ("CANAL", "ESPERA-CANAL"),
                         ("APERTURA", "ESPERA-APERTURA"), ("ADQUISICION", "ESPERA-ADQUISICION")):
        if s.startswith(pref):
            return nombre
    return "OTRO"


def limpia(t, n=300):
    return re.sub(r"\s+", " ", (t or "").replace("\t", " ")).strip()[:n]


def main():
    filas = list(csv.DictReader(open(os.path.join(QUI, "dictamen-pendientes-4.tsv"), newline="", encoding="utf-8"),
                                delimiter="\t"))
    salida = os.path.join(QUI, "decididas-por-delegacion-pendientes-4.tsv")
    with open(salida, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["id", "opcion", "razon"])
        for r in filas:
            destino = r["cerrado_por"] if r["accion"] == "CERRAR" else r["nuevo_sucesor"]
            razon = limpia(r["porque"], 200)
            w.writerow([r["id"], opcion(r), limpia(f"{destino} · {razon}" if razon else destino, 420)])
    print(f"{len(filas)} filas -> {os.path.relpath(salida)}")


if __name__ == "__main__":
    main()

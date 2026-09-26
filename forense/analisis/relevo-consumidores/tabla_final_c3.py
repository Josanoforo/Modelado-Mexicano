#!/usr/bin/env python3
"""ACTO GEN2-RELEVO-CONSUMIDORES-3 · P4. Tabla consumidor × fila × vía × estado
tras FIRMAS-18 H1/H2/H3.

Mismo universo y mismas reglas que `tabla_final.py` (RELEVO-CONSUMIDORES-2);
se anteponen las reglas de este acto (primera que casa, gana) y el sucesor
de lo que -2 difirió a «-3» y -3 no releva pasa a «-4». Ninguna fila se
teclea: se clasifica por la marca en el archivo vivo o por tipo/sección.

Uso: python3 forense/analisis/relevo-consumidores/tabla_final_c3.py [--tsv RUTA]
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import tabla_final as T  # noqa: E402

C = T.C
E = __import__("escribe_relevo_consumo")
FP = "FP-260925-GEN2-RELEVO-CONSUMIDORES-2-e760"
MARCADOS = C._consumidores_historico_sin_relevo()
CITA_H1 = {f"milpa/procedencia.yaml:asignados_probabilidad:{r}" for r, _p, _q in E.H1_CITA}
ACOTA_H2 = {f"milpa/catalogo-momentos-v0_1.tsv:{m}" for m, _r, _d in E.H2_ACOTA}
SUCESOR = "GEN2-RELEVO-CONSUMIDORES-4"

REGLAS_C3 = [
    (lambda u: u["activo"] == "SI" and ":asignados_coeficiente:" in u["consumidor"]
     and u["consumidor"] in MARCADOS,
     "escritor V6 (H1)", "HISTÓRICO-SIN-RELEVO", "firma H1 (FIRMAS-18, FP e760-01); fuera del contador", "—"),
    (lambda u: u["activo"] == "SI" and "catalogo-momentos" in u["consumidor"]
     and u["consumidor"] in MARCADOS,
     "escritor V6 (H2)", "HISTÓRICO-SIN-RELEVO", "firma H2 (FIRMAS-18, FP e760-02): cotejo NO-EQUIVALENTE; fuera del contador", "—"),
    (lambda u: u["activo"] == "SI" and u["consumidor"].startswith(C.PREFIJO_MARCO_H3)
     and u["tipo_uso"] in C.TIPOS_HISTORICO_H3,
     "firma (H3)", "HISTÓRICO-SIN-RELEVO", "firma H3 (FIRMAS-18, FP e760-03): L/AGREGADO del duelo; fuera del contador por tipo_uso", "—"),
    (lambda u: u["consumidor"] in CITA_H1 and u["generacion_leida"] == "GEN2",
     "i-CRUDO + iii (escritor V6)", "RELEVADA", "H1 regla B1: par GEN2 coincidente (CALC-ENCIG-0001 + complemento derivado, REPRODUCE)", "—"),
    (lambda u: u["consumidor"] in ACOTA_H2 and u["generacion_leida"] == "GEN2",
     "i-CRUDO (escritor V6)", "RELEVADA-ACOTADA", "H2 cotejo PARCIAL: acotado a la unidad medida (ENCIG 2025, pago digital de luz)", "—"),
    (lambda u: ":asignados_probabilidad:" in u["consumidor"] and u["generacion_leida"] != "GEN2",
     "escritor V6 (rótulo)", "NC", f"DIFERIDO-A:{SUCESOR} -- ASIGNADO-CONSERVADO-H1: B1 conserva con rótulo donde no hay par GEN2 con conducta y disparador coincidentes; sigue legacy hasta que exista medición",
     SUCESOR),
    (lambda u: u["consumidor"].endswith(":M03"),
     "—", "NC", f"DIFERIDO-A:{SUCESOR} -- H2 cotejo PARCIAL, pero no existe RESULT GEN2 de tramite.gobierno_digital.coercitivo en ninguna unidad: acotar exige un valor que no hay",
     SUCESOR),
    (lambda u: u["consumidor"].endswith((":M05", ":M23")),
     "—", "NC", "DECISIÓN-DE-MESA-PENDIENTE: cotejo DERIVADO SELLADO SIN ADOPCIÓN no es PARCIAL ni NO-EQUIVALENTE (las dos ramas de H2); champion NINGUNO y reserva consumida. Recomendación: HISTÓRICO-SIN-RELEVO",
     SUCESOR),
]


def filas() -> list[dict]:
    T.REGLAS[:0] = REGLAS_C3
    fs = T.filas()
    for f in fs:
        if f["sucesor"] == "GEN2-RELEVO-CONSUMIDORES-3" or f["sucesor"].startswith(
                "GEN2-RELEVO-CONSUMIDORES-3 "):
            f["sucesor"] = f["sucesor"].replace("CONSUMIDORES-3", "CONSUMIDORES-4")
    return fs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", type=Path)
    a = ap.parse_args()
    fs = filas()
    if a.tsv:
        with a.tsv.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(fs[0]), delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(fs)
    for (b, e), n in sorted(Counter((f["consumidor_bucket"], f["estado"]) for f in fs).items()):
        print(f"{b}\t{e}\t{n}")
    return 1 if any(f["estado"] == "SIN-DICTAMEN" for f in fs) else 0


if __name__ == "__main__":
    sys.exit(main())

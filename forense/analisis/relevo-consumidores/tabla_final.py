#!/usr/bin/env python3
"""ACTO GEN2-RELEVO-CONSUMIDORES-2 · P5. Tabla consumidor × fila × vía × estado.

Universo: usos activos del registro (`corrida0._filas_registro`) cuyo
consumidor cae en uno de los cuatro buckets del encargo (procedencia,
catálogo de momentos, marco del duelo, celdas-D). Cada fila se clasifica
por una REGLA declarada abajo (por tipo/sección del consumidor, nunca por
fila tecleada); una fila que ninguna regla cubre sale `SIN-DICTAMEN` y el
script termina con código 1.

Uso: python3 forense/analisis/relevo-consumidores/tabla_final.py [--tsv RUTA]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(RAIZ), str(RAIZ / "tools")]
import corrida0 as C  # noqa: E402

FP = "FP-260925-GEN2-RELEVO-CONSUMIDORES-2-e760"


def bucket(consumidor: str) -> str | None:
    if consumidor.startswith("forense/prereg-duelo-v2/marco-M"):
        return "marco_del_duelo"
    if consumidor.startswith("milpa/procedencia.yaml"):
        return "procedencia"
    if "catalogo-momentos" in consumidor:
        return "catalogo_de_momentos"
    if "curacion-registro/celdas-d/" in consumidor:
        return "celdas_D"
    if consumidor.startswith(("milpa/tramite.yaml", "milpa/src/")):
        return "motor"  # ADENDA-1 · P5 (FIRMAS-16 B1/B2/B3)
    return None


# (predicado, via, estado, razon A.14, sucesor). Primera que casa, gana.
B1_RETIRA = {f"milpa/tramite.yaml:{r}:{c}" for r, c, _h in __import__(
    "escribe_relevo_consumo").B1_RETIRA}
REGLAS = [
    (lambda u: u["activo"] == "NO", "escritor V5", "RETIRADA-B2",
     "rol_uso: historico (FIRMAS-16 B2); sale del consumo vivo", "—"),
    (lambda u: u["tipo_uso"] == "corte_pi", "firma", "FUERA-DEL-CONTADOR-B3",
     "partición sellada, no lectura numérica (FIRMAS-16 B3)", "—"),
    (lambda u: u["consumidor"] in B1_RETIRA and u["generacion_leida"] == "GEN2",
     "escritor V5 (B1)", "RELEVADA", "par GEN2 del hermano medido (FIRMAS-16 B1)", "—"),
    (lambda u: u["consumidor"].startswith("milpa/tramite.yaml") and u["generacion_leida"] == "GEN2",
     "escritor V1-V3 / pin", "RELEVADA-PREVIA", "relevada por un acto anterior", "—"),
    (lambda u: u["consumidor"].startswith("milpa/tramite.yaml"),
     "—", "NC-AJENA", "NC del acto RELEVO-MOTOR-34-1 (a157); B1 conserva con rótulo o sin RESULT GEN2",
     "ver forense/no-corrido.tsv (a157)"),
    (lambda u: u["generacion_leida"] == "GEN2" and u.get("via_relevo"),
     "pin", "RELEVADA-PREVIA", "pin de mesa firmado ya aplicado (TANDA-3/4)", "—"),
    (lambda u: u["generacion_leida"] == "GEN2",
     "i-CRUDO (escritor V4)", "RELEVADA", "cita B4 / columnas de relevo; CALC-ENVIPE-DENUNCIA-SEGURO-0001 REPRODUCE", "—"),
    (lambda u: ":coeficientes_generador_sellados:" in u["consumidor"],
     "—", "NC", "DIFERIDO-A:CAJA -- β̂ de generador GEN1; ningún CALC GEN2 del generador en el registro (0 CALC con MATRIZ/THETA/COEF en resultados.tsv)",
     "GEN2-RELEVO-CONSUMIDORES-3 (re-medición en CAJA)"),
    (lambda u: ":asignados_coeficiente:" in u["consumidor"],
     "—", "NC", "DECISIÓN-DE-MESA-PENDIENTE: coeficiente ASIGNADO sin medición; propuesta HISTÓRICO-SIN-RELEVO o encargo de medición",
     f"{FP}-01 (FIRMAS-17)"),
    (lambda u: ":asignados_probabilidad:" in u["consumidor"],
     "—", "NC", "DECISIÓN-DE-MESA-PENDIENTE: ASIGNADO cuyo hermano medido cambia el estimando (mismo caso que FP a157-01/02 del motor); no es relevo",
     f"{FP}-01 (FIRMAS-17)"),
    (lambda u: ":condicionales_" in u["consumidor"],
     "—", "NC", "DIFERIDO-A:θ -- condicional θ es generador de retadores (ADR-531, §4); Theta.valor() no emite; sin CALC θ GEN2",
     "GEN2-RELEVO-CONSUMIDORES-3"),
    (lambda u: ":M05" in u["consumidor"] or ":M23" in u["consumidor"],
     "—", "NC", "DECISIÓN-DE-MESA-PENDIENTE: derivado sellado, champion NINGUNO y reserva consumida; adoptarlo exige reserva nueva",
     f"{FP}-02 (FIRMAS-17)"),
    (lambda u: "catalogo-momentos" in u["consumidor"] and u["tipo_uso"] == "momento"
     and any(f":M{n:02d}" in u["consumidor"] for n in range(1, 9)),
     "—", "NC", "DECISIÓN-DE-MESA-PENDIENTE: AJUSTE sin RESULT de identidad (cotejo-documental-catalogo.md: NO-EQUIVALENTE / PARCIAL / sin instrumento)",
     f"{FP}-02 (FIRMAS-17)"),
    (lambda u: "catalogo-momentos" in u["consumidor"],
     "—", "NC", "DIFERIDO-A:instrumento -- HOLDOUT; valor_de() lanza y la dependencia demostrada (cotejo) no tiene fuente",
     "SIN-ASIGNAR (cotejo-documental-catalogo.md fija el instrumento que falta)"),
    (lambda u: "GOB.gobierno_digital" in u["consumidor"] and "celdas-d" in u["consumidor"],
     "—", "NC", "PARO-PREMISA: champion C2 firmado, pero su adjudicación ingiere RESULT de otra corrida; la guarda 4.1 vía (i) rechaza el pin (RECHAZADO-RESULT-INGERIDO)",
     "GEN2-RELEVO-CONSUMIDORES-3"),
    (lambda u: "celdas-d" in u["consumidor"],
     "—", "NC", "PARO-PREMISA: no hay champion GEN2 vigente (NINGUNO o BASELINE GEN1 sin CALC); «RESULT del champion vigente» no existe",
     "GEN2-RELEVO-CONSUMIDORES-3"),
    (lambda u: u["consumidor"].endswith(":M") and "DIN-M-01" in u["consumidor"],
     "—", "NC", "DIFERIDO-A:CAJA -- M emitido desde la regla ENNViH (RES-0029/0030), diferida por el motor",
     "CAJA (payloads ennvih en manifiesto)"),
    (lambda u: ":L:" in u["consumidor"] or u["consumidor"].endswith(":AGREGADO"),
     "—", "NC", "DECISIÓN-DE-MESA-PENDIENTE: emisión sellada de contendiente L / agregado del marcador; no es medición relevable; propuesta HISTÓRICO-SIN-RELEVO",
     f"{FP}-03 (FIRMAS-17)"),
]


def filas() -> list[dict]:
    v = C._filas_registro(verifica=False)
    salida = []
    for u in v["usos"]:
        b = bucket(str(u["consumidor"]))
        if b is None or (u["activo"] != "SI" and b != "motor"):
            continue
        regla = next((r for r in REGLAS if r[0](u)), None)
        via, estado, razon, sucesor = regla[1:] if regla else ("—", "SIN-DICTAMEN", "", "")
        salida.append({"consumidor_bucket": b, "slot": u["resultado_id"],
                       "consumidor": u["consumidor"], "generacion": u["generacion_leida"],
                       "result": u["corrida0_resultado_id"], "via": via,
                       "estado": estado, "razon": razon, "sucesor": sucesor})
    return salida


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
    from collections import Counter
    for (b, e), n in sorted(Counter((f["consumidor_bucket"], f["estado"]) for f in fs).items()):
        print(f"{b}\t{e}\t{n}")
    return 1 if any(f["estado"] == "SIN-DICTAMEN" for f in fs) else 0


if __name__ == "__main__":
    sys.exit(main())

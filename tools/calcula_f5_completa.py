#!/usr/bin/env python3
"""Extrae, calcula y adjudica F5 completa conforme a su spec congelada."""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "forense/prereg-duelo-v2"
PLAN = DIR / "F5-completa-plan-v1_0.json"
SNAPSHOT_M = DIR / "snapshot-M-triada-v1_0.json"
UNIVERSO = DIR / "universo-triada-v1_4.tsv"
SALIDA_TSV = DIR / "F5-completa-extraccion-v1_0.tsv"
SALIDA_JSON = DIR / "F5-completa-resultado-v1_0.json"

K = 8
BOOTSTRAP_N = 10_000
BOOTSTRAP_SEED = 42
DELTA_PP = 0.5
TOL_PP = 1e-9
RE_PUNTO = re.compile(r"^ESTIMACION_PUNTUAL=(\d+(?:[.,]\d+)?)%$")
CONTENDIENTES = ("L_SOLO", "L_CORPUS", "M")


def extraer(texto: str | None, estado_captura: str = "OK") -> tuple[str, float | None, str]:
    if estado_captura != "OK" or texto is None:
        return "ERROR_TECNICO", None, "captura sin respuesta CLI válida"
    lineas = [x.strip() for x in texto.splitlines() if x.strip()]
    if not lineas:
        return "MALFORMADA", None, "respuesta vacía"
    ultima = lineas[-1]
    if ultima == "ABSTENCION":
        return "ABSTENCION", None, ultima
    m = RE_PUNTO.fullmatch(ultima)
    if not m:
        return "MALFORMADA", None, ultima[:240]
    n = float(m.group(1).replace(",", "."))
    if not 0.0 <= n <= 100.0:
        return "MALFORMADA", None, ultima[:240]
    return "VALIDA", n / 100.0, ultima


def percentil(valores: list[float], q: float) -> float:
    if not valores:
        raise ValueError("percentil de lista vacía")
    xs = sorted(valores)
    pos = (len(xs) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def adjudicar_ic(lo: float, hi: float, a: str = "A", b: str = "B") -> str:
    if lo > hi:
        raise ValueError("IC invertido")
    if hi < -DELTA_PP - TOL_PP:
        return f"{a}-GANA"
    if lo > DELTA_PP + TOL_PP:
        return f"{b}-GANA"
    if lo >= -DELTA_PP - TOL_PP and hi <= DELTA_PP + TOL_PP:
        return "EMPATE-PRACTICO"
    return "INCONCLUSO"


def _r_por_celda() -> dict[str, float]:
    out = {}
    with UNIVERSO.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f, delimiter="\t"):
            cid = fila["id_celda"]
            ruta = ROOT / fila["fuente_R"] / "resultados.json"
            datos = json.loads(ruta.read_text(encoding="utf-8"))["resultados"]
            out[cid] = float(datos[f"RESULT-R-{cid}-PUNTO"])
    return out


def calcular() -> tuple[dict, list[dict]]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan["n_posiciones"] != 224:
        raise RuntimeError("plan distinto de 224")
    r = _r_por_celda()
    m = {x["id_celda"]: x.get("punto_M") for x in json.loads(SNAPSHOT_M.read_text(encoding="utf-8"))["celdas"]}
    por = {}
    filas = []
    identidad_errores = []
    for pos in plan["posiciones"]:
        ruta = ROOT / pos["ruta"]
        clave = (pos["id_celda"], pos["variante"])
        por.setdefault(clave, [])
        if not ruta.exists():
            estado, valor, evidencia = "PENDIENTE", None, "archivo ausente"
        else:
            captura = json.loads(ruta.read_text(encoding="utf-8"))
            if captura.get("identidad") != pos["identidad"]:
                identidad_errores.append(str(ruta.relative_to(ROOT)))
                estado, valor, evidencia = "ERROR_IDENTIDAD", None, "identidad distinta del plan"
            else:
                estado, valor, evidencia = extraer(captura.get("texto_crudo"), captura.get("estado_captura", "OK"))
        por[clave].append((estado, valor))
        filas.append({"id_celda": pos["id_celda"], "variante": pos["variante"], "replica": pos["replica"],
                      "estado": estado, "valor": "" if valor is None else f"{valor:.12g}",
                      "evidencia": evidencia, "archivo": pos["ruta"]})

    celdas = sorted(r)
    detalle = {}
    puntos = {"L_SOLO": {}, "L_CORPUS": {}, "M": m}
    cobertura = {"L_SOLO": 0, "L_CORPUS": 0, "M": sum(v is not None for v in m.values())}
    for cid in celdas:
        detalle[cid] = {"R": r[cid], "M": m[cid], "brazos": {}}
        for variante, nombre in (("L-solo", "L_SOLO"), ("L+corpus", "L_CORPUS")):
            estados = Counter(x[0] for x in por[(cid, variante)])
            valores = [x[1] for x in por[(cid, variante)] if x[0] == "VALIDA"]
            punto = statistics.median(valores) if valores else None
            puntos[nombre][cid] = punto
            cobertura[nombre] += punto is not None
            detalle[cid]["brazos"][nombre] = {"programadas": K, "ejecutadas": K - estados["PENDIENTE"],
                                               "validas": estados["VALIDA"], "abstenciones": estados["ABSTENCION"],
                                               "malformadas": estados["MALFORMADA"], "errores_tecnicos": estados["ERROR_TECNICO"],
                                               "pendientes": estados["PENDIENTE"], "errores_identidad": estados["ERROR_IDENTIDAD"],
                                               "punto_mediana": punto}
    u3 = [cid for cid in celdas if all(puntos[x].get(cid) is not None for x in CONTENDIENTES)]
    errores = {x: [abs(puntos[x][cid] - r[cid]) * 100 for cid in u3] for x in CONTENDIENTES}
    mae = {x: (statistics.mean(errores[x]) if u3 else None) for x in CONTENDIENTES}
    pares = (("L_CORPUS", "L_SOLO"), ("M", "L_SOLO"), ("M", "L_CORPUS"))
    comparaciones = {}
    if u3:
        rng = random.Random(BOOTSTRAP_SEED)
        indices = [[rng.randrange(len(u3)) for _ in u3] for _ in range(BOOTSTRAP_N)]
        for a, b in pares:
            deltas = [statistics.mean(errores[a][i] - errores[b][i] for i in ix) for ix in indices]
            lo, hi = percentil(deltas, .025), percentil(deltas, .975)
            comparaciones[f"{a}_vs_{b}"] = {"delta_mae_pp": mae[a] - mae[b], "ic95_lo": lo, "ic95_hi": hi,
                                               "veredicto": adjudicar_ic(lo, hi, a, b)}
    ganadores = []
    for x in CONTENDIENTES:
        otros = [y for y in CONTENDIENTES if y != x]
        gana = True
        for y in otros:
            if (x, y) in pares:
                v = comparaciones.get(f"{x}_vs_{y}", {}).get("veredicto")
            else:
                v = comparaciones.get(f"{y}_vs_{x}", {}).get("veredicto")
            gana &= v == f"{x}-GANA"
        gana &= all(cobertura[x] >= cobertura[y] for y in otros)
        if gana:
            ganadores.append(x)
    if identidad_errores or not u3:
        global_v = "NO-ADJUDICABLE-POR-CONTROL"
    elif len(ganadores) == 1:
        global_v = f"GANADOR-TRIADA-{ganadores[0]}"
    else:
        global_v = "SIN-GANADOR-UNICO"
    resultado = {"acto": "GEN2-F5-COMPLETA", "marco": 14, "u3_n": len(u3), "u3_ids": u3,
                 "cobertura_celdas_con_punto": cobertura, "mae_pp": mae, "comparaciones": comparaciones,
                 "veredicto_global": global_v, "errores_identidad": identidad_errores,
                 "bootstrap": {"replicas": BOOTSTRAP_N, "seed": BOOTSTRAP_SEED, "ic": .95},
                 "delta_pp": DELTA_PP, "tolerancia_numerica_pp": TOL_PP, "celdas": detalle}
    return resultado, filas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()
    resultado, filas = calcular()
    if args.escribir:
        SALIDA_JSON.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with SALIDA_TSV.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=filas[0].keys(), delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(filas)
    print(json.dumps({k: resultado[k] for k in ("u3_n", "cobertura_celdas_con_punto", "mae_pp", "veredicto_global")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

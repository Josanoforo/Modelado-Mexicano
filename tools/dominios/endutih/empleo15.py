"""Sucesor de P7_10_2: usuarios de internet de 15+ por ola ENDUTIH.

El primer resultado real que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from tools.dominios.endutih.pisos import COMMON, FILES, _domain, _load, _replicate_weights

FIELDS = COMMON + ("P7_1", "P7_10_2")


def _status_empleo(row: dict[str, str]) -> str:
    """La restricción etaria del reactivo precede a la respuesta observada."""
    age = int(row["EDAD"]) if row["EDAD"].isdigit() else -1
    if age < 15:
        return "SALTO"
    internet = row["P7_1"]
    if internet == "2":
        return "SALTO"
    if internet != "1":
        return "NR"
    return {"1": "SI", "2": "NO"}.get(row["P7_10_2"], "NR")


def _calculate(rows: list[dict[str, str]], entity: str) -> dict:
    valid = []
    n_edad_no_especificada = 0
    for row in rows:
        age = int(row["EDAD"]) if row["EDAD"].isdigit() else -1
        if age in (98, 99):
            n_edad_no_especificada += 1
        try:
            weight = float(row["FAC_PER"])
        except ValueError:
            weight = -1
        if 6 <= age <= 97 and weight > 0 and math.isfinite(weight) and row["EST_DIS"] and row["UPM_DIS"]:
            valid.append((row, weight))
    clusters = sorted({(r["EST_DIS"], r["UPM_DIS"]) for r, _ in valid})
    ix = {key: i for i, key in enumerate(clusters)}
    strata = np.array([x[0] for x in clusters])
    draws = _replicate_weights(strata, np.array([x[1] for x in clusters]))
    domains_by_row = [set(_domain(r, entity)) for r, _ in valid]
    domains = sorted(set().union(*domains_by_row))
    statuses = [_status_empleo(r) for r, _ in valid]
    cells = []
    rep_total = []
    for domain in domains:
        counts = Counter(statuses[i] for i, ds in enumerate(domains_by_row) if domain in ds)
        eligible = [i for i, ds in enumerate(domains_by_row) if domain in ds and statuses[i] in ("SI", "NO")]
        n = len(eligible)
        cell = {"medida": "actividad_empleo", "dominio": domain, "n": n,
                "estados": {k: int(counts[k]) for k in ("SI", "NO", "SALTO", "NR", "NS")}}
        if n < 100:
            cell["estado"] = "SUPRIMIDA-N-MENOR-100"
            cells.append(cell)
            continue
        den = np.zeros(len(clusters))
        num = np.zeros(len(clusters))
        for i in eligible:
            row, weight = valid[i]
            j = ix[(row["EST_DIS"], row["UPM_DIS"])]
            den[j] += weight
            if statuses[i] == "SI":
                num[j] += weight
        point = float(num.sum() / den.sum())
        rep_den = draws @ den
        rep_num = draws @ num
        reps = np.divide(rep_num, rep_den, out=np.full(len(draws), np.nan), where=rep_den > 0)
        good = reps[np.isfinite(reps)]
        if len(good) < 380:
            cell["estado"] = "NO-ESTIMABLE-REPLICAS"
        else:
            lo, hi = np.quantile(good, [0.025, 0.975])
            cell.update(estado="ESTIMABLE", punto=point, ic95=[float(lo), float(hi)],
                        peso_denominador=float(den.sum()), n_upm=int(np.count_nonzero(den)))
            if domain == "TOTAL":
                rep_total = [round(float(x), 9) for x in good]
        cells.append(cell)
    return {"n_tabla": len(rows), "n_base_6_97": len(valid),
            "n_edad_no_especificada": n_edad_no_especificada,
            "n_usuarios_internet_15_mas": sum(1 for r, _ in valid if int(r["EDAD"]) >= 15 and r["P7_1"] == "1"),
            "n_blanco_estructural_6_14": sum(1 for r, _ in valid if 6 <= int(r["EDAD"]) < 15 and not r["P7_10_2"]),
            "n_blanco_elegible_15_mas": sum(1 for r, _ in valid if int(r["EDAD"]) >= 15 and r["P7_1"] == "1" and not r["P7_10_2"]),
            "n_estratos": len(set(strata)), "n_upm": len(clusters),
            "replicas": {"semilla": 20260923, "B": 399,
                         "metodo": "UPM-con-reemplazo-dentro-de-estrato; singleton=certeza",
                         "total_actividad_empleo": rep_total},
            "celdas": cells}


def medir(inputs: dict, contrato: dict) -> dict:
    year = str(contrato["parametros"]["ola"])
    member, _, entity = FILES[year]
    bd = next(Path(i["ruta_absoluta"]) for i in inputs.values()
              if Path(i["ruta_absoluta"]).name.lower().endswith("bd_dbf.zip"))
    rows = _load(bd, member, FIELDS + (entity,))
    result = _calculate(rows, entity)
    return {f"RESULT-ENDUTIH-EMPLEO-15MAS-{year}-TABLA": json.dumps(result, ensure_ascii=False, sort_keys=True)}

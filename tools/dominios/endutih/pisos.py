"""Pisos ENDUTIH 2023-2025; contrato en forense/prereg-caja/ENDUTIH-PISOS-spec-v1_0.md.

El primer resultado real que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
from dbfmini import field_names, read_dbf  # noqa: E402

KEY = ("UPM", "VIV_SEL", "HOGAR", "NUM_REN")
COMMON = KEY + ("EDAD", "SEXO", "NIVEL", "TLOC", "FAC_PER", "EST_DIS", "UPM_DIS")
MAIN = COMMON + ("P7_1", "P7_2", "P7_10_2", "P7_12_3", "P7_35_4")
SECOND = KEY + ("P8_1", "P8_2")
FILES = {
    "2023": ("tic_2023_usuarios.DBF", "tic_2023_usuarios2.DBF", "ENT"),
    "2024": ("tic_2024_usuarios.DBF", "tic_2024_usuarios2.DBF", "CVE_ENT"),
    "2025": ("ti25usu.dbf", "ti25usu2.dbf", "CVE_ENT"),
}


def _load(zpath: Path, member: str, fields: tuple[str, ...]) -> list[dict[str, str]]:
    with zipfile.ZipFile(zpath) as archive:
        if member not in archive.namelist():
            raise ValueError(f"miembro ausente: {member}")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(archive.extract(member, temporary))
            found = {name for name, _, _ in field_names(path)}
            absent = set(fields) - found
            if absent:
                raise ValueError(f"{member}: columnas ausentes {sorted(absent)}")
            return list(read_dbf(path, wanted_fields=fields))


def _merge(first: list[dict[str, str]], second: list[dict[str, str]]) -> list[dict[str, str]]:
    if len(first) != len(second):
        raise ValueError("tablas de personas con cardinalidad diferente")
    # La llave completa se exige única en ambas tablas; nunca se une por orden.
    lookup = {}
    for row in second:
        key = tuple(row[k] for k in KEY)
        if key in lookup:
            raise ValueError("llave duplicada en usuarios2")
        lookup[key] = row
    out = []
    seen = set()
    for row in first:
        key = tuple(row[k] for k in KEY)
        if key in seen or key not in lookup:
            raise ValueError("llave duplicada o sin pareja en usuarios")
        seen.add(key)
        out.append(row | {k: lookup[key][k] for k in ("P8_1", "P8_2")})
    if len(seen) != len(lookup):
        raise ValueError("usuarios2 tiene llaves sin pareja")
    return out


def _domain(row: dict[str, str], entity: str) -> list[str]:
    ans = ["TOTAL"]
    if row["SEXO"] in ("1", "2"):
        ans.append("SEXO_" + row["SEXO"])
    age = int(row["EDAD"]) if row["EDAD"].isdigit() else -1
    for lo, hi, name in ((6, 11, "EDAD_06_11"), (12, 17, "EDAD_12_17"),
                         (18, 29, "EDAD_18_29"), (30, 59, "EDAD_30_59"),
                         (60, 120, "EDAD_60_MAS")):
        if lo <= age <= hi:
            ans.append(name)
    if row["TLOC"] in ("1", "2", "3", "4"):
        ans.append("TLOC_" + row["TLOC"])
    school = row["NIVEL"].zfill(2)
    if school in ("00", "01", "02"):
        ans.append("ESC_0_2")
    elif school in ("03", "04", "05"):
        ans.append("ESC_3_5")
    elif school in ("06", "07", "08", "09", "10", "11"):
        ans.append("ESC_6_11")
    if row[entity].isdigit() and 1 <= int(row[entity]) <= 32:
        ans.append("ENT_" + row[entity].zfill(2))
    return ans


def _status(row: dict[str, str], measure: str) -> str:
    # SI, NO, SALTO, NR, NS. Nunca convierte un salto o blanco en NO.
    internet = row["P7_1"]
    phone = row["P8_1"]
    if measure == "internet":
        return {"1": "SI", "2": "NO"}.get(internet, "NR")
    if measure == "celular":
        return {"1": "SI", "2": "NO"}.get(phone, "NR")
    if measure.startswith("actividad_"):
        if internet == "2":
            return "SALTO"
        if internet != "1":
            return "NR"
        field = {"actividad_empleo": "P7_10_2", "actividad_mensajes": "P7_12_3",
                 "actividad_tramite": "P7_35_4"}[measure]
        return {"1": "SI", "2": "NO"}.get(row[field], "NR")
    if measure.startswith("no_internet_"):
        if internet == "1":
            return "SALTO"
        if internet != "2":
            return "NR"
        value = row["P7_2"]
        if value not in set("12345678"):
            return "NR"
        code = {"no_internet_acceso": "1", "no_internet_costo": "4",
                "no_internet_preferencia": "3"}[measure]
        return "SI" if value == code else "NO"
    if measure.startswith("no_celular_"):
        if phone == "1":
            return "SALTO"
        if phone != "2":
            return "NR"
        value = row["P8_2"]
        if value not in set("12345678"):
            return "NR"
        code = {"no_celular_costo": "1", "no_celular_preferencia": "2",
                "no_celular_cobertura": "3"}[measure]
        return "SI" if value == code else "NO"
    raise ValueError(measure)


MEASURES = (
    "internet", "celular", "actividad_empleo", "actividad_mensajes",
    "actividad_tramite", "no_internet_acceso", "no_internet_costo",
    "no_internet_preferencia", "no_celular_costo", "no_celular_preferencia",
    "no_celular_cobertura",
)


def _replicate_weights(strata: np.ndarray, psu: np.ndarray, count: int = 399) -> np.ndarray:
    # Mismas réplicas para TODOS los dominios y desenlaces de la ola.
    groups: dict[str, list[int]] = {}
    for index, stratum in enumerate(strata):
        groups.setdefault(str(stratum), []).append(index)
    rng = np.random.default_rng(20260923)
    draws = np.zeros((count, len(psu)), dtype=np.int16)
    for indices in groups.values():
        if len(indices) == 1:
            draws[:, indices[0]] = 1  # UPM de certeza en estrato singleton.
        else:
            samples = rng.integers(0, len(indices), size=(count, len(indices)))
            for b, choices in enumerate(samples):
                draws[b, indices] = np.bincount(choices, minlength=len(indices))
    return draws


def _calculate(rows: list[dict[str, str]], entity: str) -> dict:
    valid = []
    for row in rows:
        age = int(row["EDAD"]) if row["EDAD"].isdigit() else -1
        try:
            weight = float(row["FAC_PER"])
        except ValueError:
            weight = -1
        if age >= 6 and weight > 0 and math.isfinite(weight) and row["EST_DIS"] and row["UPM_DIS"]:
            valid.append((row, weight))
    clusters = sorted({(r["EST_DIS"], r["UPM_DIS"]) for r, _ in valid})
    ix = {key: i for i, key in enumerate(clusters)}
    strata = np.array([x[0] for x in clusters])
    draws = _replicate_weights(strata, np.array([x[1] for x in clusters]))
    cells = []
    rep_total = {}
    domains = sorted({d for r, _ in valid for d in _domain(r, entity)})
    domain_sets = [set(_domain(r, entity)) for r, _ in valid]
    for measure in MEASURES:
        statuses = [_status(r, measure) for r, _ in valid]
        for domain in domains:
            counts = Counter(statuses[i] for i, ds in enumerate(domain_sets) if domain in ds)
            eligible = [i for i, ds in enumerate(domain_sets) if domain in ds and statuses[i] in ("SI", "NO")]
            n = len(eligible)
            cell = {"medida": measure, "dominio": domain, "n": n,
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
                    rep_total[measure] = [round(float(x), 9) for x in good]
            cells.append(cell)
    return {"n_tabla": len(rows), "n_universo": len(valid), "n_estratos": len(set(strata)),
            "n_upm": len(clusters), "replicas": {"semilla": 20260923, "B": 399,
            "metodo": "UPM-con-reemplazo-dentro-de-estrato; singleton=certeza",
            "total_por_medida": rep_total}, "celdas": cells}


def medir(inputs: dict, contrato: dict) -> dict:
    year = str(contrato["parametros"]["ola"])
    first, second, entity = FILES[year]
    paths = [Path(item["ruta_absoluta"]) for item in inputs.values()]
    bd = next(p for p in paths if p.name.lower().endswith("bd_dbf.zip"))
    rows = _merge(_load(bd, first, MAIN + (entity,)), _load(bd, second, SECOND))
    result = _calculate(rows, entity)
    return {f"RESULT-ENDUTIH-PISOS-{year}-TABLA": json.dumps(result, ensure_ascii=False, sort_keys=True)}

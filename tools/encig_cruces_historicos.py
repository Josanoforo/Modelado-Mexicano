#!/usr/bin/env python3
"""Cruces históricos ENCIG, congelados antes de abrir las respuestas.

La unidad es el trámite. El remuestreo es de UPM dentro de estrato y un mismo
plan se comparte entre todos los marginales y cruces de una ola. Al remuestrear
una UPM viajan juntos todos sus trámites y, por construcción comprobada, todas
las observaciones de cada persona pertenecen a una sola UPM de diseño.
"""
from __future__ import annotations

import argparse
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


AXES = {
    "SEXO": ("1", "2"),
    "EDAD": ("18-29", "30-44", "45-59", "60-96"),
    "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
}
CROSSES = (
    ("SEXO-EDAD", "SEXO", "EDAD"),
    ("SEXO-ESCOLARIDAD", "SEXO", "ESCOLARIDAD"),
    ("EDAD-ESCOLARIDAD", "EDAD", "ESCOLARIDAD"),
)
QUANTITIES = (
    "N", "PERSONAS", "PERSONAS-EVENTO", "PERSONAS-NO-EVENTO", "PERSONAS-SOLAPE",
    "NUM-W", "DEN-W", "P", "P-EE", "P-IC-LO", "P-IC-HI", "DELTA",
    "DELTA-EE", "DELTA-IC-LO", "DELTA-IC-HI", "B-VALIDAS", "CAUSA",
)


def _guard_inputs(inputs: dict, contract: dict) -> None:
    forbidden = ("encig25", "encig_2025", "2025")
    names = [str(name).lower() for name in inputs]
    if any(token in name for name in names for token in forbidden):
        raise RuntimeError("GUARDIA-ENCIG2025: insumo prohibido")
    permitted = {str(contract["parametros"]["payload_id"])}
    payloads = {name for name in inputs if name != "pisos_encig2023_resultados"}
    if payloads != permitted:
        raise RuntimeError(f"GUARDIA-ALLOWLIST: {sorted(payloads)} != {sorted(permitted)}")


def _code(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _age(series: pd.Series) -> pd.Series:
    value = pd.to_numeric(series, errors="coerce")
    out = pd.Series(pd.NA, index=series.index, dtype="object")
    out[(value >= 18) & (value <= 29)] = "18-29"
    out[(value >= 30) & (value <= 44)] = "30-44"
    out[(value >= 45) & (value <= 59)] = "45-59"
    out[(value >= 60) & (value <= 96)] = "60-96"
    return out


def _school(series: pd.Series) -> pd.Series:
    return _code(series).map({
        "0": "HASTA-PRIMARIA", "1": "HASTA-PRIMARIA", "2": "HASTA-PRIMARIA",
        "3": "SECUNDARIA", "4": "MEDIA-SUPERIOR", "5": "MEDIA-SUPERIOR",
        "6": "MEDIA-SUPERIOR", "7": "MEDIA-SUPERIOR", "8": "SUPERIOR",
        "9": "SUPERIOR",
    })


def _member_csv(archive: str, suffix: str, columns: list[str]) -> pd.DataFrame:
    with zipfile.ZipFile(archive) as zf:
        names = [name for name in zf.namelist() if name.lower().endswith(suffix.lower())]
        if len(names) != 1:
            raise RuntimeError(f"miembro CSV no único: {suffix}: {names}")
        raw = zf.read(names[0])
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            frame = pd.read_csv(io.StringIO(raw.decode(encoding)), dtype=str,
                                keep_default_na=False, na_filter=False)
            frame.columns = [str(column).strip() for column in frame.columns]
            missing = sorted(set(columns) - set(frame.columns))
            if missing:
                raise RuntimeError(f"variables ausentes en {suffix}: {missing}")
            return frame[columns].copy()
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"codificación no reconocida: {suffix}")


def _logit(value: np.ndarray) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log(value / (1.0 - value))


def _ratio(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    return np.divide(num, den, out=np.full_like(num, np.nan, dtype=float), where=den > 0)


def _summary(point: float, replicas: np.ndarray) -> tuple[float | None, float | None, float | None, int]:
    valid = np.isfinite(replicas)
    count = int(valid.sum())
    # Contrato conservador: no se publica precisión condicional si alguna
    # réplica degenera. El punto se conserva si existe.
    if not np.isfinite(point) or count != len(replicas):
        return None, None, None, count
    ee = float(np.std(replicas, ddof=1))
    lo, hi = np.percentile(replicas, [2.5, 97.5])
    return ee, float(lo), float(hi), count


def _people_counts(frame: pd.DataFrame) -> tuple[int, int, int, int]:
    if frame.empty:
        return 0, 0, 0, 0
    by_person = frame.groupby("ID_PER", sort=False)["_y"].agg(["min", "max"])
    event = int((by_person["max"] == 1).sum())
    no_event = int((by_person["min"] == 0).sum())
    overlap = int(((by_person["min"] == 0) & (by_person["max"] == 1)).sum())
    return int(len(by_person)), event, no_event, overlap


def _load_wave(inputs: dict, contract: dict) -> tuple[pd.DataFrame, dict]:
    wave = str(contract["parametros"]["ola"])
    payload_id = str(contract["parametros"]["payload_id"])
    archive = inputs[payload_id]["ruta_absoluta"]
    events = _member_csv(archive, f"encig{wave}_04_sec_7.csv",
        ["N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS", "ID_PER"])
    people = _member_csv(archive, f"encig{wave}_02_residentes_sec_2.csv",
        ["ID_PER", "SEXO", "EDAD", "NIV"])
    if people["ID_PER"].duplicated().any():
        raise RuntimeError("ID_PER no es único en residentes")
    joined = events.merge(people, on="ID_PER", how="left", validate="m:1", indicator=True)
    ntra, p73 = _code(joined["N_TRA"]), _code(joined["P7_3"])
    universe = ntra.eq("1") & p73.isin(("1", "2", "4", "5", "6"))
    frame = joined.loc[universe].copy()
    frame["_w"] = pd.to_numeric(frame["FAC_TRA"], errors="coerce")
    frame["_est"] = frame["EST_DIS"].astype(str).str.strip()
    frame["_upm"] = frame["UPM_DIS"].astype(str).str.strip()
    frame["_y"] = _code(frame["P7_3"]).isin(("4", "5")).astype(float)
    frame["SEXO"] = _code(frame["SEXO"]).where(_code(frame["SEXO"]).isin(AXES["SEXO"]))
    frame["EDAD"] = _age(frame["EDAD"])
    frame["ESCOLARIDAD"] = _school(frame["NIV"])
    design = frame["_w"].notna() & (frame["_w"] > 0) & frame["_est"].ne("") & frame["_upm"].ne("")
    frame = frame.loc[design].copy()
    frame["_key"] = frame["_est"] + "\t" + frame["_upm"]
    memberships = frame.groupby("ID_PER")["_key"].nunique()
    if (memberships > 1).any():
        raise RuntimeError("una persona pertenece a más de una UPM de diseño")
    diagnostics = {
        "FILAS-EVENTOS": int(len(events)),
        "JOIN-SIN-DEMOGRAFIA": int(joined["_merge"].ne("both").sum()),
        "N-UNIVERSO": int(universe.sum()),
        "N-DISENO-VALIDO": int(len(frame)),
        "P7-3-EXCLUIDAS": int((ntra.eq("1") & ~p73.isin(("1", "2", "4", "5", "6"))).sum()),
    }
    return frame, diagnostics


def _matrix_by_psu(frame: pd.DataFrame, masks: list[pd.Series]) -> tuple[list[str], np.ndarray, np.ndarray]:
    keys = sorted(frame["_key"].unique())
    positions = {key: pos for pos, key in enumerate(keys)}
    den = np.zeros((len(keys), len(masks)), dtype=float)
    num = np.zeros_like(den)
    for column, mask in enumerate(masks):
        chosen = frame.loc[mask]
        for key, weight, outcome in zip(chosen["_key"], chosen["_w"], chosen["_y"]):
            pos = positions[key]
            den[pos, column] += float(weight)
            num[pos, column] += float(weight) * float(outcome)
    return keys, num, den


def _bootstrap(frame: pd.DataFrame, masks: list[pd.Series], repetitions: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    keys, num, den = _matrix_by_psu(frame, masks)
    strata: dict[str, list[int]] = {}
    for pos, key in enumerate(keys):
        strata.setdefault(key.split("\t", 1)[0], []).append(pos)
    points = _ratio(num.sum(axis=0), den.sum(axis=0))
    replicas = np.full((repetitions, len(masks)), np.nan, dtype=float)
    rng = np.random.Generator(np.random.PCG64(seed))
    for start in range(0, repetitions, 50):
        size = min(50, repetitions - start)
        multiplicity = np.zeros((size, len(keys)), dtype=np.int16)
        for stratum in sorted(strata):
            indices = np.asarray(strata[stratum], dtype=int)
            # Singleton: PSU de certeza, multiplicidad uno en todas las réplicas.
            if len(indices) == 1:
                multiplicity[:, indices[0]] = 1
                continue
            draws = rng.integers(0, len(indices), size=(size, len(indices)))
            for row in range(size):
                multiplicity[row] += np.bincount(indices[draws[row]], minlength=len(keys)).astype(np.int16)
        replicas[start:start + size] = _ratio(multiplicity @ num, multiplicity @ den)
    return points, replicas, den.sum(axis=0)


def _prefix(wave: str) -> str:
    return f"RESULT-ENCIG{wave}-CRUCES-HISTORICOS"


def _selection_2023(outputs: dict, prefix: str, calc_id: str = "CALC-ENCIG2023-CRUCES-HISTORICOS-0001") -> None:
    states = [outputs[f"{prefix}-{cross}-COHERENCIA"] for cross, _, _ in CROSSES]
    candidates = [cross for cross, _, _ in CROSSES if outputs[f"{prefix}-{cross}-ELEGIBLE"] == "SI"]
    outputs[f"{prefix}-SELECCION-CALCS-CONSUMIDOS"] = calc_id
    outputs[f"{prefix}-SELECCION-CANDIDATOS"] = ",".join(candidates)
    if any(state != "COHERENTE" for state in states):
        outputs[f"{prefix}-SELECCION-RESULTADO"] = "SELECCION-PENDIENTE-DE-DEFINICION"
        outputs[f"{prefix}-SELECCION-CAUSA"] = "al menos un cruce no reproduce marginales sellados sobre su rejilla sustantiva"
        return
    if not candidates:
        outputs[f"{prefix}-SELECCION-RESULTADO"] = "NINGUN-CRUCE-ELEGIBLE-POR-SOPORTE"
        outputs[f"{prefix}-SELECCION-CAUSA"] = "ningún cruce tiene todas sus celdas con n>=200"
        return
    scores = {cross: outputs[f"{prefix}-{cross}-PUNTAJE"] for cross in candidates}
    if any(score is None for score in scores.values()):
        outputs[f"{prefix}-SELECCION-RESULTADO"] = "SELECCION-PENDIENTE-DE-REGLA"
        outputs[f"{prefix}-SELECCION-CAUSA"] = "puntaje degenerado"
        return
    best = max(scores.values())
    tied = [cross for cross, score in scores.items() if best == 0 or (best - score) < 0.10 * best]
    if len(tied) > 1:
        outputs[f"{prefix}-SELECCION-RESULTADO"] = "EMPATE-REQUIERE-ENCIG2021"
        outputs[f"{prefix}-SELECCION-CAUSA"] = ",".join(tied)
        return
    winner = tied[0]
    outputs[f"{prefix}-SELECCION-RESULTADO"] = winner
    outputs[f"{prefix}-SELECCION-CAUSA"] = "mayor puntaje sin empate relativo"


def seleccionar(resultados_2023: dict, resultados_2021: dict | None,
                sello_2023: str, sello_2021: str | None) -> dict:
    """Aplica mecánicamente la regla aprobada a dos resultados ya sellados."""
    p23, p21 = _prefix("2023"), _prefix("2021")
    consumed = {"CALC-ENCIG2023-CRUCES-HISTORICOS-0001": sello_2023}
    if resultados_2021 is not None and sello_2021:
        consumed["CALC-ENCIG2021-CRUCES-HISTORICOS-0001"] = sello_2021
    out = {"calcs_consumidos": consumed}
    incoherent = [cross for cross, _, _ in CROSSES
                  if resultados_2023[f"{p23}-{cross}-COHERENCIA"] != "COHERENTE"]
    if incoherent:
        return out | {"resultado": "SELECCION-PENDIENTE-DE-DEFINICION",
                      "candidatos": [cross for cross, _, _ in CROSSES],
                      "causa": "coherencia de universo: " + ",".join(incoherent)}
    candidates = [cross for cross, _, _ in CROSSES
                  if resultados_2023[f"{p23}-{cross}-ELEGIBLE"] == "SI"]
    if not candidates:
        return out | {"resultado": "NINGUN-CRUCE-ELEGIBLE-POR-SOPORTE",
                      "candidatos": [], "causa": "todas las rejillas fallan n>=200 en al menos una celda"}
    scores = {cross: resultados_2023[f"{p23}-{cross}-PUNTAJE"] for cross in candidates}
    if any(score is None for score in scores.values()):
        return out | {"resultado": "SELECCION-PENDIENTE-DE-REGLA",
                      "candidatos": candidates, "causa": "puntaje degenerado"}
    maximum = max(scores.values())
    tied = [cross for cross, score in scores.items()
            if maximum == 0 or (maximum - score) < 0.10 * maximum]
    concordance = {}
    incomplete_concordance = False
    if len(tied) > 1 and resultados_2021 is not None:
        for cross, axis_a, axis_b in CROSSES:
            if cross not in tied:
                continue
            comparisons = []
            for category_a in AXES[axis_a]:
                for category_b in AXES[axis_b]:
                    suffix = f"{cross}-{category_a}-{category_b}-DELTA"
                    old, new = resultados_2021.get(f"{p21}-{suffix}"), resultados_2023.get(f"{p23}-{suffix}")
                    if old is None or new is None:
                        continue
                    comparisons.append(1 if np.sign(old) == np.sign(new) else 0)
            expected = len(AXES[axis_a]) * len(AXES[axis_b])
            concordance[cross] = (sum(comparisons) / expected) if len(comparisons) == expected else None
            incomplete_concordance |= len(comparisons) != expected
        if incomplete_concordance:
            return out | {"resultado": "SELECCION-PENDIENTE-DE-REGLA", "candidatos": tied,
                          "puntajes": scores, "concordancia_signo": concordance,
                          "causa": "concordancia 2021 no comparable simétricamente"}
        if concordance and all(value is not None for value in concordance.values()):
            top = max(concordance.values())
            tied = [cross for cross in tied if concordance[cross] == top]
    elif len(tied) > 1:
        cell_counts = {cross: next(len(AXES[a]) * len(AXES[b]) for name, a, b in CROSSES if name == cross)
                       for cross in tied}
        least = min(cell_counts.values())
        tied = [cross for cross in tied if cell_counts[cross] == least]
    if len(tied) != 1:
        return out | {"resultado": "SELECCION-PENDIENTE-DE-REGLA", "candidatos": tied,
                      "puntajes": scores, "concordancia_signo": concordance,
                      "causa": "empate persiste después de la regla aplicable"}
    winner = tied[0]
    definition = next(row for row in CROSSES if row[0] == winner)
    _, axis_a, axis_b = definition
    excludes_zero = []
    for category_a in AXES[axis_a]:
        for category_b in AXES[axis_b]:
            base = f"{p23}-{winner}-{category_a}-{category_b}"
            lo, hi = resultados_2023[base + "-DELTA-IC-LO"], resultados_2023[base + "-DELTA-IC-HI"]
            excludes_zero.append(lo is not None and hi is not None and (lo > 0 or hi < 0))
    if not any(excludes_zero):
        verdict = "SIN-PODER-DE-FALSACION"
        cause = f"{winner}: ningún IC95 de delta excluye cero"
    else:
        verdict = winner
        cause = "ganador inequívoco y al menos un IC95 de delta excluye cero"
    return out | {"resultado": verdict, "cruce_elegido": winner, "candidatos": candidates,
                  "puntajes": scores, "concordancia_signo": concordance, "causa": cause}


def medir(inputs: dict, contrato: dict) -> dict:
    _guard_inputs(inputs, contrato)
    wave = str(contrato["parametros"]["ola"])
    repetitions = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    frame, diagnostics = _load_wave(inputs, contrato)
    prefix = _prefix(wave)
    outputs = {f"{prefix}-{key}": value for key, value in diagnostics.items()}
    floor = None
    if wave == "2023":
        floor_path = Path(inputs["pisos_encig2023_resultados"]["ruta_absoluta"])
        floor = json.loads(floor_path.read_text(encoding="utf-8"))["resultados"]

    masks: list[pd.Series] = []
    definitions: list[tuple[str, str, str, pd.Series, pd.Series, pd.Series, pd.Series]] = []
    for cross, axis_a, axis_b in CROSSES:
        complete = frame[axis_a].notna() & frame[axis_b].notna()
        for category_a in AXES[axis_a]:
            for category_b in AXES[axis_b]:
                ab = complete & frame[axis_a].eq(category_a) & frame[axis_b].eq(category_b)
                a = complete & frame[axis_a].eq(category_a)
                b = complete & frame[axis_b].eq(category_b)
                all_common = complete
                definitions.append((cross, category_a, category_b, ab, a, b, all_common))
                masks.extend((ab, a, b, all_common))

    points, boot, weighted_denominators = _bootstrap(frame, masks, repetitions, seed)
    for index, definition in enumerate(definitions):
        cross, category_a, category_b, ab, _a, _b, _all = definition
        offset = index * 4
        p_ab, p_a, p_b, p_all = points[offset:offset + 4]
        delta = float(_logit(np.asarray([p_ab]))[0] - _logit(np.asarray([p_a]))[0]
                      - _logit(np.asarray([p_b]))[0] + _logit(np.asarray([p_all]))[0])
        delta_boot = (_logit(boot[:, offset]) - _logit(boot[:, offset + 1])
                      - _logit(boot[:, offset + 2]) + _logit(boot[:, offset + 3]))
        p_ee, p_lo, p_hi, _ = _summary(float(p_ab), boot[:, offset])
        d_ee, d_lo, d_hi, d_valid = _summary(delta, delta_boot)
        chosen = frame.loc[ab]
        persons, persons_event, persons_no_event, overlap = _people_counts(chosen)
        base = f"{prefix}-{cross}-{category_a}-{category_b}"
        outputs.update({
            base + "-N": int(len(chosen)),
            base + "-PERSONAS": persons,
            base + "-PERSONAS-EVENTO": persons_event,
            base + "-PERSONAS-NO-EVENTO": persons_no_event,
            base + "-PERSONAS-SOLAPE": overlap,
            base + "-NUM-W": float((chosen["_w"] * chosen["_y"]).sum()),
            base + "-DEN-W": float(weighted_denominators[offset]),
            base + "-P": float(p_ab) if np.isfinite(p_ab) else None,
            base + "-P-EE": p_ee,
            base + "-P-IC-LO": p_lo,
            base + "-P-IC-HI": p_hi,
            base + "-DELTA": delta if np.isfinite(delta) else None,
            base + "-DELTA-EE": d_ee,
            base + "-DELTA-IC-LO": d_lo,
            base + "-DELTA-IC-HI": d_hi,
            base + "-B-VALIDAS": d_valid,
            base + "-CAUSA": ("OK" if np.isfinite(delta) and d_valid == repetitions else
                "DEGENERACION-PUNTUAL" if not np.isfinite(delta) else "REPLICA-DEGENERADA"),
        })

    for cross, axis_a, axis_b in CROSSES:
        complete = frame[axis_a].notna() & frame[axis_b].notna()
        lost_a = frame[axis_a].notna() & frame[axis_b].isna()
        lost_b = frame[axis_b].notna() & frame[axis_a].isna()
        base = f"{prefix}-{cross}"
        outputs[base + "-N-COMPLETOS"] = int(complete.sum())
        outputs[base + "-RESIDUO-OTRO-EJE-N-A"] = int(lost_a.sum())
        outputs[base + "-RESIDUO-OTRO-EJE-MASA-A"] = float(frame.loc[lost_a, "_w"].sum())
        outputs[base + "-RESIDUO-OTRO-EJE-N-B"] = int(lost_b.sum())
        outputs[base + "-RESIDUO-OTRO-EJE-MASA-B"] = float(frame.loc[lost_b, "_w"].sum())
        # Una rejilla sustantiva sólo reconstruye el marginal sellado si no
        # necesita el residuo desconocido del otro eje. Si lo necesita, PARA.
        reasons = []
        if lost_a.any() or lost_b.any():
            reasons.append("RESIDUO-OTRO-EJE")
        if floor is not None:
            aliases = {"SEXO": {"1": "1", "2": "2"},
                       "EDAD": {"18-29": "18-29", "30-44": "30-44", "45-59": "45-59", "60-96": "60-MAS"},
                       "ESCOLARIDAD": {"HASTA-PRIMARIA": "HASTA-PRIMARIA", "SECUNDARIA": "SECUNDARIA",
                                        "MEDIA-SUPERIOR": "MEDIA-SUPERIOR", "SUPERIOR": "SUPERIOR"}}
            tolerance = float(contrato["parametros"]["tolerancia_abs"])
            for axis in (axis_a, axis_b):
                for category in AXES[axis]:
                    chosen = frame.loc[frame[axis].eq(category)]
                    denominator = float(chosen["_w"].sum())
                    numerator = float((chosen["_w"] * chosen["_y"]).sum())
                    point = numerator / denominator if denominator > 0 else math.nan
                    floor_base = f"RESULT-PISOS-ENCIG2023-V2-DIGITAL-{axis}-{aliases[axis][category]}"
                    if (abs(denominator - float(floor[floor_base + "-DEN-W"])) > tolerance
                            or abs(point - float(floor[floor_base + "-P"])) > tolerance):
                        reasons.append(f"NO-REPRODUCE-PISO:{axis}:{category}")
        if reasons:
            outputs[base + "-COHERENCIA"] = ("PARO-COHERENCIA-UNIVERSO" if reasons == ["RESIDUO-OTRO-EJE"]
                                                else "PARO-CONTROL-MARGINAL")
            outputs[base + "-COHERENCIA-CAUSA"] = ";".join(reasons)
        else:
            outputs[base + "-COHERENCIA"] = "COHERENTE"
            outputs[base + "-COHERENCIA-CAUSA"] = "OK"
        cell_bases = [f"{base}-{a}-{b}" for a in AXES[axis_a] for b in AXES[axis_b]]
        outputs[base + "-ELEGIBLE"] = "SI" if all(outputs[cell + "-N"] >= 200 for cell in cell_bases) else "NO"
        ratios = []
        for cell in cell_bases:
            delta, ee = outputs[cell + "-DELTA"], outputs[cell + "-DELTA-EE"]
            if delta is None or ee is None or ee <= 0:
                ratios = []
                break
            ratios.append(abs(delta) / ee)
        outputs[base + "-PUNTAJE"] = float(np.mean(ratios)) if ratios else None

    if wave == "2023":
        _selection_2023(outputs, prefix, str(contrato["parametros"]["calc_id"]))
    return outputs


def declared_results(wave: str) -> list[tuple[str, str, str]]:
    prefix = _prefix(wave)
    out: list[tuple[str, str, str]] = []
    types = {
        "N": ("entero", "trámites"), "PERSONAS": ("entero", "personas distintas"),
        "PERSONAS-EVENTO": ("entero", "personas distintas"),
        "PERSONAS-NO-EVENTO": ("entero", "personas distintas"),
        "PERSONAS-SOLAPE": ("entero", "personas distintas"),
        "NUM-W": ("flotante", "numerador ponderado"), "DEN-W": ("flotante", "denominador ponderado"),
        "P": ("proporcion", "proporción [0,1]"), "P-EE": ("flotante", "error estándar"),
        "P-IC-LO": ("proporcion", "límite inferior IC95"), "P-IC-HI": ("proporcion", "límite superior IC95"),
        "DELTA": ("flotante", "logit"), "DELTA-EE": ("flotante", "error estándar logit"),
        "DELTA-IC-LO": ("flotante", "límite inferior IC95 logit"),
        "DELTA-IC-HI": ("flotante", "límite superior IC95 logit"),
        "B-VALIDAS": ("entero", "réplicas definidas"), "CAUSA": ("texto", "estado"),
    }
    for cross, axis_a, axis_b in CROSSES:
        for category_a in AXES[axis_a]:
            for category_b in AXES[axis_b]:
                base = f"{prefix}-{cross}-{category_a}-{category_b}"
                for quantity in QUANTITIES:
                    out.append((base + "-" + quantity, *types[quantity]))
        for suffix, kind, unit in (
            ("N-COMPLETOS", "entero", "trámites"),
            ("RESIDUO-OTRO-EJE-N-A", "entero", "trámites"),
            ("RESIDUO-OTRO-EJE-MASA-A", "flotante", "masa ponderada"),
            ("RESIDUO-OTRO-EJE-N-B", "entero", "trámites"),
            ("RESIDUO-OTRO-EJE-MASA-B", "flotante", "masa ponderada"),
            ("COHERENCIA", "texto", "estado"), ("COHERENCIA-CAUSA", "texto", "causa"),
            ("ELEGIBLE", "texto", "SI/NO"),
            ("PUNTAJE", "flotante", "media |delta|/EE"),
        ):
            out.append((f"{prefix}-{cross}-{suffix}", kind, unit))
    for suffix in ("FILAS-EVENTOS", "JOIN-SIN-DEMOGRAFIA", "N-UNIVERSO", "N-DISENO-VALIDO", "P7-3-EXCLUIDAS"):
        out.append((f"{prefix}-{suffix}", "entero", "filas"))
    if wave == "2023":
        out.extend((f"{prefix}-{suffix}", "texto", "estado") for suffix in
                   ("SELECCION-CALCS-CONSUMIDOS", "SELECCION-CANDIDATOS", "SELECCION-RESULTADO", "SELECCION-CAUSA"))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--declaraciones", choices=("2021", "2023"))
    parser.add_argument("--seleccionar", nargs=2, metavar=("RESULTADOS_2023", "RESULTADOS_2021"))
    parser.add_argument("--sello-2023")
    parser.add_argument("--sello-2021")
    args = parser.parse_args()
    if args.declaraciones:
        for result_id, kind, unit in declared_results(args.declaraciones):
            print(f"  - {{id: {result_id}, tipo: {kind}, unidad: \"{unit}\"}}")
    if args.seleccionar:
        if not args.sello_2023:
            parser.error("--sello-2023 es obligatorio con --seleccionar")
        paths = [Path(item) for item in args.seleccionar]
        r23 = json.loads(paths[0].read_text(encoding="utf-8"))["resultados"]
        r21 = None if str(paths[1]) == "-" else json.loads(paths[1].read_text(encoding="utf-8"))["resultados"]
        print(json.dumps(seleccionar(r23, r21, args.sello_2023, args.sello_2021),
                         ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Distribución y concentración de horas de cuidado, ENUT 2024."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


CALC_ID = "CALC-ENUT2024-DISTRIBUCION-HORAS-0002"
INPUT_DATA = "enut2024_bd_csv"
INPUT_FD = "enut2024_fd_xlsx"
EXPECTED = {
    INPUT_DATA: "25f35626464053441b367b24001d255dbca408b5f576e614e0e09ac58691c4ba",
    INPUT_FD: "4a7dddf1bc0612f5e72694b146848804edc47d8f00c86e7d34d1cfb8f5ec3f58",
}
CON = ["CUID_ESP_INT_HOG_CON_CP", "CUID_INT_0A5_CON_CP",
       "CUID_INT_6A14_CON_CP", "CUID_INT_60MAS_CON_CP"]
SIN = ["CUID_ESP_INT_HOG_SIN_CP", "CUID_INT_0A5_SIN_CP",
       "CUID_INT_6A14_SIN_CP", "CUID_INT_60MAS_SIN_CP"]
MAXIMUM = {
    "CUID_ESP_INT_HOG_CON_CP": 201.25,
    "CUID_INT_0A5_CON_CP": 280.0,
    "CUID_INT_6A14_CON_CP": 152.41666666666667,
    "CUID_INT_60MAS_CON_CP": 147.0,
    "CUID_ESP_INT_HOG_SIN_CP": 136.83333333333334,
    "CUID_INT_0A5_SIN_CP": 217.23333333333332,
    "CUID_INT_6A14_SIN_CP": 116.13333333333334,
    "CUID_INT_60MAS_SIN_CP": 74.0,
}
REQUIRED = {"LLAVEMOD", "SEXO", "EDAD", "FAC_PER", "EST_DIS", "UPM_DIS", *CON, *SIN}
SEXES = ("total", "hombre", "mujer")
DOMAINS = ("todas_validas", "participantes")
MEASURES = ("p25", "p50", "p75", "p90", "concentracion_decil_superior")
QUANTILES = (("p25", .25), ("p50", .50), ("p75", .75), ("p90", .90))
ESTIMATE_COLUMNS = [
    "variante", "sexo", "dominio", "medida", "estimacion", "ic95_inferior",
    "ic95_superior", "estado", "replicas_validas", "replicas_totales",
    "precision_nota", "n_marco", "masa_marco", "n_dominio", "masa_dominio",
    "cobertura_n", "cobertura_ponderada", "ponderador", "unidad",
]
CONTRAST_COLUMNS = [
    "tipo", "variante", "sexo", "dominio", "medida", "estimacion",
    "ic95_inferior", "ic95_superior", "estado", "replicas_validas",
    "replicas_totales", "precision_nota", "unidad",
]


def _bytes(entry: dict) -> bytes:
    return entry.get("bytes") if entry.get("bytes") is not None else Path(entry["ruta_absoluta"]).read_bytes()


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def prepare_frame(frame: pd.DataFrame):
    """Devuelve universo común, incidencias, marco 12--96 y marco de diseño."""
    missing = sorted(REQUIRED - set(frame.columns))
    if missing:
        raise ValueError(f"VARIABLES-AUSENTES:{missing}")
    work = frame[list(sorted(REQUIRED))].copy()
    incidence: dict[str, object] = {}
    incidence["llavemod_faltante"] = int((work["LLAVEMOD"].isna() | work["LLAVEMOD"].eq("")).sum())
    incidence["llavemod_duplicada"] = int(work["LLAVEMOD"].duplicated(keep=False).sum())
    if incidence["llavemod_faltante"] or incidence["llavemod_duplicada"]:
        raise ValueError("LLAVEMOD-NO-UNICA-O-FALTANTE")

    for col in ["EDAD", "FAC_PER", *CON, *SIN]:
        work[col] = pd.to_numeric(work[col], errors="coerce")
    weight_ok = work["FAC_PER"].notna() & np.isfinite(work["FAC_PER"]) & work["FAC_PER"].gt(0)
    design_ok = (work["EST_DIS"].notna() & work["EST_DIS"].ne("") &
                 work["UPM_DIS"].notna() & work["UPM_DIS"].ne(""))
    sex_ok = work["SEXO"].isin(["1", "2"])
    age_ok = work["EDAD"].between(12, 96, inclusive="both")
    analytic_base = weight_ok & design_ok & sex_ok & age_ok
    design_frame = work.loc[weight_ok & design_ok].copy()
    universe = work.loc[analytic_base].copy()
    incidence.update({
        "sexo_fuera_1_2": int((~sex_ok).sum()),
        "edad_faltante_o_fuera_12_96": int((~age_ok).sum()),
        "fac_per_invalido": int((~weight_ok).sum()),
        "diseno_faltante": int((~design_ok).sum()),
    })
    hours_valid = pd.Series(True, index=work.index)
    per_hour = {}
    for col in [*CON, *SIN]:
        missing_col = work[col].isna() | ~np.isfinite(work[col])
        negative = work[col].lt(0)
        over = work[col].gt(MAXIMUM[col])
        per_hour[col] = {
            "faltante_no_numerico": int(missing_col.sum()),
            "negativo": int(negative.sum()),
            "sobre_maximo_fd": int(over.sum()),
        }
        hours_valid &= ~(missing_col | negative | over)
    incidence["horas_por_variable"] = per_hour
    incidence["filas_fuera_universo_comun"] = int((~(analytic_base & hours_valid)).sum())

    work["sexo"] = work["SEXO"].map({"1": "hombre", "2": "mujer"})
    universe = work.loc[analytic_base].copy()
    valid = work.loc[analytic_base & hours_valid].copy()
    valid["h_con_cp"] = valid[CON].sum(axis=1)
    valid["h_sin_cp"] = valid[SIN].sum(axis=1)
    return valid, incidence, universe, design_frame


def weighted_quantile(values: np.ndarray, weights: np.ndarray, probability: float):
    """Inversa izquierda de CDF ponderada, sin interpolación."""
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    keep = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not keep.any():
        return None
    values, weights = values[keep], weights[keep]
    order = np.argsort(values, kind="mergesort")
    values, weights = values[order], weights[order]
    target = probability * weights.sum()
    index = min(int(np.searchsorted(np.cumsum(weights), target, side="left")), len(values) - 1)
    return float(values[index])


def top_mass_hour_share(values: np.ndarray, weights: np.ndarray, fraction: float = .10):
    """Horas del `fraction` superior de masa; fracciona peso en el umbral."""
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    keep = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not keep.any():
        return None
    values, weights = values[keep], weights[keep]
    total_hours = float(np.dot(values, weights))
    if total_hours <= 0:
        return None
    order = np.argsort(-values, kind="mergesort")
    values, weights = values[order], weights[order]
    target = fraction * float(weights.sum())
    cumulative = np.cumsum(weights)
    index = min(int(np.searchsorted(cumulative, target, side="left")), len(values) - 1)
    mass_before = float(cumulative[index - 1]) if index else 0.0
    hours_before = float(np.dot(values[:index], weights[:index])) if index else 0.0
    selected_hours = hours_before + (target - mass_before) * float(values[index])
    return selected_hours / total_hours


def distribution_measures(values: np.ndarray, weights: np.ndarray) -> dict[str, float | None]:
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    keep = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    order = np.argsort(values[keep], kind="mergesort")
    out = _distribution_measures_sorted(values[keep][order], weights[keep][order])
    return out


def _distribution_measures_sorted(values: np.ndarray, weights: np.ndarray) -> dict[str, float | None]:
    """Calcula todos los estimandos con valores ya ordenados ascendentemente."""
    keep = weights > 0
    values, weights = values[keep], weights[keep]
    if not len(values):
        return {measure: None for measure in MEASURES}
    cumulative = np.cumsum(weights)
    total_mass = float(cumulative[-1])
    out = {}
    for name, probability in QUANTILES:
        index = min(int(np.searchsorted(cumulative, probability * total_mass, side="left")), len(values) - 1)
        out[name] = float(values[index])
    total_hours = float(np.dot(values, weights))
    if total_hours <= 0:
        out["concentracion_decil_superior"] = None
        return out
    reverse_weights = weights[::-1]
    reverse_values = values[::-1]
    reverse_cumulative = np.cumsum(reverse_weights)
    target = .10 * total_mass
    index = min(int(np.searchsorted(reverse_cumulative, target, side="left")), len(values) - 1)
    mass_before = float(reverse_cumulative[index - 1]) if index else 0.0
    hours_before = float(np.dot(reverse_values[:index], reverse_weights[:index])) if index else 0.0
    selected = hours_before + (target - mass_before) * float(reverse_values[index])
    out["concentracion_decil_superior"] = selected / total_hours
    return out


def _bootstrap_plan(design: pd.DataFrame, n_boot: int, seed: int):
    keys = list(zip(design["EST_DIS"].astype(str), design["UPM_DIS"].astype(str)))
    unique = sorted(set(keys))
    key_to_i = {key: i for i, key in enumerate(unique)}
    by_stratum: dict[str, list[int]] = {}
    for i, (stratum, _) in enumerate(unique):
        by_stratum.setdefault(stratum, []).append(i)
    rng = np.random.Generator(np.random.PCG64(seed))
    plan = np.zeros((n_boot, len(unique)), dtype=np.int16)
    rr = np.arange(n_boot)[:, None]
    for stratum in sorted(by_stratum):
        ids = np.asarray(by_stratum[stratum], dtype=np.int64)
        draws = rng.integers(0, len(ids), size=(n_boot, len(ids)))
        np.add.at(plan, (rr, ids[draws]), 1)
    meta = {
        "n_estratos": len(by_stratum),
        "n_upm": len(unique),
        "n_estratos_upm_unica": sum(len(ids) == 1 for ids in by_stratum.values()),
        "pares_sha256": _sha("\n".join(f"{a}\t{b}" for a, b in unique).encode()),
    }
    return plan, key_to_i, meta


def _precision_note(point, finite: np.ndarray, n_boot: int, lo, hi) -> str:
    if point is None:
        return "NO-ESTIMABLE: denominador o total de horas cero"
    if len(finite) < n_boot:
        return f"PRECISION-NO-SUSTENTADA: {n_boot-len(finite)} replicas no estimables"
    if lo == hi:
        return "IC-COLAPSADO-POR-MASA-DISCRETA; no demuestra ausencia de error"
    return ""


def analyse(valid: pd.DataFrame, universe: pd.DataFrame, design: pd.DataFrame,
            n_boot: int, seed: int):
    plan, key_to_i, meta = _bootstrap_plan(design, n_boot, seed)
    valid_cluster = np.fromiter(
        (key_to_i[(str(a), str(b))] for a, b in zip(valid["EST_DIS"], valid["UPM_DIS"])),
        dtype=np.int64,
    )
    base_weight = valid["FAC_PER"].to_numpy(float)
    estimates: list[dict] = []
    points: dict[tuple, float | None] = {}
    replicates: dict[tuple, np.ndarray] = {}

    sex_masks = {
        "total": np.ones(len(valid), dtype=bool),
        "hombre": valid["sexo"].eq("hombre").to_numpy(),
        "mujer": valid["sexo"].eq("mujer").to_numpy(),
    }
    universe_masks = {
        "total": np.ones(len(universe), dtype=bool),
        "hombre": universe["SEXO"].eq("1").to_numpy(),
        "mujer": universe["SEXO"].eq("2").to_numpy(),
    }

    for variant, hcol in (("CON_CP", "h_con_cp"), ("SIN_CP", "h_sin_cp")):
        hours = valid[hcol].to_numpy(float)
        for sex in SEXES:
            sex_mask = sex_masks[sex]
            marco_mask = universe_masks[sex]
            n_marco = int(marco_mask.sum())
            mass_marco = float(universe.loc[marco_mask, "FAC_PER"].sum())
            n_valid_sex = int(sex_mask.sum())
            mass_valid_sex = float(base_weight[sex_mask].sum())
            for domain in DOMAINS:
                mask = sex_mask & ((hours > 0) if domain == "participantes" else True)
                values = hours[mask]
                weights = base_weight[mask]
                clusters = valid_cluster[mask]
                order = np.argsort(values, kind="mergesort")
                values, weights, clusters = values[order], weights[order], clusters[order]
                n_domain = int(mask.sum())
                mass_domain = float(weights.sum())
                denominator_n = n_valid_sex if domain == "participantes" else n_marco
                denominator_mass = mass_valid_sex if domain == "participantes" else mass_marco
                point_values = _distribution_measures_sorted(values, weights)
                draws = {measure: np.full(n_boot, np.nan) for measure in MEASURES}
                for r in range(n_boot):
                    replicate_weight = weights * plan[r, clusters]
                    result = _distribution_measures_sorted(values, replicate_weight)
                    for measure in MEASURES:
                        if result[measure] is not None:
                            draws[measure][r] = result[measure]
                for measure in MEASURES:
                    point = point_values[measure]
                    finite = draws[measure][np.isfinite(draws[measure])]
                    ok = point is not None and len(finite) == n_boot
                    lo, hi = (np.percentile(finite, [2.5, 97.5])
                              if point is not None and len(finite) else (None, None))
                    key = (variant, sex, domain, measure)
                    points[key], replicates[key] = point, draws[measure]
                    estimates.append({
                        "variante": variant, "sexo": sex, "dominio": domain,
                        "medida": measure, "estimacion": point,
                        "ic95_inferior": lo, "ic95_superior": hi,
                        "estado": "OK" if ok else "NO-ESTIMABLE",
                        "replicas_validas": len(finite), "replicas_totales": n_boot,
                        "precision_nota": _precision_note(point, finite, n_boot, lo, hi),
                        "n_marco": n_marco if domain == "todas_validas" else n_valid_sex,
                        "masa_marco": mass_marco if domain == "todas_validas" else mass_valid_sex,
                        "n_dominio": n_domain, "masa_dominio": mass_domain,
                        "cobertura_n": n_domain / denominator_n if denominator_n else None,
                        "cobertura_ponderada": mass_domain / denominator_mass if denominator_mass else None,
                        "ponderador": "FAC_PER",
                        "unidad": "proporcion de horas" if measure.startswith("concentracion") else "horas/semana",
                    })

    contrasts: list[dict] = []

    def add_contrast(kind: str, variant: str, sex: str, domain: str, measure: str,
                     left: tuple, right: tuple):
        left_point, right_point = points[left], points[right]
        draws = replicates[left] - replicates[right]
        finite = draws[np.isfinite(draws)]
        point = left_point - right_point if left_point is not None and right_point is not None else None
        ok = point is not None and len(finite) == n_boot
        lo, hi = (np.percentile(finite, [2.5, 97.5])
                  if point is not None and len(finite) else (None, None))
        contrasts.append({
            "tipo": kind, "variante": variant, "sexo": sex, "dominio": domain,
            "medida": measure, "estimacion": point, "ic95_inferior": lo,
            "ic95_superior": hi, "estado": "OK" if ok else "NO-ESTIMABLE",
            "replicas_validas": len(finite), "replicas_totales": n_boot,
            "precision_nota": _precision_note(point, finite, n_boot, lo, hi),
            "unidad": "diferencia de proporciones de horas" if measure.startswith("concentracion") else "horas/semana",
        })

    for sex in SEXES:
        for domain in DOMAINS:
            for measure in ("p50", "p90", "concentracion_decil_superior"):
                add_contrast("sin_cp_menos_con_cp", "PAREADA", sex, domain, measure,
                             ("SIN_CP", sex, domain, measure), ("CON_CP", sex, domain, measure))
    for domain in DOMAINS:
        for measure in ("p50", "p90"):
            add_contrast("mujer_menos_hombre", "CON_CP", "mujer-hombre", domain, measure,
                         ("CON_CP", "mujer", domain, measure), ("CON_CP", "hombre", domain, measure))
    return estimates, contrasts, meta


def _fmt(value):
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return ""
    if isinstance(value, (int, np.integer)):
        return str(value)
    return f"{float(value):.12f}" if isinstance(value, (float, np.floating)) else value


def _write_csv(path: Path, columns: list[str], rows: list[dict]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _fmt(value) for key, value in row.items()})
    return _sha(path.read_bytes())


def medir(inputs: dict, contrato: dict) -> dict:
    raw, fd = _bytes(inputs[INPUT_DATA]), _bytes(inputs[INPUT_FD])
    for iid, content in ((INPUT_DATA, raw), (INPUT_FD, fd)):
        if _sha(content) != EXPECTED[iid]:
            raise ValueError(f"SHA256-NO-COINCIDE:{iid}")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if "tvar_crea.csv" not in archive.namelist():
            raise ValueError("MIEMBRO-AUSENTE:tvar_crea.csv")
        frame = pd.read_csv(archive.open("tvar_crea.csv"), dtype=str, low_memory=False)
    valid, incidence, universe, design = prepare_frame(frame)
    estimates, contrasts, meta = analyse(
        valid, universe, design,
        int(contrato["parametros"]["bootstrap_replicas"]), int(contrato["seed"]["valor"]),
    )
    root = Path(__file__).resolve().parents[3]
    out_dir = root / contrato["parametros"]["directorio_salida"]
    distribution_path = out_dir / "enut2024-distribucion-horas-estimaciones.csv"
    contrasts_path = out_dir / "enut2024-distribucion-horas-contrastes.csv"
    incidence_path = out_dir / "enut2024-distribucion-horas-incidencias.json"
    dist_sha = _write_csv(distribution_path, ESTIMATE_COLUMNS, estimates)
    contrast_sha = _write_csv(contrasts_path, CONTRAST_COLUMNS, contrasts)
    incidence["diseno"] = meta
    incidence_path.parent.mkdir(parents=True, exist_ok=True)
    incidence_path.write_text(json.dumps(incidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    incidence_sha = _sha(incidence_path.read_bytes())
    idx = {(r["variante"], r["sexo"], r["dominio"], r["medida"]): r for r in estimates}
    cidx = {(r["tipo"], r["sexo"], r["dominio"], r["medida"]): r for r in contrasts}
    return {
        "RESULT-ENUTDH2-G-INPUT-BD-SHA256": _sha(raw),
        "RESULT-ENUTDH2-G-INPUT-FD-SHA256": _sha(fd),
        "RESULT-ENUTDH2-G-N-MARCO": int(len(frame)),
        "RESULT-ENUTDH2-G-N-VALIDO-COMUN": int(len(valid)),
        "RESULT-ENUTDH2-G-MASA-VALIDA-COMUN": float(valid["FAC_PER"].sum()),
        "RESULT-ENUTDH2-G-N-ESTRATOS": meta["n_estratos"],
        "RESULT-ENUTDH2-G-N-UPM": meta["n_upm"],
        "RESULT-ENUTDH2-G-N-ESTRATOS-UPM-UNICA": meta["n_estratos_upm_unica"],
        "RESULT-ENUTDH2-G-PARES-DISENO-SHA256": meta["pares_sha256"],
        "RESULT-ENUTDH2-G-DISTRIBUCION-N-FILAS": len(estimates),
        "RESULT-ENUTDH2-G-CONTRASTES-N-FILAS": len(contrasts),
        "RESULT-ENUTDH2-G-DISTRIBUCION-SHA256": dist_sha,
        "RESULT-ENUTDH2-G-CONTRASTES-SHA256": contrast_sha,
        "RESULT-ENUTDH2-G-INCIDENCIAS-SHA256": incidence_sha,
        "RESULT-ENUTDH2-G-INCIDENCIAS": json.dumps(incidence, ensure_ascii=False, sort_keys=True),
        "RESULT-ENUTDH2-A-CON-TODAS-P50": float(idx[("CON_CP", "total", "todas_validas", "p50")]["estimacion"]),
        "RESULT-ENUTDH2-A-CON-TODAS-P90": float(idx[("CON_CP", "total", "todas_validas", "p90")]["estimacion"]),
        "RESULT-ENUTDH2-A-CON-TODAS-CONCENTRACION": float(idx[("CON_CP", "total", "todas_validas", "concentracion_decil_superior")]["estimacion"]),
        "RESULT-ENUTDH2-A-CON-PARTICIPANTES-P50": float(idx[("CON_CP", "total", "participantes", "p50")]["estimacion"]),
        "RESULT-ENUTDH2-A-CON-PARTICIPANTES-P90": float(idx[("CON_CP", "total", "participantes", "p90")]["estimacion"]),
        "RESULT-ENUTDH2-A-CON-PARTICIPANTES-CONCENTRACION": float(idx[("CON_CP", "total", "participantes", "concentracion_decil_superior")]["estimacion"]),
        "RESULT-ENUTDH2-A-CON-BRECHA-TODAS-P50": float(cidx[("mujer_menos_hombre", "mujer-hombre", "todas_validas", "p50")]["estimacion"]),
        "RESULT-ENUTDH2-A-CON-BRECHA-TODAS-P90": float(cidx[("mujer_menos_hombre", "mujer-hombre", "todas_validas", "p90")]["estimacion"]),
        "RESULT-ENUTDH2-G-SALIDA-DISTRIBUCION": str(distribution_path.relative_to(root)),
        "RESULT-ENUTDH2-G-SALIDA-CONTRASTES": str(contrasts_path.relative_to(root)),
        "RESULT-ENUTDH2-G-SALIDA-INCIDENCIAS": str(incidence_path.relative_to(root)),
    }

#!/usr/bin/env python3
"""Participación e intensidad de cuidado por sexo y edad, ENUT 2024."""
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


CALC_ID = "CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001"
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
AGES = ("12-17", "18-29", "30-39", "40-59", "60+")
SEXES = ("hombre", "mujer")
MEASURES = ("participacion", "media_incluye_ceros", "media_participantes")
ESTIMATE_COLUMNS = [
    "variante", "desglose", "grupo", "medida", "estimacion", "ic95_inferior",
    "ic95_superior", "estado", "n_marco_grupo", "masa_marco_grupo",
    "n_valido_comun", "masa_valida_comun", "cobertura_n", "cobertura_ponderada",
    "n_participantes", "masa_participantes", "ponderador", "unidad",
]
CONTRAST_COLUMNS = [
    "tipo", "variante", "tramo_edad", "desglose", "grupo", "medida",
    "estimacion", "ic95_inferior", "ic95_superior", "estado", "unidad",
]


def _bytes(entry: dict) -> bytes:
    return entry.get("bytes") if entry.get("bytes") is not None else Path(entry["ruta_absoluta"]).read_bytes()


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _age_group(age: pd.Series) -> pd.Series:
    return pd.cut(age, [11, 17, 29, 39, 59, 96], labels=AGES).astype("string")


def prepare_frame(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """Normaliza sin imputar y devuelve universo común, incidencias y marco válido."""
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
    base = (
        work["SEXO"].isin(["1", "2"])
        & work["EDAD"].between(12, 96, inclusive="both")
        & work["FAC_PER"].notna() & np.isfinite(work["FAC_PER"]) & work["FAC_PER"].gt(0)
        & work["EST_DIS"].notna() & work["EST_DIS"].ne("")
        & work["UPM_DIS"].notna() & work["UPM_DIS"].ne("")
    )
    incidence.update({
        "sexo_fuera_1_2": int((~work["SEXO"].isin(["1", "2"])).sum()),
        "edad_faltante_o_fuera_12_96": int((~work["EDAD"].between(12, 96, inclusive="both")).sum()),
        "fac_per_invalido": int((work["FAC_PER"].isna() | ~np.isfinite(work["FAC_PER"]) | work["FAC_PER"].le(0)).sum()),
        "diseno_faltante": int((work["EST_DIS"].isna() | work["EST_DIS"].eq("") | work["UPM_DIS"].isna() | work["UPM_DIS"].eq("")).sum()),
    })
    hours_valid = pd.Series(True, index=work.index)
    per_hour = {}
    for col in [*CON, *SIN]:
        missing_col = work[col].isna() | ~np.isfinite(work[col])
        negative = work[col].lt(0)
        over = work[col].gt(MAXIMUM[col])
        per_hour[col] = {"faltante_no_numerico": int(missing_col.sum()),
                         "negativo": int(negative.sum()), "sobre_maximo_fd": int(over.sum())}
        hours_valid &= ~(missing_col | negative | over)
    incidence["horas_por_variable"] = per_hour
    incidence["filas_fuera_universo_comun"] = int((~(base & hours_valid)).sum())

    work["sexo"] = work["SEXO"].map({"1": "hombre", "2": "mujer"})
    work["edad_tramo"] = _age_group(work["EDAD"])
    marco = work.loc[base].copy()
    valid = work.loc[base & hours_valid].copy()
    valid["h_con_cp"] = valid[CON].sum(axis=1)
    valid["h_sin_cp"] = valid[SIN].sum(axis=1)
    return valid, incidence, marco


def _domains(frame: pd.DataFrame) -> list[tuple[str, str, np.ndarray]]:
    domains = [("nacional", "total", np.ones(len(frame), dtype=bool))]
    domains += [("sexo", sex, frame["sexo"].eq(sex).to_numpy()) for sex in SEXES]
    domains += [("edad", age, frame["edad_tramo"].eq(age).to_numpy()) for age in AGES]
    domains += [("sexo_edad", f"{sex} · {age}",
                 (frame["sexo"].eq(sex) & frame["edad_tramo"].eq(age)).to_numpy())
                for age in AGES for sex in SEXES]
    return domains


def _bootstrap_plan(frame: pd.DataFrame, n_boot: int, seed: int) -> tuple[np.ndarray, np.ndarray, int]:
    keys = list(zip(frame["EST_DIS"].astype(str), frame["UPM_DIS"].astype(str)))
    unique = sorted(set(keys))
    key_to_i = {key: i for i, key in enumerate(unique)}
    row_cluster = np.fromiter((key_to_i[k] for k in keys), dtype=np.int64)
    by_stratum: dict[str, list[int]] = {}
    for i, (stratum, _) in enumerate(unique):
        by_stratum.setdefault(stratum, []).append(i)
    one_psu = sum(len(v) == 1 for v in by_stratum.values())
    rng = np.random.Generator(np.random.PCG64(seed))
    plan = np.zeros((n_boot, len(unique)), dtype=np.int16)
    rr = np.arange(n_boot)[:, None]
    for stratum in sorted(by_stratum):
        ids = np.asarray(by_stratum[stratum], dtype=np.int64)
        draws = rng.integers(0, len(ids), size=(n_boot, len(ids)))
        np.add.at(plan, (rr, ids[draws]), 1)
    return plan, row_cluster, one_psu


def _safe_ratio(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    return np.divide(num, den, out=np.full_like(num, np.nan, dtype=float), where=den > 0)


def _fmt(value):
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return ""
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.12f}"


def analyse(frame: pd.DataFrame, marco: pd.DataFrame, n_boot: int, seed: int):
    domains = _domains(frame)
    marco_domains = {(d, g): mask for d, g, mask in _domains(marco)}
    plan, cluster, one_psu = _bootstrap_plan(frame, n_boot, seed)
    ncl = plan.shape[1]
    w = frame["FAC_PER"].to_numpy(float)
    estimates, reps = [], {}
    sufficient = {}

    for variant, hcol in (("CON_CP", "h_con_cp"), ("SIN_CP", "h_sin_cp")):
        h = frame[hcol].to_numpy(float)
        part = h > 0
        for breakdown, group, mask in domains:
            weighted = w * mask
            arrays = [weighted, weighted * part, weighted * h]
            cluster_sums = []
            for values in arrays:
                out = np.zeros(ncl, dtype=float)
                np.add.at(out, cluster, values)
                cluster_sums.append(out)
            totals = [float(x.sum()) for x in cluster_sums]
            boot_totals = [plan @ x for x in cluster_sums]
            values = {
                "participacion": (totals[1] / totals[0] if totals[0] else None,
                                  _safe_ratio(boot_totals[1], boot_totals[0])),
                "media_incluye_ceros": (totals[2] / totals[0] if totals[0] else None,
                                        _safe_ratio(boot_totals[2], boot_totals[0])),
                "media_participantes": (totals[2] / totals[1] if totals[1] else None,
                                        _safe_ratio(boot_totals[2], boot_totals[1])),
            }
            marco_mask = marco_domains[(breakdown, group)]
            marco_n = int(marco_mask.sum())
            marco_mass = float(marco.loc[marco_mask, "FAC_PER"].sum())
            n_valid, n_part = int(mask.sum()), int((mask & part).sum())
            for measure, (point, draws) in values.items():
                finite = draws[np.isfinite(draws)]
                estimable = point is not None and len(finite) == n_boot
                lo, hi = (np.percentile(finite, [2.5, 97.5]) if estimable else (None, None))
                estimates.append({
                    "variante": variant, "desglose": breakdown, "grupo": group,
                    "medida": measure, "estimacion": point, "ic95_inferior": lo,
                    "ic95_superior": hi, "estado": "OK" if estimable else "NO-ESTIMABLE",
                    "n_marco_grupo": marco_n, "masa_marco_grupo": marco_mass,
                    "n_valido_comun": n_valid, "masa_valida_comun": totals[0],
                    "cobertura_n": n_valid / marco_n if marco_n else None,
                    "cobertura_ponderada": totals[0] / marco_mass if marco_mass else None,
                    "n_participantes": n_part, "masa_participantes": totals[1],
                    "ponderador": "FAC_PER",
                    "unidad": "proporcion" if measure == "participacion" else "horas/semana",
                })
                reps[(variant, breakdown, group, measure)] = draws
                sufficient[(variant, breakdown, group, measure)] = point

    contrasts = []
    for variant in ("CON_CP", "SIN_CP"):
        for age in ("total", *AGES):
            breakdown = "sexo" if age == "total" else "sexo_edad"
            male, female = ("hombre", "mujer") if age == "total" else (f"hombre · {age}", f"mujer · {age}")
            for measure in MEASURES:
                m = sufficient[(variant, breakdown, male, measure)]
                f = sufficient[(variant, breakdown, female, measure)]
                draws = reps[(variant, breakdown, female, measure)] - reps[(variant, breakdown, male, measure)]
                finite = draws[np.isfinite(draws)]
                ok = m is not None and f is not None and len(finite) == n_boot
                lo, hi = np.percentile(finite, [2.5, 97.5]) if ok else (None, None)
                contrasts.append({"tipo": "mujer_menos_hombre", "variante": variant,
                                  "tramo_edad": age, "desglose": breakdown, "grupo": age,
                                  "medida": measure, "estimacion": f - m if ok else None,
                                  "ic95_inferior": lo, "ic95_superior": hi,
                                  "estado": "OK" if ok else "NO-ESTIMABLE",
                                  "unidad": "diferencia de proporciones" if measure == "participacion" else "horas/semana"})
    for breakdown, group, _ in domains:
        for measure in MEASURES:
            con = sufficient[("CON_CP", breakdown, group, measure)]
            sin = sufficient[("SIN_CP", breakdown, group, measure)]
            draws = reps[("SIN_CP", breakdown, group, measure)] - reps[("CON_CP", breakdown, group, measure)]
            finite = draws[np.isfinite(draws)]
            ok = con is not None and sin is not None and len(finite) == n_boot
            lo, hi = np.percentile(finite, [2.5, 97.5]) if ok else (None, None)
            contrasts.append({"tipo": "sin_cp_menos_con_cp", "variante": "PAREADA",
                              "tramo_edad": group if breakdown in ("edad", "sexo_edad") else "total",
                              "desglose": breakdown, "grupo": group, "medida": measure,
                              "estimacion": sin - con if ok else None, "ic95_inferior": lo,
                              "ic95_superior": hi, "estado": "OK" if ok else "NO-ESTIMABLE",
                              "unidad": "diferencia de proporciones" if measure == "participacion" else "horas/semana"})

    identity_errors = []
    for variant in ("CON_CP", "SIN_CP"):
        for breakdown, group, _ in domains:
            p = sufficient[(variant, breakdown, group, "participacion")]
            mean = sufficient[(variant, breakdown, group, "media_incluye_ceros")]
            intensity = sufficient[(variant, breakdown, group, "media_participantes")]
            if None not in (p, mean, intensity):
                identity_errors.append(abs(mean - p * intensity))
    return estimates, contrasts, one_psu, max(identity_errors, default=0.0)


def _write_csv(path: Path, columns: list[str], rows: list[dict]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _fmt(v) if v is None or isinstance(v, (int, float, np.number)) else v for k, v in row.items()})
    return hashlib.sha256(path.read_bytes()).hexdigest()


def medir(inputs: dict, contrato: dict) -> dict:
    raw, fd = _bytes(inputs[INPUT_DATA]), _bytes(inputs[INPUT_FD])
    for iid, content in ((INPUT_DATA, raw), (INPUT_FD, fd)):
        if _sha(content) != EXPECTED[iid]:
            raise ValueError(f"SHA256-NO-COINCIDE:{iid}")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if "tvar_crea.csv" not in archive.namelist():
            raise ValueError("MIEMBRO-AUSENTE:tvar_crea.csv")
        frame = pd.read_csv(archive.open("tvar_crea.csv"), dtype=str, low_memory=False)
    valid, incidence, marco = prepare_frame(frame)
    n_boot = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    estimates, contrasts, one_psu, identity_error = analyse(valid, marco, n_boot, seed)

    root = Path(__file__).resolve().parents[3]
    out_dir = root / contrato["parametros"]["directorio_salida"]
    estimates_path = out_dir / "estimaciones.csv"
    contrasts_path = out_dir / "contrastes.csv"
    incidence_path = out_dir / "incidencias.json"
    est_sha = _write_csv(estimates_path, ESTIMATE_COLUMNS, estimates)
    con_sha = _write_csv(contrasts_path, CONTRAST_COLUMNS, contrasts)
    incidence_path.parent.mkdir(parents=True, exist_ok=True)
    incidence_path.write_text(json.dumps(incidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    inc_sha = hashlib.sha256(incidence_path.read_bytes()).hexdigest()

    index = {(r["variante"], r["desglose"], r["grupo"], r["medida"]): r for r in estimates}
    contrast_index = {(r["tipo"], r["variante"], r["tramo_edad"], r["medida"]): r for r in contrasts}
    return {
        "RESULT-ENUTPI-G-INPUT-BD-SHA256": _sha(raw),
        "RESULT-ENUTPI-G-INPUT-FD-SHA256": _sha(fd),
        "RESULT-ENUTPI-G-N-MARCO": int(len(frame)),
        "RESULT-ENUTPI-G-N-VALIDO-COMUN": int(len(valid)),
        "RESULT-ENUTPI-G-MASA-VALIDA-COMUN": float(valid["FAC_PER"].sum()),
        "RESULT-ENUTPI-G-N-ESTRATOS-UPM-UNICA": int(one_psu),
        "RESULT-ENUTPI-G-IDENTIDAD-MAX-ERROR": float(identity_error),
        "RESULT-ENUTPI-G-ESTIMACIONES-N-FILAS": len(estimates),
        "RESULT-ENUTPI-G-CONTRASTES-N-FILAS": len(contrasts),
        "RESULT-ENUTPI-G-ESTIMACIONES-SHA256": est_sha,
        "RESULT-ENUTPI-G-CONTRASTES-SHA256": con_sha,
        "RESULT-ENUTPI-G-INCIDENCIAS-SHA256": inc_sha,
        "RESULT-ENUTPI-G-INCIDENCIAS": json.dumps(incidence, ensure_ascii=False, sort_keys=True),
        "RESULT-ENUTPI-A-CON-PARTICIPACION-NACIONAL": float(index[("CON_CP", "nacional", "total", "participacion")]["estimacion"]),
        "RESULT-ENUTPI-A-CON-MEDIA-NACIONAL": float(index[("CON_CP", "nacional", "total", "media_incluye_ceros")]["estimacion"]),
        "RESULT-ENUTPI-A-CON-INTENSIDAD-NACIONAL": float(index[("CON_CP", "nacional", "total", "media_participantes")]["estimacion"]),
        "RESULT-ENUTPI-A-CON-BRECHA-PARTICIPACION": float(contrast_index[("mujer_menos_hombre", "CON_CP", "total", "participacion")]["estimacion"]),
        "RESULT-ENUTPI-A-CON-BRECHA-MEDIA": float(contrast_index[("mujer_menos_hombre", "CON_CP", "total", "media_incluye_ceros")]["estimacion"]),
        "RESULT-ENUTPI-A-CON-BRECHA-INTENSIDAD": float(contrast_index[("mujer_menos_hombre", "CON_CP", "total", "media_participantes")]["estimacion"]),
        "RESULT-ENUTPI-G-SALIDA-ESTIMACIONES": str(estimates_path.relative_to(root)),
        "RESULT-ENUTPI-G-SALIDA-CONTRASTES": str(contrasts_path.relative_to(root)),
        "RESULT-ENUTPI-G-SALIDA-INCIDENCIAS": str(incidence_path.relative_to(root)),
    }

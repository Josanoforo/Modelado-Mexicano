#!/usr/bin/env python3
"""Validación independiente y producto gráfico de la serie ENVIPE p(C1,U1)."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path


getcontext().prec = 40
POINT_TOLERANCE = Decimal("1e-10")
UNCERTAINTY_SE_REL_TOLERANCE = 0.10
UNCERTAINTY_ENDPOINT_TOLERANCE = 0.002
UNCERTAINTY_WAVE = 2019


@dataclass(frozen=True)
class Wave:
    survey: int
    fact: int
    archive: str
    sha256: str
    member: str
    fmt: str
    response: str
    personal: frozenset[int]
    stratum: str
    psu: str


WAVES = (
    Wave(2011, 2010, "envipe2011/base_de_datos_envipe_2011_dbf.zip", "d6c660f00ca2179dcabf59a9af166d7605793eed48c6eb84bcd8d24f39bd2ce4", "tmod_vic.DBF", "DBF", "BP1_21", frozenset(range(4, 15)), "EST", "UPM"),
    Wave(2014, 2013, "envipe2014/bd_envipe2014_dbf.zip", "8f1d0eb519a0ceabe36d187d9a49734dbef97f219b86eea9084ebd1818973f77", "bd_envipe2014/bd_envipe2014/TMod_Vic.dbf", "DBF", "BP1_23", frozenset(range(5, 16)), "EST", "UPM"),
    Wave(2016, 2015, "envipe2016/bd_envipe2016_dbf.zip", "8c939550590bbb7941c65a2c9a3d87d8654cfe529e969f51265fe65974ef68a4", "TMod_Vic.dbf", "DBF", "BP1_23", frozenset(range(5, 16)), "EST_DIS", "UPM_DIS"),
    Wave(2017, 2016, "envipe2017/bd_envipe2017_dbf.zip", "86df9910dae338d4c4487e6760e8e3ba1a752c8a8fcda967a8af152ad49d8f74", "BASE_DE_DATOS_ENVIPE_2017_en/TMod_Vic.dbf", "DBF", "BP1_23", frozenset(range(5, 16)), "EST_DIS", "UPM_DIS"),
    Wave(2018, 2017, "envipe2018_csv.zip", "aa279993bfeaaa0bf0d821e964887140ef444f6e695e4e1767f6512e4d2c4723", "conjunto_de_datos_tmod_vic_envipe_2018/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe_2018.csv", "CSV", "BP1_23", frozenset(range(5, 16)), "EST_DIS", "UPM_DIS"),
    Wave(2019, 2018, "envipe2019_csv.zip", "24bb83987f2ba57912a3f55c8ff3bb48e5f39f2292cd167997312c1fd77207f3", "conjunto_de_datos_TMod_Vic_ENVIPE_2019/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2019.csv", "CSV", "BP1_23", frozenset(range(5, 16)), "EST_DIS", "UPM_DIS"),
    Wave(2020, 2019, "envipe2020_csv.zip", "26f468da631bfdb94994a9e5051fa973468608f0da56612b6897df16a2797b9d", "conjunto_de_datos_TMod_Vic_ENVIPE_2020/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2020.csv", "CSV", "BP1_23", frozenset(range(5, 16)), "EST_DIS", "UPM_DIS"),
    Wave(2022, 2021, "envipe2022_csv.zip", "3a6e0f3a05dd4120efe8072de519402a39f4ed1690593433a68bb2ee137e77bb", "conjunto_de_datos_TMod_Vic_ENVIPE_2022/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2022.csv", "CSV", "BP1_23", frozenset(range(5, 16)), "EST_DIS", "UPM_DIS"),
)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def zip_member(archive: zipfile.ZipFile, expected: str) -> str:
    wanted = expected.replace("\\", "/").casefold()
    matches = [name for name in archive.namelist() if name.replace("\\", "/").casefold() == wanted]
    if len(matches) != 1:
        raise ValueError(f"miembro {expected!r}: se esperó 1 coincidencia y hubo {len(matches)}")
    return matches[0]


def iter_records(path: Path, wave: Wave):
    columns = ["BPCOD", "BP1_20", wave.response, "FAC_DEL", wave.stratum, wave.psu]
    with zipfile.ZipFile(path) as archive:
        member = zip_member(archive, wave.member)
        if wave.fmt == "CSV":
            with archive.open(member) as binary:
                text = io.TextIOWrapper(binary, encoding="latin-1", newline="")
                reader = csv.DictReader(text)
                for raw in reader:
                    upper = {str(key).upper(): value for key, value in raw.items()}
                    yield {column: upper.get(column.upper()) for column in columns}
            return

        import pyreadstat

        suffix = Path(member).suffix or ".dbf"
        with tempfile.NamedTemporaryFile(suffix=suffix) as extracted:
            with archive.open(member) as source:
                shutil.copyfileobj(source, extracted)
            extracted.flush()
            frame, _ = pyreadstat.read_dbf(extracted.name, usecols=columns)
            for raw in frame.to_dict(orient="records"):
                upper = {str(key).upper(): value for key, value in raw.items()}
                yield {column: upper.get(column.upper()) for column in columns}


def integer(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    return int(number) if number == number.to_integral_value() else None


def decimal_weight(value):
    if value is None:
        return None
    try:
        number = Decimal(str(value).strip())
    except InvalidOperation:
        return None
    return number if number.is_finite() and number > 0 else None


def code(value) -> str:
    parsed = integer(value)
    if parsed is not None:
        return f"{parsed:02d}"
    text = "" if value is None else str(value).strip()
    return text or "BLANCO"


def references(repo: Path, survey: int) -> dict:
    path = repo / f"data/corrida0/CALC-ENVIPE-SERIE-{survey}/resultados.json"
    return json.loads(path.read_text(encoding="utf-8"))["resultados"]


def validate_wave(repo: Path, raw_root: Path, wave: Wave):
    path = raw_root / wave.archive
    actual_hash = file_hash(path)
    if actual_hash != wave.sha256:
        raise ValueError(f"{wave.survey}: hash {actual_hash} no coincide con {wave.sha256}")

    excluded = Counter()
    numerator = Decimal(0)
    denominator = Decimal(0)
    included = 0
    total = 0
    design_rows = []
    for row in iter_records(path, wave):
        total += 1
        bpcod = integer(row["BPCOD"])
        if bpcod not in wave.personal:
            excluded[("BPCOD-NO-PERSONAL", code(row["BPCOD"]))] += 1
            continue
        reported = integer(row["BP1_20"])
        if reported != 2:
            excluded[("BP1_20-DISTINTO-DE-02", code(row["BP1_20"]))] += 1
            continue
        response = integer(row[wave.response])
        if response not in range(1, 9):
            excluded[(f"{wave.response}-FUERA-DE-01..08", code(row[wave.response]))] += 1
            continue
        weight = decimal_weight(row["FAC_DEL"])
        if weight is None:
            excluded[("FAC_DEL-NO-VALIDO", code(row["FAC_DEL"]))] += 1
            continue
        outcome = 1 if response in {1, 2, 6} else 0
        included += 1
        denominator += weight
        numerator += weight * outcome
        if wave.survey == UNCERTAINTY_WAVE:
            design_rows.append((str(row[wave.stratum]).strip(), str(row[wave.psu]).strip(), float(weight), outcome))

    point = numerator / denominator
    ref = references(repo, wave.survey)
    prefix = f"RESULT-ENVIPE-SERIE-{wave.survey}"
    ref_point = Decimal(str(ref[f"{prefix}-P-C1-U1"]))
    ref_denominator = Decimal(str(ref[f"{prefix}-MASA-FAC-DEL-U1"]))
    ref_n = int(ref[f"{prefix}-N-U1"])
    point_delta = abs(point - ref_point)
    status = "COINCIDE" if point_delta <= POINT_TOLERANCE and denominator == ref_denominator and included == ref_n else "DIFIERE"
    result = {
        "ola_encuesta": wave.survey,
        "anio_hecho": wave.fact,
        "sha256_zip": actual_hash,
        "formato": wave.fmt,
        "miembro": wave.member,
        "reactivo": wave.response,
        "numerador_fac_del_c1": str(numerator),
        "denominador_fac_del_u1": str(denominator),
        "n_u1": included,
        "p_c1_u1_reconstruido": str(point),
        "p_c1_u1_sellado": str(ref_point),
        "diferencia_absoluta_punto": str(point_delta),
        "denominador_sellado": str(ref_denominator),
        "n_sellado": ref_n,
        "tolerancia_punto": str(POINT_TOLERANCE),
        "veredicto": status,
        "n_filas": total,
    }
    exclusion_rows = [
        {"ola_encuesta": wave.survey, "etapa": stage, "codigo": value, "n_excluido": count}
        for (stage, value), count in sorted(excluded.items())
    ]
    return result, exclusion_rows, design_rows, ref


def linearized_ratio(rows, point: float, denominator: float):
    psu_scores = defaultdict(float)
    for stratum, psu, weight, outcome in rows:
        psu_scores[(stratum, psu)] += weight * (outcome - point)
    strata = defaultdict(list)
    for (stratum, _), score in psu_scores.items():
        strata[stratum].append(score)
    variance_total = 0.0
    singleton = 0
    for scores in strata.values():
        size = len(scores)
        if size == 1:
            singleton += 1
            continue
        mean = sum(scores) / size
        variance_total += size / (size - 1) * sum((score - mean) ** 2 for score in scores)
    standard_error = math.sqrt(variance_total) / denominator
    return standard_error, singleton, len(strata), len(psu_scores)


def write_tsv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def make_figure(repo: Path, figure_dir: Path):
    import matplotlib.pyplot as plt

    source = repo / "data/corrida0/envipe-serie-denuncia-v1_0.tsv"
    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    years = [int(row["anio_hecho"]) for row in rows]
    points = [100 * float(row["p_c1_u1"]) for row in rows]
    lows = [100 * float(row["ic95_boot_lo"]) for row in rows]
    highs = [100 * float(row["ic95_boot_hi"]) for row in rows]
    errors = [[point - low for point, low in zip(points, lows)], [high - point for point, high in zip(points, highs)]]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axis = plt.subplots(figsize=(11.5, 6.4), layout="constrained")
    axis.errorbar(years, points, yerr=errors, fmt="o-", color="#175676", ecolor="#7aa6b8", capsize=3, linewidth=1.8, markersize=5)
    axis.scatter([2010], [points[0]], color="#b23a48", s=65, zorder=4)
    axis.axvline(2010.5, color="#b23a48", linestyle="--", linewidth=1.2)
    axis.annotate("Ola 2011: BP1_21 y residuos 88/98/99\n(ruptura nominal; C1/U1 sustantivo se conserva)", xy=(2010, points[0]), xytext=(2011.1, max(points) + 1.7), arrowprops={"arrowstyle": "->", "color": "#b23a48"}, color="#7d2633", fontsize=9)
    axis.set_xticks(years)
    axis.tick_params(axis="x", rotation=45)
    axis.set_ylabel("Porcentaje ponderado (IC95 bootstrap publicado)")
    axis.set_xlabel("Año del hecho")
    axis.set_title("ENVIPE 2010–2024: motivos 01/02/06 entre delitos personales no denunciados")
    axis.text(0, -0.22, "Estimando: proporción ponderada por FAC_DEL entre respuestas 01..08; unidad delito. No es tasa general de denuncia.", transform=axis.transAxes, fontsize=9)
    figure_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("svg", "png", "pdf"):
        fig.savefig(figure_dir / f"envipe-p-c1-u1-2010-2024.{suffix}", dpi=180, metadata={"Title": "ENVIPE p(C1,U1), años del hecho 2010-2024"})
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--raw-root", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    raw_root = (args.raw_root or repo / "data/raw").resolve()
    validation_rows = []
    exclusion_rows = []
    uncertainty_row = None

    for wave in WAVES:
        result, exclusions, design_rows, ref = validate_wave(repo, raw_root, wave)
        validation_rows.append(result)
        exclusion_rows.extend(exclusions)
        if wave.survey == UNCERTAINTY_WAVE:
            point = float(result["p_c1_u1_reconstruido"])
            denominator = float(result["denominador_fac_del_u1"])
            se, singleton, strata, psus = linearized_ratio(design_rows, point, denominator)
            low = max(0.0, point - 1.96 * se)
            high = min(1.0, point + 1.96 * se)
            prefix = f"RESULT-ENVIPE-SERIE-{wave.survey}"
            ref_se = float(ref[f"{prefix}-EE-C1-U1"])
            ref_low = float(ref[f"{prefix}-IC-LO-C1-U1"])
            ref_high = float(ref[f"{prefix}-IC-HI-C1-U1"])
            relative_se = abs(se - ref_se) / ref_se
            endpoint_delta = max(abs(low - ref_low), abs(high - ref_high))
            verdict = "CONCORDANTE" if relative_se <= UNCERTAINTY_SE_REL_TOLERANCE and endpoint_delta <= UNCERTAINTY_ENDPOINT_TOLERANCE else "DIFERENCIA-MATERIAL"
            uncertainty_row = {
                "ola_encuesta": wave.survey,
                "metodo_referencia": "LINEALIZACION-DIRECTA-RAZON-UPM-EN-ESTRATO",
                "ee_referencia": f"{se:.15g}",
                "ic95_lo_referencia": f"{low:.15g}",
                "ic95_hi_referencia": f"{high:.15g}",
                "ee_analitico_sellado": f"{ref_se:.15g}",
                "ic95_lo_analitico_sellado": f"{ref_low:.15g}",
                "ic95_hi_analitico_sellado": f"{ref_high:.15g}",
                "diferencia_relativa_ee": f"{relative_se:.15g}",
                "max_diferencia_extremo": f"{endpoint_delta:.15g}",
                "estratos": strata,
                "upm": psus,
                "estratos_upm_unica": singleton,
                "alcance": "COMPARACION-METODOLOGICA; NO REPRODUCE BOOTSTRAP NI PRUEBA DIFERENCIAS ENTRE ANIOS",
                "veredicto": verdict,
            }

    out = repo / "data/corrida0"
    write_tsv(out / "envipe-validacion-independiente-v1_0.tsv", validation_rows)
    write_tsv(out / "envipe-validacion-independiente-exclusiones-v1_0.tsv", exclusion_rows)
    write_tsv(out / "envipe-validacion-independiente-incertidumbre-v1_0.tsv", [uncertainty_row])
    make_figure(repo, repo / "forense/notas/figuras")

    failures = [row for row in validation_rows if row["veredicto"] != "COINCIDE"]
    if uncertainty_row["veredicto"] != "CONCORDANTE":
        failures.append(uncertainty_row)
    print(f"VALIDACION_ENVIPE · puntos={len(validation_rows)} · coinciden={len(validation_rows) - len(failures)} · incertidumbre={uncertainty_row['veredicto']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

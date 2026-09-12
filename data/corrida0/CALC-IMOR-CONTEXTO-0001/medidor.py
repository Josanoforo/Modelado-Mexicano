#!/usr/bin/env python3
"""Analiza el IMOR mensual por régimen sin cruzar la ruptura IFRS9."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics
from collections import defaultdict
from datetime import date
from pathlib import Path

CALC_ID = "CALC-IMOR-CONTEXTO-0001"
INPUT_ID = "IN-BANXICO-IMOR-CONSUMO-MENSUAL"
EXPECTED_SHA256 = "772f9d0b9da57b18ef9abdd5824b0824b6191e65668103e3a8329171d3df88e9"
PRODUCTS = ["Consumo total", "Tarjetas de crédito", "ABCD", "Nómina", "Personales"]
REGIMES = ["PRE_IFRS9_CARTERA_VENCIDA", "IFRS9_ETAPA_3"]
REGIME_BOUNDS = {
    "PRE_IFRS9_CARTERA_VENCIDA": ("2016-01", "2021-12", "saldo de cartera vencida"),
    "IFRS9_ETAPA_3": ("2022-01", "2026-03", "saldo de cartera clasificada como etapa 3"),
}
EXPECTED_UNIVERSE = (
    "banca comercial; incluye Sofomes ER subsidiarias de instituciones bancarias "
    "y grupos financieros; excluye CI Banco"
)
OUT_COLUMNS_LEVELS = [
    "fecha", "producto", "regimen_definicion", "imor_porcentaje",
    "unidad_observacion", "universo_institucional", "fuente",
]
OUT_COLUMNS_CHANGES = [
    "fecha", "producto", "regimen_definicion", "imor_porcentaje",
    "cambio_mensual_pp", "cambio_mensual_rel_pct",
    "cambio_interanual_pp", "cambio_interanual_rel_pct",
]
OUT_COLUMNS_SUMMARY = [
    "producto", "regimen_definicion", "fecha_inicio", "fecha_fin", "n_meses",
    "nivel_inicio_pct", "nivel_fin_pct", "diferencia_fin_inicio_pp",
    "diferencia_fin_inicio_rel_pct", "media_temporal_pct", "mediana_temporal_pct",
    "minimo_pct", "fechas_minimo", "maximo_pct", "fechas_maximo",
    "desv_est_poblacional_nivel_pp", "n_cambios_mensuales",
    "media_cambio_mensual_pp", "mediana_cambio_mensual_pp",
    "minimo_cambio_mensual_pp", "maximo_cambio_mensual_pp",
    "desv_est_poblacional_cambio_mensual_pp", "n_cambios_interanuales",
    "media_cambio_interanual_pp", "mediana_cambio_interanual_pp",
    "minimo_cambio_interanual_pp", "maximo_cambio_interanual_pp",
    "desv_est_poblacional_cambio_interanual_pp",
]


def _month_index(value: str) -> int:
    year, month = map(int, value.split("-"))
    if not (1 <= month <= 12):
        raise ValueError(f"mes inválido: {value}")
    return year * 12 + month - 1


def _month_from_index(value: int) -> str:
    return f"{value // 12:04d}-{value % 12 + 1:02d}"


def _fmt(value: float | None) -> str:
    return "" if value is None else f"{value:.6f}"


def _read_rows(raw: bytes) -> list[dict]:
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError(f"SHA-256 inesperado: {actual}")
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    expected_fields = {
        "fecha", "producto", "indicador", "numerador", "denominador", "valor",
        "unidad", "frecuencia", "universo_institucional", "regimen_definicion",
        "fuente", "nota",
    }
    if set(rows[0]) != expected_fields:
        raise ValueError(f"esquema inesperado: {sorted(rows[0])}")
    if len(rows) != 615:
        raise ValueError(f"se esperaban 615 filas y llegaron {len(rows)}")

    seen = set()
    months = defaultdict(set)
    parsed = []
    for row in rows:
        key = (row["fecha"], row["producto"])
        if key in seen:
            raise ValueError(f"llave duplicada: {key}")
        seen.add(key)
        if row["producto"] not in PRODUCTS:
            raise ValueError(f"producto inesperado: {row['producto']}")
        if row["regimen_definicion"] not in REGIMES:
            raise ValueError(f"régimen inesperado: {row['regimen_definicion']}")
        start, end, numerator = REGIME_BOUNDS[row["regimen_definicion"]]
        if not (start <= row["fecha"] <= end):
            raise ValueError(f"fecha fuera del régimen: {key}")
        if row["numerador"] != numerator:
            raise ValueError(f"numerador discordante: {key}")
        if row["indicador"] != "IMOR" or row["unidad"] != "porcentaje":
            raise ValueError(f"indicador/unidad inesperado: {key}")
        if row["frecuencia"] != "mensual" or row["universo_institucional"] != EXPECTED_UNIVERSE:
            raise ValueError(f"frecuencia/universo inesperado: {key}")
        value = float(row["valor"])
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"valor inválido: {key}={row['valor']}")
        months[row["fecha"]].add(row["producto"])
        parsed.append({**row, "valor_num": value, "month_index": _month_index(row["fecha"])})

    expected_months = [_month_from_index(i) for i in range(_month_index("2016-01"), _month_index("2026-03") + 1)]
    if sorted(months) != expected_months:
        raise ValueError("el corte mensual no es continuo 2016-01..2026-03")
    if any(products != set(PRODUCTS) for products in months.values()):
        raise ValueError("algún mes no contiene los cinco productos")
    return sorted(parsed, key=lambda row: (PRODUCTS.index(row["producto"]), row["month_index"]))


def _changes(rows: list[dict]) -> list[dict]:
    previous = {}
    by_month = {(r["producto"], r["month_index"]): r for r in rows}
    out = []
    for row in rows:
        group = (row["producto"], row["regimen_definicion"])
        prev = previous.get(group)
        monthly_pp = monthly_rel = None
        if prev is not None and row["month_index"] - prev["month_index"] == 1:
            monthly_pp = row["valor_num"] - prev["valor_num"]
            monthly_rel = 100 * monthly_pp / prev["valor_num"]
        previous[group] = row

        year_prev = by_month.get((row["producto"], row["month_index"] - 12))
        yoy_pp = yoy_rel = None
        if year_prev is not None and year_prev["regimen_definicion"] == row["regimen_definicion"]:
            yoy_pp = row["valor_num"] - year_prev["valor_num"]
            yoy_rel = 100 * yoy_pp / year_prev["valor_num"]
        out.append({
            **row,
            "cambio_mensual_pp_num": monthly_pp,
            "cambio_mensual_rel_pct_num": monthly_rel,
            "cambio_interanual_pp_num": yoy_pp,
            "cambio_interanual_rel_pct_num": yoy_rel,
        })
    return out


def _stats(values: list[float]) -> dict:
    return {
        "n": len(values),
        "media": statistics.fmean(values),
        "mediana": statistics.median(values),
        "minimo": min(values),
        "maximo": max(values),
        "desv_est_poblacional": statistics.pstdev(values),
    }


def _summaries(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["producto"], row["regimen_definicion"])].append(row)
    out = []
    for product in PRODUCTS:
        for regime in REGIMES:
            group = sorted(groups[(product, regime)], key=lambda row: row["month_index"])
            levels = [row["valor_num"] for row in group]
            monthly = [row["cambio_mensual_pp_num"] for row in group if row["cambio_mensual_pp_num"] is not None]
            yoy = [row["cambio_interanual_pp_num"] for row in group if row["cambio_interanual_pp_num"] is not None]
            ls, ms, ys = _stats(levels), _stats(monthly), _stats(yoy)
            delta = levels[-1] - levels[0]
            out.append({
                "producto": product,
                "regimen_definicion": regime,
                "fecha_inicio": group[0]["fecha"],
                "fecha_fin": group[-1]["fecha"],
                "n_meses": ls["n"],
                "nivel_inicio_pct": levels[0],
                "nivel_fin_pct": levels[-1],
                "diferencia_fin_inicio_pp": delta,
                "diferencia_fin_inicio_rel_pct": 100 * delta / levels[0],
                "media_temporal_pct": ls["media"],
                "mediana_temporal_pct": ls["mediana"],
                "minimo_pct": ls["minimo"],
                "fechas_minimo": ";".join(r["fecha"] for r in group if r["valor_num"] == ls["minimo"]),
                "maximo_pct": ls["maximo"],
                "fechas_maximo": ";".join(r["fecha"] for r in group if r["valor_num"] == ls["maximo"]),
                "desv_est_poblacional_nivel_pp": ls["desv_est_poblacional"],
                "n_cambios_mensuales": ms["n"],
                "media_cambio_mensual_pp": ms["media"],
                "mediana_cambio_mensual_pp": ms["mediana"],
                "minimo_cambio_mensual_pp": ms["minimo"],
                "maximo_cambio_mensual_pp": ms["maximo"],
                "desv_est_poblacional_cambio_mensual_pp": ms["desv_est_poblacional"],
                "n_cambios_interanuales": ys["n"],
                "media_cambio_interanual_pp": ys["media"],
                "mediana_cambio_interanual_pp": ys["mediana"],
                "minimo_cambio_interanual_pp": ys["minimo"],
                "maximo_cambio_interanual_pp": ys["maximo"],
                "desv_est_poblacional_cambio_interanual_pp": ys["desv_est_poblacional"],
            })
    return out


def _canonical_summary(rows: list[dict], regime: str) -> str:
    selected = [r for r in rows if r["regimen_definicion"] == regime]
    clean = []
    for row in selected:
        clean.append({key: (round(value, 12) if isinstance(value, float) else value)
                      for key, value in row.items()})
    return json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def calcular(raw: bytes) -> tuple[list[dict], list[dict], list[dict]]:
    levels = _read_rows(raw)
    changes = _changes(levels)
    summaries = _summaries(changes)
    return levels, changes, summaries


def medir(inputs: dict, contrato: dict) -> dict:
    entry = inputs[INPUT_ID]
    raw = entry.get("bytes")
    if raw is None:
        raw = Path(entry["ruta_absoluta"]).read_bytes()
    levels, changes, summaries = calcular(raw)
    monthly_n = sum(r["cambio_mensual_pp_num"] is not None for r in changes)
    yoy_n = sum(r["cambio_interanual_pp_num"] is not None for r in changes)
    return {
        "RESULT-IMOR-G-INPUT-SHA256": hashlib.sha256(raw).hexdigest(),
        "RESULT-IMOR-G-N-FILAS": len(levels),
        "RESULT-IMOR-G-N-MESES": len({r["fecha"] for r in levels}),
        "RESULT-IMOR-G-N-PRODUCTOS": len({r["producto"] for r in levels}),
        "RESULT-IMOR-G-CORTE": f"{min(r['fecha'] for r in levels)}..{max(r['fecha'] for r in levels)}",
        "RESULT-IMOR-G-N-CAMBIOS-MENSUALES": monthly_n,
        "RESULT-IMOR-G-N-CAMBIOS-INTERANUALES": yoy_n,
        "RESULT-IMOR-G-RUPTURAS-ADICIONALES": 0,
        "RESULT-IMOR-PRE-RESUMEN-JSON": _canonical_summary(summaries, REGIMES[0]),
        "RESULT-IMOR-IFRS9-RESUMEN-JSON": _canonical_summary(summaries, REGIMES[1]),
        "RESULT-IMOR-G-USO": "DESCRIPTIVO-NO-CALIBRA; porcentaje de saldos, no riesgo individual",
    }


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _plot(changes: list[dict], output: Path, field: str, ylabel: str, title: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    plt.rcParams["svg.fonttype"] = "none"
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8), sharey=True, constrained_layout=True)
    colors = dict(zip(PRODUCTS, ["#1B4965", "#E76F51", "#2A9D8F", "#7B2CBF", "#E9C46A"]))
    for axis, regime in zip(axes, REGIMES):
        for product in PRODUCTS:
            selected = [r for r in changes if r["producto"] == product and r["regimen_definicion"] == regime]
            xs = [date.fromisoformat(r["fecha"] + "-01") for r in selected]
            ys = [r[field] for r in selected]
            axis.plot(xs, ys, label=product, color=colors[product], linewidth=1.55)
        start, end, _ = REGIME_BOUNDS[regime]
        axis.set_title(f"{regime}\n{start} a {end}", fontsize=10)
        axis.set_xlabel("Mes")
        axis.grid(axis="y", color="#D9D9D9", linewidth=0.6)
        axis.xaxis.set_major_locator(mdates.YearLocator(2))
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        axis.tick_params(axis="x", rotation=30)
    axes[0].set_ylabel(ylabel)
    axes[1].legend(loc="upper right", fontsize=8, frameon=False)
    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.text(
        0.5, 0.01,
        "Banxico · banca comercial (incluye Sofomes ER subsidiarias; excluye CI Banco) · "
        "ABCD incluye bienes muebles y automotriz · líneas separadas por régimen; no R16 CNBV",
        ha="center", fontsize=8,
    )
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)


def materializar(root: Path) -> None:
    input_path = root / "data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv"
    out = root / "data/analisis-imor-contexto-temporal"
    out.mkdir(parents=True, exist_ok=True)
    levels, changes, summaries = calcular(input_path.read_bytes())
    _write_csv(out / "niveles-mensuales.csv", OUT_COLUMNS_LEVELS, [{
        "fecha": r["fecha"], "producto": r["producto"],
        "regimen_definicion": r["regimen_definicion"],
        "imor_porcentaje": _fmt(r["valor_num"]),
        "unidad_observacion": "porcentaje de saldos",
        "universo_institucional": r["universo_institucional"], "fuente": r["fuente"],
    } for r in levels])
    _write_csv(out / "cambios-mensuales-e-interanuales.csv", OUT_COLUMNS_CHANGES, [{
        "fecha": r["fecha"], "producto": r["producto"],
        "regimen_definicion": r["regimen_definicion"],
        "imor_porcentaje": _fmt(r["valor_num"]),
        "cambio_mensual_pp": _fmt(r["cambio_mensual_pp_num"]),
        "cambio_mensual_rel_pct": _fmt(r["cambio_mensual_rel_pct_num"]),
        "cambio_interanual_pp": _fmt(r["cambio_interanual_pp_num"]),
        "cambio_interanual_rel_pct": _fmt(r["cambio_interanual_rel_pct_num"]),
    } for r in changes])
    _write_csv(out / "resumen-producto-regimen.csv", OUT_COLUMNS_SUMMARY, [{
        key: (_fmt(value) if isinstance(value, float) else value)
        for key, value in row.items()
    } for row in summaries])
    _plot(changes, out / "niveles-por-producto-y-regimen.svg", "valor_num",
          "IMOR (% de saldos)", "IMOR mensual por producto y régimen metodológico")
    _plot(changes, out / "cambios-mensuales-por-producto-y-regimen.svg", "cambio_mensual_pp_num",
          "Cambio mensual (puntos porcentuales)", "Cambios mensuales comparables dentro de régimen")
    print(f"MATERIALIZADO: {out.relative_to(root)} · 3 tablas · 2 figuras")


if __name__ == "__main__":
    materializar(Path(__file__).resolve().parents[3])

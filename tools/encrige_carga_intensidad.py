#!/usr/bin/env python3
"""Deriva carga, intensidad y participaciones desde el CSV ENCRIGE sellado."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
from dataclasses import dataclass
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 40

ROOT = Path(__file__).resolve().parents[1]
PARENT_CSV = ROOT / "forense/analisis/encrige-descriptiva-1/encrige-corrupcion-por-tamano.csv"
OUTPUT_DIR = ROOT / "forense/analisis/encrige-carga-intensidad-1"
EXPECTED_PARENT_SHA256 = "632ce31b2c2cf70e22871319b5842e6168592f065588b69b11010e3552b48c26"
PREVALENCE_ID = "PREVALENCIA-EXPERIENCIA-CORRUPCION"
INCIDENCE_ID = "INCIDENCIA-EXPERIENCIAS-CORRUPCION"
NATIONAL = "Estados Unidos Mexicanos"
SIZES = ("Micro", "Pequeña", "Mediana", "Grande")
DOMAINS = (NATIONAL,) + SIZES
MASS_TOLERANCE = Decimal("0.0003")
RATIO_TOLERANCE = Decimal("0.000000000001")
Q12 = Decimal("0.000000000001")
Q4 = Decimal("0.0001")


@dataclass(frozen=True)
class DomainResult:
    dominio: str
    N: Decimal
    A: Decimal
    T: Decimal
    p: Decimal
    m: Decimal
    r: Decimal | None
    p_oficial: Decimal
    m_oficial: Decimal
    delta_p_oficial: Decimal
    delta_m_oficial: Decimal
    residuo_identidad: Decimal | None


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _d(value: str, field: str) -> Decimal:
    try:
        number = Decimal(value)
    except Exception as exc:
        raise ValueError(f"VALOR-NO-DECIMAL:{field}={value!r}") from exc
    if not number.is_finite():
        raise ValueError(f"VALOR-NO-FINITO:{field}={value!r}")
    return number


def _require_equal(prevalence: dict[str, str], incidence: dict[str, str], field: str) -> None:
    if prevalence.get(field) != incidence.get(field):
        raise ValueError(
            f"INDICADORES-INCOMPATIBLES:{field}:"
            f"{prevalence.get(field)!r}!={incidence.get(field)!r}"
        )


def derive_domain(prevalence: dict[str, str], incidence: dict[str, str]) -> DomainResult:
    """Une un dominio y aplica las guardas semánticas y algebraicas."""
    for field in (
        "dominio",
        "dominio_tipo",
        "periodo",
        "denominador_publicado",
        "unidad_numerador_denominador",
    ):
        _require_equal(prevalence, incidence, field)
    if prevalence.get("indicador_id") != PREVALENCE_ID:
        raise ValueError("INDICADOR-PREVALENCIA-INCORRECTO")
    if incidence.get("indicador_id") != INCIDENCE_ID:
        raise ValueError("INDICADOR-INCIDENCIA-INCORRECTO")
    if incidence.get("cuadro") != "t6_41":
        raise ValueError("SEMANTICA-T-NO-ACREDITADA:CUADRO")
    if incidence.get("unidad_normalizada") != "experiencias por unidad económica expuesta":
        raise ValueError("SEMANTICA-T-NO-ACREDITADA:UNIDAD")
    if "Total de trámites" not in incidence.get("localizador", ""):
        raise ValueError("SEMANTICA-T-NO-ACREDITADA:LOCALIZADOR")
    if prevalence.get("unidad_numerador_denominador") != "unidades expandidas":
        raise ValueError("UNIDAD-NO-EXPANDIDA")

    domain = prevalence["dominio"]
    N = _d(prevalence["denominador_publicado"], "N")
    A = _d(prevalence["numerador_publicado"], "A")
    T = _d(incidence["numerador_publicado"], "T")
    if N <= 0 or A < 0 or T < 0 or A > N:
        raise ValueError(f"MASAS-INVALIDAS:{domain}:N={N}:A={A}:T={T}")
    if T < A:
        raise ValueError(f"GUARDA-SEMANTICA-T-MENOR-A:{domain}:T={T}:A={A}")

    p = A / N
    m = T / N
    r = None if A == 0 else T / A
    p_official = _d(prevalence["valor_original"], "prevalencia_oficial") / Decimal(10000)
    m_official = _d(incidence["valor_original"], "incidencia_oficial") / Decimal(10000)
    delta_p = p - p_official
    delta_m = m - m_official
    if abs(delta_p) > RATIO_TOLERANCE or abs(delta_m) > RATIO_TOLERANCE:
        raise ValueError(
            f"TASA-OFICIAL-INCOMPATIBLE:{domain}:delta_p={delta_p}:delta_m={delta_m}"
        )
    identity = None if r is None else m - p * r
    if identity is not None and abs(identity) > RATIO_TOLERANCE:
        raise ValueError(f"IDENTIDAD-M-P-R-FALLA:{domain}:{identity}")
    return DomainResult(
        dominio=domain,
        N=N,
        A=A,
        T=T,
        p=p,
        m=m,
        r=r,
        p_oficial=p_official,
        m_oficial=m_official,
        delta_p_oficial=delta_p,
        delta_m_oficial=delta_m,
        residuo_identidad=identity,
    )


def load_and_derive(csv_bytes: bytes, *, enforce_parent_hash: bool = True) -> dict:
    if enforce_parent_hash and sha256(csv_bytes) != EXPECTED_PARENT_SHA256:
        raise ValueError("CSV-PADRE-SHA256-NO-COINCIDE")
    try:
        text = csv_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV-PADRE-NO-UTF8") from exc
    rows = list(csv.DictReader(io.StringIO(text)))
    if len(rows) != 10:
        raise ValueError(f"CSV-PADRE-FILAS-INESPERADAS:{len(rows)}")
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row.get("indicador_id", ""), row.get("dominio", ""))
        if key in by_key:
            raise ValueError(f"CSV-PADRE-CLAVE-DUPLICADA:{key}")
        by_key[key] = row
    expected = {(indicator, domain) for indicator in (PREVALENCE_ID, INCIDENCE_ID) for domain in DOMAINS}
    if set(by_key) != expected:
        raise ValueError("CSV-PADRE-DOMINIOS-O-INDICADORES-INCOMPATIBLES")

    domains = {
        domain: derive_domain(by_key[(PREVALENCE_ID, domain)], by_key[(INCIDENCE_ID, domain)])
        for domain in DOMAINS
    }
    sums = {
        mass: sum((getattr(domains[d], mass) for d in SIZES), Decimal(0))
        for mass in ("N", "A", "T")
    }
    residuals = {mass: sums[mass] - getattr(domains[NATIONAL], mass) for mass in sums}
    for mass, residual in residuals.items():
        if abs(residual) > MASS_TOLERANCE:
            raise ValueError(f"TAMANOS-NO-RECONSTRUYEN-NACIONAL:{mass}:{residual}")

    shares = []
    for domain in SIZES:
        result = domains[domain]
        shares.append(
            {
                "dominio": domain,
                "N": result.N,
                "participacion_N": result.N / sums["N"],
                "A": result.A,
                "participacion_A": result.A / sums["A"],
                "T": result.T,
                "participacion_T": result.T / sums["T"],
            }
        )

    micro = domains["Micro"]
    contrasts = []
    for domain in SIZES[1:]:
        item = domains[domain]
        if item.r is None or micro.r is None:
            raise ValueError(f"CONTRASTE-NO-ESTIMABLE-A-CERO:{domain}")
        delta_m = item.m - micro.m
        prevalence_term = Decimal("0.5") * (item.p - micro.p) * (item.r + micro.r)
        intensity_term = Decimal("0.5") * (item.r - micro.r) * (item.p + micro.p)
        decomposition_residual = delta_m - prevalence_term - intensity_term
        if abs(decomposition_residual) > RATIO_TOLERANCE:
            raise ValueError(f"DESCOMPOSICION-FALLA:{domain}:{decomposition_residual}")
        if abs(prevalence_term) > abs(intensity_term):
            dominant = "PREVALENCIA"
        elif abs(intensity_term) > abs(prevalence_term):
            dominant = "INTENSIDAD-CONDICIONAL"
        else:
            dominant = "IGUALES"
        contrasts.append(
            {
                "dominio": domain,
                "referencia": "Micro",
                "diferencia_p_pp": (item.p - micro.p) * Decimal(100),
                "diferencia_m": delta_m,
                "diferencia_r": item.r - micro.r,
                "contribucion_prevalencia": prevalence_term,
                "contribucion_intensidad_condicional": intensity_term,
                "suma_contribuciones": prevalence_term + intensity_term,
                "residuo_descomposicion": decomposition_residual,
                "componente_dominante_abs": dominant,
            }
        )
    return {
        "domains": domains,
        "sums": sums,
        "residuals": residuals,
        "shares": shares,
        "contrasts": contrasts,
    }


def _fmt_ratio(value: Decimal | None) -> str:
    return "" if value is None else format(value.quantize(Q12), "f")


def _fmt_mass(value: Decimal) -> str:
    return format(value.quantize(Q4), "f")


def _csv_bytes(fieldnames: list[str], rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def expanded_table(derived: dict) -> bytes:
    fields = [
        "dominio", "N_expuestas", "A_afectadas", "T_tramites_inspecciones_corrupcion",
        "p_prevalencia", "m_por_empresa_expuesta", "r_por_empresa_afectada",
        "estatus_r", "p_oficial", "m_oficial", "delta_p_oficial", "delta_m_oficial",
        "residuo_identidad_m_p_r", "periodo", "universo", "incertidumbre",
    ]
    rows = []
    for domain in DOMAINS:
        item = derived["domains"][domain]
        rows.append({
            "dominio": domain,
            "N_expuestas": _fmt_mass(item.N),
            "A_afectadas": _fmt_mass(item.A),
            "T_tramites_inspecciones_corrupcion": _fmt_mass(item.T),
            "p_prevalencia": _fmt_ratio(item.p),
            "m_por_empresa_expuesta": _fmt_ratio(item.m),
            "r_por_empresa_afectada": _fmt_ratio(item.r),
            "estatus_r": "ESTIMABLE" if item.r is not None else "NO-ESTIMABLE-A-CERO",
            "p_oficial": _fmt_ratio(item.p_oficial),
            "m_oficial": _fmt_ratio(item.m_oficial),
            "delta_p_oficial": _fmt_ratio(item.delta_p_oficial),
            "delta_m_oficial": _fmt_ratio(item.delta_m_oficial),
            "residuo_identidad_m_p_r": _fmt_ratio(item.residuo_identidad),
            "periodo": "Durante 2020 (enero a la fecha de entrevista)",
            "universo": "Empresas ENCRIGE expuestas a al menos un trámite o inspección",
            "incertidumbre": "NO-DISPONIBLE-EN-REPRESENTACION-CSV",
        })
    return _csv_bytes(fields, rows)


def participation_table(derived: dict) -> bytes:
    fields = [
        "dominio", "N_expuestas", "participacion_exposicion",
        "A_afectadas", "participacion_empresas_afectadas",
        "T_tramites_inspecciones_corrupcion", "participacion_volumen_corrupcion",
    ]
    rows = []
    for item in derived["shares"]:
        rows.append({
            "dominio": item["dominio"],
            "N_expuestas": _fmt_mass(item["N"]),
            "participacion_exposicion": _fmt_ratio(item["participacion_N"]),
            "A_afectadas": _fmt_mass(item["A"]),
            "participacion_empresas_afectadas": _fmt_ratio(item["participacion_A"]),
            "T_tramites_inspecciones_corrupcion": _fmt_mass(item["T"]),
            "participacion_volumen_corrupcion": _fmt_ratio(item["participacion_T"]),
        })
    return _csv_bytes(fields, rows)


def contrast_table(derived: dict) -> bytes:
    fields = [
        "dominio", "referencia", "diferencia_prevalencia_pp",
        "diferencia_m_por_empresa_expuesta", "diferencia_r_por_empresa_afectada",
        "contribucion_asociada_prevalencia", "contribucion_asociada_intensidad_condicional",
        "suma_contribuciones", "residuo_descomposicion", "componente_dominante_abs",
    ]
    rows = []
    for item in derived["contrasts"]:
        rows.append({
            "dominio": item["dominio"],
            "referencia": item["referencia"],
            "diferencia_prevalencia_pp": _fmt_ratio(item["diferencia_p_pp"]),
            "diferencia_m_por_empresa_expuesta": _fmt_ratio(item["diferencia_m"]),
            "diferencia_r_por_empresa_afectada": _fmt_ratio(item["diferencia_r"]),
            "contribucion_asociada_prevalencia": _fmt_ratio(item["contribucion_prevalencia"]),
            "contribucion_asociada_intensidad_condicional": _fmt_ratio(item["contribucion_intensidad_condicional"]),
            "suma_contribuciones": _fmt_ratio(item["suma_contribuciones"]),
            "residuo_descomposicion": _fmt_ratio(item["residuo_descomposicion"]),
            "componente_dominante_abs": item["componente_dominante_abs"],
        })
    return _csv_bytes(fields, rows)


def checks_json(derived: dict, parent_sha: str) -> bytes:
    identity = [
        abs(v.residuo_identidad or Decimal(0)) for v in derived["domains"].values()
    ]
    official = [
        max(abs(v.delta_p_oficial), abs(v.delta_m_oficial))
        for v in derived["domains"].values()
    ]
    decomposition = [abs(v["residuo_descomposicion"]) for v in derived["contrasts"]]
    document = {
        "csv_padre_sha256": parent_sha,
        "dominios": list(DOMAINS),
        "partes_tamano": list(SIZES),
        "nacional_excluido_de_partes": True,
        "compatibilidad": {
            "unidad": "empresa",
            "periodo": "Durante 2020 (enero a la fecha de entrevista)",
            "denominador": "unidades económicas expuestas a al menos un trámite o inspección",
            "T": "trámites o inspecciones con experiencia de corrupción",
        },
        "tolerancias_fijadas": {
            "masa_expandida_abs": str(MASS_TOLERANCE),
            "razon_abs": str(RATIO_TOLERANCE),
        },
        "suma_tamanos": {k: _fmt_mass(v) for k, v in derived["sums"].items()},
        "residuo_suma_tamanos_menos_nacional": {
            k: _fmt_mass(v) for k, v in derived["residuals"].items()
        },
        "max_delta_tasa_oficial": _fmt_ratio(max(official)),
        "max_residuo_identidad_m_p_r": _fmt_ratio(max(identity)),
        "max_residuo_descomposicion": _fmt_ratio(max(decomposition)),
        "incertidumbre": "NO-DISPONIBLE-EN-REPRESENTACION-CSV",
        "estadistica_de_respondentes": "NINGUNA",
    }
    return (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def figure_svg(derived: dict) -> bytes:
    width, height = 1280, 820
    left, bar_width = 390, 760
    colors = {"Micro": "#2864A8", "Pequeña": "#E07A2D", "Mediana": "#2A9D6F", "Grande": "#8C5AA8"}
    groups = [
        ("participacion_N", "Exposición: unidades económicas con ≥1 trámite o inspección (Nₛ / ΣNₛ)"),
        ("participacion_A", "Alcance: unidades económicas afectadas por ≥1 acto (Aₛ / ΣAₛ)"),
        ("participacion_T", "Volumen: trámites/inspecciones con corrupción (Tₛ / ΣTₛ)"),
    ]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FFFFFF"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D2733}.title{font-size:26px;font-weight:700}.subtitle{font-size:16px;fill:#52606D}.group{font-size:17px;font-weight:700}.label{font-size:15px}.value{font-size:14px;font-weight:700}.axis{font-size:12px;fill:#65717E}</style>',
        '<text x="40" y="42" class="title">ENCRIGE 2020 · participación por tamaño</text>',
        '<text x="40" y="69" class="subtitle">Empresas privadas cubiertas, expuestas a trámites/inspecciones · enero–entrevista 2020 · estimaciones expandidas</text>',
    ]
    share_by_domain = {row["dominio"]: row for row in derived["shares"]}
    start_y = 115
    for group_index, (key, label) in enumerate(groups):
        group_y = start_y + group_index * 220
        lines.append(f'<text x="40" y="{group_y}" class="group">{html.escape(label)}</text>')
        for tick in range(0, 101, 20):
            x = left + bar_width * tick / 100
            lines.append(f'<line x1="{x:.1f}" y1="{group_y+18}" x2="{x:.1f}" y2="{group_y+174}" stroke="#D9E0E7" stroke-width="1"/>')
            lines.append(f'<text x="{x:.1f}" y="{group_y+193}" text-anchor="middle" class="axis">{tick}%</text>')
        for index, domain in enumerate(SIZES):
            y = group_y + 30 + index * 36
            share = share_by_domain[domain][key]
            pixels = float(share * Decimal(bar_width))
            percent = share * Decimal(100)
            lines.append(f'<text x="{left-16}" y="{y+16}" text-anchor="end" class="label">{html.escape(domain)}</text>')
            lines.append(f'<rect x="{left}" y="{y}" width="{bar_width}" height="22" rx="3" fill="#EEF2F6"/>')
            lines.append(f'<rect x="{left}" y="{y}" width="{pixels:.3f}" height="22" rx="3" fill="{colors[domain]}"/>')
            value_x = min(left + pixels + 8, width - 82)
            anchor = "start"
            if pixels > bar_width - 75:
                value_x = left + pixels - 8
                anchor = "end"
            lines.append(f'<text x="{value_x:.3f}" y="{y+16}" text-anchor="{anchor}" class="value">{percent.quantize(Decimal("0.01"))}%</text>')
    lines.extend([
        '<text x="40" y="790" class="subtitle">Participaciones calculadas dentro de los cuatro tamaños; el total nacional no se duplica como categoría.</text>',
        '</svg>',
    ])
    return ("\n".join(lines) + "\n").encode("utf-8")


def build_artifacts(csv_bytes: bytes, *, enforce_parent_hash: bool = True) -> tuple[dict, dict[str, bytes]]:
    derived = load_and_derive(csv_bytes, enforce_parent_hash=enforce_parent_hash)
    artifacts = {
        "tabla-ampliada.csv": expanded_table(derived),
        "participaciones-por-tamano.csv": participation_table(derived),
        "contrastes-vs-micro.csv": contrast_table(derived),
        "controles.json": checks_json(derived, sha256(csv_bytes)),
        "participaciones-por-tamano.svg": figure_svg(derived),
    }
    return derived, artifacts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=PARENT_CSV)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    csv_bytes = args.input.read_bytes()
    derived, artifacts = build_artifacts(csv_bytes)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in artifacts.items():
        (args.output_dir / name).write_bytes(data)
    print(f"ENCRIGE-CARGA-INTENSIDAD · {len(derived['domains'])} dominios · {len(derived['contrasts'])} contrastes")
    for name in artifacts:
        print(args.output_dir / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

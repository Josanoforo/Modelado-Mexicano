#!/usr/bin/env python3
"""Control con Decimal; no importa ni reutiliza el medidor sellado."""
from __future__ import annotations

import csv
import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 32
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv"
CHANGES = ROOT / "data/analisis-imor-contexto-temporal/cambios-mensuales-e-interanuales.csv"
SUMMARY = ROOT / "data/analisis-imor-contexto-temporal/resumen-producto-regimen.csv"
OUTPUT = Path(__file__).with_name("control-independiente.json")
EXPECTED_SHA = "772f9d0b9da57b18ef9abdd5824b0824b6191e65668103e3a8329171d3df88e9"


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def main() -> None:
    raw = SOURCE.read_bytes()
    source_rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    values = {(r["fecha"], r["producto"]): Decimal(r["valor"]) for r in source_rows}
    groups = {}
    for row in source_rows:
        groups.setdefault((row["producto"], row["regimen_definicion"]), []).append(Decimal(row["valor"]))

    with CHANGES.open(encoding="utf-8", newline="") as handle:
        changes = {(r["fecha"], r["producto"]): r for r in csv.DictReader(handle)}
    with SUMMARY.open(encoding="utf-8", newline="") as handle:
        summary = {(r["producto"], r["regimen_definicion"]): r for r in csv.DictReader(handle)}

    sha = hashlib.sha256(raw).hexdigest()
    check(sha == EXPECTED_SHA, "sha256")
    check(len(source_rows) == 615 and len(values) == 615, "llaves")
    check(len({k[0] for k in values}) == 123 and len({k[1] for k in values}) == 5, "dimensiones")

    pre_total = groups[("Consumo total", "PRE_IFRS9_CARTERA_VENCIDA")]
    ifrs_cards = groups[("Tarjetas de crédito", "IFRS9_ETAPA_3")]
    pre_mean = sum(pre_total) / Decimal(len(pre_total))
    ifrs_cards_mean = sum(ifrs_cards) / Decimal(len(ifrs_cards))
    check(abs(pre_mean - Decimal("4.2108333333333333333333333333333")) < Decimal("1e-28"), "media pre total")
    check(abs(ifrs_cards_mean - Decimal("3.1211764705882352941176470588235")) < Decimal("1e-28"), "media IFRS9 tarjetas")

    feb22_card_pp = values[("2022-02", "Tarjetas de crédito")] - values[("2022-01", "Tarjetas de crédito")]
    jan23_card_pp = values[("2023-01", "Tarjetas de crédito")] - values[("2022-01", "Tarjetas de crédito")]
    check(feb22_card_pp == Decimal("0.14"), "cambio mensual referencia")
    check(jan23_card_pp == Decimal("0.22"), "cambio interanual referencia")
    check(changes[("2022-01", "Tarjetas de crédito")]["cambio_mensual_pp"] == "", "inicio régimen mensual vacío")
    check(changes[("2022-01", "Tarjetas de crédito")]["cambio_interanual_pp"] == "", "inicio régimen interanual vacío")
    check(Decimal(changes[("2022-02", "Tarjetas de crédito")]["cambio_mensual_pp"]) == feb22_card_pp, "tabla mensual")
    check(Decimal(changes[("2023-01", "Tarjetas de crédito")]["cambio_interanual_pp"]) == jan23_card_pp, "tabla interanual")

    check(max(groups[("Personales", "PRE_IFRS9_CARTERA_VENCIDA")]) == Decimal("7.60"), "máximo personales pre")
    check(summary[("Personales", "PRE_IFRS9_CARTERA_VENCIDA")]["fechas_maximo"] == "2021-01", "fecha máximo")
    check(min(groups[("ABCD", "IFRS9_ETAPA_3")]) == Decimal("1.36"), "mínimo ABCD IFRS9")
    check(summary[("ABCD", "IFRS9_ETAPA_3")]["fechas_minimo"] == "2024-05", "fecha mínimo")

    expected_monthly = 5 * ((72 - 1) + (51 - 1))
    expected_yoy = 5 * ((72 - 12) + (51 - 12))
    observed_monthly = sum(bool(r["cambio_mensual_pp"]) for r in changes.values())
    observed_yoy = sum(bool(r["cambio_interanual_pp"]) for r in changes.values())
    check(observed_monthly == expected_monthly == 605, "conteo mensual")
    check(observed_yoy == expected_yoy == 495, "conteo interanual")

    evidence = {
        "estado": "VALIDACION-INDEPENDIENTE-COINCIDE",
        "metodo": "csv+Decimal; no importa el medidor sellado",
        "input_sha256": sha,
        "controles": {
            "filas_llaves": 615,
            "meses": 123,
            "productos": 5,
            "media_pre_consumo_total": str(pre_mean),
            "media_ifrs9_tarjetas": str(ifrs_cards_mean),
            "tarjetas_2022_02_mensual_pp": str(feb22_card_pp),
            "tarjetas_2023_01_interanual_pp": str(jan23_card_pp),
            "personales_pre_maximo": "7.60@2021-01",
            "abcd_ifrs9_minimo": "1.36@2024-05",
            "cambios_mensuales": observed_monthly,
            "cambios_interanuales": observed_yoy,
        },
    }
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(evidence["estado"])


if __name__ == "__main__":
    main()

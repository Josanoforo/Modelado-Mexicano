#!/usr/bin/env python3
"""Materializa agregados legibles del RESULT sellado de SHED 2025."""
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-SHED2025-BNPL-DANO-0001"
OUT = ROOT / "data/shed2025-bnpl-dano"


def _write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    payload = json.loads((CALC / "resultados.json").read_text(encoding="utf-8"))
    if payload.get("spec_id") != "CALC-SHED2025-BNPL-DANO-0001":
        raise SystemExit("RESULT de otro CALC")
    r = payload["resultados"]
    OUT.mkdir(parents=True, exist_ok=True)

    labels = {
        "USO": "Uso de BNPL",
        "ATRASO": "Atraso BNPL entre usuarios",
        "CARGO": "Cargo extra entre quienes afirmaron atraso",
        "SOBREGIRO": "Sobregiro/NSF atribuido a BNPL en ruta elegible",
    }
    estimands = []
    for code, label in labels.items():
        p = f"RESULT-SHED-BNPL-{code}-"
        estimands.append({
            "estimando": code.lower(),
            "etiqueta": label,
            "n_elegible": r[p + "N-ELEGIBLE"],
            "n_valido": r[p + "N-VALIDO"],
            "n_positivos": r[p + "N-POSITIVOS"],
            "masa_elegible_weight": r[p + "MASA-ELEGIBLE"],
            "masa_valida_weight": r[p + "MASA-VALIDA"],
            "masa_positivos_weight": r[p + "MASA-POSITIVOS"],
            "proporcion_ponderada": r[p + "PUNTO"],
            "porcentaje": round(100 * r[p + "PUNTO"], 6),
            "faltantes_por_razon": r[p + "FALTANTES"],
            "definicion": r[p + "DEFINICION"],
            "geografia": "Estados Unidos",
            "interpretacion": "descriptiva_no_causal_no_transportable_a_Mexico",
        })
    _write_csv(OUT / "estimandos-shed.csv", estimands, list(estimands[0]))

    cells = []
    for afford in ("NO", "YES"):
        for late in ("NO", "YES"):
            base = f"RESULT-SHED-BNPL-ASEQ-ATRASO-CELDA-AF-{afford}-ATR-{late}-"
            cells.append({
                "bnpl4_e_asequibilidad": afford.title(),
                "bnpl3_atraso": late.title(),
                "n": r[base + "N"],
                "masa_weight": r[base + "MASA"],
                "universo": "usuarios_BNPL_con_BNPL4_e_y_BNPL3_validos",
                "geografia": "Estados Unidos",
            })
    _write_csv(OUT / "asequibilidad-atraso-2x2.csv", cells, list(cells[0]))

    missing = []
    for code in labels:
        text = r[f"RESULT-SHED-BNPL-{code}-FALTANTES"]
        for item in text.split(";"):
            reason, count = item.rsplit("=", 1)
            missing.append({"estimando": code.lower(), "razon": reason, "n": int(count)})
    text = r["RESULT-SHED-BNPL-ASEQ-ATRASO-FALTANTES"]
    for item in text.split(";"):
        reason, count = item.rsplit("=", 1)
        missing.append({"estimando": "asequibilidad_atraso", "razon": reason, "n": int(count)})
    _write_csv(OUT / "faltantes-por-ruta.csv", missing, list(missing[0]))

    p_no = r["RESULT-SHED-BNPL-ASEQ-ATRASO-P-ATRASO-AF-NO"]
    p_yes = r["RESULT-SHED-BNPL-ASEQ-ATRASO-P-ATRASO-AF-YES"]
    delta = r["RESULT-SHED-BNPL-ASEQ-ATRASO-DIF-YES-MENOS-NO"]
    table = [
        "# Resultados SHED 2025: BNPL, daño y universos", "",
        "| Estimando | n válido | positivos | masa válida | masa positiva | Punto |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in estimands:
        table.append(
            f"| {row['etiqueta']} | {row['n_valido']:,} | {row['n_positivos']:,} | "
            f"{row['masa_valida_weight']:,.4f} | {row['masa_positivos_weight']:,.4f} | "
            f"{row['porcentaje']:.2f}% |"
        )
    table += [
        "", "## Asequibilidad y atraso", "",
        f"Entre 2,004 usuarios con ambas respuestas válidas, el atraso ponderado fue "
        f"{100*p_yes:.2f}% cuando `BNPL4_e=Yes` y {100*p_no:.2f}% cuando "
        f"`BNPL4_e=No`; diferencia descriptiva **{100*delta:.2f} pp**.", "",
        "La ruta de `BNPL3` rechazado aportó 0 respuestas válidas a `BNPL3A`; "
        "permanece separada y no entra en el estimando principal de cargo.", "",
        "Todos los puntos describen Estados Unidos y el instrumento SHED 2025. "
        "No son efectos causales, tasas mexicanas ni parámetros adoptados.",
    ]
    (OUT / "resultados-legibles.md").write_text("\n".join(table) + "\n", encoding="utf-8")

    ficha = """# Ficha de uso extranjero · SHED 2025 BNPL

- **País/población:** Estados Unidos, personas adultas cubiertas por SHED 2025.
- **Unidad/periodo:** persona; corte transversal 2025.
- **Ponderador:** `weight`, postestratificación escalada al tamaño muestral.
- **Aporte permitido:** descripción de uso, atraso, cargo y sobregiro/NSF, y asociación descriptiva entre motivo de asequibilidad y atraso.
- **Uso prohibido:** transportar tasas a México, llamar causal a la asociación, construir “cualquier daño”, mezclar con default CFPB a 120 días o adoptar un parámetro del motor.
- **Precisión:** sólo puntos; no se publican EE/IC sin diseño completo acreditado.
- **Residual N34:** sigue abierta la evidencia mexicana de BNPL/crédito digital o lender, costo/fricción objetiva, daño, negativos y estrategia causal.
"""
    (OUT / "ficha-uso-extranjero.md").write_text(ficha, encoding="utf-8")

    bars = [(row["etiqueta"], row["porcentaje"], row["n_valido"]) for row in estimands]
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="410" viewBox="0 0 960 410" role="img">',
        '<title>Proporciones ponderadas BNPL en SHED 2025</title>',
        '<desc>Cuatro barras con universos distintos y denominadores explícitos. Estados Unidos; descripción no causal.</desc>',
        '<rect width="960" height="410" fill="#ffffff"/>',
        '<text x="40" y="38" font-family="sans-serif" font-size="24" font-weight="700">SHED 2025 · BNPL y daño</text>',
        '<text x="40" y="64" font-family="sans-serif" font-size="14" fill="#444">Estados Unidos · proporciones ponderadas con weight · cada barra conserva su universo</text>',
    ]
    colors = ["#2b6cb0", "#2f855a", "#b7791f", "#9b2c2c"]
    for idx, ((label, pct, n), color) in enumerate(zip(bars, colors)):
        y = 105 + idx * 70
        width = pct * 9
        svg += [
            f'<text x="40" y="{y+16}" font-family="sans-serif" font-size="15">{label}</text>',
            f'<rect x="390" y="{y}" width="{width:.2f}" height="24" rx="3" fill="{color}"/>',
            f'<text x="{405+width:.2f}" y="{y+17}" font-family="sans-serif" font-size="15" font-weight="700">{pct:.2f}% · n válido={n:,}</text>',
        ]
    svg += [
        '<text x="40" y="390" font-family="sans-serif" font-size="13" fill="#555">Cargo: sólo atraso afirmativo. Sobregiro/NSF: sólo BNPL1=Yes y BK2_f=Yes. Sin transporte a México.</text>',
        '</svg>',
    ]
    (OUT / "grafico-bnpl.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")
    print(f"PUBLICADO {OUT.relative_to(ROOT)}: 6 archivos")


if __name__ == "__main__":
    main()

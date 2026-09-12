#!/usr/bin/env python3
"""Genera vistas agregadas deterministas a partir del resultado sellado."""
from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PREFIX = "RESULT-TANDAS-PANEL-ENNVIH-"


def pct(value) -> str:
    return f"{100 * value:.2f}%"


def load():
    values = json.loads((HERE / "resultados.json").read_text())["resultados"]
    out = {}
    for pair in ("1A2", "2A3"):
        base = PREFIX + pair + "-"
        out[pair] = {
            "matrix": json.loads(values[base + "MATRIZ-JSON"]),
            "coverage": json.loads(values[base + "COBERTURA-JSON"]),
            "attrition": json.loads(values[base + "ATTRITION-JSON"]),
            "entries": json.loads(values[base + "ENTRADAS-UNIVERSO-JSON"]),
        }
    return out


def matrix_tsv(data) -> str:
    lines = ["par\tinicial\tseguimiento\tn\tn_en_masa\tmasa\ttasa_primaria\ttasa_no_ponderada\tponderacion"]
    for item in data.values():
        matrix = item["matrix"]
        for initial in ("NO", "SI"):
            rates = matrix["bases_y_tasas"][initial]
            for follow in ("NO", "SI"):
                cell = matrix["celdas"][f"{initial}_A_{follow}"]
                lines.append("\t".join(map(str, [
                    matrix["par"], initial, follow, cell["n"], cell["n_en_masa"],
                    cell["masa"], rates[f"p_sigue_{follow.lower()}_primaria"],
                    rates[f"p_sigue_{follow.lower()}_no_ponderada"], matrix["ponderacion_primaria"],
                ])))
    return "\n".join(lines) + "\n"


def coverage_tsv(data) -> str:
    lines = ["par\tdimension\tgrupo\tn_inicial_valido\tn_par_valido\tretencion\tn_perdida\tcomponente\tn_componente"]
    for item in data.values():
        par = item["coverage"]["par"]
        for dimension, groups in item["attrition"].items():
            for group, row in groups.items():
                for component, n in row["componentes"].items():
                    lines.append("\t".join(map(str, [
                        par, dimension, group, row["n_inicial_respuesta_valida"],
                        row["n_par_valido"], row["p_retencion_par_valido"],
                        row["n_perdida_par"], component, n,
                    ])))
    return "\n".join(lines) + "\n"


def entries_tsv(data) -> str:
    lines = ["par\tn_respuesta_valida_seguimiento\tn_par_valido_inicial\tn_entrada_universo\tn_ya_en_roster_inicial\tn_no_presente_roster_inicial\ttratamiento"]
    for item in data.values():
        row = item["entries"]
        lines.append("\t".join(map(str, [
            row["par"], row["n_respuesta_valida_seguimiento_total"],
            row["n_par_valido_desde_cohorte_inicial"], row["n_entrada_al_universo_analitico"],
            row["n_entrada_ya_en_roster_inicial_sin_libro_iiib_inicial"],
            row["n_entrada_no_presente_en_roster_inicial"], row["tratamiento"],
        ])))
    return "\n".join(lines) + "\n"


def svg(data) -> str:
    rows = []
    for label, item in zip(("2002 → 2005–06", "2005–06 → 2009–12"), data.values()):
        m = item["matrix"]["bases_y_tasas"]
        rows.append((label, m["SI"]["p_sigue_si_primaria"], m["NO"]["p_sigue_si_primaria"], item["matrix"]["ponderacion_primaria"]))
    bars = []
    for i, (label, stay, enter, method) in enumerate(rows):
        y = 85 + i * 150
        bars.extend([
            f'<text x="20" y="{y-34}" class="pair">{label}</text>',
            f'<text x="20" y="{y-10}" class="method">{method}</text>',
            f'<text x="20" y="{y+24}" class="label">Permanencia</text>',
            f'<rect x="150" y="{y+7}" width="{stay*520:.2f}" height="22" class="stay"/>',
            f'<text x="{160+stay*520:.2f}" y="{y+24}" class="value">{pct(stay)}</text>',
            f'<text x="20" y="{y+62}" class="label">Entrada</text>',
            f'<rect x="150" y="{y+45}" width="{enter*520:.2f}" height="22" class="enter"/>',
            f'<text x="{160+enter*520:.2f}" y="{y+62}" class="value">{pct(enter)}</text>',
        ])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="390" viewBox="0 0 760 390" role="img" aria-labelledby="title desc">
<title id="title">Permanencia y entrada a tandas entre entrevistas ENNViH</title>
<desc id="desc">Tasas condicionales para el panel observado con respuesta válida en ambas olas.</desc>
<style>.bg{{fill:#fff}}.pair{{font:700 18px sans-serif;fill:#17213a}}.method{{font:12px monospace;fill:#59647a}}.label{{font:14px sans-serif;fill:#17213a}}.value{{font:700 14px sans-serif;fill:#17213a}}.stay{{fill:#2166ac}}.enter{{fill:#d6604d}}.note{{font:12px sans-serif;fill:#59647a}}</style>
<rect class="bg" width="760" height="390"/>
<text x="20" y="28" class="pair">Transiciones de participación en tandas</text>
{''.join(bars)}
<text x="20" y="375" class="note">Panel observado; tasas descriptivas entre entrevistas, no anualizadas ni causales.</text>
</svg>\n'''


def main() -> None:
    data = load()
    outputs = {
        "matrices-transicion.tsv": matrix_tsv(data),
        "cobertura-attrition.tsv": coverage_tsv(data),
        "entradas-universo.tsv": entries_tsv(data),
        "flujos-agregados.svg": svg(data),
    }
    for name, content in outputs.items():
        (HERE / name).write_text(content)
    print("GENERADAS " + ", ".join(outputs))


if __name__ == "__main__":
    main()

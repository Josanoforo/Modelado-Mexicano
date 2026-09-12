"""Medidor Banxico: pago, problemas y costo percibido por producto y ola."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import math
from collections import Counter
from pathlib import Path

from tools.extrae_n34_producto_dano import iterar_primera_hoja_xlsx


INPUT_ID = "gen2_banxico_satisfaccion_usuarios_2019_2024_microdatos"
PFX = "RESULT-BANXICO-"
PRODUCTS = {
    "tdc": ("tarjeta_credito", {"1": "pago_total", "2": "pago_minimo_sin_atraso", "3": "atraso", "4": "no_ha_pagado"}, {3}, {4}),
    "hip": ("credito_hipotecario", {"1": "puntual", "2": "atraso_a_veces", "3": "atraso_casi_siempre", "4": "no_ha_podido_pagar"}, {2, 3}, {4}),
    "per": ("credito_personal", {"1": "puntual", "2": "atraso_a_veces", "3": "atraso_casi_siempre", "4": "no_ha_podido_pagar"}, {2, 3}, {4}),
    "nom": ("credito_nomina", {"1": "puntual", "2": "atraso_a_veces", "3": "atraso_casi_siempre", "4": "no_ha_podido_pagar"}, {2, 3}, {4}),
    "aut": ("credito_automotriz", {"1": "puntual", "2": "atraso_a_veces", "3": "atraso_casi_siempre", "4": "no_ha_podido_pagar"}, {2, 3}, {4}),
}
NOT_RAISED = {(2019, "hip"), (2019, "nom"), (2019, "aut")}
FIELDS = [
    "estimando_tipo", "producto", "ola", "variable_codigos", "universo",
    "n_elegible", "n_valido", "n_positivo", "masa_elegible", "masa_valida",
    "masa_positiva", "faltantes_por_causa", "estimacion", "unidad", "alcance",
]


def _code(value):
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _weight(value):
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) and out > 0 else None


def _csv_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def _summary_bytes(rows):
    fields = ["producto", "ola", "n_tenedores", "masa_tenedores", "atraso", "imposibilidad", "dano_combinado", "problemas", "reclamacion_entre_problemas"]
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def _missing(code, ns_code):
    if code == "":
        return "blanco"
    if code == "-1":
        return "salto_no_aplica"
    if code == str(ns_code):
        return "no_sabe_no_contesto"
    return "codigo_invalido"


def _estimate(eligible, col, allowed, positive, *, nonraised=False):
    allowed = {str(v) for v in allowed}
    positive = {str(v) for v in positive}
    miss = Counter()
    n_valid = n_positive = 0
    mass_eligible = mass_valid = mass_positive = 0.0
    for row in eligible:
        weight = _weight(row["ponderador"])
        if weight is None:
            miss["peso_no_positivo"] += 1
        else:
            mass_eligible += weight
        code = _code(row[col])
        if nonraised:
            miss["no_levantada"] += 1
            continue
        if code in allowed:
            n_valid += 1
            if code in positive:
                n_positive += 1
            if weight is not None:
                mass_valid += weight
                if code in positive:
                    mass_positive += weight
        else:
            miss[_missing(code, 5 if col.endswith("comp_pago") else 99)] += 1
    estimate = None if mass_valid <= 0 else mass_positive / mass_valid
    order = ("no_levantada", "salto_no_aplica", "no_sabe_no_contesto", "blanco", "codigo_invalido", "peso_no_positivo")
    return {
        "n_elegible": len(eligible), "n_valido": n_valid, "n_positivo": n_positive,
        "masa_elegible": mass_eligible, "masa_valida": mass_valid,
        "masa_positiva": mass_positive,
        "faltantes_por_causa": ";".join(f"{key}={miss[key]}" for key in order),
        "estimacion": estimate,
    }


def _row(kind, product, wave, variable, universe, stats, unit="proporcion ponderada"):
    def fmt(value):
        if value is None:
            return ""
        if isinstance(value, float):
            return f"{value:.12f}"
        return value
    return {
        "estimando_tipo": kind, "producto": product, "ola": wave,
        "variable_codigos": variable, "universo": universe,
        "n_elegible": stats["n_elegible"], "n_valido": stats["n_valido"],
        "n_positivo": stats["n_positivo"], "masa_elegible": fmt(stats["masa_elegible"]),
        "masa_valida": fmt(stats["masa_valida"]), "masa_positiva": fmt(stats["masa_positiva"]),
        "faltantes_por_causa": stats["faltantes_por_causa"],
        "estimacion": fmt(stats["estimacion"]), "unidad": unit,
        "alcance": "Mexico;18-70;localidades_50000_mas;descriptivo_no_causal",
    }


def _joint(eligible, pfx, product, wave, nonraised):
    cost_col, pay_col = f"{pfx}_intereses", f"{pfx}_comp_pago"
    valid = []
    miss = Counter()
    mass_eligible = 0.0
    for row in eligible:
        weight = _weight(row["ponderador"])
        if weight is None:
            miss["peso_no_positivo"] += 1
        else:
            mass_eligible += weight
        cost, pay = _code(row[cost_col]), _code(row[pay_col])
        cost_ok = cost in {str(i) for i in range(11)}
        pay_ok = (not nonraised) and pay in {"1", "2", "3", "4"}
        if not cost_ok:
            miss[f"costo_{_missing(cost, 99)}"] += 1
        if nonraised:
            miss["pago_no_levantada"] += 1
        elif not pay_ok:
            miss[f"pago_{_missing(pay, 5)}"] += 1
        if cost_ok and pay_ok:
            valid.append((row, cost, pay, weight))
    mass_valid = sum(weight for _, _, _, weight in valid if weight is not None)
    missing_text = ";".join(f"{key}={miss[key]}" for key in sorted(miss)) or "ninguno=0"
    rows = []
    for cost in range(11):
        for pay in range(1, 5):
            cell = [(row, weight) for row, c, p, weight in valid if c == str(cost) and p == str(pay)]
            mass = sum(weight for _, weight in cell if weight is not None)
            stats = {
                "n_elegible": len(eligible), "n_valido": len(valid), "n_positivo": len(cell),
                "masa_elegible": mass_eligible, "masa_valida": mass_valid, "masa_positiva": mass,
                "faltantes_por_causa": missing_text,
                "estimacion": None if mass_valid <= 0 else mass / mass_valid,
            }
            rows.append(_row("distribucion_conjunta_costo_pago", product, wave,
                             f"{cost_col}={cost}&{pay_col}={pay}",
                             "tenedores con costo y pago validos", stats))
    return rows


def _svg(summary):
    colors = {"tarjeta_credito": "#2455a4", "credito_hipotecario": "#d94841", "credito_personal": "#2f8f4e", "credito_nomina": "#8a4fb5", "credito_automotriz": "#d18b17"}
    labels = {"tarjeta_credito": "Tarjeta", "credito_hipotecario": "Hipotecario", "credito_personal": "Personal", "credito_nomina": "Nomina", "credito_automotriz": "Automotriz"}
    by = {(r["producto"], int(r["ola"])): r["dano_combinado"] for r in summary}
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="520" viewBox="0 0 900 520">', '<rect width="900" height="520" fill="white"/>', '<text x="70" y="34" font-family="sans-serif" font-size="20" font-weight="bold">Atraso o imposibilidad de pago, por producto y ola</text>', '<text x="70" y="56" font-family="sans-serif" font-size="12" fill="#555">Proporcion ponderada; cortes repetidos Banxico, localidades de 50 mil habitantes o mas</text>']
    for tick in range(0, 51, 10):
        y = 440 - tick * 7
        parts.append(f'<line x1="70" y1="{y}" x2="650" y2="{y}" stroke="#ddd"/>')
        parts.append(f'<text x="58" y="{y+4}" text-anchor="end" font-family="sans-serif" font-size="11">{tick}%</text>')
    for i, wave in enumerate(range(2019, 2025)):
        x = 90 + i * 108
        parts.append(f'<text x="{x}" y="465" text-anchor="middle" font-family="sans-serif" font-size="12">{wave}</text>')
    for j, product in enumerate(colors):
        points, segments = [], []
        for i, wave in enumerate(range(2019, 2025)):
            value = by.get((product, wave))
            if value in (None, ""):
                if len(points) > 1: segments.append(points)
                points = []
                continue
            points.append((90 + i * 108, 440 - float(value) * 700))
        if len(points) > 1: segments.append(points)
        for segment in segments:
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in segment)
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{colors[product]}" stroke-width="2.5"/>')
        for wave in range(2019, 2025):
            value = by.get((product, wave))
            if value not in (None, ""):
                x, y = 90 + (wave - 2019) * 108, 440 - float(value) * 700
                parts.append(f'<circle cx="{x}" cy="{y:.1f}" r="3.5" fill="{colors[product]}"/>')
        ly = 100 + j * 30
        parts.append(f'<line x1="690" y1="{ly}" x2="720" y2="{ly}" stroke="{colors[product]}" stroke-width="3"/>')
        parts.append(f'<text x="730" y="{ly+4}" font-family="sans-serif" font-size="12">{labels[product]}</text>')
    parts.append('<text x="70" y="500" font-family="sans-serif" font-size="11" fill="#555">Huecos: reactivo no levantado en los bytes. No son ceros.</text></svg>')
    return ("\n".join(parts) + "\n").encode("utf-8")


def calculate(path):
    iterator = iterar_primera_hoja_xlsx(Path(path))
    header = [_code(v) for v in next(iterator)]
    required = {"fecha", "ponderador"}
    for pfx in PRODUCTS:
        required.update({f"{pfx}_filtro", f"{pfx}_intereses", f"{pfx}_comp_pago", f"{pfx}_problemas", f"{pfx}_reclamacion"})
    missing_cols = sorted(required - set(header))
    if len(header) != 142 or missing_cols:
        raise ValueError(f"ESQUEMA-INESPERADO:columnas={len(header)}:faltan={missing_cols}")
    idx = {name: header.index(name) for name in required}
    data = []
    for values in iterator:
        data.append({name: values[pos] if pos < len(values) else None for name, pos in idx.items()})
    waves = Counter(int(row["fecha"]) for row in data)
    expected = {2019: 2072, 2020: 2075, 2021: 2071, 2022: 2060, 2023: 2070, 2024: 2060}
    if len(data) != 12408 or dict(sorted(waves.items())) != expected:
        raise ValueError(f"FILAS-OLAS-INESPERADAS:{len(data)}:{dict(waves)}")
    if any(_weight(row["ponderador"]) is None for row in data):
        raise ValueError("PONDERADOR-NO-POSITIVO")

    estimands, joint, cost_damage, summary = [], [], [], []
    lookup = {}
    for wave in sorted(waves):
        wave_rows = [row for row in data if int(row["fecha"]) == wave]
        for pfx, (product, pay_labels, late, impossible) in PRODUCTS.items():
            holders = [row for row in wave_rows if _code(row[f"{pfx}_filtro"]) == "1"]
            nonraised = (wave, pfx) in NOT_RAISED
            pay_col = f"{pfx}_comp_pago"
            pay_stats = {}
            for code, label in pay_labels.items():
                stats = _estimate(holders, pay_col, {1, 2, 3, 4}, {code}, nonraised=nonraised)
                pay_stats[f"pago_{code}"] = stats
                estimands.append(_row("distribucion_pago", product, wave, f"{pay_col}={code}:{label}", "tenedores con pago valido", stats))
            for name, positives in (("atraso", late), ("imposibilidad", impossible), ("dano_combinado", late | impossible)):
                stats = _estimate(holders, pay_col, {1, 2, 3, 4}, positives, nonraised=nonraised)
                pay_stats[name] = stats
                estimands.append(_row(name, product, wave, f"{pay_col}={','.join(map(str, sorted(positives)))}", "tenedores con pago valido", stats))
                lookup[(product, wave, name)] = stats
            problem = _estimate(holders, f"{pfx}_problemas", {1, 2}, {1})
            estimands.append(_row("problemas", product, wave, f"{pfx}_problemas=1", "tenedores con respuesta valida", problem))
            problem_holders = [row for row in holders if _code(row[f"{pfx}_problemas"]) == "1"]
            claim = _estimate(problem_holders, f"{pfx}_reclamacion", {1, 2}, {1})
            estimands.append(_row("reclamacion", product, wave, f"{pfx}_reclamacion=1", "tenedores con problema=1 y reclamacion valida", claim))
            joint.extend(_joint(holders, pfx, product, wave, nonraised))
            summary.append({
                "producto": product, "ola": wave, "n_tenedores": len(holders),
                "masa_tenedores": f"{sum(_weight(r['ponderador']) or 0 for r in holders):.12f}",
                "atraso": "" if pay_stats["atraso"]["estimacion"] is None else f"{pay_stats['atraso']['estimacion']:.12f}",
                "imposibilidad": "" if pay_stats["imposibilidad"]["estimacion"] is None else f"{pay_stats['imposibilidad']['estimacion']:.12f}",
                "dano_combinado": "" if pay_stats["dano_combinado"]["estimacion"] is None else f"{pay_stats['dano_combinado']['estimacion']:.12f}",
                "problemas": f"{problem['estimacion']:.12f}" if problem["estimacion"] is not None else "",
                "reclamacion_entre_problemas": f"{claim['estimacion']:.12f}" if claim["estimacion"] is not None else "",
            })
            if wave == 2024:
                for level in range(11):
                    level_holders = [row for row in holders if _code(row[f"{pfx}_intereses"]) == str(level)]
                    stats = _estimate(level_holders, pay_col, {1, 2, 3, 4}, late | impossible)
                    cost_damage.append(_row("dano_por_nivel_costo_2024", product, wave,
                                            f"{pfx}_intereses={level}&{pay_col}={','.join(map(str, sorted(late | impossible)))}",
                                            f"tenedores con costo={level} y pago valido", stats))

    artifacts = {
        "estimandos.csv": _csv_bytes(estimands),
        "conjunta-costo-pago.csv": _csv_bytes(joint),
        "costo-dano-2024.csv": _csv_bytes(cost_damage),
        "resumen-producto-ola.csv": _summary_bytes(summary),
        "atraso-por-producto-ola.svg": _svg(summary),
    }
    results = {
        PFX + "G-N-FILAS": len(data), PFX + "G-N-COLUMNAS": len(header),
        PFX + "G-N-OLAS": len(waves), PFX + "G-N-PRODUCTOS": len(PRODUCTS),
        PFX + "G-PESO-NO-POSITIVO-N": 0,
        PFX + "G-PRECISION-ESTADO": "NO-DISPONIBLE:SIN-UPM-ESTRATO-PROCEDIMIENTO",
        PFX + "G-PAGO-2019-NO-LEVANTADO": "HIP,NOM,AUT:ESTIMACION-NULL",
        PFX + "G-N-FILAS-ESTIMANDOS": len(estimands),
        PFX + "G-N-FILAS-CONJUNTA": len(joint),
        PFX + "G-N-FILAS-COSTO-DANO-2024": len(cost_damage),
    }
    hash_names = {"estimandos.csv": "ESTIMANDOS", "conjunta-costo-pago.csv": "CONJUNTA", "costo-dano-2024.csv": "COSTO-DANO-2024", "resumen-producto-ola.csv": "RESUMEN", "atraso-por-producto-ola.svg": "GRAFICO"}
    for name, label in hash_names.items():
        results[PFX + f"G-{label}-SHA256"] = hashlib.sha256(artifacts[name]).hexdigest()
    codes = {"tarjeta_credito": "TDC", "credito_hipotecario": "HIP", "credito_personal": "PER", "credito_nomina": "NOM", "credito_automotriz": "AUT"}
    for product, short in codes.items():
        for name, label in (("atraso", "ATRASO"), ("imposibilidad", "IMPOSIBILIDAD"), ("dano_combinado", "DANO")):
            stats = lookup[(product, 2024, name)]
            results[PFX + f"2024-{short}-{label}-P"] = stats["estimacion"]
        results[PFX + f"2024-{short}-DANO-N-VALIDO"] = lookup[(product, 2024, "dano_combinado")]["n_valido"]
    return results, artifacts


def medir(inputs, contrato):
    del contrato
    results, _ = calculate(inputs[INPUT_ID]["ruta_absoluta"])
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/GEN2_N34_PRODUCTO_DANO/banxico_satisfaccion_usuarios_2019_2024.xlsx"))
    parser.add_argument("--out", type=Path, default=Path("data/banxico-producto-dano-medicion"))
    args = parser.parse_args()
    results, artifacts = calculate(args.input)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, payload in artifacts.items():
        (args.out / name).write_bytes(payload)
    print(f"BANXICO-MEDICION-OK filas={results[PFX + 'G-N-FILAS']} estimandos={results[PFX + 'G-N-FILAS-ESTIMANDOS']} conjunta={results[PFX + 'G-N-FILAS-CONJUNTA']} costo2024={results[PFX + 'G-N-FILAS-COSTO-DANO-2024']}")


if __name__ == "__main__":
    main()

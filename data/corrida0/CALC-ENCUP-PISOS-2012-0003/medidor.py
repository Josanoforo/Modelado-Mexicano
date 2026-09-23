"""Distribuciones descriptivas ENCUP 2012, sin inferencia de diseño."""
from __future__ import annotations

import json
import pandas as pd

PID = "encup_2012_base_datos_xlsx"
QUESTIONS = {
    "interes_politica": ("P37", (1, 2, 3), (1,)),
    "eficacia_influencia": ("P51_2", (1, 2, 3), (1,)),
    "confianza_ife": ("P30_15", tuple(range(11)), (8, 9, 10)),
    "confianza_vecinos": ("P30_10", tuple(range(11)), (8, 9, 10)),
}


def summarize(values, valid, selected):
    labels = {"Mucho": 1, "Poco": 2, "Nada": 3}
    codes = pd.to_numeric(values.replace(labels), errors="coerce")
    freq = {str(c): int((codes == c).sum()) for c in valid}
    n = sum(freq.values())
    k = sum(freq[str(c)] for c in selected)
    return {"n_validos": n, "n_seleccionados": k,
            "proporcion": k / n if n >= 30 else None,
            "estado": "ESTIMADA" if n >= 30 else "NO-ESTIMABLE",
            "categorias": freq,
            "n_sin_respuesta_sustantiva": int(len(codes) - n)}


def medir(inputs, contrato):
    path = inputs[PID]["ruta_absoluta"]
    data = pd.read_excel(path, sheet_name="BaseDatos_ENCUP_2012_Final")
    # El XLSX usa el código seguido de punto y texto completo del reactivo.
    columns = {}
    for name, _, _ in QUESTIONS.values():
        hits = [c for c in data.columns if str(c).startswith(name + ". ")]
        if len(hits) != 1:
            raise ValueError(f"reactivo ENCUP no único: {name}, n={len(hits)}")
        columns[name] = hits[0]
    table = {key: summarize(data[columns[name]], valid, selected)
             for key, (name, valid, selected) in QUESTIONS.items()}
    return {"RESULT-ENCUP-PISOS-2012-FILAS": int(len(data)),
            "RESULT-ENCUP-PISOS-2012-TABLA": json.dumps(
                table, ensure_ascii=False, sort_keys=True,
                separators=(",", ":"), allow_nan=False)}

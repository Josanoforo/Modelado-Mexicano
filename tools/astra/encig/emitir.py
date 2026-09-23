"""Emisión prospectiva ENCIG: sólo agregados históricos y marginales publicados.

No importa lectores de microdato ni abre rutas arbitrarias. La interfaz es la
del runner corrida0: medir(inputs, contrato) -> RESULT.
"""
from __future__ import annotations

import json
import math
import re


HISTORY = {
    "historico_2021": (2021, "CALC-ENCIG2021-CRUCES-HISTORICOS-0003"),
    "historico_2023": (2023, "CALC-ENCIG2023-CRUCES-HISTORICOS-0002"),
}
ALLOWED = set(HISTORY) | {"marginales_publicos_2025"}
AGES = ("18-29", "30-44", "45-59", "60-96")
SCHOOL = ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR")
SEX = ("1", "2")


def _guard(inputs):
    if set(inputs) != ALLOWED:
        raise ValueError("lista de entradas distinta de la lista congelada")
    for name, item in inputs.items():
        path = str(item.get("ruta_absoluta", "")).lower()
        expected = ("tramite-ola5-propuesta-v0.yaml" if name == "marginales_publicos_2025"
                    else f"{HISTORY[name][1].lower()}/resultados.json")
        if not path.endswith(expected):
            raise ValueError(f"ruta no autorizada para {name}")
        if "bytes" not in item:
            raise ValueError(f"faltan bytes verificados para {name}")


def _published(text):
    # Extracción limitada a los dos bloques nombrados, no a los demás R del YAML.
    begin = "  - id: tramite.gobierno_digital.util_sin_coercion_encig2025\n"
    end = "  - id: tramite.gobierno_digital.util_sin_coercion_ejes_encig2025\n"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError("bloques publicados no únicos")
    base = text.split(begin, 1)[1].split("\n  - id:", 1)[0]
    match = re.search(r"conducta: adopta_canal_digital_encig2025, p: ([0-9.]+)", base)
    if not match:
        raise ValueError("nacional publicado ausente")
    national = float(match.group(1))
    axes = text.split(end, 1)[1].split("\n  - id:", 1)[0]
    blocks = re.split(r"\n      - eje: (sexo|edad|escolaridad)\n", axes)
    result = {}
    for i in range(1, len(blocks), 2):
        axis, body = blocks[i], blocks[i + 1]
        values = re.findall(r'\{celda: "([^"]+)", p: ([0-9.]+),', body)
        if axis == "sexo":
            result[axis] = {label[0]: float(p) for label, p in values}
        elif axis == "edad":
            result[axis] = {("60-96" if label == "60+" else label): float(p)
                            for label, p in values}
        else:
            result[axis] = {label.upper().replace(" ", "-"): float(p)
                            for label, p in values}
    if (set(result) != {"sexo", "edad", "escolaridad"}
            or set(result["sexo"]) != set(SEX)
            or set(result["edad"]) != set(AGES)
            or set(result["escolaridad"]) != set(SCHOOL)):
        raise ValueError("rejilla marginal incompleta")
    for value in [national, *[v for axis in result.values() for v in axis.values()]]:
        if not 0 < value < 1:
            raise ValueError("marginal en frontera")
    return national, result


def _logit(p):
    return math.log(p / (1 - p))


def _expit(x):
    return 1 / (1 + math.exp(-x))


def _history(item, year, axis, sex, other):
    data = json.loads(item["bytes"])["resultados"]
    root = f"RESULT-ENCIG{year}-CRUCES-HISTORICOS-SEXO-{axis}-{sex}-{other}-"
    if data.get(root + "CAUSA") != "OK" or data.get(root + "B-VALIDAS") != 10000:
        raise ValueError(f"residuo histórico no estimable: {root}")
    delta, se = data.get(root + "DELTA"), data.get(root + "DELTA-EE")
    if not isinstance(delta, (int, float)) or not isinstance(se, (int, float)):
        raise ValueError(f"residuo histórico incompleto: {root}")
    if not math.isfinite(delta) or not math.isfinite(se) or se <= 0:
        raise ValueError(f"residuo histórico inválido: {root}")
    return delta, se


def medir(inputs, contrato):
    _guard(inputs)
    par = contrato["parametros"]
    cross = par["cruce"]
    if cross not in ("EDADXSEXO", "ESCOLARIDADXSEXO"):
        raise ValueError("cruce no autorizado")
    tau, omega = float(par["tau"]), float(par["omega"])
    if (tau, omega) != (0.15, 0.10):
        raise ValueError("hiperparámetros distintos de los congelados")
    if par.get("nivel") != 0.95:
        raise ValueError("nivel no congelado")
    national, marginal = _published(inputs["marginales_publicos_2025"]["bytes"].decode("utf-8"))
    axis = "edad" if cross == "EDADXSEXO" else "escolaridad"
    other_categories = AGES if axis == "edad" else SCHOOL
    hist_axis = "EDAD" if axis == "edad" else "ESCOLARIDAD"
    out = {}
    for sex in SEX:
        for other in other_categories:
            observations = [_history(inputs[name], year, hist_axis, sex, other)
                            for name, (year, _) in HISTORY.items()]
            # δ_t = θ_c + u_t + e_t; θ_c~N(0,tau²), u_t~N(0,omega²),
            # e_t~N(0,se_t²). u_2025 independiente; 2025 marginal fijo.
            precisions = [1 / (se * se + omega * omega) for _, se in observations]
            variance = 1 / (1 / (tau * tau) + sum(precisions))
            mean = variance * sum(w * d for w, (d, _) in zip(precisions, observations))
            predictive_sd = math.sqrt(variance + omega * omega)
            base = _logit(marginal["sexo"][sex]) + _logit(marginal[axis][other]) - _logit(national)
            ident = f"RESULT-ASTRA-ENCIG-{cross}-{other}-{sex}"
            out[ident + "-P"] = _expit(base + mean)
            out[ident + "-IC-LO"] = _expit(base + mean - 1.959963984540054 * predictive_sd)
            out[ident + "-IC-HI"] = _expit(base + mean + 1.959963984540054 * predictive_sd)
            out[ident + "-NIVEL"] = 0.95
            out[ident + "-TIPO"] = "PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS"
    return out

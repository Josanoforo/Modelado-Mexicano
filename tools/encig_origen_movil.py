#!/usr/bin/env python3
"""Validación de origen móvil de cuatro pisos mecánicos sobre la serie ENCIG.

ACTO GEN2-ENCIG-SERIE-Y-TENDENCIA-1 (21/sep/2026), pieza P3. Aritmética
entre sellados: no abre microdato. Cada ola se predice SOLO con las
anteriores, por celda (nacional + 10 marginales), en escala logit, con cuatro
pisos que no tienen ningún parámetro que alguien elija:

  PERSISTENCIA   L̂_k = L_{k-1}                          (IC: el sellado de k-1, verbatim)
  TENDENCIA-2    recta por (y_{k-2}, y_{k-1}) extrapolada a y_k
  TENDENCIA-3    mínimos cuadrados sobre las 3 olas anteriores
  TENDENCIA-SERIE mínimos cuadrados sobre TODAS las olas anteriores (>= 2)

Incertidumbre: ee_i en logit desde el IC95 sellado de cada ola
(ee = (logit(hi) - logit(lo)) / (2 z)), olas independientes, y el piso de
tendencia es una combinación lineal fija de logits: var = sum w_i^2 ee_i^2.
Misma aproximación que CALC-PISO-PERSISTENCIA-ERROR-0001.

El dictamen se calcula con reglas escritas antes de ver la serie (spec
ENCIG-ORIGEN-MOVIL-spec-v1_0.md §4) y sale como texto: una de cuatro palabras.

El primer resultado que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import json
import math

import yaml

Z95 = 1.959964
PISOS = ("PERSISTENCIA", "TENDENCIA-2", "TENDENCIA-3", "TENDENCIA-SERIE")
MINIMO_OLAS = {"PERSISTENCIA": 1, "TENDENCIA-2": 2, "TENDENCIA-3": 3, "TENDENCIA-SERIE": 2}
CELDAS = (("ALL", "ALL"), ("SEXO", "1"), ("SEXO", "2"),
          ("EDAD", "18-29"), ("EDAD", "30-44"), ("EDAD", "45-59"), ("EDAD", "60-MAS"),
          ("ESCOLARIDAD", "HASTA-PRIMARIA"), ("ESCOLARIDAD", "SECUNDARIA"),
          ("ESCOLARIDAD", "MEDIA-SUPERIOR"), ("ESCOLARIDAD", "SUPERIOR"))
# Nombres de celda en milpa/tramite-ola5-propuesta-v0.yaml (ola 2025 sellada).
CELDA_YAML = {("SEXO", "1"): ("sexo", "1 Hombre"), ("SEXO", "2"): ("sexo", "2 Mujer"),
              ("EDAD", "18-29"): ("edad", "18-29"), ("EDAD", "30-44"): ("edad", "30-44"),
              ("EDAD", "45-59"): ("edad", "45-59"), ("EDAD", "60-MAS"): ("edad", "60+"),
              ("ESCOLARIDAD", "HASTA-PRIMARIA"): ("escolaridad", "hasta primaria"),
              ("ESCOLARIDAD", "SECUNDARIA"): ("escolaridad", "secundaria"),
              ("ESCOLARIDAD", "MEDIA-SUPERIOR"): ("escolaridad", "media superior"),
              ("ESCOLARIDAD", "SUPERIOR"): ("escolaridad", "superior")}
ID_NACIONAL_2025 = "tramite.gobierno_digital.util_sin_coercion_encig2025"
ID_EJES_2025 = "tramite.gobierno_digital.util_sin_coercion_ejes_encig2025"


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def _expit(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _ee_logit(lo: float, hi: float) -> float:
    return (_logit(hi) - _logit(lo)) / (2.0 * Z95)


def pesos(piso: str, anios: list[float], objetivo: float) -> list[float] | None:
    """Pesos w_i tales que L̂ = sum w_i L_i sobre las olas anteriores `anios`
    (ordenadas). None si el piso no está definido con esas olas."""
    n = len(anios)
    if n < MINIMO_OLAS[piso]:
        return None
    if piso == "PERSISTENCIA":
        return [0.0] * (n - 1) + [1.0]
    if piso == "TENDENCIA-2":
        usados = anios[-2:]
    elif piso == "TENDENCIA-3":
        usados = anios[-3:]
    else:
        usados = anios
    k = len(usados)
    xbar = sum(usados) / k
    sxx = sum((x - xbar) ** 2 for x in usados)
    if sxx <= 0:
        return None
    # Predicción OLS en `objetivo`: w_i = 1/k + (objetivo - xbar)(x_i - xbar)/sxx.
    w_usados = [1.0 / k + (objetivo - xbar) * (x - xbar) / sxx for x in usados]
    return [0.0] * (n - k) + w_usados


def predice(piso: str, anios: list[float], logits: list[float], ees: list[float],
            objetivo: float, ic_sellado: tuple[float, float] | None) -> dict | None:
    w = pesos(piso, anios, objetivo)
    if w is None:
        return None
    L = sum(wi * li for wi, li in zip(w, logits))
    if piso == "PERSISTENCIA" and ic_sellado is not None:
        lo, hi = ic_sellado
    else:
        ee = math.sqrt(sum((wi * ei) ** 2 for wi, ei in zip(w, ees)))
        lo, hi = _expit(L - Z95 * ee), _expit(L + Z95 * ee)
    return {"p": _expit(L), "lo": lo, "hi": hi}


def _serie_desde_inputs(inputs: dict, contrato: dict) -> dict:
    """{(eje, cat): [(anio, p, lo, hi), ...]} ordenado por año, con las olas
    2015-2023 desde los CALC sellados y 2025 desde el YAML sellado."""
    olas = contrato["parametros"]["olas_serie"]           # p.ej. ["2015", ..., "2023"]
    serie = {c: [] for c in CELDAS}
    for ola in olas:
        r = json.loads(inputs[f"CALC-ENCIG-SERIE-CANAL-{ola}"]["bytes"].decode("utf-8"))
        r = r.get("resultados", r)
        for eje, cat in CELDAS:
            b = f"RESULT-ENCIG-SERIE-{ola}-DIGITAL-{eje}-{cat}"
            serie[(eje, cat)].append((float(ola), r[b + "-P"], r[b + "-IC-LO"], r[b + "-IC-HI"]))
    y = yaml.safe_load(inputs["TRAMITE-OLA5-PROPUESTA"]["bytes"].decode("utf-8"))
    reglas = {x["id"]: x for x in y["reglas_propuestas"]}
    nac = reglas[ID_NACIONAL_2025]
    p_nac = [e["p"] for e in nac["entonces"] if e["conducta"] == "adopta_canal_digital_encig2025"][0]
    serie[("ALL", "ALL")].append((2025.0, float(p_nac), float(nac["ic95"][0]), float(nac["ic95"][1])))
    ejes = {e["eje"]: {c["celda"]: c for c in e["celdas"]} for e in reglas[ID_EJES_2025]["ejes"]}
    for key, (eje, celda) in CELDA_YAML.items():
        c = ejes[eje][celda]
        serie[key].append((2025.0, float(c["p"]), float(c["ic95"][0]), float(c["ic95"][1])))
    return serie


def origen_movil(serie: dict, params: dict) -> dict:
    """Corazón determinista, separado de la lectura de inputs para poder
    probarlo con series sintéticas."""
    out = {}
    anios_all = sorted({a for pts in serie.values() for a, *_ in pts})
    comunes = [float(a) for a in params["olas_comunes"]]
    umbral = float(params["delta_mae_material_pp"])
    err = {piso: [] for piso in PISOS}            # (anio, celda, abs_err)
    cob = {piso: [] for piso in PISOS}
    for (eje, cat), pts in serie.items():
        # Un punto sin estimación (P nulo, soporte vacío) no existe para la
        # serie de su celda: ni se predice ni sirve para predecir.
        pts = sorted(p for p in pts if p[1] is not None and p[2] is not None and p[3] is not None)
        tag = f"{eje}-{cat}"
        for anio in anios_all[1:]:
            prev = [p for p in pts if p[0] < anio]
            actual = [p for p in pts if p[0] == anio]
            anios = [p[0] for p in prev]
            logits = [_logit(p[1]) for p in prev]
            ees = [_ee_logit(p[2], p[3]) for p in prev]
            for piso in PISOS:
                base = f"RESULT-ENCIG-OM-{int(anio)}-{tag}-{piso}"
                pr = None
                if actual and prev:
                    R = actual[0][1]
                    pr = predice(piso, anios, logits, ees, anio, (prev[-1][2], prev[-1][3]))
                if pr is None:
                    out[base + "-P"] = None; out[base + "-ERROR-PP"] = None
                    out[base + "-CUBRE"] = "NO-DEFINIDO"
                    continue
                e = 100.0 * (pr["p"] - R)
                cubre = "SI" if pr["lo"] <= R <= pr["hi"] else "NO"
                out[base + "-P"] = pr["p"]; out[base + "-ERROR-PP"] = e
                out[base + "-CUBRE"] = cubre
                err[piso].append((anio, tag, abs(e)))
                cob[piso].append((anio, tag, cubre == "SI"))
    mae_comun = {}
    for piso in PISOS:
        todos = [x[2] for x in err[piso]]
        com = [x[2] for x in err[piso] if x[0] in comunes]
        out[f"RESULT-ENCIG-OM-{piso}-MAE-TODAS-PP"] = sum(todos) / len(todos) if todos else None
        out[f"RESULT-ENCIG-OM-{piso}-N-PREDICCIONES"] = len(todos)
        out[f"RESULT-ENCIG-OM-{piso}-MAE-COMUN-PP"] = sum(com) / len(com) if com else None
        out[f"RESULT-ENCIG-OM-{piso}-N-COMUN"] = len(com)
        cobs = [x[2] for x in cob[piso] if x[0] in comunes]
        out[f"RESULT-ENCIG-OM-{piso}-COBERTURA-COMUN"] = (sum(cobs) / len(cobs)) if cobs else None
        mae_comun[piso] = out[f"RESULT-ENCIG-OM-{piso}-MAE-COMUN-PP"]
        for anio in anios_all[1:]:
            xs = [x[2] for x in err[piso] if x[0] == anio]
            out[f"RESULT-ENCIG-OM-{piso}-MAE-{int(anio)}-PP"] = sum(xs) / len(xs) if xs else None
        nac = [x[2] for x in err[piso] if x[1] == "ALL-ALL" and x[0] in comunes]
        out[f"RESULT-ENCIG-OM-{piso}-MAE-NACIONAL-COMUN-PP"] = sum(nac) / len(nac) if nac else None
    # Pares (celda, ola común): ¿cuántas veces cada tendencia yerra menos que persistencia?
    per = {(a, t): e for a, t, e in err["PERSISTENCIA"]}
    for piso in PISOS[1:]:
        gana = [1 if e < per[(a, t)] else 0 for a, t, e in err[piso] if a in comunes and (a, t) in per]
        out[f"RESULT-ENCIG-OM-{piso}-VENCE-PERSISTENCIA-COMUN"] = int(sum(gana))
        out[f"RESULT-ENCIG-OM-{piso}-DELTA-MAE-COMUN-PP"] = (
            (mae_comun["PERSISTENCIA"] - mae_comun[piso])
            if mae_comun[piso] is not None and mae_comun["PERSISTENCIA"] is not None else None)
    # Serie nacional: ¿sube sostenida?
    nac = sorted(serie[("ALL", "ALL")])
    dif = [(nac[i][1] - nac[i - 1][1]) for i in range(1, len(nac))]
    traslapa = [nac[i][2] <= nac[i - 1][3] and nac[i - 1][2] <= nac[i][3] for i in range(1, len(nac))]
    positivos = sum(1 for d in dif if d > 0)
    negativos_significativos = sum(1 for d, t in zip(dif, traslapa) if d <= 0 and not t)
    out["RESULT-ENCIG-OM-NACIONAL-N-OLAS"] = len(nac)
    out["RESULT-ENCIG-OM-NACIONAL-PARES-POSITIVOS"] = int(positivos)
    out["RESULT-ENCIG-OM-NACIONAL-PARES-NEGATIVOS-SIGNIFICATIVOS"] = int(negativos_significativos)
    out["RESULT-ENCIG-OM-NACIONAL-CAMBIO-TOTAL-PP"] = 100.0 * (nac[-1][1] - nac[0][1]) if nac else None
    out["RESULT-ENCIG-OM-NACIONAL-SALTO-MAXIMO-PP"] = 100.0 * max(dif) if dif else None
    out["RESULT-ENCIG-OM-NACIONAL-SALTO-MAXIMO-OLA"] = (
        str(int(nac[1 + max(range(len(dif)), key=lambda i: dif[i])][0])) if dif else "NINGUNA")
    n_pares = len(dif)
    sostenida = (n_pares >= 2 and positivos >= n_pares - 1 and negativos_significativos == 0
                 and (nac[-1][1] - nac[0][1]) > 0)
    out["RESULT-ENCIG-OM-NACIONAL-SUBE-SOSTENIDA"] = "SI" if sostenida else "NO"
    mejor = None
    for piso in PISOS[1:]:
        d = out[f"RESULT-ENCIG-OM-{piso}-DELTA-MAE-COMUN-PP"]
        if d is not None and (mejor is None or d > mejor[1]):
            mejor = (piso, d)
    material = mejor is not None and mejor[1] >= umbral
    out["RESULT-ENCIG-OM-MEJOR-TENDENCIA"] = mejor[0] if mejor else "NINGUNA"
    out["RESULT-ENCIG-OM-TENDENCIA-ERRA-MATERIALMENTE-MENOS"] = "SI" if material else "NO"
    n_comp = int(params["olas_comparables"])
    cambio = params.get("cambio_instrumento_en_ola")
    if n_comp < 3:
        dictamen = "NO-DECIDIBLE"
    elif cambio not in (None, "", "NINGUNA"):
        dictamen = "CAMBIO-DE-INSTRUMENTO"
    elif sostenida and material:
        dictamen = "TENDENCIA"
    else:
        dictamen = "SALTO-SIN-EXPLICAR"
    out["RESULT-ENCIG-OM-DICTAMEN"] = dictamen
    return out


def ids_resultado(olas_serie: list[str], anio_final: str = "2025") -> list[dict]:
    anios = [int(o) for o in olas_serie] + [int(anio_final)]
    out = []
    for anio in anios[1:]:
        for eje, cat in CELDAS:
            for piso in PISOS:
                b = f"RESULT-ENCIG-OM-{anio}-{eje}-{cat}-{piso}"
                out += [{"id": b + "-P", "tipo": "proporcion", "unidad": "predicción del piso [0,1]", "permite_no_estimable": True},
                        {"id": b + "-ERROR-PP", "tipo": "flotante", "unidad": "puntos porcentuales (piso menos R)", "permite_no_estimable": True},
                        {"id": b + "-CUBRE", "tipo": "texto", "unidad": "SI | NO | NO-DEFINIDO (R dentro del IC95 del piso)"}]
    for piso in PISOS:
        out += [{"id": f"RESULT-ENCIG-OM-{piso}-MAE-TODAS-PP", "tipo": "flotante", "unidad": "MAE pp sobre todas las predicciones definidas", "permite_no_estimable": True},
                {"id": f"RESULT-ENCIG-OM-{piso}-N-PREDICCIONES", "tipo": "entero", "unidad": "predicciones definidas"},
                {"id": f"RESULT-ENCIG-OM-{piso}-MAE-COMUN-PP", "tipo": "flotante", "unidad": "MAE pp sobre las olas comunes a los cuatro pisos", "permite_no_estimable": True},
                {"id": f"RESULT-ENCIG-OM-{piso}-N-COMUN", "tipo": "entero", "unidad": "predicciones en olas comunes"},
                {"id": f"RESULT-ENCIG-OM-{piso}-COBERTURA-COMUN", "tipo": "proporcion", "unidad": "fracción de R dentro del IC95 del piso, olas comunes", "permite_no_estimable": True},
                {"id": f"RESULT-ENCIG-OM-{piso}-MAE-NACIONAL-COMUN-PP", "tipo": "flotante", "unidad": "MAE pp de la celda nacional, olas comunes", "permite_no_estimable": True}]
        for anio in anios[1:]:
            out.append({"id": f"RESULT-ENCIG-OM-{piso}-MAE-{anio}-PP", "tipo": "flotante", "unidad": "MAE pp de la ola, 11 celdas", "permite_no_estimable": True})
    for piso in PISOS[1:]:
        out += [{"id": f"RESULT-ENCIG-OM-{piso}-VENCE-PERSISTENCIA-COMUN", "tipo": "entero", "unidad": "pares (celda, ola común) con |error| menor que persistencia"},
                {"id": f"RESULT-ENCIG-OM-{piso}-DELTA-MAE-COMUN-PP", "tipo": "flotante", "unidad": "MAE persistencia menos MAE del piso, olas comunes, pp", "permite_no_estimable": True}]
    out += [{"id": "RESULT-ENCIG-OM-NACIONAL-N-OLAS", "tipo": "entero", "unidad": "olas en la serie nacional"},
            {"id": "RESULT-ENCIG-OM-NACIONAL-PARES-POSITIVOS", "tipo": "entero", "unidad": "pares consecutivos con incremento > 0"},
            {"id": "RESULT-ENCIG-OM-NACIONAL-PARES-NEGATIVOS-SIGNIFICATIVOS", "tipo": "entero", "unidad": "pares con decremento y IC95 sin traslape"},
            {"id": "RESULT-ENCIG-OM-NACIONAL-CAMBIO-TOTAL-PP", "tipo": "flotante", "unidad": "pp, última menos primera ola", "permite_no_estimable": True},
            {"id": "RESULT-ENCIG-OM-NACIONAL-SALTO-MAXIMO-PP", "tipo": "flotante", "unidad": "pp, mayor incremento entre olas consecutivas", "permite_no_estimable": True},
            {"id": "RESULT-ENCIG-OM-NACIONAL-SALTO-MAXIMO-OLA", "tipo": "texto", "unidad": "ola destino del mayor incremento"},
            {"id": "RESULT-ENCIG-OM-NACIONAL-SUBE-SOSTENIDA", "tipo": "texto", "unidad": "SI | NO (spec §4.1)"},
            {"id": "RESULT-ENCIG-OM-MEJOR-TENDENCIA", "tipo": "texto", "unidad": "piso de tendencia con mayor reducción de MAE común"},
            {"id": "RESULT-ENCIG-OM-TENDENCIA-ERRA-MATERIALMENTE-MENOS", "tipo": "texto", "unidad": "SI | NO (spec §4.2)"},
            {"id": "RESULT-ENCIG-OM-DICTAMEN", "tipo": "texto", "unidad": "CAMBIO-DE-INSTRUMENTO | TENDENCIA | SALTO-SIN-EXPLICAR | NO-DECIDIBLE"}]
    return out


def medir(inputs: dict, contrato: dict) -> dict:
    serie = _serie_desde_inputs(inputs, contrato)
    return origen_movil(serie, contrato["parametros"])

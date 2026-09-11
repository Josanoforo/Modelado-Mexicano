"""Medidor congelado: canal del ultimo producto entre tenedores fintech, ENIF 2021.

La salida numerica es exclusivamente 2021. ENIF 2024 se abre como control
puntual contra valores ya publicados y solo produce un guardia textual.
"""
from __future__ import annotations

import csv
import io
import math
import zipfile

ID_2021 = "enif2021_csv"
ID_2024 = "enif2024_csv"
MEMBER_2021 = (
    "conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/"
    "conjunto_de_datos_tmodulo_enif_2021.csv"
)
MEMBER_2024 = (
    "conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/"
    "conjunto_de_datos_tmodulo_enif2024.csv"
)
P = "RESULT-ENIF-FINTECH-2021-"
COLS_2021 = ["EDAD", "P5_4_8", "P5_17", "P6_2_8", "P6_7",
             "FAC_ELE", "EST_DIS", "UPM_DIS"]
COLS_2024 = ["P6_2_8", "P6_6", "FAC_PER"]
CATEGORIAS = {
    "CUENTA": {
        "filtro": "P5_4_8",
        "canal": "P5_17",
        "mapa": {
            "1": "SUCURSAL",
            "2": "APP-CELULAR",
            "3": "PAGINA-INTERNET",
            "4": "ESTABLECIMIENTO",
            "5": "PROMOTOR",
            "6": "EMPLEADOR",
            "7": "OTRO",
        },
    },
    "CREDITO": {
        "filtro": "P6_2_8",
        "canal": "P6_7",
        "mapa": {
            "1": "SUCURSAL",
            "2": "APP-CELULAR",
            "3": "PAGINA-INTERNET",
            "4": "ESTABLECIMIENTO",
            "5": "PROMOTOR",
            "6": "OTRO",
        },
    },
}
Z975 = 1.959963985


def _norm(value):
    return str(value).lstrip("\ufeff").lstrip("ï»¿").strip().upper()


def _cod(value):
    return "" if value is None else str(value).strip()


def _peso(value):
    try:
        out = float(str(value).strip().replace(",", ""))
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) and out > 0 else None


def _lee_zip(path, member, columns):
    with zipfile.ZipFile(path) as zf:
        raw = zf.read(member)
    try:
        text, encoding = raw.decode("utf-8-sig"), "utf-8-sig"
    except UnicodeDecodeError:
        text, encoding = raw.decode("latin-1"), "latin-1"
    reader = csv.reader(io.StringIO(text, newline=""))
    header = [_norm(x) for x in next(reader)]
    missing = [x for x in columns if x not in header]
    if missing:
        return [], missing, encoding, len(header)
    idx = {x: header.index(x) for x in columns}
    rows = []
    for row in reader:
        if row:
            rows.append({x: row[idx[x]] if idx[x] < len(row) else ""
                         for x in columns})
    return rows, [], encoding, len(header)


def _prop_dominio(rows, domain, outcome):
    """Proporcion de dominio y varianza linealizada usando la muestra completa."""
    domain_rows = [(row, weight) for row, weight in rows
                   if weight is not None and domain(row)]
    denominator = sum(weight for _, weight in domain_rows)
    if denominator <= 0:
        return None
    numerator = sum(weight for row, weight in domain_rows if outcome(row))
    p_hat = numerator / denominator

    psu_z = {}
    strata_psu = {}
    n_domain_without_design = 0
    for row, weight in rows:
        if weight is None:
            continue
        h, u = _cod(row.get("EST_DIS")), _cod(row.get("UPM_DIS"))
        in_domain = domain(row)
        if in_domain and (not h or not u):
            n_domain_without_design += 1
        if not h or not u:
            continue
        key = (h, u)
        z = (weight * ((1.0 if outcome(row) else 0.0) - p_hat) /
             denominator) if in_domain else 0.0
        psu_z[key] = psu_z.get(key, 0.0) + z
        strata_psu.setdefault(h, set()).add(u)

    variance = 0.0
    singletons = 0
    for h, psus in strata_psu.items():
        values = [psu_z.get((h, u), 0.0) for u in psus]
        m_h = len(values)
        if m_h < 2:
            singletons += 1
            continue
        mean = sum(values) / m_h
        variance += (m_h / (m_h - 1)) * sum((x - mean) ** 2 for x in values)
    se = math.sqrt(max(0.0, variance))
    return {
        "p": p_hat,
        "se": se,
        "lo": max(0.0, p_hat - Z975 * se),
        "hi": min(1.0, p_hat + Z975 * se),
        "n_den": len(domain_rows),
        "mass_den": denominator,
        "n_num": sum(1 for row, _ in domain_rows if outcome(row)),
        "mass_num": numerator,
        "n_strata": len(strata_psu),
        "n_psu": len(psu_z),
        "n_singleton": singletons,
        "n_domain_without_design": n_domain_without_design,
    }


def _resume_familia(rows, family, put):
    cfg = CATEGORIAS[family]
    filter_col, channel_col = cfg["filtro"], cfg["canal"]
    valid_channels = set(cfg["mapa"])
    valid_weight_rows = [(row, _peso(row["FAC_ELE"])) for row in rows]
    filter_yes = [(row, w) for row, w in valid_weight_rows
                  if w is not None and _cod(row[filter_col]) == "1"]
    filter_no = [(row, w) for row, w in valid_weight_rows
                 if w is not None and _cod(row[filter_col]) == "2"]
    filter_missing = [(row, w) for row, w in valid_weight_rows
                      if w is not None and _cod(row[filter_col]) not in {"1", "2"}]
    channel_valid = [(row, w) for row, w in filter_yes
                     if _cod(row[channel_col]) in valid_channels]
    channel_ns = [(row, w) for row, w in filter_yes
                  if _cod(row[channel_col]) == "9"]
    channel_blank = [(row, w) for row, w in filter_yes
                     if _cod(row[channel_col]) in {"", "b", "B"}]
    channel_invalid = [(row, w) for row, w in filter_yes
                       if _cod(row[channel_col]) not in valid_channels | {"9", "", "b", "B"}]

    def count_mass(label, values):
        put(f"{family}-{label}-N", len(values))
        put(f"{family}-{label}-MASA", round(sum(w for _, w in values), 6))

    count_mass("FILTRO-SI", filter_yes)
    count_mass("FILTRO-NO", filter_no)
    count_mass("FILTRO-FALTANTE", filter_missing)
    count_mass("CANAL-VALIDO", channel_valid)
    count_mass("CANAL-NS", channel_ns)
    count_mass("CANAL-BLANCO", channel_blank)
    count_mass("CANAL-INVALIDO", channel_invalid)
    put(f"{family}-PESO-INVALIDO-N", sum(_peso(row["FAC_ELE"]) is None for row in rows))

    valid_weight_rows = [(row, w) for row, w in valid_weight_rows if w is not None]
    domain = lambda row: (_cod(row[filter_col]) == "1" and
                          _cod(row[channel_col]) in valid_channels)
    sum_p = 0.0
    design_profile = None
    for code, label in cfg["mapa"].items():
        estimate = _prop_dominio(
            valid_weight_rows,
            domain,
            lambda row, code=code: _cod(row[channel_col]) == code,
        )
        if estimate is None:
            raise ValueError(f"NO-ESTIMABLE-UNIVERSO-VACIO:{family}")
        sum_p += estimate["p"]
        put(f"{family}-CANAL-{label}-N", estimate["n_num"])
        put(f"{family}-CANAL-{label}-MASA", round(estimate["mass_num"], 6))
        put(f"{family}-CANAL-{label}-P", round(estimate["p"], 12))
        put(f"{family}-CANAL-{label}-EE", round(estimate["se"], 12))
        put(f"{family}-CANAL-{label}-IC-LO", round(estimate["lo"], 12))
        put(f"{family}-CANAL-{label}-IC-HI", round(estimate["hi"], 12))
        profile = (estimate["n_strata"], estimate["n_psu"],
                   estimate["n_singleton"], estimate["n_domain_without_design"])
        if design_profile is None:
            design_profile = profile
        elif design_profile != profile:
            raise ValueError(f"PERFIL-DISENO-INCONSISTENTE:{family}")
    if abs(sum_p - 1.0) > 1e-10:
        raise ValueError(f"CATEGORIAS-NO-CIERRAN:{family}:{sum_p}")
    put(f"{family}-SUMA-P", round(sum_p, 12))
    n_strata, n_psu, n_singleton, n_without = design_profile
    put(f"{family}-N-ESTRATOS", n_strata)
    put(f"{family}-N-UPM", n_psu)
    put(f"{family}-N-ESTRATOS-UPM-UNICA", n_singleton)
    put(f"{family}-N-DOMINIO-SIN-DISENO", n_without)
    method = ("ULTIMATE-CLUSTER-CON-ESTRATOS-UPM-UNICA" if n_singleton
              else "ULTIMATE-CLUSTER-LINEALIZADO")
    put(f"{family}-METODO-IC", method)


def _control_2024(rows):
    valid = []
    for row in rows:
        w = _peso(row["FAC_PER"])
        if (w is not None and _cod(row["P6_2_8"]) == "1" and
                _cod(row["P6_6"]) in set("123456")):
            valid.append((row, w))
    numerator = [(row, w) for row, w in valid if _cod(row["P6_6"]) == "2"]
    mass = sum(w for _, w in valid)
    p_app = sum(w for _, w in numerator) / mass if mass else None
    observed = (len(valid), int(round(mass)), None if p_app is None else round(p_app, 3))
    expected = (200, 1178431, 0.575)
    if observed != expected:
        raise ValueError(f"CONTROL-2024-NO-REPRODUCE:{observed!r}")
    return "COINCIDE:n=200;masa=1178431;p_app_3d=0.575"


def medir(inputs, contrato):
    out = {}

    def put(suffix, value):
        out[P + suffix] = value

    rows21, missing21, encoding21, width21 = _lee_zip(
        inputs[ID_2021]["ruta_absoluta"], MEMBER_2021, COLS_2021)
    put("G-N-FILAS", len(rows21))
    put("G-N-COLUMNAS", width21)
    put("G-ENCODING", encoding21)
    put("G-COLUMNAS-AUSENTES", ";".join(missing21) if missing21 else "NINGUNA")
    if missing21:
        raise ValueError("COLUMNAS-AUSENTES-2021:" + ";".join(missing21))
    ages = [int(_cod(row["EDAD"])) for row in rows21 if _cod(row["EDAD"]).isdigit()]
    put("G-EDAD-MIN", min(ages) if ages else None)
    put("G-EDAD-MAX", max(ages) if ages else None)
    put("G-POBLACION-18MAS", "SI" if ages and min(ages) >= 18 else "NO")
    if not ages or min(ages) < 18:
        raise ValueError("POBLACION-2021-NO-18MAS")

    _resume_familia(rows21, "CUENTA", put)
    _resume_familia(rows21, "CREDITO", put)

    rows24, missing24, encoding24, width24 = _lee_zip(
        inputs[ID_2024]["ruta_absoluta"], MEMBER_2024, COLS_2024)
    put("G-CONTROL-2024-ARCHIVO", f"filas={len(rows24)};columnas={width24};encoding={encoding24}")
    put("G-CONTROL-2024-COLUMNAS-AUSENTES", ";".join(missing24) if missing24 else "NINGUNA")
    if missing24:
        raise ValueError("COLUMNAS-AUSENTES-2024:" + ";".join(missing24))
    put("G-CONTROL-2024-CREDITO-APP", _control_2024(rows24))
    put("G-OBJETO", "CANAL-ULTIMO-PRODUCTO-ENTRE-TENEDORES-FINTECH;NO-CANAL-FINTECH-EXACTO")
    return out

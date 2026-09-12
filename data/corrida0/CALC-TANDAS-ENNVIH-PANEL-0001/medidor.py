"""Medidor de transiciones descriptivas de participación en tandas, ENNViH.

Interfaz estable: medir(inputs, contrato) -> {"RESULT-...": escalar}.
La identidad entre olas sigue las recetas oficiales documentadas en las guías
ENNViH-2 y ENNViH-3; nunca usa orden de fila ni atributos aproximados.
"""
from __future__ import annotations

import io
import json
import math
import re
import zipfile

import numpy as np
import pandas as pd


PREFIX = "RESULT-TANDAS-PANEL-ENNVIH-"
VALID_OUTCOMES = {1, 3}
ACTIVE_ROSTER_CODES = {1, 4, 6}
AWAY_ROSTER_CODES = {3, 5}
PID10_RE = re.compile(r"^[0-9]{10}$")
PID12_RE = re.compile(r"^[0-9]{6}(?:AP|BP|CP|CH)[0-9]{4}$")


def _read_member(path: str, member: str) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        return pd.read_stata(
            io.BytesIO(zf.read(member)),
            convert_categoricals=False,
            preserve_dtypes=False,
        )


def _integer_text(value, width: int) -> str:
    if pd.isna(value):
        raise ValueError("identificador ausente")
    if isinstance(value, (int, float, np.integer, np.floating)):
        if not float(value).is_integer():
            raise ValueError(f"identificador numerico no entero: {value!r}")
        text = str(int(value))
    else:
        text = str(value).strip()
    if not text.isdigit() or len(text) > width:
        raise ValueError(f"identificador invalido para ancho {width}: {value!r}")
    return text.zfill(width)


def pid_w1(folio, ls) -> str:
    """Receta oficial ENNViH-1: folio %08d + ls %02d."""
    return _integer_text(folio, 8) + _integer_text(ls, 2)


def pid10(value) -> str:
    text = str(value).strip()
    if not PID10_RE.fullmatch(text):
        raise ValueError(f"pid_link ENNViH-2 invalido: {value!r}")
    return text


def pid12(value) -> str:
    text = str(value).strip().replace(" ", "")
    if not PID12_RE.fullmatch(text):
        raise ValueError(f"pid_link ENNViH-3 invalido: {value!r}")
    return text


def pid10_to_pid12(value) -> str:
    """Representa en formato ENNViH-3 un pid_link observado en ENNViH-2.

    Los primeros ocho dígitos del pid10 son el primer folio de registro. Un
    folio acabado en 00 fue abierto en 2002 (AP); los demás fueron abiertos en
    2005 por desdoblamiento (BP). Esta regla está descrita en ambas guías.
    """
    text = pid10(value)
    folio, ls = text[:8], text[8:]
    origin = "AP" if folio.endswith("00") else "BP"
    return folio[:6] + origin + folio[6:] + ls


def _current_key(df: pd.DataFrame, wave: int) -> pd.Series:
    if wave == 1:
        return pd.Series(
            [pid_w1(f, ls) for f, ls in zip(df["folio"], df["ls"])],
            index=df.index,
            dtype="object",
        )
    if wave == 3:
        def folio3(value) -> str:
            text = str(value).strip().replace(" ", "")
            if not re.fullmatch(r"^[0-9]{6}(?:AP|BP|CP|CH)[0-9]{2}$", text):
                raise ValueError(f"folio ENNViH-3 invalido: {value!r}")
            return text
        return (
            df["folio"].map(folio3)
            + df["ls"].map(lambda x: _integer_text(x, 2))
        )
    width = 8
    return (
        df["folio"].map(lambda x: _integer_text(x, width))
        + df["ls"].map(lambda x: _integer_text(x, 2))
    )


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _assert_unique(df: pd.DataFrame, column: str, label: str) -> None:
    if df[column].eq("").any() or df[column].duplicated().any():
        raise ValueError(f"{label}: identidad ausente o duplicada")


def _prepare_initial(cr: pd.DataFrame, port: pd.DataFrame, roster: pd.DataFrame,
                     wave: int) -> tuple[pd.DataFrame, set[str]]:
    cr = cr.copy()
    port = port.copy()
    roster = roster.copy()
    cr["_key"] = _current_key(cr, wave)
    port["_key"] = _current_key(port, wave)
    roster["_key"] = _current_key(roster, wave)
    _assert_unique(cr, "_key", f"ola {wave} CR")
    _assert_unique(port, "_key", f"ola {wave} portada")
    _assert_unique(roster, "_key", f"ola {wave} roster por folio+ls")

    if wave == 1:
        cr["pid"] = cr["_key"]
        roster["pid_persona"] = roster["_key"]
    elif wave == 2:
        cr["pid"] = cr["pid_link"].map(pid10_to_pid12)
        raw = roster["pid_link"].fillna("").astype(str).str.strip()
        blank = raw.eq("")
        # En el microdato, los 1,277 blancos son exclusivamente renglones
        # preimpresos con ls01a=3 en hogares panel terminados en 00. La guía
        # autoriza conservar folio+ls de ese renglón porque el LS no se
        # reutiliza. Sirve para cobertura, nunca para crear una respuesta.
        if not (
            roster.loc[blank, "folio"].astype(str).str.endswith("00").all()
            and _number(roster.loc[blank, "ls01a"]).eq(3).all()
        ):
            raise ValueError("ola 2 roster: pid blanco fuera del caso oficial acreditado")
        pid10_roster = raw.where(~blank, roster["_key"])
        roster["pid_persona"] = pid10_roster.map(pid10_to_pid12)
    else:  # pragma: no cover - no se usa como ola inicial en esta spec
        raise ValueError(f"ola inicial no soportada: {wave}")

    joined = cr.merge(
        port[["_key", "edad"]], on="_key", how="left", validate="one_to_one"
    ).merge(
        roster[["_key", "ls04"]], on="_key", how="left", validate="one_to_one"
    )
    joined["outcome_initial"] = _number(joined["cr04"])
    joined["age_initial"] = _number(joined["edad"])
    joined["sex_initial"] = _number(joined["ls04"])
    return joined, set(roster["pid_persona"])


def _prepare_followup(cr: pd.DataFrame, roster: pd.DataFrame, wave: int):
    cr = cr.copy()
    roster = roster.copy()
    cr["_key"] = _current_key(cr, wave)
    roster["_key"] = _current_key(roster, wave)
    _assert_unique(cr, "_key", f"ola {wave} CR por folio+ls")
    if wave == 2:
        cr["pid"] = cr["pid_link"].map(pid10)
        raw = roster["pid_link"].fillna("").astype(str).str.strip()
        blank = raw.eq("")
        if not (
            roster.loc[blank, "folio"].astype(str).str.endswith("00").all()
            and _number(roster.loc[blank, "ls01a"]).eq(3).all()
        ):
            raise ValueError("ola 2 roster: pid blanco fuera del caso oficial acreditado")
        roster["pid_persona"] = raw.where(~blank, roster["_key"]).map(pid10)
    elif wave == 3:
        cr["pid"] = cr["pid_link"].map(pid12)
        roster["pid_persona"] = roster["pid_link"].map(pid12)
    else:  # pragma: no cover
        raise ValueError(f"ola de seguimiento no soportada: {wave}")
    _assert_unique(cr, "pid", f"ola {wave} CR por pid_link")
    cr["outcome_followup"] = _number(cr["cr04"])
    cr["book_followup"] = True

    summaries = {}
    for key, group in roster.groupby("pid_persona", sort=False):
        statuses = {
            int(v) for v in _number(group["ls01a"]).dropna().tolist()
        }
        alive = {
            int(v) for v in _number(group["ls19d"]).dropna().tolist()
        }
        summaries[key] = {"statuses": statuses, "alive": alive}
    cardinality = {
        "filas_roster": int(len(roster)),
        "personas_roster": int(roster["pid_persona"].nunique()),
        "ids_roster_duplicados": int(
            roster["pid_persona"].value_counts().gt(1).sum()
        ),
        "max_filas_por_persona_roster": int(
            roster["pid_persona"].value_counts().max()
        ),
        "filas_cr": int(len(cr)),
        "personas_cr": int(cr["pid"].nunique()),
    }
    return cr[["pid", "outcome_followup", "book_followup"]], summaries, cardinality


def _followup_state(row, roster_summary: dict[str, dict]) -> str:
    if bool(row.get("book_followup", False)):
        if row["outcome_followup"] in VALID_OUTCOMES:
            return "RESPUESTA-VALIDA"
        return "NO-RESPUESTA-ITEM"
    info = roster_summary.get(row["pid"])
    if not info:
        return "SIN-REGISTRO-SEGUIMIENTO"
    statuses = info["statuses"]
    if statuses & ACTIVE_ROSTER_CODES:
        return "SIN-RESPUESTA-LIBRO-IIIB"
    if 0 in statuses or 3 in info["alive"]:
        return "MUERTE"
    if statuses & AWAY_ROSTER_CODES:
        return "FUERA-HOGAR-SIN-LIBRO-IIIB"
    return "OTRO-ROSTER-SIN-LIBRO-IIIB"


def _age_group(value) -> str:
    if pd.isna(value) or value < 15 or value > 120:
        return "EDAD-FUERA-O-FALTANTE"
    if value <= 29:
        return "15-29"
    if value <= 49:
        return "30-49"
    return "50-MAS"


def _sex_group(value) -> str:
    if value == 1:
        return "HOMBRE"
    if value == 3:
        return "MUJER"
    return "SEXO-OTRO-O-FALTANTE"


def _attrition_breakdown(df: pd.DataFrame) -> dict:
    valid_initial = df["outcome_initial"].isin(VALID_OUTCOMES)
    dimensions = {
        "participacion_inicial": df["outcome_initial"].map({1: "SI", 3: "NO"}),
        "edad_inicial": df["age_initial"].map(_age_group),
        "sexo_inicial": df["sex_initial"].map(_sex_group),
    }
    out = {}
    for dimension, labels in dimensions.items():
        rows = {}
        for label in sorted(set(labels[valid_initial].dropna())):
            mask = valid_initial & labels.eq(label)
            states = df.loc[mask, "followup_state"].value_counts()
            n = int(mask.sum())
            n_pair = int(states.get("RESPUESTA-VALIDA", 0))
            rows[label] = {
                "n_inicial_respuesta_valida": n,
                "n_libro_seguimiento": int(df.loc[mask, "book_followup"].sum()),
                "n_par_valido": n_pair,
                "p_retencion_par_valido": n_pair / n if n else None,
                "n_perdida_par": n - n_pair,
                "componentes": {k: int(v) for k, v in sorted(states.items())},
            }
        out[dimension] = rows
    return out


def _matrix(df: pd.DataFrame, weighted: bool) -> tuple[dict, dict]:
    pair = df[
        df["outcome_initial"].isin(VALID_OUTCOMES)
        & df["outcome_followup"].isin(VALID_OUTCOMES)
    ].copy()
    if weighted:
        mass_ok = np.isfinite(pair["analysis_weight"]) & (pair["analysis_weight"] > 0)
    else:
        pair["analysis_weight"] = 1.0
        mass_ok = pd.Series(True, index=pair.index)
    pair["mass_ok"] = mass_ok

    cells = {}
    for initial_code, initial_label in [(1, "SI"), (3, "NO")]:
        for follow_code, follow_label in [(1, "SI"), (3, "NO")]:
            mask = (pair["outcome_initial"] == initial_code) & (
                pair["outcome_followup"] == follow_code
            )
            use = mask & pair["mass_ok"]
            key = f"{initial_label}_A_{follow_label}"
            cells[key] = {
                "n": int(mask.sum()),
                "n_en_masa": int(use.sum()),
                "masa": float(math.fsum(pair.loc[use, "analysis_weight"].tolist())),
            }

    rates = {}
    for initial_label in ["SI", "NO"]:
        a = cells[f"{initial_label}_A_SI"]
        b = cells[f"{initial_label}_A_NO"]
        n_base = a["n"] + b["n"]
        mass_base = a["masa"] + b["masa"]
        rates[initial_label] = {
            "n_base": n_base,
            "n_base_en_masa": a["n_en_masa"] + b["n_en_masa"],
            "masa_base": mass_base,
            "p_sigue_si_no_ponderada": a["n"] / n_base if n_base else None,
            "p_sigue_no_no_ponderada": b["n"] / n_base if n_base else None,
            "p_sigue_si_primaria": a["masa"] / mass_base if mass_base else None,
            "p_sigue_no_primaria": b["masa"] / mass_base if mass_base else None,
        }
    matrix = {"celdas": cells, "bases_y_tasas": rates}
    scalars = {
        "n_pair": int(len(pair)),
        "n_mass": int(pair["mass_ok"].sum()),
        "mass": float(math.fsum(pair.loc[pair["mass_ok"], "analysis_weight"].tolist())),
        "stay": rates["SI"]["p_sigue_si_primaria"],
        "exit": rates["SI"]["p_sigue_no_primaria"],
        "enter": rates["NO"]["p_sigue_si_primaria"],
        "not_enter": rates["NO"]["p_sigue_no_primaria"],
    }
    return matrix, scalars


def _measure_pair(initial: pd.DataFrame, initial_roster: set[str],
                  follow: pd.DataFrame, follow_roster: dict[str, dict],
                  cardinality: dict, weight: pd.DataFrame | None,
                  pair_label: str, weighting_label: str) -> tuple[dict, dict]:
    df = initial.merge(follow, on="pid", how="left", validate="one_to_one")
    df["book_followup"] = df["book_followup"].fillna(False).astype(bool)
    df["followup_state"] = [
        _followup_state(row, follow_roster) for _, row in df.iterrows()
    ]
    if weight is None:
        df["analysis_weight"] = 1.0
        weighted = False
    else:
        df = df.merge(weight, on="pid", how="left", validate="one_to_one")
        weighted = True

    matrix, scalars = _matrix(df, weighted)
    matrix.update({"par": pair_label, "ponderacion_primaria": weighting_label})
    valid_initial = df["outcome_initial"].isin(VALID_OUTCOMES)
    valid_follow = df["outcome_followup"].isin(VALID_OUTCOMES)
    states = df.loc[valid_initial, "followup_state"].value_counts()
    coverage = {
        "par": pair_label,
        "n_cohorte_elegible_inicial": int(len(df)),
        "n_respuesta_inicial_valida": int(valid_initial.sum()),
        "n_respuesta_inicial_excluida": int((~valid_initial).sum()),
        "n_identidad_en_roster_o_libro_seguimiento": int(
            df["pid"].isin(set(follow_roster) | set(follow["pid"])).sum()
        ),
        "n_libro_iiib_seguimiento": int(df["book_followup"].sum()),
        "n_par_respuesta_valida": int((valid_initial & valid_follow).sum()),
        "n_perdida_analitica_desde_respuesta_inicial_valida": int(
            (valid_initial & ~valid_follow).sum()
        ),
        "componentes_desde_respuesta_inicial_valida": {
            k: int(v) for k, v in sorted(states.items())
        },
    }
    follow_valid = follow[follow["outcome_followup"].isin(VALID_OUTCOMES)]
    entrants = follow_valid[~follow_valid["pid"].isin(set(initial["pid"]))]
    entries = {
        "par": pair_label,
        "n_respuesta_valida_seguimiento_total": int(len(follow_valid)),
        "n_par_valido_desde_cohorte_inicial": int((valid_initial & valid_follow).sum()),
        "n_entrada_al_universo_analitico": int(len(entrants)),
        "n_entrada_ya_en_roster_inicial_sin_libro_iiib_inicial": int(
            entrants["pid"].isin(initial_roster).sum()
        ),
        "n_entrada_no_presente_en_roster_inicial": int(
            (~entrants["pid"].isin(initial_roster)).sum()
        ),
        "tratamiento": "EXCLUIDAS-DE-TASAS-DE-TRANSICION",
    }
    identity = dict(cardinality)
    identity.update({
        "par": pair_label,
        "personas_cohorte_inicial": int(initial["pid"].nunique()),
        "personas_cr_seguimiento_enlazadas": int(initial["pid"].isin(set(follow["pid"])).sum()),
        "cr_seguimiento_sin_roster": int((~follow["pid"].isin(set(follow_roster))).sum()),
    })
    objects = {
        "matrix": matrix,
        "coverage": coverage,
        "attrition": _attrition_breakdown(df),
        "entries": entries,
        "identity": identity,
    }
    return objects, scalars


def _longitudinal_weight_w2(path: str) -> pd.DataFrame:
    d = _read_member(path, "ehh05lw_all/ehh05_lw_b3b.dta")
    d["pid"] = _current_key(d, 2).map(pid10)
    _assert_unique(d, "pid", "ponderador longitudinal 2005")
    d["analysis_weight"] = _number(d["fac_3bl"])
    return d[["pid", "analysis_weight"]]


def _audit_weight_w3(path: str) -> dict:
    d = _read_member(path, "ehh09lw_all/ehh09_lw_b3b.dta")
    d["pid"] = _current_key(d, 3)
    values = _number(d["fac_3bl"])
    origins = sorted(set(d["folio"].astype(str).str.slice(6, 8)))
    return {
        "filas": int(len(d)),
        "ids_folio_ls": int(d["pid"].nunique()),
        "ids_duplicados": int(d["pid"].value_counts().gt(1).sum()),
        "filas_factor_positivo": int((values > 0).sum()),
        "codigos_origen_folio": origins,
        "uso": "NO-USADO: solo cohorte AP/2002; no cubre cohorte inicial completa 2005",
    }


def medir(inputs, contrato):
    paths = {key: value["ruta_absoluta"] for key, value in inputs.items()}
    w1_data = paths["ennvih1_2002_hogar_dta"]
    w2_data = paths["ennvih2_2005_hogar_dta"]
    w3_data = paths["ennvih3_2009_hogar_dta"]

    w1_cr = _read_member(w1_data, "ehh02dta_all/ehh02dta_b3b/iiib_cr.dta")
    w1_port = _read_member(w1_data, "ehh02dta_all/ehh02dta_b3b/iiib_portad.dta")
    w1_roster = _read_member(w1_data, "ehh02dta_all/ehh02dta_bc/c_ls.dta")
    w2_cr = _read_member(w2_data, "ehh05dta_b3b/iiib_cr.dta")
    w2_port = _read_member(w2_data, "ehh05dta_b3b/iiib_portad.dta")
    w2_roster = _read_member(w2_data, "ehh05dta_bc/c_ls.dta")
    w3_cr = _read_member(w3_data, "ehh09dta_all/ehh09dta_b3b/iiib_cr.dta")
    w3_roster = _read_member(w3_data, "ehh09dta_all/ehh09dta_bc/c_ls.dta")

    initial12, roster1 = _prepare_initial(w1_cr, w1_port, w1_roster, 1)
    follow2, roster2, card2 = _prepare_followup(w2_cr, w2_roster, 2)
    weight2 = _longitudinal_weight_w2(
        paths["ennvih2_2005_ponderador_longitudinal"]
    )
    pair12, scalars12 = _measure_pair(
        initial12,
        roster1,
        follow2,
        roster2,
        card2,
        weight2,
        "ENNVIH-1-2002_A_ENNVIH-2-2005-06",
        "FAC_3BL_LONGITUDINAL_2005",
    )

    initial23, roster2_initial = _prepare_initial(w2_cr, w2_port, w2_roster, 2)
    follow3, roster3, card3 = _prepare_followup(w3_cr, w3_roster, 3)
    pair23, scalars23 = _measure_pair(
        initial23,
        roster2_initial,
        follow3,
        roster3,
        card3,
        None,
        "ENNVIH-2-2005-06_A_ENNVIH-3-2009-12",
        "NO-PONDERADO-PANEL-OBSERVADO",
    )
    pair23["identity"]["auditoria_fac_3bl_2009"] = _audit_weight_w3(
        paths["ennvih3_2009_ponderador_longitudinal"]
    )

    out = {}
    for short, objects, scalars, method in [
        ("1A2", pair12, scalars12, "FAC_3BL_LONGITUDINAL_2005"),
        ("2A3", pair23, scalars23, "NO-PONDERADO-PANEL-OBSERVADO"),
    ]:
        base = PREFIX + short + "-"
        out[base + "MATRIZ-JSON"] = _json(objects["matrix"])
        out[base + "COBERTURA-JSON"] = _json(objects["coverage"])
        out[base + "ATTRITION-JSON"] = _json(objects["attrition"])
        out[base + "ENTRADAS-UNIVERSO-JSON"] = _json(objects["entries"])
        out[base + "IDENTIDAD-JSON"] = _json(objects["identity"])
        out[base + "PONDERACION"] = method
        out[base + "N-PAR-VALIDO"] = scalars["n_pair"]
        out[base + "N-PAR-EN-MASA"] = scalars["n_mass"]
        out[base + "MASA-PAR"] = scalars["mass"]
        out[base + "P-PERMANECE"] = scalars["stay"]
        out[base + "P-SALE"] = scalars["exit"]
        out[base + "P-ENTRA"] = scalars["enter"]
        out[base + "P-NO-ENTRA"] = scalars["not_enter"]
    return out

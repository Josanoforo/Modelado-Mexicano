"""Perfil de contacto y respuesta a dadivas, ENCUCI 2020.

Interfaz GEN2: ``medir(inputs, contrato) -> {RESULT-...: valor}``.
El modulo no abre la spec ni resuelve payloads. Todas las razones se estiman
como dominios de un unico marco de personas con FAC_SEL valido. La
incertidumbre usa el mismo bootstrap de UPM dentro de estrato para todas las
estadisticas, de modo que los contrastes conservan su covarianza de diseno.
"""
from __future__ import annotations

import json
import struct
import zipfile

import numpy as np


PAYLOAD_ID = "encuci2020_bd_dbf"
MEMBER = "ENCUCI_2020_SEC_4_5.dbf"
CONTACT = [f"AP5_16_{i}" for i in range(1, 11)]
LABELS = [
    "policia_transito_seguridad_publica", "ministerio_publico", "jueces",
    "salud_publica", "educacion_publica", "seguridad_social_bienestar",
    "gobierno_municipal_alcaldia", "gobierno_estatal_federal",
    "guardia_nacional", "ejercito_marina",
]
COLUMNS = ["ID_PER", *CONTACT, "AP5_17", "AP5_18", "FAC_SEL",
           "EST_DIS", "UPM_DIS", "DOMINIO"]
SEP = "\u241f"


def _fields(buf: bytes):
    nrec = struct.unpack("<I", buf[4:8])[0]
    hsize = struct.unpack("<H", buf[8:10])[0]
    rsize = struct.unpack("<H", buf[10:12])[0]
    out, pos = [], 32
    while pos + 32 <= hsize:
        d = buf[pos:pos + 32]
        if d[0:1] == b"\x0d":
            break
        name = d[0:11].split(b"\x00")[0].decode("latin-1").strip()
        out.append((name, d[16]))
        pos += 32
    return nrec, hsize, rsize, out


def _read_dbf(buf: bytes, columns):
    nrec, hsize, rsize, fields = _fields(buf)
    names = {name for name, _ in fields}
    missing = [c for c in columns if c not in names]
    if missing:
        raise ValueError("columnas ausentes: " + ",".join(missing))
    offsets, off = {}, 1
    for name, width in fields:
        if name in columns:
            offsets[name] = (off, off + width)
        off += width
    rows = []
    for i in range(nrec):
        rec = buf[hsize + i * rsize:hsize + (i + 1) * rsize]
        if len(rec) != rsize:
            raise ValueError(f"registro DBF truncado: {i}")
        if rec[0:1] == b"*":
            continue
        rows.append({c: rec[a:b].decode("latin-1").strip()
                     for c, (a, b) in offsets.items()})
    return rows


def _code(value):
    text = str(value or "").strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not np.isfinite(number) or number != int(number):
        return None
    return int(number)


def _weight(value):
    try:
        out = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return out if np.isfinite(out) and out > 0 else None


def classify_contacts(values):
    """Return (any_contact, exact_count); None represents unknown."""
    codes = [_code(v) for v in values]
    if any(c == 1 for c in codes):
        any_contact = 1
    elif all(c == 2 for c in codes):
        any_contact = 0
    else:
        any_contact = None
    exact = sum(c == 1 for c in codes) if all(c in (1, 2) for c in codes) else None
    return any_contact, exact


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def _pct(series):
    good = series[np.isfinite(series)]
    if not len(good):
        return None, None
    return (float(np.percentile(good, 2.5)),
            float(np.percentile(good, 97.5)))


class Survey:
    def __init__(self, rows, replicas, seed):
        valid = [(r, _weight(r.get("FAC_SEL"))) for r in rows]
        valid = [(r, w) for r, w in valid if w is not None]
        self.rows = [r for r, _ in valid]
        self.w = np.asarray([w for _, w in valid], dtype=float)
        self.n = len(self.rows)
        self.replicas = int(replicas)
        self.design_ok = bool(self.n) and all(
            str(r.get("EST_DIS", "")).strip() and
            str(r.get("UPM_DIS", "")).strip() for r in self.rows)
        self.est = np.asarray([str(r.get("EST_DIS", "")).strip()
                               for r in self.rows])
        self.upm = np.asarray([str(r.get("UPM_DIS", "")).strip()
                               for r in self.rows])
        self.psu_inverse = None
        self.draws = None
        self.n_strata = 0
        self.n_psu = 0
        self.n_singleton = 0
        if self.design_ok:
            keys = np.asarray([f"{a}{SEP}{b}" for a, b in zip(self.est, self.upm)])
            psus, self.psu_inverse = np.unique(keys, return_inverse=True)
            psu_strata = np.asarray([x.split(SEP, 1)[0] for x in psus])
            strata = np.unique(psu_strata)
            self.n_strata, self.n_psu = len(strata), len(psus)
            self.draws = np.zeros((self.replicas, self.n_psu), dtype=np.int16)
            rng = np.random.Generator(np.random.PCG64(int(seed)))
            for stratum in strata:
                pos = np.flatnonzero(psu_strata == stratum)
                k = len(pos)
                if k == 1:
                    self.n_singleton += 1
                    self.draws[:, pos[0]] = 1
                else:
                    self.draws[:, pos] = rng.multinomial(
                        k, np.full(k, 1.0 / k), size=self.replicas)

    def ratio(self, numerator, denominator):
        numerator = np.asarray(numerator, dtype=bool)
        denominator = np.asarray(denominator, dtype=bool)
        den_w = self.w * denominator
        mass = float(den_w.sum())
        point = None if mass <= 0 else float((self.w * numerator * denominator).sum() / mass)
        series = None
        lo = hi = None
        if point is not None and self.design_ok:
            den_psu = np.bincount(self.psu_inverse, weights=den_w,
                                  minlength=self.n_psu)
            num_psu = np.bincount(
                self.psu_inverse,
                weights=self.w * numerator * denominator,
                minlength=self.n_psu)
            den_rep = self.draws @ den_psu
            num_rep = self.draws @ num_psu
            with np.errstate(divide="ignore", invalid="ignore"):
                series = np.where(den_rep > 0, num_rep / den_rep, np.nan)
            lo, hi = _pct(series)
        return {"n": int(denominator.sum()), "masa": mass, "p": point,
                "ic95_lo": lo, "ic95_hi": hi}, series


def _difference(name, left, right):
    lp, ls = left
    rp, rs = right
    point = None if lp["p"] is None or rp["p"] is None else lp["p"] - rp["p"]
    lo = hi = None
    if ls is not None and rs is not None:
        lo, hi = _pct(ls - rs)
    return {"contraste": name, "estimacion": point, "ic95_lo": lo,
            "ic95_hi": hi, "escala": "proporcion"}


def measure_rows(rows, replicas=2000, seed=20260919):
    survey = Survey(rows, replicas, seed)
    n = survey.n
    contacts = [classify_contacts([r.get(c) for c in CONTACT])
                for r in survey.rows]
    any_c = np.asarray([x[0] if x[0] is not None else -1 for x in contacts])
    counts = np.asarray([x[1] if x[1] is not None else -1 for x in contacts])
    request = np.asarray([_code(r.get("AP5_17")) for r in survey.rows], dtype=object)
    delivery = np.asarray([_code(r.get("AP5_18")) for r in survey.rows], dtype=object)
    domain = np.asarray([str(r.get("DOMINIO", "")).strip() for r in survey.rows])
    all_mask = np.ones(n, dtype=bool)

    exposure = []
    for var, label in zip(CONTACT, LABELS):
        code = np.asarray([_code(r.get(var)) for r in survey.rows], dtype=object)
        valid = np.asarray([x in (1, 2) for x in code])
        yes = np.asarray([x == 1 for x in code])
        stat, _ = survey.ratio(yes, valid)
        unknown, _ = survey.ratio(~valid, all_mask)
        exposure.append({"variable": var, "tipo": label, **stat,
                         "n_desconocido": int((~valid).sum()),
                         "masa_desconocida_prop": unknown["p"]})

    any_known = any_c >= 0
    any_yes = any_c == 1
    any_stat, _ = survey.ratio(any_yes, any_known)
    any_unknown, _ = survey.ratio(~any_known, all_mask)
    any_table = {**any_stat, "n_desconocido": int((~any_known).sum()),
                 "masa_desconocida_prop": any_unknown["p"],
                 "regla": "si algun_si=>si; todos_no=>no; resto=>desconocido"}

    complete = counts >= 0
    count_table = []
    count_stats = {}
    for key, mask in [("0", counts == 0), ("1", counts == 1),
                      ("2", counts == 2), ("3+", counts >= 3)]:
        stat, series = survey.ratio(mask, complete)
        count_stats[key] = (stat, series)
        count_table.append({"numero_tipos": key, "n_categoria": int(mask.sum()),
                            **stat})
    complete_stat, _ = survey.ratio(complete, all_mask)

    valid_response = np.asarray([(a in (1, 2) and b in (1, 2))
                                 for a, b in zip(request, delivery)])
    req_yes = np.asarray([a == 1 for a in request])
    del_yes = np.asarray([b == 1 for b in delivery])
    union = req_yes | del_yes
    joint_masks = {
        "ninguna": (~req_yes) & (~del_yes),
        "solo_solicitud": req_yes & (~del_yes),
        "solo_entrega": (~req_yes) & del_yes,
        "ambas": req_yes & del_yes,
    }
    groups = [
        ("total_contacto", any_yes),
        ("tipos_1", any_yes & (counts == 1)),
        ("tipos_2", any_yes & (counts == 2)),
        ("tipos_3mas", any_yes & (counts >= 3)),
        ("dominio_U", any_yes & (domain == "U")),
        ("dominio_C", any_yes & (domain == "C")),
        ("dominio_R", any_yes & (domain == "R")),
    ]
    joint_table, group_metrics = [], {}
    for group, base in groups:
        eligible = base & valid_response
        coverage, _ = survey.ratio(valid_response, base)
        cells, cell_series = {}, {}
        for cell, cell_mask in joint_masks.items():
            cells[cell], cell_series[cell] = survey.ratio(cell_mask, eligible)
        cond_req = survey.ratio(del_yes, eligible & req_yes)
        cond_no_req = survey.ratio(del_yes, eligible & (~req_yes))
        union_stat = survey.ratio(union, eligible)
        cond_gap = _difference("entrega_dado_solicitud_menos_entrega_dado_no_solicitud",
                               cond_req, cond_no_req)
        joint_table.append({
            "grupo": group, "n_base": int(base.sum()),
            "masa_base": float(survey.w[base].sum()),
            "cobertura_respuestas_validas": coverage,
            "distribucion": cells,
            "p_entrega_dado_solicitud": cond_req[0],
            "p_entrega_dado_no_solicitud": cond_no_req[0],
            "diferencia_condicional": cond_gap,
            "p_solicitud_o_entrega": union_stat[0],
        })
        group_metrics[group] = {"union": union_stat,
                                "gap": ({"p": cond_gap["estimacion"]},
                                        None if cond_req[1] is None or cond_no_req[1] is None
                                        else cond_req[1] - cond_no_req[1])}

    contrasts = []
    for other in ("tipos_2", "tipos_3mas"):
        contrasts.append(_difference(
            f"{other}_menos_tipos_1_en_union",
            group_metrics[other]["union"], group_metrics["tipos_1"]["union"]))
        contrasts.append(_difference(
            f"{other}_menos_tipos_1_en_brecha_condicional",
            group_metrics[other]["gap"], group_metrics["tipos_1"]["gap"]))

    total = next(x for x in joint_table if x["grupo"] == "total_contacto")
    cells = total["distribucion"]
    partition = sum(cells[k]["p"] for k in joint_masks) if all(
        cells[k]["p"] is not None for k in joint_masks) else None
    union_identity = None
    if all(cells[k]["p"] is not None for k in joint_masks):
        p_req = cells["solo_solicitud"]["p"] + cells["ambas"]["p"]
        p_del = cells["solo_entrega"]["p"] + cells["ambas"]["p"]
        union_identity = (total["p_solicitud_o_entrega"]["p"] -
                          (p_req + p_del - cells["ambas"]["p"]))

    ids = [str(r.get("ID_PER", "")).strip() for r in survey.rows]
    method = ("BOOTSTRAP-UPM-EN-ESTRATO-MARCO-COMPLETO" if survey.design_ok
              and not survey.n_singleton else
              "BOOTSTRAP-UPM-EN-ESTRATO-CON-SINGLETON-AUTOREMUESTREADO"
              if survey.design_ok else "IC-NO-DISPONIBLE-DISENO-INCOMPLETO")
    old = 0.12600561008991654
    observed_union = total["p_solicitud_o_entrega"]["p"]
    control = {"universo": "contacto_y_AP5_17_18_validas",
               "resultado_sellado_CALC_ENCUCI_0001": old,
               "resultado_actual": observed_union,
               "delta": None if observed_union is None else observed_union - old,
               "nota": "control de contexto; no resultado nacional nuevo"}
    return {
        "RESULT-ENCUCI2020-ER-N-FILAS": len(rows),
        "RESULT-ENCUCI2020-ER-N-PONDERADOR-VALIDO": n,
        "RESULT-ENCUCI2020-ER-MASA-PONDERADA": float(survey.w.sum()),
        "RESULT-ENCUCI2020-ER-LLAVE-IDPER": "UNICA" if len(ids) == len(set(ids)) else "NO-UNICA",
        "RESULT-ENCUCI2020-ER-N-ESTRATOS": survey.n_strata,
        "RESULT-ENCUCI2020-ER-N-UPM": survey.n_psu,
        "RESULT-ENCUCI2020-ER-N-ESTRATOS-SINGLETON": survey.n_singleton,
        "RESULT-ENCUCI2020-ER-METODO-IC": method,
        "RESULT-ENCUCI2020-ER-EXPOSICION-POR-TIPO": _json(exposure),
        "RESULT-ENCUCI2020-ER-CONTACTO-CUALQUIERA": _json(any_table),
        "RESULT-ENCUCI2020-ER-COBERTURA-CONTEO-EXACTO": complete_stat["p"],
        "RESULT-ENCUCI2020-ER-CONTEO-TIPOS": _json(count_table),
        "RESULT-ENCUCI2020-ER-RESPUESTA-CONJUNTA": _json(joint_table),
        "RESULT-ENCUCI2020-ER-CONTRASTES": _json(contrasts),
        "RESULT-ENCUCI2020-ER-CONTROL-NACIONAL": _json(control),
        "RESULT-ENCUCI2020-ER-VALIDACION-PARTICION": None if partition is None else partition - 1.0,
        "RESULT-ENCUCI2020-ER-VALIDACION-UNION": union_identity,
    }


def medir(inputs, contrato):
    path = inputs[PAYLOAD_ID]["ruta_absoluta"]
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        matches = [x for x in names if x.rsplit("/", 1)[-1] == MEMBER]
        if len(matches) != 1:
            raise ValueError(f"miembro {MEMBER}: coincidencias={len(matches)}")
        rows = _read_dbf(archive.read(matches[0]), COLUMNS)
    par = contrato["parametros"]
    seed = contrato["seed"]
    return measure_rows(rows, int(par["bootstrap_replicas"]), int(seed["valor"]))

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

    any_yes = any_c == 1
    complete = counts >= 0
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
    contact_codes = [np.asarray([_code(r.get(var)) for r in survey.rows], dtype=object)
                     for var in CONTACT]
    by_contact, validations = [], []
    for var, label, code in zip(CONTACT, LABELS, contact_codes):
        base = np.asarray([x == 1 for x in code])
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
        by_contact.append({
            "variable": var, "tipo": label, "universo": "personas con contacto con el tipo",
            "n_base": int(base.sum()),
            "masa_base": float(survey.w[base].sum()),
            "cobertura_respuestas_validas": coverage,
            "distribucion": cells,
            "p_entrega_dado_solicitud": cond_req[0],
            "p_entrega_dado_no_solicitud": cond_no_req[0],
            "diferencia_condicional": cond_gap,
            "p_solicitud_o_entrega": union_stat[0],
        })
        partition_j = (sum(cells[k]["p"] for k in joint_masks)
                       if all(cells[k]["p"] is not None for k in joint_masks) else None)
        union_j = None
        if partition_j is not None:
            p_req = cells["solo_solicitud"]["p"] + cells["ambas"]["p"]
            p_del = cells["solo_entrega"]["p"] + cells["ambas"]["p"]
            union_j = union_stat[0]["p"] - (p_req + p_del - cells["ambas"]["p"])
        validations.append({"variable": var, "tipo": label,
                            "particion_cuatro_celdas_menos_uno": None if partition_j is None else partition_j - 1.0,
                            "union_menos_solicitud_mas_entrega_menos_ambas": union_j})
    contrasts = []
    for var, label, code in zip(CONTACT, LABELS, contact_codes):
        known = np.asarray([x in (1, 2) for x in code])
        base = any_yes & valid_response
        yes = np.asarray([x == 1 for x in code])
        no = np.asarray([x == 2 for x in code])
        left_union = survey.ratio(union, base & yes)
        right_union = survey.ratio(union, base & no)
        left_both = survey.ratio(joint_masks["ambas"], base & yes)
        right_both = survey.ratio(joint_masks["ambas"], base & no)
        unknown, _ = survey.ratio(~known, base)
        contrasts.append({"variable": var, "tipo": label,
                          "universo": "personas con algun contacto acreditado y AP5_17/AP5_18 validas",
                          "n_excluido_contacto_desconocido": int((base & ~known).sum()),
                          "masa_excluida_contacto_desconocido": float(survey.w[base & ~known].sum()),
                          "proporcion_excluida_contacto_desconocido": unknown["p"],
                          "diferencia_union_si_menos_no": _difference("si_menos_no_union", left_union, right_union),
                          "diferencia_ambas_si_menos_no": _difference("si_menos_no_ambas", left_both, right_both)})

    solapamiento = []
    for var, label, code in zip(CONTACT, LABELS, contact_codes):
        base = np.asarray([x == 1 for x in code])
        complete_base = base & complete
        coverage_all = survey.ratio(valid_response, base)
        coverage_complete = survey.ratio(valid_response, complete_base)
        other = counts - 1
        dist = {}
        for name, mask in (("0", other == 0), ("1", other == 1), ("2+", other >= 2)):
            dist[name], _ = survey.ratio(mask, complete_base)
        solapamiento.append({"variable": var, "tipo": label,
                             "n_contacto": int(base.sum()), "n_vector_completo": int(complete_base.sum()),
                             "distribucion_numero_otros_tipos": dist,
                             "cobertura_respuestas_contacto": coverage_all[0],
                             "cobertura_respuestas_vector_completo": coverage_complete[0],
                             "diferencia_cobertura_completo_menos_contacto": _difference("completo_menos_contacto", coverage_complete, coverage_all)})

    ids = [str(r.get("ID_PER", "")).strip() for r in survey.rows]
    method = ("BOOTSTRAP-UPM-EN-ESTRATO-MARCO-COMPLETO" if survey.design_ok
              and not survey.n_singleton else
              "BOOTSTRAP-UPM-EN-ESTRATO-CON-SINGLETON-AUTOREMUESTREADO"
              if survey.design_ok else "IC-NO-DISPONIBLE-DISENO-INCOMPLETO")
    return {
        "RESULT-ENCUCI2020-RPCV11-N-FILAS": len(rows),
        "RESULT-ENCUCI2020-RPCV11-N-PONDERADOR-VALIDO": n,
        "RESULT-ENCUCI2020-RPCV11-MASA-PONDERADA": float(survey.w.sum()),
        "RESULT-ENCUCI2020-RPCV11-LLAVE-IDPER": "UNICA" if len(ids) == len(set(ids)) else "NO-UNICA",
        "RESULT-ENCUCI2020-RPCV11-N-ESTRATOS": survey.n_strata,
        "RESULT-ENCUCI2020-RPCV11-N-UPM": survey.n_psu,
        "RESULT-ENCUCI2020-RPCV11-N-ESTRATOS-SINGLETON": survey.n_singleton,
        "RESULT-ENCUCI2020-RPCV11-METODO-IC": method,
        "RESULT-ENCUCI2020-RPCV11-PERFIL-POR-CONTACTO": _json(by_contact),
        "RESULT-ENCUCI2020-RPCV11-CONTRASTES-POR-CONTACTO": _json(contrasts),
        "RESULT-ENCUCI2020-RPCV11-SOLAPAMIENTO-OTROS-CONTACTOS": _json(solapamiento),
        "RESULT-ENCUCI2020-RPCV11-VALIDACIONES-POR-CONTACTO": _json(validations),
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

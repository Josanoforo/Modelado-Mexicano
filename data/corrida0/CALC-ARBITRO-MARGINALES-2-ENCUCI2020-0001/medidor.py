"""ARBITRO-MARGINALES-2, pieza ENCUCI2020.

Formaliza en GEN2 dos reglas de milpa/tramite-ola5-propuesta-v0.yaml que P1
clasifico RE-MEDIDA (nueva): civico.transferencia.entitlement_encuci2020 y
civico.voto.agencia_con_secreto_encuci2020. El universo, el eje, el desenlace,
el ponderador y el metodo de IC son los que el propio GEN1 ya prerregistro
(spec humana: forense/prereg-caja/ARBITRO-MARGINALES-2-ENCUCI2020-spec-v1_0.md).

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor}.
"""
from __future__ import annotations

import json
import struct
import zipfile

import numpy as np

PAYLOAD_ID = "encuci2020_bd_dbf"
MEMBER = "ENCUCI_2020_SEC_6_7_8.dbf"
COLUMNS = ["ID_PER", "AP6_9", "AP6_10", "AP6_11", "AP7_13", "AP7_15",
           "FAC_SEL", "EST_DIS", "UPM_DIS"]
SEP = "␟"


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


def _pct(series):
    good = series[np.isfinite(series)]
    if not len(good):
        return None, None
    return (float(np.percentile(good, 2.5)), float(np.percentile(good, 97.5)))


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False)


class Survey:
    """Bootstrap de UPM dentro de estrato, con reemplazo -- mismo metodo que
    CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001, semilla 42 (la que el GEN1 de
    este par de reglas declara: 'IC95 bootstrap de conglomerado, 10 000
    replicas, seed 42')."""

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
        self.n_strata = 0
        self.n_psu = 0
        self.n_singleton = 0
        self.psu_inverse = None
        self.draws = None
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
        point = None if mass <= 0 else float(
            (self.w * numerator * denominator).sum() / mass)
        series = None
        lo = hi = None
        if point is not None and self.design_ok:
            den_psu = np.bincount(self.psu_inverse, weights=den_w,
                                   minlength=self.n_psu)
            num_psu = np.bincount(self.psu_inverse,
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
        lo, hi = _pct((ls - rs) * 100.0)
    return {"contraste": name, "brecha_pp": None if point is None else point * 100.0,
            "ic95_brecha_pp_lo": lo, "ic95_brecha_pp_hi": hi}


def measure_rows(rows, replicas, seed):
    survey = Survey(rows, replicas, seed)
    ids = [str(r.get("ID_PER", "")).strip() for r in survey.rows]
    llave = "UNICA" if len(ids) == len(set(ids)) else "NO-UNICA"

    ap69 = np.asarray([_code(r.get("AP6_9")) for r in survey.rows], dtype=object)
    ap610 = np.asarray([_code(r.get("AP6_10")) for r in survey.rows], dtype=object)
    ap611 = np.asarray([_code(r.get("AP6_11")) for r in survey.rows], dtype=object)
    ap713 = np.asarray([str(r.get("AP7_13", "")).strip() for r in survey.rows])
    ap715 = np.asarray([_code(r.get("AP7_15")) for r in survey.rows], dtype=object)

    # --- Regla A: civico.transferencia.entitlement_encuci2020 ---
    universo_a = np.asarray([x in (1, 2) for x in ap69])
    derecho = np.asarray([x == 2 for x in ap69])
    ben_si = universo_a & np.asarray([x == 1 for x in ap610])
    ben_no = universo_a & np.asarray([x == 2 for x in ap610])
    stat_ben_si = survey.ratio(derecho, ben_si)
    stat_ben_no = survey.ratio(derecho, ben_no)
    brecha_a = _difference("derecho_beneficiario_menos_no_beneficiario",
                            stat_ben_si, stat_ben_no)

    anidado_base = ben_si & np.asarray([x in (1, 2) for x in ap611])
    pidieron = anidado_base & np.asarray([x == 1 for x in ap611])
    no_pidieron = anidado_base & np.asarray([x == 2 for x in ap611])
    stat_pidieron = survey.ratio(derecho, pidieron)
    stat_no_pidieron = survey.ratio(derecho, no_pidieron)
    brecha_anidada = _difference("derecho_le_pidieron_menos_no_le_pidieron",
                                  stat_pidieron, stat_no_pidieron)

    regla_a = {
        "universo_n": int(universo_a.sum()),
        "beneficiario_si": stat_ben_si[0],
        "beneficiario_no": stat_ben_no[0],
        "brecha": brecha_a,
        "eje_anidado_ap6_11": {
            "le_pidieron_algo_a_cambio": stat_pidieron[0],
            "no_le_pidieron": stat_no_pidieron[0],
            "brecha": brecha_anidada,
        },
    }

    # --- Regla B: civico.voto.agencia_con_secreto_encuci2020 ---
    ap713_valida = (ap713 != "") & (ap713 != "99")
    morena = ap713 == "07"
    universo_b = (np.asarray([x in (1, 2) for x in ap610]) &
                  np.asarray([x in (1, 2) for x in ap715]) & ap713_valida)
    ramas = {}
    for nombre, codigo in (("SECRETO", 1), ("OBSERVABLE", 2)):
        rama_mask = universo_b & np.asarray([x == codigo for x in ap715])
        si_mask = rama_mask & np.asarray([x == 1 for x in ap610])
        no_mask = rama_mask & np.asarray([x == 2 for x in ap610])
        stat_si = survey.ratio(morena, si_mask)
        stat_no = survey.ratio(morena, no_mask)
        ramas[nombre] = {
            "beneficiario_si": stat_si[0],
            "beneficiario_no": stat_no[0],
            "brecha": _difference(f"morena_beneficiario_menos_no_{nombre.lower()}",
                                   stat_si, stat_no),
        }

    regla_b = {"universo_n": int(universo_b.sum()), "ramas": ramas}

    return {
        "RESULT-ARB2-ENCUCI-N-FILAS": len(rows),
        "RESULT-ARB2-ENCUCI-LLAVE-IDPER": llave,
        "RESULT-ARB2-ENCUCI-N-ESTRATOS": survey.n_strata,
        "RESULT-ARB2-ENCUCI-N-UPM": survey.n_psu,
        "RESULT-ARB2-ENCUCI-N-ESTRATOS-SINGLETON": survey.n_singleton,
        "RESULT-ARB2-ENCUCI-METODO-IC": (
            "BOOTSTRAP-UPM-EN-ESTRATO-SEED42" if survey.design_ok
            else "IC-NO-DISPONIBLE-DISENO-INCOMPLETO"),
        "RESULT-ARB2-ENCUCI-ENTITLEMENT": _json(regla_a),
        "RESULT-ARB2-ENCUCI-AGENCIA-SECRETO": _json(regla_b),
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

"""GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · pieza P-ENCUCI2020 · CALC-PDR1-ENCUCI2020-0001.

Pisos descriptivos RETROSPECTIVOS de seis afirmaciones del dominio AUTORIDAD
(ASTRA5-U0-AUTOR-001/002/003/010/030/031, tabla ENCUCI_2020_SEC_4_5) y la
pieza faltante de la regla RG-67c84a2224 (tabla ENCUCI_2020_SEC_6_7_8):
proporción conjunta derecho (AP6_9=2) x voto secreto (AP7_15=1) entre
beneficiarios de programa social a quienes no se pidió nada a cambio.
Spec humana: forense/prereg-caja/PDR1-ENCUCI2020-spec-v1_0.md.

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor}.
Ponderador y bootstrap de UPM dentro de estrato copiados de la plantilla
CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001 (misma clase Survey, semilla 42).
"""
from __future__ import annotations

import json
import struct
import zipfile

import numpy as np

PAYLOAD_ID = "encuci2020_bd_dbf"
M45 = "ENCUCI_2020_SEC_4_5.dbf"
M678 = "ENCUCI_2020_SEC_6_7_8.dbf"
MSD = "ENCUCI_2020_SD.dbf"
C45 = ["ID_PER", "AP4_9_1", "AP4_9_4", "AP4_13", "AP5_1_4", "AP5_11",
       "FAC_SEL", "EST_DIS", "UPM_DIS", "DOMINIO"]
C678 = ["ID_PER", "AP6_9", "AP6_10", "AP6_11", "AP7_15",
        "FAC_SEL", "EST_DIS", "UPM_DIS", "DOMINIO"]
CSD = ["ID_PER", "SEXO", "EDAD"]
SEP = "␟"
P = "RESULT-PDR1-ENCUCI2020-"

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



def _edad_grupo(value):
    e = _code(value)
    if e is None or e < 15 or e > 96:
        return None          # 97/98/99/blanco: edad no especificada
    if e <= 29:
        return "15-29"
    if e <= 44:
        return "30-44"
    if e <= 59:
        return "45-59"
    return "60+"


def _segmentos(rows, sd):
    sexo, edad, dom = [], [], []
    for r in rows:
        s = sd.get(str(r.get("ID_PER", "")).strip())
        sx = _code(s.get("SEXO")) if s else None
        sexo.append({1: "HOMBRE", 2: "MUJER"}.get(sx))
        edad.append(_edad_grupo(s.get("EDAD")) if s else None)
        d = str(r.get("DOMINIO", "")).strip()
        dom.append(d if d in ("U", "C", "R") else None)
    return {"sexo": np.asarray(sexo, dtype=object),
            "edad": np.asarray(edad, dtype=object),
            "dominio": np.asarray(dom, dtype=object)}


def _celda(survey, num, den, segs):
    stat, series = survey.ratio(num, den)
    out = {"total": stat, "segmentos": {}}
    for eje, vals in segs.items():
        cats = sorted({v for v in vals if v is not None})
        out["segmentos"][eje] = {
            c: survey.ratio(num, den & (vals == c))[0] for c in cats}
    return out, series


def _in(arr, codes):
    return np.asarray([x in codes for x in arr])


def measure(rows45, rows678, rowssd, replicas, seed):
    sd = {}
    for r in rowssd:
        sd.setdefault(str(r.get("ID_PER", "")).strip(), r)
    out = {}

    # ---------------- Tabla SEC_4_5: afirmaciones AUTOR ----------------
    s = Survey(rows45, replicas, seed)
    segs = _segmentos(s.rows, sd)
    out[P + "SEC45-N-FILAS"] = len(rows45)
    out[P + "SEC45-N-UPM"] = s.n_psu
    out[P + "SEC45-N-ESTRATOS"] = s.n_strata
    out[P + "SEC45-JOIN-SD-N"] = int(sum(
        1 for r in s.rows if str(r.get("ID_PER", "")).strip() in sd))
    out[P + "METODO-IC"] = ("BOOTSTRAP-UPM-EN-ESTRATO-SEED42" if s.design_ok
                            else "IC-NO-DISPONIBLE-DISENO-INCOMPLETO")

    a91 = np.asarray([_code(r.get("AP4_9_1")) for r in s.rows], dtype=object)
    a94 = np.asarray([_code(r.get("AP4_9_4")) for r in s.rows], dtype=object)
    a413 = np.asarray([_code(r.get("AP4_13")) for r in s.rows], dtype=object)
    a514 = np.asarray([str(r.get("AP5_1_4", "")).strip() for r in s.rows])
    a511 = np.asarray([_code(r.get("AP5_11")) for r in s.rows], dtype=object)

    def put(clave, celda):
        est = celda[0]["total"]
        out[P + clave] = est["p"]
        out[P + clave + "-IC95-INF"] = est["ic95_lo"]
        out[P + clave + "-IC95-SUP"] = est["ic95_hi"]
        out[P + clave + "-N"] = est["n"]
        out[P + clave + "-SEGMENTOS"] = _json(celda[0]["segmentos"])

    # AUTOR-001
    v91 = _in(a91, (1, 2, 3, 4))
    c001 = _celda(s, _in(a91, (1, 2)), v91, segs)
    put("AUTOR001-LIDER-FUERTE-ACUERDO", c001)
    # AUTOR-002
    v94 = _in(a94, (1, 2, 3, 4))
    c002 = _celda(s, _in(a94, (1, 2)), v94, segs)
    put("AUTOR002-PARTICIPAN-TODOS-ACUERDO", c002)
    # AUTOR-003 (texto de dos dígitos 00..10)
    v514 = np.asarray([x in {f"{k:02d}" for k in range(11)} for x in a514])
    alto = np.asarray([x in ("08", "09", "10") for x in a514])
    c003 = _celda(s, alto, v514, segs)
    put("AUTOR003-CONFIA-SERVIDORES-8A10", c003)
    # AUTOR-010: conjunta y condicional
    ambos_validos = v91 & v94
    ac91 = _in(a91, (1, 2))
    ac94 = _in(a94, (1, 2))
    c010j = _celda(s, ac91 & ac94, ambos_validos, segs)
    put("AUTOR010-CONJUNTA-LIDER-Y-PARTICIPACION", c010j)
    c010c = _celda(s, ac94, ambos_validos & ac91, segs)
    put("AUTOR010-PARTICIPACION-DADO-LIDER", c010c)
    # AUTOR-030: AP5_11 categorías 1..4 entre válidos
    v511 = _in(a511, (1, 2, 3, 4))
    series511 = {}
    for k, nom in ((1, "OBEDECER-SIEMPRE"), (2, "PEDIR-CAMBIO"),
                   (3, "DESOBEDECER-INJUSTA"), (4, "NINGUNA")):
        c = _celda(s, a511 == k, v511, segs)
        put(f"AUTOR030-AP5_11-{nom}", c)
        series511[k] = c[1]
    lo, hi = (None, None)
    if series511[2] is not None and series511[1] is not None:
        lo, hi = _pct(series511[2] - series511[1])
    p1 = out[P + "AUTOR030-AP5_11-OBEDECER-SIEMPRE"]
    p2 = out[P + "AUTOR030-AP5_11-PEDIR-CAMBIO"]
    out[P + "AUTOR030-DIF-PEDIR-MENOS-OBEDECER"] = (
        None if p1 is None or p2 is None else p2 - p1)
    out[P + "AUTOR030-DIF-PEDIR-MENOS-OBEDECER-IC95-INF"] = lo
    out[P + "AUTOR030-DIF-PEDIR-MENOS-OBEDECER-IC95-SUP"] = hi
    # AUTOR-031: AP4_13 2+3 entre válidos 1..4; y categoría 1
    v413 = _in(a413, (1, 2, 3, 4))
    c031 = _celda(s, _in(a413, (2, 3)), v413, segs)
    put("AUTOR031-NO-DEMOCRATICO-O-INDIFERENTE", c031)
    c031d = _celda(s, a413 == 1, v413, segs)
    put("AUTOR031-DEMOCRACIA-PREFERIBLE", c031d)
    lo, hi = (None, None)
    if c031[1] is not None and c031d[1] is not None:
        lo, hi = _pct(c031d[1] - c031[1])
    pa, pb = out[P + "AUTOR031-DEMOCRACIA-PREFERIBLE"], out[P + "AUTOR031-NO-DEMOCRATICO-O-INDIFERENTE"]
    out[P + "AUTOR031-DIF-DEMOCRACIA-MENOS-NODEM"] = (
        None if pa is None or pb is None else pa - pb)
    out[P + "AUTOR031-DIF-DEMOCRACIA-MENOS-NODEM-IC95-INF"] = lo
    out[P + "AUTOR031-DIF-DEMOCRACIA-MENOS-NODEM-IC95-SUP"] = hi

    # ---------------- Tabla SEC_6_7_8: regla RG-67c84a2224 ----------------
    t = Survey(rows678, replicas, seed)
    segt = _segmentos(t.rows, sd)
    out[P + "SEC678-N-FILAS"] = len(rows678)
    out[P + "SEC678-JOIN-SD-N"] = int(sum(
        1 for r in t.rows if str(r.get("ID_PER", "")).strip() in sd))
    b69 = np.asarray([_code(r.get("AP6_9")) for r in t.rows], dtype=object)
    b610 = np.asarray([_code(r.get("AP6_10")) for r in t.rows], dtype=object)
    b611 = np.asarray([_code(r.get("AP6_11")) for r in t.rows], dtype=object)
    b715 = np.asarray([_code(r.get("AP7_15")) for r in t.rows], dtype=object)
    uni = (_in(b610, (1,)) & _in(b611, (2,)) & _in(b69, (1, 2))
           & _in(b715, (1, 2)))
    derecho = _in(b69, (2,))
    secreto = _in(b715, (1,))
    put("RG67C8-CONJUNTA-DERECHO-Y-SECRETO", _celda(t, derecho & secreto, uni, segt))
    put("RG67C8-SECRETO", _celda(t, secreto, uni, segt))
    put("RG67C8-DERECHO", _celda(t, derecho, uni, segt))
    return out


def medir(inputs, contrato):
    path = inputs[PAYLOAD_ID]["ruta_absoluta"]
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()

        def leer(member, cols):
            m = [x for x in names if x.rsplit("/", 1)[-1] == member]
            if len(m) != 1:
                raise ValueError(f"miembro {member}: coincidencias={len(m)}")
            return _read_dbf(archive.read(m[0]), cols)
        r45, r678, rsd = leer(M45, C45), leer(M678, C678), leer(MSD, CSD)
    par = contrato["parametros"]
    return measure(r45, r678, rsd, int(par["bootstrap_replicas"]),
                   int(contrato["seed"]["valor"]))

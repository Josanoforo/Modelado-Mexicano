"""Extracción descriptiva de tabulados oficiales INEGI (unidad económica):
proporción = absolutos / total del dominio, con control de fórmula contra la
tasa o el relativo publicados.

El primer resultado que produzca este procedimiento es el que se reporta.
Gobernado por la spec humana que cita `spec_md`. Los tabulados no publican
EE, CV ni n muestral: no se construye IC (incertidumbre NO-DISPONIBLE). Qué
tabla, qué fila y qué columna vienen en `parametros`, por encabezado verbatim;
el medidor no elige ninguna.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
import zipfile
from pathlib import Path


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def _num(s):
    t = (s or "").strip().replace(",", "")
    return float(t) if re.fullmatch(r"-?\d+(\.\d+)?", t) else None


def _lee(zf, sufijo, encoding):
    cands = [n for n in zf.namelist() if n.endswith("/" + sufijo)]
    if len(cands) != 1:
        raise ValueError(f"tabla {sufijo}: {len(cands)} miembros")
    texto = zf.read(cands[0]).decode(encoding)
    return cands[0], [r for r in csv.reader(io.StringIO(texto)) if any(c.strip() for c in r)]


def medir(inputs, contrato):
    par = contrato["parametros"]
    pid = par["payload_id"]
    ruta = inputs[pid]["ruta_absoluta"]
    if _sha(ruta) != par["hash_payload_sha256"]:
        raise ValueError("GUARDIA: sha256 del payload no es el fijado")
    out = {}
    tabla = {"_incertidumbre": "NO-DISPONIBLE-EN-TABULADO", "_n_muestral": "NO-PUBLICADO"}
    max_delta = 0.0
    with zipfile.ZipFile(ruta) as zf:
        for t in par["tablas"]:
            miembro, filas = _lee(zf, t["archivo"], par["encoding"])
            cab = [_norm(c) for c in filas[0]]

            def col(h):
                hh = _norm(h)
                idx = [i for i, c in enumerate(cab) if c == hh]
                if len(idx) != 1:
                    raise ValueError(f"{t['archivo']}: encabezado '{h}' casa {len(idx)} columnas")
                return idx[0]

            den_i = col(t["denominador"])
            por_dom = {_norm(r[0]): r for r in filas[1:]}
            for dom in t["dominios"]:
                r = por_dom.get(_norm(dom))
                if r is None:
                    raise ValueError(f"{t['archivo']}: dominio '{dom}' ausente")
                den = _num(r[den_i])
                for ind in t["indicadores"]:
                    num = _num(r[col(ind["numerador"])])
                    pub = _num(r[col(ind["publicado"])])
                    clave = f"{t['clave']}|{dom}|{ind['clave']}"
                    if den in (None, 0.0) or num is None:
                        tabla[clave] = {"estado": "NO-ESTIMABLE", "p": None}
                        continue
                    p = num / den
                    delta = None if pub is None else abs(p - pub / float(ind["escala_publicado"]))
                    if delta is not None:
                        max_delta = max(max_delta, delta)
                    tabla[clave] = {"estado": "EXTRAIDA", "p": p, "absolutos": num,
                                    "denominador": den, "publicado": pub,
                                    "delta_formula": delta, "miembro": miembro}
    tabla["_max_delta_formula"] = max_delta
    tabla["_control_formula"] = "PASA" if max_delta <= float(par["tolerancia_formula"]) else "FALLA"
    out[par["result_tabla"]] = json.dumps(tabla, ensure_ascii=False, sort_keys=True,
                                          separators=(",", ":"), allow_nan=False)
    out[par["result_control"]] = tabla["_control_formula"]
    return out

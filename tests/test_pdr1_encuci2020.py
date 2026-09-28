#!/usr/bin/env python3
"""GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · pieza P-ENCUCI2020 · prueba sintética del COMMIT-1.

Fabrica un zip con la forma de BD_ENCUCI2020_dbf.zip (miembros SEC_4_5,
SEC_6_7_8 y SD en DBF con campos C/N como el real) y exige que `medir()`
devuelva exactamente los ids de `spec.yaml` y que `corrida0._valida_outputs`
salga vacía; también la rama degenerada (sin válidos -> None declarado).
"""
from __future__ import annotations

import importlib.util
import io
import struct
import sys
import zipfile
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-PDR1-ENCUCI2020-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_pdr1_encuci", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _dbf(fields, rows):
    """fields: [(name, tipo 'C'|'N', ancho)]."""
    rsize = 1 + sum(w for _, _, w in fields)
    hsize = 32 + 32 * len(fields) + 1
    head = struct.pack("<BBBBIHH20x", 3, 126, 1, 1, len(rows), hsize, rsize)
    desc = b""
    for n, t, w in fields:
        desc += n.encode().ljust(11, b"\0") + t.encode() + b"\0" * 4 + bytes([w, 0]) + b"\0" * 14
    body = b""
    for r in rows:
        rec = b" "
        for n, t, w in fields:
            v = str(r.get(n, ""))
            rec += (v.rjust(w) if t == "N" else v.ljust(w)).encode("latin-1")[:w]
        body += rec
    return head + desc + b"\r" + body + b"\x1a"


def _fabrica(degenerado=False):
    rng = np.random.default_rng(1)
    r45, r678, rsd = [], [], []
    for i in range(400):
        pid = f"{i // 4:07d}.01.{i % 4 + 1:02d}"
        est, upm = f"{i % 10:03d}", f"{i // 4:07d}"
        dom = "UCR"[i % 3]
        fac = f"{float(rng.integers(50, 500)):.10f}"
        c = (lambda k: "9") if degenerado else (lambda k: str(rng.integers(1, k + 1)))
        r45.append({"ID_PER": pid, "AP4_9_1": c(4), "AP4_9_4": c(4), "AP4_13": c(4),
                    "AP5_1_4": "99" if degenerado else f"{rng.integers(0, 11):02d}",
                    "AP5_11": c(4), "FAC_SEL": fac, "EST_DIS": est, "UPM_DIS": upm,
                    "DOMINIO": dom})
        r678.append({"ID_PER": pid, "AP6_9": c(2), "AP6_10": c(2), "AP6_11": c(2),
                     "AP7_15": c(2), "FAC_SEL": fac, "EST_DIS": est, "UPM_DIS": upm,
                     "DOMINIO": dom})
        rsd.append({"ID_PER": pid, "SEXO": str(1 + i % 2), "EDAD": str(15 + i % 80)})
    f45 = [("ID_PER", "C", 13), ("AP4_9_1", "N", 19), ("AP4_9_4", "N", 19),
           ("AP4_13", "C", 6), ("AP5_1_4", "C", 7), ("AP5_11", "N", 19),
           ("FAC_SEL", "N", 19), ("DOMINIO", "C", 7), ("UPM_DIS", "C", 7), ("EST_DIS", "C", 7)]
    f678 = [("ID_PER", "C", 13), ("AP6_9", "N", 19), ("AP6_10", "N", 19), ("AP6_11", "N", 19),
            ("AP7_15", "N", 19), ("FAC_SEL", "N", 19), ("DOMINIO", "C", 7),
            ("UPM_DIS", "C", 7), ("EST_DIS", "C", 7)]
    fsd = [("ID_PER", "C", 13), ("SEXO", "C", 4), ("EDAD", "C", 4)]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("ENCUCI_2020_SEC_4_5.dbf", _dbf(f45, r45))
        z.writestr("ENCUCI_2020_SEC_6_7_8.dbf", _dbf(f678, r678))
        z.writestr("ENCUCI_2020_SD.dbf", _dbf(fsd, rsd))
    return buf.getvalue()


def _corre(tmp_path, degenerado):
    import corrida0
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    p = tmp_path / "BD_ENCUCI2020_dbf.zip"
    p.write_bytes(_fabrica(degenerado))
    contrato = {"parametros": {"bootstrap_replicas": 50}, "seed": {"valor": 42}}
    out = _load().medir({"encuci2020_bd_dbf": {"ruta_absoluta": str(p)}}, contrato)
    return corrida0._valida_outputs(spec, out), out


def test_sintetico(tmp_path):
    problemas, out = _corre(tmp_path, False)
    assert problemas == []
    assert out["RESULT-PDR1-ENCUCI2020-SEC45-JOIN-SD-N"] == 400
    assert out["RESULT-PDR1-ENCUCI2020-AUTOR001-LIDER-FUERTE-ACUERDO"] is not None


def test_degenerado(tmp_path):
    problemas, out = _corre(tmp_path, True)
    assert problemas == []
    assert out["RESULT-PDR1-ENCUCI2020-AUTOR001-LIDER-FUERTE-ACUERDO"] is None

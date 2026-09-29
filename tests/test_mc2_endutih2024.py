#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENDUTIH 2024 · prueba sintética del COMMIT-1.

Escribe un dBase III mínimo con la forma de `tic_2024_usuarios.DBF` (campos C, un registro borrado), lo lee con
el lector sellado `tests/dbfmini.py` a través de `medir()` y exige `corrida0._valida_outputs(spec, out) == []`,
respuestas conocidas (uso por edad, horas, WhatsApp entre usuarios) y el camino degenerado (sin 65+ -> None).
Uso: python3 tests/test_mc2_endutih2024.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENDUTIH2024-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_endutih2024", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _dbf(path, campos, filas, borrado=None):
    ancho = {c: 10 for c in campos}
    hdr_len = 32 + 32 * len(campos) + 1
    rec_len = 1 + sum(ancho.values())
    with open(path, "wb") as f:
        f.write(struct.pack("<BBBBIHH20x", 3, 126, 9, 28, len(filas) + (1 if borrado else 0), hdr_len, rec_len))
        for c in campos:
            f.write(c.encode().ljust(11, b"\0") + b"C" + b"\0" * 4 + bytes([ancho[c], 0]) + b"\0" * 14)
        f.write(b"\x0d")
        for i, r in enumerate(filas + ([borrado] if borrado else [])):
            f.write(b"*" if r is borrado else b" ")
            for c in campos:
                f.write(str(r.get(c, "")).encode("latin-1")[:ancho[c]].ljust(ancho[c]))
        f.write(b"\x1a")


def _fabrica(tmp, med, n=900, sin_viejos=False):
    filas = []
    for i in range(n):
        edad = 18 + i % 40 if sin_viejos else 18 + i % 60
        usa = "1" if (i % 4 != 0 or edad < 25) else "2"
        filas.append({"EDAD": edad, "FAC_PER": 100, "EST_DIS": f"{1 + i % 8:03d}", "UPM_DIS": f"{1 + i % 40:05d}",
                      "P7_1": usa, "P7_3": "1" if usa == "1" else "", "P7_4": "06" if usa == "1" else "",
                      "P7_15": ("1" if i % 3 else "2") if usa == "1" else "",
                      "P7_16_6": ("1" if i % 3 else "") if usa == "1" else "", "OTRA": "x"})
    dbf = tmp / med.MIEMBRO
    _dbf(dbf, list(med.CAMPOS) + ["OTRA"], filas, borrado={"EDAD": 30, "P7_1": "2", "FAC_PER": 100})
    z = tmp / "endutih.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.write(dbf, med.MIEMBRO)
    return z


def corre(sin_viejos=False, reps=40):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z = _fabrica(Path(t), med, sin_viejos=sin_viejos)
        return med.medir({med.PAYLOAD: {"ruta_absoluta": str(z)}, med.LECTOR: {"ruta_absoluta": str(RAIZ / "tests/dbfmini.py")}},
                         {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}})


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    P = med.PFX
    assert out[f"{P}-DIAG-FILAS"] == 900                      # el registro borrado no entra
    assert out[f"{P}-INTERNET-EDAD-18-24-P"] == 1.0
    assert abs(out[f"{P}-HORAS-DIA-NAC-P"] - 6.0) < 1e-9
    assert out[f"{P}-WHATSAPP-USUARIOS-REDES-NAC-P"] == 1.0
    assert abs(out[f"{P}-WHATSAPP-USUARIOS-INTERNET-NAC-P"] - 2 / 3) < 0.02
    out2 = corre(sin_viejos=True)
    assert out2[f"{P}-INTERNET-EDAD-65-MAS-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_endutih2024")

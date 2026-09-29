#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENVIPE 2025 · prueba sintética del COMMIT-1.

Fabrica zips con la forma de envipe2025_csv / envipe2024_csv (CSV con fin de
línea `\\r` solo, cabecera entrecomillada, rutas `…/conjunto_de_datos/…`), corre
`medir()` y exige `corrida0._valida_outputs(spec, out) == []`, respuestas
conocidas (cifra negra, denuncia, extorsión telefónica, Sinaloa 2025−2024) y el
camino degenerado (sin extorsiones -> None).
Uso: python3 tests/test_mc2_envipe2025.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENVIPE2025-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_envipe2025", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _csv(cols, rows):
    out = [",".join(f'"{c}"' for c in cols)]
    for r in rows:
        out.append(",".join(f'"{r.get(c, "")}"' for c in cols))
    return ("\r".join(out) + "\r").encode("utf-8")


def _fabrica(tmp: Path, med, n=1200, sin_ext=False):
    dl, p24, p25 = [], [], []
    for i in range(n):
        dis = {"EST_DIS": f"{1 + i % 8:03d}", "UPM_DIS": f"{1 + i % 50:05d}", "DOMINIO": "URC"[i % 3]}
        # delitos: 1 de cada 10 denunciado; de esos, la mitad con carpeta -> cifra negra 0.95
        den = "1" if i % 10 == 0 else "2"
        dl.append({**dis, "FAC_DEL": "100", "SEXO": str(1 + i % 2),
                   "BPCOD": ("09" if (i % 4 == 0 and not sin_ext) else "01"),
                   "BP1_20": den, "BP1_21": "2" if den == "2" else "",
                   "BP1_24": ("1" if i % 20 == 0 else "2") if den == "1" else "",
                   "BP1_5A_2": ("1" if i % 8 == 0 else "0") if (i % 4 == 0 and not sin_ext) else ""})
        base = {**dis, "FAC_ELE": "50", "SEXO": str(1 + i % 2), "EDAD": str(18 + i % 70),
                "CVE_ENT": ("25" if i % 5 == 0 else "09")}
        r24 = {**base, "AP4_3_3": ("2" if (i % 5 == 0 and i % 2 == 0) else "1"),
               "AP4_10_01": "1" if i % 3 == 0 else ("3" if i % 7 == 0 else "2")}
        for k in range(1, 14):
            r24[f"AP4_2_{k:02d}"] = "1" if k == 5 else "0"
        r24["AP4_2_99"] = "0"
        for col in med.AP44.values():
            r24[col] = "2" if i % 2 else "1"
        p24.append(r24)
        p25.append({**base, "AP4_3_3": ("2" if i % 5 == 0 else "1")})
    z25, z24 = tmp / "e25.zip", tmp / "e24.zip"
    extra = ["ID_DEL", "OTRA"]
    with zipfile.ZipFile(z25, "w") as z:
        z.writestr("tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv",
                   _csv(extra + med.COLS_DEL, dl))
        z.writestr("tper_vic1_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2025.csv",
                   _csv(extra + med.COLS_PER25, p25))
    with zipfile.ZipFile(z24, "w") as z:
        z.writestr("tper_vic1_envipe2024/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2024.csv",
                   _csv(extra + med.COLS_PER24, p24))
    return z24, z25


def corre(sin_ext=False, reps=60):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z24, z25 = _fabrica(Path(t), med, sin_ext=sin_ext)
        inputs = {med.P24: {"ruta_absoluta": str(z24)}, med.P25: {"ruta_absoluta": str(z25)}}
        contrato = {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}}
        return med.medir(inputs, contrato)


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    P = med.PFX
    assert abs(out[f"{P}-DEL-DENUNCIA-NAC-P"] - 0.10) < 1e-9
    assert abs(out[f"{P}-DEL-CIFRA-NEGRA-NAC-P"] - 0.95) < 1e-9
    assert abs(out[f"{P}-DEL-EXT-TELEFONICA-NAC-P"] - 0.5) < 1e-9
    assert abs(out[f"{P}-EDO-INSEGURO-2025-SINALOA-P"] - 1.0) < 1e-9
    assert abs(out[f"{P}-EDO-INSEGURO-2024-SINALOA-P"] - 0.5) < 1e-9
    assert abs(out[f"{P}-EDO-INSEGURO-SINALOA-DIF-2025-2024-P"] - 0.5) < 1e-9
    assert out[f"{P}-PREOC-INSEGURIDAD-2024-NAC-P"] == 1.0 and out[f"{P}-PREOC-AGUA-2024-NAC-P"] == 0.0
    out2 = corre(sin_ext=True)
    assert out2[f"{P}-DEL-EXT-TELEFONICA-NAC-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_envipe2025")

#!/usr/bin/env python3
"""PDR1 pieza ENADID2023 · prueba sintética del medidor congelado.

Fabrica un zip con la forma real de base_datos_enadid23_csv.zip (miembros,
cabecera completa de TSDEM en minúsculas, comillas, CRLF, sin BOM) y exige:
ids devueltos == ids del spec.yaml, `_valida_outputs == []`, todo str
<= 1024 bytes, y que el dictamen B-bis sale por la rama esperada.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import zipfile

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALC = os.path.join(ROOT, "data", "corrida0", "CALC-PDR1-ENADID2023-0001")

HEADER = ('upm,viv_sel,hogar,n_ren,llave_viv,llave_hog,llave_per,ent,tam_loc,paren,paren_c,sexo,edad,'
          'p3_4,p3_5,p3_5a,p3_6,p3_6a,p3_7,p3_8_1,p3_9_1,p3_8_2,p3_9_2,p3_8_3,p3_9_3,p3_8_4,p3_9_4,'
          'p3_8_5,p3_9_5,p3_8_6,p3_9_6,p3_8_7,p3_9_7,p3_8_8,p3_9_8,p3_10,p3_10c,p3_11,p3_12,p3_13,'
          'p3_14a1,p3_14b1,p3_14a2,p3_14b2,p3_14a3,p3_14b3,p3_14a4,p3_14b4,p3_14a5,p3_14b5,p3_14a6,'
          'p3_14b6,p3_14a7,p3_14b7,p3_14a8,p3_14b8,p3_15,p3_16,p3_16c,p3_17,p3_17c,p3_18,p3_18c,p3_19,'
          'p3_20c,p3_21,niv,gra,p3_23,p3_24,p3_24c,p3_25,p3_25c,p3_26,p3_26c,p3_27,p3_28_1,p3_28_2,'
          'p3_28_3,p3_28_4,p3_28_5,p3_28_6,p3_28_7,p3_29,p3_30,p3_31,p3_32,fac_viv,t_loc_ur,t_loc_ag1,'
          'con_ele,edad_1ag,edad_2ag,par_ag,niv_esc,esco_acum,c_afil,p3_27_ag,cond_act,c_limdisc,'
          'estrato,est_dis,upm_dis').split(",")
MIEMBROS = ["nota_bases_datos_enadid_2023.txt", "TFECHISEMB.csv", "THOGAR.csv", "TMIGRANTE.csv",
            "TMUJER1.csv", "TMUJER2.csv", "TSDEM.csv", "TVIVIENDA.csv"]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def fabrica(path, n=6000, seed=7):
    rng = np.random.default_rng(seed)
    lines = [",".join(f'"{h}"' for h in HEADER)]
    for i in range(n):
        row = {h: "" for h in HEADER}
        est = 1 + i % 32
        row.update(sexo=str(rng.integers(1, 3)), edad=f"{int(rng.choice([rng.integers(0, 110), 999])):03d}",
                   p3_12=str(rng.choice(["1", "2", ""], p=[.2, .75, .05])),
                   p3_23=str(rng.choice(["1", "2", "9"], p=[.85, .13, .02])),
                   t_loc_ur=str(rng.integers(1, 3)), fac_viv=str(int(rng.integers(14, 5772))),
                   est_dis=f"{est:03d}", upm_dis=f"{est * 10 + (i % 3 if est != 5 else 0):05d}",
                   ent=f"{est:02d}")
        ind, an = row["p3_12"] == "1", row["p3_23"] == "2"
        if ind and rng.random() < .3:
            row["p3_23"] = "2"
        elif not ind and an and rng.random() < .7:
            row["p3_23"] = "1"
        lines.append(",".join(f'"{row[h]}"' for h in HEADER))
    body = ("\r\n".join(lines) + "\r\n").encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for m in MIEMBROS:
            z.writestr(m, body if m == "TSDEM.csv" else b"x\r\n")


def corre(tmp):
    med = _load(os.path.join(CALC, "medidor.py"), "medidor_pdr1_enadid2023")
    contrato = yaml.safe_load(open(os.path.join(CALC, "spec.yaml"), encoding="utf-8"))
    p = os.path.join(tmp, "base_datos_enadid23_csv.zip")
    fabrica(p)
    out = med.medir({"enadid2023_base_datos_csv": {"ruta_absoluta": p}}, contrato)
    return contrato, out


def test_sintetico(tmp_path):
    c0 = _load(os.path.join(ROOT, "tools", "corrida0.py"), "corrida0_pdr1_enadid")
    contrato, out = corre(str(tmp_path))
    assert c0._valida_outputs(contrato, out) == []
    assert {r["id"] for r in contrato["resultados"]} == set(out)
    for k, v in out.items():
        if isinstance(v, str):
            assert len(v.encode("utf-8")) <= 1024, k
    assert out["RESULT-PDR1-ENADID2023-DICTAMEN-BBIS"] in {"CONFIRMA", "MATIZA", "ROMPE"}
    assert out["RESULT-PDR1-ENADID2023-BRECHA-TOTAL"] > 0
    assert out["RESULT-PDR1-ENADID2023-N-ESTRATOS-SINGLETON"] == 1


if __name__ == "__main__":  # imprime el bloque resultados: derivado del medidor
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        _, out = corre(t)
    for k, v in out.items():
        tipo = "texto" if isinstance(v, str) else ("entero" if isinstance(v, int) else "proporcion")
        print(k, tipo)

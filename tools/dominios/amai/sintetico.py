"""Payloads sintéticos con la forma real de ENIGH 2022, ENIF 2021/2024 y
ENDUTIH 2023-2025, para probar el conducto sin tocar el corpus (E.5).

Valores aleatorios con semilla fija; los códigos respetan los FD citados en
la spec. `rama` fuerza caminos terminales: 'normal', 'rara' (pocos hogares:
todo SUPRIMIDA-N) y 'sin_nse' (un componente ausente en todos los hogares).
"""
from __future__ import annotations

import io
import struct
import zipfile
from pathlib import Path

import numpy as np


def _dbf_bytes(campos: list[str], filas: list[dict]) -> bytes:
    anchos = {c: max([len(c)] + [len(str(f.get(c, ""))) for f in filas] + [1]) for c in campos}
    anchos = {c: min(max(w, 1), 254) for c, w in anchos.items()}
    rec = 1 + sum(anchos.values())
    head = 32 + 32 * len(campos) + 1
    out = io.BytesIO()
    out.write(struct.pack("<BBBBIHH20x", 3, 126, 1, 1, len(filas), head, rec))
    for c in campos:
        out.write(struct.pack("<11sc4xBB14x", c.encode("latin-1")[:11], b"C", anchos[c], 0))
    out.write(b"\x0d")
    for f in filas:
        out.write(b" ")
        for c in campos:
            out.write(str(f.get(c, "")).ljust(anchos[c])[:anchos[c]].encode("latin-1"))
    out.write(b"\x1a")
    return out.getvalue()


def _csv_bytes(campos: list[str], filas: list[dict], bom: bool = True) -> bytes:
    lineas = [",".join(f'"{c}"' for c in campos)]
    lineas += [",".join(f'"{f.get(c, "")}"' for c in campos) for f in filas]
    texto = "\r\n".join(lineas) + "\r\n"
    return (b"\xef\xbb\xbf" if bom else b"") + texto.encode("utf-8")


def _diseno(rng, i):
    upm = i // 4
    return {"est": f"{(upm % 6) + 1:03d}", "upm": f"{upm:05d}"}


# ------------------------------------------------------------------ ENIGH

def enigh2022(ruta: Path, n: int = 1200, rama: str = "normal", semilla: int = 1) -> Path:
    rng = np.random.default_rng(semilla)
    hog, con, viv = [], [], []
    for i in range(n):
        fv, fh = f"{i:010d}", "1"
        d = _diseno(rng, i)
        viv.append({"folioviv": fv, "cuart_dorm": int(rng.integers(0, 6)),
                    "bano_comp": "" if rama == "sin_nse" else int(rng.integers(0, 4)),
                    "est_dis": d["est"], "upm": d["upm"], "factor": 100})
        hog.append({"folioviv": fv, "foliohog": fh, "conex_inte": int(rng.integers(1, 3)),
                    "num_auto": int(rng.integers(0, 3)), "num_van": int(rng.integers(0, 2)),
                    "num_pickup": 0, "est_dis": d["est"], "upm": d["upm"], "factor": 100})
        con.append({"folioviv": fv, "foliohog": fh, "educa_jefe": f"{int(rng.integers(1, 12)):02d}",
                    "ocupados": int(rng.integers(0, 6)), "upm": d["upm"], "est_dis": d["est"],
                    "factor": int(rng.integers(50, 400)),
                    "remesas": float(rng.choice([0, 0, 0, 1500.5]))})
    base = "conjunto_de_datos_{t}_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_{t}_enigh2022_ns.csv"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr(base.format(t="hogares"), _csv_bytes(list(hog[0]), hog, bom=True))
        z.writestr(base.format(t="concentradohogar"), _csv_bytes(list(con[0]), con, bom=True))
        z.writestr(base.format(t="viviendas"), _csv_bytes(list(viv[0]), viv, bom=True))
    return ruta


# ------------------------------------------------------------------- ENIF

def enif(ruta: Path, ola: str, n: int = 1200, rama: str = "normal", semilla: int = 2) -> Path:
    rng = np.random.default_rng(semilla)
    viv, hog, sdem, mod = [], [], [], []
    nivmax = 9 if ola == "2021" else 11
    for i in range(n):
        d = _diseno(rng, i)
        folio, vs, h = f"{i // 2:05d}", f"{i % 2 + 1:02d}", "1"
        lviv, lhog = folio + vs, folio + vs + h
        tiene_auto = rng.integers(1, 3)
        tiene_int = rng.integers(1, 3)
        v = {"P0_1": f"{int(rng.integers(1, 5)):02d}",
             "P0_3": "" if rama == "sin_nse" else f"{int(rng.integers(0, 4)):02d}",
             "P0_4_1": str(tiene_auto), "P0_4_1A": str(int(rng.integers(1, 4))) if tiene_auto == 1 else "",
             "P0_4_2": str(tiene_int), "P0_4_2A": str(int(rng.integers(1, 3))) if tiene_int == 1 else "",
             "EST_DIS": d["est"], "UPM_DIS": d["upm"], "FAC_VIV": 100}
        hg = {"P2_8": f"{int(rng.integers(0, 5)):02d}", "EST_DIS": d["est"],
              "UPM_DIS": d["upm"], "FAC_HOG": int(rng.integers(50, 400))}
        niv = int(rng.integers(0, nivmax + 1))
        s = {"NIV": f"{niv:02d}", "GRA": str(int(rng.integers(1, 7)))}
        if ola == "2024":
            viv.append({"LLAVEVIV": lviv, **v})
            hog.append({"LLAVEHOG": lhog, "LLAVEVIV": lviv, **hg})
            sdem.append({"LLAVESDE": lhog + "01", "LLAVEVIV": lviv, "LLAVEHOG": lhog,
                         "PAREN": "1", **s})
            sdem.append({"LLAVESDE": lhog + "02", "LLAVEVIV": lviv, "LLAVEHOG": lhog,
                         "PAREN": "3", "NIV": "02", "GRA": "3"})
            m = {"LLAVEMOD": lhog + "01", "LLAVEVIV": lviv, "LLAVEHOG": lhog}
        else:
            viv.append({"FOLIO": folio, "VIV_SEL": vs, **v})
            hog.append({"FOLIO": folio, "VIV_SEL": vs, "HOGAR": h, **hg})
            sdem.append({"FOLIO": folio, "VIV_SEL": vs, "HOGAR": h, "N_REN": "01", "P2_3": "1", **s})
            m = {"FOLIO": folio, "VIV_SEL": vs, "HOGAR": h, "N_REN": "01"}
        ah = [str(int(rng.integers(1, 3))) for _ in range(15)]
        p38 = str(rng.choice(["1", "8"]))
        m.update({"EDAD_V": str(int(rng.integers(18, 90))), "FAC_PER": int(rng.integers(50, 900)),
                  "FAC_ELE": int(rng.integers(50, 900)),
                  "EST_DIS": d["est"], "UPM_DIS": d["upm"],
                  "P3_8": p38, "P3_9": "7" if p38 == "8" else "",
                  "P4_10": str(int(rng.integers(1, 6))),
                  "P3_13": str(rng.choice(["1", "2", "7"])),
                  "P5_20": "", "P5_23": str(rng.choice(["1", "2"])),
                  "FILTRO_S9_1": str(rng.choice(["1", "2"])),
                  "P9_9_4": str(rng.choice(["1", "2"]))})
        for j in range(6):
            m[f"P5_1_{j + 1}"] = ah[j]
        for j in range(9):
            m[f"P5_6_{j + 1}"] = ah[6 + j]
            m[f"P5_4_{j + 1}"] = "1" if j == 0 and i % 3 else "2"
        if m["P5_4_1"] == "2":
            m["P5_20"] = f"{int(rng.integers(1, 11)):02d}"
        mod.append(m)
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("conjunto_de_datos/TVIVIENDA.csv", _csv_bytes(list(viv[0]), viv))
        z.writestr("conjunto_de_datos/THOGAR.csv", _csv_bytes(list(hog[0]), hog))
        z.writestr("conjunto_de_datos/TSDEM.csv", _csv_bytes(list(sdem[0]), sdem))
        z.writestr("conjunto_de_datos/TMODULO.csv", _csv_bytes(list(mod[0]), mod))
    return ruta


# ---------------------------------------------------------------- ENDUTIH

def endutih(ruta: Path, ola: str, n: int = 1200, rama: str = "normal", semilla: int = 3) -> Path:
    from tools.dominios.amai.componentes import ENDUTIH
    from tools.dominios.endutih.pisos import FILES
    rng = np.random.default_rng(semilla)
    fviv, fhog, fres = ENDUTIH[ola]
    fusu, fusu2, ent = FILES[ola]
    viv, hog, res, usu, usu2 = [], [], [], [], []
    for i in range(n):
        d = _diseno(rng, i)
        k = {"UPM": f"{i // 3:07d}", "VIV_SEL": f"{i % 3 + 1:02d}"}
        viv.append({**k, "P1_5_3": str(int(rng.integers(1, 3))), "FAC_VIV": 100,
                    "EST_DIS": d["est"], "UPM_DIS": d["upm"]})
        p44 = str(int(rng.integers(1, 3)))
        hog.append({**k, "HOGAR": "1", "P4_4": "" if rama == "sin_nse" else p44,
                    "P4_5": str(int(rng.integers(1, 4))) if p44 == "1" else "",
                    "FAC_HOG": int(rng.integers(50, 400)), "EST_DIS": d["est"], "UPM_DIS": d["upm"]})
        for r in range(1, 4):
            edad = int(rng.integers(6, 80)) if r < 3 else int(rng.integers(0, 14))
            res.append({**k, "HOGAR": "1", "NUM_REN": f"{r:02d}", "PAREN": "1" if r == 1 else "3",
                        "EDAD": str(edad), "NIVEL": f"{int(rng.integers(0, 12)):02d}",
                        "GRADO": str(int(rng.integers(1, 7))),
                        "P3_10": str(int(rng.integers(1, 10))) if edad >= 6 else "",
                        "P3_11": str(int(rng.integers(1, 5)))})
        p71, p81 = str(int(rng.integers(1, 3))), str(int(rng.integers(1, 3)))
        u = {**k, "HOGAR": "1", "NUM_REN": "01", "EDAD": str(int(rng.integers(6, 90))),
             "SEXO": "1", "NIVEL": "03", "TLOC": "1", ent: "01",
             "FAC_PER": int(rng.integers(50, 900)), "EST_DIS": d["est"], "UPM_DIS": d["upm"],
             "P7_1": p71, "P7_2": str(int(rng.integers(1, 9))) if p71 == "2" else "",
             "P7_10_2": str(int(rng.integers(1, 3))) if p71 == "1" else "",
             "P7_12_3": str(int(rng.integers(1, 3))) if p71 == "1" else "",
             "P7_35_4": str(int(rng.integers(1, 3))) if p71 == "1" else ""}
        usu.append(u)
        usu2.append({**{c: u[c] for c in ("UPM", "VIV_SEL", "HOGAR", "NUM_REN")},
                     "P8_1": p81, "P8_2": str(int(rng.integers(1, 9))) if p81 == "2" else ""})
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr(fviv, _dbf_bytes(list(viv[0]), viv))
        z.writestr(fhog, _dbf_bytes(list(hog[0]), hog))
        z.writestr(fres, _dbf_bytes(list(res[0]), res))
        z.writestr(fusu, _dbf_bytes(list(usu[0]), usu))
        z.writestr(fusu2, _dbf_bytes(list(usu2[0]), usu2))
    return ruta

#!/usr/bin/env python3
"""Ejecuta el PROCEDIMIENTO R v1.0 + ENMIENDA 1. COMMIT-2 de ACTO E7 R-SCORING.

No reimplementa nada: el estimador y su EE salen de tests/svystat.py
(prop_ultimate_cluster, conglomerado ultimo), importado tal cual.
Escribe un JSON por celda arbitrable en el directorio de este script.
"""
import csv, io, json, os, re, sys, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(RAIZ, "tests"))
import dbfmini
from svystat import prop_ultimate_cluster

RAW = os.path.join(RAIZ, "data", "raw")
AQUI = os.path.dirname(os.path.abspath(__file__))
TMP = os.environ.get("TMPDIR", "/tmp")


def csv_zip(zpath, member):
    """Filas de un CSV dentro de un zip, como dicts con claves en minuscula."""
    with zipfile.ZipFile(os.path.join(RAW, zpath)) as z:
        with z.open(member) as fh:
            for row in csv.DictReader(io.TextIOWrapper(fh, encoding="latin-1")):
                yield {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}


def dbf_zip(zpath, member, campos=None):
    with zipfile.ZipFile(os.path.join(RAW, zpath)) as z:
        p = os.path.join(TMP, "_e7_" + os.path.basename(member))
        with open(p, "wb") as o:
            o.write(z.read(member))
    try:
        for row in dbfmini.read_dbf(p, wanted_fields=campos):
            yield {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
    finally:
        os.remove(p)


def num(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None


def estima(filas, col_y, uno, cero, col_w, col_est, col_upm, filtro=None):
    """filas -> (estrato, upm, peso, y) segun la regla congelada. Devuelve el dict de svystat + conteos."""
    rows, n_bruto, n_excl_cod, n_excl_filtro, n_sin_peso = [], 0, 0, 0, 0
    for f in filas:
        n_bruto += 1
        if filtro and not filtro(f):
            n_excl_filtro += 1
            continue
        v = str(f.get(col_y, "")).strip()
        if v in uno:
            y = 1.0
        elif v in cero:
            y = 0.0
        else:
            n_excl_cod += 1
            continue
        w = num(f.get(col_w))
        if w is None or w <= 0:
            n_sin_peso += 1
            continue
        rows.append((str(f.get(col_est, "")), str(f.get(col_upm, "")), w, y))
    r = prop_ultimate_cluster(rows) if rows else None
    return r, {"n_filas_leidas": n_bruto, "n_fuera_de_universo": n_excl_filtro,
               "n_codigo_no_valido": n_excl_cod, "n_sin_ponderador": n_sin_peso,
               "n_efectivo": len(rows)}


def escribe(cid, spec, res, conteos, extra=None):
    if res is None:
        doc = {"id_celda": cid, "estado": "SIN_FILAS", **spec, **conteos}
    else:
        cv = (res["se"] / res["p_hat"]) if res["p_hat"] else None
        doc = {"id_celda": cid, "estado": "COMPUTADO", **spec,
               "R": res["p_hat"], "EE_R": res["se"],
               "ic95_lo": res["ic95"][0], "ic95_hi": res["ic95"][1],
               "cv": cv, "cv_pct": (cv * 100 if cv is not None else None),
               "n_estratos": res["n_estratos"], "n_upm_total": res["n_upm_total"],
               "n_estratos_singleton": res["n_estratos_singleton"], **conteos}
    if extra:
        doc.update(extra)
    with open(os.path.join(AQUI, f"{cid}.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    return doc


# ── Las nueve celdas arbitrables ───────────────────────────────────────────

def celda_CIV_08():
    spec = {"encuesta": "ENVIPE", "ola": "2023", "payload_id": "envipe2023_csv",
            "tabla": "tper_vic1_envipe2023/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2023.csv",
            "variable": "AP4_4_03", "ponderador": "FAC_ELE", "estrato": "EST_DIS", "upm": "UPM_DIS",
            "codificacion": "y=1 si AP4_4_03=='2' (Inseguro); y=0 si=='1' (Seguro); 3 y 9 fuera",
            "universo": "poblacion de 18 anios y mas (TPer_Vic1)"}
    filas = csv_zip("envipe2023_csv.zip", spec["tabla"])
    r, c = estima(filas, "ap4_4_03", {"2"}, {"1"}, "fac_ele", "est_dis", "upm_dis")
    return escribe("CIV-08", spec, r, c)


def celda_DIN_03():
    spec = {"encuesta": "ENIF", "ola": "2012", "payload_id": "enif_2012_bases_enif2012_dbf",
            "tabla": "stmodulo2_e2.dbf  (join stsdem_e2.dbf por CONTROL+VIV_SEL+HOGAR+R_SEL=N_REN)",
            "variable": "P7_1", "ponderador": "FAC_PER", "estrato": "EST_DIS", "upm": "UPM_DIS",
            "codificacion": "y=1 si P7_1=='1' (Si); y=0 si=='2'; resto fuera",
            "universo": "mujeres de 18 a 70 anios, persona elegida del hogar"}
    sdem = {}
    for f in dbf_zip("bases_enif2012_dbf.zip", "stsdem_e2.dbf",
                     ["CONTROL", "VIV_SEL", "HOGAR", "N_REN", "SEXO", "EDAD"]):
        sdem[(f["control"], f["viv_sel"], f["hogar"], f["n_ren"])] = (f.get("sexo"), f.get("edad"))
    def gen():
        for f in dbf_zip("bases_enif2012_dbf.zip", "stmodulo2_e2.dbf"):
            k = (f.get("control"), f.get("viv_sel"), f.get("hogar"), f.get("r_sel"))
            sx, ed = sdem.get(k, (None, None))
            f["_sexo"], f["_edad"] = sx, ed
            yield f
    def filtro(f):
        e = num(f.get("_edad"))
        return str(f.get("_sexo")) == "2" and e is not None and 18 <= e <= 70
    r, c = estima(gen(), "p7_1", {"1"}, {"2"}, "fac_per", "est_dis", "upm_dis", filtro)
    return escribe("DIN-03", spec, r, c,
                   {"nota_join": "SEXO==2 (mujer) y EDAD 18-70 vienen de stsdem_e2; "
                                 "las filas sin pareja en el join caen por el filtro"})


def celda_DIN_05():
    spec = {"encuesta": "ENFIH", "ola": "2019", "payload_id": "enfih2019_bd_csv_zip",
            "tabla": "TMODULO.csv", "variable": "P8_1_1", "ponderador": "FACTOR",
            "estrato": "EDIS", "upm": "UPM_DIS",
            "codificacion": "y=1 si P8_1_1=='1' (Si); y=0 si=='2'; resto fuera",
            "universo": "personas de 18+ en localidades menores de 2 500 habitantes (TLOC=='4')"}
    filas = csv_zip("enfih2019/enfih_2019_base_de_datos_csv.zip", "TMODULO.csv")
    r, c = estima(filas, "p8_1_1", {"1"}, {"2"}, "factor", "edis", "upm_dis",
                  lambda f: str(f.get("tloc", "")).strip() == "4")
    return escribe("DIN-05", spec, r, c,
                   {"nota_universo": "TLOC=='4' es 'menor de 2 500 habitantes' segun enfih_2019_fd.xlsx hoja TVivienda"})


def celda_DIN_11():
    spec = {"encuesta": "ENIF", "ola": "2018", "payload_id": "enif2018_csv",
            "tabla": "conjunto_de_datos_tmodulo_enif_2018/conjunto_de_datos/tmodulo.csv",
            "variable": "P5_3", "ponderador": "fac_per", "estrato": "est_dis", "upm": "upm_dis",
            "codificacion": "y=1 si P5_3=='1' (Si); y=0 si=='2'; resto fuera",
            "universo": "personas de 18 a 70 anios, persona elegida del hogar (la tabla ya es ese universo)"}
    filas = csv_zip("enif2018_csv.zip", spec["tabla"])
    r, c = estima(filas, "p5_3", {"1"}, {"2"}, "fac_per", "est_dis", "upm_dis")
    return escribe("DIN-11", spec, r, c)


def celda_SFT_04():
    spec = {"encuesta": "ENASEM", "ola": "2018", "payload_id": "enasem2018_bd_csv_zip",
            "tabla": "SECT_A_C_D_F_E_PC_H_I_2018.csv", "variable": "H16D_18",
            "ponderador": "FACTORI_18", "estrato": "EST_DIS", "upm": "UPM_DIS",
            "codificacion": "y=1 si H16D_18=='1' (Si); y=0 si=='2'; 8 y 9 fuera",
            "universo": "personas de 50+ y conyuge, entrevista directa (la tabla ya es ese universo)"}
    filas = csv_zip("enasem2018/enasem_2018_bd_csv.zip", "SECT_A_C_D_F_E_PC_H_I_2018.csv")
    r, c = estima(filas, "h16d_18", {"1"}, {"2"}, "factori_18", "est_dis", "upm_dis")
    return escribe("SFT-04", spec, r, c)


def celda_SFT_06():
    spec = {"encuesta": "ENASEM", "ola": "2024", "payload_id": "enasem2024_bd_csv_zip",
            "tabla": "tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv", "variable": "F55_24",
            "ponderador": "FACTORI_24", "estrato": "EST_DIS_24", "upm": "UPM_DIS_24",
            "codificacion": "y=1 si F55_24=='1' (Si); y=0 si=='2'; 8 y 9 fuera",
            "universo": "personas de 50+ y conyuge, entrevista directa (la tabla ya es ese universo)"}
    filas = csv_zip("enasem2024/enasem_2024_bd_csv.zip", "tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv")
    r, c = estima(filas, "f55_24", {"1"}, {"2"}, "factori_24", "est_dis_24", "upm_dis_24")
    return escribe("SFT-06", spec, r, c)


LLAVE_ENOE = ("cd_a", "ent", "con", "v_sel", "n_hog", "h_mud", "n_ren")
Z_ENOE = "conjunto_de_datos_enoe_2024_1t_csv.zip"
T_COE1 = "conjunto_de_datos_coe1_enoe_2024_1t/conjunto_de_datos/conjunto_de_datos_coe1_enoe_2024_1t.csv"
T_SDEM = "conjunto_de_datos_sdem_enoe_2024_1t/conjunto_de_datos/conjunto_de_datos_sdem_enoe_2024_1t.csv"


def _enoe_join():
    """COE1 enriquecido con est_d_tri de SDEM por la llave estandar de ENOE."""
    sdem = {}
    for f in csv_zip(Z_ENOE, T_SDEM):
        sdem[tuple(f.get(k, "") for k in LLAVE_ENOE)] = f.get("est_d_tri", "")
    for f in csv_zip(Z_ENOE, T_COE1):
        f["_est_d_tri"] = sdem.get(tuple(f.get(k, "") for k in LLAVE_ENOE), "")
        yield f


def celda_TIC_01():
    spec = {"encuesta": "ENOE", "ola": "2024 1er trimestre", "payload_id": "enoe_2024_1t_csv",
            "tabla": "COE1 join SDEM", "variable": "p3i", "ponderador": "fac_tri",
            "estrato": "est_d_tri (de SDEM)", "upm": "upm",
            "codificacion": "y=1 si p3i=='1' (Si); y=0 si=='2'; 9 fuera",
            "universo": "poblacion ocupada subordinada y remunerada de 15+ con empleo actual (COE1)"}
    r, c = estima(_enoe_join(), "p3i", {"1"}, {"2"}, "fac_tri", "_est_d_tri", "upm")
    return escribe("TIC-01", spec, r, c,
                   {"nota_join": "p3i vive en COE1; est_d_tri en SDEM. Llave: " + "+".join(LLAVE_ENOE)})


def celda_TIC_08():
    spec = {"encuesta": "ENDUTIH", "ola": "2024", "payload_id": "endutih2024_bd_dbf_zip",
            "tabla": "tic_2024_usuarios.DBF", "variable": "P7_15", "ponderador": "FAC_PER",
            "estrato": "EST_DIS", "upm": "UPM_DIS",
            "codificacion": "y=1 si P7_15=='1' (Si); y=0 si=='2'; resto fuera",
            "universo": "persona elegida de 6 anios y mas (tabla tic_2024_usuarios)"}
    filas = dbf_zip("endutih2024/endutih2024_bd_dbf.zip", "tic_2024_usuarios.DBF",
                    ["P7_15", "FAC_PER", "EST_DIS", "UPM_DIS"])
    r, c = estima(filas, "p7_15", {"1"}, {"2"}, "fac_per", "est_dis", "upm_dis")
    return escribe("TIC-08", spec, r, c)


def celda_TIC_12():
    """Categorica k=10. R principal = categoria 8; el vector completo tambien se escribe."""
    spec = {"encuesta": "ENOE", "ola": "2024 1er trimestre", "payload_id": "enoe_2024_1t_csv",
            "tabla": "COE1 join SDEM", "variable": "p3n", "ponderador": "fac_tri",
            "estrato": "est_d_tri (de SDEM)", "upm": "upm",
            "codificacion": "R principal: y=1 si p3n=='8' (familiar/amigo/conocido); "
                            "y=0 si p3n en 1..10 distinto de 8; 99 y vacio fuera",
            "universo": "poblacion ocupada subordinada y remunerada de 15+ con empleo actual (COE1)"}
    validas = {str(i) for i in range(1, 11)}
    filas = list(_enoe_join())
    r, c = estima(filas, "p3n", {"8"}, validas - {"8"}, "fac_tri", "_est_d_tri", "upm")
    vector = {}
    for k in sorted(validas, key=int):
        rk, _ = estima(filas, "p3n", {k}, validas - {k}, "fac_tri", "_est_d_tri", "upm")
        if rk:
            vector[k] = {"R": rk["p_hat"], "EE_R": rk["se"]}
    return escribe("TIC-12", spec, r, c,
                   {"categoria_principal": "8", "vector_categorias": vector,
                    "nota_join": "p3n vive en COE1; est_d_tri en SDEM. Llave: " + "+".join(LLAVE_ENOE)})


CELDAS = [("CIV-08", celda_CIV_08), ("DIN-03", celda_DIN_03), ("DIN-05", celda_DIN_05),
          ("DIN-11", celda_DIN_11), ("SFT-04", celda_SFT_04), ("SFT-06", celda_SFT_06),
          ("TIC-01", celda_TIC_01), ("TIC-08", celda_TIC_08), ("TIC-12", celda_TIC_12)]

if __name__ == "__main__":
    solo = sys.argv[1:] or None
    for cid, fn in CELDAS:
        if solo and cid not in solo:
            continue
        try:
            d = fn()
            print(f"{cid}: {d['estado']} R={d.get('R')} EE={d.get('EE_R')} "
                  f"n={d.get('n_efectivo')} upm={d.get('n_upm_total')} single={d.get('n_estratos_singleton')}")
        except Exception as e:
            print(f"{cid}: ERROR {type(e).__name__}: {e}")

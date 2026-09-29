#!/usr/bin/env python3
"""Reconstruccion independiente CALC-ENADID-COLA-2018-0001 desde paquete/docs/spec-humana.md.

Ejecutar desde el directorio de trabajo: python3 salida/codigo/reconstruye.py
Lee solo las columnas autorizadas; escribe salida/resultado.json y salida/diagnostico.json.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

PAQ = "paquete"
OUT = "salida"
SEED = 20261001
REPLICAS = 2000
BLOQUE = 50

IDENTIDAD = {
    "paquete": "enadid-cola-2018-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "2907d439d3e41dc143848c606efdcce12b85fe3051d28be83afbcbfb56ac24fb",
}

COLS_MUJ = ["p10_1", "edad_muj", "tam_loc", "niv", "fac_per", "est_dis", "upm_dis"]
COLS_SDEM = ["llave_hog", "paren", "sexo", "ent", "tam_loc", "fac_viv", "est_dis", "upm_dis"]
COLS_MIG = ["llave_hog", "p4_6", "p4_15"]

LEIDOS = []


def lee_csv(nombre, cols):
    ruta = os.path.join(PAQ, "datos", nombre)
    LEIDOS.append(ruta)
    return pd.read_csv(ruta, usecols=cols, dtype=str, keep_default_na=False,
                       encoding="utf-8-sig")


def s(x):
    return repr(float(x))


# ---------------------------------------------------------------- ejes
TAMLOC = {"1": "100MIL-MAS", "2": "15MIL-99MIL", "3": "2500-14999", "4": "MENOS-2500"}
ESCOL = {}
for c in ("00", "01", "02"):
    ESCOL[c] = "HASTA-PRIMARIA"
for c in ("03", "04", "05"):
    ESCOL[c] = "SECUNDARIA"
for c in ("06", "07"):
    ESCOL[c] = "MEDIA-SUPERIOR"
for c in ("08", "09", "10", "11"):
    ESCOL[c] = "SUPERIOR"


def edad_grupo(e):
    out = pd.Series(pd.NA, index=e.index, dtype="object")
    for lo, hi in ((15, 24), (25, 34), (35, 44), (45, 54)):
        out[(e >= lo) & (e <= hi)] = f"{lo}-{hi}"
    return out


# ---------------------------------------------------------------- bootstrap
class Bootstrap:
    """Bootstrap de UPM dentro de estrato; estrato de UPM unica = de certeza (no se remuestrea)."""

    def __init__(self, est, upm):
        d = pd.DataFrame({"est": est.values, "upm": upm.values}).drop_duplicates()
        d = d.sort_values(["est", "upm"]).reset_index(drop=True)
        self.upms = d
        self.idx_upm = pd.Series(np.arange(len(d)), index=d["est"] + "|" + d["upm"])
        self.n_upm = len(d)
        rng = np.random.Generator(np.random.PCG64(SEED))
        grupos = [np.flatnonzero(d["est"].values == e) for e in d["est"].unique()]
        mult = np.zeros((REPLICAS, self.n_upm), dtype=np.float64)
        self.n_estratos = len(grupos)
        self.n_certeza = 0
        for b0 in range(0, REPLICAS, BLOQUE):
            nb = min(BLOQUE, REPLICAS - b0)
            for g in grupos:
                nh = len(g)
                if nh == 1:
                    mult[b0:b0 + nb, g[0]] = 1.0
                    continue
                draws = rng.integers(0, nh, size=(nb, nh))
                for k in range(nb):
                    mult[b0 + k, g] = np.bincount(draws[k], minlength=nh)
        self.n_certeza = sum(1 for g in grupos if len(g) == 1)
        self.mult = mult

    def posicion(self, est, upm):
        return self.idx_upm.loc[(est + "|" + upm).values].values


def estima(pos, w, y, boot):
    """Razon ponderada sum(w*y)/sum(w) y replicas bootstrap. Devuelve dict."""
    den = w.sum()
    if den <= 0 or len(w) == 0:
        return {"estado": "DENOMINADOR-CERO"}
    punto = (w * y).sum() / den
    num_u = np.bincount(pos, weights=w * y, minlength=boot.n_upm)
    den_u = np.bincount(pos, weights=w, minlength=boot.n_upm)
    rn = boot.mult @ num_u
    rd = boot.mult @ den_u
    degeneradas = int((rd <= 0).sum())
    res = {"estado": "RECONSTRUIDO", "punto": punto, "replicas_degeneradas": degeneradas}
    if degeneradas > 0:
        res["estado_ic"] = "NO-IDENTIFICADA"
        res["motivo_ic"] = (f"{degeneradas} de {REPLICAS} replicas bootstrap con denominador "
                            "ponderado cero en el dominio; contrato conservador de la spec §4 "
                            "(una replica degenerada -> sin EE ni IC)")
        return res
    r = rn / rd
    if not np.all(np.isfinite(r)):
        res["estado_ic"] = "NO-IDENTIFICADA"
        res["motivo_ic"] = "replica bootstrap no finita; contrato conservador spec §4"
        return res
    lo, hi = np.percentile(r, [2.5, 97.5])
    res["estado_ic"] = "CALCULADO"
    res["ic95_inf"] = lo
    res["ic95_sup"] = hi
    res["ee_bootstrap"] = float(np.std(r, ddof=1))
    return res


# ---------------------------------------------------------------- marcos
def marco_mujeres(diag):
    m = lee_csv("tmujer2.csv", COLS_MUJ)
    n0 = len(m)
    edad = pd.to_numeric(m["edad_muj"], errors="coerce")
    fac = pd.to_numeric(m["fac_per"], errors="coerce")
    est = m["est_dis"].str.strip()
    upm = m["upm_dis"].str.strip()
    exc = {
        "edad_fuera_15_54_o_vacia": int((~edad.between(15, 54)).sum()),
        "fac_per_no_positivo_o_vacio": int((~(fac > 0)).sum()),
        "est_dis_vacio": int((est == "").sum()),
        "upm_dis_vacio": int((upm == "").sum()),
    }
    ok = edad.between(15, 54) & (fac > 0) & (est != "") & (upm != "")
    m = m[ok].copy()
    m["w"] = fac[ok].astype(float)
    m["est"] = est[ok]
    m["upm"] = upm[ok]
    m["edad"] = edad[ok]
    diag["marcos"]["MUJERES"] = {"filas_archivo": n0, "exclusiones_marco": exc,
                                 "filas_validas_marco": int(len(m))}
    boot = Bootstrap(m["est"], m["upm"])
    diag["marcos"]["MUJERES"].update({"upm": boot.n_upm, "estratos": boot.n_estratos,
                                      "estratos_certeza_upm_unica": boot.n_certeza})
    m["pos"] = boot.posicion(m["est"], m["upm"])
    p = m["p10_1"].str.strip()
    conductas = {
        "separada-entre-union-libre": ({"1", "2", "5"}, {"2"}),
        "separada-o-divorciada-entre-matrimonio": ({"3", "4", "6", "7"}, {"3", "4"}),
    }
    ejes = {
        "TOTAL": pd.Series("TODOS", index=m.index),
        "EDAD": edad_grupo(m["edad"]),
        "TAMLOC": m["tam_loc"].str.strip().map(TAMLOC),
        "ESCOLARIDAD": m["niv"].str.strip().map(ESCOL),
    }
    return m, boot, p, conductas, ejes, n0 - len(m)


def marco_hogares(diag):
    sd = lee_csv("tsdem.csv", COLS_SDEM)
    mig = lee_csv("tmigrante.csv", COLS_MIG)
    n0 = len(sd)
    jef = sd["paren"].str.strip() == "1"
    fac = pd.to_numeric(sd["fac_viv"], errors="coerce")
    est = sd["est_dis"].str.strip()
    upm = sd["upm_dis"].str.strip()
    exc = {
        "paren_distinto_de_1": int((~jef).sum()),
        "jefatura_fac_viv_no_positivo_o_vacio": int((jef & ~(fac > 0)).sum()),
        "jefatura_est_dis_vacio": int((jef & (est == "")).sum()),
        "jefatura_upm_dis_vacio": int((jef & (upm == "")).sum()),
    }
    ok = jef & (fac > 0) & (est != "") & (upm != "")
    h = sd[ok].copy()
    h["w"] = fac[ok].astype(float)
    h["est"] = est[ok]
    h["upm"] = upm[ok]
    h["llave_hog"] = h["llave_hog"].str.strip()
    dup = int(h["llave_hog"].duplicated().sum())

    mm = mig.copy()
    mm["llave_hog"] = mm["llave_hog"].str.strip()
    marca = (mm["p4_6"].str.strip() == "1") & mm["p4_15"].str.strip().isin({"1", "3"})
    hog_con = set(mm.loc[marca, "llave_hog"])
    h["con_mig"] = h["llave_hog"].isin(hog_con)
    diag["marcos"]["HOGARES"] = {
        "filas_archivo_tsdem": n0, "exclusiones_marco": exc,
        "filas_validas_marco_jefaturas": int(len(h)), "llave_hog_duplicadas_en_jefaturas": dup,
        "filas_tmigrante": int(len(mig)),
        "migrantes_varon_fuera_de_mexico": int(marca.sum()),
        "hogares_tmigrante_con_marca": len(hog_con),
        "hogares_con_marca_sin_jefatura_valida": len(hog_con - set(h["llave_hog"])),
        "hogares_validos_con_migrante_varon": int(h["con_mig"].sum()),
        "hogares_validos_sin_migrante_varon": int((~h["con_mig"]).sum()),
    }
    boot = Bootstrap(h["est"], h["upm"])
    diag["marcos"]["HOGARES"].update({"upm": boot.n_upm, "estratos": boot.n_estratos,
                                      "estratos_certeza_upm_unica": boot.n_certeza})
    h["pos"] = boot.posicion(h["est"], h["upm"])
    ejes = {
        "TOTAL": pd.Series("TODOS", index=h.index),
        "TAMLOC": h["tam_loc"].str.strip().map(TAMLOC),
        "ENTIDAD": h["ent"].str.strip().where(h["ent"].str.strip().isin(
            [f"{i:02d}" for i in range(1, 33)])),
    }
    return h, boot, ejes, n0 - len(h)


# ---------------------------------------------------------------- main
def main():
    ruta_esq = os.path.join(PAQ, "esquema-identidades.tsv")
    LEIDOS.append(ruta_esq)
    esq = pd.read_csv(ruta_esq, sep="\t", dtype=str, keep_default_na=False)
    diag = {"marcos": {}, "llaves": {}, "parametros_bootstrap": {
        "generador": "numpy.random.Generator(numpy.random.PCG64(20261001)), uno nuevo por marco",
        "replicas": REPLICAS, "bloque": BLOQUE, "ic": "percentil 2.5/97.5 (numpy.percentile lineal)"}}

    m, bm, p, cm, ejes_m, excl_m = marco_mujeres(diag)
    h, bh, ejes_h, excl_h = marco_hogares(diag)

    filas = []
    for _, r in esq.iterrows():
        llave, unidad = r["llave"], r["unidad"]
        conducta, eje, seg, ola = r["conducta"], r["eje"], r["segmento"], r["ola"]
        fila = {"llave": llave, "unidad": unidad}
        d = {"conducta": conducta, "eje": eje, "segmento": seg}
        if ola != "2018":
            fila.update(estado="NO-RECALCULABLE-DESDE-SPEC",
                        motivo=f"ola {ola} no abierta por la spec (solo 2018)")
            filas.append(fila); diag["llaves"][llave] = d; continue
        if conducta in cm:
            sub, uno = cm[conducta]
            ejes = ejes_m
            if eje not in ejes:
                fila.update(estado="NO-RECALCULABLE-DESDE-SPEC",
                            motivo=f"eje {eje} no definido para el marco MUJERES en spec §3")
                filas.append(fila); diag["llaves"][llave] = d; continue
            en_sub = p.isin(sub)
            ax = ejes[eje]
            dom = ax == seg
            sel = en_sub & dom.fillna(False)
            d["exclusiones"] = {
                "filtro_marco_mujeres": excl_m,
                "p10_1_fuera_de_subpoblacion": int((~en_sub).sum()),
                "eje_sin_categoria_en_subpoblacion": int((en_sub & ax.isna()).sum()),
                "otro_segmento_del_eje_en_subpoblacion": int((en_sub & ax.notna() & ~dom.fillna(False)).sum()),
            }
            sub_df = m[sel]
            y = p[sel].isin(uno).astype(float).values
            d["n_valido"] = int(sel.sum()); d["n_uno"] = int(y.sum())
            res = estima(sub_df["pos"].values, sub_df["w"].values, y, bm)
        elif conducta in ("jefatura-femenina-con-migrante-varon",
                          "jefatura-femenina-sin-migrante-varon"):
            ejes = ejes_h
            if eje not in ejes:
                fila.update(estado="NO-RECALCULABLE-DESDE-SPEC",
                            motivo=f"eje {eje} no definido para el marco HOGARES en spec §3")
                filas.append(fila); diag["llaves"][llave] = d; continue
            part = h["con_mig"] if "con-migrante" in conducta else ~h["con_mig"]
            sexo = h["sexo"].str.strip()
            sx_ok = sexo.isin({"1", "2"})
            ax = ejes[eje]
            dom = (ax == seg).fillna(False)
            sel = part & sx_ok & dom
            d["exclusiones"] = {
                "filtro_marco_hogares": excl_h,
                "fuera_de_particion_migrante": int((~part).sum()),
                "sexo_no_1_2_en_particion": int((part & ~sx_ok).sum()),
                "eje_sin_categoria_en_particion": int((part & sx_ok & ax.isna()).sum()),
                "otro_segmento_del_eje_en_particion": int((part & sx_ok & ax.notna() & ~dom).sum()),
            }
            sub_df = h[sel]
            y = (sexo[sel] == "2").astype(float).values
            d["n_valido"] = int(sel.sum()); d["n_uno"] = int(y.sum())
            res = estima(sub_df["pos"].values, sub_df["w"].values, y, bh)
        else:
            fila.update(estado="NO-RECALCULABLE-DESDE-SPEC",
                        motivo=f"conducta {conducta} no definida en spec §2")
            filas.append(fila); diag["llaves"][llave] = d; continue

        if res["estado"] == "DENOMINADOR-CERO":
            fila.update(estado="DENOMINADOR-CERO",
                        motivo="dominio sin observaciones validas (suma de pesos cero) bajo spec suficiente")
        else:
            fila.update(estado="RECONSTRUIDO", punto=s(res["punto"]), estado_ic=res["estado_ic"])
            if res["estado_ic"] == "CALCULADO":
                fila.update(ic95_inf=s(res["ic95_inf"]), ic95_sup=s(res["ic95_sup"]))
                d["ee_bootstrap"] = s(res["ee_bootstrap"])
            else:
                fila["motivo_ic"] = res["motivo_ic"]
            d["replicas_degeneradas"] = res["replicas_degeneradas"]
        filas.append(fila)
        diag["llaves"][llave] = d

    ruta_dec = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decisiones.json")
    with open(ruta_dec, encoding="utf-8") as f:
        diag["decisiones"] = json.load(f)
    diag["archivos_leidos_por_codigo"] = LEIDOS + [os.path.relpath(ruta_dec)]

    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    llaves = [f["llave"] for f in filas]
    assert len(llaves) == len(set(llaves)) == len(esq)
    with open(os.path.join(OUT, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(os.path.join(OUT, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diag, f, ensure_ascii=False, indent=1)
        f.write("\n")
    cuenta = pd.Series([f["estado"] + "/" + f.get("estado_ic", "-") for f in filas]).value_counts()
    print(cuenta.to_string())


if __name__ == "__main__":
    main()

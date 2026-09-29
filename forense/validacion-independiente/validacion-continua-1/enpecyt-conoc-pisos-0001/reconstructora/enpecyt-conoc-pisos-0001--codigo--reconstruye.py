#!/usr/bin/env python3
"""Reconstruccion independiente CALC-ENPECYT-CONOC-PISOS-0001 (spec humana v1.0).

Ejecutar desde el directorio de trabajo:  python3 salida/codigo/reconstruye.py
Lee solo ./paquete/ y escribe salida/resultado.json y salida/diagnostico.json.
"""
import csv
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "paquete/lib")
from dbfread import DBF  # solo para leer el encabezado (lista de campos)

PAQ = "paquete"
SAL = "salida"
IDENTIDAD = {
    "paquete": "enpecyt-conoc-pisos-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "3c16ea013079651ad944b2864f4130b1616c06fac89d28935e7a99bec978ca0c",
}
SEMILLA = 20260925
B = 1000
OLAS = ("2011", "2013", "2015")

# Columnas autorizadas (FIRMAS / encargo); nada fuera de esta lista se decodifica.
AUT = {
    "2011_cb1": ["CD", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "FAC", "S4P1_3", "S4P14_13", "S4P14_14", "S4P14_4"],
    "2011_cb2": ["CD", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "S4P26_1", "S4P33_2_1"],
    "2011_cs": ["CD", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "SEX", "EDA", "NIV"],
    "2013_cb1": ["CD_A", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "FAC", "S4P1_3", "S4P14_13", "S4P14_14", "S4P14_4"],
    "2013_cb2": ["CD_A", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "S4P26_1", "S4P33_2_1"],
    "2013_cs": ["CD_A", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "SEX", "EDA", "NIV", "EST_DIS", "UPM_DIS"],
    "2015_cb1": ["CD_A", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "FAC", "S4P1_3", "S4P14_12", "S4P14_13", "S4P14_16", "S4P14_17"],
    "2015_cb2": ["CD_A", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "S4P25_1", "S4P31_1_1"],
    "2015_cs": ["CD_A", "PER", "CON", "V_SEL", "N_HOG", "N_REN", "SEX", "EDA", "NIV", "EST_DIS", "UPM_DIS"],
}

# Reactivos por ola (spec §0)
REACTIVO = {
    "interes": {"2011": "S4P1_3", "2013": "S4P1_3", "2015": "S4P1_3"},
    "gob": {"2011": "S4P26_1", "2013": "S4P26_1", "2015": "S4P25_1"},
    "fe": {"2011": "S4P33_2_1", "2013": "S4P33_2_1", "2015": "S4P31_1_1"},
    "bombero": {"2011": "S4P14_13", "2013": "S4P14_13", "2015": "S4P14_12"},
    "enfermera": {"2011": "S4P14_14", "2013": "S4P14_14", "2015": "S4P14_13"},
    "investigador": {"2011": "S4P14_4", "2013": "S4P14_4", "2015": "S4P14_16"},
    "inventor": {"2015": "S4P14_17"},
}
# conducta -> (reactivo, codigos numerador, codigos denominador)  (spec §2)
CONDUCTA = {
    "interes-al-menos-moderado": ("interes", {1, 2, 3}, {1, 2, 3, 4}),
    "interes-grande-o-mas": ("interes", {1, 2}, {1, 2, 3, 4}),
    "gob-invertir-acuerdo": ("gob", {1, 2}, {1, 2, 3, 4, 5}),
    "gob-invertir-acuerdo-sin-ns": ("gob", {1, 2}, {1, 2, 3, 4}),
    "fe-ciencia-acuerdo": ("fe", {1, 2}, {1, 2, 3, 4, 5}),
    "fe-ciencia-acuerdo-sin-ns": ("fe", {1, 2}, {1, 2, 3, 4}),
    "respeta-10-bombero": ("bombero", {10}, set(range(1, 11))),
    "respeta-10-enfermera": ("enfermera", {10}, set(range(1, 11))),
    "respeta-10-investigador": ("investigador", {10}, set(range(1, 11))),
    "respeta-10-inventor": ("inventor", {10}, set(range(1, 11))),
}

LEIDOS = []


def lee_dbf(nombre, cols):
    """Decodifica solo `cols` de un DBF por offset de bytes; omite registros borrados."""
    ruta = os.path.join(PAQ, "datos", f"enpecyt{nombre}.dbf")
    LEIDOS.append(ruta)
    t = DBF(ruta, load=False)
    offs, pos = {}, 1  # byte 0 = marca de borrado
    for f in t.fields:
        offs[f.name] = (pos, f.length, f.type)
        pos += f.length
    faltan = [c for c in cols if c not in offs]
    if faltan:
        raise SystemExit(f"{nombre}: faltan columnas autorizadas {faltan}")
    hlen, rlen, nrec = t.header.headerlen, t.header.recordlen, t.header.numrecords
    out = {c: [] for c in cols}
    borrados = 0
    with open(ruta, "rb") as fh:
        fh.seek(hlen)
        for _ in range(nrec):
            rec = fh.read(rlen)
            if len(rec) < rlen:
                break
            if rec[0:1] == b"*":
                borrados += 1
                continue
            for c in cols:
                p, ln, ty = offs[c]
                s = rec[p:p + ln].decode("latin-1").strip()
                if ty in ("N", "F"):
                    out[c].append(float(s) if s else np.nan)
                else:
                    out[c].append(s)
    return pd.DataFrame(out), {"registros": nrec, "borrados": borrados}


def num(s):
    return pd.to_numeric(s, errors="coerce")


def prepara_ola(y, diag):
    ci = "CD" if y == "2011" else "CD_A"
    K = [ci, "PER", "CON", "V_SEL", "N_HOG", "N_REN"]
    tabs = {}
    d = {}
    for t in ("cb1", "cb2", "cs"):
        df, info = lee_dbf(f"{y}_{t}", AUT[f"{y}_{t}"])
        for c in K:
            df[c] = df[c].astype(str).str.strip()
        dup = df.duplicated(K, keep=False)
        d[f"{t}_filas"] = int(len(df))
        d[f"{t}_filas_con_llave_duplicada"] = int(dup.sum())
        d[f"{t}_registros_borrados"] = info["borrados"]
        tabs[t] = df[~dup]
    b1 = tabs["cb1"]
    n0 = len(b1)
    m = b1.merge(tabs["cb2"], on=K, how="inner")
    d["cb1_llave_unica"] = int(n0)
    d["excluidas_sin_par_unico_cb2"] = int(n0 - len(m))
    n1 = len(m)
    m = m.merge(tabs["cs"], on=K, how="inner")
    d["excluidas_sin_par_unico_cs"] = int(n1 - len(m))
    d["cb2_no_pareadas"] = int(len(tabs["cb2"].merge(b1[K], on=K, how="left", indicator=True).query("_merge=='left_only'")))
    fac = num(m["FAC"])
    d["excluidas_fac_no_positivo_o_ausente"] = int((~(fac > 0)).sum())
    m = m[fac > 0].copy()
    m["w"] = num(m["FAC"]).astype(float)
    eda = num(m["EDA"])
    d["excluidas_eda_menor_18"] = int((eda < 18).sum())
    m = m[~(eda < 18)].copy()
    d["n_universo"] = int(len(m))
    # ejes
    m["_eda"] = num(m["EDA"])
    sex = num(m["SEX"])
    niv = num(m["NIV"])
    e = m["_eda"]
    seg = {
        ("TOTAL", "TODOS"): pd.Series(True, index=m.index),
        ("SEXO", "HOMBRE"): sex == 1,
        ("SEXO", "MUJER"): sex == 2,
        ("EDAD", "18-29"): (e >= 18) & (e <= 29),
        ("EDAD", "30-44"): (e >= 30) & (e <= 44),
        ("EDAD", "45-59"): (e >= 45) & (e <= 59),
        ("EDAD", "60-MAS"): e >= 60,
        ("ESCOLARIDAD", "BASICA-O-MENOS"): niv.between(0, 3),
        ("ESCOLARIDAD", "MEDIA"): niv.between(4, 6),
        ("ESCOLARIDAD", "SUPERIOR"): niv.between(7, 10),
    }
    seg = {k: v.fillna(False).to_numpy(bool) for k, v in seg.items()}
    d["sin_categoria_por_eje"] = {
        "SEXO": int((~(seg[("SEXO", "HOMBRE")] | seg[("SEXO", "MUJER")])).sum()),
        "EDAD": int((~(seg[("EDAD", "18-29")] | seg[("EDAD", "30-44")] | seg[("EDAD", "45-59")] | seg[("EDAD", "60-MAS")])).sum()),
        "ESCOLARIDAD": int((~(seg[("ESCOLARIDAD", "BASICA-O-MENOS")] | seg[("ESCOLARIDAD", "MEDIA")] | seg[("ESCOLARIDAD", "SUPERIOR")])).sum()),
    }
    # diseño
    rep = None
    if y != "2011":
        est = m[ci].astype(str) + "|" + m["EST_DIS"].astype(str).str.strip()
        upm = est + "|" + m["UPM_DIS"].astype(str).str.strip()
        rep, dd = multiplicidades(est.to_numpy(), upm.to_numpy())
        d["diseno"] = dd
    diag[y] = d
    return m.reset_index(drop=True), seg, rep


def multiplicidades(est, upm):
    """Bootstrap de UPM dentro de estrato: n_h extracciones con reemplazo por estrato.

    Devuelve matriz (B, n_personas) de multiplicidades de la UPM de cada persona.
    Generador PCG64(20260925) nuevo por ola; estratos y UPM en orden lexicografico;
    bucle externo replicas, interno estratos.
    """
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    estratos = sorted(set(est))
    upms_por_est = {h: sorted(set(upm[est == h])) for h in estratos}
    idx_upm = {u: i for i, u in enumerate(sorted(set(upm)))}
    cont = np.zeros((B, len(idx_upm)))
    for b in range(B):
        for h in estratos:
            us = upms_por_est[h]
            nh = len(us)
            sel = rng.integers(0, nh, size=nh)
            for j in sel:
                cont[b, idx_upm[us[j]]] += 1
    col = np.array([idx_upm[u] for u in upm])
    dd = {
        "estratos": len(estratos),
        "upm": len(idx_upm),
        "estratos_con_una_upm": int(sum(len(v) == 1 for v in upms_por_est.values())),
        "replicas": B,
        "semilla": f"PCG64({SEMILLA})",
    }
    return cont[:, col], dd


def fnum(x):
    return repr(float(x))


def main():
    esquema = []
    with open(os.path.join(PAQ, "esquema-identidades.tsv"), encoding="utf-8") as fh:
        LEIDOS.append(os.path.join(PAQ, "esquema-identidades.tsv"))
        for r in csv.DictReader(fh, delimiter="\t"):
            esquema.append(r)

    diag_olas = {}
    datos = {y: prepara_ola(y, diag_olas) for y in OLAS}

    filas, diag_llaves = [], []
    for r in esquema:
        llave, y, cond = r["llave"], r["ola"], r["conducta"]
        eje, segm = r["eje"], r["segmento"]
        fila = {"llave": llave, "unidad": r["unidad"]}
        dl = {"llave": llave, "ola": y, "conducta": cond, "eje": eje, "segmento": segm}
        if y not in datos or cond not in CONDUCTA or (eje, segm) not in datos[y][1]:
            fila.update(estado="NO-RECALCULABLE-DESDE-SPEC",
                        motivo="ola/conducta/segmento sin definicion en la spec humana")
            filas.append(fila); diag_llaves.append(dl); continue
        reac, numc, denc = CONDUCTA[cond]
        if y not in REACTIVO[reac]:
            fila.update(estado="NO-RECALCULABLE-DESDE-SPEC",
                        motivo=f"la spec no identifica reactivo '{reac}' para la ola {y}")
            filas.append(fila); diag_llaves.append(dl); continue
        m, seg, rep = datos[y]
        var = REACTIVO[reac][y]
        v = num(m[var]).to_numpy(float)
        dom = seg[(eje, segm)]
        valido = np.isin(v, list(denc))
        den_mask = dom & valido
        yv = np.isin(v, list(numc)).astype(float)
        w = m["w"].to_numpy(float)
        dl["variable"] = var
        dl["n_universo"] = int(len(m))
        dl["n_dominio"] = int(dom.sum())
        dl["n_valido"] = int(den_mask.sum())
        vals, cnts = np.unique(np.where(np.isnan(v[dom & ~valido]), -1, v[dom & ~valido]), return_counts=True)
        dl["excluidas_en_dominio_por_codigo_fuera_de_denominador"] = {
            ("ausente" if k == -1 else str(int(k))): int(c) for k, c in zip(vals, cnts)}
        dl["excluidas_fuera_del_segmento"] = int((~dom).sum())
        dl["excluidas_sin_categoria_en_eje"] = diag_olas[y]["sin_categoria_por_eje"].get(eje, 0)
        dl["n_numerador"] = int((den_mask & (yv > 0)).sum())
        sw = w[den_mask].sum()
        if den_mask.sum() == 0 or sw <= 0:
            fila.update(estado="DENOMINADOR-CERO",
                        motivo="dominio sin casos validos para el denominador de la conducta")
            filas.append(fila); diag_llaves.append(dl); continue
        p = (w[den_mask] * yv[den_mask]).sum() / sw
        dl["suma_pesos_denominador"] = fnum(sw)
        fila.update(estado="RECONSTRUIDO", punto=fnum(p))
        if y == "2011":
            fila["estado_ic"] = "SIN-IC"
        else:
            wr = rep[:, den_mask] * w[den_mask]
            numr = (wr * yv[den_mask]).sum(axis=1)
            denr = wr.sum(axis=1)
            ok = denr > 0
            pr = np.where(ok, numr / np.where(ok, denr, 1.0), np.nan)
            dl["replicas_con_denominador_cero"] = int((~ok).sum())
            prv = pr[ok]
            ee = float(np.std(prv, ddof=1)) if len(prv) > 1 else float("nan")
            dl["ee_bootstrap_escala_p"] = fnum(ee)
            if 0 < p < 1:
                lr = np.log(prv[(prv > 0) & (prv < 1)] / (1 - prv[(prv > 0) & (prv < 1)]))
                dl["ee_bootstrap_escala_logit"] = fnum(np.std(lr, ddof=1)) if len(lr) > 1 else None
                dl["replicas_en_0_o_1"] = int(len(prv) - len(lr))
            lo, hi = np.quantile(prv, [0.025, 0.975])
            dl["ic95_percentil_bootstrap"] = [fnum(lo), fnum(hi)]
            if y == "2013":
                if (~ok).any():
                    fila.update(estado_ic="NO-IDENTIFICADA",
                                motivo_ic=f"{int((~ok).sum())} replicas bootstrap con dominio vacio; la spec no fija su tratamiento")
                else:
                    fila.update(estado_ic="CALCULADO", ic95_inf=fnum(lo), ic95_sup=fnum(hi))
            else:  # 2015: piso con IC calibrado por persistencia
                if cond == "respeta-10-inventor":
                    mot = ("IC calibrado requiere tau^2 sobre 2011->2013->2015; el reactivo inventor "
                           "solo existe en 2015 (spec §2), tau^2 no es estimable con una ola")
                else:
                    mot = ("IC calibrado expit(logit p +- z*sqrt(ee_2015^2+tau^2)) requiere tau^2 'por conducta x eje x "
                           "categoria sobre 2011->2013->2015'; la spec no define en prosa el estimador de tau^2 "
                           "(escala, grados de libertad, descuento de varianza muestral con 2011 sin EE) ni la "
                           "escala de ee_2015 dentro de ic_calibrado de la receta, que no esta en el paquete")
                fila.update(estado_ic="NO-IDENTIFICADA", motivo_ic=mot)
        filas.append(fila)
        diag_llaves.append(dl)

    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    llaves = [f["llave"] for f in filas]
    assert len(llaves) == len(set(llaves)) == len(esquema)
    os.makedirs(SAL, exist_ok=True)
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    decisiones = json.load(open(os.path.join(os.path.dirname(__file__), "decisiones.json"), encoding="utf-8"))
    diag = {
        "identidad": IDENTIDAD,
        "universo_y_union_por_ola": diag_olas,
        "decisiones_de_implementacion": decisiones,
        "resumen_estados": pd.Series([f["estado"] + "/" + f.get("estado_ic", "-") for f in filas]).value_counts().to_dict(),
        "llaves": diag_llaves,
        "archivos_datos_leidos": LEIDOS,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as fh:
        json.dump(diag, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()

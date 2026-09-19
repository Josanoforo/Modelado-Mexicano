"""Motor compartido de los pisos GEN2 por eje.

El módulo recibe únicamente los paths ya resueltos por ``corrida0``.  No abre
el manifiesto ni decide la identidad de insumos.  El bootstrap remuestrea UPM
con reemplazo dentro de estrato (semilla PCG64 fija), nunca filas iid.
"""
from __future__ import annotations

import io, json, zipfile
import numpy as np
import pandas as pd


def _csv(zip_path, suffix, cols):
    with zipfile.ZipFile(zip_path) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(suffix.lower()))
        raw = z.read(name)
    for enc in ("utf-8", "latin-1"):
        try:
            d = pd.read_csv(io.StringIO(raw.decode(enc)), dtype=str,
                            keep_default_na=False, na_filter=False)
            d.columns = [x.strip() for x in d.columns]
            return d[cols]
        except UnicodeDecodeError:
            continue
    raise RuntimeError("CSV sin codificacion util")


def _age(s):
    x = pd.to_numeric(s, errors="coerce")
    return pd.cut(x, [17, 29, 44, 59, 97], labels=["18-29", "30-44", "45-59", "60+"]).astype(str)


def _bootstrap(d, groups, reps=10000, seed=42):
    """Tabla compacta por categoría: punto e IC percentil por conglomerados."""
    d = d.copy(); d["_key"] = d["_est"].astype(str) + "\t" + d["_upm"].astype(str)
    keys = sorted(d["_key"].unique()); pos = {k:i for i,k in enumerate(keys)}
    gvals = sorted(groups.unique()); gpos = {g:i for i,g in enumerate(gvals)}
    W = np.zeros((len(keys), len(gvals))); Y = W.copy()
    for r in d[["_key", "_grp", "_w", "_y"]].itertuples(index=False, name=None):
        i, j = pos[r[0]], gpos[r[1]]
        W[i,j] += r[2]; Y[i,j] += r[2] * r[3]
    point = np.divide(Y.sum(0), W.sum(0), out=np.full(len(gvals), np.nan), where=W.sum(0)>0)
    by_h = {}
    for k in keys:
        by_h.setdefault(k.split("\t",1)[0], []).append(pos[k])
    rng = np.random.Generator(np.random.PCG64(seed)); vals=[]
    # Batches avoid storing a 10,000 × all-UPM matrix.
    for start in range(0, reps, 50):
        b = min(50, reps-start); mult=np.zeros((b,len(keys)), dtype=np.int16)
        for _, ix in sorted(by_h.items()):
            ix=np.asarray(ix); draw=rng.integers(0,len(ix),size=(b,len(ix)))
            for row in range(b): mult[row] += np.bincount(ix[draw[row]], minlength=len(keys)).astype(np.int16)
        den=mult @ W; num=mult @ Y
        vals.append(np.divide(num,den,out=np.full_like(num,np.nan),where=den>0))
    v=np.vstack(vals)
    return [{"categoria":g, "punto":None if not np.isfinite(point[i]) else float(point[i]),
             "ic95":[None if not np.isfinite(x) else float(x) for x in np.nanpercentile(v[:,i],[2.5,97.5])],
             "n":int((groups==g).sum())} for i,g in enumerate(gvals)]


def _tabla(d, axes, prefix):
    out={}
    for name, grp in axes.items():
        ok=grp.notna() & d["_w"].notna() & (d["_w"]>0) & d["_est"].ne("") & d["_upm"].ne("")
        x=d.loc[ok].copy(); x["_grp"]=grp.loc[ok].astype(str)
        out[name]=_bootstrap(x, x["_grp"])
    return {f"RESULT-{prefix}-TABLA":json.dumps(out,ensure_ascii=False,sort_keys=True,separators=(",",":")),
            f"RESULT-{prefix}-N-UNIVERSO":int(len(d))}


def envipe(inputs, contrato):
    z=inputs["envipe2024_csv"]["ruta_absoluta"]
    a=_csv(z,"conjunto_de_datos_tmod_vic_envipe2024.csv",["BP1_20","BP1_23","BP2_1","BPCOD","FAC_DEL","EST_DIS","UPM_DIS","ID_PER","SEXO","EDAD","DOMINIO"])
    b=_csv(z,"conjunto_de_datos_tsdem_envipe2024.csv",["ID_PER","NIV"])
    d=a.merge(b,on="ID_PER",how="left",validate="m:1")
    d["_w"]=pd.to_numeric(d.FAC_DEL,errors="coerce"); d["_est"]=d.EST_DIS.str.strip(); d["_upm"]=d.UPM_DIS.str.strip()
    # La primera tasa es evasión; la segunda, reporte entre víctimas con seguro.
    d["_y"]=(d.BP1_20.str.strip().eq("2") & d.BP1_23.str.strip().isin(["04","05","06","08"])).astype(int)
    axes={"sexo":d.SEXO.str.strip(),"edad":_age(d.EDAD),"escolaridad_proxy":d.NIV.str.strip(),"dominio":d.DOMINIO.str.strip()}
    return _tabla(d,axes,"PISOS-ENVIPE2024-EVASION")


def encig(inputs, contrato):
    z=inputs["encig23_base_datos_csv"]["ruta_absoluta"]
    a=_csv(z,"encig2023_04_sec_7.csv",["N_TRA","P7_3","FAC_TRA","EST_DIS","UPM_DIS","ID_PER"])
    b=_csv(z,"encig2023_02_residentes_sec_2.csv",["ID_PER","SEXO","EDAD","NIV"])
    d=a.merge(b,on="ID_PER",how="left",validate="m:1"); d=d[d.N_TRA.str.strip().eq("01")].copy()
    d["_w"]=pd.to_numeric(d.FAC_TRA,errors="coerce"); d["_est"]=d.EST_DIS.str.strip(); d["_upm"]=d.UPM_DIS.str.strip()
    # Catálogo ENCIG: P7_3=03 es canal Internet; no se infiere coacción.
    d["_y"]=d.P7_3.str.strip().eq("03").astype(int)
    return _tabla(d,{"sexo":d.SEXO.str.strip(),"edad":_age(d.EDAD),"escolaridad":d.NIV.str.strip()},"PISOS-ENCIG2023-DIGITAL")


def enif(inputs, contrato):
    z=inputs["enif2021_csv"]["ruta_absoluta"]
    inf=[f"P5_1_{i}" for i in range(1,7)]; formal=[f"P5_7_{i}" for i in range(1,10)]
    cols=inf+formal+["SEXO","EDAD","TLOC","P3_1_1","FAC_ELE","EST_DIS","UPM_DIS"]+[f"P5_6_{i}" for i in [1,2,3,4,5,8,9]]
    d=_csv(z,"conjunto_de_datos_tmodulo_enif_2021.csv",cols)
    d["_w"]=pd.to_numeric(d.FAC_ELE,errors="coerce"); d["_est"]=d.EST_DIS.str.strip(); d["_upm"]=d.UPM_DIS.str.strip()
    informal=d[inf].apply(lambda x:x.astype(str).apply(lambda y:y.str.strip().eq("1")).any(axis=1))
    cuenta=d[formal].apply(lambda x:x.astype(str).apply(lambda y:y.str.strip().eq("1")).any(axis=1))
    d["_y"]=(informal & ~cuenta).astype(int) # D9: sólo informal, los nueve tipos formales.
    cuenta_eje=d[[f"P5_6_{i}" for i in [1,2,3,4,5,8,9]]].astype(str).apply(lambda x:x.apply(lambda y:y.str.strip().eq("1")).any(axis=1)).map({True:"con_cuenta",False:"sin_cuenta"})
    return _tabla(d,{"sexo":d.SEXO.str.strip(),"edad":_age(d.EDAD),"escolaridad":d.P3_1_1.str.strip(),"localidad":d.TLOC.str.strip(),"cuenta_formal":cuenta_eje},"PISOS-ENIF2021-D9")

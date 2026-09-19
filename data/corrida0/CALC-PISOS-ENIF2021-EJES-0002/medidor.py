from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

Medidor autocontenido. Cada réplica bootstrap se crea una vez por instrumento
y se comparte entre todas las celdas y desenlaces de esta corrida.
"""
import io
import zipfile
import numpy as np
import pandas as pd

EDADES=("18-29","30-44","45-59","60+")
ESCOLARIDAD=("hasta_primaria","secundaria","media_superior","superior")

def _csv(path,suffix,cols):
    with zipfile.ZipFile(path) as zf:
        names=[n for n in zf.namelist() if n.lower().endswith(suffix.lower())]
        if len(names)!=1: raise RuntimeError(f"miembro CSV no único: {suffix}: {names}")
        raw=zf.read(names[0])
    for enc in ("utf-8-sig","latin-1"):
        try:
            d=pd.read_csv(io.StringIO(raw.decode(enc)),dtype=str,
                          keep_default_na=False,na_filter=False)
            d.columns=[str(x).strip() for x in d.columns]
            missing=sorted(set(cols)-set(d.columns))
            if missing: raise RuntimeError(f"variables ausentes: {missing}")
            return d[cols].copy()
        except UnicodeDecodeError: pass
    raise RuntimeError(f"codificación no reconocida: {suffix}")

def _code(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)","",regex=True)

def _age(s):
    x=pd.to_numeric(s,errors="coerce")
    out=pd.Series(pd.NA,index=s.index,dtype="object")
    out[(x>=18)&(x<=29)]="18-29"; out[(x>=30)&(x<=44)]="30-44"
    out[(x>=45)&(x<=59)]="45-59"; out[(x>=60)&(x<=96)]="60+"
    return out

def _school(s):
    return _code(s).map({"0":"hasta_primaria","1":"hasta_primaria",
        "2":"hasta_primaria","3":"secundaria","4":"media_superior",
        "5":"media_superior","6":"media_superior","7":"media_superior",
        "8":"superior","9":"superior"})

def _slug(v):
    return (str(v).upper().replace("Á","A").replace("É","E").replace("Í","I")
            .replace("Ó","O").replace("Ú","U").replace("+","-MAS")
            .replace("_","-").replace(" ","-"))

def _cells(prefix,outcome,axes):
    return [{"base":f"RESULT-{prefix}-{_slug(axis)}-{_slug(cat)}",
             "mask":groups.eq(cat)&outcome.notna(),"y":outcome}
            for axis,(groups,cats) in axes.items() for cat in cats]

def _estimate(d,cells,reps=10000,seed=42):
    design=d["_w"].notna()&(d["_w"]>0)&d["_est"].ne("")&d["_upm"].ne("")
    w=d.loc[design].copy(); w["_key"]=w["_est"].astype(str)+"\t"+w["_upm"].astype(str)
    keys=sorted(w["_key"].unique()); pos={k:i for i,k in enumerate(keys)}
    denm=np.zeros((len(keys),len(cells))); num=np.zeros_like(denm)
    counts=np.zeros(len(cells),dtype=np.int64)
    for j,cell in enumerate(cells):
        chosen=w.loc[cell["mask"].reindex(w.index,fill_value=False)]
        y=cell["y"].reindex(chosen.index); counts[j]=len(chosen)
        for key,weight,value in zip(chosen["_key"],chosen["_w"],y):
            i=pos[key]; denm[i,j]+=float(weight); num[i,j]+=float(weight)*float(value)
    den=denm.sum(0)
    point=np.divide(num.sum(0),den,out=np.full(len(cells),np.nan),where=den>0)
    strata={}
    for key in keys: strata.setdefault(key.split("\t",1)[0],[]).append(pos[key])
    rng=np.random.Generator(np.random.PCG64(seed))
    boot=np.full((reps,len(cells)),np.nan)
    for start in range(0,reps,50):
        size=min(50,reps-start); mult=np.zeros((size,len(keys)),dtype=np.int16)
        for h in sorted(strata):
            ix=np.asarray(strata[h],dtype=int)
            draws=rng.integers(0,len(ix),size=(size,len(ix)))
            for row in range(size):
                mult[row]+=np.bincount(ix[draws[row]],minlength=len(keys)).astype(np.int16)
        den_b=mult@denm
        boot[start:start+size]=np.divide(mult@num,den_b,
            out=np.full_like(den_b,np.nan),where=den_b>0)
    out={}
    for j,cell in enumerate(cells):
        valid=np.isfinite(boot[:,j])
        if np.isfinite(point[j]) and valid.any():
            lo,hi=np.percentile(boot[valid,j],[2.5,97.5]); vals=(float(point[j]),float(lo),float(hi))
        else: vals=(None,None,None)
        rid=cell["base"]
        out[rid+"-P"],out[rid+"-IC-LO"],out[rid+"-IC-HI"]=vals
        out[rid+"-N"]=int(counts[j]); out[rid+"-DEN-W"]=float(den[j])
        out[rid+"-B-VALIDAS"]=int(valid.sum())
    return out

def _known_any(d,cols):
    c=d[cols].apply(_code); out=pd.Series(pd.NA,index=d.index,dtype="boolean")
    out.loc[c.eq("1").any(axis=1)]=True; out.loc[c.eq("2").all(axis=1)]=False
    return out

def _formal(d,accounts,savings):
    a=d[accounts].apply(_code); s=d[savings].apply(_code)
    out=pd.Series(pd.NA,index=d.index,dtype="boolean")
    yes=s.eq("1").any(axis=1)
    out.loc[(a.eq("2")|s.eq("2")).all(axis=1)&~yes]=False
    out.loc[yes]=True
    return out

def medir(inputs,contrato):
    z=inputs["enif2021_csv"]["ruta_absoluta"]
    inf=[f"P5_1_{i}" for i in range(1,7)]
    accounts=[f"P5_4_{i}" for i in range(1,10)]
    savings=[f"P5_7_{i}" for i in range(1,10)]
    cols=inf+accounts+savings+["SEXO","EDAD","TLOC","P3_1_1","FAC_ELE","EST_DIS","UPM_DIS"]
    d=_csv(z,"conjunto_de_datos_tmodulo_enif_2021.csv",cols)
    d["_w"]=pd.to_numeric(d["FAC_ELE"],errors="coerce")
    d["_est"]=d["EST_DIS"].str.strip(); d["_upm"]=d["UPM_DIS"].str.strip()
    informal=_known_any(d,inf); formal=_formal(d,accounts,savings)
    any_inf=informal.astype("Float64")
    only=pd.Series(pd.NA,index=d.index,dtype="Float64")
    only.loc[informal.eq(False)|formal.eq(True)]=0.0
    only.loc[informal.eq(True)&formal.eq(False)]=1.0
    a=d[accounts].apply(_code); account=pd.Series(pd.NA,index=d.index,dtype="object")
    account.loc[a.eq("1").any(axis=1)]="con cuenta"
    account.loc[a.eq("2").all(axis=1)]="sin cuenta"
    locality=_code(d["TLOC"]).map({"1":"15 000 y mas","2":"15 000 y mas",
        "3":"menor de 15 000","4":"menor de 15 000"})
    axes={"sexo":(_code(d["SEXO"]),("1","2")),"edad":(_age(d["EDAD"]),EDADES),
      "escolaridad":(_school(d["P3_1_1"]),ESCOLARIDAD),
      "localidad":(locality,("menor de 15 000","15 000 y mas")),
      "cuenta":(account,("sin cuenta","con cuenta"))}
    cells=_cells("PISOS-ENIF2021-V2-D9",only,axes)
    cells+=_cells("PISOS-ENIF2021-V2-INFORMAL-CUALQUIERA",any_inf,axes)
    out=_estimate(d,cells,int(contrato["parametros"]["bootstrap_replicas"]),
                  int(contrato["seed"]["valor"]))
    out.update({"RESULT-PISOS-ENIF2021-V2-FILAS-PERSONAS":int(len(d)),
      "RESULT-PISOS-ENIF2021-V2-D9-N-UNIVERSO":int(only.notna().sum()),
      "RESULT-PISOS-ENIF2021-V2-INFORMAL-CUALQUIERA-N-UNIVERSO":int(any_inf.notna().sum()),
      "RESULT-PISOS-ENIF2021-V2-D9-DESENLACE-INDEFINIDO":int(only.isna().sum()),
      "RESULT-PISOS-ENIF2021-V2-INFORMAL-CUALQUIERA-DESENLACE-INDEFINIDO":
        int(any_inf.isna().sum()),
      "RESULT-PISOS-ENIF2021-V2-FORMALIDAD-CELDAS-NO-CONSTRUIBLES":4})
    return out

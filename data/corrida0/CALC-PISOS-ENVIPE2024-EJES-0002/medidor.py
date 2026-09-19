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

def medir(inputs,contrato):
    z=inputs["envipe2024_csv"]["ruta_absoluta"]
    vic=_csv(z,"conjunto_de_datos_tmod_vic_envipe2024.csv",
        ["BP1_20","BP1_23","BP2_1","BPCOD","FAC_DEL","EST_DIS","UPM_DIS",
         "ID_PER","SEXO","EDAD","DOMINIO"])
    dem=_csv(z,"conjunto_de_datos_tsdem_envipe2024.csv",["ID_PER","NIV"])
    d=vic.merge(dem,on="ID_PER",how="left",validate="m:1",indicator=True)
    d["_w"]=pd.to_numeric(d["FAC_DEL"],errors="coerce")
    d["_est"]=d["EST_DIS"].str.strip(); d["_upm"]=d["UPM_DIS"].str.strip()
    b=_code(d["BP1_20"]); ev_ok=b.isin(["1","2"])
    ev=pd.Series(pd.NA,index=d.index,dtype="Float64")
    ev.loc[ev_ok]=(b.loc[ev_ok].eq("2")&
        _code(d.loc[ev_ok,"BP1_23"]).isin(["4","5","6","8"])).astype(float)
    ev_axes={"sexo":(_code(d["SEXO"]),("1","2")),
        "edad":(_age(d["EDAD"]),EDADES),
        "escolaridad":(_school(d["NIV"]),ESCOLARIDAD),
        "dominio":(d["DOMINIO"].str.strip().map(
            {"R":"Rural","C":"Complemento urbano","U":"Urbano"}),
            ("Rural","Complemento urbano","Urbano"))}
    den_ok=_code(d["BPCOD"]).eq("1")&b.isin(["1","2"])&_code(d["BP2_1"]).isin(["1","2"])
    den=pd.Series(pd.NA,index=d.index,dtype="Float64")
    den.loc[den_ok]=b.loc[den_ok].eq("1").astype(float)
    coverage=_code(d["BP2_1"]).map({"1":"asegurado","2":"no_asegurado"})
    cells=_cells("PISOS-ENVIPE2024-V2-EVASION",ev,ev_axes)
    cells+=_cells("PISOS-ENVIPE2024-V2-DENUNCIA",den,
        {"cobertura_seguro":(coverage,("no_asegurado","asegurado"))})
    out=_estimate(d,cells,int(contrato["parametros"]["bootstrap_replicas"]),
                  int(contrato["seed"]["valor"]))
    out.update({"RESULT-PISOS-ENVIPE2024-V2-FILAS-VICTIMIZACION":int(len(vic)),
      "RESULT-PISOS-ENVIPE2024-V2-JOIN-SIN-DEMOGRAFIA":int(d["_merge"].ne("both").sum()),
      "RESULT-PISOS-ENVIPE2024-V2-EVASION-N-UNIVERSO":int(ev_ok.sum()),
      "RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-N-UNIVERSO":int(den_ok.sum()),
      "RESULT-PISOS-ENVIPE2024-V2-BP1-20-FUERA":int((~b.isin(["1","2"])).sum())})
    return out

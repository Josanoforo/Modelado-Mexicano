#!/usr/bin/env python3
"""Medidor autocontenido de CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001.

El primer evento no se desempata por orden del archivo: un empate en el año
mínimo con códigos distintos se declara incompatible y no entra al estimando.
"""
from __future__ import annotations
import argparse, io, json, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ID = "CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001"
P = "RESULT-EDER2017-PRIMERA-UNION-SEXO-COHORTE-"
KEY = ["folioviv", "foliohog", "id_pobla"]
LIBRE = {"1","12","13","14","17","18","126"}
DIRECTO = {"2","3","4","26","27","28","46","47","48"}
COHORTES = ["<=1970", "1971-1980", "1981-1990", "1991+"]

def _member(z, name):
    x=[n for n in z.namelist() if n.rsplit("/",1)[-1].lower()==name]
    if len(x)!=1: raise ValueError("miembro ambiguo/ausente: "+name)
    return x[0]

def _read(z, name, cols):
    b=z.read(_member(z,name)).replace(b"\r\n",b"\n").replace(b"\r",b"\n")
    d=pd.read_csv(io.BytesIO(b),encoding="latin-1",dtype=str,keep_default_na=False,low_memory=False)
    d.columns=[c.strip().lstrip("\ufeff").lstrip("ï»¿").lower() for c in d.columns]
    # INEGI's CSV can retain a UTF-8 BOM after latin-1 decoding.  Resolve a
    # requested field only when its exact name or one unique suffixed name is
    # available; ambiguity is an error rather than an accidental selection.
    rename={}
    for c in cols:
        candidates=[h for h in d.columns if h==c or h.endswith(c)]
        if len(candidates)==1: rename[candidates[0]]=c
    miss=[c for c in cols if c not in rename.values()]
    if miss: raise ValueError(name+" columna ausente: "+",".join(miss))
    return d[list(rename)].rename(columns=rename)[cols]

def _coh(x):
    if not np.isfinite(x): return "desconocida"
    return "<=1970" if x<=1970 else "1971-1980" if x<=1980 else "1981-1990" if x<=1990 else "1991+"

def carga(zip_path):
  with zipfile.ZipFile(zip_path) as z:
    hv=_read(z,"historiavida.csv",KEY+["anio_retro","anio_nac","edo_civil1"])
    ant=_read(z,"antecedentes.csv",KEY+["factor_per"])
    per=_read(z,"persona.csv",KEY+["sexo"])
    viv=_read(z,"vivienda.csv",["folioviv","est_dis","upm"])
  audit={"filas_historiavida":len(hv),"personas_historiavida":int(hv[KEY].drop_duplicates().shape[0]),
         "persona_llave_unica":bool(not per.duplicated(KEY).any()),"antecedentes_llave_unica":bool(not ant.duplicated(KEY).any()),"vivienda_llave_unica":bool(not viv.duplicated(["folioviv"]).any())}
  if not all(audit[k] for k in ("persona_llave_unica","antecedentes_llave_unica","vivienda_llave_unica")): raise ValueError("llave no unica")
  hv["edo_civil1"]=hv.edo_civil1.str.strip(); hv["anio"] = pd.to_numeric(hv.anio_retro,errors="coerce")
  nz=hv[(hv.edo_civil1!="")&(hv.edo_civil1!="0")&hv.anio.notna()].copy()
  mins=nz.groupby(KEY,dropna=False).anio.transform("min"); first=nz[nz.anio.eq(mins)].copy()
  ncode=first.groupby(KEY).edo_civil1.nunique(); bad=ncode[ncode>1].index
  audit["sin_primera_union_observada"]=int(hv[KEY].drop_duplicates().shape[0]-nz[KEY].drop_duplicates().shape[0]); audit["empates_incompatibles"]=int(len(bad))
  first=first.merge(ncode.rename("ncode"),left_on=KEY,right_index=True,how="left"); first=first[first.ncode.eq(1)].drop_duplicates(KEY)
  d=first.merge(ant,on=KEY,how="left",indicator="_ant").merge(per,on=KEY,how="left",indicator="_per").merge(viv,on="folioviv",how="left",indicator="_viv")
  audit.update({"huerfanos_antecedentes":int((d._ant!="both").sum()),"huerfanos_persona":int((d._per!="both").sum()),"huerfanos_vivienda":int((d._viv!="both").sum())})
  d["w"]=pd.to_numeric(d.factor_per,errors="coerce"); d=d[np.isfinite(d.w)&(d.w>0)].copy()
  d["sexo_cat"]=d.sexo.map({"1":"hombre","2":"mujer"}).fillna("desconocido")
  d["cohorte"]=pd.to_numeric(d.anio_nac,errors="coerce").map(_coh)
  d["tipo"]=np.where(d.edo_civil1.isin(LIBRE),"libre",np.where(d.edo_civil1.isin(DIRECTO),"directo","sin_clasificar"))
  d["design_ok"]=(d.est_dis.str.strip()!="")&(d.upm.str.strip()!="")
  audit["primera_disolucion"] = int(d.edo_civil1.isin({"6","7","8","60","70","80"}).sum())
  audit["sexo_desconocido"] = int((d.sexo_cat=="desconocido").sum()); audit["cohorte_desconocida"] = int((d.cohorte=="desconocida").sum())
  audit["universo_factor_valido"] = int(len(d)); audit["sin_diseno"] = int((~d.design_ok).sum())
  return d,audit

def point(d, mask):
  x=d[mask]; den=x.w.sum()
  return {"n":int(len(x)),"masa":float(den),"libre":float((x.w*(x.tipo=="libre")).sum()/den) if den else None,"directo":float((x.w*(x.tipo=="directo")).sum()/den) if den else None,"sin_clasificar":float((x.w*(x.tipo=="sin_clasificar")).sum()/den) if den else None}

def bootstrap(d, reps=2000, seed=20260919):
  d=d[d.design_ok].copy(); rng=np.random.Generator(np.random.PCG64(seed)); d["cl"]=d.est_dis.str.strip()+"\x1f"+d.upm.str.strip()
  cls=d[["cl","est_dis"]].drop_duplicates().sort_values(["est_dis","cl"]); totals=[]; single=0
  for _,g in cls.groupby("est_dis",sort=True):
    a=g.cl.to_numpy(); k=len(a); single+=k==1; totals.append((a,k))
  vals=[]
  for r in range(reps):
    mult={c:0 for c in cls.cl}
    for a,k in totals:
      for c in a[rng.integers(0,k,k)]: mult[c]+=1
    w=d.w.to_numpy()*d.cl.map(mult).to_numpy(); vals.append(_summary(d,w))
  return vals,{"replicas_solicitadas":reps,"estratos_singleton":single,"replicas_validas":reps}

def _summary(d,w):
  z=d.assign(wb=w); good=(z.sexo_cat.isin(["mujer","hombre"]))&(z.cohorte.isin(COHORTES)); out={}
  # cohort contrasts and reference shares use all first-union types, including residual.
  for c in COHORTES:
    a=[]
    for s in ("mujer","hombre"):
      q=z[(z.sexo_cat==s)&(z.cohorte==c)]; den=q.wb.sum(); a.append(None if den==0 else float((q.wb*(q.tipo=="libre")).sum()/den))
    out["coh_"+c]=None if None in a else a[0]-a[1]
  q=z[good]; wm=q[q.sexo_cat=="mujer"]; wh=q[q.sexo_cat=="hombre"]
  def p(x): return None if x.wb.sum()==0 else float((x.wb*(x.tipo=="libre")).sum()/x.wb.sum())
  out["cruda"]=None if p(wm) is None or p(wh) is None else p(wm)-p(wh)
  ref=q.groupby("cohorte").wb.sum(); den=ref.sum(); alpha={c:(ref.get(c,0)/den if den else 0) for c in COHORTES}
  pm=[]; ph=[]
  for c in COHORTES:
    pm.append(p(wm[wm.cohorte==c])); ph.append(p(wh[wh.cohorte==c]))
  out["estandarizada"]=None if None in pm+ph or den==0 else float(sum(alpha[c]*(a-b) for c,a,b in zip(COHORTES,pm,ph)))
  out["cambio"]=None if out["cruda"] is None or out["estandarizada"] is None else out["estandarizada"]-out["cruda"]
  return out

def ci(x):
  a=np.array([v for v in x if v is not None],float)
  return {"ee":float(a.std(ddof=1)) if len(a)>1 else None,"ic95":[float(np.percentile(a,2.5)),float(np.percentile(a,97.5))] if len(a)>=1000 else None,"replicas_validas":int(len(a))}

def medir(inputs, contrato):
  d,a=carga(inputs["eder_2017_eder2017_bases_csv"]["ruta_absoluta"]); return {P+"ESTADO":"ESTIMABLE",P+"RESUMEN":json.dumps(a,sort_keys=True)}

def run(zip_path,outdir):
  d,a=carga(zip_path); rows=[]
  for dim,vals in [("total",["total"]),("sexo",["hombre","mujer","desconocido"]),("cohorte",COHORTES+["desconocida"])]:
    for v in vals:
      m=np.ones(len(d),bool) if v=="total" else (d[dim if dim!="sexo" else "sexo_cat"].eq(v).to_numpy())
      rows.append({"dimension":dim,"categoria":v,**point(d,m)})
  for s in ("hombre","mujer"):
    for c in COHORTES: rows.append({"dimension":"sexo_x_cohorte","categoria":s+"|"+c,**point(d,(d.sexo_cat==s)&(d.cohorte==c))})
  reps,design=bootstrap(d); base=_summary(d,d.w.to_numpy()); con=[]
  for c in COHORTES: con.append({"contraste":"mujer-hombre libre "+c,"p_mujer":point(d,(d.sexo_cat=="mujer")&(d.cohorte==c))["libre"],"p_hombre":point(d,(d.sexo_cat=="hombre")&(d.cohorte==c))["libre"],"diferencia":base["coh_"+c],**ci([x["coh_"+c] for x in reps])})
  for k in ("cruda","estandarizada","cambio"): con.append({"contraste":k,"diferencia":base[k],**ci([x[k] for x in reps])})
  valid=d[d.sexo_cat.isin(["mujer","hombre"])&d.cohorte.isin(COHORTES)]; ref=valid.groupby("cohorte").w.sum(); ref=(ref/ref.sum()).reindex(COHORTES).reset_index(name="peso_referencia")
  out=Path(outdir); out.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(out/"perfiles.csv",index=False); pd.DataFrame(con).to_csv(out/"contrastes.csv",index=False); ref.to_csv(out/"pesos_estandarizacion.csv",index=False)
  result={"calc_id":ID,"auditoria":a,"diseno":design,"perfiles":rows,"contrastes":con,"pesos_estandarizacion":ref.to_dict("records")}; (out/"resultados.json").write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); return result

if __name__=="__main__":
  q=argparse.ArgumentParser(); q.add_argument("--zip",required=True); q.add_argument("--out",required=True); a=q.parse_args(); run(a.zip,a.out)

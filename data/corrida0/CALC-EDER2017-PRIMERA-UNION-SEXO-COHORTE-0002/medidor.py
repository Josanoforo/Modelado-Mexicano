#!/usr/bin/env python3
"""Medidor autocontenido de CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002.

El primer evento no se desempata por orden del archivo: un empate en el año
mínimo con códigos distintos se declara incompatible y no entra al estimando.
"""
from __future__ import annotations
import argparse, io, json, zipfile, tempfile
from pathlib import Path
import numpy as np
import pandas as pd

ID = "CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002"
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
  # Marco de bootstrap: TODAS las personas ponderables, antes de dominio.
  # Las fuera de primera unión o de sexo/cohorte válido permanecen con cero.
  d=ant.merge(per,on=KEY,how="left",indicator="_per").merge(viv,on="folioviv",how="left",indicator="_viv")
  d=d.merge(first[KEY+["anio_nac","edo_civil1"]],on=KEY,how="left")
  audit.update({"huerfanos_antecedentes":0,"huerfanos_persona":int((d._per!="both").sum()),"huerfanos_vivienda":int((d._viv!="both").sum())})
  d["w"]=pd.to_numeric(d.factor_per,errors="coerce"); d=d[np.isfinite(d.w)&(d.w>0)].copy()
  d["sexo_cat"]=d.sexo.map({"1":"hombre","2":"mujer"}).fillna("desconocido")
  d["cohorte"]=pd.to_numeric(d.anio_nac,errors="coerce").map(_coh)
  d["in_domain"]=d.edo_civil1.notna()
  d["tipo"]=np.where(d.edo_civil1.isin(LIBRE),"libre",np.where(d.edo_civil1.isin(DIRECTO),"directo","sin_clasificar"))
  d["design_ok"]=(d.est_dis.str.strip()!="")&(d.upm.str.strip()!="")
  audit["primera_disolucion"] = int(d.edo_civil1.isin({"6","7","8","60","70","80"}).sum())
  audit["sexo_desconocido"] = int((d.sexo_cat=="desconocido").sum()); audit["cohorte_desconocida"] = int((d.cohorte=="desconocida").sum())
  audit["marco_ponderable_completo"] = int(len(d)); audit["universo_factor_valido"] = int(d.in_domain.sum()); audit["sin_diseno"] = int((~d.design_ok & d.in_domain).sum())
  return d,audit

def point(d, mask):
  x=d[mask]; den=x.w.sum()
  return {"n":int(len(x)),"masa":float(den),"libre":float((x.w*(x.tipo=="libre")).sum()/den) if den else None,"directo":float((x.w*(x.tipo=="directo")).sum()/den) if den else None,"sin_clasificar":float((x.w*(x.tipo=="sin_clasificar")).sum()/den) if den else None}

def bootstrap(d, reps=2000, seed=20260919):
  # Agrega primero por UPM×sexo×cohorte. Así cada réplica comparte exactamente
  # el sorteo de todos los estimandos, sin recorrer las personas 2,000 veces.
  frame=d[d.design_ok].copy(); frame["cl"]=frame.est_dis.str.strip()+"\x1f"+frame.upm.str.strip()
  z=frame[frame.in_domain & frame.sexo_cat.isin(["mujer","hombre"]) & frame.cohorte.isin(COHORTES)].copy()
  cls=frame[["cl","est_dis"]].drop_duplicates().sort_values(["est_dis","cl"]).reset_index(drop=True)
  cmap={c:i for i,c in enumerate(cls.cl)}; C=len(cls); den=np.zeros((C,8)); free=np.zeros((C,8))
  for row in z.itertuples():
    j=(0 if row.sexo_cat=="mujer" else 1)*4+COHORTES.index(row.cohorte); i=cmap[row.cl]
    den[i,j]+=row.w
    if row.tipo=="libre": free[i,j]+=row.w
  rng=np.random.Generator(np.random.PCG64(seed)); M=np.zeros((reps,C)); single=0
  for _,g in cls.groupby("est_dis",sort=True):
    pos=g.index.to_numpy(); k=len(pos); single+=k==1
    draw=rng.integers(0,k,size=(reps,k));
    for j in range(k): M[np.arange(reps),pos[draw[:,j]]]+=1
  D=M@den; F=M@free; vals=[]
  for r in range(reps):
    x={}; pm=F[r,:4]/D[r,:4]; ph=F[r,4:]/D[r,4:]
    x.update({"coh_"+c:float(pm[i]-ph[i]) if D[r,i]>0 and D[r,i+4]>0 else None for i,c in enumerate(COHORTES)})
    x["cruda"]=float(F[r,:4].sum()/D[r,:4].sum()-F[r,4:].sum()/D[r,4:].sum()) if D[r,:4].sum()>0 and D[r,4:].sum()>0 else None
    al=(D[r,:4]+D[r,4:]); al=al/al.sum() if al.sum()>0 else al
    x["estandarizada"]=float(np.sum(al*(pm-ph))) if np.isfinite(pm).all() and np.isfinite(ph).all() else None
    x["cambio"]=None if x["estandarizada"] is None or x["cruda"] is None else x["estandarizada"]-x["cruda"]
    vals.append(x)
  return vals,{"replicas_solicitadas":reps,"estratos_singleton":single,"replicas_validas":reps,"n_upm":C,"marco":"personas ponderables completas; contribución cero fuera del dominio"},M,cmap

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
  with tempfile.TemporaryDirectory(prefix="eder-replay-") as tmp:
    out=Path(tmp); r=run(inputs["eder_2017_eder2017_bases_csv"]["ruta_absoluta"],out)
    hashes={p.name:__import__("hashlib").sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob("*.csv"))}
  return {P+"ESTADO":"ESTIMABLE",P+"RESUMEN":json.dumps({"auditoria":r["auditoria"],"tablas_sha256":hashes},sort_keys=True)}

def run(zip_path,outdir):
  d,a=carga(zip_path); u=d[d.in_domain].copy(); rows=[]
  for dim,vals in [("total",["total"]),("sexo",["hombre","mujer","desconocido"]),("cohorte",COHORTES+["desconocida"])]:
    for v in vals:
      m=np.ones(len(u),bool) if v=="total" else (u[dim if dim!="sexo" else "sexo_cat"].eq(v).to_numpy())
      rows.append({"dimension":dim,"categoria":v,**point(u,m)})
  for s in ("hombre","mujer"):
    for c in COHORTES: rows.append({"dimension":"sexo_x_cohorte","categoria":s+"|"+c,**point(u,(u.sexo_cat==s)&(u.cohorte==c))})
  reps,design,M,cmap=bootstrap(d); base=_summary(u,u.w.to_numpy()); con=[]
  # Perfil: misma matriz de réplicas de UPM; categorías fuera de dominio ya
  # tienen contribución cero porque M procede del marco completo.
  u["cl"]=u.est_dis.str.strip()+"\x1f"+u.upm.str.strip()
  for row in rows:
    if row["n"]==0: row.update({"ee_libre":None,"ic95_libre":None,"ee_directo":None,"ic95_directo":None,"ee_sin_clasificar":None,"ic95_sin_clasificar":None}); continue
    if row["dimension"]=="total": q=u
    elif row["dimension"]=="sexo": q=u[u.sexo_cat==row["categoria"]]
    elif row["dimension"]=="cohorte": q=u[u.cohorte==row["categoria"]]
    else:
      s,c=row["categoria"].split("|"); q=u[(u.sexo_cat==s)&(u.cohorte==c)]
    den=np.zeros(M.shape[1]); np.add.at(den,[cmap[x] for x in q.cl],q.w.to_numpy())
    for typ in ("libre","directo","sin_clasificar"):
      num=np.zeros(M.shape[1]); qq=q[q.tipo==typ]; np.add.at(num,[cmap[x] for x in qq.cl],qq.w.to_numpy()); vv=(M@num)/(M@den); zz=ci(vv.tolist()); row["ee_"+typ]=zz["ee"]; row["ic95_"+typ]=zz["ic95"]
  for c in COHORTES: con.append({"contraste":"mujer-hombre libre "+c,"p_mujer":point(u,(u.sexo_cat=="mujer")&(u.cohorte==c))["libre"],"p_hombre":point(u,(u.sexo_cat=="hombre")&(u.cohorte==c))["libre"],"diferencia":base["coh_"+c],**ci([x["coh_"+c] for x in reps])})
  for k in ("cruda","estandarizada","cambio"): con.append({"contraste":k,"diferencia":base[k],**ci([x[k] for x in reps])})
  valid=u[u.sexo_cat.isin(["mujer","hombre"])&u.cohorte.isin(COHORTES)]; ref=valid.groupby("cohorte").w.sum(); ref=(ref/ref.sum()).reindex(COHORTES).reset_index(name="peso_referencia")
  out=Path(outdir); out.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(out/"perfiles.csv",index=False); pd.DataFrame(con).to_csv(out/"contrastes.csv",index=False); ref.to_csv(out/"pesos_estandarizacion.csv",index=False)
  result={"calc_id":ID,"auditoria":a,"diseno":design,"perfiles":rows,"contrastes":con,"pesos_estandarizacion":ref.to_dict("records")}; (out/"resultados.json").write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); return result

if __name__=="__main__":
  q=argparse.ArgumentParser(); q.add_argument("--zip",required=True); q.add_argument("--out",required=True); a=q.parse_args(); run(a.zip,a.out)

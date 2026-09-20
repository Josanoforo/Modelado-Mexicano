#!/usr/bin/env python3
"""Precisión condicional de las seis interacciones WBES México 2023."""
from __future__ import annotations

import csv, hashlib, importlib.util, io, math, zipfile
from pathlib import Path
import pandas as pd
from scipy.stats import t as student_t

CALC_ID = "CALC-WBES2023-PRECISION-INTERACCIONES-0001"
PARENT_ID = "CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001"
PRECISION_TYPE = "IC-APROXIMADO-CONDICIONAL-A-SUPUESTOS"
SCENARIOS = ("SINGLETON-CERTEZA", "SINGLETON-AVERAGE")
STRATUM = "strata"
INPUTS = ("wbes_mexico_2023_ddi_xml", "wbes_mexico_2023_ddi_pdf", "wbes_mexico_2023_microdato_dta_zip", "wbes_mexico_2023_documentacion_zip", "wbes_sampling_note_consolidated_2022_pdf")
EXPECTED_SHA256 = {"wbes_mexico_2023_ddi_xml":"1d5cded32bef39cc2f129ef63c122d59e4e37b1257b36fc98bc0cc8daccad54c", "wbes_mexico_2023_ddi_pdf":"069fe4981e1e5d3b2d765009462fc51d24892d6593724f46a8985561b69ae603", "wbes_mexico_2023_microdato_dta_zip":"bc09225244f1e1274d9c9e58221acf8884512a1ab600551f98fbc0466f479f3f", "wbes_mexico_2023_documentacion_zip":"2b3b0db77f12b841814a37265db279cfcb1778c4377876b77e0a4b725a76c0f7", "wbes_sampling_note_consolidated_2022_pdf":"199b37eac44a700146e2f75ec84e2afc79eda52fb48fd2a2059e50ac9df8fa74"}
OUT = ["tipo_fila","interaccion_id","interaccion","ventana_referencia","dominio_id","dominio","escenario_singleton","n_marco","masa_marco","n_expuestos","masa_expuestos","n_si","masa_si","n_no","masa_no","n_desconocidos","masa_desconocidos","tasa_observada","limite_inferior_faltantes","limite_superior_faltantes","anchura_identificacion_faltantes","ee","ic95_inferior","ic95_superior","anchura_ic95","n_unidades_diseno","n_estratos","n_singleton","grados_libertad","covarianza_diseno","cobertura_doble_expuestos","estado"]

def _parent():
 p=Path(__file__).resolve().parents[1]/PARENT_ID/"medidor.py"; s=importlib.util.spec_from_file_location("wbes_parent",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
PARENT=_parent()
REQUIRED=set(PARENT.REQUIRED_COLUMNS)|{STRATUM}

def _code(v, n):
 return PARENT._is_code(v,n)
def _class(frame, interaction):
 return PARENT._classifications(frame,interaction)
def validate_design(frame):
 PARENT.validate_frame(frame)
 if STRATUM not in frame: raise ValueError("CAMPO-DISENO-AUSENTE:strata")
 if frame[STRATUM].isna().any() or frame[STRATUM].nunique()<2: raise ValueError("DISENO-ESTRATO-INVALIDO")

def profile(frame):
 counts=frame.groupby(STRATUM).size()
 return len(frame),len(counts),int((counts==1).sum()),int((counts-1).clip(lower=0).sum())
def variance(frame, influence, scenario):
 pieces=[]; single=0
 for _,ix in frame.groupby(STRATUM,sort=True).groups.items():
  z=[float(influence.loc[i]) for i in ix]; n=len(z)
  if n==1: single+=1; continue
  mean=math.fsum(z)/n; pieces.append(n/(n-1)*math.fsum((v-mean)**2 for v in z))
 v=math.fsum(pieces)
 if scenario=="SINGLETON-AVERAGE":
  if not pieces: raise ValueError("SIN-ESTRATOS-NO-SINGLETON")
  v*= (len(pieces)+single)/len(pieces)
 return v
def covar(frame, a, b, scenario):
 pieces=[]; single=0
 for _,ix in frame.groupby(STRATUM,sort=True).groups.items():
  x=[float(a.loc[i]) for i in ix]; y=[float(b.loc[i]) for i in ix]; n=len(x)
  if n==1: single+=1; continue
  mx=math.fsum(x)/n; my=math.fsum(y)/n
  pieces.append(n/(n-1)*math.fsum((u-mx)*(v-my) for u,v in zip(x,y)))
 z=math.fsum(pieces)
 return z*((len(pieces)+single)/len(pieces)) if scenario=="SINGLETON-AVERAGE" else z
def interval(p,se,df):
 if p<=0 or p>=1: return None,None,"PRECISION-NO-ESTIMABLE-FRONTERA"
 if not math.isfinite(se) or df<=0: return None,None,"PRECISION-NO-ESTIMABLE-VARIANZA-O-GL"
 q=student_t.ppf(.975,df); l=math.log(p/(1-p)); sl=se/(p*(1-p)); inv=lambda x:1/(1+math.exp(-x))
 return inv(l-q*sl),inv(l+q*sl),"OK"
def _interaction(frame, item, domain=("TOTAL","Total nacional cubierto",None), scenario="SINGLETON-CERTEZA"):
 iid,label,_,_,window=item; did,dlabel,size=domain; mask=pd.Series(True,index=frame.index) if size is None else frame[PARENT.SIZE].map(lambda x:_code(x,size))
 elig,out=_class(frame,item); exposed=mask&elig.eq("eligible"); yes=exposed&out.eq("yes"); no=exposed&out.eq("no"); unk=exposed&out.eq("unknown")
 w=frame[PARENT.WEIGHT]; wy=float(w[yes].sum()); wn=float(w[no].sum()); wu=float(w[unk].sum()); we=wy+wn+wu; den=wy+wn
 p=wy/den if den else None; lo=wy/we if we else None; hi=(wy+wu)/we if we else None
 n,nh,ns,df=profile(frame); infl=pd.Series(0.,index=frame.index) if not den else w*(yes.astype(float)-p*(yes|no).astype(float))/den
 va=variance(frame,infl,scenario) if p is not None else float("nan"); se=math.sqrt(max(0,va)) if math.isfinite(va) else None; il,ih,status=interval(p,se,df) if p is not None else (None,None,"DENOMINADOR-VACIO")
 return {"tipo_fila":"INTERACCION","interaccion_id":iid,"interaccion":label,"ventana_referencia":window,"dominio_id":did,"dominio":dlabel,"escenario_singleton":scenario,"n_marco":int(mask.sum()),"masa_marco":float(w[mask].sum()),"n_expuestos":int(exposed.sum()),"masa_expuestos":we,"n_si":int(yes.sum()),"masa_si":wy,"n_no":int(no.sum()),"masa_no":wn,"n_desconocidos":int(unk.sum()),"masa_desconocidos":wu,"tasa_observada":p,"limite_inferior_faltantes":lo,"limite_superior_faltantes":hi,"anchura_identificacion_faltantes":hi-lo if hi is not None else None,"ee":se,"ic95_inferior":il,"ic95_superior":ih,"anchura_ic95":ih-il if ih is not None else None,"n_unidades_diseno":n,"n_estratos":nh,"n_singleton":ns,"grados_libertad":df,"covarianza_diseno":None,"cobertura_doble_expuestos":None,"estado":PRECISION_TYPE if status=="OK" else status},infl
def contrast(frame, scenario):
 fiscal=PARENT.INTERACTIONS[3]; op=PARENT.INTERACTIONS[5]; ef,of=_class(frame,fiscal); eo,oo=_class(frame,op); common=ef.eq("eligible")&eo.eq("eligible"); valid=common&of.isin(("yes","no"))&oo.isin(("yes","no")); w=frame[PARENT.WEIGHT]; den=float(w[valid].sum())
 if not den: return {k:None for k in OUT}|{"tipo_fila":"CONTRASTE","interaccion_id":"FISCAL-MENOS-OPERACION","interaccion":"Fiscal menos licencia de operación","escenario_singleton":scenario,"estado":"NO-ESTIMABLE-SIN-SOPORTE"}
 yf=(valid&of.eq("yes")).astype(float); yo=(valid&oo.eq("yes")).astype(float); pf=float((w*yf).sum()/den); po=float((w*yo).sum()/den); d=pf-po; a=w*(yf-pf*valid.astype(float))/den; b=w*(yo-po*valid.astype(float))/den; vd=variance(frame,a-b,scenario); cv=covar(frame,a,b,scenario); n,nh,ns,df=profile(frame); q=student_t.ppf(.975,df) if df else float("nan"); se=math.sqrt(vd); lo=d-q*se if df else None; hi=d+q*se if df else None
 return {"tipo_fila":"CONTRASTE","interaccion_id":"FISCAL-MENOS-OPERACION","interaccion":"Inspección fiscal menos licencia de operación","ventana_referencia":"fiscal: último año; operación: últimos dos años","dominio_id":"TOTAL","dominio":"Total, desenlaces dobles válidos","escenario_singleton":scenario,"n_marco":len(frame),"masa_marco":float(w.sum()),"n_expuestos":int(common.sum()),"masa_expuestos":float(w[common].sum()),"n_si":int((valid&of.eq("yes")).sum()),"masa_si":float((w*(valid&of.eq("yes"))).sum()),"n_no":int((valid&oo.eq("yes")).sum()),"masa_no":float((w*(valid&oo.eq("yes"))).sum()),"n_desconocidos":int((common&~valid).sum()),"masa_desconocidos":float(w[common&~valid].sum()),"tasa_observada":d,"limite_inferior_faltantes":None,"limite_superior_faltantes":None,"anchura_identificacion_faltantes":None,"ee":se,"ic95_inferior":lo,"ic95_superior":hi,"anchura_ic95":hi-lo if hi is not None else None,"n_unidades_diseno":n,"n_estratos":nh,"n_singleton":ns,"grados_libertad":df,"covarianza_diseno":cv,"cobertura_doble_expuestos":den/float(w[common].sum()),"estado":"IC-DIFERENCIA-T-95-CONDICIONAL" ,"punto_fiscal":pf,"punto_operacion":po}
def calculate(frame):
 validate_design(frame); rows=[]
 for item in PARENT.INTERACTIONS:
  for domain in PARENT.DOMAINS:
   for s in SCENARIOS: rows.append(_interaction(frame,item,domain,s)[0])
 for s in SCENARIOS: rows.append(contrast(frame,s))
 return rows
def _fmt(v): return "" if v is None else (f"{v:.12f}" if isinstance(v,float) else str(v))
def serialize(rows):
 b=io.StringIO(newline=""); w=csv.DictWriter(b,fieldnames=OUT,extrasaction="ignore",lineterminator="\n"); w.writeheader(); w.writerows([{k:_fmt(r.get(k)) for k in OUT} for r in rows]); return b.getvalue().encode()
def medir(inputs,contrato):
 raw={k:(inputs[k].get("bytes") or Path(inputs[k]["ruta_absoluta"]).read_bytes()) for k in INPUTS}
 for k,v in raw.items():
  if hashlib.sha256(v).hexdigest()!=EXPECTED_SHA256[k]: raise ValueError("SHA256-INESPERADO:"+k)
 if not raw[INPUTS[0]].lstrip().startswith(b"<?xml") or not raw[INPUTS[1]].startswith(b"%PDF") or not raw[INPUTS[4]].startswith(b"%PDF"): raise ValueError("DOCUMENTACION-INVALIDA")
 with zipfile.ZipFile(io.BytesIO(raw[INPUTS[2]])) as z: frame=pd.read_stata(io.BytesIO(z.read("Mexico-2023-full-data.dta")),columns=sorted(REQUIRED),convert_categoricals=False)
 rows=calculate(frame); out=Path(__file__).resolve().parents[3]/"forense/analisis/wbes2023-precision-interacciones-cli-2/wbes2023-precision-interacciones.csv"; out.parent.mkdir(parents=True,exist_ok=True); blob=serialize(rows); out.write_bytes(blob)
 r={"RESULT-WBES2023-INT-G-TIPO":PRECISION_TYPE,"RESULT-WBES2023-INT-G-CSV-SHA256":hashlib.sha256(blob).hexdigest(),"RESULT-WBES2023-INT-G-SALIDA":str(out.relative_to(Path(__file__).resolve().parents[3])),"RESULT-WBES2023-INT-G-N-FILAS":len(rows)}
 for row in rows:
  if row["tipo_fila"]=="CONTRASTE":
   z="CERTEZA" if row["escenario_singleton"].endswith("CERTEZA") else "AVERAGE"; r[f"RESULT-WBES2023-INT-CONTRASTE-{z}-DIFERENCIA"]=row["tasa_observada"]; r[f"RESULT-WBES2023-INT-CONTRASTE-{z}-COVARIANZA"]=row["covarianza_diseno"]
 return r

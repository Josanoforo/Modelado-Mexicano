#!/usr/bin/env python3
"""Medición descriptiva fijada de consistencia de familia en ISSP México."""
from __future__ import annotations

import csv, hashlib, io, json, math, tempfile, zipfile
from itertools import combinations
from pathlib import Path

import pandas as pd

CALC_ID = "CALC-ISSP2017-CONSISTENCIA-APOYO-FAMILIAR-0001"
ANALYSIS = "forense/analisis/issp2017-consistencia-apoyo-familiar-cli-2"
PRECISION = "EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO"
VARS = [("v21", "Q7a", "Hogar o jardín"), ("v22", "Q7b", "Hogar durante enfermedad"), ("v23", "Q7c", "Hablar al sentirse deprimido"), ("v24", "Q7d", "Consejo sobre problemas familiares"), ("v25", "Q7e", "Ocasión social agradable")]
CATS = [(1, "Familiar cercano"), (2, "Familiar más lejano"), (3, "Amigo cercano"), (4, "Vecino"), (5, "Compañero de trabajo"), (6, "Alguien más"), (7, "Ninguno")]
EXPECTED = {"za6980_q_mx":"61bc0c80415521965ec1b2546fbe3b2400cfacb2e6b0b542583304821544f2ed", "za6980_backgroundvar_mx":"6004c300ca1331bfd15f163c4deaa726c71b66b46ae9e05361f40ae8cc26ca5f", "za6980_v2_0_0_dta":"aa3bfcbcc1dc20a2735e8e9d2d3d47a72d909dade66e8c4623b910965dc227de", "za6980_v2_0_0_sav":"20a1420f4aa8f8dcb30f7de61879796d20b7c3042805e7925e56c30b4ae97ca5"}
COLS = ["studyno","doi","version","country","c_alphan","CASEID","SEX","WEIGHT",*[v for v,_,_ in VARS]]
BASE = ["tipo","calc_id","pais","universo","precision","estado"]

def sha(raw): return hashlib.sha256(raw).hexdigest()
def raw(entry): return entry["bytes"] if entry.get("bytes") is not None else Path(entry["ruta_absoluta"]).read_bytes()
def num(s): return pd.to_numeric(s, errors="coerce")
def ratio(a,b): return None if b <= 0 else a/b
def fmt(x):
    if x is None or (isinstance(x,float) and math.isnan(x)): return ""
    return f"{x:.12f}" if isinstance(x,float) else str(x)
def serial(rows, cols):
    out=io.StringIO(newline=""); w=csv.DictWriter(out,fieldnames=cols,lineterminator="\n"); w.writeheader(); w.writerows([{k:fmt(r.get(k)) for k in cols} for r in rows]); return out.getvalue().encode()
def base(state="OK"): return {"tipo":"RESULT","calc_id":CALC_ID,"pais":"México","universo":"Muestra ISSP 2017 México","precision":PRECISION,"estado":state}
def wok(f): return f.WEIGHT.notna() & f.WEIGHT.map(math.isfinite) & f.WEIGHT.gt(0)
def valid(f,v): return wok(f) & f[v].isin(range(1,8))
def write(name, rows, cols):
    payload=serial(rows,cols); p=Path(__file__).resolve().parents[3]/ANALYSIS/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(payload); return sha(payload)

def source(inputs):
    payload={k:raw(inputs[k]) for k in EXPECTED}
    for k, expected in EXPECTED.items():
        if sha(payload[k]) != expected: raise ValueError(f"SHA256-INESPERADO:{k}")
    evidence=raw(inputs["za6980_q7_evidencia_precedente"]).decode()
    if not all(t in evidence for t in ("v21 = Q7a","v25 = Q7e","7 No one","operación no es ciega")): raise ValueError("EVIDENCIA-Q7-INCOMPLETA")
    with zipfile.ZipFile(io.BytesIO(payload["za6980_v2_0_0_dta"])) as z:
        if z.testzip() or [i.filename for i in z.infolist() if not i.is_dir()] != ["ZA6980_v2-0-0.dta","ZA6980_v2-0-0_missing.txt"]: raise ValueError("DTA-ZIP-INESPERADO")
        f=pd.read_stata(io.BytesIO(z.read("ZA6980_v2-0-0.dta")),columns=COLS,convert_categoricals=False)
    if list(f.columns)!=COLS: raise ValueError("COLUMNAS-NO-AUTORIZADAS")
    f=f.loc[f.c_alphan.astype(str).eq("MX")].copy()
    for c in ["studyno","country","SEX","WEIGHT",*[v for v,_,_ in VARS]]: f[c]=num(f[c])
    if len(f)!=1002 or not f.country.eq(484).all() or not f.studyno.eq(6980).all() or f.CASEID.isna().any() or f.CASEID.duplicated().any(): raise ValueError("IDENTIDAD-MEXICO-DISCREPA")
    if set(f.doi.astype(str))!={"doi:10.4232/1.13322"} or set(f.version.astype(str))!={"2.0.0 (2019-08-19)"}: raise ValueError("VERSION-DISCREPA")
    if not f.SEX.dropna().isin([1,2,9]).all() or any(not f[v].dropna().isin(range(1,10)).all() for v,_,_ in VARS): raise ValueError("CATALOGO-DISCREPA")
    return f

def matrix_rows(frame, a, b, universe):
    av,ai,as_=a; bv,bi,bs=b; va=valid(frame,av); vb=valid(frame,bv); mask=(va&vb) if universe=="PAREJA-DOS-VALIDAS" else va&vb&valid(frame,"v21")&valid(frame,"v22")&valid(frame,"v23")&valid(frame,"v24")&valid(frame,"v25")
    part=frame.loc[mask]; dn,dm=len(part),float(part.WEIGHT.sum()); rows=[]
    for ca,ta in CATS:
      for cb,tb in CATS:
        hit=part[av].eq(ca)&part[bv].eq(cb); nm=float(part.loc[hit,"WEIGHT"].sum()); rows.append({**base("OK" if dm else "DENOMINADOR-NULO"),"universo_matriz":universe,"variable_a":av,"item_a":ai,"situacion_a":as_,"codigo_a":ca,"categoria_a":ta,"variable_b":bv,"item_b":bi,"situacion_b":bs,"codigo_b":cb,"categoria_b":tb,"n_denominador":dn,"masa_denominador":dm,"n_numerador":int(hit.sum()),"masa_numerador":nm,"proporcion":ratio(nm,dm),"unidad":"proporcion-respuestas-validas"})
    return rows

def calculate(f):
    complete=wok(f)
    for v,_,_ in VARS: complete &= f[v].isin(range(1,8))
    comp=f.loc[complete].copy(); comp["familias"]=sum(comp[v].isin([1,2]).astype(int) for v,_,_ in VARS)
    count=[]; summary=[]
    for did,label,sex in [("TOTAL","México",None),("HOMBRES","Hombres",1),("MUJERES","Mujeres",2)]:
        p=comp if sex is None else comp.loc[comp.SEX.eq(sex)]; dm=float(p.WEIGHT.sum())
        for k in range(6):
            hit=p.familias.eq(k); nm=float(p.loc[hit,"WEIGHT"].sum()); count.append({**base("OK" if dm else "DENOMINADOR-NULO"),"dominio_id":did,"dominio":label,"situaciones_con_familia":k,"n_denominador":len(p),"masa_denominador":dm,"n_numerador":int(hit.sum()),"masa_numerador":nm,"proporcion":ratio(nm,dm),"unidad":"proporcion-cinco-validas"})
        for ident,desc,hit in [("FAMILIA_NINGUNA","Familia en ninguna situación",p.familias.eq(0)),("FAMILIA_ALGUNA","Familia en alguna situación",p.familias.ge(1)),("FAMILIA_TODAS","Familia en las cinco situaciones",p.familias.eq(5))]:
            nm=float(p.loc[hit,"WEIGHT"].sum()); summary.append({**base("OK" if dm else "DENOMINADOR-NULO"),"dominio_id":did,"indicador":ident,"descripcion":desc,"n_denominador":len(p),"masa_denominador":dm,"n_numerador":int(hit.sum()),"masa_numerador":nm,"proporcion":ratio(nm,dm),"unidad":"proporcion-cinco-validas"})
    eligible=f.loc[wok(f)]; summary.append({**base(),"dominio_id":"TOTAL","indicador":"COBERTURA_CINCO_VALIDAS","descripcion":"Cinco respuestas válidas entre peso utilizable","n_denominador":len(eligible),"masa_denominador":float(eligible.WEIGHT.sum()),"n_numerador":len(comp),"masa_numerador":float(comp.WEIGHT.sum()),"proporcion":ratio(float(comp.WEIGHT.sum()),float(eligible.WEIGHT.sum())),"unidad":"proporcion-peso-utilizable"})
    native=[]; sensitivity=[]; two=[]; assoc=[]
    for a,b in combinations(VARS,2):
      for universe,target in [("CINCO-RESPUESTAS-VALIDAS",native),("PAREJA-DOS-VALIDAS",sensitivity)]:
        rows=matrix_rows(f,a,b,universe); target.extend(rows); dm=rows[0]["masa_denominador"]
        cells={}
        for ra,rb in [((1,2),(1,2)),((1,2),(3,4,5,6,7)),((3,4,5,6,7),(1,2)),((3,4,5,6,7),(3,4,5,6,7))]:
            chosen=[r for r in rows if r["codigo_a"] in ra and r["codigo_b"] in rb]
            cells[(ra,rb)]={"estado": rows[0]["estado"], "n_denominador": rows[0]["n_denominador"], "n_numerador":sum(r["n_numerador"] for r in chosen), "masa_numerador":sum(r["masa_numerador"] for r in chosen)}
        labels=[("FAMILIA","FAMILIA",((1,2),(1,2))), ("FAMILIA","NO_FAMILIA",((1,2),(3,4,5,6,7))), ("NO_FAMILIA","FAMILIA",((3,4,5,6,7),(1,2))), ("NO_FAMILIA","NO_FAMILIA",((3,4,5,6,7),(3,4,5,6,7)))]
        for la,lb,key in labels:
            r=cells[key]; two.append({**base(r["estado"]),"universo_matriz":universe,"variable_a":a[0],"item_a":a[1],"variable_b":b[0],"item_b":b[1],"familia_a":la,"familia_b":lb,"n_denominador":r["n_denominador"],"masa_denominador":dm,"n_numerador":r["n_numerador"],"masa_numerador":r["masa_numerador"],"proporcion":ratio(r["masa_numerador"],dm),"unidad":"proporcion-matriz"})
        ff,fn,nf,nn=(cells[((1,2),(1,2))],cells[((1,2),(3,4,5,6,7))],cells[((3,4,5,6,7),(1,2))],cells[((3,4,5,6,7),(3,4,5,6,7))])
        for measure,value,den in [("ACUERDO",ff["masa_numerador"]+nn["masa_numerador"],dm),("DISCORDANCIA_A_FAMILIA_B_NO",fn["masa_numerador"],dm),("DISCORDANCIA_A_NO_B_FAMILIA",nf["masa_numerador"],dm),("P_FAMILIA_B_DADO_FAMILIA_A",ff["masa_numerador"],ff["masa_numerador"]+fn["masa_numerador"]),("P_FAMILIA_B_DADO_NO_FAMILIA_A",nf["masa_numerador"],nf["masa_numerador"]+nn["masa_numerador"]),("P_FAMILIA_A_DADO_FAMILIA_B",ff["masa_numerador"],ff["masa_numerador"]+nf["masa_numerador"]),("P_FAMILIA_A_DADO_NO_FAMILIA_B",fn["masa_numerador"],fn["masa_numerador"]+nn["masa_numerador"])]:
            assoc.append({**base("OK" if den else "CONDICIONAL-NO-ESTIMABLE"),"universo_matriz":universe,"variable_a":a[0],"item_a":a[1],"situacion_a":a[2],"variable_b":b[0],"item_b":b[1],"situacion_b":b[2],"medida":measure,"masa_denominador":den,"masa_numerador":value,"proporcion":ratio(value,den),"unidad":"proporcion"})
    controls={"particion_conteo":all(abs(sum(r["proporcion"] or 0 for r in count if r["dominio_id"]==d)-1)<1e-10 for d in ["TOTAL","HOMBRES","MUJERES"] if any(r["dominio_id"]==d and r["masa_denominador"]>0 for r in count)),"matrices_completas":len(native)==490 and len(sensitivity)==490,"reconstruccion_sexo_mas_residuo":len(comp)==int(comp.SEX.eq(1).sum())+int(comp.SEX.eq(2).sum())+int((~comp.SEX.isin([1,2])).sum()),"n_completos":len(comp),"masa_completos":float(comp.WEIGHT.sum()),"sexo_residuo_n":int((~comp.SEX.isin([1,2])).sum())}
    if not all(v for v in controls.values() if isinstance(v,bool)): raise ValueError("CONTROL-MATERIAL-FALLA")
    return count,summary,native,sensitivity,two,assoc,controls

def medir(inputs, contrato):
    f=source(inputs); count,summary,native,sens,two,assoc,controls=calculate(f)
    h={"conteo":write("conteo-familia.csv",count,BASE+["dominio_id","dominio","situaciones_con_familia","n_denominador","masa_denominador","n_numerador","masa_numerador","proporcion","unidad"]),"resumen":write("resumen-familia.csv",summary,BASE+["dominio_id","indicador","descripcion","n_denominador","masa_denominador","n_numerador","masa_numerador","proporcion","unidad"]),"matrices":write("matrices-nativas.csv",native,BASE+["universo_matriz","variable_a","item_a","situacion_a","codigo_a","categoria_a","variable_b","item_b","situacion_b","codigo_b","categoria_b","n_denominador","masa_denominador","n_numerador","masa_numerador","proporcion","unidad"]),"sensibilidad":write("matrices-nativas-sensibilidad-pareja.csv",sens,BASE+["universo_matriz","variable_a","item_a","situacion_a","codigo_a","categoria_a","variable_b","item_b","situacion_b","codigo_b","categoria_b","n_denominador","masa_denominador","n_numerador","masa_numerador","proporcion","unidad"]),"2x2":write("tablas-familia-2x2.csv",two,BASE+["universo_matriz","variable_a","item_a","variable_b","item_b","familia_a","familia_b","n_denominador","masa_denominador","n_numerador","masa_numerador","proporcion","unidad"]),"asociaciones":write("asociaciones-familia.csv",assoc,BASE+["universo_matriz","variable_a","item_a","situacion_a","variable_b","item_b","situacion_b","medida","masa_denominador","masa_numerador","proporcion","unidad"])}
    out=Path(__file__).resolve().parents[3]/ANALYSIS/"controles-medidor.json"; out.write_text(json.dumps({"calc_id":CALC_ID,**controls},ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    point=lambda x: next(r["proporcion"] for r in summary if r["dominio_id"]=="TOTAL" and r["indicador"]==x)
    return {"RESULT-ISSP-CONSISTENCIA-FAMILIA-N-MEXICO":len(f),"RESULT-ISSP-CONSISTENCIA-FAMILIA-PRECISION":PRECISION,"RESULT-ISSP-CONSISTENCIA-FAMILIA-COBERTURA-CINCO":point("COBERTURA_CINCO_VALIDAS"),"RESULT-ISSP-CONSISTENCIA-FAMILIA-NINGUNA":point("FAMILIA_NINGUNA"),"RESULT-ISSP-CONSISTENCIA-FAMILIA-ALGUNA":point("FAMILIA_ALGUNA"),"RESULT-ISSP-CONSISTENCIA-FAMILIA-TODAS":point("FAMILIA_TODAS"),"RESULT-ISSP-CONSISTENCIA-FAMILIA-CONTEO-SHA256":h["conteo"],"RESULT-ISSP-CONSISTENCIA-FAMILIA-MATRICES-SHA256":h["matrices"],"RESULT-ISSP-CONSISTENCIA-FAMILIA-SENSIBILIDAD-SHA256":h["sensibilidad"],"RESULT-ISSP-CONSISTENCIA-FAMILIA-2X2-SHA256":h["2x2"],"RESULT-ISSP-CONSISTENCIA-FAMILIA-ASOCIACIONES-SHA256":h["asociaciones"]}

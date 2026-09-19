#!/usr/bin/env python3
"""Recalcula una matriz, una condicional y conteos sin importar el medidor."""
from __future__ import annotations
import argparse,csv,io,json,math,zipfile
from pathlib import Path
import pandas as pd
V=["v21","v22","v23","v24","v25"]
def rows(p):
  with p.open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h))
def main():
 p=argparse.ArgumentParser(); p.add_argument("--dta-zip",type=Path,required=True); p.add_argument("--conteo",type=Path,required=True); p.add_argument("--matrices",type=Path,required=True); p.add_argument("--asociaciones",type=Path,required=True); p.add_argument("--output",type=Path); a=p.parse_args()
 with zipfile.ZipFile(a.dta_zip) as z: f=pd.read_stata(io.BytesIO(z.read("ZA6980_v2-0-0.dta")),columns=["country","c_alphan","WEIGHT",*V],convert_categoricals=False)
 f=f.loc[f.c_alphan.astype(str).eq("MX") & pd.to_numeric(f.country,errors="coerce").eq(484)].copy()
 for c in ["WEIGHT",*V]:f[c]=pd.to_numeric(f[c],errors="coerce")
 ok=f.WEIGHT.notna() & f.WEIGHT.map(math.isfinite) & f.WEIGHT.gt(0)
 complete=ok.copy()
 for v in V:complete &= f[v].isin(range(1,8))
 c=f.loc[complete].copy(); c["n"]=sum(c[v].isin([1,2]).astype(int) for v in V)
 count,mat,assoc=rows(a.conteo),rows(a.matrices),rows(a.asociaciones)
 if sum(int(x["n_numerador"]) for x in count if x["dominio_id"]=="TOTAL")!=len(c):raise SystemExit("CONTROL-FALLA-CONTEO")
 probe=next(x for x in mat if x["variable_a"]=="v21" and x["variable_b"]=="v22" and x["codigo_a"]=="1" and x["codigo_b"]=="1")
 if int(probe["n_numerador"])!=int((c.v21.eq(1)&c.v22.eq(1)).sum()):raise SystemExit("CONTROL-FALLA-MATRIZ")
 con=next(x for x in assoc if x["universo_matriz"]=="CINCO-RESPUESTAS-VALIDAS" and x["variable_a"]=="v21" and x["variable_b"]=="v22" and x["medida"]=="P_FAMILIA_B_DADO_FAMILIA_A")
 den=c.v21.isin([1,2]); expected=None if not den.any() else float(c.loc[den & c.v22.isin([1,2]),"WEIGHT"].sum()/c.loc[den,"WEIGHT"].sum())
 if expected is not None and not math.isclose(float(con["proporcion"]),expected,abs_tol=1e-10):raise SystemExit("CONTROL-FALLA-CONDICIONAL")
 out={"control_id":"CONTROL-INDEPENDIENTE-ISSP-CONSISTENCIA-FAMILIA-0001","estado":"CONTROL-INDEPENDIENTE-OK","no_importa_medidor":True,"n_mexico":len(f),"n_completos":len(c),"matriz_v21_v22_1_1":True,"condicional_v21_v22":True,"conteo":True}
 text=json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; (a.output.write_text(text,encoding="utf-8") if a.output else None); print(text,end="")
if __name__=="__main__":main()

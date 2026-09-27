#!/usr/bin/env python3
"""Ensamble documental por identidad; no abre raw ni adopta cifras."""
import csv,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent

def read(p):
    with p.open() as f:return list(csv.DictReader(f,delimiter="\t"))
p1=read(R/"p1/adjudicacion.tsv");p3=read(R/"p3/efectos-producto.tsv")
a={r["identidad_original"]:r for r in p1};b={r["identidad_original"]:r for r in p3}
assert len(a)==len(p1)==685 and len(b)==len(p3)==685 and a.keys()==b.keys()
patch={"externos":"p4/externos-reciente-2011.patch","edad2011":"p4/edad-permisos-2011.patch","reciente":"p4/externos-reciente-2011.patch","instituciones":"p4/institucion-afectadas-alternativa.patch","permisos":"p4/edad-permisos-2011.patch","denuncia":"p4/denuncia-enlace-2011.patch","edad2021":"p4/edad-permisos-2021.patch"}
rows=[]
for key,x in sorted(a.items()):
    y=b[key];amb=x["dictamen_documental"]!="DEFECTO-PRODUCTOR"
    rows.append({"identidad_original":key,"estado":"PROPUESTO-POR-EJECUTOR","decision_recomendada":"MANTENER-AMBIGUEDAD-CON-RESERVA" if amb else "PROPONER-RETIRO-TEMPORAL-Y-SUCESOR","motivo":x["dictamen_documental"]+"; "+x["evidencia_ref"],"efecto_documentado":y["conclusion"],"delta_nativo_historico":x["delta_nativo"],"delta_pp_historico":x["delta_pp"],"denominador_n_productor":y["denominador_n_productor"],"denominador_masa_productor":y["denominador_masa_productor"],"denominador_n_variante_P2":y["denominador_n_variante_P2"],"denominador_masa_variante_P2":y["denominador_masa_variante_P2"],"delta_n_P2":y["delta_denominador_n_P2"],"delta_masa_P2":y["delta_denominador_masa_P2"],"adopcion_vigente":y["adopcion"],"consumidor":y["consumidor_serie"],"especificacion":"p4/spec-sucesor-2011.patch" if "2011" in key else "p4/spec-sucesor-2021.patch","patch":patch.get(x["familia"],"Ver especificacion-sucesores.md y familia "+x["familia"]),"limite":"No se ejecuta retiro, correccion sellada o adopcion. Delta historico no equivale a contribucion de una regla; leer P2. IC/publicabilidad sesion02."})
with (R/"decisiones-por-objeto.tsv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(rows)
from collections import Counter
summary={"identidades":len(rows),"dictamen_documental":dict(Counter(x["dictamen_documental"] for x in p1)),"familias":dict(Counter(x["familia"] for x in p1)),"decisiones_propuestas":dict(Counter(x["decision_recomendada"] for x in rows)),"adopcion_vigente":dict(Counter(x["adopcion"] for x in p3)),"ranking_diagnostico_cambia":sum(x["rango_desc_productor"]!=x["rango_desc_reimplementacion"] for x in p3),"deltas_fuente":"Primer cotejo congelado #1184, no cifras corregidas","firmas":"NINGUNA NUEVA; propuesta pendiente","raw_en_repo":False}
(R/"c1-puntos-resumen.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(summary,ensure_ascii=False))

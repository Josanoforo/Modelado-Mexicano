#!/usr/bin/env python3
"""Gate local: cobertura, llaves, linaje, propuestas, hashes de inputs; sin raw."""
from pathlib import Path
import csv,json,hashlib,subprocess,tarfile
R=Path(__file__).resolve().parent
REPO=R.parents[2]
def rows(p):
    with p.open() as f:return list(csv.DictReader(f,delimiter="\t"))
source=rows(REPO/"forense/validacion-independiente/catalogo-1-ejecucion-lote1/efectos-discrepancias.tsv")
expected={r["llave"] for r in source if r["componente"]=="punto"}
assert len(expected)==685
for name,key in [("p1/adjudicacion.tsv","identidad_original"),("p2/cobertura-685.tsv","llave"),("p3/efectos-producto.tsv","identidad_original"),("decisiones-por-objeto.tsv","identidad_original")]:
    rs=rows(R/name);ks={r[key] for r in rs};assert len(rs)==len(ks)==685 and ks==expected,(name,len(rs),len(ks))
    assert all(all(k is not None for k in r) for r in rs),name
link=rows(R/"p3/linaje-consumidores.tsv");assert {x["identidad_original"] for x in link}==expected
s=json.loads((R/"p3/c1-puntos-p3-resumen.json").read_text())
for name,sha in s["fuentes_hash"].items():
    assert hashlib.sha256((REPO/name).read_bytes()).hexdigest()==sha,name
synthetic=json.loads((R/"p4/comprobacion-patches.json").read_text())
assert synthetic["total_pass"]==len(synthetic["casos"]) and all(x["estado"]=="PASS" for x in synthetic["casos"])
for p in R.rglob("*"):
    if p.is_file():assert p.suffix.lower() not in {".zip",".csv",".dbf",".pdf",".xls",".xlsx"},p
aux=json.loads((R/"c1-puntos-testimonios-auxiliares.json").read_text())
assert hashlib.sha256((R/"c1-puntos-testimonios-auxiliares.tar").read_bytes()).hexdigest()==aux["sha256_archive"]
with tarfile.open(R/"c1-puntos-testimonios-auxiliares.tar") as t:
    for x in aux["archivos"]:
        assert x["ruta_original"].endswith(".tsv")
        assert hashlib.sha256(t.extractfile(x["ruta_original"]).read()).hexdigest()==x["sha256"]
contrasts=rows(R/"p2/cotejo-final2011.tsv")
assert len(contrasts)==683 and all(x["baseline_p_coincide"]=="True" and x["baseline_n_coincide"]=="True" and abs(float(x["residual_independiente"]))<=1e-10 for x in contrasts)
product=rows(R/"p3/efectos-producto.tsv")
assert all(x["punto_P2_reimplementacion_coincide"]=="True" and x["denominador_n_variante_P2"] and x["denominador_masa_variante_P2"] for x in product)
changed=subprocess.check_output(["git","diff","--name-only","origin/main"],cwd=REPO,text=True).splitlines()
assert all(x.startswith(str(R.relative_to(REPO))+"/") or x=="forense/firmas-pendientes.tsv" for x in changed),changed
print(json.dumps({"estado":"PASS","identidades":len(expected),"aristas":len(link),"llaves_completas":True,"hashes_fuentes":len(s["fuentes_hash"]),"sin_raw_en_raiz":True,"perimetro_diff":True},ensure_ascii=False))

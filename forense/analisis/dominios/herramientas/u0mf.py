#!/usr/bin/env python3
"""u0mf: consulta data/manifiesto.yaml por id exacto (--id) o por substring plegado
(--busca, repetible, AND) sobre id/archivo/url_origen/usado_para/formato/nota.
Declara siempre cuántas entradas examinó (A.13). Muestra estado_reserva.
Además: --calc <id> lista corridas de data/corrida0/corridas.tsv cuyo input_ids contiene ese id."""
import argparse, unicodedata, yaml, sys
REPO = str(__import__("pathlib").Path(__file__).resolve().parents[4])
def pl(s):
    s = unicodedata.normalize("NFD", str(s or "")); return "".join(c for c in s.lower() if unicodedata.category(c) != "Mn")
ap = argparse.ArgumentParser()
ap.add_argument("--id", action="append"); ap.add_argument("--busca", action="append")
ap.add_argument("--calc", action="append"); ap.add_argument("--limite", type=int, default=60)
a = ap.parse_args()
M = yaml.safe_load(open(REPO + "/data/manifiesto.yaml", encoding="utf-8"))
print(f"# u0mf A.13: {len(M)} entradas examinadas en data/manifiesto.yaml")
def show(e, full=False):
    f = [e.get("id"), e.get("archivo",""), e.get("raiz","data_raw"), (e.get("sha256") or "")[:64], str(e.get("tamano_bytes","")),
         e.get("estado_reserva",""), (str(e.get("formato") or ""))[:160].replace("\n"," "), (str(e.get("url_origen") or ""))[:160]]
    print("\t".join(str(x) for x in f))
    if full:
        for k in ("usado_para","nota","licencia","fecha_descarga"):
            if e.get(k): print(f"   {k}: {str(e.get(k))[:600]}")
if a.id:
    idx = {e["id"]: e for e in M}
    for i in a.id:
        e = idx.get(i)
        if e: show(e, True)
        else: print(f"{i}\tNO-ENCONTRADO-POR-ID (0 de {len(M)})")
if a.busca:
    ts = [pl(t) for t in a.busca]; n = 0
    for e in M:
        blob = pl(" ".join(str(e.get(k,"")) for k in ("id","archivo","url_origen","usado_para","formato","nota")))
        if all(t in blob for t in ts):
            n += 1
            if n <= a.limite: show(e)
    print(f"# busca {a.busca}: {n} entradas coinciden (mostradas {min(n,a.limite)})")
if a.calc:
    L = [l for l in open(REPO + "/data/corrida0/corridas.tsv", encoding="utf-8").read().split("\n") if l and not l.startswith("#")]
    cab = L[0].split("\t"); ix = {c:i for i,c in enumerate(cab)}
    for i in a.calc:
        hits = [r.split("\t") for r in L[1:] if i in r.split("\t")[ix["input_ids"]].split(",") or i in r.split("\t")[ix["input_ids"]]]
        print(f"# corridas con input {i}: {len(hits)} (de {len(L)-1} corridas)")
        for r in hits[:40]:
            print("\t".join([r[ix["corrida_id"]], r[ix["spec_id"]], r[ix["estado"]], r[ix["cuenta_gen2"]], r[ix["fecha"]], r[ix["n_resultados"]], r[ix["resultado_replay"]]]))

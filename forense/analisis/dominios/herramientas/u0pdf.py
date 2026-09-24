#!/usr/bin/env python3
"""u0pdf: busca texto en los PDF REGISTRADOS en data/manifiesto.yaml (texto extraído con
pdftotext -layout a una caché; los PDF de olas reservadas ENOE 2026 / ENVIPE 2026 / ENCO
NO se extrajeron). Devuelve id de manifiesto, sha256, página y línea.
Uso: u0pdf.py -q "pensado en suicid" [-q ...] [--id <manifest_id> ...] [--idsub ensanut] [--contexto 1] [--limite 30]
Plegado: minúsculas sin acentos; espacios múltiples colapsados. '|' = OR dentro de -q."""
import argparse, glob, os, re, unicodedata, yaml
S = __import__("os").environ.get("U0_CACHE", __import__("os").path.join(__import__("os").environ.get("TMPDIR", "/tmp"), "u0-cache"))
REPO = str(__import__("pathlib").Path(__file__).resolve().parents[4])
def pl(s):
    s = unicodedata.normalize("NFD", s or ""); s = "".join(c for c in s.lower() if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s)
ap = argparse.ArgumentParser()
ap.add_argument("-q", action="append", required=True); ap.add_argument("--id", action="append")
ap.add_argument("--idsub"); ap.add_argument("--contexto", type=int, default=1); ap.add_argument("--limite", type=int, default=30)
a = ap.parse_args()
M = {e["id"]: e for e in yaml.safe_load(open(REPO + "/data/manifiesto.yaml", encoding="utf-8"))}
files = sorted(glob.glob(S + "/pdftxt/*.txt"))
if a.id: files = [f for f in files if os.path.basename(f)[:-4] in set(a.id)]
if a.idsub: files = [f for f in files if pl(a.idsub) in pl(os.path.basename(f))]
print(f"# u0pdf A.13: {len(files)} PDF registrados examinados (caché pdftotext de {len(glob.glob(S + '/pdftxt/*.txt'))})")
for q in a.q:
    terms = [pl(t) for t in q.split("|") if t.strip()]
    n = 0; out = []
    for f in files:
        mid = os.path.basename(f)[:-4]
        pages = open(f, encoding="utf-8", errors="replace").read().split("\f")
        for pi, pg in enumerate(pages, start=1):
            flat = pl(pg)
            for t in terms:
                for m in re.finditer(re.escape(t), flat):
                    n += 1
                    if len(out) < a.limite:
                        e = M.get(mid, {})
                        snip = flat[max(0, m.start() - 160): m.end() + 160]
                        out.append(f"{mid}\t{(e.get('sha256') or '')}\t{e.get('raiz','data_raw')}\tp.{pi}\t…{snip}…")
    print(f"# consulta {q!r}: {n} coincidencias (texto de página aplanado); mostrando {len(out)}")
    print("manifest_id\tsha256\traiz\tpagina\tcontexto")
    for o in out: print(o)

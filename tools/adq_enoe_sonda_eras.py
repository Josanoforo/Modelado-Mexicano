#!/usr/bin/env python3
"""ADQ-ENOE-PRE2019 · T2, segunda extension declarada sobre COMMIT A.

Sonda de ERA. El diferencial de variables sobre la ventana adquirida
(2016T1-2018T4) dio SOLO_PRE=0: ni una variable existe antes de 2019 y falta
despues. Pero esa ventana usa los MISMOS instrumentos que el barrido moderno
ya habia leido (`c_bas_v5`, `c_amp_v5`, `c_sdem_v4` gobiernan 2016-2019).

La hipotesis del encargo -- "puede que las olas viejas si traigan lo que las
nuevas no" -- solo puede ser cierta en las eras de instrumento ANTERIORES, las
que `fd_c_amp_v1`/`fd_c_bas_v1` describen y que `CAL-ENOE Fase A` nunca abrio.
Esta sonda baja una ola por era para correr el mismo diferencial exhaustivo
sobre ellas, en vez de dejar el negativo apoyado solo en PDF.
"""
import hashlib, os, subprocess, sys

CORPUS = "/home/pc0/mm-corpus/raw"
URL = "https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/{y}trim{t}_csv.zip"
OLAS = [(2005, 1), (2008, 1), (2012, 1), (2014, 1)]

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def main():
    tmp = os.path.join(CORPUS, ".adq_enoe_parcial"); os.makedirs(tmp, exist_ok=True)
    rows = []
    for y, t in OLAS:
        nombre = f"{y}trim{t}_csv.zip"; url = URL.format(y=y, t=t)
        dest = os.path.join(CORPUS, nombre)
        if os.path.exists(dest):
            rows.append((nombre, f"{y}T{t}", "YA_EXISTIA", os.path.getsize(dest), sha256(dest), url))
            print(f"[ya] {nombre}", flush=True); continue
        scratch = os.path.join(tmp, nombre)
        r = subprocess.run(["curl", "-sS", "-L", "--fail", "--max-time", "900",
                            "-o", scratch, url], capture_output=True, text=True)
        if r.returncode != 0:
            rows.append((nombre, f"{y}T{t}", f"FALLO_CURL_{r.returncode}", 0, "", url))
            print(f"[XX] {nombre}: curl {r.returncode}", flush=True); continue
        with open(scratch, "rb") as f:
            magic = f.read(2)
        size = os.path.getsize(scratch)
        if magic != b"PK":
            rows.append((nombre, f"{y}T{t}", f"SOFT404_magic={magic!r}", size, "", url))
            print(f"[XX] {nombre}: NO es zip ({size} B)", flush=True)
            os.remove(scratch); continue
        h = sha256(scratch); os.replace(scratch, dest)
        rows.append((nombre, f"{y}T{t}", "DESCARGADO", size, h, url))
        print(f"[ok] {nombre}  {size:,} B  {h[:16]}…", flush=True)
    out = "data/adq-enoe-pre2019-sonda-eras-evidencia.tsv"
    with open(out, "w", encoding="utf-8") as f:
        f.write("archivo\tola\testado\tbytes\tsha256\turl_origen\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    print(f"\n{sum(1 for r in rows if r[2] in ('DESCARGADO','YA_EXISTIA'))}/{len(rows)} en corpus · {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

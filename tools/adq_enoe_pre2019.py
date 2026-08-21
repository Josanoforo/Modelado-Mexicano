#!/usr/bin/env python3
"""ADQ-ENOE-PRE2019 · T1. Baja las 13 olas que COMMIT A (bbis-adq-enoe-pre2019
§2) pre-registro, DIRECTO al corpus compartido, y emite un TSV de evidencia.

No renombra: conserva el nombre que sirve INEGI, para que `archivo` y
`url_origen` del manifiesto sean trazables el uno del otro.

Detecta el soft-404 de INEGI (200 + text/html) que §3 de COMMIT A midio:
un .zip que no empieza con PK se rechaza y NO entra al corpus.
"""
import hashlib, os, subprocess, sys, time

CORPUS = "/home/pc0/mm-corpus/raw"
MICRO  = "https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/{y}trim{t}_csv.zip"
ABIER  = "https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/datosabiertos/{y}/conjunto_de_datos_enoe_{y}_{t}t_csv.zip"

def plan():
    for y in (2016, 2017, 2018):
        for t in (1, 2, 3, 4):
            yield MICRO.format(y=y, t=t), f"{y}trim{t}_csv.zip", "microdatos", y, t
    yield ABIER.format(y=2018, t=4), "conjunto_de_datos_enoe_2018_4t_csv.zip", "datosabiertos", 2018, 4

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def main():
    os.makedirs(CORPUS, exist_ok=True)
    # El scratch vive DENTRO del corpus: os.replace no cruza sistemas de
    # archivos, y $TMPDIR y el corpus estan en dispositivos distintos.
    tmp = os.path.join(CORPUS, ".adq_enoe_parcial")
    os.makedirs(tmp, exist_ok=True)
    rows = []
    for url, nombre, ruta, y, t in plan():
        dest = os.path.join(CORPUS, nombre)
        if os.path.exists(dest):                       # A.8, segunda linea de defensa
            rows.append((nombre, ruta, f"{y}T{t}", "YA_EXISTIA", os.path.getsize(dest),
                         sha256(dest), url))
            print(f"[ya] {nombre}", flush=True)
            continue
        scratch = os.path.join(tmp, nombre)
        t0 = time.time()
        r = subprocess.run(["curl", "-sS", "-L", "--fail", "--max-time", "900",
                            "-o", scratch, url], capture_output=True, text=True)
        if r.returncode != 0:
            rows.append((nombre, ruta, f"{y}T{t}", f"FALLO_CURL_{r.returncode}", 0, "", url))
            print(f"[XX] {nombre}: curl {r.returncode} {r.stderr.strip()[:120]}", flush=True)
            continue
        with open(scratch, "rb") as f:
            magic = f.read(2)
        size = os.path.getsize(scratch)
        if magic != b"PK":                              # soft-404 de INEGI
            rows.append((nombre, ruta, f"{y}T{t}", f"SOFT404_magic={magic!r}", size, "", url))
            print(f"[XX] {nombre}: NO es zip ({size} B, magic {magic!r})", flush=True)
            os.remove(scratch)
            continue
        h = sha256(scratch)
        os.replace(scratch, dest)
        rows.append((nombre, ruta, f"{y}T{t}", "DESCARGADO", size, h, url))
        print(f"[ok] {nombre}  {size:,} B  {h[:16]}…  {time.time()-t0:.0f}s", flush=True)

    out = "data/adq-enoe-pre2019-evidencia.tsv"
    with open(out, "w", encoding="utf-8") as f:
        f.write("archivo\truta_inegi\tola\testado\tbytes\tsha256\turl_origen\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    ok = sum(1 for r in rows if r[3] in ("DESCARGADO", "YA_EXISTIA"))
    print(f"\n{ok}/{len(rows)} en corpus  ·  evidencia -> {out}")
    return 0 if ok == len(rows) else 1

if __name__ == "__main__":
    sys.exit(main())

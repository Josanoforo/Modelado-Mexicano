#!/usr/bin/env python3
"""ADQ-ENOE-PRE2019 · T2, extension declarada sobre COMMIT A.

COMMIT A (`bbis-adq-enoe-pre2019` §2) pre-registro 13 payloads de microdato.
Esta extension baja ademas los DESCRIPTORES DE INSTRUMENTO de las dos eras de
la ENOE, `14ymas` y `15ymas`, que `data/indice-descarga-masiva-2026-08-05.tsv`
lista y que `CAL-ENOE Fase A` (31/jul/2026) NO leyo: su universo fueron nueve
cuestionarios que cubren 2016T1-2026T1, todos de la era `15ymas`.

Razon de la extension, escrita aqui y no en COMMIT A porque se descubrio
despues de congelarlo: los tres cuestionarios que gobiernan 2016-2018
(`c_bas_v5`, `c_amp_v5`, `c_sdem_v4`) YA estaban en ese universo, asi que el
barrido de las olas de §2 no puede, por si solo, contestar si "las olas viejas
traen lo que las nuevas no" -- para eso hace falta la era que nadie leyo.
"""
import hashlib, os, subprocess, sys

CORPUS = "/home/pc0/mm-corpus/raw"
BASE14 = "https://www.inegi.org.mx/contenidos/programas/enoe/14ymas/doc/"
BASE15 = "https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/"

DOCS = [(BASE14 + n, n, "14ymas") for n in (
            "fd_c_amp_v1.pdf", "fd_c_amp_v2.pdf", "fd_c_amp_v3.pdf",
            "fd_c_amp_v4.pdf", "fd_c_bas_v1.pdf", "fd_c_bas_v2.pdf",
            "fd_c_bas_amp_conapo.pdf")] + \
       [(BASE15 + n, n, "15ymas") for n in (
            "fd_c_bas_amp_15ymas.pdf", "enoe_123_fd_c_bas_amp.pdf",
            "enoe_325_fd_c_bas_amp.pdf")]

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def main():
    tmp = os.path.join(CORPUS, ".adq_enoe_parcial")
    os.makedirs(tmp, exist_ok=True)
    rows = []
    for url, nombre, era in DOCS:
        dest = os.path.join(CORPUS, nombre)
        if os.path.exists(dest):
            rows.append((nombre, era, "YA_EXISTIA", os.path.getsize(dest), sha256(dest), url))
            print(f"[ya] {nombre}", flush=True); continue
        scratch = os.path.join(tmp, nombre)
        r = subprocess.run(["curl", "-sS", "-L", "--fail", "--max-time", "300",
                            "-o", scratch, url], capture_output=True, text=True)
        if r.returncode != 0:
            rows.append((nombre, era, f"FALLO_CURL_{r.returncode}", 0, "", url))
            print(f"[XX] {nombre}: curl {r.returncode}", flush=True); continue
        with open(scratch, "rb") as f:
            magic = f.read(5)
        size = os.path.getsize(scratch)
        if magic != b"%PDF-":                       # soft-404 de INEGI
            rows.append((nombre, era, f"SOFT404_magic={magic!r}", size, "", url))
            print(f"[XX] {nombre}: NO es pdf ({size} B, {magic!r})", flush=True)
            os.remove(scratch); continue
        h = sha256(scratch)
        os.replace(scratch, dest)
        rows.append((nombre, era, "DESCARGADO", size, h, url))
        print(f"[ok] {nombre}  {size:,} B  {h[:16]}…", flush=True)

    out = "data/adq-enoe-pre2019-docs-evidencia.tsv"
    with open(out, "w", encoding="utf-8") as f:
        f.write("archivo\tera\testado\tbytes\tsha256\turl_origen\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    ok = sum(1 for r in rows if r[2] in ("DESCARGADO", "YA_EXISTIA"))
    print(f"\n{ok}/{len(rows)} en corpus  ·  evidencia -> {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

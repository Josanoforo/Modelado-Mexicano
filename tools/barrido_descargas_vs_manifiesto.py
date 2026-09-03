#!/usr/bin/env python3
"""Barrido A.8 de solo lectura: ¿qué hay en las carpetas de descargas que el
manifiesto NO conoce? Cruza por sha256 (dedup real), no por nombre.

Uso (desde el clon, WSL):
  python3 tools/barrido_descargas_vs_manifiesto.py \
      "/mnt/c/Users/PC0/Descargas MX" "/mnt/c/Users/PC0/Descargas MX/Descargas Manuales"

Si la segunda es subcarpeta de la primera, pásala igual: el reporte lo dice.
No escribe en el manifiesto ni en ninguna otra parte.
"""
import hashlib, os, re, sys

MANIFIESTO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "manifiesto.yaml")
if not os.path.exists(MANIFIESTO):
    MANIFIESTO = "data/manifiesto.yaml"

def leer_manifiesto(ruta):
    txt = open(ruta, encoding="utf-8").read()
    por_sha, por_nombre = {}, {}
    for ent in re.split(r"\n- id: ", txt)[1:]:
        mid = ent.split("\n", 1)[0].strip()
        sha = re.search(r"^\s+sha256:\s*['\"]?([0-9a-f]{64})", ent, re.M)
        arc = re.search(r"^\s+archivo:\s*(.+)$", ent, re.M)
        raiz = re.search(r"^\s+raiz:\s*(\S+)", ent, re.M)
        if sha:
            por_sha[sha.group(1)] = mid
        if arc:
            base = os.path.basename(arc.group(1).strip().strip("'\""))
            por_nombre.setdefault(base, []).append((mid, raiz.group(1) if raiz else "data_raw"))
    return por_sha, por_nombre

def sha256_de(p, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(bufsize), b""):
            h.update(chunk)
    return h.hexdigest()

def main(rutas):
    por_sha, por_nombre = leer_manifiesto(MANIFIESTO)
    print(f"manifiesto: {MANIFIESTO} · entradas con sha256: {len(por_sha)}")
    vistos = set()
    for raiz in rutas:
        raiz = os.path.abspath(raiz)
        print(f"\n=== {raiz}")
        if not os.path.isdir(raiz):
            print("   NO-ACCESIBLE: no es carpeta en esta máquina"); continue
        reg, nuevo, conflicto, n, ya = [], [], [], 0, 0
        for dp, _, fs in os.walk(raiz):
            for f in fs:
                p = os.path.join(dp, f)
                if p in vistos:
                    ya += 1; continue
                vistos.add(p); n += 1
                rel = os.path.relpath(p, raiz)
                try:
                    s = sha256_de(p)
                except OSError as e:
                    print(f"   ERROR-LECTURA {rel}: {e}"); continue
                if s in por_sha:
                    reg.append((rel, por_sha[s]))
                elif f in por_nombre:
                    conflicto.append((rel, por_nombre[f]))
                else:
                    nuevo.append((rel, os.path.getsize(p)))
        print(f"   archivos examinados: {n} · REGISTRADO(sha coincide): {len(reg)} · "
              f"NO-REGISTRADO: {len(nuevo)} · MISMO-NOMBRE-OTRO-SHA: {len(conflicto)}"
              + (f" · ya cubiertos por una raíz anterior (subcarpeta): {ya}" if ya else ""))
        for rel, sz in sorted(nuevo):
            print(f"   NO-REGISTRADO  {sz:>12,d}  {rel}")
        for rel, ids in sorted(conflicto):
            print(f"   MISMO-NOMBRE-OTRO-SHA  {rel}  ↔ {ids}")
    print("\nA.13: los conteos de arriba son por comando os.walk; un 0 en NO-REGISTRADO "
          "con 'archivos examinados' > 0 sí es un negativo.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1:])

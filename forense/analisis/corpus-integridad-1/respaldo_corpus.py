#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Juego de respaldo del corpus (P3 de ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1,
21/sep/2026). Cuatro pasos, cada uno un subcomando; todos sólo LEEN las
raíces del corpus (nunca borran, mueven ni renombran nada: PARO b).

  --indexa      camina las raíces FÍSICAS del corpus (no el manifiesto) y
                escribe <destino>/indice.tsv (raiz · ruta_rel · tamano_bytes ·
                sha256) más <destino>/SHA256SUMS (formato `sha256sum -c`).
                Symlinks se omiten (mm-corpus/raw/raw -> mm-corpus/raw es un
                bucle; medido 21/sep/2026).
  --copia       rsync -rt --safe-links de cada raíz a <destino>/<raiz>/.
  --verifica    rehashea TODO lo copiado en destino contra indice.tsv.
  --restaura N  prueba de restauración: copia una muestra (un archivo por
                primer subdirectorio de cada raíz, o N al azar con semilla)
                desde el destino a un directorio temporal y verifica su sha.

Raíces (nombre lógico -> ruta física) se pasan con --raiz NOMBRE=RUTA; por
defecto se toman las tres que este acto censó:
  data_raw=/home/pc0/mm-corpus/raw
  descargas_mx=/mnt/c/Users/PC0/Descargas MX
  reserva_respondentes=/home/pc0/mm-corpus/reservas-respondentes
Debe correr FUERA del sandbox (descargas_mx vive en /mnt/c).

Los payloads reservados se copian y se hashean; no se abren ni se listan
(el índice registra ruta, tamaño y sha256, igual que el manifiesto).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

RAICES_DEFECTO = {
    "data_raw": "/home/pc0/mm-corpus/raw",
    "descargas_mx": "/mnt/c/Users/PC0/Descargas MX",
    "reserva_respondentes": "/home/pc0/mm-corpus/reservas-respondentes",
}
# Lock de escritura de tests/manifiesto.py (ADR-399 D6): no es dato.
EXCLUIR_BASENAMES = {".manifiesto.lock"}
COLS = ["raiz", "ruta_rel", "tamano_bytes", "sha256"]


def sha256_de(path, buf=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(buf), b""):
            h.update(b)
    return h.hexdigest()


def caminar(base):
    """Archivos regulares bajo `base`, sin seguir symlinks internos, rutas
    relativas ordenadas."""
    out = []
    for dirpath, dirs, files in os.walk(base, followlinks=False):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            if os.path.islink(p) or f in EXCLUIR_BASENAMES:
                continue
            out.append(os.path.relpath(p, base))
    return out


def leer_indice(destino):
    filas = []
    with open(os.path.join(destino, "indice.tsv"), encoding="utf-8") as f:
        next(f)
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln:
                continue
            r, rel, tam, sha = ln.split("\t")
            filas.append((r, rel, int(tam), sha))
    return filas


def cmd_indexa(a, raices):
    os.makedirs(a.destino, exist_ok=True)
    t0 = time.time()
    filas = []
    for nombre, base in raices.items():
        rels = caminar(base)
        print(f"[{nombre}] {len(rels)} archivos bajo {base}", file=sys.stderr)
        for i, rel in enumerate(rels, 1):
            p = os.path.join(base, rel)
            filas.append((nombre, rel, os.path.getsize(p), sha256_de(p)))
            if i % 200 == 0:
                print(f"   {i}/{len(rels)} ({time.time()-t0:.0f}s)", file=sys.stderr)
    with open(os.path.join(a.destino, "indice.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(COLS) + "\n")
        for r in filas:
            f.write("\t".join(str(x) for x in r) + "\n")
    with open(os.path.join(a.destino, "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as f:
        for nombre, rel, _t, sha in filas:
            f.write(f"{sha}  {nombre}/{rel}\n")
    tot = sum(r[2] for r in filas)
    por = {}
    for nombre, _r, t, _s in filas:
        c = por.setdefault(nombre, [0, 0])
        c[0] += 1
        c[1] += t
    print(f"INDICE: archivos={len(filas)} bytes={tot} ({time.time()-t0:.0f}s) -> {a.destino}/indice.tsv")
    for n, (c, b) in sorted(por.items()):
        print(f"  {n}: archivos={c} bytes={b}")


def cmd_copia(a, raices):
    os.makedirs(a.destino, exist_ok=True)
    for nombre, base in raices.items():
        dst = os.path.join(a.destino, nombre) + "/"
        cmd = ["rsync", "-rt", "--safe-links", "--no-links", "--exclude", ".manifiesto.lock",
               "--stats", base.rstrip("/") + "/", dst]
        print("$ " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr)
            sys.exit(f"rsync falló en {nombre} (rc={r.returncode})")
        resumen = [ln for ln in r.stdout.splitlines()
                   if ln.startswith(("Number of files", "Number of regular files transferred",
                                     "Total file size", "Total transferred file size"))]
        print("\n".join("  " + ln for ln in resumen))


def cmd_verifica(a, raices):
    filas = leer_indice(a.destino)
    t0 = time.time()
    ok = bad = falta = 0
    for i, (nombre, rel, tam, sha) in enumerate(filas, 1):
        p = os.path.join(a.destino, nombre, rel)
        if not os.path.exists(p):
            falta += 1
            print(f"FALTA {nombre}/{rel}")
            continue
        if os.path.getsize(p) != tam or sha256_de(p) != sha:
            bad += 1
            print(f"NO-COINCIDE {nombre}/{rel}")
        else:
            ok += 1
        if i % 200 == 0:
            print(f"   {i}/{len(filas)} ({time.time()-t0:.0f}s)", file=sys.stderr)
    print(f"VERIFICA-DESTINO: examinados={len(filas)} coincide={ok} no_coincide={bad} "
          f"falta={falta} ({time.time()-t0:.0f}s) -> "
          + ("VERDE" if bad == 0 and falta == 0 else "ROJO"))
    sys.exit(0 if bad == 0 and falta == 0 else 1)


def cmd_restaura(a, raices):
    filas = leer_indice(a.destino)
    # muestra: un archivo por primer subdirectorio de cada raíz (los archivos
    # sueltos en la raíz cuentan como subdirectorio "."), más N al azar.
    por_dir = {}
    for f in filas:
        clave = (f[0], f[1].split("/", 1)[0] if "/" in f[1] else ".")
        por_dir.setdefault(clave, f)
    muestra = list(por_dir.values())
    rnd = random.Random(a.semilla)
    extra = rnd.sample(filas, min(a.restaura, len(filas)))
    vistos = {(m[0], m[1]) for m in muestra}
    muestra += [e for e in extra if (e[0], e[1]) not in vistos]
    # El temporal va a --tmp (por defecto junto al destino): $TMPDIR del
    # sandbox es un tmpfs pequeño y una muestra de GB lo llena (medido
    # 21/sep/2026: ENOSPC en el primer intento).
    os.makedirs(a.tmp, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="restaura-corpus-", dir=a.tmp)
    ok = bad = 0
    bytes_ = 0
    print(f"RESTAURA: {len(muestra)} archivos ({len(por_dir)} subdirectorios + {a.restaura} al azar, "
          f"semilla={a.semilla}) -> {tmp}")
    for nombre, rel, tam, sha in muestra:
        src = os.path.join(a.destino, nombre, rel)
        dst = os.path.join(tmp, nombre, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        real = sha256_de(dst)
        bytes_ += tam
        estado = "COINCIDE" if real == sha and os.path.getsize(dst) == tam else "NO-COINCIDE"
        ok += estado == "COINCIDE"
        bad += estado != "COINCIDE"
        print(f"  {estado} {nombre}/{rel} {tam} {sha[:12]}")
    print(f"RESTAURA-RESUMEN: restaurados={len(muestra)} bytes={bytes_} coincide={ok} "
          f"no_coincide={bad} dir={tmp} -> " + ("VERDE" if bad == 0 else "ROJO"))
    if not a.conserva:
        shutil.rmtree(tmp)
        print(f"  (directorio temporal borrado; --conserva lo deja)")
    sys.exit(0 if bad == 0 else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--destino", required=True, help="directorio del juego de respaldo")
    ap.add_argument("--raiz", action="append", default=[], metavar="NOMBRE=RUTA")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--indexa", action="store_true")
    g.add_argument("--copia", action="store_true")
    g.add_argument("--verifica", action="store_true")
    g.add_argument("--restaura", type=int, metavar="N", help="N archivos extra al azar")
    ap.add_argument("--semilla", type=int, default=20260921)
    ap.add_argument("--conserva", action="store_true", help="no borrar el temporal de --restaura")
    ap.add_argument("--tmp", default=None, help="dónde crear el temporal de --restaura "
                    "(defecto: <destino>/../restauraciones-tmp)")
    a = ap.parse_args()
    if a.tmp is None:
        a.tmp = os.path.join(os.path.dirname(os.path.abspath(a.destino)), "restauraciones-tmp")
    raices = dict(RAICES_DEFECTO)
    for par in a.raiz:
        k, v = par.split("=", 1)
        raices[k] = v
    for k, v in raices.items():
        if not os.path.isdir(v) and not (a.verifica or a.restaura is not None):
            sys.exit(f"raíz {k} no accesible: {v} (¿sandbox? corre fuera de él)")
    if a.indexa:
        cmd_indexa(a, raices)
    elif a.copia:
        cmd_copia(a, raices)
    elif a.verifica:
        cmd_verifica(a, raices)
    else:
        cmd_restaura(a, raices)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Censo de integridad del corpus, entrada por entrada (P1 de
ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1, 21/sep/2026).

Reusa `tests/payload_resolver.resolver_payload` (no reimplementa la
resolución raíz->archivo->hash). Por cada entrada de data/manifiesto.yaml
escribe una fila TSV con:

  id · raiz_declarada (SIN-RAIZ si el campo no está; se resuelve a data_raw
  por la cabecera del manifiesto) · raiz_resuelta · archivo · estado_A1
  (COINCIDE / NO_COINCIDE / AUSENTE / RAIZ_NO_CONFIGURADA /
  FUERA_DE_PERIMETRO / NO-ES-ARCHIVO) · clase_P1 (ESTÁ-Y-COINCIDE /
  ESTÁ-Y-NO-COINCIDE / NO-ESTÁ / NO-ES-ARCHIVO / NO-VERIFICABLE) ·
  tamano_declarado · tamano_real · hallado_en_otra_raiz (para NO-ESTÁ: en
  qué raíz configurada existe un archivo con el mismo basename, y si su
  sha256 coincide) · tiene_url_origen · estado_reserva · licencia.

Nunca escribe en el manifiesto ni en ninguna raíz. Sólo lee. Los payloads
con estado_reserva se hashean (permitido) y no se abren ni se listan.

Uso:  python3 forense/analisis/corpus-integridad-1/censo_integridad.py \
          --salida forense/analisis/corpus-integridad-1/censo-2026-09-21.tsv
Debe correr FUERA del sandbox: descargas_mx vive en /mnt/c.
"""
from __future__ import annotations

import argparse
import os
import sys
import time

RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ_REPO, "tests"))
import manifiesto as M  # noqa: E402
import payload_resolver as PR  # noqa: E402

COLS = ["id", "raiz_declarada", "raiz_resuelta", "archivo", "estado_A1", "clase_P1",
        "tamano_declarado", "tamano_real", "hallado_en_otra_raiz",
        "tiene_url_origen", "estado_reserva", "licencia"]


def indice_basenames(raices):
    """{raiz: {basename: [ruta_abs, ...]}} sobre las raíces escaneables
    configuradas más las de --busca-tambien. Un solo os.walk por raíz,
    SIN seguir symlinks internos: `mm-corpus/raw/raw -> mm-corpus/raw` es
    un bucle (medido 21/sep/2026: con followlinks=True el índice infló a
    51 641 "archivos"; sin seguirlos, 1 291). El symlink de entrada
    (data/raw) sí se resuelve porque os.walk abre el top con scandir."""
    idx = {}
    for nombre, base in raices.items():
        d = idx.setdefault(nombre, {})
        for dirpath, _dirs, files in os.walk(base, followlinks=False):
            for f in files:
                d.setdefault(f, []).append(os.path.join(dirpath, f))
    return idx


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--sin-hash-ajeno", action="store_true",
                    help="no hashea los candidatos hallados en otra raíz (más rápido)")
    ap.add_argument("--busca-tambien", action="append", default=[], metavar="NOMBRE=RUTA",
                    help="raíz extra donde buscar por basename lo NO-ESTÁ / NO-VERIFICABLE "
                         "(p. ej. reserva_respondentes=/ruta, repo=/ruta). Sólo lectura.")
    a = ap.parse_args()

    manifiesto_path, raw_dir = M.rutas(RAIZ_REPO)
    _cab, entradas = M.leer_manifiesto(manifiesto_path)

    raices = {M.RAIZ_INTEGRADA: raw_dir}
    for k, v in M.raices_configuradas(RAIZ_REPO).items():
        if M.raiz_escaneable(k) and v and os.path.isdir(v):
            raices[k] = v
    print(f"raíces escaneables configuradas y accesibles: {sorted(raices)}", file=sys.stderr)
    extra = {}
    for par in a.busca_tambien:
        nombre, ruta = par.split("=", 1)
        if os.path.isdir(ruta):
            extra[nombre] = ruta
    print(f"raíces extra de búsqueda (--busca-tambien): {sorted(extra)}", file=sys.stderr)
    raices_busqueda = {**raices, **extra}
    t0 = time.time()
    idx = indice_basenames(raices_busqueda)
    n_idx = {k: sum(len(v) for v in d.values()) for k, d in idx.items()}
    print(f"archivos indexados por raíz: {n_idx} ({time.time()-t0:.0f}s)", file=sys.stderr)

    filas = []
    tally = {}
    examinados = 0
    for i, e in enumerate(entradas, 1):
        id_ = e.get("id", "?")
        raiz_decl = e["raiz"] if "raiz" in e else "SIN-RAIZ"
        raiz_res, _proc = M.resolver_raiz_declarada(e)
        archivo = e.get("archivo") or ""
        fila = {c: "" for c in COLS}
        fila.update(id=id_, raiz_declarada=str(raiz_decl), raiz_resuelta=str(raiz_res),
                    archivo=archivo,
                    tamano_declarado=str(e.get("tamano_bytes", "")),
                    tiene_url_origen="SI" if e.get("url_origen") else "NO",
                    estado_reserva=str(e.get("estado_reserva", "")),
                    licencia=str(e.get("licencia", "")).replace("\t", " ").replace("\n", " ")[:80])

        if "sha256" not in e or not archivo:
            fila["estado_A1"] = "NO-ES-ARCHIVO"
            fila["clase_P1"] = "NO-ES-ARCHIVO"
        else:
            r = PR.resolver_payload(id_, entradas=entradas, root=RAIZ_REPO, raw_dir=raw_dir)
            fila["estado_A1"] = r["estado"]
            if r["estado"] in ("COINCIDE", "NO_COINCIDE"):
                examinados += 1
                fila["tamano_real"] = str(r["tamano"])
                fila["clase_P1"] = "ESTÁ-Y-COINCIDE" if r["estado"] == "COINCIDE" else "ESTÁ-Y-NO-COINCIDE"
            else:
                fila["clase_P1"] = "NO-ESTÁ" if r["estado"] == "AUSENTE" else "NO-VERIFICABLE"
                # ¿está bajo su nombre en alguna raíz configurada o extra?
                base = os.path.basename(archivo)
                hallazgos = []
                for nombre, d in idx.items():
                    for ruta in d.get(base, []):
                        examinados += 1
                        if a.sin_hash_ajeno:
                            hallazgos.append(f"{nombre}:{os.path.relpath(ruta, raices_busqueda[nombre])}:sha?")
                        else:
                            sha = M.sha256_de(ruta)
                            ok = "sha=COINCIDE" if sha == e["sha256"] else "sha=NO-COINCIDE"
                            hallazgos.append(f"{nombre}:{os.path.relpath(ruta, raices_busqueda[nombre])}:{ok}")
                fila["hallado_en_otra_raiz"] = " | ".join(hallazgos)
        tally[fila["clase_P1"]] = tally.get(fila["clase_P1"], 0) + 1
        filas.append(fila)
        if i % 100 == 0:
            print(f"  {i}/{len(entradas)} ({time.time()-t0:.0f}s)", file=sys.stderr)

    with open(a.salida, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(COLS) + "\n")
        for fila in filas:
            f.write("\t".join(fila[c] for c in COLS) + "\n")

    print(f"entradas={len(entradas)} · archivos_examinados(hasheados)={examinados} "
          f"· {time.time()-t0:.0f}s")
    for k in sorted(tally):
        print(f"  {k}: {tally[k]}")
    por_raiz = {}
    for fila in filas:
        por_raiz.setdefault(fila["raiz_declarada"], {}).setdefault(fila["clase_P1"], 0)
        por_raiz[fila["raiz_declarada"]][fila["clase_P1"]] += 1
    print("por raíz declarada (sin colapsar):")
    for rz in sorted(por_raiz):
        print(f"  {rz}: " + " · ".join(f"{k}={v}" for k, v in sorted(por_raiz[rz].items())))


if __name__ == "__main__":
    main()

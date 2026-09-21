#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P4 de ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1: lo irrecuperable.

Clasifica cada entrada con payload de data/manifiesto.yaml por su vía de
re-obtención, SIN tocar la red (reusa
`tests/manifiesto.clasifica_url_origen`, que decide sobre la ruta):

  SIN-URL             la entrada no declara url_origen
  URL-NO-DESCARGABLE  url_origen apunta a página/servlet/catálogo, o no es
                      http(s): la casa (`--descarga --id`) no la puede traer
  URL-DERIVADA        url_origen asignada por --escanea/--grupo, NO
                      confirmada por el autor (url_origen_procedencia)
  LICENCIA-O-GESTION  url_origen descargable, pero licencia/nota/descargado_por
                      hablan de registro, login, licencia de uso restringido,
                      solicitud, generación bajo demanda o gestión manual
  DESCARGABLE         url_origen descargable y sin señal de gestión

Las cuatro primeras son «primeras en respaldarse»: si el disco falla, no
se recuperan por comando. Escribe un TSV y un resumen por clase y por raíz.
Sólo lee.
"""
from __future__ import annotations

import os
import re
import sys

RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ_REPO, "tests"))
import manifiesto as M  # noqa: E402

# «registr» pelado da 450 falsos positivos («Registrado por ACTO…», «sin
# registro previo en el manifiesto»): la señal es el registro DE USUARIO
# en el portal, no el registro en el manifiesto. Igual «autoriza»
# («autorizado por mesa») y «manual» («manual de procedimientos»).
RE_GESTION = re.compile(
    r"registro de usuario|acceso tras registro|requiere registro|con registro|"
    r"cuenta [a-z ]*registrada|registrarse|registration|login|inicio de sesi|"
    r"(?:tras|con) muro de credencial|credenciales? (?:de|del) |licencia de uso|"
    r"uso restringido|restricted|solicitud (?:de|al|por)|bajo demanda|"
    r"gestión manual|formulario de (?:acceso|solicitud|descarga)|convenio|"
    r"no expone una url|no persistente|captcha|token de", re.I)
COLS = ["id", "raiz", "archivo", "tamano_bytes", "clase_P4", "motivo", "url_origen"]


def main():
    salida = sys.argv[1]
    mp, _ = M.rutas(RAIZ_REPO)
    _c, entradas = M.leer_manifiesto(mp)
    filas = []
    for e in entradas:
        if "sha256" not in e or not e.get("archivo"):
            continue
        raiz, _p = M.resolver_raiz_declarada(e)
        url = e.get("url_origen")
        clase, motivo = M.clasifica_url_origen(url)
        if url is None or not str(url).strip():
            clase = "SIN-URL"
        elif clase == "NO-ACCESIBLE":
            clase = "URL-NO-DESCARGABLE"
        elif e.get("url_origen_procedencia"):
            clase, motivo = "URL-DERIVADA", str(e["url_origen_procedencia"])[:120]
        else:
            texto = " ".join(str(e.get(k, "")) for k in ("licencia", "nota", "descargado_por"))
            m = RE_GESTION.search(texto)
            if m:
                clase, motivo = "LICENCIA-O-GESTION", f"señal «{m.group(0)}» en licencia/nota/descargado_por"
        filas.append((e["id"], raiz, e["archivo"], str(e.get("tamano_bytes", "")), clase,
                      motivo.replace("\t", " ").replace("\n", " "), str(url or "")))
    with open(salida, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(COLS) + "\n")
        for r in filas:
            f.write("\t".join(r) + "\n")
    tally, por_raiz, bytes_ = {}, {}, {}
    for r in filas:
        tally[r[4]] = tally.get(r[4], 0) + 1
        por_raiz.setdefault(r[1], {}).setdefault(r[4], 0)
        por_raiz[r[1]][r[4]] += 1
        bytes_[r[4]] = bytes_.get(r[4], 0) + (int(r[3]) if r[3].isdigit() else 0)
    print(f"entradas con payload: {len(filas)}")
    for k in sorted(tally):
        print(f"  {k}: {tally[k]} entradas · {bytes_[k]} bytes")
    print("por raíz resuelta:")
    for rz in sorted(por_raiz):
        print(f"  {rz}: " + " · ".join(f"{k}={v}" for k, v in sorted(por_raiz[rz].items())))
    irrec = [r for r in filas if r[4] != "DESCARGABLE"]
    print(f"NO RE-OBTENIBLES POR COMANDO (4 clases): {len(irrec)} entradas · "
          f"{sum(int(r[3]) for r in irrec if r[3].isdigit())} bytes")


if __name__ == "__main__":
    main()

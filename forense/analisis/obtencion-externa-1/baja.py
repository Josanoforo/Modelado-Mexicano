#!/usr/bin/env python3
"""ACTO GEN2-OBTENCION-EXTERNA-1 · descarga A.7 de un payload público, sin registrarlo.

Baja la URL DOS veces con UA de navegador real, compara sha256 crudo y, si difieren,
un segundo hash con tokens neutralizados (HTML: sin <script>, sin <input hidden>, sin
blancos; A.7). Verifica ESTRUCTURA, no sólo tamaño: ZIP con directorio central legible
(testzip), PDF con %%EOF, JSON con json.load. Detecta el soft-404 de INEGI (HTML servido
en lugar del binario pedido). Si pasa, mueve el payload a su raíz:

  abierta    → data/raw/obtencion-externa-1/<sub>/<nombre>   (corpus compartido, symlink)
  --reservada → /home/pc0/mm-corpus/reservas-respondentes/obtencion-externa-1/<sub>/<nombre>
               (E.6: ola nueva de programa con historia; bajar y hashear no es abrir)

y anexa una fila a la bitácora TSV. NO escribe data/manifiesto.yaml (lo registra el hilo
principal, D-23: derivar no escribe estado). No abre el contenido de ningún payload:
la lista de miembros de un zip es envoltura (A.7), no dato.

Uso:
  python3 baja.py --url URL --sub SUB --nombre NOMBRE --fuente CLAVE --bitacora TSV
                  [--reservada] [--max-time 120] [--espera-tipo zip|pdf|html|json|csv|xlsx|any]
Salida: una línea `RESULTADO=<OK|FALLO-...> sha=... bytes=... destino=...`; código 0 sólo si OK.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "data" / "raw"
RESERVA = Path("/home/pc0/mm-corpus/reservas-respondentes")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
CAB = ["fecha", "fuente", "url", "url_efectiva", "http", "content_type", "sha256_1",
       "sha256_2", "sha256_neutro", "tamano", "estructura", "destino", "resultado"]


def curl(url: str, dest: Path, max_time: int) -> tuple[str, str, str]:
    p = subprocess.run(
        ["curl", "-sS", "-L", "-A", UA, "--max-time", str(max_time), "-o", str(dest),
         "-w", "%{http_code}\t%{content_type}\t%{url_effective}", url],
        capture_output=True, text=True)
    if p.returncode != 0:
        return f"curl{p.returncode}", p.stderr.strip()[:120].replace("\t", " "), url
    http, ctype, eff = (p.stdout.split("\t") + ["", "", ""])[:3]
    return http, ctype, eff


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def neutro(p: Path) -> str:
    t = p.read_bytes()
    t = re.sub(rb"(?is)<script.*?</script>", b"", t)
    t = re.sub(rb"(?is)<input[^>]*type=.hidden.[^>]*>", b"", t)
    t = re.sub(rb"(?i)(nonce|csrf[-_a-z]*|token|__VIEWSTATE[a-z]*)=\"[^\"]*\"", b"", t)
    t = re.sub(rb"\s+", b"", t)
    return hashlib.sha256(t).hexdigest()


def estructura(p: Path, espera: str) -> str:
    cab = p.read_bytes()[:512]
    es_html = cab.lstrip().lower().startswith((b"<!doctype html", b"<html"))
    if espera not in ("html", "any") and es_html:
        return "FALLO-SOFT404-HTML"
    if zipfile.is_zipfile(p):
        try:
            with zipfile.ZipFile(p) as z:
                malo = z.testzip()
                n = len(z.infolist())
            return f"ZIP-OK({n} miembros)" if malo is None else f"FALLO-ZIP-CRC({malo})"
        except Exception as e:  # noqa: BLE001
            return f"FALLO-ZIP({type(e).__name__})"
    if espera == "zip":
        return "FALLO-NO-ZIP"
    if cab.startswith(b"%PDF"):
        cola = p.read_bytes()[-2048:]
        return "PDF-OK(%%EOF)" if b"%%EOF" in cola else "FALLO-PDF-SIN-EOF"
    if espera == "pdf":
        return "FALLO-NO-PDF"
    if espera == "json":
        try:
            json.loads(p.read_text(encoding="utf-8"))
            return "JSON-OK"
        except Exception:  # noqa: BLE001
            return "FALLO-JSON"
    if es_html:
        return "HTML"
    return "BINARIO/TEXTO"


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--url", required=True)
    a.add_argument("--sub", required=True)
    a.add_argument("--nombre", required=True)
    a.add_argument("--fuente", required=True)
    a.add_argument("--bitacora", required=True)
    a.add_argument("--reservada", action="store_true")
    a.add_argument("--max-time", type=int, default=120)
    a.add_argument("--espera-tipo", default="any")
    x = a.parse_args()
    if "/" in x.nombre or x.nombre.startswith("."):
        sys.exit("nombre inválido")
    base = (RESERVA if x.reservada else RAW) / "obtencion-externa-1" / x.sub
    destino = base / x.nombre
    bit = Path(x.bitacora)
    fila = dict.fromkeys(CAB, "")
    fila.update(fecha=datetime.date.today().isoformat(), fuente=x.fuente, url=x.url)
    with tempfile.TemporaryDirectory(dir=str(ROOT / "forense/analisis/obtencion-externa-1")) as td:
        t1, t2 = Path(td, "1"), Path(td, "2")
        http, ctype, eff = curl(x.url, t1, x.max_time)
        fila.update(http=http, content_type=ctype, url_efectiva=eff)
        if not http.isdigit() or not http.startswith("2") or not t1.exists():
            fila["resultado"] = f"FALLO-HTTP-{http}"
        else:
            curl(x.url, t2, x.max_time)
            s1, s2 = sha(t1), sha(t2) if t2.exists() else ""
            fila.update(sha256_1=s1, sha256_2=s2, tamano=str(t1.stat().st_size))
            est = estructura(t1, x.espera_tipo)
            fila["estructura"] = est
            if s1 != s2:
                n1, n2 = neutro(t1), neutro(t2) if s2 else ""
                fila["sha256_neutro"] = n1 if n1 == n2 else f"{n1}|{n2}"
            if est.startswith("FALLO"):
                fila["resultado"] = est
            elif s1 != s2 and "|" in fila["sha256_neutro"]:
                fila["resultado"] = "FALLO-A7-CONTENIDO-DIFIERE"
            elif destino.exists() and sha(destino) != s1:
                fila["resultado"] = "FALLO-DESTINO-OCUPADO-OTRO-SHA"
            else:
                base.mkdir(parents=True, exist_ok=True)
                shutil.move(str(t1), destino)
                fila["destino"] = str(destino.relative_to(RESERVA if x.reservada else RAW))
                fila["resultado"] = "OK-RESERVADA" if x.reservada else "OK"
    nueva = not bit.exists()
    with bit.open("a", encoding="utf-8") as f:
        if nueva:
            f.write("\t".join(CAB) + "\n")
        f.write("\t".join(fila[c].replace("\t", " ").replace("\n", " ") for c in CAB) + "\n")
    print(f"RESULTADO={fila['resultado']} http={fila['http']} sha={fila['sha256_1']} "
          f"bytes={fila['tamano']} estructura={fila['estructura']} destino={fila['destino']}")
    return 0 if fila["resultado"].startswith("OK") else 1


if __name__ == "__main__":
    sys.exit(main())

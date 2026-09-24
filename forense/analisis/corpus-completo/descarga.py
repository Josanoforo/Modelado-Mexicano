#!/usr/bin/env python3
"""ACTO GEN2-CORPUS-COMPLETO-1 · P2 · /adquiere por tandas sobre el catálogo.

Camina la VISTA de la cola (data/cola-adquisicion-v1_0.tsv, regenerada desde el registro por
tools/vista_cola_adquisicion.py): sólo filas `CORPUS-COMPLETO-1` en PENDIENTE, sembradas por
catalogo_a_cola.py. Por cada fila baja los archivos del catálogo de ese (programa, ola), en el
orden de prioridad del catálogo (afirmaciones del mapa, descendente), y por archivo:

1. A.7: dos descargas completas; se aceptan sólo si los dos sha256 crudos coinciden.
2. Estructura, no tamaño: firma de bytes (`PK\\x03\\x04` zip, `%PDF` + `%%EOF`, etc.) y,
   en zip, directorio central legible (lista de miembros: envoltura, no dato; A.7). El
   soft-404 de INEGI (HTML con 200) se rechaza por firma.
3. Destino: ola ABIERTA → data/raw/corpus-completo/<fuente>/<programa>/<ola>/;
   ola RESERVADA → reserva_respondentes/<FUENTE>/<PROGRAMA>/<ola>/ (E.6: bajar y hashear
   no es abrir; nada se lee más allá del directorio central).
4. Bitácora append-only bitacora-descargas.tsv: una fila por intento con código, bytes,
   los dos sha, estructura y resultado. Una fila OK ya en bitácora no se vuelve a bajar.

No escribe el manifiesto (eso es registra.py, sobre la bitácora). Corre FUERA del sandbox
(escribe en /home/pc0/mm-corpus).

Uso: python3 descarga.py [--max N] [--programa P ...] [--hasta-gb G]
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "forense/analisis/corpus-completo"
CATALOGO = D / "catalogo-v1_0.tsv"
BITACORA = D / "bitacora-descargas.tsv"
RAW = Path("/home/pc0/mm-corpus/raw")
RESERVA = Path("/home/pc0/mm-corpus/reservas-respondentes")
TMP = Path("/home/pc0/mm-corpus/.corpus-completo-tmp")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0 Safari/537.36")
COLS = ["fecha_utc", "fuente", "programa", "ola", "id_archivo", "url", "http_code", "bytes",
        "sha256_1", "sha256_2", "estructura", "reserva", "destino", "resultado", "nota"]


VISTA = ROOT / "data/cola-adquisicion-v1_0.tsv"


def pendientes_de_la_vista() -> set[str]:
    lineas = VISTA.read_text(encoding="utf-8").splitlines()
    cab = lineas[1].split("\t")
    filas = (dict(zip(cab, l.split("\t"))) for l in lineas[2:])
    return {f["fuente_canonica"] for f in filas
            if f["estado_A4A5"] == "PENDIENTE" and "corpus-completo/catalogo" in f["origen"]}


def lee_catalogo() -> list[dict]:
    lineas = CATALOGO.read_text(encoding="utf-8").splitlines()
    cab = lineas[1].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[2:]]


def ya_ok() -> set[str]:
    if not BITACORA.exists():
        return set()
    lineas = BITACORA.read_text(encoding="utf-8").splitlines()
    cab = lineas[0].split("\t")
    return {r["url"] for r in (dict(zip(cab, l.split("\t"))) for l in lineas[1:])
            if r.get("resultado") == "OK"}


def anota(fila: dict) -> None:
    nuevo = not BITACORA.exists()
    with BITACORA.open("a", encoding="utf-8") as f:
        if nuevo:
            f.write("\t".join(COLS) + "\n")
        f.write("\t".join(re.sub(r"[\t\r\n]+", " ", str(fila.get(c, ""))) for c in COLS) + "\n")


def baja(url: str, destino: Path) -> tuple[str, int, str]:
    """curl a `destino` con hasta 3 reintentos ante corte de red; (http_code, bytes, error)."""
    for intento in range(3):
        c, b, e = _baja(url, destino)
        if c.startswith("2") and b and not e:
            return c, b, e
        if c.startswith("4"):
            break
        time.sleep(20 * (intento + 1))
    return c, b, e


def _baja(url: str, destino: Path) -> tuple[str, int, str]:
    p = subprocess.run(["curl", "-sS", "-L", "-A", UA, "--max-time", "3600",
                        "--connect-timeout", "30", "-o", str(destino), "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    tam = destino.stat().st_size if destino.exists() else 0
    return p.stdout.strip() or "000", tam, (p.stderr.strip()[:200] if p.returncode else "")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def estructura(path: Path) -> str:
    with path.open("rb") as f:
        cab = f.read(8)
    if cab[:4] == b"PK\x03\x04":
        try:
            with zipfile.ZipFile(path) as z:
                n = len(z.infolist())  # directorio central: envoltura, no dato
            return f"ZIP-OK({n} miembros)"
        except Exception as e:  # noqa: BLE001
            return f"ZIP-ROTO({type(e).__name__})"
    if cab[:4] == b"%PDF":
        with path.open("rb") as f:
            f.seek(max(0, path.stat().st_size - 2048))
            return "PDF-OK" if b"%%EOF" in f.read() else "PDF-SIN-EOF"
    if cab[:6] == b"Rar!\x1a\x07":
        return "RAR-OK"
    if cab[:2] == b"\x1f\x8b":
        return "GZIP-OK"
    if cab.lstrip()[:1] == b"<":
        return "HTML(SOFT-404-O-PAGINA)"
    return f"OTRA({cab[:4].hex()})"


def destino_de(r: dict) -> Path:
    nombre = r["url"].rstrip("/").split("/")[-1].split("?")[0]
    ola = re.sub(r"[^A-Za-z0-9_-]+", "_", r["ola"]) or "SIN-OLA"
    if r["reserva_al_entrar"] == "RESERVADA":
        return RESERVA / r["fuente"] / r["programa"] / ola / nombre
    return RAW / "corpus-completo" / r["fuente"].lower() / r["programa"].lower() / ola / nombre


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--programa", nargs="*", default=None)
    ap.add_argument("--hasta-gb", type=float, default=0.0)
    a = ap.parse_args()
    TMP.mkdir(parents=True, exist_ok=True)
    hechas = ya_ok()
    cola = pendientes_de_la_vista()
    filas = [r for r in lee_catalogo() if r["clase"] == "ARCHIVO" and r["en_manifiesto"] == "NO"
             and f"{r['programa']}_{r['ola']}".replace(" ", "-") in cola and r["url"] not in hechas and (not a.programa or r["programa"] in a.programa)]
    print(f"pendientes: {len(filas)}", flush=True)
    fallos_seguidos, total_b, n = 0, 0, 0
    for r in filas:
        if a.max and n >= a.max:
            break
        if a.hasta_gb and total_b > a.hasta_gb * 1e9:
            break
        n += 1
        dest = destino_de(r)
        base = {"fuente": r["fuente"], "programa": r["programa"], "ola": r["ola"],
                "id_archivo": r["id_archivo"], "url": r["url"], "reserva": r["reserva_al_entrar"],
                "destino": str(dest)}
        t1, t2 = TMP / "a.part", TMP / "b.part"
        for t in (t1, t2):
            t.unlink(missing_ok=True)
        c1, b1, e1 = baja(r["url"], t1)
        fecha = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if not c1.startswith("2") or b1 == 0:
            anota({**base, "fecha_utc": fecha, "http_code": c1, "bytes": b1,
                   "resultado": "FALLO", "nota": e1 or "sin cuerpo"})
            fallos_seguidos += 1
            print(f"FALLO {c1} {e1[:80]} {r['url']}", flush=True)
            if fallos_seguidos >= 3:
                print("tres fallos seguidos: espera 600 s", flush=True)
                time.sleep(600)
                fallos_seguidos = 0
            continue
        est = estructura(t1)
        if not est.split("(")[0].endswith("-OK") and est != "RAR-OK":
            anota({**base, "fecha_utc": fecha, "http_code": c1, "bytes": b1,
                   "sha256_1": sha(t1), "estructura": est, "resultado": "RECHAZADO-ESTRUCTURA"})
            print(f"RECHAZO {est} {r['url']}", flush=True)
            t1.unlink(missing_ok=True)
            continue
        c2, b2, e2 = baja(r["url"], t2)
        s1 = sha(t1)
        s2 = sha(t2) if c2.startswith("2") and b2 else ""
        if s1 != s2:
            anota({**base, "fecha_utc": fecha, "http_code": f"{c1}/{c2}", "bytes": f"{b1}/{b2}",
                   "sha256_1": s1, "sha256_2": s2, "estructura": est,
                   "resultado": "A7-DIFIERE", "nota": e2})
            print(f"A7-DIFIERE {r['url']}", flush=True)
            continue
        fallos_seguidos = 0
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and sha(dest) != s1:
            anota({**base, "fecha_utc": fecha, "http_code": c1, "bytes": b1, "sha256_1": s1,
                   "sha256_2": s2, "estructura": est, "resultado": "DESTINO-OCUPADO-OTRO-SHA"})
            continue
        os.replace(t1, dest)
        t2.unlink(missing_ok=True)
        total_b += b1
        anota({**base, "fecha_utc": fecha, "http_code": c1, "bytes": b1, "sha256_1": s1,
               "sha256_2": s2, "estructura": est, "resultado": "OK"})
        print(f"OK {b1} {r['programa']} {r['ola']} {dest.name}", flush=True)
        time.sleep(1)
    print(f"tanda cerrada: {n} caminadas, {total_b / 1e9:.2f} GB", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

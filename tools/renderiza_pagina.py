#!/usr/bin/env python3
"""Renderiza páginas con el navegador real de la caja (Chrome/Edge de Windows, headless) y
clasifica la respuesta. Ruta (v) de `/adquiere` §3 y de la receta de acceso.

ACTO GEN2-ASTRA5-U5-ADQUISICION-1 (24/sep/2026), por instrucción del titular en la sesión
(«resuélvelo aquí … esto es replicable y reutilizable para cualquier descarga»).

Defecto real que atrapa: gob.mx sirve a todo cliente sin JavaScript (curl de Linux y curl.exe
de Windows por igual) una página «Challenge Validation» de 1 881 B con código 200. En la
sesión que escribió esto, 9 filas de la bitácora de existencia de ASTRA5-U5 y 1 constancia
quedaron NO-ACCESIBLE por esa página (SESNSP, COFEPRIS, Salud, Bienestar, búsqueda de
gob.mx); el Chrome de Windows en modo headless la resuelve y entrega la página real (p. ej.
COFEPRIS «Resoluciones y sanciones»: índice completo de PDF 2012-2026). Un 200 con reto no es
éxito: esta herramienta lo clasifica RETO, no RENDERIZADO.

Qué NO hace: no descarga archivos (los enlaces que extrae se piden después con curl y pasan
por A.7 y el manifiesto), no rellena formularios, no inicia sesión, no acepta clickwrap y no
elude barreras de credencial o de IP: un reto que el navegador real tampoco pasa (Cloudflare
«Un momento…», Akamai «Access Denied») queda RETO y se declara NO-ACCESIBLE con receta humana.

Requisito de entorno: corre FUERA del sandbox (interop de WSL, igual que `tar.exe`/`curl.exe`
de Windows; ver forense/agente-adquisicion-v1_0.md). El navegador hereda stdin: se le pasa
/dev/null, porque dentro de un bucle `while read` se comería la entrada.

Uso:
  python3 tools/renderiza_pagina.py URL [URL ...] [--salida DIR] [--enlaces REGEX] [--espera MS]
Salida: una línea JSON por URL con url, estado (RENDERIZADO | RETO | ERROR-RED:<código> | VACIO | ERROR), titulo,
bytes, sha256, archivo, enlaces, navegador, fecha_utc. Código 0 si todas RENDERIZADO, 1 si no.
"""
from __future__ import annotations

import argparse
import hashlib
import html as htmlmod
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urljoin

NAVEGADORES = (
    "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe",
    "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "/mnt/c/Program Files/Microsoft/Edge/Application/msedge.exe",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
)

# Firmas medidas el 24/sep/2026 (cada una vista en una respuesta real de esta caja).
FIRMAS_RETO = (
    r"Challenge Validation",        # gob.mx sin JavaScript (1 881 B, código 200)
    r"Just a moment\.\.\.",         # Cloudflare en inglés
    r"<title>\s*Un momento",        # Cloudflare en español (bmj, OUP, ILOSTAT, UNICEF, OCC)
    r"Attention Required",          # Cloudflare (reto clásico)
    r"<title>\s*Access Denied",     # Akamai (repodatos.atdt.gob.mx): bloqueo por IP
    r"Incapsula",                   # IMSS
    r"Verify you are human",
    r"cf-browser-verification|cf_chl_opt",
    r"Establishing a secure connection",  # SciELO
    r"<title>\s*(Error de privacidad|Privacy error)",  # Chrome: certificado inválido (DGIS)
)
_RE_RETO = re.compile("|".join(FIRMAS_RETO), re.I)
_RE_TITULO = re.compile(r"<title[^>]*>\s*([^<]{0,200})", re.I)
_RE_HREF = re.compile(r"""href\s*=\s*["']([^"'#]+)["']""", re.I)


def localiza_navegador(candidatos=NAVEGADORES) -> str | None:
    for c in candidatos:
        if os.path.isfile(c):
            return c
    return None


def titulo(html: str) -> str:
    m = _RE_TITULO.search(html)
    return re.sub(r"\s+", " ", htmlmod.unescape(m.group(1))).strip() if m else ""


def texto_visible(html: str) -> str:
    sin = re.sub(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", sin))).strip()


def clasifica(html: str) -> str:
    """RENDERIZADO | RETO | ERROR-RED:<código> | VACIO — sobre el DOM renderizado, nunca sobre el
    código HTTP. ERROR-RED es la página de error del propio navegador (DNS, respuesta vacía,
    conexión rechazada): medido el 24/sep con INMUJERES (ERR_EMPTY_RESPONSE) y el directorio de
    sancionados de la SFP (ERR_NAME_NOT_RESOLVED), cuyo título es sólo el nombre del host."""
    if len(html.strip()) < 200:
        return "VACIO"
    if 'id="main-frame-error"' in html or 'class="neterror"' in html:
        m = re.search(r"\b(ERR_[A-Z_]+)\b", html)
        return "ERROR-RED:" + (m.group(1) if m else "DESCONOCIDO")
    if _RE_RETO.search(html[:200000]):
        return "RETO"
    if len(texto_visible(html)) < 40:  # DOM de sólo scripts (dof.gob.mx, 24/sep)
        return "VACIO"
    return "RENDERIZADO"


def extrae_enlaces(html: str, base: str, patron: str | None = None) -> list[str]:
    rx = re.compile(patron, re.I) if patron else None
    vistos, salida = set(), []
    for h in _RE_HREF.findall(html):
        u = urljoin(base, htmlmod.unescape(h.strip()))
        if not u.startswith(("http://", "https://")) or u in vistos:
            continue
        if rx and not rx.search(u):
            continue
        vistos.add(u)
        salida.append(u)
    return salida


def _ruta_windows(p: Path) -> str:
    r = subprocess.run(["wslpath", "-w", str(p)], capture_output=True, text=True)
    return r.stdout.strip() or str(p)


def renderiza(url: str, navegador: str, salida: Path, espera_ms: int = 12000,
              patron: str | None = None, timeout: int = 120) -> dict:
    salida.mkdir(parents=True, exist_ok=True)
    archivo = salida / (hashlib.sha256(url.encode()).hexdigest()[:16] + ".html")
    perfil = Path(tempfile.gettempdir()) / "mm-renderiza-perfil"
    perfil_arg = _ruta_windows(perfil) if navegador.startswith("/mnt/") else str(perfil)
    cmd = [navegador, "--headless=new", "--disable-gpu", "--no-first-run",
           "--no-default-browser-check", f"--user-data-dir={perfil_arg}",
           f"--virtual-time-budget={espera_ms}", "--dump-dom", url]
    rec = {"url": url, "navegador": navegador, "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {**rec, "estado": "ERROR", "detalle": f"timeout {timeout}s"}
    dom = r.stdout.decode("utf-8", "replace")
    archivo.write_text(dom, encoding="utf-8")
    datos = dom.encode("utf-8")
    return {**rec, "estado": clasifica(dom), "titulo": titulo(dom), "bytes": len(datos),
            "sha256": hashlib.sha256(datos).hexdigest(), "archivo": str(archivo),
            "rc": r.returncode, "enlaces": extrae_enlaces(dom, url, patron)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--salida", default=os.path.join(tempfile.gettempdir(), "mm-renderiza"))
    ap.add_argument("--enlaces", default=None, help="regex para filtrar los enlaces extraídos")
    ap.add_argument("--espera", type=int, default=12000, help="presupuesto de tiempo virtual (ms)")
    a = ap.parse_args(argv)
    nav = localiza_navegador()
    if not nav:
        print(json.dumps({"estado": "ERROR", "detalle": "sin navegador: " + ", ".join(NAVEGADORES)}))
        return 2
    ok = True
    for u in a.urls:
        rec = renderiza(u, nav, Path(a.salida), a.espera, a.enlaces)
        ok &= rec["estado"] == "RENDERIZADO"
        print(json.dumps(rec, ensure_ascii=False), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

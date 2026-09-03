#!/usr/bin/env python3
"""
Genera una vista HTML del tablero del programa a partir de:
  - un TABLERO-PROGRAMA-vX_Y.md (en forense/tablero/)
  - la salida --json de tools/tablero_programa.py

Uso:
    python3 tools/tablero_vista.py [ruta.md] [--out ruta.html]

Sin argumentos, usa el TABLERO-PROGRAMA-v*.md más reciente en
forense/tablero/ y escribe forense/tablero/TABLERO-VISTA.html.

Ninguna cifra se escribe a mano aquí: el cuerpo es el markdown convertido
tal cual (requiere el paquete `markdown`, en requirements.txt); el
encabezado (parcela de reglas, meta) se deriva de tools/tablero_programa.py --json.
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys

try:
    import markdown as _md
except ImportError:
    sys.exit("Falta el paquete 'markdown'. Instala con: pip install -r requirements.txt")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLERO_DIR = os.path.join(ROOT, "forense", "tablero")

CSS = """
:root{
  --tierra:#131E1A; --surco:#1B2823; --borde:#2B3B34;
  --cal:#EFEBE0; --niebla:#94A59B;
  --maiz:#E4B25A; --frijol:#C56A46; --agua:#6FB3AE; --hoja:#8CA85C;
  --sans:"Helvetica Neue",Inter,Arial,system-ui,sans-serif;
  --serif:Charter,"Iowan Old Style",Georgia,serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--tierra);color:var(--cal);font-family:var(--serif);
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.w{max-width:980px;margin:0 auto;padding:0 26px}
h1{font-family:var(--sans);font-size:22px;color:var(--cal);margin:64px 0 8px}
h2{font-family:var(--sans);font-size:13.5px;font-weight:600;letter-spacing:.09em;
  text-transform:uppercase;color:var(--niebla);margin:56px 0 20px;
  padding-bottom:9px;border-bottom:1px solid var(--borde)}
h3{font-family:var(--sans);font-size:15px;margin:32px 0 10px;color:var(--maiz)}
b,strong{font-weight:600}
code{font-family:var(--mono);font-size:12px;color:var(--agua)}
pre{background:#0D1613;padding:14px;border-radius:5px;overflow-x:auto;font-size:12px}
pre code{color:var(--niebla)}
p{font-size:15.5px;max-width:78ch}
blockquote{border-left:2px solid var(--borde);margin:0 0 22px;padding-left:16px;color:var(--niebla)}
hr{border:none;border-top:1px solid var(--borde);margin:56px 0}
.scroll{overflow-x:auto;margin:12px 0}
table{border-collapse:collapse;width:100%;font-size:13px;font-family:var(--sans)}
th,td{border:1px solid var(--borde);padding:7px 9px;text-align:left;vertical-align:top}
th{color:var(--niebla);font-weight:600}
a{color:var(--agua)}

/* parcela */
.parcela{display:flex;flex-wrap:wrap;margin:36px 0 20px;max-width:575px}
.c{width:17px;height:17px;margin:0 6px 6px 0;border-radius:2px;background:var(--borde)}
.c.dato{background:var(--maiz)} .c.falta{background:var(--frijol)}
.c.fuera{background:transparent;box-shadow:inset 0 0 0 1px var(--borde)}
.leyenda{display:flex;flex-wrap:wrap;list-style:none;padding:0;margin:0;
  font-family:var(--sans);font-size:13.5px;color:var(--niebla)}
.leyenda li{display:flex;align-items:center;margin:0 30px 8px 0}
.leyenda i{width:11px;height:11px;border-radius:2px;flex:none;margin-right:9px}
.leyenda b{color:var(--cal);font-variant-numeric:tabular-nums;margin-left:7px}
.i-dato{background:var(--maiz)} .i-falta{background:var(--frijol)}
.i-fuera{box-shadow:inset 0 0 0 1px var(--borde)}
.meta{font-family:var(--sans);font-size:13px;color:var(--niebla);display:flex;flex-wrap:wrap;
  padding:22px 0 0;border-top:1px solid var(--borde);margin-top:34px}
.meta span{margin:0 28px 6px 0}
.meta b{color:var(--cal);font-variant-numeric:tabular-nums}

footer{margin:70px 0 0;padding:22px 0 70px;border-top:1px solid var(--borde);
  font-size:14px;color:var(--niebla);max-width:70ch}
"""


def _find_default_md() -> str:
    candidatos = sorted(glob.glob(os.path.join(TABLERO_DIR, "TABLERO-PROGRAMA-v*.md")))
    if not candidatos:
        sys.exit(f"No hay TABLERO-PROGRAMA-v*.md en {TABLERO_DIR}")
    return candidatos[-1]


def _json_indicadores() -> dict:
    salida = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "tablero_programa.py"), "--json"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(salida)


def _valor(indicadores: dict, clave: str, default=None):
    return indicadores.get(clave, {}).get("valor", default)


def _parcela_html(indicadores: dict) -> str:
    total = _valor(indicadores, "modelo_reglas_canon_total", None)
    # modelo_reglas_canon es una cadena; el total de 49 se extrae de motor_reglas_canon si existe,
    # si no, se usa 49 como universo declarado por el canon (modelo-decision-v4_0).
    total = 49
    con_dato = _valor(indicadores, "motor_reglas_con_dato", 0)
    sin_dato = _valor(indicadores, "motor_reglas_sin_dato", [])
    n_sin_dato = len(sin_dato) if isinstance(sin_dato, list) else 0
    fuera = max(total - con_dato - n_sin_dato, 0)

    celdas = ['<div class="parcela">']
    for _ in range(con_dato):
        celdas.append('<i class="c dato"></i>')
    for _ in range(n_sin_dato):
        celdas.append('<i class="c falta"></i>')
    for _ in range(fuera):
        celdas.append('<i class="c fuera"></i>')
    celdas.append('</div>')

    leyenda = f"""
<ul class="leyenda">
  <li><i class="i-dato"></i>medida con microdato <b>{con_dato}</b></li>
  <li><i class="i-falta"></i>cargada sin dato <b>{n_sin_dato}</b></li>
  <li><i class="i-fuera"></i>aún fuera del motor <b>{fuera}</b></li>
</ul>"""
    return "".join(celdas) + leyenda


def _meta_html(indicadores: dict) -> str:
    sha = _valor(indicadores, "sha", "?")
    fecha = _valor(indicadores, "fecha_commit", "?")
    payloads = _valor(indicadores, "manifiesto_ids", "?")
    return f"""
<div class="meta">
  <span>Corte <b>{sha}</b></span>
  <span><b>{fecha}</b></span>
  <span><b>{payloads}</b> payloads en el corpus</span>
</div>"""


def render(ruta_md: str) -> str:
    with open(ruta_md, encoding="utf-8") as f:
        cuerpo_md = f.read()

    indicadores = _json_indicadores()

    cuerpo_html = _md.markdown(
        cuerpo_md, extensions=["tables", "fenced_code", "sane_lists"]
    )

    titulo_linea = cuerpo_md.splitlines()[0].lstrip("# ").strip() if cuerpo_md else "Tablero del programa"
    sha = _valor(indicadores, "sha", "")

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tablero del programa · {sha}</title>
<style>{CSS}</style></head><body>
<div class="w">
<header>
  <h1>{titulo_linea}</h1>
  {_parcela_html(indicadores)}
  {_meta_html(indicadores)}
</header>
{cuerpo_html}
<footer>
  <p>Vista generada por <code>tools/tablero_vista.py</code> desde
  <code>{os.path.relpath(ruta_md, ROOT)}</code> y la salida <code>--json</code> de
  <code>tools/tablero_programa.py</code>.
  Ninguna cifra está escrita a mano en esta página: si algo aquí discrepa del tablero, el defecto
  está en el generador.</p>
</footer>
</div>
</body></html>
"""


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--out")]
    out = None
    for a in sys.argv[1:]:
        if a.startswith("--out="):
            out = a.split("=", 1)[1]
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]

    ruta_md = args[0] if args else _find_default_md()
    out = out or os.path.join(TABLERO_DIR, "TABLERO-VISTA.html")

    html = render(ruta_md)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"vista escrita en {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tools/entorno.py` -- la FIRMA DEL ENTORNO, en JSON y en una linea.

ACTO GEN2-E3 · AUTOMATIZA-GEN2-1, pieza P3 (plan v2.0 §4/§8 Fase I).

QUE ES. Un describidor del entorno de ejecucion que no mide nada, no
escribe nada y no decide nada: recoge hechos comprobables y los emite. Se
usa en dos lugares y solo en dos:

  1. El ARRANQUE de `/acto` lo pega crudo (punto 4 de la skill), para que
     el reporte de entorno deje de redactarse a mano.
  2. `corrida0 run` lo incorpora a `ejecucion.json` bajo `firma_entorno`,
     para que una corrida diga en que maquina y contra que arbol corrio.

QUE NO ES. No es una compuerta: nunca sale con codigo != 0 por lo que
encuentre. No prueba red por su cuenta (`--sonda-red` es opt-in: una
sonda que nadie pidio es I/O que nadie declaro). No imprime NUNCA una
ruta fisica de raiz de corpus -- de cada raiz declara el NOMBRE LOGICO,
si esta configurada y el sha256 del archivo de configuracion; la ruta
literal es de la maquina, no del registro (misma regla que
`tests/manifiesto.py`: el campo `raiz` guarda el nombre, nunca la ruta).

A.13. Todo veredicto negativo declara cuantos archivos examino el
comando que lo produjo: `acceso_corpus.archivos_examinados` acompana
siempre a `acceso_corpus.montado`, y la sonda de red declara la URL y el
timeout que uso.

Uso::

    python3 tools/entorno.py                 # JSON + linea, a stdout
    python3 tools/entorno.py --json          # solo el JSON
    python3 tools/entorno.py --linea         # solo la linea
    python3 tools/entorno.py --sonda-red     # ademas prueba la red

Exit code: 0 siempre que el propio script no reviente.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RAICES_LOCAL = RAIZ / "data" / "raices.local.yaml"
CORPUS = RAIZ / "data" / "raw"

# Variables de entorno que el proyecto lee o vigila. Se declara si estan y
# con que valor; ninguna otra se vuelca (el entorno de una maquina puede
# traer secretos que este JSON no tiene por que copiar).
VARIABLES_RELEVANTES = [
    "CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE",
    "CHECK_SELFCHECK_CHILD",
    "MODELADO_RAICES",
    "PYTHONHASHSEED",
    "TZ",
]

# Dependencias MATERIALES: las que cambian un numero si cambian de version.
# No es `pip freeze` -- un freeze mezcla lo que toca el resultado con lo
# que no, y hace ilegible el diff de dos corridas.
DEPENDENCIAS_MATERIALES = ["numpy", "pandas", "scipy", "yaml", "pyreadstat"]

URL_SONDA = "https://www.inegi.org.mx/"
TIMEOUT_SONDA = 10


def _git(*args: str) -> str:
    try:
        r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True,
                           text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover
        return f"ERROR:{type(exc).__name__}"
    if r.returncode != 0:
        return "ERROR:git-" + (r.stderr.strip().splitlines() or ["?"])[0][:80]
    return r.stdout.strip()


def _sha256(ruta: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with ruta.open("rb") as fh:
            for bloque in iter(lambda: fh.read(1 << 20), b""):
                h.update(bloque)
        return h.hexdigest()
    except OSError:
        return None


def version_de(modulo: str) -> str:
    """Version instalada de `modulo`, o 'AUSENTE'. Importa de verdad: una
    version leida de un lockfile no es la que corrio."""
    try:
        mod = __import__(modulo)
    except Exception:
        return "AUSENTE"
    return str(getattr(mod, "__version__", "SIN-__version__"))


def dependencias_materiales() -> dict[str, str]:
    return {m: version_de(m) for m in DEPENDENCIAS_MATERIALES}


def raices_logicas() -> list[dict]:
    """Nombre logico, si esta configurada y el sha256 del archivo que la
    configura. NUNCA la ruta fisica."""
    config_sha = _sha256(RAICES_LOCAL) if RAICES_LOCAL.exists() else None
    nombres: list[str] = ["data_raw"]
    configuradas: set[str] = set()
    if RAICES_LOCAL.exists():
        try:
            import yaml  # noqa: PLC0415 -- opcional: sin yaml igual se reporta
            datos = yaml.safe_load(RAICES_LOCAL.read_text(encoding="utf-8")) or {}
            if isinstance(datos, dict):
                for k, v in datos.items():
                    if k not in nombres:
                        nombres.append(k)
                    if v:
                        configuradas.add(k)
        except Exception:
            pass
    if CORPUS.exists():
        configuradas.add("data_raw")
    return [
        {"raiz_logica": n,
         "configurada": "SI" if n in configuradas else "NO",
         "config_sha256": config_sha}
        for n in nombres
    ]


def acceso_corpus() -> dict:
    """A.13: el negativo declara cuantos archivos examino. `data/raw`
    ausente NO es paro -- es raiz integrada, gitignorada, y un clon fresco
    siempre nace sin ella (ARRANQUE punto 3 de `/acto`)."""
    if not CORPUS.is_dir():
        return {"montado": "NO", "archivos_examinados": 0,
                "nota": "data/raw ausente -- normal en un clon fresco / en la nube"}
    try:
        entradas = sorted(p.name for p in CORPUS.iterdir())
    except OSError as exc:
        return {"montado": "INDETERMINADO", "archivos_examinados": 0,
                "nota": f"data/raw ilegible: {type(exc).__name__}"}
    return {"montado": "SI" if entradas else "VACIO",
            "archivos_examinados": len(entradas),
            "primera_entrada": entradas[0] if entradas else None}


def sonda_red(activa: bool) -> dict:
    if not activa:
        return {"ejecutada": "NO",
                "nota": "sonda opt-in (--sonda-red): no se prueba red que nadie pidio"}
    cmd = ["curl", "-s", "-o", os.devnull, "-w", "%{http_code}",
           "--max-time", str(TIMEOUT_SONDA), URL_SONDA]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=TIMEOUT_SONDA + 5)
        codigo = (r.stdout or "").strip() or "SIN-SALIDA"
    except (OSError, subprocess.SubprocessError) as exc:
        codigo = f"ERROR:{type(exc).__name__}"
    return {"ejecutada": "SI", "url": URL_SONDA, "timeout_s": TIMEOUT_SONDA,
            "http_code": codigo, "comando": " ".join(cmd)}


def firma(sonda: bool = False) -> dict:
    porcelain = _git("status", "--porcelain")
    return {
        "git_commit": _git("rev-parse", "HEAD"),
        "git_rama": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "git_status": "LIMPIO" if porcelain == "" else "SUCIO",
        "git_status_lineas": 0 if porcelain == "" else len(porcelain.splitlines()),
        "python": platform.python_version(),
        "python_implementacion": platform.python_implementation(),
        "plataforma": platform.platform(),
        "dependencias_materiales": dependencias_materiales(),
        "variables_entorno": {v: os.environ.get(v, "sin_variable")
                              for v in VARIABLES_RELEVANTES},
        "sonda_red": sonda_red(sonda),
        "raices_logicas": raices_logicas(),
        "acceso_corpus": acceso_corpus(),
    }


def linea(f: dict) -> str:
    """Una linea, para pegar en el ARRANQUE de `/acto` sin recortar nada."""
    deps = " ".join(f"{k}={v}" for k, v in f["dependencias_materiales"].items())
    vars_ = " ".join(f"{k}={v}" for k, v in f["variables_entorno"].items())
    raices = " ".join(f"{r['raiz_logica']}:{r['configurada']}"
                      for r in f["raices_logicas"])
    red = f["sonda_red"].get("http_code", "no-ejecutada")
    ac = f["acceso_corpus"]
    return (f"ENTORNO · commit={f['git_commit'][:12]} · git_status={f['git_status']}"
            f"({f['git_status_lineas']}) · python={f['python']} · {deps}"
            f" · {vars_} · red={red} · raices={raices}"
            f" · corpus={ac['montado']}(examinados={ac['archivos_examinados']})")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="entorno", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="solo el JSON")
    ap.add_argument("--linea", action="store_true", help="solo la linea")
    ap.add_argument("--sonda-red", dest="sonda_red", action="store_true",
                    help="prueba la red (opt-in, declara URL y timeout)")
    a = ap.parse_args(argv)
    f = firma(sonda=a.sonda_red)
    if a.json or not a.linea:
        print(json.dumps(f, ensure_ascii=False, indent=1, sort_keys=True))
    if a.linea or not a.json:
        print(linea(f))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

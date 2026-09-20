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
    python3 tools/entorno.py --arranque      # reporte de <=12 lineas para el hook SessionStart

Exit code: 0 siempre que el propio script no reviente. `--arranque` refuerza
esta regla: es la salida de un hook, y un hook que revienta la sesion es
peor que un hook que reporta un fallo como texto y sigue. Cada sonda de
`--arranque` corre en su propio try/except; una que falla no impide que
las demas se reporten.
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


def dependencias_materiales_de(nombres: list[str]) -> dict[str, str]:
    """Versiones resueltas de una lista DECLARADA por el llamador (p. ej. el
    campo `dependencias_materiales` de un `spec.yaml`, ACTO GEN2-E3-1 · P2) --
    no la lista fija de arriba. Un nombre repetido se resuelve una sola vez;
    el orden del resultado no importa, `dependencias_materiales()` ya
    establece el precedente de devolver un dict."""
    return {m: version_de(m) for m in dict.fromkeys(nombres)}


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
    cmd = ["curl", "-sS", "-o", os.devnull,
           "-w", "%{http_code} %{http_connect}",
           "--max-time", str(TIMEOUT_SONDA), URL_SONDA]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=TIMEOUT_SONDA + 5)
        salida = (r.stdout or "").strip()
        codigo = salida.split()[0] if salida else "SIN-SALIDA"
        http_connect = salida.split()[1] if len(salida.split()) > 1 else "000"
    except (OSError, subprocess.SubprocessError) as exc:
        codigo = f"ERROR:{type(exc).__name__}"
        http_connect = "000"
    return {"ejecutada": "SI", "url": URL_SONDA, "timeout_s": TIMEOUT_SONDA,
            "http_code": codigo, "http_connect": http_connect,
            "comando": " ".join(cmd)}


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


def _proba(fn, *args, **kwargs):
    """Corre `fn` y devuelve su resultado, o una linea de error legible --
    nunca deja que una sonda individual tumbe a las demas."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # pragma: no cover -- defensivo por diseno
        return f"ERROR:{type(exc).__name__}:{exc}"[:200]


def _senal_entorno_derivado() -> tuple[str, list[str]]:
    """ENTORNO-DERIVADO + las senales, SIN fusionarlas (una por linea).
    Regla: CAJA exige corpus montado (`data/raw` con >=1 entrada, o una
    raiz configurada); NUBE si hay senal de sesion remota (variable de
    entorno tipica de Claude Code on the web/sandbox) y el corpus no esta
    montado; si ninguna de las dos se cumple con certeza, INDETERMINADO."""
    lineas: list[str] = []
    ac = _proba(acceso_corpus)
    montado = ac.get("montado") if isinstance(ac, dict) else "INDETERMINADO"
    n = ac.get("archivos_examinados", 0) if isinstance(ac, dict) else 0
    lineas.append(f"senal-corpus: montado={montado} archivos_examinados={n}")

    remoto = os.environ.get("CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE", "sin_variable")
    lineas.append(f"senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE={remoto}")

    if montado == "SI":
        derivado = "CAJA"
    elif remoto != "sin_variable":
        derivado = "NUBE"
    else:
        # Sin corpus montado y sin la variable de sesion remota: el docstring
        # del proyecto ya documenta que un clon fresco nace sin `data/raw`
        # tanto en la nube como en la caja, asi que la sola ausencia del
        # corpus no basta para concluir NUBE -- queda INDETERMINADO.
        derivado = "INDETERMINADO"
    return derivado, lineas


def _sonda_red_arranque() -> str:
    """Reusa `sonda_red()` (activa=True) y colapsa su `http_code` en los
    TRES estados no colapsados que pide el hook de arranque."""
    r = _proba(sonda_red, True)
    if not isinstance(r, dict):
        return f"red: SIN-RED ({r})"
    codigo = str(r.get("http_code", ""))
    connect = str(r.get("http_connect", "000"))
    if codigo.isdigit() and 200 <= int(codigo) < 400:
        estado = "PERMITIDA"
    elif connect == "403":
        # El proxy respondio 403 al CONNECT (no la peticion final, que ni
        # se hizo): denegacion por politica de egreso, no red caida.
        estado = "DENEGADA-POR-POLITICA"
    else:
        estado = "SIN-RED"
    return (f"red: {estado} (http_code={codigo}, http_connect={connect}, "
            f"via_proxy={'SI' if os.environ.get('HTTPS_PROXY') else 'NO'})")


def _head_vs_origin_main() -> str:
    r = _proba(_git, "rev-list", "--left-right", "--count", "origin/main...HEAD")
    if isinstance(r, str) and r and not r.startswith("ERROR"):
        partes = r.split()
        if len(partes) == 2:
            return f"head-vs-origin/main: detras={partes[0]} adelante={partes[1]} (sin fetch)"
    return "head-vs-origin/main: NO-DETERMINABLE (no hay origin/main local o el comando fallo)"


def _worktrees_y_ramas() -> list[str]:
    lineas = []
    wt = _proba(_git, "worktree", "list")
    n_wt = len(wt.splitlines()) if isinstance(wt, str) and not wt.startswith("ERROR") else "NO-DETERMINABLE"
    lineas.append(f"worktrees: {n_wt}")

    es_wt = _proba(_git, "rev-parse", "--git-common-dir")
    git_dir = _proba(_git, "rev-parse", "--git-dir")
    if isinstance(es_wt, str) and isinstance(git_dir, str) and not es_wt.startswith("ERROR"):
        lineas.append(f"es-worktree: {'SI' if es_wt != git_dir else 'NO'}")
    else:
        lineas.append("es-worktree: NO-DETERMINABLE")

    ramas = _proba(_git, "for-each-ref", "--format=%(refname:short)", "refs/heads/")
    if isinstance(ramas, str) and not ramas.startswith("ERROR") and ramas:
        propias = 0
        for rama in ramas.splitlines():
            cnt = _proba(_git, "rev-list", "--count", f"origin/main..{rama}")
            if isinstance(cnt, str) and cnt.isdigit() and int(cnt) > 0:
                propias += 1
        lineas.append(f"ramas-locales-con-commits-propios: {propias}/{len(ramas.splitlines())}")
    else:
        lineas.append("ramas-locales-con-commits-propios: NO-DETERMINABLE")

    lineas.append(f"data-raw-en-este-worktree: {'SI' if CORPUS.exists() else 'NO'}")
    return lineas


def arranque() -> str:
    """<=12 lineas de hechos para el hook `SessionStart`. SIEMPRE devuelve
    texto -- nunca levanta -- y `main()` la envuelve para salir 0 pase lo
    que pase."""
    lineas: list[str] = []
    try:
        derivado, senales = _senal_entorno_derivado()
        lineas.append(f"ENTORNO-DERIVADO = {derivado}")
        lineas.extend(senales)
    except Exception as exc:  # pragma: no cover
        lineas.append(f"ENTORNO-DERIVADO = INDETERMINADO (ERROR:{type(exc).__name__})")

    lineas.append(_proba(_sonda_red_arranque))
    lineas.append(_proba(_head_vs_origin_main))
    try:
        lineas.extend(_worktrees_y_ramas())
    except Exception as exc:  # pragma: no cover
        lineas.append(f"worktrees/ramas: ERROR:{type(exc).__name__}")

    lineas.append(
        "SI EL ENCARGO DECLARA OTRO ENTORNO QUE ENTORNO-DERIVADO: "
        "PARA ANTES DE CUALQUIER OTRA COSA."
    )
    return "\n".join(str(l) for l in lineas[:12])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="entorno", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="solo el JSON")
    ap.add_argument("--linea", action="store_true", help="solo la linea")
    ap.add_argument("--sonda-red", dest="sonda_red", action="store_true",
                    help="prueba la red (opt-in, declara URL y timeout)")
    ap.add_argument("--arranque", action="store_true",
                    help="reporte de <=12 lineas para el hook SessionStart; "
                         "siempre sale con codigo 0")
    a = ap.parse_args(argv)
    if a.arranque:
        try:
            print(arranque())
        except Exception as exc:  # pragma: no cover -- ultima red de seguridad
            print(f"ENTORNO-DERIVADO = INDETERMINADO (fallo total: {type(exc).__name__})")
        return 0
    f = firma(sonda=a.sonda_red)
    if a.json or not a.linea:
        print(json.dumps(f, ensure_ascii=False, indent=1, sort_keys=True))
    if a.linea or not a.json:
        print(linea(f))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

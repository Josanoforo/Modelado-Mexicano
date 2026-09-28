#!/usr/bin/env python3
"""⟲ Resumen derivado de la suite completa (ACTO GEN2-TUBERIA-RESUMEN-SUITE-1 · P1).

Defecto que atrapa: el tablero lleva siete cortes diciendo «suite no derivada»
y un puesto que no puede correr la suite reportó 3 FAIL que en CI no existen.
Sin un resumen publicado por el nocturno nadie distingue «la suite falla en
main» de «mi puesto no puede correrla».

No corre la suite: LEE el log que `tests/check.py --baseline` ya escribió en el
job `suite` (la suite corre una sola vez) y emite un TSV `clave<TAB>valor`,
una fila por dato; las listas repiten la clave (`fail_nuevo`, `warn_nuevo`).

    python3 tools/resumen_suite.py construye --log L --commit SHA --duracion-s N \\
        [--run-id ID] [--fecha ISO] > data/derivados/suite-resumen.tsv
    python3 tools/resumen_suite.py lee [RUTA]      # una línea para el tablero

`resultado`: VERDE / ROJO por FAIL nuevos contra la línea base (ADR-534), o
NO-TERMINÓ si el log no trae la línea `LÍNEA BASE:` (la suite murió antes).
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(RAIZ, "data", "derivados", "suite-resumen.tsv")
CABECERA = "# DERIVADO por tools/resumen_suite.py desde el log del job `suite` (nocturno); no se edita a mano"
VIEJO_DIAS = 2  # nocturno diario: más de 2 días sin resumen = el nocturno no está publicando

_RE_BASE = re.compile(r"LÍNEA BASE: (VERDE|ROJO)")
_RE_TOT = re.compile(r"^\s*(\d+) FAIL · (\d+) WARN\s*$")
_RE_WN = re.compile(r"WARN NUEVOS \(estado, no adjudican\): (\d+)")
_RE_ITEM = re.compile(r"^\s*· (T[\w\-]*: .*)$")


def parsea(log: str) -> dict:
    r = {"resultado": "NO-TERMINÓ", "fail_total": "", "warn_total": "",
         "fail_nuevos": 0, "warn_nuevos": 0, "fail_nuevo": [], "warn_nuevo": []}
    seccion = None
    for linea in log.splitlines():
        m = _RE_TOT.match(linea)
        if m:
            r["fail_total"], r["warn_total"] = m.group(1), m.group(2)
            continue
        m = _RE_BASE.search(linea)
        if m:
            r["resultado"] = m.group(1)
            seccion = "fail_nuevo" if m.group(1) == "ROJO" else None
            continue
        m = _RE_WN.search(linea)
        if m:
            seccion = "warn_nuevo"
            continue
        if linea.startswith("─"):
            seccion = None
            continue
        m = _RE_ITEM.match(linea)
        if m and seccion:
            r[seccion].append(m.group(1).strip())
    r["fail_nuevos"] = len(r["fail_nuevo"])
    r["warn_nuevos"] = len(r["warn_nuevo"])
    return r


def construye(log: str, commit: str, duracion_s: str, run_id: str = "", fecha: str = "") -> str:
    r = parsea(log)
    fecha = fecha or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    buf = io.StringIO()
    buf.write(CABECERA + "\n")
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    w.writerow(["clave", "valor"])
    for k, v in (("commit", commit), ("fecha", fecha), ("run_id", run_id),
                 ("resultado", r["resultado"]), ("fail_total", r["fail_total"]),
                 ("warn_total", r["warn_total"]), ("fail_nuevos", r["fail_nuevos"]),
                 ("warn_nuevos", r["warn_nuevos"]), ("duracion_s", duracion_s)):
        w.writerow([k, v])
    for k in ("fail_nuevo", "warn_nuevo"):
        for v in r[k]:
            w.writerow([k, v])
    return buf.getvalue()


def lee(ruta: str = RUTA) -> dict | None:
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as f:
        filas = [l for l in f if not l.startswith("#")]
    d: dict = {"fail_nuevo": [], "warn_nuevo": []}
    for fila in csv.DictReader(filas, delimiter="\t"):
        k, v = fila["clave"], fila["valor"]
        if k in ("fail_nuevo", "warn_nuevo"):
            d[k].append(v)
        else:
            d[k] = v
    return d


def linea(d: dict | None, hoy: _dt.datetime | None = None) -> str:
    if d is None:
        return "suite: sin resumen publicado (data/derivados/suite-resumen.tsv ausente)"
    hoy = hoy or _dt.datetime.now(_dt.timezone.utc)
    try:
        f = _dt.datetime.strptime(d.get("fecha", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except ValueError:
        return f"suite: resumen con fecha ilegible ({d.get('fecha')!r})"
    base = (f"suite {d.get('resultado')} @ {d.get('commit', '')[:8]} · {d.get('fecha')} · "
            f"{d.get('fail_total')} FAIL · {d.get('warn_total')} WARN · "
            f"FAIL nuevos {d.get('fail_nuevos')} · WARN nuevos {d.get('warn_nuevos')} · "
            f"{d.get('duracion_s')} s · run {d.get('run_id') or '?'}")
    if (hoy - f).days > VIEJO_DIAS:
        return f"suite: sin corrida nocturna desde {d.get('fecha')} ({(hoy - f).days} días) · último: {base}"
    return base


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("construye")
    c.add_argument("--log", required=True)
    c.add_argument("--commit", required=True)
    c.add_argument("--duracion-s", required=True)
    c.add_argument("--run-id", default="")
    c.add_argument("--fecha", default="")
    l_ = sub.add_parser("lee")
    l_.add_argument("ruta", nargs="?", default=RUTA)
    a = ap.parse_args(argv)
    if a.cmd == "construye":
        with open(a.log, encoding="utf-8", errors="replace") as f:
            sys.stdout.write(construye(f.read(), a.commit, a.duracion_s, a.run_id, a.fecha))
    else:
        print(linea(lee(a.ruta)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

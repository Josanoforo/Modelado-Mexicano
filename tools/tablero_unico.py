#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tablero_unico.py -- bloques TABLERO-UNICO:CARRILES y TABLERO-UNICO:PENDIENTES del
tablero único (ACTO GEN2-TUBERIA-TABLERO-UNICO-1, 29/sep/2026; firma de mesa 5-bis (b)).

Defecto que atrapa: el programa tenía cinco artefactos de tablero (TABLERO-PROGRAMA.md,
TABLERO-CARRILES.md, docs/tablero.md, docs/tablero-carriles.html y el inventario
PENDIENTES-PROGRAMA-v5.md) y dos de ellos con cifras propias que se desfasaban. A un lector
le costaba saber cuál creer. Ahora los carriles y los pendientes viven en un solo archivo,
entre sus propios marcadores, y los reescribe el mismo comando y el mismo commit [deriva].

Uso (desde la raíz del clon; lo llama `tools/tablero_programa.py --actualiza`):
    python3 tools/tablero_unico.py --stdout carriles      # bloque de carriles
    python3 tools/tablero_unico.py --stdout pendientes    # bloque de pendientes
    python3 tools/tablero_unico.py --actualiza RUTA...    # reescribe los dos bloques en cada RUTA

Ninguna cifra se teclea: carriles = `tools/tablero_carriles.py` (mismo derivar()); firmas =
`forense/firmas-pendientes.tsv`; deuda = `tools/nc_por_clase.py` (derivar(), que no escribe).
No decide nada ni cierra nada; solo muestra de quién es cada cosa.
"""
from __future__ import annotations

import collections
import csv
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_por_clase as NPC  # noqa: E402
import tablero_carriles as TC  # noqa: E402

csv.field_size_limit(sys.maxsize)
RAIZ = TC.RAIZ
MARCAS = {"carriles": ("<!-- TABLERO-UNICO:CARRILES:BEGIN -->", "<!-- TABLERO-UNICO:CARRILES:END -->"),
          "pendientes": ("<!-- TABLERO-UNICO:PENDIENTES:BEGIN -->", "<!-- TABLERO-UNICO:PENDIENTES:END -->")}
DUENO = {"ESPERA-MESA-DECISION": "MESA-DECISION", "ESPERA-MESA-ACCION": "MESA-ACCION",
         "ESPERA-DIRECCION-ENCARGO": "DIRECCION-ENCARGO", "ESPERA-CANAL": "CANAL", "ESPERA-APERTURA": "APERTURA",
         "ESPERA-ADQUISICION": "ADQUISICION", "ESPERA-ACTO-NOMBRADO": "CAJA", "ESPERA-MESA": "MESA",
         "ESPERA-DIRECCION": "DIRECCION", "EN-CURSO": "EN-CURSO", "ESPERA-FIRMA": "FIRMA", "SIN-ASIGNAR": "SIN-ASIGNAR",
         "VENCIDA-CANDIDATA": "VENCIDA-CANDIDATA"}
ORDEN_D = ["MESA-DECISION", "MESA-ACCION", "DIRECCION-ENCARGO", "CANAL", "APERTURA", "ADQUISICION", "CAJA",
           "MESA", "DIRECCION", "FIRMA", "EN-CURSO", "VENCIDA-CANDIDATA", "SIN-ASIGNAR"]
MUEVE = {"MESA-DECISION": "mesa elige una opción de la hoja de decisiones",
         "MESA-ACCION": "mesa hace algo con su identidad (acceso, envío, recibo)",
         "DIRECCION-ENCARGO": "dirección revisa y lanza un encargo ya redactado",
         "CANAL": "que se fusione el `[deriva]` en cola",
         "APERTURA": "que se abra una ola reservada (pre-registro o mesa por escrito, E.6)",
         "ADQUISICION": "que llegue el payload que nombra la solicitud",
         "CAJA": "que caja corra un encargo ya archivado",
         "MESA": "mesa (dueño sin subtipo)", "DIRECCION": "dirección (dueño sin subtipo)",
         "FIRMA": "una firma abierta", "EN-CURSO": "un acto en vuelo",
         "VENCIDA-CANDIDATA": "dictaminar la fila (cerrar por producto o reasignar)", "SIN-ASIGNAR": "asignar dueño"}


def celda(s, n=None) -> str:
    s = re.sub(r"\s+", " ", str(s or "")).replace("|", "/")
    # un «E6» o «M3» suelto copiado de una fila cuenta como rótulo sin serie (T25): punto medio
    s = re.sub(r"(?<![A-Za-z0-9_\-\.])([EM])(-?\d+)(?![\w\-])", r"\1·\2", s)
    return s if n is None or len(s) <= n else s[: n - 1].rstrip() + "…"


def _baja(md: str, niveles: int = 2) -> str:
    """Baja `niveles` los encabezados `#` de un markdown (fuera de bloques de código)."""
    return re.sub(r"(?m)^(#{1,4}) ", lambda m: "#" * (len(m.group(1)) + niveles) + " ", md)


def bloque_carriles(D: dict | None = None) -> str:
    D = D or TC.derivar()
    pre = ("_Derivado con `python3 tools/tablero_carriles.py` (mismo `derivar()`), sin escribir aparte. Un carril es un "
           "report temático del corpus. Los umbrales del semáforo y la precedencia de la siguiente acción viven en un solo "
           "sitio, la cabecera de `tools/tablero_carriles.py`; las versiones del catálogo, las reglas y las familias se "
           "resuelven del puntero `docs/data/catalogo-vigente.json` o de la serie más alta del árbol, y la cadena de "
           "procedencia del pie dice cuáles leyó. Este bloque sustituye a `TABLERO-CARRILES.md` y a su página web._\n")
    return pre + "\n" + _baja(TC.render_md(D)).strip() + "\n"


def _fps() -> list[dict]:
    with open(os.path.join(RAIZ, "forense/firmas-pendientes.tsv"), encoding="utf-8") as f:
        return list(csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t"))


def _hoy() -> str:
    r = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short"], capture_output=True, text=True, cwd=RAIZ)
    return r.stdout.strip()


def bloque_pendientes(D: dict | None = None, npc: dict | None = None) -> str:
    D = D or TC.derivar()
    npc = npc or NPC.derivar()
    F = npc["filas"]
    abiertas = [r for r in _fps() if r["estado"].startswith("ABIERTA")]
    frena = collections.defaultdict(set)
    for c in D["carriles"]:
        for s in c["stoppers"].get("FIRMA", []):
            frena[s["id"]].add(c["carril"][-2:])
    hoy = _hoy()
    por = collections.defaultdict(list)
    for x in F:
        por[DUENO.get(x["clase"], x["clase"])].append(x)
    w = []
    o = w.append
    o("_Derivado con `python3 tools/nc_por_clase.py --json` (`derivar()`, que no escribe) y `forense/firmas-pendientes.tsv`; "
      f"universo de la deuda: {npc['universo']}. La clase de cada fila es la del clasificador, sin reinterpretar. No toca el libro "
      "ni cierra nada. Este bloque sustituye al inventario `PENDIENTES-PROGRAMA` que ya no se publica aparte._\n")

    def plazo(r):
        m = re.search(r"PLAZO (\d{4}-\d{2}-\d{2})", r.get("gatea", ""))
        return m.group(1) if m else ""
    o(f"#### P.1 · Firmas de mesa abiertas: {len(abiertas)}\n")
    o(f"Ordenadas por plazo y después por cuántos carriles frenan. «Vence» se compara con la fecha del commit del corte ({hoy}). "
      "Solo cuentan como freno las firmas que gatean un instrumento, una ola o un payload del núcleo (una firma sobre el "
      "aparato no frena ningún carril).\n")
    o("| firma | qué se firma | plazo | carriles que frena | creada |")
    o("|---|---|---|---|---|")
    for r in sorted(abiertas, key=lambda r: (plazo(r) or "9999", -len(frena.get(r["id"], ())), r["id"])):
        p = plazo(r)
        pl = (f"**{p} · vence**" if p and p <= hoy else p) or "—"
        cs = sorted(frena.get(r["id"], ()))
        o(f"| `{r['id']}` | {celda(r['qué_se_firma'], 150)} | {pl} | {', '.join(cs) if cs else '—'} | {r['creado']} |")
    o("")
    o(f"#### P.2 · Deuda abierta por dueño: {len(F)} filas\n")
    o("| dueño | filas | qué la mueve |")
    o("|---|---:|---|")
    for d in ORDEN_D + sorted(set(por) - set(ORDEN_D)):
        if por.get(d):
            o(f"| {d} | {len(por[d])} | {MUEVE.get(d, '—')} |")
    o(f"| **total** | **{len(F)}** | |\n")
    o("#### P.3 · El detalle, fila por fila, por dueño\n")
    for d in ORDEN_D + sorted(set(por) - set(ORDEN_D)):
        xs = por.get(d)
        if not xs:
            continue
        o(f"**{d} · {len(xs)}**\n")
        o("| id | pieza | qué le falta | evidencia derivada |\n|---|---|---|---|")
        for x in sorted(xs, key=lambda x: x["id"]):
            o(f"| `{x['id']}` | {celda(x.get('pieza'), 100) or '—'} | {celda(x.get('que_le_falta'), 110)} | "
              f"{celda(x.get('evidencia_derivada'), 110) or '—'} |")
        o("")
    return "\n".join(w)


def reemplaza(texto: str, clave: str, cuerpo: str, ruta: str = "") -> str:
    b, e = MARCAS[clave]
    if texto.count(b) != 1 or texto.count(e) != 1 or texto.index(b) > texto.index(e):
        raise SystemExit(f"error: {ruta or 'archivo'} debe traer exactamente un par {b} / {e}")
    i, j = texto.index(b), texto.index(e)
    return texto[: i + len(b)] + "\n" + cuerpo.strip() + "\n" + texto[j:]


def actualiza(rutas: list[str], D: dict | None = None) -> int:
    D = D or TC.derivar()
    cuerpos = {"carriles": bloque_carriles(D), "pendientes": bloque_pendientes(D)}
    for ruta in rutas:
        p = os.path.join(RAIZ, ruta)
        if not os.path.exists(p):
            print(f"error: no existe {ruta}", file=sys.stderr)
            return 1
        t0 = open(p, encoding="utf-8").read()
        t = t0
        for clave, cuerpo in cuerpos.items():
            t = reemplaza(t, clave, cuerpo, ruta)
        if t != t0:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(t)
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--stdout"] and len(argv) == 2 and argv[1] in MARCAS:
        print(bloque_carriles() if argv[1] == "carriles" else bloque_pendientes())
        return 0
    if argv[:1] == ["--actualiza"] and len(argv) > 1:
        return actualiza(argv[1:])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())

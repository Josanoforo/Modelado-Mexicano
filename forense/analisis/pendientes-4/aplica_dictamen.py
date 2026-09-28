#!/usr/bin/env python3
"""aplica_dictamen.py -- ACTO GEN2-PENDIENTES-4: aplica `dictamen-pendientes-4.tsv` sobre
`forense/no-corrido.tsv`, POR LÍNEA (el módulo csv corrompe filas ajenas al reescribir: ver
PENDIENTES-3). Sólo cambia las columnas previstas y lo prueba antes de escribir.

Por fila del dictamen:
  accion=CERRAR -> estado=CERRADA · cerrado_por · fecha_cierre
  accion=DUENO  -> sucesor = `<nuevo_sucesor> · antes: <sucesor viejo LIMPIO>`
                   (el dueño va al PRINCIPIO del campo: A.16, token por prefijo)
LIMPIO = sin el dueño viejo `MESA (fecha) ·` y sin las frases «encargo por escribir» /
«cierre por diseño propuesto»: el «hecho» de P3 exige 0 filas ABIERTA que las contengan, y
un `antes:` que las conserve las reintroduce.
Sólo toca filas que siguen ABIERTA; una fila ya cerrada en main por otro acto se reporta y no
se toca. Idempotente.

    python3 forense/analisis/pendientes-4/aplica_dictamen.py            # dry-run
    python3 forense/analisis/pendientes-4/aplica_dictamen.py --escribe
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
NC = os.path.join(RAIZ, "forense", "no-corrido.tsv")
DICT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictamen-pendientes-4.tsv")
FECHA = "2026-09-28"
FRASES = (r"encargo por escribir", r"cierre por dise[ñn]o propuesto")


def limpia_antes(s):
    """Sucesor viejo sin dueño `MESA (fecha) ·` y sin las frases prohibidas."""
    t = re.sub(r"^MESA \(\d{4}-\d{2}-\d{2}\)\s*·?\s*", "", s.strip())
    t = re.sub(r"^(?:encargo por escribir|cierre por dise[ñn]o propuesto)\s*[:;]?\s*", "", t, flags=re.I)
    for f in FRASES:  # residuo en medio del texto
        t = re.sub(f, "encargo pendiente de redactar" if "encargo" in f else "cierre propuesto", t, flags=re.I)
    return t.strip(" ·")


def main():
    escribe = "--escribe" in sys.argv
    dl = [l for l in open(DICT, encoding="utf-8").read().split("\n") if l.strip()]
    dcab = dl[0].split("\t")
    dic = {}
    for l in dl[1:]:
        r = dict(zip(dcab, l.split("\t")))
        if r["id"] in dic:
            sys.exit(f"id duplicado en dictamen: {r['id']}")
        dic[r["id"]] = r
    original = open(NC, encoding="utf-8").read()
    lineas = original.split("\n")
    cab = lineas[0].split("\t")
    i_est, i_suc, i_cp, i_fc = (cab.index(c) for c in ("estado", "sucesor", "cerrado_por", "fecha_cierre"))
    previstas = {i_est, i_suc, i_cp, i_fc}
    vistos, cerradas, duenos, ajenas, sin_cambio = set(), 0, 0, [], 0
    for n, l in enumerate(lineas[1:], start=1):
        if not l:
            continue
        f = l.split("\t")
        r = dic.get(f[0])
        if r is None:
            continue
        if f[0] in vistos:
            sys.exit(f"id repetido en el libro: {f[0]}")
        vistos.add(f[0])
        if len(f) != len(cab):
            sys.exit(f"{f[0]}: {len(f)} campos, cabecera {len(cab)}")
        if f[i_est] != "ABIERTA":
            ajenas.append(f"{f[0]}={f[i_est]}")
            continue
        antes = list(f)
        if r["accion"] == "CERRAR":
            if not re.search(r"CERRADA \((?:producto|diseño|firma|duplicada): [^)]+\)|SIN-OBJETO \([^)]+\)", r["cerrado_por"]):
                sys.exit(f"{f[0]}: cerrado_por sin forma de dictamen: {r['cerrado_por'][:80]}")
            f[i_est], f[i_cp], f[i_fc] = "CERRADA", r["cerrado_por"], FECHA
            cerradas += 1
        elif r["accion"] == "DUENO":
            if not f[i_suc].startswith(r["nuevo_sucesor"]):
                f[i_suc] = f"{r['nuevo_sucesor']} · antes: {limpia_antes(f[i_suc])}"
            duenos += 1
        elif r["accion"] == "NADA":
            sin_cambio += 1
            continue
        else:
            sys.exit(f"{f[0]}: accion desconocida {r['accion']!r}")
        for c in f:
            if "\t" in c or "\n" in c:
                sys.exit(f"{f[0]}: tab o salto dentro de celda")
        cambiadas = {i for i in range(len(f)) if f[i] != antes[i]}
        if not cambiadas <= previstas:
            sys.exit(f"{f[0]}: cambió una columna no prevista: {[cab[i] for i in cambiadas - previstas]}")
        lineas[n] = "\t".join(f)
    faltan = sorted(set(dic) - vistos)
    print(f"dictamen: {len(dic)} filas · CERRAR {cerradas} · DUENO {duenos} · NADA {sin_cambio} · "
          f"ya no ABIERTA en el libro {len(ajenas)} · ids ausentes {len(faltan)}")
    for a in ajenas:
        print("  no tocada (estado ajeno):", a)
    for a in faltan:
        print("  AUSENTE en el libro:", a)
    if faltan:
        return 1
    nuevo = "\n".join(lineas)
    if len(nuevo.split("\n")) != len(original.split("\n")):
        sys.exit("el número de líneas cambió: abortado")
    if escribe:
        with open(NC, "w", encoding="utf-8", newline="") as fh:
            fh.write(nuevo)
        print("escrito:", os.path.relpath(NC, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())

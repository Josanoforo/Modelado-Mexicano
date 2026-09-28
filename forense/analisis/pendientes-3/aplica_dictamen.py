#!/usr/bin/env python3
"""aplica_dictamen.py -- ACTO GEN2-PENDIENTES-3: aplica `dictamen-pendientes-3.tsv` sobre
`forense/no-corrido.tsv`, POR LÍNEA (el módulo csv corrompe filas ajenas al
reescribir: ver hallazgos de FP29-RECONCILIA y CAJA-REACTIVOS-FD-1).

Por fila del dictamen:
  accion=CERRAR  -> estado=CERRADA · cerrado_por · fecha_cierre
  accion=DUENO   -> sucesor = `<nuevo_sucesor> · antes: <sucesor viejo>`
                    (el dueño va al PRINCIPIO del campo: A.16, token por prefijo)
Sólo toca filas que siguen ABIERTA; una fila ya cerrada en main por otro acto
se reporta y no se toca. Idempotente: un sucesor que ya empieza por el dueño
nuevo no se re-prefija.

    python3 forense/analisis/pendientes-3/aplica_dictamen.py            # dry-run
    python3 forense/analisis/pendientes-3/aplica_dictamen.py --escribe
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
NC = os.path.join(RAIZ, "forense", "no-corrido.tsv")
DICT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictamen-pendientes-3.tsv")
FECHA = "2026-09-28"


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
    texto = open(NC, encoding="utf-8").read()
    lineas = texto.split("\n")
    cab = lineas[0].split("\t")
    i_est, i_suc, i_cp, i_fc = (cab.index(c) for c in ("estado", "sucesor", "cerrado_por", "fecha_cierre"))
    vistos, cerradas, duenos, ajenas = set(), 0, 0, []
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
        if r["accion"] == "CERRAR":
            f[i_est], f[i_cp], f[i_fc] = "CERRADA", r["cerrado_por"], FECHA
            cerradas += 1
        elif r["accion"] == "DUENO":
            if not f[i_suc].startswith(r["nuevo_sucesor"]):
                f[i_suc] = f"{r['nuevo_sucesor']} · antes: {f[i_suc]}"
            duenos += 1
        else:
            sys.exit(f"{f[0]}: accion desconocida {r['accion']!r}")
        for c in f:
            if "\t" in c or "\n" in c:
                sys.exit(f"{f[0]}: tab o salto dentro de celda")
        lineas[n] = "\t".join(f)
    faltan = sorted(set(dic) - vistos)
    print(f"dictamen: {len(dic)} filas · CERRAR {cerradas} · DUENO {duenos} · "
          f"ya no ABIERTA en el libro {len(ajenas)} · ids ausentes {len(faltan)}")
    for a in ajenas:
        print("  no tocada (estado ajeno):", a)
    for a in faltan:
        print("  AUSENTE en el libro:", a)
    if faltan:
        return 1
    if escribe:
        with open(NC, "w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(lineas))
        print("escrito:", os.path.relpath(NC, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())

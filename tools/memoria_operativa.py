#!/usr/bin/env python3
"""T-MEM: regenera los bloques derivados de canon/MEMORIA-OPERATIVA.md.

ACTO GEN2-TUBERIA-CABLEADO-SESIONES-1, P3. Dos derivados, sin tocar las
secciones escritas a mano:

  1. Bloque «Decisiones activas» (entre `<!-- T-MEM:INICIO -->` y
     `<!-- T-MEM:FIN -->`): filas de forense/firmas-pendientes.tsv con estado
     que empieza en FIRMADA y fecha de firma (primer dd/mmm/aaaa de
     `firmada_en`) dentro de VENTANA días del ÚLTIMO CORTE (la fecha de firma
     más reciente del TSV, no el reloj: el bloque es función solo del TSV).
     Se muestran las MAX_FILAS más recientes; el resto se cuenta con el
     comando para listarlas.
  2. forense/analisis/cableado/herramientas.tsv: tools/*.py con la primera
     línea de su docstring (la memoria cabe en 80 líneas; el índice completo
     vive aparte).

Uso:
  python3 tools/memoria_operativa.py --verifica   # lee; falla si difiere (D-23)
  python3 tools/memoria_operativa.py --escribe    # paso explícito (T-MEM de /tramite)
  python3 tools/memoria_operativa.py --lista      # todas las filas de la ventana
"""
import ast
import csv
import datetime
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(RAIZ, "canon", "MEMORIA-OPERATIVA.md")
FIRMAS = os.path.join(RAIZ, "forense", "firmas-pendientes.tsv")
HERR = os.path.join(RAIZ, "forense", "analisis", "cableado", "herramientas.tsv")
INI, FIN = "<!-- T-MEM:INICIO -->", "<!-- T-MEM:FIN -->"
VENTANA, MAX_FILAS, MAX_LINEAS = 14, 12, 80
MESES = {m: i + 1 for i, m in enumerate(
    "ene feb mar abr may jun jul ago sep oct nov dic".split())}
csv.field_size_limit(10 ** 9)


def fecha_firma(texto):
    m = re.search(r"\b(\d{1,2})/([a-z]{3})/(\d{4})", texto or "")
    if not m or m.group(2) not in MESES:
        return None
    return datetime.date(int(m.group(3)), MESES[m.group(2)], int(m.group(1)))


def ventana():
    with open(FIRMAS, encoding="utf-8", newline="") as f:
        filas = [r for r in csv.DictReader(f, delimiter="\t")
                 if (r.get("estado") or "").startswith("FIRMADA")]
    fechadas = [(fecha_firma(r.get("firmada_en")), r) for r in filas]
    fechadas = [(d, r) for d, r in fechadas if d]
    if not fechadas:
        return None, []
    corte = max(d for d, _ in fechadas)
    desde = corte - datetime.timedelta(days=VENTANA)
    sel = [(d, r) for d, r in fechadas if d > desde]
    sel.sort(key=lambda x: (x[0], x[1]["id"]), reverse=True)
    return corte, sel


def corta(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def bloque():
    corte, sel = ventana()
    out = [INI]
    if corte is None:
        out.append("- (sin filas FIRMADA con fecha en firmas-pendientes.tsv)")
    else:
        out.append("- Corte %s · %d FIRMADA en %d días · se muestran %d · todas: "
                   "`python3 tools/memoria_operativa.py --lista`"
                   % (corte.isoformat(), len(sel), VENTANA, min(MAX_FILAS, len(sel))))
        for d, r in sel[:MAX_FILAS]:
            out.append("- %s · %s · %s" % (
                r["id"], corta(r.get("gatea"), 70), d.strftime("%d/%m")))
    out.append(FIN)
    return "\n".join(out)


def herramientas():
    filas = ["herramienta\tdescripcion"]
    d = os.path.join(RAIZ, "tools")
    for n in sorted(os.listdir(d)):
        if not n.endswith(".py"):
            continue
        try:
            doc = ast.get_docstring(ast.parse(open(os.path.join(d, n), encoding="utf-8").read())) or ""
        except (SyntaxError, ValueError, OSError):
            doc = ""
        primera = corta(doc.strip().splitlines()[0] if doc.strip() else "SIN-DOCSTRING", 150)
        filas.append("tools/%s\t%s" % (n, primera.replace("\t", " ")))
    return "\n".join(filas) + "\n"


def memoria_con(bloq):
    t = open(MEM, encoding="utf-8").read()
    i, j = t.index(INI), t.index(FIN) + len(FIN)
    return t[:i] + bloq + t[j:]


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--lista":
        corte, sel = ventana()
        for d, r in sel:
            print("%s\t%s\t%s" % (d.isoformat(), r["id"], corta(r.get("gatea"), 120)))
        return 0
    nueva, herr = memoria_con(bloque()), herramientas()
    if arg == "--escribe":
        open(MEM, "w", encoding="utf-8").write(nueva)
        os.makedirs(os.path.dirname(HERR), exist_ok=True)
        open(HERR, "w", encoding="utf-8").write(herr)
        print("T-MEM: escrito (%d líneas)" % nueva.count("\n"))
        return 0
    if arg == "--verifica":
        fallas = []
        actual = open(MEM, encoding="utf-8").read()
        if actual != nueva:
            fallas.append("bloque derivado difiere de firmas-pendientes.tsv")
        if actual.count("\n") > MAX_LINEAS:
            fallas.append("memoria > %d líneas (%d)" % (MAX_LINEAS, actual.count("\n")))
        if not os.path.exists(HERR) or open(HERR, encoding="utf-8").read() != herr:
            fallas.append("herramientas.tsv difiere de tools/")
        for f in fallas:
            print("FALLA T-MEM: " + f)
        print("T-MEM: %s" % ("VERDE" if not fallas else "ROJO -- corre --escribe"))
        return 1 if fallas else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())

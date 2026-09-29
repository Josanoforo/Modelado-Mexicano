#!/usr/bin/env python3
"""conteos_pendientes_4.py -- ACTO GEN2-PENDIENTES-4 · P4: conteos del libro de NC por comando, para el antes y el
después del acto (ninguna cifra tecleada). Lector CSV (el libro no usa comillas pero el conteo
por línea física ya falló una vez con campos citados: instrucciones §2).

    python3 forense/analisis/pendientes-4/conteos_pendientes_4.py                 # JSON a stdout
    python3 forense/analisis/pendientes-4/conteos_pendientes_4.py --lee <json>    # tabla antes/después vs ese JSON
    python3 forense/analisis/pendientes-4/conteos_pendientes_4.py --lee <json> --intermedio <ref-git>
        # tres columnas: arranque (el JSON) · el libro de esa referencia (p. ej. origin/main, sobre el que se aplicó
        # el acto: otros actos ya lo habían movido) · el árbol de ahora
"""
import csv
import io
import json
import os
import re
import subprocess
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import nc_por_clase as NPC  # noqa: E402

NC = os.path.join(RAIZ, "forense", "no-corrido.tsv")
FRASES = ("encargo por escribir", "cierre por diseño propuesto")


def dueno(s):
    m = re.match(r"^([A-Z][A-Z-]*) \(", (s or "").strip())
    return m.group(1) if m else "(sin token)"


def tipo_cierre(cp):
    m = re.search(r"CERRADA \((producto|diseño|firma|duplicada):|SIN-OBJETO", cp or "")
    return (m.group(1) or "SIN-OBJETO") if m else "(otro)"


def mide():
    with open(NC, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    ab = [r for r in rows if r["estado"] == "ABIERTA"]
    hoy = [r for r in rows if r["estado"].startswith("CERRADA") and "GEN2-PENDIENTES-4" in (r["cerrado_por"] or "")]
    d = NPC.derivar()
    return {
        "filas": len(rows),
        "estado": dict(Counter(r["estado"] for r in rows)),
        "abiertas": len(ab),
        "abiertas_por_dueno": dict(Counter(dueno(r["sucesor"]) for r in ab)),
        "abiertas_por_razon": dict(Counter(re.split(r"[: ·]", r["razon"])[0] for r in ab)),
        "abiertas_con_frase_prohibida": sum(any(fr in r["sucesor"].lower() for fr in FRASES) for r in ab),
        "clase_nc_por_clase": dict(Counter(f["clase"] for f in d["filas"])),
        "cerradas_por_este_acto": len(hoy),
        "cerradas_por_este_acto_por_tipo": dict(Counter(tipo_cierre(r["cerrado_por"]) for r in hoy)),
    }


def mide_ref(ref):
    """Las cifras de dueños del libro tal como está en una referencia de git (sin tocar el árbol)."""
    txt = subprocess.run(["git", "show", f"{ref}:forense/no-corrido.tsv"], cwd=RAIZ, capture_output=True, text=True,
                         check=True).stdout
    rows = list(csv.DictReader(io.StringIO(txt, newline=""), delimiter="\t"))
    ab = [r for r in rows if r["estado"] == "ABIERTA"]
    return {"filas": len(rows), "abiertas": len(ab),
            "abiertas_por_dueno": dict(Counter(dueno(r["sucesor"]) for r in ab)),
            "abiertas_con_frase_prohibida": sum(any(fr in r["sucesor"].lower() for fr in FRASES) for r in ab)}


def main():
    m = mide()
    if "--lee" in sys.argv and "--intermedio" in sys.argv:
        antes = json.load(open(sys.argv[sys.argv.index("--lee") + 1], encoding="utf-8"))
        ref = sys.argv[sys.argv.index("--intermedio") + 1]
        mid = mide_ref(ref)
        print(f"columnas: arranque (JSON) · {ref} · árbol de ahora")
        print(f"abiertas: {antes['abiertas']} · {mid['abiertas']} · {m['abiertas']}")
        print(f"filas del libro: {antes['filas']} · {mid['filas']} · {m['filas']}")
        print(f"con frase prohibida: {antes['abiertas_con_frase_prohibida']} · {mid['abiertas_con_frase_prohibida']} · {m['abiertas_con_frase_prohibida']}")
        print("\nabiertas_por_dueno:")
        for c in sorted(set(antes["abiertas_por_dueno"]) | set(mid["abiertas_por_dueno"]) | set(m["abiertas_por_dueno"])):
            print(f"  {c}: {antes['abiertas_por_dueno'].get(c, 0)} · {mid['abiertas_por_dueno'].get(c, 0)} · {m['abiertas_por_dueno'].get(c, 0)}")
        print(f"\ncerradas por este acto: {m['cerradas_por_este_acto']} {m['cerradas_por_este_acto_por_tipo']}")
        return 0
    if "--lee" in sys.argv:
        antes = json.load(open(sys.argv[sys.argv.index("--lee") + 1], encoding="utf-8"))
        print(f"abiertas: {antes['abiertas']} → {m['abiertas']}")
        for k in ("abiertas_por_dueno", "clase_nc_por_clase"):
            claves = sorted(set(antes[k]) | set(m[k]))
            print(f"\n{k}:")
            for c in claves:
                print(f"  {c}: {antes[k].get(c, 0)} → {m[k].get(c, 0)}")
        print(f"\ncon frase prohibida: {antes['abiertas_con_frase_prohibida']} → {m['abiertas_con_frase_prohibida']}")
        print(f"cerradas por este acto: {m['cerradas_por_este_acto']} {m['cerradas_por_este_acto_por_tipo']}")
        return 0
    print(json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

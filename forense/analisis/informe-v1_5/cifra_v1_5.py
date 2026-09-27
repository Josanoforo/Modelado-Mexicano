#!/usr/bin/env python3
"""Cifras del informe v1.5 (ACTO GEN2-CIERRE-SEMANAL-2), una por clave.

Solo lee artefactos del árbol; no escribe. Sucesor de
`forense/analisis/informe-v1_4/cifra.py` (intacto, E.1): las claves `cat:` leen el
catálogo v1.3. Uso:
    python3 forense/analisis/informe-v1_5/cifra_v1_5.py <clave>
Claves: cat:<clave de conteos-v1_3.json> · cat_origen:<origen_piso> ·
cat_estado:<estado_adopcion> · cat_temporalidad:<PROSPECTIVA|RETROSPECTIVA> · mapa11_dominios · mapa11_dominios_medidos ·
tabla_dominios (imprime la tabla de cobertura por dominio del mapa v1.1) ·
recibo:<recomendacion> · recibo_frase (1 si la frase de §5 está en la nota) ·
vetados_eic (filas de veto de CALC-EIC-HOGARES-2015-0001 en decisiones.tsv) ·
vista_fecha (fecha ISO del último commit que tocó data/corrida0/usos.tsv) ·
familias2027 · legacy_24sep
"""
import csv
import glob
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)
ROOT = pathlib.Path(__file__).resolve().parents[3]
CAT = "canon/catalogo-del-mexicano-v1_3.tsv"
MAPA = "canon/mapa-dominios-v1_1.tsv"
RECIBO = ("forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/"
          "2026-09-27-gen2-recibo-astra6-1--tabla-result-estado-efecto.tsv")
NOTA_RECIBO = "forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/nota-recibo.md"


def lee(p):
    with open(ROOT / p, newline="", encoding="utf-8") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def tabla_dominios() -> str:
    """Una fila por dominio del mapa v1.1: afirmaciones por dictamen y estimadores del catálogo v1.3."""
    mapa, cat = lee(MAPA), Counter(r["dominio"] for r in lee(CAT))
    por = {}
    for m in mapa:
        por.setdefault(m["dominio"], Counter())[m["dictamen"]] += 1
    out = ["| dominio (mapa v1.1) | afirmaciones | medibles en corpus | con adquisición | no medibles por diseño | "
           "estimadores catálogo v1.3 | estado |", "|---|---:|---:|---:|---:|---:|---|"]
    for d in sorted(por):
        c = por[d]
        est = "MEDIDO" if cat[d] else ("MEDIBLE-EN-CORPUS-SIN-CALC" if c["MEDIBLE-EN-CORPUS"] else
                                       "MEDIBLE-CON-ADQUISICIÓN" if c["MEDIBLE-CON-ADQUISICIÓN"] else
                                       "NO-MEDIBLE-POR-DISEÑO")
        out.append(f"| `{d}` | {sum(c.values())} | {c['MEDIBLE-EN-CORPUS']} | {c['MEDIBLE-CON-ADQUISICIÓN']} | "
                   f"{c['NO-MEDIBLE-POR-DISEÑO']} | {cat[d]} | {est} |")
    return "\n".join(out)


def main(clave: str) -> int:
    tipo, _, arg = clave.partition(":")
    if tipo == "cat":
        v = json.loads((ROOT / "forense/analisis/catalogo/v1_3/conteos-v1_3.json").read_text())[arg]
    elif tipo == "cat_origen":
        v = sum(r["origen_piso"] == arg for r in lee(CAT))
    elif tipo == "cat_temporalidad":
        v = sum(r["temporalidad"] == arg for r in lee(CAT))
    elif tipo == "cat_estado":
        v = sum(r["estado_adopcion"] == arg for r in lee(CAT))
    elif tipo == "mapa11_dominios":
        v = len({r["dominio"] for r in lee(MAPA)})
    elif tipo == "mapa11_dominios_medidos":
        v = len({r["dominio"] for r in lee(MAPA)} & {r["dominio"] for r in lee(CAT)})
    elif tipo == "tabla_dominios":
        v = tabla_dominios()
    elif tipo == "recibo":
        v = sum(r["recomendacion"] == arg for r in lee(RECIBO))
    elif tipo == "recibo_frase":
        v = int("«En el primer lote de validación ciega (ENDIREH 2011 y 2021" in (ROOT / NOTA_RECIBO).read_text())
    elif tipo == "vetados_eic":
        v = sum(r["objeto"].startswith("RESULT-EIC-HOGARES-2015-") and
                r["decision"].startswith("adopcion=VETADA-POR-DECISION") for r in lee("data/corrida0/decisiones.tsv"))
    elif tipo == "vista_fecha":
        v = subprocess.run(["git", "log", "-1", "--format=%cs %h", "--", "data/corrida0/usos.tsv"], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.strip()
    elif tipo == "familias2027":
        v = len({re.sub(r"-spec-v1_.*", "", p) for p in glob.glob(str(ROOT / "forense/prereg-caja/FAMILIA-2027-*-spec-v1_*.md"))})
    elif tipo == "legacy_24sep":
        t = (ROOT / "forense/notas/2026-09-24-GEN2-ADOPCION-BLOQUE-Y-PINES-2-cierre.md").read_text()
        v = int(re.search(r"\| `dependencias_numericas_legacy_activas` \| (\d+) \|", t).group(1))
    else:
        raise SystemExit(f"clave desconocida: {clave}")
    print(v)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

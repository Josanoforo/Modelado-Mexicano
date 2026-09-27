#!/usr/bin/env python3
"""Revisión por NOMBRE de las equivalencias NO-ENCONTRADO del mapa v1.1 · ACTO GEN2-COLA-COMPLETA-1 (P-C).

El derivador del mapa (`forense/analisis/dominios/redictamina_v1_1.py`) casa el texto de
instrumento con el catálogo sólo por SIGLA exacta o por un alias declarado. Una afirmación que
cita «Encuesta Nacional de Ocupación y Empleo» sin escribir «ENOE» sale NO-ENCONTRADO aunque el
programa esté en corpus. Esta revisión hace la segunda pasada, por comando:

  1. nombres largos de cada programa del catálogo de CORPUS-COMPLETO
     (`forense/analisis/corpus-completo/catalogo-v1_0.tsv`, `titulo` antes de « · », sin año ni
     paréntesis, sin el sufijo de población tras « , »), normalizados (minúsculas, sin acentos);
  2. alias en inglés/abreviados declarados abajo (lista cerrada, una línea por alias);
  3. sólo programas con olas en `tabla-final-v1_0.tsv` (los que pueden medirse).

Cada fila NO-ENCONTRADO sale con una CLASE:
  CANDIDATO-POR-NOMBRE  — el texto contiene el nombre largo o un alias de un programa en corpus;
                          la adjudicación (casa / no casa) es humana y vive en
                          `equivalencias-revisadas-v1_0.tsv` (este acto), no aquí.
  SIN-PROGRAMA          — ningún nombre ni alias del catálogo: documento, paper, informe
                          internacional, registro administrativo o fuente no identificada; queda
                          con su texto (encargo §1 (c)).

    python3 tools/dominios/cola-completa/revisa_no_encontrado.py            # escribe
    python3 tools/dominios/cola-completa/revisa_no_encontrado.py --verifica # byte a byte
"""
from __future__ import annotations

import csv
import io
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EQ = ROOT / "forense/analisis/dominios/equivalencias-v1_1.tsv"
CATALOGO = ROOT / "forense/analisis/corpus-completo/catalogo-v1_0.tsv"
TABLA = ROOT / "forense/analisis/corpus-completo/tabla-final-v1_0.tsv"
OUT = Path(__file__).resolve().parent / "no-encontrado-revision-v1_0.tsv"

# Alias declarados (texto normalizado → programa). Sólo nombres que el catálogo no trae en
# español o que los reports escriben abreviados. Nada de siglas: las siglas ya las casó el
# derivador.
ALIAS = {
    "encuesta nacional de consumo de drogas": "ENCODAT",
    "encuesta nacional de seguridad publica urbana": "ENSU",
    "encuesta nacional de calidad e impacto gubernamental": "ENCIG",
    "encuesta nacional de inclusion financiera": "ENIF",
    "encuesta nacional sobre la dinamica de las relaciones en los hogares": "ENDIREH",
    "encuesta nacional sobre disponibilidad y uso de tecnologias": "ENDUTIH",
    "encuesta nacional sobre diversidad sexual": "ENDISEG",
    "encuesta nacional sobre discriminacion": "ENADIS",
    "encuesta nacional de bienestar autorreportado": "ENBIARE",
    "modulo de movilidad social intergeneracional": "MMSI",
    "encuesta nacional de salud y nutricion": "ENSANUT",
    "encuesta nacional de la dinamica demografica": "ENADID",
    "encuesta nacional de ocupacion y empleo": "ENOE",
    "encuesta nacional de ingresos y gastos": "ENIGH",
    "encuesta nacional sobre uso del tiempo": "ENUT",
    "encuesta nacional de victimizacion": "ENVIPE",
    "encuesta nacional de salud y envejecimiento": "ENASEM",
    "mexican health and aging study": "ENASEM",
    "censo de poblacion y vivienda": "CCPV",
    "censos de poblacion y vivienda": "CCPV",
    "censo general de poblacion": "CCPV",
    "encuesta intercensal": "INTERCENSAL",
    "consejo nacional de evaluacion": "CONEVAL",
    "comision nacional bancaria": "CNBV",
    "global attitudes": "PEW",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def lee(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")), delimiter="\t"))


def nombres() -> dict[str, str]:
    """nombre normalizado → programa, sólo programas con olas en la tabla final."""
    con_olas = {r["programa"] for r in lee(TABLA)
                if (r["olas_adquiridas_por_este_acto"] + r["olas_ya_en_corpus"]).strip()}
    out: dict[str, str] = {}
    for r in lee(CATALOGO):
        if r["programa"] not in con_olas:
            continue
        t = r["titulo"].split(" · ")[0]
        t = re.sub(r"\(.*?\)", "", t)
        t = re.sub(r"\b(?:19|20)\d\d\b", "", t)
        t = norm(t).split(" , ")[0].strip(" .,-")
        if len(t) >= 20:  # nombres cortos o vacíos casarían con cualquier cosa
            out[t] = r["programa"]
    for a, p in ALIAS.items():
        if p in con_olas:
            out[a] = p
    return out


def main(verifica: bool) -> int:
    nom = nombres()
    filas = []
    for r in lee(EQ):
        if r["programa_id"] != "NO-ENCONTRADO":
            continue
        t = norm(r["instrumento_texto"])
        hits = sorted({(t.find(k), p, k) for k, p in nom.items() if k in t})
        progs, vistos = [], set()
        for _, p, k in hits:
            if p not in vistos:
                vistos.add(p)
                progs.append((p, k))
        filas.append({
            "id_afirmacion": r["id_afirmacion"],
            "clase": "CANDIDATO-POR-NOMBRE" if progs else "SIN-PROGRAMA",
            "programa_candidato": ";".join(p for p, _ in progs),
            "casado_por_nombre": ";".join(k for _, k in progs),
            "instrumento_texto": r["instrumento_texto"],
        })
    buf = io.StringIO()
    buf.write("# GENERADO por tools/dominios/cola-completa/revisa_no_encontrado.py — no editar\n")
    w = csv.DictWriter(buf, list(filas[0].keys()), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(filas)
    txt = buf.getvalue()
    c = Counter(f["clase"] for f in filas)
    por_prog = Counter(p for f in filas for p in f["programa_candidato"].split(";") if p)
    print("NO-ENCONTRADO revisadas:", len(filas), dict(c))
    print("candidatos por programa:", dict(sorted(por_prog.items())))
    if verifica:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == txt
        print(("COINCIDE " if ok else "DIFIERE  ") + str(OUT.relative_to(ROOT)))
        return 0 if ok else 1
    OUT.write_text(txt, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifica" in sys.argv))

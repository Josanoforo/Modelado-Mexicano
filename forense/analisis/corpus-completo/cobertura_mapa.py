#!/usr/bin/env python3
"""ACTO GEN2-CORPUS-COMPLETO-1 · P3 · ¿qué afirmación ADQUIRIR del mapa tiene ya su instrumento?

Entradas (versionadas): forense/analisis/dominios/hoja-adquisicion-derivada-v1_0.tsv (filas
estado_hoja=ADQUIRIR, derivadas por ensambla_mapa.py), el registro de la cola
(data/curacion-registro/cola-adquisicion-registro.tsv: filas OBTENIDO de cualquier acto) y el
catálogo (programas y olas; sus filas en_manifiesto=SI cuentan como ola ya en corpus). Regla, sobre `instrumento_ola` de la afirmación (no sobre pieza_o_razon, que
nombra alternativas descartadas: mención, no uso):

- se buscan los programas del catálogo con su patrón (PATRON_MAPA de catalogo.py, sin distinguir
  mayúsculas, o la sigla exacta)
  y los años 19xx/20xx citados;
- INSTRUMENTO-Y-OLA-EN-CORPUS: algún programa citado tiene fila OBTENIDO en la cola para un
  año citado;
- INSTRUMENTO-EN-CORPUS-OLA-DISTINTA: el programa está OBTENIDO, pero no en el año citado (o
  la afirmación no cita año);
- SIN-INSTRUMENTO-EN-CORPUS: ningún programa del catálogo citado, u ninguno OBTENIDO.

Salida: cobertura-mapa-v1_0.tsv (una fila por afirmación ADQUIRIR). La lee ensambla_mapa.py
para la columna `instrumento_en_corpus` de la hoja (el mapa se mueve por derivador, nunca a mano).
Uso: python3 cobertura_mapa.py [--verifica]
"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "forense/analisis/corpus-completo"
sys.path.insert(0, str(D))
sys.path.insert(0, str(ROOT / "tools" / "curador_registro"))
from catalogo import PATRON_MAPA  # noqa: E402
from tsv_crudo import leer_dicts  # noqa: E402

HOJA = ROOT / "forense/analisis/dominios/hoja-adquisicion-derivada-v1_0.tsv"
REGISTRO = ROOT / "data/curacion-registro/cola-adquisicion-registro.tsv"
SALIDA = D / "cobertura-mapa-v1_0.tsv"
# siglas de 3 letras o palabras comunes que casarían texto libre por accidente
AMBIGUAS = {"SALUD", "INVESTIGACION", "ACCIDENTES", "MORTALIDAD", "NATALIDAD", "EMPLEO", "VIVIENDA",
            "EDUCACION", "MUSEOS", "CE", "EMS"}


def sin_acentos(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def deriva() -> str:
    csv.field_size_limit(10**9)
    with HOJA.open(encoding="utf-8", newline="") as f:
        hoja = [r for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                if r["estado_hoja"] == "ADQUIRIR"]
    obtenido = defaultdict(set)  # PROGRAMA -> {ola}
    for r in leer_dicts(REGISTRO):
        if r["estado_A4A5"].split("(")[0] != "OBTENIDO":
            continue
        m = re.match(r"(.+?)_((?:19|20)\d\d\S*)$", r["fuente_canonica"])
        if m:
            obtenido[m.group(1).upper()].add(m.group(2)[:4])
    # olas que ya estaban en el manifiesto antes del acto (catálogo en_manifiesto=SI)
    cat = (D / "catalogo-v1_0.tsv").read_text(encoding="utf-8").splitlines()
    cab = cat[1].split("\t")
    for l in cat[2:]:
        c = dict(zip(cab, l.split("\t")))
        if c["en_manifiesto"] == "SI" and re.match(r"(19|20)\d\d", c["ola"]):
            obtenido[c["programa"].upper()].add(c["ola"][:4])
    patrones = {}
    for p in obtenido:
        if p in AMBIGUAS or len(p) < 3:
            continue
        # patrón declarado o nombre de >=5 letras: sin distinguir mayúsculas («Latinobarometro»);
        # sigla corta: exacta (ENE ≠ «ene»ro)
        if p.lower() in PATRON_MAPA:
            patrones[p] = re.compile(PATRON_MAPA[p.lower()], re.I)
        else:
            patrones[p] = re.compile(rf"\b{re.escape(p)}\b", re.I if len(p) >= 5 else 0)
    out = ["id_afirmacion\tinstrumento_en_corpus\tprogramas_citados\tolas_citadas\tolas_en_corpus"]
    for r in hoja:
        texto = sin_acentos(r["instrumento_ola"])  # la pieza cita alternativas «que no sustituyen»: mención, no uso
        progs = sorted(p for p, rx in patrones.items() if rx.search(texto))
        anios = sorted(set(re.findall(r"(?<!\d)(?:19|20)\d\d(?!\d)", texto)))  # «CPV2020»
        en = sorted({f"{p}_{a}" for p in progs for a in anios if a in obtenido[p]})
        if en:
            estado = "INSTRUMENTO-Y-OLA-EN-CORPUS"
        elif progs:
            estado = "INSTRUMENTO-EN-CORPUS-OLA-DISTINTA"
        else:
            estado = "SIN-INSTRUMENTO-EN-CORPUS"
        out.append("\t".join([r["id_afirmacion"], estado, ";".join(progs), ";".join(anios), ";".join(en)]))
    return "\n".join(out) + "\n"


def main() -> int:
    texto = deriva()
    if "--verifica" in sys.argv:
        ok = SALIDA.exists() and SALIDA.read_text(encoding="utf-8") == texto
        print("COINCIDE" if ok else "DIFIERE")
        return 0 if ok else 1
    SALIDA.write_text(texto, encoding="utf-8")
    from collections import Counter
    print(Counter(l.split("\t")[1] for l in texto.splitlines()[1:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

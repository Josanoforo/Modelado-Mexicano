"""Censa publicación del último piso por conducta desde el canon sellado."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/analisis/region"
FIELDS = ("instrumento", "conducta", "ola_ultima", "nivel_geografico",
          "esperadas", "publicables", "suprimidas_n", "otros_estados", "alcance")


def genera():
    with (ROOT / "canon/eje-regional-v1_0.tsv").open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t")
                if r["naturaleza_estimacion"].startswith("IC-DE-DISEÑO")]
    latest = {}
    for r in rows:
        k = (r["instrumento"], r["conducta"])
        latest[k] = max(latest.get(k, ""), r["ola"])
    out = []
    for (inst, conducta), year in sorted(latest.items()):
        group = [r for r in rows if (r["instrumento"], r["conducta"], r["ola"]) ==
                 (inst, conducta, year)]
        levels = {r["nivel_geografico"] for r in group}
        if len(levels) != 1:
            raise ValueError(f"nivel ambiguo: {inst}:{conducta}")
        geos = {r["geografia_codigo"] for r in group}
        if len(geos) != len(group):
            raise ValueError(f"geografías duplicadas: {inst}:{conducta}")
        c = Counter(r["estado_publicacion"] for r in group)
        other = sum(v for k,v in c.items() if k not in ("PUBLICABLE", "SUPRIMIDA-N"))
        out.append(dict(zip(FIELDS, (inst, conducta, year, next(iter(levels)), len(group),
            c["PUBLICABLE"], c["SUPRIMIDA-N"], other,
            "última ola medida de esta conducta; no denominador del catálogo general"))))
    with (OUT / "cobertura-celdas-v1_0.tsv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(out)
    with (OUT / "alcance-u1-v1_0.tsv").open(newline="", encoding="utf-8") as f:
        u1 = list(csv.DictReader(f, delimiter="\t"))
    states = Counter(r["estado_regional_u5"] for r in u1)
    lines = ["# Cobertura de celdas regionales medidas · RETROSPECTIVA", "",
        "Generado por `python3 tools/astra/region/cobertura.py` desde el canon y el snapshot "
        "U1 fijado en `3d8e82fb`. La tabla TSV enumera **todas** las geografías esperadas de "
        "la última ola medida por conducta; la suma publicable + suprimida + otros = esperadas. "
        "No interpreta una supresión como cero.", "",
        f"Identidades U1 dictaminadas: {len(u1)}. De ellas, {states['MEDIDO-REGION']} tienen "
        "piso regional, una identidad de seguro tiene 128/128 celdas medidas pero suprimidas "
        "por R2, cuatro reglas de ejes tienen conducta base medida sin extender sus cruces a "
        "región, y 21 son celdas de interacción, no conductas adicionales. Las 37 identidades "
        "no son 37 conductas independientes.", "",
        "| Instrumento | Conducta | Última ola | Publicables / esperadas | SUPRIMIDA-N |",
        "|---|---|---:|---:|---:|"]
    for r in out:
        lines.append(f"| {r['instrumento']} | `{r['conducta']}` | {r['ola_ultima']} | "
                     f"{r['publicables']}/{r['esperadas']} | {r['suprimidas_n']} |")
    lines += ["", "El denominador de esta tabla son **celdas de conductas efectivamente medidas "
              "en su última ola**, no todas las posibles interacciones del catálogo. "
              "Los cruces U1 edad/sexo/escolaridad o interacción no se transforman en "
              "región×eje sin una spec propia. La tabla deja explícito ese límite; "
              "no declara cobertura total del catálogo general ni una cifra de sesgo rural, "
              "indígena o popular. ENCIG cubre solo su marco urbano; ENIF publica región "
              "oficial sin estados; ENVIPE usa residencia, no lugar del delito.", ""]
    (OUT / "cobertura-celdas-v1_0.md").write_text("\n".join(lines), encoding="utf-8")
    print(len(out), sum(int(r["esperadas"]) for r in out),
          sum(int(r["publicables"]) for r in out))


if __name__ == "__main__":
    genera()

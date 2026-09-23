"""Compara retrospectivamente pisos regionales sellados, sin reabrir microdatos."""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SERIES = {
    "ENVIPE:evade_norma_envipe2025": [(2023, "CALC-REGION-HIST-ENVIPE-2023-0001"),
                                       (2024, "CALC-REGION-ENVIPE-2024-0001"),
                                       (2025, "CALC-REGION-HIST-ENVIPE-2025-0001")],
    "ENCIG:canal_digital_luz": [(2017, "CALC-REGION-HIST-ENCIG-2017-0001"),
                                (2019, "CALC-REGION-HIST-ENCIG-2019-0001"),
                                (2021, "CALC-REGION-HIST-ENCIG-2021-0001"),
                                (2023, "CALC-REGION-ENCIG-2023-0001"),
                                (2025, "CALC-REGION-ENCIG-CONSUMIDORES-2025-0001")],
    "ENIF:informal_cualquiera_18a70": [(2018, "CALC-REGION-HIST-ENIF-2018-0001"),
                                        (2021, "CALC-REGION-HIST-ENIF-2021-0001"),
                                        (2024, "CALC-REGION-HIST-ENIF-2024-0001")],
}
PREF_EXPLICITO = {
    "CALC-REGION-ENCIG-CONSUMIDORES-2025-0001":
        "RESULT-REGION-ENCIG-2025-adopta_encig2025_luz-JSON",
}
FIELDS = ("instrumento", "conducta", "geografia_codigo", "ola_piso", "ola_observada",
          "piso_punto", "piso_ic95_inf", "piso_ic95_sup", "observado_punto",
          "categoria", "calc_piso", "calc_observado", "naturaleza", "temporalidad")


def _filas(calc):
    p = ROOT / "data/corrida0" / calc / "resultados.json"
    r = json.loads(p.read_text(encoding="utf-8"))["resultados"]
    key = PREF_EXPLICITO.get(calc)
    if key is None:
        candidatos = [k for k in r if k.endswith("-JSON")]
        if len(candidatos) != 1:
            raise ValueError(f"RESULT JSON ambiguo: {calc}")
        key = candidatos[0]
    return {f["geografia"]: f for f in json.loads(r[key])["filas"]}


def _wilson(x, n):
    if n == 0:
        return None, None
    z = 1.959963984540054
    p = x / n
    d = 1 + z*z/n
    a = (p + z*z/(2*n))/d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return a-h, a+h


def genera():
    rows = []
    for nombre, serie in SERIES.items():
        instrumento, conducta = nombre.split(":", 1)
        for (ola0, calc0), (ola1, calc1) in zip(serie, serie[1:]):
            antes, despues = _filas(calc0), _filas(calc1)
            if set(antes) != set(despues):
                raise ValueError(f"geografías incompatibles: {calc0}, {calc1}")
            for geo in sorted(antes):
                a, b = antes[geo], despues[geo]
                if a["estado"] != "PUBLICABLE" or b["estado"] != "PUBLICABLE":
                    categoria = "SIN-COMPARABILIDAD"
                elif a["ic_inf"] <= b["punto"] <= a["ic_sup"]:
                    categoria = "DENTRO-IC-MUESTRAL-ANTERIOR"
                else:
                    categoria = "FUERA-IC-MUESTRAL-ANTERIOR"
                rows.append(dict(zip(FIELDS, (instrumento, conducta, geo, ola0, ola1,
                    a["punto"], a["ic_inf"], a["ic_sup"], b["punto"], categoria,
                    calc0, calc1, "comparación descriptiva de IC de diseño; sin IC predictivo calibrado",
                    "RETROSPECTIVA"))))
    out = ROOT / "forense/analisis/region"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "mapa-estabilidad-v1_0.tsv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    lines = ["# Mapa descriptivo regional · RETROSPECTIVA", "",
             "Generado por `python3 tools/astra/region/mapa.py` desde los `resultados.json` sellados "
             "identificados en cada fila del TSV. Evento: punto de la ola observada dentro del IC95 "
             "de diseño de la ola anterior. El intervalo anterior no es predictivo calibrado; "
             "esta comparación no demuestra estabilidad ni cambio sostenido.", "",
             "| Serie | Transición | Dentro / comparables | Wilson 95 % descriptivo |",
             "|---|---:|---:|---:|"]
    grupos = sorted({(r["instrumento"], r["conducta"], r["ola_piso"], r["ola_observada"]) for r in rows})
    for inst, conducta, t0, t1 in grupos:
        rr = [r for r in rows if (r["instrumento"], r["conducta"], r["ola_piso"], r["ola_observada"]) == (inst, conducta, t0, t1)]
        c = Counter(r["categoria"] for r in rr)
        n = c["DENTRO-IC-MUESTRAL-ANTERIOR"] + c["FUERA-IC-MUESTRAL-ANTERIOR"]
        lo, hi = _wilson(c["DENTRO-IC-MUESTRAL-ANTERIOR"], n)
        intervalo = f"[{lo:.3f}, {hi:.3f}]" if lo is not None else "no estimable"
        lines.append(f"| {inst} {conducta} | {t0}→{t1} | {c['DENTRO-IC-MUESTRAL-ANTERIOR']}/{n} | {intervalo} |")
    lines += ["", "Wilson supone eventos Bernoulli independientes entre geografías. El diseño "
              "compartido, las regiones ENIF y la repetición de entidades entre transiciones "
              "pueden violar ese supuesto; por ello el intervalo es solo una descripción "
              "binomial condicional, no un IC de diseño ni una cobertura por conglomerado válida. "
              "No se dispone aquí de evaluación temporal calibrada libre de fuga ni de un número "
              "de transiciones independientes suficiente para inferir persistencia regional. "
              "Los 32 estados no se reinterpretan como UPM; las seis regiones ENIF tampoco.", "",
              "No se aplica corrección de multiplicidad: ninguna categoría individual se presenta "
              "como hallazgo simultáneo. El mapa completo incluye SIN-COMPARABILIDAD si una "
              "de las dos olas tiene publicación suprimida.", ""]
    (out / "mapa-estabilidad-v1_0.md").write_text("\n".join(lines), encoding="utf-8")
    print(len(rows), dict(Counter(r["categoria"] for r in rows)))


if __name__ == "__main__":
    genera()

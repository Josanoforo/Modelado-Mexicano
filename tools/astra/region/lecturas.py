"""Escribe lecturas por conducta usando solo tablas regionales generadas."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/analisis/region/lecturas-regionales-v1_0.md"


def _read(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def genera():
    cobertura = _read("forense/analisis/region/cobertura-celdas-v1_0.tsv")
    mapa = _read("forense/analisis/region/mapa-estabilidad-v1_0.tsv")
    by_series = defaultdict(list)
    for r in mapa:
        by_series[(r["instrumento"], r["conducta"])].append(r)
    lines = ["# Lecturas regionales por conducta · RETROSPECTIVA", "",
        "Generado por `python3 tools/astra/region/lecturas.py` desde el censo de última "
        "ola y el mapa muestral. Cada conducta se consulta por `instrumento` y `conducta` en "
        "`canon/eje-regional-v1_0.tsv`; los RESULT y hashes de cada cifra están allí. "
        "Todas las fuentes son encuestas mexicanas ENVIPE, ENCIG o ENIF. Este documento "
        "no asigna tier de adopción ni incorpora el eje al marcador.", ""]
    for r in cobertura:
        inst, conducta = r["instrumento"], r["conducta"]
        alias = "canal_digital_luz" if (inst, conducta) == ("ENCIG", "adopta_encig2025_luz") else conducta
        serie = by_series.get((inst, alias), [])
        comp = [x for x in serie if x["categoria"] != "SIN-COMPARABILIDAD"]
        ultima = max((x["ola_observada"] for x in comp), default=None)
        final = [x for x in comp if x["ola_observada"] == ultima] if ultima else []
        if final:
            up = sum(float(x["observado_punto"]) > float(x["piso_punto"]) for x in final)
            down = sum(float(x["observado_punto"]) < float(x["piso_punto"]) for x in final)
            equal = len(final)-up-down
            change = (f"En la transición {final[0]['ola_piso']}→{ultima}, el punto sube en {up}, "
                      f"baja en {down} y empata en {equal} geografías comparables. "
                      "Es una diferencia descriptiva, sin prueba de cambio sostenido.")
        else:
            change = ("**SIN-HISTORIA-PARA-CALIBRAR en este producto.** Solo hay último "
                      "piso comparable o las celdas están suprimidas; no se afirma "
                      "transición temporal de esta conducta ni se fabrica IC predictivo.")
        level = "entidades de residencia" if r["nivel_geografico"] == "ENTIDAD" else "regiones oficiales ENIF"
        alias_note = (" La serie comparable continúa en 2025 bajo `adopta_encig2025_luz`; "
                      "no se cuentan ambos nombres como dos desenlaces."
                      if (inst, conducta) == ("ENCIG", "canal_digital_luz") else "")
        lines += [f"## {inst} · `{conducta}`", "",
            f"Consultar la última ola {r['ola_ultima']} en {level}: "
            f"{r['publicables']}/{r['esperadas']} celdas con punto e IC de diseño; "
            f"{r['suprimidas_n']} SUPRIMIDA-N y {r['otros_estados']} de otro estado. "
            "La unidad, el universo y el CALC están en cada fila del canon." + alias_note + " "
            "Fuente: encuesta mexicana; tier regional: exploratorio, `adopta: NO`.", "",
            change, "",
            "**Límite y falsador:** una discrepancia de codificación, universo, factor, "
            "geografía o reproducción del RESULT sellado invalidaría esta lectura. "
            "El nivel regional puede reflejar oferta e instituciones; no identifica "
            "preferencias culturales, clase, pertenencia indígena ni causalidad. "
            "No se promete detectar cambios futuros.", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(len(cobertura), len(lines))


if __name__ == "__main__":
    genera()

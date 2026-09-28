"""GEN2-CORPUS-LICENCIAS-1 · ningún payload NUEVO entra al manifiesto sin licencia.

Defecto que atrapa: 554 entradas registradas sin campo `licencia` y 29 con
«no declarada por la fuente» (626 en total al 27/sep), requisito I2 para ir
públicos. La línea base congelada (sin-licencia-base.tsv) solo puede
encoger: un id sin licencia fuera de ella es FAIL.
"""
import csv
import pathlib

import yaml

RAIZ = pathlib.Path(__file__).resolve().parents[1]
BASE = RAIZ / "forense/analisis/corpus-licencias-1/sin-licencia-base.tsv"


def _sin_licencia(v):
    v = str(v or "").strip().lower()
    return v in ("", "none") or "no declarada" in v


def test_ningun_payload_nuevo_sin_licencia():
    es = yaml.safe_load((RAIZ / "data/manifiesto.yaml").read_text(encoding="utf-8"))
    with BASE.open(encoding="utf-8", newline="") as f:
        base = {r["id"] for r in csv.DictReader(f, delimiter="\t")}
    nuevos = sorted(e["id"] for e in es if _sin_licencia(e.get("licencia")) and e["id"] not in base)
    assert not nuevos, f"payloads sin licencia fuera de la línea base: {nuevos[:20]}"


def test_una_sola_grafia_inegi():
    txt = (RAIZ / "data/manifiesto.yaml").read_text(encoding="utf-8")
    assert "licencia: Terminos de Libre Uso de la Informacion del INEGI" not in txt


def test_grafias_puras_inegi_unificadas():
    """GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1: 22 grafías de la misma referencia INEGI → una cadena."""
    es = yaml.safe_load((RAIZ / "data/manifiesto.yaml").read_text(encoding="utf-8"))
    viejas = {"Términos de libre uso de la información del INEGI",
              "Términos de Libre Uso de la Información del INEGI",
              "Términos de Libre Uso de la Información del INEGI: https://www.inegi.org.mx/inegi/terminos.html",
              "Términos de uso INEGI"}
    malas = [e["id"] for e in es if "inegi.org.mx" in str(e.get("url_origen") or "")
             and str(e.get("licencia") or "").strip() in viejas]
    assert not malas, malas[:20]

"""Tests de `tools/benchmark.py` (ACTO GEN2-PRODUCTO-CONSULTA-1).

Defecto que atrapan: una consulta que devuelva una cifra distinta del RESULT
sellado que cita (PARO c del encargo), y un export de Pages que se separe del
catálogo vigente. El de equivalencia recorre el catálogo entero.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import benchmark as b  # noqa: E402


def test_equivalencia_catalogo_entero_contra_result_sellado():
    ver, filas = b.catalogo()
    malas = []
    for f in filas:
        s = b.resuelve_sellado(f)
        if not b.iguales(s["punto"], f["punto"]):
            malas.append((f["llave"], "punto"))
        if s["ic95"] is not None:
            for k, v in zip(("ic95_inf", "ic95_sup"), s["ic95"]):
                if not b.iguales(v, f[k]):
                    malas.append((f["llave"], k))
    assert not malas, f"{len(malas)} filas de {ver} no reproducen su RESULT: {malas[:5]}"
    assert len(filas) > 0


def test_salida_de_consulta_es_la_fila_sellada():
    r = b.consulta(texto="ahorro", limite=None)
    assert r["n"] == len(r["respuestas"]) > 0
    _, filas = b.catalogo()
    por_llave = {f["llave"]: f for f in filas}
    for a in r["respuestas"]:
        f = por_llave[a["llave"]]
        assert a["punto"] == float(f["punto"])
        assert a["terminos"] == b.TERMINOS
        assert a["temporalidad"] in ("PROSPECTIVA", "RETROSPECTIVA")
        assert a["oferta"]
        assert a["tipo_ic"] in ("diseno", "calibrado", "ic-con-r", "sin-ic")


def test_segmento_filtra_por_familia_de_eje():
    r = b.consulta(conducta="no_tiene_ahorros_enif2024", segmentos=["nse=bajo"], limite=None)
    assert r["n"] >= 1 and all(a["eje"] == "NSE" and "BAJO" in a["segmento"] for a in r["respuestas"])


def test_no_contesta_con_razon():
    r = b.consulta(conducta="no-existe-esto", limite=None)
    assert r["n"] == 0 and [n["razon"] for n in r["no_contesta"]] == ["SIN-COINCIDENCIA"]
    r = b.consulta(texto="ahorro", segmentos=["religiosidad=alta"])
    assert r["n"] == 0 and r["no_contesta"][0]["razon"] == "EJE-NO-DISPONIBLE"


def test_ola_reservada_se_declara_sin_abrir():
    assert ("ENOE", "2026") in b.olas_reservadas()
    r = b.consulta(texto="empleo", instrumento="ENOE", ola="2026")
    assert "OLA-RESERVADA" in [n["razon"] for n in r["no_contesta"]]


def test_verificar_cadena():
    ok, pasos = b.verificar("RESULT-ENOE-PISOS-TABLA#0")
    assert ok and pasos[-1].startswith("CADENA-VERIFICADA")
    ok, _ = b.verificar("RESULT-NO-EXISTE")
    assert not ok


def test_export_de_pages_es_el_catalogo_vigente():
    ver, filas = b.catalogo()
    p = RAIZ / "docs/data" / f"catalogo-{ver}.json"
    ptr = json.loads((RAIZ / "docs/data/catalogo-vigente.json").read_text(encoding="utf-8"))
    assert ptr == {"catalogo": ver, "archivo": p.name}, "puntero de Pages desfasado"
    assert p.exists(), "falta el export: python3 tools/benchmark.py exporta"
    assert p.stat().st_size < 8_000_000, "export fuera de cota (8 MB)"
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d == json.loads(json.dumps(b.exporta_dict(), ensure_ascii=False)), \
        "export desfasado: python3 tools/benchmark.py exporta"
    cols = d["columnas"]
    assert len(d["filas"]) == len(filas)
    for fila, f in zip(d["filas"], filas):
        v = {c: (d["diccionarios"][c][x] if c in d["diccionarios"] else x) for c, x in zip(cols, fila)}
        llave = v["llave"] or (f"{v['result_id']}#{v['celda']}" if v["celda"].isdigit() else v["result_id"])
        assert llave == f["llave"] and v["punto"] == f["punto"]
        assert math.isfinite(float(v["punto"]))


def test_ejemplos_no_desfasados():
    p = RAIZ / "docs/ejemplos.md"
    assert p.read_text(encoding="utf-8") == b.ejemplos_md(), "python3 tools/benchmark.py ejemplos"
    assert p.read_text(encoding="utf-8").count("CADENA-VERIFICADA") >= 5


def test_segmento_exacto_antes_que_subcadena():
    r = b.consulta(conducta="laboral", segmentos=["escolaridad=superior"], limite=None)
    assert r["n"] >= 1 and all(a["segmento"] == "superior" for a in r["respuestas"])
